# 05 · Vías de acceso y nuevas fuentes

**Fecha de consulta:** 14-11-2026 · **Alcance:** piloto 1931-1939 · **Método:** lectura de documentación y robots.txt, y de 1 a 3 peticiones por endpoint con `curl`. No se descargó ningún fondo completo, no se rastreó ningún visor y no se eludió ninguna protección.

**Leyenda de verificación**

- **[V]** verificado hoy con una petición propia (código HTTP o respuesta del endpoint).
- **[S]** solo consta en fuentes secundarias (web de la institución, buscador, artículo) y no se ha probado el endpoint.
- **[X]** probado y bloqueado o caído.

## 0. Corrección importante al contexto de partida

El contexto decía que el robots.txt de boe.es «no bloquea /buscar/ salvo parámetros de idioma». **No es así [V]:** el robots.txt actual incluye

```
Disallow: /buscar/gazeta.php?
Disallow: /datos/pdfs/
```

Es decir: los resultados de búsqueda de la Gazeta y los PDF del diario están vetados a agentes automáticos. Cualquier flujo automatizado sobre la Gazeta queda descartado. Solo caben uso humano o solicitud formal (ver 1.1 y 4).

---

## 1. Fuentes «solo buscador»: vía estructurada y flujo recomendado

### (a) Tabla resumen

| Fuente | Vía estructurada encontrada | Endpoint probado | Licencia | Vía recomendada | Esfuerzo |
|---|---|---|---|---|---|
| **BOE Gazeta 1931-1939** | Ninguna. API de datos abiertos solo desde 1960. | `/gazeta/dias/1931/04/15/` → 404 [V]. robots veta `/buscar/gazeta.php?` y `/datos/pdfs/` [V] | Aviso legal con «Condiciones de reutilización» (Ley 37/2007); texto no leído completo [S] | Curación humana de una lista cerrada de disposiciones (50-150 para el piloto) + solicitud formal de volcado a la AEBOE. Para normas clave, Wikisource/Wikidata como capa de texto | Medio (manual) |
| **PARES / CDMH** | Archives Portal Europe (APE) API, con clave, solo para instituciones que la hayan habilitado | Búsqueda APE devuelve 403 a curl [X]. API no probada (requiere registro) | Metadatos APE vía API: CC0 [S, nota del Ministerio de Cultura]. Imágenes PARES: dominio público libre, resto uso privado | 1) Registrar cuenta APE y comprobar si los archivos estatales españoles autorizan la API. 2) Si no, fichas curadas a mano. 3) Solicitud formal al CDMH (borrador en 4.2) | Bajo (probar) / Medio |
| **BNE Hemeroteca Digital** | **Europeana API** (dataset `9200302_Ag_EU_TEL_a0597_Newspapers_Spain`): 21.693 números 1931-1939 con metadatos por número y enlace al visor BNE. Manifiesto IIIF de Europeana por número | Europeana Search API 200 [V]; manifiesto IIIF 200 sin lienzos (las imágenes siguen en BNE) [V]; IIIF Search API del número → 404 «no record» (sin texto completo en Europeana) [V] | **CC BY-NC-SA 4.0** en Europeana para este dataset [V] | Metadatos por número desde Europeana (API oficial) + texto completo desde los ZIP del CSV de datos.gob.es ya localizado (CC BY 4.0). Discrepancia de licencia a resolver: ver nota 1 | Bajo |
| **BNE Biblioteca Digital Hispánica** | **Europeana** (dataset `2022717_Ag_ES_Hispana_Biblioteca_Nacional`, 3.430 objetos 1931-1939, 2.879 imágenes) y **Hispana OAI-PMH set `bdh`** | `bdh-rd.bne.es/oai/oai.cmd` y `bdh.bne.es/bnesearch/oai` → 403 página de bloqueo [X]. `iiif.bne.es` no responde [X]. Hispana OAI 200 [V]. Europeana 200 [V] | CC BY-NC-SA 4.0 en Europeana [V] | Metadatos vía Europeana o Hispana OAI (set `bdh`). `edmIsShownBy` apunta a `bdh-rd.bne.es/pdf.raw?...&jpeg=true`, pero ese host bloquea clientes automáticos: imagen solo por enlace o descarga manual | Bajo |
| **Catálogo BNE (SRU/Z39.50)** | No hallado SRU público. `catalogo.bne.es` es Alma/Primo con `Disallow: /discovery/search` y `Crawl-delay: 10` [V] | Solo robots | n/d | No usar para el piloto. Si hiciera falta un registro bibliográfico, Wikidata o Europeana | n/a |
| **Biblioteca Virtual de Prensa Histórica (BVPH)** | **Hispana OAI-PMH sets `esebvph`, `esebvph1`-`4`, `esebvph1a`...** y **Europeana** (proveedor «Virtual Library of Historical Press», 1.735.320 objetos; solo 117 cabeceras con fecha 1931-1939 como objeto de título) | OAI propio `prensahistorica.mcu.es/.../oai...` → 503 «mantenimiento» y luego sin respuesta [X]. Hispana OAI 200 [V]. Europeana 200 [V] | **CC BY 4.0** en Europeana para BVPH [V] | Hispana OAI (set `esebvph*`) o Europeana API para el inventario de cabeceras y números; imágenes enlazadas al visor (`edmIsShownBy` = `prensahistorica.mcu.es/i18n/catalogo_imagenes/imagen_id.do?idImagen=...`). Reintentar el OAI propio otro día | Bajo |

