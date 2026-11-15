"""Imágenes con derechos abiertos verificadas una a una (Wikimedia Commons, con custodio institucional).

Criterio (David, 15-11-2026): solo imágenes con derechos abiertos explícitos, verificadas una a una y en
equilibrio entre bandos (por parejas). Se descartan las de procedencia dudosa aunque Commons las marque como
dominio público: tomadas de agencias comerciales (Getty/Keystone), de prensa actual o de webs de aficionados.
No se incluyen imágenes de violencia: esperan a los revisores (R1).
Carteles: «Los Nacionales» (BnF) es una sátira del Ministerio de Propaganda de la República contra la Junta de Burgos,
no un cartel sublevado; se descarta. La pareja de «Aixafem el feixisme» (BnF) es «¡Arriba España!» (Biblioteca Regional
de Madrid), localizado con la API de Europeana (clave pública de pruebas api2demo).

Biblioteca Virtual de Madrid (bibliotecavirtualmadrid.comunidad.madrid): sin robots.txt (404, comprobado 15-11-2026);
cada ficha declara «Derechos: Obra de dominio público». BiValDi (bivaldi.gva.es) veta en robots.txt a claudebot y
anthropic-ai: no se consulta.

Cada imagen guarda autor, fecha, custodio, licencia, enlace a su ficha y, si existe, el pie original del
archivo, que puede ser de parte (los pies del Bundesarchiv proceden de la RDA o del Tercer Reich).

Robots: commons.wikimedia.org (API) y upload.wikimedia.org solo vetan /wikipedia/commons/archive/ (comprobado 15-11-2026).
Uso: python3 -I scripts/etl/imagenes_commons.py   (idempotente; descarga miniaturas de 1000 px)
"""
import json
import pathlib
import time
import urllib.parse
import urllib.request

RAIZ = pathlib.Path(__file__).resolve().parents[2]
DEST = RAIZ / "site/public/img/archivo"
OUT = RAIZ / "data/imagenes.json"
UA = {"User-Agent": "memoria-viva/0.1 (https://github.com/pedri77/memoria-viva; proyecto de investigación sin ánimo de lucro)"}

BVM = "https://bibliotecavirtualmadrid.comunidad.madrid/bvmadrid_publicacion"
PDM = "https://creativecommons.org/publicdomain/mark/1.0/deed.es"

