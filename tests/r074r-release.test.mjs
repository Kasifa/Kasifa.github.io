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

test("R0.74R publication accounting advances without recap drift", () => {
  assert.deepEqual(JSON.parse(read("public/site-version.json")), { schemaVersion: "research-site-version-v1", version: "1.84", latestRelease: "R0.74R", publicHtmlNoteCount: 220, postR060PublishedNodeCount: 160, postR060RecapNodeCount: 157, latestRecapRelease: "R0.74O", publicPdfNoteCount: 177, publishedDate: "2026-09-02" });
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r074r");
  assert.equal(manifest.nextRelease, "r074s");
  assert.equal(manifest.postR070APublishedReleaseCount, 122);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 97);
  assert.equal(manifest.formalFigureExemptReleaseCount, 1);
  assert.equal(manifest.latestRecapRelease, "r074o");
  assert.equal(manifest.latestReleaseGate, "tests/r074r-terminal-window-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r074r-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r074r-pdf.mjs");
  assert.equal(manifest.latestReleaseTranslationScript, "scripts/add-r074r-translations.mjs");
  assert.equal(sha("public/recap-r0-61-r0-74o.html"), "d06c9edb093664c9835feb814a11ecd180305780b3efcdcd560908f754fba4b2");
  assert.equal(sha("public/recap-r0-61-r0-74o.pdf"), "80264dab72ca12569252a360d9b70388ba0c4b107132012b98d73b76d634d076");
});

test("R0.74R reader is complete Chinese and preserves every claim boundary", () => {
  const note = read("public/notes/r0-74r.html");
  for (const marker of [
    "窗口 lobe packing：PROVED", "第一壳层收缩：PROVED", "任意时钟三分法：PROVED",
    "固定尺度结论：PROVED CONDITIONAL", "普适提取输入：OPEN", "no-go witness：NOT NSE",
    "完整中文版本", "9/9", "12/12", "5/5", "双语词典", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 25000, "reader UTF-8 payload is unexpectedly short");
  assert.ok(!note.includes("独立数学审计尚未完成"));
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
  for (const path of ["public/notes/r0-74r.pdf", "research/r074r_note_pdf_render.json", "research/r074r_pdf_bindings.json"]) assert.ok(statSync(resolve(root, path)).size > 0, path);
  const binding = JSON.parse(read("research/r074r_pdf_bindings.json"));
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74r.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74r.pdf"));
  assert.equal(binding.publicPdf.pageCount, 9);
  assert.equal(binding.claimBoundary.terminalWindowLobePacking, "PROVED");
  assert.equal(binding.claimBoundary.firstShellConcentration, "PROVED_IN_FROZEN_TARGET_FAMILY");
  assert.equal(binding.claimBoundary.arbitraryCompletedClockTrichotomy, "PROVED");
  assert.equal(binding.claimBoundary.arbitraryClockToFixedScaleImplication, "PROVED_CONDITIONAL_INPUT");
  assert.equal(binding.claimBoundary.universalExtractionInputs, "OPEN");
  assert.equal(binding.claimBoundary.noGoWitnesses, "PROVED_ABSTRACT_OR_FUNCTIONAL_NOT_NSE_SOLUTIONS");
  assert.equal(binding.claimBoundary.fixedScaleInequality, "OPEN");
  assert.equal(binding.claimBoundary.formalFigure, "PUBLISHED_DERIVED_FROM_FROZEN_ANALYTIC_SOURCE");
});

test("R0.74R public mirrors, short homepage card, and literature boundary are synchronized", () => {
  const home = read("public/research-review.html");
  assert.match(home, /LATEST RELEASE · R0\.74R/);
  assert.match(home, /R0\.70A–R0\.74R · 122 节已公开/);
  assert.match(home, /97 节完整封存/);
  assert.equal((home.match(/id="r074r" data-release="r074r"/g) ?? []).length, 1);
  const card = home.match(/<div class="task-one" id="r074r"[\s\S]*?<\/div>/)?.[0] ?? "";
  assert.ok(card.length > 0 && card.length < 900, `homepage card length ${card.length}`);
  assert.ok(card.includes("no-go witness 不是 NSE 解"));
  const literature = read("public/literature-review.html");
  assert.equal((literature.match(/id="r074r-boundary"/g) ?? []).length, 1);
  for (const marker of ["no-go witness 只排除抽象或纯函数捷径", "不是 Navier--Stokes 解", "不否定 Q.1", "有限未命中不证明新颖性、优先权或可发表性"]) assert.ok(literature.includes(marker), marker);

  for (const ext of ["svg", "pdf", "png"]) {
    const canonical = `research/figures/r074r/fig-r074r-clock-triage/figure.${ext}`;
    assert.ok(existsSync(resolve(root, canonical)), canonical);
    assert.equal(sha(`public/assets/r074r/fig-r074r-clock-triage.${ext}`), sha(canonical));
    assert.equal(sha(`public/figures/r074r/fig-r074r-clock-triage/figure.${ext}`), sha(canonical));
    assert.equal(sha(`figures/r074r/fig-r074r-clock-triage/figure.${ext}`), sha(canonical));
  }
  const validation = JSON.parse(read("research/figures/r074r/fig-r074r-clock-triage/validation.json"));
  assert.equal(validation.summary.result, "PASS");
  assert.equal(validation.summary.passed, 15);
  assert.equal(validation.summary.total, 15);
});

test("R0.74R translations and formal archive inventory are complete", () => {
  const translation = execFileSync(node, [resolve(root, "scripts/add-r074r-translations.mjs"), "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(translation, /"checked": 148/);
  assert.match(translation, /"applied": false/);
  const dictionary = read("research/r074r_bilingual_dictionary.md");
  for (const marker of ["NOT CLAY", "no-go", "OPEN", "not an NSE solution"]) assert.ok(dictionary.includes(marker), marker);
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.latestPublishedRelease, "r074r");
  assert.ok(inventory.publishedReleases.includes("r074r"));
  assert.ok(inventory.formalSealedReleases.includes("r074r"));
  assert.ok(!inventory.formalFigureExemptReleases.includes("r074r"));
  assert.equal(inventory.publishedReleaseCount, 122);
  assert.equal(inventory.formalSealedReleaseCount, 97);
  assert.equal(inventory.formalFigureExemptReleaseCount, 1);
});
