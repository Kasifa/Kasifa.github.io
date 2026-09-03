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

test("R0.74V Step 21 reader is explicitly a route memo", () => {
  const note = read("public/notes/r0-74v.html");
  for (const marker of [
    "ROUTE MEMO",
    "EXACT DECOMPOSITIONS",
    "COARSE BUDGETS",
    "CONDITIONAL ALGEBRA",
    "V.47-V.50 OPEN",
    "V.56 OPEN",
    "ell_k=s_k+s_k^3",
    "12191}{132088320}",
    "remote common-shear comparison：OPEN",
    "没有文献审计",
    "没有科学图、DNS、仿真或 PDE 数据",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 90000);
  assert.equal(note.includes('<section id="figure">'), false);
  assert.equal(note.includes("/assets/r074v/"), false);
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
});

test("R0.74V Step 21 PDF is bound while the Step 17 recap is preserved", () => {
  const binding = JSON.parse(read("research/r074v_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r074v-step21-note-synchronized-pdf-binding-v1");
  assert.equal(binding.step, 21);
  assert.equal(binding.kind, "route-memo-note");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74v.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74v.pdf"));
  assert.ok(binding.publicPdf.pageCount >= 88);
  assert.equal(binding.claimBoundary.routeMemo, true);
  assert.equal(binding.claimBoundary.completedClockUpperTheorem, false);
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.literatureAudit, false);
  assert.equal(binding.claimBoundary.noveltyPriorityOrPublishabilityClaim, false);
  assert.equal(binding.claimBoundary.pdeData, false);
  assert.equal(binding.claimBoundary.dns, false);
  assert.equal(binding.claimBoundary.simulation, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(sha("public/recap-r0-61-r0-74s.html"), "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81");
  assert.equal(sha("public/recap-r0-61-r0-74s.pdf"), "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec");
});

test("R0.74V Step 21 routes, accounting, boundary, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  for (const marker of ["R0.74V Step 21", "ROUTE MEMO", "V.47-V.50", "NEXT · R0.74W FROZEN PACKAGE"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.74V Step 21 路线与主张边界", "没有 literature audit", "V.56", "remote/adjacent-inward", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.equal(version.version, "2.00");
  assert.equal(version.publicHtmlNoteCount, 224);
  assert.equal(version.publicPdfNoteCount, 181);
  assert.equal(version.postR060PublishedNodeCount, 164);
  assert.equal(version.postR060RecapNodeCount, 161);
  assert.equal(version.latestRecapRelease, "R0.74S");
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 126);
  assert.equal(inventory.formalSealedReleaseCount, 100);
  assert.equal(inventory.publishedReleases.filter((row) => row === "r074v").length, 1);
  assert.equal(inventory.formalSealedReleases.filter((row) => row === "r074v").length, 0);
  assert.equal(inventory.formalFigureExemptReleaseCount, 2);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r074v").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedStep, 21);
  assert.equal(manifest.nextRelease, "r074w");
  assert.equal(manifest.latestReleaseGate, "tests/r074v-step21-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r074v-step21-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r074v-step21-pdf.mjs");
  assert.equal(manifest.latestReleaseStepTranslationScript, "scripts/add-r074v-step21-translations.mjs");
  assert.equal(manifest.latestReleaseBrowserQaScript, "scripts/qa-r074v-step21-browser.mjs");
  assert.equal(manifest.latestReleaseOnlineVerifierScript, "scripts/verify-r074v-step21-online.mjs");
  assert.deepEqual(manifest.latestPublicationIdentity, {
    releaseId: "r074v-step21",
    handoffCommit: "2bd41a53800b2d6f532b6843f4d70ad7fad7ed46",
    sourceCommit: "29f2b56d1a1a22b665de4b36736eeea20c0a0039",
    coreCommit: "29f2b56d1a1a22b665de4b36736eeea20c0a0039",
    formalFigureRequired: false,
    recapRequired: false,
  });
  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r074v-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 81/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
