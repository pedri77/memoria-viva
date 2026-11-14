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

// robots.txt: se respeta el grupo «User-agent: *». Una URL vetada no se pide: se marca como «omitida».
const robotsCache = new Map();
async function robotsRules(origin) {
  if (robotsCache.has(origin)) return robotsCache.get(origin);
  const rules = [];
  try {
    const r = await fetch(`${origin}/robots.txt`, { headers: { "User-Agent": UA }, signal: AbortSignal.timeout(20000) });
    if (r.ok) {
      let applies = false, lastWasAgent = false;
      for (const raw of (await r.text()).split(/\r?\n/)) {
        const line = raw.replace(/#.*/, "").trim();
        const m = line.match(/^([A-Za-z-]+)\s*:\s*(.*)$/);
        if (!m) continue;
        const [, k, v] = m; const key = k.toLowerCase();
        if (key === "user-agent") { applies = lastWasAgent ? applies || v === "*" : v === "*"; lastWasAgent = true; continue; }
        lastWasAgent = false;
        if (applies && (key === "disallow" || key === "allow") && v) rules.push({ allow: key === "allow", path: v });
      }
    }
  } catch {}
  robotsCache.set(origin, rules);
  return rules;
}
const toRe = (p) => new RegExp("^" + p.replace(/[.+?^${}()|[\]\\]/g, "\\$&").replace(/\*/g, ".*").replace(/\\\$$/, "$"));
async function allowed(u) {
  const { origin, pathname, search } = new URL(u);
  const path = pathname + search;
  let best = null;
  for (const r of await robotsRules(origin)) {
    if (toRe(r.path).test(path) && (!best || r.path.length > best.path.length || (r.path.length === best.path.length && r.allow))) best = r;
  }
  return !best || best.allow;
}

let bad = 0, skipped = 0, warn = 0;
for (const [u, where] of urls) {
  if (!(await allowed(u))) { skipped++; console.log(`- robots ${u}  (${where})`); continue; }
  let status = "ERR";
  try {
    const r = await fetch(u, { headers: { "User-Agent": UA }, redirect: "follow", signal: AbortSignal.timeout(30000) });
    status = r.status;
    r.body?.cancel();
  } catch (e) { status = e.name; }
  // 403 suele ser protección antibot (p. ej. BNE): aviso, no error.
  // Una fuente caída es un aviso (el registro lo recoge); un documento citado roto es un error.
  const ok = typeof status === "number" && (status < 400 || status === 403);
  const isSource = where.startsWith("sources/");
  if (!ok && !isSource) bad++;
  if (!ok && isSource) warn++;
  console.log(`${ok ? (status === 403 ? "!" : "✓") : isSource ? "!" : "✗"} ${status} ${u}  (${where})`);
  await sleep(1000);
}
console.log(`${bad ? "✗" : "✓"} ${urls.size} enlaces: ${bad} rotos en documentos, ${warn} fuentes caídas (aviso), ${skipped} omitidos por robots.txt`);
process.exit(bad ? 1 : 0);
