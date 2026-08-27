import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");

async function json(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

test("publishes the 100-node cumulative recap in 26 phases", async () => {
  const recap = await readFile(
    resolve(publicRoot, "recap-r0-61-r0-72j.html"),
    "utf8",
  );

  assert.match(recap, /R0\.61–R0\.72J 的 100 节公开笔记/);
  assert.match(recap, /回顾截止时公开笔记：160/);
  assert.match(recap, /62<\/strong><span>R0\.70A–R0\.72J 已公开版本/);
  assert.match(recap, /38<\/strong><span>当前 formal-figure 合同下完整封存/);
  assert.match(recap, /24<\/strong><span>旧版 formal-figure 档案待回补/);
  assert.match(recap, /26<\/strong><span>按问题划分的研究阶段/);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 26);

  for (const token of [
    "R0.61–R0.66",
    "R0.69P–R0.69W",
    "R0.70A–R0.70I",
    "R0.71A–R0.71D",
    "R0.71U–R0.71Z",
    "R0.72A",
    "R0.72I",
    "R0.72J",
  ]) {
    assert.ok(recap.includes(token), token);
  }

  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  assert.equal(
    (recap.slice(start, end).match(/href="\/notes\/r0-[^"]+\.html"/g) ?? [])
      .length,
    100,
  );
  assert.match(recap, /href="\/recap-r0-60\.html"/);
  assert.match(recap, /href="\/recap-r0-61-r0-72i\.html"/);
  assert.match(recap, /href="\/notes\/r0-72j\.html"/);
  assert.match(recap, /R0\.72K/);
  assert.match(recap, /multi-scale|多尺度/);
  assert.match(recap, /complex-root|复目标/);
  assert.doesNotMatch(recap, /千禧年问题(?:已经|已被|得到)(?:解决|证明)/);
});

test("retains J while synchronizing v1.28, latest O, next P, and archive counts", async () => {
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
  assert.match(home, /67 个版本已公开/);
  assert.match(home, /43 个按当前 formal-figure 合同完整封存|43 个完整封存/);
  assert.match(home, /24 个旧版附图档案仍列入回补清单/);
  assert.equal((home.match(/data-release="r072k"/g) ?? []).length, 1);
  assert.equal((home.match(/data-release="r072j"/g) ?? []).length, 1);
  assert.match(home, /recap-r0-61-r0-72o\.html/);
  assert.match(home, /href="\/notes\/r0-72j\.html"/);

  assert.match(literature, /本站 R0\.69P–R0\.72O 只列为研究笔记/);
  assert.match(literature, /id="r072k-boundary"/);
  assert.match(literature, /id="r072j-boundary"/);
  assert.match(literature, /开放接口 · R0\.72P/);
  assert.match(literature, /href="\/notes\/r0-72k\.html"/);
  assert.match(literature, /href="\/notes\/r0-72j\.html"/);
  for (const source of [
    "arxiv.org/abs/2411.19428",
    "arxiv.org/abs/math/0307142",
    "arxiv.org/abs/1905.01374",
    "arxiv.org/abs/2101.11694",
    "arxiv.org/abs/1204.5082",
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
      published: 67,
      sealed: 43,
      backlog: 24,
    },
  );
  assert.equal(
    release.latestReleaseGate,
    "tests/r072o-physical-reinsertion-gate.test.mjs",
  );
  assert.equal(archive.latestPublishedRelease, "r072o");
  assert.equal(archive.publishedReleaseCount, 67);
  assert.equal(archive.formalSealedReleaseCount, 43);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.ok(archive.publishedReleases.includes("r072k"));
  assert.ok(archive.formalSealedReleases.includes("r072k"));
  assert.ok(archive.publishedReleases.includes("r072j"));
  assert.ok(archive.formalSealedReleases.includes("r072j"));
  assert.equal(archive.publishedReleases.length, 67);
  assert.equal(archive.formalSealedReleases.length, 43);
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.28",
    latestRelease: "R0.72O",
    publicHtmlNoteCount: 165,
    publishedDate: "2026-08-27",
  });
});

test("current shell uses v1.25 while historical J pages retain v1.23", async () => {
  const currentPages = await Promise.all(
    ["research-review.html", "literature-review.html"].map((name) =>
      readFile(resolve(publicRoot, name), "utf8"),
    ),
  );
  const historicalPages = await Promise.all(
    ["notes/r0-72j.html", "recap-r0-61-r0-72j.html"].map((name) =>
      readFile(resolve(publicRoot, name), "utf8"),
    ),
  );
  for (const page of currentPages) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.28"/);
  }
  for (const page of historicalPages) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.23"/);
  }
  for (const page of [...currentPages, ...historicalPages]) {
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  }
});

test("R0.72J table of contents names only existing section anchors", async () => {
  const note = await readFile(resolve(publicRoot, "notes/r0-72j.html"), "utf8");
  const tocStart = note.indexOf('<aside class="toc">');
  const tocEnd = note.indexOf("</aside>", tocStart);
  assert.ok(tocStart >= 0 && tocEnd > tocStart);
  const toc = note.slice(tocStart, tocEnd);
  const anchors = [...toc.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.deepEqual(anchors, [
    "result",
    "graph",
    "triangle",
    "band",
    "coherent",
    "root",
    "audit",
    "figure",
    "value",
    "next",
    "claims",
    "reproduce",
  ]);
  for (const anchor of anchors) {
    assert.ok(note.includes('id="' + anchor + '"'), anchor);
  }
});

test("the J note constrains its formal figure to the article width", async () => {
  const note = await readFile(resolve(publicRoot, "notes/r0-72j.html"), "utf8");
  assert.match(note, /article img\{max-width:100%;height:auto\}/);
});

test("all J-facing rate statements retain the exact critical-log offset", async () => {
  const pages = await Promise.all(
    [
      "research-review.html",
      "notes/r0-72j.html",
      "recap-r0-61-r0-72j.html",
    ].map((name) => readFile(resolve(publicRoot, name), "utf8")),
  );
  for (const page of pages) {
    assert.ok(page.includes("R^{-4/9}(1+\\log R)^{-2/3}"));
    assert.doesNotMatch(page, /R\^\{-4\/9\}\(\\log R\)\^\{-2\/3\}/);
  }
});

test("publishes nontrivial synchronized note and recap PDFs", async () => {
  const [notePdf, recapPdf] = await Promise.all([
    readFile(resolve(publicRoot, "notes/r0-72j.pdf")),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72j.pdf")),
  ]);
  for (const pdf of [notePdf, recapPdf]) {
    assert.equal(pdf.subarray(0, 5).toString(), "%PDF-");
    assert.ok(pdf.length > 100_000);
  }
});
