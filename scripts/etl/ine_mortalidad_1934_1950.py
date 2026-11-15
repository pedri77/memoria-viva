"""Defunciones, mortalidad y mortalidad infantil por provincia, 1934-1950 (INE, Anuarios Estadísticos).

Entradas, transcritas a mano de las tablas de los Anuarios Estadísticos de España (INEbase Historia):
  data/external/ine_anuario1943/mnp_provincias_1934_1942.csv
      Anuario de 1943, «Movimiento natural de la población, por provincias», 1934-1942
      (las cifras de 1939-1942 son provisionales en esa edición).
  data/external/ine_anuarios/mnp_provincias_1939_1950.csv
      la misma tabla en ediciones posteriores: la última edición que publica cada año.
  data/external/ine_anuarios/mortalidad_infantil_provincias_1933_1946.csv
      «Mortalidad infantil, por provincias»: fallecidos de menos de 1 año y de menos de 5.

Para cada año se usa la edición más reciente; la del Anuario de 1943 sirve de contraste.

Comprobaciones (fallan con AssertionError):
  1. Cada año tiene las 50 provincias y la fila de totales.
  2. En cada fila, varones + mujeres = total (nacidos y fallecidos) y nacidos − fallecidos = diferencia.
  3. La suma de provincias reproduce la fila de totales, salvo erratas del total documentadas.
  4. Si hay tasa impresa, la población implícita es coherente con la de los censos de 1930 y 1940.
  5. Mortalidad infantil: menores de 1 año ≤ menores de 5; las sumas reproducen el total; el
     «por 100 defunciones» impreso coincide con los fallecidos de la misma edición (±0,06).
  6. Las cifras definitivas de 1939-1942 no se apartan más de un 10 % de las provisionales; las revisiones de más del 1 % se publican como nota en el dato.

Salidas: un documento por edición (doc-ine-anuarioAAAA-mnp) e indicadores
  ind-mortalidad-prov (tasa oficial), ind-sobremortalidad-prov (media 1934-1935 = 100),
  ind-mortalidad-infantil-prov (menores de 1 año por 1.000 nacidos vivos).

Uso: python3 -I scripts/etl/ine_mortalidad_1934_1950.py
"""
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
SRC43 = ROOT / "data/external/ine_anuario1943/mnp_provincias_1934_1942.csv"
SRCN = ROOT / "data/external/ine_anuarios/mnp_provincias_1939_1950.csv"
SRCI = ROOT / "data/external/ine_anuarios/mortalidad_infantil_provincias_1933_1946.csv"
TODAY = "2026-11-15"
BASE = ("1934", "1935")
ABS = ("nacidos", "fall_v", "fall_h", "fall_t", "diferencia")
ARBOL = {"1943": "161311", "1944-1945": "161457", "1946-1947": "163148", "1948": "163298", "1949": "164782", "1950": "30270", "1951": "166448"}
NOTAS_ANIO = {
    "1936": "El escaneo de la tabla de 1936 está muy dañado: varios dígitos se han fijado con la aritmética de la propia fila (varones + mujeres = total; nacidos − fallecidos = diferencia) y siempre de forma compatible con la imagen; detalle en data/external/ine_anuario1943/notas_transcripcion_1936.txt.",
}
NOTAS_INF = {
    "1943": "En la tabla de mortalidad infantil de 1943 la suma de los menores de un año solo cuadró con el total impreso tras fijar cuatro dígitos dañados del escaneo (Ávila, Guadalajara, Logroño y Tarragona); detalle en data/external/ine_anuarios/notas_transcripcion_inf_1943.txt.",
}
ERRATA_TOTAL = {("1943", "1942", "fall_v"): -68, ("1943", "1942", "fall_h"): 68}  # (anuario, año, columna): suma de provincias − total impreso
POB_DISTINTA = {("11", str(y)) for y in range(1938, 1944)}
NOTA_POB = {"11": "Para Cádiz, el Anuario calcula las tasas de estos años sobre unos 475.000 habitantes, menos que los 600.440 de hecho del censo de 1940; las tasas de nacidos y fallecidos impresas dan la misma base."}
SIN_AFRICA = "Las tablas provinciales del Anuario no incluyen las posesiones del norte y costa occidental de África."
doc_id = lambda anuario: f"doc-ine-anuario{anuario}-mnp"


