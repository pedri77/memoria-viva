# F4 · BOE de Burgos (zona sublevada, 1936-1939): estado

**Fecha:** 15-11-2026

## Objetivo

Equilibrar la cronología, que hasta ahora salía casi entera de la Gaceta de la República, con disposiciones de la zona sublevada.

## Vía de acceso y límites

- El `robots.txt` de boe.es prohíbe a agentes automáticos el buscador de la Gazeta (`/buscar/gazeta.php?`) y los PDF (`/datos/pdfs/`). No se ha usado ninguna de las dos rutas.
- Sí están permitidas las fichas de documento `https://www.boe.es/buscar/doc.php?id=BOE-A-AAAA-N`, que existen para el BOE editado en Burgos desde su núm. 1 (2 de octubre de 1936). Cada ficha da el título oficial, el número, la fecha, las páginas y el departamento. **No da el texto**: remite al PDF.
- Por eso las afirmaciones de estos acontecimientos se limitan al **título oficial y a los datos de publicación**. Cada ficha documental lo dice en su revisión y en su campo `text_origin: ninguno`.
- El **Boletín Oficial de la Junta de Defensa Nacional** (25 de julio a 1 de octubre de 1936) no tiene fichas `doc.php`: sigue siendo una laguna (por ejemplo, el decreto de 29 de septiembre de 1936 que nombra a Franco jefe del Gobierno del Estado).

## Método

`scripts/etl/boe_localizar.py` busca los identificadores correlativos de una fecha: usa como anclas las fichas ya consultadas y biseca hasta el día pedido. Después recorre las disposiciones de ese día y marca las que contienen la palabra clave. Hace una petición cada 1,5 s y guarda una caché local, que no se publica.

**Coste real:** unas 1.000 peticiones. Unas 400 se perdieron por un fallo de la primera versión, que recorría uno a uno tramos largos sin fichas en la numeración de 1936; se detectó y se paró. La versión corregida necesitó entre 30 y 120 peticiones por fecha.

Las fichas seleccionadas están en `data/external/boe_burgos/fichas.json`; los documentos y acontecimientos se generan con `scripts/etl/eventos_burgos.py`.

## Incorporado

| Fecha (BOE) | Disposición | Identificador |
|---|---|---|
| 02-10-1936 | Ley de organización administrativa de la nueva estructura del Estado (BOE núm. 1) | BOE-A-1936-9134 |
| 11-11-1936 | Decreto núm. 66, revisión total del personal de Instrucción Pública, y orden de aplicación | BOE-A-1936-9694, 9705 |
| 11-11-1936 | Decreto núm. 67, inscripción de fallecimientos o desapariciones (solo como documento) | BOE-A-1936-9695 |
| 20-04-1937 | Decreto núm. 255, de unificación | BOE-A-1937-3746 |
| 31-01-1938 | Ley de organización de la Administración Central del Estado | BOE-A-1938-1406 |
| 10-03-1938 | Fuero del Trabajo | BOE-A-1938-3093 |
| 24-04-1938 | Ley de Prensa de 22-04-1938 (publicación rectificada) | BOE-A-1938-4796 |
| 23-09-1938 | Ley de reforma de la Enseñanza Media y decreto de Inspección | BOE-A-1938-11039, 11040 |
| 13-02-1939 | Ley de Responsabilidades Políticas | BOE-A-1939-1451 |

La cronología pasa de 23 a 31 acontecimientos; 8 proceden de la zona sublevada. La narrativa de las escuelas incorpora el Decreto núm. 66 en la escena «Maestros en guerra».

## Pendiente

- Leer el texto de estas disposiciones (lectura humana de los PDF o solicitud formal de volcado a la AEBOE) para pasar de afirmaciones de título a afirmaciones de contenido.
- Boletín de la Junta de Defensa Nacional (julio-septiembre de 1936).
- Más disposiciones de 1937-1939 con el mismo método, siempre con un tope de peticiones por sesión.