**Nota 1 (licencia BNE).** El mismo material sale con dos licencias según el canal: CC BY 4.0 en el CSV de datos.gob.es y CC BY-NC-SA 4.0 en Europeana. Para un proyecto personal, público y no comercial ambas valen, pero la ficha de cada objeto debe guardar la licencia **del canal por el que se obtuvo** y no mezclar. Recomendación: texto completo y metadatos de título desde datos.gob.es (CC BY), y usar Europeana solo como índice por número y fecha, citando NC-SA si se publica su metadato tal cual.

### (b) Detalle por fuente

#### 1.1 BOE · Gazeta de Madrid / Gaceta de la República / BOE de Burgos

- No hay vía estructurada. Las páginas de sumario por día no existen para la Gazeta (404) y los PDF y búsquedas están vetados en robots.txt [V].
- **Flujo legítimo propuesto (humano asistido):**
  1. Lista cerrada de disposiciones del piloto a partir de fuentes secundarias (Wikipedia/Wikidata «leyes de la Segunda República», bibliografía) con fecha y número de Gazeta.
  2. Una persona abre cada una en el navegador, guarda el PDF y anota la URL del documento y la fecha de consulta. A unos 2 minutos por pieza, 100 disposiciones ≈ 3-4 horas.
  3. El texto se toma de Wikisource cuando exista (CC BY-SA, dominio público el original) y se enlaza el PDF del BOE como fuente primaria.
  4. En paralelo, solicitud formal a la AEBOE de un volcado (metadatos y PDF) de la Gazeta 1931-1939, citando la Ley 37/2007 de reutilización. No se adjunta borrador propio: puede adaptarse el de la BNE (4.1).
- Las disposiciones son normas oficiales, excluidas de propiedad intelectual (art. 13 LPI) [S]. El límite es técnico y de condiciones de la sede, no de derechos.

#### 1.2 PARES / CDMH

- PARES no expone OAI (`/oai` 404, ya verificado). APE recibe sus EAD; la API de APE da metadatos con CC0 **solo si la institución lo habilita** en su panel (valor por defecto: deshabilitado) [S, nota del Ministerio de Cultura sobre la API de APE].
- La búsqueda web de APE devuelve 403 a curl [X]; no se insiste.
- **Siguiente paso:** registrar una cuenta en archivesportaleurope.net, pedir la clave y hacer una consulta de prueba por el repositorio CDMH. Si no está habilitado, pedirlo por escrito (borrador 4.2, que pide también que se active la API en APE).
- Mientras tanto: fichas a mano con signatura y URL de PARES, sin imagen salvo dominio público.

#### 1.3 BNE Hemeroteca Digital y BDH

- Europeana es el agregador oficial de ambas y su API es pública (clave gratuita; para las pruebas se usó la clave de demostración `api2demo`). Consulta de ejemplo verificada:
  `api.europeana.eu/record/v2/search.json?query=*&qf=edm_datasetName:9200302_Ag_EU_TEL_a0597_Newspapers_Spain&qf=YEAR:[1931 TO 1939]` → 21.693 resultados, cada uno un número de periódico con fecha y enlace `hemerotecadigital.bne.es/details.vm?q=id:...` [V].
- Búsqueda «guerra civil», país España, 1931-1939: 13.443 objetos, 11.740 de la BNE y el resto de ICGC (688), Museu Postal de Barcelona (260), Memòria Digital de Catalunya (212), Filmoteca de Catalunya (177), Biblioteca Digital de Madrid (125) [V].
- Los endpoints propios de la BNE (OAI de BDH, IIIF, SPARQL) están bloqueados o caídos [X]. No se insiste.
- **Flujo:** Europeana para índice e imagen en miniatura; ZIP de texto de datos.gob.es para el texto; visor BNE como enlace de consulta. Para imágenes en alta, descarga manual por una persona de las páginas que se vayan a mostrar (decenas, no miles), o solicitud formal (4.1).

#### 1.4 Biblioteca Virtual de Prensa Histórica

- El OAI propio estaba en mantenimiento (503) y después no respondía [X]. Hispana la recolecta y publica sus registros en los sets `esebvph*` [V], y Europeana la ofrece con CC BY 4.0 [V].
- **Flujo:** Hispana OAI o Europeana para el inventario. Para 1931-1939 Europeana solo indexa 117 objetos a nivel de cabecera, así que el nivel de número habrá que tomarlo de Hispana OAI (comprobar en la siguiente sesión con `ListRecords` + `set=esebvph4` y filtro por fecha).

---

## 2. Archivos municipales y autonómicos

### 2.1 Municipales

