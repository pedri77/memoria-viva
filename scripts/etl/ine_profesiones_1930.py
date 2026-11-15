"""Población con profesión por grupos, censo de 1930 (INE, INEbase Historia, Tomo III).

Entrada, transcrita a mano de las tablas oficiales «Habitantes inscritos en la población de
HECHO y clasificados por sexo, edad, estado civil y profesiones o industrias», bloque de la
PROVINCIA entera de cada volumen regional:
  data/external/ine1930/profesiones_1930_provincias.csv
  (cod_prov, td, paginas, grupo, varones, mujeres, total, nota). Grupos I-XXVII según los
  «TOTALES DEL GRUPO» impresos, y la fila 85 («Diversas», grupo XV) como grupo «f85».

Comprobaciones de cada provincia (fallan con AssertionError):
  1. Están los 27 grupos, una vez cada uno, y la fila 85.
  2. En cada grupo, varones + mujeres = total.
  3. La suma de los 27 grupos reproduce, por sexo, los totales de la tabla de instrucción
     de 1930 (data/external/ine1930/instruccion_1930_provincias.csv, ya comprobada).
  4. La suma total coincide con la población de hecho de 1930 (ind-pob-hecho-prov).

Salidas: data/canonical/documents/doc-ine-censo1930-profesiones.json
         data/canonical/indicators/ind-prof-agraria-prov.json          (grupo II, ambos sexos)
         data/canonical/indicators/ind-prof-agraria-varones-prov.json  (grupo II, varones)
         data/canonical/indicators/ind-prof-diversas-prov.json         (fila 85, ambos sexos)

Uso: python3 -I scripts/etl/ine_profesiones_1930.py
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
SRC = ROOT / "data/external/ine1930/profesiones_1930_provincias.csv"
INSTR = ROOT / "data/external/ine1930/instruccion_1930_provincias.csv"
TODAY = "2026-11-15"
DID = "doc-ine-censo1930-profesiones"
G = "I II III IV V VI VII VIII IX X XI XII XIII XIV XV XVI XVII XVIII XIX XX XXI XXII XXIII XXIV XXV XXVI XXVII".split()
SIN_PROFESION = ("XXIV", "XXV", "XXVI", "XXVII")  # población escolar, improductivos, miembros de la familia, profesión desconocida
# Provincias cuyo PDF no trae todas las páginas: grupos ausentes y motivo.
PARCIALES = {
    "11": {"faltan": ["XII", "XIII", "XIV", "XV", "XVI", "f85"],
           "motivo": "El PDF de Cádiz no trae la página de la provincia con las filas 64 a 90 (grupos XII a XVI)."},
    "17": {"faltan": ["I", "II", "III", "IV", "V", "VI"],
           "motivo": "Al PDF de Gerona le falta la primera página de la provincia (impresas 116 y 117, filas 1 a 33: grupos I a VI)."},
    "48": {"faltan":["I", "II", "III", "IV", "V", "VI"],
           "motivo": "En el PDF de Vizcaya la página de la provincia con las filas 1 a 33 (grupos I a VI) es una hoja sin tabla."},
}
SINDATO = {
    "plc-prov-51": "Las posesiones del norte y costa occidental de África no tienen tabla de profesiones en el Tomo III del censo de 1930.",
    "plc-prov-52": "Las posesiones del norte y costa occidental de África no tienen tabla de profesiones en el Tomo III del censo de 1930.",
}


def leer() -> dict:
    data: dict = {}
    for r in csv.DictReader(SRC.open(encoding="utf-8")):
        d = data.setdefault(r["cod_prov"], {"td": r["td"], "paginas": r["paginas"], "g": {}, "notas": []})
        v, m, t = int(r["varones"]), int(r["mujeres"]), int(r["total"])
        assert v + m == t, f"{r['cod_prov']} grupo {r['grupo']}: {v}+{m} != {t}"
        assert r["grupo"] not in d["g"], f"{r['cod_prov']}: grupo {r['grupo']} repetido"
        d["g"][r["grupo"]] = (v, m, t)
        if r["nota"]:
            d["notas"].append(r["nota"])
    sexo = {(r["cod_prov"], r["sexo"]): int(r["total"]) for r in csv.DictReader(INSTR.open(encoding="utf-8"))}
    hecho = json.loads((OUT / "indicators/ind-pob-hecho-prov.json").read_text())
    pob = {o["place_id"]: o["value"] for o in hecho["observations"] if o["period"] == "1930"}
    for cod, d in data.items():
        falta = PARCIALES.get(cod, {}).get("faltan", [])
        assert sorted(d["g"]) == sorted(g for g in G + ["f85"] if g not in falta), f"{cod}: grupos {set(G + ['f85']) - set(d['g']) - set(falta)} sin transcribir"
        sv = sum(d["g"][g][0] for g in G if g not in falta); sm = sum(d["g"][g][1] for g in G if g not in falta)
        ref = (sexo[(cod, "varones")], sexo[(cod, "mujeres")])
        assert ref[0] + ref[1] == pob[f"plc-prov-{cod}"], f"{cod}: el censo por sexo no suma la población de hecho"
        if falta:
            # Grupos ausentes del PDF: su suma conjunta se deduce del total por sexo y no puede ser negativa.
            assert ref[0] - sv >= 0 and ref[1] - sm >= 0, f"{cod}: los grupos leídos superan el total"
            d["resto"] = (ref[0] - sv, ref[1] - sm, ref[0] + ref[1] - sv - sm)
        else:
            assert (sv, sm) == ref, f"{cod}: suma por sexo {(sv, sm)} frente a {ref}"
            assert d["g"]["f85"][2] <= d["g"]["XV"][2], f"{cod}: la fila 85 supera el total del grupo XV"
    return data


def documento(data: dict) -> None:
    (OUT / f"documents/{DID}.json").write_text(json.dumps({
        "id": DID,
        "title": "Censo de 1930, Tomo III: población de hecho por sexo, edad, estado civil y profesiones o industrias, por provincias",
        "title_original": "Habitantes inscritos en la población de HECHO y clasificados por sexo, edad, estado civil y profesiones o industrias",
        "document_type": "tabla_estadistica", "source_ids": ["F010"],
        "custodian": "Instituto Nacional de Estadística, INEbase Historia (fondo documental)",
        "signature": "Censo de la población de España de 1930, Tomo III. Volúmenes regionales, tabla de profesiones de cada provincia (un PDF por provincia; su número td figura en cada observación)",
        "canonical_url": "https://www.ine.es/inebaseweb/treeNavigation.do?tn=92538",
        "date": "1930-12-31", "date_precision": "dia", "place_ids": ["plc-espana"],
        "summary": "Tablas oficiales del censo de 1930 que clasifican la población de hecho de cada provincia por sexo, edad y estado civil en 129 profesiones o industrias agrupadas en 27 grupos, del I (pesca) al XXVII (profesión desconocida).",
        "context": "Cifras oficiales de la Dirección General de Estadística. La profesión se declaraba en la hoja censal. Las mujeres que trabajaban en la casa o en la explotación familiar figuran sobre todo en el grupo XXVI («miembros de la familia»), no en el de su actividad; y el grupo XV incluye una fila «Diversas» muy numerosa en algunas provincias que no especifica la actividad.",
        "text_origin": "transcripcion_validada",
        "rights": {"status": "cc_by", "action": "almacenar",
                   "attribution": "Fuente: Instituto Nacional de Estadística (INE), INEbase Historia, Censo de 1930",
                   "evidence_url": "https://www.ine.es/ine/codigobp/politica_difusion_es.pdf", "checked_at": TODAY,
                   "note": "El INE aplica a la información de su web la licencia CC BY 4.0 salvo indicación contraria (Política de Difusión Estadística, febrero de 2026)."},
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": f"Transcritos a mano los totales de los 27 grupos y la fila 85 de {len(data)} provincias; en cada una, varones + mujeres = total por grupo, y la suma de los grupos reproduce por sexo los totales del censo y la población de hecho."},
        "consulted_at": TODAY,
    }, ensure_ascii=False, indent=2) + "\n")


def obs(data: dict, fila: str, sexo: int) -> list:
    out = []
    for cod in sorted(data):
        d = data[cod]
        con = d["g"]
        if fila not in con:
            out.append({"place_id": f"plc-prov-{cod}", "period": "1930", "value": None, "document_id": DID,
                        "missingness_reason": PARCIALES[cod]["motivo"]})
            continue
        total = sum(con[g][sexo] for g in G if g in con) + (d["resto"][sexo] if "resto" in d else 0)
        denom = total - sum(con[g][sexo] for g in SIN_PROFESION)
        o = {"place_id": f"plc-prov-{cod}", "period": "1930", "value": round(100 * con[fila][sexo] / denom, 1), "document_id": DID,
             "locator": f"provincia entera, págs. {d['paginas']} del PDF https://www.ine.es/inebaseweb/pdfDispacher.do?td={d['td']}&ext=.pdf; «Totales del grupo» {'II' if fila == 'II' else 'XV, fila 85'} y grupos XXIV a XXVII"}
        notas = list(d["notas"])
        if "resto" in d:
            notas.append(PARCIALES[cod]["motivo"] + " Esos grupos no se necesitan para este dato: el denominador usa el total por sexo del censo.")
        if notas:
            o["uncertainty"] = " ".join(notas)
        out.append(o)
    for pid, motivo in SINDATO.items():
        out.append({"place_id": pid, "period": "1930", "value": None, "document_id": DID, "missingness_reason": motivo})
    return out


def main() -> None:
    data = leer()
    documento(data)
    base = {
        "unit": "% de la población con profesión",
        "denominator": "población de hecho menos los grupos XXIV (población escolar), XXV (improductivos), XXVI (miembros de la familia) y XXVII (profesión desconocida)",
        "source_ids": ["F010"],
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Generado por scripts/etl/ine_profesiones_1930.py desde la transcripción comprobada. Pendiente de segunda revisión humana."},
    }
    nota_diversas = "Una parte de la fila 85 («Diversas», grupo XV) corresponde con probabilidad a jornaleros sin actividad declarada, también agrícolas; por eso el peso del grupo II es un mínimo. El indicador ind-prof-diversas-prov muestra el tamaño de esa fila en cada provincia."
    nota_mujeres = "El trabajo de las mujeres en la explotación familiar se registra sobre todo en el grupo XXVI y no cuenta en el denominador."
    for iid, fila, sexo, concepto, definicion, notas in (
        ("ind-prof-agraria-prov", "II", 2, "Población con profesión en explotaciones forestales y agrícolas, 1930",
         "Porcentaje de la población con profesión de cada provincia clasificada en el grupo II del censo de 1930 (explotación de montes, agricultura y ganadería).", f"{nota_diversas} {nota_mujeres}"),
        ("ind-prof-agraria-varones-prov", "II", 0, "Varones con profesión en explotaciones forestales y agrícolas, 1930",
         "Porcentaje de los varones con profesión de cada provincia clasificados en el grupo II del censo de 1930.", nota_diversas),
        ("ind-prof-diversas-prov", "f85", 2, "Población con profesión en «industrias diversas» (fila 85), 1930",
         "Porcentaje de la población con profesión de cada provincia clasificada en la fila 85, «Diversas», del grupo XV («Industrias varias») del censo de 1930.",
         "La fila no especifica la actividad. Se publica para medir la incertidumbre del grupo II: donde es grande, el peso real de la agricultura puede ser mayor que el que da el grupo II."),
    ):
        (OUT / f"indicators/{iid}.json").write_text(json.dumps({
            "id": iid, "concept": concepto, "definition": definicion, **base,
            "method": f"Total del {'grupo II' if fila == 'II' else 'grupo XV, fila 85'} / (población de hecho − grupos XXIV a XXVII), {'varones' if sexo == 0 else 'ambos sexos'}, sobre la tabla oficial transcrita a mano con comprobación aritmética (scripts/etl/ine_profesiones_1930.py).",
            "comparability_notes": notas, "observations": obs(data, fila, sexo)}, ensure_ascii=False, indent=2) + "\n")
    comp = [c for c in data if c not in PARCIALES]
    tot = {g: sum(data[c]["g"][g][2] for c in comp) for g in G + ["f85"]}
    con = sum(tot[g] for g in G) - sum(tot[g] for g in SIN_PROFESION)
    print(f"{len(data)} provincias ({len(comp)} completas). En las completas: grupo II = {100 * tot['II'] / con:.1f} % de la población con profesión; fila 85 = {100 * tot['f85'] / con:.1f} %")


if __name__ == "__main__":
    main()
