"""Racionamiento por provincias, 1943 y 1948-1950: kilos de aceite, azúcar y patatas por persona (INE, Anuarios).

Fuentes: Anuarios Estadísticos de España de 1944-1945 (año 1943), 1949, 1950 y 1951, sección «Precios, salarios, racionamiento
y consumo»:
  - «Distribución, mediante racionamiento, por provincias en el año …» (un artículo por página): kilos
    distribuidos a la población civil (régimen normal + economatos o colectividades) y a pequeñas industrias.
  - «Cartillas de racionamiento inscritas en tiendas, economatos … por provincias», a 31 de diciembre.

Entradas: data/external/ine_anuarios/racionamiento_provincias_1943_1950.csv y cartillas_provincias_1948_1950.csv

Cálculo: kilos distribuidos a la población civil en el año / cartillas inscritas a 31 de diciembre. En 1943
el Anuario no da cartillas por provincia y se divide por la población de hecho del censo de 1940. La
Subdelegación del Campo de Gibraltar, que las tablas dan aparte en 1948 y en el primer trimestre de 1949,
se suma a Cádiz (sus cartillas ya figuran en Cádiz).

Comprobaciones (fallan con AssertionError):
  1. Kilos: en cada fila régimen normal + economatos = total civil y total civil + industrias = total
     general; en cada columna, la suma de las filas = TOTAL impreso. Salvo erratas corregidas (CORRECCIONES)
     o anotadas sin efecto en el cálculo (ERRATAS_GENERAL, solo en total general).
  2. Cartillas: tiendas + colectivos + economatos = total por fila y suma de provincias = TOTAL por columna.

Salidas: data/canonical/documents/doc-ine-anuarioAAAA-racionamiento.json
         data/canonical/indicators/ind-racion-{aceite,azucar,patatas}-prov.json

Uso: python3 -I scripts/etl/ine_racionamiento_1943_1950.py
"""
import csv
import json
import pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
SRCK = ROOT / "data/external/ine_anuarios/racionamiento_provincias_1943_1950.csv"
SRCC = ROOT / "data/external/ine_anuarios/cartillas_provincias_1948_1950.csv"
TODAY = "2026-11-15"
ED = {"1943": ("1944-1945", "162173", None), "1948": ("1949", "164753", "164751"), "1949": ("1950", "29963", "29961"), "1950": ("1951", "165650", "165652")}
K = ["regimen_normal", "economatos", "total_civil", "industrias", "total_general"]
C = ["tiendas", "colectivos", "economatos", "total"]
# (año, artículo o «cartillas», cod, columna) -> (impreso, corregido, motivo)
CORRECCIONES = {
    ("1943", "aceite", "29", "total_civil"): (8402413, 8402314, "Málaga, aceite, 1943: la tabla imprime 8.402.413 kg para la población civil; régimen normal (7.957.712) + economatos (444.602), el total general y el total de la columna dan 8.402.314."),
    ("1950", "aceite", "01", "total_civil"): (883784, 833784, "Álava, aceite, 1950: la tabla imprime 883.784 kg para la población civil; régimen normal (727.711) + economatos (106.073) y el total de la columna dan 833.784."),
    ("1949", "cartillas", "21", "tiendas"): (552911, 352911, "Huelva, cartillas de 1949: la tabla imprime 552.911 en tiendas; el total de la fila (403.889) y el de la columna solo cuadran con 352.911."),
}
# Erratas en «total general» (no se usa en el cálculo): (año, artículo, cod) -> diferencia impreso − coherente
ERRATAS_GENERAL = {("1943", "aceite", "07"): 200, ("1950", "aceite", "07"): -1000, ("1950", "azucar", "22"): -3, ("1950", "patatas", "35"): -50}
ART = {"aceite": "aceite", "azucar": "azúcar", "patatas": "patatas"}
NOTA = ("Kilos distribuidos mediante racionamiento a la población civil (régimen normal más economatos y colectividades) "
        "divididos por las cartillas inscritas a 31 de diciembre. Mide lo que repartió oficialmente el racionamiento, "
        "no lo que se consumió: no incluye el mercado negro (estraperlo) ni el autoabastecimiento, y las raciones "
        "variaban por categorías de cartilla.")


def num(v):
    return int(str(v).replace(".", "").strip() or 0)


