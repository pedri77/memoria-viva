"""F1 · Documentos de la Gaceta y acontecimientos 1931-1939 curados a mano.

Cada entrada se ha comprobado sobre el PDF del ejemplar completo (ruta /gazeta/dias/ de boe.es,
permitida por robots.txt) con scripts/etl/pdf_buscar.py: número, páginas impresas del sumario
y fecha de firma («Dado en…»). Las fechas que no se han podido leer en el documento no se usan:
en ese caso el acontecimiento se fecha por la publicación y se dice así.

Uso: python3 -I scripts/etl/eventos_f1.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
TODAY = "2026-11-14"
BOE_RIGHTS = {
    "status": "reuse_conditions", "action": "enlazar",
    "attribution": "Fuente: Agencia Estatal Boletín Oficial del Estado, www.boe.es",
    "evidence_url": "https://www.boe.es/informacion/aviso_legal/index.php", "checked_at": TODAY,
    "note": "Normas oficiales excluidas de propiedad intelectual (art. 13 LPI); se enlaza al ejemplar de la sede del BOE.",
}
REVIEW = {"status": "revision", "date": TODAY, "by": ["autor"],
          "note": "Comprobado sobre el PDF del ejemplar (OCR del BOE). Pendiente de segunda revisión humana."}
CATALUNA = ["plc-prov-08", "plc-prov-17", "plc-prov-25", "plc-prov-43"]

# (fecha publicación, núm., páginas, título del documento, resumen, contexto, lugares)
GACETAS = {
    "gaceta-1931-05-30": ("1931-05-30", 150, "1033-1034",
        "Gaceta de Madrid n.º 150, 30 de mayo de 1931: decreto que crea el Patronato de Misiones Pedagógicas",
        "Decreto que crea, dependiente del Ministerio de Instrucción Pública, un Patronato de Misiones Pedagógicas para difundir la cultura general, la orientación docente moderna y la educación ciudadana en aldeas, villas y lugares, con atención a la población rural.",
        "Disposición del Gobierno provisional. Acredita la creación del organismo, no su actividad posterior.",
        ["plc-espana"]),
    "gaceta-1931-06-24": ("1931-06-24", 175, "1612-1613",
        "Gaceta de Madrid n.º 175, 24 de junio de 1931: decreto que autoriza la creación de 7.000 plazas de maestros",
        "Decreto de 23 de junio de 1931 que autoriza al Ministerio de Instrucción Pública a crear, a partir del 1 de julio, 7.000 plazas de maestros y maestras con destino a las escuelas nacionales. Su preámbulo recoge los informes de la Inspección: existían 35.716 escuelas unitarias y secciones de graduada y harían falta 27.151 más.",
        "Disposición del Gobierno provisional. Las cifras de escuelas y maestros de su preámbulo son del propio Gobierno.",
        ["plc-espana"]),
    "gaceta-1931-12-10": ("1931-12-10", 344, "1578 y siguientes",
        "Gaceta de Madrid n.º 344, 10 de diciembre de 1931: Constitución de la República Española",
        "Texto de la Constitución aprobada por las Cortes Constituyentes, fechada en el Palacio de las Cortes el 9 de diciembre de 1931. El artículo 48 (pág. 1582) regula la enseñanza.",
        "Publicación oficial del texto constitucional.",
        ["plc-espana", "plc-madrid"]),
    "gaceta-1932-09-21": ("1932-09-21", 265, "2090-2102",
        "Gaceta de Madrid n.º 265, 21 de septiembre de 1932: Estatuto de Cataluña y Ley de Reforma Agraria",
        "Publica la ley relativa al Estatuto de Cataluña (págs. 2090-2094) y la ley relativa a la Reforma Agraria (págs. 2095-2102), ambas firmadas en San Sebastián el 15 de septiembre de 1932.",
        "Publicación oficial de dos leyes aprobadas por las Cortes Constituyentes.",
        ["plc-espana"] + CATALUNA),
    "gaceta-1933-06-03": ("1933-06-03", 154, "1651-1653",
        "Gaceta de Madrid n.º 154, 3 de junio de 1933: Ley de Confesiones y Congregaciones Religiosas",
        "Publica la ley relativa a Confesiones y Congregaciones Religiosas (págs. 1651-1653), firmada en Madrid el 2 de junio de 1933. Su artículo 30 prohíbe a las órdenes y congregaciones religiosas dedicarse a la enseñanza, salvo la formación de sus propios miembros; una disposición transitoria fija el cese el 1 de octubre siguiente para toda clase de enseñanzas, excepto la primaria, que terminará el 31 de diciembre.",
        "Publicación oficial de una ley aprobada por las Cortes Constituyentes.",
        ["plc-espana"]),
    "gaceta-1933-10-10": ("1933-10-10", 283, "251-252",
        "Gaceta de Madrid n.º 283, 10 de octubre de 1933: disolución de las Cortes Constituyentes y convocatoria de elecciones",
        "Decreto que declara disueltas las Cortes Constituyentes (págs. 251-252) y otro que dispone que las elecciones generales a Cortes se celebren el domingo 19 de noviembre.",
        "Publicación oficial. La paginación de la Gaceta se reinicia cada trimestre.",
        ["plc-espana"]),
    "gaceta-1934-10-07": ("1934-10-07", 280, "194",
        "Gaceta de Madrid n.º 280, 7 de octubre de 1934: declaración del estado de guerra en todo el territorio de la República",
        "Decreto de la Presidencia del Consejo de Ministros que declara el estado de guerra en todo el territorio de la República, precedido de una nota del Gobierno que cita los sucesos de Asturias y la proclamación del «Estat Català» por el presidente de la Generalidad.",
        "Fuente oficial del Gobierno: presenta los hechos según su versión y su calificación («los mal aconsejados»). No es una descripción neutral de los sucesos.",
        ["plc-espana", "plc-prov-33"] + CATALUNA),
    "gaceta-1936-07-19": ("1936-07-19", 201, "721-724",
        "Gaceta de Madrid n.º 201, 19 de julio de 1936: nuevo Gobierno y decretos del Ministerio de la Guerra frente a la sublevación",
        "Publica la dimisión y el nombramiento de ministros y, del Ministerio de la Guerra, un decreto que anula la declaración del estado de guerra en todas las plazas de la Península, Marruecos, Baleares y Canarias donde se haya dictado (pág. 723), otro que declara disueltas todas las unidades del Ejército que toman parte en el movimiento insurreccional y otro que declara licenciadas las tropas cuyos cuadros de mando se han colocado frente a la legalidad republicana (pág. 724). Decretos fechados en Madrid el 19 de julio de 1936.",
        "Fuente oficial del Gobierno de la República en las primeras horas de la sublevación. Acredita las medidas adoptadas, no su eficacia.",
        ["plc-espana", "plc-madrid"]),
    "gaceta-1936-10-07": ("1936-10-07", 281, "211-216",
        "Gaceta de Madrid n.º 281, 7 de octubre de 1936: Ley relativa al Estatuto Vasco",
        "Publica la ley relativa al Estatuto Vasco (págs. 211-214) y el decreto que crea en Madrid un Tribunal especial de responsabilidades civiles derivadas de la rebelión (págs. 215-216). Las disposiciones de este número están fechadas en Madrid el 6 de octubre de 1936.",
        "Publicación oficial. En esa fecha buena parte del territorio vasco ya estaba bajo control de los sublevados.",
        ["plc-espana", "plc-prov-01", "plc-prov-20", "plc-prov-48"]),
    "gaceta-1931-04-30": ("1931-04-30", 120, "413-414",
        "Gaceta de Madrid n.º 120, 30 de abril de 1931: decreto sobre el uso del catalán en las escuelas primarias",
        "Decreto que deroga las disposiciones dictadas contra el uso del catalán en las escuelas primarias, dispone que en las escuelas maternales y de párvulos la enseñanza se dé exclusivamente en la lengua materna, castellana o catalana, e igualmente en las primarias, y que en estas se enseñe a los alumnos catalanes, a partir de los ocho años, el conocimiento y la práctica de la lengua española (págs. 413-414).",
        "Disposición del Gobierno provisional. El preámbulo justifica la medida por el principio pedagógico de la enseñanza en la lengua materna y por la reparación de las medidas de la Dictadura contra el catalán.",
        ["plc-espana"] + CATALUNA),
    "gaceta-1931-05-09": ("1931-05-09", 129, "619-620",
        "Gaceta de Madrid n.º 129, 9 de mayo de 1931: decreto que hace voluntaria la instrucción religiosa",
        "Decreto de 6 de mayo de 1931 que dispone que la instrucción religiosa no será obligatoria en las escuelas primarias ni en los demás centros dependientes del Ministerio de Instrucción Pública. Los alumnos cuyos padres lo deseen la seguirán recibiendo; si el maestro declara su deseo de no darla, se confiará a sacerdotes que voluntaria y gratuitamente quieran encargarse de ella (págs. 619-620).",
        "Disposición del Gobierno provisional.",
        ["plc-espana"]),
    "gaceta-1931-06-04": ("1931-06-04", 155, "1174-1175",
        "Gaceta de Madrid n.º 155, 4 de junio de 1931: convocatoria de las Cortes Constituyentes",
        "Decreto que dispone que las Cortes Constituyentes, de una sola Cámara elegida por sufragio popular directo, se reúnan en el Palacio del Congreso el 14 de julio; las elecciones se celebrarán en toda España el 28 de junio con arreglo al decreto de 8 de mayo y a la ley electoral de 1907.",
        "Disposición del Gobierno provisional.",
        ["plc-espana", "plc-madrid"]),
    "gaceta-1936-10-08": ("1936-10-08", 282, "234-237",
        "Gaceta de Madrid n.º 282, 8 de octubre de 1936: ley de 5.300 plazas de maestros y decreto de expropiación de fincas rústicas",
        "Publica la ley que aprueba la autorización del decreto de 28 de febrero de 1936 para crear 5.300 plazas de maestros y maestras a partir del 1 de octubre (págs. 234-235) y el decreto, fechado el 7 de octubre de 1936, que acuerda la expropiación sin indemnización y a favor del Estado de las fincas rústicas pertenecientes el 18 de julio a personas que hubieran intervenido directa o indirectamente en el movimiento insurreccional contra la República (págs. 236-237).",
        "Fuente oficial del Gobierno de la República en guerra. Acredita las normas, no su aplicación efectiva.",
        ["plc-espana"]),
    "gaceta-1936-07-20": ("1936-07-20", 202, "739",
        "Gaceta de Madrid n.º 202, 20 de julio de 1936: dimisión de Diego Martínez Barrio y nombramiento de José Giral como Presidente del Consejo de Ministros",
        "Decreto que admite la dimisión de Diego Martínez Barrio como Presidente del Consejo de Ministros y otro que nombra a José Giral Pereira (pág. 739).",
        "Publicación oficial. Martínez Barrio había sido nombrado el 19 de julio (Gaceta n.º 201).",
        ["plc-espana", "plc-madrid"]),
}

GOGORA_DOC = "doc-gogora-bombardeos"
# Lugares municipales (centroide de mapSpainHist 1930, nunca la coordenada del suceso)
MUNICIPIOS = {
    "plc-mun-48046": ("Gernika-Lumo", "48046", "plc-prov-48", [-2.6925, 43.311]),
    "plc-mun-48027": ("Durango", "48027", "plc-prov-48", [-2.6521, 43.1799]),
    "plc-mun-01059": ("Vitoria-Gasteiz", "01059", "plc-prov-01", [-2.6547, 42.8186]),
}

# Acontecimientos: (id, título, tipo, fecha, precisión, lugares, precisión espacial, wikidata, [(texto, tipo, doc, localizador)])
EVENTOS = [
    ("evt-1931-04-30-catalan-escuelas", "Decreto sobre el uso del catalán en las escuelas primarias", "educativo",
     "1931-04-30", "dia", ["plc-espana"] + CATALUNA, "region", None,
     [("La Gaceta del 30 de abril de 1931 publica un decreto que deroga las disposiciones dictadas contra el uso del catalán en las escuelas primarias.",
       "documento", "doc-gaceta-1931-04-30", "págs. 413-414"),
      ("El decreto dispone que en las escuelas maternales, de párvulos y primarias la enseñanza se dé en la lengua materna, castellana o catalana, y que a partir de los ocho años se enseñe a los alumnos catalanes el conocimiento y la práctica de la lengua española.",
       "documento", "doc-gaceta-1931-04-30", "págs. 413-414")]),
    ("evt-1931-05-06-religion-voluntaria", "La instrucción religiosa deja de ser obligatoria en la escuela", "educativo",
     "1931-05-06", "dia", ["plc-espana"], "estatal", None,
     [("Un decreto de 6 de mayo de 1931 dispone que la instrucción religiosa no será obligatoria en las escuelas primarias ni en los demás centros dependientes del Ministerio de Instrucción Pública.",
       "documento", "doc-gaceta-1931-05-09", "art. 1, pág. 620"),
      ("Los alumnos cuyos padres lo pidan seguirán recibiéndola; si el maestro no desea darla, se confiará a sacerdotes que quieran encargarse de ella de forma voluntaria y gratuita.",
       "documento", "doc-gaceta-1931-05-09", "arts. 2 y 3, pág. 620")]),
    ("evt-1931-05-30-misiones-pedagogicas", "Creación del Patronato de Misiones Pedagógicas", "educativo",
     "1931-05-30", "dia", ["plc-espana"], "estatal", "Q6018462",
     [("La Gaceta de Madrid del 30 de mayo de 1931 publica el decreto que crea el Patronato de Misiones Pedagógicas, dependiente del Ministerio de Instrucción Pública.",
       "documento", "doc-gaceta-1931-05-30", "págs. 1033-1034"),
      ("Según el decreto, su fin es difundir la cultura general, la orientación docente moderna y la educación ciudadana en aldeas, villas y lugares, con atención especial a la población rural.",
       "documento", "doc-gaceta-1931-05-30", "sumario, pág. 1")]),
    ("evt-1931-06-23-plazas-maestros", "Creación de 7.000 plazas de maestros y maestras", "educativo",
     "1931-06-23", "dia", ["plc-espana"], "estatal", None,
     [("Un decreto de 23 de junio de 1931 autoriza al Ministerio de Instrucción Pública a crear, a partir del 1 de julio, 7.000 plazas de maestros y maestras con destino a las escuelas nacionales.",
       "documento", "doc-gaceta-1931-06-24", "págs. 1612-1613"),
      ("Según los informes de la Inspección que cita el preámbulo, existían en España 35.716 escuelas unitarias y secciones de graduada, y harían falta 27.151 más para atender a la población escolar.",
       "estimacion", "doc-gaceta-1931-06-24", "preámbulo, pág. 1612", "Gobierno provisional de la República, a partir de los informes de las inspecciones provinciales de Primera enseñanza")]),
    ("evt-1931-12-09-constitucion", "Aprobación de la Constitución de la República Española", "legislativo",
     "1931-12-09", "dia", ["plc-espana", "plc-madrid"], "estatal", "Q2745432",
     [("Las Cortes Constituyentes aprueban la Constitución de la República Española, fechada en el Palacio de las Cortes el 9 de diciembre de 1931.",
       "documento", "doc-gaceta-1931-12-10", "pág. 1578"),
      ("La Gaceta de Madrid publica el texto al día siguiente, 10 de diciembre de 1931.",
       "documento", "doc-gaceta-1931-12-10", "pág. 1578"),
      ("Su artículo 48 declara que el servicio de la cultura es atribución esencial del Estado, prestado mediante instituciones educativas enlazadas por el sistema de la escuela unificada; que la enseñanza primaria será gratuita y obligatoria; que los maestros, profesores y catedráticos de la enseñanza oficial son funcionarios públicos, y reconoce la libertad de cátedra.",
       "documento", "doc-gaceta-1931-12-10", "art. 48, pág. 1582")]),
    ("evt-1932-09-15-estatuto-cataluna", "Ley del Estatuto de Cataluña", "legislativo",
     "1932-09-15", "dia", ["plc-espana"] + CATALUNA, "region", "Q4896294",
     [("La ley relativa al Estatuto de Cataluña se firma en San Sebastián el 15 de septiembre de 1932 y se publica en la Gaceta del 21 de septiembre.",
       "documento", "doc-gaceta-1932-09-21", "págs. 2090-2094")]),
    ("evt-1932-09-15-reforma-agraria", "Ley de Reforma Agraria", "legislativo",
     "1932-09-15", "dia", ["plc-espana"], "estatal", None,
     [("La ley relativa a la Reforma Agraria se firma en San Sebastián el 15 de septiembre de 1932 y se publica en la Gaceta del 21 de septiembre.",
       "documento", "doc-gaceta-1932-09-21", "págs. 2095-2102"),
      ("La ley encarga su aplicación a un Instituto de Reforma Agraria, con juntas provinciales.",
       "documento", "doc-gaceta-1932-09-21", "págs. 2095-2096")]),
    ("evt-1933-06-03-congregaciones", "Ley de Confesiones y Congregaciones Religiosas", "legislativo",
     "1933-06-03", "dia", ["plc-espana"], "estatal", "Q91117278",
     [("La Gaceta de Madrid del 3 de junio de 1933 publica la ley relativa a Confesiones y Congregaciones Religiosas, firmada el 2 de junio.",
       "documento", "doc-gaceta-1933-06-03", "págs. 1651-1653"),
      ("Su artículo 30 dispone que las órdenes y congregaciones religiosas no podrán dedicarse al ejercicio de la enseñanza, salvo la destinada a la formación de sus propios miembros, y encarga a la inspección del Estado impedir que sostengan colegios por medio de seglares interpuestos.",
       "documento", "doc-gaceta-1933-06-03", "art. 30, págs. 1652-1653"),
      ("Una disposición transitoria fija el cese de esa enseñanza el 1 de octubre siguiente para toda clase de enseñanzas, excepto la primaria, que terminará el 31 de diciembre.",
       "documento", "doc-gaceta-1933-06-03", "disposiciones transitorias, pág. 1653")]),
    ("evt-1933-10-10-disolucion-cortes", "Disolución de las Cortes Constituyentes y convocatoria de elecciones generales", "electoral",
     "1933-10-10", "dia", ["plc-espana"], "estatal", None,
     [("La Gaceta del 10 de octubre de 1933 publica el decreto que declara disueltas las Cortes Constituyentes.",
       "documento", "doc-gaceta-1933-10-10", "págs. 251-252"),
      ("Otro decreto del mismo número fija las elecciones generales a Cortes para el domingo 19 de noviembre de 1933.",
       "documento", "doc-gaceta-1933-10-10", "sumario")]),
    ("evt-1934-10-07-estado-guerra", "Declaración del estado de guerra en todo el territorio de la República", "politico",
     "1934-10-07", "dia", ["plc-espana", "plc-prov-33"] + CATALUNA, "estatal", "Q16782534",
     [("La Gaceta del 7 de octubre de 1934 publica el decreto que declara el estado de guerra en todo el territorio de la República.",
       "documento", "doc-gaceta-1934-10-07", "pág. 194"),
      ("La nota del Gobierno que lo acompaña justifica la medida por los sucesos de Asturias y por la proclamación del «Estat Català» por el presidente de la Generalidad.",
       "documento", "doc-gaceta-1934-10-07", "pág. 194")]),
    ("evt-1936-07-19-decretos-sublevacion", "Primeros decretos del Gobierno de la República frente a la sublevación militar", "militar",
     "1936-07-19", "dia", ["plc-espana", "plc-madrid"], "estatal", "Q2436825",
     [("El 19 de julio de 1936 el Gobierno de la República anula por decreto la declaración del estado de guerra en todas las plazas de la Península, Marruecos, Baleares y Canarias donde se hubiera dictado.",
       "documento", "doc-gaceta-1936-07-19", "pág. 723"),
      ("El mismo día declara disueltas las unidades del Ejército que toman parte en el «movimiento insurreccional» y licenciadas las tropas cuyos mandos «se han colocado frente a la legalidad republicana».",
       "documento", "doc-gaceta-1936-07-19", "pág. 724")]),
    ("evt-1936-10-06-estatuto-vasco", "Ley del Estatuto Vasco", "legislativo",
     "1936-10-07", "dia", ["plc-espana", "plc-prov-01", "plc-prov-20", "plc-prov-48"], "region", "Q4895036",
     [("La Gaceta de Madrid del 7 de octubre de 1936 publica la ley relativa al Estatuto Vasco.",
       "documento", "doc-gaceta-1936-10-07", "págs. 211-214")]),
    ("evt-1936-07-19-gobiernos-martinez-barrio-giral", "Gobierno de Martínez Barrio y paso al Gobierno de Giral", "politico",
     "1936-07-19", "intervalo", ["plc-espana", "plc-madrid"], "estatal", None,
     [("Por decreto de 19 de julio de 1936, el presidente de la República, Manuel Azaña, nombra Presidente del Consejo de Ministros a Diego Martínez Barrio.",
       "documento", "doc-gaceta-1936-07-19", "pág. 722"),
      ("La Gaceta del 20 de julio publica la dimisión de Martínez Barrio y el nombramiento de José Giral Pereira como Presidente del Consejo de Ministros.",
       "documento", "doc-gaceta-1936-07-20", "pág. 739")]),
    ("evt-1936-10-06-tribunal-especial", "Creación en Madrid de un Tribunal especial de responsabilidades civiles", "politico",
     "1936-10-07", "dia", ["plc-espana", "plc-madrid"], "estatal", None,
     [("La Gaceta del 7 de octubre de 1936 publica el decreto que crea en Madrid un Tribunal especial para exigir las responsabilidades civiles derivadas de los delitos de rebelión, sedición, contra la seguridad del Estado, traición y espionaje, y las de quienes hubieran participado en el «movimiento rebelde».",
       "documento", "doc-gaceta-1936-10-07", "págs. 215-216")]),
    ("evt-1931-06-28-elecciones-constituyentes", "Elecciones a Cortes Constituyentes", "electoral",
     "1931-06-28", "dia", ["plc-espana"], "estatal", None,
     [("Un decreto publicado en la Gaceta del 4 de junio de 1931 fija las elecciones a Cortes Constituyentes en toda España para el 28 de junio, con arreglo al decreto de 8 de mayo y a la ley electoral de 1907.",
       "documento", "doc-gaceta-1931-06-04", "págs. 1174-1175"),
      ("El mismo decreto dispone que las Cortes, de una sola Cámara elegida por sufragio popular directo, se reúnan en el Palacio del Congreso el 14 de julio.",
       "documento", "doc-gaceta-1931-06-04", "págs. 1174-1175")]),
    ("evt-1933-11-19-elecciones-generales", "Elecciones generales a Cortes de 1933", "electoral",
     "1933-11-19", "dia", ["plc-espana"], "estatal", "Q3132158",
     [("Un decreto publicado en la Gaceta del 10 de octubre de 1933 dispone que las elecciones generales a Cortes se celebren el domingo 19 de noviembre de 1933.",
       "documento", "doc-gaceta-1933-10-10", "sumario")]),
    ("evt-1936-10-07-expropiacion-fincas", "Decreto de expropiación de fincas rústicas de quienes intervinieron en la sublevación", "economico",
     "1936-10-07", "dia", ["plc-espana"], "estatal", None,
     [("Un decreto de 7 de octubre de 1936 acuerda la expropiación sin indemnización y a favor del Estado de las fincas rústicas pertenecientes el 18 de julio a personas que hubieran intervenido directa o indirectamente en el movimiento insurreccional contra la República.",
       "documento", "doc-gaceta-1936-10-08", "págs. 236-237")]),
    ("evt-1936-10-08-plazas-maestros", "Ley de creación de 5.300 plazas de maestros y maestras", "educativo",
     "1936-10-08", "dia", ["plc-espana"], "estatal", None,
     [("La Gaceta del 8 de octubre de 1936 publica la ley que aprueba la creación de 5.300 plazas de maestros y maestras con destino a escuelas nacionales, autorizada por decreto de 28 de febrero de 1936, a partir del 1 de octubre.",
       "documento", "doc-gaceta-1936-10-08", "págs. 234-235")]),
    ("evt-1936-09-25-bombardeos-durango", "Bombardeos aéreos de Durango", "violencia",
     "1936-09-25", "intervalo", ["plc-mun-48027"], "municipio", None,
     [("Según la base de datos de bombardeos de Gogora, la aviación del bando sublevado bombardeó Durango al menos 14 veces entre el 25 de septiembre de 1936 y el 29 de abril de 1937, con participación de aviación alemana e italiana; buena parte de los ataques se concentraron en abril de 1937.",
       "documento", "doc-gogora-bombardeos", "fila «Durango»"),
      ("Gogora estima más de 350 víctimas en total, sin cifra exacta.",
       "estimacion", "doc-gogora-bombardeos", "fila «Durango»", "Gogora, Instituto de la Memoria del Gobierno Vasco")]),
    ("evt-1936-09-17-bombardeos-vitoria", "Bombardeos aéreos republicanos de Vitoria", "violencia",
     "1936-09-17", "intervalo", ["plc-mun-01059"], "municipio", None,
     [("Según la base de datos de bombardeos de Gogora, la aviación republicana bombardeó Vitoria en 10 ocasiones entre el 17 de septiembre de 1936 y el 29 de mayo de 1937, con daños en fábricas, cuarteles de Caballería y la estación del Norte.",
       "documento", "doc-gogora-bombardeos", "fila «Vitoria-Gasteiz»"),
      ("La base de datos indica que no hay información concreta sobre el número de víctimas.",
       "documento", "doc-gogora-bombardeos", "fila «Vitoria-Gasteiz»")]),
    ("evt-1937-04-26-bombardeo-gernika", "Bombardeo de Gernika", "violencia",
     "1937-04-26", "dia", ["plc-mun-48046"], "municipio", "Q170351",
     [("Según la base de datos de bombardeos de Gogora, la aviación del bando sublevado, con aviones alemanes e italianos, bombardeó Gernika el 26 de abril de 1937 con bombas explosivas e incendiarias; más del 90 % de los edificios sufrió daños.",
       "documento", "doc-gogora-bombardeos", "fila «Gernika»"),
      ("Un informe del Gobierno Vasco de junio de 1937 habló de 1.654 muertos y 889 heridos.",
       "estimacion", "doc-gogora-bombardeos", "fila «Gernika»", "Gobierno Vasco, informe de junio de 1937, citado por Gogora"),
      ("Gogora cifra hoy las víctimas en más de dos mil. Otras estimaciones historiográficas son sensiblemente inferiores; la cifra sigue en debate.",
       "estimacion", "doc-gogora-bombardeos", "fila «Gernika»", "Gogora, Instituto de la Memoria del Gobierno Vasco")]),
]


def dump(path: pathlib.Path, obj: dict) -> None:
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# Fin de los acontecimientos con precisión «intervalo» (leído en la misma evidencia)
END_DATES = {
    "evt-1936-09-25-bombardeos-durango": "1937-04-29",
    "evt-1936-09-17-bombardeos-vitoria": "1937-05-29",
    "evt-1936-07-19-gobiernos-martinez-barrio-giral": "1936-07-20",
}


def claim(text, kind, doc, loc, attributed_to=None):
    c = {"text": text, "kind": kind, "evidence": [{"document_id": doc, "locator": loc}]}
    if attributed_to:
        c["attributed_to"] = attributed_to
    return c


def main() -> None:
    for pid, (name, ine, parent, centroid) in MUNICIPIOS.items():
        dump(OUT / f"places/{pid}.json", {
            "id": pid, "canonical_name": name, "place_type": "municipio", "parent_id": parent, "ine_code": ine,
            "centroid": centroid, "geometry_ref": f"municipios_1930#cod_ine={ine}", "geometry_precision": "centroide",
            "source_ids": ["F033"], "review": dict(REVIEW)})
    dump(OUT / f"documents/{GOGORA_DOC}.json", {
        "id": GOGORA_DOC, "title": "Bombardeos de la Guerra Civil en Euskadi (base de datos de Gogora, Open Data Euskadi)",
        "document_type": "tabla_estadistica", "source_ids": ["F040"],
        "custodian": "Gogora, Instituto de la Memoria, la Convivencia y los Derechos Humanos (Gobierno Vasco)",
        "canonical_url": "https://opendata.euskadi.eus/catalogo/-/bombardeos-de-la-guerra-civil-en-euskadi/",
        "date": "2017-12-26", "date_precision": "dia",
        "summary": "197 localidades bombardeadas en Euskadi durante la guerra, con número de bombardeos, fechas, bando atacante, descripción y fuentes (partes de operaciones, archivos italianos y británicos, prensa de la época).",
        "context": "Compilación institucional del Gobierno Vasco a partir de fuentes primarias de ambos bandos y de prensa. Incluye bombardeos de la aviación sublevada (la gran mayoría) y de la republicana. Las cifras de víctimas son estimaciones de la propia base o de las fuentes que cita.",
        "text_origin": "ninguno",
        "rights": {"status": "reuse_conditions", "action": "enlazar", "attribution": "Fuente: Gogora / Open Data Euskadi",
                   "evidence_url": "https://opendata.euskadi.eus/catalogo/-/bombardeos-de-la-guerra-civil-en-euskadi/", "checked_at": TODAY,
                   "note": "Licencia de la ficha no legible sin JavaScript; pendiente de verificar (Open Data Euskadi suele publicar con CC BY 4.0). Mientras, solo enlace y paráfrasis."},
        "review": dict(REVIEW), "consulted_at": TODAY})
    for key, (fecha, num, pags, titulo, resumen, contexto, lugares) in GACETAS.items():
        y, m, d = fecha.split("-")
        dump(OUT / f"documents/doc-{key}.json", {
            "id": f"doc-{key}", "title": titulo, "title_original": f"Gaceta de Madrid. Núm. {num}",
            "document_type": "disposicion", "source_ids": ["F015"],
            "custodian": "Agencia Estatal Boletín Oficial del Estado (colección histórica Gazeta)",
            "signature": f"Gaceta de Madrid, núm. {num}, {d}/{m}/{y}, págs. {pags}",
            "canonical_url": f"https://www.boe.es/gazeta/dias/{y}/{m}/{d}/pdfs/GMD-{y}-{num:03d}.pdf",
            "date": fecha, "date_precision": "dia", "place_ids": lugares,
            "summary": resumen, "context": contexto, "text_origin": "ocr_automatico",
            "rights": dict(BOE_RIGHTS), "review": dict(REVIEW), "consulted_at": TODAY,
        })
    for eid, titulo, tipo, fecha, prec, lugares, esp, qid, claims in EVENTOS:
        obj = {"id": eid, "title": titulo, "event_type": tipo, "start_date": fecha, "date_precision": prec,
               "place_ids": lugares, "spatial_precision": esp,
               "claims": [claim(*c) for c in claims],
               "review": dict(REVIEW)}
        if qid:
            obj["wikidata"] = qid
        if eid in END_DATES:
            obj["end_date"] = END_DATES[eid]
        dump(OUT / f"events/{eid}.json", obj)
    print(f"{len(GACETAS)} documentos, {len(EVENTOS)} acontecimientos")


if __name__ == "__main__":
    main()
