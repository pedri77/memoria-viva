"""Genera data/canonical/sources/F###.json a partir de data/canonical/source_registry.csv.

Uso: python3 -I scripts/etl/registry_to_sources.py
"""
import csv
import json
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]
REG = ROOT / "data/canonical/source_registry.csv"
OUT = ROOT / "data/canonical/sources"
CHECKED_AT = "2026-11-14"


def first_url(*vals):
    for v in vals:
        m = re.search(r"https?://\S+", v or "")
        if m:
            return m.group(0).rstrip(";,")
    return None


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    n = 0
    for r in csv.DictReader(REG.open(encoding="utf-8")):
        url = first_url(r["url_verificada"], r["url_doc"])
        if not url:
            continue
        obj = {
            "id": r["id"],
            "name": r["fuente"],
            "url": url,
            "priority": r["prioridad_propuesta"],
            "status": r["estado"],
            "license": r["licencia_metadatos"] or "por verificar",
            "access": r["acceso_verificado"] + (f"; {r['api_o_descarga']}" if r["api_o_descarga"] not in ("", "n/a") else ""),
            "years": r["anios"],
            "risks": r["riesgos"],
            "checked_at": CHECKED_AT,
        }
        (OUT / f"{r['id']}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        n += 1
    print(f"{n} fuentes escritas en {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
