"""Reforma agraria en el Anuario Estadístico de España de 1934 (INE, INEbase Historia), sección «Reforma agraria».

Entradas, transcritas a mano (data/external/ine_anuario1934/):
  riqueza_por_categoria_propietarios.csv   tabla IV (td=102040): propietarios y líquido imponible por categoría
  grandeza_extension_expropiable.csv       tabla V  (td=102041): extensión expropiable de la extinguida Grandeza
  grandeza_fincas_expropiadas.csv          tabla VI (td=102042): fincas de la Grandeza expropiadas y obreros asentados

Comprobaciones (fallan con AssertionError):
  IV: en cada provincia, los porcentajes impresos coinciden (±0,02) con los recalculados desde las cifras absolutas.
  V:  la suma de hectáreas, áreas y centiáreas (con sus acarreos) reproduce el total impreso.
  VI: las tres columnas suman el total impreso.

Las tablas solo recogen las provincias que estudió el Anuario (zona de latifundio y algunas más); el resto queda
sin dato con su motivo.

Salidas: data/canonical/documents/doc-ine-anuario1934-reforma-agraria.json e indicadores ind-ra-*-prov.
Uso: python3 -I scripts/etl/ine_reforma_agraria_1934.py
"""
import collections
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
SRC = ROOT / "data/external/ine_anuario1934"
TODAY = "2026-11-15"
DID = "doc-ine-anuario1934-reforma-agraria"
PER = "1934"
FUERA = "La tabla del Anuario de 1934 no incluye esta provincia: solo recoge las provincias de la zona estudiada por la Reforma agraria."


def leer(nombre):
    return list(csv.DictReader((SRC / nombre).open(encoding="utf-8")))


