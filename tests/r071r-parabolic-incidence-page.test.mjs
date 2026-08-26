import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificatesRoot = new URL("research/certificates/r071r/", root);
const figureSourceRoot = new URL(
  "figures/r071r-parabolic-incidence/fig-r071r-parabolic-incidence/",
  root,
);

function occurrenceCount(value, fragment) {
  return value.split(fragment).length - 1;
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function assertLocalAnchorsResolve(html, minimumUniqueTargets) {
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

function sliceReleaseCard(html, opening) {
  const start = html.indexOf(opening);
  assert.ok(start >= 0, opening);
  const next = html.indexOf('<div class="task-one"', start + opening.length);
  const sectionEnd = html.indexOf("</section>", start);
  const end = next >= 0 && next < sectionEnd ? next : sectionEnd;
  assert.ok(end > start, "release card closing boundary");
  return html.slice(start, end);
}

function releaseSequence() {
  const values = [];
  for (let code = "a".charCodeAt(0); code <= "z".charCodeAt(0); code += 1) {
    values.push("r0-70" + String.fromCharCode(code));
  }
  for (let code = "a".charCodeAt(0); code <= "r".charCodeAt(0); code += 1) {
    values.push("r0-71" + String.fromCharCode(code));
  }
  return values;
}

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71r.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71r.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("keeps historical R0.71R artifacts while v1.12 publishes R0.71Z as current", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 150);
  assert.match(home, /<strong>v1\.12<\/strong>网页版本/);
  assert.match(home, /<strong>150<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.71Z<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.71Z<\/span>/);
  assert.match(home, /展开 60 篇公开笔记/);
  assert.match(home, /累计回顾收录 90 个节点；全站现有 150 篇公开研究笔记/);
  assert.match(home, /NEXT · R0\.72A/);

  const currentRoute = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.71Z">([\s\S]*?)<\/nav>/,
  );
  assert.ok(currentRoute);
  assert.equal(occurrenceCount(currentRoute[1], 'href="/notes/'), 60);
  assert.ok(occurrenceCount(recap, '<article class="phase">') >= 12);
  assert.match(recap, /收录节点：82/);
  assert.match(recap, /回顾截止时公开笔记：142/);
  assert.match(recap, /R0\.70A–R0\.71R 完成版本/);
  assert.match(literature, /R0\.69P–R0\.71Z/);
  assert.match(literature, /开放接口 · R0\.72A/);

  for (const [page, minimum, i18nVersion] of [
    [home, 10, "1.12"],
    [note, 14, "1.03"],
    [recap, 8, "1.03"],
    [literature, 49, "1.12"],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71R/);
    assert.ok(page.includes('src="/i18n-en.js?v=' + i18nVersion + '"'));
  }
});

