# /// script
# requires-python = ">=3.11"
# dependencies = ["rapidfuzz"]
# ///
"""Comprueba contra el OCR local de la Gaceta las afirmaciones que la citan.

Para cada claim de data/canonical/{stories,events} y cada resumen de documento cuya fuente es
un PDF de la Gaceta (canonical_url en /gazeta/dias/), busca en data/raw/ocr/gaceta/<PDF>/
(salida de ocr_gaceta.py):
  - citas literales «…» de 15 caracteres o más: similitud parcial con la página citada
    (OK >= 90, DUDOSA 80-89, NO ESTÁ < 80);
  - cifras de tres o más dígitos (35.716, 7.000, 50.000): presencia literal.
Si algo no está en la página citada pero sí en otra del mismo PDF, avisa de la página real.

El OCR del 0.8B tiene ~2 % de cifras mal en tablas: un aviso es para mirar el facsímil,
no prueba de error. Años (1900-1999) y artículos no se comprueban como cifras.
Falsos avisos conocidos (revisión del 16-11-2026, 9 avisos en 104 comprobaciones, ninguno era
error de la web):
  - cifras que el impreso da en letra: «cincuenta mil», «cien mil» (GMD-1931-130), votos de
    Azaña «setecientos cincuenta y cuatro…» (GMD-1936-132);
  - errores del OCR: 5.500 por 5.300 plazas de maestros en la pág. 234 (GMD-1936-282; la capa
    de texto del BOE y el sumario dicen 5.300).

Uso: uv run scripts/etl/verificar_citas_ocr.py [--todo]   (--todo lista también los OK)
"""
import argparse
import importlib.util
import json
import pathlib
import re
import unicodedata

from rapidfuzz import fuzz

RAIZ = pathlib.Path(__file__).resolve().parents[2]
OCR = RAIZ / "data/raw/ocr/gaceta"
PDFS = RAIZ / "data/raw/gaceta"

_spec = importlib.util.spec_from_file_location("preparar", RAIZ / "scripts/ocr_piloto/preparar.py")
preparar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(preparar)


def norm(t: str) -> str:
    t = re.sub(r"<[^>]+>", " ", t)
    t = re.sub(r"[#*_`|]", " ", t)
    t = re.sub(r"(\w)[­-]\s*\n\s*(\w)", r"\1\2", t)          # guion de fin de línea
    t = unicodedata.normalize("NFKD", t.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))  # «á» de 1907 = «a»
    t = re.sub(r"(?<=\d)[.,'’ ](?=\d{3}\b)", "", t)             # 35.716 → 35716
    return re.sub(r"\s+", " ", t).strip()


def cifras(t: str) -> set[str]:
    out = set()
    for n in re.findall(r"\d+", norm(t)):
        if len(n) >= 3 and not (len(n) == 4 and 1800 <= int(n) <= 1999):
            out.add(n)
    return out


def paginas_impresas(locator: str) -> list[int]:
    m = re.search(r"p[áa]gs?\.\s*(\d+)(?:\s*(?:[-–]|y)\s*(\d+))?", locator or "")
    if not m:
        return []
    a, b = int(m[1]), int(m[2] or m[1])
    return list(range(a, b + 1)) if b >= a and b - a < 10 else [a]


_cache: dict = {}


def texto_pdf(pid: str) -> dict[int, str]:
    if pid not in _cache:
        d = OCR / pid
        _cache[pid] = {int(f.stem[1:]): norm(f.read_text()) for f in d.glob("p*.md")} if d.exists() else {}
    return _cache[pid]


def fisicas(pid: str, impresas: list[int]) -> list[int]:
    out = []
    for n in impresas:
        try:
            out.append(preparar.pagina_fisica(PDFS / f"{pid}.pdf", str(n)))
        except SystemExit:
            pass
    return out


