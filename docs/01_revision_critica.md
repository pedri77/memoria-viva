# 01 · Revisión crítica de EMV-MASTER-001 v1.0

**Fecha:** 14-11-2026 · **Objeto:** `00_origen/EMV-MASTER-001_v1.0.md` (703 líneas) · **Destino real del proyecto:** proyecto personal público (un autor, GitHub Pages).

Severidad: **A** bloquea o invalida una decisión · **M** hay que corregirlo antes de construir · **B** mejora.

## Valoración general

El documento es sólido en lo que más importa en un proyecto de memoria histórica: procedencia obligatoria, separación entre documento, interpretación y recreación, prudencia con datos nominales y con la cobertura desigual de los archivos. Las reglas editoriales (l.38-45) y la definición de «listo para publicar» (l.695-697) se pueden conservar casi tal cual.

Sus tres problemas de fondo:

1. **Está escrito para una institución con equipo**, no para un autor solo. Comité, dual control, seis roles RBAC, SLA del 99,5 % y un stack de siete servicios no se pueden sostener a la vez.
2. **Da por buenas rutas de datos que no existen para el periodo.** La auditoría (ver `03_auditoria_fuentes.md`) muestra que la API del INE no tiene censos anteriores a 1981 y que la API del BOE empieza en septiembre de 1960. Dos de las siete fuentes P0 no sirven para 1931-1939 por la vía que propone el documento.
3. **Promete anexos y ficheros que no están** (CSV de 11 campos, PRD y matriz originales).

## Hallazgos

