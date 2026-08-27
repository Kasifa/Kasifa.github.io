import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  collectSiteStrings,
  extractProtectedTokens,
} from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");

async function json(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

function nodeIndex(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start, "current recap node index");
  return recap.slice(start, end);
}

test("publishes a unique 106-node recap through R0.72P", async () => {
  const recap = await readFile(resolve(publicRoot, "recap-r0-61-r0-72p.html"), "utf8");
  assert.match(recap, /R0\.61–R0\.72P 的 106 节公开笔记/);
  assert.match(recap, /回顾截止时公开笔记：166/);
  assert.match(recap, /68<\/strong><span>R0\.70A–R0\.72P 已公开版本/);
  assert.match(recap, /44<\/strong><span>当前 formal-figure 合同下完整封存/);
  assert.match(recap, /24<\/strong><span>旧版 formal-figure 档案待回补/);
  assert.match(recap, /28<\/strong><span>按问题划分的研究阶段/);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 28);

  const index = nodeIndex(recap);
  const links = [...index.matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map((match) => match[1]);
  assert.equal(links.length, 106);
  assert.equal(new Set(links).size, 106, "node index must not repeat a note");
  assert.equal(links.filter((slug) => slug === "r0-69w").length, 1);
  for (const [series, end] of [["70", "z"], ["71", "z"], ["72", "p"]]) {
    for (let code = 97; code <= end.charCodeAt(0); code += 1) {
      const slug = `r0-${series}${String.fromCharCode(code)}`;
      assert.equal(links.filter((entry) => entry === slug).length, 1, slug);
    }
  }
  for (const token of [
    "R0.72L–R0.72P",
    "fixed real-collinear-phase 1:2",
    "full-superposition ED",
    "\\mathcal C_\\times\\lesssim4a^2\\sqrt\\varepsilon",
    "Morse applicability wall",
    "R0.72Q",
    "/recap-r0-60.html",
    "/recap-r0-61-r0-72o.html",
  ]) assert.ok(recap.includes(token), token);
});

test("synchronizes v1.29, latest P, next Q, route 76, and release counts", async () => {
  const [home, literature, release, archive, site, files] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    json(resolve(root, "research/release-manifest.json")),
    json(resolve(root, "research/formal-archive-inventory.json")),
    json(resolve(publicRoot, "site-version.json")),
    readdir(resolve(publicRoot, "notes")),
  ]);
  assert.equal(files.filter((name) => name.endsWith(".html")).length, 166);
  for (const pattern of [
    /data-site-version="1\.29"/,
    /<strong>v1\.29<\/strong>网页版本/,
    /<strong>166<\/strong>公开研究笔记/,
    /<strong>R0\.72P<\/strong>最新研究节点/,
    /R0\.70A–R0\.72P：68 节已公开，44 节完整封存/,
    /<span class="route-range">R0\.69P–R0\.72P<\/span>/,
    /展开 76 篇公开笔记/,
    /NEXT · R0\.72Q/,
    /累计回顾收录 106 个节点；全站现有 166 篇公开研究笔记/,
  ]) assert.match(home, pattern);
  assert.equal((home.match(/data-release="r072p"/g) ?? []).length, 1);
  assert.match(home, /href="\/notes\/r0-72p\.html"/);
  assert.match(home, /fig-r072p-superposition-gate/);

  assert.match(literature, /本站 R0\.69P–R0\.72P 只列为研究笔记/);
  assert.match(literature, /id="r072p-boundary"/);
  assert.match(literature, /开放接口 · R0\.72Q/);
  assert.match(literature, /href="\/notes\/r0-72p\.html"/);
  assert.match(literature, /href="\/recap-r0-61-r0-72p\.html"/);
  for (const source of [
    "10.4310/CMS.2024.v22.n6.a10",
    "10.1007/s00205-017-1099-y",
    "10.1112/jlms.12782",
  ]) assert.ok(literature.includes(source) || home.includes(source), source);

  assert.deepEqual({
    latest: release.latestCompletedRelease,
    version: release.siteVersion,
    notes: release.publicHtmlNoteCount,
    recap: release.postR060RecapNodeCount,
    next: release.nextRelease,
    gate: release.latestReleaseGate,
    publicationTest: release.latestReleasePublicationTest,
    published: release.postR070APublishedReleaseCount,
    sealed: release.postR070AFormalSealedReleaseCount,
    backlog: release.legacyFormalFigureBacklogCount,
  }, {
    latest: "r072p",
    version: "1.29",
    notes: 166,
    recap: 106,
    next: "r072q",
    gate: "tests/r072p-superposition-gate.test.mjs",
    publicationTest: "tests/r072p-release.test.mjs",
    published: 68,
    sealed: 44,
    backlog: 24,
  });
  assert.equal(archive.latestPublishedRelease, "r072p");
  assert.equal(archive.publishedReleaseCount, 68);
  assert.equal(archive.formalSealedReleaseCount, 44);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.equal(archive.publishedReleases.length, 68);
  assert.equal(archive.formalSealedReleases.length, 44);
  assert.equal(archive.publishedReleases.at(-1), "r072p");
  assert.equal(archive.formalSealedReleases.at(-1), "r072p");
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.29",
    latestRelease: "R0.72P",
    publicHtmlNoteCount: 166,
    publishedDate: "2026-08-27",
  });
});