test("ships one R0.71R release card and the complete reader-facing package", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071r" data-release="r071r"';
  const card = sliceReleaseCard(home, opening);

  assert.equal(occurrenceCount(home, opening), 1);
  assert.equal(occurrenceCount(home, 'href="/notes/r0-71r.html"'), 2);
  for (const token of [
    'href="/notes/r0-71r.html"',
    'href="/notes/r0-71r.pdf"',
    'href="/figures/r0-71r-parabolic-incidence.pdf"',
    "research/certificates/r071r",
    "research/r071r_report-source.md",
    "research/r071r_literature_audit.md",
    "research/r071r_gap_matrix.md",
    "research/r071r_independent_audit.md",
    "figures/r071r-parabolic-incidence/fig-r071r-parabolic-incidence",
    'href="/recap-r0-61-r0-71z.html"',
    'href="/recap-r0-61-r0-71z.pdf"',
  ]) {
    assert.ok(card.includes(token), token);
  }
  assert.match(card, /R0\.71S 已完成/);

  for (const token of [
    'href="/recap-r0-61-r0-71r.html"',
    'href="/notes/r0-71r.pdf"',
    'href="/recap-r0-61-r0-71r.pdf"',
    'src="/figures/r0-71r-parabolic-incidence.svg"',
    "research/r071r_report-source.md",
    "research/r071r_literature_audit.md",
    "research/r071r_independent_audit.md",
    "research/r071r_gap_matrix.md",
    "research/r071r_exact_audit.py",
    "research/r071r_independent_audit.py",
    "research/certificates/r071r",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(recap, /href="\/notes\/r0-71r\.html"/);
  assert.match(recap, /href="\/figures\/r0-71r-parabolic-incidence\.pdf"/);
  assert.match(literature, /<header><b>R0\.71R<\/b>/);
});

test("states the conditional theorem and every reviewed rigor boundary", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "C_{j,Q,t}-\\nu\\Delta C_{j,Q}=G_{j,Q}",
    "0&lt;\\theta_-\\le\\theta_\\beta\\le\\theta_*",
    "M=\\sup_\\alpha\\operatorname*{ess\\,sup}_{s}",
    "A_{\\beta,+}\\le\\Gamma_\\rho\\kappa_j^{-\\rho}",
    "\\sum_{j,Q}\\kappa_j^{-6}\\|G_{j,Q}\\|_2^2",
    "\\Gamma_\\rho^{\\rm opt}[u_\\lambda,\\mathcal E_\\lambda]",
    "=\\lambda^\\rho\\Gamma_\\rho^{\\rm opt}[u,\\mathcal E]",
    "\\|L\\|_2^2/Y+\\nu^2\\|\\nabla\\omega\\|_2^2/Y",
    "\\Gamma_{2,\\mathrm{jet}}",
    "=\\frac{K^2}{4\\theta^2}",
    "不是 positive-time certificate (3.3) 的 \\(\\Gamma_2\\) 下界",
    "不排除其他 Duhamel designs",
    "Leray energy 支付有限时间区间上的 source integral",
    "frame constants 则因 frame 固定而与 finite truncation 无关",
    "\\Gamma_\\rho\\) 是 upper comparison constant",
    "\\(1/\\Gamma_\\rho\\) 编码",
    "theorem gates，不是右端乘子",
    "定义 \\(\\Gamma_\\rho^{\\rm opt}[u,\\mathcal E]\\) 为 certificate (3.3) 中最小的 admissible upper comparison constant",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(note, /固定 torus.*integer\/dyadic.*multiplier.*cutoff.*event.*window/is);
  assert.match(note, /统一 .*theta_-.*hypothesis/is);
  assert.match(note, /缺少它时.*windows.*缩短.*overlap/is);
  assert.match(note, /完整 theorem 右端仍可能因.*Gamma_2.*M.*不一致/is);
  assert.match(note, /不声称.*等价于任何 Serrin norm/is);
  assert.match(note, /一参数 endpoint-square、termwise source-square certificate \(3\.3\)/);

  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, /Gamma_2\s*(?:\\gtrsim|\\ge|>=)/);
    assert.doesNotMatch(page, /initial (?:Fourier )?jet[^.。]*forces Gamma_2/i);
    assert.doesNotMatch(page, /quadratic (?:Duhamel )?route (?:stops|stopped|closed)/i);
    assert.doesNotMatch(page, /strong\/Serrin-level/i);
    assert.doesNotMatch(page, /h_\\beta\\asymp|h\\asymp/);
    assert.doesNotMatch(page, /lower incidence constant/i);
    assert.doesNotMatch(page, /删除同刻 cell multiplicity|同刻空间 multiplicity 被删除/);
    assert.doesNotMatch(page, /我们/);
  }
  assert.match(home, /Gamma_\{2,\\mathrm\{jet\}\}/);
  assert.match(recap, /Gamma_\{2,jet\} surrogate/);
  assert.match(home, /time-slice square-function estimate.*吸收同刻 batch/is);
  assert.match(recap, /time-slice square-function estimate.*吸收同刻 batch/is);
  assert.match(literature, /time-slice square-function estimate.*吸收同刻 batch/is);
  assert.match(literature, /least admissible optimal upper comparison constant/is);
  assert.match(note, /uniform parabolicity.*coefficient regularity.*boundary hypotheses.*positive time/is);
  assert.match(literature, /rho=2 是 minimal Leray-paid index/is);
  assert.match(literature, /initial Fourier example.*只定义 Gamma_\{2,jet\} surrogate.*不给 positive-time upper comparison constant Gamma_2 下界/is);
});