def main() -> None:
    iv = leer("riqueza_por_categoria_propietarios.csv")
    by = collections.defaultdict(list)
    for r in iv:
        by[r["cod_prov"]].append(r)
    for c, rs in by.items():
        tp = sum(int(r["propietarios"]) for r in rs); tl = sum(int(r["liquido_imponible"]) for r in rs)
        for r in rs:
            assert abs(100 * int(r["propietarios"]) / tp - float(r["pct_propietarios"])) <= 0.02, f"IV {c} {r['categoria']}: % propietarios"
            assert abs(100 * int(r["liquido_imponible"]) / tl - float(r["pct_liquido"])) <= 0.02, f"IV {c} {r['categoria']}: % líquido"
    v = leer("grandeza_extension_expropiable.csv")
    ca = sum(int(r["hectareas"]) * 10000 + int(r["areas"]) * 100 + int(r["centiareas"]) for r in v if r["cod_prov"] != "TOTAL")
    t = next(r for r in v if r["cod_prov"] == "TOTAL")
    assert ca == int(t["hectareas"]) * 10000 + int(t["areas"]) * 100 + int(t["centiareas"]), "V: la suma no reproduce el total"
    vi = leer("grandeza_fincas_expropiadas.csv")
    tvi = next(r for r in vi if r["cod_prov"] == "TOTAL")
    for k in ("fincas", "superficie_ha", "obreros_asentados"):
        assert sum(int(r[k]) for r in vi if r["cod_prov"] != "TOTAL") == int(tvi[k]), f"VI: suma de {k}"

    (OUT / f"documents/{DID}.json").write_text(json.dumps({
        "id": DID,
        "title": "Anuario Estadístico de España 1934: reforma agraria (propiedad catastrada por categoría de propietarios y fincas de la extinguida Grandeza de España)",
        "title_original": "Reforma agraria. IV. Distribución, por la categoría de los propietarios, de la riqueza catastrada en cada provincia; V. Extensión expropiable perteneciente a la extinguida Grandeza de España, por provincias; VI. Fincas de la extinguida Grandeza de España que han sido expropiadas para los fines de la Reforma agraria, por provincias",
        "document_type": "tabla_estadistica", "source_ids": ["F010"],
        "custodian": "Instituto Nacional de Estadística, INEbase Historia (fondo documental)",
        "signature": "Anuario Estadístico de España 1934, Agricultura, «Reforma agraria», págs. 213-214 (tablas IV td=102040, V td=102041, VI td=102042)",
        "canonical_url": "https://www.ine.es/inebaseweb/treeNavigation.do?tn=102811",
        "date": "1934-12-31", "date_precision": "anio", "place_ids": ["plc-espana"],
        "summary": "Tablas oficiales sobre la propiedad rústica y la Reforma agraria en las provincias de latifundio: número de propietarios y riqueza catastrada (líquido imponible) de los pequeños, medianos y grandes propietarios; extensión expropiable de la extinguida Grandeza de España, y fincas de la Grandeza expropiadas, con su superficie y los obreros asentados.",
        "context": "Cifras oficiales publicadas en el Anuario de 1934 a partir de datos del catastro y del Instituto de Reforma Agraria; el Anuario no indica la fecha de referencia de cada tabla. Las fincas expropiadas son solo las de la extinguida Grandeza (base 20 de la ley de 1932), no el conjunto de la reforma. Según la nota de la tabla V, los 99 miembros de la extinguida Grandeza declararon 577 359 hectáreas en todo el territorio.",
        "text_origin": "transcripcion_validada",
        "rights": {"status": "cc_by", "action": "almacenar",
                   "attribution": "Fuente: Instituto Nacional de Estadística (INE), INEbase Historia, Anuario Estadístico de España 1934",
                   "evidence_url": "https://www.ine.es/ine/codigobp/politica_difusion_es.pdf", "checked_at": TODAY,
                   "note": "El INE aplica a la información de su web la licencia CC BY 4.0 salvo indicación contraria (Política de Difusión Estadística, febrero de 2026)."},
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Transcritas a mano; los 48 porcentajes de la tabla IV coinciden con los recalculados desde las cifras absolutas, y las tablas V y VI suman sus totales impresos."},
        "consulted_at": TODAY}, ensure_ascii=False, indent=2) + "\n")

    provs = sorted(p.stem[-2:] for p in (OUT / "places").glob("plc-prov-*.json"))
    rev = {"status": "revision", "date": TODAY, "by": ["autor"], "note": "Generado por scripts/etl/ine_reforma_agraria_1934.py."}

    def indicador(iid, concepto, definicion, unidad, metodo, notas, valores, loc, uncert=None):
        obs = []
        for c in provs:
            if c in valores:
                o = {"place_id": f"plc-prov-{c}", "period": PER, "value": valores[c], "document_id": DID, "locator": loc}
                if uncert and uncert.get(c):
                    o["uncertainty"] = uncert[c]
            else:
                o = {"place_id": f"plc-prov-{c}", "period": PER, "value": None, "document_id": DID, "missingness_reason": FUERA}
            obs.append(o)
        (OUT / f"indicators/{iid}.json").write_text(json.dumps({
            "id": iid, "concept": concepto, "definition": definicion, "unit": unidad, "denominator": "ver definición", "method": metodo,
            "source_ids": ["F010"], "comparability_notes": notas, "review": rev, "observations": obs}, ensure_ascii=False, indent=2) + "\n")

    grandes = {r["cod_prov"]: float(r["pct_liquido"]) for r in iv if r["categoria"] == "grandes"}
    indicador("ind-ra-riqueza-grandes-prov", "Riqueza rústica en manos de los grandes propietarios (Anuario de 1934)",
              "Porcentaje del líquido imponible catastrado de la provincia que corresponde a los grandes propietarios (cuotas de más de 5.000 pesetas).",
              "% del líquido imponible", "Porcentaje impreso en la tabla IV, comprobado contra las cifras absolutas.",
              "Solo 8 provincias. Mide riqueza imponible según el catastro, no superficie. El Anuario no indica la fecha de referencia del catastro.",
              grandes, "tabla IV, «Grandes propietarios», tanto por ciento del líquido imponible")
    vi_p = {r["cod_prov"]: r for r in vi if r["cod_prov"] != "TOTAL"}
    nota_vi = {c: r["nota"] for c, r in vi_p.items() if r["nota"]}
    aviso_vi = "Solo las fincas de la extinguida Grandeza de España expropiadas hasta la fecha del Anuario, no el conjunto de la reforma; el Anuario no indica la fecha de corte."
    indicador("ind-ra-asentados-prov", "Obreros asentados en fincas expropiadas a la Grandeza (Anuario de 1934)",
              "Número de obreros asentados en las fincas de la extinguida Grandeza de España expropiadas para los fines de la Reforma agraria.",
              "obreros asentados", "Cifra impresa en la tabla VI.", aviso_vi,
              {c: int(r["obreros_asentados"]) for c, r in vi_p.items()}, "tabla VI, «Número de obreros asentados»")
    indicador("ind-ra-superficie-expropiada-prov", "Superficie expropiada a la Grandeza (Anuario de 1934)",
              "Hectáreas de las fincas de la extinguida Grandeza de España expropiadas para los fines de la Reforma agraria.",
              "hectáreas", "Cifra impresa en la tabla VI.", aviso_vi,
              {c: int(r["superficie_ha"]) for c, r in vi_p.items()}, "tabla VI, «Superficie, en hectáreas»", nota_vi)
    indicador("ind-ra-expropiable-grandeza-prov", "Superficie expropiable de la Grandeza (Anuario de 1934)",
              "Hectáreas de las fincas de la extinguida Grandeza de España declaradas expropiables en la provincia.",
              "hectáreas", "Cifra impresa en la tabla V (hectáreas enteras; las áreas y centiáreas se omiten).",
              "Solo 8 provincias. En todo el territorio, los 99 miembros de la extinguida Grandeza declararon 577.359 hectáreas (nota de la tabla V).",
              {r["cod_prov"]: int(r["hectareas"]) for r in v if r["cod_prov"] != "TOTAL"}, "tabla V, «Hectáreas»")
    print(f"IV {len(by)} provincias, V {len(v) - 1}, VI {len(vi_p)}; asentados {tvi['obreros_asentados']}, expropiadas {tvi['superficie_ha']} ha")


if __name__ == "__main__":
    main()
