"""Busca expresiones en un PDF página a página (pdftotext) tolerando OCR y tildes.

Uso: python3 -I scripts/etl/pdf_buscar.py FICHERO.pdf "expresión 1" ["expresión 2" ...]
Imprime: página física del PDF, número de página impreso (si aparece en cabecera) y contexto.
"""
import re
import subprocess
import sys
import unicodedata


def norm(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[­\-]\s*\n\s*", "", s)  # guiones de corte de línea
    return re.sub(r"\s+", " ", s)


def main() -> None:
    pdf, *exprs = sys.argv[1:]
    n = int(re.search(r"Pages:\s+(\d+)", subprocess.run(["pdfinfo", pdf], capture_output=True, text=True).stdout).group(1))
    for p in range(1, n + 1):
        raw = subprocess.run(["pdftotext", "-f", str(p), "-l", str(p), pdf, "-"], capture_output=True, text=True).stdout
        t = norm(raw)
        impresa = re.match(r"\s*(\d{1,4})\b", raw)
        for e in exprs:
            m = re.search(re.escape(norm(e)).replace(r"\ ", r"\s*"), t)
            if m:
                ctx = t[max(0, m.start() - 160): m.end() + 260]
                print(f"[pág. PDF {p}/{n}, impresa {impresa.group(1) if impresa else '?'}] «{e}»: …{ctx}…")


if __name__ == "__main__":
    main()
