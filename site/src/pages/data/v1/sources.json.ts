import { sources } from "../../../lib/data";
export function GET() {
  return new Response(JSON.stringify({ version: "v1", generated: new Date().toISOString().slice(0, 10), license: "Datos propios CC BY-SA 4.0; datos de terceros según el campo rights de cada objeto", count: sources.length, items: sources }), { headers: { "Content-Type": "application/json; charset=utf-8" } });
}
