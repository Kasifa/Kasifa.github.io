import assert from "node:assert/strict";
import { access, readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificatesRoot = new URL("research/certificates/r071o/", root);
const figureSourceRoot = new URL(
  "figures/r071o-soft-denominator-faces/fig-r071o-soft-denominator-faces/",
  root,
);

function occurrenceCount(value, fragment) {
  return value.split(fragment).length - 1;
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
  for (let code = "a".charCodeAt(0); code <= "o".charCodeAt(0); code += 1) {
    values.push("r0-71" + String.fromCharCode(code));
  }
  return values;
}

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71o.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71o.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("keeps historical R0.71O artifacts reachable after R0.72A becomes current", async () => {
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
  assert.match(home, /累计回顾收录 91 个节点；全站现有 151 篇公开研究笔记/);
  assert.match(home, /R0\.70A–R0\.72A 共 53 个完成版本/);
  assert.match(home, /NEXT · R0\.72B/);

  const currentRoute = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72A">([\s\S]*?)<\/nav>/,
  );
  assert.ok(currentRoute);
  assert.equal(occurrenceCount(currentRoute[1], 'href="/notes/'), 61);
  assert.equal(occurrenceCount(currentRoute[1], 'href="/notes/r0-71o.html"'), 1);
  assert.equal(occurrenceCount(recap, '<article class="phase">'), 12);
  assert.match(recap, /收录节点：79/);
  assert.match(recap, /回顾截止时公开笔记：139/);
  assert.match(recap, /R0\.70A–R0\.71O 完成版本/);
  assert.match(literature, /R0\.69P–R0\.72A/);
  assert.match(literature, /开放接口 · R0\.72B/);

  for (const [page, minimum, i18nVersion] of [
    [home, 10, "1.14"],
    [note, 16, "1.00"],
    [recap, 8, "1.00"],
    [literature, 49, "1.14"],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71O/);
    assert.ok(page.includes(`src="/i18n-en.js?v=${i18nVersion}"`));
  }
});

test("keeps one release card, exactly two homepage links, and all reproducibility links", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071o" data-release="r071o"';
  const card = sliceReleaseCard(home, opening);

  assert.equal(occurrenceCount(home, opening), 1);
  assert.equal(occurrenceCount(home, 'href="/notes/r0-71o.html"'), 2);
  for (const token of [
    'href="/notes/r0-71o.html"',
    'href="/notes/r0-71o.pdf"',
    'href="/figures/r0-71o-soft-denominator-faces.pdf"',
    "research/certificates/r071o",
    "research/r071o_report-source.md",
    "research/r071o_literature_audit.md",
    "research/r071o_gap_matrix.md",
    "figures/r071o-soft-denominator-faces/fig-r071o-soft-denominator-faces",
    'href="/recap-r0-61-r0-72a.html"',
    'href="/recap-r0-61-r0-72a.pdf"',
  ]) {
    assert.ok(card.includes(token), token);
  }
  assert.match(card, /R0\.71P 已完成/);

  for (const token of [
    'href="/notes/r0-71o.pdf"',
    'href="/recap-r0-61-r0-71o.html"',
    'href="/recap-r0-61-r0-71o.pdf"',
    'src="/figures/r0-71o-soft-denominator-faces.svg"',
    "research/r071o_report-source.md",
    "research/r071o_literature_audit.md",
    "research/r071o_independent_audit.md",
    "research/r071o_gap_matrix.md",
    "research/r071o_exact_audit.py",
    "research/r071o_independent_audit.py",
    "research/certificates/r071o",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(recap, /href="\/notes\/r0-71o\.html"/);
  assert.match(recap, /href="\/figures\/r0-71o-soft-denominator-faces\.pdf"/);
  assert.match(literature, /<header><b>R0\.71O<\/b>/);
  assert.match(literature, /href="\/notes\/r0-71o\.html"/);
});

test("states the finite-order C1 theorem, face atoms, raw cancellation, abstract separation, and NSE entry boundary", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "z_{Q,\\varepsilon}=\\sqrt{\\sigma_{Q,\\varepsilon}}",
    "2z_{Q,\\varepsilon}^+\\mathcal J^N_{Q,\\varepsilon}",
    "C_{Q,t}(t_0+\\tau)=m c\\,\\tau^{m-1}+O_H(|\\tau|^m)",
    "A_+-A_-",
    "A_++A_-",
    "\\gamma^2\\log",
    "C_N(t)=N^{-1}\\sin(Nt)e",
    "\\operatorname{TV}(a_{N,\\varepsilon_N})",
    "\\|F_j(0)\\|_2^2=\\frac14",
    "\\boxed{\\lim_{t\\downarrow0}a_Q(t)=\\frac14}",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(note, /soft regularization 解决的是 .*坐标定义，不是 face-payment/);
  assert.match(note, /signed atom 可以消失/);
  assert.match(note, /各自总变差.*发散；联合后对数精确抵消/);
  assert.match(note, /smooth Hilbert path，不是耦合 NSE/);
  assert.match(note, /不是内部 crossing，也没有构造任意多 NSE faces/);
  assert.match(note, /没有新的 continuation criterion/);
  assert.match(note, /不作新颖性、优先权或发表级别声明/);
  assert.match(note, /未证明：内部 NSE faces 可以任意多/);
  assert.match(note, /未证明：refresh、moving cells、弱解极限/);
  assert.match(note, /https:\/\/doi\.org\/10\.1007\/BF02196453/);
  assert.doesNotMatch(note, /BF01040914/);

  const next = note.slice(note.indexOf('<section id="next">'), note.indexOf('<section id="claims">'));
  assert.match(next, /A_{j,Q,\+}/);
  assert.doesNotMatch(next, /A_{j,Q,-}/);
  assert.match(home, /soft denominator|Jordan face/i);
  assert.match(recap, /raw source\/radial logs/);
  assert.match(literature, /相邻框架，不推出本节的 BV 引理/is);
  assert.match(literature, /不作新颖性、优先权或 NSE 正则性声明/);
});

