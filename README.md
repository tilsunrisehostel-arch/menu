# Menú digital — Til Sunrise Specialty Coffee

Carta de Til Sunrise Specialty Coffee (Cali, Colombia) publicada como página web,
con códigos QR listos para imprimir.

**Menú en vivo:** https://tilsunrisehostel-arch.github.io/menu/
**English:** https://tilsunrisehostel-arch.github.io/menu/en.html

El QR apunta siempre a esa dirección. Si cambias un precio aquí, el QR impreso
sigue funcionando: **no hay que reimprimir nada.**

---

## Cambiar precios o platos

1. Abre `menu.json` y edita lo que necesites.
2. Ejecuta `python build.py`.
3. Sube los cambios: `git add -A && git commit -m "actualizar precios" && git push`.

En un par de minutos la página web queda actualizada.

> ¿Solo un precio y con prisa? También puedes editar `index.html` y `en.html`
> directamente en GitHub. Pero recuerda copiar el cambio a `menu.json`, porque
> la próxima vez que alguien ejecute `build.py` se regeneran desde ahí.

### Dos detalles útiles al editar `menu.json`

**Nota de sección.** Una sección puede llevar una línea que aplica a todos sus platos
—como la de Desayunos, que explica qué acompaña a todos los huevos. Se escribe así,
al mismo nivel que `"items"`:

```json
"note": { "es": "Todos los huevos vienen...", "en": "All egg dishes come with..." }
```

**Descripción en un solo idioma.** A veces una aclaración solo hace falta en inglés:
un colombiano no necesita que le expliquen qué es un pandebono, pero un viajero sí.
En ese caso basta con poner el idioma que hace falta y la otra página simplemente
no muestra nada:

```json
"desc": { "en": "Colombian cheese bread." }
```

## Imprimir los códigos QR

En la carpeta `qr/` ya están listos:

| Archivo | Para qué sirve |
|---|---|
| `card-a5.pdf` | Una tarjeta grande A5 — mostrador, vitrina, entrada |
| `cards-a4.pdf` | Cuatro tarjetas A6 en una hoja A4, con guías de corte — mesas |
| `til-sunrise-menu-qr.png` | QR suelto con el logo, 2000 px — redes, flyers, empaques |
| `til-sunrise-menu-qr-plain.png` | QR suelto sin logo — máxima compatibilidad |
| `til-sunrise-menu-qr.svg` | QR vectorial — para imprenta, escala sin perder calidad |
| `card-a5.html`, `cards-a4.html` | Las tarjetas en HTML por si quieres reimprimir o ajustar |

Para imprimir desde el HTML: ábrelo en el navegador, `Ctrl+P` (`Cmd+P` en Mac),
elige **Márgenes: ninguno** y activa **Gráficos de fondo**.

### Tamaño mínimo al imprimir

El QR mide 78 mm en la tarjeta A5 y 55 mm en las de mesa. No lo imprimas a menos
de **25 mm** de lado o algunos teléfonos tendrán problemas para leerlo.

## Si algún día cambias de dirección web

Por ejemplo, a un dominio propio tipo `menu.tilsunrise.co`:

1. Cambia `MENU_URL` en `make-qr.py` y `SITE_URL` en `build.py`.
2. Ejecuta `python make-qr.py && python make-cards.py && python build.py`.
3. Reimprime las tarjetas.

`make-qr.py` verifica solo que el QR generado se pueda leer, y avisa si algo falla.

---

## Estructura

```
menu.json          <- fuente de verdad: platos, precios y traducciones
build.py           <- genera index.html (ES) y en.html (EN)
make-qr.py         <- genera y verifica los códigos QR
make-cards.py      <- genera las tarjetas imprimibles
index.html         <- menú en español   (generado)
en.html            <- menú en inglés    (generado)
menu.pdf           <- la carta original en PDF; ya no se enlaza desde la web,
                      pero make-art.py saca de ahí las ilustraciones
assets/            <- estilos, fuentes, logo e ilustraciones
qr/                <- códigos QR y tarjetas para imprimir
```

El gato y la taza aparecen juntos en la cabecera, delante de un sol naciente —
la misma pareja que ya venía dibujada en el PDF original.

`assets/og.html` es la plantilla de la imagen que se ve al compartir el enlace
por WhatsApp o Instagram. Si la cambias, ábrela servida por HTTP, captura el
recuadro de 1200x630 y guárdala como `assets/og.png`.

Las ilustraciones (gato, taza, hojas) y el logo se extrajeron del PDF original de
la carta. Las fuentes Montserrat están incluidas en el repositorio (licencia SIL
Open Font License), así que la página carga rápido y no depende de servicios externos.

## Requisitos para regenerar

Python 3 con `segno` y `pillow`:

```
pip install segno pillow
```

Para que `make-qr.py` verifique la lectura del QR, opcionalmente: `pip install opencv-python`.
