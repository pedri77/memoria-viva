# F4 · Población por profesiones, censo de 1930 (P1 del backlog)

**Fecha:** 15-11-2026.

## Fuente

INE, INEbase Historia, Censo de 1930, Tomo III, volúmenes regionales. Cada provincia tiene su tabla «Habitantes inscritos en la población de HECHO y clasificados por sexo, edad, estado civil y profesiones o industrias»: 129 filas en 27 grupos, con un bloque para la capital y otro para la provincia entera. Licencia CC BY 4.0.

El Tomo II solo trae las profesiones de la nación, de las capitales y de las posesiones de África. No las da por provincia.

## Transcripción

- De cada provincia (bloque de la provincia entera) se transcriben a mano los «Totales del grupo» de los 27 grupos y la fila 85, «Diversas». Están en `data/external/ine1930/profesiones_1930_provincias.csv`.
- Lo hicieron cinco subagentes en paralelo, sobre tiras de imagen preparadas con `scripts/etl/ine_tiras_totales.py`. Huesca, transcrita a mano antes del reparto, sirvió de modelo.
- Comprobaciones de `scripts/etl/ine_profesiones_1930.py`, todas superadas:
  1. En cada grupo, varones + mujeres = total.
  2. La suma de los grupos reproduce, por sexo, los totales del censo (tabla de instrucción de 1930).
  3. La suma total coincide con la población de hecho de mapSpainHist.
- Cotejo humano independiente: los grupos XII a XIV de Badajoz y de Madrid, 18 cifras, todas coinciden.

### Erratas e incidencias (anotadas en el campo `nota` del CSV)

| Provincia | Incidencia | Qué se hizo |
|---|---|---|
| Granada | La línea de totales del grupo XV dice 16.670 varones; las filas suman 16.676. | Se usa 16.676. |
| Castellón | En el grupo XX los varones se imprimen como 901 y la fila no cuadra (total 979, mujeres 18). | Se usa 961. |
| Salamanca | En el grupo XXIV los varones se imprimen como 22.318; las filas 119 y 120 suman 32.318. | Se usa 32.318. |
| Valladolid | En el grupo XX el total general se imprime como 1.376; 1.365 + 31 = 1.396. | Se usa 1.396. |
| Murcia | La página 20 del PDF está cortada por la derecha. | Las mujeres de los grupos XXIV a XXVII se calculan con las columnas de estado civil impresas en esa misma página. |
| Huelva | La página 14 lleva la cabecera «Capital» por error. | Sus cifras son las de la provincia. |
| Zaragoza | La fila 129 lleva impreso el número 126. | Se toma como la fila 129. |
| Cuenca | El grupo XXVI viene en cifras redondas. | Se copia tal cual y cuadra. |

### Provincias incompletas

El PDF de tres provincias no trae alguna página. Están en el registro de lagunas (`laguna-profesiones-paginas`).

| Provincia | Qué falta en el PDF | Efecto |
|---|---|---|
| Cádiz | Página de las filas 64 a 90 (grupos XII a XVI) | El grupo II sí está y su porcentaje se calcula con el total por sexo del censo. Sin dato de «Diversas». |
| Gerona | Grupos I a VI | Sin dato agrícola. |
| Vizcaya | Grupos I a VI | Sin dato agrícola. |

## Indicadores

Denominador de los tres: la población con profesión, es decir, la población de hecho menos los grupos XXIV (escolar), XXV (improductivos), XXVI (miembros de la familia) y XXVII (desconocida).

- `ind-prof-agraria-prov`: grupo II (montes, agricultura y ganadería), ambos sexos. Va del 8,6 % de Madrid al 76,9 % de Orense.
- `ind-prof-agraria-varones-prov`: grupo II, solo varones. Va del 10,8 % de Madrid al 78,4 % de Cuenca.
- `ind-prof-diversas-prov`: fila 85, «Diversas». Va del 2,3 % de Álava al 33,3 % de Las Palmas.

En las 47 provincias completas, el grupo II es el 46,1 % de la población con profesión y la fila 85, el 12,9 %.

## Cautelas publicadas con el dato

- La fila «Diversas» no dice la actividad y parte serían jornaleros agrícolas. Por eso el grupo II es un mínimo.
- El trabajo de las mujeres en la explotación familiar se registra sobre todo en el grupo XXVI, que queda fuera del denominador. Por eso se publica también el indicador de varones.

## Hallazgo para P3 (alfabetización por edad)

El Tomo III de 1930 trae para cada provincia la tabla de edad combinada con sexo, estado civil e instrucción (p. ej. Huesca, td=103310). Queda anotado en la laguna `laguna-alfabetizacion-edad`.
