import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, readFileSync, statSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFileSync(resolve(root, path), "utf8");
const sha = (path) => createHash("sha256").update(readFileSync(resolve(root, path))).digest("hex");

test("R0.74Q publication accounting advances without recap drift", () => {
  assert.deepEqual(JSON.parse(read("public/site-version.json")), { schemaVersion: "research-site-version-v1", version: "1.83", latestRelease: "R0.74Q", publicHtmlNoteCount: 219, postR060PublishedNodeCount: 159, postR060RecapNodeCount: 157, latestRecapRelease: "R0.74O", publicPdfNoteCount: 176, publishedDate: "2026-09-02" });
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r074q");
  assert.equal(manifest.nextRelease, "r074r");
  assert.equal(manifest.postR070APublishedReleaseCount, 121);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 96);
  assert.equal(manifest.formalFigureExemptReleaseCount, 1);
  assert.equal(manifest.latestRecapRelease, "r074o");
  assert.equal(sha("public/recap-r0-61-r0-74o.html"), "d06c9edb093664c9835feb814a11ecd180305780b3efcdcd560908f754fba4b2");
  assert.equal(sha("public/recap-r0-61-r0-74o.pdf"), "80264dab72ca12569252a360d9b70388ba0c4b107132012b98d73b76d634d076");
});

test("R0.74Q reader is complete Chinese and preserves every claim boundary", () => {
  const note = read("public/notes/r0-74q.html");
  for (const marker of [
    "许多壳层同时亮起", "mathcal S_N", "N_{\\rm eff}", "partial_3^2", "R^{-1}e^{-a_SL_1^2}",
    "L_N=\\frac{16}{63}L^2", "delta_\\times", "Y_{2,R}^{\\rm sf}", "P_R^{M,(N)}", "5120}{47258883",
    "PROVED", "INHERITED", "FINITE", "CONDITIONAL", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY",
    "完整中文版本", "正式图件：NOT APPLICABLE", "无仿真 / NO DGX",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(note.length > 23000, `reader unexpectedly short: ${note.length}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 33000, "reader UTF-8 payload is unexpectedly short");
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
  for (const path of ["public/notes/r0-74q.pdf", "research/r074q_note_pdf_render.json", "research/r074q_pdf_bindings.json"]) assert.ok(statSync(resolve(root, path)).size > 0, path);
  const binding = JSON.parse(read("research/r074q_pdf_bindings.json"));
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74q.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74q.pdf"));
  assert.equal(binding.publicPdf.pageCount, 14);
  assert.equal(binding.claimBoundary.completeMatchedSquareFunctionUpperBound, "OPEN");
  assert.equal(binding.claimBoundary.formalFigure, "NOT_APPLICABLE");
});

test("R0.74Q public mirrors, short homepage card, and literature boundary are synchronized", () => {
  for (const path of ["public/assets/r074q", "public/figures/r074q", "research/figures/r074q", "figures/r074q"]) assert.equal(existsSync(resolve(root, path)), false, path);
  const home = read("public/research-review.html");
  assert.match(home, /LATEST RELEASE · R0\.74Q/);
  assert.match(home, /R0\.70A–R0\.74Q · 121 节已公开/);
  assert.match(home, /96 节完整封存/);
  const card = home.match(/<div class="task-one" id="r074q"[\s\S]*?<\/div>/)?.[0] ?? "";
  assert.ok(card.length > 0 && card.length < 900, `homepage card length ${card.length}`);
  assert.ok(card.includes("真实三次支付阻断"));
  assert.doesNotMatch(card, /assets\/r074q|figures\/r074q/);
  const literature = read("public/literature-review.html");
  assert.match(literature, /id="r074q-boundary"/);
  assert.match(literature, /2D3C 和共同线性标量方程的叠加机制是既有结构/);
  assert.match(literature, /有限未命中也不证明新颖性、优先权或可发表性/);
  assert.match(literature, /开放接口 · R0\.74R/);
});
