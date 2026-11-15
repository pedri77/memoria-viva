# Guía editorial

Versión 0.1 · 14-11-2026 · Se aplica a todo objeto de `data/canonical/` y a todo texto publicado en la web.

## 1. Principios

1. **Fuente siempre.** Ningún objeto se publica sin `source_ids`, enlace al custodio y estado de derechos. Lo comprueba `npm run validate`.
2. **Un documento acredita lo que dice, no que sea verdad.** Cada documento lleva `context`: quién lo produjo, para qué y con qué sesgo previsible (propaganda, documentación generada por la represión, prensa de partido, informe oficial).
3. **Cuatro tipos de afirmación** (`claims[].kind`):
   - `documento`: lo que dice un documento concreto. Se redacta como «Según…» o con el acto jurídico («El decreto de… dispone…»).
   - `hecho`: lo acreditado por varias fuentes independientes o por consenso historiográfico. Necesita al menos dos evidencias o una referencia historiográfica.
   - `interpretacion`: lectura historiográfica. Siempre con `attributed_to` (autor y obra).
   - `estimacion`: cifras no observadas directamente. Siempre con `attributed_to`, rango si existe y método.
4. **Sin simetrías artificiales.** La violencia y la represión de los distintos actores se describen según la evidencia: periodo, agente, mecanismo, escala y carácter institucional u organizado. No se igualan fenómenos de naturaleza distinta ni se omite ninguno.
5. **Las lagunas se muestran.** La falta de documentos no prueba la falta de hechos. Si una provincia no tiene datos, se dice y se explica por qué (`missingness_reason`).
6. **Fechas y lugares con su precisión real.** `date_precision` y `spatial_precision` obligatorios. Nunca se inventan coordenadas.

## 2. Vocabulario

Regla: el texto propio usa el término de la columna «Proyecto». Si una fuente usa otro, se cita entre comillas y atribuido.

| Concepto | Proyecto | Términos de época o de parte (solo citados) | Nota |
|---|---|---|---|
| 17-18 de julio de 1936 | golpe de Estado (y sublevación militar) | «Alzamiento Nacional», «Glorioso Movimiento» | El fracaso parcial del golpe da paso a la guerra. |
| Bando que se subleva | bando sublevado, zona sublevada; desde octubre de 1936, también «zona franquista» | «nacionales», «bando nacional» | «Nacional» es autodenominación; se cita entre comillas. |
| Bando que defiende la legalidad | bando republicano, zona republicana | «rojos», «marxistas» (fuentes sublevadas) | Se distinguen Gobierno, partidos, sindicatos y milicias cuando la fuente lo permite. |
| Régimen 1939-1975 | dictadura franquista, franquismo | «Nuevo Estado», «Régimen» | |
| Violencia en retaguardia | violencia política en retaguardia, represión | «terror rojo», «terror blanco», «paseos», «sacas» | «Paseo» y «saca» se usan entre comillas y se explican. |
| Centros de detención irregulares republicanos | checas (entre comillas la primera vez, con explicación) | | |
| Guerra 1936-1939 | Guerra Civil española | «Cruzada», «Guerra de Liberación» | |

La guía se amplía con cada narrativa. Cada término nuevo lleva una referencia historiográfica que justifica su uso.

## 3. Personas y datos personales

- **Se nombra:** a cargos públicos y personas con proyección pública en el ejercicio de su función, cuando consta en una fuente publicada (Gaceta, BOE, Diario de Sesiones, prensa).
- **No se nombra en el MVP:** víctimas, familiares, testigos ni responsables de actos de represión, aunque aparezcan en fuentes públicas. Motivo: Ley 16/1985 art. 57.1.c, LOPDGDD art. 3 y riesgo de confusión por homónimos.
- Nunca se fusionan personas por coincidencia de nombre.
- Las peticiones de retirada por privacidad se atienden primero retirando y después revisando.

## 4. Lugares sensibles

Fosas, lugares de ejecución, centros de detención: como mucho, nivel municipio, con `sensitive: true`. Nunca coordenadas exactas.

## 5. Derechos

| `rights.status` | Qué se puede hacer |
|---|---|
| `public_domain`, `cc0`, `cc_by`, `cc_by_sa` | almacenar y mostrar con atribución |
| `cc_by_nc`, `cc_by_nc_sa` | almacenar y mostrar con atribución mientras el proyecto no tenga uso comercial; lo derivado de un `nc_sa` hereda esa licencia y se indica junto al dato |
| `reuse_open` | almacenar y mostrar con la cita que exija el custodio: condiciones generales de reutilización del sector público (Ley 37/2007) que autorizan expresamente copiar y transformar, como las del SNPSAP (añadido el 15-11-2026) |
| `reuse_conditions` | enlazar y citar; reproducir solo si las condiciones lo permiten expresamente |
| `link_only` | solo enlace |
| `restricted` | solo la referencia, sin enlace a imagen |

Obras de autores fallecidos después de 1946 (carteles, fotografías, artículos firmados) pueden tener derechos vigentes: `link_only` salvo autorización. El validador rechaza `almacenar` o `descargar` con derechos no abiertos.

## 6. IA

- Se puede usar IA para transcribir, extraer entidades o proponer resúmenes, siempre como borrador y con revisión humana antes de `aprobado`.
- Nunca se publica una imagen, voz o testimonio generado como si fuera un documento.
- Toda recreación lleva la etiqueta «Recreación» visible y su expediente de evidencias.

## 7. Revisión y publicación

| `review.status` | Significado | ¿Se publica? |
|---|---|---|
| `borrador` | creado, sin revisar | sí en la fase F0-F1 con aviso; no desde F2 |
| `revision` | en revisión | igual que borrador |
| `aprobado` | revisado contra la fuente | sí |
| `retirado` | retirado por error o petición | no (se mantiene en el historial) |

Las narrativas necesitan dos revisores con formación en historia contemporánea (`reviewers`, mínimo 2, lo exige el esquema).

## 8. Retirada

1. Se cambia `review.status` a `retirado`, con la fecha y el motivo en `review.note` (obligatorio: el validador lo exige).
2. Si otro objeto publicado cita el retirado, la validación falla: hay que corregirlo o retirarlo también.
3. Al compilar, el objeto desaparece de listados, JSON público y búsqueda; su URL muestra un aviso con el motivo, y la retirada figura en el registro de cambios.
4. El historial se conserva en git. Si la retirada es por datos personales sensibles, además se valora reescribir el historial.

Prueba automática: `npm run test:retirada` (también en CI).

## 9. Correcciones

Formulario público (issue de GitHub). Respuesta razonada en el propio issue. Cada corrección es un commit que cita el número del issue. No se publican datos de quien comunica el error.
