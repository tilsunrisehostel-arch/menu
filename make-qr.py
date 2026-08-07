#!/usr/bin/env python3
"""Genera los códigos QR que apuntan al menú y verifica que se puedan leer.

Uso:  python make-qr.py

Si algún día cambias la dirección del menú (por ejemplo a un dominio propio),
cambia MENU_URL aquí abajo, vuelve a ejecutar el script y reimprime el QR.
"""

from __future__ import annotations

import sys
from pathlib import Path

import segno
from PIL import Image, ImageDraw

MENU_URL = "https://tilsunrisehostel-arch.github.io/menu/"

NAVY = "#123a59"
CREAM = "#fff9ef"
PRINT_PX = 2000       # lado aproximado del PNG para imprimir
LOGO_FRACTION = 0.22  # ancho del logo respecto al ancho total del QR

ROOT = Path(__file__).parent
QR_DIR = ROOT / "qr"
QR_DIR.mkdir(exist_ok=True)


def build_qr() -> segno.QRCode:
    # error='h' -> 30% de redundancia, suficiente para tapar el centro con el logo.
    return segno.make(MENU_URL, error="h")


def save_svg(qr: segno.QRCode, path: Path) -> None:
    qr.save(str(path), kind="svg", scale=10, border=4, dark=NAVY, light=CREAM,
            svgclass=None, lineclass=None, omitsize=True)
    print(f"  {path.name}")


def save_png(qr: segno.QRCode, path: Path, with_logo: bool) -> Image.Image:
    modules = qr.symbol_size(scale=1, border=4)[0]
    scale = max(1, round(PRINT_PX / modules))
    qr.save(str(path), kind="png", scale=scale, border=4, dark=NAVY, light=CREAM)

    img = Image.open(path).convert("RGBA")
    if with_logo:
        img = stamp_logo(img)
        img.save(path)
    print(f"  {path.name}  ({img.width}x{img.height}px)")
    return img


def stamp_logo(qr_img: Image.Image) -> Image.Image:
    """Pega el logo en el centro sobre una placa color crema con borde azul."""
    logo_src = ROOT / "assets" / "logo.png"
    if not logo_src.exists():
        print("  (aviso: no se encontró assets/logo.png, se omite el logo)", file=sys.stderr)
        return qr_img

    side = qr_img.width
    plate = round(side * LOGO_FRACTION)
    radius = round(plate * 0.2)

    # Placa crema con un filo azul fino: separa el logo de los módulos del QR.
    card = Image.new("RGBA", (plate, plate), (0, 0, 0, 0))
    d = ImageDraw.Draw(card)
    d.rounded_rectangle([0, 0, plate - 1, plate - 1], radius=radius,
                        fill=CREAM, outline=NAVY, width=max(2, round(plate * 0.035)))

    logo = Image.open(logo_src).convert("RGBA")
    inner = round(plate * 0.68)
    ratio = inner / max(logo.size)
    logo = logo.resize((max(1, round(logo.width * ratio)),
                        max(1, round(logo.height * ratio))), Image.LANCZOS)
    card.alpha_composite(logo, ((plate - logo.width) // 2, (plate - logo.height) // 2))

    out = qr_img.copy()
    out.alpha_composite(card, ((side - plate) // 2, (side - plate) // 2))
    return out


def verify(path: Path, expected: str) -> bool:
    """Lee el QR de vuelta con OpenCV, incluso encogido como se vería de lejos."""
    try:
        import cv2
        import numpy as np
    except ImportError:
        print("  (opencv no disponible: no se pudo verificar automáticamente)", file=sys.stderr)
        return True

    img = Image.open(path).convert("RGB")
    ok_sizes = []
    for size in (1200, 600, 400, 300, 200):
        small = img.resize((size, size), Image.LANCZOS)
        arr = cv2.cvtColor(np.array(small), cv2.COLOR_RGB2BGR)
        data, _, _ = cv2.QRCodeDetector().detectAndDecode(arr)
        if data == expected:
            ok_sizes.append(size)

    if ok_sizes:
        print(f"  OK  {path.name}: decodificado a {min(ok_sizes)}px y {len(ok_sizes)} tamaños")
        return True
    print(f"  FALLO  {path.name}: no se pudo decodificar", file=sys.stderr)
    return False


def main() -> int:
    qr = build_qr()
    print(f"URL: {MENU_URL}")
    print(f"QR versión {qr.version}, corrección de errores {qr.error.upper()}, "
          f"{qr.symbol_size(scale=1, border=0)[0]} módulos\n")

    print("Generando:")
    save_svg(qr, QR_DIR / "til-sunrise-menu-qr.svg")
    save_png(qr, QR_DIR / "til-sunrise-menu-qr-plain.png", with_logo=False)
    save_png(qr, QR_DIR / "til-sunrise-menu-qr.png", with_logo=True)

    print("\nVerificando lectura:")
    ok = all([
        verify(QR_DIR / "til-sunrise-menu-qr-plain.png", MENU_URL),
        verify(QR_DIR / "til-sunrise-menu-qr.png", MENU_URL),
    ])
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
