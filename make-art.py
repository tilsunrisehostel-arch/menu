#!/usr/bin/env python3
"""Extrae las ilustraciones del PDF original de la carta.

Uso:  python make-art.py

Lo importante es `assets/cat-and-cup.png`: el gato y la taza en una sola
imagen, colocados exactamente como están en la carta impresa.

La posición no se decide a ojo. El PDF guarda, para cada imagen, una matriz
que dice dónde y con qué tamaño va dibujada; ahí también se ve que las dos
ilustraciones van con espejo horizontal (la escala en x es negativa, que es
la razón de que el gato mire hacia la taza). Este script lee esas matrices,
calcula la posición real de cada dibujo sobre la página y reproduce esa misma
composición. Así el gato y la taza quedan a la distancia correcta y no se
recorta ningún grano de café.
"""

from __future__ import annotations

from pathlib import Path

import fitz
from PIL import Image

ROOT = Path(__file__).parent
PDF = ROOT / "menu.pdf"
ASSETS = ROOT / "assets"

# La taza vive en una hoja de sprites junto a otras tazas más pequeñas; solo
# nos interesa la grande, que ocupa esta esquina de la hoja. Se guarda como
# fracción del sprite para que siga valiendo si cambia su resolución.
CUP_REGION_FRAC = (0.0, 0.15625, 0.625, 0.78125)

FRINGE = 32          # alfa por debajo de esto es halo de recorte, se elimina
SCENE_WIDTH = 400    # ancho final en píxeles; deja al gato a tamaño nativo


def load_rgba(doc: fitz.Document, xref: int) -> Image.Image:
    """Rasteriza una imagen del PDF incluyendo su máscara de transparencia."""
    info = next(i for i in doc[0].get_images(full=True) if i[0] == xref)
    pix = fitz.Pixmap(doc, xref)
    if info[1]:
        pix = fitz.Pixmap(pix, fitz.Pixmap(doc, info[1]))
    mode = "RGBA" if pix.alpha else "RGB"
    return Image.frombytes(mode, (pix.width, pix.height), pix.samples).convert("RGBA")


def drop_fringe(img: Image.Image) -> Image.Image:
    px = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = px[x, y]
            if a < FRINGE:
                px[x, y] = (r, g, b, 0)
    return img


def find_cat_and_cup(page: fitz.Page) -> tuple[dict, dict]:
    """Localiza el gato y la taza sin depender del número interno de la imagen.

    Las hojas decorativas se dibujan a sangre: su marco arranca fuera de la
    página, con coordenadas negativas. El gato y la taza son las únicas dos que
    empiezan dentro de la hoja (aunque el gato asome un poco por la derecha).
    Entre esas dos, el gato es el alto y la taza la ancha. Con eso basta para
    reconocerlas aunque el PDF se vuelva a exportar y cambien de numeración.
    """
    inside = []
    seen = set()
    for info in page.get_image_info(xrefs=True):
        if info["xref"] in seen:
            continue
        seen.add(info["xref"])
        box = fitz.Rect(info["bbox"])
        if box.x0 >= page.rect.x0 and box.y0 >= page.rect.y0:
            inside.append(info)

    if len(inside) != 2:
        raise SystemExit(
            f"Se esperaban 2 ilustraciones dentro de la página y se encontraron {len(inside)}. "
            "Revisa make-art.py si el PDF cambió de estructura."
        )

    inside.sort(key=lambda i: fitz.Rect(i["bbox"]).height / fitz.Rect(i["bbox"]).width)
    cup, cat = inside          # la taza es la más achatada, el gato el más alto
    return cat, cup


def placement(info: dict) -> tuple[fitz.Rect, bool]:
    return fitz.Rect(info["bbox"]), info["transform"][0] < 0


