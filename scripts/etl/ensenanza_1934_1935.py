"""F4 · Enseñanza primaria en 1934-1935: acontecimientos y escena de la narrativa de las escuelas.

Evidencia: Gaceta del 03-08-1934 (PDF en /gazeta/dias/, texto comprobado) y fichas doc.php
de 1935 (título y publicación). Localizadas con scripts/etl/boe_localizar.py a partir de
fechas citadas por la bibliografía; solo se afirma lo que dice cada documento.

Uso: python3 -I scripts/etl/ensenanza_1934_1935.py   (idempotente)
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).parent))
from eventos_1934_1935 import OUT, RIGHTS, REV_PDF, REV_FICHA, larga, write  # noqa: E402

FICHAS = [
    {"id": "BOE-A-1935-7071", "title": "Decreto suprimiendo la Inspección Central de Primera enseñanza.", "num": 206, "date": "1935-07-25", "pages": "856 a 856"},
    {"id": "BOE-A-1935-10978", "title": "Decreto disponiendo quede redactado en la forma que se inserta el artículo 20 del Decreto de 2 de Diciembre de 1932.", "num": 332, "date": "1935-11-28", "pages": "1723 a 1723"},
]
COEDU = ("La Gaceta del 3 de agosto de 1934 publica una orden de 1 de agosto que deja sin efecto el régimen de coeducación establecido, con y sin autorización ministerial, y prohíbe a maestros e inspectores implantarlo en las escuelas primarias nacionales, salvo en las escuelas mixtas y de párvulos.",
         "doc-gaceta-1934-08-03", "pág. 1224")
COEDU_MOTIVO = ("La orden lo justifica en que algunos inspectores habían establecido la coeducación en escuelas unitarias sin autorización del Ministerio, «provocando la protesta de los Ayuntamientos, de los padres de los niños y de los propios Maestros».",
                "doc-gaceta-1934-08-03", "pág. 1224")
INSP = ("La Gaceta del 25 de julio de 1935 publica un decreto del Ministerio de Instrucción Pública que suprime la Inspección Central de Primera enseñanza.", "doc-boe-a-1935-7071", "pág. 856")
ART20 = ("La Gaceta del 28 de noviembre de 1935 publica un decreto que da nueva redacción al artículo 20 del decreto de 2 de diciembre de 1932.", "doc-boe-a-1935-10978", "pág. 1723")
BACH = ("Un decreto de 29 de agosto de 1934 establece un Bachillerato de siete cursos, divididos en un primer ciclo de tres y un segundo de cuatro.", "doc-gaceta-1934-08-30", "art. 1.º, pág. 1872")

EVENTOS = [
    ("evt-1934-08-01-orden-coeducacion", "Orden que deja sin efecto la coeducación en las escuelas primarias", "educativo", "1934-08-01", [COEDU, COEDU_MOTIVO], REV_PDF),
    ("evt-1935-07-25-supresion-inspeccion-central", "Supresión de la Inspección Central de Primera enseñanza", "educativo", "1935-07-25", [INSP], REV_FICHA),
    ("evt-1935-11-28-inspeccion-articulo-20", "Nueva redacción del artículo 20 del decreto de Inspección de 1932", "educativo", "1935-11-28", [ART20], REV_FICHA),
]


def main() -> None:
    for f in FICHAS:
        write("documents", {
            "id": f"doc-{f['id'].lower()}", "title": f"Gaceta de Madrid n.º {f['num']}, {larga(f['date'])}: {f['title'].rstrip('.')}",
            "title_original": f["title"], "document_type": "disposicion", "source_ids": ["F015"],
            "custodian": "Agencia Estatal Boletín Oficial del Estado",
            "signature": f"{f['id']} · «Gaceta de Madrid», núm. {f['num']}, {larga(f['date'])}, págs. {f['pages']} · Ministerio de Instrucción Pública y Bellas Artes",
            "canonical_url": f"https://www.boe.es/buscar/doc.php?id={f['id']}",
            "date": f["date"], "date_precision": "dia", "place_ids": ["plc-espana"],
            "summary": f"Disposición del Ministerio de Instrucción Pública y Bellas Artes publicada en la Gaceta de Madrid núm. {f['num']} de {larga(f['date'])}: «{f['title'].rstrip('.')}».",
            "context": "Ficha oficial del BOE. Solo se usan el título y los datos de publicación; el texto no se ha consultado.",
            "text_origin": "ninguno",
            "rights": dict(RIGHTS, note="Normas oficiales excluidas de propiedad intelectual (art. 13 LPI); se enlaza a la ficha oficial."),
            "review": dict(REV_FICHA), "consulted_at": "2026-11-15"})
    write("documents", {
        "id": "doc-gaceta-1934-08-03", "title": "Gaceta de Madrid n.º 215, 3 de agosto de 1934: orden sobre la coeducación en las escuelas primarias",
        "title_original": "Gaceta de Madrid. Núm. 215", "document_type": "disposicion", "source_ids": ["F015"],
        "custodian": "Agencia Estatal Boletín Oficial del Estado (colección histórica Gazeta)",
        "signature": "Gaceta de Madrid, núm. 215, 03/08/1934, pág. 1224",
        "canonical_url": "https://www.boe.es/gazeta/dias/1934/08/03/pdfs/GMD-1934-215.pdf",
        "date": "1934-08-03", "date_precision": "dia", "place_ids": ["plc-espana"],
        "summary": "Orden del Ministerio de Instrucción Pública de 1 de agosto de 1934, firmada por Filiberto Villalobos, que deja sin efecto el régimen de coeducación establecido y prohíbe a maestros e inspectores implantarlo en las escuelas primarias nacionales, salvo en las mixtas y de párvulos.",
        "context": "Disposición del Gobierno; el preámbulo expone los motivos del propio Ministerio.",
        "text_origin": "ocr_automatico",
        "rights": dict(RIGHTS, note="Normas oficiales excluidas de propiedad intelectual (art. 13 LPI); se enlaza al ejemplar de la sede del BOE."),
        "review": dict(REV_PDF), "consulted_at": "2026-11-15"})
    for eid, titulo, tipo, fecha, claims, rev in EVENTOS:
        write("events", {"id": eid, "title": titulo, "event_type": tipo, "start_date": fecha, "date_precision": "dia",
                         "place_ids": ["plc-espana"], "spatial_precision": "estatal",
                         "claims": [{"text": t, "kind": "documento", "evidence": [{"document_id": d, "locator": loc}]} for t, d, loc in claims],
                         "review": dict(rev)})

    # Escena nueva en la narrativa de las escuelas, antes de «guerra»
    p = OUT / "stories/story-escuelas-republica.json"
    s = json.loads(p.read_text())
    s["scenes"] = [sc for sc in s["scenes"] if sc["id"] != "segundo-bienio"]
    escena = {
        "id": "segundo-bienio", "heading": "Cambio de rumbo", "date_label": "1934-1935",
        "intro": "Tras las elecciones de noviembre de 1933, el Ministerio de Instrucción Pública dicta normas que modifican algunas de las de 1931-1933.",
        "claims": [{"text": t, "kind": "documento", "evidence": [{"document_id": d, "locator": loc}]} for t, d, loc in (COEDU, COEDU_MOTIVO, BACH, INSP, ART20)],
        "event_ids": ["evt-1934-08-01-orden-coeducacion", "evt-1934-08-29-plan-bachillerato", "evt-1935-07-25-supresion-inspeccion-central", "evt-1935-11-28-inspeccion-articulo-20"],
        "editorial_note": "De los dos decretos de 1935 solo se conoce el título oficial: qué decía la nueva redacción del artículo 20 y cómo se aplicó la supresión de la Inspección Central requiere leer su texto.",
    }
    idx = next(i for i, sc in enumerate(s["scenes"]) if sc["id"] == "guerra")
    s["scenes"].insert(idx, escena)
    s["gaps"] = [g for g in s["gaps"] if not g.startswith(("Del periodo 1934-1935", "De 1934-1935 falta"))]
    s["gaps"].append("De 1934-1935 falta la sustitución de la enseñanza de las congregaciones religiosas, cuyo plazo para la primaria fijaba la ley de 1933, y el texto de los decretos de Inspección de 1935.")
    s["summary"] = ("Qué dicen las normas publicadas en la Gaceta sobre la escuela entre la proclamación de la República y la guerra: "
                    "el diagnóstico de 1931, la lengua y la religión en el aula, las Misiones Pedagógicas, la Constitución, la ley de "
                    "congregaciones de 1933, los cambios de 1934-1935 y las plazas de maestros de 1936. Es una historia de normas, no de su aplicación.")
    s["review"]["date"] = "2026-11-15"
    p.write_text(json.dumps(s, ensure_ascii=False, indent=2) + "\n")

    lp = OUT.parent / "lagunas.json"
    lag = json.loads(lp.read_text())
    for laguna in lag:
        if laguna["id"] == "laguna-ensenanza-1934-1935":
            laguna["tema"] = "Sustitución de la enseñanza de las congregaciones y texto de los decretos de Inspección, 1934-1935"
            laguna["falta"] = "Las disposiciones sobre el plazo de sustitución de la enseñanza de las congregaciones religiosas en la primaria y el texto de los decretos de 25 de julio y 28 de noviembre de 1935 sobre la Inspección (hoy solo su título)."
            laguna["buscado"] = "Fichas doc.php del 2-3 de agosto de 1934, 24-25 de julio y 27-28 de noviembre de 1935 (localizados la orden de coeducación y los dos decretos de Inspección). La sustitución no se ha buscado por fecha concreta."
    lp.write_text(json.dumps(lag, ensure_ascii=False, indent=2) + "\n")
    print("3 documentos, 3 acontecimientos, escena «segundo-bienio»")


if __name__ == "__main__":
    main()
