"""Series nacionales de la posguerra: salarios reales, coste de la vida medio y población reclusa (INE, Anuarios).

Entradas (transcritas de los Anuarios Estadísticos de España, INEbase Historia):
  data/external/ine_anuarios/salarios_reales_1939_1950.csv
      «Números índices de las remuneraciones reales, máxima y mínima, por jornada, que como cifra media
      nacional estimada corresponden a obreros de tipo profesional corriente, según los distintos grupos
      de actividad» (base año 1936 = 100), siete ediciones; todas las lecturas, con la columna `lector`.
  data/external/ine_anuarios/coste_vida_capitales_1939_1950.csv  (fila ESPAÑA: media ponderada de las capitales)
  data/external/ine_anuarios/poblacion_reclusa_1922_1950.csv     (Anuario 1950, td 29648)
  data/external/ine_anuarios/reclusos_situacion_1939_1950.csv    (Anuario 1950, td 29649, cuadro II)
  data/external/ine_anuarios/penados_no_comunes_1943_1950.csv    (Anuario 1950, td 29649, cuadro III)

Comprobaciones (fallan con AssertionError):
  1. Salarios: cada año, oficio, sexo y tipo tiene al menos dos lecturas y todas coinciden, salvo la
     columna de máximos de 1942 del Anuario de 1944-1945, que repite por error la de 1940 del Anuario de
     1943 (se usa la del Anuario de 1943).
  2. Reclusos: varones + mujeres = total; penados + procesados + detenidos = total; el total del cuadro II
     coincide con el del cuadro I. Una errata corregida (CORR_RECLUSOS).

Salidas: site/src/data/series_nacionales.json y los documentos doc-ine-anuarioAAAA-salarios-reales y
doc-ine-anuario1950-poblacion-reclusa.

Uso: python3 -I scripts/etl/ine_series_nacionales_posguerra.py   (después de ine_coste_vida_1939_1950.py)
"""
import csv
import json
import pathlib
from collections import defaultdict

ROOT = pathlib.Path(__file__).resolve().parents[2]
EXT = ROOT / "data/external/ine_anuarios"
OUT = ROOT / "data/canonical"
SITE = ROOT / "site/src/data/series_nacionales.json"
TODAY = "2026-11-15"
ORDEN = ["160638", "162168", "162870", "163594", "164743", "29958", "165648"]
ED = {"160638": "1943", "162168": "1944-1945", "162870": "1946-1947", "163594": "1948", "164743": "1949", "29958": "1950", "165648": "1951"}
ERRATA_1942 = "162168"  # sus máximos de 1942 repiten los de 1940 del Anuario de 1943
SERIES_SAL = [("Agrícolas", "Hombres"), ("Albañiles", "Hombres"), ("Metalúrgicos", "Hombres"), ("Textiles", "Mujeres"), ("Costureras y modistas", "Mujeres")]
CORR_RECLUSOS = {("1943-01-01", "procesados_h"): (613, 3613, "1 de enero de 1943, mujeres procesadas: la tabla imprime 613; el total de mujeres (11.688) y el de procesados (43.398) solo cuadran con 3.613.")}
NOTAS_ANIO = {
    "1939": "1939: promedio del segundo semestre (coste de la vida).",
    "1944": "1944 y 1945: sin las cifras del segundo semestre (nota de la tabla).",
    "1945": "1944 y 1945: sin las cifras del segundo semestre (nota de la tabla).",
    "1950": "1950: la columna del Anuario de 1951 repite casi exactamente la de 1948; se publica tal como está impresa.",
}


def doc(did, titulo, original, firma, td, fecha, resumen, contexto):
    (OUT / f"documents/{did}.json").write_text(json.dumps({
        "id": did, "title": titulo, "title_original": original, "document_type": "tabla_estadistica", "source_ids": ["F010"],
        "custodian": "Instituto Nacional de Estadística, INEbase Historia (fondo documental)", "signature": firma,
        "canonical_url": f"https://www.ine.es/inebaseweb/pdfDispacher.do?td={td}&ext=.pdf",
        "date": fecha, "date_precision": "anio", "place_ids": ["plc-espana"], "summary": resumen, "context": contexto,
        "text_origin": "transcripcion_validada",
        "rights": {"status": "cc_by", "action": "almacenar", "attribution": f"Fuente: Instituto Nacional de Estadística (INE), INEbase Historia, {firma.split(',')[0]}",
                   "evidence_url": "https://www.ine.es/ine/codigobp/politica_difusion_es.pdf", "checked_at": TODAY,
                   "note": "El INE aplica a la información de su web la licencia CC BY 4.0 salvo indicación contraria (Política de Difusión Estadística, febrero de 2026)."},
        "review": {"status": "revision", "date": TODAY, "by": ["autor"], "note": "Transcrita de la imagen del PDF con doble lectura o comprobación aritmética."},
        "consulted_at": TODAY}, ensure_ascii=False, indent=2) + "\n")


