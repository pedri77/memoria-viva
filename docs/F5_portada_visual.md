# F5 · Portada «Del documento al mapa» y capa visual común

**Fecha:** 15-11-2026. Estado: en local, pendiente de push.

## Qué cambia

- **Portada nueva** (`site/src/pages/index.astro`, datos en `site/src/lib/portada.ts`):
  - Apertura: el mapa provincial de 1930 se dibuja al cargar; al desplazarse, el año corre de 1931 a 1939 y se encienden los acontecimientos con lugar.
  - «Saber leer»: coropletas de los censos de 1920 y 1930, con interpolación entre pasos.
  - «Votar»: participación por circunscripción en 1931, 1933 y 1936, con fundido entre mapas.
  - Cronología en carrete horizontal y un índice editorial de secciones.
- **Plantilla común** (`Base.astro`):
  - Fuentes alojadas en el propio sitio (`@fontsource-variable`): se retira Google Fonts y ya no se envía la IP del visitante a terceros.
  - Cabecera que marca la sección activa (`aria-current`) y menú móvil que funciona sin JS.
  - Transiciones entre páginas con `@view-transition`, desactivadas con movimiento reducido.
  - Favicon (antes daba 404).

## Reglas que se mantienen

- Ninguna imagen generada (guía editorial §6). Todo el material visual son datos del proyecto.
- Los textos de los pasos son las afirmaciones de las narrativas, leídas en build con su documento. Si una afirmación cambia, la portada cambia con ella. Si la afirmación desaparece, el build falla.
- Los dominios de color salen de los datos, no se fijan a mano. Las provincias sin dato aparecen rayadas.
- Con cada mapa va su atribución de licencia: INE CC BY 4.0 y Atlas Electoral CC BY-NC-SA 4.0.
- **Sin JS**, todas las secciones van en flujo normal con los mapas en su estado final. **Con movimiento reducido**, no hay animaciones autónomas.

## Verificación

- validate, build y test:retirada en verde.
- axe (WCAG 2.1 AA) sin incidencias en la portada (claro y oscuro), en una historia y en las lagunas.
- Capturas a 1440 y 390 px, en modo oscuro y sin JS.
- Detector de Impeccable: en una primera pasada saltó una transición de `max-height` en el menú; ya está corregida.

## Relato «La tierra» (15-11-2026)

Tercer relato de la portada, entre «Votar» y la cronología. Tiene cinco pasos:
1. El censo de 1930: población con profesión en montes, agricultura y ganadería.
2. Lo que el censo no aclara: la fila «Diversas» y las provincias sin dato.
3. El decreto de términos municipales de 1931.
4. La Ley de Reforma Agraria de 1932.
5. La ley de arrendamientos de 1935 y la «reforma de la reforma».

Reglas del relato:
- **Textos:** son las afirmaciones de la cronología, tal cual, con sus fuentes agrupadas por documento. Los extremos del mapa (provincia y valor) se calculan a partir de los datos.
- **Mapas:** los dos tienen escalas distintas, así que se funden en lugar de interpolar colores, y la leyenda cambia de rango con el paso.
- **Sin JS:** se ve el mapa agrario.
- **Verificación:** axe sin incidencias en claro y oscuro; capturas de los cinco pasos a 1440 y 390 px.
