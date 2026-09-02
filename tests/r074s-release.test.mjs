import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, statSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const readBytes = (path) => readFileSync(resolve(root, path));
const read = (path) => readBytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(readBytes(path)).digest("hex");
const node = process.env.CODEX_NODE || process.execPath;

test("R0.74S publication accounting advances without recap drift", () => {
  assert.deepEqual(JSON.parse(read("public/site-version.json")), { schemaVersion: "research-site-version-v1", version: "1.85", latestRelease: "R0.74S", publicHtmlNoteCount: 221, postR060PublishedNodeCount: 161, postR060RecapNodeCount: 157, latestRecapRelease: "R0.74O", publicPdfNoteCount: 178, publishedDate: "2026-09-02" });
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r074s");
  assert.equal(manifest.nextRelease, "r074t");
  assert.equal(manifest.postR070APublishedReleaseCount, 123);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 98);
  assert.equal(manifest.formalFigureExemptReleaseCount, 1);
  assert.equal(manifest.latestRecapRelease, "r074o");
  assert.equal(manifest.latestReleaseGate, "tests/r074s-ball-clock-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r074s-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r074s-pdf.mjs");
  assert.equal(manifest.latestReleaseTranslationScript, "scripts/add-r074s-translations.mjs");
  assert.equal(sha("public/recap-r0-61-r0-74o.html"), "d06c9edb093664c9835feb814a11ecd180305780b3efcdcd560908f754fba4b2");
  assert.equal(sha("public/recap-r0-61-r0-74o.pdf"), "80264dab72ca12569252a360d9b70388ba0c4b107132012b98d73b76d634d076");
});

test("R0.74S reader is complete Chinese and preserves every claim boundary", () => {
  const note = read("public/notes/r0-74s.html");
  for (const marker of [
    "一侧 ball cutoff：PROVED", "三条 stopped orientation：PROVED", "terminal Abel identity：PROVED",
    "PROVED ABSTRACT NO-GO", "NOT PDE/NSE", "cross-channel sign：OPEN", "完整中文版本",
    "5/5", "7/7", "55/55", "4/4", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 18000, "reader UTF-8 payload is unexpectedly short");
  assert.ok(!note.includes("独立数学审计尚未完成"));
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
  for (const path of ["public/notes/r0-74s.pdf", "research/r074s_note_pdf_render.json", "research/r074s_pdf_bindings.json"]) assert.ok(statSync(resolve(root, path)).size > 0, path);
  const binding = JSON.parse(read("research/r074s_pdf_bindings.json"));
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74s.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74s.pdf"));
  assert.equal(binding.publicPdf.pageCount, 7);
  assert.equal(binding.claimBoundary.oneSidedBallClocks, "PROVED");
  assert.equal(binding.claimBoundary.stoppedOrientations, "PROVED");
  assert.equal(binding.claimBoundary.terminalAbelIdentity, "PROVED");
  assert.equal(binding.claimBoundary.scalarPositiveClockObstruction, "PROVED_ABSTRACT_NO_GO");
  assert.equal(binding.claimBoundary.pdeOrNseCounterexample, false);
  assert.equal(binding.claimBoundary.crossChannelDynamicalSign, "OPEN");
  assert.equal(binding.claimBoundary.fixedScaleInequality, "OPEN");
  assert.equal(binding.claimBoundary.formalFigure, "PUBLISHED_DERIVED_FROM_FROZEN_ANALYTIC_SOURCE");
});

test("R0.74S public mirrors, concise homepage card, and literature boundary are synchronized", () => {
  const home = read("public/research-review.html");
  assert.match(home, /LATEST RELEASE · R0\.74S/);
  assert.match(home, /R0\.70A–R0\.74S · 123 节已公开/);
  assert.match(home, /98 节完整封存/);
  assert.equal((home.match(/id="r074s" data-release="r074s"/g) ?? []).length, 1);
  const card = home.match(/<div class="task-one" id="r074s"[\s\S]*?<\/div>/)?.[0] ?? "";
  assert.ok(card.length > 0 && card.length < 500, `homepage card length ${card.length}`);
  for (const marker of ["ℓ¹", "不是 PDE/NSE 反例", "NOT CLAY"]) assert.ok(card.includes(marker), marker);
  const literature = read("public/literature-review.html");
  assert.equal((literature.match(/id="r074s-boundary"/g) ?? []).length, 1);
  for (const marker of ["仅排除 scalar positivity", "见证不是速度、压力、耗散测度或 NSE 解", "跨通道动力学符号", "NOT PDE/NSE. NOT CLAY."]) assert.ok(literature.includes(marker), marker);

  for (const ext of ["svg", "pdf", "png"]) {
    const canonical = `research/figures/r074s/fig-r074s-ball-clock-debt/figure.${ext}`;
    assert.ok(existsSync(resolve(root, canonical)), canonical);
    assert.equal(sha(`public/assets/r074s/fig-r074s-ball-clock-debt.${ext}`), sha(canonical));
    assert.equal(sha(`public/figures/r074s/fig-r074s-ball-clock-debt/figure.${ext}`), sha(canonical));
    assert.equal(sha(`figures/r074s/fig-r074s-ball-clock-debt/figure.${ext}`), sha(canonical));
  }
  const validation = JSON.parse(read("research/figures/r074s/fig-r074s-ball-clock-debt/validation.json"));
  assert.equal(validation.summary.result, "PASS");
  assert.equal(validation.summary.passed, 14);
  assert.equal(validation.summary.total, 14);
});

test("R0.74S translations and formal archive inventory are complete", () => {
  const translation = execFileSync(node, [resolve(root, "scripts/add-r074s-translations.mjs"), "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translation, /"checked": 122/);
  assert.match(translation, /"applied": false/);
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.latestPublishedRelease, "r074s");
  assert.ok(inventory.publishedReleases.includes("r074s"));
  assert.ok(inventory.formalSealedReleases.includes("r074s"));
  assert.ok(!inventory.formalFigureExemptReleases.includes("r074s"));
  assert.equal(inventory.publishedReleaseCount, 123);
  assert.equal(inventory.formalSealedReleaseCount, 98);
  assert.equal(inventory.formalFigureExemptReleaseCount, 1);
});
