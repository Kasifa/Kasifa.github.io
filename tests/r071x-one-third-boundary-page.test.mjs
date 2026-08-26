import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificateRoot = new URL("research/certificates/r071x/", root);
const figureRoot = new URL(
  "figures/r071x-one-third-boundary/fig-r071x-endpoint-saturation/",
  root,
);

function count(value, fragment) {
  return value.split(fragment).length - 1;
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function assertAnchorsResolve(html, minimumUniqueTargets) {
  const idList = [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]);
  const ids = new Set(idList);
  assert.equal(ids.size, idList.length, "duplicate HTML id");
  const targets = [...html.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.ok(new Set(targets).size >= minimumUniqueTargets);
  for (const target of targets) assert.ok(ids.has(target), target);
}

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71x.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71x.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("retains R0.71X while v1.11 publishes R0.71Y as current", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 149);
  assert.match(home, /<strong>v1\.11<\/strong>网页版本/);
  assert.match(home, /<strong>149<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.71Y<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.71Y<\/span>/);
  assert.match(home, /展开 59 篇公开笔记/);
  assert.match(home, /href="#r070a">R0\.70A–R0\.71Y 完成版本<\/a>/);
  assert.match(home, /累计回顾收录 89 个节点；全站现有 149 篇公开研究笔记/);
  assert.match(home, /R0\.70A–R0\.71Y 共 51 个完成版本/);
  assert.match(home, /NEXT · R0\.71Z/);
  assert.equal(count(home, 'data-release="r071x"'), 1);
  assert.equal(count(home, 'href="/notes/r0-71x.html"'), 2);

  const route = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.71Y">([\s\S]*?)<\/nav>/,
  );
  assert.ok(route);
  assert.equal(count(route[1], 'href="/notes/'), 59);
  assert.equal(count(route[1], 'href="/notes/r0-71x.html"'), 1);

  assert.equal(count(recap, '<article class="phase">'), 17);
  assert.match(recap, /R0\.60 之后的路线分成十七段/);
  assert.match(recap, /R0\.71U–R0\.71X/);
  assert.match(recap, /收录节点：88/);
  assert.match(recap, /回顾截止时公开笔记：148/);
  assert.match(recap, /R0\.70A–R0\.71X 完成版本/);
  const index = recap.match(/<div class="node-index-grid">([\s\S]*?)<\/div>/)?.[1] ?? "";
  assert.equal(count(index, 'href="/notes/'), 88);
  assert.equal(count(index, 'href="/notes/r0-71x.html"'), 1);

  assert.match(literature, /R0\.69P–R0\.71Y/);
  assert.match(literature, /<header><b>R0\.71X<\/b>/);
  assert.match(literature, /开放接口 · R0\.71Z/);
  for (const letter of "abcdefghijklmnopqrstuvwxyz") {
    assert.ok(literature.includes('href="/notes/r0-70' + letter + '.html"'));
  }
  for (const letter of "abcdefghijklmnopqrstuvwxy") {
    assert.ok(literature.includes('href="/notes/r0-71' + letter + '.html"'));
  }

  for (const [page, minimum, version] of [
    [home, 10, "1.11"],
    [note, 15, "1.10"],
    [recap, 8, "1.10"],
    [literature, 50, "1.11"],
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

test("states the fixed-small-coupling endpoint theorem and every open boundary precisely", async () => {
  const { home, note, recap } = await publishedPages();
  const literatureAudit = await readFile(
    new URL("research/r071x_literature_audit.md", root),
    "utf8",
  );

  for (const token of [
    "从 launch time 向前全局光滑",
    "\\mathscr A_{q,\\delta}=\\delta q^2",
    "D_{q,\\delta}\\asymp\\delta^2q^6",
    "\\mathcal J_{q,\\delta}\\asymp\\delta^2q^2",
    "\\nu^2\\le\\Lambda_1",
    "\\asymp\\delta^{4/3}",
    "\\beta&lt;1/3",
    "\\beta=1/3",
    "\\beta&gt;1/3",
    "ECT 零点预算",
    "固定紧区间上有 \\(\\|H_{q,\\delta}-\\Gamma\\|_{C^1}",
    "积分因子",
    "\\Gamma_\\infty\\ne0",
    "\\varepsilon_N",
    "\\delta_{\\mathrm{op},N}",
    "atomProxy",
    "\\delta=1/128",
    "growing \\(N(q)\\)",
    "R0.71Y",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /完整实时间 target 根集/is);
  assert.match(note, /fixed-dimensional local-IFT triangular family/is);
  assert.match(note, /不是对全部 triangular solutions/is);
  assert.match(note, /不是 universal endpoint|不证明.*universal endpoint/is);
  assert.match(note, /strong-coupling Bessel.*后续候选/is);
  assert.doesNotMatch(note, /delta 的四分之三次方/);
  assert.match(note, /delta 的三分之四次方/);

  assert.match(home, /declared-family internal saturation/is);
  assert.match(recap, /energy proxy.*不等于精确 operator IFT parameter/is);
  assert.match(recap, /strong-coupling Bessel 路线保留为后续候选/is);
  assert.match(literatureAudit, /Non-collision boundary for R0\.71X/is);
  assert.match(recap, /不是 universal endpoint 或正则性定理/is);

  for (const doi of [
    "10.1088/1361-6544/ab9246",
    "10.1512/iumj.2008.57.3716",
    "10.1017/jfm.2017.136",
    "10.1017/jfm.2020.204",
    "10.4208/cmr.2021-0106",
    "10.1080/03605308108820180",
    "10.1007/BF02096982",
    "10.1016/j.jde.2025.113486",
    "10.1016/j.jmaa.2022.126428",
  ]) {
    assert.ok(note.includes(doi), doi);
    assert.ok(literatureAudit.includes(doi), doi);
  }
});

test("verifies the 9/9, 8/8, and 10/10 audit layers", async () => {
  const [exact, independent, truncated, report, gap, literatureAudit, independentAudit] =
    await Promise.all([
      readFile(new URL("result.json", certificateRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-result.json", certificateRoot), "utf8").then(JSON.parse),
      readFile(new URL("truncated-coset-result.json", certificateRoot), "utf8").then(JSON.parse),
      readFile(new URL("research/r071x_report-source.md", root), "utf8"),
      readFile(new URL("research/r071x_gap_matrix.md", root), "utf8"),
      readFile(new URL("research/r071x_literature_audit.md", root), "utf8"),
      readFile(new URL("research/r071x_independent_audit.md", root), "utf8"),
    ]);

  assert.equal(exact.status, "passed");
  assert.equal(exact.checks.length, 9);
  assert.ok(exact.checks.every((entry) => entry.passed));
  assert.equal(independent.release, "R0.71X");
  assert.equal(independent.status, "passed");
  assert.equal(independent.checks.length, 8);
  assert.ok(independent.checks.every((entry) => entry.passed));
  assert.equal(truncated.status, "passed");
  assert.equal(truncated.checks.length, 10);
  assert.ok(truncated.checks.every((entry) => entry.passed));

  assert.ok(Math.abs(exact.fittedQPowers.dataSize - 6) < 0.02);
  assert.ok(Math.abs(exact.fittedQPowers.atomSum - 2) < 0.02);
  assert.ok(Math.abs(exact.fittedQPowers.atomOverDataOneThird) < 0.02);
  assert.ok(Math.abs(exact.deltaCollapse.fittedPower - 4 / 3) < 0.002);
  assert.deepEqual(
    exact.betaTrichotomy.map((entry) => entry.classification),
    ["diverges", "diverges", "diverges", "saturates", "vanishes", "vanishes"],
  );

  assert.match(report, /global forward from the launch time/i);
  assert.match(report, /No-spurious-root route/i);
  assert.match(report, /complete target-root set/i);
  assert.match(report, /proves no universal\s+\\\(D\^\{1\/3\}\\\) payment/i);
  assert.match(gap, /energy proxy, not the operator parameter/i);
  assert.match(literatureAudit, /bounded primary-source|bounded search/i);
  assert.match(independentAudit, /independent/i);
  assert.doesNotMatch(report, /we prove global regularity/i);
});

test("ships the monitored journal figure package and byte-identical public mirrors", async () => {
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

  const [manifest, validation, publicSvg, publicPdf, publicPng, sourceSvg, sourcePdf, sourcePng] =
    await Promise.all([
      readFile(new URL("manifest.json", figureRoot), "utf8").then(JSON.parse),
      readFile(new URL("validation.json", figureRoot), "utf8").then(JSON.parse),
      readFile(new URL("figures/r0-71x-endpoint-saturation.svg", publicRoot)),
      readFile(new URL("figures/r0-71x-endpoint-saturation.pdf", publicRoot)),
      readFile(new URL("figures/r0-71x-endpoint-saturation.png", publicRoot)),
      readFile(new URL("figure.svg", figureRoot)),
      readFile(new URL("figure.pdf", figureRoot)),
      readFile(new URL("figure.png", figureRoot)),
    ]);

  assert.equal(validation.status, "passed");
  assert.equal(validation.checkCount, 23);
  assert.equal(validation.passedCheckCount, 23);
  assert.ok(validation.checks.every((entry) => entry.passed));
  assert.equal(manifest.computation.actualMultiplierLockedJStar, false);
  assert.equal(manifest.computation.continuumIftRadiusCertifiedAtFixedDelta, false);
  assert.equal(manifest.computation.dns, false);
  assert.equal(manifest.computation.monitoring.enabled, true);
  assert.match(manifest.claimBoundary, /atomProxy is not the multiplier-locked J_\*/);
  assert.match(manifest.claimBoundary, /delta=1\/128 has not been proved/);

  assert.match(publicSvg.toString("utf8"), /<svg/);
  assert.equal(publicPdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(publicPng.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(sha256(publicSvg), sha256(sourceSvg));
  assert.equal(sha256(publicPdf), sha256(sourcePdf));
  assert.equal(sha256(publicPng), sha256(sourcePng));
});
