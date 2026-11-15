"""Alfabetización de los mayores de 10 años por provincia, censo de 1930 (INE, Tomo III).

Fuente: Censo de 1930, Tomo III. Volúmenes regionales, tabla «Clasificación de los habitantes por su
edad combinada con el sexo, estado civil e instrucción elemental» de cada provincia (un PDF por
provincia en INEbase Historia; su número td figura en el CSV y en cada observación). El td de cada
provincia se localizó recorriendo el árbol del Tomo III (treeNavigation.do?tn=92538).

Entrada: data/external/ine1930/instruccion_edad_1930_provincias.csv, transcrita de la imagen del
bloque «Resumen de la PROVINCIA»: por sexo, filas «Habitantes según su edad», «Saben sólo leer»,
«Saben escribir», «No saben leer» y «No consta», columnas TOTAL y menos de 5, 5, 6, 7, 8 y 9 años.

Cálculo: mayores de 10 = TOTAL menos las seis columnas de menos de 10 años (incluye, por tanto, a
quienes no declararon la edad). Tasa = (saben sólo leer + saben escribir) / habitantes, ambos de 10
años en adelante.

Comprobaciones (fallan con AssertionError):
  1. En cada provincia, sexo y columna, las cuatro filas de instrucción suman la de habitantes,
     tras aplicar CORRECCIONES (erratas con testigo) y salvo los descuadres anotados en ERRATAS.
  2. La columna TOTAL coincide, fila a fila, con la transcripción independiente del Tomo II
     (data/external/ine1930/instruccion_1930_provincias.csv).

Salidas: data/canonical/documents/doc-ine-censo1930-edad-instruccion.json
         data/canonical/indicators/ind-alfab10-{total,varones,mujeres}-prov.json

Uso: python3 -I scripts/etl/ine_alfabetizacion_edad_1930.py
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
SRC = ROOT / "data/external/ine1930/instruccion_edad_1930_provincias.csv"
TOMO2 = ROOT / "data/external/ine1930/instruccion_1930_provincias.csv"
TODAY = "2026-11-15"
DID = "doc-ine-censo1930-edad-instruccion"
FILAS = ["habitantes", "solo_leer", "leer_escribir", "no_saben", "no_consta"]
JOVEN = ["m5", "e5", "e6", "e7", "e8", "e9"]
T2 = {"habitantes": "total", "solo_leer": "saben_solo_leer", "leer_escribir": "saben_leer_y_escribir",
      "no_saben": "no_saben_leer", "no_consta": "instr_no_consta"}
SEXO = {"V": "varones", "H": "mujeres"}
# Erratas de la tabla impresa corregidas: (cod_prov, sexo, fila, columna) -> (impreso, corregido, motivo).
# En las columnas de menos de 10 años todos son solteros, así que la fila «Solteros» repite la de habitantes
# y sirve de testigo independiente.
CORRECCIONES = {
    ("11", "H", "habitantes", "e7"): (4691, 5691, "Cádiz, mujeres de 7 años: la tabla imprime 4.691 habitantes; la fila de solteras y la suma de la instrucción dan 5.691."),
    ("24", "V", "habitantes", "e9"): (5069, 5059, "León, varones de 9 años: la tabla imprime 5.069 habitantes; la fila de solteros y la suma de la instrucción dan 5.059."),
    ("30", "V", "no_saben", "total"): (59938, 159938, "Murcia, varones que no saben leer: la tabla imprime 59.938; el Tomo II y el total conjunto impreso (211.644 + 159.938 = 371.582) dan 159.938."),
    ("33", "H", "leer_escribir", "e8"): (4037, 5037, "Oviedo, mujeres de 8 años que saben escribir: la tabla imprime 4.037 y la instrucción suma 1.000 menos que los habitantes, que confirma la fila de solteras; se atribuye el error a esta fila por la progresión por edades (3.596 a los 7 años, 5.769 a los 9)."),
}
# Descuadres sin corregir porque no se puede saber qué fila de instrucción está mal impresa: (cod_prov, sexo, columna) -> diferencia.
# Ninguno afecta a las filas de habitantes (confirmadas por la de solteros) y su efecto en las tasas es menor de 0,01 puntos.
ERRATAS = {
    ("13", "H", "m5"): 10, ("29", "V", "e8"): 10, ("30", "V", "e9"): 1, ("30", "H", "e9"): -1,
    ("31", "V", "m5"): 600, ("33", "V", "e6"): 82, ("47", "V", "e6"): 1,
}
NOTA_PROV = {
    "11": "Corregida una errata de la tabla impresa (mujeres de 7 años).",
    "24": "Corregida una errata de la tabla impresa (varones de 9 años).",
    "30": "Corregida una errata de la tabla impresa (varones que no saben leer: 59.938 por 159.938). En la columna de 9 años la instrucción difiere en 1 de los habitantes.",
    "33": "Corregida una errata de la tabla impresa (mujeres de 8 años que saben escribir: 4.037 por 5.037, atribuida por la progresión por edades).",
    "13": "En la columna de menores de 5 años (mujeres) la instrucción suma 10 menos que los habitantes; efecto inapreciable.",
    "29": "Escaneo muy degradado; en la columna de 8 años (varones) la instrucción suma 10 menos que los habitantes; efecto inapreciable.",
}


def leer() -> dict:
    d: dict = {}
    for r in csv.DictReader(SRC.open(encoding="utf-8")):
        c = d.setdefault(r["cod_prov"], {"td": r["td"]})
        v = {k: int(r[k]) for k in ["total"] + JOVEN}
        for k in v:
            corr = CORRECCIONES.get((r["cod_prov"], r["sexo"], r["fila"], k))
            if corr:
                assert v[k] == corr[0], f"{r['cod_prov']} {r['sexo']} {r['fila']} {k}: se esperaba {corr[0]} impreso"
                v[k] = corr[1]
        c.setdefault(r["sexo"], {})[r["fila"]] = v
    t2 = {(r["cod_prov"], r["sexo"]): r for r in csv.DictReader(TOMO2.open(encoding="utf-8"))}
    assert len(d) == 50, f"{len(d)} provincias"
    for cod, c in d.items():
        for s in "VH":
            f = c[s]
            for col in ["total"] + JOVEN:
                suma = sum(f[x][col] for x in FILAS[1:])
                dif = ERRATAS.get((cod, s, col), 0)
                assert f["habitantes"][col] - suma == dif, f"{cod} {s} {col}: instrucción {suma} ≠ habitantes {f['habitantes'][col]}"
            for x in FILAS:
                ref = int(t2[(cod, SEXO[s])][T2[x]])
                assert f[x]["total"] == ref, f"{cod} {s} {x}: Tomo III {f[x]['total']} ≠ Tomo II {ref}"
    return d


def mayores(f: dict, fila: str) -> int:
    return f[fila]["total"] - sum(f[fila][c] for c in JOVEN)


def tasa(c: dict, sexos: str) -> float:
    lee = sum(mayores(c[s], "solo_leer") + mayores(c[s], "leer_escribir") for s in sexos)
    return round(100 * lee / sum(mayores(c[s], "habitantes") for s in sexos), 1)


def main() -> None:
    d = leer()
    (OUT / f"documents/{DID}.json").write_text(json.dumps({
        "id": DID,
        "title": "Censo de 1930, Tomo III: habitantes por edad, sexo, estado civil e instrucción elemental, resumen de cada provincia",
        "title_original": "Clasificación de los habitantes por su edad combinada con el sexo, estado civil e instrucción elemental",
        "document_type": "tabla_estadistica", "source_ids": ["F010"],
        "custodian": "Instituto Nacional de Estadística, INEbase Historia (fondo documental)",
        "signature": "Censo de la población de España de 1930, Tomo III. Volúmenes regionales, tabla de edad e instrucción de cada provincia (un PDF por provincia; su número td figura en cada observación)",
        "canonical_url": "https://www.ine.es/inebaseweb/treeNavigation.do?tn=92538",
        "date": "1930-12-31", "date_precision": "dia", "place_ids": ["plc-espana"],
        "summary": "Tablas oficiales del censo de 1930, una por provincia, que cruzan la edad de los habitantes de hecho con el sexo, el estado civil y la instrucción elemental (saben solo leer, saben escribir, no saben leer, no consta).",
        "context": "Cifras oficiales de la Dirección General de Estadística. La instrucción se declaraba en la hoja censal, sin prueba de lectura. Permiten calcular la alfabetización de los mayores de 10 años, la medida habitual en la historiografía.",
        "text_origin": "transcripcion_validada",
        "rights": {"status": "cc_by", "action": "almacenar",
                   "attribution": "Fuente: Instituto Nacional de Estadística (INE), INEbase Historia, Censo de 1930",
                   "evidence_url": "https://www.ine.es/ine/codigobp/politica_difusion_es.pdf", "checked_at": TODAY,
                   "note": "El INE aplica a la información de su web la licencia CC BY 4.0 salvo indicación contraria (Política de Difusión Estadística, febrero de 2026)."},
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Transcrita de la imagen del PDF; cada columna cuadrada por instrucción y la columna total contrastada fila a fila con la transcripción independiente del Tomo II."},
        "consulted_at": TODAY,
    }, ensure_ascii=False, indent=2) + "\n")
    base = {
        "unit": "% de la población de hecho de 10 años o más",
        "denominator": "población de hecho de 10 años o más (incluye a quienes no declararon la edad)",
        "method": "(saben solo leer + saben escribir) / habitantes, ambos de 10 años en adelante, calculados como el total menos las columnas de menos de 5 y de 5 a 9 años de la tabla de edad e instrucción de cada provincia (Tomo III del censo de 1930), transcrita con comprobación aritmética (scripts/etl/ine_alfabetizacion_edad_1930.py).",
        "source_ids": ["F010"],
        "comparability_notes": "Medida habitual en la historiografía, más alta que la calculada sobre toda la población (ind-alfab-*). Es una declaración censal, no una prueba de lectura. Solo 1930: el Tomo III de 1920 no se ha transcrito.",
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Generado por scripts/etl/ine_alfabetizacion_edad_1930.py. Pendiente de segunda revisión humana."},
    }
    for suf, sexos, concepto, quien in (("total", "VH", "Saben leer, mayores de 10 años, 1930", "la población"),
                                        ("varones", "V", "Varones que saben leer, mayores de 10 años, 1930", "los varones"),
                                        ("mujeres", "H", "Mujeres que saben leer, mayores de 10 años, 1930", "las mujeres")):
        obs = []
        for cod in sorted(d):
            o = {"place_id": f"plc-prov-{cod}", "period": "1930", "value": tasa(d[cod], sexos), "document_id": DID,
                 "locator": f"«Resumen de la PROVINCIA», columnas total y menos de 10 años, PDF https://www.ine.es/inebaseweb/pdfDispacher.do?td={d[cod]['td']}&ext=.pdf"}
            if cod in NOTA_PROV:
                o["uncertainty"] = NOTA_PROV[cod]
            obs.append(o)
        for pid in ("plc-prov-51", "plc-prov-52"):
            obs.append({"place_id": pid, "period": "1930", "value": None, "document_id": DID,
                        "missingness_reason": "El Tomo III de 1930 no trae tabla propia de Ceuta y Melilla."})
        iid = f"ind-alfab10-{suf}-prov"
        (OUT / f"indicators/{iid}.json").write_text(json.dumps({
            "id": iid, "concept": concepto,
            "definition": f"Porcentaje de {quien} de hecho de 10 años o más de cada provincia que, según el censo de 1930, sabía leer (solo leer, o leer y escribir).",
            **base, "observations": obs}, ensure_ascii=False, indent=2) + "\n")
    nac = {s: round(100 * sum(mayores(d[c][s], "solo_leer") + mayores(d[c][s], "leer_escribir") for c in d) /
                    sum(mayores(d[c][s], "habitantes") for c in d), 1) for s in "VH"}
    tot = round(100 * sum(mayores(d[c][s], "solo_leer") + mayores(d[c][s], "leer_escribir") for c in d for s in "VH") /
                sum(mayores(d[c][s], "habitantes") for c in d for s in "VH"), 1)
    ext = sorted((tasa(d[c], "VH"), c) for c in d)
    print("España sin Ceuta y Melilla, mayores de 10:", nac, "total", tot, "| mín", ext[0], "máx", ext[-1])


if __name__ == "__main__":
    main()
