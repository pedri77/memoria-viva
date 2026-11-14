"""Localiza disposiciones del BOE de 1936-1939 (zona sublevada) por fecha y palabra clave.

Usa solo las fichas https://www.boe.es/buscar/doc.php?id=BOE-A-AAAA-N, permitidas por el
robots.txt de boe.es (que prohíbe el buscador de la Gazeta y /datos/pdfs/). Los identificadores
son correlativos dentro de cada año: se busca por bisección el primer documento de la fecha
pedida y después se recorren los de ese día. Una petición cada 1,5 s y caché en disco para no
repetir consultas.

Uso: python3 -I scripts/etl/boe_localizar.py AAAA-MM-DD "palabra clave" [CACHE.json]
"""
import datetime
import html
import json
import pathlib
import re
import sys
import time
import urllib.request

UA = "memoria-viva/0.1 (+https://github.com/pedri77/memoria-viva)"
PAUSA = 1.5
MESES = {m: i for i, m in enumerate(["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
                                      "septiembre", "octubre", "noviembre", "diciembre"], 1)}
_cache: dict = {}
_cache_path: pathlib.Path | None = None


def meta(boe_id: str):
    if boe_id in _cache:
        return _cache[boe_id]
    req = urllib.request.Request(f"https://www.boe.es/buscar/doc.php?id={boe_id}", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            t = r.read().decode("utf-8", "replace")
    except Exception:
        t = ""
    time.sleep(PAUSA)
    txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", re.sub(r"(?s)<(script|style).*?</\1>", "", t))))
    m = re.search(r"Documento " + re.escape(boe_id) + r" Documento " + re.escape(boe_id) + r" (.*?) Publicado en: «([^»]+)» núm\. (\d+), de (\d+) de (\w+) de (\d{4}), páginas? ([\d a]+?)(?: \(|\s+Departamento)", txt)
    dept = re.search(r"Departamento: (.*?) Referencia:", txt)
    res = None
    if m:
        d = datetime.date(int(m.group(6)), MESES[m.group(5).lower()], int(m.group(4))).isoformat()
        res = {"id": boe_id, "title": m.group(1).strip(), "diario": m.group(2), "num": int(m.group(3)), "date": d,
               "pages": m.group(7).strip(), "dept": dept.group(1).strip() if dept else None}
    _cache[boe_id] = res
    if _cache_path:
        _cache_path.write_text(json.dumps(_cache, ensure_ascii=False, indent=0))
    return res


def probe(year: int, n: int, tries: int = 4):
    """Ficha en n o en los siguientes (como mucho `tries` peticiones). Devuelve (n_real, meta) o (n, None)."""
    for k in range(tries):
        m = meta(f"BOE-A-{year}-{n + k}")
        if m:
            return n + k, m
    return n, None


def first_on_or_after(year: int, date: str, top: int = 25000):
    """Primer identificador con fecha >= date. Usa como anclas las fichas en caché, sondea con
    pocas peticiones donde no hay anclas y biseca tolerando huecos de numeración."""
    def known():
        return sorted((int(k.rsplit("-", 1)[1]), v["date"]) for k, v in _cache.items()
                      if v and k.startswith(f"BOE-A-{year}-"))
    if not known():
        for n in (500, 1000, 2000, 4000, 6000, 8000, 10000, 12000, 16000):
            probe(year, n, tries=2)
    for _ in range(40):
        k = known()
        below = [n for n, d in k if d < date]
        above = [n for n, d in k if d >= date]
        lo = max(below) if below else None
        hi = min(above) if above else None
        if lo is None and hi is not None:          # sin ancla inferior: bajar a saltos
            for back in (300, 150, 60):
                real, m = probe(year, max(1, hi - back), tries=2)
                if m:
                    break
            if m is None:
                return max(1, hi - 300)
            continue
        if hi is None and lo is not None:          # sin ancla superior: subir a saltos
            real, m = probe(year, lo + 300, tries=2)
            if m is None:
                return lo
            continue
        if lo is None and hi is None:
            return 1
        if hi - lo <= 40:
            return lo
        mid = (lo + hi) // 2
        real, m = probe(year, mid, tries=3)
        if m is None:                              # hueco: probar el otro lado del punto medio
            probe(year, (lo + mid) // 2, tries=2)
            if known() == k:
                return lo
    return lo or 1


def docs_on(date: str, max_docs: int = 200, max_req: int = 300):
    year = int(date[:4])
    n = first_on_or_after(year, date)
    out, vacios, req = [], 0, 0
    while len(out) < max_docs and vacios < 8 and req < max_req:
        m = meta(f"BOE-A-{year}-{n}")
        n += 1
        req += 1
        if m is None:
            vacios += 1
            continue
        vacios = 0
        if m["date"] < date:
            continue
        if m["date"] > date:
            break
        out.append(m)
    return out


if __name__ == "__main__":
    date, kw = sys.argv[1], sys.argv[2].lower()
    if len(sys.argv) > 3:
        _cache_path = pathlib.Path(sys.argv[3])
        if _cache_path.exists():
            _cache.update(json.loads(_cache_path.read_text()))
    docs = docs_on(date)
    print(f"{len(docs)} disposiciones el {date}")
    for d in docs:
        mark = ">>" if kw in d["title"].lower() else "  "
        print(mark, d["id"], f"núm. {d['num']}, págs. {d['pages']}", "|", d["dept"], "|", d["title"][:160])
