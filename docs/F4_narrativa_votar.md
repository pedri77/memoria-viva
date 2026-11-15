# F4 · Segunda narrativa: «Votar en la República, 1931-1936»

**Fecha:** 15-11-2026 · **Estado:** borrador en revisión (mismo circuito que la primera narrativa: dos revisores antes de `aprobado`).

## Contenido

6 escenas y 15 afirmaciones, todas de tipo `documento`:

| Escena | Evidencia |
|---|---|
| Nuevas reglas antes de votar (mayo de 1931) | Gaceta 10-05-1931, págs. 639-640: decreto que modifica la ley electoral para las Constituyentes (circunscripciones provinciales, 23 años, mujeres y sacerdotes elegibles, mínimo del 20 %) |
| Las Cortes Constituyentes (junio de 1931) | Gaceta 04-06-1931 y Atlas Electoral (participación y candidatura más votada) |
| La Constitución y el voto de las mujeres | Gaceta 10-12-1931, arts. 36 (pág. 1581), 52 y 53 (pág. 1582) |
| Reglas para las siguientes elecciones (julio de 1933) | Gaceta 28-07-1933, pág. 635: ley que extiende el decreto de 1931 y sube a 150.000 habitantes el umbral de circunscripción propia |
| Noviembre de 1933: el censo se duplica | Gaceta 10-10-1933 y Atlas Electoral |
| Febrero de 1936 | Atlas Electoral |

Documentos nuevos: `doc-gaceta-1931-05-10` y `doc-gaceta-1933-07-28` (PDF en la ruta permitida `/gazeta/dias/`).

## Cifras derivadas del Atlas (primera vuelta)

| Elección | Circunscripciones | Electores registrados (suma) | Participación agregada | Mínima | Máxima |
|---|---|---|---|---|---|
| 1931 | 63 | 6.199.713 | 70,1 % | Málaga capital 47,0 % | Palencia 87,9 % |
| 1933 | 60 | 13.132.211 | 66,3 % | Cádiz 37,3 % | Palencia 81,3 % |
| 1936 | 60 | 13.486.852 | 71,9 % | Santa Cruz de Tenerife 57,0 % | Sevilla capital 97,5 % |

Sumas propias sobre `elect` y `votant`. El Atlas solo agrega mesas con ambos datos, así que pueden quedarse cortas frente a los totales oficiales. El 97,5 % de Sevilla capital se publica con nota editorial, sin corregir.

## Cautelas

- La ley de julio de 1933 aparece fechada en el OCR el «veintiuno de julio»; como el OCR no es fiable en fechas, la narrativa la cita solo por su publicación (Gaceta del 28-07-1933).
- La narrativa no atribuye el aumento del censo en 1933 al voto femenino: el Atlas no separa por sexo. Lo dice en una nota editorial.
- El voto exclusivamente masculino en 1931 no se afirma: depende del texto de la ley de 1907, que aún no está en el proyecto.

## Cambios de código

- Esquema de narrativa: campo opcional `atlas_query` por escena.
- Página de historia: enlace «Ver estas elecciones en el atlas» con la capa y la elección de la escena.

## Comprobaciones

`validate` OK (stories=2), build OK (207 páginas indexadas), `test:retirada` 6/6, Lighthouse local móvil: rendimiento 90, accesibilidad 100.
