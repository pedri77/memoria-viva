"""Registro de fuentes: quién produjo cada fondo, si es consultable en línea y su sesgo previsible,
y archivos que faltaban para que estén representados los dos bandos, la Iglesia y los archivos extranjeros.

Criterio (David, 15-11-2026): ser ecuánimes no es una simetría forzada (guía editorial §1.4), sino no dejar
fuera las fuentes de ningún lado y decir de cada una quién la produjo y con qué sesgo.

Los archivos nuevos entran como «candidate»: su URL responde (comprobado el 15-11-2026), pero su forma de
acceso y su contenido digitalizado están por verificar. No se afirma nada de sus fondos que no conste en su web.

Uso: python3 -I scripts/etl/fuentes_equilibrio.py   (idempotente)
"""
import json
import pathlib

OUT = pathlib.Path(__file__).resolve().parents[2] / "data/canonical/sources"
HOY = "2026-11-15"
R, S = "oficial_republica", "oficial_sublevados"
PR, OS = "partidos_bando_republicano", "organizaciones_bando_sublevado"
EST, INV, BIB, MEM, EXT, IGL = "estadistica_y_administracion", "investigacion", "bibliotecas_y_prensa", "memoria_actual", "extranjero", "iglesia"

# Fuentes ya registradas: (productores, digital)
EXISTENTES = {
    "F001": ([R, S], "parcial"), "F002": ([PR, S], "parcial"), "F003": ([S], "parcial"), "F004": ([EXT], "parcial"),
    "F005": ([PR, R], "parcial"), "F006": ([S], "parcial"), "F007": ([BIB], "si"), "F008": ([BIB], "si"),
    "F009": ([EST], "si"), "F010": ([EST], "si"), "F011": ([EST], "si"), "F012": ([EST], "si"),
    "F013": ([MEM], "parcial"), "F014": ([MEM], "parcial"), "F015": ([R, S], "si"), "F016": ([R], "parcial"),
    "F017": ([EST], "parcial"), "F018": ([R, S], "parcial"), "F019": ([R, S], "no"), "F020": ([R, S], "parcial"),
    "F021": ([BIB], "si"), "F022": ([BIB], "si"), "F023": ([BIB], "si"), "F024": ([S], "parcial"), "F025": ([BIB], "parcial"),
    "F026": ([EXT], "parcial"), "F027": ([EXT], "parcial"), "F028": ([EXT], "parcial"), "F029": ([EXT], "parcial"),
    "F030": ([INV], "si"), "F031": ([R], "si"), "F032": ([INV], "si"), "F033": ([INV], "si"), "F034": ([EST], "si"),
    "F035": ([EST], "si"), "F036": ([BIB], "si"), "F037": ([BIB], "si"), "F038": ([BIB], "si"), "F039": ([BIB], "si"),
    "F040": ([MEM], "si"), "F041": ([MEM], "si"), "F042": ([MEM], "si"), "F043": ([MEM], "si"), "F044": ([MEM], "si"),
    "F045": ([MEM], "si"), "F046": ([INV, MEM], "si"), "F047": ([R], "si"), "F048": ([MEM], "si"), "F049": ([PR], "parcial"),
    "F050": ([BIB], "si"), "F051": ([BIB], "si"), "F052": ([BIB], "si"), "F053": ([INV], "parcial"), "F054": ([INV], "si"),
    "F055": ([BIB], "si"), "F056": ([INV], "si"), "F057": ([EST], "parcial"), "F058": ([INV], "si"), "F059": ([MEM], "si"),
    "F060": ([EST], "si"),
}
SESGO_EXISTENTES = {
    "F002": "Documentación incautada durante la guerra y la posguerra por las autoridades franquistas a partidos, sindicatos, logias y particulares para usarla en la represión: los documentos son de organizaciones del bando republicano, pero el fondo se formó con fines represivos.",
    "F003": "Registros producidos por la represión franquista (fichas, expedientes); dicen lo que anotaron sus autores.",
    "F006": "Fotografías de la propaganda oficial: muestran lo que se quería mostrar.",
    "F024": "Archivo de la Administración del Estado franquista: acredita sus decisiones, no su justicia.",
    "F049": "Archivos de organizaciones libertarias (CNT, FAI y otras): documentación de parte.",
}