| Archivo | URL | Qué hay del periodo | Licencia | Vía de acceso | Estado |
|---|---|---|---|---|---|
| **Madrid · Memoria de Madrid (Archivo de Villa, Hemeroteca Municipal, Biblioteca Histórica, Museo de Historia)** | memoriademadrid.es | 260.803 registros recolectados por Hispana (15-07-2025); prensa, carteles, fotografía | `dc:rights` «Creative Commons» sin versión en Hispana [V]; condiciones propias no leídas | `memoriademadrid.es/oai` devuelve 403 de Akamai a curl [X]. **Vía legítima: Hispana OAI set `bdmmadrid`** (200, registros en oai_dc) [V] | Usable |
| **Madrid · datos.madrid.es** | datos.madrid.es | **«memoria de Madrid. Publicaciones periódicas de la Guerra Civil»**: 691 cabeceras de ambos bandos, 619 fechadas 1936-1939; CSV, XLSX, RDF, publicado 10-11-2026. Además «memoria de Madrid. Carteles» (148491), «Tarjetas postales» (879311), «Placas Stolpersteine», «Placas conmemorativas» | **CC BY 4.0** (publicaciones de Guerra Civil) [V]; resto: listados en el catálogo [V], licencia no comprobada | API CKAN `datos.madrid.es/api/3/action/package_show` [V] | **P0** |
| **Barcelona · Arxiu Municipal** | catalegarxiumunicipal.bcn.cat | 410.000 registros, 30 % digitalizados, 77.000 fotografías, 14.000 carteles y planos [S] | Usos comerciales o de difusión requieren permiso del centro [S] | Solo catálogo web. No se halló OAI ni dataset en Open Data BCN | Manual / solicitud |
| **Barcelona provincia · Xarxa d'Arxius Municipals (Diputació)** | dadesobertes.diba.cat/datasets/arxius-municipals-digitals | Directorio de arxius municipals digitals | CC0 [S] | Dataset de directorio, no de fondos | Útil para localizar |
| **Valencia · Arxiu Històric Electoral (ARGOS, GVA)** | argos.gva.es/ahe | Resultados electorales históricos de la Comunitat y otras CCAA, descarga de ficheros | No consta | Formulario de descarga de ficheros; el servidor devolvió 503 [X] | Reintentar |
| **Valencia · Centro Documental de la Memoria Democrática Valenciana** | (set Hispana `democratica`) | Fondos de memoria democrática | No comprobada | **Hispana OAI set `democratica`** [V, el set existe] | Explorar |
| **Zaragoza · Archivo, Biblioteca y Hemeroteca Municipal** | zaragoza.es/archivo | 325.000 documentos digitales; Hemeroteca Digital con Heraldo de Aragón 1903-1941, El Lunes 1933-1937, Hoja Oficial del Lunes 1936-1941 [S] | Visualización y descarga libres; publicación y difusión requieren autorización (archivo@zaragoza.es) [S] | Buscador NUBA; el dataset abierto del archivo solo cubre cuadro de clasificación, no fondos [S] | Manual / solicitud |
| **Aragón · DARA Historia Reciente** | dara-aragon.es/dara/memoriademocratica | 82.531 descripciones de represión 1936-1977; 11.533 expedientes digitalizados (576.000 imágenes); 1.067 fotos de la Fototeca de la Diputación de Huesca [S] | No comprobada; datos personales | Buscador web | P2 (nominal) |
| **Bilbao · Bilbao Liburutegi Digitala** | bilbao.eus/bld | Repositorio digital de las bibliotecas municipales, acceso abierto [S] | No comprobada | Probable DSpace con OAI (no probado) | Explorar |
| **Málaga · Archivo Municipal** | (MediaSearch) | Catálogo con imagen digitalizada en la mayoría de documentos [S] | No comprobada | Buscador web | Manual |
| **Sevilla · Hemeroteca/Archivo Municipal** | n/d | No se halló vía estructurada en esta sesión | n/d | n/d | Pendiente |

### 2.2 Autonómicos