test("verifies exact and independent certificates and their declared boundaries", async () => {
  const [exact, independent, report] = await Promise.all([
    readFile(new URL("result.json", certificatesRoot), "utf8").then(JSON.parse),
    readFile(new URL("independent-result.json", certificatesRoot), "utf8").then(JSON.parse),
    readFile(new URL("research/r071o_report-source.md", root), "utf8"),
  ]);
  await Promise.all([
    access(new URL("SHA256SUMS", certificatesRoot)),
    access(new URL("research/r071o_gap_matrix.md", root)),
    access(new URL("research/r071o_literature_audit.md", root)),
  ]);

  assert.equal(exact.release, "R0.71O");
  assert.equal(exact.status, "passed");
  assert.ok(Object.values(exact.checks).every((check) => check.passed));
  assert.match(exact.checks.finiteOrderFace.hypothesis, /C_t=m\*c/);
  assert.equal(
    exact.checks.finiteOrderFace.measureLimit.positiveDerivativeAtom,
    "A_plus*delta_t0",
  );
  assert.equal(
    exact.checks.finiteOrderFace.measureLimit.negativeDerivativeAtom,
    "A_minus*delta_t0",
  );
  assert.match(exact.checks.rawSplitCancellation.conclusion, /logarithmically divergent/);
  assert.match(exact.checks.oscillatorySeparation.claimBoundary, /not constrained.*NSE/i);
  assert.equal(exact.checks.nseInitialFace.rightEntryTrace, "1/4");
  assert.match(exact.claimBoundary, /No refresh or moving-cell theorem/);

  assert.equal(independent.release, "R0.71O");
  assert.equal(independent.status, "passed");
  assert.ok(Object.values(independent.checks).every((check) => check.passed));
  assert.equal(independent.checks.nseInitialFace.gridOrder, 32);
  assert.equal(independent.checks.nseInitialFace.rightEntryTrace, 0.25);
  assert.ok(independent.checks.innerProfiles.maximumDerivativeMassError < 1e-14);
  assert.ok(independent.checks.rawSplitCancellation.maximumJointRelativeError < 1e-14);
  assert.ok(independent.checks.oscillatoryPaths.maximumVariationRelativeError < 1e-14);
  assert.match(independent.claimBoundary, /No time integration/);

  assert.match(report, /bounded primary-source search/i);
  assert.match(report, /weighted all-cell\/all-shell entry measure/i);
  assert.match(report, /No continuation, regularity, or singularity conclusion follows/i);
  assert.match(report, /https:\/\/doi\.org\/10\.1007\/BF02196453/);
});

