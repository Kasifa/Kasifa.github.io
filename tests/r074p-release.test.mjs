import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync, statSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFileSync(resolve(root, path), "utf8");
const sha = (path) => createHash("sha256").update(readFileSync(resolve(root, path))).digest("hex");

test("R0.74P publication accounting advances without recap drift", () => {
  const site = JSON.parse(read("public/site-version.json"));
  assert.deepEqual(site, { schemaVersion: "research-site-version-v1", version: "1.82", latestRelease: "R0.74P", publicHtmlNoteCount: 218, postR060PublishedNodeCount: 158, postR060RecapNodeCount: 157, latestRecapRelease: "R0.74O", publicPdfNoteCount: 175, publishedDate: "2026-09-02" });
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r074p");
  assert.equal(manifest.nextRelease, "r074q");
  assert.equal(manifest.postR070APublishedReleaseCount, 120);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 96);
  assert.equal(manifest.postR060RecapNodeCount, 157);
  assert.equal(manifest.latestRecapRelease, "r074o");
  assert.equal(sha("public/recap-r0-61-r0-74o.html"), "d06c9edb093664c9835feb814a11ecd180305780b3efcdcd560908f754fba4b2");
  assert.equal(sha("public/recap-r0-61-r0-74o.pdf"), "80264dab72ca12569252a360d9b70388ba0c4b107132012b98d73b76d634d076");
});

test("R0.74P reader is complete Chinese and preserves every claim boundary", () => {
  const note = read("public/notes/r0-74p.html");
  for (const marker of [
    "哪些时间可观测量真正看见了缺失的尺度", "T_*:=", "K_*:=", "mathcal C_{\\sigma,R}",
    "K_{k,R}=Q_{k,R}+F_{k,R}", "Y_{1,R}^{\\rm clk}", "cT_*\\le v_{j,R}\\le CT_*",
    "640}{43", "Y_{2,R}^{\\rm sf}[u,p]", "stackrel{?}{\\le}",
    "PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY",
    "完整中文版本", "LOCAL DIRECT / NO DGX",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(note.length > 15000, `reader unexpectedly short: ${note.length}`);
  assert.ok(Buffer.byteLength(note, "utf8") > 20000, "reader UTF-8 payload is unexpectedly short");
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
  for (const path of ["public/notes/r0-74p.pdf", "research/r074p_note_pdf_render.json", "research/r074p_pdf_bindings.json"]) assert.ok(statSync(resolve(root, path)).size > 0, path);
  const binding = JSON.parse(read("research/r074p_pdf_bindings.json"));
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74p.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74p.pdf"));
  assert.equal(binding.claimBoundary.completeMatchedSquareFunctionUpperBound, "OPEN");
});

test("R0.74P public mirrors, short homepage card, and literature boundary are synchronized", () => {
  for (const ext of ["svg", "pdf", "png"]) {
    assert.equal(sha(`public/assets/r074p/fig-r074p-observable-triage.${ext}`), sha(`research/figures/r074p/fig-r074p-observable-triage/figure.${ext}`));
  }
  for (const name of ["figure.svg", "figure.pdf", "figure.png", "source-data.csv", "validation.json", "caption.md"]) {
    assert.equal(sha(`public/figures/r074p/fig-r074p-observable-triage/${name}`), sha(`research/figures/r074p/fig-r074p-observable-triage/${name}`));
  }
  const home = read("public/research-review.html");
  assert.match(home, /LATEST RELEASE · R0\.74P/);
  assert.match(home, /R0\.70A–R0\.74P · 120 节已公开/);
  const card = home.match(/<div class="task-one" id="r074p"[\s\S]*?<\/div>/)?.[0] ?? "";
  assert.ok(card.length > 0 && card.length < 900, `homepage card length ${card.length}`);
  assert.ok(card.includes("完整匹配平方函数上界仍开放"));
  const literature = read("public/literature-review.html");
  assert.match(literature, /id="r074p-boundary"/);
  assert.match(literature, /有限未命中不证明新颖性、优先权、检索完备性或可发表性/);
  assert.match(literature, /开放接口 · R0\.74Q/);
});
