# F4 · Alfabetización de los mayores de 10 años, censo de 1930 (P3)

**Fecha:** 15-11-2026

**Fuente:** INE, INEbase Historia, Censo de 1930, Tomo III. Volúmenes regionales: tabla «Clasificación de los habitantes por su edad combinada con el sexo, estado civil e instrucción elemental» de cada provincia. El número `td` de cada una se obtuvo recorriendo el árbol del Tomo III (`treeNavigation.do?tn=92538`), porque no siguen una numeración regular. Licencia CC BY 4.0. Se leyó solo el bloque «Resumen de la PROVINCIA» (Ávila y Álava: página 2, tras una portada; Murcia: un PDF de 11 páginas).

**Qué se transcribe:** por sexo, las filas habitantes, saben solo leer, saben escribir, no saben leer y no consta, en las columnas total, menos de 5 años y 5 a 9 años (`data/external/ine1930/instruccion_edad_1930_provincias.csv`, 500 filas, con el valor impreso y una nota en las dudosas). Cinco agentes transcribieron diez provincias cada uno; el cálculo y las comprobaciones son de `scripts/etl/ine_alfabetizacion_edad_1930.py`.

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
