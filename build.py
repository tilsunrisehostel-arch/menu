#!/usr/bin/env python3
"""Genera index.html (español) y en.html (inglés) a partir de menu.json.

Uso:  python build.py

El HTML resultante es estático: no necesita JavaScript para leerse.
Para cambiar precios o platos edita menu.json y vuelve a ejecutar este script.
"""

from __future__ import annotations

import html
import json
from pathlib import Path

ROOT = Path(__file__).parent
SITE_URL = "https://tilsunrisehostel-arch.github.io/menu/"

PAGES = {
    "es": {"file": "index.html", "other": ("en", "en.html", "English")},
    "en": {"file": "en.html", "other": ("es", "index.html", "Español")},
}

STRINGS = {
    "es": {
        "title": "Menú | Til Sunrise Specialty Coffee — Cali, Colombia",
        "description": (
            "Carta de Til Sunrise Specialty Coffee en Cali, Colombia: "
            "café de especialidad, bebidas frías, smoothies y tortas."
        ),
        "skip": "Ir al menú",
        "nav_label": "Secciones del menú",
        "pdf": "Descargar carta en PDF",
        "top": "Volver arriba",
        "art_alt_cup": "",
        "menu_word": "Menú",
    },
    "en": {
        "title": "Menu | Til Sunrise Specialty Coffee — Cali, Colombia",
        "description": (
            "Menu for Til Sunrise Specialty Coffee in Cali, Colombia: "
            "specialty coffee, cold drinks, smoothies and cakes."
        ),
        "skip": "Skip to menu",
        "nav_label": "Menu sections",
        "pdf": "Download menu as PDF",
        "top": "Back to top",
        "art_alt_cup": "",
        "menu_word": "Menu",
    },
}

# Ilustraciones decorativas por sección (extraídas del PDF original).
SECTION_ART = {
    "calientes": ('cup.png', 'section__art--cup'),
    "smoothies": ('cat.png', 'section__art--cat'),
    "tortas": ('leaf-gold.png', 'section__art--leaf'),
}

IG_SVG = (
    '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" '
    'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'
    '<rect x="2" y="2" width="20" height="20" rx="5"/>'
    '<circle cx="12" cy="12" r="4"/><circle cx="17.5" cy="6.5" r="1.1" fill="currentColor" stroke="none"/>'
    "</svg>"
)


def e(text: str) -> str:
    return html.escape(str(text), quote=True)


def price(value: str) -> str:
    return f"${value}"


def render_item(item: dict, lang: str) -> str:
    name = e(item["name"][lang])
    parts = [
        '        <li class="item">',
        f'          <span class="item__name">{name}</span>',
        '          <span class="item__leader" aria-hidden="true"></span>',
        f'          <span class="item__price">{e(price(item["price"]))}</span>',
    ]
    if item.get("desc"):
        parts.append(f'          <p class="item__desc">{e(item["desc"][lang])}</p>')
    parts.append("        </li>")
    return "\n".join(parts)


def render_section(section: dict, lang: str) -> str:
    title = e(section["title"][lang])
    stacked = " items--stacked" if section.get("style") == "stacked" else ""
    out = [
        f'      <section class="section" id="{e(section["id"])}" aria-labelledby="{e(section["id"])}-title">',
    ]

    art = SECTION_ART.get(section["id"])
    if art:
        out.append(
            f'        <img class="art section__art {art[1]}" src="assets/{art[0]}" alt="" '
            'aria-hidden="true" loading="lazy" decoding="async">'
        )

    out += [
        '        <div class="section__head">',
        f'          <h2 class="section__title" id="{e(section["id"])}-title">{title}</h2>',
        "        </div>",
        f'        <ul class="items{stacked}">',
    ]
    out += [render_item(item, lang) for item in section["items"]]
    out.append("        </ul>")

    box = section.get("box")
    if box:
        out += [
            '        <div class="box">',
            f'          <p class="box__title"><span>{e(box["title"][lang])}</span></p>',
            '          <ul class="items">',
        ]
        out += [render_item(item, lang) for item in box["items"]]
        out += ["          </ul>", "        </div>"]

    out.append("      </section>")
    return "\n".join(out)


def render_jsonld(data: dict, lang: str) -> str:
    brand = data["brand"]
    payload = {
        "@context": "https://schema.org",
        "@type": "CafeOrCoffeeShop",
        "name": brand["full"],
        "servesCuisine": "Coffee",
        "address": {"@type": "PostalAddress", "addressLocality": "Cali", "addressCountry": "CO"},
        "sameAs": [f"https://www.instagram.com/{brand['instagram']}/"],
        "hasMenu": {
            "@type": "Menu",
            "inLanguage": lang,
            "hasMenuSection": [
                {
                    "@type": "MenuSection",
                    "name": section["title"][lang],
                    "hasMenuItem": [
                        {
                            "@type": "MenuItem",
                            "name": item["name"][lang],
                            **({"description": item["desc"][lang]} if item.get("desc") else {}),
                            "offers": {
                                "@type": "Offer",
                                "price": item["price"].replace(".", ""),
                                "priceCurrency": "COP",
                            },
                        }
                        for item in section["items"]
                    ],
                }
                for section in data["sections"]
            ],
        },
    }
    return json.dumps(payload, ensure_ascii=False, separators=(",", ":"))


