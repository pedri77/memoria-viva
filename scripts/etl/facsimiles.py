"""Facsímiles: imagen de la primera página de cada número de la Gaceta de Madrid (y de las tablas del INE)
que cita el proyecto, para mostrarla en las fichas y la cronología.

Derechos:
  - Gaceta: condiciones de reutilización de la AEBOE (licencia tipo de 27-06-2024), que permiten copiar,
    reproducir y difundir citando «Fuente de los datos: Agencia Estatal Boletín Oficial del Estado» con
    enlace a https://www.boe.es. Solo se usan los PDF de la ruta permitida por robots.txt
    (/gazeta/dias/AAAA/MM/DD/pdfs/GMD-AAAA-NNN.pdf); nunca /datos/pdfs/.
  - INE: CC BY 4.0.

Entrada: documentos de data/canonical/documents con canonical_url de esas rutas; PDF en caché en
data/raw/gaceta/ (fuera de git) o descargados con una petición cada 2 s.
Salida: site/public/facsimiles/<id>.webp (520 px de ancho) y site/src/data/facsimiles.json.

Uso: python3 -I scripts/etl/facsimiles.py   (requiere pdftoppm y cwebp)
"""
import json
import pathlib
import re
import subprocess
import tempfile
import time
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
DOCS = ROOT / "data/canonical/documents"
CACHE = ROOT / "data/raw/gaceta"
OUT = ROOT / "site/public/facsimiles"
MANIFEST = ROOT / "site/src/data/facsimiles.json"
UA = {"User-Agent": "memoria-viva/0.1 (proyecto de investigación sin ánimo de lucro)"}
GAZ = re.compile(r"^https://www\.boe\.es/gazeta/dias/\d{4}/\d{2}/\d{2}/pdfs/([A-Z]{3}-\d{4}-\d+)\.pdf$")
INE = re.compile(r"^https://www\.ine\.es/inebaseweb/pdfDispacher\.do\?td=(\d+)&ext=\.pdf$")
ANCHO = 520


def pdf_local(url: str, nombre: str) -> pathlib.Path:
    CACHE.mkdir(parents=True, exist_ok=True)
    f = CACHE / f"{nombre}.pdf"
    if not f.exists() or f.stat().st_size < 5000:
        with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=120) as r:
            f.write_bytes(r.read())
        time.sleep(2)
    return f


def render(pdf: pathlib.Path, destino: pathlib.Path) -> tuple[int, int]:
    with tempfile.TemporaryDirectory() as d:
        subprocess.run(["pdftoppm", "-r", "90", "-png", "-f", "1", "-l", "1", "-scale-to-x", str(ANCHO), "-scale-to-y", "-1", str(pdf), f"{d}/p"], check=True)
        png = next(pathlib.Path(d).glob("p*.png"))
        subprocess.run(["cwebp", "-quiet", "-q", "62", str(png), "-o", str(destino)], check=True)
        out = subprocess.run(["sips", "-g", "pixelWidth", "-g", "pixelHeight", str(png)], capture_output=True, text=True).stdout
    w, h = (int(x) for x in re.findall(r"pixel\w+: (\d+)", out))
    return w, h


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    MANIFEST.parent.mkdir(parents=True, exist_ok=True)
    man = {}
    for f in sorted(DOCS.glob("*.json")):
        d = json.loads(f.read_text())
        u = d["canonical_url"]
        if m := GAZ.match(u):
            pdf, cita = pdf_local(u, m.group(1)), "Fuente de los datos: Agencia Estatal Boletín Oficial del Estado (https://www.boe.es)"
        elif m := INE.match(u):
            pdf, cita = pdf_local(u, f"INE-{m.group(1)}"), "Fuente: Instituto Nacional de Estadística (INE), INEbase Historia (CC BY 4.0)"
        else:
            continue
        destino = OUT / f"{d['id']}.webp"
        w, h = render(pdf, destino)
        man[d["id"]] = {"src": f"facsimiles/{d['id']}.webp", "w": w, "h": h, "pagina": 1, "cita": cita, "original": u}
    MANIFEST.write_text(json.dumps(man, ensure_ascii=False, indent=1) + "\n")
    print(f"{len(man)} facsímiles; {sum(p.stat().st_size for p in OUT.glob('*.webp')) // 1024} KB")


if __name__ == "__main__":
    main()
