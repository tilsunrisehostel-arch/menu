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

XREF_CAT = 284
XREF_CUP = 287

# La taza vive en una hoja de sprites junto a otras tazas más pequeñas; solo
# nos interesa la grande, que ocupa esta esquina de la hoja.
CUP_REGION = (0, 100, 500, 500)

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


def placement(page: fitz.Page, xref: int) -> tuple[fitz.Rect, bool]:
    info = next(i for i in page.get_image_info(xrefs=True) if i["xref"] == xref)
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

    # --- gato ---------------------------------------------------------------
    cat = drop_fringe(load_rgba(doc, XREF_CAT))
    cat_content = cat.getbbox()
    cat_box, cat_mirror = placement(page, XREF_CAT)
    cat_on_page = to_page_box(cat_content, cat.size, cat_box, cat_mirror)

    # --- taza ---------------------------------------------------------------
    cup_sheet = drop_fringe(load_rgba(doc, XREF_CUP))
    region = cup_sheet.crop(CUP_REGION)
    rb = region.getbbox()
    cup_content = (rb[0] + CUP_REGION[0], rb[1] + CUP_REGION[1],
                   rb[2] + CUP_REGION[0], rb[3] + CUP_REGION[1])
    cup_box, cup_mirror = placement(page, XREF_CUP)
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