IMAGENES = [
    {"id": "img-cartel-aixafem-feixisme", "pareja": "propaganda", "bando": "republicano",
     "fichero": "File:Aixafem el feixisme Ecrasons le Fascime affiche, non identifié.jpg",
     "titulo": "«Aixafem el feixisme» (Aplastemos el fascismo)",
     "pie": "Cartel editado por la Comissaria de Propaganda de la Generalitat de Catalunya: una alpargata pisa una esvástica. Propaganda del bando republicano.",
     "autor": "Autor no identificado (fotografía firmada «Fot. Catalá»)", "fecha": "1936-1939",
     "custodio": "Bibliothèque nationale de France, ENT QB-1 (1936)-FT6",
     "licencia": "Dominio público (declarado por la BnF)", "licencia_url": PDM,
     "verificacion": "Ficha de la BnF reproducida en Commons: editor, fecha, signatura y «Rights: Public domain»."},
    {"id": "img-cartel-arriba-espana", "pareja": "propaganda", "bando": "sublevado",
     "bvm": {"registro": 24500, "imagen": 12131433},
     "titulo": "«¡Arriba España!»",
     "pie": "Dibujo para cartel, a la acuarela, con el yugo y las flechas de Falange: ciudadanos armados con la mano alzada. Propaganda del bando sublevado.",
     "autor": "Autor anónimo", "fecha": "hacia 1937",
     "custodio": "Biblioteca Regional de Madrid, Mg.XXVI/74,9",
     "licencia": "Dominio público (declarado por la Biblioteca Regional de Madrid: obra anónima sin derechos de autor localizados)", "licencia_url": PDM,
     "verificacion": "Ficha de la Biblioteca Virtual de Madrid, registro 24500: «Derechos: Obra de dominio público»."},
    {"id": "img-miliciana-barcelona", "pareja": "movilizacion", "bando": "republicano",
     "bvm": {"registro": 24512, "imagen": 12131438},
     "titulo": "Milicianos en una calle de Barcelona",
     "pie": "Dos hombres y una mujer, uniformados y armados, posan en Barcelona. Copia de agencia retocada a mano, como muchas fotos de prensa de la época.",
     "autor": "Fotógrafo anónimo, distribuida por Keystone View Company (Londres)", "fecha": "julio de 1936",
     "custodio": "Biblioteca Regional de Madrid, Mg.XXVIII/1320",
     "licencia": "Dominio público (declarado por la Biblioteca Regional de Madrid)", "licencia_url": PDM,
     "verificacion": "Ficha de la Biblioteca Virtual de Madrid, registro 24512: «Derechos: Obra de dominio público»; sello al verso «D.M. 28 JUL 1936»."},
    {"id": "img-flechas-burgos", "pareja": "movilizacion", "bando": "sublevado",
     "bvm": {"registro": 24520, "imagen": 12131560},
     "titulo": "Niños de las Flechas desfilando en Burgos",
     "pie": "Niños desfilan en formación con fusiles de imitación por un puente de Burgos, sede del Gobierno de la zona sublevada.",
     "pie_original": "Nota de la agencia al verso: «Spain's Young Fascists» (Los jóvenes fascistas de España). Pie de prensa británica.",
     "autor": "Fotógrafo anónimo, distribuida por Keystone View Company (Londres)", "fecha": "1936",
     "custodio": "Biblioteca Regional de Madrid, Mg.XXVIII/1381",
     "licencia": "Dominio público (declarado por la Biblioteca Regional de Madrid)", "licencia_url": PDM,
     "verificacion": "Ficha de la Biblioteca Virtual de Madrid, registro 24520: «Derechos: Obra de dominio público»."},
    {"id": "img-soldados-puerta-del-sol", "pareja": "frente", "bando": "republicano",
     "bvm": {"registro": 24518, "imagen": 12131692},
     "titulo": "Soldados aclamados en la Puerta del Sol camino del frente",
     "pie": "Soldados en un carro tirado por caballos pasan por la Puerta del Sol de Madrid hacia el frente, entre vecinos que los saludan con el puño en alto.",
     "autor": "Fotógrafo anónimo, distribuida por The Associated Press of Great Britain (Londres)", "fecha": "1936",
     "custodio": "Biblioteca Regional de Madrid, Mg.XXVIII/1448",
     "licencia": "Dominio público (declarado por la Biblioteca Regional de Madrid)", "licencia_url": PDM,
     "verificacion": "Ficha de la Biblioteca Virtual de Madrid, registro 24518: «Derechos: Obra de dominio público». Lleva al verso el sello «Copyright Associated Press Photo»; como mera fotografía de 1936, su protección en España (25 años, art. 128 LPI) está extinguida."},
    {"id": "img-soldados-burgos", "pareja": "frente", "bando": "sublevado",
     "bvm": {"registro": 24608, "imagen": 12131458},
     "titulo": "Soldados aclamados a su paso por Burgos",
     "pie": "Una columna de soldados avanza por una calle principal de Burgos entre civiles que la saludan con el brazo en alto.",
     "autor": "Fotógrafo anónimo, distribuida por The Associated Press of Great Britain (Londres)", "fecha": "1936",
     "custodio": "Biblioteca Regional de Madrid, Mg.XXVIII/1330",
     "licencia": "Dominio público (declarado por la Biblioteca Regional de Madrid)", "licencia_url": PDM,
     "verificacion": "Ficha de la Biblioteca Virtual de Madrid, registro 24608: «Derechos: Obra de dominio público». Lleva al verso el sello «Copyright Associated Press Photo»; como mera fotografía de 1936, su protección en España (25 años, art. 128 LPI) está extinguida."},
    {"id": "img-retrato-durruti", "pareja": "retratos", "bando": "republicano",
     "bvm": {"registro": 24508, "imagen": 12131426},
     "titulo": "«Durruti. 20 noviembre 1936»",
     "pie": "Dibujo para cartel, a la acuarela: retrato del sindicalista anarquista Buenaventura Durruti con motivo de su muerte, según la ficha de la biblioteca.",
     "autor": "Autor anónimo", "fecha": "hacia 1937",
     "custodio": "Biblioteca Regional de Madrid, Mg.XXVI/74,2",
     "licencia": "Dominio público (declarado por la Biblioteca Regional de Madrid: obra anónima sin derechos de autor localizados)", "licencia_url": PDM,
     "verificacion": "Ficha de la Biblioteca Virtual de Madrid, registro 24508: «Derechos: Obra de dominio público»."},
    {"id": "img-retrato-jose-antonio", "pareja": "retratos", "bando": "sublevado",
     "bvm": {"registro": 24507, "imagen": 12131427},
     "titulo": "Retrato de José Antonio Primo de Rivera",
     "pie": "Dibujo para cartel, a la acuarela: retrato del fundador de Falange Española, con camisa azul.",
     "autor": "Autor anónimo", "fecha": "hacia 1937",
     "custodio": "Biblioteca Regional de Madrid, Mg.XXVI/74,3",
     "licencia": "Dominio público (declarado por la Biblioteca Regional de Madrid: obra anónima sin derechos de autor localizados)", "licencia_url": PDM,
     "verificacion": "Ficha de la Biblioteca Virtual de Madrid, registro 24507: «Derechos: Obra de dominio público»."},
    {"id": "img-batallon-etkar-andre", "pareja": "extranjeros", "bando": "republicano",
     "fichero": "File:Bundesarchiv Bild 183-H28510, Spanien, Gefechtsstand des Etkar André Bataillons.jpg",
     "titulo": "El batallón «Etkar André» de las Brigadas Internacionales, en reposo tras el frente",
     "pie": "Voluntarios alemanes de las Brigadas Internacionales, que combatieron con la República.",
     "pie_original": "Pie del archivo de la RDA (ADN-ZB/IML-ZPA): «Guerra nacional-revolucionaria del pueblo español…». Vocabulario de parte.",
     "autor": "Fotógrafo desconocido", "fecha": "1936",
     "custodio": "Bundesarchiv, Bild 183-H28510",
     "licencia": "CC BY-SA 3.0 DE", "licencia_url": "https://creativecommons.org/licenses/by-sa/3.0/de/deed.es",
     "verificacion": "Donación del Bundesarchiv a Commons (proyecto de cooperación) con su signatura."},
    {"id": "img-legion-condor-avila", "pareja": "extranjeros", "bando": "sublevado",
     "fichero": "File:Bundesarchiv Bild 183-E20569-21, Spanien, Ausbildung durch \"Legion Condor\".jpg",
     "titulo": "Escuela de infantería de Ávila con instructores de la Legión Cóndor",
     "pie": "Aspirantes a oficial del ejército sublevado formados por instructores alemanes y españoles. La Legión Cóndor fue la fuerza enviada por la Alemania nazi en apoyo de Franco.",
     "pie_original": "Pie del archivo de la RDA (Zentralbild): califica a Franco de «general reaccionario». Vocabulario de parte.",
     "autor": "Fotógrafo desconocido", "fecha": "enero de 1939",
     "custodio": "Bundesarchiv, Bild 183-E20569-21",
     "licencia": "CC BY-SA 3.0 DE", "licencia_url": "https://creativecommons.org/licenses/by-sa/3.0/de/deed.es",
     "verificacion": "Donación del Bundesarchiv a Commons (proyecto de cooperación) con su signatura."},
    {"id": "img-guernica-ruinas", "pareja": "efectos", "bando": "poblacion_civil",
     "fichero": "File:Bundesarchiv Bild 183-H25224, Guernica, Ruinen.jpg",
     "titulo": "Ruinas de Guernica",
     "pie": "Edificios destruidos en Guernica en 1937. El título del archivo atribuye la destrucción al ataque aéreo de la Legión Cóndor.",
     "pie_original": "Título del archivo: «Ruinas de edificios destruidos tras el ataque aéreo alemán de la Legión Cóndor».",
     "autor": "Fotógrafo desconocido", "fecha": "1937",
     "custodio": "Bundesarchiv, Bild 183-H25224",
     "licencia": "CC BY-SA 3.0 DE", "licencia_url": "https://creativecommons.org/licenses/by-sa/3.0/de/deed.es",
     "verificacion": "Donación del Bundesarchiv a Commons (proyecto de cooperación) con su signatura."},
]


