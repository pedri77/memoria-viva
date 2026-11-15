# Backlog de ampliaciones

**Actualizado:** 15-11-2026. Este fichero es la lista de trabajo; `data/lagunas.json` es el registro público de lo que se buscó sin encontrarlo.

## Pendientes de revisores (decisión de David, 15-11-2026: se harán más adelante)

Requieren que antes haya al menos un revisor con formación en historia contemporánea, por lo delicado del tema o por los derechos.

| # | Ampliación | Por qué espera | Material ya disponible |
|---|---|---|---|
| R1 | **Tercera narrativa: las normas de las dos zonas durante la guerra (1936-1939)** | Es el tema más delicado: vocabulario y riesgo de simetrías artificiales (guía editorial, §1.4 y §2). | 8 acontecimientos del BOE de Burgos (`scripts/etl/eventos_burgos.py`), Gaceta de la zona republicana de julio y octubre de 1936 (`doc-gaceta-1936-07-19`, `-07-20`, `-10-07`, `-10-08`), Decreto 66 sobre el magisterio, bombardeos de Euskadi (Gogora, licencia sin verificar, en `data/raw/`). Lagunas: Boletín de la Junta de Defensa Nacional y texto completo de las normas. |
| R2 | **Imágenes de Europeana en las fichas** | Hay que revisar los derechos imagen por imagen; ninguna se publica sin una licencia abierta verificada. **Criterio de equilibrio (David, 15-11-2026):** si se usan archivos de partidos u organizaciones de un bando, se suman los equivalentes del otro (p. ej. fotos del Archivo Histórico del PCE en Europeana junto a fondos del Archivo General Militar o de FET y de las JONS en el Archivo General de la Administración). | Fuente catalogada en `docs/05_acceso_y_nuevas_fuentes.md`. API de Europeana con clave gratuita. |
| R3 | **Ampliación del periodo a 1939-1975** | Es otro proyecto por tamaño: necesita su propia guía editorial (represión, exilio, fosas) y revisores. | `mapSpainHist` cubre los censos de 1940 a 1970; los BOE de 1939-1975 tienen fichas `doc.php`. |

## Pendientes sin revisores (por orden de valor)

| # | Ampliación | Coste | Nota |
|---|---|---|---|
| ~~P1~~ | ~~Censo de 1930 por profesiones~~ | Hecho 15-11-2026 | `docs/F4_profesiones_1930.md`. Pendiente: usarlo en una narrativa (reforma agraria) y recuperar las páginas de Cádiz, Gerona y Vizcaya. |
| P2 | Prensa del día en los acontecimientos clave (enlaces a números de la BNE, sin citas) | Medio | El servidor de la BNE bloquea clientes automáticos: los enlaces se construyen desde el CSV oficial y se comprueban a mano. |
| P3 | Alfabetización por edad (mayores de 10 años), censo de 1930, tomo III | Alto: tablas regionales | Laguna `laguna-alfabetizacion-edad`. Localizadas: una tabla por provincia en el Tomo III (p. ej. td=103310); mismo método que P1. **Hecho 15-11-2026 para 1930 y 1920** (`docs/F4_alfabetizacion_edad_1930.md`). |
| P4 | Georreferenciación de mapas históricos del CNIG | Alto | Aplazado desde F2. |
| P5 | Enlaces Wikidata de los municipios de 1930 | Medio | Aplazado desde F2. |

## Hecho fuera de la lista

- 15-11-2026: portada «Del documento al mapa» y capa visual común (`docs/F5_portada_visual.md`).

- Menor: `npm run preview` falla con Astro 7 («Preview server process exited before becoming ready»); la build y el despliegue no se ven afectados.

## Propuestas de David (15-11-2026): triaje

Regla para todas: **los datos oficiales agregados se pueden preparar ya; los relatos sobre la guerra (R1) y la posguerra (R3) esperan a los revisores.** Las personas (víctimas, represaliados, exiliados, brigadistas) solo aparecen en cifras agregadas (guía §3).

