# F4 · Reforma agraria: tablas del Anuario Estadístico de 1934

**Fecha:** 15-11-2026. Continúa la laguna `laguna-aplicacion-reforma-agraria`.

## Fuente

INE, INEbase Historia, Anuario Estadístico de España 1934, Agricultura, «Reforma agraria», págs. 211-215. Licencia CC BY 4.0. Las tablas solo cubren las provincias que estudió el Anuario: Badajoz, Cáceres, Ciudad Real, Córdoba, Huelva, Jaén, Sevilla y Toledo, más Cádiz, Granada, Málaga y Salamanca en la tabla VI.

## Transcrito y comprobado

Datos en `data/external/ine_anuario1934/`.

| Tabla | Contenido | Comprobación |
|---|---|---|
| IV (td=102040) | Propietarios y líquido imponible por categoría (pequeños, medianos y grandes) en 8 provincias | Los 48 porcentajes impresos coinciden (±0,02) con los recalculados desde las cifras absolutas |
| V (td=102041) | Extensión expropiable de la extinguida Grandeza en 8 provincias | Hectáreas, áreas y centiáreas suman exactamente el total impreso: 266.453 ha 58 a 99 ca |
| VI (td=102042) | Fincas de la Grandeza expropiadas, superficie y obreros asentados en 11 provincias | Las tres columnas suman sus totales impresos: 370 fincas, 89.127 ha y 8.559 asentados |

En la tabla VI, la superficie de Cádiz tenía un dígito dañado; se fija en 19.299 por la suma de la columna y queda anotado.

## Indicadores

Script: `scripts/etl/ine_reforma_agraria_1934.py`. Las provincias que no están en la tabla quedan sin dato, con su motivo.

- `ind-ra-riqueza-grandes-prov`: % de la riqueza catastrada en manos de los grandes propietarios. Va del 31,14 % de Ciudad Real al 71,79 % de Sevilla.
- `ind-ra-asentados-prov`: obreros asentados en fincas de la Grandeza. El máximo es Córdoba, con 2.564.
- `ind-ra-superficie-expropiada-prov`: hectáreas expropiadas a la Grandeza.
- `ind-ra-expropiable-grandeza-prov`: hectáreas expropiables de la Grandeza.

## Cautelas

- La tabla VI solo cuenta las fincas de la extinguida Grandeza (base 20 de la ley de 1932), no el conjunto de la reforma.
- El Anuario no da la fecha de corte de las cifras ni la fecha de referencia del catastro.
- La tabla IV mide riqueza imponible, no superficie.

## En la web

- El relato «La tierra» de la portada pasa a siete pasos. Se añaden «Quién tenía la tierra» (tabla IV) y «Lo que se expropió a la Grandeza» (tablas V y VI), cada uno con su mapa y su leyenda.
- La página de datos tiene el tema nuevo «Propiedad y reforma agraria».
- Las fichas de provincia muestran los datos de un solo año como lista, no como gráfico.

## Pendiente

Siguen en la laguna, sin transcribir:
- formas de explotación;
- distribución de fincas por superficie;
- propiedad catastrada;
- señoríos;
- montes;
- arrendamientos colectivos.

Tampoco se han buscado todavía el Boletín del Instituto de Reforma Agraria ni el Anuario de 1936.
