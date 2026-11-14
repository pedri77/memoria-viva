// Comprueba que las URL citadas en documentos y fuentes responden.
// Petición GET ligera, una cada segundo, para no cargar a los custodios.
import { readFileSync, readdirSync } from "node:fs";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const urls = new Map();
for (const kind of ["documents", "sources"]) {
  const dir = join(ROOT, "data/canonical", kind);
  for (const f of readdirSync(dir).filter((x) => x.endsWith(".json"))) {
    const o = JSON.parse(readFileSync(join(dir, f), "utf8"));
    for (const u of [o.canonical_url, o.url, o.rights?.evidence_url]) if (u) urls.set(u, `${kind}/${f}`);
  }
}
const UA = "memoria-viva-linkcheck/0.1 (+https://github.com/pedri77/memoria-viva)";
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
let bad = 0;
for (const [u, where] of urls) {
  let status = "ERR";
  try {
    const r = await fetch(u, { headers: { "User-Agent": UA }, redirect: "follow", signal: AbortSignal.timeout(30000) });
    status = r.status;
    r.body?.cancel();
  } catch (e) { status = e.name; }
  // 403 suele ser protección antibot (p. ej. BNE): aviso, no error.
  const ok = typeof status === "number" && (status < 400 || status === 403);
  if (!ok) bad++;
  console.log(`${ok ? (status === 403 ? "!" : "✓") : "✗"} ${status} ${u}  (${where})`);
  await sleep(1000);
}
console.log(bad ? `✗ ${bad} enlaces rotos de ${urls.size}` : `✓ ${urls.size} enlaces comprobados`);
process.exit(bad ? 1 : 0);
