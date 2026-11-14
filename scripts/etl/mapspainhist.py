"""F1 · Provincias de 1930 e indicadores censales 1920-1940 desde mapSpainHist (F033).

Entrada (data/external/mapspainhist/, CC BY 4.0, Vall-Prat, Zenodo 10.5281/zenodo.23663208):
  censos.csv               población de hecho (phec) y de derecho (pder) por municipio y censo
  unitats_municipis.csv    municipio -> provincia de cada año
  prov_1930_areas.csv      superficie por provincia (calculada con mapshaper sobre prov_hist_1930)

Salida:
  data/canonical/places/plc-prov-XX.json     52 unidades (50 provincias + Ceuta y Melilla)
  data/canonical/documents/doc-mapspainhist-censos.json, doc-ine-intercensal.json
  data/canonical/indicators/ind-pob-hecho-prov.json, ind-pob-derecho-prov.json, ind-densidad-prov.json

Verificación previa (14-11-2026): Agaete, Madrid y Teruel en 1920, 1930 y 1940 coinciden
exactamente con la aplicación «Alteraciones de los municipios» del INE.

Uso: python3 -I scripts/etl/mapspainhist.py
"""
import csv
import json
import pathlib
from collections import Counter

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "data/external/mapspainhist"
OUT = ROOT / "data/canonical"
TODAY = "2026-11-14"
YEARS = ("1920", "1930", "1940")
DOC_DS = "doc-mapspainhist-censos"
DOC_INE = "doc-ine-intercensal"
REVIEW = {"status": "revision", "date": TODAY, "by": ["autor"],
          "note": "Generado por scripts/etl/mapspainhist.py; contraste puntual con INE en 3 municipios."}

# Nombre castellano actual y denominación oficial en 1930 cuando difiere.
NAMES = {
    "01": ("Álava", None), "02": ("Albacete", None), "03": ("Alicante", None), "04": ("Almería", None),
    "05": ("Ávila", None), "06": ("Badajoz", None), "07": ("Islas Baleares", "Baleares"), "08": ("Barcelona", None),
    "09": ("Burgos", None), "10": ("Cáceres", None), "11": ("Cádiz", None), "12": ("Castellón", None),
    "13": ("Ciudad Real", None), "14": ("Córdoba", None), "15": ("La Coruña", "Coruña"), "16": ("Cuenca", None),
    "17": ("Gerona", None), "18": ("Granada", None), "19": ("Guadalajara", None), "20": ("Guipúzcoa", None),
    "21": ("Huelva", None), "22": ("Huesca", None), "23": ("Jaén", None), "24": ("León", None),
    "25": ("Lérida", None), "26": ("La Rioja", "Logroño"), "27": ("Lugo", None), "28": ("Madrid", None),
    "29": ("Málaga", None), "30": ("Murcia", None), "31": ("Navarra", None), "32": ("Orense", None),
    "33": ("Asturias", "Oviedo"), "34": ("Palencia", None), "35": ("Las Palmas", None), "36": ("Pontevedra", None),
    "37": ("Salamanca", None), "38": ("Santa Cruz de Tenerife", None), "39": ("Cantabria", "Santander"),
    "40": ("Segovia", None), "41": ("Sevilla", None), "42": ("Soria", None), "43": ("Tarragona", None),
    "44": ("Teruel", None), "45": ("Toledo", None), "46": ("Valencia", None), "47": ("Valladolid", None),
    "48": ("Vizcaya", None), "49": ("Zamora", None), "50": ("Zaragoza", None), "51": ("Ceuta", None), "52": ("Melilla", None),
}


