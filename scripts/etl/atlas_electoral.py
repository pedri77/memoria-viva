"""F4 · Capa electoral 1931-1936 desde el Atlas Electoral de la Segunda República (F032).

Fuente: Rodon, Vall-Prat y Martín Álvarez, «Electoral Atlas of the Spanish Second Republic
(1931-1936)», v2.1, CORA/Dataverse, https://doi.org/10.34810/DATA3274 · CC BY-NC-SA 4.0.
Descargado por la API oficial de Dataverse (data/external/atlas_electoral/).

Geometrías: mapSpainHist (circ_hist_AAAA y municipios de 1930), CC BY 4.0.
Las capas derivadas heredan la licencia CC BY-NC-SA 4.0 del Atlas.

Salidas:
  site/public/data/v1/circunscripciones_{1931,1933,1936}.geojson
  site/public/data/v1/elecciones_municipios.json   {cod_ine: {año: [bloque, participación]}}
  site/public/data/v1/elecciones_bloques.json      etiquetas y descripción de bloques
  data/canonical/documents/doc-atlas-electoral.json

Uso: python3 -I scripts/etl/atlas_electoral.py   (necesita mapshaper vía npx)
"""
import csv
import json
import pathlib
import re
import subprocess
import tempfile
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "data/external/atlas_electoral"
TOPO = ROOT / "data/external/mapspainhist/mapSpainHist_geometries_v1.0.0.topojson"
OUT = ROOT / "site/public/data/v1"
DOC = ROOT / "data/canonical/documents/doc-atlas-electoral.json"
TODAY = "2026-11-14"
YEARS = ("1931", "1933", "1936")
CANARIAS = ("35", "38")
SHIFT = (6, 7)  # igual que scripts/etl/capas_mapa.sh

# Bloques del Atlas (codebook, tabla 4) con etiqueta en castellano fiel a su definición.
BLOQUES = {
    "broad_republican_socialist_coalition": ("Conjunción republicano-socialista", "Coalición de republicanos de izquierda y de centro-derecha con el PSOE (1931)."),
    "left_wing_republican_socialist_coalition": ("Coalición de republicanos de izquierda y socialistas", "Alianza de republicanos de izquierda y PSOE (1931, 1933)."),
    "republican_socialist_coalition": ("Coalición republicano-socialista", "Coalición de republicanos y socialistas recogida a escala municipal (1933)."),
    "center_right_republican_platforms": ("Republicanos de centro y centro-derecha", "Candidaturas republicanas de centro y centro-derecha, solas o aliadas (1931, 1933)."),
    "left_wing_republican_platforms": ("Republicanos de izquierda", "Republicanos de izquierda sin socialistas ni centro-derecha (1931, 1933)."),
    "socialist_platforms": ("Socialistas", "Candidaturas del PSOE en solitario (1931, 1933)."),
    "communist_and_other_lw_platforms": ("Comunistas y otra izquierda obrera", "PCE y otros pequeños partidos obreros de izquierda (1931, 1933)."),
    "left_wing_regionalist_platforms": ("Regionalistas o nacionalistas de izquierda", "Cataluña, País Vasco y Galicia (1931, 1933)."),
    "right_wing_regionalist_platforms": ("Regionalistas o nacionalistas de derecha", "Cataluña, País Vasco y Navarra (1931, 1933)."),
    "right_wing_platforms": ("Derechas", "Coaliciones y candidaturas de derecha (1931, 1933)."),
    "left_coalition": ("Coalición de izquierdas (Frente Popular)", "Coalición de partidos de izquierda en 1936."),
    "right_coalition": ("Coalición de derechas", "Coalición de partidos de derecha en 1936."),
    "centrist_platforms": ("Centro", "Republicanos de centro fuera de las dos grandes coaliciones (1936)."),
    "basque_nat_coal": ("Nacionalistas vascos (PNV)", "Candidaturas encabezadas por el PNV (1936)."),
    "other": ("Otras", "Pequeñas candidaturas e independientes."),
    "blank_and_null": ("Blancos y nulos", "Votos en blanco y nulos."),
}
ALIAS = {"alava": "araba", "alicante": "alacant", "baleares": "balears", "castellon": "castello",
         "guipuzcoa": "gipuzkoa", "stacruzdetenerife": "santacruzdetenerife",
         "vizcayacapital": "bilbao", "vizcayaprovincia": "bizkaia"}


