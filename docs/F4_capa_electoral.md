# F4 · Capa electoral 1931-1936: estado

**Fecha:** 14-11-2026

## Condición previa (de `04_roadmap.md`) y cómo se cumplió

| Condición | Estado |
|---|---|
| Verificar F032 y los derechos de los datos usados | ✓ Atlas Electoral de la Segunda República v2.1, CC BY-NC-SA 4.0 (DataCite y API de Dataverse). Descargado por la API oficial, sin pasar por la web con reto antibot |

## Qué se ha construido

- **Atlas, capa «Elecciones por circunscripción»** (1931, 1933 y 1936): candidatura más votada, participación, escaños y electos en primera vuelta por bloque. Aviso cuando la circunscripción fue a segunda vuelta.
- **Atlas, capa «Elecciones por municipio»** (1933 y 1936): candidatura más votada o participación. Aviso permanente: más superficie no significa más votos (en 1936 la coalición de derechas es la más votada en 5.590 municipios y la de izquierdas en 2.736, pero la de izquierdas lo es en 34 de 60 circunscripciones).
- **Versión sin WebGL:** tablas por circunscripción de las tres elecciones.
- **Acontecimientos:** resultados por circunscripción añadidos a las elecciones de 1931 y 1933 y nuevo acontecimiento «Elecciones generales a Cortes de 1936».
- **Ficha documental:** `doc-atlas-electoral`, con licencia NC-SA y contexto metodológico.

## Decisiones de rigor

- **No se publican porcentajes por bloque.** El libro de códigos del Atlas advierte que aplicar fórmulas de candidatura a bloques sintéticos introduce sesgos. Se muestran el bloque más votado, la participación y los escaños, que son más robustos.
- **No se suman escaños a escala nacional.** Los datos solo recogen electos en primera vuelta; las circunscripciones que fueron a segunda vuelta (por ejemplo, Gipuzkoa y Álava en 1936) aparecen sin escaños.
- **Paleta categórica de Paul Tol**, apta para daltonismo, sin la convención rojo/azul. Las chinchetas de acontecimientos son blancas con borde oscuro, para no confundirse con ningún bloque.
- **Licencia:** todo lo derivado del Atlas se declara CC BY-NC-SA 4.0 (`LICENSE-contenido.md`), con atribución en el mapa, en el panel y en la tabla.

## Verificación

- Fechas del Atlas (28-06-1931, 19-11-1933, 16-02-1936) contrastadas con la Gaceta para 1931 y 1933. El Readme del depósito dice «abril de 1931», pero los datos usan la fecha correcta.
- Casos conocidos coherentes con la historiografía general: Navarra (derechas, 7 de 7 en 1933 y 1936), Madrid capital y Barcelona capital (Frente Popular en 1936), Bilbao 1936 (4 Frente Popular y 2 PNV).
- **Incoherencias de la fuente:** en 3 de 183 casos (Ciudad Real 1931, Barcelona capital 1933, Ourense 1933) el bloque «más votado» no es el que obtuvo la mayoría de escaños. Se publican tal cual, con aviso en el panel y en la tabla. **Pendiente: comunicarlo a los autores** (contacto en el Readme del depósito).
- Lighthouse (local, perfil móvil): atlas por defecto 100/100; capa de circunscripciones 99/100; capa municipal 96/100. Las capas se cargan por URL para que MapLibre las procese en su worker.

## Fallo corregido de F2

En MapLibre 6, la propiedad interna `_data` de las fuentes GeoJSON ya no contiene el GeoJSON. Desde F2, al cambiar de indicador o de censo, el mapa recalculaba los cortes pero seguía coloreando con los valores del primer indicador. Corregido guardando referencias propias a los datos.

## Pendiente

- Elecciones de 1931 por municipio: el Atlas aún no las publica.
- Segunda vuelta y escaños finales: requieren otra fuente.
- Comunicar las 3 incoherencias a los autores del Atlas.
