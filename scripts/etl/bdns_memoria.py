"""Ayudas públicas de memoria democrática a entidades locales, por provincia y año (BDNS).

Entrada: data/external/bdns/*.csv (scripts/etl/bdns_memoria_descarga.py).
Salidas: data/canonical/sources/F060.json, data/canonical/documents/doc-bdns-memoria-democratica.json,
         data/canonical/indicators/ind-subv-memoria-local-prov.json

Provincia: la del NIF de la entidad local beneficiaria (letra P + código INE de provincia, o ese código + 50
en las numeraciones ampliadas, + código de municipio). Solo entidades locales: en asociaciones o universidades el NIF no da la provincia con
seguridad. Los demás beneficiarios se resumen en la página /memoria-hoy/.

Comprobaciones: cada concesión remite a una convocatoria descargada; NIF de entidad local con
provincia válida; importes no negativos.

Uso: python3 -I scripts/etl/bdns_memoria.py
"""
import collections
import csv
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
SRC = ROOT / "data/external/bdns"
EXTRACCION = "2026-11-15"
DID = "doc-bdns-memoria-democratica"


def prov_nif(nif: str, provs: set) -> str:
    """Provincia del NIF de una entidad local: P + código INE de provincia. Cuando se agotaron los números,
    se asignaron códigos ampliados (provincia + 50: 58 Barcelona, 61 Cádiz, 67 Gerona, 75 Lérida,
    84 Palencia, 86 Pontevedra, 93 Tarragona), comprobados con el nombre de cada entidad."""
    c = nif[1:3]
    if c in provs:
        return c
    c2 = f"{int(c) - 50:02d}"
    assert c2 in provs, f"provincia desconocida en {nif}"
    return c2


