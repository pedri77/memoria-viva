# F1 · Datos de referencia 1931-1939: estado

**Fecha:** 14-11-2026

## Puerta de salida (de `04_roadmap.md`)

| Criterio | Estado |
|---|---|
| 100 % de objetos con fuente y derechos (CI) | ✓ `npm run validate` en verde |
| 50 provincias con geometría | ✓ 50 provincias + Ceuta y Melilla, límites de 1930 (mapSpainHist, CC BY 4.0) |
| 3 series censales por provincia | ✓ población de hecho, población de derecho y densidad; censos 1920, 1930 y 1940 |
| 20 acontecimientos con `date_precision` y evidencia | ✓ 20 (16 con la Gaceta, 3 con Gogora, 1 de F0) |
| 100 fichas documentales con derechos | ✓ 100 (13 Gaceta, 84 cabeceras BNE, 3 conjuntos de datos) |
| Muestra de 20 objetos revisada sin errores | ◐ las 13 fichas de la Gaceta y sus 17 acontecimientos se comprobaron sobre el PDF; falta la segunda revisión humana |
| 1 hoja raster del CNIG georreferenciada | ✗ pendiente (pasa a F2 junto con el mapa) |
| Municipios de 1930 enlazados a Wikidata | ✗ pendiente; solo los municipios usados en acontecimientos tienen ficha |

## Qué se ha verificado y cómo

- **Censos (mapSpainHist):** Agaete, Madrid y Teruel en 1920, 1930 y 1940 coinciden exactamente con la aplicación del INE «Alteraciones de los municipios». La superficie total calculada (506.673 km²) difiere menos del 0,2 % de la oficial.
- **Gaceta:** número, páginas impresas y fecha de firma leídos en cada PDF (`scripts/etl/pdf_buscar.py`). Cuando la fecha de firma no se pudo leer, el acontecimiento se fecha por la publicación y el texto lo dice.
- **Gogora:** las afirmaciones parafrasean la base de datos y las cifras de víctimas van como estimaciones atribuidas. En Gernika se avisa de que la cifra está en debate historiográfico.

## Sesgos que hay que mostrar en la web

- **Prensa:** la BNE solo ofrece texto completo en dominio público. Faltan ABC, Ya, Informaciones, Mundo Obrero, La Vanguardia y Arriba España. 61 de las 84 cabeceras son de Madrid.
- **Bombardeos:** solo Euskadi tiene una base abierta con este detalle. Su ausencia en otras regiones no significa que no hubiera bombardeos.
- **Acontecimientos:** 16 de 20 proceden de la Gaceta de la República, porque el BOE de Burgos no se puede consultar de forma automática. Faltan las disposiciones de la zona sublevada: se compensará con búsqueda manual o con la solicitud a la AEBOE.

## Fuentes de datos añadidas al repositorio (licencia abierta)

| Fichero | Fuente | Licencia |
|---|---|---|
| `data/external/bne/hemeroteca_fulltext_2026-11-14.csv` | BNE, datos.gob.es | CC BY 4.0 |
| `data/external/mapspainhist/*` | Vall-Prat, Zenodo 10.5281/zenodo.23663208 | CC BY 4.0 |
| `data/external/madrid/publicaciones_periodicas_guerra_civil.csv` | Ayuntamiento de Madrid, datos.madrid.es | CC BY 4.0 |
| (no incluido) | Gogora, Open Data Euskadi | por verificar: fuera del repositorio, solo paráfrasis y enlace |

## Siguiente

1. Segunda revisión humana de las 13 fichas de la Gaceta y sus acontecimientos.
2. Buscar a mano en la Gazeta 4-6 disposiciones de la zona sublevada (BOE de Burgos) para equilibrar la cronología.
3. F2: atlas con MapLibre y PMTiles (provincias y municipios de 1930), cronología sincronizada y vista sin WebGL.