def leer():
    k = defaultdict(dict)
    for r in csv.DictReader(SRCK.open(encoding="utf-8")):
        v = {c: num(r[c]) for c in K}
        for c in K:
            corr = CORRECCIONES.get((r["anio"], r["articulo"], r["cod"], c))
            if corr:
                assert v[c] == corr[0], f"{r['anio']} {r['articulo']} {r['cod']} {c}: se esperaba {corr[0]}"
                v[c] = corr[1]
        k[(r["anio"], r["articulo"])][r["cod"]] = v
    c = defaultdict(dict)
    for r in csv.DictReader(SRCC.open(encoding="utf-8")):
        v = {x: num(r[x]) for x in C}
        for x in C:
            corr = CORRECCIONES.get((r["anio"], "cartillas", r["cod"], x))
            if corr:
                assert v[x] == corr[0]
                v[x] = corr[1]
        c[r["anio"]][r["cod"]] = v
    for (a, art), filas in k.items():
        provs = [x for x in filas if x != "TOT"]
        assert len([x for x in provs if x != "GIB"]) == 50, f"{a} {art}: {len(provs)} filas"
        for cod, v in filas.items():
            assert v["regimen_normal"] + v["economatos"] == v["total_civil"], f"{a} {art} {cod}: civil"
            assert v["total_civil"] + v["industrias"] - v["total_general"] == -ERRATAS_GENERAL.get((a, art, cod), 0), f"{a} {art} {cod}: general"
        for col in K:
            s = sum(filas[x][col] for x in provs)
            err = sum(ERRATAS_GENERAL.get((a, art, x), 0) for x in provs) if col == "total_general" else 0
            assert s == filas["TOT"][col] + err, f"{a} {art} {col}: suma {s} ≠ TOTAL {filas['TOT'][col]}"
    for a, filas in c.items():
        provs = [x for x in filas if x != "TOT"]
        assert len(provs) == 50, f"cartillas {a}"
        for cod, v in filas.items():
            assert v["tiendas"] + v["colectivos"] + v["economatos"] == v["total"], f"cartillas {a} {cod}"
        for col in C:
            assert sum(filas[x][col] for x in provs) == filas["TOT"][col], f"cartillas {a} {col}"
    return k, c


def poblacion_1940() -> dict:
    d = json.loads((OUT / "indicators/ind-pob-hecho-prov.json").read_text())
    return {o["place_id"][9:]: o["value"] for o in d["observations"] if o["period"] == "1940" and o["value"]}


def denom(c, pob, a, cod):
    return pob[cod] if a == "1943" else c[a][cod]["total"]


