import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

test("R0.74M owns exact current-state accounting", async () => {
  const [manifest, site, inventory, version, home, index, noteFiles] = await Promise.all([
    text("research/release-manifest.json").then(JSON.parse),
    text("public/site-version.json").then(JSON.parse),
    text("research/formal-archive-inventory.json").then(JSON.parse),
    text("VERSION").then((value) => value.trim()),
    text("public/research-review.html"),
    text("public/notes/index.html"),
    readdir(resolve(root, "public/notes")),
  ]);
  const htmlCount = noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length;
  const pdfCount = noteFiles.filter((name) => /^r0-[0-9a-z]+\.pdf$/.test(name)).length;
  const routeStart = home.indexOf('<section class="route-overview"');
  const routeEnd = home.indexOf('<div class="page-shell">', routeStart);
  const route = home.slice(routeStart, routeEnd);
  const routeLinks = [...route.matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map((match) => match[1]);
  const postR060Count = routeLinks.length - routeLinks.indexOf("r0-61");

  assert.equal(version, "1.79");
  assert.equal(manifest.siteVersion, version);
  assert.equal(site.version, version);
  assert.equal(manifest.latestCompletedRelease, "r074m");
  assert.equal(site.latestRelease, "R0.74M");
  assert.equal(manifest.nextRelease, "r074n");
  assert.equal(manifest.publicHtmlNoteCount, htmlCount);
  assert.equal(site.publicHtmlNoteCount, htmlCount);
  assert.equal(htmlCount, 215);
  assert.equal(manifest.publicPdfNoteCount, pdfCount);
  assert.equal(site.publicPdfNoteCount, pdfCount);
  assert.equal(pdfCount, 172);
  assert.equal(manifest.postR060PublishedNodeCount, postR060Count);
  assert.equal(site.postR060PublishedNodeCount, postR060Count);
  assert.equal(postR060Count, 155);
  assert.equal(manifest.postR060RecapNodeCount, 140);
  assert.equal(site.postR060RecapNodeCount, 140);
  assert.equal(manifest.latestRecapRelease, "r073x");
  assert.equal(site.latestRecapRelease, "R0.73X");
  assert.equal(inventory.latestPublishedRelease, "r074m");
  assert.equal(inventory.publishedReleaseCount, 117);
  assert.equal(inventory.formalSealedReleaseCount, 93);
  assert.equal(manifest.postR070APublishedReleaseCount, 117);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 93);
  assert.ok(inventory.publishedReleases.includes("r074m"));
  assert.ok(inventory.formalSealedReleases.includes("r074m"));

  for (const marker of [
    "LATEST RELEASE · R0.74M · 2026-09-02", "215 篇研究笔记总索引",
    "R0.70A–R0.74M · 117 节已公开", "93 节完整封存", "当前端点 R0.74M",
    "<strong>R0.74M</strong>最新研究节点", "展开 125 篇公开笔记",
  ]) assert.ok(home.includes(marker), marker);
  assert.equal((index.match(/class="note-entry"/g) ?? []).length, htmlCount);
  assert.ok(index.includes('data-note="r0-74m"'));
  assert.ok(index.includes('href="/notes/r0-74m.pdf"'));
});

