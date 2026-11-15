# /// script
# requires-python = ">=3.11"
# dependencies = ["datasets>=4.0.0", "rapidfuzz", "pillow"]
# ///
"""Compara la capa de texto del BOE con LightOnOCR-3 0.8B y 4B en las páginas del piloto.

No hay transcripción de referencia completa. Se mide:
  1. Referencia a mano en oro/ (fragmentos de texto y cifras de tablas). Es la única
     métrica de calidad real; el resto son indicios.
  2. Acuerdo entre fuentes (CER cruzado): si los dos modelos coinciden entre sí y discrepan
     del BOE, el error suele estar en la capa del BOE, y al revés.
  3. Ruido: letras sueltas separadas por espacios («S U M A R I O») y tokens con símbolos.
Genera data/raw/ocr_piloto/informe.html con la imagen y los tres textos lado a lado.

Uso: uv run scripts/ocr_piloto/comparar.py USUARIO_HF   # salidas de HF Jobs
     uv run scripts/ocr_piloto/comparar.py --local      # salidas de local_mlx.py
"""
import html
import json
import pathlib
import re
import sys
import unicodedata

from datasets import load_dataset, load_from_disk
from rapidfuzz import fuzz
from rapidfuzz.distance import Levenshtein

RAIZ = pathlib.Path(__file__).resolve().parents[2]
DIR = RAIZ / "data/raw/ocr_piloto"
ORO = pathlib.Path(__file__).with_name("oro")


def norm(t: str) -> str:
    t = re.sub(r"<[^>]+>", " ", t)                 # HTML de tablas
    t = re.sub(r"[#*_`|>\-]{1,}", " ", t)          # marcas markdown
    t = re.sub(r"(\w)[­-]\s*\n\s*(\w)", r"\1\2", t)  # guiones de corte de línea
    t = unicodedata.normalize("NFC", t).lower()
    return re.sub(r"\s+", " ", t).strip()


def cer(a: str, b: str) -> float:
    return Levenshtein.normalized_distance(norm(a), norm(b)) if b else float("nan")


def fragmento(frag: str, t: str) -> float:
    """Similitud 0-1 del fragmento de referencia con su mejor alineación dentro del texto."""
    return round(fuzz.partial_ratio(norm(frag), norm(t)) / 100, 3)


def cifras(lista: list[str], t: str) -> float:
    """Fracción de cifras de referencia que aparecen literales (solo dígitos) en el texto."""
    seq = re.sub(r"(?<=\d)[.,'‘’`´*· ](?=\d)", "", t)
    nums = set(re.findall(r"\d+", seq))
    ok = sum(1 for c in lista if re.sub(r"\D", "", c) in nums)
    return round(ok / len(lista), 3)


def ruido(t: str) -> dict:
    toks = t.split()
    sueltas = len(re.findall(r"(?:\b\w\s){3,}\w\b", t))
    raros = sum(1 for w in toks if re.search(r"[^\wáéíóúüñÁÉÍÓÚÜÑ.,;:()º°ª'\"¿?¡!%/$€-]", w))
    return {"letras_sueltas": sueltas, "tokens_raros_pct": round(100 * raros / max(len(toks), 1), 1)}


def main() -> None:
    if sys.argv[1] == "--local":
        boe = {r["id"]: r["texto_boe"] for r in load_from_disk(str(DIR / "dataset"))
               .remove_columns("image")}
        por_id = {}
        for m in ("0.8b", "4b"):
            f = DIR / f"salida-{m}.jsonl"
            filas_m = [json.loads(l) for l in f.open()] if f.exists() else []
            por_id[m] = {r["id"]: {**r, "texto_boe": boe[r["id"]]} for r in filas_m}
    else:
        user = sys.argv[1]
        por_id = {m: {r["id"]: r for r in load_dataset(
            f"{user}/memoria-viva-ocr-piloto-{m}", split="train")} for m in ("0.8b", "4b")}
    filas, bloques = [], []
    for pid, r08 in sorted(por_id["0.8b"].items()):
        r4 = por_id["4b"].get(pid, {})
        tiempos = {m: por_id[m].get(pid, {}).get("segundos") for m in ("0.8b", "4b")}
        textos = {"boe": r08["texto_boe"], "0.8b": r08["markdown"], "4b": r4.get("markdown", "")}
        frag = (ORO / f"{pid}.txt").read_text() if (ORO / f"{pid}.txt").exists() else ""
        cif = [l.strip() for l in (ORO / f"{pid}.cifras").read_text().splitlines()
               if l.strip() and not l.startswith("#")] if (ORO / f"{pid}.cifras").exists() else []
        fila = {"id": pid,
                "oro_fragmento": {k: fragmento(frag, v) for k, v in textos.items()} if frag else None,
                "oro_cifras": {k: cifras(cif, v) for k, v in textos.items()} if cif else None,
                "cer_08_vs_4": round(cer(textos["0.8b"], textos["4b"]), 3),
                "cer_boe_vs_4": round(cer(textos["boe"], textos["4b"]), 3),
                "cer_boe_vs_08": round(cer(textos["boe"], textos["0.8b"]), 3),
                "ruido": {k: ruido(v) for k, v in textos.items()},
                "segundos": tiempos}
        filas.append(fila)
        cols = "".join(f"<td><h4>{k}</h4><pre>{html.escape(v)}</pre></td>" for k, v in textos.items())
        bloques.append(f"<h2>{pid}</h2><p>{html.escape(json.dumps(fila, ensure_ascii=False))}</p>"
                       f"<table><tr><td><img src='{pid}.png' width='500'></td>{cols}</tr></table>")

    (DIR / "metricas.json").write_text(json.dumps(filas, ensure_ascii=False, indent=1))
    (DIR / "informe.html").write_text(
        "<!doctype html><meta charset='utf-8'><title>Piloto OCR Gaceta</title>"
        "<style>body{font:14px system-ui;margin:16px}td{vertical-align:top;width:25%}"
        "pre{white-space:pre-wrap;font-size:11px;max-height:900px;overflow:auto}</style>"
        + "".join(bloques))

    for k in ("cer_08_vs_4", "cer_boe_vs_4", "cer_boe_vs_08"):
        vals = [f[k] for f in filas]
        print(f"{k}: media {sum(vals) / len(vals):.3f}")
    for src in ("boe", "0.8b", "4b"):
        s = sum(f["ruido"][src]["letras_sueltas"] for f in filas)
        print(f"letras sueltas {src}: {s}")
    for clave, nombre in (("oro_fragmento", "similitud con fragmento a mano"),
                          ("oro_cifras", "cifras exactas")):
        con = [f for f in filas if f[clave]]
        for src in ("boe", "0.8b", "4b"):
            if con:
                print(f"{nombre} {src}: {sum(f[clave][src] for f in con) / len(con):.3f} "
                      f"({len(con)} páginas)")
    for m in ("0.8b", "4b"):
        seg = [f["segundos"][m] for f in filas if f.get("segundos", {}).get(m)]
        if seg:
            print(f"segundos por página {m}: media {sum(seg) / len(seg):.1f} ({len(seg)} páginas)")
    print(f"Informe: {DIR / 'informe.html'}")


if __name__ == "__main__":
    main()
