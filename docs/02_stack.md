# 02 · Valoración del stack y propuesta

**Fecha:** 14-11-2026 · Versiones consultadas en npm ese día.

## Diagnóstico

El stack del documento (l.163-169, l.408-423) es razonable para una plataforma institucional con API pública, contribuciones y backoffice editorial. Para un proyecto personal en fase piloto tiene tres costes que no se compensan:

- **Operación:** PostgreSQL+PostGIS, OpenSearch, MinIO, Redis, Celery, FastAPI y Next.js son siete servicios que vigilar, actualizar y respaldar. OpenSearch solo necesita 2-4 GB de RAM.
- **Superficie de ataque y datos personales:** un backoffice con login es justo lo que no hace falta mientras no se publiquen datos nominales.
- **Volumen real:** el piloto revisado tiene unos cientos de registros. Cabe entero en ficheros JSON de pocos MB.

## Valoración capa por capa

| Capa (doc) | Veredicto | Motivo | Sustituto en el MVP |
|---|---|---|---|
| Next.js + TS | Cambiar | SSR y BFF sin backend no aportan; el patrón propio de David es Vite + TS (torre-osi, archipielago-cuerpo). | **Astro 7** (páginas estáticas por ficha, buen SEO, islas interactivas) o Vite 8 si se quiere una sola SPA. Recomendado: Astro, porque cada ficha necesita URL propia indexable. |
| MapLibre GL + deck.gl | Mantener MapLibre, quitar deck.gl | deck.gl solo compensa con decenas de miles de puntos. | **maplibre-gl 6.18** + **pmtiles 4.5** (teselas vectoriales en un único fichero estático). |
| D3 / ECharts | Mantener ECharts | Series con anotaciones de discontinuidad y tabla accesible. | **echarts 6.1** |
| GSAP | Mantener | Narrativa con scroll; respetar `prefers-reduced-motion`. | **gsap 3.15** |
| Three.js | Aplazar | Fuera del MVP (l.126 ya lo pone en P2). | Fase 4 |
| FastAPI + Pydantic | Aplazar | Sin datos dinámicos no hay API que servir. El contrato `/api/v1/...` se emula con JSON estáticos versionados (`/data/v1/events.json`). | Ficheros JSON |
| PostgreSQL + PostGIS | Aplazar | La geometría se prepara offline. | **DuckDB** (con extensión spatial) en el ETL; salida GeoJSON → PMTiles |
| OpenSearch | Quitar | Sobredimensionado. | **Pagefind 1.6** (índice estático generado en el build, búsqueda en cliente) |
| S3 / MinIO | Quitar | Por política del propio documento, por defecto se enlaza al custodio. Las pocas imágenes de dominio público caben en el repo o en R2. | Repo (imágenes pequeñas) |
| Redis + Celery | Quitar | No hay trabajos en segundo plano. | Scripts Python que se ejecutan a mano o en GitHub Actions |
| Qdrant / RAG | Aplazar | Ver R16. | Fase 4, modelo local |
| OpenTelemetry + Grafana | Quitar | Sin servidores. | Lighthouse CI y comprobador de enlaces en Actions |
| OIDC + MFA backoffice | Quitar | Sin backoffice. La edición es Git: cada cambio es un commit firmado y revisable, que además resuelve el historial y la auditoría que pide l.440. | GitHub + PR |
| IIIF | Mantener como lector | Solo para mostrar manifiestos de terceros que ya lo ofrecen (Europeana). | Visor ligero (p. ej. Tify o Mirador) en fase 3 |

## Arquitectura propuesta (MVP)

```text
fuentes (web, datos.gob.es, CNIG, Gazeta)
   │  captura manual o script con permiso
   ▼
data/raw/<fuente>/...            (no se publica si los derechos no lo permiten)
   │  scripts/etl/*.py  (Python + DuckDB, ejecución reproducible)
   ▼
data/canonical/*.json|geojson    (fuente de verdad, en git, validada con JSON Schema)
   │  build (Astro)
   ▼
dist/  páginas estáticas + /data/v1/*.json + tiles.pmtiles + índice Pagefind
   │  GitHub Actions: validar esquemas, citas, enlaces, axe, Lighthouse
   ▼
GitHub Pages (push a main = despliegue)
```

Estructura del repo:

```text
memoria-viva/
  docs/                 documentación (este directorio)
  schemas/              JSON Schema: source, document, event, place, indicator, observation, claim, story
  data/canonical/       datos revisados
  data/raw/             capturas (gitignore si no son redistribuibles)
  scripts/etl/          un script por fuente
  scripts/checks/       validar_citas.py, validar_enlaces.py
  site/                 Astro
  .github/workflows/    ci.yml, deploy.yml
```

## Modelo de datos mínimo (subset del §I.8)

Se mantienen las entidades del documento, pero el MVP solo implementa: `source`, `document`, `event`, `place` (+ `geometry_version`), `indicator`, `observation`, `claim`, `story`, `revision`. `person` queda fuera hasta resolver ADR-007; mientras, solo actores colectivos (`organization`).

Campos obligatorios que el validador comprueba en cada objeto publicado: `id`, `source_ids[]` (no vacío), `rights.status` ∈ {`public_domain`, `cc_by`, `link_only`, `restricted`}, `review.status`, `review.date`, y `date_precision` en eventos.

## Criterios para escalar (cuándo volver al stack del documento)

Pasar a PostgreSQL+PostGIS y FastAPI (en Hetzner, UE) solo si se cumple al menos uno:

1. Contribuciones de terceros que no pasan por PR de Git.
2. Más de ~50.000 registros o JSON servidos de más de 20 MB por página.
3. Necesidad de API consultable por terceros con filtros arbitrarios.
4. Publicación de datos nominales con control de acceso (exige además ADR-007 resuelto y asesoría jurídica).

## ADR del §II.13 reformulados

| ADR | Decisión propuesta |
|---|---|
| ADR-001 Licencias | Código: MIT. Textos y datos propios: CC BY-SA 4.0. Datos de terceros: su licencia, registrada por objeto (CNIG y BNE datos.gob: CC BY 4.0; BOE: condiciones de reutilización de la AEBOE; PARES: dominio público o solo enlace). |
| ADR-002 Hosting | GitHub Pages; dominio propio opcional después. Sin RPO/RTO: el repo es la copia de seguridad. |
| ADR-003 Mapas base | Base actual neutra (OSM o IGN Base, con atribución) + límites provinciales vigentes en 1931-1939 (prácticamente los de 1833; la única diferencia relevante es la división de Canarias en 1927). Municipios: solo los existentes en el censo de 1930, con la tabla de alteraciones del INE. Cartografía antigua del CNIG como capa raster opcional, georreferenciada por el proyecto y con el error declarado. |
| ADR-004 Lugares sensibles | Fosas y lugares de represión: solo a nivel municipio en el MVP; nunca coordenadas exactas. |
| ADR-005 Acuerdo con archivo | Aplazado. El MVP usa solo vías de acceso públicas y licencias abiertas. |
| ADR-006 HTR | Aplazado. Para prensa se usa el OCR de la BNE tal cual, marcado como automático. |
| ADR-007 Registros nominativos | No en el MVP. Antes de habilitarlos: evaluación jurídica (Ley 16/1985 art. 57, LOPDGDD art. 3, Ley 20/2022) y procedimiento de retirada probado. |
| ADR-008 RAG | No en el MVP. Criterio de activación: corpus propio publicado, modelo local, 0 citas inventadas en 100 preguntas de prueba. |
