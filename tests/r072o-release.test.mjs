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

test("publishes a unique 105-node recap through R0.72O", async () => {
  const recap = await readFile(
    resolve(publicRoot, "recap-r0-61-r0-72o.html"),
    "utf8",
  );
  assert.match(recap, /R0\.61–R0\.72O 的 105 节公开笔记/);
  assert.match(recap, /回顾截止时公开笔记：165/);
  assert.match(recap, /67<\/strong><span>R0\.70A–R0\.72O 已公开版本/);
  assert.match(recap, /43<\/strong><span>当前 formal-figure 合同下完整封存/);
  assert.match(recap, /24<\/strong><span>旧版 formal-figure 档案待回补/);
  assert.match(recap, /28<\/strong><span>按问题划分的研究阶段/);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 28);

  const index = nodeIndex(recap);
  const links = [...index.matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map(
    (match) => match[1],
  );
  assert.equal(links.length, 105);
  assert.equal(new Set(links).size, 105, "node index must not repeat a note");
  assert.equal(links.filter((slug) => slug === "r0-69w").length, 1);
  for (const [series, end] of [
    ["70", "z"],
    ["71", "z"],
    ["72", "o"],
  ]) {
    for (let code = "a".charCodeAt(0); code <= end.charCodeAt(0); code += 1) {
      const slug = `r0-${series}${String.fromCharCode(code)}`;
      assert.equal(links.filter((entry) => entry === slug).length, 1, slug);
    }
  }
  for (const token of [
    "R0.72L–R0.72O",
    "U_{\\rm ED}^{(1)}=\\varepsilon^{11/6}",
    "\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^2",
    "full-superposition integrated ED",
    "common-band support 不能自动保证统一 Morse margin",
    "R0.72P",
    "/recap-r0-60.html",
    "/recap-r0-61-r0-72n.html",
  ]) {
    assert.ok(recap.includes(token), token);
  }
});

test("synchronizes v1.28, latest O, next P, and release counts", async () => {
  const [home, literature, release, archive, site, files] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    json(resolve(root, "research/release-manifest.json")),
    json(resolve(root, "research/formal-archive-inventory.json")),
    json(resolve(publicRoot, "site-version.json")),
    readdir(resolve(publicRoot, "notes")),
  ]);

  assert.equal(files.filter((name) => name.endsWith(".html")).length, 165);
  assert.match(home, /<html lang="zh-CN" data-site-version="1\.28">/);
  assert.match(home, /<strong>v1\.28<\/strong>网页版本/);
  assert.match(home, /<strong>165<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72O<\/strong>最新研究节点/);
  assert.match(home, /R0\.70A–R0\.72O：67 节已公开，43 节完整封存/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72O<\/span>/);
  assert.match(home, /展开 75 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72P/);
  assert.match(home, /累计回顾收录 105 个节点；全站现有 165 篇公开研究笔记/);
  assert.equal((home.match(/data-release="r072o"/g) ?? []).length, 1);
  assert.equal((home.match(/href="\/notes\/r0-72o\.html"/g) ?? []).length, 2);
  assert.match(home, /physical reinsertion/i);
  assert.match(home, /full-superposition ED gate/i);

  assert.match(literature, /本站 R0\.69P–R0\.72O 只列为研究笔记/);
  assert.match(literature, /id="r072o-boundary"/);
  assert.match(literature, /开放接口 · R0\.72P/);
  assert.match(literature, /href="\/notes\/r0-72o\.html"/);
  assert.match(literature, /href="\/recap-r0-61-r0-72o\.html"/);
  for (const source of [
    "arxiv.org/html/2309.15738",
    "10.4310/CMS.2024.v22.n6.a10",
    "10.1112/jlms.12782",
  ]) {
    assert.ok(literature.includes(source) || home.includes(source), source);
  }

  assert.deepEqual(
    {
      latest: release.latestCompletedRelease,
      version: release.siteVersion,
      notes: release.publicHtmlNoteCount,
      recap: release.postR060RecapNodeCount,
      next: release.nextRelease,
      gate: release.latestReleaseGate,
      published: release.postR070APublishedReleaseCount,
      sealed: release.postR070AFormalSealedReleaseCount,
      backlog: release.legacyFormalFigureBacklogCount,
    },
    {
      latest: "r072o",
      version: "1.28",
      notes: 165,
      recap: 105,
      next: "r072p",
      gate: "tests/r072o-physical-reinsertion-gate.test.mjs",
      published: 67,
      sealed: 43,
      backlog: 24,
    },
  );
  assert.equal(archive.latestPublishedRelease, "r072o");
  assert.equal(archive.publishedReleaseCount, 67);
  assert.equal(archive.formalSealedReleaseCount, 43);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.equal(archive.publishedReleases.length, 67);
  assert.equal(archive.formalSealedReleases.length, 43);
  assert.equal(archive.publishedReleases.at(-1), "r072o");
  assert.equal(archive.formalSealedReleases.at(-1), "r072o");
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.28",
    latestRelease: "R0.72O",
    publicHtmlNoteCount: 165,
    publishedDate: "2026-08-27",
  });
});

