# F4 · Memoria democrática hoy: ayudas públicas (BDNS)

**Fecha:** 15-11-2026. Propuesta de David: qué información dan los ayuntamientos, las ayudas (incluidas las europeas) y cómo se usan. Es bloque A: datos públicos actuales y sin datos personales.

## Fuente

Base de Datos Nacional de Subvenciones (SNPSAP, IGAE), a través de la API del portal [infosubvenciones.es](https://www.infosubvenciones.es/bdnstrans/GE/es/index).
- **Reutilización:** su aviso legal remite a la Ley 37/2007 y exige citar «Origen de los datos: Intervención General de la Administración del Estado» y la fecha.
- **Datos personales:** solo pueden usarse disociados.
- **Robots:** el sitio no publica robots.txt. Se hace una petición por segundo.

## Qué se descargó

- **Convocatorias:** 777, buscadas por los términos «memoria democrática», «memoria histórica», «exhumación», «fosas», «simbología franquista», «guerra civil», «franquismo» y «víctimas de la guerra civil».
- **Concesiones a entidades:** 3.244, por 41,3 millones de euros. La BDNS solo muestra las de 2022 en adelante.
- **Concesiones a personas físicas:** 63, por 226.443 €. Solo se guardan el número y el total por convocatoria y año.

No se guardan los títulos de las convocatorias, porque algunos llevan el nombre de una persona: solo una categoría temática calculada a partir de ellos.

Scripts:
- `scripts/etl/bdns_memoria_descarga.py`: descarga.
- `scripts/etl/bdns_memoria.py`: fuente F060, documento `doc-bdns-memoria-democratica` e indicador `ind-subv-memoria-local-prov`.

## Provincia

Solo para entidades locales, por el NIF: P + código INE de provincia + código de municipio. Los NIF con numeración ampliada usan provincia + 50 (58 Barcelona, 61 Cádiz, 67 Gerona, 75 Lérida, 84 Palencia, 86 Pontevedra, 93 Tarragona), lo que se ha comprobado con el nombre de cada entidad. En asociaciones o universidades el NIF no da la provincia con seguridad, así que se resumen por tipo.

## En la web

- **Página `/memoria-hoy/`:** importes por año, por administración convocante, por tipo de beneficiario, por tema, por provincia, y las 30 entidades locales con más importe.
- **Atlas:** capa anual por provincia.

## Cambio de reglas

Nuevo estado de derechos `reuse_open`: reutilización abierta con cita según las condiciones generales de la Ley 37/2007, que permite almacenar. Está en el esquema, el validador, las etiquetas de la web, el CSV y la guía editorial §5.

## Pendiente

En la laguna `laguna-ayuntamientos-memoria`:
- lo que publica cada ayuntamiento (portales de transparencia, catálogos de vestigios, lugares de memoria);
- la ejecución de las ayudas;
- los proyectos europeos del programa CERV «European Remembrance».
