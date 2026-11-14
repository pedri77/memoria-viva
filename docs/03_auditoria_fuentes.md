# 03 · Auditoría de fuentes

**Fecha de consulta:** 14-11-2026 · **Registro completo:** `source_registry.csv` (31 filas, 16 columnas).

## Método

- Las 34 URL del documento se comprobaron con `curl -L` (una petición por URL, 1 s de pausa) y se guardó el código HTTP y la URL final.
- Se leyó el `robots.txt` de cada fuente P0.
- Se probaron solo APIs públicas documentadas (INE `wstempus`, API de sumarios del BOE, API del catálogo de datos.gob.es) con pocas peticiones. Se comprobó si había OAI-PMH donde era plausible (PARES, BNE, Hispana).
- No se descargó ningún fondo, no se hizo scraping de visores y no se consultó ningún buscador nominal.

## Resultado general de las 34 URL

- 29 responden 200 (algunas tras redirección).
- 2 devuelven 403 a clientes automáticos (`bne.es`, protección antibot).
- 2 no responden: `archives.unesco.org` y el registro de fosas en `datos.gob.es` en la web (la API del catálogo sí responde).
- 1 redirige a un dominio antiguo que no responde (F018, `mecd.gob.es`).
- 7 URL son genéricas (portadas o páginas de listado) y no identifican la fuente: F005, F006, F014, F019, F020, F025, F027.

## Auditoría de las 7 fuentes P0

### F001 PARES y F002 CDMH

- **Acceso:** buscador web y micrositio de Guerra Civil. `pares.cultura.gob.es/oai` devuelve 404: **no hay API ni OAI-PMH pública**. Los archivos estatales envían descripciones EAD a Archives Portal Europe, que tiene API con clave: es la única vía automatizable plausible y queda **por probar**.
- **robots.txt:** solo bloquea rutas internas y otras lenguas. Aun así, el proyecto no hará extracción automática del visor.
- **Derechos (FAQ de PARES, pregunta 9):** «La información descriptiva y las imágenes de documentos en dominio público [...] pueden reproducirse y utilizarse sin permiso previo. La reproducción de documentos que no sean de dominio público solo está permitida para uso privado con fines culturales, científicos o educativos. La difusión de imágenes de estos documentos requerirá de una autorización previa». Las imágenes llevan marca de agua.
- **Decisión:** fichas curadas a mano (signatura, URL, fecha de consulta). Imagen solo si el documento es de dominio público.
- **Nota:** la ficha PARES 678242 que cita el documento es un pleito de 1483 y no sirve como ejemplo de los fondos del periodo.

### F007 BNE Hemeroteca Digital

- **Acceso web:** `hemerotecadigital.bne.es/robots.txt` contiene `User-agent: * / Disallow: /` (solo permite Googlebot y bingbot). `www.bne.es` responde 403 a clientes automáticos. **Prohibido el scraping.**
- **Vía abierta encontrada:** la BNE publica en datos.gob.es dos conjuntos con **licencia CC BY 4.0**: «Hemeroteca digital. Texto completo» (CSV, actualizado 08-09-2026) y «Hemeroteca digital. Listado de títulos» (28-09-2026). Las distribuciones apuntan a `hemerotecadigital.bne.es/hd/es/fulltext-csv`.
- **Pendiente:** que David confirme si la descarga de esa distribución oficial es aceptable aunque el robots.txt del host prohíba agentes. Recomendación: sí, porque es la distribución publicada para reutilización, con una sola descarga manual y sin rastreo.
- **Decisión:** prensa del piloto solo desde ese conjunto; páginas citadas con enlace al visor.

### F009 INE OpenAPI

- **Comprobado:** la API funciona (166 operaciones), pero la operación Censo de Población (id 463) tiene 988 tablas, todas de 2021. No hay operaciones con datos anteriores a 1981.
- **Decisión:** bajar a P2. **No sirve para el horizonte 1874-1978.**

### F010 INE censos históricos

- **Rutas reales:** INEbase Historia (`ine.es/inebaseweb`, anuarios y censos escaneados) y «Alteraciones de los municipios en los Censos de Población desde 1842» (`ine.es/intercensal`). Ambas responden 200.
- **Formato:** imágenes y PDF, tablas web por municipio. Transcripción manual con doble comprobación.
- **Decisión:** fuente estadística principal del piloto. Censos de 1920, 1930 y 1940 (población de hecho y de derecho por provincia), con la discontinuidad declarada.

### F011 CNIG cartografía antigua

- **Licencia (página de la serie):** Orden FOM/2807/2015, «licencia de uso, compatible con CC-BY 4.0», reconocimiento obligatorio del origen y la propiedad. La FAQ añade que se permite el uso comercial y la publicación.
- **Formato:** la serie CartoAntigua (1.752 ficheros) cubre 1500-1900, en JPG de 250 ppp y PDF **sin georreferenciar**. Para 1931-1939 hay que buscar las primeras ediciones del MTN50 y las minutas en sus propias series.
- **Decisión:** P0 para el mapa base histórico raster, con georreferenciación propia y error declarado.

