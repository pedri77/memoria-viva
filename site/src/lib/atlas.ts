// Conjunto compacto para el atlas y la cronología, calculado en build.
import { events, places, indicators, documents, byId } from "./data";

export const YEARS = [1931, 1932, 1933, 1934, 1935, 1936, 1937, 1938, 1939];
export const CENSOS = ["1920", "1930", "1940"];
export const CANARIAS = ["35", "38"];
export const CANARIAS_SHIFT: [number, number] = [6, 7]; // igual que scripts/etl/capas_mapa.sh

export const TYPE_LABEL: Record<string, string> = {
  politico: "Política", legislativo: "Legislación", electoral: "Elecciones", militar: "Militar",
  violencia: "Violencia", social: "Social", economico: "Economía", cultural: "Cultura", educativo: "Educación",
};

const yearOf = (d: string) => Number(d.slice(0, 4));

export function atlasData() {
  const ev = events.map((e) => {
    const firstDoc = byId(documents, e.claims[0].evidence[0].document_id);
    const pts = e.place_ids
      .map((id: string) => byId(places, id))
      .filter((p: any) => p && p.place_type !== "estado" && p.centroid)
      .map((p: any) => ({ id: p.id, name: p.canonical_name, c: p.centroid, ine: p.ine_code }));
    return {
      id: e.id, title: e.title, type: e.event_type, date: e.start_date, end: e.end_date ?? null, prec: e.date_precision,
      y0: yearOf(e.start_date), y1: yearOf(e.end_date ?? e.start_date),
      estatal: e.spatial_precision === "estatal" || pts.length === 0,
      pts: e.spatial_precision === "estatal" ? [] : pts,
      claim: e.claims[0].text,
      doc: firstDoc ? { id: firstDoc.id, title: firstDoc.title, url: firstDoc.canonical_url } : null,
    };
  });
  const prov: Record<string, any> = {};
  for (const p of places.filter((p) => p.id.startsWith("plc-prov-"))) {
    prov[p.ine_code] = { id: p.id, name: p.canonical_name, hist: p.historical_names?.[0]?.name ?? null, ind: {} };
  }
  for (const ind of indicators) {
    for (const o of ind.observations) {
      const code = o.place_id.replace("plc-prov-", "");
      if (!prov[code]) continue;
      (prov[code].ind[ind.id] ??= {})[o.period] = o.value;
    }
  }
  for (const code of Object.keys(prov)) {
    prov[code].events = ev.filter((e) => e.pts.some((p) => p.ine === code || p.ine?.startsWith(code))).map((e) => e.id);
  }
  const SHORT: Record<string, string> = { "ind-densidad-prov": "Densidad (hab./km²)", "ind-pob-derecho-prov": "Pobl. de derecho", "ind-pob-hecho-prov": "Pobl. de hecho", "ind-alfab-total-prov": "Saben leer (%)", "ind-alfab-varones-prov": "Varones que leen (%)", "ind-alfab-mujeres-prov": "Mujeres que leen (%)", "ind-prof-agraria-prov": "Agricultura, 1930 (%)", "ind-prof-agraria-varones-prov": "Agricultura, varones, 1930 (%)", "ind-prof-diversas-prov": "«Diversas», 1930 (%)", "ind-mortalidad-prov": "Mortalidad (‰)", "ind-sobremortalidad-prov": "Defunciones (1934-35 = 100)", "ind-mortalidad-infantil-prov": "Mortalidad infantil (‰ nacidos)", "ind-subv-memoria-local-prov": "Ayudas de memoria a entidades locales (€), hoy" };
  const inds = indicators.map((i) => ({ id: i.id, concept: i.concept, short: SHORT[i.id] ?? i.concept, unit: i.unit }))
    .sort((a, b) => a.id.localeCompare(b.id));
  return { events: ev, prov, inds };
}

// Mapa SVG provincial generado en build (versión sin WebGL). Proyección equirectangular con
// corrección de latitud media; Canarias ya viene desplazada en la capa.
import provRaw from "../../public/data/v1/provincias_1930.geojson?raw";
export function svgProvincias(width = 640) {
  const gj = JSON.parse(provRaw);
  const [minX, maxX, minY, maxY] = [-13.2, 4.6, 34.3, 44.0];
  const k = Math.cos((40 * Math.PI) / 180);
  const sx = width / ((maxX - minX) * k);
  const height = Math.round((maxY - minY) * sx);
  const pt = ([x, y]: number[]) => `${((x - minX) * k * sx).toFixed(1)},${((maxY - y) * sx).toFixed(1)}`;
  const ring = (r: number[][]) => "M" + r.map(pt).join("L") + "Z";
  const paths = gj.features.map((f: any) => {
    const g = f.geometry;
    const polys = g.type === "Polygon" ? [g.coordinates] : g.coordinates;
    return { code: f.properties.cod_unit, d: polys.map((p: number[][][]) => p.map(ring).join("")).join("") };
  });
  return { width, height, paths };
}

// Resultados por circunscripción (Atlas Electoral, CC BY-NC-SA 4.0) para la versión sin WebGL.
import c1931 from "../../public/data/v1/circunscripciones_1931.geojson?raw";
import c1933 from "../../public/data/v1/circunscripciones_1933.geojson?raw";
import c1936 from "../../public/data/v1/circunscripciones_1936.geojson?raw";
import bloquesRaw from "../../public/data/v1/elecciones_bloques.json?raw";
export const BLOQUES: Record<string, { label: string; desc: string }> = JSON.parse(bloquesRaw);
export function eleccionesCirc() {
  const out: Record<string, any[]> = {};
  for (const [y, raw] of [["1931", c1931], ["1933", c1933], ["1936", c1936]] as const) {
    out[y] = JSON.parse(raw).features.map((f: any) => f.properties).sort((a: any, b: any) => a.nombre.localeCompare(b.nombre, "es"));
  }
  return out;
}
