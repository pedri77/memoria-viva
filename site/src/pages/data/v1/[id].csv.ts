import { indicators, places, byId } from "../../../lib/data";
export function getStaticPaths() {
  return indicators.map((i) => ({ params: { id: i.id } }));
}
const q = (s: unknown) => `"${String(s ?? "").replace(/"/g, '""')}"`;
export function GET({ params }: { params: { id: string } }) {
  const ind = indicators.find((i) => i.id === params.id)!;
  const head = ["provincia", "codigo_1930", "censo", "valor", "unidad", "motivo_ausencia", "documento", "localizador", "fuente", "licencia"];
  const rows = ind.observations.map((o: any) => {
    const p = byId(places, o.place_id);
    return [p?.canonical_name, p?.ine_code, o.period, o.value, ind.unit, o.missingness_reason, o.document_id, o.locator,
      "mapSpainHist (Vall-Prat, Zenodo 10.5281/zenodo.23663208) a partir de censos del INE; elaboración: España: Memoria Viva", "CC BY 4.0"].map(q).join(",");
  });
  return new Response("﻿" + [head.join(","), ...rows].join("\r\n") + "\r\n", { headers: { "Content-Type": "text/csv; charset=utf-8" } });
}
