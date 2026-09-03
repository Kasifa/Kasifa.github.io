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
const figureId = "fig-r074z-remote-persistence-gate";

test("R0.74Z Step 25 reader publishes the exact persistence gate and stop line", () => {
  const note = read("public/notes/r0-74z.html");
  for (const marker of [
    "PERSISTENT TUBE PROVED",
    "STRICT SIDE ONLY",
    "TIME-TAME CONDITIONAL",
    "CRITICAL OPEN",
    "FULL CLOCK OPEN",
    "limsup",
    "kappa_*",
    "Z.22",
    "moving-strip all-winding uniformity",
    "arbitrary exponentially ill-conditioned finite family",
    "Z.39",
    "finite literature non-hit",
    "ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NO NOVELTY CLAIM | NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 300_000);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 1);
  assert.ok(note.includes(`/assets/r074z/${figureId}.svg`));
  assert.ok(note.includes("R0.75A、R0.75B 与其他未列工作未读取、未公开"));
  assert.ok(!note.includes("/assets/r075a/"));
  assert.ok(!note.includes("/assets/r075b/"));
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
});

test("R0.74Z Step 25 figure validation and public masters preserve the frozen boundary", () => {
  const canonicalRoot = `research/figures/r074z/${figureId}`;
  const names = readdirSync(resolve(root, canonicalRoot)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort();
  assert.equal(names.length, 25);
  assert.equal(names.reduce((sum, name) => sum + statSync(resolve(root, canonicalRoot, name)).size, 0), 3032354);
  const validation = JSON.parse(read(`${canonicalRoot}/validation.json`));
  assert.equal(validation.status, "PASS");
  assert.equal(validation.visualQAConfirmed, true);
  assert.equal(validation.checks.claimBoundary.shellTubeHolderCoercivity, true);
  assert.equal(validation.checks.claimBoundary.strictSubcriticalKappaNoGoForWKinetic, true);
  assert.equal(validation.checks.claimBoundary.timeTamePersistenceConditional, true);
  assert.equal(validation.checks.claimBoundary.criticalLayerResolved, false);
  assert.equal(validation.checks.claimBoundary.movingStripAllWindingUniformityProved, false);
  assert.equal(validation.checks.claimBoundary.noveltyClaim, false);
  assert.equal(validation.checks.claimBoundary.clayClaim, false);
  for (const extension of ["svg", "pdf", "png"]) {
    assert.equal(sha(`public/assets/r074z/${figureId}.${extension}`), sha(`${canonicalRoot}/figure.${extension}`));
  }
});

test("R0.74Z Step 25 reader PDF is bound while the R0.74S recap is preserved", () => {
  const binding = JSON.parse(read("research/r074z_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r074z-step25-note-synchronized-pdf-binding-v1");
  assert.equal(binding.step, 25);
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74z.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74z.pdf"));
  assert.equal(binding.publicPdf.pageCount, 111);
  assert.equal(binding.claimBoundary.persistentTubeHolderCoercivityProved, true);
  assert.equal(binding.claimBoundary.endpointToTubePersistence, "CONDITIONAL ON Z.22 AND MOVING-STRIP ALL-WINDING UNIFORMITY");
  assert.equal(binding.claimBoundary.criticalLayerClosed, false);
  assert.equal(binding.claimBoundary.accumulatedClockRowsControlled, false);
  assert.equal(binding.claimBoundary.fullClockY57Proved, false);
  assert.equal(binding.claimBoundary.fixedDeletionClosed, false);
  assert.equal(binding.claimBoundary.noveltyPriorityCorrectnessOrPublishabilityClaim, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.figure.assets.length, 3);
  assert.equal(sha("public/recap-r0-61-r0-74s.html"), "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81");
  assert.equal(sha("public/recap-r0-61-r0-74s.pdf"), "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec");
});

test("R0.74Z Step 25 routes, accounting, boundary, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  for (const marker of ["R0.74Z Step 25", "PERSISTENCE GATE", "time-tame", "NEXT · R0.75A FROZEN PACKAGE REQUIRED"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.74Z Step 25 的 bounded literature screen", "finite primary-source non-hit", "critical layer", "full-clock", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.equal(version.version, "2.04");
  assert.equal(version.publicHtmlNoteCount, 228);
  assert.equal(version.publicPdfNoteCount, 185);
  assert.equal(version.postR060PublishedNodeCount, 168);
  assert.equal(version.postR060RecapNodeCount, 161);
  assert.equal(version.latestRecapRelease, "R0.74S");
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 130);
  assert.equal(inventory.formalSealedReleaseCount, 103);
  assert.equal(inventory.publishedReleases.filter((row) => row === "r074z").length, 1);
  assert.equal(inventory.formalSealedReleases.filter((row) => row === "r074z").length, 1);
  assert.equal(inventory.formalFigureExemptReleaseCount, 3);
  assert.equal(inventory.formalFigureExemptReleases.includes("r074z"), false);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedStep, 25);
  assert.equal(manifest.nextRelease, "r075a");
  assert.equal(manifest.latestReleaseGate, "tests/r074z-step25-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r074z-step25-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r074z-step25-pdf.mjs");
  assert.equal(manifest.latestReleaseStepTranslationScript, "scripts/add-r074z-step25-translations.mjs");
  assert.equal(manifest.latestReleaseBrowserQaScript, "scripts/qa-r074z-step25-browser.mjs");
  assert.equal(manifest.latestReleaseOnlineVerifierScript, "scripts/verify-r074z-step25-online.mjs");
  assert.deepEqual(manifest.latestPublicationIdentity, {
    releaseId: "r074z-step25",
    handoffCommit: "90c6ceedb0e1f9fff02a32a81356376e138cc428",
    sourceCommit: "91aaac829c6b54a0ad24cf10ff3f533f58a10035",
    coreCommit: "91aaac829c6b54a0ad24cf10ff3f533f58a10035",
    figureSourceCommit: "30ed47c9ae2334a9e9cb3468a5094dfb3dc65907",
    formalFigureRequired: true,
    recapRequired: false,
  });
  assert.equal(manifest.latestFormalFigurePublication.inventory.files, 25);
  assert.equal(manifest.latestFormalFigurePublication.inventory.bytes, 3032354);
  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r074z-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 108/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
