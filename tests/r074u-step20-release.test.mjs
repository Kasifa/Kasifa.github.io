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

test("R0.74U Step 20 reader publishes the exact lower-only K boundary", () => {
  const note = read("public/notes/r0-74u.html");
  for (const marker of [
    "U.21-U.25",
    "U.33",
    "U.34-U.35",
    "U.36-U.41",
    "U.45",
    "K-SUPERLEVEL LOWER ONLY",
    "603445}{89413632}",
    "869 exact finite cases",
    "1,651 Rational assertions",
    "Inage（2026）",
    "ANALYTIC SCHEMATIC / DERIVED ANALYTIC VALUES / NOT PDE DATA / NOT DNS / NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 90000);
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
});

test("R0.74U Step 20 figure archive and all mirrors are byte exact", () => {
  const id = "fig-r074u-intrinsic-certified-residence";
  const canonicalRoot = `research/figures/r074u/${id}`;
  const names = readdirSync(resolve(root, canonicalRoot)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort();
  assert.equal(names.length, 25);
  assert.deepEqual(readdirSync(resolve(root, `figures/r074u/${id}`)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
  assert.deepEqual(readdirSync(resolve(root, `public/figures/r074u/${id}`)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
  for (const name of names) {
    assert.equal(sha(`figures/r074u/${id}/${name}`), sha(`${canonicalRoot}/${name}`), name);
    assert.equal(sha(`public/figures/r074u/${id}/${name}`), sha(`${canonicalRoot}/${name}`), name);
  }
  const validation = JSON.parse(read(`${canonicalRoot}/validation.json`));
  assert.equal(validation.checkCount, 47);
  assert.equal(validation.checks.length, 47);
  assert.ok(validation.checks.every((row) => row.pass));
  const manifest = JSON.parse(read(`${canonicalRoot}/manifest.json`));
  assert.equal(manifest.inventory.count, 25);
  assert.equal(manifest.claimBoundary.fullClockSuperlevelLowerOnly, true);
  assert.equal(manifest.claimBoundary.fullClockUpperBound, false);
  for (const extension of ["svg", "pdf", "png"]) {
    assert.equal(sha(`public/assets/r074u/${id}.${extension}`), sha(`${canonicalRoot}/figure.${extension}`));
  }
});

test("R0.74U Step 20 PDF is bound while the Step 17 recap is preserved", () => {
  const binding = JSON.parse(read("research/r074u_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r074u-step20-note-synchronized-pdf-binding-v1");
  assert.equal(binding.step, 20);
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74u.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74u.pdf"));
  assert.ok(binding.publicPdf.pageCount >= 85);
  assert.deepEqual(binding.claimBoundary.proved, ["U.21-U.25", "U.33", "U.34-U.35 lower only", "U.36-U.41", "U.45"]);
  assert.equal(binding.claimBoundary.certifiedGeometricCorridorUpperTransfersToFullKSuperlevel, false);
  assert.equal(binding.claimBoundary.fullKSuperlevelLowerOnly, true);
  assert.equal(binding.claimBoundary.pdeData, false);
  assert.equal(binding.claimBoundary.navierStokesCounterexample, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(sha("public/recap-r0-61-r0-74s.html"), "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81");
  assert.equal(sha("public/recap-r0-61-r0-74s.pdf"), "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec");
});

test("R0.74U Step 20 routes, accounting, literature boundary, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  for (const marker of ["R0.74U Step 20", "Theta(L_iR^3)", "K-superlevel", "NEXT · FROZEN PACKAGE"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.74U Step 20 的文献近碰撞与主张边界", "Inage（2026）", "terminology-level near collision", "lower-only", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.equal(version.version, "1.99");
  assert.equal(version.publicHtmlNoteCount, 223);
  assert.equal(version.publicPdfNoteCount, 180);
  assert.equal(version.postR060PublishedNodeCount, 163);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedStep, 20);
  assert.equal(manifest.latestReleaseGate, "tests/r074u-step20-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r074u-step20-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r074u-step20-pdf.mjs");
  assert.equal(manifest.latestReleaseStepTranslationScript, "scripts/add-r074u-step20-translations.mjs");
  assert.equal(manifest.latestReleaseBrowserQaScript, "scripts/qa-r074u-step20-browser.mjs");
  assert.equal(manifest.latestReleaseOnlineVerifierScript, "scripts/verify-r074u-step20-online.mjs");
  assert.deepEqual(manifest.latestPublicationIdentity, {
    releaseId: "r074u-step20",
    handoffCommit: "f3031095b7dfa51837df511f5b015bacb34c473b",
    sourceCommit: "735030d9e51068518796a79571ada291c5414a06",
    coreCommit: "d74e7b297928147334136f4c3cb29c5226d66381",
    figureSourceCommit: "8b75193df63a962392f89fcf1dbc20a8411334ba",
  });
  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r074u-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 85/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
