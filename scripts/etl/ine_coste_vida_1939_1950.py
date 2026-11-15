"""Índice del coste de la vida en las capitales de provincia, 1939-1950 (INE, Anuarios Estadísticos).

Fuente: Anuarios Estadísticos de España de 1943 a 1951, sección «Precios, salarios, racionamiento y
consumo», «Índice del coste de la vida en las capitales», promedios anuales por capital de provincia,
base julio de 1936 = 100. Siete tablas (td en TABLAS); cada una trae tres o cuatro años y varios se
repiten de una edición a otra.

Entrada: data/external/ine_anuarios/coste_vida_capitales_1939_1950.csv, con TODAS las lecturas
(columna `lector`): cada año está leído al menos dos veces, en dos ediciones del Anuario o, si solo
sale en una, por dos transcriptores independientes. Solo dos grupos: alimentación e índice general.

Comprobaciones (fallan con AssertionError):
  1. Cada tabla, año y grupo tiene las 50 capitales y la media nacional («ESPAÑA»).
  2. Cada año y grupo tiene al menos dos lecturas.
  3. Dos lecturas de la misma tabla coinciden, salvo las resueltas a la vista de la imagen (RESUELTAS).
  4. Entre ediciones distintas, las diferencias se aceptan como revisiones solo si están en REVISIONES.

Regla: para cada año se usa la edición más reciente del Anuario que lo publica.

Salidas: data/canonical/documents/doc-ine-anuarioAAAA-coste-vida.json (una por edición usada)
         data/canonical/indicators/ind-coste-vida-{alimentacion,general}-prov.json

Uso: python3 -I scripts/etl/ine_coste_vida_1939_1950.py
"""
import csv
import json
import pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
SRC = ROOT / "data/external/ine_anuarios/coste_vida_capitales_1939_1950.csv"
TODAY = "2026-11-15"
# td -> (edición del Anuario, años, páginas impresas si constan)
TABLAS = {
    "160628": ("1943", ["1939", "1940", "1941", "1942"]),
    "162162": ("1944-1945", ["1942", "1943", "1944"]),
    "162863": ("1946-1947", ["1944", "1945", "1946"]),
    "163586": ("1948", ["1945", "1946", "1947"]),
    "164740": ("1949", ["1946", "1947", "1948"]),
    "29950": ("1950", ["1949"]),
    "165640": ("1951", ["1950"]),
}
ORDEN = ["1943", "1944-1945", "1946-1947", "1948", "1949", "1950", "1951"]
ARBOL = {"1943": "161311", "1944-1945": "161457", "1946-1947": "163148", "1948": "163298", "1949": "164782", "1950": "30270", "1951": "166448"}
# (td, cod, año, grupo) -> (valor elegido, motivo)
RESUELTAS = {
    ("162162", "ES", "1943", "general"): ("245.0", "Media nacional de 1943, índice general: la tercera cifra está dañada (5 o 6); se toma 245,0, la lectura de la capa de texto del PDF y de la segunda transcripción. No se publica en el mapa."),
    ("165640", "30", "1950", "general"): ("566.5", "Murcia, 1950, índice general: el dígito central está dañado (se lee «5o6,5»); es un 6 sin el trazo superior, más bajo que los ceros enteros de la columna, y 566,5 es coherente con la subida de su alimentación (+12,6 %) y de las demás capitales, mientras que 506,5 supondría una bajada."),
}
# (cod, año, grupo) -> nota: diferencias entre ediciones aceptadas como revisión
REVISIONES = {
    ("12", "1947", "alimentacion"): "Castellón de la Plana, 1947, alimentación: el Anuario de 1948 imprime 505,9 y el de 1949, 504,9 (la capa de texto de los dos PDF lo confirma); se usa la edición más reciente.",
}
NOTA_1939 = "El dato de 1939 es el promedio del segundo semestre, no del año completo (nota «(a) 2.º semestre» de la tabla)."
NOTA_TABLA = ("Según la nota de las propias tablas, los índices miden la variación del coste de la vida en cada capital "
              "respecto a julio de 1936 y no permiten deducir que la vida fuera más cara en una capital que en otra.")


def leer():
    lect = defaultdict(list)
    for r in csv.DictReader(SRC.open(encoding="utf-8")):
        lect[(r["td"], r["cod"], r["anio"], r["grupo"])].append(r)
    porano = defaultdict(dict)  # (cod, año, grupo) -> {edición: valor}
    for td, (ed, anios) in TABLAS.items():
        for a in anios:
            for g in ("alimentacion", "general"):
                cods = {k[1] for k in lect if k[0] == td and k[2] == a and k[3] == g}
                assert len(cods) == 51 and "ES" in cods, f"{td} {a} {g}: {len(cods)} filas"
                for c in cods:
                    vals = {x["valor"] for x in lect[(td, c, a, g)]}
                    if (td, c, a, g) in RESUELTAS:
                        v = RESUELTAS[(td, c, a, g)][0]
                        assert v in vals, f"{td} {c} {a} {g}: la resolución no es ninguna de las lecturas"
                    else:
                        assert len(vals) == 1, f"{td} {c} {a} {g}: lecturas distintas {vals}"
                        v = vals.pop()
                    porano[(c, a, g)][ed] = (float(v), td, len(lect[(td, c, a, g)]))
    for (c, a, g), eds in porano.items():
        n = sum(x[2] for x in eds.values())
        assert n >= 2, f"{c} {a} {g}: una sola lectura"
        vs = {x[0] for x in eds.values()}
        if len(vs) > 1:
            assert (c, a, g) in REVISIONES, f"{c} {a} {g}: ediciones distintas {eds}"
    return porano


