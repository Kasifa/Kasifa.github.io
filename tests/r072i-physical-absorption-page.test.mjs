import assert from "node:assert/strict";
import { access, readdir, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");

async function readJson(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

function visibleText(html) {
  return html
    .replace(/<style\b[\s\S]*?<\/style>/gi, " ")
    .replace(/<script\b[\s\S]*?<\/script>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/\s+/g, " ")
    .trim();
}

function parseCompiledTranslations(source) {
  const match = source.match(/Object\.freeze\(([\s\S]+)\);\s*$/);
  assert.ok(match, "compiled i18n dictionary");
  return JSON.parse(match[1]);
}

async function assertLocalLinksResolve(html) {
  const links = [...html.matchAll(/href="(\/[^"]*)"/g)].map(
    (match) => match[1],
  );
  assert.ok(links.length > 0);
  for (const href of new Set(links)) {
    const pathname = href.split(/[?#]/, 1)[0];
    if (pathname === "/") continue;
    await access(resolve(publicRoot, pathname.slice(1)));
  }
}

test("publishes the R0.72I distinction, dual audit, figure, and PDFs", async () => {
  const [home, note, recap, literature, notePdf, recapPdf] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72i.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72i.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72i.pdf")),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72i.pdf")),
  ]);

  assert.match(note, /研究笔记 R0\.72I/);
  assert.match(note, /一个上界不能吸收[\s\S]{0,80}不等于真实账本很大/);
  assert.match(note, /FALSE · TERM-BY-TERM ABSORPTION/);
  assert.match(note, /TRUE · ACTUAL ALL-ODD LEDGER DECAYS/);
  assert.ok(note.includes(String.raw`M^{1/2}\log M\longrightarrow\infty`));
  assert.ok(note.includes(String.raw`M^{-4/9}(\log M)^{-2/3}\longrightarrow0`));
  assert.ok(note.includes(String.raw`\mathcal J_{\rm all}`));
  assert.match(note, /这不是物理反例|没有推翻物理 critical-log 候选/);
  assert.match(note, /joint exposure/i);
  assert.match(note, /奇偶格点分裂|奇偶分裂|parity/);

  assert.match(note, /PRODUCER · ARCHIVED PASS/);
  assert.match(note, /INDEPENDENT · ARCHIVED PASS/);
  assert.match(note, /8\.69826/);
  assert.match(note, /0\.00356315/);
  assert.match(note, /57\.3302314/);
  assert.match(note, /0\.1646408965/);
  assert.match(note, /1\.61\s*\\times10\^\{-4\}/);
  assert.match(note, /research\/certificates\/r072i/);
  for (const extension of ["pdf", "png", "svg"]) {
    assert.match(
      note,
      new RegExp(`/figures/r0-72i-physical-absorption\\.${extension}`),
    );
  }
  assert.match(note, /R0\.72J/);
  assert.match(note, /mixed-parity|混合奇偶|混合 parity/i);
  assert.match(note, /不是千禧年问题|千禧年问题解答|一般三维正则性：OPEN/);
  assert.doesNotMatch(note, /千禧年问题(?:已经|已被|得到)(?:解决|证明)/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);

  assert.match(literature, /id="r072i-boundary"/);
  assert.match(literature, /href="\/notes\/r0-72i\.html"/);
  assert.match(literature, /R0\.72J 完成 gcd-reduced Cayley graph 的二分分类/);
  assert.match(literature, /开放接口 · R0\.72O/);
  assert.match(literature, /bounded non-collision check/i);
  assert.match(literature, /R0\.69P–R0\.72N/);

  for (const [label, pdf] of Object.entries({ notePdf, recapPdf })) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label);
    assert.ok(pdf.length > 10_000, label);
  }
  for (const page of [note, recap]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.22"/);
  }
  for (const page of [home, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.27"/);
  }
  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(
      visibleText(page),
      /RELEASE PLACEHOLDER|附图占位|累计回顾占位|正式附图归档占位/i,
    );
  }
  await Promise.all([assertLocalLinksResolve(note), assertLocalLinksResolve(recap)]);
});

test("recaps every post-R0.60 node through R0.72I in 25 phases", async () => {
  const recap = await readFile(
    resolve(publicRoot, "recap-r0-61-r0-72i.html"),
    "utf8",
  );

  assert.match(recap, /R0\.60 之后的研究回顾/);
  assert.match(recap, /R0\.61–R0\.72I 的 99 节公开笔记/);
  assert.match(recap, /回顾截止时公开笔记：159/);
  assert.match(recap, /61<\/strong><span>R0\.70A–R0\.72I 已公开版本/);
  assert.match(recap, /37<\/strong><span>当前 formal-figure 合同下完整封存/);
  assert.match(recap, /24<\/strong><span>旧版 formal-figure 档案待回补/);
  assert.match(recap, /25<\/strong><span>按问题划分的研究阶段/);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 25);

  for (const routeToken of [
    "R0.61–R0.66",
    "R0.69P–R0.69W",
    "R0.70A–R0.70I",
    "R0.71A–R0.71D",
    "R0.71U–R0.71Z",
    "R0.72A",
    "R0.72F",
    "R0.72G",
    "R0.72H",
    "R0.72I",
  ]) {
    assert.ok(recap.includes(routeToken), routeToken);
  }
  assert.match(recap, /termwise physical absorption|逐项物理吸收|正项吸收/i);
  assert.match(recap, /odd-carrier parity|全奇载波|奇偶分裂/i);
  assert.match(recap, /真实 complete ledger|真实完整账本/i);
  assert.match(recap, /问题状态：仍未解决/);
  assert.match(recap, /R0\.72J/);
  assert.match(recap, /mixed-parity|混合奇偶|混合 parity/i);

  const nodeIndexStart = recap.indexOf('<section id="node-index">');
  const nodeIndexEnd = recap.indexOf("</section>", nodeIndexStart);
  assert.ok(nodeIndexStart >= 0 && nodeIndexEnd > nodeIndexStart);
  assert.equal(
    (
      recap
        .slice(nodeIndexStart, nodeIndexEnd)
        .match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []
    ).length,
    99,
  );
  assert.match(recap, /href="\/recap-r0-60\.html"/);
  assert.match(recap, /href="\/notes\/r0-72i\.html"/);
  assert.match(recap, /href="\/recap-r0-61-r0-72h\.html"/);
  assert.doesNotMatch(recap, /千禧年问题(?:已经|已被|得到)(?:解决|证明)/);
});

