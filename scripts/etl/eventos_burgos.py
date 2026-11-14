"""F4 · Disposiciones de la zona sublevada (BOE de Burgos, 1936-1939).

Entrada: data/external/boe_burgos/fichas.json, con los metadatos oficiales de cada disposición
(título, diario, número, fecha, páginas y departamento) leídos de su ficha
https://www.boe.es/buscar/doc.php?id=BOE-A-AAAA-N por scripts/etl/boe_localizar.py.
El texto completo de estas fichas no está disponible en la sede del BOE (solo PDF, en una ruta
que robots.txt prohíbe a agentes automáticos), así que las afirmaciones se limitan a lo que
dice el título oficial de la disposición y a sus datos de publicación.

Uso: python3 -I scripts/etl/eventos_burgos.py
"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
FICHAS = ROOT / "data/external/boe_burgos/fichas.json"
OUT = ROOT / "data/canonical"
TODAY = "2026-11-14"
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto", "septiembre", "octubre", "noviembre", "diciembre"]
RIGHTS = {"status": "reuse_conditions", "action": "enlazar",
          "attribution": "Fuente: Agencia Estatal Boletín Oficial del Estado, www.boe.es",
          "evidence_url": "https://www.boe.es/informacion/aviso_legal/index.php", "checked_at": TODAY,
          "note": "Normas oficiales excluidas de propiedad intelectual (art. 13 LPI); se enlaza a la ficha oficial."}
REVIEW = {"status": "revision", "date": TODAY, "by": ["autor"],
          "note": "Título, número, fecha y páginas leídos en la ficha oficial del BOE. Texto completo no consultado (solo PDF en ruta vetada a robots); pendiente de lectura humana."}
CONTEXT = ("Boletín Oficial del Estado editado en Burgos por las autoridades de la zona sublevada desde el 2 de octubre de 1936. "
           "Acredita las normas que dictaban esas autoridades, no su aplicación ni sus efectos.")

# Selección editorial. Cada acontecimiento: (id, título, tipo, fecha, wikidata, [(texto, id BOE)]).
# Los textos se limitan al título oficial y a los datos de publicación de cada ficha.
EVENTOS = [
    ("evt-1936-10-02-organizacion-estado-sublevado", "Primera organización administrativa del Estado en la zona sublevada", "politico", "1936-10-02", None,
     [("El primer número del Boletín Oficial del Estado editado en Burgos, de 2 de octubre de 1936, publica en sus páginas 1 y 2 la «Ley estableciendo la organización administrativa a que ha de ajustarse la nueva estructura del Estado».", "BOE-A-1936-9134")]),
    ("evt-1936-11-11-revision-personal-instruccion", "Decreto de revisión del personal de Instrucción Pública en la zona sublevada", "educativo", "1936-11-11", None,
     [("El BOE de Burgos del 11 de noviembre de 1936 publica el Decreto núm. 66, que dispone «se lleve a cabo una revisión total en el personal de Instrucción Pública, por medio de las Comisiones que se crean».", "BOE-A-1936-9694"),
      ("El mismo número publica una orden de la Presidencia de la Junta Técnica del Estado que dicta las reglas para aplicar ese decreto.", "BOE-A-1936-9705")]),
    ("evt-1937-04-20-decreto-unificacion", "Decreto de unificación de Falange Española y los requetés", "politico", "1937-04-20", "Q5390265",
     [("El BOE de 20 de abril de 1937 publica el Decreto núm. 255, que dispone que Falange Española y Requetés se integren, bajo la Jefatura del Jefe del Estado, en una sola entidad política de carácter nacional.", "BOE-A-1937-3746")]),
    ("evt-1938-01-31-administracion-central", "Ley de organización de la Administración Central del Estado", "politico", "1938-01-31", None,
     [("El BOE de 31 de enero de 1938 publica la «Ley organizando la Administración Central del Estado», del Gobierno del Estado.", "BOE-A-1938-1406")]),
    ("evt-1938-03-10-fuero-trabajo", "Fuero del Trabajo", "social", "1938-03-10", "Q3028296",
     [("El BOE de 10 de marzo de 1938 publica el decreto que aprueba el Fuero del Trabajo formulado por el Consejo Nacional de Falange Española Tradicionalista y de las J.O.N.S.", "BOE-A-1938-3093")]),
    ("evt-1938-04-22-ley-prensa", "Ley de Prensa de 1938", "cultural", "1938-04-22", None,
     [("La Ley de Prensa está fechada el 22 de abril de 1938; el BOE del 24 de abril la publica de nuevo, rectificada, por un error en su publicación del día anterior.", "BOE-A-1938-4796")]),
    ("evt-1938-09-23-reforma-ensenanza-media", "Ley sobre reforma de la Enseñanza Media", "educativo", "1938-09-23", None,
     [("El BOE de 23 de septiembre de 1938 publica la «Ley sobre reforma de la Enseñanza Media».", "BOE-A-1938-11039"),
      ("El mismo número publica un decreto del Ministerio de Educación Nacional que crea la Inspección de la Enseñanza Media oficial y privada.", "BOE-A-1938-11040")]),
    ("evt-1939-02-13-responsabilidades-politicas", "Ley de Responsabilidades Políticas", "politico", "1939-02-13", "Q3816909",
     [("El BOE de 13 de febrero de 1939, núm. 44, publica en sus páginas 824 a 847 la Ley de Responsabilidades Políticas, de la Jefatura del Estado.", "BOE-A-1939-1451")]),
]


def fecha_larga(d: str) -> str:
    y, m, dd = d.split("-")
    return f"{int(dd)} de {MESES[int(m) - 1]} de {y}"


def main() -> None:
    fichas = json.loads(FICHAS.read_text())
    n_doc = n_ev = 0
    for f in fichas:
        did = f"doc-{f['id'].lower()}"
        (OUT / f"documents/{did}.json").write_text(json.dumps({
            "id": did,
            "title": f"BOE n.º {f['num']}, {fecha_larga(f['date'])}: {f['title'].rstrip('.')}",
            "title_original": f["title"],
            "document_type": "disposicion",
            "source_ids": ["F015"],
            "custodian": "Agencia Estatal Boletín Oficial del Estado",
            "signature": f"{f['id']} · «{f['diario']}», núm. {f['num']}, {fecha_larga(f['date'])}, págs. {f['pages']} · {f['dept']}",
            "canonical_url": f"https://www.boe.es/buscar/doc.php?id={f['id']}",
            "date": f["date"], "date_precision": "dia",
            "place_ids": ["plc-espana"],
            "summary": f"Disposición de {f['dept']} publicada en el BOE núm. {f['num']} de {fecha_larga(f['date'])}, págs. {f['pages']}: «{f['title'].rstrip('.')}».",
            "context": CONTEXT,
            "text_origin": "ninguno",
            "rights": dict(RIGHTS), "review": dict(REVIEW), "consulted_at": TODAY,
        }, ensure_ascii=False, indent=2) + "\n")
        n_doc += 1
    by_id = {f["id"]: f for f in fichas}
    for eid, titulo, tipo, fecha, qid, claims in EVENTOS:
        obj = {"id": eid, "title": titulo, "event_type": tipo, "start_date": fecha, "date_precision": "dia",
               "place_ids": ["plc-espana"], "spatial_precision": "estatal",
               "claims": [{"text": txt, "kind": "documento",
                           "evidence": [{"document_id": f"doc-{bid.lower()}", "locator": f"págs. {by_id[bid]['pages']}"}]} for txt, bid in claims],
               "review": dict(REVIEW)}
        if qid:
            obj["wikidata"] = qid
        (OUT / f"events/{eid}.json").write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
        n_ev += 1
    print(f"{n_doc} documentos, {n_ev} acontecimientos")


if __name__ == "__main__":
    main()
