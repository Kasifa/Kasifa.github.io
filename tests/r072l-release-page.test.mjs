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

test("publishes the 102-node recap in 28 phases", async () => {
  const recap = await readFile(
    resolve(publicRoot, "recap-r0-61-r0-72l.html"),
    "utf8",
  );

  assert.match(recap, /R0\.61–R0\.72L 的 102 节公开笔记/);
  assert.match(recap, /回顾截止时公开笔记：162/);
  assert.match(recap, /64<\/strong><span>R0\.70A–R0\.72L 已公开版本/);
  assert.match(recap, /40<\/strong><span>当前 formal-figure 合同下完整封存/);
  assert.match(recap, /24<\/strong><span>旧版 formal-figure 档案待回补/);
  assert.match(recap, /28<\/strong><span>按问题划分的研究阶段/);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 28);

  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  assert.equal(
    (recap.slice(start, end).match(/href="\/notes\/r0-[^"]+\.html"/g) ?? [])
      .length,
    102,
  );
  for (const token of [
    "R0.72K",
    "R0.72L",
    "R0.72M",
    "phase-aligned",
    "row-aligned",
    "exact-corrected",
    "little-o",
    "extreme strong coupling",
  ]) {
    assert.ok(recap.includes(token), token);
  }
});

test("synchronizes v1.25, latest L, next M, and archive counts", async () => {
  const [home, literature, release, archive, site, files] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    json(resolve(root, "research/release-manifest.json")),
    json(resolve(root, "research/formal-archive-inventory.json")),
    json(resolve(publicRoot, "site-version.json")),
    readdir(resolve(publicRoot, "notes")),
  ]);

  assert.equal(files.filter((name) => name.endsWith(".html")).length, 162);
  assert.match(home, /<html lang="zh-CN" data-site-version="1\.25">/);
  assert.match(home, /<strong>v1\.25<\/strong>网页版本/);
  assert.match(home, /<strong>162<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72L<\/strong>最新研究节点/);
  assert.match(home, /R0\.70A–R0\.72L：64 节已公开，40 节完整封存/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72L<\/span>/);
  assert.match(home, /展开 72 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72M/);
  assert.match(home, /累计回顾收录 102 个节点；全站现有 162 篇公开研究笔记/);
  assert.equal((home.match(/data-release="r072l"/g) ?? []).length, 1);
  assert.match(home, /enstrophy-aware moderate strong-coupling closure/i);
  assert.match(home, /extreme strong-coupling cascade ledger/i);

  assert.match(literature, /本站 R0\.69P–R0\.72L 只列为研究笔记/);
  assert.match(literature, /id="r072l-boundary"/);
  assert.match(literature, /开放接口 · R0\.72M/);
  assert.match(literature, /href="\/notes\/r0-72l\.html"/);
  for (const source of [
    "10.1063/1.4990082",
    "10.1063/1.858309",
    "10.1017/jfm.2013.637",
    "10.1006/aima.2000.1937",
    "10.4310/MAA.2007.v14.n2.a5",
    "10.1070/RM2003v058n02ABEH000609",
    "10.1090/jams/838",
    "10.1007/s00222-025-01396-z",
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
      latest: "r072l",
      version: "1.25",
      notes: 162,
      recap: 102,
      next: "r072m",
      published: 64,
      sealed: 40,
      backlog: 24,
    },
  );
  assert.equal(
    release.latestReleaseGate,
    "tests/r072l-strong-coupling-gate.test.mjs",
  );
  assert.equal(archive.latestPublishedRelease, "r072l");
  assert.equal(archive.publishedReleaseCount, 64);
  assert.equal(archive.formalSealedReleaseCount, 40);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.equal(archive.publishedReleases.length, 64);
  assert.equal(archive.formalSealedReleases.length, 40);
  assert.ok(archive.publishedReleases.includes("r072l"));
  assert.ok(archive.formalSealedReleases.includes("r072l"));
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.25",
    latestRelease: "R0.72L",
    publicHtmlNoteCount: 162,
    publishedDate: "2026-08-27",
  });
});

