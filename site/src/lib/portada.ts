// Datos de la portada, calculados en build a partir de data/canonical y de las capas públicas.
// Nada se escribe a mano: textos de las escenas = afirmaciones de las narrativas con su fuente.
import { events, places, indicators, documents, stories, byId } from "./data";
import { CANARIAS, CANARIAS_SHIFT } from "./atlas";
import provRaw from "../../public/data/v1/provincias_1930.geojson?raw";
import c1931 from "../../public/data/v1/circunscripciones_1931.geojson?raw";
import c1933 from "../../public/data/v1/circunscripciones_1933.geojson?raw";
import c1936 from "../../public/data/v1/circunscripciones_1936.geojson?raw";

// Misma proyección que svgProvincias (equirectangular corregida a 40° N).
const W = 800;
const [minX, maxX, minY, maxY] = [-13.2, 4.6, 34.3, 44.0];
const k = Math.cos((40 * Math.PI) / 180);
const sx = W / ((maxX - minX) * k);
export const MAPA = { w: W, h: Math.round((maxY - minY) * sx) };
const xy = ([x, y]: number[]) => [(x - minX) * k * sx, (maxY - y) * sx];
const pt = (c: number[]) => xy(c).map((v) => v.toFixed(1)).join(",");
const ring = (r: number[][]) => "M" + r.map(pt).join("L") + "Z";
const pathOf = (g: any) => (g.type === "Polygon" ? [g.coordinates] : g.coordinates)
  .map((p: number[][][]) => p.map(ring).join("")).join("");

const obs = (indId: string) => {
  const out: Record<string, Record<string, number | null>> = {};
  for (const o of byId(indicators, indId)?.observations ?? []) {
    (out[o.place_id.replace("plc-prov-", "")] ??= {})[o.period] = o.value;
  }
  return out;
};

export function provincias() {
  const tot = obs("ind-alfab-total-prov");
  const muj = obs("ind-alfab-mujeres-prov");
  const nombre = (code: string) => places.find((p) => p.ine_code === code && p.id.startsWith("plc-prov-"))?.canonical_name ?? code;
  return JSON.parse(provRaw).features.map((f: any) => {
    const code = f.properties.cod_unit;
    return { code, name: nombre(code), d: pathOf(f.geometry), a20: tot[code]?.["1920"] ?? null, a30: tot[code]?.["1930"] ?? null, m30: muj[code]?.["1930"] ?? null };
  });
}

export function circunscripciones() {
  const out: Record<string, { d: string; part: number | null; nombre: string }[]> = {};
  for (const [y, raw] of [["1931", c1931], ["1933", c1933], ["1936", c1936]] as const) {
    out[y] = JSON.parse(raw).features.map((f: any) => ({ d: pathOf(f.geometry), part: f.properties.part ?? null, nombre: f.properties.nombre }));
  }
  return out;
}

// Acontecimientos con lugar concreto, como puntos sobre el mapa (Canarias desplazada igual que la capa).
export function puntos() {
  const out: { x: number; y: number; year: number; id: string }[] = [];
  for (const e of events) {
    if (e.spatial_precision === "estatal") continue;
    for (const id of e.place_ids) {
      const p = byId(places, id);
      if (!p?.centroid || p.place_type === "estado") continue;
      let c = p.centroid as number[];
      if (p.ine_code && CANARIAS.includes(p.ine_code.slice(0, 2))) c = [c[0] + CANARIAS_SHIFT[0], c[1] + CANARIAS_SHIFT[1]];
      const [x, y] = xy(c);
      out.push({ x: +x.toFixed(1), y: +y.toFixed(1), year: Number(e.start_date.slice(0, 4)), id: e.id });
    }
  }
  return out;
}

// Una afirmación de una narrativa, con su primera evidencia resuelta.
export function afirmacion(storyId: string, sceneId: string, i: number) {
  const s = byId(stories, storyId);
  const sc = s?.scenes.find((x: any) => x.id === sceneId);
  const c = sc?.claims[i];
  if (!c) throw new Error(`Portada: no existe la afirmación ${storyId}/${sceneId}/${i}`);
  const e = c.evidence[0];
  const d = byId(documents, e.document_id);
  return { text: c.text as string, kind: c.kind as string, doc: { id: e.document_id, title: d?.title ?? e.document_id, locator: e.locator ?? "" }, story: storyId.replace("story-", ""), scene: sceneId };
}

export function docIndicador(indId: string, period: string) {
  const o = byId(indicators, indId)?.observations.find((o: any) => o.period === period);
  const d = o && byId(documents, o.document_id);
  return d ? { id: d.id, title: d.title } : null;
}

export const cronologia = () => events.map((e) => ({ id: e.id, title: e.title, date: e.start_date, prec: e.date_precision, type: e.event_type }));