def main() -> None:
    k, c = leer()
    pob = poblacion_1940()
    for a, (ed, tdk, tdc) in ED.items():
        (OUT / f"documents/doc-ine-anuario{ed}-racionamiento.json").write_text(json.dumps({
            "id": f"doc-ine-anuario{ed}-racionamiento",
            "title": f"Anuario Estadístico de España {ed}: racionamiento por provincias en {a}" + ("" if tdc is None else " y cartillas a 31 de diciembre"),
            "title_original": (f"Resumen, por provincias, de las cantidades de artículos distribuidos mediante racionamiento a la población civil. Año {a}" if tdc is None else f"Distribución, mediante racionamiento, por provincias en el año {a}; Cartillas de racionamiento inscritas en tiendas, economatos y cooperativas, por provincias"),
            "document_type": "tabla_estadistica", "source_ids": ["F010"],
            "custodian": "Instituto Nacional de Estadística, INEbase Historia (fondo documental)",
            "signature": f"Anuario Estadístico de España {ed}, «Precios, salarios, racionamiento y consumo» (distribución td={tdk}" + ("" if tdc is None else f"; cartillas td={tdc}") + ")",
            "canonical_url": f"https://www.ine.es/inebaseweb/pdfDispacher.do?td={tdk}&ext=.pdf",
            "date": f"{a}-12-31", "date_precision": "anio", "place_ids": ["plc-espana"],
            "summary": f"Kilos de cada artículo distribuidos mediante racionamiento en {a} en cada provincia, a la población civil y a pequeñas industrias" + ("." if tdc is None else ", y número de cartillas de racionamiento inscritas por provincia a 31 de diciembre."),
            "context": "Estadística oficial de la Comisaría General de Abastecimientos y Transportes recogida por el INE bajo el franquismo. Registra el reparto oficial, no el consumo real: no incluye el mercado negro ni el autoabastecimiento.",
            "text_origin": "transcripcion_validada",
            "rights": {"status": "cc_by", "action": "almacenar",
                       "attribution": f"Fuente: Instituto Nacional de Estadística (INE), INEbase Historia, Anuario Estadístico de España {ed}",
                       "evidence_url": "https://www.ine.es/ine/codigobp/politica_difusion_es.pdf", "checked_at": TODAY,
                       "note": "El INE aplica a la información de su web la licencia CC BY 4.0 salvo indicación contraria (Política de Difusión Estadística, febrero de 2026)."},
            "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                       "note": "Transcrita de la imagen del PDF con cuadre por filas y por columnas contra los totales impresos."},
            "consulted_at": TODAY,
        }, ensure_ascii=False, indent=2) + "\n")
    for art, nom in ART.items():
        obs = []
        for a, (ed, tdk, tdc) in ED.items():
            filas = k[(a, art)]
            for cod in sorted(x for x in filas if x not in ("TOT", "GIB")):
                kg = filas[cod]["total_civil"] + (filas["GIB"]["total_civil"] if cod == "11" and "GIB" in filas else 0)
                if a == "1943" and art == "aceite" and cod == "14":
                    obs.append({"place_id": "plc-prov-14", "period": a, "value": None, "document_id": f"doc-ine-anuario{ed}-racionamiento",
                                "missingness_reason": "La tabla de 1943 solo trae el aceite de Córdoba de agosto a diciembre (nota (2) de la tabla)."})
                    continue
                o = {"place_id": f"plc-prov-{cod}", "period": a, "value": round(kg / denom(c, pob, a, cod), 1),
                     "document_id": f"doc-ine-anuario{ed}-racionamiento",
                     "locator": (f"Anuario {ed}: «{nom}», total de población civil (td={tdk}); población de hecho del censo de 1940" if a == "1943"
                                 else f"Anuario {ed}: «{nom}», total de población civil (td={tdk}); cartillas inscritas a 31-12-{a}, total (td={tdc})")}
                notas = [m for (aa, ar, cc, _), (_, _, m) in CORRECCIONES.items() if aa == a and cc == cod and ar in (art, "cartillas")]
                if cod == "11" and "GIB" in filas:
                    notas.append("Incluye la Subdelegación del Campo de Gibraltar, que la tabla da aparte" + (" (solo el primer trimestre: después sus municipios pasaron a Cádiz y Málaga)." if a == "1949" else "."))
                if kg == 0:
                    notas.append(f"La tabla trae raya: ese año no se repartieron {nom} mediante racionamiento en la provincia.")
                if a == "1943":
                    notas.append("En 1943 se divide por la población de hecho del censo de 1940, porque el Anuario no da cartillas por provincia.")
                if notas:
                    o["uncertainty"] = " ".join(notas)
                obs.append(o)
            for pid in ("plc-prov-51", "plc-prov-52"):
                obs.append({"place_id": pid, "period": a, "value": None, "document_id": f"doc-ine-anuario{ed}-racionamiento",
                            "missingness_reason": "Las tablas de racionamiento del Anuario no incluyen Ceuta ni Melilla."})
        (OUT / f"indicators/ind-racion-{art}-prov.json").write_text(json.dumps({
            "id": f"ind-racion-{art}-prov", "concept": f"Racionamiento de {nom}, 1943 y 1948-1950",
            "definition": f"Kilos de {nom} repartidos mediante racionamiento a la población civil de cada provincia en el año, por cartilla de racionamiento inscrita (en 1943, por habitante del censo de 1940).",
            "unit": "kg por cartilla y año (1943: por habitante)", "denominator": "cartillas de racionamiento inscritas a 31 de diciembre; en 1943, población de hecho del censo de 1940",
            "method": NOTA + " Tablas transcritas con cuadre por filas y columnas (scripts/etl/ine_racionamiento_1943_1950.py).",
            "source_ids": ["F010"],
            "comparability_notes": NOTA + " Las cartillas cubrían a casi toda la población (28,9 millones en 1948)." + (" Las patatas se racionaban sobre todo en las provincias no productoras, y en 1950 dejaron de repartirse en muchas: las diferencias entre provincias reflejan la producción local más que el hambre." if art == "patatas" else "") + " En 1943 el Anuario no da cartillas por provincia y se usa la población de hecho del censo de 1940; las cartillas de 1948 superaban en un 3 % a la población, así que la comparación entre 1943 y 1948 es aproximada. 1944-1947 no se publican por provincias en los Anuarios consultados.",
            "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                       "note": "Generado por scripts/etl/ine_racionamiento_1943_1950.py. Pendiente de segunda revisión humana."},
            "observations": obs}, ensure_ascii=False, indent=2) + "\n")
    for a in ED:
        tot = sum(pob.values()) if a == "1943" else c[a]["TOT"]["total"]
        print(a, "denominador", tot, {art: round(k[(a, art)]["TOT"]["total_civil"] / tot, 1) for art in ART})


if __name__ == "__main__":
    main()
