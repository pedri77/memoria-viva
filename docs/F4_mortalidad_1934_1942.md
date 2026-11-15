# F4 · Hambre de posguerra (1): defunciones por provincia, 1934-1942

**Fecha:** 15-11-2026. Es el bloque A del triaje: datos oficiales agregados, sin relato. El relato sobre la posguerra (R3) espera a los revisores.

## Fuente

INE, INEbase Historia, Anuario Estadístico de España 1943, Demografía, «Movimiento de la población». Trae una tabla por año, de 1934 a 1942, con los matrimonios, los nacidos vivos y los fallecidos de cada provincia, en cifras absolutas y por 1.000 habitantes. Licencia CC BY 4.0. Los números de documento (td) están en el CSV.

## Transcripción

Tres subagentes transcribieron tres años cada uno, sobre las páginas partidas en mitades a 200 ppp (`scripts/etl/ine_mitades_pagina.py`). Para cada provincia y año se recogieron:
- nacidos;
- fallecidos varones, mujeres y total;
- tasa de mortalidad total;
- diferencia entre nacidos y fallecidos.

Datos en `data/external/ine_anuario1943/mnp_provincias_1934_1942.csv`, con las notas de cada año en `notas_transcripcion_AAAA.txt`.

Comprobaciones de `scripts/etl/ine_mortalidad_1934_1942.py`, superadas en los 9 años:
1. En cada fila, varones + mujeres = total, y nacidos − fallecidos = diferencia impresa.
2. Las 50 provincias suman la fila de la nación en todas las columnas.
3. La población que se deduce de la tasa está entre 0,8 y 1,25 veces la interpolada entre los censos de 1930 y 1940.

Excepciones documentadas:
- **Total nacional de 1942:** los varones y las mujeres impresos tienen una errata (±68) que se compensa entre ellos. El total conjunto cuadra.
- **Cádiz, de 1938 a 1940:** el INE calculó la tasa sobre unos 475.000 habitantes, frente a los 600.440 del censo de 1940. La natalidad impresa da la misma base. Va anotado en esas observaciones.
- **Escaneo de 1936:** muy dañado. Muchos dígitos se fijaron con la aritmética de la propia fila, siempre de forma compatible con la imagen. El detalle está en las notas de ese año.
- **Erratas de la tabla corregidas y anotadas:** León 1935, Oviedo 1937, Navarra y Vizcaya 1940, y Palencia 1942.

## Indicadores

- `ind-mortalidad-prov`: tasa de mortalidad tal como la publica el INE, por 1.000 habitantes.
- `ind-sobremortalidad-prov`: fallecidos del año en porcentaje de la media de 1934 y 1935, en la misma provincia. Se calcula con cifras absolutas, sin interpolar población.

España en su conjunto (1934-1935 = 100):

| 1934 | 1935 | 1936 | 1937 | 1938 | 1939 | 1940 | 1941 | 1942 |
|---|---|---|---|---|---|---|---|---|
| 101 | 99 | 107 | 122 | 125 | 122 | 110 | 125 | 99 |

En 1941 los valores más altos son los de Huelva (212), Badajoz (195), Cádiz (171) y Sevilla (161). El más bajo es el de Teruel (93).

## Cautelas publicadas con el dato

- Los años de guerra solo recogen las muertes inscritas en el Registro Civil. Faltan muchas en el frente, en bombardeos y por violencia, y la inscripción fue desigual en cada zona.
- De 1939 a 1942 las cifras son provisionales en la fuente.
- El índice no descuenta la variación de la población: refugiados, tropas, exilio.
- El dato no dice la causa de las muertes. Atribuir la subida de 1941 al hambre o a las epidemias es una interpretación que tendrá que ir atribuida a la historiografía cuando se escriba el relato (R3).

## Cambios en la web

- **Atlas:** el selector «Censo» pasa a «Año del dato» y se rellena con los años del indicador. Las series anuales usan los mismos cortes de color todos los años, para que se puedan comparar.
- **Datos:** columnas y gráfico con los años de cada indicador. El eje horizontal respeta la distancia entre años.
- **Fichas de provincia:** nueva sección «Series anuales».

## Siguiente (hambre, parte 2)

- **1943-1950:** defunciones de los Anuarios de 1944-1945, 1946-1947, 1948, 1949 y 1950.
- **Mortalidad infantil por provincia, 1933-1942:** ya localizada en el mismo Anuario de 1943 (td 161414 a 161432, los números pares son las provincias).
- **Precios y racionamiento:** en el apartado «Precios, salarios y consumo» de los Anuarios.