| Tema | Fuente primaria abierta | Bloqueo | Bloque |
|---|---|---|---|
| Hambre de posguerra | INE: Movimiento Natural de la Población y Anuarios de 1935-1950 (mortalidad, precios, racionamiento) | Ninguno para los datos; el relato es R3. **Partes 1 y 2 hechas 15-11-2026** (defunciones 1934-1950 y mortalidad infantil 1934-1946, `docs/F4_mortalidad_1934_1950.md`); **coste de la vida 1939-1950 hecho 15-11-2026** (`docs/F4_coste_vida_1939_1950.md`); **racionamiento 1943 y 1948-1950 y salarios reales 1939-1950 hechos** (`docs/F4_racionamiento_1948_1950.md`, `docs/F4_series_nacionales_posguerra.md`) | A |
| Cárceles | Anuarios estadísticos del INE (población reclusa por año) | Datos sí; relato R3. **Serie nacional 1922-1950 hecha 15-11-2026** (`docs/F4_series_nacionales_posguerra.md`) | A |
| Alfabetización por edad (P3) | INE, Censo de 1930, Tomo III | Ninguno; **hecho 1920 y 1930** | A |
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
| Archivos de partidos y sindicatos | AHPCE (fotos de la guerra en Europeana; prensa clandestina en la BVPH), Fundación Pablo Iglesias (PSOE), Fundación Anselmo Lorenzo (CNT); contrapeso: Archivo General Militar (Ávila), fondos de FET y de las JONS en el AGA | Equilibrio entre bandos (criterio de David); derechos por documento; Patrimonio Digital Complutense veta en robots.txt /s/patrimonio/item* | B |
| Ayuntamientos y fondos públicos para memoria democrática hoy (propuesta de David, 15-11-2026) | BDNS / infosubvenciones (concesiones por beneficiario; p. ej. convocatoria BDNS 907882 de fosas y exhumaciones, RD 866/2025 de ayudas directas a entidades locales y a la FEMP); portal de transparencia de cada ayuntamiento; UE: programa CERV «European Remembrance» (resultados en el Funding & Tenders Portal; no se ha encontrado aún ningún ayuntamiento español beneficiario) | Datos actuales de entidades públicas, sin datos personales: se puede hacer sin revisores como capa de datos (mapa de importes por municipio y año). Qué publica cada ayuntamiento exige revisar web a web (respetando robots.txt) | A |
| Imágenes | Europeana, Biblioteca Digital Hispánica (carteles anónimos de 1936-1939: dominio público si son anónimos y publicados hace más de 70 años) | R2: derechos imagen por imagen | B |
| Libros | Catálogo BNE (solo metadatos y enlaces) | Selección con revisores para evitar sesgo | B |
| Música | Biblioteca Digital Hispánica, Europeana Sounds: solo enlaces y metadatos, nunca letras ni grabaciones con derechos | Derechos y equilibrio | C |
| «El florido pensil» | Libro de Andrés Sopeña Monsalve (1994) sobre la escuela nacionalcatólica: se cita, no se reproduce | Derechos de autor | B |

A = sin revisores · B = preparar ahora, publicar tras revisión · C = solo con revisores y guía ampliada

- 15-11-2026: facsímiles de la Gaceta, cronología rediseñada y datos al pasar el ratón (`docs/F5_facsimiles_y_cronologia.md`). Pendiente: llevar el mismo estilo a archivo, fichas de lugar, datos y metodología.

- Reforma agraria, aplicación: tablas del Anuario de 1934 localizadas (`laguna-aplicacion-reforma-agraria`); mismo método de transcripción que P1. Alimentaría el relato «La tierra» de la portada.

## Pendientes de David (no técnicos)

- 3 pruebas informales con usuarios (F2).
- 2 revisores para las narrativas (borrador del correo en `docs/F3_estado.md`).
- Anuncio público (borrador en `docs/F3_estado.md`).
- Comunicar a los autores del Atlas Electoral las 3 incoherencias detectadas (`docs/F4_capa_electoral.md`).
