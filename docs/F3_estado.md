# F3 · Primera narrativa y publicación: estado

**Fecha:** 14-11-2026

## Puerta de salida (de `04_roadmap.md`)

| Criterio | Estado |
|---|---|
| Narrativa con scroll | ✓ «Las escuelas de la República, 1931-1936»: 6 escenas, 11 afirmaciones, mapa fijo que resalta los lugares de cada escena, notas de fuente numeradas y sección «Lo que esta historia todavía no cuenta» |
| Cada afirmación enlazada a una evidencia | ✓ lo exige el esquema (`claims[].evidence`, mínimo 1) y el validador comprueba que el documento existe y no está retirado |
| Formulario de corrección y registro de cambios público | ✓ plantilla de issue (ya en F0) y `/cambios/`, generado desde git en cada build, con los contenidos retirados y su motivo |
| Prueba de retirada de principio a fin | ✓ `npm run test:retirada`: 6 de 6 comprobaciones (aviso en la URL original, fuera de listados, JSON y búsqueda, en el registro de cambios, y fallo al retirar un documento citado). En CI |
| Revisión por 2 personas con formación en historia contemporánea | ✗ pendiente: la narrativa se publica como «Borrador en revisión» y el esquema impide marcarla `aprobado` sin dos revisores |
| Anuncio y difusión | ✗ pendiente de David (borrador abajo) |

## Evidencia nueva incorporada

- Gaceta del 30-04-1931, págs. 413-414: decreto sobre el catalán en la escuela primaria.
- Gaceta del 09-05-1931, pág. 620: decreto de 6 de mayo de 1931, instrucción religiosa voluntaria.
- Gaceta del 24-06-1931, pág. 1612: preámbulo con el recuento de la Inspección (35.716 escuelas existentes y 27.151 necesarias), presentado como estimación del Gobierno.
- Gaceta del 10-12-1931, pág. 1582: artículo 48 de la Constitución.
- Gaceta del 03-06-1933, págs. 1652-1653: artículo 30 y disposición transitoria b) de la Ley de Confesiones y Congregaciones Religiosas.

## Rendimiento y accesibilidad (local, perfil móvil)

| Página | Rendimiento | Accesibilidad | axe |
|---|---|---|---|
| `/historias/escuelas-republica/` | 90 | 100 | 0 incidencias |
| `/historias/` | 99 | 100 | |
| `/cambios/` | 97 | 100 | 0 incidencias |

## Para enviar a los revisores (borrador, no enviado)

> Asunto: Revisión de una narrativa documental sobre la escuela en la Segunda República
>
> Hola, [nombre]:
>
> Estoy construyendo un atlas documental de España entre 1931 y 1939, sin ánimo de lucro, en el que cada afirmación enlaza a su fuente original: https://pedri77.github.io/memoria-viva/
>
> La primera narrativa, «Las escuelas de la República, 1931-1936», tiene 6 escenas y 11 afirmaciones, todas sacadas de la Gaceta de Madrid: https://pedri77.github.io/memoria-viva/historias/escuelas-republica/
>
> Te pido una revisión de unos 30 minutos: si alguna afirmación es inexacta, si el vocabulario es adecuado, si falta contexto imprescindible y si las lagunas declaradas son las importantes. Puedes responder por correo o en el formulario público de correcciones. Si te parece bien, tu nombre figurará como revisor.
>
> Gracias.

## Anuncio (borrador, no publicado)

> «Memoria Viva» es un atlas documental de España entre 1931 y 1939. Cada dato enlaza a la Gaceta, a la BNE o a los censos del INE. Primera historia: las escuelas de la República, contada solo con lo que dicen las normas y con lo que todavía falta, avisado. https://pedri77.github.io/memoria-viva/
