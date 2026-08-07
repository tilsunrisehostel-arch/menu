#!/usr/bin/env python3
"""Genera las tarjetas imprimibles con el código QR.

Uso:  python make-qr.py && python make-cards.py

Produce dos archivos HTML autocontenidos (el logo y el QR van incrustados,
así que se pueden abrir o enviar por correo sin nada más):

  qr/card-a5.html    -> una tarjeta A5, para el mostrador o la vitrina
  qr/cards-a4.html   -> cuatro tarjetas A6 en una hoja A4, para las mesas

Para imprimir: abre el archivo en el navegador y usa Ctrl+P (Cmd+P en Mac).
Elige "Márgenes: ninguno" y activa "Gráficos de fondo".
"""

from __future__ import annotations

import base64
import re
from pathlib import Path

ROOT = Path(__file__).parent
QR_DIR = ROOT / "qr"

MENU_URL_LABEL = "tilsunrisehostel-arch.github.io/menu"
INSTAGRAM = "@tilsunrisespecialitycoffee"

NAVY = "#123a59"
CREAM = "#fff9ef"
GOLD = "#f6cc4b"
INK = "#45543f"


def data_uri(path: Path, mime: str) -> str:
    return f"data:{mime};base64," + base64.b64encode(path.read_bytes()).decode("ascii")


def qr_svg_inner() -> str:
    """Devuelve el contenido del SVG del QR, sin fondo y sin cabecera XML."""
    svg = (QR_DIR / "til-sunrise-menu-qr.svg").read_text(encoding="utf-8")
    svg = re.sub(r"<\?xml.*?\?>\s*", "", svg, flags=re.S)
    # quitamos el rectángulo de fondo: la tarjeta ya es color crema
    svg = svg.replace(f'<path fill="{CREAM}" d="M0 0h49v49h-49z"/>', "")
    return svg.strip()


CARD_MARKUP = """
      <article class="card">
        <img class="card__logo" src="{logo}" alt="Til Sunrise Specialty Coffee">

        <p class="card__kicker">Café de especialidad · Cali</p>

        <div class="card__qr">
          {qr}
          <img class="card__qrlogo" src="{logo}" alt="">
        </div>

        <p class="card__cta">Escanea para ver el menú</p>
        <p class="card__cta card__cta--en" lang="en">Scan for the menu</p>

        <p class="card__foot">
          <span class="card__ig">{ig}</span>
        </p>
      </article>"""


def font_face() -> str:
    """Incrusta Montserrat para que la tarjeta se imprima igual en cualquier equipo."""
    fonts = ROOT / "assets" / "fonts"
    normal = data_uri(fonts / "montserrat-latin.woff2", "font/woff2")
    italic = data_uri(fonts / "montserrat-italic-latin.woff2", "font/woff2")
    return f"""  @font-face {{
    font-family: 'Montserrat';
    font-style: normal;
    font-weight: 400 800;
    src: url({normal}) format('woff2');
  }}
  @font-face {{
    font-family: 'Montserrat';
    font-style: italic;
    font-weight: 400 500;
    src: url({italic}) format('woff2');
  }}"""


