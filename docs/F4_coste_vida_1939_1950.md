# F4 · Hambre de posguerra, parte 3: coste de la vida en las capitales, 1939-1950

**Fecha:** 15-11-2026

**Fuente:** INE, Anuarios Estadísticos de España de 1943 a 1951, sección «Precios, salarios, racionamiento y consumo», «Índice del coste de la vida en las capitales», promedios anuales por capital de provincia, base julio de 1936 = 100. Licencia CC BY 4.0.

**Tablas (td):**

| td | Anuario | Años |
|---|---|---|
| 160628 | 1943 | 1939-1942 |
| 162162 | 1944-1945 | 1942-1944 |
| 162863 | 1946-1947 | 1944-1946 |
| 163586 | 1948 | 1945-1947 |
| 164740 | 1949 | 1946-1948 |
| 29950 | 1950 | 1949 |
| 165640 | 1951 | 1950 |

**Transcripción:** solo alimentación e índice general; 50 capitales y la media nacional. Todas las lecturas están en `data/external/ine_anuarios/coste_vida_capitales_1939_1950.csv`, con la columna `lector`.
- **Doble lectura:** cada cifra está leída al menos dos veces. Los años que se repiten se leyeron en dos o tres ediciones del Anuario. Los que salen en una sola (1939-1941, 1943, 1948, 1949 y 1950) los leyeron dos transcriptores independientes.
- **Discrepancias:** 3 entre unas 2.500 lecturas.
  - Murcia, índice general de 1950: «5o6,5». Se resuelve en 566,5 por la forma del dígito y por la coherencia con la subida de la alimentación.
  - Castellón, alimentación de 1947: 505,9 en el Anuario de 1948 y 504,9 en el de 1949. Se trata como una revisión entre ediciones.
  - Media nacional del índice general de 1943: 245,0 o 246,0. No se publica en el mapa.
- **Regla:** para cada año se usa la edición más reciente del Anuario. Script: `scripts/etl/ine_coste_vida_1939_1950.py`.

**Cautelas** (publicadas en el indicador):
- Los índices miden la subida en cada capital respecto a su propio julio de 1936. La nota de las tablas advierte que no permiten deducir en qué capital era más cara la vida.
- Mide la capital, no la provincia.
- Son precios oficiales de un presupuesto tipo: no recogen el estraperlo ni la escasez.
- 1939 es el promedio del segundo semestre.

**Media de las capitales** (julio de 1936 = 100):

| Año | Alimentación | General |
|---|---|---|
| 1939 | 177,7 | 153,6 |
| 1940 | 214,6 | 178,1 |
| 1941 | 300,0 | 231,5 |
| 1942 | 318,4 | 247,4 |
| 1943 | 310,0 | 245,0 |
| 1944 | 323,0 | 256,9 |
| 1945 | 347,0 | 274,8 |
| 1946 | 491,1 | 360,6 |
| 1947 | 580,7 | 424,4 |
| 1948 | 599,2 | 453,0 |
| 1949 | 622,9 | 477,5 |
| 1950 | 694,0 | 529,3 |

**Indicadores:** `ind-coste-vida-alimentacion-prov` e `ind-coste-vida-general-prov`, en el atlas y en Datos («Mortalidad y hambre»).

**Pendiente:**
- Racionamiento por provincias: Anuarios de 1944-1945 y de 1949 a 1951, tablas de distribución por provincias y cartillas.
- Salarios reales: índice nacional.
- El relato de la posguerra sigue esperando a los revisores (R3).