| Archivo / portal | URL | Qué hay | Licencia | Vía | Estado |
|---|---|---|---|---|---|
| **Arxiu Nacional de Catalunya · Arxius en línia** | arxiusenlinia.cultura.gencat.cat | 128 centros, 16,5 M objetos digitales; fondos ANC1-1 Generalitat (Segona República), Brangulí, Boix (guerra), Col·lecció Fotogràfica de la Guerra Civil, Aviazione Legionaria [S] | Aviso legal: reproducción privada para investigación o docencia, **sin difusión** [S]. Excepción: lista de autores en dominio público publicada por el ANC [S] | Portal web. Parte de la fotografía llega a Europeana («Europeana Photography») y al repositorio Calaix (`calaix.gencat.cat`, DSpace) | Solo dominio público |
| **Memòria Digital de Catalunya (CSUC)** | mdc.csuc.cat | Cartells del Pavelló de la República (>1.000 de II República y guerra), adhesius, Cartes del Temps del SMC 1921-1939 (22.000 docs) [S] | Por colección | **OAI-PMH `mdc.csuc.cat/oai/oai.php`** 200 [V] | Usable |
| **Generalitat de Catalunya · Dades obertes** | analisi.transparenciacatalunya.cat | `x8yr-e7bz` Resultats electorals Segona República per municipis; `u2ix-2jr6` Cens de persones desaparegudes durant la Guerra Civil; `6js6-vud6` Fosses comunes; `t3s8-kna9` Catàleg de publicacions de la Generalitat 1931-1939; `r2n5-8zfj` Camps i refugis de refugiats a França 1939 [V] | «See Terms of Use» en Socrata [V]; las condiciones de gencat son equivalentes a CC BY [S] | API Socrata (CSV, JSON) [V] | **P0** (electoral), P1 (resto) |
| **Euskadi · Gogora / Open Data Euskadi** | opendata.euskadi.eus | Víctimas mortales de la guerra civil en Euskadi (JSON 14,6 MB, actualización semanal); Bombardeos de la Guerra Civil (GeoJSON, CSV); Exhumaciones; Fosas [V el JSON responde 200] | **CC BY 4.0** según datos.gob.es [S] | Descarga directa | **P0** (bombardeos), P1 (víctimas) |
| **Euskadi · Elecciones Segunda República** | hauteskundeak.euskadi.eus | Resultados 1931, 1933 y 1936 por municipio y por distrito y sección de Álava, Gipuzkoa, Bizkaia y Bilbao, en CSV [S] | Open Data Euskadi (CC BY 4.0) [S] | CSV descargables | P0 (ya incluido en el Atlas UPF) |
| **Andalucía · Fosas comunes de la Guerra Civil** | juntadeandalucia.es/datosabiertos | CSV, JSON, XLSX; modificado 11-08-2026 | **CC BY 4.0** [V] | API CKAN [V] | P1 |
| **Galicia · Nomes e Voces** | vitimas.nomesevoces.net | Base de víctimas de la represión 1936-1939 en CSV (`/media/base-datos.csv`, última modificación 05-02-2015) [V el fichero responde 200] | CC BY-NC (atribución, sin lucro) según nota de 2009 [S]; enlace «licenzas de uso» en la web | Descarga directa del CSV | P1 (nominal) |
| **Navarra · Fondo Documental de la Memoria Histórica (UPNA)** | memoria-oroimena.unavarra.es | 29.095 hechos represivos de 22.555 personas; informes «memoriapaper(ak)» con tablas agregadas [S] | No declarada | Buscador web e informes PDF. Sin dataset abierto hallado | Solicitud / agregados |
| **Navarra · Oroibidea** | oroibidea.es | Buscador de víctimas, mapas por población (Gobierno de Navarra) [S] | No comprobada | Buscador | Explorar |

**Cautela sobre datos nominales.** Las bases de víctimas contienen nombres de personas fallecidas. El RGPD no protege a los difuntos, pero hay familiares vivos y campos sensibles (filiación política, causa de muerte). Para el piloto se recomienda publicar **agregados municipales** y enlazar a la fuente oficial para la consulta nominal.

---

## 3. Nuevas fuentes (desde F032)