def num(r, k):
    return int(r[k]) if r.get(k, "").strip() else None


def leer_mnp(path, anuario_fijo=None) -> dict:
    out: dict = {}
    for r in csv.DictReader(path.open(encoding="utf-8")):
        an = anuario_fijo or r["anuario"]
        d = out.setdefault(r["anio"], {"td": r["td"], "anuario": an, "filas": {}})
        v = {k: num(r, k) for k in ABS + ("nacidos_v", "nacidos_h")}
        v["tasa_t"] = float(r["tasa_t"]) if r.get("tasa_t", "").strip() else None
        v["nota"] = r.get("nota", "")
        assert r["cod_prov"] not in d["filas"], f"{r['anio']} {r['cod_prov']} repetida"
        assert v["fall_v"] + v["fall_h"] == v["fall_t"], f"{r['anio']} {r['prov_impresa']}: fallecidos V+H != T"
        if v["nacidos_v"] is not None:
            assert v["nacidos_v"] + v["nacidos_h"] == v["nacidos"], f"{r['anio']} {r['prov_impresa']}: nacidos V+H != T"
        assert v["nacidos"] - v["fall_t"] == v["diferencia"], f"{r['anio']} {r['prov_impresa']}: nacidos − fallecidos != diferencia"
        d["filas"][r["cod_prov"]] = v
    return out


def comprobar(data: dict, pob: dict) -> None:
    for y, d in data.items():
        provs = {c: v for c, v in d["filas"].items() if c != "TOTAL"}
        assert len(provs) == 50 and "TOTAL" in d["filas"], f"{y}: {len(provs)} provincias"
        for k in ABS:
            s = sum(v[k] for v in provs.values())
            assert s - d["filas"]["TOTAL"][k] == ERRATA_TOTAL.get((d["anuario"], y, k), 0), f"{d['anuario']} {y}: suma de {k} {s} frente a {d['filas']['TOTAL'][k]}"
        for c, v in provs.items():
            if v["tasa_t"] and (c, y) not in POB_DISTINTA:
                a, b = pob[(c, "1930")], pob[(c, "1940")]
                ref = a + (b - a) * (int(y) - 1930) / 10 if int(y) <= 1940 else b
                assert 0.75 <= v["fall_t"] * 1000 / v["tasa_t"] / ref <= 1.3, f"{y} {c}: tasa incoherente con la población"


def leer_inf(data: dict) -> dict:
    inf: dict = {}
    for r in csv.DictReader(SRCI.open(encoding="utf-8")):
        d = inf.setdefault(r["anio"], {"td": r["td"], "anuario": r["anuario"], "filas": {}})
        v = {"m1": int(r["m1"]), "m5": int(r["m5"]), "p100_m1": float(r["p100_m1"]) if r["p100_m1"].strip() else None}
        assert v["m1"] <= v["m5"], f"inf {r['anio']} {r['cod_prov']}: m1 > m5"
        d["filas"][r["cod_prov"]] = v
    for y, d in inf.items():
        provs = {c: v for c, v in d["filas"].items() if c != "TOTAL"}
        assert len(provs) == 50 and "TOTAL" in d["filas"], f"inf {y}: {len(provs)} provincias"
        for k in ("m1", "m5"):
            assert sum(v[k] for v in provs.values()) == d["filas"]["TOTAL"][k], f"inf {y}: suma de {k}"
        if y in data and data[y]["anuario"] == d["anuario"]:
            for c, v in d["filas"].items():
                if v["p100_m1"] is not None:
                    calc = 100 * v["m1"] / data[y]["filas"][c]["fall_t"]
                    assert abs(calc - v["p100_m1"]) <= 0.06, f"inf {y} {c}: por 100 defunciones {v['p100_m1']} frente a {calc:.2f}"
    return inf


