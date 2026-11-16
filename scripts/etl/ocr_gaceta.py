# /// script
# requires-python = ">=3.11"
# dependencies = ["mlx-vlm>=0.7.12", "torch", "torchvision"]
# ///
"""OCR de la Gaceta en local (Apple Silicon) con LightOnOCR-3 0.8B, pesos oficiales bf16.

Decisión del piloto del 15-11-2026 (scripts/ocr_piloto/): el 0.8B iguala al 4B en texto
corrido y casi en cifras (93 % frente a 95 %) en 1/5,6 del tiempo, y supera con mucho la capa
de texto del BOE (72 % de cifras, columnas mezcladas). Nada sale del Mac.

Alcance:
  --citadas (por defecto)  páginas que citan las firmas de data/canonical/documents (~70)
  --todo                   todas las páginas de data/raw/gaceta/*.pdf (~683, unas 9 h)
  --pdf GMD-1931-130       limita a uno o varios PDF

Salida (no se publica, data/raw/ está en .gitignore):
  data/raw/ocr/gaceta/<PDF>/p<NN>.md        markdown de la página física NN
  data/raw/ocr/gaceta/<PDF>/indice.json     página física → impresa, segundos, modelo
Reanuda: salta las páginas que ya tienen .md. Revisar a mano las tablas de 1907 y anteriores.

Páginas cortadas (indice.json "truncada": true, el modelo llegó a --max-tokens):
  --rehacer-truncadas --max-tokens 12288     repite solo esas; basta en tablas largas
  --rehacer-truncadas --partir 2             si entra en bucle de repetición (tablas de
                                             nombres o celdas vacías): franjas horizontales
                                             con solape; ojo, mezcla el orden en texto a
                                             varias columnas
Corrida del 16-11-2026: 683 páginas, 37,7 s/pág; de 13 cortadas quedó 1 (GMD-1907-222 p18,
calendario astronómico).

Uso: uv run scripts/etl/ocr_gaceta.py [--todo] [--pdf ID ...] [--dry-run]
"""
import argparse
import importlib.util
import json
import pathlib
import re
import subprocess
import tempfile
import time

RAIZ = pathlib.Path(__file__).resolve().parents[2]
PDFS = RAIZ / "data/raw/gaceta"
SALIDA = RAIZ / "data/raw/ocr/gaceta"
MODELO = "lightonai/LightOnOCR-3-0.8B"
SEG_PAGINA = 48  # medido en el piloto (M5, 24 GB)

# Reutiliza la localización de página impresa → física del piloto.
_spec = importlib.util.spec_from_file_location("preparar", RAIZ / "scripts/ocr_piloto/preparar.py")
preparar = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(preparar)


def citadas() -> dict[str, set[int]]:
    """{pdf: {páginas impresas}} a partir de canonical_url y signature de cada documento."""
    out: dict[str, set[int]] = {}
    for f in (RAIZ / "data/canonical/documents").glob("*.json"):
        d = json.loads(f.read_text())
        m = re.search(r"/(G[A-Z]{2}-\d{4}-\d+)\.pdf", d.get("canonical_url", ""))
        r = re.search(r"p[áa]gs?\.\s*(\d+)(?:\s*[-–]\s*(\d+))?", d.get("signature", ""))
        if m and r:
            a, b = int(r[1]), int(r[2] or r[1])
            out.setdefault(m[1], set()).update(range(a, b + 1))
    return out


