# /// script
# requires-python = ">=3.11"
# dependencies = ["mlx-vlm>=0.7.12", "torch", "torchvision"]
# ///
"""Piloto OCR en local (Apple Silicon, MLX): LightOnOCR-3 sobre las páginas de manifiesto.json.

Gratis y sin sacar nada del Mac. Usa los pesos oficiales de lightonai (bf16) salvo que se
indique otro repo. Modo plain: imagen sin texto de prompt, salida markdown.

Uso:
  uv run scripts/ocr_piloto/local_mlx.py 0.8B            # las 20 páginas
  uv run scripts/ocr_piloto/local_mlx.py 4B --solo GMD-1931-130-p03
Salida: data/raw/ocr_piloto/salida-{0.8b|4b}.jsonl (id, markdown, segundos, tokens).
Reanuda: salta los id que ya estén en el jsonl.
"""
import argparse
import json
import pathlib
import time

RAIZ = pathlib.Path(__file__).resolve().parents[2]
DIR = RAIZ / "data/raw/ocr_piloto"


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("modelo", choices=["0.8B", "4B"])
    ap.add_argument("--repo", help="repo MLX alternativo (p. ej. cuantizado)")
    ap.add_argument("--max-tokens", type=int, default=6144)
    ap.add_argument("--solo", nargs="*", help="ids concretos")
    args = ap.parse_args()

    from mlx_vlm import generate, load
    from mlx_vlm.prompt_utils import apply_chat_template

    repo = args.repo or f"lightonai/LightOnOCR-3-{args.modelo}"
    model, processor = load(repo)
    salida = DIR / f"salida-{args.modelo.lower()}.jsonl"
    hechos = {json.loads(l)["id"] for l in salida.open()} if salida.exists() else set()

    paginas = json.loads((DIR / "manifiesto.json").read_text())
    for p in paginas:
        if p["id"] in hechos or (args.solo and p["id"] not in args.solo):
            continue
        prompt = apply_chat_template(processor, model.config, "", num_images=1)
        t0 = time.time()
        r = generate(model, processor, prompt, image=[p["png"]],
                     max_tokens=args.max_tokens, temperature=0.0, verbose=False)
        seg = round(time.time() - t0, 1)
        tokens = getattr(r, "generation_tokens", None)
        with salida.open("a") as fh:
            fh.write(json.dumps({"id": p["id"], "markdown": r.text, "segundos": seg,
                                 "tokens": tokens, "repo": repo}, ensure_ascii=False) + "\n")
        print(f"{p['id']}: {seg} s, {tokens} tokens", flush=True)


if __name__ == "__main__":
    main()
