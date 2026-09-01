import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

test("R0.74L owns exact current-state accounting", async () => {
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

  assert.equal(version, "1.78");
  assert.equal(manifest.siteVersion, version);
  assert.equal(site.version, version);
  assert.equal(manifest.latestCompletedRelease, "r074l");
  assert.equal(site.latestRelease, "R0.74L");
  assert.equal(manifest.nextRelease, "r074m");
  assert.equal(manifest.publicHtmlNoteCount, htmlCount);
  assert.equal(site.publicHtmlNoteCount, htmlCount);
  assert.equal(htmlCount, 214);
  assert.equal(manifest.publicPdfNoteCount, pdfCount);
  assert.equal(site.publicPdfNoteCount, pdfCount);
  assert.equal(pdfCount, 171);
  assert.equal(manifest.postR060PublishedNodeCount, postR060Count);
  assert.equal(site.postR060PublishedNodeCount, postR060Count);
  assert.equal(postR060Count, 154);
  assert.equal(manifest.postR060RecapNodeCount, 140);
  assert.equal(site.postR060RecapNodeCount, 140);
  assert.equal(manifest.latestRecapRelease, "r073x");
  assert.equal(site.latestRecapRelease, "R0.73X");
  assert.equal(inventory.latestPublishedRelease, "r074l");
  assert.equal(inventory.publishedReleaseCount, 116);
  assert.equal(inventory.formalSealedReleaseCount, 92);
  assert.equal(manifest.postR070APublishedReleaseCount, 116);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 92);
  assert.ok(inventory.publishedReleases.includes("r074l"));
  assert.ok(inventory.formalSealedReleases.includes("r074l"));

  for (const marker of [
    "LATEST RELEASE · R0.74L · 2026-09-02", "214 篇研究笔记总索引",
    "R0.70A–R0.74L · 116 节已公开", "92 节完整封存", "当前端点 R0.74L",
    "<strong>R0.74L</strong>最新研究节点", "展开 124 篇公开笔记",
  ]) assert.ok(home.includes(marker), marker);
  assert.equal((index.match(/class="note-entry"/g) ?? []).length, htmlCount);
  assert.ok(index.includes('data-note="r0-74l"'));
  assert.ok(index.includes('href="/notes/r0-74l.pdf"'));
});

test("complete Chinese note preserves the L theorem, qualifiers, and evidence links", async () => {
  const note = await text("public/notes/r0-74l.html");
  for (const marker of [
    "完整中文版本", "PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY",
    "\\sup_{\\tau\\in I_{R_j}}\\mathscr B_j(\\tau)\\le C L_jR_j^5",
    "\\text{main target collar}\\le C\\Gamma_jL_jR_j^5",
    "|F_j|^2\\le2(|F_j^+|^2+|F_j^-|^2)",
    "A=\\frac{4876875}{1476395008}", "A-\\frac1{320}=\\frac{1315703}{7381975040}>0",
    "O(L_jR_j^3)", "\\sup_{x_3}\\int M_j^\\sharp(x_2,x_3)",
    "24/24", "45/45", "22/22", "最近内领圈仍然 OPEN", "没有使用正负包之间的抵消",
  ]) assert.ok(note.includes(marker), marker);
  for (const path of [
    "r074l_problem_freeze.md", "r074l_forward_bridge_bv_reduction.md",
    "r074l_main_collar_independent_audit.md", "r074l_final_source_rebind_audit.md",
    "r074l_main_collar_certificate.py", "r074l_main_collar_certificate_independent.rb",
    "r074l_main_collar_certificate.json", "r074l_main_collar_certificate_report.md",
    "r074l_certificate_independent_audit.md", "r074l_primary_literature_audit.md",
    "r074l_gap_matrix.md", "r074l_bilingual_dictionary.md", "r074l_report-source.md",
    "r074l_freeze_manifest.json", "source-data.csv", "caption.md", "qa-report.md",
    "plot.py", "validate.py", "manifest.json", "SHA256SUMS",
  ]) assert.ok(note.includes(path), path);
  assert.ok(note.includes('srcset="/assets/r074l/fig-r074l-forward-clock-bv.svg"'));
  assert.ok(note.includes('src="/assets/r074l/fig-r074l-forward-clock-bv.png"'));
  for (const forbidden of ["世界首个", "首次证明", "解决千禧年问题", "接近解决"])
    assert.ok(!note.includes(forbidden), forbidden);
});

test("public L figure mirrors and masters are exact frozen copies", async () => {
  const source = "research/figures/r074l/fig-r074l-forward-clock-bv";
  const mirror = "public/figures/r074l/fig-r074l-forward-clock-bv";
  const names = await readdir(resolve(root, source));
  assert.equal(names.length, 23);
  for (const name of names)
    assert.deepEqual(await read(`${mirror}/${name}`), await read(`${source}/${name}`), name);
  for (const extension of ["svg", "pdf", "png"])
    assert.deepEqual(
      await read(`public/assets/r074l/fig-r074l-forward-clock-bv.${extension}`),
      await read(`${source}/figure.${extension}`), extension,
    );
});

test("homepage and literature expose one concise L release boundary", async () => {
  const [home, literature] = await Promise.all([
    text("public/research-review.html"), text("public/literature-review.html"),
  ]);
  assert.equal((home.match(/data-release="r074l"/g) ?? []).length, 1);
  const start = home.indexOf('<div class="task-one" id="r074l"');
  const end = home.indexOf('<div class="task-one"', start + 1);
  const card = home.slice(start, end);
  assert.ok(start >= 0 && end > start);
  assert.ok(card.length < 900, "homepage R0.74L card must remain concise");
  assert.ok(card.includes("变化的桥族、短时钟"));
  assert.ok(card.includes("最近内领圈仍为 OPEN"));
  assert.ok(literature.includes('id="r074l-boundary"'));
  assert.ok(literature.includes("有界十篇主源审计"));
  assert.ok(literature.includes("开放接口 · R0.74M"));
});

test("R0.74L PDF is cryptographically bound to Chinese HTML", async () => {
  await access(resolve(root, "public/notes/r0-74l.pdf"));
  const binding = JSON.parse(await text("research/r074l_pdf_bindings.json"));
  const html = await read("public/notes/r0-74l.html");
  const pdf = await read("public/notes/r0-74l.pdf");
  assert.equal(binding.release, "R0.74L");
  assert.equal(binding.publicChineseNote.sha256, sha256(html));
  assert.equal(binding.publicPdf.sha256, sha256(pdf));
  assert.ok(binding.publicPdf.pageCount >= 2 && binding.publicPdf.pageCount <= 4);
  assert.equal(binding.publicPdf.title, "R0.74L｜变化的桥族、短时钟，和一个闭合的主领圈");
  assert.deepEqual(binding.claimBoundary.evidenceClassesSeparated, ["PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY"]);
});

test("R0.73X recap remains byte-preserved and no R0.74L recap exists", async () => {
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.html")), "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776");
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.pdf")), "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa");
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74l.html")));
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74l.pdf")));
});
