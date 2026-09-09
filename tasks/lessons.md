# Lecciones

## 2026-09-04 — "Publicar" es parte de "agregar al menú"

**Qué pasó.** Se pidió agregar doce platos a la carta. Se hizo todo —JSON,
build, verificación— y se dejó el commit **solo en local**, preguntando antes
de hacer push porque publicar lo pone frente a clientes reales. La respuesta
fue: *"Is this live? I don't see it."*

**Por qué estuvo mal.** La carta que no está publicada no está agregada. El
push no era un paso extra que hubiera que consultar: era la última parte de lo
que se pidió. Preguntar ahí no protegió de nada, solo dejó el trabajo a medias
y obligó a un viaje de ida y vuelta.

**Regla.** En este repo, "agregar / quitar / cambiar algo del menú" incluye
`git push` y la comprobación de que quedó en vivo. No preguntar por eso.

**Dónde sí hay que parar.** Cuando la instrucción es ambigua *y* las lecturas
posibles cambian lo que se le cobra al cliente. Ejemplo real que sí valió la
pena preguntar: *"add jam and cream cheese toppings to pandebono x4 (13,000)"*
— ¿el x4 sencillo de $10.000 desaparece, o quedan los dos? Ahí preguntar
evitó dejar precios equivocados en vivo. La diferencia con el caso anterior es
que aquí no había forma de deducir la respuesta; en el otro sí.

## 2026-09-03 — Verificar contra la URL en vivo, no contra el archivo local

`python build.py` puede salir perfecto y la página seguir sirviendo la versión
vieja: GitHub Pages tarda 1–2 minutos y además hay caché. Todo cambio de esta
sesión se confirmó haciendo `curl` a la URL pública y comprobando nombres y
precios en los dos idiomas. Vale la pena: es la única prueba de que el huésped
que escanea el QR ve lo que se cambió.
