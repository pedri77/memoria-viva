"""Alfabetización por provincia en el censo de 1930 (INE, INEbase Historia).

Entrada: data/external/ine1930/instruccion_1930_provincias.csv, transcrita a mano de
«Habitantes inscritos en la Población de HECHO del Censo de 1930 clasificados según el sexo
en combinación con el estado civil y con la instrucción elemental, por provincias»
(Censo de 1930, Tomo II. Resúmenes generales de la nación, INEbase Historia, td=194363).

Comprobaciones de la transcripción (fallan con AssertionError):
  1. Por provincia y sexo, estado civil e instrucción suman cada uno el total de la fila.
  2. Varones + mujeres = total de la provincia.
  3. La suma de las 50 provincias y las posesiones de África coincide con los totales
     nacionales impresos, columna a columna.
  4. El total de cada provincia coincide con la población de hecho de 1930 ya publicada
     (ind-pob-hecho-prov, suma municipal de mapSpainHist).

Salidas: data/canonical/documents/doc-ine-censo1930-instruccion.json
         data/canonical/indicators/ind-alfab-{total,varones,mujeres}-prov.json

Uso: python3 -I scripts/etl/ine_alfabetizacion.py
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "data/external/ine1930/instruccion_1930_provincias.csv"
OUT = ROOT / "data/canonical"
TODAY = "2026-11-15"
DOC = "doc-ine-censo1930-instruccion"
COLS = ["total", "solteros", "casados", "viudos", "ec_no_consta", "saben_solo_leer", "saben_leer_y_escribir", "no_saben_leer", "instr_no_consta"]
IMPRESO = {
    "varones": [11565805, 6829771, 4272348, 445346, 18340, 73195, 7101076, 4270370, 121164],
    "mujeres": [12111989, 6639063, 4331013, 1123977, 17936, 136146, 6070609, 5754569, 150665],
}
TOTAL_PROV = {}  # se rellena desde la fila de varones + mujeres


def main() -> None:
    rows = list(csv.DictReader(SRC.open(encoding="utf-8")))
    data: dict = {}
    suma = {"varones": [0] * 9, "mujeres": [0] * 9}
    for r in rows:
        n = [int(r[c]) for c in COLS]
        t, so, ca, vi, nc, le, ly, ns, nc2 = n
        assert so + ca + vi + nc == t, f"{r['cod_prov']} {r['sexo']}: estado civil no suma"
        assert le + ly + ns + nc2 == t, f"{r['cod_prov']} {r['sexo']}: instrucción no suma"
        suma[r["sexo"]] = [a + b for a, b in zip(suma[r["sexo"]], n)]
        data.setdefault(r["cod_prov"], {})[r["sexo"]] = dict(zip(COLS, n), nota=r["nota"])
    for s in suma:
        assert suma[s] == IMPRESO[s], f"totales nacionales de {s} no coinciden: {suma[s]}"
    hecho = json.loads((OUT / "indicators/ind-pob-hecho-prov.json").read_text())
    pob1930 = {o["place_id"]: o["value"] for o in hecho["observations"] if o["period"] == "1930"}
    for cod, d in data.items():
        if cod == "AF":
            continue
        t = d["varones"]["total"] + d["mujeres"]["total"]
        assert pob1930.get(f"plc-prov-{cod}") == t, f"{cod}: total {t} distinto de ind-pob-hecho-prov"

    (OUT / f"documents/{DOC}.json").write_text(json.dumps({
        "id": DOC,
        "title": "Censo de 1930, Tomo II: población de hecho por sexo, estado civil e instrucción elemental, por provincias",
        "title_original": "Habitantes inscritos en la Población de HECHO del Censo de 1930 clasificados según el sexo en combinación con el estado civil y con la instrucción elemental, por provincias",
        "document_type": "tabla_estadistica",
        "source_ids": ["F010"],
        "custodian": "Instituto Nacional de Estadística, INEbase Historia (fondo documental)",
        "signature": "Censo de la población de España de 1930, Tomo II. Resúmenes generales de la nación, «Resumen por provincias», págs. 2-4 del PDF",
        "canonical_url": "https://www.ine.es/inebaseweb/pdfDispacher.do?td=194363&ext=.pdf",
        "date": "1930-12-31", "date_precision": "dia",
        "place_ids": ["plc-espana"],
        "summary": "Tabla oficial del censo de 1930 con la población de hecho de cada provincia, por sexo, clasificada por estado civil y por instrucción elemental: saben solo leer, saben leer y escribir, no saben leer y no consta.",
        "context": "Cifras oficiales de la Dirección General de Estadística. La instrucción se declaraba en la hoja censal, sin prueba de lectura, y se cuenta para todas las edades, incluidos los niños pequeños. La tabla impresa contiene al menos una errata (Sevilla, mujeres que saben leer y escribir), corregida en la transcripción con la regla documentada en el CSV.",
        "text_origin": "transcripcion_validada",
        "rights": {"status": "cc_by", "action": "almacenar",
                   "attribution": "Fuente: Instituto Nacional de Estadística (INE), INEbase Historia, Censo de 1930",
                   "evidence_url": "https://www.ine.es/ine/codigobp/politica_difusion_es.pdf",
                   "checked_at": TODAY,
                   "note": "El INE aplica a la información de su web la licencia CC BY 4.0 salvo indicación contraria (Política de Difusión Estadística, febrero de 2026)."},
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Transcrita a mano de la imagen del PDF; 102 filas cuadradas por estado civil e instrucción, totales nacionales impresos reproducidos columna a columna y totales provinciales iguales a la suma municipal de mapSpainHist."},
        "consulted_at": TODAY,
    }, ensure_ascii=False, indent=2) + "\n")

    def obs(sexos):
        out = []
        for cod in sorted(k for k in data if k != "AF"):
            t = sum(data[cod][s]["total"] for s in sexos)
            saben = sum(data[cod][s]["saben_solo_leer"] + data[cod][s]["saben_leer_y_escribir"] for s in sexos)
            o = {"place_id": f"plc-prov-{cod}", "period": "1930", "value": round(100 * saben / t, 1),
                 "document_id": DOC, "locator": f"fila de la provincia {cod}, columnas «saben leer» y «saben leer y escribir»"}
            if any(data[cod][s]["nota"] for s in sexos):
                o["uncertainty"] = "Errata corregida en la tabla impresa: " + " ".join(data[cod][s]["nota"] for s in sexos if data[cod][s]["nota"])
            out.append(o)
        for cod in ("51", "52"):
            out.append({"place_id": f"plc-prov-{cod}", "period": "1930", "value": None, "document_id": DOC,
                        "missingness_reason": "La tabla agrupa Ceuta, Melilla y el resto de posesiones del norte y costa occidental de África en una sola fila."})
        return out

    base = {
        "unit": "% de la población de hecho",
        "denominator": "población de hecho de todas las edades",
        "method": "(saben solo leer + saben leer y escribir) / total de la población de hecho, sobre la tabla oficial del censo de 1930 transcrita a mano con comprobación aritmética (scripts/etl/ine_alfabetizacion.py).",
        "source_ids": ["F010"],
        "comparability_notes": "El denominador incluye a toda la población, también a los menores que aún no estaban en edad de aprender a leer, así que la cifra es más baja que las tasas de alfabetización calculadas sobre mayores de 10 años que usa la historiografía. Es una declaración censal, no una prueba de lectura. No comparable directamente con las series de 1920 y 1940 del atlas, que son de población.",
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Generado por scripts/etl/ine_alfabetizacion.py desde la transcripción comprobada. Pendiente de segunda revisión humana."},
    }
    for sufijo, sexos, concepto in (("total", ("varones", "mujeres"), "Población que sabe leer, 1930"),
                                    ("varones", ("varones",), "Varones que saben leer, 1930"),
                                    ("mujeres", ("mujeres",), "Mujeres que saben leer, 1930")):
        iid = f"ind-alfab-{sufijo}-prov"
        (OUT / f"indicators/{iid}.json").write_text(json.dumps({
            "id": iid, "concept": concepto,
            "definition": f"Porcentaje de {'la población' if sufijo == 'total' else 'los varones' if sufijo == 'varones' else 'las mujeres'} de hecho de cada provincia que, según el censo de 1930, sabía leer (solo leer, o leer y escribir).",
            **base, "observations": obs(sexos)}, ensure_ascii=False, indent=2) + "\n")
    nac = {s: round(100 * (IMPRESO[s][5] + IMPRESO[s][6]) / IMPRESO[s][0], 1) for s in IMPRESO}
    print("ok: 3 indicadores; España (con África):", nac)


if __name__ == "__main__":
    main()
