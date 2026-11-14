"""Localiza ejemplares completos de la Gaceta en la ruta permitida por robots.txt de boe.es.

Ruta: https://www.boe.es/gazeta/dias/AAAA/MM/DD/pdfs/<PREFIJO>-AAAA-NNN.pdf
(robots.txt de boe.es prohíbe /buscar/gazeta.php? y /datos/pdfs/, no /gazeta/dias/).

Uso: python3 -I scripts/etl/gazeta_localizar.py AAAA-MM-DD [PREFIJO] [CACHE_DIR]
Prueba números de ejemplar alrededor del día del año con peticiones HEAD espaciadas,
descarga el PDF encontrado al directorio de caché (no se publica) e imprime la URL.
"""
import datetime
import pathlib
import sys
import time
import urllib.request

UA = "memoria-viva/0.1 (+https://github.com/pedri77/memoria-viva)"
PAUSA = 1.5


def head(url: str) -> bool:
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": UA})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return r.status == 200 and "pdf" in r.headers.get("Content-Type", "")
    except Exception:
        return False
    finally:
        time.sleep(PAUSA)


def localizar(fecha: str, prefijo: str = "GMD", cache: str | None = None) -> str | None:
    d = datetime.date.fromisoformat(fecha)
    doy = d.timetuple().tm_yday
    base = f"https://www.boe.es/gazeta/dias/{d:%Y/%m/%d}/pdfs/{prefijo}-{d.year}-"
    for delta in (0, -1, 1, -2, 2, -3, 3, -4, 4, -5, 5, -6, 6):
        n = doy + delta
        if n < 1:
            continue
        url = f"{base}{n:03d}.pdf"
        if head(url):
            if cache:
                dest = pathlib.Path(cache) / f"{prefijo}-{fecha}.pdf"
                if not dest.exists():
                    req = urllib.request.Request(url, headers={"User-Agent": UA})
                    with urllib.request.urlopen(req, timeout=120) as r:
                        dest.write_bytes(r.read())
                    time.sleep(PAUSA)
            return url
    return None


if __name__ == "__main__":
    fecha = sys.argv[1]
    pref = sys.argv[2] if len(sys.argv) > 2 else "GMD"
    cache = sys.argv[3] if len(sys.argv) > 3 else None
    print(localizar(fecha, pref, cache) or "NO ENCONTRADO")
