# Backlog de ampliaciones

**Actualizado:** 15-11-2026. Este fichero es la lista de trabajo; `data/lagunas.json` es el registro público de lo que se buscó sin encontrarlo.

## Pendientes de revisores (decisión de David, 15-11-2026: se harán más adelante)

Requieren que antes haya al menos un revisor con formación en historia contemporánea, por lo delicado del tema o por los derechos.

| # | Ampliación | Por qué espera | Material ya disponible |
|---|---|---|---|
| R1 | **Tercera narrativa: las normas de las dos zonas durante la guerra (1936-1939)** | Es el tema más delicado: vocabulario y riesgo de simetrías artificiales (guía editorial, §1.4 y §2). | 8 acontecimientos del BOE de Burgos (`scripts/etl/eventos_burgos.py`), Gaceta de la zona republicana de julio y octubre de 1936 (`doc-gaceta-1936-07-19`, `-07-20`, `-10-07`, `-10-08`), Decreto 66 sobre el magisterio, bombardeos de Euskadi (Gogora, licencia sin verificar, en `data/raw/`). Lagunas: Boletín de la Junta de Defensa Nacional y texto completo de las normas. |
| R2 | **Imágenes de Europeana en las fichas** | Hay que revisar los derechos imagen por imagen; ninguna se publica sin una licencia abierta verificada. | Fuente catalogada en `docs/05_acceso_y_nuevas_fuentes.md`. API de Europeana con clave gratuita. |
| R3 | **Ampliación del periodo a 1939-1975** | Es otro proyecto por tamaño: necesita su propia guía editorial (represión, exilio, fosas) y revisores. | `mapSpainHist` cubre los censos de 1940 a 1970; los BOE de 1939-1975 tienen fichas `doc.php`. |

## Pendientes sin revisores (por orden de valor)

| # | Ampliación | Coste | Nota |
|---|---|---|---|
| ~~P1~~ | ~~Censo de 1930 por profesiones~~ | Hecho 15-11-2026 | `docs/F4_profesiones_1930.md`. Pendiente: usarlo en una narrativa (reforma agraria) y recuperar las páginas de Cádiz, Gerona y Vizcaya. |
| P2 | Prensa del día en los acontecimientos clave (enlaces a números de la BNE, sin citas) | Medio | El servidor de la BNE bloquea clientes automáticos: los enlaces se construyen desde el CSV oficial y se comprueban a mano. |
| P3 | Alfabetización por edad (mayores de 10 años), censo de 1930, tomo III | Alto: tablas regionales | Laguna `laguna-alfabetizacion-edad`. Localizadas: una tabla por provincia en el Tomo III (p. ej. td=103310); mismo método que P1. |
| P4 | Georreferenciación de mapas históricos del CNIG | Alto | Aplazado desde F2. |
| P5 | Enlaces Wikidata de los municipios de 1930 | Medio | Aplazado desde F2. |

## Hecho fuera de la lista

- 15-11-2026: portada «Del documento al mapa» y capa visual común (`docs/F5_portada_visual.md`).

- Menor: `npm run preview` falla con Astro 7 («Preview server process exited before becoming ready»); la build y el despliegue no se ven afectados.

## Propuestas de David (15-11-2026): triaje

Regla para todas: **los datos oficiales agregados se pueden preparar ya; los relatos sobre la guerra (R1) y la posguerra (R3) esperan a los revisores.** Las personas (víctimas, represaliados, exiliados, brigadistas) solo aparecen en cifras agregadas (guía §3).

| Tema | Fuente primaria abierta | Bloqueo | Bloque |
|---|---|---|---|
| Hambre de posguerra | INE: Movimiento Natural de la Población y Anuarios de 1935-1950 (mortalidad, precios, racionamiento) | Ninguno para los datos; el relato es R3. **Parte 1 hecha 15-11-2026** (defunciones 1934-1942, `docs/F4_mortalidad_1934_1942.md`); falta 1943-1950, mortalidad infantil y precios | A |
| Cárceles | Anuarios estadísticos del INE (población reclusa por año) | Datos sí; relato R3 | A |
| Alfabetización por edad (P3) | INE, Censo de 1930, Tomo III | Ninguno | A |
| Calles de toda España | INE, Callejero del Censo Electoral (por provincia, semestral) | Clasificar a los «personajes» exige criterio de revisores; el catálogo estatal de símbolos (RD 1040/2025) aún no está publicado | B |
| Fosas | datos.gob.es «Fosas o lugares de enterramiento» (e05232701); su enlace de descarga se ha dado por roto: verificar | Solo agregado por municipio (guía §4) y revisores | B |
| Cuerpos de seguridad | Gaceta/BOE: Guardia de Asalto, Guardia Civil, Policía Armada (1941), etc. | Normas de 1931-1936 sí; posteriores, R3 | A/B |
| Escuela pública, Iglesia y adoctrinamiento | BOE (leyes de 1938-1970), MANES (UNED, catálogo de manuales) | R3; «adoctrinamiento» es interpretación atribuida | B |
| Propiedades (Iglesia, tierra) | Gaceta (Ley de Confesiones 1933, Reforma Agraria 1932), BOE (devoluciones 1939-1940, Concordato 1953) | Hasta 1936 sí; después, R3 | A/B |
| Avance de la guerra | No hay geodatos oficiales del frente; cartografía de época del CNIG o del Ejército; historiografía | R1 | B |
| Intervención extranjera | FRUS (EE. UU., dominio público) y Documents on German Foreign Policy, serie D, vol. III (1950): confirmar derechos; Comité de No Intervención en la Gaceta | R1 | B |
| Brigadistas | SIDBRINT (Universitat de Barcelona): datos personales; solo cifras por país con permiso | R1 y derechos de la base | B |
| Exilio | PARES, CDMH; destinos agregados (Francia, México, URSS) | R3 y datos personales | B |
| Campos de concentración | Archivo General Militar (ICCP); listados historiográficos con derechos | R3 | B |
| Ejecuciones hasta 1978 | Consejos de guerra (archivos militares); BOE para los últimos casos | Muy sensible: R3, agregados y revisores | C |
| Represión | Estimaciones historiográficas atribuidas | R1/R3 | C |
| Lugares y actos de memoria hoy | Catálogos autonómicos (Memorial Democràtic, Andalucía), Ley 20/2022 | Revisores para la selección | B |
| Vivienda | INE, Censo de Viviendas de 1950; BOE: Instituto Nacional de la Vivienda (1939), Regiones Devastadas | R3 | B |
| Imágenes | Europeana, Biblioteca Digital Hispánica (carteles anónimos de 1936-1939: dominio público si son anónimos y publicados hace más de 70 años) | R2: derechos imagen por imagen | B |
| Libros | Catálogo BNE (solo metadatos y enlaces) | Selección con revisores para evitar sesgo | B |
| Música | Biblioteca Digital Hispánica, Europeana Sounds: solo enlaces y metadatos, nunca letras ni grabaciones con derechos | Derechos y equilibrio | C |
| «El florido pensil» | Libro de Andrés Sopeña Monsalve (1994) sobre la escuela nacionalcatólica: se cita, no se reproduce | Derechos de autor | B |

A = sin revisores · B = preparar ahora, publicar tras revisión · C = solo con revisores y guía ampliada

## Pendientes de David (no técnicos)

- 3 pruebas informales con usuarios (F2).
- 2 revisores para las narrativas (borrador del correo en `docs/F3_estado.md`).
- Anuncio público (borrador en `docs/F3_estado.md`).
- Comunicar a los autores del Atlas Electoral las 3 incoherencias detectadas (`docs/F4_capa_electoral.md`).
