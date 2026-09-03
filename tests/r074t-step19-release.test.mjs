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

test("R0.74T Step 19 reader publishes the exact proved and open boundary", () => {
  const note = read("public/notes/r0-74t.html");
  for (const number of [1, 2, 4, 6, 7, 9, 10, 11, 12, 15, 16, 17, 18, 21, 23, 24, 25, 26, 28, 29, 30, 31, 33, 34, 35, 36, 39, 41, 42, 43]) {
    assert.ok(note.includes(`T.${number}`), `T.${number}`);
  }
  for (const marker of [
    "精确 Hölder coercivity",
    "K-clock fixed-deletion witness",
    "full clock upper bound",
    "603445}{89413632}",
    "18,933",
    "9,201 assertions",
    "ANALYTIC SCHEMATIC / DERIVED ANALYTIC VALUES / NOT PDE DATA / NOT DNS / NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 80000);
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
});

test("R0.74T Step 19 figure archive and all mirrors are byte exact", () => {
  const id = "fig-r074t-schedule-invariant-dwell-barrier";
  const canonicalRoot = `research/figures/r074t/${id}`;
  const names = readdirSync(resolve(root, canonicalRoot)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort();
  assert.equal(names.length, 25);
  assert.deepEqual(readdirSync(resolve(root, `figures/r074t/${id}`)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
  assert.deepEqual(readdirSync(resolve(root, `public/figures/r074t/${id}`)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort(), names);
  for (const name of names) {
    assert.equal(sha(`figures/r074t/${id}/${name}`), sha(`${canonicalRoot}/${name}`), name);
    assert.equal(sha(`public/figures/r074t/${id}/${name}`), sha(`${canonicalRoot}/${name}`), name);
  }
  const validation = JSON.parse(read(`${canonicalRoot}/validation.json`));
  assert.equal(validation.checkCount, 47);
  assert.equal(validation.checks.length, 47);
  assert.ok(validation.checks.every((row) => row.pass));
  assert.equal(JSON.parse(read(`${canonicalRoot}/manifest.json`)).inventory.count, 25);
  for (const extension of ["svg", "pdf", "png"]) {
    assert.equal(sha(`public/assets/r074t/${id}.${extension}`), sha(`${canonicalRoot}/figure.${extension}`));
  }
});

test("R0.74T Step 19 note PDF is bound while the Step 17 recap is preserved", () => {
  const binding = JSON.parse(read("research/r074t_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r074t-step19-note-synchronized-pdf-binding-v1");
  assert.equal(binding.step, 19);
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74t.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74t.pdf"));
  assert.ok(binding.publicPdf.pageCount >= 80);
  assert.deepEqual(binding.claimBoundary.proved, ["T.9-T.10", "T.17", "T.24-T.29", "T.34-T.43"]);
  assert.equal(binding.claimBoundary.pdeData, false);
  assert.equal(binding.claimBoundary.navierStokesCounterexample, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(sha("public/recap-r0-61-r0-74s.html"), "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81");
  assert.equal(sha("public/recap-r0-61-r0-74s.pdf"), "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec");
});

test("R0.74T Step 19 routes, accounting, and bilingual snapshot are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  for (const marker of ["R0.74T Step 19", "persistent outer lobe", "K-clock", "等待同一发布任务中的下一份明确冻结包"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.74T Step 19 的文献与主张边界", "PROVED", "FINITE", "OPEN", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.equal(version.version, "1.98");
  assert.equal(version.publicHtmlNoteCount, 222);
  assert.equal(version.publicPdfNoteCount, 179);
  assert.equal(version.postR060PublishedNodeCount, 162);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedStep, 19);
  assert.equal(manifest.latestReleaseGate, "tests/r074t-step19-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r074t-step19-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r074t-step19-pdf.mjs");
  assert.equal(manifest.latestReleaseStepTranslationScript, "scripts/add-r074t-step19-translations.mjs");
  assert.equal(manifest.latestReleaseBrowserQaScript, "scripts/qa-r074t-step19-browser.mjs");
  assert.equal(manifest.latestReleaseOnlineVerifierScript, "scripts/verify-r074t-step19-online.mjs");
  assert.deepEqual(manifest.latestPublicationIdentity, {
    releaseId: "r074t-step19",
    handoffCommit: "cbe52bd5df2dfdb948b0ac8bb761ccd8774004f1",
    sourceCommit: "2a3a59d4626face7b883159ee9b18500005e41d7",
    coreCommit: "b120598d36140385676bb4a9922d46abcdff0ba4",
    figureSourceCommit: "0433c129868ddf349c7b64d427747f590fa06898",
  });
  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r074t-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 129/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
