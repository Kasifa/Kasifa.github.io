import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificateRoot = new URL("research/certificates/r071w/", root);
const figureRoot = new URL(
  "figures/r071w-complete-ledger/fig-r071w-amplitude-doping/",
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
    readFile(new URL("notes/r0-71w.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71w.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("retains R0.71W while v1.14 publishes R0.72A as current", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 151);
  assert.match(home, /<strong>v1\.14<\/strong>网页版本/);
  assert.match(home, /<strong>151<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72A<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72A<\/span>/);
  assert.match(home, /展开 61 篇公开笔记/);
  assert.match(home, /href="#r070a">R0\.70A–R0\.72A 完成版本<\/a>/);
  assert.match(home, /累计回顾收录 91 个节点；全站现有 151 篇公开研究笔记/);
  assert.match(home, /R0\.70A–R0\.72A 共 53 个完成版本/);
  assert.match(home, /NEXT · R0\.72B/);
  assert.equal(count(home, 'data-release="r071w"'), 1);
  assert.equal(count(home, 'href="/notes/r0-71w.html"'), 2);

  const route = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72A">([\s\S]*?)<\/nav>/,
  );
  assert.ok(route);
  assert.equal(count(route[1], 'href="/notes/'), 61);
  assert.equal(count(route[1], 'href="/notes/r0-71w.html"'), 1);

  assert.equal(count(recap, '<article class="phase">'), 17);
  assert.match(recap, /R0\.60 之后的路线分成十七段/);
  assert.match(recap, /R0\.61–R0\.66/);
  assert.match(recap, /R0\.71U–R0\.71W/);
  assert.match(recap, /收录节点：87/);
  assert.match(recap, /回顾截止时公开笔记：147/);
  assert.match(recap, /R0\.70A–R0\.71W 完成版本/);
  const index =
    recap.match(/<div class="node-index-grid">([\s\S]*?)<\/div>/)?.[1] ?? "";
  assert.equal(count(index, 'href="/notes/'), 87);
  assert.equal(count(index, 'href="/notes/r0-71w.html"'), 1);

  assert.match(literature, /R0\.69P–R0\.72A/);
  assert.match(literature, /<header><b>R0\.71W<\/b>/);
  assert.match(literature, /开放接口 · R0\.72B/);
  for (const letter of "abcdefghijklmnopqrstuvwxyz") {
    assert.ok(
      literature.includes('href="/notes/r0-70' + letter + '.html"'),
      "R0.70" + letter.toUpperCase(),
    );
  }
  for (const letter of "abcdefghijklmnopqrstuvw") {
    assert.ok(
      literature.includes('href="/notes/r0-71' + letter + '.html"'),
      "R0.71" + letter.toUpperCase(),
    );
  }

  for (const [page, minimum, version] of [
    [home, 10, "1.14"],
    [note, 16, "1.09"],
    [recap, 8, "1.09"],
    [literature, 50, "1.14"],
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

test("states the amplitude-doped complete-ledger theorem and its data boundary precisely", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const endpointRecap = await readFile(
    new URL("recap-r0-61-r0-71x.html", publicRoot),
    "utf8",
  );

  for (const token of [
    "\\mathscr A_q=q^\\alpha",
    "1&lt;\\alpha&lt;2",
    "\\delta_q=\\frac{\\mathscr A_q}{q^2}",
    "指定的 \\(m=2\\)",
    "filtered \\(C_{*,t}\\)",
    "J_{*,2,q}",
    "\\mathcal R_{Y_q}(I)=O(1)",
    "\\frac{\\mathscr A_q^2}{q^4}",
    "\\frac{J_{*,2,q}}{\\Lambda_1(I;u_q)}",
    "q^{2\\alpha+2}",
    "\\beta&lt;1/3",
    "D^{1/3}",
    "初始 energy/enstrophy 无界",
    "这不是千禧年问题的解答",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /完整.*projected rotational charge/is);
  assert.match(note, /full-frequency.*不是 selected-shell proxy/is);
  assert.match(note, /finite.*corroboration.*不是 DNS/is);
  assert.doesNotMatch(note, /第二个正根/);
  assert.match(home, /complete first-row ledger.*data-independent/is);
  assert.match(recap, /data-uniform complete first-row no-go/is);
  assert.match(literature, /初始 data size 无界/is);
  assert.match(
    endpointRecap,
    /fixed-dimensional declared triangular family internal saturation/is,
  );
});

test("verifies the exact, independent, and truncated-coset R0.71W audits", async () => {
  const [exact, independent, truncated, report, gap, literatureAudit, independentAudit] =
    await Promise.all([
      readFile(new URL("result.json", certificateRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-result.json", certificateRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("truncated-coset-result.json", certificateRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("research/r071w_report-source.md", root), "utf8"),
      readFile(new URL("research/r071w_gap_matrix.md", root), "utf8"),
      readFile(new URL("research/r071w_literature_audit.md", root), "utf8"),
      readFile(new URL("research/r071w_independent_audit.md", root), "utf8"),
    ]);

  assert.equal(exact.release, "R0.71W");
  assert.equal(exact.status, "passed");
  assert.ok(Object.values(exact.checks).every((entry) => entry.passed));
  assert.equal(independent.release, "R0.71W");
  assert.equal(independent.status, "passed");
  assert.ok(Object.values(independent.checks).every((entry) => entry.passed));
  assert.equal(truncated.status, "passed");
  assert.ok(truncated.checks.every((entry) => entry.passed));

  const fitted = exact.checks.amplitudeDopedLedger.fittedPowers;
  assert.ok(Math.abs(fitted.leadingAtomProxy - 1) < 0.01);
  assert.ok(Math.abs(fitted.rotationalChargeUpper + 1) < 0.01);
  assert.ok(Math.abs(fitted.atomToCompleteLedgerProxy - 1) < 0.01);
  assert.ok(Math.abs(fitted.leadingEnstrophyAtLastRoot - 5) < 0.01);
  assert.ok(truncated.checks[0].value < 1e-10);

  assert.match(report, /complete first-row Leray ledger/i);
  assert.match(report, /uniform rescaled implicit-function theorem/i);
  assert.match(report, /data-independent/i);
  assert.match(report, /1\/3/);
  assert.match(gap, /data|initial/i);
  assert.match(literatureAudit, /bounded primary-source audit/i);
  assert.match(independentAudit, /does not import the producer/i);
  assert.match(independentAudit, /uses neither of the first two\s+programs/i);
  assert.doesNotMatch(report, /we prove global regularity/i);
});

test("ships the journal figure package and exact public mirrors", async () => {
  await Promise.all(
    [
      "README.md",
      "caption.md",
      "config.json",
      "contract.json",
      "figure.pdf",
      "figure.png",
      "figure.svg",
      "manifest.json",
      "validation.json",
    ].map((path) => access(new URL(path, figureRoot))),
  );

  const [publicSvg, publicPdf, publicPng, sourceSvg, sourcePdf, sourcePng] =
    await Promise.all([
      readFile(new URL("figures/r0-71w-amplitude-doping.svg", publicRoot)),
      readFile(new URL("figures/r0-71w-amplitude-doping.pdf", publicRoot)),
      readFile(new URL("figures/r0-71w-amplitude-doping.png", publicRoot)),
      readFile(new URL("figure.svg", figureRoot)),
      readFile(new URL("figure.pdf", figureRoot)),
      readFile(new URL("figure.png", figureRoot)),
    ]);

  assert.match(publicSvg.toString("utf8"), /<svg/);
  assert.equal(publicPdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(publicPng.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(sha256(publicSvg), sha256(sourceSvg));
  assert.equal(sha256(publicPdf), sha256(sourcePdf));
  assert.equal(sha256(publicPng), sha256(sourcePng));
});
