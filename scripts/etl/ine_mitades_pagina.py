# Herramienta de transcripción (movimiento natural, Anuario de 1943): renderiza una página del PDF a 200 ppp y la parte en dos mitades.
# Uso: uv run --with pillow tools/mitades.py <pdf> <página> <prefijo>  -> <prefijo>-a.png (arriba) y -b.png (abajo), 200 ppp
import sys, subprocess, tempfile, pathlib
from PIL import Image
pdf, pag, pre = sys.argv[1], sys.argv[2], sys.argv[3]
with tempfile.TemporaryDirectory() as d:
    subprocess.run(["pdftoppm", "-r", "200", "-png", "-f", pag, "-l", pag, pdf, f"{d}/p"], check=True)
    im = Image.open(next(pathlib.Path(d).glob("p-*.png"))).convert("L")
w, h = im.size
im.crop((0, int(h*.17), w, int(h*.52))).save(f"{pre}-a.png")
im.crop((0, int(h*.50), w, int(h*.86))).save(f"{pre}-b.png")
print(im.size)
