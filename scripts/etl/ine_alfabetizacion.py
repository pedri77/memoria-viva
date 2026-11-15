"""Alfabetización por provincia en los censos de 1920 y 1930 (INE, INEbase Historia).

Entradas, transcritas a mano de las tablas oficiales de población de HECHO por sexo, estado
civil e instrucción elemental, resumen por provincias:
  data/external/ine1920/instruccion_1920_provincias.csv  (Censo de 1920, Tomo II, td=86929)
  data/external/ine1930/instruccion_1930_provincias.csv  (Censo de 1930, Tomo II, td=194363)

Comprobaciones de cada transcripción (fallan con AssertionError):
  1. Por provincia y sexo, estado civil e instrucción suman cada uno el total de la fila.
  2. La suma de todas las filas reproduce columna a columna los totales nacionales impresos.
  3. El total de cada provincia coincide con la población de hecho de ese censo ya publicada
     (ind-pob-hecho-prov, suma municipal de mapSpainHist), salvo las diferencias explicadas
     en DIF_CONOCIDAS.

Salidas: data/canonical/documents/doc-ine-censo{1920,1930}-instruccion.json
         data/canonical/indicators/ind-alfab-{total,varones,mujeres}-prov.json

Uso: python3 -I scripts/etl/ine_alfabetizacion.py
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
TODAY = "2026-11-15"
COLS = ["total", "solteros", "casados", "viudos", "ec_no_consta", "saben_solo_leer", "saben_leer_y_escribir", "no_saben_leer", "instr_no_consta"]
CENSOS = {
    "1920": {
        "csv": ROOT / "data/external/ine1920/instruccion_1920_provincias.csv",
        "td": "86929", "fecha": "1920-12-31",
        "titulo": "Censo de 1920, Tomo II: población de hecho por sexo, estado civil e instrucción elemental, resumen general por provincias",
        "original": "Censo de la población de España de 1920. Tomo II. Clasificación de la población de hecho por sexo, estado civil e instrucción elemental. Resumen general por provincias",
        "firma": "Censo de la población de España de 1920, Tomo II, «Resumen general por provincias», págs. 449-451",
        "impreso": {"varones": [10373382, 6090810, 3801777, 453299, 27496, 75193, 5442129, 4802641, 53419],
                    "mujeres": [11016460, 6064395, 3920957, 1007737, 23371, 127164, 4462730, 6365165, 61401]},
        # diferencias con mapSpainHist explicadas: Cádiz incluye Ceuta; Gerona difiere en 60 habitantes sin explicar
        "dif": {"11": 35219, "17": 60},
        "nota_ctx": "En 1920 Canarias era una sola provincia y la provincia de Cádiz incluía Ceuta.",
    },
    "1930": {
        "csv": ROOT / "data/external/ine1930/instruccion_1930_provincias.csv",
        "td": "194363", "fecha": "1930-12-31",
        "titulo": "Censo de 1930, Tomo II: población de hecho por sexo, estado civil e instrucción elemental, por provincias",
        "original": "Habitantes inscritos en la Población de HECHO del Censo de 1930 clasificados según el sexo en combinación con el estado civil y con la instrucción elemental, por provincias",
        "firma": "Censo de la población de España de 1930, Tomo II. Resúmenes generales de la nación, «Resumen por provincias», págs. 2-4 del PDF",
        "impreso": {"varones": [11565805, 6829771, 4272348, 445346, 18340, 73195, 7101076, 4270370, 121164],
                    "mujeres": [12111989, 6639063, 4331013, 1123977, 17936, 136146, 6070609, 5754569, 150665]},
        "dif": {},
        "nota_ctx": "La tabla impresa contiene al menos una errata (Sevilla, mujeres que saben leer y escribir), corregida en la transcripción con la regla documentada en el CSV.",
    },
}
SINDATO = {
    "1920": {"plc-prov-51": "En 1920 el censo incluye Ceuta en la provincia de Cádiz.",
             "plc-prov-52": "La tabla agrupa Melilla con el resto de posesiones del norte y costa occidental de África."},
    "1930": {"plc-prov-51": "La tabla agrupa Ceuta, Melilla y el resto de posesiones del norte y costa occidental de África en una sola fila.",
             "plc-prov-52": "La tabla agrupa Ceuta, Melilla y el resto de posesiones del norte y costa occidental de África en una sola fila."},
}


def leer(year: str) -> dict:
    cfg = CENSOS[year]
    data: dict = {}
    suma = {"varones": [0] * 9, "mujeres": [0] * 9}
    for r in csv.DictReader(cfg["csv"].open(encoding="utf-8")):
        n = [int(r[c]) for c in COLS]
        t, so, ca, vi, nc, le, ly, ns, nc2 = n
        assert so + ca + vi + nc == t, f"{year} {r['cod_prov']} {r['sexo']}: estado civil no suma"
        assert le + ly + ns + nc2 == t, f"{year} {r['cod_prov']} {r['sexo']}: instrucción no suma"
        suma[r["sexo"]] = [a + b for a, b in zip(suma[r["sexo"]], n)]
        data.setdefault(r["cod_prov"], {})[r["sexo"]] = dict(zip(COLS, n), nota=r["nota"])
    for s in suma:
        assert suma[s] == cfg["impreso"][s], f"{year}: totales nacionales de {s} no coinciden: {suma[s]}"
    hecho = json.loads((OUT / "indicators/ind-pob-hecho-prov.json").read_text())
    pob = {o["place_id"]: o["value"] for o in hecho["observations"] if o["period"] == year}
    for cod, d in data.items():
        if cod == "AF":
            continue
        t = d["varones"]["total"] + d["mujeres"]["total"]
        ref = pob["plc-prov-35"] + pob["plc-prov-38"] if cod == "CAN" else pob.get(f"plc-prov-{cod}")
        assert t - ref == cfg["dif"].get(cod, 0), f"{year} {cod}: total {t} frente a {ref} en ind-pob-hecho-prov"
    return data


def documento(year: str) -> None:
    cfg = CENSOS[year]
    did = f"doc-ine-censo{year}-instruccion"
    (OUT / f"documents/{did}.json").write_text(json.dumps({
        "id": did, "title": cfg["titulo"], "title_original": cfg["original"],
        "document_type": "tabla_estadistica", "source_ids": ["F010"],
        "custodian": "Instituto Nacional de Estadística, INEbase Historia (fondo documental)",
        "signature": cfg["firma"],
        "canonical_url": f"https://www.ine.es/inebaseweb/pdfDispacher.do?td={cfg['td']}&ext=.pdf",
        "date": cfg["fecha"], "date_precision": "dia", "place_ids": ["plc-espana"],
        "summary": f"Tabla oficial del censo de {year} con la población de hecho de cada provincia, por sexo, clasificada por estado civil y por instrucción elemental: saben solo leer, saben leer y escribir, no saben leer y no consta.",
        "context": "Cifras oficiales de la Dirección General de Estadística. La instrucción se declaraba en la hoja censal, sin prueba de lectura, y se cuenta para todas las edades, incluidos los niños pequeños. " + cfg["nota_ctx"],
        "text_origin": "transcripcion_validada",
        "rights": {"status": "cc_by", "action": "almacenar",
                   "attribution": f"Fuente: Instituto Nacional de Estadística (INE), INEbase Historia, Censo de {year}",
                   "evidence_url": "https://www.ine.es/ine/codigobp/politica_difusion_es.pdf", "checked_at": TODAY,
                   "note": "El INE aplica a la información de su web la licencia CC BY 4.0 salvo indicación contraria (Política de Difusión Estadística, febrero de 2026)."},
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Transcrita a mano de la imagen del PDF; todas las filas cuadradas por estado civil e instrucción, totales nacionales impresos reproducidos columna a columna y totales provinciales contrastados con la suma municipal de mapSpainHist."},
        "consulted_at": TODAY,
    }, ensure_ascii=False, indent=2) + "\n")


def tasa(d: dict, sexos) -> float:
    t = sum(d[s]["total"] for s in sexos)
    return round(100 * sum(d[s]["saben_solo_leer"] + d[s]["saben_leer_y_escribir"] for s in sexos) / t, 1)


def observaciones(year: str, data: dict, sexos) -> list:
    did = f"doc-ine-censo{year}-instruccion"
    out = []
    for cod in sorted(k for k in data if k not in ("AF", "CAN")):
        o = {"place_id": f"plc-prov-{cod}", "period": year, "value": tasa(data[cod], sexos), "document_id": did,
             "locator": f"fila de la provincia {cod}, columnas «saben leer» y «saben leer y escribir»"}
        notas = " ".join(data[cod][s]["nota"] for s in sexos if data[cod][s]["nota"])
        if notas:
            o["uncertainty"] = notas
        if year == "1920" and cod == "17":
            o["uncertainty"] = "El total de la tabla supera en 60 habitantes la suma municipal de mapSpainHist; diferencia sin explicar, sin efecto apreciable en el porcentaje."
        out.append(o)
    if "CAN" in data:
        v = tasa(data["CAN"], sexos)
        for cod in ("35", "38"):
            out.append({"place_id": f"plc-prov-{cod}", "period": year, "value": None, "document_id": did,
                        "missingness_reason": f"En {year} Canarias era una sola provincia; el censo da {str(v).replace('.', ',')} % para el conjunto del archipiélago."})
    for pid, motivo in SINDATO[year].items():
        out.append({"place_id": pid, "period": year, "value": None, "document_id": did, "missingness_reason": motivo})
    return out


def main() -> None:
    datos = {y: leer(y) for y in CENSOS}
    for y in CENSOS:
        documento(y)
    base = {
        "unit": "% de la población de hecho",
        "denominator": "población de hecho de todas las edades",
        "method": "(saben solo leer + saben leer y escribir) / total de la población de hecho, sobre las tablas oficiales de los censos de 1920 y 1930 transcritas a mano con comprobación aritmética (scripts/etl/ine_alfabetizacion.py).",
        "source_ids": ["F010"],
        "comparability_notes": "El denominador incluye a toda la población, también a los menores que aún no estaban en edad de aprender a leer, así que la cifra es más baja que las tasas de alfabetización calculadas sobre mayores de 10 años que usa la historiografía. Es una declaración censal, no una prueba de lectura. 1920 y 1930 usan la misma clasificación y son comparables entre sí; en 1920 Canarias era una sola provincia y Cádiz incluía Ceuta.",
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Generado por scripts/etl/ine_alfabetizacion.py desde las transcripciones comprobadas. Pendiente de segunda revisión humana."},
    }
    for sufijo, sexos, concepto, quien in (("total", ("varones", "mujeres"), "Población que sabe leer", "la población"),
                                           ("varones", ("varones",), "Varones que saben leer", "los varones"),
                                           ("mujeres", ("mujeres",), "Mujeres que saben leer", "las mujeres")):
        iid = f"ind-alfab-{sufijo}-prov"
        obs = [o for y in CENSOS for o in observaciones(y, datos[y], sexos)]
        (OUT / f"indicators/{iid}.json").write_text(json.dumps({
            "id": iid, "concept": f"{concepto}, 1920 y 1930",
            "definition": f"Porcentaje de {quien} de hecho de cada provincia que, según el censo, sabía leer (solo leer, o leer y escribir).",
            **base, "observations": obs}, ensure_ascii=False, indent=2) + "\n")
    for y in CENSOS:
        imp = CENSOS[y]["impreso"]
        print(y, {s: round(100 * (imp[s][5] + imp[s][6]) / imp[s][0], 1) for s in imp},
              "total", round(100 * sum(imp[s][5] + imp[s][6] for s in imp) / sum(imp[s][0] for s in imp), 1))


if __name__ == "__main__":
    main()
