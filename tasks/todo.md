# Til Sunrise — menú digital · registro de trabajo

**Repo:** `C:/Users/claws/OneDrive/Desktop/mom/til-sunrise-menu`
→ `github.com/tilsunrisehostel-arch/menu` → GitHub Pages
**En vivo:** https://tilsunrisehostel-arch.github.io/menu/ · [EN](https://tilsunrisehostel-arch.github.io/menu/en.html)

> Ojo: este proyecto **no** es el mismo que `Desktop/til_sunrise` (el sitio del
> hostal en Next.js) ni `Desktop/til-sunrise-admin`. La carta QR vive en `mom/`.

---

## Cómo se edita (resumen)

```
1. editar menu.json          <- única fuente de verdad
2. python build.py           <- regenera index.html y en.html
3. git add -A && git commit -m "..." && git push
```

GitHub Pages publica en 1–2 minutos. **El QR impreso nunca cambia:** apunta a una
dirección fija, así que cambiar precios o platos no obliga a reimprimir nada.

Requisitos: Python 3 con `segno` y `pillow` (ya instalados en esta máquina).

---

## Sesión 2026-09-03 → 2026-09-08

Tres despliegues, todos verificados contra la URL en vivo (no contra la copia local).

### 1. `946e5e4` — comida: desayunos, sándwiches y tostadas, amasijos

Doce platos nuevos en tres secciones. Orden final de la carta:

`Calientes → Fríos → Filtrados → Smoothies → Desayunos → Sándwiches y tostadas → Amasijos → Postres`

(bebidas → comida → postre; los smoothies se quedan con las bebidas en vez de
quedar sueltos detrás del bloque de comida)

Hizo falta tocar `build.py` y `assets/menu.css` para dos cosas que no existían:

- **`"note"` de sección.** Los desayunos comparten una aclaración —el pan, el queso
  crema, la mermelada y la bebida incluidos— que no cabía en la descripción de cada
  plato. Se renderiza entre el título y la lista, con estilo propio en claro, oscuro
  e impresión, y además sale como `description` en los datos estructurados.
- **Descripción en un solo idioma.** A un colombiano no hay que explicarle qué es un
  pandebono; a un viajero sí. Antes eso dejaba un `<p>` vacío en la otra página.

Ambas cosas quedaron documentadas en el README para quien edite después.

### 2. `a1beaf6` — fuera el enlace al PDF

El pie enlazaba `menu.pdf`, que es la carta vieja: sin desayunos, sin sándwiches,
sin amasijos. Un huésped que lo abría veía una carta que contradecía la página.

El archivo **se queda** en el repo porque `make-art.py` saca de ahí las
ilustraciones (el gato, la taza, las hojas). Solo desapareció el enlace y los
textos "Descargar carta en PDF" / "Download menu as PDF", ya sin uso.

### 3. `64be411` — postres nuevos y ajustes

- Fuera `Cappuccino vainilla` (Calientes queda en 13).
- Postres pasa de 5 a 9, reagrupados por tipo (tortas → cheesecakes y tarta →
  alfajores) en vez de apilar lo nuevo al final:
  torta banano $8.000 · cheesecake frutos amarillos $15.000 ·
  cheesecake frutos rojos $15.000 · tarta de lulo $15.000
- `Pandebono x4`: $10.000 → **$13.000**, ahora con queso crema y mermelada.
  **Ya no hay versión sencilla de cuatro** (decisión confirmada con la dueña).

Total en vivo: **51 platos** + 2 adiciones.

---

## Decisiones de traducción (para no deshacerlas sin querer)

| Caso | Qué se hizo | Por qué |
|---|---|---|
| `Huevos rancheros` | Nombre igual en inglés, con descripción "scrambled with Colombian ranchera sausage" | El plato mexicano del mismo nombre son huevos fritos con tortilla y salsa. Quien lo conozca ve enseguida que no es ese. |
| `Huevos pericos` | Se queda en español + descripción | Igual que `Lulada`: no es un falso amigo, solo desconocido. |
| `chontaduro`, `pandebono`, `lulo` | Glosa **solo en inglés** | Fuera de Colombia nadie los conoce; en español explicarlos sobra. |
| `arequipe` | "dulce de leche" | Ya se traducía así en `Alfajor con arequipe`. |
| `rúgula` | "arugula" | Más legible que "rocket" para huéspedes internacionales. |
| `Tostada napolitana` | Minúscula en "napolitana" | Igual que `Sodas italianas`, que ya existía. |
| `Torta banano` | Sin "de" | Como `Torta chocolate` y `Torta zanahoria`. Revisado por hablante nativo: suena bien. |
| `Tarta de lulo` | Con "de", y "tarta" no "torta" | Es tarta, no torta. La carta ya distingue categorías (`Cheesecake de…`, `Alfajor…`). |

---

## Pendiente

- [ ] **Frutas de los cheesecakes.** "Cheesecake de frutos amarillos / rojos" no le
      dice nada a un extranjero. No se le puso descripción porque **no sabemos qué
      frutas llevan** e inventarlas en una carta en vivo sería mentir. En cuanto la
      dueña las diga, se agrega descripción a los dos.
      (Nota: `Sodas italianas` ya usa "frutos rojos, amarillos" sin explicar, así
      que al menos es coherente.)
- [ ] **`menu.pdf` desactualizado.** Ya no se enlaza, pero sigue siendo la carta
      vieja. Si algún día se quiere volver a ofrecer un PDF, hay que regenerarlo
      con la carta actual.
- [ ] **`assets/og.png`** (la imagen que se ve al compartir por WhatsApp) no se
      tocó. Sigue siendo válida, pero ya no representa toda la carta.

---

## Para retomar en otra sesión

Prompt autocontenido, listo para pegar:

```
Trabajo en la carta digital QR de Til Sunrise Specialty Coffee (Cali, Colombia).

Repo: C:/Users/claws/OneDrive/Desktop/mom/til-sunrise-menu
  -> github.com/tilsunrisehostel-arch/menu -> GitHub Pages
En vivo: https://tilsunrisehostel-arch.github.io/menu/  (inglés: /en.html)
OJO: no confundir con Desktop/til_sunrise (sitio Next.js del hostal) ni
con Desktop/til-sunrise-admin. La carta QR está en mom/.

Cómo se edita: menu.json es la única fuente de verdad -> `python build.py`
regenera index.html y en.html -> commit y push -> Pages publica en 1-2 min.
El QR impreso apunta a una URL fija: cambiar precios NO obliga a reimprimir.

Estado: 8 secciones, 51 platos + 2 adiciones, bilingüe ES/EN. El historial
completo y las decisiones de traducción están en tasks/todo.md de ese repo:
léelo antes de tocar nada, sobre todo la tabla de decisiones, para no
deshacer sin querer cosas como "Huevos rancheros" o las glosas solo-en-inglés.

Convenciones que hay que respetar: nombres en minúscula tipo oración; precios
como cadena "15.000" (build.py agrega el $); descripciones largas terminan en
punto; una descripción puede existir en un solo idioma cuando la glosa solo
hace falta para extranjeros.

Pendiente principal: la dueña tiene que decir qué frutas llevan el cheesecake
de frutos amarillos y el de frutos rojos, para poder describirlos. No
inventarlas.

Tarea de hoy: <describir aquí>

Criterio de terminado: cambio verificado contra la URL EN VIVO (no la copia
local) con curl, en ambos idiomas, precios incluidos.
```