test("ships synchronized PDFs and byte-identical three-format figure mirrors with manifest QA", async () => {
  const [
    { home, note, recap },
    notePdf,
    recapPdf,
    svg,
    figurePdf,
    png,
    sourceSvg,
    sourceFigurePdf,
    sourcePng,
    manifest,
    validation,
    independentValidation,
  ] = await Promise.all([
    publishedPages(),
    readFile(new URL("notes/r0-71o.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71o.pdf", publicRoot)),
    readFile(new URL("figures/r0-71o-soft-denominator-faces.svg", publicRoot)),
    readFile(new URL("figures/r0-71o-soft-denominator-faces.pdf", publicRoot)),
    readFile(new URL("figures/r0-71o-soft-denominator-faces.png", publicRoot)),
    readFile(new URL("figure.svg", figureSourceRoot)),
    readFile(new URL("figure.pdf", figureSourceRoot)),
    readFile(new URL("figure.png", figureSourceRoot)),
    readFile(new URL("manifest.json", figureSourceRoot), "utf8").then(JSON.parse),
    readFile(new URL("validation.json", figureSourceRoot), "utf8").then(JSON.parse),
    readFile(new URL("independent-validation.json", figureSourceRoot), "utf8").then(JSON.parse),
  ]);

  assert.equal(notePdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.equal(recapPdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.ok(notePdf.length > 10_000);
  assert.ok(recapPdf.length > 10_000);
  assert.match(svg.toString("utf8"), /<svg/);
  assert.equal(figurePdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.deepEqual(svg, sourceSvg);
  assert.deepEqual(figurePdf, sourceFigurePdf);
  assert.deepEqual(png, sourcePng);

  assert.match(note, /src="\/figures\/r0-71o-soft-denominator-faces\.svg"/);
  assert.match(recap, /href="\/recap-r0-61-r0-71o\.pdf"/);
  assert.match(home, /href="\/figures\/r0-71o-soft-denominator-faces\.pdf"/);
  assert.equal(manifest.release, "R0.71O");
  assert.equal(manifest.figureId, "fig-r071o-soft-denominator-faces");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 118);
  assert.equal(manifest.figure.outputs.find((output) => output.path === "figure.png").dpi, 600);
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.computation.pdeTimeStepping, false);
  assert.equal(manifest.computation.dns, false);
  assert.match(manifest.claimBoundary, /abstract smooth Hilbert path, not a coupled NSE observable/i);
  assert.equal(validation.release, "R0.71O");
  assert.equal(validation.status, "pass");
  assert.equal(independentValidation.release, "R0.71O");
  assert.equal(independentValidation.status, "pass");

  if (manifest.status === "formal") {
    assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
    assert.equal(manifest.git.certificateCommit, manifest.git.sourceCommit);
    assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  } else {
    assert.equal(manifest.status, "draft");
  }
});

test("keeps all 41 R0.70A-R0.71O releases continuous and screens discouraged wording", async () => {
  const [{ home, note, recap, literature }, instructions] = await Promise.all([
    publishedPages(),
    readFile(new URL("AGENTS.md", root), "utf8"),
  ]);
  const routeMatch = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72A">([\s\S]*?)<\/nav>/,
  );
  assert.ok(routeMatch);
  const releases = releaseSequence();
  assert.equal(releases.length, 41);

  for (const slug of releases) {
    const releaseId = slug.replaceAll("-", "");
    const link = 'href="/notes/' + slug + '.html"';
    const opening = '<div class="task-one" id="' + releaseId + '" data-release="' + releaseId + '"';
    const pdf = await readFile(new URL("notes/" + slug + ".pdf", publicRoot));
    await access(new URL("notes/" + slug + ".html", publicRoot));
    assert.equal(occurrenceCount(home, opening), 1, releaseId);
    assert.equal(occurrenceCount(home, link), 2, slug);
    assert.equal(occurrenceCount(routeMatch[1], link), 1, "route " + slug);
    assert.equal(occurrenceCount(sliceReleaseCard(home, opening), link), 1, "card " + slug);
    assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-", slug);
    assert.ok(pdf.length > 10_000, slug);
  }

  for (const phrase of ["我们", "攻关", "主攻", "研究纪律", "杀死错误想法"]) {
    assert.ok(instructions.includes(phrase), phrase);
  }
  const forbidden = /攻关|主攻|研究纪律|三重审计|杀死错误想法|重大突破|颠覆性|世界首个|接近解决|解决了千禧年|证明了全局正则性|原创性定理|首次证明/;
  const brokenTex = /(^|\n)u K\^|(^|\n)abla\b|(^|\n)imes\b|(^|\n)rac\b|\\!left\b|,qquad\b/m;
  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, forbidden);
    assert.doesNotMatch(page, /我们/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /\t/);
    assert.doesNotMatch(page, brokenTex);
  }
});
