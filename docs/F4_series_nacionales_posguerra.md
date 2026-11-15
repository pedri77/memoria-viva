# F4 · Series nacionales de la posguerra: salarios reales, coste de la vida y población reclusa

**Fecha:** 15-11-2026

Datos que los Anuarios Estadísticos de España (INE) solo publican para el conjunto del país. Se muestran en Datos, sección «Series nacionales de la posguerra»: un gráfico SVG estático con tabla y notas (`site/src/components/SerieNacional.astro`). Los datos están en `site/src/data/series_nacionales.json`, generado por `scripts/etl/ine_series_nacionales_posguerra.py`.

## Salarios reales, 1939-1950

**Fuente:** «Números índices de las remuneraciones reales, máxima y mínima, por jornada, que como cifra media nacional estimada corresponden a obreros de tipo profesional corriente, según los distintos grupos de actividad», base 1936 = 100. Hay siete ediciones: td 160638, 162168, 162870, 163594, 164743, 29958 y 165648. Según su propia nota, el INE estima el índice relacionando los salarios nominales con el coste de la vida.

**Transcripción:** 42 filas de oficio y sexo, máximo y mínimo, todas las ediciones (`data/external/ine_anuarios/salarios_reales_1939_1950.csv`, columna `lector`).
- **Doble lectura:** cada cifra está leída al menos dos veces y todas coinciden.
- **Errata del original:** la columna de máximos de 1942 del Anuario de 1944-1945 repite la de 1940 del Anuario de 1943. Para 1942 se usa el Anuario de 1943, con una segunda lectura propia.
- **Cautelas:**
  - 1944 y 1945 no incluyen el segundo semestre.
  - La columna de 1950 del Anuario de 1951 repite casi exactamente la de 1948.
  - Son salarios por jornada de tarifa, no ingresos anuales: no reflejan el paro ni el estraperlo.

**Publicado:** salario real máximo de cinco oficios.

| Año | Agrícolas (h) | Albañiles (h) | Metalúrgicos (h) | Textiles (m) | Costureras (m) |
|---|---|---|---|---|---|
| 1939 | 76 | 70 | 74 | 75 | 74 |
| 1945 | 72 | 58 | 57 | 73 | 69 |
| 1949 | 53 | 47 | 44 | 67 | 67 |

## Coste de la vida, media de las capitales

Es la fila «Índice medio ponderado de las capitales» de las tablas de `docs/F4_coste_vida_1939_1950.md`.

## Población reclusa, 1922-1950

**Fuente:** Anuario 1950, «Población reclusa», págs. 939-940 (td 29648 y 29649).
- Cuadro I: existencia a 1 de enero de 1922 a 1934 y de 1939 a 1950, por sexo.
- Cuadro II: penados, procesados y detenidos.
- Cuadro III: penados por «delitos no comunes».

**Transcripción propia** (`poblacion_reclusa_1922_1950.csv`, `reclusos_situacion_1939_1950.csv`, `penados_no_comunes_1943_1950.csv`), con cuadres por fila y entre cuadros.
- **Errata corregida:** mujeres procesadas a 1 de enero de 1943, 613 por 3.613. Lo confirman el total de mujeres y el de procesados.

**Notas de la fuente:**
- 1932: sin la prisión de Sevilla, cuyo archivo se destruyó.
- 1944: sin clasificación por sexo.
- 1939: a 1 de abril.
- 1943 (penados por «delitos no comunes»): a 1 de julio.

**Cautelas publicadas:**
- No hay cifras de 1935 a 1938.
- No incluye campos de concentración, batallones de trabajadores ni colonias penitenciarias militarizadas.
- «Delitos no comunes» es la denominación de la fuente.

**Cifras clave:**
- 12.574 reclusos a 1 de enero de 1934.
- 100.262 a 1 de abril de 1939.
- 270.719 a 1 de enero de 1940, el máximo.
- 36.127 en 1950.
- Penados por delitos no comunes: 49.453 en julio de 1943 y 7.734 en 1950.

## Pendiente

El relato de la posguerra (R3), con revisores.
