# F4 · Alfabetización de los mayores de 10 años, censo de 1930 (P3)

**Fecha:** 15-11-2026

**Fuente:** INE, INEbase Historia, Censo de 1930, Tomo III. Volúmenes regionales: tabla «Clasificación de los habitantes por su edad combinada con el sexo, estado civil e instrucción elemental» de cada provincia. El número `td` de cada una se obtuvo recorriendo el árbol del Tomo III (`treeNavigation.do?tn=92538`), porque no siguen una numeración regular. Licencia CC BY 4.0. Se leyó solo el bloque «Resumen de la PROVINCIA» (Ávila y Álava: página 2, tras una portada; Murcia: un PDF de 11 páginas).

**Qué se transcribe:** por sexo, las filas habitantes, saben solo leer, saben escribir, no saben leer y no consta, en las columnas total, menos de 5 años y 5 a 9 años (`data/external/ine1930/instruccion_edad_1930_provincias.csv`, 500 filas, con el valor impreso y una nota en las dudosas). Cinco agentes transcribieron diez provincias cada uno; el cálculo y las comprobaciones son de `scripts/etl/ine_alfabetizacion_edad.py`.

**Cálculo:** mayores de 10 = total menos las seis columnas de menos de 10 años (incluye a quienes no declararon la edad). Tasa = (saben solo leer + saben escribir) / habitantes, ambos de 10 años o más.

**Comprobaciones:**
1. **Contraste con el Tomo II:** la columna total coincide, fila a fila y por sexo, con la transcripción independiente del Tomo II (P1) en las 50 provincias. La única diferencia era una errata del Tomo III (Murcia).
2. **Cuadre por columna:** en cada provincia, sexo y columna, la instrucción suma los habitantes. En menores de 10 años todos son solteros, así que la fila de solteros sirve de testigo de la de habitantes.

**Erratas corregidas** (con testigo):
- Cádiz, mujeres de 7 años: 4.691 por 5.691.
- León, varones de 9 años: 5.069 por 5.059.
- Murcia, varones que no saben leer: 59.938 por 159.938.
- Oviedo, mujeres de 8 años que saben escribir: 4.037 por 5.037. Se atribuye a esta fila por la progresión por edades.

**Descuadres sin corregir:** no se puede saber qué fila de instrucción está mal impresa. Son Ciudad Real (10), Málaga (10), Murcia (1 y 1), Navarra (600, en no saben o no consta), Oviedo (82, casilla en blanco) y Valladolid (1). La fila de habitantes está confirmada por la de solteros en todos. Su efecto en las tasas es menor de 0,01 puntos.

**Resultado** (50 provincias, sin Ceuta, Melilla ni las posesiones de África):
- **Mayores de 10 años:** 75,1 % de los varones, 60,5 % de las mujeres y 67,6 % del total.
- **Toda la población:** 62,0 %, 51,2 % y 56,5 %.
- **Extremos provinciales:** Albacete, 46,6 %, y Álava, 90,9 %.

**Cambios en el sitio:**
- Indicadores `ind-alfab10-{total,varones,mujeres}-prov` en el atlas y en Datos.
- Afirmación nueva en «Las escuelas de la República».
- La laguna `laguna-alfabetizacion-edad` queda solo para 1920 (Tomo III de 1920, `tn=80563`).

## Ampliación: censo de 1920 (15-11-2026)

**Fuente:** Censo de 1920, Tomo III, «Estados relativos a provincias, capitales, municipios de 20.000 o más habitantes…», un PDF por provincia (`treeNavigation.do?tn=88197`). El bloque «Resumen de la provincia» está en la penúltima página. Canarias es una sola provincia y Cádiz incluye Ceuta.

**Corrección:** el nodo `tn=80563` que se citaba antes en la laguna es el Tomo III de 1910, no el de 1920. El de 1920 es `tn=87955`.

**Transcripción:** 490 filas en `data/external/ine1920/instruccion_edad_1920_provincias.csv`, con el mismo método y el mismo script (`scripts/etl/ine_alfabetizacion_edad.py`, para los dos censos).

**Comprobaciones:**
- **Habitantes:** los totales de las 49 provincias coinciden con el Tomo II.
- **Instrucción, diferencias entre tomos:** en Cuenca (los dos sexos), Gerona (varones) y Orense (mujeres), el reparto entre las cuatro categorías difiere del Tomo II. Por ejemplo, las mujeres de Orense que saben solo leer son 11.519 en el Tomo III y 14.225 en el Tomo II. El resumen nacional del propio Tomo III (td 88553) coincide con la suma de sus provincias (124.513 mujeres que saben solo leer, frente a 127.164 del Tomo II). Por tanto, los dos tomos publican cifras distintas; se usa el Tomo III y cada dato lleva una nota.
- **Erratas corregidas:**
  - Soria, varones de 9 años que no saben leer: 579 por 379.
  - Gerona, varones con instrucción «no consta»: 173 por 178.
- **Descuadres menores anotados:** Cuenca, Guipúzcoa, Lugo, Vizcaya y Canarias.

**Resultado de 1920** (mayores de 10 años): 64,4 % de los varones, 49,2 % de las mujeres y 56,5 % del total. Va de Jaén, 30,7 %, a Santander, 89,3 %. Entre 1920 y 1930, +11,1 puntos.

**Cambios en el sitio:**
- Los indicadores `ind-alfab10-*` pasan a tener 1920 y 1930.
- La afirmación de «Las escuelas de la República» incluye 1920.
- Se retira la laguna `laguna-alfabetizacion-edad`.
