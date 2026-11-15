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
