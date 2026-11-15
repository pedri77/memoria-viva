"""Imágenes con derechos abiertos verificadas una a una (Wikimedia Commons, con custodio institucional).

Criterio (David, 15-11-2026): solo imágenes con derechos abiertos explícitos, verificadas una a una y en
equilibrio entre bandos (por parejas). Se descartan las de procedencia dudosa aunque Commons las marque como
dominio público: tomadas de agencias comerciales (Getty/Keystone), de prensa actual o de webs de aficionados.
No se incluyen imágenes de violencia: esperan a los revisores (R1).
Carteles: los dos de la BnF con derechos claros son republicanos («Aixafem el feixisme» y «Los Nacionales», que es
una sátira del Ministerio de Propaganda de la República contra la Junta de Burgos, no un cartel sublevado). No se ha
localizado ninguno del bando sublevado con procedencia verificable, así que no entra ninguno (laguna-imagenes-carteles).

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

IMAGENES = [
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
    q = urllib.parse.urlencode({"action": "query", "titles": "|".join(i["fichero"] for i in IMAGENES), "prop": "imageinfo",
                                "iiprop": "url|size", "iiurlwidth": "1000", "format": "json"})
    with urllib.request.urlopen(urllib.request.Request("https://commons.wikimedia.org/w/api.php?" + q, headers=UA), timeout=90) as r:
        pages = {p["title"]: p["imageinfo"][0] for p in json.load(r)["query"]["pages"].values()}
    norm = lambda t: t.replace("_", " ")
    for img in IMAGENES:
        ii = pages[norm(img["fichero"])]
        dst = DEST / f"{img['id']}.jpg"
        if not dst.exists():
            with urllib.request.urlopen(urllib.request.Request(ii["thumburl"], headers=UA), timeout=90) as r:
                dst.write_bytes(r.read())
            time.sleep(2)
        img.update({"commons_url": ii["descriptionurl"], "src": f"img/archivo/{img['id']}.jpg",
                    "ancho": ii["thumbwidth"], "alto": ii["thumbheight"], "consultado": "2026-11-15"})
    OUT.write_text(json.dumps(IMAGENES, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(IMAGENES)} imágenes")


if __name__ == "__main__":
    main()
