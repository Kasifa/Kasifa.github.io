import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const readBytes = (path) => readFileSync(resolve(root, path));
const read = (path) => readBytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(readBytes(path)).digest("hex");
const node = process.env.CODEX_NODE || process.execPath;
const figureId = "fig-r074w-remote-adjacent-inward-threshold";

test("R0.74W Step 22 reader publishes the exact relative-probability and fixed-deletion boundary", () => {
  const note = read("public/notes/r0-74w.html");
  for (const marker of [
    "RELATIVE PROBABILITY",
    "UNIFORM SLAB",
    "ALL WINDINGS RETAINED",
    "q_{65}",
    "q_{64}",
    "12191}{132088320}",
    "matching all-shell",
    "fixed deletion",
    "bounded non-hit",
    "ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 250_000);
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
});

test("R0.74W Step 22 figure archive, mirrors, and public masters are byte exact", () => {
  const canonicalRoot = `research/figures/r074w/${figureId}`;
  const names = readdirSync(resolve(root, canonicalRoot)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort();
  assert.equal(names.length, 25);
  assert.equal(names.reduce((sum, name) => sum + statSync(resolve(root, canonicalRoot, name)).size, 0), 3774363);
  assert.deepEqual(readdirSync(resolve(root, `figures/r074w/${figureId}`)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
  assert.deepEqual(readdirSync(resolve(root, `public/figures/r074w/${figureId}`)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
  for (const name of names) {
    assert.equal(sha(`figures/r074w/${figureId}/${name}`), sha(`${canonicalRoot}/${name}`), name);
    assert.equal(sha(`public/figures/r074w/${figureId}/${name}`), sha(`${canonicalRoot}/${name}`), name);
  }
  const validation = JSON.parse(read(`${canonicalRoot}/validation.json`));
  assert.equal(validation.status, "PASS");
  assert.equal(validation.visualQAConfirmed, true);
  assert.equal(Object.keys(validation.checks).length, 12);
  assert.equal(validation.checks.claimBoundary.fixedDeletionResolved, false);
  assert.equal(validation.checks.claimBoundary.weightedPacket2EndpointDivergence, true);
  for (const extension of ["svg", "pdf", "png"]) {
    assert.equal(sha(`public/assets/r074w/${figureId}.${extension}`), sha(`${canonicalRoot}/figure.${extension}`));
  }
});

test("R0.74W Step 22 reader PDF is bound while the R0.74S recap is preserved", () => {
  const binding = JSON.parse(read("research/r074w_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r074w-step22-note-synchronized-pdf-binding-v1");
  assert.equal(binding.step, 22);
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74w.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74w.pdf"));
  assert.ok(binding.publicPdf.pageCount >= 90);
  assert.equal(binding.claimBoundary.relativeProbabilityStatement, true);
  assert.equal(binding.claimBoundary.uniformSlabSurvivalBelowQ65, true);
  assert.equal(binding.claimBoundary.uniformSlabSweepingAboveQ64, true);
  assert.equal(binding.claimBoundary.frozenPlacementMatchingAllShellUpper, false);
  assert.equal(binding.claimBoundary.fixedDeletionResolved, false);
  assert.equal(binding.claimBoundary.noveltyPriorityCorrectnessOrPublishabilityClaim, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.figure.assets.length, 3);
  assert.equal(sha("public/recap-r0-61-r0-74s.html"), "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81");
  assert.equal(sha("public/recap-r0-61-r0-74s.pdf"), "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec");
});

test("R0.74W Step 22 routes, accounting, literature boundary, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  for (const marker of ["R0.74W Step 22", "relative threshold", "fixed deletion", "NEXT · FROZEN PACKAGE REQUIRED"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.74W Step 22 的 bounded literature screen", "finite primary-source non-hit", "fixed deletion", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.equal(version.version, "2.01");
  assert.equal(version.publicHtmlNoteCount, 225);
  assert.equal(version.publicPdfNoteCount, 182);
  assert.equal(version.postR060PublishedNodeCount, 165);
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 127);
  assert.equal(inventory.formalSealedReleaseCount, 101);
  assert.equal(inventory.formalFigureExemptReleaseCount, 2);
  assert.equal(inventory.formalSealedReleases.filter((row) => row === "r074w").length, 1);
  assert.equal(inventory.formalFigureExemptReleases.includes("r074w"), false);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedStep, 22);
  assert.equal(manifest.latestReleaseGate, "tests/r074w-step22-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r074w-step22-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r074w-step22-pdf.mjs");
  assert.equal(manifest.latestReleaseStepTranslationScript, "scripts/add-r074w-step22-translations.mjs");
  assert.equal(manifest.latestReleaseBrowserQaScript, "scripts/qa-r074w-step22-browser.mjs");
  assert.equal(manifest.latestReleaseOnlineVerifierScript, "scripts/verify-r074w-step22-online.mjs");
  assert.deepEqual(manifest.latestPublicationIdentity, {
    releaseId: "r074w-step22",
    handoffCommit: "eb72349afeb5f7b02ee133b7c4d10466e2ae8ff4",
    sourceCommit: "f581c46ee7759c190b6f407633549e7106ff60b5",
    coreCommit: "f581c46ee7759c190b6f407633549e7106ff60b5",
    figureSourceCommit: "0143d65322a3c854fe220aa9d3e4f93a1f6ca09e",
    formalFigureRequired: true,
    recapRequired: false,
  });
  assert.equal(manifest.latestFormalFigurePublication.inventory.files, 25);
  assert.equal(manifest.latestFormalFigurePublication.inventory.bytes, 3774363);
  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r074w-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 110/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