test("ships synchronized O note, recap, figure assets, and source links", async () => {
  const [note, notePdf, recap, recapPdf, home, literature] = await Promise.all([
    readFile(resolve(publicRoot, "notes/r0-72o.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72o.pdf")),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72o.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72o.pdf")),
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
  ]);
  for (const page of [note, recap, home, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.28"/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  }
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  assert.match(note, /href="\/notes\/r0-72o\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-72o\.html"/);
  assert.match(note, /href="\/recap-r0-61-r0-72o\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-72o\.pdf"/);
  for (const [label, pdf] of [["note", notePdf], ["recap", recapPdf]]) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label);
    assert.ok(pdf.length > 10_000, label + " PDF is unexpectedly small");
  }
  for (const extension of ["pdf", "png", "svg"]) {
    const relative = `/assets/r072o/fig-r072o-physical-reinsertion.${extension}`;
    const asset = await readFile(resolve(publicRoot, relative.slice(1)));
    assert.ok(note.includes(relative), relative);
    assert.ok(asset.length > 1_000, extension);
  }
  for (const source of [
    "research/r072o_report-source.md",
    "research/r072o_literature_audit.md",
    "research/r072o_gap_matrix.md",
    "research/r072o_independent_audit.md",
    "research/certificates/r072o",
    "figures/r072o-physical-reinsertion/fig-r072o-physical-reinsertion",
  ]) {
    assert.ok(note.includes(source), source);
  }
});

test("keeps the O theorem, conditional interface, and claim boundaries exact", async () => {
  const note = await readFile(resolve(publicRoot, "notes/r0-72o.html"), "utf8");
  const tocStart = note.indexOf('<aside class="toc">');
  const tocEnd = note.indexOf("</aside>", tocStart);
  const anchors = [...note.slice(tocStart, tocEnd).matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.deepEqual(anchors, [
    "result", "identification", "reinsertion", "ledger", "window", "fixed",
    "superposition", "gate", "literature", "figure", "value", "next",
    "claims", "reproduce",
  ]);
  for (const anchor of anchors) assert.ok(note.includes(`id="${anchor}"`), anchor);

  for (const token of [
    "one-carrier exact correction: CLOSED",
    "multi-carrier full-superposition ED: CONDITIONAL",
    "对 correction 前的 antisymmetric one-carrier launch",
    "\\mathcal C_\\times(\\widetilde G)\\lesssim a^2\\varepsilon^{1/2}",
    "\\varepsilon^{11/6}",
    "\\sqrt\\varepsilon\\lesssim R^{2/3}L_{R,\\varepsilon}",
    "\\varepsilon\\lesssim R^{4/3}L_{R,\\varepsilon}^{\\,2}",
    "上沿只给 \\(O(1)\\)；little-o 版本才使比值趋零",
    "这是带统一常数假设的条件蕴含，不是当前 common-band class 的无条件定理",
    "\\mathcal C_{\\times,R}\\asymp a^2N^2",
    "U_R'(0)=U_R''(0)=0",
    "不能直接调用 Coble–He 的统一非退化定理",
    "Clay 千禧年问题仍未解决",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /Coble–He[\s\S]*不陈述这里的 cubic、物理回填或多载波结论/);
  assert.doesNotMatch(
    note,
    /Coble[–-]He (?:proved|证明).*(?:cubic|physical|multi-carrier)|common-band support (?:guarantees|保证).*Morse/i,
  );
});

test("covers every live Chinese string with the R0.72O bilingual batch", async () => {
  const [source, translations, built] = await Promise.all([
    collectSiteStrings(publicRoot),
    json(resolve(root, "translations/en.json")),
    readFile(resolve(publicRoot, "i18n-en.js"), "utf8"),
  ]);
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry]));
  assert.equal(byChinese.size, translations.length);
  assert.deepEqual(source.filter((entry) => !byChinese.has(entry.zh)), []);
  const batch = translations.filter((entry) => /^r072o\d+$/.test(entry.id));
  assert.ok(batch.length > 0, "R0.72O translation batch is empty");
  assert.deepEqual([...new Set(batch.flatMap((entry) => entry.files))].sort(), [
    "literature-review.html",
    "notes/r0-72o.html",
    "recap-r0-61-r0-72o.html",
    "research-review.html",
  ]);
  for (const entry of batch) {
    assert.ok(entry.en.trim(), entry.zh);
    assert.doesNotMatch(entry.en, /[\u3400-\u9fff\uf900-\ufaff]/u);
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh));
  }
  for (const chinese of [
    "状态 · R0.72O 定理与条件接口完成",
    "平方根 raw exponent 经过物理 lift 后变成 \\(11/6\\)",
    "这是带统一常数假设的条件蕴含，不是当前 common-band class 的无条件定理。",
    "R0.72P：先处理有统一 Morse margin 的有限 carrier pattern",
  ]) {
    assert.ok(byChinese.has(chinese), chinese);
    assert.ok(built.includes(JSON.stringify(chinese)), chinese);
  }
});

test("the deterministic generator advances exactly from N to O", async () => {
  const generator = await readFile(
    resolve(root, "scripts/generate_r072o_release.py"),
    "utf8",
  );
  for (const token of [
    "r0-72n.html",
    "r0-72o.html",
    "recap-r0-61-r0-72n.html",
    "recap-r0-61-r0-72o.html",
    "expected 165 public HTML notes",
    '"recapNodes": 105',
    '"published": 67',
    '"formalSealed": 43',
    '"legacyBacklog": 24',
    '"phases": 28',
    '"next": "R0.72P"',
    "r0-69w",
    "ord(\"z\")",
    "ord(\"o\")",
    "figures/r072o-physical-reinsertion/fig-r072o-physical-reinsertion",
    "tests/r072o-physical-reinsertion-gate.test.mjs",
  ]) {
    assert.ok(generator.includes(token), token);
  }
});
