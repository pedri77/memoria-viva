# Herramienta de transcripción (censo de 1930, profesiones): une la parte derecha de las páginas
# de la provincia (columnas «TOTAL DE» y «TOTAL general») en una sola imagen para leerla.
# Uso: uv run --with pillow tools/tiras.py <pdf> <salida.png> <pág1,pág2,...> [x0=0.70]
import sys, subprocess, tempfile, pathlib
from PIL import Image
pdf, out, pags = sys.argv[1], sys.argv[2], [int(p) for p in sys.argv[3].split(",")]
x0 = float(sys.argv[4]) if len(sys.argv) > 4 else 0.70
tiras = []
with tempfile.TemporaryDirectory() as d:
    for p in pags:
        subprocess.run(["pdftoppm", "-r", "150", "-png", "-f", str(p), "-l", str(p), pdf, f"{d}/p"], check=True)
        im = Image.open(next(pathlib.Path(d).glob("p-*.png"))).convert("L")
        for f in pathlib.Path(d).glob("p-*.png"): f.unlink()
        w, h = im.size
        tiras.append(im.crop((int(w * x0), int(h * 0.16), w, int(h * 0.80))))
W = sum(t.width for t in tiras) + 12 * (len(tiras) - 1); H = max(t.height for t in tiras)
S = Image.new("L", (W, H), 255); x = 0
for t in tiras: S.paste(t, (x, 0)); x += t.width + 12
S.save(out)
print(S.size)