NUEVAS = [
    ("F061", "Causa General (Archivo Histórico Nacional, digitalizada en PARES)", "https://pares.cultura.gob.es/", "P1", [S], "si",
     "consulta digital en PARES; por verificar la descarga", "1936-1939",
     "Instruida por el Ministerio Fiscal del Estado franquista desde 1940 para documentar la violencia en la zona republicana. Útil para nombres, lugares y fechas; de parte en atribuciones, cifras y calificaciones. Contiene datos personales."),
    ("F062", "Archivo General Militar de Ávila (documentación de los ejércitos de las dos zonas)", "https://www.defensa.gob.es/", "P1", [R, S], "no",
     "consulta presencial; por verificar qué está descrito en línea", "1936-1939",
     "Documentación militar de los dos ejércitos: órdenes, partes y organización; cada parte refleja la visión de quien lo redactó."),
    ("F063", "Consejos de guerra (sumarios de los tribunales militares)", "https://www.defensa.gob.es/", "P2", [S], "restringido",
     "consulta presencial en los archivos de los tribunales militares territoriales y de Defensa; datos personales protegidos", "1936-1950",
     "Procedimientos de la justicia militar franquista: documentan acusaciones y condenas según quienes las dictaron."),
    ("F064", "Archivo General de la Administración: fondos de FET y de las JONS", "https://www.cultura.gob.es/cultura/areas/archivos/mc/archivos/aga/portada.html", "P2", [OS], "no",
     "descripciones en PARES; consulta presencial", "1937-1977",
     "Documentación del partido único del franquismo: de parte."),
    ("F065", "Archivo Histórico del Partido Comunista de España", "https://www.archivohistoricopce.org/", "P1", [PR], "parcial",
     "cita previa; fotografías de la guerra en Europeana; su robots.txt no restringe la web, pero Patrimonio Digital Complutense veta /s/patrimonio/item*", "1920-1991",
     "Archivo de un partido del bando republicano: documentación de parte."),
    ("F066", "Fundación Pablo Iglesias (archivo del PSOE)", "https://fpabloiglesias.es/", "P1", [PR], "parcial",
     "por verificar", "1879-actualidad", "Archivo de un partido del bando republicano: documentación de parte."),
    ("F067", "Fundación Francisco Largo Caballero (archivo de la UGT)", "https://fflc.ugt.org/", "P2", [PR], "parcial",
     "por verificar", "1888-actualidad", "Archivo de un sindicato del bando republicano: documentación de parte."),
    ("F068", "Fundación Anselmo Lorenzo (archivo de la CNT)", "https://fal.cnt.es/", "P2", [PR], "parcial",
     "por verificar; fotografías de la guerra digitalizadas según la prensa", "1910-actualidad", "Archivo de un sindicato libertario: documentación de parte."),
    ("F069", "Fundación Sabino Arana (archivo del nacionalismo vasco)", "https://www.sabinoarana.eus/", "P2", [PR], "parcial",
     "por verificar", "1895-actualidad", "Archivo del nacionalismo vasco, alineado con la República en la guerra: documentación de parte."),
    ("F070", "Arxiu Nacional de Catalunya", "https://anc.gencat.cat/", "P2", [R, PR], "parcial",
     "por verificar", "siglos XIX-XXI", "Fondos de la Generalitat republicana y de partidos y particulares catalanes."),
    ("F071", "Fundación Nacional Francisco Franco (archivo personal de Franco)", "https://fnff.es/", "P2", [S], "restringido",
     "acceso restringido por la fundación; por verificar las condiciones", "1936-1975",
     "Archivo personal del jefe del bando sublevado custodiado por una fundación privada que defiende su figura: documentación de parte y de acceso no garantizado."),
    ("F072", "Biblioteca Virtual Larramendi (carlismo y pensamiento tradicionalista)", "https://www.larramendi.es/", "P2", [OS, INV], "si",
     "biblioteca digital; por verificar licencias", "siglos XIX-XX", "Publicaciones del carlismo y del pensamiento tradicionalista, integrado en el bando sublevado: de parte."),
    ("F073", "Real Academia de la Historia (archivos personales)", "https://www.rah.es/", "P2", [INV], "parcial",
     "por verificar", "siglos XIX-XX", "Archivos personales depositados; cada uno refleja a su autor."),
    ("F074", "Archivos diocesanos y de órdenes religiosas", "https://www.conferenciaepiscopal.es/", "P2", [IGL], "no",
     "cada diócesis y orden tiene su archivo; consulta presencial; la dirección es solo un punto de partida", "1936-1939",
     "Documentación de la Iglesia, víctima de la violencia en la zona republicana y apoyo del bando sublevado: de parte."),
    ("F075", "Archivo Apostólico Vaticano (pontificado de Pío XI)", "https://www.archivioapostolicovaticano.va/", "P2", [IGL, EXT], "no",
     "consulta presencial para investigadores", "1922-1939", "Diplomacia de la Santa Sede: de parte."),
    ("F076", "Archivo Estatal Ruso de Historia Sociopolítica (RGASPI: Komintern y Brigadas Internacionales)", "http://rgaspi.org/", "P2", [EXT], "parcial",
     "por verificar; acceso internacional variable", "1919-1943", "Documentación de la Internacional Comunista y de la URSS sobre la intervención en España: de parte."),
    ("F077", "Bundesarchiv (Alemania)", "https://www.bundesarchiv.de/", "P2", [EXT], "parcial",
     "por verificar", "1933-1945", "Documentación del Estado nazi, incluida su intervención en apoyo del bando sublevado: de parte."),
    ("F078", "Archivio Centrale dello Stato (Italia)", "https://acs.cultura.gov.it/", "P2", [EXT], "parcial",
     "por verificar", "1922-1945", "Documentación del Estado fascista italiano, incluida su intervención en apoyo del bando sublevado: de parte."),
    ("F079", "National Archives and Records Administration (Estados Unidos)", "https://www.archives.gov/", "P2", [EXT], "parcial",
     "por verificar; las publicaciones del Gobierno federal de EE. UU. son de dominio público", "1931-1939", "Diplomacia de un país neutral; su mirada es la de su servicio exterior."),
    ("F080", "Archivos de la Sociedad de Naciones (ONU, Ginebra)", "https://archives.ungeneva.org/", "P2", [EXT], "parcial",
     "por verificar", "1931-1939", "Debates y documentos internacionales sobre la guerra de España."),
    ("F081", "SIDBRINT · Brigadas Internacionales (Universitat de Barcelona)", "https://sidbrint.ub.edu/", "P2", [INV], "si",
     "portal web; datos personales: solo cifras agregadas y con permiso de la UB", "1936-1939", "Base de investigación universitaria sobre los voluntarios internacionales."),
]


def main() -> None:
    for f in sorted(OUT.glob("F*.json")):
        d = json.loads(f.read_text())
        if d["id"] in EXISTENTES:
            d["productores"], d["digital"] = EXISTENTES[d["id"]]
            if d["id"] in SESGO_EXISTENTES:
                d["sesgo"] = SESGO_EXISTENTES[d["id"]]
            f.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n")
    for fid, nombre, url, prio, prod, dig, acceso, anios, sesgo in NUEVAS:
        (OUT / f"{fid}.json").write_text(json.dumps({
            "id": fid, "name": nombre, "url": url, "priority": prio, "status": "candidate",
            "license": "por verificar", "access": acceso, "years": anios,
            "risks": "Fuente por auditar: acceso, derechos y contenido digitalizado sin comprobar.",
            "checked_at": HOY, "productores": prod, "digital": dig, "sesgo": sesgo}, ensure_ascii=False, indent=2) + "\n")
    print(f"{len(EXISTENTES)} clasificadas, {len(NUEVAS)} nuevas")


if __name__ == "__main__":
    main()