def main() -> None:
    porano = leer()
    usadas = set()
    for (c, a, g), eds in porano.items():
        usadas.add(max(eds, key=ORDEN.index))
    for ed in sorted(usadas, key=ORDEN.index):
        tds = [td for td, (e, _) in TABLAS.items() if e == ed]
        anios = sorted({a for td in tds for a in TABLAS[td][1]})
        (OUT / f"documents/doc-ine-anuario{ed}-coste-vida.json").write_text(json.dumps({
            "id": f"doc-ine-anuario{ed}-coste-vida",
            "title": f"Anuario Estadístico de España {ed}: índice del coste de la vida en las capitales, {anios[0]}-{anios[-1]}",
            "title_original": "Índice del coste de la vida en las capitales. Promedios mensuales, por capitales (Base: julio de 1936 = 100)",
            "document_type": "tabla_estadistica", "source_ids": ["F010"],
            "custodian": "Instituto Nacional de Estadística, INEbase Historia (fondo documental)",
            "signature": f"Anuario Estadístico de España {ed}, «Precios, salarios, racionamiento y consumo», coste de la vida en las capitales (td={', '.join(tds)})",
            "canonical_url": f"https://www.ine.es/inebaseweb/pdfDispacher.do?td={tds[0]}&ext=.pdf",
            "date": f"{anios[-1]}-12-31", "date_precision": "anio", "place_ids": ["plc-espana"],
            "summary": f"Índices del coste de la vida en cada capital de provincia y en el conjunto, por grupos (alimentación, vestido, vivienda, gastos de casa, gastos generales) e índice general, base julio de 1936 = 100, años {anios[0]} a {anios[-1]}.",
            "context": "Estadística oficial de la Dirección General de Estadística bajo el franquismo. " + NOTA_TABLA + " Son índices de precios de un presupuesto tipo: no miden la escasez, el racionamiento ni el mercado negro.",
            "text_origin": "transcripcion_validada",
            "rights": {"status": "cc_by", "action": "almacenar",
                       "attribution": f"Fuente: Instituto Nacional de Estadística (INE), INEbase Historia, Anuario Estadístico de España {ed}",
                       "evidence_url": "https://www.ine.es/ine/codigobp/politica_difusion_es.pdf", "checked_at": TODAY,
                       "note": "El INE aplica a la información de su web la licencia CC BY 4.0 salvo indicación contraria (Política de Difusión Estadística, febrero de 2026)."},
            "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                       "note": "Transcrita de la imagen del PDF; cada cifra leída al menos dos veces (dos ediciones o dos transcriptores independientes)."},
            "consulted_at": TODAY,
        }, ensure_ascii=False, indent=2) + "\n")
    base = {
        "unit": "índice, julio de 1936 = 100",
        "denominator": "nivel de precios de julio de 1936 en la misma capital",
        "method": "Promedio anual del índice publicado por el INE para la capital de cada provincia, tal como se imprime. Para cada año se usa la edición más reciente del Anuario que lo publica; cada cifra se leyó al menos dos veces (scripts/etl/ine_coste_vida_1939_1950.py).",
        "source_ids": ["F010"],
        "comparability_notes": "Mide la capital, no la provincia. " + NOTA_TABLA + " Es un índice de precios oficiales de un presupuesto tipo: no recoge el mercado negro (estraperlo), muy extendido en esos años, ni la escasez. " + NOTA_1939,
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Generado por scripts/etl/ine_coste_vida_1939_1950.py. Pendiente de segunda revisión humana."},
    }
    for g, concepto, defi in (("alimentacion", "Coste de la alimentación, 1939-1950", "Índice del coste de la alimentación en la capital de cada provincia, julio de 1936 = 100."),
                             ("general", "Coste de la vida, 1939-1950", "Índice general del coste de la vida en la capital de cada provincia, julio de 1936 = 100.")):
        obs = []
        for (c, a, gg), eds in sorted(porano.items()):
            if gg != g or c == "ES":
                continue
            ed = max(eds, key=ORDEN.index)
            v, td, _ = eds[ed]
            o = {"place_id": f"plc-prov-{c}", "period": a, "value": v, "document_id": f"doc-ine-anuario{ed}-coste-vida",
                 "locator": f"Anuario {ed}, coste de la vida por capitales, año {a} (td={td}), fila de la capital"}
            notas = [NOTA_1939] if a == "1939" else []
            if (c, a, g) in REVISIONES:
                notas.append(REVISIONES[(c, a, g)])
            notas += [m for (t, cc, aa, gg2), (_, m) in RESUELTAS.items() if (cc, aa, gg2) == (c, a, g) and t == td]
            if notas:
                o["uncertainty"] = " ".join(notas)
            obs.append(o)
        anios = sorted({a for (_, a, _) in porano})
        for pid, motivo in (("plc-prov-51", "Los Anuarios no publican índice de Ceuta."), ("plc-prov-52", "Los Anuarios no publican índice de Melilla.")):
            for a in anios:
                obs.append({"place_id": pid, "period": a, "value": None, "document_id": "doc-ine-anuario1951-coste-vida", "missingness_reason": motivo})
        (OUT / f"indicators/ind-coste-vida-{g}-prov.json").write_text(json.dumps({
            "id": f"ind-coste-vida-{g}-prov", "concept": concepto, "definition": defi, **base, "observations": obs},
            ensure_ascii=False, indent=2) + "\n")
    es = {(a, g): porano[("ES", a, g)][max(porano[("ES", a, g)], key=ORDEN.index)][0] for (c, a, g) in porano if c == "ES"}
    for a in sorted({a for a, _ in es}):
        print(a, "alimentación", es[(a, "alimentacion")], "general", es[(a, "general")])


if __name__ == "__main__":
    main()
