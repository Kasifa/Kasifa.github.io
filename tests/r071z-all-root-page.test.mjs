import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import test from "node:test";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "../scripts/i18n-lib.mjs";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const figureRoot = new URL(
  "figures/r071z-all-root-floorfree/fig-r071z-all-root/",
  root,
);

function count(value, fragment) {
  return value.split(fragment).length - 1;
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function assertAnchorsResolve(html, minimumUniqueTargets) {
  const idList = [...html.matchAll(/\sid="([^"]+)"/g)].map(
    (match) => match[1],
  );
  const ids = new Set(idList);
  assert.equal(ids.size, idList.length, "duplicate HTML id");
  const targets = [...html.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(new Set(targets).size >= minimumUniqueTargets);
  for (const target of targets) assert.ok(ids.has(target), target);
}

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71z.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71z.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("retains R0.71Z while v1.21 publishes R0.72H with synchronized counts and route", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 158);
  assert.match(home, /<strong>v1\.21<\/strong>网页版本/);
  assert.match(home, /<strong>158<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72H<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72H<\/span>/);
  assert.match(home, /展开 68 篇公开笔记/);
  assert.match(home, /R0\.70A–R0\.72H 共 60 个版本已公开；36 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单/);
  assert.match(home, /累计回顾收录 98 个节点；全站现有 158 篇公开研究笔记/);
  assert.match(home, /NEXT · R0\.72I/);
  assert.equal(count(home, 'data-release="r071z"'), 1);
  assert.equal(count(home, 'href="/notes/r0-71z.html"'), 2);

  const route = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72H">([\s\S]*?)<\/nav>/,
  );
  assert.ok(route);
  assert.equal(count(route[1], 'href="/notes/'), 68);
  assert.equal(count(route[1], 'href="/notes/r0-71z.html"'), 1);

  assert.equal(count(recap, '<article class="phase">'), 17);
  assert.match(recap, /R0\.71U–R0\.71Z/);
  assert.match(recap, /收录节点：90/);
  assert.match(recap, /回顾截止时公开笔记：150/);
  assert.match(recap, /R0\.70A–R0\.71Z 完成版本/);
  const index =
    recap.match(/<div class="node-index-grid">([\s\S]*?)<\/div>/)?.[1] ?? "";
  assert.equal(count(index, 'href="/notes/'), 90);
  assert.equal(count(index, 'href="/notes/r0-71z.html"'), 1);

  assert.match(literature, /R0\.69P–R0\.72H/);
  assert.match(literature, /<header><b>R0\.72A<\/b>/);
  assert.match(literature, /开放接口 · R0\.72I/);
  for (const letter of "abcdefghijklmnopqrstuvwxyz") {
    assert.ok(literature.includes('href="/notes/r0-70' + letter + '.html"'));
    assert.ok(literature.includes('href="/notes/r0-71' + letter + '.html"'));
  }

  for (const [page, minimum, version] of [
    [home, 10, "1.21"],
    [note, 15, "1.12"],
    [recap, 8, "1.12"],
    [literature, 50, "1.21"],
  ]) {
    assertAnchorsResolve(page, minimum);
    assert.ok(page.includes('src="/i18n-en.js?v=' + version + '"'));
    assert.doesNotMatch(
      page,
      /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
    );
    assert.doesNotMatch(page, /千禧年问题已经解决|解决了千禧年问题/);
  }
});

test("states the all-root theorem and every mandatory boundary precisely", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "W^{2,1}",
    "\\sum_m|g'(\\tau_m)|^2",
    "C_\\kappa=\\frac{\\pi^2}{\\sqrt{45}\\nu d^2}",
    "G_{\\rm all}^{\\rm ex}",
    "不需要先证明 zero-count theorem",
    "launch",
    "\\mathcal R_Y",
    "\\sup_KY",
    "\\theta_I^{-1}",
    "e^{-2\\nu d^2R^2A_0}",
    "M^{-2}",
    "M^{6/7}",
    "strong coupling",
    "shrinking observation layer",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(note, /complete all-root upper bound/is);
  assert.match(note, /不是 general 3D NSE endpoint/is);
  assert.match(note, /不是 DNS，也不构造 growing-dimensional exact-root family/is);
  assert.match(note, /不构成原创性、优先权或不存在性声明/is);
  assert.match(note, /只覆盖 exact triangular 2\.5D class/is);
  assert.match(note, /没有得到：.*raw zero-count theorem.*继续性判据.*有限时奇性.*global regularity/is);
  assert.match(home, /complete all-root、mixed-window floor-free upper bound/is);
  assert.match(recap, /一般 NSE 的 complete atom theorem/is);
  assert.match(literature, /相邻框架，不推出本节的 BV 引理/is);

  for (const doi of [
    "10.1090/S0025-5718-04-01708-9",
    "10.1016/0022-1236(85)90050-3",
    "10.1007/s00365-008-9010-6",
    "10.1090/S0002-9947-1953-0054167-3",
    "10.3792/pja/1195521421",
    "10.1016/j.physd.2008.03.007",
  ]) {
    assert.ok(note.includes(doi), doi);
    assert.ok(literature.includes(doi), doi);
  }
});

