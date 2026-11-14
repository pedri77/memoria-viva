# España: Memoria Viva

Atlas y archivo documental de la historia contemporánea de España. Piloto: Segunda República y Guerra Civil (1931-1939). Cada afirmación publicada enlaza a la fuente que la sostiene, con su fecha, su lugar, su grado de certeza y sus condiciones de reutilización.

**Estado:** fase F4: capa electoral 1931-1936 en el atlas; primera narrativa en revisión; cronología, datos y búsqueda operativos. Ver `docs/04_roadmap.md`.

## Estructura

| Ruta | Contenido |
|---|---|
| `docs/` | documento maestro v1.1, revisión crítica, stack, auditoría de fuentes, roadmap y guía editorial |
| `schemas/` | JSON Schema de fuentes, lugares, documentos, acontecimientos, indicadores y narrativas |
| `data/canonical/` | datos revisados (fuente de verdad) |
| `data/external/` | datos de terceros con licencia abierta, sin modificar |
| `scripts/etl/` | scripts de preparación de datos (Python) |
| `scripts/checks/` | validación de esquemas e integridad, comprobación de enlaces |
| `site/` | web estática (Astro) |

## Uso

```bash
npm install
npm run validate      # esquemas + referencias cruzadas + reglas de derechos
npm run check:links   # comprueba que las URL citadas responden
npm run dev           # web en local
npm run build         # valida y genera dist/
```

## Contribuir y corregir

Los errores se notifican con el [formulario de correcciones](https://github.com/pedri77/memoria-viva/issues/new?template=correccion.yml). Antes de proponer datos, lee `docs/guia_editorial.md`.

## Licencias

Código MIT. Textos y datos propios CC BY-SA 4.0. Datos de terceros, su licencia. Detalle en `LICENSE-contenido.md`.