def documento(anuario: str, data: dict, inf: dict) -> None:
    mnp = sorted(y for y, d in data.items() if d["anuario"] == anuario)
    mi = sorted(y for y, d in inf.items() if d["anuario"] == anuario)
    partes = ([f"movimiento natural de la población por provincias ({', '.join(mnp)})"] if mnp else []) + ([f"mortalidad infantil por provincias ({', '.join(mi)})"] if mi else [])
    tds = "; ".join([f"movimiento natural {y}: td={data[y]['td']}" for y in mnp] + [f"mortalidad infantil {y}: td={inf[y]['td']}" for y in mi])
    (OUT / f"documents/{doc_id(anuario)}.json").write_text(json.dumps({
        "id": doc_id(anuario),
        "title": f"Anuario Estadístico de España {anuario}: {' y '.join(partes)}",
        "title_original": "Movimiento natural de la población, por provincias" + ("; Mortalidad infantil, por provincias" if mi else ""),
        "document_type": "tabla_estadistica", "source_ids": ["F010"],
        "custodian": "Instituto Nacional de Estadística, INEbase Historia (fondo documental)",
        "signature": f"Anuario Estadístico de España {anuario}, Demografía, «Movimiento de la población» ({tds})",
        "canonical_url": f"https://www.ine.es/inebaseweb/treeNavigation.do?tn={ARBOL[anuario]}",
        "date": f"{anuario[-4:]}-12-31", "date_precision": "anio", "place_ids": ["plc-espana"],
        "summary": "Tablas oficiales con los nacidos vivos y los fallecidos de cada provincia y año, por sexo, y su diferencia"
                   + ("; y con los fallecidos de menos de un año y de menos de cinco." if mi else "."),
        "context": "Cifras de los registros civiles recopiladas por el Instituto Nacional de Estadística. Los fallecidos excluyen a los nacidos muertos y a los muertos antes de las primeras veinticuatro horas. Cada edición del Anuario puede revisar las cifras provisionales de las anteriores.",
        "text_origin": "transcripcion_validada",
        "rights": {"status": "cc_by", "action": "almacenar",
                   "attribution": f"Fuente: Instituto Nacional de Estadística (INE), INEbase Historia, Anuario Estadístico de España {anuario}",
                   "evidence_url": "https://www.ine.es/ine/codigobp/politica_difusion_es.pdf", "checked_at": TODAY,
                   "note": "El INE aplica a la información de su web la licencia CC BY 4.0 salvo indicación contraria (Política de Difusión Estadística, febrero de 2026)."},
        "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                   "note": "Transcritas a mano; cada fila cuadra por sexo y con la diferencia impresa, y la suma de provincias reproduce la fila de totales."},
        "consulted_at": TODAY,
    }, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    hecho = json.loads((OUT / "indicators/ind-pob-hecho-prov.json").read_text())
    pob = {(o["place_id"][-2:], o["period"]): o["value"] for o in hecho["observations"]}
    a43 = leer_mnp(SRC43, "1943")
    nuevo = leer_mnp(SRCN)
    comprobar(a43, pob)
    comprobar(nuevo, pob)
    for y in sorted(set(a43) & set(nuevo)):  # provisional (1943) frente a definitiva
        for c, v in nuevo[y]["filas"].items():
            p = a43[y]["filas"][c]["fall_t"]
            assert abs(v["fall_t"] - p) <= 0.10 * p, f"{y} {c}: definitiva {v['fall_t']} frente a provisional {p}"
            if c != "TOTAL" and abs(v["fall_t"] - p) > 0.01 * p:
                v["nota"] = (v["nota"] + " " if v["nota"] else "") + f"El Anuario {nuevo[y]['anuario']} revisa los fallecidos de este año: {v['fall_t']:,} frente a {p:,} provisionales en el de 1943 ({100 * (v['fall_t'] - p) / p:+.1f} %).".replace(",", ".")
    data = {**a43, **nuevo}  # la edición posterior prevalece
    inf = leer_inf(data)
    for an in sorted({d["anuario"] for d in data.values()} | {d["anuario"] for d in inf.values()}):
        documento(an, data, inf)
    rev = {"status": "revision", "date": TODAY, "by": ["autor"],
           "note": "Generado por scripts/etl/ine_mortalidad_1934_1950.py desde las transcripciones comprobadas. Pendiente de segunda revisión humana."}
    cautela = ("Los años de guerra (1936-1938) recogen solo las defunciones inscritas en el Registro Civil: faltan muchas muertes en el frente, en bombardeos y por violencia, y la inscripción en cada zona fue desigual. "
               "Para cada año se usa la última edición del Anuario que lo publica; las de 1939 a 1942 sustituyen a las cifras provisionales del Anuario de 1943.")
    anios = sorted(data)
    obs_t, obs_i, obs_inf = [], [], []
    for y in anios:
        d = data[y]
        for c, v in sorted(d["filas"].items()):
            if c == "TOTAL":
                continue
            loc = f"Anuario {d['anuario']}, tabla del año {y} (td={d['td']}), fila de la provincia"
            notas = [NOTAS_ANIO.get(y, "") if d["anuario"] == "1943" else "", v["nota"]]
            if v["tasa_t"] is not None:
                o = {"place_id": f"plc-prov-{c}", "period": y, "value": v["tasa_t"], "document_id": doc_id(d["anuario"]), "locator": loc + ", fallecidos por 1.000 habitantes, en total"}
                nt = notas + [NOTA_POB[c] if (c, y) in POB_DISTINTA else ""]
                if any(nt):
                    o["uncertainty"] = " ".join(x for x in nt if x)
                obs_t.append(o)
            base = sum(a43[b]["filas"][c]["fall_t"] for b in BASE) / len(BASE)
            oi = {"place_id": f"plc-prov-{c}", "period": y, "value": round(100 * v["fall_t"] / base, 1), "document_id": doc_id(d["anuario"]),
                  "locator": loc + ", fallecidos en total, frente a la media de 1934 y 1935 del Anuario de 1943"}
            if any(notas):
                oi["uncertainty"] = " ".join(x for x in notas if x)
            obs_i.append(oi)
        con_tasa = any(v["tasa_t"] is not None for v in d["filas"].values())
        for pid in ("plc-prov-51", "plc-prov-52"):
            obs_i.append({"place_id": pid, "period": y, "value": None, "document_id": doc_id(d["anuario"]), "missingness_reason": SIN_AFRICA})
            if con_tasa:
                obs_t.append({"place_id": pid, "period": y, "value": None, "document_id": doc_id(d["anuario"]), "missingness_reason": SIN_AFRICA})
    for y in sorted(inf):
        if y not in data:
            continue  # sin nacidos de ese año no se puede calcular la tasa
        d, m = data[y], inf[y]
        for c, v in sorted(m["filas"].items()):
            if c == "TOTAL":
                continue
            obs_inf.append({"place_id": f"plc-prov-{c}", "period": y, "value": round(1000 * v["m1"] / d["filas"][c]["nacidos"], 1),
                            "document_id": doc_id(m["anuario"]),
                            "locator": f"Anuario {m['anuario']}, «Mortalidad infantil, por provincias», año {y} (td={m['td']}), fallecidos de menos de un año; nacidos vivos de la tabla del movimiento natural del Anuario {d['anuario']} (td={d['td']})", **({"uncertainty": NOTAS_INF[y]} if y in NOTAS_INF else {})})
        for pid in ("plc-prov-51", "plc-prov-52"):
            obs_inf.append({"place_id": pid, "period": y, "value": None, "document_id": doc_id(m["anuario"]), "missingness_reason": SIN_AFRICA})

    def ind(iid, concepto, definicion, unidad, denom, metodo, notas, obs):
        (OUT / f"indicators/{iid}.json").write_text(json.dumps({
            "id": iid, "concept": concepto, "definition": definicion, "unit": unidad, "denominator": denom, "method": metodo,
            "source_ids": ["F010"], "comparability_notes": notas, "review": rev, "observations": obs}, ensure_ascii=False, indent=2) + "\n")

    t_anios = sorted({o["period"] for o in obs_t})
    ind("ind-mortalidad-prov", f"Mortalidad, {t_anios[0]}-{t_anios[-1]}",
        "Fallecidos de cada provincia y año por 1.000 habitantes, según la tasa publicada por el INE.",
        "fallecidos por 1.000 habitantes", "población estimada por el INE para cada año",
        "Tasa tal como la publica el Anuario; solo existe en las ediciones que la imprimen. Transcrita a mano y comprobada contra los fallecidos y la población de los censos (scripts/etl/ine_mortalidad_1934_1950.py).",
        cautela + " Las tasas usan la población que estimó entonces el INE.", obs_t)
    ind("ind-sobremortalidad-prov", f"Defunciones frente a 1934-1935 ({anios[0]}-{anios[-1]})",
        "Fallecidos inscritos en cada provincia y año, en porcentaje de la media de 1934 y 1935 (100 = igual que antes de la guerra).",
        "índice, media 1934-1935 = 100", "media de los fallecidos de 1934 y 1935 en la misma provincia",
        "Fallecidos del año / media de los fallecidos de 1934 y 1935 × 100, con cifras absolutas (scripts/etl/ine_mortalidad_1934_1950.py). No corrige por cambios de población.",
        cautela + " El índice no descuenta la variación de la población ni sus desplazamientos: una provincia que recibió refugiados o tropas, o que creció, puede subir sin que empeorase la salud de sus vecinos; cuanto más se aleja de 1935, más pesa el crecimiento de la población.", obs_i)
    i_anios = sorted({o["period"] for o in obs_inf})
    ind("ind-mortalidad-infantil-prov", f"Mortalidad infantil, {i_anios[0]}-{i_anios[-1]}",
        "Fallecidos de menos de un año por cada 1.000 nacidos vivos del mismo año y provincia.",
        "fallecidos de menos de un año por 1.000 nacidos vivos", "nacidos vivos del mismo año en la provincia",
        "Fallecidos de menos de un año (tabla «Mortalidad infantil, por provincias») / nacidos vivos (tabla del movimiento natural) × 1.000. El Anuario no publica esta tasa por provincia: se calcula aquí (scripts/etl/ine_mortalidad_1934_1950.py).",
        cautela + " Los fallecidos de menos de un año en un año natural no son exactamente los nacidos ese año; es la aproximación habitual en las estadísticas de la época. Los muertos antes de las 24 horas no cuentan como nacidos vivos ni como fallecidos, lo que rebaja la tasa frente a las definiciones actuales.", obs_inf)
    t = {y: data[y]["filas"]["TOTAL"] for y in anios}
    base = sum(a43[b]["filas"]["TOTAL"]["fall_t"] for b in BASE) / 2
    print("España, índice de defunciones (1934-35 = 100):", ", ".join(f"{y}: {100 * t[y]['fall_t'] / base:.0f}" for y in anios))
    print("España, mortalidad infantil (‰):", ", ".join(f"{y}: {1000 * inf[y]['filas']['TOTAL']['m1'] / data[y]['filas']['TOTAL']['nacidos']:.0f}" for y in sorted(inf) if y in data))


if __name__ == "__main__":
    main()