def render_page(data: dict, lang: str) -> str:
    s = STRINGS[lang]
    brand = data["brand"]
    other_lang, other_file, other_label = PAGES[lang]["other"]
    self_file = PAGES[lang]["file"]

    chips = "\n".join(
        f'            <a href="#{e(sec["id"])}">{e(sec["title"][lang])}</a>'
        for sec in data["sections"]
    )
    sections = "\n\n".join(render_section(sec, lang) for sec in data["sections"])

    lang_links = "\n".join(
        [
            f'          <a href="{e(self_file)}" aria-current="true" lang="{lang}">'
            f'{"ES" if lang == "es" else "EN"}</a>',
            f'          <a href="{e(other_file)}" lang="{other_lang}">'
            f'{"EN" if lang == "es" else "ES"}</a>',
        ]
    )

    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{e(s["title"])}</title>
<meta name="description" content="{e(s["description"])}">
<meta name="theme-color" content="#fff9ef" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0b2439" media="(prefers-color-scheme: dark)">
<meta name="color-scheme" content="light dark">

<link rel="canonical" href="{SITE_URL}{'' if lang == 'es' else 'en.html'}">
<link rel="alternate" hreflang="es" href="{SITE_URL}">
<link rel="alternate" hreflang="en" href="{SITE_URL}en.html">
<link rel="alternate" hreflang="x-default" href="{SITE_URL}">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(brand["full"])}">
<meta property="og:title" content="{e(s["title"])}">
<meta property="og:description" content="{e(s["description"])}">
<meta property="og:url" content="{SITE_URL}{'' if lang == 'es' else 'en.html'}">
<meta property="og:image" content="{SITE_URL}assets/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="{'es_CO' if lang == 'es' else 'en_US'}">
<meta name="twitter:card" content="summary_large_image">

<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png">
<link rel="apple-touch-icon" href="assets/apple-touch-icon.png">
<link rel="manifest" href="manifest.webmanifest">

<link rel="preload" href="assets/fonts/montserrat-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="stylesheet" href="assets/menu.css">
<script type="application/ld+json">{render_jsonld(data, lang)}</script>
</head>
<body>
<a class="skip" href="#menu">{e(s["skip"])}</a>

<header class="hero" id="top">
  <img class="art hero__art--tl" src="assets/leaf-navy.png" alt="" aria-hidden="true" decoding="async">
  <img class="art hero__art--tr" src="assets/leaf-gold2.png" alt="" aria-hidden="true" decoding="async">

  <div class="wrap hero__inner">
    <picture>
      <source srcset="assets/logo-dark.png" media="(prefers-color-scheme: dark)">
      <img class="hero__logo" src="assets/logo.png" width="707" height="643"
           alt="{e(brand["full"])}" fetchpriority="high" decoding="async">
    </picture>

    <h1 class="wordmark">{e(s["menu_word"])}
      <span class="wordmark__sub">{e(brand["city"][lang])}</span>
    </h1>

    <p class="star-rule" aria-hidden="true"><span>✦</span></p>

    <div class="tagline">
      <p class="tagline__title">{e(brand["tagline_title"][lang])}</p>
      <p class="tagline__body">{e(brand["tagline_body"][lang])}</p>
    </div>

    <div class="langbar">
      <nav class="langtoggle" aria-label="{'Idioma' if lang == 'es' else 'Language'}">
{lang_links}
      </nav>
    </div>
  </div>
</header>

<nav class="sectionnav" aria-label="{e(s["nav_label"])}">
  <div class="wrap">
    <div class="sectionnav__scroll">
{chips}
    </div>
  </div>
</nav>

<main id="menu">
  <div class="wrap">

{sections}

  </div>
</main>

<footer class="footer">
  <img class="art footer__art" src="assets/leaf-navy.png" alt="" aria-hidden="true" loading="lazy" decoding="async">
  <div class="wrap footer__inner">
    <picture>
      <source srcset="assets/logo-dark.png" media="(prefers-color-scheme: dark)">
      <img class="footer__logo" src="assets/logo.png" width="707" height="643"
           alt="{e(brand["full"])}" loading="lazy" decoding="async">
    </picture>

    <a class="ig" href="https://www.instagram.com/{e(brand["instagram"])}/" rel="noopener">
      {IG_SVG}<span>@{e(brand["instagram"])}</span>
    </a>

    <p class="footer__links">
      <a href="menu.pdf">{e(s["pdf"])}</a>
      <a href="{e(other_file)}" lang="{other_lang}">{e(other_label)}</a>
      <a href="#top">{e(s["top"])}</a>
    </p>

    <p class="footer__note">{e(brand["currency_note"][lang])}</p>
  </div>
</footer>

<script src="assets/menu.js" defer></script>
</body>
</html>
"""


def main() -> None:
    data = json.loads((ROOT / "menu.json").read_text(encoding="utf-8"))
    for lang, cfg in PAGES.items():
        out = ROOT / cfg["file"]
        out.write_text(render_page(data, lang), encoding="utf-8")
        print(f"wrote {out.name}  ({len(out.read_text(encoding='utf-8')):,} bytes)")


if __name__ == "__main__":
    main()
