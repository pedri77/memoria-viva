"""F4 · Acontecimientos de 1934-1935 (bienio de gobiernos radicales y cedistas).

Evidencia: ejemplares de la Gaceta de Madrid descargados por la ruta permitida
/gazeta/dias/AAAA/MM/DD/pdfs/ (texto comprobado sobre el PDF) y, cuando el ejemplar no está
en esa ruta, fichas https://www.boe.es/buscar/doc.php?id=BOE-A-AAAA-N (solo título y datos de
publicación, sin texto). Las afirmaciones se limitan a lo que dice cada documento.

Uso: python3 -I scripts/etl/eventos_1934_1935.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
OUT = ROOT / "data/canonical"
TODAY = "2026-11-15"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
RIGHTS = {"status": "reuse_conditions", "action": "enlazar",
          "attribution": "Fuente: Agencia Estatal Boletín Oficial del Estado, www.boe.es",
          "evidence_url": "https://www.boe.es/informacion/aviso_legal/index.php", "checked_at": TODAY}
REV_PDF = {"status": "revision", "date": TODAY, "by": ["autor"],
           "note": "Comprobado sobre el PDF del ejemplar (OCR del BOE). Pendiente de segunda revisión humana."}
REV_FICHA = {"status": "revision", "date": TODAY, "by": ["autor"],
             "note": "Título, número, fecha y páginas leídos en la ficha oficial del BOE. Texto completo no consultado; pendiente de lectura humana."}
CAT = ["plc-prov-08", "plc-prov-17", "plc-prov-25", "plc-prov-43"]

# Ejemplares completos: (fecha, número, páginas, título corto, resumen, contexto)
GACETAS = [
    ("1934-04-25", 115, "548-549", "ley de amnistía",
     "Ley que concede amnistía por los hechos que enumera en sus apartados, entre ellos los delitos de imprenta, los de rebelión y sedición, los cometidos con ocasión de conflictos sociales, huelgas o paros y los electorales, con excepciones.",
     "Ley aprobada por las Cortes elegidas en noviembre de 1933 y promulgada por el presidente de la República."),
    ("1934-08-30", 242, "1872-1874", "nuevo plan de estudios del Bachillerato",
     "Decreto del Ministerio de Instrucción Pública, de 29 de agosto de 1934, que establece un Bachillerato de siete cursos dividido en dos ciclos, de tres y cuatro cursos, con un examen de conjunto al final del tercero y una reválida.",
     "Disposición del Gobierno. El preámbulo expone los motivos del propio Ministerio."),
    ("1934-10-05", 278, "178-179", "nombramiento del Gobierno presidido por Alejandro Lerroux",
     "Decretos de 4 de octubre de 1934 que admiten la dimisión de Ricardo Samper Ibáñez como presidente del Consejo de Ministros y de sus ministros, nombran presidente a Alejandro Lerroux García y nombran a los ministros del nuevo Gobierno.",
     "Decretos del presidente de la República."),
    ("1935-08-10", 222, "1288-1291", "ley de reforma de la de Reforma agraria",
     "Ley llamada «de reforma de la de Reforma agraria», que modifica la ley de 15 de septiembre de 1932: deroga su base 7.ª y anula el inventario de fincas formado por el Instituto de Reforma Agraria en cumplimiento de ella.",
     "Ley aprobada por las Cortes elegidas en noviembre de 1933."),
]
# Fichas sin texto: (id BOE, metadatos leídos en la ficha)
FICHAS = [
    {"id": "BOE-A-1935-101", "title": "Ley dejando en suspenso las facultades concedidas por el Estatuto de Cataluña al Parlamento de la Generalidad, hasta que las Cortes, a propuesta del Gobierno y después de levantada la suspensión de garantías constitucionales, acuerden el restablecimiento gradual del régimen autonómico.",
     "diario": "Gaceta de Madrid", "num": 3, "date": "1935-01-03", "pages": "82 a 83", "dept": "Presidencia del Consejo de Ministros", "places": ["plc-espana", *CAT]},
    {"id": "BOE-A-1935-2712", "title": "Ley relativa a contratos de arrendamientos de fincas rústicas.",
     "diario": "Gaceta de Madrid", "num": 83, "date": "1935-03-24", "pages": "2346 a 2351", "dept": "Ministerio de Agricultura", "places": ["plc-espana"]},
]

EVENTOS = [
    ("evt-1934-04-25-ley-amnistia", "Ley de amnistía de 1934", "legislativo", "1934-04-25", None, ["plc-espana"], [
        ("La Gaceta del 25 de abril de 1934 publica una ley que concede amnistía por los hechos que enumera, entre ellos los delitos y faltas cometidos por medio de la imprenta o de la palabra, los de sedición y rebelión, los cometidos con motivo de conflictos sociales, huelgas o paros y los relacionados con elecciones.", "doc-gaceta-1934-04-25", "artículo único, apartados 1.º, 3.º, 9.º y 14, pág. 548"),
        ("La ley excluye de varios de esos apartados los delitos contra la vida y la integridad corporal que constituyeran homicidio o lesiones graves.", "doc-gaceta-1934-04-25", "apartados 9.º y 14, pág. 548")]),
    ("evt-1934-08-29-plan-bachillerato", "Nuevo plan de estudios del Bachillerato", "educativo", "1934-08-29", None, ["plc-espana"], [
        ("Un decreto de 29 de agosto de 1934, publicado en la Gaceta del día siguiente, establece que el Bachillerato se desarrollará en siete cursos, divididos en un primer ciclo de tres y un segundo de cuatro.", "doc-gaceta-1934-08-30", "preámbulo y art. 1.º, pág. 1872"),
        ("El preámbulo introduce un examen de conjunto al final del tercer curso para orientar a otros estudios a los alumnos que, según el Ministerio, no tengan capacidad o vocación; el decreto exige además una reválida al final, con diecisiete años cumplidos.", "doc-gaceta-1934-08-30", "preámbulo, págs. 1872-1873")]),
    ("evt-1934-10-04-gobierno-lerroux", "Nombramiento del Gobierno presidido por Alejandro Lerroux", "politico", "1934-10-04", None, ["plc-espana"], [
        ("Decretos de 4 de octubre de 1934, publicados en la Gaceta del día 5, admiten la dimisión de Ricardo Samper Ibáñez como presidente del Consejo de Ministros y nombran para el cargo a Alejandro Lerroux García.", "doc-gaceta-1934-10-05", "pág. 178"),
        ("Otros decretos del mismo número admiten la dimisión de los ministros del Gobierno saliente y nombran a los del nuevo.", "doc-gaceta-1934-10-05", "págs. 178-179")]),
    ("evt-1935-01-03-suspension-estatuto-cataluna", "Suspensión de las facultades del Parlamento de Cataluña", "politico", "1935-01-03", None, ["plc-espana", *CAT], [
        ("La Gaceta del 3 de enero de 1935 publica una ley que deja en suspenso las facultades concedidas por el Estatuto de Cataluña al Parlamento de la Generalidad hasta que las Cortes, a propuesta del Gobierno y después de levantada la suspensión de garantías constitucionales, acuerden el restablecimiento gradual del régimen autonómico.", "doc-boe-a-1935-101", "págs. 82 a 83")]),
    ("evt-1935-03-24-arrendamientos-rusticos", "Ley de arrendamientos de fincas rústicas", "economico", "1935-03-24", None, ["plc-espana"], [
        ("La Gaceta del 24 de marzo de 1935 publica la «Ley relativa a contratos de arrendamientos de fincas rústicas», del Ministerio de Agricultura.", "doc-boe-a-1935-2712", "págs. 2346 a 2351")]),
    ("evt-1935-08-10-reforma-reforma-agraria", "Ley de reforma de la Reforma agraria", "economico", "1935-08-10", None, ["plc-espana"], [
        ("La Gaceta del 10 de agosto de 1935 publica la ley llamada «de reforma de la de Reforma agraria», que mantiene en vigor la ley de 15 de septiembre de 1932 con modificaciones.", "doc-gaceta-1935-08-10", "art. 1.º, pág. 1288"),
        ("Entre ellas, deroga la base 7.ª de la ley de 1932 y anula el inventario de fincas formado por el Instituto de Reforma Agraria en cumplimiento de esa base.", "doc-gaceta-1935-08-10", "art. 1.º, pág. 1288")]),
]


def larga(d: str) -> str:
    y, m, dd = d.split("-")
    return f"{int(dd)} de {MESES[int(m) - 1]} de {y}"


def write(kind: str, obj: dict) -> None:
    (OUT / f"{kind}/{obj['id']}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")


def main() -> None:
    for fecha, num, pags, corto, resumen, ctx in GACETAS:
        y, m, d = fecha.split("-")
        write("documents", {
            "id": f"doc-gaceta-{fecha}", "title": f"Gaceta de Madrid n.º {num}, {larga(fecha)}: {corto}",
            "title_original": f"Gaceta de Madrid. Núm. {num}", "document_type": "disposicion", "source_ids": ["F015"],
            "custodian": "Agencia Estatal Boletín Oficial del Estado (colección histórica Gazeta)",
            "signature": f"Gaceta de Madrid, núm. {num}, {d}/{m}/{y}, págs. {pags}",
            "canonical_url": f"https://www.boe.es/gazeta/dias/{y}/{m}/{d}/pdfs/GMD-{y}-{num:03d}.pdf",
            "date": fecha, "date_precision": "dia", "place_ids": ["plc-espana"],
            "summary": resumen, "context": ctx, "text_origin": "ocr_automatico",
            "rights": dict(RIGHTS, note="Normas oficiales excluidas de propiedad intelectual (art. 13 LPI); se enlaza al ejemplar de la sede del BOE."),
            "review": dict(REV_PDF), "consulted_at": TODAY})
    for f in FICHAS:
        write("documents", {
            "id": f"doc-{f['id'].lower()}", "title": f"Gaceta de Madrid n.º {f['num']}, {larga(f['date'])}: {f['title'].rstrip('.')}",
            "title_original": f["title"], "document_type": "disposicion", "source_ids": ["F015"],
            "custodian": "Agencia Estatal Boletín Oficial del Estado",
            "signature": f"{f['id']} · «{f['diario']}», núm. {f['num']}, {larga(f['date'])}, págs. {f['pages']} · {f['dept']}",
            "canonical_url": f"https://www.boe.es/buscar/doc.php?id={f['id']}",
            "date": f["date"], "date_precision": "dia", "place_ids": f["places"],
            "summary": f"Disposición de {f['dept']} publicada en la Gaceta de Madrid núm. {f['num']} de {larga(f['date'])}, págs. {f['pages']}: «{f['title'].rstrip('.')}».",
            "context": "Ficha oficial del BOE. El ejemplar completo no está en la ruta de la sede del BOE que este proyecto consulta, así que solo se usan el título y los datos de publicación.",
            "text_origin": "ninguno",
            "rights": dict(RIGHTS, note="Normas oficiales excluidas de propiedad intelectual (art. 13 LPI); se enlaza a la ficha oficial."),
            "review": dict(REV_FICHA), "consulted_at": TODAY})
    for eid, titulo, tipo, fecha, qid, places, claims in EVENTOS:
        obj = {"id": eid, "title": titulo, "event_type": tipo, "start_date": fecha, "date_precision": "dia",
               "place_ids": places, "spatial_precision": "estatal",
               "claims": [{"text": t, "kind": "documento", "evidence": [{"document_id": doc, "locator": loc}]} for t, doc, loc in claims],
               "review": dict(REV_FICHA if claims[0][1].startswith("doc-boe") else REV_PDF)}
        if qid:
            obj["wikidata"] = qid
        write("events", obj)
    print(f"{len(GACETAS) + len(FICHAS)} documentos, {len(EVENTOS)} acontecimientos")


if __name__ == "__main__":
    main()
