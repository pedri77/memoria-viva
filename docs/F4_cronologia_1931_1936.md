# F4 · Huecos de la cronología: 1931-1933 y primavera de 1936

**Fecha:** 15-11-2026

Seis acontecimientos nuevos (la cronología pasa de 37 a 43):

| Fecha | Acontecimiento | Evidencia |
|---|---|---|
| 30-04-1931 | Decreto de términos municipales (braceros vecinos del municipio) | Gaceta, pág. 415 (texto) |
| 24-01-1932 | Disolución de la Compañía de Jesús | Ficha BOE-A-1932-592 (título) |
| 11-03-1932 | Ley de divorcio (y rectificación del día siguiente) | Fichas BOE-A-1932-1855 y 1898 (título) |
| 12-08-1932 | Ley de separación de funcionarios hostiles a la República | Ficha BOE-A-1932-6203 (título) |
| 30-07-1933 | Ley de Orden Público | Ficha BOE-A-1933-6584 (título) |
| 10-05-1936 | Elección de Azaña como presidente de la República (754 de 847 votos) | Gaceta 09-04-1936, pág. 259, y 11-05-1936, pág. 1379 (texto) |

## Lo que no se ha podido documentar, y por qué

- **Sublevación de Sanjurjo (10-08-1932).** Las fichas del 11 y 12 de agosto de 1932 no contienen ninguna disposición que la nombre. La ley de separación de funcionarios se publica dos días después, pero su título no menciona la sublevación. Por eso el acontecimiento no la relaciona con ella: hacerlo sería una interpretación sin fuente.
- **Destitución de Alcalá-Zamora (abril de 1936).** El ejemplar del 8 de abril no está en `/gazeta/dias/`, y en 1936 no hay fichas `doc.php` antes de octubre. Solo puede afirmarse que los decretos de 8 de abril los firma Diego Martínez Barrio. Una nota editorial en el acontecimiento declara la laguna.
- **Amnistía y Gobierno de febrero de 1936.** Los ejemplares del 20, 22 y 23 de febrero y del 1 de marzo de 1936 no están en la ruta permitida.

## Cambios de código

- Esquema de acontecimiento: campo opcional `editorial_note`, que se muestra en la ficha.
- `scripts/etl/eventos_1932_1936.py`. Amplía el título del ejemplar del 30-04-1931, que ahora cubre también el decreto de los braceros.

## Comprobaciones

- `validate` OK: 131 documentos, 43 acontecimientos.
- Build OK: 234 páginas indexadas.
- `test:retirada` OK.

## Registro de lagunas (`data/lagunas.json`, página `/lagunas/`)

A petición de David, todo lo buscado sin éxito queda registrado para retomarlo con otras fuentes. Cada laguna indica:
- qué falta;
- dónde se buscó;
- qué fuentes probar, con su URL;
- a qué narrativas afecta.

`validate` comprueba que cada laguna tenga los campos mínimos, que los identificadores no se repitan, que las narrativas citadas existan y que las URL sean https. Hay 12 lagunas iniciales. La página está enlazada desde el pie del sitio y desde la sección «Lo que esta historia todavía no cuenta» de cada narrativa.

**Incidencia:** al comprobar que las fuentes alternativas responden, hice una petición a `https://www.boe.es/buscar/gazeta.php`, ruta que el `robots.txt` del BOE prohíbe a agentes automáticos. Fue una sola petición. El registro la recomienda solo para consulta manual.

## Lagunas cerradas el 15-11-2026

**Ley electoral de 1907** (`laguna-ley-electoral-1907`, retirada del registro). En la Gaceta del 10-08-1907, pág. 584:
- El art. 1.º declara electores a «todos los españoles varones» mayores de 25 años.
- El art. 4.º declara elegibles a los varones de estado seglar.

La narrativa del voto afirma ya, con dos evidencias, que en junio de 1931 votaban solo los varones. La fecha de 8 de agosto la da el decreto de mayo de 1931; el OCR del ejemplar no la deja leer.

**Enseñanza primaria 1934-1935** (`laguna-ensenanza-1934-1935`, reducida). Fechas tomadas de la bibliografía y verificadas en las fichas oficiales:

| Fecha | Disposición | Evidencia |
|---|---|---|
| 01-08-1934 | Orden que deja sin efecto la coeducación en las escuelas primarias nacionales, salvo en las mixtas y de párvulos | Gaceta 03-08-1934, pág. 1224 (texto) |
| 25-07-1935 | Decreto que suprime la Inspección Central de Primera enseñanza | Ficha BOE-A-1935-7071 (título) |
| 28-11-1935 | Decreto que da nueva redacción al art. 20 del decreto de Inspección de 1932 | Ficha BOE-A-1935-10978 (título) |

- **En la narrativa:** nueva escena de la narrativa de las escuelas, «Cambio de rumbo (1934-1935)», con 5 afirmaciones.
- **Lo que no se afirma:** que el decreto de noviembre de 1935 suprimiera la inamovilidad de los inspectores. Lo dice la bibliografía, pero el título no; queda como nota editorial.
- **Sigue abierto en el registro:** la sustitución de la enseñanza de las congregaciones.

**Generador:** `scripts/etl/ensenanza_1934_1935.py`, idempotente.

**Recuento:** 135 documentos, 46 acontecimientos y 11 lagunas.
