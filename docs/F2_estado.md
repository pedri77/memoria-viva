# F2 · MVP web: estado

**Fecha:** 14-11-2026

## Puerta de salida (de `04_roadmap.md`)

| Criterio | Estado |
|---|---|
| Atlas con selector de año 1931-1939, capas provincia / indicador / acontecimientos, enlaces profundos | ✓ `/atlas/` (estado en la URL: `year`, `ind`, `censo`, `munis`, `sel`) |
| Cronología filtrable sincronizada con el atlas | ✓ filtros por año y tipo, enlace «ver en el mapa» por acontecimiento |
| Fichas de lugar, acontecimiento y documento con cita | ✓ 57 fichas de lugar nuevas; las de documento ya tenían «citar» |
| Datos: gráfico con notas de discontinuidad y descarga CSV | ✓ gráfico SVG con el tramo de posguerra en discontinuo; CSV por indicador en `/data/v1/<id>.csv` |
| Búsqueda | ✓ Pagefind (178 páginas indexadas, filtro por tipo de ficha) |
| Vista sin WebGL | ✓ `/atlas/tabla/`: mapa SVG estático generado en el build y tabla filtrable |
| Mapa → acontecimiento → documento original en ≤3 clics | ✓ 2 clics: punto del mapa (o elemento de la lista) → «Abrir el documento original» |
| Lighthouse ≥90 en accesibilidad y rendimiento en las páginas tipo | ✓ accesibilidad 100 en las 8 páginas tipo; rendimiento 98-100 (portada 99, versión sin mapa 98, resto 100). Medido en local sin compresión, perfil móvil |
| axe sin errores críticos | ✓ 0 incidencias en datos y atlas con el panel abierto |
| 3 pruebas informales con usuarios | ✗ pendiente: las tiene que hacer David |

## Pendiente o diferido

- Hoja raster del CNIG georreferenciada: diferida. Requiere elegir hoja y puntos de control a mano; no aporta al MVP.
- Municipios de 1930 enlazados a Wikidata: diferido a F4.
- Sin mapa base de terceros (decisión, no carencia).
- Comprobar en producción (con gzip) que las cifras de Lighthouse se mantienen.