def norm(s: str) -> str:
    s = re.sub(r"[^a-z]", "", unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower())
    return ALIAS.get(s, s)


def num(v):
    return None if v in ("", "NA", None) else round(float(v.replace(",", ".")), 1)


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    dist = list(csv.DictReader((SRC / "dataset_district_vote_shares_wide.csv").open(encoding="utf-8-sig"), delimiter=";"))
    seat_cols = [c for c in dist[0] if c.startswith("elected_candidates_")]
    resumen = {}
    for y in YEARS:
        with tempfile.TemporaryDirectory() as tmp:
            raw = pathlib.Path(tmp) / "c.geojson"
            subprocess.run(["npx", "--no-install", "mapshaper", "-i", str(TOPO), "-target", f"circ_hist_{y}",
                            "-proj", "wgs84", "-simplify", "5%", "keep-shapes",
                            "-o", str(raw), "format=geojson", "precision=0.0001"],
                           check=True, cwd=ROOT, capture_output=True)
            gj = json.loads(raw.read_text())
        rows = {norm(r["circuns"]): r for r in dist if r["year"] == y}
        sin = []
        for f in gj["features"]:
            p = f["properties"]
            r = rows.get(norm(p["nom"]))
            if not r:
                sin.append(p["nom"])
                continue
            seats = {c.replace("elected_candidates_", ""): int(float(r[c].replace(",", "."))) for c in seat_cols if r[c] not in ("", "NA") and float(r[c].replace(",", ".")) > 0}
            f["properties"] = {"cod": p["cod_unit"], "nombre": p["nom"], "fp": r["first_platform"],
                               "part": num(r["turnout_real"]), "escanos": int(float(r["total_seats"].replace(",", "."))) if r["total_seats"] not in ("", "NA") else None,
                               "electos": seats, "fuente": r.get("data_source", "")}
            if seats:
                top = max(seats, key=seats.get)
                if f["properties"]["escanos"] and seats[top] > f["properties"]["escanos"] / 2 and top != r["first_platform"]:
                    f["properties"]["aviso"] = "mayoria_distinta"
            if p["cod_unit"][:2] in CANARIAS:
                shift_geom(f["geometry"])
        assert not sin, f"{y}: circunscripciones sin datos: {sin}"
        (OUT / f"circunscripciones_{y}.geojson").write_text(json.dumps(gj, ensure_ascii=False, separators=(",", ":")))
        fp = {}
        tot = {}
        for f in gj["features"]:
            fp[f["properties"]["fp"]] = fp.get(f["properties"]["fp"], 0) + 1
            for b, n in f["properties"]["electos"].items():
                tot[b] = tot.get(b, 0) + n
        resumen[y] = {"circunscripciones": len(gj["features"]), "mas_votado": fp, "electos_primera_vuelta": tot}

    muni = {}
    for r in csv.DictReader((SRC / "dataset_muni_vote_shares_wide.csv").open(encoding="utf-8-sig"), delimiter=";"):
        if r["elect_round"] != "1":
            continue
        muni.setdefault(r["cod_mun"], {})[r["year"]] = [None if r["first_platform"] in ("NA", "") else r["first_platform"], num(r["turnout_real"])]
    (OUT / "elecciones_municipios.json").write_text(json.dumps(muni, separators=(",", ":")))
    # GeoJSON municipal con los datos incrustados (MapLibre lo analiza en su worker)
    mg = json.loads((OUT / "municipios_1930.geojson").read_text())
    for f in mg["features"]:
        r = muni.get(f["properties"]["cod_ine"], {})
        for y in ("1933", "1936"):
            fp_, part = r.get(y, [None, None])
            f["properties"][f"e{y}"] = fp_
            f["properties"][f"p{y}"] = part
        f["properties"].pop("phec1930", None)
    (OUT / "municipios_1930_elecciones.geojson").write_text(json.dumps(mg, ensure_ascii=False, separators=(",", ":")))
    def quint(vals):
        v = sorted(x for x in vals if x is not None)
        return [v[int(q * (len(v) - 1))] for q in (0.2, 0.4, 0.6, 0.8)]
    res_web = {}
    for y in YEARS:
        res_web[y] = {"circ_bloques": sorted(resumen[y]["mas_votado"])}
        if y != "1931":
            res_web[y]["muni_bloques"] = sorted({v[y][0] for v in muni.values() if y in v and v[y][0]})
            res_web[y]["muni_part_cortes"] = quint([v[y][1] for v in muni.values() if y in v])
    (OUT / "elecciones_resumen.json").write_text(json.dumps(res_web, ensure_ascii=False))
    (OUT / "elecciones_bloques.json").write_text(json.dumps({k: {"label": v[0], "desc": v[1]} for k, v in BLOQUES.items()}, ensure_ascii=False, indent=1))
    desconocidos = {b for y in resumen for b in resumen[y]["mas_votado"]} - set(BLOQUES)
    assert not desconocidos, f"bloques sin etiqueta: {desconocidos}"

    DOC.write_text(json.dumps({
        "id": "doc-atlas-electoral",
        "title": "Atlas Electoral de la Segunda República (1931-1936), v2.1",
        "document_type": "tabla_estadistica",
        "source_ids": ["F032"],
        "custodian": "Universitat Pompeu Fabra · CORA, Repositori de Dades de Recerca (Dataverse)",
        "signature": "doi:10.34810/DATA3274",
        "canonical_url": "https://doi.org/10.34810/DATA3274",
        "date": "2026-10-13", "date_precision": "dia",
        "summary": "Resultados de las elecciones generales de 1931, 1933 y 1936 (primera vuelta): por circunscripción para las tres y por municipio para 1933 y 1936. Agrupa las candidaturas en bloques políticos sintéticos definidos por los autores.",
        "context": "Base de datos académica de Toni Rodon, Pau Vall-Prat y Diego Martín Álvarez, compilada a partir de fuentes primarias y secundarias detalladas en su libro de códigos. Los bloques son una clasificación de los autores y sus porcentajes por bloque tienen sesgos que el propio libro de códigos advierte; por eso el atlas solo muestra el bloque más votado, la participación y los escaños de primera vuelta. El Readme del depósito fecha las elecciones de 1931 en abril; los datos usan la fecha correcta, 28 de junio de 1931.",
        "text_origin": "transcripcion_validada",
        "rights": {"status": "cc_by_nc_sa", "action": "almacenar",
                   "attribution": "Rodon, T., Vall-Prat, P. y Martín Álvarez, D. Electoral Atlas of the Spanish Second Republic (1931-1936), CORA, doi:10.34810/DATA3274 (CC BY-NC-SA 4.0)",
                   "evidence_url": "https://api.datacite.org/dois/10.34810/data3274", "checked_at": TODAY,
                   "note": "Licencia no comercial y compartir igual: las capas derivadas del atlas heredan CC BY-NC-SA 4.0."},
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Generado por scripts/etl/atlas_electoral.py. Fechas contrastadas con la Gaceta (1931 y 1933)."},
        "consulted_at": TODAY,
    }, ensure_ascii=False, indent=2) + "\n")
    (SRC / "resumen_derivado.json").write_text(json.dumps(resumen, ensure_ascii=False, indent=1))
    print(json.dumps(resumen, ensure_ascii=False, indent=1))
    print("municipios con datos:", len(muni))


def shift_geom(g):
    def sh(c):
        return [[shift_ring(r) for r in poly] for poly in c] if g["type"] == "MultiPolygon" else [shift_ring(r) for r in c]
    g["coordinates"] = sh(g["coordinates"])


def shift_ring(r):
    return [[round(x + SHIFT[0], 4), round(y + SHIFT[1], 4)] for x, y in r]


if __name__ == "__main__":
    main()
