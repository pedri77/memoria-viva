import { indicators, places, documents, byId } from "../../../lib/data";
export function getStaticPaths() {
  return indicators.map((i) => ({ params: { id: i.id } }));
}
const LIC: Record<string, string> = { cc_by: "CC BY 4.0", cc_by_sa: "CC BY-SA 4.0", cc_by_nc: "CC BY-NC 4.0", cc_by_nc_sa: "CC BY-NC-SA 4.0", cc0: "CC0", public_domain: "Dominio público", reuse_open: "Reutilización con cita (Ley 37/2007, condiciones generales del custodio)" };
const q = (s: unknown) => `"${String(s ?? "").replace(/"/g, '""')}"`;
export function GET({ params }: { params: { id: string } }) {
  const ind = indicators.find((i) => i.id === params.id)!;
  const head = ["provincia", "codigo_1930", "censo", "valor", "unidad", "motivo_ausencia", "documento", "localizador", "fuente", "licencia"];
  const rows = ind.observations.map((o: any) => {
    const p = byId(places, o.place_id);
    return [p?.canonical_name, p?.ine_code, o.period, o.value, ind.unit, o.missingness_reason, o.document_id, o.locator,
      `${byId(documents, o.document_id)?.rights?.attribution ?? o.document_id}; elaboración: España: Memoria Viva`, LIC[byId(documents, o.document_id)?.rights?.status] ?? "ver documento"].map(q).join(",");
  });
  return new Response("﻿" + [head.join(","), ...rows].join("\r\n") + "\r\n", { headers: { "Content-Type": "text/csv; charset=utf-8" } });
}