def main() -> None:
    import subprocess
    com = [i for i in IMAGENES if "fichero" in i]
    for img in [i for i in IMAGENES if "bvm" in i]:
        dst = DEST / f"{img['id']}.jpg"
        if not dst.exists():
            tmp = DEST / f"{img['id']}.orig"
            with urllib.request.urlopen(urllib.request.Request(f"{BVM}/i18n/catalogo_imagenes/imagen_id.do?idImagen={img['bvm']['imagen']}", headers=UA), timeout=90) as r:
                tmp.write_bytes(r.read())
            subprocess.run(["sips", "-s", "format", "jpeg", "-Z", "1200", str(tmp), "--out", str(dst)], check=True, capture_output=True)
            tmp.unlink()
            time.sleep(2)
        img["ficha_url"] = f"{BVM}/es/consulta/registro.do?id={img['bvm']['registro']}"
        img["src"] = f"img/archivo/{img['id']}.jpg"
        img["consultado"] = "2026-11-15"
    q = urllib.parse.urlencode({"action": "query", "titles": "|".join(i["fichero"] for i in com), "prop": "imageinfo",
                                "iiprop": "url|size", "iiurlwidth": "1000", "format": "json"})
    with urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers=UA), timeout=90) as r:
        pages = {p["title"]: p["imageinfo"][0] for p in json.load(r)["query"]["pages"].values()}
    norm = lambda t: t.replace("_", " ")
    for img in com:
        ii = pages[norm(img["fichero"])]
        dst = DEST / f"{img['id']}.jpg"
        if not dst.exists():
            with urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=90) as r:
                dst.write_bytes(r.read())
            time.sleep(2)
        img.update({"ficha_url": ii["descriptionurl"], "src": f"img/archivo/{img['id']}.jpg", "consultado": "2026-11-15"})
    for img in IMAGENES:
        dst = DEST / f"{img['id']}.jpg"
        dims = lambda: (lambda o: (int(o[o.index("pixelWidth:") + 1]), int(o[o.index("pixelHeight:") + 1])))(
            subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(dst)], capture_output=True, text=True).stdout.split())
        if max(dims()) > 1200:  # solo reducir, nunca ampliar
            subprocess.run(["sips", "-Z", "1200", str(dst)], check=True, capture_output=True)
        img["ancho"], img["alto"] = dims()
    OUT.write_text(json.dumps(IMAGENES, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(IMAGENES)} imágenes")


if __name__ == "__main__":
    main()
