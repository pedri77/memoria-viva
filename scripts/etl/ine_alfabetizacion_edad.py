"""Alfabetización de los mayores de 10 años por provincia, censos de 1920 y 1930 (INE, Tomo III).

Fuente: Tomo III de cada censo, tabla «Clasificación de los habitantes por su edad combinada con el sexo,
estado civil e instrucción elemental» de cada provincia (un PDF por provincia en INEbase Historia; su número
td figura en el CSV y en cada observación). Los td se localizaron recorriendo el árbol del Tomo III
(1930: treeNavigation.do?tn=92538; 1920: tn=88197; ojo, tn=80563 es el Tomo III de 1910).

Entradas: data/external/ine1930/instruccion_edad_1930_provincias.csv y
          data/external/ine1920/instruccion_edad_1920_provincias.csv, transcritas de la imagen del bloque de
          resumen de la provincia: por sexo, filas habitantes, saben sólo leer, saben escribir, no saben leer
          y no consta; columnas TOTAL y menos de 5, 5, 6, 7, 8 y 9 años.

Cálculo: mayores de 10 = TOTAL menos las seis columnas de menos de 10 años (incluye a quienes no declararon
la edad). Tasa = (saben sólo leer + saben escribir) / habitantes, ambos de 10 años en adelante.

Comprobaciones (fallan con AssertionError):
  1. En cada provincia, sexo y columna, las cuatro filas de instrucción suman la de habitantes, tras aplicar
     las correcciones (erratas con testigo) y salvo los descuadres anotados en «erratas».
  2. La columna TOTAL coincide, fila a fila, con la transcripción independiente del Tomo II, salvo en 1920
     el reparto de la instrucción de Cuenca, Gerona y Orense («dif_tomo2»): los dos tomos publican cifras
     distintas y el Tomo III coincide con su propio resumen nacional (td 88553).

Salidas: data/canonical/documents/doc-ine-censo{1920,1930}-edad-instruccion.json
         data/canonical/indicators/ind-alfab10-{total,varones,mujeres}-prov.json

Uso: python3 -I scripts/etl/ine_alfabetizacion_edad.py
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
TODAY = "2026-11-15"
FILAS = ["habitantes", "solo_leer", "leer_escribir", "no_saben", "no_consta"]
JOVEN = ["m5", "e5", "e6", "e7", "e8", "e9"]
T2 = {"habitantes": "total", "solo_leer": "saben_solo_leer", "leer_escribir": "saben_leer_y_escribir",
      "no_saben": "no_saben_leer", "no_consta": "instr_no_consta"}
SEXO = {"V": "varones", "H": "mujeres"}
# En las columnas de menos de 10 años todos son solteros, así que la fila «Solteros» repite la de habitantes
# y sirve de testigo independiente.
CENSOS = {
    "1930": {
        "src": ROOT / "data/external/ine1930/instruccion_edad_1930_provincias.csv",
        "tomo2": ROOT / "data/external/ine1930/instruccion_1930_provincias.csv",
        "arbol": "92538", "n": 50,
        "titulo": "Censo de 1930, Tomo III: habitantes por edad, sexo, estado civil e instrucción elemental, resumen de cada provincia",
        "bloque": "«Resumen de la PROVINCIA»",
        # (cod_prov, sexo, fila, columna) -> (impreso, corregido, motivo)
        "correcciones": {
            ("11", "H", "habitantes", "e7"): (4691, 5691, "Cádiz, mujeres de 7 años: la tabla imprime 4.691 habitantes; la fila de solteras y la suma de la instrucción dan 5.691."),
            ("24", "V", "habitantes", "e9"): (5069, 5059, "León, varones de 9 años: la tabla imprime 5.069 habitantes; la fila de solteros y la suma de la instrucción dan 5.059."),
            ("30", "V", "no_saben", "total"): (59938, 159938, "Murcia, varones que no saben leer: la tabla imprime 59.938; el Tomo II y el total conjunto impreso (211.644 + 159.938 = 371.582) dan 159.938."),
            ("33", "H", "leer_escribir", "e8"): (4037, 5037, "Oviedo, mujeres de 8 años que saben escribir: la tabla imprime 4.037 y la instrucción suma 1.000 menos que los habitantes, que confirma la fila de solteras; se atribuye el error a esta fila por la progresión por edades (3.596 a los 7 años, 5.769 a los 9)."),
        },
        # Descuadres sin corregir: (cod_prov, sexo, columna) -> habitantes − suma de la instrucción
        "erratas": {("13", "H", "m5"): 10, ("29", "V", "e8"): 10, ("30", "V", "e9"): 1, ("30", "H", "e9"): -1,
                    ("31", "V", "m5"): 600, ("33", "V", "e6"): 82, ("47", "V", "e6"): 1},
        # Diferencias aceptadas con el Tomo II: (cod_prov, sexo) -> motivo
        "dif_tomo2": {},
        "notas": {
            "11": "Corregida una errata de la tabla impresa (mujeres de 7 años).",
            "24": "Corregida una errata de la tabla impresa (varones de 9 años).",
            "30": "Corregida una errata de la tabla impresa (varones que no saben leer: 59.938 por 159.938). En la columna de 9 años la instrucción difiere en 1 de los habitantes.",
            "33": "Corregida una errata de la tabla impresa (mujeres de 8 años que saben escribir: 4.037 por 5.037, atribuida por la progresión por edades).",
            "13": "En la columna de menores de 5 años (mujeres) la instrucción suma 10 menos que los habitantes; efecto inapreciable.",
            "29": "Escaneo muy degradado; en la columna de 8 años (varones) la instrucción suma 10 menos que los habitantes; efecto inapreciable.",
        },
    },
    "1920": {
        "src": ROOT / "data/external/ine1920/instruccion_edad_1920_provincias.csv",
        "tomo2": ROOT / "data/external/ine1920/instruccion_1920_provincias.csv",
        "arbol": "88197", "n": 49,
        "titulo": "Censo de 1920, Tomo III: habitantes por edad, sexo, estado civil e instrucción elemental, resumen de cada provincia",
        "bloque": "«Resumen de la provincia»",
        "correcciones": {
            ("42", "V", "no_saben", "e9"): (579, 379, "Soria, varones de 9 años que no saben leer: la tabla imprime 579; los habitantes (1.803, confirmados por la fila de solteros) y el total de la fila «No saben leer» solo cuadran con 379."),
            ("17", "V", "no_consta", "total"): (173, 178, "Gerona, varones con instrucción «no consta»: la tabla imprime 173; los habitantes de la fila y el total conjunto impreso (431 = 178 + 253) dan 178."),
        },
        "erratas": {("16", "H", "e9"): -2, ("20", "V", "e7"): 1, ("27", "H", "e9"): -20, ("48", "H", "e5"): -47, ("CAN", "H", "e8"): -10},
        "dif_tomo2": {
            ("16", "V"): "Cuenca", ("16", "H"): "Cuenca", ("17", "V"): "Gerona", ("32", "H"): "Orense",
        },
        "notas": {
            "42": "Corregida una errata de la tabla impresa (varones de 9 años que no saben leer: 579 por 379).",
            "17": "Corregida una errata de la tabla impresa (varones con instrucción «no consta»: 173 por 178). El reparto de la instrucción de los varones difiere del Tomo II del mismo censo; se usa el del Tomo III.",
            "16": "El reparto de la instrucción difiere del publicado en el Tomo II del mismo censo (mismos habitantes); se usa el del Tomo III, que coincide con su propio resumen nacional. En la columna de 9 años (mujeres) la instrucción suma 2 más que los habitantes.",
            "32": "El reparto de la instrucción de las mujeres difiere mucho del publicado en el Tomo II del mismo censo (11.519 frente a 14.225 que saben solo leer, con los mismos habitantes); se usa el del Tomo III, que coincide con su propio resumen nacional.",
            "27": "En la columna de 9 años (mujeres) la instrucción suma 20 más que los habitantes; efecto inapreciable.",
            "48": "En la columna de 5 años (mujeres) la instrucción suma 47 más que los habitantes; efecto inapreciable.",
        },
    },
}


def leer(year: str) -> dict:
    cfg = CENSOS[year]
    d: dict = {}
    for r in csv.DictReader(cfg["src"].open(encoding="utf-8")):
        c = d.setdefault(r["cod_prov"], {"td": r["td"]})
        v = {k: int(r[k]) for k in ["total"] + JOVEN}
        for k in v:
            corr = cfg["correcciones"].get((r["cod_prov"], r["sexo"], r["fila"], k))
            if corr:
                assert v[k] == corr[0], f"{year} {r['cod_prov']} {r['sexo']} {r['fila']} {k}: se esperaba {corr[0]} impreso"
                v[k] = corr[1]
        c.setdefault(r["sexo"], {})[r["fila"]] = v
    t2 = {(r["cod_prov"], r["sexo"]): r for r in csv.DictReader(cfg["tomo2"].open(encoding="utf-8"))}
    assert len(d) == cfg["n"], f"{year}: {len(d)} provincias"
    for cod, c in d.items():
        for s in "VH":
            f = c[s]
            for col in ["total"] + JOVEN:
                suma = sum(f[x][col] for x in FILAS[1:])
                dif = cfg["erratas"].get((cod, s, col), 0)
                assert f["habitantes"][col] - suma == dif, f"{year} {cod} {s} {col}: instrucción {suma} ≠ habitantes {f['habitantes'][col]}"
            for x in FILAS:
                ref = int(t2[(cod, SEXO[s])][T2[x]])
                if x == "habitantes" or (cod, s) not in cfg["dif_tomo2"]:
                    assert f[x]["total"] == ref, f"{year} {cod} {s} {x}: Tomo III {f[x]['total']} ≠ Tomo II {ref}"
    return d


def mayores(f: dict, fila: str) -> int:
    return f[fila]["total"] - sum(f[fila][c] for c in JOVEN)


def tasa(c: dict, sexos: str) -> float:
    lee = sum(mayores(c[s], "solo_leer") + mayores(c[s], "leer_escribir") for s in sexos)
    return round(100 * lee / sum(mayores(c[s], "habitantes") for s in sexos), 1)


def main() -> None:
    datos = {y: leer(y) for y in CENSOS}
    for y, cfg in CENSOS.items():
        did = f"doc-ine-censo{y}-edad-instruccion"
        (OUT / f"documents/{did}.json").write_text(json.dumps({
            "id": did, "title": cfg["titulo"],
            "title_original": "Clasificación de los habitantes por su edad combinada con el sexo, estado civil e instrucción elemental",
            "document_type": "tabla_estadistica", "source_ids": ["F010"],
            "custodian": "Instituto Nacional de Estadística, INEbase Historia (fondo documental)",
            "signature": f"Censo de la población de España de {y}, Tomo III, tabla de edad e instrucción de cada provincia (un PDF por provincia; su número td figura en cada observación)",
            "canonical_url": f"https://www.ine.es/inebaseweb/treeNavigation.do?tn={cfg['arbol']}",
            "date": f"{y}-12-31", "date_precision": "dia", "place_ids": ["plc-espana"],
            "summary": f"Tablas oficiales del censo de {y}, una por provincia, que cruzan la edad de los habitantes de hecho con el sexo, el estado civil y la instrucción elemental (saben solo leer, saben escribir, no saben leer, no consta).",
            "context": "Cifras oficiales de la Dirección General de Estadística. La instrucción se declaraba en la hoja censal, sin prueba de lectura. Permiten calcular la alfabetización de los mayores de 10 años, la medida habitual en la historiografía."
                       + (" En 1920 Canarias era una sola provincia y la de Cádiz incluía Ceuta. En tres provincias (Cuenca, Gerona y Orense) el reparto de la instrucción difiere del publicado en el Tomo II." if y == "1920" else ""),
            "text_origin": "transcripcion_validada",
            "rights": {"status": "cc_by", "action": "almacenar",
                       "attribution": f"Fuente: Instituto Nacional de Estadística (INE), INEbase Historia, Censo de {y}",
                       "evidence_url": "https://www.ine.es/ine/codigobp/politica_difusion_es.pdf", "checked_at": TODAY,
                       "note": "El INE aplica a la información de su web la licencia CC BY 4.0 salvo indicación contraria (Política de Difusión Estadística, febrero de 2026)."},
            "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                       "note": "Transcrita de la imagen del PDF; cada columna cuadrada por instrucción y la columna total contrastada fila a fila con la transcripción independiente del Tomo II."},
            "consulted_at": TODAY,
        }, ensure_ascii=False, indent=2) + "\n")
    base = {
        "unit": "% de la población de hecho de 10 años o más",
        "denominator": "población de hecho de 10 años o más (incluye a quienes no declararon la edad)",
        "method": "(saben solo leer + saben escribir) / habitantes, ambos de 10 años en adelante, calculados como el total menos las columnas de menos de 5 y de 5 a 9 años de la tabla de edad e instrucción de cada provincia (Tomo III de los censos de 1920 y 1930), transcrita con comprobación aritmética (scripts/etl/ine_alfabetizacion_edad.py).",
        "source_ids": ["F010"],
        "comparability_notes": "Medida habitual en la historiografía, más alta que la calculada sobre toda la población (ind-alfab-*). Es una declaración censal, no una prueba de lectura. En 1920 Canarias era una sola provincia y Cádiz incluía Ceuta.",
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Generado por scripts/etl/ine_alfabetizacion_edad.py. Pendiente de segunda revisión humana."},
    }
    for suf, sexos, concepto, quien in (("total", "VH", "Saben leer, mayores de 10 años, 1920 y 1930", "la población"),
                                        ("varones", "V", "Varones que saben leer, mayores de 10 años, 1920 y 1930", "los varones"),
                                        ("mujeres", "H", "Mujeres que saben leer, mayores de 10 años, 1920 y 1930", "las mujeres")):
        obs = []
        for y, d in datos.items():
            did = f"doc-ine-censo{y}-edad-instruccion"
            for cod in sorted(k for k in d if k != "CAN"):
                o = {"place_id": f"plc-prov-{cod}", "period": y, "value": tasa(d[cod], sexos), "document_id": did,
                     "locator": f"{CENSOS[y]['bloque']}, columnas total y menos de 10 años, PDF https://www.ine.es/inebaseweb/pdfDispacher.do?td={d[cod]['td']}&ext=.pdf"}
                nota = CENSOS[y]["notas"].get(cod, "")
                if y == "1920" and cod == "11":
                    nota = (nota + " " if nota else "") + "En 1920 la provincia de Cádiz incluía Ceuta."
                if nota:
                    o["uncertainty"] = nota
                obs.append(o)
            if "CAN" in d:
                v = str(tasa(d["CAN"], sexos)).replace(".", ",")
                for cod in ("35", "38"):
                    obs.append({"place_id": f"plc-prov-{cod}", "period": y, "value": None, "document_id": did,
                                "missingness_reason": f"En {y} Canarias era una sola provincia; el censo da {v} % para el conjunto del archipiélago."})
            for pid in ("plc-prov-51", "plc-prov-52"):
                obs.append({"place_id": pid, "period": y, "value": None, "document_id": did,
                            "missingness_reason": f"El Tomo III de {y} no trae una tabla propia de Ceuta y Melilla" + (" (en 1920 Ceuta va dentro de Cádiz)." if y == "1920" else ".")})
        iid = f"ind-alfab10-{suf}-prov"
        (OUT / f"indicators/{iid}.json").write_text(json.dumps({
            "id": iid, "concept": concepto,
            "definition": f"Porcentaje de {quien} de hecho de 10 años o más de cada provincia que, según los censos de 1920 y 1930, sabía leer (solo leer, o leer y escribir).",
            **base, "observations": obs}, ensure_ascii=False, indent=2) + "\n")
    for y, d in datos.items():
        nac = {s: round(100 * sum(mayores(d[c][s], "solo_leer") + mayores(d[c][s], "leer_escribir") for c in d) /
                        sum(mayores(d[c][s], "habitantes") for c in d), 1) for s in "VH"}
        tot = round(100 * sum(mayores(d[c][s], "solo_leer") + mayores(d[c][s], "leer_escribir") for c in d for s in "VH") /
                    sum(mayores(d[c][s], "habitantes") for c in d for s in "VH"), 1)
        ext = sorted((tasa(d[c], "VH"), c) for c in d)
        print(y, "mayores de 10:", nac, "total", tot, "| mín", ext[0], "máx", ext[-1])


if __name__ == "__main__":
    main()