| ID | Fuente | URL | Tema | Años | Licencia | Acceso | Prioridad | Por qué |
|---|---|---|---|---|---|---|---|---|
| **F032** | Atlas Electoral de la Segunda República (UPF: Rodon, Vall-Prat, Martín Álvarez) | doi.org/10.34810/DATA3274 · tonirodon.cat/second-republic-atlas · github.com/tonirc/spain2Rep | Resultados municipales de las elecciones generales | 1931, 1933, 1936 (1936 completo; 1933 y 1931 en curso según README) | En CORA; licencia exacta **no verificada**: el repositorio pone un reto antibot (Anubis) a curl [X] | Descarga manual del dataset en CORA por una persona, o paquete R `spain2Rep` | **P0** | Única base municipal de toda España (~9.000 municipios), con códec y fuentes por municipio |
| **F033** | mapSpainHist · Historical municipal boundaries of Spain 1900-2001 (Vall-Prat) | zenodo.org/records/23663208 | Límites municipales y provinciales por censo, circunscripciones de 1931, 1933, 1936; censos 1842-2011 | 1900-2001 (incluye 1930) | **CC BY 4.0** (datos), MIT (paquete) [S, página de Zenodo] | GeoPackage 103 MB, TopoJSON 6,5 MB, CSV | **P0** | Cartografía base del atlas con los municipios de 1930 y las circunscripciones republicanas, compatible con F032 |
| **F034** | Resultats electorals de la Segona República a Catalunya per municipis (Generalitat) | analisi.transparenciacatalunya.cat/d/x8yr-e7bz | Elecciones a Cortes, Parlament y referéndums | 1931-1936 | Términos de uso gencat [V «See Terms of Use»] | API Socrata CSV/JSON [V] | P1 | Detalle catalán (incluye votos a favor y en contra de referéndums); integrado parcialmente en F032 |
| **F035** | Resultados Segunda República en Euskadi | hauteskundeak.euskadi.eus | Resultados por municipio, distrito y sección | 1931, 1933, 1936 | Open Data Euskadi [S] | CSV | P1 | Nivel de sección censal; validación de F032 |
| **F036** | Memoria de Madrid · Publicaciones periódicas de la Guerra Civil | datos.madrid.es/dataset/215863-0-... | 691 cabeceras de prensa de guerra | 1936-1939 (619) | **CC BY 4.0** [V] | CSV/XLSX/RDF vía CKAN [V] | **P0** | Inventario limpio y con licencia de la prensa de ambos bandos |
| **F037** | Memoria de Madrid · Carteles | datos.madrid.es/dataset/148491-0-memoria-de-madrid-carteles | Carteles municipales | multiperiodo | No comprobada | CKAN | P1 | Complementa F005 carteles |
| **F038** | Hispana OAI-PMH (agregador del Ministerio de Cultura) | hispana.mcu.es/i18n/oai/oai_hispana.mcu.es.do | 130 sets: BVPH, BDH, Memoria de Madrid, Galiciana, BV Defensa, CDMD Valenciana, Memoria Digital Vasca, BV Andalucía, Bivaldi, BiNaDi | multiperiodo | Por registro (`dc:rights`) | **OAI-PMH 200** [V] | **P0** | Una sola vía estándar para recolectar metadatos de casi todas las fuentes «solo buscador» |
| **F039** | Europeana · dataset Newspapers Spain (BNE) | api.europeana.eu, `edm_datasetName:9200302_Ag_EU_TEL_a0597_Newspapers_Spain` | Números de prensa por fecha | 1931-1939: 21.693 | CC BY-NC-SA 4.0 [V] | Search API + manifiesto IIIF [V] | P0 | Índice día a día de la prensa BNE (ver nota 1) |
| **F040** | Bombardeos de la Guerra Civil en Euskadi (Gogora) | opendata.euskadi.eus | Bombardeos geolocalizados | 1936-1937 | CC BY 4.0 [S] | GeoJSON/CSV | **P0** | Capa de eventos geolocalizada lista para el mapa |
| **F041** | Víctimas mortales de la guerra civil en Euskadi (Gogora) | opendata.euskadi.eus/contenidos/ds_general/victimas_guerra_civil/ | Víctimas de ambos bandos | 1936-... | CC BY 4.0 [S] | JSON/XML/XLSX [V 200] | P1 | Agregable por municipio |
| **F042** | Cens de persones desaparegudes durant la Guerra Civil (Generalitat) | analisi.transparenciacatalunya.cat/d/u2ix-2jr6 | Desaparecidos, frentes, unidades | 1936-1939 | Términos gencat [V] | Socrata [V] | P1 | Lugares de desaparición (frentes) agregables |
| **F043** | Fosses comunes a Catalunya | analisi.transparenciacatalunya.cat/d/6js6-vud6 | Fosas | 1936-... | Términos gencat [V] | Socrata [V] | P1 | Sustituye en Cataluña al dataset estatal sin actualizar (F013) |
| **F044** | Fosas comunes de la Guerra Civil (Junta de Andalucía) | juntadeandalucia.es/datosabiertos/portal/dataset/fosas-comunes-de-la-guerra-civil | Fosas | 1936-... | **CC BY 4.0** [V] | CSV/JSON [V] | P1 | Igual que F043 para Andalucía |
| **F045** | Cartografía de la desaparición forzada en Andalucía | andalucia.desaparicionforzada.com | Fosas, víctimas, traslados a Cuelgamuros, campos de concentración | 1936-1951 | Bases PDDL 1.0, datos CC BY 4.0, mapas CC BY-NC-SA [S] | SHP, GPKG, CSV | P2 | Geodatos ya depurados; fuente asociativa, validar contra F044 |
| **F046** | Nomes e Voces | vitimas.nomesevoces.net | Víctimas de la represión en Galicia | 1936-1939 | CC BY-NC [S] | CSV [V 200] | P1 | Única base gallega descargable |
| **F047** | Catàleg de publicacions de la Generalitat 1931-1939 | analisi.transparenciacatalunya.cat/d/t3s8-kna9 | Publicaciones oficiales | 1931-1939 | Términos gencat [V] | Socrata [V] | P2 | Documentación institucional republicana |
| **F048** | Camps i refugis amb refugiats espanyols a França (1939) | analisi.transparenciacatalunya.cat/d/r2n5-8zfj | Exilio, campos | 1939 | Términos gencat [V] | Socrata [V] | P1 | Capa del exilio de 1939 para el mapa |
| **F049** | IISG Amsterdam (CNT, FAI, SIA, FIJL; 2.000 fotos CNT) | iisg.amsterdam/en/collections/using/machine-access | Archivos anarquistas y sindicales | 1931-1939 | Metadatos **CC0** [S]; objetos según depositante | **OAI-PMH 200** [V]; SRU responde (0 resultados para «spain civil war», revisar sintaxis CQL) [V] | P1 | Archivo de primer orden con API abierta |
| **F050** | Biblioteca Virtual de Defensa | bibliotecavirtual.defensa.gob.es | Diario Oficial del Ministerio de la Guerra, boletines de los sublevados 1936-1939, cartografía | 1888-1978 | No comprobada | **OAI-PMH 200** [V]; set Hispana `bvdefensa` (194.160 registros) [V] | P1 | Fuente oficial militar de ambos lados con OAI |
| **F051** | Memòria Digital de Catalunya | mdc.csuc.cat | Cartells del Pavelló de la República, Cartes del Temps 1921-1939, adhesius | 1931-1939 | Por colección | **OAI-PMH 200** [V] | P1 | Carteles del periodo con OAI |
| **F052** | Biblioteca Virtual Miguel de Cervantes (portal Exilio, Fundación Pablo Iglesias, Archivo Carlos Esplá) | cervantesvirtual.com | Exilio republicano, prensa, correspondencia | 1931-1975 | Por obra | **OAI-PMH 200** [V]; SPARQL en `data.cervantesvirtual.com/bvmc-lod/repositories/data` responde [V] (0 obras con fecha 1937 por esa propiedad) | P2 | Exilio y documentos de la Fundación Pablo Iglesias |
| **F053** | Estadísticas Históricas de España, siglos XIX-XX (Fundación BBVA, Carreras y Tafunell, 2005) | fbbva.es/publicaciones/estadisticas-historicas-de-espana-siglos-xix-xx | Población, economía, elecciones y política (cap. 14), precios | 1800-2000 | Libro en PDF gratuito; derechos reservados [S] | PDF; Excel solo en el CD-ROM original | P1 | Series nacionales y provinciales para contexto; extraer cifras con cita, no redistribuir tablas |
| **F054** | HIPGDAC-ES · rejillas de población histórica (Goerlich) | doi.org/10.5281/zenodo.13916658 | Población en rejilla 1 km y 100 m | 1900-2021 (incluye 1930 y 1940) | Datos en Zenodo, licencia del depósito por confirmar; artículo CC BY-NC-ND [S] | GeoTIFF/GPKG | P2 | Densidad de población de 1930 para mapas de calor |
| **F055** | Wikimedia Commons · Category:Spanish Civil War y Category:Second Spanish Republic | commons.wikimedia.org | Fotografía, carteles, mapas | 1931-1939 | Libre por fichero (PD, CC BY, CC BY-SA) | API MediaWiki [V]: 570 ficheros y 74 subcategorías en la raíz de Spanish Civil War; 110 y 35 en Second Spanish Republic | **P0** | Imágenes con licencia libre ya verificada por fichero; recorrer subcategorías |
| **F056** | Wikidata · eventos de la Guerra Civil | query.wikidata.org | Batallas, eventos, personas, lugares | 1931-1939 | CC0 | SPARQL [V]: 120 entidades con `part of` Guerra Civil (Q10859) | **P0** | Columna vertebral de identificadores y coordenadas para el atlas |
| **F057** | Archivo Histórico Electoral (ARGOS, GVA) | argos.gva.es/ahe | Elecciones | histórico | No consta | Descarga de ficheros; 503 hoy [X] | P2 | Confirmar si incluye 1931-1936 |
| **F058** | Francisco Villamil · Data resources for Spain | franvillamil.com/data_spain.html | Scripts y datos de víctimas, sindicatos y elecciones de los años 30 (Asturias 1936 en CSV, Lugo 1936) | 1930-1942 | Cada fuente con su licencia; scripts propios [S] | CSV y R | P2 | Atajos ya depurados y guía de fuentes por provincia |
| **F059** | DARA Historia Reciente (Aragón) | dara-aragon.es/dara/memoriademocratica | Represión, consejos de guerra, fotos de la Fototeca de Huesca | 1936-1977 | No comprobada | Buscador | P2 | Fotografía de guerra en Huesca y documentación judicial |

