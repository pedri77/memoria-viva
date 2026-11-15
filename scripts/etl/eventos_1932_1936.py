"""F4 · Huecos de la cronología: 1931-1933 y primavera de 1936.

Evidencia: fichas https://www.boe.es/buscar/doc.php?id=BOE-A-AAAA-N (título y publicación,
sin texto) y ejemplares de la Gaceta en la ruta permitida /gazeta/dias/ (texto comprobado
sobre el PDF). Las afirmaciones se limitan a lo que dice cada documento.

Uso: python3 -I scripts/etl/eventos_1932_1936.py   (después de eventos_1934_1935.py)
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eventos_1934_1935 import OUT, RIGHTS, REV_PDF, REV_FICHA, larga, write  # noqa: E402

FICHAS = [
    {"id": "BOE-A-1932-592", "title": "Decreto declarando disuelta en el territorio español la Compañía de Jesús, y disponiendo que los religiosos y novicios de dicha Compañía cesen en la vida común dentro del territorio nacional en el término de diez días.",
     "num": 24, "date": "1932-01-24", "pages": "610 a 611", "dept": "Ministerio de Justicia"},
    {"id": "BOE-A-1932-1855", "title": "Ley relativa al divorcio.", "num": 71, "date": "1932-03-11", "pages": "1762 a 1767", "dept": "Ministerio de Justicia"},
    {"id": "BOE-A-1932-1898", "title": "Ley (rectificada) relativa al divorcio.", "num": 72, "date": "1932-03-12", "pages": "1794 a 1799", "dept": "Ministerio de Justicia"},
    {"id": "BOE-A-1932-6203", "title": "Ley autorizando al Gobierno para separar definitivamente del servicio a los funcionarios civiles o militares que, rebasando el derecho que les otorga el artículo 41 de la Constitución, realicen o hayan realizado actos de hostilidad o menosprecio contra la República.",
     "num": 225, "date": "1932-08-12", "pages": "1122 a 1122", "dept": "Presidencia del Consejo de Ministros"},
    {"id": "BOE-A-1933-6584", "title": "Ley de Orden público.", "num": 211, "date": "1933-07-30", "pages": "682 a 690", "dept": "Ministerio de la Gobernación"},
]
GACETAS = [
    ("1936-04-09", 100, "259", "decretos de 8 de abril de 1936",
     "Ejemplar con decretos fechados el 8 de abril de 1936 que firma Diego Martínez Barrio, con el refrendo de Manuel Azaña como presidente del Consejo de Ministros.",
     "Ejemplar ordinario de la Gaceta. Se cita por las firmas de los decretos."),
    ("1936-05-11", 132, "1379", "elección de Manuel Azaña como presidente de la República",
     "Acta de la Asamblea de Diputados a Cortes y Compromisarios que proclama presidente electo de la República a Manuel Azaña el 10 de mayo de 1936, acta de su aceptación y decretos que admiten su dimisión como presidente del Consejo de Ministros y nombran para ese cargo a Augusto Barcia Trelles.",
     "Publicación oficial del Congreso de los Diputados y decretos firmados por Diego Martínez Barrio."),
]
EVENTOS = [
    ("evt-1931-04-30-terminos-municipales", "Decreto de términos municipales", "social", "1931-04-30", ["plc-espana"], [
        ("La Gaceta del 30 de abril de 1931 publica un decreto del Ministerio de Trabajo y Previsión cuyo artículo 1.º obliga a los patronos a emplear preferentemente, en todos los trabajos agrícolas, a los braceros vecinos del municipio en que se realicen.", "doc-gaceta-1931-04-30", "art. 1.º, pág. 415"),
        ("El decreto ordena abrir en cada municipio un registro en el que puedan inscribirse los obreros agrícolas sin colocación y entre los que los patronos deberán elegir a los que empleen.", "doc-gaceta-1931-04-30", "arts. 2.º y 3.º, pág. 415")]),
    ("evt-1932-01-24-disolucion-jesuitas", "Disolución de la Compañía de Jesús", "legislativo", "1932-01-24", ["plc-espana"], [
        ("La Gaceta del 24 de enero de 1932 publica un decreto del Ministerio de Justicia que declara disuelta en el territorio español la Compañía de Jesús y dispone que sus religiosos y novicios cesen en la vida común dentro del territorio nacional en el término de diez días.", "doc-boe-a-1932-592", "págs. 610 a 611")]),
    ("evt-1932-03-11-ley-divorcio", "Ley de divorcio", "social", "1932-03-11", ["plc-espana"], [
        ("La Gaceta del 11 de marzo de 1932 publica la «Ley relativa al divorcio», del Ministerio de Justicia.", "doc-boe-a-1932-1855", "págs. 1762 a 1767"),
        ("Al día siguiente la Gaceta la publica de nuevo, rectificada.", "doc-boe-a-1932-1898", "págs. 1794 a 1799")]),
    ("evt-1932-08-12-separacion-funcionarios", "Ley de separación de funcionarios hostiles a la República", "politico", "1932-08-12", ["plc-espana"], [
        ("La Gaceta del 12 de agosto de 1932 publica una ley que autoriza al Gobierno a separar definitivamente del servicio a los funcionarios civiles o militares que, rebasando el derecho que les otorga el artículo 41 de la Constitución, realicen o hayan realizado actos de hostilidad o menosprecio contra la República.", "doc-boe-a-1932-6203", "pág. 1122")]),
    ("evt-1933-07-30-ley-orden-publico", "Ley de Orden Público de 1933", "legislativo", "1933-07-30", ["plc-espana"], [
        ("La Gaceta del 30 de julio de 1933 publica la «Ley de Orden público», del Ministerio de la Gobernación.", "doc-boe-a-1933-6584", "págs. 682 a 690")]),
    ("evt-1936-05-10-azana-presidente", "Elección de Manuel Azaña como presidente de la República", "politico", "1936-05-10", ["plc-espana", "plc-madrid"], [
        ("Los decretos de 8 de abril de 1936 publicados en la Gaceta del día siguiente los firma Diego Martínez Barrio, no Niceto Alcalá-Zamora.", "doc-gaceta-1936-04-09", "pág. 259"),
        ("Según el acta publicada en la Gaceta del 11 de mayo de 1936, el día 10 la Asamblea de Diputados a Cortes y Compromisarios proclamó presidente electo de la República a Manuel Azaña y Díaz, con 754 de los 847 votos emitidos, más de la mitad más uno de los 911 miembros de la Asamblea.", "doc-gaceta-1936-05-11", "Congreso de los Diputados, pág. 1379"),
        ("Decretos del mismo día, firmados por Diego Martínez Barrio, admiten la dimisión de Azaña como presidente del Consejo de Ministros por haber sido elegido presidente de la República y nombran para ese cargo a Augusto Barcia Trelles.", "doc-gaceta-1936-05-11", "Ministerio de Justicia, pág. 1379")]),
]
NOTA_ED = {"evt-1936-05-10-azana-presidente": "El acuerdo de las Cortes que puso fin al mandato de Niceto Alcalá-Zamora no está en los ejemplares de la Gaceta que este proyecto puede consultar."}


def main() -> None:
    for f in FICHAS:
        write("documents", {
            "id": f"doc-{f['id'].lower()}", "title": f"Gaceta de Madrid n.º {f['num']}, {larga(f['date'])}: {f['title'].rstrip('.')}",
            "title_original": f["title"], "document_type": "disposicion", "source_ids": ["F015"],
            "custodian": "Agencia Estatal Boletín Oficial del Estado",
            "signature": f"{f['id']} · «Gaceta de Madrid», núm. {f['num']}, {larga(f['date'])}, págs. {f['pages']} · {f['dept']}",
            "canonical_url": f"https://www.boe.es/buscar/doc.php?id={f['id']}",
            "date": f["date"], "date_precision": "dia", "place_ids": ["plc-espana"],
            "summary": f"Disposición de {f['dept']} publicada en la Gaceta de Madrid núm. {f['num']} de {larga(f['date'])}, págs. {f['pages']}: «{f['title'].rstrip('.')}».",
            "context": "Ficha oficial del BOE. Solo se usan el título y los datos de publicación; el texto no se ha consultado.",
            "text_origin": "ninguno",
            "rights": dict(RIGHTS, note="Normas oficiales excluidas de propiedad intelectual (art. 13 LPI); se enlaza a la ficha oficial."),
            "review": dict(REV_FICHA), "consulted_at": "2026-11-15"})
    for fecha, num, pags, corto, resumen, ctx in GACETAS:
        y, m, d = fecha.split("-")
        write("documents", {
            "id": f"doc-gaceta-{fecha}", "title": f"Gaceta de Madrid n.º {num}, {larga(fecha)}: {corto}",
            "title_original": f"Gaceta de Madrid. Núm. {num}", "document_type": "disposicion", "source_ids": ["F015"],
            "custodian": "Agencia Estatal Boletín Oficial del Estado (colección histórica Gazeta)",
            "signature": f"Gaceta de Madrid, núm. {num}, {d}/{m}/{y}, pág. {pags}",
            "canonical_url": f"https://www.boe.es/gazeta/dias/{y}/{m}/{d}/pdfs/GMD-{y}-{num:03d}.pdf",
            "date": fecha, "date_precision": "dia", "place_ids": ["plc-espana"],
            "summary": resumen, "context": ctx, "text_origin": "ocr_automatico",
            "rights": dict(RIGHTS, note="Normas oficiales excluidas de propiedad intelectual (art. 13 LPI); se enlaza al ejemplar de la sede del BOE."),
            "review": dict(REV_PDF), "consulted_at": "2026-11-15"})
    # El ejemplar del 30-04-1931 ya existe (decreto del catalán): se amplía su título y resumen
    p = OUT / "documents/doc-gaceta-1931-04-30.json"
    doc = json.loads(p.read_text())
    doc["title"] = "Gaceta de Madrid n.º 120, 30 de abril de 1931: decretos sobre el catalán en la escuela y sobre la contratación de braceros"
    doc["signature"] = "Gaceta de Madrid, núm. 120, 30/04/1931, págs. 413-415"
    if "braceros" not in doc["summary"]:
        doc["summary"] += " El mismo número publica un decreto del Ministerio de Trabajo y Previsión que obliga a los patronos a emplear preferentemente en los trabajos agrícolas a los braceros vecinos del municipio (pág. 415)."
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=2) + "\n")
    for eid, titulo, tipo, fecha, places, claims in EVENTOS:
        obj = {"id": eid, "title": titulo, "event_type": tipo, "start_date": fecha, "date_precision": "dia",
               "place_ids": places, "spatial_precision": "estatal",
               "claims": [{"text": t, "kind": "documento", "evidence": [{"document_id": doc_id, "locator": loc}]} for t, doc_id, loc in claims],
               "review": dict(REV_FICHA if claims[0][1].startswith("doc-boe") else REV_PDF)}
        if eid in NOTA_ED:
            obj["editorial_note"] = NOTA_ED[eid]
        write("events", obj)
    print(f"{len(FICHAS) + len(GACETAS)} documentos nuevos, {len(EVENTOS)} acontecimientos")


if __name__ == "__main__":
    main()
