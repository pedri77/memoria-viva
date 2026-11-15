# F4 · Hambre de posguerra, parte 4: racionamiento por provincias, 1948-1950

**Fecha:** 15-11-2026

**Fuente:** INE, Anuarios Estadísticos de España de 1949, 1950 y 1951, sección «Precios, salarios, racionamiento y consumo». Licencia CC BY 4.0.

| Año | Anuario | Distribución por provincias (td) | Cartillas a 31-12 (td) |
|---|---|---|---|
| 1948 | 1949 | 164753 | 164751 |
| 1949 | 1950 | 29963 | 29961 |
| 1950 | 1951 | 165650 | 165652 |

**Transcripción:**
- **Kilos:** aceite, azúcar y patatas: régimen normal, economatos o colectividades, total civil, pequeñas industrias y total general, por provincia (`data/external/ine_anuarios/racionamiento_provincias_1948_1950.csv`).
- **Cartillas:** en tiendas, establecimientos colectivos y economatos preferentes (`cartillas_provincias_1948_1950.csv`).
- **Comprobaciones:** todas las filas y columnas cuadran contra los totales impresos (`scripts/etl/ine_racionamiento_1948_1950.py`).

**Erratas de la tabla impresa:**
- **Corregidas:**
  - Álava, aceite, 1950: total civil 883.784 por 833.784.
  - Huelva, cartillas en tiendas, 1949: 552.911 por 352.911.
- **Anotadas sin efecto en el cálculo:** tres «total general» de 1950 (Baleares aceite, Huesca azúcar, Las Palmas patatas).

**Cálculo:** kilos repartidos a la población civil / cartillas inscritas a 31 de diciembre. El Campo de Gibraltar se suma a Cádiz. En 1949 solo trae el primer trimestre; después sus municipios pasaron a Cádiz y Málaga.

**Resultado** (kg por cartilla y año, España sin Ceuta ni Melilla):

| Año | Cartillas | Aceite | Azúcar | Patatas |
|---|---|---|---|---|
| 1948 | 28.886.779 | 9,3 | 3,3 | 22,4 |
| 1949 | 29.231.465 | 7,0 | 4,3 | 27,1 |
| 1950 | 29.480.935 | 7,5 | 3,8 | 5,4 |

**Cautelas** (publicadas en los indicadores):
- Miden el reparto oficial, no el consumo: el estraperlo y el autoabastecimiento quedan fuera.
- Las raciones variaban por categoría de cartilla.
- Las patatas se racionaban sobre todo en provincias no productoras: Orense recibe 2,5 kg y Vizcaya 57 en 1948. En 1950 dejaron de repartirse en muchas provincias; las que traen raya en la tabla llevan nota.

**Indicadores:** `ind-racion-{aceite,azucar,patatas}-prov`, en el atlas y en Datos («Mortalidad y hambre»).

**Pendiente:**
- 1943 (Anuario de 1944-1945, td 162173): distribución sin cartillas por provincia.
- Resto de artículos (legumbres, arroz, pan).
- Salarios reales.
- Relato R3.