| # | Sev. | Línea(s) | Hallazgo | Propuesta |
|---|---|---|---|---|
| R01 | A | 567, 605 | F009 «INE OpenAPI» figura como P0 con «API oficial». Comprobado: las 988 tablas de la operación Censo de Población (id 463) son de 2021 y no hay ninguna operación con series anteriores a 1981. | Bajar F009 a P2 (fuera de horizonte). La fuente real del periodo es F010: INEbase Historia (anuarios y censos escaneados) y la aplicación «Alteraciones de los municipios en los Censos de Población desde 1842» (`ine.es/intercensal`). |
| R02 | A | 573 | F015 propone «API histórica por verificar». Comprobado: la API de datos abiertos del BOE solo tiene sumarios desde septiembre de 1960 (FAQ oficial y prueba: 19360718 → 404; 19600901 → 200). La Gazeta (1661-1959) incluye «Gaceta de la República» y el «BOE» de Burgos, pero solo por formulario web, con texto OCR buscable 1836-1959. | Mantener P0, pero como fuente de **referencias curadas a mano** (enlace ELI o URL de Gazeta por disposición), no de ingesta automática. |
| R03 | A | 565, 600 | F007 BNE: el documento no sabe cómo acceder. Comprobado: `hemerotecadigital.bne.es/robots.txt` prohíbe todo agente salvo Google y Bing, y `www.bne.es` devuelve 403 a clientes automáticos. Sin embargo, la BNE publica en datos.gob.es «Hemeroteca digital. Texto completo» y «Listado de títulos» con **licencia CC BY 4.0** (CSV y HTML, actualizado 08-09-2026). | Única vía de ingesta permitida: los datasets de datos.gob.es. Nada de scraping del visor. |
| R04 | A | 591 | «El CSV adjunto conserva 11 campos por fuente»: no existe. | Creado `source_registry.csv` en esta revisión. |
| R05 | M | 531-532, 703 | Parte II y la trazabilidad citan `PRD_Espana_Memoria_Viva_v1.md`, `02_..._Diseno...md` y `03_..._Matriz_Fuentes_v1.md`, que no se entregaron. | Declarar el maestro como fuente única y quitar referencias a ficheros ausentes. |
| R06 | M | 238, 533, 649 | La FAQ de PARES aparece con dos rutas (`/pares/preguntas-frecuentes.html` y `/preguntas-frecuentes.html`). Ambas responden 200 hoy; la canónica es la segunda. | Unificar. |
| R07 | M | 558-588 | URL genéricas o erróneas: F014 (RTVE) repite la URL de F013; F005, F006 y F019 comparten la página general de bases de datos; F025 apunta a la portada del Ministerio; F027 a la portada de diplomatie.gouv.fr y no a Archives diplomatiques; F018 redirige a un dominio antiguo (`mecd.gob.es`) que no responde; F026 (UNESCO) no respondió en dos intentos. | Corregidas o marcadas en `source_registry.csv`. |
| R08 | M | 650 | La ficha PARES 678242 que se cita como «ejemplo de condiciones» es un pleito de 1483 de la Real Chancillería de Valladolid. No representa los fondos del CDMH. | Citar la FAQ de PARES (pregunta 9), que es la que fija las condiciones: dominio público sin permiso previo; resto, solo uso privado y autorización para difundir. |
| R09 | M | 615, 658 | Fosas: el registro de datos.gob.es no se actualiza desde el 17-12-2015 y su única distribución es el buscador web. Correcto que el documento no confirme descarga; falta decir que **no hay dataset vigente**. | Fuera del MVP. Si se usa, solo agregados por provincia y enlace al mapa oficial. |
| R10 | A | 156, 483-485, 464 | Gobernanza institucional (comité multidisciplinar, dual control, RBAC de 6 roles, OIDC+MFA) incompatible con un autor solo. | Gobernanza mínima: autor responsable identificado, 2-3 revisores externos voluntarios por narrativa, changelog público, formulario de corrección. Sin backoffice en el MVP. |
| R11 | M | 174 | RNF-003 «99,5 % mensual» sin operador de guardia. | Con hosting estático la disponibilidad la da GitHub Pages; se elimina el requisito. |
| R12 | A | 198 | Piloto: 500 fichas, 50 eventos, 10 series, 5 narrativas, 3 familias de capas. Con revisión humana real por ficha es trabajo de meses para un equipo. | Piloto: 100 fichas, 20 eventos, 3 series, 1 narrativa, 2 capas. Ver `04_roadmap.md`. |
| R13 | M | 256 vs 164, 413 | «No requiere WebGL para funcionar» y a la vez MapLibre/deck.gl, que necesitan WebGL. | Exigir una vista alternativa real: listado tabular filtrable de eventos y lugares, más mapa SVG estático por provincias. |
| R14 | M | 510, 206, 204 | Métricas no medibles en solitario: test UX n≥8, auditoría WCAG formal, «0 citas fabricadas en corpus adversarial». | Comprobaciones automáticas: axe-core y Lighthouse CI en cada push, script que verifica que cada cita apunta a una fuente del registro y que la URL responde, 3 pruebas de usuario informales por fase. |
| R15 | A | 539 | Marco legal incompleto. Faltan: Ley 37/2007 de reutilización de la información del sector público y RD 1495/2011; Ley 16/1985 de Patrimonio Histórico, art. 57.1.c (documentos con datos personales: 25 años desde la muerte o 50 desde la fecha del documento); LOPDGDD art. 3 (datos de personas fallecidas: el RGPD no aplica, pero familiares y herederos pueden pedir acceso, rectificación o supresión). | Añadir al §II.14 y a ADR-007. Y añadir que, como proyecto personal, la responsabilidad legal recae en el autor: no publicar nombres de víctimas ni de responsables en el MVP. |
| R16 | M | 120-123, 396 | IA/RAG en P1 con «modelo» sin especificar. | Aplazar a fase 4. Si se hace, modelo local (Ollama) y solo sobre corpus de dominio público ya publicado. Nunca respuestas sin cita. |
| R17 | M | 41, 158 | Faltan criterios de vocabulario. En este periodo los términos son parte del debate («bando nacional» frente a «sublevado», «Alzamiento» frente a «golpe de Estado», «represión», «paseos», «checas»). | Guía de vocabulario: término propio del proyecto, término de la fuente entre comillas y atribuido, y referencia historiográfica que justifica el uso. |
| R18 | M | 87 | Laguna en dominios de datos: elecciones de 1931, 1933 y 1936 no tienen fuente en la matriz. Son la capa estadística más pedida del periodo. | Añadir fuente candidata: Congreso, «Histórico de Diputados 1810-1977» y estudios electorales publicados (con cita y derechos revisados). |
| R19 | B | 629 | La matriz técnica añade más de 25 campos. Excesivo para empezar. | Registro con 16 columnas (ver CSV); ampliar solo si hace falta. |
| R20 | B | 632 | La fórmula de puntuación de preparación S está bien, pero nadie la había calculado. | Calculada con evidencia para las 7 P0 en `03_auditoria_fuentes.md`. |
| R21 | B | 366 | Paleta con granate `#8D423C` como color de acento: en este tema el rojo arrastra lectura política. | Mantener la paleta, pero usar el granate solo en elementos editoriales, nunca para codificar bandos o capas. |
| R22 | B | 165 | Qdrant, Redis, Celery, OpenSearch y MinIO en el MVP. | Ver `02_stack.md`. |

## Qué se mantiene sin cambios

- Reglas editoriales transversales (l.38-45).
- Modelo `claim` / `claim_evidence` y separación hecho, documento, interpretación y estimación (l.139).
- No fusionar personas por nombre (l.18, l.474).
- Estados de ingesta `DISCOVERED → … → PUBLISHED` y `BLOCKED_RIGHTS` (l.479).
- «Enlazar por defecto, copiar solo con derecho constatado» (l.683).
- Definición de listo para publicar (l.697).
