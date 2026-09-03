import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const readBytes = (path) => readFileSync(resolve(root, path));
const read = (path) => readBytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(readBytes(path)).digest("hex");
const node = process.env.CODEX_NODE || process.execPath;

test("R0.74S Step 18 reader publishes the exact proved, abstract, and open boundary", () => {
  const note = read("public/notes/r0-74s.html");
  for (let number = 476; number <= 493; number += 1) assert.ok(note.includes(`S.${number}`), `S.${number}`);
  for (const marker of [
    "moving deletion ≤ fixed deletion ≤ separable maximum",
    "target-scale equivalence",
    "ABSTRACT information-theoretic obstruction",
    "不是 Navier--Stokes 反例",
    "S.486、S.487、direct hybrid、S.472、S.407、Q.12、Q.1",
    "NOT PDE DATA / NOT DNS / NOT CLAY",
    "283,157",
    "72,144 assertions",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 80000);
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
});

test("R0.74S Step 18 four-panel archive and all mirrors are byte exact", () => {
  const id = "fig-r074s-fixed-deletion-quantifier-gap";
  const canonicalRoot = `research/figures/r074s/${id}`;
  const names = readdirSync(resolve(root, canonicalRoot)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort();
  assert.equal(names.length, 25);
  assert.deepEqual(readdirSync(resolve(root, `figures/r074s/${id}`)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
  assert.deepEqual(readdirSync(resolve(root, `public/figures/r074s/${id}`)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
  for (const name of names) {
    assert.equal(sha(`figures/r074s/${id}/${name}`), sha(`${canonicalRoot}/${name}`), name);
    assert.equal(sha(`public/figures/r074s/${id}/${name}`), sha(`${canonicalRoot}/${name}`), name);
  }
  const validation = JSON.parse(read(`${canonicalRoot}/validation.json`));
  assert.equal(validation.checkCount, 39);
  assert.equal(validation.checks.length, 39);
  assert.ok(validation.checks.every((row) => row.pass));
  assert.equal(JSON.parse(read(`${canonicalRoot}/manifest.json`)).inventory.count, 25);
  for (const extension of ["svg", "pdf", "png"]) {
    assert.equal(sha(`public/assets/r074s/${id}.${extension}`), sha(`${canonicalRoot}/figure.${extension}`));
  }
});

test("R0.74S Step 18 note PDF is bound while the Step 17 recap is preserved", () => {
  const binding = JSON.parse(read("research/r074s_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r074s-step18-note-synchronized-pdf-binding-v1");
  assert.equal(binding.step, 18);
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74s.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74s.pdf"));
  assert.ok(binding.publicPdf.pageCount >= 80);
  assert.deepEqual(binding.claimBoundary.proved, ["S.476-S.485", "S.488-S.493"]);
  assert.equal(binding.claimBoundary.pdeData, false);
  assert.equal(binding.claimBoundary.navierStokesCounterexample, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(sha("public/recap-r0-61-r0-74s.html"), "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81");
  assert.equal(sha("public/recap-r0-61-r0-74s.pdf"), "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec");
});

test("R0.74S Step 18 routes, accounting, and bilingual snapshot are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  for (const marker of ["R0.74S Step 18", "fixed deletion", "simultaneous height", "等待同一发布任务中的下一份明确冻结包"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.74S Step 18 的文献与主张边界", "ABSTRACT ONLY", "FINITE", "OPEN", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.equal(version.version, "1.97");
  assert.equal(version.publicHtmlNoteCount, 221);
  assert.equal(version.publicPdfNoteCount, 178);
  assert.equal(version.postR060PublishedNodeCount, 161);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedStep, 18);
  assert.equal(manifest.latestReleaseGate, "tests/r074s-step18-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r074s-step18-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r074s-step18-pdf.mjs");
  assert.equal(manifest.latestReleaseStepTranslationScript, "scripts/add-r074s-step18-translations.mjs");
  assert.equal(manifest.latestReleaseBrowserQaScript, "scripts/qa-r074s-step18-browser.mjs");
  assert.equal(manifest.latestReleaseOnlineVerifierScript, "scripts/verify-r074s-step18-online.mjs");
  assert.deepEqual(manifest.latestPublicationIdentity, {
    releaseId: "r074s-step18",
    sourceCommit: "5a9c172e1db8886d49fdf15b8676b4810b002ae3",
    figureSeal: "963613d54303eb240c1daa40c57ffc106a92535b",
  });
  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r074s-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 128/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