Fuentes del enunciado no ampliadas en esta sesión por falta de vía estructurada clara: Hoover Institution y Marx Memorial Library (solo catálogo y visitas), Arolsen Archives (pertinente sobre todo para deportados de 1940-1945), anuarios del INE digitalizados (INEbase Historia responde 200 [V], son escaneados y ya estaban en F009-F010).

---

## 4. Borradores de solicitudes formales (no enviados)

### 4.1 Biblioteca Nacional de España

> **Para:** Biblioteca Nacional de España, Departamento de Proceso Técnico / Biblioteca Digital (dirección que indique la sede electrónica para reutilización de información)
> **Asunto:** Solicitud de reutilización de datos de la Hemeroteca Digital y la Biblioteca Digital Hispánica (1931-1939) para un proyecto divulgativo sin ánimo de lucro
>
> Buenos días:
>
> Me dirijo a ustedes como responsable del proyecto personal y no comercial «España: Memoria Viva», un atlas documental en línea de la historia de España cuyo piloto cubre 1931-1939. El proyecto publica cada objeto con su fuente y su licencia, y su código y datos son abiertos.
>
> Ya reutilizamos el conjunto «Hemeroteca digital. Texto completo» publicado por la BNE en datos.gob.es con licencia CC BY 4.0. Para no generar tráfico automatizado sobre sus servidores, cuyo robots.txt no lo permite, solicitamos, al amparo de la Ley 37/2007 sobre reutilización de la información del sector público:
>
> 1. Un volcado de metadatos (Dublin Core, MARC o EDM) de los números de prensa de la Hemeroteca Digital fechados entre el 1 de enero de 1931 y el 31 de diciembre de 1939, con su identificador y URL del visor.
> 2. Un volcado equivalente de los objetos de la Biblioteca Digital Hispánica del mismo periodo (carteles, fotografías, mapas).
> 3. Si existe, acceso al servicio OAI-PMH o IIIF de la BDH, o la indicación de la vía preferida por la BNE para acceder a las imágenes de forma programática.
> 4. Aclaración de la licencia aplicable: en datos.gob.es figura CC BY 4.0 y en Europeana el mismo material figura con CC BY-NC-SA 4.0.
>
> Nos comprometemos a citar a la BNE en cada objeto, a enlazar siempre a su visor y a no redistribuir imágenes en alta resolución sin autorización.
>
> Quedo a su disposición para cualquier aclaración.
>
> Atentamente,
> [Nombre] · [correo de contacto del proyecto] · [URL del repositorio]