def salarios():
    lect = defaultdict(list)
    for r in csv.DictReader((EXT / "salarios_reales_1939_1950.csv").open(encoding="utf-8")):
        lect[(r["oficio"], r["sexo"], r["anio"], r["tipo"])].append(r)
    out = {}
    for k, rs in lect.items():
        validas = [r for r in rs if not (k[2] == "1942" and k[3] == "max" and r["td"] == ERRATA_1942)]
        assert len(validas) >= 2, f"{k}: {len(validas)} lecturas"
        vals = {r["valor"] for r in validas}
        assert len(vals) == 1, f"{k}: lecturas distintas {vals}"
        td = max((r["td"] for r in validas), key=ORDEN.index)
        out[k] = (int(vals.pop()), td)
    return out


def reclusos():
    I = {r["fecha"]: r for r in csv.DictReader((EXT / "poblacion_reclusa_1922_1950.csv").open(encoding="utf-8"))}
    for f, r in I.items():
        if r["varones"]:
            assert int(r["varones"]) + int(r["mujeres"]) == int(r["total"]), f
    for r in csv.DictReader((EXT / "reclusos_situacion_1939_1950.csv").open(encoding="utf-8")):
        g = lambda k: (CORR_RECLUSOS[(r["fecha"], k)][1] if (r["fecha"], k) in CORR_RECLUSOS else int(r[k])) if r[k] else None
        if (r["fecha"], "procesados_h") in CORR_RECLUSOS:
            assert int(r["procesados_h"]) == CORR_RECLUSOS[(r["fecha"], "procesados_h")][0]
        for p in ("penados", "procesados", "detenidos", "total"):
            if r[p + "_v"]:
                assert g(p + "_v") + g(p + "_h") == g(p), (r["fecha"], p)
        assert g("penados") + g("procesados") + g("detenidos") == g("total"), r["fecha"]
        assert g("total") == int(I[r["fecha"]]["total"]), r["fecha"]
    pnc = list(csv.DictReader((EXT / "penados_no_comunes_1943_1950.csv").open(encoding="utf-8")))
    for r in pnc:
        if r["varones"]:
            assert int(r["varones"]) + int(r["mujeres"]) == int(r["total"]), r["fecha"]
    return I, pnc


