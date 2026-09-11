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

## Sesión 2026-09-03 → 2026-09-09

Cuatro despliegues, todos verificados contra la URL en vivo (no contra la copia local).

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

### 4. `32deea4` — cuadrar con la carta impresa

La dueña mandó fotos de la carta diseñada (dos páginas) y pidió que la web
coincidiera. Se transcribieron las dos imágenes tres veces por separado y se
compararon contra `menu.json`; después, otras tres pasadas independientes
(por conteo, por precio y por ingrediente) confirmaron que ya coinciden.

**Calientes:** vuelve `Cappuccino vainilla` $11.000, entran `Aromática` $5.000
e `Infusión de frutas` $7.500, y sale `Chocolate masmelos`.

**Adiciones:** la caja cambia entera — antes almendra y leche regular; ahora
leche de avena $3.000, zumo de limón / michelada $3.000 y adición de licor $8.000.

**Postres:** sale `Torta naranja y amapola`. Los dos cheesecakes de frutas se
juntan en uno solo, `Cheesecake` $17.000. `Torta banano` pasa a `Torta de
banano`. El orden queda como en la carta impresa.

**Amasijos:** la arepa de chontaduro pasa de $10.000 a $15.000, y se agrega una
**segunda** arepa de $18.000 con queso crema y mermelada o arequipe.
`Pandebono canasta x6` pasa a llamarse `Pandebono x6`.

**Desayunos:** `Huevos revueltos con jamón y queso` se parte en nombre
(`Huevos revueltos`) y descripción (`Con jamón y queso`), como en la carta.

Fríos, filtrados, smoothies y sándwiches ya coincidían: no se tocaron.

#### Defectos de la carta impresa (no copiarlos)

- En el bloque de amasijos, la descripción de la arepa **se encima** sobre la
  línea de `PANDEBONO`, y parece un tachado. No lo es: el pandebono de $3.000
  es un producto normal. Es un choque de cajas de texto del diseño.
- `AREPA DE CHONTADURO` aparece **dos veces** y hay cinco precios para cuatro
  filas. Confirmado con la dueña: **son dos arepas distintas**, $15.000 y $18.000.
- El título impreso dice `SÁNDWICHES Y TOSTADOS`; en la web se deja
  `Sándwiches y tostadas`, que es lo correcto para los platos que lista.
- La carta impresa trae varios errores de tildes y comas (`Piña.`, `maracuya`,
  `mani`). La web mantiene la ortografía correcta a propósito.

#### Lo que se decidió NO copiar de la carta impresa

- La **nota de desayunos** se queda, aunque no está impresa: explica el pan, el
  queso crema, la mermelada y la bebida que van incluidos, y es lo que justifica
  el precio de $20.000–$22.000.
- **Postres y Amasijos siguen separados.** La carta impresa los junta en
  `POSTRES Y PANES` por espacio; la web tiene barra de secciones y no lo necesita.
- El **inglés se queda**. La carta impresa es solo en español.

---

## Sesión 2026-09-11 — carta v6 (`Menú Til Sunrise (6).zip`)

La dueña mandó la versión 6 de la carta diseñada (dos PNG de 1448×2000 en un
zip en Descargas). Se leyó tres veces por separado cada página, se votó por
mayoría, se comparó contra la lectura propuesta (cero diferencias) y luego
quince afirmaciones —cada precio cambiado, cada plato que sale, cada orden—
pasaron por tres refutadores independientes cada una. Ninguna cayó.

### Qué cambió respecto a `32deea4`

**Calientes** (15 → 14): sale `Cappuccino vainilla` $11.000. Orden nuevo tal
cual la carta: sencillo, doble, americano, macchiato, latte, cappuccino, flat
white, moccachino, aromática, infusión de frutas, chai, milo, chocolate,
chocolate con queso. La línea *«fresa fresca y hojas de menta»* ahora está
impresa **debajo de Aromática**, e `Infusión de frutas` queda sin descripción;
la web lo copia así (ver «para confirmar con la dueña»).

**Adiciones:** `Leche de avena` → **`Leche vegetal`** («Plant-based milk»).

**Fríos** (11 → 10): sale `Malteada de café` $18.000. `Orange coffee`
$12.000 → **$13.000**. Orden nuevo: cold brew, iced latte, orange coffee,
granizado, limonada, jugos, milo frío, iced chai, lulada, sodas italianas.

