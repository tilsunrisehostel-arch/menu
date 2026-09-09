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

### 4. `PENDIENTE-HASH` — cuadrar con la carta impresa

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
- [ ] **Las dos arepas se llaman igual.** `Arepa de chontaduro` aparece dos veces
      ($15.000 y $18.000) y solo las distingue la descripción, tal cual la carta
      impresa. Si confunde a los huéspedes, vale la pena ponerle un nombre propio
      a la de $18.000.
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

Estado: 8 secciones, 52 platos + 3 adiciones, bilingüe ES/EN, cuadrada
con la carta impresa que tiene la dueña. El historial
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
