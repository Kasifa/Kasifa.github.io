import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { collectSiteStrings } from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");

async function json(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

test("publishes the 103-node post-R0.60 recap in 28 phases", async () => {
  const recap = await readFile(
    resolve(publicRoot, "recap-r0-61-r0-72m.html"),
    "utf8",
  );

  assert.match(recap, /R0\.61–R0\.72M 的 103 节公开笔记/);
  assert.match(recap, /回顾截止时公开笔记：163/);
  assert.match(recap, /65<\/strong><span>R0\.70A–R0\.72M 已公开版本/);
  assert.match(recap, /41<\/strong><span>当前 formal-figure 合同下完整封存/);
  assert.match(recap, /24<\/strong><span>旧版 formal-figure 档案待回补/);
  assert.match(recap, /28<\/strong><span>按问题划分的研究阶段/);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 28);

  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start, "current recap node index");
  const index = recap.slice(start, end);
  assert.equal(
    (index.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length,
    103,
  );
  assert.equal(
    (index.match(/href="\/notes\/r0-72m\.html"/g) ?? []).length,
    1,
  );

  for (const token of [
    "R0.72L–R0.72M",
    "exact danger-window theorem",
    "full-lattice reference",
    "action-poor",
    "16/\\pi^2",
    "R0.72N",
    "/recap-r0-60.html",
    "/recap-r0-61-r0-72l.html",
  ]) {
    assert.ok(recap.includes(token), token);
  }
});

test("retains M while synchronizing v1.27, latest N, next O, and all publication counts", async () => {
  const [home, literature, release, archive, site, files] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    json(resolve(root, "research/release-manifest.json")),
    json(resolve(root, "research/formal-archive-inventory.json")),
    json(resolve(publicRoot, "site-version.json")),
    readdir(resolve(publicRoot, "notes")),
  ]);

  assert.equal(files.filter((name) => name.endsWith(".html")).length, 164);
  assert.match(home, /<html lang="zh-CN" data-site-version="1\.27">/);
  assert.match(home, /<strong>v1\.27<\/strong>网页版本/);
  assert.match(home, /<strong>164<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72N<\/strong>最新研究节点/);
  assert.match(home, /R0\.70A–R0\.72N：66 节已公开，42 节完整封存/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72N<\/span>/);
  assert.match(home, /展开 74 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72O/);
  assert.match(home, /累计回顾收录 104 个节点；全站现有 164 篇公开研究笔记/);
  assert.equal((home.match(/data-release="r072m"/g) ?? []).length, 1);
  assert.equal(
    (home.match(/href="\/notes\/r0-72m\.html"/g) ?? []).length,
    2,
  );
  assert.match(home, /exact action danger window/i);
  assert.match(home, /dissipative one-carrier decision/i);
  assert.match(home, /physical reinsertion and multi-carrier/i);

  assert.match(literature, /本站 R0\.69P–R0\.72N 只列为研究笔记/);
  assert.match(literature, /id="r072m-boundary"/);
  assert.match(literature, /开放接口 · R0\.72O/);
  assert.match(literature, /href="\/notes\/r0-72m\.html"/);
  assert.match(literature, /href="\/recap-r0-61-r0-72n\.html"/);
  for (const source of [
    "10.1063/1.858309",
    "10.1017/jfm.2013.637",
    "10.1007/s00205-017-1099-y",
    "10.1112/jlms.12782",
    "https://dlmf.nist.gov/10.6",
    "https://dlmf.nist.gov/10.17",
    "https://dlmf.nist.gov/10.19.iii",
    "https://dlmf.nist.gov/10.20.i",
  ]) {
    assert.ok(literature.includes(source), source);
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
      latest: "r072n",
      version: "1.27",
      notes: 164,
      recap: 104,
      next: "r072o",
      gate: "tests/r072n-dissipative-carrier-gate.test.mjs",
      published: 66,
      sealed: 42,
      backlog: 24,
    },
  );

  assert.equal(archive.latestPublishedRelease, "r072n");
  assert.equal(archive.publishedReleaseCount, 66);
  assert.equal(archive.formalSealedReleaseCount, 42);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.equal(archive.publishedReleases.length, 66);
  assert.equal(archive.formalSealedReleases.length, 42);
  assert.equal(archive.legacyFormalFigureBacklog.length, 24);
  assert.equal(archive.publishedReleases.at(-1), "r072n");
  assert.equal(archive.formalSealedReleases.at(-1), "r072n");

  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.27",
    latestRelease: "R0.72N",
    publicHtmlNoteCount: 164,
    publishedDate: "2026-08-27",
  });
});

