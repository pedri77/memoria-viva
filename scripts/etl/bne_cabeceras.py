"""F1 · Fichas de cabeceras de prensa 1931-1939 con texto completo en la Hemeroteca Digital (BNE).

Entrada: data/external/bne/hemeroteca_fulltext_2026-11-14.csv
  («Hemeroteca digital. Texto completo», BNE, datos.gob.es, CC BY 4.0)
Criterio: cabeceras con enlace a texto completo, editadas en España, con al menos 5 años
publicados dentro de 1931-1939; se toman las de mayor cobertura hasta MAX fichas.

Sesgo declarado: la BNE solo ofrece texto completo de cabeceras en dominio público, así que
faltan grandes diarios del periodo (ABC, Ya, Informaciones, Mundo Obrero, La Vanguardia,
Arriba España…). La selección no es representativa de la prensa de la época.

Uso: python3 -I scripts/etl/bne_cabeceras.py
"""
import csv
import json
import pathlib
import re
import unicodedata

ROOT = pathlib.Path(__file__).resolve().parents[2]
SRC = ROOT / "data/external/bne/hemeroteca_fulltext_2026-11-14.csv"
OUT = ROOT / "data/canonical/documents"
TODAY = "2026-11-14"
MAX = 84
NO_ESPANA = {"Argentina", "Francia", "Suiza", "México", "Cuba", "Estados Unidos", "Reino Unido", "Chile",
             "Uruguay", "Brasil", "Bélgica", "Italia", "Alemania", "Portugal", "Filipinas", "Puerto Rico", "Marruecos"}
# Ámbito geográfico (provincia, nombre BNE) -> código de provincia de 1930
PROV = {"Álava": "01", "Albacete": "02", "Alicante": "03", "Almería": "04", "Ávila": "05", "Badajoz": "06",
        "Baleares": "07", "Islas Baleares": "07", "Barcelona": "08", "Burgos": "09", "Cáceres": "10", "Cádiz": "11",
        "Castellón": "12", "Ciudad Real": "13", "Córdoba": "14", "La Coruña": "15", "Coruña": "15", "Cuenca": "16",
        "Gerona": "17", "Girona": "17", "Granada": "18", "Guadalajara": "19", "Guipúzcoa": "20", "Huelva": "21",
        "Huesca": "22", "Jaén": "23", "León": "24", "Lérida": "25", "Lleida": "25", "La Rioja": "26", "Logroño": "26",
        "Lugo": "27", "Madrid": "28", "Málaga": "29", "Murcia": "30", "Navarra": "31", "Orense": "32", "Ourense": "32",
        "Asturias": "33", "Oviedo": "33", "Palencia": "34", "Las Palmas": "35", "Pontevedra": "36", "Salamanca": "37",
        "Santa Cruz de Tenerife": "38", "Cantabria": "39", "Santander": "39", "Segovia": "40", "Sevilla": "41",
        "Soria": "42", "Tarragona": "43", "Teruel": "44", "Toledo": "45", "Valencia": "46", "Valladolid": "47",
        "Vizcaya": "48", "Bizkaia": "48", "Zamora": "49", "Zaragoza": "50", "Ceuta": "51", "Melilla": "52"}


def slug(s: str) -> str:
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:48].strip("-")


def span(f: str):
    d = re.findall(r"(\d{2})/(\d{2})/(\d{4})", f)
    if not d:
        return None
    a = f"{d[0][2]}-{d[0][1]}-{d[0][0]}"
    b = f"{d[1][2]}-{d[1][1]}-{d[1][0]}" if len(d) > 1 else None
    return a, b


def main() -> None:
    rows = list(csv.DictReader(SRC.open(encoding="utf-8-sig"), delimiter=";"))
    cand = []
    for r in rows:
        s = span(r["Fecha"])
        url = r["Enlace al texto completo (txt)"]
        if not s or not url or r["Ámbito geográfico"] in NO_ESPANA:
            continue
        a, b = max(s[0], "1931-01-01"), min(s[1] or "9999", "1939-12-31")
        years = int(b[:4]) - int(a[:4]) + 1
        if a <= b and years >= 5:
            cand.append((years, r, s))
    cand.sort(key=lambda x: (-x[0], x[1]["Título"]))
    n = 0
    for _, r, (a, b) in cand[:MAX]:
        issn = r["ISSN"]
        did = f"doc-bne-{issn.lower()}-{slug(r['Título'])}".rstrip("-")
        prov = PROV.get(r["Ámbito geográfico"])
        obj = {
            "id": did,
            "title": f"{r['Título']} (cabecera de prensa, Hemeroteca Digital BNE)",
            "title_original": r["Título"],
            "document_type": "prensa",
            "source_ids": ["F007"],
            "custodian": "Biblioteca Nacional de España, Hemeroteca Digital",
            "signature": f"ISSN {issn}",
            "canonical_url": r["Enlace al texto completo (txt)"].replace("http://", "https://"),
            "date": a,
            "date_end": b or "2026",
            "date_precision": "intervalo",
            "place_ids": [f"plc-prov-{prov}"] if prov else ["plc-espana"],
            "summary": f"Cabecera publicada entre {a[:4]} y {(b or 'hoy')[:4]} con texto completo (OCR) descargable en la Hemeroteca Digital. Ámbito: {r['Ámbito geográfico']}. Idioma: {r['Idioma']}.",
            "context": "La prensa refleja la línea de su empresa o partido y la censura de cada momento; no valida por sí sola los hechos que narra. "
                       "La BNE solo ofrece texto completo de cabeceras en dominio público: faltan grandes diarios del periodo (ABC, Ya, Informaciones, Mundo Obrero, La Vanguardia, Arriba España), así que esta colección no es representativa.",
            "text_origin": "ocr_automatico",
            "rights": {"status": "cc_by", "action": "enlazar",
                       "attribution": "Biblioteca Nacional de España, «Hemeroteca digital. Texto completo» (datos.gob.es, CC BY 4.0)",
                       "evidence_url": "https://datos.gob.es/catalogo/ea0019768-hemeroteca-digital-texto-completo1",
                       "checked_at": TODAY,
                       "note": "Metadatos y texto completo con CC BY 4.0. El servidor de la BNE bloquea clientes automáticos: el enlace es para lectores humanos."},
            "review": {"status": "revision", "date": TODAY, "by": ["autor"],
                       "note": "Generado desde el CSV oficial de la BNE (scripts/etl/bne_cabeceras.py)."},
            "consulted_at": TODAY,
        }
        if r["Ámbito geográfico"] not in PROV:
            obj["review"]["note"] += f" Ámbito «{r['Ámbito geográfico']}» sin provincia asignada."
        (OUT / f"{did}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        n += 1
    print(f"{n} fichas de cabecera (de {len(cand)} candidatas)")


if __name__ == "__main__":
    main()