test("complete Chinese note preserves the M theorem, qualifiers, and evidence links", async () => {
  const note = await text("public/notes/r0-74m.html");
  for (const marker of [
    "完整中文版本", "PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY",
    "\\sup_{\\tau\\in I_{R_j}}[\\mathcal J_{j,j-1}(\\tau)]_+\\le C\\Gamma_jL_jR_j^5",
    "\\Sigma_L=\\frac1{32768}e^{-L^2/640}",
    "\\frac{\\Sigma_L}{LR}=\\frac{e^{L^2/640}}{32768L}\\longrightarrow\\infty",
    "\\frac1{16}-\\frac1{320}-\\frac2{1323}=\\frac{24497}{423360}>0",
    "|F_j^++F_j^-|^2\\le2(|F_j^+|^2+|F_j^-|^2)",
    "38/38", "49/49", "23 项校验和", "其余壳层行的合成", "不假设正负包抵消",
  ]) assert.ok(note.includes(marker), marker);
  for (const path of [
    "r074m_problem_freeze.md", "r074m_final_segment_expulsion.md",
    "r074m_nearest_inward_independent_audit.md", "r074m_final_source_rebind_audit.md",
    "r074m_nearest_inward_certificate.py", "r074m_nearest_inward_certificate_independent.rb",
    "r074m_nearest_inward_certificate.json", "r074m_nearest_inward_certificate_report.md",
    "r074m_certificate_independent_audit.md", "r074m_primary_literature_boundary.md",
    "r074m_gap_matrix.md", "r074m_bilingual_dictionary.md", "r074m_report-source.md",
    "r074m_reader_source_independent_audit.md", "r074m_figure_independent_audit.md",
    "r074m_freeze_manifest.json", "source-data.csv", "caption.md", "qa-report.md",
    "plot.py", "validate.py", "validation.json", "manifest.json", "SHA256SUMS",
  ]) assert.ok(note.includes(path), path);
  assert.ok(note.includes('srcset="/assets/r074m/fig-r074m-nearest-inward-expulsion.svg"'));
  assert.ok(note.includes('src="/assets/r074m/fig-r074m-nearest-inward-expulsion.png"'));
  for (const forbidden of ["世界首个", "首次证明", "解决千禧年问题", "接近解决"])
    assert.ok(!note.includes(forbidden), forbidden);
});

test("public M figure mirrors and masters are exact frozen copies", async () => {
  const source = "research/figures/r074m/fig-r074m-nearest-inward-expulsion";
  const mirror = "public/figures/r074m/fig-r074m-nearest-inward-expulsion";
  const names = await readdir(resolve(root, source));
  assert.equal(names.length, 24);
  for (const name of names)
    assert.deepEqual(await read(`${mirror}/${name}`), await read(`${source}/${name}`), name);
  for (const extension of ["svg", "pdf", "png"])
    assert.deepEqual(
      await read(`public/assets/r074m/fig-r074m-nearest-inward-expulsion.${extension}`),
      await read(`${source}/figure.${extension}`), extension,
    );
});

test("homepage and literature expose one concise M release boundary", async () => {
  const [home, literature] = await Promise.all([
    text("public/research-review.html"), text("public/literature-review.html"),
  ]);
  assert.equal((home.match(/data-release="r074m"/g) ?? []).length, 1);
  const start = home.indexOf('<div class="task-one" id="r074m"');
  const end = home.indexOf('<div class="task-one"', start + 1);
  const card = home.slice(start, end);
  assert.ok(start >= 0 && end > start);
  assert.ok(card.length < 900, "homepage R0.74M card must remain concise");
  assert.ok(card.includes("最后一小段布朗路径"));
  assert.ok(card.includes("最近内领圈完整行已闭合"));
  assert.ok(literature.includes('id="r074m-boundary"'));
  assert.ok(literature.includes("有界七篇一手文献检索"));
  assert.ok(literature.includes("开放接口 · R0.74N"));
});

test("R0.74M PDF is cryptographically bound to Chinese HTML", async () => {
  await access(resolve(root, "public/notes/r0-74m.pdf"));
  const binding = JSON.parse(await text("research/r074m_pdf_bindings.json"));
  const html = await read("public/notes/r0-74m.html");
  const pdf = await read("public/notes/r0-74m.pdf");
  assert.equal(binding.release, "R0.74M");
  assert.equal(binding.publicChineseNote.sha256, sha256(html));
  assert.equal(binding.publicPdf.sha256, sha256(pdf));
  assert.ok(binding.publicPdf.pageCount >= 2 && binding.publicPdf.pageCount <= 4);
  assert.equal(binding.publicPdf.title, "R0.74M｜最后一小段布朗路径，排出了最近内领圈");
  assert.deepEqual(binding.claimBoundary.evidenceClassesSeparated, ["PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY"]);
});

test("R0.73X recap remains byte-preserved and no R0.74M recap exists", async () => {
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.html")), "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776");
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.pdf")), "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa");
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74m.html")));
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74m.pdf")));
});