test("verifies R0.71R certificates without promoting the initial jet", async () => {
  const [exact, independent, report, gap] = await Promise.all([
    readFile(new URL("result.json", certificatesRoot), "utf8").then(JSON.parse),
    readFile(new URL("independent-result.json", certificatesRoot), "utf8").then(JSON.parse),
    readFile(new URL("research/r071r_report-source.md", root), "utf8"),
    readFile(new URL("research/r071r_gap_matrix.md", root), "utf8"),
  ]);

  assert.equal(exact.release, "R0.71R");
  assert.equal(exact.status, "passed");
  assert.ok(Object.values(exact.checks).every((check) => check.passed));
  assert.match(exact.scope, /conditional NSE parabolic-incidence implication/i);
  assert.match(exact.scope, /no uniform incidence theorem/i);
  assert.equal(
    exact.checks.scaleMatchedSourceLedger.annularDerivativeLedger.minimalEnergyMatchedRhoTwo,
    "sum kappa_j^-6||G||^2 <= C*(||L||_{H^-1}^2+nu^2*Y)",
  );
  assert.equal(
    exact.checks.nseFrequencyJetScaling.rows.at(-1).gammaTwoTaylorJetSurrogate,
    "65536",
  );
  assert.match(
    exact.checks.nseFrequencyJetScaling.claimBoundary,
    /not an exact positive-time NSE integration/i,
  );

  assert.equal(independent.release, "R0.71R");
  assert.equal(independent.status, "passed");
  assert.ok(Object.values(independent.checks).every((check) => check.passed));
  assert.equal(independent.checks.sampledDuhamelChecks.seed, 71073);
  assert.equal(independent.checks.sampledDuhamelChecks.gridSize, 200001);
  assert.ok(independent.checks.sampledDuhamelChecks.maximumDuhamelRatio < 1);

  assert.match(report, /first-jet|Taylor jet/i);
  assert.ok(
    gap.includes(
      "This is not a lower bound for the actual positive-time \\(\\Gamma_2\\)",
    ),
  );
  assert.match(gap, /no Duhamel remainder estimate is claimed/i);
});

test("ships hash-identical figure mirrors and 44 continuous completed releases", async () => {
  const [{ home }, svg, pdf, png, sourceSvg, sourcePdf, sourcePng, manifest] =
    await Promise.all([
      publishedPages(),
      readFile(new URL("figures/r0-71r-parabolic-incidence.svg", publicRoot)),
      readFile(new URL("figures/r0-71r-parabolic-incidence.pdf", publicRoot)),
      readFile(new URL("figures/r0-71r-parabolic-incidence.png", publicRoot)),
      readFile(new URL("figure.svg", figureSourceRoot)),
      readFile(new URL("figure.pdf", figureSourceRoot)),
      readFile(new URL("figure.png", figureSourceRoot)),
      readFile(new URL("manifest.json", figureSourceRoot), "utf8").then(JSON.parse),
    ]);

  assert.match(svg.toString("utf8"), /<svg/);
  assert.equal(pdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.deepEqual(svg, sourceSvg);
  assert.deepEqual(pdf, sourcePdf);
  assert.deepEqual(png, sourcePng);
  assert.equal(manifest.figureId, "fig-r071r-parabolic-incidence");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 118);
  assert.equal(manifest.computation.pdeTimeStepping, false);
  assert.equal(manifest.computation.dns, false);
  assert.match(manifest.claimBoundary, /first-jet coefficient, not a positive-time integration/i);

  for (const [path, publicValue, sourceValue] of [
    ["figure.svg", svg, sourceSvg],
    ["figure.pdf", pdf, sourcePdf],
    ["figure.png", png, sourcePng],
  ]) {
    const expected = manifest.figure.outputs.find((output) => output.path === path);
    assert.ok(expected, path);
    assert.equal(sha256(publicValue), expected.sha256, "public hash " + path);
    assert.equal(sha256(sourceValue), expected.sha256, "source hash " + path);
  }

  const routeMatch = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.71Z">([\s\S]*?)<\/nav>/,
  );
  assert.ok(routeMatch);
  const releases = releaseSequence();
  assert.equal(releases.length, 44);
  for (const slug of releases) {
    const releaseId = slug.replaceAll("-", "");
    const link = 'href="/notes/' + slug + '.html"';
    const opening = '<div class="task-one" id="' + releaseId + '" data-release="' + releaseId + '"';
    await access(new URL("notes/" + slug + ".html", publicRoot));
    assert.equal(occurrenceCount(home, opening), 1, releaseId);
    assert.equal(occurrenceCount(home, link), 2, slug);
    assert.equal(occurrenceCount(routeMatch[1], link), 1, "route " + slug);
    assert.equal(occurrenceCount(sliceReleaseCard(home, opening), link), 1, "card " + slug);
  }
});
