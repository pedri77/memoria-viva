# 04 · Roadmap de construcción

Proyecto personal, un autor. Sin fechas cerradas: cada fase termina cuando se cumple su puerta, no en un plazo. Los esfuerzos son orientativos.

## F0 · Fundamentos (≈1-2 semanas)

**Entregables**
- Repo `pedri77/memoria-viva` con la estructura de `02_stack.md`, LICENSE (MIT) y LICENSE-contenido (CC BY-SA 4.0).
- JSON Schema de `source`, `document`, `event`, `place`, `indicator`, `observation`, `claim`, `story`.
- `docs/guia_editorial.md`: reglas transversales, guía de vocabulario (R17), política de datos personales (sin nombres en el MVP) y procedimiento de corrección y retirada.
- CI: validación de esquemas y comprobador de enlaces.
- Astro con una página de metodología vacía publicada en GitHub Pages.

**Puerta:** CI en verde con 3 objetos de ejemplo; la web de metodología está publicada; guía editorial leída por al menos 1 revisor externo.

## F1 · Datos de referencia 1931-1939 (≈3-4 semanas)

**Entregables**
- `place`: 50 provincias del periodo con geometría (base actual + nota sobre Canarias 1927) y municipios del censo de 1930 enlazados a Wikidata.
- `indicator` + `observation`: 3 series de F010 por provincia (población de hecho 1920/1930/1940, densidad y tasa de alfabetización si el censo la da), transcritas a mano con doble comprobación.
- `event`: 20 acontecimientos 1931-1939, cada uno con al menos una disposición de la Gazeta (F015) o una ficha PARES (F001), con `date_precision`.
- `document`: 100 fichas (prensa de F007 vía datos.gob.es, Gazeta, PARES y CNIG), todas con `rights.status`.
- 1 hoja raster histórica del CNIG georreferenciada, con el error medio declarado.

**Puerta:** 100 % de objetos con fuente y derechos (lo comprueba CI); muestra de 20 objetos revisada sin errores de fecha ni enlace; `scripts/checks/validar_citas.py` en verde.

## F2 · MVP web (≈3-4 semanas)

**Entregables**
- Atlas: MapLibre + PMTiles, selector de año 1931-1939, capas provincias / indicador / eventos, enlaces profundos (`?year=&place=&layers=`).
- Cronología filtrable sincronizada con el atlas.
- Fichas de lugar, evento y documento (páginas estáticas con «citar este recurso»).
- Datos: gráfico ECharts por indicador con notas de discontinuidad y descarga CSV.
- Búsqueda con Pagefind.
- Vista sin WebGL: tabla filtrable y mapa SVG por provincias (R13).

**Puerta:** mapa → evento → documento original en ≤3 clics; Lighthouse ≥90 en accesibilidad y rendimiento en las 4 páginas tipo; axe sin errores críticos; 3 pruebas informales con usuarios anotadas.

## F3 · Primera narrativa y publicación (≈2-3 semanas)

**Entregables**
- 1 narrativa con scroll (tema propuesto: «Las escuelas de la República 1931-1936», documentable con Gazeta, censos y prensa de dominio público, y menos sensible para empezar).
- Formulario de corrección (issue de GitHub con plantilla) y changelog público.
- Anuncio y difusión.

**Puerta:** narrativa revisada por 2 personas con formación en historia contemporánea; cada afirmación enlazada a una evidencia; prueba de retirada de un objeto hecha de principio a fin.

## F4 · Ampliaciones (cada una con su propia puerta)

| Ampliación | Condición previa |
|---|---|
| Más narrativas (hasta 5) | revisores disponibles para cada una |
| Periodo 1939-1975 | F1 replicado para el nuevo periodo |
| Capa electoral 1931-1933-1936 | verificar F031 y derechos de los estudios usados |
| Imágenes vía Europeana | clave API y derechos por objeto |
| Personas | ADR-007 resuelto con asesoría jurídica |
| Asistente con citas (RAG local) | corpus publicado y evaluación de 100 preguntas sin citas inventadas |
| 3D | expediente de evidencias por escena |
| Backend (PostGIS + FastAPI) | se cumple un criterio de escalado de `02_stack.md` |

## Riesgos principales

| Riesgo | Mitigación |
|---|---|
| Carga editorial en solitario | piloto pequeño, revisores voluntarios por narrativa, publicar solo lo revisado |
| Derechos de imágenes | enlazar por defecto; imagen solo con `public_domain` o `cc_by` registrado |
| Polémica política | guía de vocabulario, atribución de interpretaciones, fuentes de ambos bandos contextualizadas, changelog público |
| Datos personales | ningún nombre de víctima o responsable en el MVP |
| Fuentes que cambian o caen | comprobador de enlaces semanal en Actions; fecha de consulta en cada ficha |
| Transcripción de censos con errores | doble transcripción y comparación automática de totales |
