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
const certificateRoot = new URL("research/certificates/r071y/", root);
const figureRoot = new URL(
  "figures/r071y-growing-root-suppression/fig-r071y-operator-sampling/",
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
    readFile(new URL("notes/r0-71y.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71y.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("retains R0.71Y while v1.16 publishes R0.72C as current", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 153);
  assert.match(home, /<strong>v1\.16<\/strong>网页版本/);
  assert.match(home, /<strong>153<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72C<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72C<\/span>/);
  assert.match(home, /展开 63 篇公开笔记/);
  assert.match(home, /href="#r070a">R0\.70A–R0\.72C 已公开并封存版本<\/a>/);
  assert.match(home, /累计回顾收录 93 个节点；全站现有 153 篇公开研究笔记/);
  assert.match(home, /R0\.70A–R0\.72C 共 55 个已公开并封存版本/);
  assert.match(home, /NEXT · R0\.72D/);
  assert.equal(count(home, 'data-release="r071y"'), 1);
  assert.equal(count(home, 'href="/notes/r0-71y.html"'), 2);

  const route = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72C">([\s\S]*?)<\/nav>/,
  );
  assert.ok(route);
  assert.equal(count(route[1], 'href="/notes/'), 63);
  assert.equal(count(route[1], 'href="/notes/r0-71y.html"'), 1);

  assert.equal(count(recap, '<article class="phase">'), 17);
  assert.match(recap, /R0\.60 之后的路线分成十七段/);
  assert.match(recap, /R0\.71U–R0\.71Y/);
  assert.match(recap, /收录节点：89/);
  assert.match(recap, /回顾截止时公开笔记：149/);
  assert.match(recap, /R0\.70A–R0\.71Y 完成版本/);
  const index =
    recap.match(/<div class="node-index-grid">([\s\S]*?)<\/div>/)?.[1] ?? "";
  assert.equal(count(index, 'href="/notes/'), 89);
  assert.equal(count(index, 'href="/notes/r0-71y.html"'), 1);

  assert.match(literature, /R0\.69P–R0\.72C/);
  assert.match(literature, /<header><b>R0\.72A<\/b>/);
  assert.match(literature, /开放接口 · R0\.72D/);
  for (const letter of "abcdefghijklmnopqrstuvwxyz") {
    assert.ok(literature.includes('href="/notes/r0-70' + letter + '.html"'));
  }
  for (const letter of "abcdefghijklmnopqrstuvwxyz") {
    assert.ok(literature.includes('href="/notes/r0-71' + letter + '.html"'));
  }

  for (const [page, minimum, version] of [
    [home, 10, "1.16"],
    [note, 16, "1.11"],
    [recap, 8, "1.11"],
    [literature, 50, "1.16"],
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

test("states the selected-root theorem, R0.71X correction, and open boundaries precisely", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "M=2N+1",
    "单位模 carrier phases",
    "实 shear",
    "matched background",
    "\\ell^2",
    "根坐标的 heat term 消失",
    "G_N^{\\rm ex}\\le NM\\Omega_N^2",
    "\\mathcal J_N^{\\rm sel}",
    "C\\nu^{-2}\\frac{\\delta_{\\rm obs,N}^{4/3}}N",
    "\\delta_{\\rm obs,N}\\gtrsim N^{3/4}",
    "R\\gtrsim M^2",
    "heat weighted",
    "没有统一的 unweighted",
    "\\eta_{\\rm Dyson,N}",
    "inverse Jacobian",
    "A_{0,N}\\to0",
    "all-root count",
    "floor-free",
    "strong coupling",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(note, /selected exact roots/is);
  assert.match(note, /不是全部 nonlinear roots/is);
  assert.match(note, /不能把这个条件结论写成 complete all-root theorem/is);
  assert.match(note, /不是 DNS，也不构造 growing exact-root family/is);
  assert.match(note, /不是 true nonlinear IFT branch radius 的上界/is);
  assert.match(note, /没有得到：.*universal endpoint.*继续性判据.*有限时奇性.*global regularity/is);
  assert.match(home, /bounded observation coupling.*selected growing-root endpoint ratio/is);
  assert.match(recap, /不是 complete all-root no-go/is);
  assert.match(literature, /相邻框架，不推出本节的 BV 引理/is);

  for (const doi of [
    "10.1007/BF01398878",
    "10.3934/dcdss.2020082",
    "10.1137/S0895479803438225",
  ]) {
    assert.ok(note.includes(doi), doi);
    assert.ok(literature.includes(doi), doi);
  }

  assert.match(note, /1\.806 增至.*49\.029/);
  assert.doesNotMatch(note, /1\.806 墁到/);
});

test("verifies all 13/13 producer and 12/12 independent audit checks", async () => {
  const [producer, independent, report, gap, literatureAudit, independentAudit] =
    await Promise.all([
      readFile(new URL("result.json", certificateRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-result.json", certificateRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("research/r071y_report-source.md", root), "utf8"),
      readFile(new URL("research/r071y_gap_matrix.md", root), "utf8"),
      readFile(new URL("research/r071y_literature_audit.md", root), "utf8"),
      readFile(new URL("research/r071y_independent_audit.md", root), "utf8"),
    ]);

  assert.equal(producer.release, "R0.71Y");
  assert.equal(producer.status, "passed");
  assert.equal(producer.checks.length, 13);
  assert.ok(producer.checks.every((entry) => entry.passed));
  assert.equal(independent.release, "R0.71Y");
  assert.equal(independent.status, "passed");
  assert.equal(independent.checks.length, 12);
  assert.ok(independent.checks.every((entry) => entry.passed));

  assert.ok(Math.abs(producer.latticeTailPower + 1) < 0.002);
  assert.ok(
    Math.abs(producer.separatedRootEnvelope.fixedGapTailPower + 2) < 0.002,
  );
  assert.ok(
    Math.abs(producer.separatedRootEnvelope.quasiuniformGapTailPower + 1) <
      0.002,
  );
  assert.ok(Math.abs(producer.criticalCoupling.tailPower) < 0.002);
  assert.ok(Math.abs(producer.subcriticalCoupling.tailPower + 1 / 3) < 0.002);
  assert.ok(producer.equalGridInverseLower.at(-1).log10InverseLower > 40);

  assert.match(report, /selected.*exact roots/is);
  assert.match(report, /does not prove.*all-root count/is);
  assert.match(report, /does not prove.*universal/is);
  assert.match(gap, /Y17/);
  assert.match(literatureAudit, /bounded primary-source literature audit/i);
  assert.match(independentAudit, /13 of 13/);
  assert.match(independentAudit, /12 of 12/);
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
    readFile(new URL("figures/r0-71y-operator-sampling.svg", publicRoot)),
    readFile(new URL("figures/r0-71y-operator-sampling.pdf", publicRoot)),
    readFile(new URL("figures/r0-71y-operator-sampling.png", publicRoot)),
    readFile(new URL("figure.svg", figureRoot)),
    readFile(new URL("figure.pdf", figureRoot)),
    readFile(new URL("figure.png", figureRoot)),
  ]);

  assert.equal(validation.status, "passed");
  assert.equal(validation.checkCount, 24);
  assert.equal(validation.passedCheckCount, 24);
  assert.ok(validation.checks.every((entry) => entry.passed));
  assert.equal(manifest.computation.completeAllRootCount, false);
  assert.equal(manifest.computation.exactGrowingRootConstruction, false);
  assert.equal(manifest.computation.quantitativeIftRadiusUpperBound, false);
  assert.equal(manifest.computation.dns, false);
  assert.equal(manifest.computation.universalEndpointTheorem, false);
  assert.equal(manifest.computation.navierStokesRegularityResult, false);
  assert.equal(manifest.computation.monitoring.enabled, true);
  assert.match(manifest.claimBoundary, /do not construct growing exact roots/i);
  assert.match(manifest.claimBoundary, /not DNS/i);

  assert.match(publicSvg.toString("utf8"), /<svg/);
  assert.equal(publicPdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(publicPng.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(sha256(publicSvg), sha256(sourceSvg));
  assert.equal(sha256(publicPdf), sha256(sourcePdf));
  assert.equal(sha256(publicPng), sha256(sourcePng));
});

test("ships complete TeX-safe neutral-voice English translations for every public page", async () => {
  const [translations, generated, source, updater] = await Promise.all([
    readFile(new URL("translations/en.json", root), "utf8").then(JSON.parse),
    readFile(new URL("i18n-en.js", publicRoot), "utf8"),
    collectSiteStrings(fileURLToPath(publicRoot)),
    readFile(new URL("scripts/add-r071y-translations.mjs", root), "utf8"),
  ]);
  const batch = translations.filter((entry) => /^r071y\d+$/.test(entry.id));
  const sourceByChinese = new Map(source.map((entry) => [entry.zh, entry]));

  assert.equal(batch.length, 148);
  assert.equal(new Set(batch.map((entry) => entry.zh)).size, batch.length);
  assert.deepEqual(
    batch.map((entry) => entry.id),
    Array.from(
      { length: 148 },
      (_, index) => "r071y" + String(index + 1).padStart(3, "0"),
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

  assert.match(updater, /R0\.71Y translation source drift/);
  assert.match(updater, /protected-token mismatch/);
  assert.match(updater, /first-person plural voice/);
  assert.match(updater, /missing\.length !== 148/);
});
