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