test("ships the validated journal figure package and byte-identical public mirrors", async () => {
  await Promise.all(
    [
      "README.md",
      "caption.md",
      "config.json",
      "contract.json",
      "data.csv",
      "data.json",
      "figure.pdf",
      "figure.png",
      "figure.svg",
      "manifest.json",
      "progress.ndjson",
      "resource-log.ndjson",
      "validation.json",
    ].map((path) => access(new URL(path, figureRoot))),
  );

  const [
    manifest,
    validation,
    publicSvg,
    publicPdf,
    publicPng,
    sourceSvg,
    sourcePdf,
    sourcePng,
  ] = await Promise.all([
    readFile(new URL("manifest.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("validation.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("figures/r0-71z-all-root.svg", publicRoot)),
    readFile(new URL("figures/r0-71z-all-root.pdf", publicRoot)),
    readFile(new URL("figures/r0-71z-all-root.png", publicRoot)),
    readFile(new URL("figure.svg", figureRoot)),
    readFile(new URL("figure.pdf", figureRoot)),
    readFile(new URL("figure.png", figureRoot)),
  ]);

  assert.equal(validation.status, "passed");
  assert.equal(
    validation.checks.filter((entry) => entry.passed).length,
    validation.checkCount,
  );
  assert.ok(validation.checks.every((entry) => entry.passed));
  assert.equal(
    manifest.git.sourceCommit,
    "98e1ea3018091565a87b755e6c2a41f9373fb024",
  );
  assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  assert.equal(manifest.computation.dns, false);
  assert.equal(manifest.computation.navierStokesRegularityResult, false);
  assert.equal(manifest.computation.monitoring.enabled, true);
  assert.match(manifest.claimBoundary, /no PDE time stepping or DNS/i);

  assert.match(publicSvg.toString("utf8"), /<svg/);
  assert.equal(publicPdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(publicPng.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(sha256(publicSvg), sha256(sourceSvg));
  assert.equal(sha256(publicPdf), sha256(sourcePdf));
  assert.equal(sha256(publicPng), sha256(sourcePng));
});

test("ships TeX-safe neutral-voice English translations for every public page", async () => {
  const [translations, generated, source, updater] = await Promise.all([
    readFile(new URL("translations/en.json", root), "utf8").then(JSON.parse),
    readFile(new URL("i18n-en.js", publicRoot), "utf8"),
    collectSiteStrings(fileURLToPath(publicRoot)),
    readFile(new URL("scripts/add-r071z-translations.mjs", root), "utf8"),
  ]);
  const batch = translations.filter((entry) => /^r071z\d+$/.test(entry.id));
  const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));

  assert.equal(batch.length, 139);
  assert.equal(new Set(batch.map((entry) => entry.zh)).size, batch.length);
  assert.deepEqual(
    batch.map((entry) => entry.id),
    Array.from(
      { length: batch.length },
      (_, index) => "r071z" + String(index + 1).padStart(3, "0"),
    ),
  );
  for (const entry of batch) {
    assert.ok(entry.en.trim(), entry.id);
    assert.ok(!containsChinese(entry.en), entry.id);
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|us)\b/i, entry.id);
    assert.deepEqual(
      extractProtectedTokens(entry.en),
      extractProtectedTokens(entry.zh),
      entry.id,
    );
  }

  const dictionaryMatch = generated.match(
    /globalThis\.NS_EN_TRANSLATIONS = Object\.freeze\((\{[\s\S]*\})\);/,
  );
  assert.ok(dictionaryMatch);
  const dictionary = JSON.parse(dictionaryMatch[1]);
  assert.equal(Object.keys(dictionary).length, source.length);
  for (const entry of source) assert.equal(dictionary[entry.zh]?.trim().length > 0, true);
  for (const entry of batch.filter((entry) => sourceByChinese.has(entry.zh))) {
    assert.equal(dictionary[entry.zh], entry.en);
  }

  assert.match(updater, /R0\.71Z translation source drift/);
  assert.match(updater, /protected-token mismatch/);
  assert.match(updater, /first-person plural voice/);
});

test("ships synchronized PDF copies", async () => {
  const [notePdf, recapPdf] = await Promise.all([
    readFile(new URL("notes/r0-71z.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71z.pdf", publicRoot)),
  ]);
  assert.equal(notePdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(recapPdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.ok(notePdf.length > 50_000);
  assert.ok(recapPdf.length > 100_000);
});
