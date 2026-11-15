"""F4 · Gobiernos durante la guerra (1936-1938), en los diarios oficiales de las dos zonas.

Evidencia:
  - Gaceta de Madrid / Gaceta de la República, PDF de la ruta permitida /gazeta/dias/ (texto comprobado
    con scripts/etl/pdf_buscar.py sobre el PDF).
  - BOE editado en Burgos, fichas doc.php (título y publicación; el texto no se ha consultado).
Las afirmaciones se limitan a lo que dice cada documento: nombramientos, firmas y lugar de fecha.

Uso: python3 -I scripts/etl/eventos_gobiernos_guerra.py   (idempotente)
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eventos_1934_1935 import OUT, RIGHTS, REV_PDF, REV_FICHA, larga, write  # noqa: E402

GACETAS = [
    ("1936-09-05", "GMD-1936-249", "Gaceta de Madrid", 249, "1671-1672", "nombramiento del Gobierno de Francisco Largo Caballero",
     "Decretos de 4 de septiembre de 1936, firmados por Manuel Azaña, que admiten las dimisiones del Gobierno anterior y nombran presidente del Consejo de Ministros y ministro de la Guerra a Francisco Largo Caballero y a los ministros de su Gobierno."),
    ("1937-05-18", "GRP-1937-138", "Gaceta de la República", 138, "751-752", "nombramiento del Gobierno de Juan Negrín",
     "Decretos dados en Valencia el 17 de mayo de 1937, firmados por Manuel Azaña, que admiten las dimisiones del Gobierno de Largo Caballero y nombran presidente del Consejo de Ministros y ministro de Hacienda y Economía a Juan Negrín López."),
]
FICHAS = [
    {"id": "BOE-A-1938-1406", "title": "Ley organizando la Administración Central del Estado.", "num": 467, "date": "1938-01-31", "pages": "5514 a 5515", "dept": "Gobierno del Estado"},
    {"id": "BOE-A-1938-1424", "title": "Decreto núm. 453 nombrando Ministro de Vicepresidente del Gobierno de la Nación al Teniente General D. Francisco Gómez Jordana y Sousa.", "num": 468, "date": "1938-02-01", "pages": "5547 a 5547", "dept": "Jefatura del Estado"},
    {"id": "BOE-A-1938-1417", "title": "Decreto núm. 446 nombrando Ministro del Interior a D. Ramón Serrano Suñer.", "num": 468, "date": "1938-02-01", "pages": "5547 a 5547", "dept": "Jefatura del Estado"},
]
CONTEXT_BOE = ("Boletín Oficial del Estado editado en Burgos por las autoridades de la zona sublevada desde el 2 de octubre de 1936. "
               "Acredita las normas que dictaban esas autoridades, no su aplicación ni sus efectos.")
EVENTOS = [
    ("evt-1936-09-04-gobierno-largo-caballero", "Gobierno de Francisco Largo Caballero", "politico", "1936-09-04", REV_PDF, [
        ("La Gaceta de Madrid del 5 de septiembre de 1936 publica el decreto de 4 de septiembre por el que Manuel Azaña, en uso de las atribuciones del artículo 75 de la Constitución, nombra presidente del Consejo de Ministros y ministro de la Guerra a Francisco Largo Caballero.", "doc-gaceta-1936-09-05", "pág. 1671"),
        ("Los decretos del mismo día nombran a los demás ministros del nuevo Gobierno, entre ellos a Jesús Hernández Tomás en Instrucción Pública y Bellas Artes.", "doc-gaceta-1936-09-05", "pág. 1672")]),
    ("evt-1937-05-17-gobierno-negrin", "Gobierno de Juan Negrín", "politico", "1937-05-17", REV_PDF, [
        ("La Gaceta de la República del 18 de mayo de 1937 publica un decreto dado en Valencia el 17 de mayo de 1937 por el que Manuel Azaña, en uso de las atribuciones del artículo 75 de la Constitución, nombra presidente del Consejo de Ministros y ministro de Hacienda y Economía a Juan Negrín López.", "doc-gaceta-1937-05-18", "pág. 751"),
        ("Decretos del mismo día, también fechados en Valencia, admiten la dimisión de los ministros del Gobierno anterior, entre ellos Indalecio Prieto en Marina y Aire.", "doc-gaceta-1937-05-18", "pág. 751")]),
    ("evt-1938-01-30-administracion-central-burgos", "Primer Gobierno de la zona sublevada", "politico", "1938-01-31", REV_FICHA, [
        ("El BOE editado en Burgos publica el 31 de enero de 1938 la «Ley organizando la Administración Central del Estado», del Gobierno del Estado.", "doc-boe-a-1938-1406", "págs. 5514 a 5515"),
        ("El BOE del 1 de febrero de 1938 publica los decretos de la Jefatura del Estado que nombran a los ministros, entre ellos al teniente general Francisco Gómez Jordana y Sousa como vicepresidente del Gobierno.", "doc-boe-a-1938-1424", "pág. 5547"),
        ("Otro decreto del mismo número nombra ministro del Interior a Ramón Serrano Suñer.", "doc-boe-a-1938-1417", "pág. 5547")]),
]


def main() -> None:
    for fecha, ident, diario, num, pags, corto, resumen in GACETAS:
        y, m, d = fecha.split("-")
        write("documents", {
            "id": f"doc-gaceta-{fecha}", "title": f"{diario} n.º {num}, {larga(fecha)}: {corto}",
            "title_original": f"{diario}. Núm. {num}", "document_type": "disposicion", "source_ids": ["F015"],
            "custodian": "Agencia Estatal Boletín Oficial del Estado (colección histórica Gazeta)",
            "signature": f"{diario}, núm. {num}, {d}/{m}/{y}, págs. {pags}",
            "canonical_url": f"https://www.boe.es/gazeta/dias/{y}/{m}/{d}/pdfs/{ident}.pdf",
            "date": fecha, "date_precision": "dia", "place_ids": ["plc-espana"],
            "summary": resumen,
            "context": "Diario oficial del Gobierno de la República. Acredita los nombramientos y su fecha y lugar de firma, no la actuación de los gobiernos.",
            "text_origin": "ocr_automatico",
            "rights": dict(RIGHTS, note="Normas oficiales excluidas de propiedad intelectual (art. 13 LPI); se enlaza al ejemplar de la sede del BOE."),
            "review": dict(REV_PDF), "consulted_at": "2026-11-15"})
    for f in FICHAS:
        write("documents", {
            "id": f"doc-{f['id'].lower()}", "title": f"BOE n.º {f['num']}, {larga(f['date'])}: {f['title'].rstrip('.')}",
            "title_original": f["title"], "document_type": "disposicion", "source_ids": ["F015"],
            "custodian": "Agencia Estatal Boletín Oficial del Estado",
            "signature": f"{f['id']} · «Boletín Oficial del Estado», núm. {f['num']}, {larga(f['date'])}, págs. {f['pages']} · {f['dept']}",
            "canonical_url": f"https://www.boe.es/buscar/doc.php?id={f['id']}",
            "date": f["date"], "date_precision": "dia", "place_ids": ["plc-espana"],
            "summary": f"Disposición de {f['dept']} publicada en el BOE núm. {f['num']} de {larga(f['date'])}, págs. {f['pages']}: «{f['title'].rstrip('.')}».",
            "context": CONTEXT_BOE, "text_origin": "ninguno",
            "rights": dict(RIGHTS, note="Normas oficiales excluidas de propiedad intelectual (art. 13 LPI); se enlaza a la ficha oficial."),
            "review": dict(REV_FICHA), "consulted_at": "2026-11-15"})
    for eid, titulo, tipo, fecha, rev, claims in EVENTOS:
        write("events", {"id": eid, "title": titulo, "event_type": tipo, "start_date": fecha, "date_precision": "dia",
                         "place_ids": ["plc-espana"], "spatial_precision": "estatal",
                         "claims": [{"text": t, "kind": "documento", "evidence": [{"document_id": d, "locator": loc}]} for t, d, loc in claims],
                         "review": dict(rev)})
    print(f"{len(GACETAS) + len(FICHAS)} documentos, {len(EVENTOS)} acontecimientos")


if __name__ == "__main__":
    main()