def to_page_box(content: tuple[int, int, int, int], sprite: tuple[int, int],
                box: fitz.Rect, mirrored: bool) -> tuple[float, float, float, float]:
    """Convierte un recorte en píxeles del sprite a coordenadas de la página."""
    x0, y0, x1, y1 = content
    sw, sh = sprite

    def px_to_x(px: float) -> float:
        u = px / sw
        return box.x1 - u * box.width if mirrored else box.x0 + u * box.width

    left, right = sorted((px_to_x(x0), px_to_x(x1)))
    top = box.y0 + (y0 / sh) * box.height
    bottom = box.y0 + (y1 / sh) * box.height
    return left, top, right, bottom


def main() -> None:
    doc = fitz.open(PDF)
    page = doc[0]
    cat_info, cup_info = find_cat_and_cup(page)
    print(f"ilustraciones encontradas: gato xref {cat_info['xref']}, taza xref {cup_info['xref']}")

    # --- gato ---------------------------------------------------------------
    cat = drop_fringe(load_rgba(doc, cat_info["xref"]))
    cat_content = cat.getbbox()
    cat_box, cat_mirror = placement(cat_info)
    cat_on_page = to_page_box(cat_content, cat.size, cat_box, cat_mirror)

    # --- taza ---------------------------------------------------------------
    cup_sheet = drop_fringe(load_rgba(doc, cup_info["xref"]))
    cw, ch = cup_sheet.size
    region_box = (round(CUP_REGION_FRAC[0] * cw), round(CUP_REGION_FRAC[1] * ch),
                  round(CUP_REGION_FRAC[2] * cw), round(CUP_REGION_FRAC[3] * ch))
    rb = cup_sheet.crop(region_box).getbbox()
    cup_content = (rb[0] + region_box[0], rb[1] + region_box[1],
                   rb[2] + region_box[0], rb[3] + region_box[1])
    cup_box, cup_mirror = placement(cup_info)
    cup_on_page = to_page_box(cup_content, cup_sheet.size, cup_box, cup_mirror)

    print(f"gato: recorte {cat_content} -> pagina "
          f"({cat_on_page[0]:.1f}, {cat_on_page[1]:.1f})-({cat_on_page[2]:.1f}, {cat_on_page[3]:.1f})"
          f"  espejo={cat_mirror}")
    print(f"taza: recorte {cup_content} -> pagina "
          f"({cup_on_page[0]:.1f}, {cup_on_page[1]:.1f})-({cup_on_page[2]:.1f}, {cup_on_page[3]:.1f})"
          f"  espejo={cup_mirror}")

    # --- escena completa ----------------------------------------------------
    left = min(cat_on_page[0], cup_on_page[0])
    top = min(cat_on_page[1], cup_on_page[1])
    right = max(cat_on_page[2], cup_on_page[2])
    bottom = max(cat_on_page[3], cup_on_page[3])
    scale = SCENE_WIDTH / (right - left)
    scene = Image.new("RGBA",
                      (SCENE_WIDTH, round((bottom - top) * scale)), (0, 0, 0, 0))
    print(f"escena: {right - left:.1f}x{bottom - top:.1f} pt -> {scene.size} px")

    overlap = cup_on_page[2] - cat_on_page[0]
    print(f"la taza y el gato se solapan {overlap:.1f} pt en horizontal")

    def paste(src: Image.Image, content, on_page, z_note: str) -> None:
        piece = src.crop(content)
        if (on_page is cat_on_page and cat_mirror) or (on_page is cup_on_page and cup_mirror):
            piece = piece.transpose(Image.FLIP_LEFT_RIGHT)
        w = max(1, round((on_page[2] - on_page[0]) * scale))
        h = max(1, round((on_page[3] - on_page[1]) * scale))
        piece = piece.resize((w, h), Image.LANCZOS)
        scene.alpha_composite(piece, (round((on_page[0] - left) * scale),
                                      round((on_page[1] - top) * scale)))
        print(f"  {z_note}: {piece.size} px")

    # el gato va detrás, la taza delante — igual que en la carta
    paste(cat, cat_content, cat_on_page, "gato")
    paste(cup_sheet, cup_content, cup_on_page, "taza")

    out = ASSETS / "cat-and-cup.png"
    scene.save(out)
    print(f"\nescrito {out.relative_to(ROOT)}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