def comprobar(texto: str, pid: str, locator: str) -> dict[str, str]:
    """{elemento: aviso} de lo que no aparece en la página citada."""
    pags = texto_pdf(pid)
    if not pags:
        return {"_ocr": f"sin OCR de {pid}"}
    imp = paginas_impresas(locator)
    fis = fisicas(pid, imp)
    # «y ss.» o sin página: la citada y las dos siguientes
    if fis and ("ss" in (locator or "") or len(fis) == 1):
        fis = sorted(set(fis) | {fis[-1] + 1, fis[-1] + 2})
    ventana = " ".join(pags.get(p, "") for p in fis) if fis else " ".join(pags.values())
    avisos = {}
    # Las citas de títulos suelen salir del sumario (página física 1), no de la citada.
    ventana_q = ventana + " " + pags.get(1, "")
    for q in re.findall(r"«([^»]{15,})»", texto):
        s = fuzz.partial_ratio(norm(q), ventana_q)
        if s >= 90:
            continue
        mejor = max(pags, key=lambda p: fuzz.partial_ratio(norm(q), pags[p]))
        s2 = fuzz.partial_ratio(norm(q), pags[mejor])
        donde = f"; en el PDF, p{mejor:02d} da {s2:.0f}" if fis and mejor not in fis and s2 >= 90 else ""
        avisos[q] = f"{'CITA DUDOSA' if s >= 80 else 'CITA NO ESTÁ'} ({s:.0f}) «{q[:70]}»{donde}"
    # Fuera las citas y las referencias de página («págs. 413-415»), que no son datos.
    datos = re.sub(r"«[^»]*»|p[áa]gs?\.\s*[\d\s,y–-]+", "", texto)
    for c in sorted(cifras(datos)):
        if c in cifras(ventana):
            continue
        otras = [p for p, t in pags.items() if c in cifras(t)]
        donde = f"; sí en p{', p'.join(f'{p:02d}' for p in otras)}" if otras and fis else ""
        avisos[c] = f"CIFRA {c} no está en la página citada{donde}"
    if imp and not fis:
        avisos["_pag"] = f"no localizo la pág. impresa {imp} en el PDF"
    return avisos


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--todo", action="store_true")
    args = ap.parse_args()

    docs = {}
    for f in (RAIZ / "data/canonical/documents").glob("*.json"):
        d = json.loads(f.read_text())
        m = re.search(r"/gazeta/dias/.*/(G[A-Z]{2}-\d{4}-[\d-]+)\.pdf", d.get("canonical_url", ""))
        if m:
            docs[d["id"]] = (m[1], d)

    casos = []  # (origen, texto, [(pdf, locator), ...])
    for did, (pid, d) in sorted(docs.items()):
        casos.append((f"{did} (resumen)", d["summary"], [(pid, d.get("signature", ""))]))
    for carpeta in ("stories", "events"):
        for f in sorted((RAIZ / "data/canonical" / carpeta).glob("*.json")):
            o = json.loads(f.read_text())
            claims = [c for s in o.get("scenes", []) for c in s["claims"]] + o.get("claims", [])
            for i, c in enumerate(claims):
                ev = [(docs[e["document_id"]][0], e.get("locator", ""))
                      for e in c.get("evidence", []) if e["document_id"] in docs]
                if ev:
                    casos.append((f"{o['id']} claim {i}", c["text"], ev))

    con_aviso = 0
    for origen, texto, ev in casos:
        # Con varias pruebas, un elemento solo falla si no está en ninguna de ellas.
        por_ev = [comprobar(texto, pid, loc) for pid, loc in ev]
        fallan = set.intersection(*(set(a) for a in por_ev))
        if fallan:
            con_aviso += 1
        if fallan or args.todo:
            print(f"{origen} → " + " + ".join(f"{pid} «{loc}»" for pid, loc in ev))
            for k in sorted(fallan) or ["OK"]:
                print(f"   {next(a[k] for a in por_ev if k in a) if fallan else k}")
    print(f"\n{len(casos)} comprobaciones, {con_aviso} con avisos")


if __name__ == "__main__":
    main()
