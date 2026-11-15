# F4 · Alfabetización de 1930 y cronología de 1934-1935

**Fecha:** 15-11-2026

## 1. Alfabetización por provincia (censo de 1930)

**Fuente:** INE, INEbase Historia, Censo de 1930, Tomo II, «Habitantes inscritos en la Población de HECHO ... clasificados según el sexo en combinación con el estado civil y con la instrucción elemental, por provincias» (`pdfDispacher.do?td=194363`). Licencia CC BY 4.0 (Política de Difusión Estadística del INE, febrero de 2026). `robots.txt` del INE solo veta `/buscar/`, `/cgi-bin/` y rutas de administración.

**Transcripción:** a mano desde la imagen del PDF (el OCR del INE es inservible para cifras), en `data/external/ine1930/instruccion_1930_provincias.csv`: 50 provincias y las posesiones de África, por sexo, 9 columnas.

**Comprobaciones** (en `scripts/etl/ine_alfabetizacion.py`, fallan si algo no cuadra):

1. En cada una de las 102 filas, estado civil e instrucción suman el total de la fila.
2. Varones + mujeres = total de la provincia.
3. La suma de todas las filas reproduce columna a columna los totales nacionales impresos.
4. El total de cada provincia es idéntico a la suma municipal de mapSpainHist (`ind-pob-hecho-prov`, 1930), que es una fuente independiente.

Las comprobaciones encontraron dos discrepancias:
- Un error mío de lectura (Barcelona, mujeres casadas: 366.735, no 266.735).
- Una **errata de la tabla impresa**: Sevilla, mujeres que saben leer y escribir. La tabla imprime 159.486, pero la fila y el total nacional solo cuadran con 195.486. Se corrige y queda anotado en el CSV y en la observación (`uncertainty`).

**Indicadores nuevos:** `ind-alfab-total-prov`, `ind-alfab-varones-prov`, `ind-alfab-mujeres-prov`.
- **Definición:** (saben solo leer + saben leer y escribir) / población de hecho de todas las edades.
- **Totales nacionales:** 62,0 % de los varones y 51,2 % de las mujeres.
- **Extremos provinciales:** Albacete 37,1 % y Álava 76,8 %.
- **Ceuta y Melilla:** sin dato, porque la tabla las agrupa con el resto de posesiones de África.
- **Cautela publicada:** el denominador incluye a los niños pequeños, así que las cifras son más bajas que las tasas sobre mayores de 10 años de la historiografía.

**Cambios en el sitio:**
- Atlas: si el indicador elegido no tiene datos del censo seleccionado, el selector salta al censo que sí los tiene. Los porcentajes se muestran con un decimal.
- Narrativa de las escuelas: nueva afirmación con las cifras de 1930. Se elimina la laguna «falta la alfabetización» y se añade la cautela sobre el denominador.

## 2. Cronología de 1934-1935

Seis acontecimientos nuevos (la cronología pasa de 31 a 37):

| Fecha | Acontecimiento | Evidencia |
|---|---|---|
| 25-04-1934 | Ley de amnistía | Gaceta, pág. 548 (texto) |
| 29-08-1934 | Plan de Bachillerato de siete cursos | Gaceta 30-08-1934, págs. 1872-1873 (texto) |
| 04-10-1934 | Gobierno presidido por Lerroux | Gaceta 05-10-1934, págs. 178-179 (texto) |
| 03-01-1935 | Suspensión de las facultades del Parlamento de Cataluña | Ficha BOE-A-1935-101 (solo título) |
| 24-03-1935 | Ley de arrendamientos de fincas rústicas | Ficha BOE-A-1935-2712 (solo título) |
| 10-08-1935 | Ley de reforma de la Reforma agraria | Gaceta, pág. 1288 (texto) |

**Hallazgo útil:** las fichas `doc.php` del BOE también cubren la Gaceta de Madrid, no solo el BOE de Burgos. Sirven para los ejemplares que no están en `/gazeta/dias/` (enero-marzo de 1935, enero de 1936).

**Cautelas:**
- No se afirma la composición partidista del Gobierno de octubre de 1934: la Gaceta da nombres, no partidos.
- Cuando el OCR da una fecha de sanción dudosa, el acontecimiento lleva la fecha de publicación.

## Comprobaciones

- `validate` OK: 123 documentos, 37 acontecimientos, 6 indicadores.
- Build OK: 220 páginas indexadas.
- `test:retirada` OK.
- Prueba del atlas con un navegador sin interfaz: carga la capa, salta de 1920 a 1930 y no da errores propios.

## 3. Ampliación: alfabetización de 1920 (15-11-2026)

**Fuente:** Censo de 1920, Tomo II, «Clasificación de la población de Hecho por sexo, estado civil e instrucción elemental», «Resumen general por provincias» (INEbase Historia, `td=86929`). Licencia CC BY 4.0.

**Transcripción:** a mano, en `data/external/ine1920/instruccion_1920_provincias.csv` (100 filas). Pasa las mismas comprobaciones que la de 1930:
- Todas las filas cuadran a la primera.
- Los totales nacionales impresos se reproducen columna a columna.

**Contraste con mapSpainHist (suma municipal de 1920):**
- **Canarias:** era una sola provincia en 1920. Su total coincide exactamente con la suma de Las Palmas y Santa Cruz de Tenerife.
- **Cádiz:** supera la suma municipal en 35.219 habitantes, que es exactamente la población de Ceuta. En 1920 el censo incluía Ceuta en Cádiz.
- **Gerona:** 60 habitantes de diferencia, sin explicar. Queda anotado en la observación.

**Resultado:**
- En España saben leer el 47,3 % en 1920 y el 56,5 % en 1930.
- Varones: del 53,2 % al 62,0 %. Mujeres: del 41,7 % al 51,2 %.
- Mayores subidas: Málaga (+18,1 puntos), Granada (+16,1) y Almería (+15,0).
- Palencia y Santander bajan ligeramente, desde niveles altos.
- Sin dato provincial en 1920:
  - Las Palmas y Santa Cruz de Tenerife: la observación da la cifra del archipiélago.
  - Ceuta: incluida en Cádiz.
  - Melilla: agrupada con las posesiones.

**Cambios:** los tres indicadores `ind-alfab-*` tienen ahora observaciones de 1920 y 1930. La narrativa de las escuelas da las dos cifras.

## 4. Convocatoria de las elecciones de 1936: no localizable

La Gaceta de enero de 1936 no está en ninguna de las dos vías permitidas por el `robots.txt` del BOE:
- **Ruta de PDF** `/gazeta/dias/`: no aparece.
- **Fichas `doc.php`:** en 1936 no hay ninguna ficha antes de `BOE-A-1936-9134`, el núm. 1 del BOE de Burgos. Se probaron identificadores repartidos entre 1 y 9133.

La laguna de la narrativa del voto lo explica con este detalle. Para cerrarla hay que consultar la Gaceta en otra hemeroteca.