### F015 BOE Gazeta

- **API:** la FAQ oficial dice que los sumarios están disponibles «desde septiembre de 1960». Prueba: `sumario/19360718` → 404; `sumario/19600901` → 200.
- **Colección histórica Gazeta:** 1661-1959, unos 1.470.000 documentos, texto OCR buscable de 1836 a 1959. Incluye la «Gaceta de la República» y el «Boletín Oficial del Estado» de Burgos: las dos administraciones del periodo de guerra.
- **Licencia:** condiciones de reutilización de la AEBOE (licencia tipo aprobada el 27-06-2024).
- **Decisión:** P0 como fuente de referencias normativas curadas a mano.

## Puntuación de preparación técnica (fórmula del §III.7)

`S = 25·A + 20·I + 20·D + 15·C + 10·T + 10·R`. Valores 0-1 estimados con la evidencia anterior; sirven para ordenar el trabajo, no son una auditoría formal.

| Fuente | A acceso | I interop. | D derechos | C cobertura del periodo | T trazab. | R robustez | **S** |
|---|---|---|---|---|---|---|---|
| F011 CNIG | 0,8 | 0,5 | 1,0 | 0,7 | 0,9 | 0,8 | **77,5** |
| F015 BOE Gazeta | 0,6 | 0,3 | 0,9 | 1,0 | 1,0 | 0,9 | **73,0** |
| F007 BNE (vía datos.gob.es) | 0,7 | 0,6 | 0,8 | 0,7 | 0,8 | 0,6 | **70,0** |
| F010 INE histórico | 0,6 | 0,2 | 0,9 | 0,9 | 0,8 | 0,8 | **66,5** |
| F001 PARES | 0,6 | 0,3 | 0,6 | 0,5 | 0,9 | 0,7 | **56,5** |
| F002 CDMH | 0,5 | 0,2 | 0,5 | 0,7 | 0,8 | 0,7 | **52,0** |
| F009 INE OpenAPI | 1,0 | 0,9 | 0,9 | 0,05 | 0,9 | 0,9 | **79,8, pero fuera del periodo** |

F009 puntúa alto y no sirve: por eso el componente C debería actuar como umbral (C < 0,2 ⇒ descartar), no solo como peso. Se propone así en la v1.1.

## Otros hallazgos

- **Fosas (F013):** el registro de datos.gob.es no se actualiza desde el 17-12-2015 y solo enlaza al buscador web. No hay conjunto de datos nacional vigente.
- **Wikidata (F030):** CC0 y SPARQL. Se propone subir a P1 como identificador de lugares y organizaciones, nunca como evidencia.
- **Laguna electoral:** ninguna fuente cubre las elecciones de 1931, 1933 y 1936. Se añade F031 (Congreso, Histórico de Diputados) como candidata.
- **Europeana (F021):** metadatos CC0 y APIs con clave gratuita. Es la mejor vía para imágenes con derechos ya declarados.

## Fuentes consultadas (14-11-2026)

- PARES FAQ: https://pares.cultura.gob.es/preguntas-frecuentes.html
- CDMH bases de datos: https://www.cultura.gob.es/cultura/areas/archivos/mc/archivos/cdmh/bases-de-datos.html
- robots.txt Hemeroteca BNE: https://hemerotecadigital.bne.es/robots.txt
- datos.gob.es, Hemeroteca digital texto completo: https://datos.gob.es/catalogo/ea0019768-hemeroteca-digital-texto-completo1
- BNElab, dataset Hemeroteca: https://bnelab.bne.es/en/dataset/digital-periodical-library/
- INE API: https://servicios.ine.es/wstempus/js/ES/OPERACIONES_DISPONIBLES
- INE alteraciones de municipios: https://www.ine.es/intercensal/
- CNIG CartoAntigua: https://centrodedescargas.cnig.es/CentroDescargas/catalogo.do?Serie=CAANT
- CNIG FAQ: https://centrodedescargas.cnig.es/CentroDescargas/faqs
- BOE FAQ datos abiertos: https://www.boe.es/datosabiertos/faq/boe.php
- BOE Gazeta, ayuda: https://www.boe.es/buscar/ayudas/gazeta_ayuda.php
- BOE condiciones de reutilización: https://www.boe.es/informacion/aviso_legal/index.php
- datos.gob.es, fosas: https://datos.gob.es/es/catalogo/e05232701-fosas-o-lugares-de-enterramiento-en-el-territorio-espanol
- Archives Portal Europe, contexto de la API: https://archiveshub.ac.uk/ape

## Solicitudes a preparar (no enviadas)

1. CDMH: condiciones para reproducir en la web carteles de la Guerra Civil cuyo autor murió después de 1946.
2. Archives Portal Europe: clave de API para leer las descripciones de los archivos estatales.
3. Ministerio de Memoria Democrática: si existe una descarga actual del mapa de fosas (solo para agregados).