test("all L-facing pages and the generator avoid forbidden control bytes", async () => {
  const paths = [
    resolve(root, "scripts/generate_r072l_release.py"),
    resolve(publicRoot, "research-review.html"),
    resolve(publicRoot, "literature-review.html"),
    resolve(publicRoot, "notes/r0-72l.html"),
    resolve(publicRoot, "recap-r0-61-r0-72l.html"),
  ];
  for (const path of paths) {
    const value = await readFile(path, "utf8");
    assert.doesNotMatch(value, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  }
});

test("the R0.72L bilingual batch covers every live Chinese site string", async () => {
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
  const batch = translations.filter((entry) => /^r072l\d+$/.test(entry.id));
  assert.equal(batch.length, 136);
  assert.deepEqual(
    [...new Set(batch.flatMap((entry) => entry.files))],
    [
      "literature-review.html",
      "notes/r0-72l.html",
      "recap-r0-61-r0-72l.html",
      "research-review.html",
    ],
  );
  for (const token of [
    '"状态 · R0.72L 定理完成": "Status · R0.72L theorem complete"',
    '"strong coupling 应由 common-band exposure scale 定义": "Strong coupling is defined by the common-band exposure scale"',
    '"01 · 二十八个研究阶段": "01 · Twenty-eight research phases"',
  ]) {
    assert.ok(built.includes(token), token);
  }
});

test("keeps every R0.72L inline formula and formal-figure link intact", async () => {
  const pages = await Promise.all(
    [
      "research-review.html",
      "literature-review.html",
      "notes/r0-72l.html",
      "recap-r0-61-r0-72l.html",
    ].map((name) => readFile(resolve(publicRoot, name), "utf8")),
  );
  for (const page of pages) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.25"/);
    assert.doesNotMatch(page, /\(varepsilon|\(mathcal|\(Theta|\(tau|\(Omega|\(1lesssim/);
  }

  const [note, recap, home] = pages.slice(2).concat(pages[0]);
  for (const token of [
    "\\(\\varepsilon=gB/R^2&gt;0\\)",
    "\\(K=\\mathcal R_Y\\)",
    "\\(x=\\Theta Q_*\\)",
    "\\(\\tau=c_*/(R^2+gB)\\)",
    "\\(x\\ge Z\\)",
    "\\(1\\lesssim\\varepsilon\\lesssim p^{2/3}R^{2/3}(1+\\log R)\\)",
  ]) {
    assert.ok(home.includes(token), token);
  }
  assert.ok(note.includes("\\varepsilon=o(p^{2/3}R^{2/3}(1+\\log R))"));
  assert.ok(recap.includes("\\varepsilon^{7/3}p^{4/3}"));

  for (const extension of ["pdf", "png", "svg"]) {
    const relative = `/assets/r072l/fig-r072l-strong-window.${extension}`;
    assert.ok(note.includes(relative), relative);
    const asset = await readFile(
      resolve(publicRoot, `assets/r072l/fig-r072l-strong-window.${extension}`),
    );
    assert.ok(asset.length > 1_000, extension);
  }
  assert.ok(recap.includes("/assets/r072l/fig-r072l-strong-window.pdf"));
  assert.ok(home.includes("/assets/r072l/fig-r072l-strong-window.pdf"));
  for (const page of [note, recap, home]) {
    assert.doesNotMatch(page, /\/figures\/r0-72l-strong-window/);
  }
});

test("the L table of contents names only existing section anchors", async () => {
  const note = await readFile(resolve(publicRoot, "notes/r0-72l.html"), "utf8");
  const tocStart = note.indexOf('<aside class="toc">');
  const tocEnd = note.indexOf("</aside>", tocStart);
  assert.ok(tocStart >= 0 && tocEnd > tocStart);
  const toc = note.slice(tocStart, tocEnd);
  const anchors = [...toc.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.deepEqual(anchors, [
    "result",
    "parameter",
    "ledger",
    "physical",
    "floor",
    "window",
    "galerkin",
    "multiscale",
    "audit",
    "figure",
    "value",
    "next",
    "claims",
    "reproduce",
  ]);
  for (const anchor of anchors) {
    assert.ok(note.includes(`id="${anchor}"`), anchor);
  }
});

test("the deterministic generator starts from K and targets L exactly", async () => {
  const generator = await readFile(
    resolve(root, "scripts/generate_r072l_release.py"),
    "utf8",
  );
  assert.match(generator, /r0-72k\.html/);
  assert.match(generator, /recap-r0-61-r0-72k\.html/);
  assert.match(generator, /r0-72l\.html/);
  assert.match(generator, /recap-r0-61-r0-72l\.html/);
  assert.match(generator, /expected 162 public HTML notes/);
  assert.match(generator, /"recapNodes": 102/);
  assert.match(generator, /"phases": 28/);
  assert.match(generator, /"next": "R0\.72M"/);
});