### 4.2 Centro Documental de la Memoria Histórica (Salamanca)

> **Para:** Centro Documental de la Memoria Histórica, Subdirección General de los Archivos Estatales
> **Asunto:** Solicitud de acceso a descripciones archivísticas en formato estructurado (1931-1939)
>
> Buenos días:
>
> En el marco del proyecto divulgativo sin ánimo de lucro «España: Memoria Viva», atlas documental en línea cuyo piloto cubre la Segunda República y la Guerra Civil, solicitamos:
>
> 1. Las descripciones archivísticas (EAD o exportación de PARES) de los fondos del CDMH relativos a 1931-1939 que sean públicas, en particular: Incautados (Sección Político-Social), Carteles, Fotografía y Prensa de guerra.
> 2. Si el CDMH publica ya esas descripciones en Archives Portal Europe, que se valore habilitar el acceso por la API de APE para su reutilización como datos abiertos.
> 3. Información sobre qué imágenes digitalizadas se consideran de dominio público según la pregunta 9 de las FAQ de PARES, y el procedimiento para solicitar autorización de difusión de las demás.
>
> No solicitamos datos personales ni expedientes nominales. Publicaremos solo metadatos descriptivos y enlaces a PARES, con cita de signatura y fecha de consulta.
>
> Atentamente,
> [Nombre] · [correo] · [URL del repositorio]

### 4.3 Archivo de Villa / Biblioteca Digital Memoria de Madrid

> **Para:** Biblioteca Digital memoriademadrid (bdigitalmemoria@madrid.es), con copia al Archivo de Villa
> **Asunto:** Acceso al servicio OAI-PMH y condiciones de reutilización de imágenes (1931-1939)
>
> Buenos días:
>
> Desde el proyecto sin ánimo de lucro «España: Memoria Viva» ya reutilizamos el conjunto «memoria de Madrid. Publicaciones periódicas de la Guerra Civil» de datos.madrid.es (CC BY 4.0). Querríamos ampliar el trabajo a carteles, fotografías y documentos del Archivo de Villa de 1931-1939 y les solicitamos:
>
> 1. Acceso al servicio OAI-PMH de memoriademadrid.es (`/oai`), que actualmente rechaza las peticiones automatizadas, o confirmación de que la vía preferida es la recolección de Hispana (set `bdmmadrid`).
> 2. La versión exacta de la licencia Creative Commons que aplican a las imágenes (en Hispana figura solo «Creative Commons»).
> 3. Si existe, un listado o exportación de los documentos digitalizados del Archivo de Villa fechados entre 1931 y 1939.
>
> Citaremos la institución en cada objeto y enlazaremos siempre a su ficha original.
>
> Atentamente,
> [Nombre] · [correo] · [URL del repositorio]

---

## 5. URLs consultadas (14-11-2026)

Verificadas con petición propia:

- https://prensahistorica.mcu.es/robots.txt (sin respuesta), /es/oai/oai.do y /i18n/oai/oai.cmd (503), /i18n/oai/oai_prensahistorica.mcu.es.do (sin respuesta)
- https://bdh-rd.bne.es/oai/oai.cmd, https://bdh.bne.es/bnesearch/oai, https://bdh-rd.bne.es/viewer.vm (403), https://iiif.bne.es/ (sin respuesta)
- https://hemerotecadigital.bne.es/robots.txt, https://catalogo.bne.es/robots.txt
- https://api.europeana.eu/record/v2/search.json (varias consultas con `api2demo`), https://api.europeana.eu/record/v2/9200302/BibliographicResource_3000059474668.json
- https://iiif.europeana.eu/presentation/9200302/BibliographicResource_3000059474668/manifest y /search
- https://hispana.mcu.es/es/oai/oai.cmd?verb=Identify, https://hispana.mcu.es/i18n/oai/oai_hispana.mcu.es.do (ListSets, ListRecords set=bdmmadrid)
- https://www.boe.es/robots.txt, https://www.boe.es/informacion/aviso_legal/index.php, https://www.boe.es/gazeta/dias/1931/04/15/ (404)
- https://www.memoriademadrid.es/robots.txt y /oai (403 Akamai)
- https://doi.org/10.34810/DATA3274 → dataverse.csuc.cat (reto antibot)
- https://datos.madrid.es/api/3/action/package_show?id=215863-0-memoria-de-madrid-publicaciones-periodicas-de-la-guerra-civil, package_search?q=memoria de madrid
- https://analisi.transparenciacatalunya.cat/api/views/x8yr-e7bz.json, /u2ix-2jr6.json, /api/catalog/v1?q=guerra civil
- http://vitimas.nomesevoces.net/media/base-datos.csv (HEAD), /robots.txt
- https://www.juntadeandalucia.es/datosabiertos/portal/api/3/action/package_show?id=fosas-comunes-de-la-guerra-civil
- https://opendata.euskadi.eus/contenidos/ds_general/victimas_guerra_civil/opendata/victimas_guerra_civil.json (HEAD)
- http://api.socialhistoryservices.org/solr/all/oai?verb=Identify, /srw
- https://data.cervantesvirtual.com/bvmc-lod/repositories/data (SPARQL), https://www.cervantesvirtual.com/oaibvmc/servlet/OAIHandler?verb=Identify
- https://bibliotecavirtual.defensa.gob.es/BVMDefensa/i18n/oai/oai_bibliotecavirtualdefensa.es.do?verb=Identify
- https://mdc.csuc.cat/oai/oai.php?verb=Identify
- https://commons.wikimedia.org/w/api.php (categoryinfo), https://query.wikidata.org/sparql
- https://www.archivesportaleurope.net/advanced-search/... (403)
- https://www.ine.es/inebaseweb/libros.do?tntp=25687 (200)
- http://www.argos.gva.es/robots.txt (503)

