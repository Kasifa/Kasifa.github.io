import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

test("R0.74K owns exact current-state accounting", async () => {
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

  assert.match(version, /^\d+\.\d+$/);
  assert.equal(version, "1.77");
  assert.equal(manifest.siteVersion, version);
  assert.equal(site.version, version);
  assert.equal(manifest.latestCompletedRelease, "r074k");
  assert.equal(site.latestRelease, "R0.74K");
  assert.equal(manifest.nextRelease, "r074l");
  assert.equal(manifest.publicHtmlNoteCount, htmlCount);
  assert.equal(site.publicHtmlNoteCount, htmlCount);
  assert.equal(htmlCount, 213);
  assert.equal(manifest.publicPdfNoteCount, pdfCount);
  assert.equal(site.publicPdfNoteCount, pdfCount);
  assert.equal(pdfCount, 170);
  assert.equal(manifest.postR060PublishedNodeCount, postR060Count);
  assert.equal(site.postR060PublishedNodeCount, postR060Count);
  assert.equal(postR060Count, 153);
  assert.equal(manifest.postR060RecapNodeCount, 140);
  assert.equal(site.postR060RecapNodeCount, 140);
  assert.equal(manifest.latestRecapRelease, "r073x");
  assert.equal(site.latestRecapRelease, "R0.73X");
  assert.equal(inventory.latestPublishedRelease, "r074k");
  assert.equal(inventory.publishedReleaseCount, inventory.publishedReleases.length);
  assert.equal(inventory.formalSealedReleaseCount, inventory.formalSealedReleases.length);
  assert.equal(inventory.publishedReleaseCount, 115);
  assert.equal(inventory.formalSealedReleaseCount, 91);
  assert.equal(manifest.postR070APublishedReleaseCount, 115);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 91);
  assert.ok(inventory.publishedReleases.includes("r074k"));
  assert.ok(inventory.formalSealedReleases.includes("r074k"));

  for (const marker of [
    "LATEST RELEASE · R0.74K · 2026-09-02", "213 篇研究笔记总索引",
    "R0.70A–R0.74K · 115 节已公开", "91 节完整封存", "当前端点 R0.74K",
    "<strong>R0.74K</strong>最新研究节点", "展开 123 篇公开笔记",
  ]) assert.ok(home.includes(marker), marker);
  assert.equal((index.match(/class="note-entry"/g) ?? []).length, htmlCount);
  assert.ok(index.includes('data-note="r0-74k"'));
  assert.ok(index.includes('href="/notes/r0-74k.pdf"'));
});

test("complete Chinese note preserves the K formulas, qualifiers, and evidence links", async () => {
  const note = await text("public/notes/r0-74k.html");
  for (const marker of [
    "完整中文版本", "PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY",
    "\\lambda=63/32", "c_h=15/16", "c_\\gamma=8/3969",
    "\\frac{204385}{134120448}", "\\frac{536399}{8583708672}", "1/262144",
    "4033r_j/8064", "4033/8064+1/256", "|x_1|,|x_2|&lt;r_j/64",
    "I_{2R_j}\\cap(-\\infty,\\tau]",
    "\\Gamma_jL_jR_j^5", "[\\mathcal I_j(\\tau)]_+", "\\mathfrak C_j\\lesssim B_j^2L_jR_j^2",
    "P_j^{2/3}\\sqrt{1+\\log_+P_j}", "自由热包替换无法关闭", "不是对目标可观测量上界的反例",
    "41/41", "25 文件", "这个随机路径估计尚未证明", "匹配上界仍为 OPEN",
  ]) assert.ok(note.includes(marker), marker);
  for (const path of [
    "r074k_single_collar_shear_lag_reduction.md", "r074k_inward_tail_independent_audit.md",
    "r074k_collar_reduction_independent_audit.md", "r074k_figure_independent_audit.md",
    "r074k_final_source_rebind_audit.md", "r074k_report-source.md",
    "r074k_single_collar_exponent_certificate_report.md", "r074k_single_collar_exponent_certificate.json",
    "r074k_single_collar_exponent_certificate.py", "r074k_single_collar_exponent_certificate_independent.rb",
    "r074k_certificate_independent_audit.md", "r074k_primary_literature_boundary.md",
    "r074k_primary_literature_independent_audit.md", "r074k_gap_matrix.md",
    "r074k_bilingual_dictionary.md", "r074k_freeze_manifest.json", "source-data.csv",
    "caption.md", "qa-report.md", "plot.py", "validate.py", "manifest.json", "validation.json",
  ]) assert.ok(note.includes(path), path);
  assert.ok(note.includes('srcset="/assets/r074k/fig-r074k-single-inward-collar.svg"'));
  assert.ok(note.includes('src="/assets/r074k/fig-r074k-single-inward-collar.png"'));
  for (const forbidden of ["世界首个", "首次证明", "解决千禧年问题", "接近解决"])
    assert.ok(!note.includes(forbidden), forbidden);
});

test("public K figure mirrors and masters are exact frozen copies", async () => {
  const source = "research/figures/r074k/fig-r074k-single-inward-collar";
  const mirror = "public/figures/r074k/fig-r074k-single-inward-collar";
  const names = await readdir(resolve(root, source));
  assert.equal(names.length, 25);
  for (const name of names)
    assert.deepEqual(await read(`${mirror}/${name}`), await read(`${source}/${name}`), name);
  for (const extension of ["svg", "pdf", "png"])
    assert.deepEqual(
      await read(`public/assets/r074k/fig-r074k-single-inward-collar.${extension}`),
      await read(`${source}/figure.${extension}`), extension,
    );
});

test("homepage and literature expose one concise K release boundary", async () => {
  const [home, literature] = await Promise.all([
    text("public/research-review.html"), text("public/literature-review.html"),
  ]);
  assert.equal((home.match(/data-release="r074k"/g) ?? []).length, 1);
  const start = home.indexOf('<div class="task-one" id="r074k"');
  const end = home.indexOf('<div class="task-one"', start + 1);
  const card = home.slice(start, end);
  assert.ok(start >= 0 && end > start);
  assert.ok(card.length < 1600, "homepage R0.74K card must remain concise");
  assert.ok(card.includes("自由热指数为何只卡在最近内领圈"));
  assert.ok(card.includes("不构成千禧年问题结论"));
  assert.ok(literature.includes('id="r074k-boundary"'));
  assert.ok(literature.includes("Bedrossian--Coti Zelati"));
  assert.ok(literature.includes("Gardner--Liss--Mattingly"));
  assert.ok(literature.includes("开放接口 · R0.74L"));
});

test("R0.74K PDF is cryptographically bound to Chinese HTML", async () => {
  await access(resolve(root, "public/notes/r0-74k.pdf"));
  const binding = JSON.parse(await text("research/r074k_pdf_bindings.json"));
  const html = await read("public/notes/r0-74k.html");
  const pdf = await read("public/notes/r0-74k.pdf");
  assert.equal(binding.release, "R0.74K");
  assert.equal(binding.publicChineseNote.sha256, sha256(html));
  assert.equal(binding.publicPdf.sha256, sha256(pdf));
  assert.ok(binding.publicPdf.pageCount >= 2 && binding.publicPdf.pageCount <= 4);
  assert.equal(binding.publicPdf.title, "R0.74K｜自由热指数为何只卡在最近内领圈");
  assert.deepEqual(binding.claimBoundary.evidenceClassesSeparated, ["PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY"]);
});

test("R0.73X recap remains byte-preserved and no R0.74K recap exists", async () => {
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.html")), "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776");
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.pdf")), "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa");
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74k.html")));
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74k.pdf")));
});
