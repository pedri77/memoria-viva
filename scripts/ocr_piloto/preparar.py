# /// script
# requires-python = ">=3.11"
# dependencies = ["datasets>=4.0.0", "pillow"]
# ///
"""Prepara el dataset del piloto OCR (20 páginas de la Gaceta) para HF Jobs.

Lee seleccion.csv, localiza la página física de cada página impresa en los PDF de
data/raw/gaceta/ (descargados solo por la ruta /gazeta/dias/, permitida por robots.txt),
la renderiza a 400 DPI con el lado mayor a 2048 px (recomendación de LightOnOCR-3)
y guarda también la capa de texto del BOE como referencia de comparación.

Uso:
  uv run scripts/ocr_piloto/preparar.py                 # solo local
  uv run scripts/ocr_piloto/preparar.py --push USER/memoria-viva-ocr-piloto   # dataset PRIVADO

Salida local: data/raw/ocr_piloto/ (imágenes PNG, manifiesto.json y dataset en disco).
"""
import argparse
import csv
import json
import pathlib
import re
import subprocess

RAIZ = pathlib.Path(__file__).resolve().parents[2]
PDFS = RAIZ / "data/raw/gaceta"
SALIDA = RAIZ / "data/raw/ocr_piloto"


def texto(pdf: pathlib.Path, p: int, layout: bool = False) -> str:
    """Capa de texto del BOE. Sin -layout sale en orden de lectura (columna a columna);
    con -layout conserva la línea de cabecera, útil solo para localizar la página."""
    extra = ["-layout"] if layout else []
    return subprocess.run(["pdftotext", *extra, "-f", str(p), "-l", str(p), str(pdf), "-"],
                          capture_output=True, text=True, check=True).stdout


def paginas(pdf: pathlib.Path) -> int:
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True, check=True).stdout
    return int(re.search(r"Pages:\s+(\d+)", info).group(1))


def pagina_fisica(pdf: pathlib.Path, impresa: str) -> int:
    """Busca la página física cuya cabecera lleva el número impreso.

    La capa OCR del BOE es ruidosa, así que se busca el número como palabra suelta en las
    primeras líneas de cada página y se elige la coincidencia más cercana a la estimación
    lineal desde la primera página.
    """
    if impresa == "sumario":
        return 1
    n = int(impresa)
    total = paginas(pdf)
    cand = []
    for p in range(1, total + 1):
        cab = "\n".join(texto(pdf, p, layout=True).splitlines()[:6])
        if re.search(rf"(?<!\d){n}(?!\d)", cab):
            cand.append(p)
    primera = re.search(r"P[áa]g(?:ina|\.)?\s*\.?\s*(\d{1,4})", texto(pdf, 1, layout=True))
    estimada = n - int(primera.group(1)) + 1 if primera else None
    if cand:
        return min(cand, key=lambda p: abs(p - estimada)) if estimada else cand[0]
    if estimada and 1 <= estimada <= total:
        return estimada
    raise SystemExit(f"{pdf.name}: no encuentro la página impresa {n}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--push", help="repo de dataset en HF (se sube PRIVADO)")
    args = ap.parse_args()

    SALIDA.mkdir(parents=True, exist_ok=True)
    urls = {}
    for f in (RAIZ / "data/canonical").rglob("*.json"):
        for u in re.findall(r"https://www\.boe\.es/gazeta/dias/[^\"]+\.pdf", f.read_text()):
            urls[u.rsplit("/", 1)[1]] = u

    filas = []
    with open(pathlib.Path(__file__).with_name("seleccion.csv")) as fh:
        for r in csv.DictReader(fh):
            pdf = PDFS / r["pdf"]
            if not pdf.exists():
                raise SystemExit(f"Falta {pdf}: descárgalo antes por /gazeta/dias/")
            p = pagina_fisica(pdf, r["pagina_impresa"])
            pid = f"{r['pdf'].removesuffix('.pdf')}-p{p:02d}"
            png = SALIDA / f"{pid}.png"
            if not png.exists():
                subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", "400",
                                "-scale-to", "2048", "-png", "-singlefile", str(pdf),
                                str(png.with_suffix(""))], check=True)
            filas.append({"id": pid, "pdf": r["pdf"], "pdf_url": urls.get(r["pdf"], ""),
                          "pagina_fisica": p, "pagina_impresa": r["pagina_impresa"],
                          "motivo": r["motivo"], "texto_boe": texto(pdf, p), "png": str(png)})
            print(f"{pid}: impresa {r['pagina_impresa']} → física {p}")

    (SALIDA / "manifiesto.json").write_text(json.dumps(
        [{k: v for k, v in f.items() if k != "texto_boe"} for f in filas], ensure_ascii=False, indent=1))

    from datasets import Dataset, Features, Image, Value
    feats = Features({"image": Image(), "id": Value("string"), "pdf": Value("string"),
                      "pdf_url": Value("string"), "pagina_fisica": Value("int32"),
                      "pagina_impresa": Value("string"), "motivo": Value("string"),
                      "texto_boe": Value("string")})
    ds = Dataset.from_list([{**{k: v for k, v in f.items() if k != "png"}, "image": f["png"]}
                            for f in filas], features=feats)
    ds.save_to_disk(str(SALIDA / "dataset"))
    print(f"{len(ds)} páginas en {SALIDA / 'dataset'}")
    if args.push:
        ds.push_to_hub(args.push, private=True)
        print(f"Subido PRIVADO a https://huggingface.co/datasets/{args.push}")


if __name__ == "__main__":
    main()
