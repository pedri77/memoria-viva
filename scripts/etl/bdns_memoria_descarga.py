"""Descarga de la BDNS (Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas) de las
convocatorias y concesiones relacionadas con la memoria democrática.

Fuente: API del portal https://www.infosubvenciones.es/bdnstrans/ (la misma que usa el portal
público; el portal declara ofrecer «una API para la consulta de los datos»). Reutilización según el
aviso legal del SNPSAP (Ley 37/2007): «Origen de los datos: Intervención General de la Administración
del Estado». El sitio no publica robots.txt.

Privacidad (aviso legal del SNPSAP y guía editorial §3):
  - No se guardan los títulos de las convocatorias (algunos llevan el nombre de una persona); solo una
    categoría calculada a partir de ellos.
  - De las concesiones a personas físicas (beneficiario con DNI enmascarado «***…») solo se guarda el
    número y el importe total por convocatoria y año; ni nombres ni importes individuales.

Salidas (data/external/bdns/): convocatorias_memoria.csv, concesiones_entidades.csv,
concesiones_personas_agregadas.csv.

Uso: python3 -I scripts/etl/bdns_memoria_descarga.py   (≈ 15 minutos: una petición por segundo)
"""
import collections
import csv
import json
import pathlib
import re
import time
import unicodedata
import urllib.parse
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/external/bdns"
API = "https://www.infosubvenciones.es/bdnstrans/api/"
UA = {"User-Agent": "memoria-viva/0.1 (proyecto de investigación sin ánimo de lucro)"}
TERMINOS = ["memoria democrática", "memoria histórica", "exhumación", "fosas", "simbología franquista",
            "guerra civil", "franquismo", "víctimas de la guerra civil"]
CATEGORIAS = [
    ("indemnizaciones", r"indemniz|ex ?presos|pensi"),
    ("fosas", r"fosa|exhum|adn|genetic|identificaci|restos"),
    ("simbolos", r"simbolog|vestigi|retirada|callejero"),
    ("lugares", r"refugi|interpretaci|museo|bunker|trinchera|patrimoni|senaliz|lugar(es)? de (la )?memoria|monument|panteon|polvorin|aerodrom|espai|espacio"),
    ("investigacion", r"investig|archiv|beca|estudi|digitaliz|document|catalog|publicaci|tesis|premio|libro"),
    ("divulgacion", r"jornada|curso|cine|exposici|acto|homenaje|difusi|divulg|sensibiliz|educa|congres|semana|festival|teatro|concierto"),
    ("general", r"."),
]
PERSONA = re.compile(r"^\*{3}")
NIF = re.compile(r"^([A-Z]{1,2}\d{2}\d{3}\d{2}[A-Z0-9]|[A-Z]{2}\d+|\d+)\s+(.*)$")
norm = lambda s: unicodedata.normalize("NFKD", (s or "").lower()).encode("ascii", "ignore").decode()


def get(ruta: str) -> dict:
    with urllib.request.urlopen(urllib.request.Request(API + ruta, headers=UA), timeout=60) as r:
        d = json.load(r)
    time.sleep(1)
    return d


def paginas(ruta: str):
    p = 0
    while True:
        d = get(f"{ruta}&pageSize=100&page={p}")
        yield from d["content"]
        if d["last"]:
            return
        p += 1


def categoria(c: dict) -> str:
    t = norm(c["descripcion"]) + " " + norm(c.get("descripcionLeng"))
    return next(k for k, rx in CATEGORIAS if re.search(rx, t))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    conv: dict = {}
    for t in TERMINOS:
        for c in paginas("convocatorias/busqueda?vpd=GE&descripcion=" + urllib.parse.quote(t)):
            conv.setdefault(c["numeroConvocatoria"], {**c, "termino": t})
    with (OUT / "convocatorias_memoria.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["numero_convocatoria", "fecha_recepcion", "nivel1", "nivel2", "nivel3", "categoria", "termino_busqueda"])
        for k, c in sorted(conv.items()):
            w.writerow([k, c["fechaRecepcion"], c["nivel1"], c["nivel2"], c["nivel3"] or "", categoria(c), c["termino"]])
    personas = collections.defaultdict(lambda: [0, 0.0])
    with (OUT / "concesiones_entidades.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["numero_convocatoria", "cod_concesion", "fecha_concesion", "nif", "entidad", "importe", "instrumento"])
        for k in sorted(conv):
            for x in paginas(f"concesiones/busqueda?vpd=GE&numeroConvocatoria={k}"):
                b = (x.get("beneficiario") or "").strip()
                if PERSONA.match(b):
                    a = personas[(k, (x.get("fechaConcesion") or "")[:4])]
                    a[0] += 1
                    a[1] += x.get("importe") or 0
                    continue
                m = NIF.match(b)
                assert m, f"beneficiario sin NIF reconocible en la convocatoria {k}"
                w.writerow([k, x["codConcesion"], x["fechaConcesion"], m.group(1), re.sub(r"\s+", " ", m.group(2)).strip(), x["importe"], (x.get("instrumento") or "").strip()])
    with (OUT / "concesiones_personas_agregadas.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["numero_convocatoria", "anio", "concesiones", "importe_total"])
        for (k, y), (n, i) in sorted(personas.items()):
            w.writerow([k, y, n, round(i, 2)])
    print(f"{len(conv)} convocatorias")


if __name__ == "__main__":
    main()
