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
| P1 | Censo de 1930 por profesiones (peso del sector agrario por provincia) | Alto: tabla grande, transcripción a mano | Clave para contextualizar la reforma agraria. |
| P2 | Prensa del día en los acontecimientos clave (enlaces a números de la BNE, sin citas) | Medio | El servidor de la BNE bloquea clientes automáticos: los enlaces se construyen desde el CSV oficial y se comprueban a mano. |
| P3 | Alfabetización por edad (mayores de 10 años), censo de 1930, tomo III | Alto: tablas regionales | Laguna `laguna-alfabetizacion-edad`. |
| P4 | Georreferenciación de mapas históricos del CNIG | Alto | Aplazado desde F2. |
| P5 | Enlaces Wikidata de los municipios de 1930 | Medio | Aplazado desde F2. |

## Pendientes de David (no técnicos)

- 3 pruebas informales con usuarios (F2).
- 2 revisores para las narrativas (borrador del correo en `docs/F3_estado.md`).
- Anuncio público (borrador en `docs/F3_estado.md`).
- Comunicar a los autores del Atlas Electoral las 3 incoherencias detectadas (`docs/F4_capa_electoral.md`).
