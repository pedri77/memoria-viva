// Carga los datos canónicos en tiempo de build. Fuente de verdad: data/canonical/.
type Json = Record<string, any>;
const loadAll = (mods: Record<string, unknown>) =>
  Object.values(mods).map((m: any) => (m.default ?? m) as Json);
// Los objetos retirados no se publican en listados, JSON ni búsqueda; su URL muestra un aviso.
export const retired: Record<string, Json[]> = {};
const load = (mods: Record<string, unknown>, kind = "otros") =>
  loadAll(mods).filter((o) => (o.review?.status === "retirado" ? ((retired[kind] ??= []).push(o), false) : true));

export const sources = load(import.meta.glob("../../../data/canonical/sources/*.json", { eager: true }), "sources")
  .sort((a, b) => a.id.localeCompare(b.id));
export const places = load(import.meta.glob("../../../data/canonical/places/*.json", { eager: true }), "places");
export const documents = load(import.meta.glob("../../../data/canonical/documents/*.json", { eager: true }), "documents");
export const stories = load(import.meta.glob("../../../data/canonical/stories/*.json", { eager: true }), "stories");
export const indicators = load(import.meta.glob("../../../data/canonical/indicators/*.json", { eager: true }), "indicators");
export const events = load(import.meta.glob("../../../data/canonical/events/*.json", { eager: true }), "events")
  .sort((a, b) => a.start_date.localeCompare(b.start_date));

export const byId = <T extends Json>(list: T[], id: string) => list.find((x) => x.id === id);
export const url = (path: string) => `${import.meta.env.BASE_URL}${path}`.replace(/\/{2,}/g, "/");

export const RIGHTS_LABEL: Record<string, string> = {
  public_domain: "Dominio público",
  cc0: "CC0",
  cc_by: "CC BY",
  cc_by_sa: "CC BY-SA",
  reuse_conditions: "Reutilizable con condiciones del custodio",
  reuse_open: "Reutilización abierta con cita (Ley 37/2007)",
  link_only: "Solo enlace",
  restricted: "Acceso restringido",
};
export const KIND_LABEL: Record<string, string> = {
  hecho: "Hecho documentado",
  documento: "Según el documento",
  interpretacion: "Interpretación atribuida",
  estimacion: "Estimación",
};
export const PRECISION_LABEL: Record<string, string> = {
  dia: "día exacto", mes: "mes", anio: "año", decada: "década",
  aproximada: "fecha aproximada", intervalo: "intervalo", desconocida: "fecha desconocida",
};