**Desayunos** (4 → 5): la `Arepa de chontaduro` $15.000 (suero costeño y
cuajada) **se muda de Amasijos a Desayunos**, de primera. La nota de la sección
sigue diciendo «todos los huevos…», así que no aplica a la arepa: correcto.

**Sándwiches y tostadas:** mismo contenido, orden invertido como en la carta:
napolitana, Sunrise, jamón y queso, pollo al pesto.

**Postres:** `Alfajor con arequipe` $5.000 → **$7.000**. Orden nuevo por precio
ascendente: alfajor arequipe, alfajor chocolate, torta de banano, torta
zanahoria, torta chocolate, tarta de lulo, cheesecake.

**Amasijos** (5 → 3): salen las **dos** arepas (la de $15.000 se fue a
Desayunos; la de $18.000 con queso crema y mermelada o arequipe **ya no
existe**). Quedan los tres pandebonos. Esto cierra el pendiente de «las dos
arepas se llaman igual».

**Orden de secciones:** Postres pasa antes de Amasijos, como en la carta
(«Postres y panes»: primero los postres, luego los panes).

Total en vivo: **49 platos** + 3 adiciones.

### Lo que se decidió NO copiar (misma línea que la sesión anterior)

- `Pandebono x4` $13.000 **conserva** «Acompañado de queso crema y mermelada»
  aunque la carta v6 no lo imprime. Razón: 4 × $3.000 = $12.000 < $13.000, así
  que el precio solo se explica con el acompañamiento, y la dueña lo confirmó
  el 2026-09-04. Si un día el x4 vuelve a ser sencillo, hay que quitar la
  descripción *y* revisar el precio.
- La nota de desayunos, la separación Postres / Amasijos, el inglés, y la
  ortografía correcta (`Piña,` no `Piña.`; `maní`; `maracuyá`; `Infusión` con
  tilde y no `Infusiòn`; «tostadas» y no «tostados»).

### Para confirmar con la dueña

- **¿A quién pertenece «fresa fresca y hojas de menta»?** En la v5 estaba bajo
  `Infusión de frutas` («Aromática a elección, fresa fresca y hojas de menta»).
  En la v6 está impresa bajo `Aromática` $5.000 y la infusión de $7.500 quedó
  sin descripción. La web copia la v6. Si fue un corrimiento del diseñador,
  mover el `desc` de `Aromática` a `Infusión de frutas` en `menu.json` es un
  cambio de una línea.

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

- [x] ~~Frutas de los cheesecakes~~ — resuelto por la carta impresa: ya no son dos
      cheesecakes de frutas sino **uno solo**, `Cheesecake` $17.000, sin sabor
      especificado. Si algún día vuelven los sabores, habrá que preguntar qué
      frutas llevan antes de describirlos.
- [x] ~~Las dos arepas se llaman igual~~ — resuelto por la carta v6: la de
      $18.000 desapareció y la de $15.000 pasó a Desayunos.
- [ ] **Aromática vs. Infusión de frutas:** confirmar con la dueña a cuál de las
      dos pertenece «fresa fresca y hojas de menta» (ver sesión 2026-09-11).
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

Estado: 8 secciones, 49 platos + 3 adiciones, bilingüe ES/EN, cuadrada
con la carta impresa v6 (Menú Til Sunrise (6).zip, 2026-09-11). El historial
completo y las decisiones de traducción están en tasks/todo.md de ese repo:
léelo antes de tocar nada, sobre todo la tabla de decisiones, para no
deshacer sin querer cosas como "Huevos rancheros" o las glosas solo-en-inglés.

Convenciones que hay que respetar: nombres en minúscula tipo oración; precios
como cadena "15.000" (build.py agrega el $); descripciones largas terminan en
punto; una descripción puede existir en un solo idioma cuando la glosa solo
hace falta para extranjeros.

Pendiente principal: confirmar con la dueña si «fresa fresca y hojas de
menta» va con Aromática ($5.000, como está impreso en la v6 y en la web) o con
Infusión de frutas ($7.500, como estaba en la v5). No cambiarlo sin preguntar.

Tarea de hoy: <describir aquí>

Criterio de terminado: cambio verificado contra la URL EN VIVO (no la copia
local) con curl, en ambos idiomas, precios incluidos.
```