def main() -> None:
    sal = salarios()
    I, pnc = reclusos()
    coste = defaultdict(dict)
    for r in csv.DictReader((EXT / "coste_vida_capitales_1939_1950.csv").open(encoding="utf-8")):
        if r["cod"] == "ES":
            coste[r["grupo"]].setdefault(r["anio"], {})[r["anuario"]] = r["valor"]
    eds = ["1943", "1944-1945", "1946-1947", "1948", "1949", "1950", "1951"]
    for td in ORDEN:
        ed = ED[td]
        anios = sorted({k[2] for k, (_, t) in sal.items() if t == td} | {k[2] for k in [(0, 0, a, 0) for a in []]})
        doc(f"doc-ine-anuario{ed}-salarios-reales", f"Anuario Estadístico de España {ed}: índices de las remuneraciones reales por oficios",
            "Números índices de las remuneraciones reales, máxima y mínima, por jornada, que como cifra media nacional estimada corresponden a obreros de tipo profesional corriente, según los distintos grupos de actividad (Base: año 1936 = 100)",
            f"Anuario Estadístico de España {ed}, «Precios, salarios, racionamiento y consumo», Salarios (td={td})", td, f"{ed[-4:]}-12-31",
            "Índices nacionales estimados de la remuneración real máxima y mínima por jornada de los obreros de tipo profesional corriente, por oficio y sexo, base 1936 = 100.",
            "Estimación oficial: según la propia tabla, se obtiene relacionando los índices de salarios nominales con el índice del coste de la vida. Son salarios por jornada de convenio o tarifa, no ingresos anuales, y no incluyen el paro ni el estraperlo.")
    doc("doc-ine-anuario1950-poblacion-reclusa", "Anuario Estadístico de España 1950: población reclusa, 1922-1950",
        "Población reclusa. I. Existencia en 1.º de enero. Años 1922 a 1950; II. Reclusos en las fechas que se detallan; III. Penados por delitos no comunes, clasificados por el tiempo de sus condenas",
        "Anuario Estadístico de España 1950, «Justicia y culto», Población reclusa, págs. 939-940 (td=29648 y 29649)", "29648", "1950-12-31",
        "Reclusos existentes en las prisiones a 1 de enero de cada año (1922-1934 y 1939-1950), por sexo; reclusos penados, procesados y detenidos (1939-1950) y penados por «delitos no comunes» (1943-1950).",
        "Datos primarios de la Dirección General de Prisiones. La tabla no da cifras de 1935 a 1938. «Delitos no comunes» es la denominación de la fuente para los delitos políticos, sobre todo la «rebelión militar» juzgada por los tribunales franquistas. Los totales no incluyen los campos de concentración, los batallones de trabajadores ni las colonias penitenciarias militarizadas.")
    nota_sal = ("Índice nacional estimado por el INE de la remuneración real (salario por jornada dividido por el coste de la vida), máximo, base 1936 = 100. "
                "Por debajo de 100 un jornal compraba menos que en 1936.")
    series = []
    for oficio, sexo in SERIES_SAL:
        pts = []
        for a in sorted({k[2] for k in sal if k[0] == oficio and k[1] == sexo}):
            v, td = sal[(oficio, sexo, a, "max")]
            p = {"periodo": a, "valor": v, "documento": f"doc-ine-anuario{ED[td]}-salarios-reales", "td": td}
            if a in NOTAS_ANIO and a != "1939":
                p["nota"] = NOTAS_ANIO[a]
            if a == "1942":
                p["nota"] = "Se usa el Anuario de 1943: la columna de máximos de 1942 del Anuario de 1944-1945 repite por error la de 1940."
            pts.append(p)
        series.append({"id": "salario-real-" + {"Agrícolas": "agricolas", "Albañiles": "albaniles", "Metalúrgicos": "metalurgicos", "Textiles": "textiles", "Costureras y modistas": "costureras"}[oficio] + f"-{sexo.lower()}", "grupo": "salarios",
                       "titulo": f"{oficio} ({sexo.lower()})", "unidad": "índice, 1936 = 100", "nota": nota_sal, "puntos": pts})
    for g, t in (("alimentacion", "Alimentación"), ("general", "Índice general")):
        pts = []
        for a in sorted(coste[g]):
            ed = max(coste[g][a], key=eds.index)
            pts.append({"periodo": a, "valor": float(coste[g][a][ed]), "documento": f"doc-ine-anuario{ed}-coste-vida", **({"nota": NOTAS_ANIO["1939"]} if a == "1939" else {})})
        series.append({"id": f"coste-vida-{g}-espana", "grupo": "precios", "titulo": t, "unidad": "índice, julio de 1936 = 100",
                       "nota": "Media ponderada de las capitales de provincia publicada por el INE. Precios oficiales de un presupuesto tipo, sin estraperlo.", "puntos": pts})
    pts = []
    for f, r in sorted(I.items()):
        p = {"periodo": f[:4], "fecha": f, "valor": int(r["total"]), "documento": "doc-ine-anuario1950-poblacion-reclusa", "td": "29648"}
        if r["nota"]:
            p["nota"] = r["nota"]
        pts.append(p)
    series.append({"id": "poblacion-reclusa", "grupo": "prisiones", "titulo": "Reclusos a 1 de enero", "unidad": "personas",
                   "nota": "Reclusos en las prisiones a 1 de enero (en 1939, a 1 de abril). Sin datos de 1935 a 1938. No incluye campos de concentración, batallones de trabajadores ni colonias penitenciarias militarizadas.", "puntos": pts})
    series.append({"id": "penados-no-comunes", "grupo": "prisiones", "titulo": "Penados por «delitos no comunes»", "unidad": "personas",
                   "nota": "Denominación de la fuente para los delitos políticos, sobre todo la «rebelión militar»; el resto de presos lo eran por delitos comunes o estaban procesados o detenidos. En 1943, a 1 de julio.",
                   "puntos": [{"periodo": r["fecha"][:4], "fecha": r["fecha"], "valor": int(r["total"]), "documento": "doc-ine-anuario1950-poblacion-reclusa", "td": "29649",
                               **({"nota": r["nota"]} if r["nota"] else {})} for r in pnc]})
    SITE.write_text(json.dumps({"generado": TODAY, "series": series}, ensure_ascii=False, indent=1) + "\n")
    for s in series:
        print(s["id"], [(p["periodo"], p["valor"]) for p in s["puntos"]][:14])


if __name__ == "__main__":
    main()