test("ships synchronized P note, recap, figure assets, and source links", async () => {
  const [note, notePdf, recap, recapPdf, home, literature] = await Promise.all([
    readFile(resolve(publicRoot, "notes/r0-72p.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72p.pdf")),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72p.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72p.pdf")),
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
  ]);
  for (const page of [note, recap, home, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.29"/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /[A-Za-z0-9_}]\\\(/, "function arguments must not become fresh MathJax delimiters");
    assert.doesNotMatch(page, /\\\((?:(?!\\\)).)*\\\(/s, "inline MathJax delimiters must not nest");
  }
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  assert.match(note, /href="\/notes\/r0-72p\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-72p\.html"/);
  assert.match(note, /href="\/recap-r0-61-r0-72p\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-72p\.pdf"/);
  for (const [label, pdf] of [["note", notePdf], ["recap", recapPdf]]) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label);
    assert.ok(pdf.length > 10_000, label + " PDF is unexpectedly small");
  }
  for (const extension of ["pdf", "png", "svg"]) {
    const relative = `/assets/r072p/fig-r072p-superposition-gate.${extension}`;
    const asset = await readFile(resolve(publicRoot, relative.slice(1)));
    assert.ok(note.includes(relative), relative);
    assert.ok(asset.length > 1_000, extension);
  }
  for (const source of [
    "research/r072p_report-source.md",
    "research/r072p_literature_audit.md",
    "research/r072p_gap_matrix.md",
    "research/r072p_independent_audit.md",
    "research/certificates/r072p",
    "figures/r072p-superposition-gate/fig-r072p-superposition-gate",
  ]) assert.ok(note.includes(source), source);
});

