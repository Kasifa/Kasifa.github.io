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
const figureId = "fig-r074x-three-packet-payment-gate";

test("R0.74X Step 23 reader publishes the exact fixed-deletion and cubic-payment boundary", () => {
  const note = read("public/notes/r0-74x.html");
  for (const marker of [
    "TWO COORDINATES",
    "TIMES MAY DIFFER",
    "T* OBSTRUCTION PROVED",
    "ACTUAL GATE NOT PROVED",
    "CUBIC PAYMENT NO-GO",
    "3306805}{134120448}",
    "3062597}{134120448}",
    "X.52",
    "bounded non-hit",
    "ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 275_000);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 1);
  assert.ok(note.includes(`/assets/r074x/${figureId}.svg`));
  assert.ok(!note.includes("/assets/r074w/"));
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
});

test("R0.74X Step 23 figure archive, mirrors, and public masters are byte exact", () => {
  const canonicalRoot = `research/figures/r074x/${figureId}`;
  const names = readdirSync(resolve(root, canonicalRoot)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort();
  assert.equal(names.length, 25);
  assert.equal(names.reduce((sum, name) => sum + statSync(resolve(root, canonicalRoot, name)).size, 0), 3096940);
  assert.deepEqual(readdirSync(resolve(root, `figures/r074x/${figureId}`)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
  assert.deepEqual(readdirSync(resolve(root, `public/figures/r074x/${figureId}`)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
  for (const name of names) {
    assert.equal(sha(`figures/r074x/${figureId}/${name}`), sha(`${canonicalRoot}/${name}`), name);
    assert.equal(sha(`public/figures/r074x/${figureId}/${name}`), sha(`${canonicalRoot}/${name}`), name);
  }
  const validation = JSON.parse(read(`${canonicalRoot}/validation.json`));
  assert.equal(validation.status, "PASS");
  assert.equal(validation.visualQAConfirmed, true);
  assert.equal(Object.keys(validation.checks).length, 13);
  assert.equal(validation.checks.claimBoundary.actualPaymentNormalizedGateCounterexample, false);
  assert.equal(validation.checks.claimBoundary.twoCoordinateTstarEndpointObstruction, true);
  assert.equal(validation.checks.claimBoundary.equalTargetWStripRouteNoGo, true);
  for (const extension of ["svg", "pdf", "png"]) {
    assert.equal(sha(`public/assets/r074x/${figureId}.${extension}`), sha(`${canonicalRoot}/figure.${extension}`));
  }
});

test("R0.74X Step 23 reader PDF is bound while the R0.74S recap is preserved", () => {
  const binding = JSON.parse(read("research/r074x_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r074x-step23-note-synchronized-pdf-binding-v1");
  assert.equal(binding.step, 23);
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74x.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74x.pdf"));
  assert.ok(binding.publicPdf.pageCount >= 90);
  assert.equal(binding.claimBoundary.twoDistinctTStarNormalizedEndpointDivergences, true);
  assert.equal(binding.claimBoundary.fixedDeletionSetChosenBeforeTimeSupremum, true);
  assert.equal(binding.claimBoundary.witnessTimesMayDiffer, true);
  assert.equal(binding.claimBoundary.actualPaymentNormalizedCounterexampleProved, false);
  assert.equal(binding.claimBoundary.equalTargetWStripRoute, "NO-GO BY CUBIC PAYMENT");
  assert.equal(binding.claimBoundary.noveltyPriorityCorrectnessOrPublishabilityClaim, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.figure.assets.length, 3);
  assert.equal(sha("public/recap-r0-61-r0-74s.html"), "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81");
  assert.equal(sha("public/recap-r0-61-r0-74s.pdf"), "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec");
});

test("R0.74X Step 23 routes, accounting, literature boundary, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  for (const marker of ["R0.74X Step 23", "two-coordinate", "cubic payment", "NEXT · R0.74Y FROZEN PACKAGE REQUIRED"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.74X Step 23 的 bounded literature screen", "finite primary-source non-hit", "fixed-deletion", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.equal(version.version, "2.02");
  assert.equal(version.publicHtmlNoteCount, 226);
  assert.equal(version.publicPdfNoteCount, 183);
  assert.equal(version.postR060PublishedNodeCount, 166);
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 128);
  assert.equal(inventory.formalSealedReleaseCount, 102);
  assert.equal(inventory.formalFigureExemptReleaseCount, 2);
  assert.equal(inventory.formalSealedReleases.filter((row) => row === "r074x").length, 1);
  assert.equal(inventory.formalFigureExemptReleases.includes("r074x"), false);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedStep, 23);
  assert.equal(manifest.latestReleaseGate, "tests/r074x-step23-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r074x-step23-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r074x-step23-pdf.mjs");
  assert.equal(manifest.latestReleaseStepTranslationScript, "scripts/add-r074x-step23-translations.mjs");
  assert.equal(manifest.latestReleaseBrowserQaScript, "scripts/qa-r074x-step23-browser.mjs");
  assert.equal(manifest.latestReleaseOnlineVerifierScript, "scripts/verify-r074x-step23-online.mjs");
  assert.deepEqual(manifest.latestPublicationIdentity, {
    releaseId: "r074x-step23",
    handoffCommit: "9bddf4a591a159ac99f43602700a80f736dcc61b",
    sourceCommit: "802e5572b3490b326a03706c512f35ef6f5afa31",
    coreCommit: "802e5572b3490b326a03706c512f35ef6f5afa31",
    figureSourceCommit: "a5670383091098331b557869a57c6ed9b6fa72e9",
    formalFigureRequired: true,
    recapRequired: false,
  });
  assert.equal(manifest.latestFormalFigurePublication.inventory.files, 25);
  assert.equal(manifest.latestFormalFigurePublication.inventory.bytes, 3096940);
  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r074x-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 93/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
