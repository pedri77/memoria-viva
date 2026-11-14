// Valida data/canonical contra schemas/ y comprueba integridad referencial.
// Sale con código 1 si hay cualquier error.
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";
import Ajv2020 from "ajv/dist/2020.js";
import addFormats from "ajv-formats";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const read = (p) => JSON.parse(readFileSync(join(ROOT, p), "utf8"));
const list = (d) => readdirSync(join(ROOT, d)).filter((f) => f.endsWith(".json")).map((f) => join(d, f));

const ajv = new Ajv2020({ allErrors: true, strict: true, strictRequired: false });
addFormats(ajv);
for (const f of list("schemas")) ajv.addSchema(read(f));

const KINDS = {
  sources: "source.schema.json",
  places: "place.schema.json",
  documents: "document.schema.json",
  events: "event.schema.json",
  indicators: "indicator.schema.json",
  stories: "story.schema.json",
};
const base = "https://memoria-viva/schemas/";
const errors = [];
const data = {};

for (const [kind, schema] of Object.entries(KINDS)) {
  data[kind] = new Map();
  let files = [];
  try { files = list(`data/canonical/${kind}`); } catch { continue; }
  const validate = ajv.getSchema(base + schema);
  for (const f of files) {
    const obj = read(f);
    if (!validate(obj)) {
      for (const e of validate.errors) errors.push(`${f}: ${e.instancePath || "/"} ${e.message}`);
    }
    const id = obj.id ?? obj.slug;
    const expected = f.split("/").pop().replace(/\.json$/, "");
    if (id !== expected) errors.push(`${f}: el id «${id}» no coincide con el nombre del fichero`);
    if (data[kind].has(id)) errors.push(`${f}: id duplicado ${id}`);
    data[kind].set(id, obj);
  }
}

const need = (f, kind, id) => {
  if (!data[kind].has(id)) return errors.push(`${f}: referencia rota a ${kind}/${id}`);
  const target = data[kind].get(id);
  const [k, oid] = f.split("/");
  const source = data[k]?.get(oid);
  if (target.review?.status === "retirado" && source?.review?.status !== "retirado")
    errors.push(`${f}: cita ${kind}/${id}, que está retirado; retira o corrige también este objeto`);
};
// Toda retirada debe explicar el motivo
for (const kind of Object.keys(data)) for (const [id, o] of data[kind])
  if (o.review?.status === "retirado" && !o.review.note) errors.push(`${kind}/${id}: retirado sin motivo en review.note`);
for (const [id, o] of data.places) {
  o.source_ids.forEach((s) => need(`places/${id}`, "sources", s));
  if (o.parent_id) need(`places/${id}`, "places", o.parent_id);
}
for (const [id, o] of data.documents) {
  o.source_ids.forEach((s) => need(`documents/${id}`, "sources", s));
  (o.place_ids ?? []).forEach((p) => need(`documents/${id}`, "places", p));
  // Regla editorial: no se almacena ni descarga nada que no sea de dominio público o con licencia abierta.
  if (["almacenar", "descargar"].includes(o.rights.action) && !["public_domain", "cc0", "cc_by", "cc_by_sa"].includes(o.rights.status))
    errors.push(`documents/${id}: acción «${o.rights.action}» no permitida con derechos «${o.rights.status}»`);
}
for (const [id, o] of data.events) {
  o.place_ids.forEach((p) => need(`events/${id}`, "places", p));
  o.claims.forEach((c) => c.evidence.forEach((e) => need(`events/${id}`, "documents", e.document_id)));
}
for (const [id, o] of data.indicators) {
  o.source_ids.forEach((s) => need(`indicators/${id}`, "sources", s));
  o.observations.forEach((ob) => { need(`indicators/${id}`, "places", ob.place_id); need(`indicators/${id}`, "documents", ob.document_id); });
}
for (const [id, o] of data.stories) {
  o.scenes.forEach((s) => {
    (s.event_ids ?? []).forEach((e) => need(`stories/${id}`, "events", e));
    (s.place_ids ?? []).forEach((p) => need(`stories/${id}`, "places", p));
    s.claims.forEach((c) => c.evidence.forEach((e) => need(`stories/${id}`, "documents", e.document_id)));
  });
}

const counts = Object.entries(data).map(([k, m]) => `${k}=${m.size}`).join(" ");
if (errors.length) {
  console.error(`✗ ${errors.length} errores (${counts})`);
  errors.forEach((e) => console.error("  " + e));
  process.exit(1);
}
console.log(`✓ datos válidos (${counts})`);