test("ships synchronized M HTML/PDF, recap PDF, and three public figure assets", async () => {
  const [note, notePdf, recap, recapPdf, home, literature] = await Promise.all([
    readFile(resolve(publicRoot, "notes/r0-72m.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72m.pdf")),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72m.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72m.pdf")),
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
  ]);

  for (const page of [note, recap]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.26"/);
  }
  for (const page of [home, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.27"/);
  }
  for (const page of [note, recap, home, literature]) {
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  }
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  assert.match(note, /href="\/notes\/r0-72m\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-72m\.html"/);
  assert.match(note, /href="\/recap-r0-61-r0-72m\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-72m\.pdf"/);
  assert.match(home, /href="\/notes\/r0-72m\.pdf"/);
  assert.match(literature, /href="\/notes\/r0-72m\.html"/);

  for (const [label, pdf] of [
    ["note", notePdf],
    ["recap", recapPdf],
  ]) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", `${label} PDF header`);
    assert.ok(pdf.length > 10_000, `${label} PDF is unexpectedly small`);
  }

  for (const extension of ["pdf", "png", "svg"]) {
    const relative = `/assets/r072m/fig-r072m-danger-window.${extension}`;
    const asset = await readFile(
      resolve(publicRoot, `assets/r072m/fig-r072m-danger-window.${extension}`),
    );
    assert.ok(note.includes(relative), relative);
    assert.ok(asset.length > 1_000, extension);
  }
  assert.ok(recap.includes("/assets/r072m/fig-r072m-danger-window.pdf"));
  assert.ok(home.includes("/assets/r072m/fig-r072m-danger-window.pdf"));
});

test("keeps the M table of contents and claim-boundary anchors intact", async () => {
  const note = await readFile(resolve(publicRoot, "notes/r0-72m.html"), "utf8");
  const tocStart = note.indexOf('<aside class="toc">');
  const tocEnd = note.indexOf("</aside>", tocStart);
  assert.ok(tocStart >= 0 && tocEnd > tocStart);
  const anchors = [
    ...note.slice(tocStart, tocEnd).matchAll(/href="#([^"]+)"/g),
  ].map((match) => match[1]);

  assert.deepEqual(anchors, [
    "result",
    "window",
    "bessel",
    "action",
    "cubic",
    "placement",
    "audit",
    "figure",
    "literature",
    "value",
    "next",
    "claims",
    "reproduce",
  ]);
  for (const anchor of anchors) {
    assert.ok(note.includes(`id="${anchor}"`), anchor);
  }
  for (const token of [
    "dissipative uniform theorem: OPEN",
    "一般三维正则性：OPEN",
    "Clay 千禧年问题仍未解决",
    "耗散曲线只表明两种有限离散",
  ]) {
    assert.ok(note.includes(token), token);
  }
});

test("covers every live Chinese string with the R0.72M bilingual batch", async () => {
  const [source, translations, built] = await Promise.all([
    collectSiteStrings(publicRoot),
    json(resolve(root, "translations/en.json")),
    readFile(resolve(publicRoot, "i18n-en.js"), "utf8"),
  ]);
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry]));
  assert.equal(byChinese.size, translations.length);
  assert.deepEqual(
    source.filter((entry) => !byChinese.has(entry.zh)),
    [],
    "every live Chinese string must have an English translation",
  );

  const batch = translations.filter((entry) => /^r072m\d+$/.test(entry.id));
  assert.ok(batch.length > 0, "R0.72M translation batch is empty");
  assert.deepEqual(
    [...new Set(batch.flatMap((entry) => entry.files))].sort(),
    [
      "literature-review.html",
      "notes/r0-72m.html",
      "recap-r0-61-r0-72m.html",
      "research-review.html",
    ],
  );
  for (const chinese of [
    "状态 · R0.72M 定理完成",
    "危险项只在中间 action 窗口出现；",
    "R0.72N：回到带 \\(-n^2f_n\\) 的耗散链",
  ]) {
    const entry = byChinese.get(chinese);
    assert.ok(entry, chinese);
    assert.ok(entry.en.trim().length > 0, chinese + ": English value");
    assert.ok(built.includes(JSON.stringify(chinese)), chinese + ": built dictionary");
  }
});

test("the deterministic generator advances exactly from L to M", async () => {
  const generator = await readFile(
    resolve(root, "scripts/generate_r072m_release.py"),
    "utf8",
  );
  for (const token of [
    "r0-72l.html",
    "r0-72m.html",
    "recap-r0-61-r0-72l.html",
    "recap-r0-61-r0-72m.html",
    "expected 163 public HTML notes",
    '"recapNodes": 103',
    '"published": 65',
    '"formalSealed": 41',
    '"legacyBacklog": 24',
    '"phases": 28',
    '"next": "R0.72N"',
  ]) {
    assert.ok(generator.includes(token), token);
  }
});
