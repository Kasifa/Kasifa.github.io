import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const readBytes = (path) => readFileSync(resolve(root, path));
const read = (path) => readBytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(readBytes(path)).digest("hex");
const node = process.env.CODEX_NODE || process.execPath;

test("R0.74Y Step 24 reader publishes the route screen with exact claim grades", () => {
  const note = read("public/notes/r0-74y.html");
  for (const marker of [
    "ROUTE SCREEN",
    "FROZEN NO-GO PROVED",
    "AGES DISTINCT",
    "AMPLITUDE CANCELS",
    "CANCELLATION WINDOW FORMAL",
    "Y.57 NOT PROVED",
    "875993}{968647680}",
    "16723709}{249570720000}",
    "DIMENSIONALLY DISFAVORED, BUT NOT YET CERTIFIED",
    "NO FORMAL FIGURE",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 290_000);
  assert.equal(note.includes('<section id="figure">'), false);
  assert.equal(note.includes("/assets/r074y/"), false);
  assert.equal(note.includes("/assets/r074x/"), false);
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
});

test("R0.74Y Step 24 PDF is bound while the R0.74S recap is preserved", () => {
  const binding = JSON.parse(read("research/r074y_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r074y-step24-note-synchronized-pdf-binding-v1");
  assert.equal(binding.step, 24);
  assert.equal(binding.kind, "payment-compatible-route-screen-note");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74y.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74y.pdf"));
  assert.ok(binding.publicPdf.pageCount >= 100);
  assert.equal(binding.claimBoundary.routeScreen, true);
  assert.equal(binding.claimBoundary.frozenGeometrySamePacketSelfPaymentNoGoProved, true);
  assert.equal(binding.claimBoundary.deficitAgeAndHeatAgeDistinct, true);
  assert.equal(binding.claimBoundary.changedGeometryRationalWindow, "FORMAL NECESSARY EXPONENTS ONLY");
  assert.equal(binding.claimBoundary.cancellationCellConstructed, false);
  assert.equal(binding.claimBoundary.propositionY57Proved, false);
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.dgxUsed, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(sha("public/recap-r0-61-r0-74s.html"), "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81");
  assert.equal(sha("public/recap-r0-61-r0-74s.pdf"), "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec");
});

test("R0.74Y Step 24 routes, accounting, boundary, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  for (const marker of ["R0.74Y Step 24", "ROUTE SCREEN", "formal necessary", "NEXT · R0.74Z FROZEN PACKAGE REQUIRED"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.74Y Step 24 的 bounded literature screen", "finite non-hit", "FORMAL NECESSARY ONLY", "NOT CERTIFIED", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.equal(version.version, "2.03");
  assert.equal(version.publicHtmlNoteCount, 227);
  assert.equal(version.publicPdfNoteCount, 184);
  assert.equal(version.postR060PublishedNodeCount, 167);
  assert.equal(version.postR060RecapNodeCount, 161);
  assert.equal(version.latestRecapRelease, "R0.74S");
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 129);
  assert.equal(inventory.formalSealedReleaseCount, 102);
  assert.equal(inventory.publishedReleases.filter((row) => row === "r074y").length, 1);
  assert.equal(inventory.formalSealedReleases.filter((row) => row === "r074y").length, 0);
  assert.equal(inventory.formalFigureExemptReleaseCount, 3);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r074y").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedStep, 24);
  assert.equal(manifest.nextRelease, "r074z");
  assert.equal(manifest.latestReleaseGate, "tests/r074y-step24-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r074y-step24-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r074y-step24-pdf.mjs");
  assert.equal(manifest.latestReleaseStepTranslationScript, "scripts/add-r074y-step24-translations.mjs");
  assert.equal(manifest.latestReleaseBrowserQaScript, "scripts/qa-r074y-step24-browser.mjs");
  assert.equal(manifest.latestReleaseOnlineVerifierScript, "scripts/verify-r074y-step24-online.mjs");
  assert.deepEqual(manifest.latestPublicationIdentity, {
    releaseId: "r074y-step24",
    handoffCommit: "87e32a45c78ee7131a919ebb51768714cd561b62",
    sourceCommit: "e75ccf1197484d0e551e8073f409e6a39b248564",
    coreCommit: "e75ccf1197484d0e551e8073f409e6a39b248564",
    formalFigureRequired: false,
    recapRequired: false,
  });
  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r074y-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 102/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
