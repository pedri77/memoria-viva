# Licencias del contenido y de los datos

| Qué | Licencia |
|---|---|
| Código (`scripts/`, `site/`, `schemas/`) | MIT (ver `LICENSE`) |
| Textos, fichas y datos elaborados por el proyecto (`data/canonical/`, `docs/`) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.es) |
| Datos y documentos de terceros | La licencia de cada custodio, registrada objeto a objeto en el campo `rights` |

## Datos de terceros incluidos en el repositorio

- `data/external/bne/hemeroteca_fulltext_2026-11-14.csv`: «Hemeroteca digital. Texto completo», Biblioteca Nacional de España, publicado en datos.gob.es con licencia CC BY 4.0 (https://datos.gob.es/catalogo/ea0019768-hemeroteca-digital-texto-completo1). Descargado el 14-11-2026, SHA-256 `76495ff01ae6723ac56308a27dee3e88a5805b080ab8833ec023e074a1292ddc`. Sin modificar.

- `data/external/mapspainhist/`: «Historical municipal boundaries of Spain, 1900-2001», Pau Vall-Prat, Zenodo (https://doi.org/10.5281/zenodo.23663208), CC BY 4.0. Descargado el 14-11-2026, sin modificar (`prov_1930_areas.csv` es derivado).
- `data/external/madrid/publicaciones_periodicas_guerra_civil.csv`: «memoria de Madrid. Publicaciones periódicas de la Guerra Civil», Ayuntamiento de Madrid (datos.madrid.es), CC BY 4.0.
- «Bombardeos de la Guerra Civil en Euskadi» (Gogora, Open Data Euskadi): licencia por verificar, por eso **no** se incluye en el repositorio; las fichas solo enlazan y parafrasean.

- `data/external/atlas_electoral/`: «Electoral Atlas of the Spanish Second Republic (1931-1936)», v2.1, Toni Rodon, Pau Vall-Prat y Diego Martín Álvarez (UPF), CORA (https://doi.org/10.34810/DATA3274), **CC BY-NC-SA 4.0**. Descargado por la API de Dataverse el 14-11-2026, sin modificar.
- Derivados del anterior, también **CC BY-NC-SA 4.0** (uso no comercial y compartir igual): `site/public/data/v1/circunscripciones_*.geojson`, `elecciones_municipios.json`, `municipios_1930_elecciones.geojson`, `elecciones_resumen.json`, `elecciones_bloques.json`.

Los documentos de la Gaceta de Madrid y del BOE se enlazan a www.boe.es y se reutilizan según las condiciones de la Agencia Estatal Boletín Oficial del Estado.