test("retains R0.72I while synchronizing v1.27, latest N, and next O", async () => {
  const [home, releaseManifest, archive, siteVersion, noteFiles] =
    await Promise.all([
      readFile(resolve(publicRoot, "research-review.html"), "utf8"),
      readJson(resolve(root, "research/release-manifest.json")),
      readJson(resolve(root, "research/formal-archive-inventory.json")),
      readJson(resolve(publicRoot, "site-version.json")),
      readdir(resolve(publicRoot, "notes")),
    ]);

  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 164);
  assert.match(home, /<html lang="zh-CN" data-site-version="1\.27">/);
  assert.match(home, /<strong>v1\.27<\/strong>网页版本/);
  assert.match(home, /<strong>164<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72N<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72N<\/span>/);
  assert.match(home, /展开 74 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72O/);
  assert.match(home, /累计回顾收录 104 个节点；全站现有 164 篇公开研究笔记/);
  assert.match(home, /66 个版本已公开/);
  assert.match(home, /42 个按当前 formal-figure 合同完整封存|42 个完整封存/);
  assert.match(home, /24 个旧版附图档案仍列入回补清单/);
  assert.equal((home.match(/href="\/notes\/r0-72i\.html"/g) ?? []).length, 2);
  assert.equal((home.match(/data-release="r072i"/g) ?? []).length, 1);
  assert.equal((home.match(/href="\/notes\/r0-72k\.html"/g) ?? []).length, 2);
  assert.equal((home.match(/data-release="r072k"/g) ?? []).length, 1);
  assert.match(home, /recap-r0-61-r0-72n\.html/);

  assert.equal(releaseManifest.latestCompletedRelease, "r072n");
  assert.equal(releaseManifest.siteVersion, "1.27");
  assert.equal(releaseManifest.publicHtmlNoteCount, 164);
  assert.equal(releaseManifest.postR060RecapNodeCount, 104);
  assert.equal(releaseManifest.postR070APublishedReleaseCount, 66);
  assert.equal(releaseManifest.postR070AFormalSealedReleaseCount, 42);
  assert.equal(releaseManifest.legacyFormalFigureBacklogCount, 24);
  assert.equal(releaseManifest.nextRelease, "r072o");
  assert.equal(
    releaseManifest.latestReleaseGate,
    "tests/r072n-dissipative-carrier-gate.test.mjs",
  );

  assert.equal(archive.latestPublishedRelease, "r072n");
  assert.equal(archive.publishedReleaseCount, 66);
  assert.equal(archive.formalSealedReleaseCount, 42);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.ok(archive.publishedReleases.includes("r072i"));
  assert.ok(archive.formalSealedReleases.includes("r072i"));
  assert.ok(archive.publishedReleases.includes("r072k"));
  assert.ok(archive.formalSealedReleases.includes("r072k"));

  assert.equal(siteVersion.version, "1.27");
  assert.equal(siteVersion.latestRelease, "R0.72N");
  assert.equal(siteVersion.publicHtmlNoteCount, 164);
  assert.equal(siteVersion.publishedDate, "2026-08-27");
});

test("leaves zero reader-facing strings missing from the final English build", async () => {
  const [entries, translationRows, compiledSource] = await Promise.all([
    collectSiteStrings(publicRoot),
    readJson(resolve(root, "translations/en.json")),
    readFile(resolve(publicRoot, "i18n-en.js"), "utf8"),
  ]);
  const translationMap = new Map(
    translationRows.map((row) => [row.zh, String(row.en ?? "").trim()]),
  );
  assert.equal(translationMap.size, translationRows.length);
  const compiled = parseCompiledTranslations(compiledSource);
  const missing = entries.filter((entry) => !translationMap.get(entry.zh));
  const compiledMissing = entries.filter((entry) => !compiled[entry.zh]);
  assert.deepEqual(missing, []);
  assert.deepEqual(compiledMissing, []);

  for (const entry of entries) {
    const translated = translationMap.get(entry.zh);
    assert.equal(containsChinese(translated), false, entry.zh);
    assert.deepEqual(
      extractProtectedTokens(translated),
      extractProtectedTokens(entry.zh),
      entry.zh,
    );
    assert.equal(compiled[entry.zh], translated, `compiled cache: ${entry.zh}`);
  }
});