def main() -> None:
    conv = {r["numero_convocatoria"]: r for r in csv.DictReader((SRC / "convocatorias_memoria.csv").open(encoding="utf-8"))}
    provs = {p.stem.replace("plc-prov-", "") for p in (OUT / "places").glob("plc-prov-*.json")}
    suma = collections.defaultdict(float)
    anios = set()
    for r in csv.DictReader((SRC / "concesiones_entidades.csv").open(encoding="utf-8")):
        assert r["numero_convocatoria"] in conv, f"concesión {r['cod_concesion']} sin convocatoria"
        imp = float(r["importe"] or 0)
        assert imp >= 0, f"importe negativo en {r['cod_concesion']}"
        y = r["fecha_concesion"][:4]
        anios.add(y)
        if r["nif"].startswith("P"):
            c = prov_nif(r["nif"], provs)
            suma[(c, y)] += imp
    (OUT / "sources/F060.json").write_text(json.dumps({
        "id": "F060", "name": "Base de Datos Nacional de Subvenciones (SNPSAP, IGAE)",
        "url": "https://www.infosubvenciones.es/bdnstrans/GE/es/index",
        "priority": "P1", "status": "pilot",
        "license": "reutilización según el aviso legal del SNPSAP (Ley 37/2007), con cita «Origen de los datos: Intervención General de la Administración del Estado»",
        "access": "API JSON del portal (convocatorias/busqueda y concesiones/busqueda); sin robots.txt publicado; una petición por segundo",
        "years": "convocatorias desde 2016; concesiones visibles desde 2022",
        "risks": "datos dinámicos que la fuente puede corregir o retirar; las concesiones solo se publican durante un plazo limitado; títulos con datos personales; búsqueda por palabras clave",
        "checked_at": EXTRACCION}, ensure_ascii=False, indent=2) + "\n")
    (OUT / f"documents/{DID}.json").write_text(json.dumps({
        "id": DID,
        "title": f"Convocatorias y concesiones de memoria democrática en la Base de Datos Nacional de Subvenciones (extracción del {EXTRACCION[8:10]}-{EXTRACCION[5:7]}-{EXTRACCION[:4]})",
        "title_original": "Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas: convocatorias y concesiones",
        "document_type": "tabla_estadistica", "source_ids": ["F060"],
        "custodian": "Intervención General de la Administración del Estado (IGAE), Ministerio de Hacienda",
        "signature": f"Búsqueda por los términos de scripts/etl/bdns_memoria_descarga.py; {len(conv)} convocatorias y sus concesiones",
        "canonical_url": "https://www.infosubvenciones.es/bdnstrans/GE/es/convocatorias",
        "date": EXTRACCION, "date_precision": "dia", "place_ids": ["plc-espana"],
        "summary": "Convocatorias de subvenciones y ayudas públicas de las administraciones estatal, autonómica y local cuyo título se refiere a la memoria democrática o histórica, la Guerra Civil, el franquismo, las fosas o la simbología franquista, y las concesiones registradas.",
        "context": "Registro administrativo de publicidad de subvenciones. Recoge lo que cada administración inscribe; la búsqueda por palabras del título puede dejar fuera ayudas con otros títulos. Las concesiones solo son visibles desde 2022.",
        "text_origin": "ninguno",
        "rights": {"status": "reuse_open", "action": "almacenar",
                   "attribution": "Origen de los datos: Intervención General de la Administración del Estado",
                   "evidence_url": "https://www.infosubvenciones.es/bdnstrans/GE/es/avisolegal", "checked_at": EXTRACCION,
                   "note": "El aviso legal permite la reutilización con fines comerciales y no comerciales citando la fuente y la fecha; los datos personales solo con fines históricos, estadísticos o científicos y disociados. No se publican nombres de personas ni títulos de convocatorias."},
        "review": {"status": "revision", "date": EXTRACCION, "by": ["autor"],
                   "note": "Extracción automática; clasificación temática aproximada por palabras clave del título."},
        "consulted_at": EXTRACCION}, ensure_ascii=False, indent=2) + "\n")
    obs = []
    for y in sorted(anios):
        for c in sorted(provs):
            o = {"place_id": f"plc-prov-{c}", "period": y, "value": round(suma.get((c, y), 0.0)), "document_id": DID,
                 "locator": f"concesiones de {y} a beneficiarios con NIF de entidad local (P{c}…), convocatorias de memoria democrática"}
            if y == EXTRACCION[:4]:
                o["uncertainty"] = f"Año incompleto: datos hasta el {EXTRACCION[8:10]}-{EXTRACCION[5:7]}-{EXTRACCION[:4]}."
            obs.append(o)
    (OUT / "indicators/ind-subv-memoria-local-prov.json").write_text(json.dumps({
        "id": "ind-subv-memoria-local-prov", "concept": "Ayudas de memoria democrática a ayuntamientos y entidades locales",
        "definition": "Importe de las concesiones registradas en la Base de Datos Nacional de Subvenciones a ayuntamientos y otras entidades locales de cada provincia, en convocatorias cuyo título se refiere a la memoria democrática o histórica, la Guerra Civil, el franquismo, las fosas o la simbología franquista.",
        "unit": "euros", "denominator": "ninguno (importe absoluto)",
        "method": "Suma de importes por año de concesión y provincia del NIF de la entidad local beneficiaria (scripts/etl/bdns_memoria.py). Las concesiones a asociaciones, universidades, empresas y personas se resumen aparte en /memoria-hoy/.",
        "source_ids": ["F060"],
        "comparability_notes": "Es un dato de hoy, no del periodo 1931-1939. Cero significa que no hay concesiones registradas con esos términos, no que no se hiciera nada: la búsqueda depende del título y las concesiones solo son visibles desde 2022. Los importes son los concedidos, no los pagados. Origen de los datos: Intervención General de la Administración del Estado.",
        "review": {"status": "revision", "date": EXTRACCION, "by": ["autor"], "note": "Generado por scripts/etl/bdns_memoria.py."},
        "observations": obs}, ensure_ascii=False, indent=2) + "\n")
    tot = sum(suma.values())
    print(f"{len(conv)} convocatorias; a entidades locales {tot:,.0f} € en {len({c for c, _ in suma})} provincias")


if __name__ == "__main__":
    main()
