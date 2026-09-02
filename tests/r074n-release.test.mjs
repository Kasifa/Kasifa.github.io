import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

test("R0.74N owns exact current-state accounting", async () => {
  const [manifest, site, inventory, version, home, index, noteFiles] = await Promise.all([
    text("research/release-manifest.json").then(JSON.parse),
    text("public/site-version.json").then(JSON.parse),
    text("research/formal-archive-inventory.json").then(JSON.parse),
    text("VERSION").then((value) => value.trim()),
    text("public/research-review.html"), text("public/notes/index.html"),
    readdir(resolve(root, "public/notes")),
  ]);
  const htmlCount = noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length;
  const pdfCount = noteFiles.filter((name) => /^r0-[0-9a-z]+\.pdf$/.test(name)).length;
  const routeStart = home.indexOf('<section class="route-overview"');
  const routeEnd = home.indexOf('<div class="page-shell">', routeStart);
  const routeLinks = [...home.slice(routeStart, routeEnd).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map((match) => match[1]);
  const postR060Count = routeLinks.length - routeLinks.indexOf("r0-61");

  assert.equal(version, "1.80");
  assert.equal(manifest.siteVersion, version); assert.equal(site.version, version);
  assert.equal(manifest.latestCompletedRelease, "r074n"); assert.equal(site.latestRelease, "R0.74N");
  assert.equal(manifest.nextRelease, "r074o");
  assert.equal(manifest.publicHtmlNoteCount, htmlCount); assert.equal(site.publicHtmlNoteCount, htmlCount); assert.equal(htmlCount, 216);
  assert.equal(manifest.publicPdfNoteCount, pdfCount); assert.equal(site.publicPdfNoteCount, pdfCount); assert.equal(pdfCount, 173);
  assert.equal(manifest.postR060PublishedNodeCount, postR060Count); assert.equal(site.postR060PublishedNodeCount, postR060Count); assert.equal(postR060Count, 156);
  assert.equal(manifest.postR060RecapNodeCount, 140); assert.equal(site.postR060RecapNodeCount, 140);
  assert.equal(manifest.latestRecapRelease, "r073x"); assert.equal(site.latestRecapRelease, "R0.73X");
  assert.equal(inventory.latestPublishedRelease, "r074n"); assert.equal(inventory.publishedReleaseCount, 118); assert.equal(inventory.formalSealedReleaseCount, 94);
  assert.equal(manifest.postR070APublishedReleaseCount, 118); assert.equal(manifest.postR070AFormalSealedReleaseCount, 94);
  assert.ok(inventory.publishedReleases.includes("r074n")); assert.ok(inventory.formalSealedReleases.includes("r074n"));
  for (const marker of ["LATEST RELEASE · R0.74N · 2026-09-02", "216 篇研究笔记总索引", "R0.70A–R0.74N · 118 节已公开", "94 节完整封存", "当前端点 R0.74N", "<strong>R0.74N</strong>最新研究节点", "展开 126 篇公开笔记"]) assert.ok(home.includes(marker), marker);
  assert.equal((index.match(/class="note-entry"/g) ?? []).length, htmlCount);
  assert.ok(index.includes('data-note="r0-74n"')); assert.ok(index.includes('href="/notes/r0-74n.pdf"'));
});

test("complete Chinese note preserves the theorem and corrected family boundary", async () => {
  const note = await text("public/notes/r0-74n.html");
  for (const marker of [
    "完整中文版本", "PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY",
    "\\sup_{\\tau\\in I_{R_j}}[\\mathcal I_j(\\tau)]_+\\le C\\Gamma_jL_jR_j^5",
    "\\mathcal I_j=\\mathcal I_<+\\mathcal I_=+\\mathcal I_>",
    "0\\le D_<\\le C\\sum_{k\\ge1}2^ke^{-4^{k-1}/32}=:C_*&lt;\\infty",
    "\\frac1{16}-\\frac1{320}-\\frac8{3969}=\\frac{72851}{1270080}>0",
    "3c_\\gamma-\\rho=\\frac{1237}{423360}>0",
    "X_j\\asymp\\mathfrak C_j\\asymp B_j^2L_jR_j^2\\asymp P_j^{2/3}\\sqrt{1+\\log_+P_j}",
    "0\\le\\mathcal D_{{\\rm ext},j}\\le CT_j", "没有已证明的匹配下界",
    "84/84", "67/67", "25 行校验和", "任意流上的全壳层", "没有假设壳层或正负包之间发生抵消",
  ]) assert.ok(note.includes(marker), marker);
  for (const path of [
    "r074n_problem_freeze.md", "r074n_all_shell_synthesis.md", "r074n_all_shell_independent_audit.md", "r074n_crossnote_implication_independent_audit.md", "r074n_final_source_rebind_audit.md", "r074n_all_shell_certificate.py", "r074n_all_shell_certificate_independent.rb", "r074n_all_shell_certificate.json", "r074n_all_shell_certificate_report.md", "r074n_certificate_independent_audit.md", "r074n_certificate_adversarial_audit.md", "r074n_primary_literature_boundary.md", "r074n_primary_literature_independent_audit.md", "r074n_gap_matrix.md", "r074n_bilingual_dictionary.md", "r074n_report-source.md", "r074n_reader_source_independent_audit.md", "r074n_figure_independent_audit.md", "r074n_freeze_manifest.json", "source-data.csv", "caption.md", "chart-contract-and-source-data.md", "qa-report.md", "plot.py", "validate.py", "validation.json", "manifest.json", "SHA256SUMS",
  ]) assert.ok(note.includes(path), path);
  assert.ok(note.includes('srcset="/assets/r074n/fig-r074n-all-shell-synthesis.svg"'));
  assert.ok(note.includes('src="/assets/r074n/fig-r074n-all-shell-synthesis.png"'));
  for (const forbidden of ["世界首个", "首次证明", "解决千禧年问题", "接近解决"]) assert.ok(!note.includes(forbidden), forbidden);
});

test("public N figure mirrors and masters are exact frozen copies", async () => {
  const source = "research/figures/r074n/fig-r074n-all-shell-synthesis";
  const mirror = "public/figures/r074n/fig-r074n-all-shell-synthesis";
  const names = await readdir(resolve(root, source)); assert.equal(names.length, 26);
  for (const name of names) assert.deepEqual(await read(`${mirror}/${name}`), await read(`${source}/${name}`), name);
  for (const extension of ["svg", "pdf", "png"]) assert.deepEqual(await read(`public/assets/r074n/fig-r074n-all-shell-synthesis.${extension}`), await read(`${source}/figure.${extension}`), extension);
});

test("homepage and literature expose one concise N release boundary", async () => {
  const [home, literature] = await Promise.all([text("public/research-review.html"), text("public/literature-review.html")]);
  assert.equal((home.match(/data-release="r074n"/g) ?? []).length, 1);
  const start = home.indexOf('<div class="task-one" id="r074n"');
  const end = home.indexOf('<div class="task-one"', start + 1);
  const card = home.slice(start, end);
  assert.ok(start >= 0 && end > start); assert.ok(card.length < 900, "homepage R0.74N card must remain concise");
  assert.ok(card.includes("把所有壳层合起来")); assert.ok(card.includes("耗散下界和任意流端点仍开放"));
  assert.ok(literature.includes('id="r074n-boundary"')); assert.ok(literature.includes("有界八篇一手文献检索")); assert.ok(literature.includes("开放接口 · R0.74O"));
});

test("R0.74N PDF is cryptographically bound to Chinese HTML", async () => {
  await access(resolve(root, "public/notes/r0-74n.pdf"));
  const binding = JSON.parse(await text("research/r074n_pdf_bindings.json"));
  const html = await read("public/notes/r0-74n.html"); const pdf = await read("public/notes/r0-74n.pdf");
  assert.equal(binding.release, "R0.74N"); assert.equal(binding.publicChineseNote.sha256, sha256(html)); assert.equal(binding.publicPdf.sha256, sha256(pdf));
  assert.ok(binding.publicPdf.pageCount >= 2 && binding.publicPdf.pageCount <= 5);
  assert.equal(binding.publicPdf.title, "R0.74N｜把所有壳层合起来，完整领圈条件闭合了");
  assert.deepEqual(binding.claimBoundary.evidenceClassesSeparated, ["PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY"]);
  assert.equal(binding.claimBoundary.matchingExactFamilyEndpointLaw, true); assert.equal(binding.claimBoundary.exteriorDissipationMatchingLowerBound, false); assert.equal(binding.claimBoundary.universalEndpointEstimate, false);
});

test("R0.73X recap remains byte-preserved and no R0.74N recap exists", async () => {
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.html")), "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776");
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.pdf")), "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa");
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74n.html"))); await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74n.pdf")));
});