Leídas vía buscador (fuente secundaria):

- https://github.com/tonirc/spain2Rep · https://www.tonirodon.cat/second-republic-atlas/en/codebook.html · https://www.tonirodon.cat/second-republic-atlas/es/methods.html · https://www.upf.edu/web/focus/w/atles-digital-mapa-electoral-segona-republica-toni-rodon
- https://datos.gob.es/es/catalogo/a09002970-resultados-electorales-de-la-segunda-republica-en-cataluna-resultados-por-municipios
- https://pauvallprat.github.io/mapSpainHist/ · https://zenodo.org/records/23663208 · https://zenodo.org/records/15345101 · https://doi.org/10.1038/s41597-025-04533-8
- https://franvillamil.com/data_spain.html
- https://www.cultura.gob.es/en/cultura/archivos/informacion-general/cooperacion-internacional/apef/apideape.html · https://pro.europeana.eu/organisation/archives-portal-europe · https://pares.cultura.gob.es/participamos-en/fundacion-ape/ampliar-informacion.html
- https://datos.madrid.es/dataset/215863-0-memoria-de-madrid-publicaciones-periodicas-de-la-guerra-civil · https://hispana.mcu.es/es/recoleccion/datos.do?idOai=3685&idOrigen=1175 · https://www.condeduquemadrid.es/conde-duque/servicios/biblioteca-digital-memoriademadrid
- https://hauteskundeak.euskadi.eus/informacion/resultados-segunda-republica-elecciones-1936/webelec00-content/es/ · https://opendata.euskadi.eus/catalogo/-/victimas-mortales-de-la-guerra-civil-en-euskadi/ · https://datos.gob.es/es/catalogo/a16003011-victimas-mortales-de-la-guerra-civil-en-euskadi
- https://codigocero.com/2009/10/27/nomes-e-voces-libera-o-seu/ · https://nomesevoces.net/recursos/informes/1/informe-de-resultados-vitimas-galicia-1936-1939
- https://www.juntadeandalucia.es/datosabiertos/portal/dataset/fosas-comunes-de-la-guerra-civil · https://andalucia.desaparicionforzada.com/cartografias/descarga-de-geodatos/
- https://memoria-oroimena.unavarra.es/ · https://oroibidea.es/
- https://memoria.gencat.cat/ca/que-fem/banc-memoria-democratica/fons/cost-huma-de-la-guerra-civil/ · https://mptmd.gob.es/ca/portal/memoria-democratica/archivos-estatales/guiadecensosdevictimas/comunidadesautonomas/cataluna
- https://www.fbbva.es/publicaciones/estadisticas-historicas-de-espana-siglos-xix-xx/
- https://iisg.amsterdam/en/collections/using/machine-access · https://archief.socialhistory.org/en/collections/spanish-civil-war-organizations
- https://ajuntament.barcelona.cat/arxiumunicipal/ca/consulta/consulta-els-documents · https://catalegarxiumunicipal.bcn.cat/page/welcome · https://dadesobertes.diba.cat/datasets/arxius-municipals-digitals
- https://arxiusenlinia.cultura.gencat.cat/ · https://anc.gencat.cat/ca/serveis/Domini_public/index.html · https://calaix.gencat.cat/handle/10687/399225
- https://data.cervantesvirtual.com/datos-enlazados · https://www.cervantesvirtual.com/portales/exilio/presentacion/
- http://www.argos.gva.es/ahe/indexv.html
- https://www.dara-aragon.es/dara/memoriademocratica/presentacion.jsp · https://www.zaragoza.es/sede/servicio/noticia/318882 · https://zaragoza.es/sede/portal/usic/servicio/tramite/3723
- https://www.ub.edu/imatgespavello/content/cartells-del-pavell%C3%B3-de-la-rep%C3%BAblica · https://mdc.csuc.cat/digital/custom/collections
- https://bibliotecavirtual.defensa.gob.es/BVMDefensa/en/ayuda/oai.do · https://www.bne.es/es/blog/recursosprensa/2012/09/11/biblioteca-virtual-de-defensa-hemeroteca
- https://www.bilbao.eus/bld/
