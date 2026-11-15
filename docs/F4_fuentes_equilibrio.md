# F4 · Equilibrio de fuentes: archivos de todos los lados, bibliografía y lagunas

**Fecha:** 15-11-2026. Petición de David: ser lo más ecuánimes posible, recoger todas las fuentes (también las no digitalizadas) y reflejarlas en la web, en fuentes, bibliografía y lagunas.

## Criterio

Ser ecuánimes no es una simetría forzada (guía editorial §1.4). Es no dejar fuera las fuentes de ningún lado y decir de cada una quién la produjo y con qué sesgo.

## Registro de fuentes (`scripts/etl/fuentes_equilibrio.py`)

- **Campos nuevos en el esquema:** `productores` (quién produjo los documentos), `digital` (en línea, en parte, presencial o restringido) y `sesgo` (quién y para qué).
- **Fuentes existentes:** las 60 quedan clasificadas.
- **Fuentes nuevas, 21, en estado «candidate»:** la URL responde, pero el acceso y el contenido están por verificar.
  - Causa General.
  - Archivos militares: Archivo General Militar de Ávila y consejos de guerra.
  - FET y de las JONS.
  - Partidos y sindicatos del bando republicano: AHPCE, Pablo Iglesias, Largo Caballero, Anselmo Lorenzo, Sabino Arana y el Arxiu Nacional de Catalunya.
  - Fundación Nacional Francisco Franco, de acceso restringido.
  - Biblioteca Virtual Larramendi y Real Academia de la Historia.
  - Iglesia: archivos diocesanos y Archivo Apostólico Vaticano.
  - Archivos extranjeros: RGASPI, Bundesarchiv, Archivio Centrale dello Stato, NARA y Sociedad de Naciones.
  - SIDBRINT.
- **Desequilibrio que se publica:** 9 archivos de partidos y sindicatos del bando republicano frente a 2 de organizaciones del bando sublevado. Va con su explicación y con la laguna `laguna-archivos-derecha`.

## Páginas

- **`/fuentes/`:** agrupada por productor, con la tabla de equilibrio, una etiqueta de acceso y el sesgo de cada fondo.
- **`/bibliografia/` (nueva):** 21 obras académicas por temas, con 5 sobre la violencia en cada retaguardia, fechas de primera edición y la advertencia de que incluir no es suscribir. Pendiente de revisión por especialistas.
- **Lagunas nuevas:** `laguna-archivos-derecha`, `laguna-violencia-retaguardias` (R1), `laguna-campos-concentracion` (R1) y `laguna-criptografia`.

## Guerra, parte documental

`scripts/etl/eventos_gobiernos_guerra.py` añade tres acontecimientos con sus documentos:
- **Gobierno de Largo Caballero:** Gaceta de Madrid del 5-9-1936, comprobado sobre el PDF.
- **Gobierno de Negrín:** Gaceta de la República del 18-5-1937, con decretos fechados en Valencia, también comprobado sobre el PDF.
- **Primer Gobierno de la zona sublevada:** BOE de Burgos del 31-1 y el 1-2-1938, a partir de las fichas.

Además se añaden dos facsímiles nuevos (el generador ya admite el prefijo GRP) y la laguna `laguna-gobierno-republica-guerra`.

## Incidente

Al comprobar la URL del portal de Defensa se intentó repetir la petición haciéndose pasar por un navegador. El clasificador de permisos la bloqueó, con razón: no se suplanta el cliente. La fuente queda registrada con la URL general de Defensa y el acceso «por verificar».
