# F5 · Facsímiles, cronología y datos al pasar el ratón

**Fecha:** 15-11-2026. Peticiones de David: ver los datos al pasar el ratón por los mapas, aplicar el estilo de la portada a otras páginas (como la cronología) e incluir más imágenes.

## Imágenes: facsímiles de los propios documentos

Las imágenes que se añaden son los documentos que el proyecto ya cita, no ilustraciones: la guía editorial §6 prohíbe publicar imágenes generadas como si fueran documentos.
- **Generador:** `scripts/etl/facsimiles.py` crea la primera página de cada número de la Gaceta de Madrid citado y de las tablas del INE con PDF propio: 27 imágenes WebP de 520 px, 1,6 MB en total. Están en `site/public/facsimiles/` y la lista, en `site/src/data/facsimiles.json`.
- **Derechos de la Gaceta:** condiciones de reutilización de la AEBOE (licencia tipo de 27-06-2024). Permiten copiar y difundir citando «Fuente de los datos: Agencia Estatal Boletín Oficial del Estado» con enlace a boe.es.
- **Derechos del INE:** CC BY 4.0.
- **Rutas:** solo la de PDF permitida por robots.txt (`/gazeta/dias/`). Los PDF de las fichas del BOE (`/datos/pdfs/`) están prohibidos, así que esos documentos no tienen facsímil.
- **Dónde salen:** en las fichas de documento y de acontecimiento, y como miniatura en la cronología. Al pulsar la imagen se abre el original.

Siguen pendientes las imágenes de otros archivos (Europeana, AHPCE, Archivo General Militar, etc.) en la fase R2, con revisores, derechos imagen por imagen y el criterio de equilibrio entre bandos.

## Cronología (`/acontecimientos/`)

- Un bloque por año, con el número del año grande y fijo mientras pasan sus acontecimientos (en móvil no se fija).
- Tarjetas con la fecha en texto, el tipo, el título, el inicio de la primera afirmación, la fuente y el facsímil si lo hay.
- Los filtros por año y tipo siguen funcionando y ocultan los años vacíos.
- Las tarjetas aparecen al entrar en pantalla, salvo con movimiento reducido. Sin JavaScript se ven todas.

## Datos al pasar el ratón

- **Atlas:** etiqueta flotante en todas las capas. La prioridad es acontecimiento, luego municipio y luego la capa de fondo.
- **Mapas SVG** de la portada, las historias y la tabla del atlas: una etiqueta común definida en `Base.astro` para cualquier elemento con `data-tip` (los `<title>` se convierten solos). No aparece en pantallas táctiles.

## Verificación

- Compilación sin errores.
- axe sin incidencias en la cronología (modo claro y oscuro), la ficha de la Constitución y `/memoria-hoy/`.
- Capturas a 1440 y 390 px.
- Prueba del ratón en un navegador sin interfaz, en el atlas y en la portada.