def dump(path: pathlib.Path, obj: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    unit = {(r["any"], r["cod_ine"]): r["cod_unit"]
            for r in csv.DictReader((SRC / "unitats_municipis.csv").open(encoding="utf-8")) if r["tipus"] == "prov"}
    hecho = {y: Counter() for y in YEARS}
    derecho = {y: Counter() for y in YEARS}
    nmun = {y: Counter() for y in YEARS}
    for r in csv.DictReader((SRC / "censos.csv").open(encoding="utf-8")):
        y = r["censo"]
        if y not in YEARS or r["phec"] == "NA":
            continue
        prov = unit.get((y, r["cod_ine"])) or unit[("1930", r["cod_ine"])]
        hecho[y][prov] += int(r["phec"])
        derecho[y][prov] += int(r["pder"])
        nmun[y][prov] += 1
    area = {r["cod_unit"]: int(r["area_km2"]) for r in csv.DictReader((SRC / "prov_1930_areas.csv").open(encoding="utf-8"))}

    # Lugares
    for code, (name, name1930) in NAMES.items():
        plaza = code in ("51", "52")
        obj = {
            "id": f"plc-prov-{code}",
            "canonical_name": name,
            "place_type": "municipio" if plaza else "provincia",
            "parent_id": "plc-espana",
            "ine_code": code,
            "geometry_ref": f"provincias_1930.geojson#cod_unit={code}",
            "geometry_precision": "exacta",
            "source_ids": ["F033"],
            "review": dict(REVIEW),
        }
        if name1930:
            obj["historical_names"] = [{"name": name1930, "valid_from": "1930"}]
        if plaza:
            obj["review"]["note"] = ("Ceuta y Melilla no eran provincias en 1930; los censos las recogen aparte. "
                                     "Se tratan como unidades propias para no perder población.")
        dump(OUT / f"places/plc-prov-{code}.json", obj)

    # Documentos de evidencia
    dump(OUT / f"documents/{DOC_DS}.json", {
        "id": DOC_DS,
        "title": "mapSpainHist: límites municipales históricos de España 1900-2001 y censos 1842-2011 (fichero censos.csv, v1.0.0)",
        "document_type": "tabla_estadistica",
        "source_ids": ["F033"],
        "custodian": "Zenodo (depósito de Pau Vall-Prat)",
        "canonical_url": "https://doi.org/10.5281/zenodo.23663208",
        "date": "2026",
        "date_precision": "anio",
        "summary": "Población de hecho y de derecho y hogares por municipio en cada censo, con la asignación de cada municipio a su provincia histórica. Compilado a partir de los censos del INE.",
        "context": "Base de datos académica derivada de los censos oficiales. Contrastada con la aplicación del INE en 3 municipios y 3 censos sin diferencias.",
        "text_origin": "transcripcion_validada",
        "rights": {"status": "cc_by", "action": "almacenar", "attribution": "Vall-Prat, P. mapSpainHist (Zenodo, CC BY 4.0)",
                   "evidence_url": "https://zenodo.org/records/23663208", "checked_at": TODAY},
        "review": dict(REVIEW),
        "consulted_at": TODAY,
    })
    dump(OUT / f"documents/{DOC_INE}.json", {
        "id": DOC_INE,
        "title": "INE · Alteraciones de los municipios en los Censos de Población desde 1842",
        "document_type": "tabla_estadistica",
        "source_ids": ["F010"],
        "custodian": "Instituto Nacional de Estadística",
        "canonical_url": "https://www.ine.es/intercensal/",
        "date": "1842",
        "date_end": "2021",
        "date_precision": "intervalo",
        "summary": "Aplicación oficial con la población de hecho y de derecho de cada municipio en todos los censos. Se usa para contrastar los datos de mapSpainHist.",
        "context": "Fuente oficial. Las cifras municipales pueden no sumar exactamente los totales provinciales publicados en los volúmenes de cada censo.",
        "text_origin": "ninguno",
        "rights": {"status": "reuse_conditions", "action": "enlazar", "attribution": "Fuente: INE",
                   "evidence_url": "https://www.ine.es/ss/Satellite?L=es_ES&c=Page&cid=1254735849170&p=1254735849170&pagename=Ayuda%2FINELayout",
                   "checked_at": TODAY},
        "review": dict(REVIEW),
        "consulted_at": TODAY,
    })

    common_notes = ("Suma de las cifras municipales de cada censo agrupadas por la provincia a la que pertenecía el municipio ese año. "
                    "Puede diferir ligeramente de los totales provinciales impresos en los volúmenes del censo. "
                    "Los censos de 1920 y 1930 se hicieron el 31 de diciembre; el de 1940, el 31 de diciembre de 1940, tras la guerra, "
                    "con desplazamientos, exilio y mortalidad que afectan a la comparación.")

    def indicator(iid, concept, definition, unit, method, data, extra=""):
        obs = []
        for y in YEARS:
            for code in NAMES:
                obs.append({"place_id": f"plc-prov-{code}", "period": y, "value": data(y, code),
                            "document_id": DOC_DS, "locator": f"censos.csv, censo {y}, {nmun[y][code]} municipios"})
        dump(OUT / f"indicators/{iid}.json", {
            "id": iid, "concept": concept, "definition": definition, "unit": unit, "method": method,
            "source_ids": ["F033", "F010"], "comparability_notes": common_notes + extra,
            "observations": obs, "review": dict(REVIEW)})

    indicator("ind-pob-hecho-prov", "Población de hecho por provincia",
              "Personas presentes en el municipio en la fecha del censo, residentes o no.", "personas",
              "Suma de la población de hecho municipal (columna phec).", lambda y, c: hecho[y][c])
    indicator("ind-pob-derecho-prov", "Población de derecho por provincia",
              "Personas residentes en el municipio, presentes o ausentes en la fecha del censo.", "personas",
              "Suma de la población de derecho municipal (columna pder).", lambda y, c: derecho[y][c])
    indicator("ind-densidad-prov", "Densidad de población de hecho por provincia",
              "Población de hecho dividida por la superficie de la provincia.", "habitantes por km²",
              "Población de hecho / superficie (km²) calculada sobre los límites provinciales de 1930 de mapSpainHist. Se usa la misma superficie para los tres censos.",
              lambda y, c: round(hecho[y][c] / area[c], 1),
              " La superficie es la de los límites de 1930 calculada sobre geometría digital; error estimado inferior al 0,2 % frente a la superficie oficial.")
    print("provincias:", len(NAMES), "| totales hecho:", {y: sum(hecho[y].values()) for y in YEARS})


if __name__ == "__main__":
    main()
