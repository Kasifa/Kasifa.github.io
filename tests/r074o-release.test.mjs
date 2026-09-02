import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

test("R0.74O owns exact current-state and milestone accounting", async () => {
  const [manifest, site, inventory, version, home, index, noteFiles] = await Promise.all([
    text("research/release-manifest.json").then(JSON.parse),
    text("public/site-version.json").then(JSON.parse),
    text("research/formal-archive-inventory.json").then(JSON.parse),
    text("VERSION").then((value) => value.trim()),
    text("public/research-review.html"), text("public/notes/index.html"),
    readdir(resolve(root, "public/notes")),
  ]);
  const htmlCount = noteFiles.filter((name) => /^r0-[0-9a-z-]+\.html$/.test(name)).length;
  const pdfCount = noteFiles.filter((name) => /^r0-[0-9a-z-]+\.pdf$/.test(name)).length;
  const routeStart = home.indexOf('<section class="route-overview"');
  const routeEnd = home.indexOf('<div class="page-shell">', routeStart);
  const routeLinks = [...home.slice(routeStart, routeEnd).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map((match) => match[1]);
  const orderedUnique = [...new Set(routeLinks)];
  const postR060Count = orderedUnique.slice(orderedUnique.indexOf("r0-61")).length;

  assert.equal(version, "1.81");
  assert.equal(manifest.siteVersion, version); assert.equal(site.version, version);
  assert.equal(manifest.latestCompletedRelease, "r074o"); assert.equal(site.latestRelease, "R0.74O");
  assert.equal(manifest.nextRelease, "r074p");
  assert.equal(manifest.publicHtmlNoteCount, htmlCount); assert.equal(site.publicHtmlNoteCount, htmlCount); assert.equal(htmlCount, 217);
  assert.equal(manifest.publicPdfNoteCount, pdfCount); assert.equal(site.publicPdfNoteCount, pdfCount); assert.equal(pdfCount, 174);
  assert.equal(manifest.postR060PublishedNodeCount, postR060Count); assert.equal(site.postR060PublishedNodeCount, postR060Count); assert.equal(postR060Count, 157);
  assert.equal(manifest.postR060RecapNodeCount, 157); assert.equal(site.postR060RecapNodeCount, 157);
  assert.equal(manifest.latestRecapRelease, "r074o"); assert.equal(site.latestRecapRelease, "R0.74O");
  assert.equal(inventory.latestPublishedRelease, "r074o"); assert.equal(inventory.publishedReleaseCount, 119); assert.equal(inventory.formalSealedReleaseCount, 95);
  assert.equal(manifest.postR070APublishedReleaseCount, 119); assert.equal(manifest.postR070AFormalSealedReleaseCount, 95);
  assert.ok(inventory.publishedReleases.includes("r074o")); assert.ok(inventory.formalSealedReleases.includes("r074o"));
  for (const marker of ["LATEST RELEASE · R0.74O · 2026-09-02", "217 篇研究笔记总索引", "R0.70A–R0.74O · 119 节已公开", "95 节完整封存", "当前端点 R0.74O", "<strong>R0.74O</strong>最新研究节点", "展开 127 篇公开笔记", "/recap-r0-61-r0-74o.html"]) assert.ok(home.includes(marker), marker);
  assert.equal((index.match(/class="note-entry"/g) ?? []).length, htmlCount);
  assert.ok(index.includes('data-note="r0-74o"')); assert.ok(index.includes('href="/notes/r0-74o.pdf"'));
});

test("complete Chinese note preserves the exact no-go quantifiers and evidence classes", async () => {
  const note = await text("public/notes/r0-74o.html");
  for (const marker of [
    "完整中文版本", "PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY",
    "m=\\rho-\\tfrac32c_\\gamma=43/423360>0", "\\varkappa_j=L_j^{2/3}",
    "P_{R_j}^{M,*}=P_{R_j}^{F,*}\\asymp B_j^3R_j^3",
    "X_{R_j}^{\\alpha,*}\\asymp\\mathfrak C_{R_j}^{\\alpha,*}",
    "\\delta_*=86/11907", "q_*=8024/11907", "(1+\\log_+P_{R_j}^{\\alpha,*})^{7/6}",
    "\\Phi(p)=o\\!\\left(p^{8024/11907}(1+\\log_+p)^{7/6}\\right)",
    "先固定任意 \\(\\gamma\\in\\mathbb R\\)", "可依赖于 \\(\\gamma\\) 的精确光滑解族",
    "下界来自端点能量分量", "没有证明匹配耗散下界", "245/245", "72/72", "25 行校验和",
  ]) assert.ok(note.includes(marker), marker);
  for (const path of [
    "r074o_problem_freeze.md", "r074o_amplitude_endpoint_counterexample.md", "r074o_amplitude_endpoint_independent_audit.md", "r074o_final_source_rebind_audit.md", "r074o_amplitude_endpoint_certificate.py", "r074o_amplitude_endpoint_certificate_independent.rb", "r074o_amplitude_endpoint_certificate.json", "r074o_amplitude_endpoint_certificate_report.md", "r074o_certificate_independent_audit.md", "r074o_primary_literature_boundary.md", "r074o_primary_literature_independent_audit.md", "r074o_gap_matrix.md", "r074o_bilingual_dictionary.md", "r074o_report-source.md", "r074o_reader_source_independent_audit.md", "r074o_milestone_recap_delta.md", "r074o_milestone_recap_independent_audit.md", "r074o_figure_independent_audit.md", "r074o_freeze_manifest.json", "source-data.csv", "caption.md", "chart-contract-and-source-data.md", "qa-report.md", "plot.py", "validate.py", "validation.json", "manifest.json", "SHA256SUMS",
  ]) assert.ok(note.includes(path), path);
  assert.ok(note.includes('srcset="/assets/r074o/fig-r074o-amplitude-endpoint.svg"'));
  assert.ok(note.includes('src="/assets/r074o/fig-r074o-amplitude-endpoint.png"'));
  for (const forbidden of ["世界首个", "首次证明", "解决千禧年问题", "接近解决"] ) assert.ok(!note.includes(forbidden), forbidden);
});

test("public R0.74O figure mirror and primary assets are exact frozen copies", async () => {
  const source = "research/figures/r074o/fig-r074o-amplitude-endpoint";
  const mirror = "public/figures/r074o/fig-r074o-amplitude-endpoint";
  const names = await readdir(resolve(root, source));
  assert.equal(names.length, 26);
  for (const name of names) assert.deepEqual(await read(`${mirror}/${name}`), await read(`${source}/${name}`), name);
  for (const extension of ["svg", "pdf", "png"]) assert.deepEqual(await read(`public/assets/r074o/fig-r074o-amplitude-endpoint.${extension}`), await read(`${source}/figure.${extension}`), extension);
});

test("homepage and literature expose one concise O boundary and the new recap", async () => {
  const [home, literature] = await Promise.all([text("public/research-review.html"), text("public/literature-review.html")]);
  assert.equal((home.match(/data-release="r074o"/g) ?? []).length, 1);
  const start = home.indexOf('<div class="task-one" id="r074o"');
  const end = home.indexOf('<div class="task-one"', start + 1);
  const card = home.slice(start, end);
  assert.ok(start >= 0 && end > start); assert.ok(card.length < 900, "homepage R0.74O card must remain concise");
  assert.ok(card.includes("自由振幅否定")); assert.ok(card.includes("增广任意流端点仍开放"));
  assert.ok(literature.includes('id="r074o-boundary"')); assert.ok(literature.includes("十四篇一手来源")); assert.ok(literature.includes("开放接口 · R0.74P"));
  assert.ok(literature.includes('/recap-r0-61-r0-74o.html'));
});

test("note and milestone recap PDFs are cryptographically bound to Chinese HTML", async () => {
  for (const item of [
    { html: "public/notes/r0-74o.html", pdf: "public/notes/r0-74o.pdf", binding: "research/r074o_pdf_bindings.json", title: "R0.74O｜自由振幅否定了标量平方根对数端点", pages: 3 },
    { html: "public/recap-r0-61-r0-74o.html", pdf: "public/recap-r0-61-r0-74o.pdf", binding: "research/r074o_recap_pdf_bindings.json", title: "R0.61–R0.74O 累计回顾｜从 projected-Lamb 到标量支付 no-go", pages: 2 },
  ]) {
    await access(resolve(root, item.pdf));
    const binding = JSON.parse(await text(item.binding));
    const html = await read(item.html); const pdf = await read(item.pdf);
    assert.equal(binding.release, "R0.74O"); assert.equal(binding.publicChineseHtml.sha256, sha256(html)); assert.equal(binding.publicPdf.sha256, sha256(pdf));
    assert.equal(binding.publicPdf.pageCount, item.pages); assert.equal(binding.publicPdf.title, item.title);
    assert.deepEqual(binding.claimBoundary.evidenceClassesSeparated, ["PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY"]);
    assert.equal(binding.claimBoundary.scalarPaymentOnlySquareRootLogEndpoint, "REFUTED"); assert.equal(binding.claimBoundary.clayProblemSolved, false);
  }
});

test("new recap covers exactly R0.61 through R0.74O while the R0.73X recap remains byte-preserved", async () => {
  const recap = await text("public/recap-r0-61-r0-74o.html");
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.html")), "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776");
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.pdf")), "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa");
  const section = recap.slice(recap.indexOf('<section id="node-index">'));
  const links = [...section.matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map((match) => match[1]);
  assert.equal(links.length, 157); assert.equal(new Set(links).size, 157); assert.equal(links[0], "r0-61"); assert.equal(links.at(-1), "r0-74o");
  for (const marker of ["R0.61–R0.74O", "收录节点：157", "回顾截止时公开笔记：217", "projected-Lamb", "\\mathcal V\\in L_t^1", "2K^2", "R0.74P", "R0.74O"]) assert.ok(recap.includes(marker), marker);
  for (const forbidden of ["CONTENTS", "路线怎样一步步收缩", "当前门槛", "价值确认", "common-response", "精确账本", "交换子桥"]) assert.ok(!recap.includes(forbidden), forbidden);
});
