// Prueba de extremo a extremo de la retirada de un objeto.
// 1) marca como retirado un documento que nadie cita; 2) valida y compila;
// 3) comprueba que su URL muestra el aviso, que no aparece en listados, JSON ni búsqueda;
// 4) comprueba que retirar un documento citado hace fallar la validación; 5) restaura todo.
import { readFileSync, writeFileSync, existsSync } from "node:fs";
import { execSync } from "node:child_process";
import { join, dirname } from "node:path";
import { fileURLToPath } from "node:url";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..", "..");
const sh = (c) => execSync(c, { cwd: ROOT, stdio: "pipe", encoding: "utf8" });
const DOC = "doc-bne-0034-771x-revista-de-archivos-bibliotecas-y-museos";
const CITED = "doc-gaceta-1931-05-30";
const fDoc = join(ROOT, "data/canonical/documents", `${DOC}.json`);
const fCited = join(ROOT, "data/canonical/documents", `${CITED}.json`);
const orig = readFileSync(fDoc, "utf8"), origCited = readFileSync(fCited, "utf8");
const fails = [];
const check = (ok, msg) => { console.log(`${ok ? "✓" : "✗"} ${msg}`); if (!ok) fails.push(msg); };
const retire = (txt, note) => { const o = JSON.parse(txt); o.review = { status: "retirado", date: "2026-11-14", by: ["prueba"], note }; return JSON.stringify(o, null, 2); };
try {
  writeFileSync(fDoc, retire(orig, "Prueba automática de retirada."));
  sh("npm run -s build");
  const page = join(ROOT, "dist/documentos", DOC, "index.html");
  check(existsSync(page) && readFileSync(page, "utf8").includes("Contenido retirado"), "la URL original muestra el aviso de retirada");
  check(!readFileSync(join(ROOT, "dist/documentos/index.html"), "utf8").includes(DOC), "no aparece en el listado del archivo");
  check(!JSON.parse(readFileSync(join(ROOT, "dist/data/v1/documents.json"), "utf8")).items.some((d) => d.id === DOC), "no aparece en el JSON público");
  check(!readFileSync(page, "utf8").includes("data-pagefind-body"), "su página no se indexa en la búsqueda");
  check(readFileSync(join(ROOT, "dist/cambios/index.html"), "utf8").includes("Prueba automática de retirada."), "figura en el registro de cambios con su motivo");
  writeFileSync(fDoc, orig);
  writeFileSync(fCited, retire(origCited, "Prueba: documento citado."));
  let failed = false; try { sh("npm run -s validate"); } catch { failed = true; }
  check(failed, "retirar un documento citado por un acontecimiento hace fallar la validación");
} finally {
  writeFileSync(fDoc, orig); writeFileSync(fCited, origCited);
  sh("npm run -s build");
}
console.log(fails.length ? `✗ ${fails.length} comprobaciones fallidas` : "✓ retirada probada de extremo a extremo");
process.exit(fails.length ? 1 : 0);