def page(title: str, page_css: str, body: str) -> str:
    return f"""<!doctype html>
<html lang="es">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
{font_face()}

  @page {{ {page_css} margin: 0; }}

  :root {{
    --navy: {NAVY};
    --cream: {CREAM};
    --gold: {GOLD};
    --ink: {INK};
  }}

  * {{ box-sizing: border-box; }}

  html, body {{
    margin: 0;
    padding: 0;
    background: #e9e4da;
    font-family: 'Montserrat', ui-sans-serif, system-ui, -apple-system,
      'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
    color: var(--ink);
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  .sheet {{
    background: var(--cream);
    margin: 0 auto;
    overflow: hidden;
  }}

  .card {{
    position: relative;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    padding: 8mm 6mm;
    background: var(--cream);
    text-align: center;
  }}

  /* marco interior dorado */
  .card::before {{
    content: '';
    position: absolute;
    inset: 3.5mm;
    border: 0.5mm solid var(--gold);
    border-radius: 3mm;
    pointer-events: none;
  }}

  .card__logo {{
    width: var(--logo-w);
    height: auto;
    margin-bottom: 2mm;
  }}

  .card__kicker {{
    margin: 2mm 0 4mm;
    color: var(--navy);
    font-size: var(--kicker-fs);
    font-weight: 600;
    letter-spacing: 0.18em;
    text-indent: 0.18em;
    text-transform: uppercase;
  }}

  .card__qr {{
    position: relative;
    width: var(--qr-w);
    height: var(--qr-w);
  }}
  .card__qr svg {{
    display: block;
    width: 100%;
    height: 100%;
  }}
  .card__qrlogo {{
    position: absolute;
    top: 50%;
    left: 50%;
    width: 21%;
    transform: translate(-50%, -50%);
    padding: 1.4%;
    background: var(--cream);
    border: 0.35mm solid var(--navy);
    border-radius: 1.6mm;
  }}

  .card__cta {{
    margin: 4mm 0 0;
    color: var(--navy);
    font-size: var(--cta-fs);
    font-weight: 800;
    line-height: 1.15;
    letter-spacing: 0.01em;
    text-transform: uppercase;
  }}
  .card__cta--en {{
    margin-top: 1mm;
    color: var(--ink);
    font-size: var(--cta-en-fs);
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: none;
    font-style: italic;
  }}

  .card__foot {{
    margin: 6mm 0 0;
    font-size: var(--foot-fs);
  }}
  .card__ig {{
    display: inline-block;
    padding: 1.6mm 3.4mm;
    border: 0.35mm solid var(--navy);
    border-radius: 20mm;
    color: var(--navy);
    font-weight: 700;
    letter-spacing: 0.02em;
  }}

  @media screen {{
    body {{ padding: 12mm; }}
    .sheet {{ box-shadow: 0 4px 30px rgba(0,0,0,0.18); }}
  }}

{{body_css}}
</style>
</head>
<body>
{body}
</body>
</html>
"""


def build_a5(logo: str, qr: str) -> str:
    body_css = """
  .sheet {
    width: 148mm;
    height: 210mm;
    --logo-w: 34mm;
    --kicker-fs: 7pt;
    --qr-w: 78mm;
    --cta-fs: 15pt;
    --cta-en-fs: 10pt;
    --foot-fs: 8.5pt;
  }
  .sheet .card { padding: 14mm 10mm; }
  .sheet .card::before { inset: 6mm; }
"""
    card = CARD_MARKUP.format(logo=logo, qr=qr, ig=INSTAGRAM)
    body = f'    <div class="sheet">\n{card}\n    </div>'
    return page("Til Sunrise — tarjeta QR A5", "size: A5;", body).replace(
        "{body_css}", body_css
    )


def build_a4_four_up(logo: str, qr: str) -> str:
    body_css = """
  .sheet {
    display: grid;
    grid-template-columns: 105mm 105mm;
    grid-template-rows: 148mm 148mm;
    width: 210mm;
    height: 296mm;
    --logo-w: 24mm;
    --kicker-fs: 5.5pt;
    --qr-w: 55mm;
    --cta-fs: 10.5pt;
    --cta-en-fs: 7.5pt;
    --foot-fs: 6.5pt;
  }
  /* guías de corte */
  .sheet .card { outline: 0.2mm dashed rgba(18,58,89,0.35); outline-offset: -0.1mm; }
"""
    card = CARD_MARKUP.format(logo=logo, qr=qr, ig=INSTAGRAM)
    body = '    <div class="sheet">\n' + ("\n".join([card] * 4)) + "\n    </div>"
    return page("Til Sunrise — 4 tarjetas QR en A4", "size: A4;", body).replace(
        "{body_css}", body_css
    )


def main() -> None:
    logo = data_uri(ROOT / "assets" / "logo.png", "image/png")
    qr = qr_svg_inner()

    targets = {
        "card-a5.html": build_a5(logo, qr),
        "cards-a4.html": build_a4_four_up(logo, qr),
    }
    for name, html in targets.items():
        out = QR_DIR / name
        out.write_text(html, encoding="utf-8")
        print(f"wrote qr/{name}  ({out.stat().st_size:,} bytes)")


if __name__ == "__main__":
    main()