test("keeps the fixed 1:2 theorem, applicability wall, and open claims exact", async () => {
  const note = await readFile(resolve(publicRoot, "notes/r0-72p.html"), "utf8");
  const tocStart = note.indexOf('<aside class="toc">');
  const tocEnd = note.indexOf("</aside>", tocStart);
  const anchors = [...note.slice(tocStart, tocEnd).matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.deepEqual(anchors, [
    "result", "reduction", "shape", "theorem", "compact", "cubic", "window",
    "wall", "scope", "literature", "figure", "value", "next", "reproduce",
  ]);
  for (const anchor of anchors) assert.ok(note.includes(`id="${anchor}"`), anchor);
  for (const token of [
    "fixed carrier pattern \\(R:2R\\): CLOSED",
    "full-superposition ED: CLOSED",
    "arbitrary phases / carrier sets: OPEN",
    "0&lt;\\lambda_-\\le|\\lambda|\\le1/8",
    "B=N=2",
    "p=2^{-1/2}",
    "1+4\\lambda e^{-3y}\\cos\\phi",
    "C_{\\rm ED}",
    "c_{\\rm ED}",
    "E(1)\\le C_{\\rm ED}e^{-c_{\\rm ED}\\sqrt\\varepsilon}E(0)",
    "\\mathcal C_\\times\\lesssim4a^2\\sqrt\\varepsilon",
    "\\varepsilon^{11/6}p^{4/3}",
    "\\lambda=\\pm1/4",
    "Morse applicability wall",
    "在本项目中首次把 multi-carrier gate",
    "它不证明 enhanced dissipation 失败",
    "Clay 千禧年问题仍未解决",
  ]) assert.ok(note.includes(token), token);
  assert.match(note, /proof-level corollary[\s\S]*不是原论文逐字陈述的 arbitrary-family theorem/);
  assert.doesNotMatch(note, /(?:arbitrary phases|一般三维).*CLOSED/i);
});

test("keeps the legacy R0.69W HTML/PDF publication pair fail closed", async () => {
  const [note, pdf, home, recap] = await Promise.all([
    readFile(resolve(publicRoot, "notes/r0-69w.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-69w.pdf")),
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72p.html"), "utf8"),
  ]);
  assert.match(note, /href="\/notes\/r0-69w\.pdf"/);
  assert.equal(pdf.subarray(0, 4).toString(), "%PDF");
  assert.ok(pdf.length > 10_000, "R0.69W PDF is unexpectedly small");
  assert.match(home, /href="\/notes\/r0-69w\.html"/);
  assert.match(home, /href="\/notes\/r0-69w\.pdf"/);
  assert.match(nodeIndex(recap), /href="\/notes\/r0-69w\.html"/);
});

test("covers every live Chinese string with the R0.72P bilingual batch", async () => {
  const [source, translations, built] = await Promise.all([
    collectSiteStrings(publicRoot),
    json(resolve(root, "translations/en.json")),
    readFile(resolve(publicRoot, "i18n-en.js"), "utf8"),
  ]);
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry]));
  assert.equal(byChinese.size, translations.length);
  assert.deepEqual(source.filter((entry) => !byChinese.has(entry.zh)), []);
  const batch = translations.filter((entry) => /^r072p\d+$/.test(entry.id));
  assert.ok(batch.length > 0, "R0.72P translation batch is empty");
  assert.deepEqual([...new Set(batch.flatMap((entry) => entry.files))].sort(), [
    "literature-review.html",
    "notes/r0-72p.html",
    "recap-r0-61-r0-72p.html",
    "research-review.html",
  ]);
  for (const entry of batch) {
    assert.ok(entry.en.trim(), entry.zh);
    assert.doesNotMatch(entry.en, /[\u3400-\u9fff\uf900-\ufaff]/u);
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i);
    assert.doesNotMatch(entry.en, /^This (?:literature-boundary|R0\.72P note|cumulative-recap|route) entry\b/);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh));
  }
  for (const chinese of [
    "状态 · R0.72P 固定两载波正类完成",
    "两个载波必须作为一个完整算子缩到固定圆周",
    "\\(\\lambda=\\pm1/4\\) 是适用性墙，不是动力学反例",
    "R0.72Q：测试相位扰动与更一般有限 pattern 的 uniform shape contract",
  ]) {
    assert.ok(byChinese.has(chinese), chinese);
    assert.ok(built.includes(JSON.stringify(chinese)), chinese);
  }
});

test("the deterministic generator advances exactly from O to P", async () => {
  const generator = await readFile(resolve(root, "scripts/generate_r072p_release.py"), "utf8");
  for (const token of [
    "public/notes/r0-72o.html",
    "public/recap-r0-61-r0-72o.html",
    "notes/r0-72p.html",
    "recap-r0-61-r0-72p.html",
    "expected 166 public HTML notes",
    '"recapNodes": 106',
    '"published": 68',
    '"formalSealed": 44',
    '"legacyBacklog": 24',
    '"routeNotes": 76',
    '"next": "R0.72Q"',
    "r0-69w",
    "figures/r072p-superposition-gate/fig-r072p-superposition-gate",
    "tests/r072p-superposition-gate.test.mjs",
    "tests/r072p-release.test.mjs",
    "assert_mathjax_clean",
    "E(1)\\le C_{\\rm ED}",
    "在本项目中首次把 multi-carrier gate",
  ]) assert.ok(generator.includes(token), token);
  assert.ok(generator.indexOf('"latestCompletedRelease": "r072o"') < generator.indexOf('"latestCompletedRelease": "r072p"'));
  assert.doesNotMatch(generator, /r072p-physical-reinsertion|fig-r072p-physical-reinsertion/);
});