def plan(todo: bool, solo: list[str] | None) -> list[tuple[pathlib.Path, int, str]]:
    """Lista de (pdf, página física, página impresa o '')."""
    tareas = []
    if todo:
        for pdf in sorted(PDFS.glob("*.pdf")):
            tareas += [(pdf, p, "") for p in range(1, preparar.paginas(pdf) + 1)]
    else:
        for pid, imp in sorted(citadas().items()):
            pdf = PDFS / f"{pid}.pdf"
            if not pdf.exists():
                print(f"AVISO: falta {pdf.name}; descárgalo por /gazeta/dias/ (gazeta_localizar.py)")
                continue
            fis = {}
            for n in sorted(imp):
                try:
                    fis[preparar.pagina_fisica(pdf, str(n))] = str(n)
                except SystemExit as e:
                    print(f"AVISO: {e}")
            tareas += [(pdf, p, n) for p, n in sorted(fis.items())]
    if solo:
        tareas = [t for t in tareas if t[0].stem in solo]
    return tareas


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--todo", action="store_true")
    ap.add_argument("--pdf", nargs="*")
    ap.add_argument("--dry-run", action="store_true", help="solo cuenta páginas y tiempo")
    ap.add_argument("--max-tokens", type=int, default=6144)
    ap.add_argument("--rehacer-truncadas", action="store_true",
                    help="repite solo las páginas marcadas truncada en indice.json")
    ap.add_argument("--partir", type=int, default=1,
                    help="corta la página en N franjas horizontales (solape 3 %%) y las "
                         "transcribe por separado; para tablas densas o bucles de repetición")
    args = ap.parse_args()

    tareas = plan(args.todo, args.pdf)
    if args.rehacer_truncadas:
        trunc = set()
        for f in SALIDA.glob("*/indice.json"):
            trunc |= {(f.parent.name, int(p)) for p, v in json.loads(f.read_text()).items()
                      if v.get("truncada")}
        pend = [t for t in tareas if (t[0].stem, t[1]) in trunc]
    else:
        pend = [t for t in tareas if not (SALIDA / t[0].stem / f"p{t[1]:02d}.md").exists()]
    print(f"{len(tareas)} páginas, {len(pend)} pendientes, "
          f"~{len(pend) * SEG_PAGINA / 3600:.1f} h a {SEG_PAGINA} s/página")
    if args.dry_run or not pend:
        return

    from mlx_vlm import generate, load
    from mlx_vlm.prompt_utils import apply_chat_template

    model, processor = load(MODELO)
    prompt = apply_chat_template(processor, model.config, "", num_images=1)
    with tempfile.TemporaryDirectory() as tmp:
        for i, (pdf, p, imp) in enumerate(pend, 1):
            png = pathlib.Path(tmp) / "pagina"
            # Con franjas se renderiza más grande para que cada una salga a ~2048 px.
            subprocess.run(["pdftoppm", "-f", str(p), "-l", str(p), "-r", "400", "-scale-to",
                            str(2048 * args.partir), "-png", "-singlefile", str(pdf), str(png)],
                           check=True)
            imgs = [f"{png}.png"]
            if args.partir > 1:
                from PIL import Image
                im = Image.open(f"{png}.png")
                alto, solape = im.height / args.partir, int(im.height * 0.03)
                imgs = []
                for k in range(args.partir):
                    caja = (0, max(0, int(k * alto) - solape), im.width,
                            min(im.height, int((k + 1) * alto) + solape))
                    f = pathlib.Path(tmp) / f"franja{k}.png"
                    franja = im.crop(caja)
                    franja.thumbnail((2048, 2048))
                    franja.save(f)
                    imgs.append(str(f))
            t0 = time.time()
            textos, tokens, truncada = [], 0, False
            for img in imgs:
                r = generate(model, processor, prompt, image=[img],
                             max_tokens=args.max_tokens, temperature=0.0, verbose=False)
                n = getattr(r, "generation_tokens", None) or 0
                textos.append(r.text)
                tokens += n
                truncada |= n >= args.max_tokens
            seg = round(time.time() - t0, 1)
            d = SALIDA / pdf.stem
            d.mkdir(parents=True, exist_ok=True)
            (d / f"p{p:02d}.md").write_text("\n\n".join(textos))
            idx_f = d / "indice.json"
            idx = json.loads(idx_f.read_text()) if idx_f.exists() else {}
            idx[str(p)] = {"pagina_impresa": imp, "segundos": seg, "tokens": tokens,
                           "truncada": truncada, "franjas": len(imgs), "modelo": MODELO}
            idx_f.write_text(json.dumps(idx, ensure_ascii=False, indent=1))
            print(f"[{i}/{len(pend)}] {pdf.stem} p{p:02d} (impresa {imp or '?'}): "
                  f"{seg} s, {tokens} tokens", flush=True)


if __name__ == "__main__":
    main()
