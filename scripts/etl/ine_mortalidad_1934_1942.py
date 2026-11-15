"""Defunciones y mortalidad por provincia, 1934-1942 (INE, Anuario Estadístico de España 1943).

Entrada, transcrita a mano de las tablas «Movimiento natural de la población, por provincias.
Año AAAA» del Anuario de 1943 (un PDF por año en INEbase Historia):
  data/external/ine_anuario1943/mnp_provincias_1934_1942.csv
  (anio, td, prov_impresa, cod_prov, nacidos, fall_v, fall_h, fall_t, tasa_t, diferencia, nota);
  la fila de la nación lleva cod_prov = «TOTAL».

Comprobaciones de cada año (fallan con AssertionError):
  1. Las 50 provincias y la fila TOTAL, una vez cada una.
  2. En cada fila, fallecidos varones + mujeres = total, y nacidos − fallecidos = diferencia impresa.
  3. La suma de las 50 provincias reproduce la fila TOTAL en todas las columnas absolutas.
  4. La población implícita (fallecidos × 1000 / tasa) está entre 0,8 y 1,25 veces la de hecho
     interpolada entre los censos de 1930 y 1940: detecta tasas o fallecidos mal leídos.

Salidas: data/canonical/documents/doc-ine-anuario1943-mnp.json
         data/canonical/indicators/ind-mortalidad-prov.json      (tasa oficial, por 1.000 habitantes)
         data/canonical/indicators/ind-sobremortalidad-prov.json (defunciones, media 1934-1935 = 100)

Uso: python3 -I scripts/etl/ine_mortalidad_1934_1942.py
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
SRC = ROOT / "data/external/ine_anuario1943/mnp_provincias_1934_1942.csv"
TODAY = "2026-11-15"
DID = "doc-ine-anuario1943-mnp"
ANIOS = [str(y) for y in range(1934, 1943)]
BASE = ("1934", "1935")
COLS = ("nacidos", "fall_v", "fall_h", "fall_t", "diferencia")
# Notas al pie y cautelas de cada año, copiadas de las tablas (se completan con la transcripción).
NOTAS_ANIO = {
    "1936": "El escaneo de la tabla de 1936 está muy dañado: varios dígitos se han fijado con la aritmética de la propia fila (varones + mujeres = total; nacidos − fallecidos = diferencia) y siempre de forma compatible con la imagen; detalle en data/external/ine_anuario1943/notas_transcripcion_1936.txt.",
    "1939": "Cifras provisionales según la fuente.",
    "1940": "Cifras provisionales según la fuente.",
    "1941": "Cifras provisionales según la fuente.",
    "1942": "Cifras provisionales según la fuente.",
}
# Total nacional impreso con errata: suma de provincias − total impreso, por columna.
ERRATA_TOTAL = {("1942", "fall_v"): -68, ("1942", "fall_h"): 68}
# Tasas calculadas por el INE sobre una población muy distinta de la censal (comprobado con la natalidad impresa).
POB_DISTINTA = {("11", "1938"), ("11", "1939"), ("11", "1940")}
NOTA_POB = {"11": "Para Cádiz, de 1938 a 1940 el Anuario calcula las tasas sobre unos 475.000 habitantes, menos que los 600.440 de hecho del censo de 1940; las tasas de nacidos y fallecidos impresas dan la misma base."}


def leer() -> dict:
    data: dict = {}
    for r in csv.DictReader(SRC.open(encoding="utf-8")):
        d = data.setdefault(r["anio"], {"td": r["td"], "filas": {}})
        assert r["cod_prov"] not in d["filas"], f"{r['anio']} {r['cod_prov']} repetida"
        v = {k: int(r[k]) for k in COLS}
        v["tasa_t"] = float(r["tasa_t"])
        v["nota"] = r["nota"]
        assert v["fall_v"] + v["fall_h"] == v["fall_t"], f"{r['anio']} {r['prov_impresa']}: V+H != T"
        assert v["nacidos"] - v["fall_t"] == v["diferencia"], f"{r['anio']} {r['prov_impresa']}: nacidos − fallecidos != diferencia"
        d["filas"][r["cod_prov"]] = v
    hecho = json.loads((OUT / "indicators/ind-pob-hecho-prov.json").read_text())
    pob = {(o["place_id"][-2:], o["period"]): o["value"] for o in hecho["observations"]}
    assert sorted(data) == ANIOS, f"años: {sorted(data)}"
    for y, d in data.items():
        provs = {c: v for c, v in d["filas"].items() if c != "TOTAL"}
        assert len(provs) == 50 and "TOTAL" in d["filas"], f"{y}: {len(provs)} provincias"
        for k in COLS:
            s = sum(v[k] for v in provs.values())
            assert s - d["filas"]["TOTAL"][k] == ERRATA_TOTAL.get((y, k), 0), f"{y}: suma de {k} {s} frente a TOTAL {d['filas']['TOTAL'][k]}"
        for c, v in provs.items():
            ref = pob[(c, "1930")] + (pob[(c, "1940")] - pob[(c, "1930")]) * (int(y) - 1930) / 10  # interpolación lineal
            imp = v["fall_t"] * 1000 / v["tasa_t"]
            if (c, y) not in POB_DISTINTA:
                assert 0.8 <= imp / ref <= 1.25, f"{y} {c}: población implícita {imp:.0f} frente a {ref}"
    return data


def documento(data: dict) -> None:
    tds = ", ".join(f"{y}: td={data[y]['td']}" for y in ANIOS)
    (OUT / f"documents/{DID}.json").write_text(json.dumps({
        "id": DID,
        "title": "Anuario Estadístico de España 1943: movimiento natural de la población por provincias, años 1934 a 1942",
        "title_original": "Movimiento natural de la población, por provincias. Años 1934 a 1942",
        "document_type": "tabla_estadistica", "source_ids": ["F010"],
        "custodian": "Instituto Nacional de Estadística, INEbase Historia (fondo documental)",
        "signature": f"Anuario Estadístico de España 1943, Demografía, «Movimiento de la población»: una tabla por año ({tds})",
        "canonical_url": "https://www.ine.es/inebaseweb/treeNavigation.do?tn=161311",
        "date": "1943-12-31", "date_precision": "anio", "place_ids": ["plc-espana"],
        "summary": "Tablas oficiales con los matrimonios, los nacidos vivos y los fallecidos de cada provincia, en cifras absolutas y por 1.000 habitantes, para cada año de 1934 a 1942.",
        "context": "Cifras de los registros civiles recopiladas por el Instituto Nacional de Estadística. Los fallecidos excluyen a los nacidos muertos y a los muertos antes de las primeras veinticuatro horas. Durante la guerra el registro fue incompleto y muchas muertes se inscribieron tarde o nunca; las cifras de 1939 en adelante se publican como provisionales.",
        "text_origin": "transcripcion_validada",
        "rights": {"status": "cc_by", "action": "almacenar",
                   "attribution": "Fuente: Instituto Nacional de Estadística (INE), INEbase Historia, Anuario Estadístico de España 1943",
                   "evidence_url": "https://www.ine.es/ine/codigobp/politica_difusion_es.pdf", "checked_at": TODAY,
                   "note": "El INE aplica a la información de su web la licencia CC BY 4.0 salvo indicación contraria (Política de Difusión Estadística, febrero de 2026)."},
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Transcritas a mano las defunciones, los nacidos, la tasa y la diferencia de las 50 provincias y la nación para nueve años; cada fila cuadra por sexo y con la diferencia impresa, y la suma de provincias reproduce la fila de la nación."},
        "consulted_at": TODAY,
    }, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    data = leer()
    documento(data)
    rev = {"status": "revision", "date": TODAY, "by": ["autor"],
           "note": "Generado por scripts/etl/ine_mortalidad_1934_1942.py desde la transcripción comprobada. Pendiente de segunda revisión humana."}
    cautela = ("Los años de guerra (1936-1938) recogen solo las defunciones inscritas en el Registro Civil: faltan muchas muertes en el frente, en bombardeos y por violencia, y la inscripción en cada zona fue desigual. "
               "Las cifras de 1939 a 1942 son provisionales en la fuente. Las tasas usan la población que estimó entonces el INE.")
    obs_t, obs_i = [], []
    for y in ANIOS:
        for c, v in sorted(data[y]["filas"].items()):
            if c == "TOTAL":
                continue
            loc = f"Anuario 1943, tabla del año {y} (td={data[y]['td']}), fila de la provincia, fallecidos"
            o = {"place_id": f"plc-prov-{c}", "period": y, "value": v["tasa_t"], "document_id": DID, "locator": loc + ", «por 1.000 habitantes, en total»"}
            notas = [NOTAS_ANIO.get(y, ""), v["nota"], NOTA_POB.get(c, "") if (c, y) in POB_DISTINTA else ""]
            if any(notas):
                o["uncertainty"] = " ".join(x for x in notas if x)
            obs_t.append(o)
            base = sum(data[b]["filas"][c]["fall_t"] for b in BASE) / len(BASE)
            oi = {"place_id": f"plc-prov-{c}", "period": y, "value": round(100 * v["fall_t"] / base, 1), "document_id": DID, "locator": loc + ", cifra absoluta en total, frente a la media de 1934 y 1935"}
            notas_i = [NOTAS_ANIO.get(y, ""), v["nota"]]
            if any(notas_i):
                oi["uncertainty"] = " ".join(x for x in notas_i if x)
            obs_i.append(oi)
    for pid in ("plc-prov-51", "plc-prov-52"):
        for y in ANIOS:
            for lst in (obs_t, obs_i):
                lst.append({"place_id": pid, "period": y, "value": None, "document_id": DID, "missingness_reason": "Las tablas provinciales del Anuario no incluyen las posesiones del norte y costa occidental de África."})
    (OUT / "indicators/ind-mortalidad-prov.json").write_text(json.dumps({
        "id": "ind-mortalidad-prov", "concept": "Mortalidad, 1934-1942",
        "definition": "Fallecidos de cada provincia y año por 1.000 habitantes, según la tasa publicada por el INE.",
        "unit": "fallecidos por 1.000 habitantes", "denominator": "población estimada por el INE para cada año",
        "method": "Tasa tal como la publica el Anuario Estadístico de 1943; transcrita a mano y comprobada contra los fallecidos y la población interpolada entre los censos de 1930 y 1940 (scripts/etl/ine_mortalidad_1934_1942.py).",
        "source_ids": ["F010"], "comparability_notes": cautela, "review": rev, "observations": obs_t}, ensure_ascii=False, indent=2) + "\n")
    (OUT / "indicators/ind-sobremortalidad-prov.json").write_text(json.dumps({
        "id": "ind-sobremortalidad-prov", "concept": "Defunciones frente a 1934-1935",
        "definition": "Fallecidos inscritos en cada provincia y año, en porcentaje de la media de 1934 y 1935 (100 = igual que antes de la guerra).",
        "unit": "índice, media 1934-1935 = 100", "denominator": "media de los fallecidos de 1934 y 1935 en la misma provincia",
        "method": "Fallecidos del año / media de los fallecidos de 1934 y 1935 × 100, con las cifras absolutas del Anuario de 1943 (scripts/etl/ine_mortalidad_1934_1942.py). No corrige por cambios de población.",
        "source_ids": ["F010"],
        "comparability_notes": cautela + " El índice no descuenta la variación de la población ni sus desplazamientos: una provincia que recibió refugiados o tropas puede subir sin que empeorase la salud de sus vecinos.",
        "review": rev, "observations": obs_i}, ensure_ascii=False, indent=2) + "\n")
    t = {y: data[y]["filas"]["TOTAL"] for y in ANIOS}
    base = sum(t[b]["fall_t"] for b in BASE) / 2
    print("España, fallecidos e índice (1934-35 = 100):", ", ".join(f"{y}: {t[y]['fall_t']} ({100 * t[y]['fall_t'] / base:.0f})" for y in ANIOS))


if __name__ == "__main__":
    main()
