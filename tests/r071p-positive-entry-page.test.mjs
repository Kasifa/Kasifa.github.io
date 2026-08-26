import assert from "node:assert/strict";
import { access, readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificatesRoot = new URL("research/certificates/r071p/", root);
const figureSourceRoot = new URL(
  "figures/r071p-positive-entry-batching/fig-r071p-positive-entry-batching/",
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
  for (let code = "a".charCodeAt(0); code <= "p".charCodeAt(0); code += 1) {
    values.push("r0-71" + String.fromCharCode(code));
  }
  return values;
}

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71p.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71p.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("keeps R0.71P reachable after R0.72D becomes current", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 154);
  assert.match(home, /<strong>v1\.17<\/strong>网页版本/);
  assert.match(home, /<strong>154<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72D<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72D<\/span>/);
  assert.match(home, /展开 64 篇公开笔记/);
  assert.match(home, /累计回顾收录 94 个节点；全站现有 154 篇公开研究笔记/);
  assert.match(home, /R0\.70A–R0\.72D 共 56 个已公开并封存版本/);
  assert.match(home, /NEXT · R0\.72E/);

  const currentRoute = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72D">([\s\S]*?)<\/nav>/,
  );
  assert.ok(currentRoute);
  assert.equal(occurrenceCount(currentRoute[1], 'href="/notes/'), 64);
  assert.equal(occurrenceCount(recap, '<article class="phase">'), 12);
  assert.match(recap, /收录节点：80/);
  assert.match(recap, /回顾截止时公开笔记：140/);
  assert.match(recap, /R0\.70A–R0\.71P 完成版本/);
  assert.match(literature, /R0\.69P–R0\.72D/);
  assert.match(literature, /开放接口 · R0\.72E/);

  for (const [page, minimum, i18nVersion] of [
    [home, 10, "1.17"],
    [note, 16, "1.01"],
    [recap, 8, "1.01"],
    [literature, 49, "1.17"],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71P/);
    assert.ok(page.includes(`src="/i18n-en.js?v=${i18nVersion}"`));
  }
});

test("ships one R0.71P release card and complete reproducibility links", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071p" data-release="r071p"';
  const card = sliceReleaseCard(home, opening);

  assert.equal(occurrenceCount(home, opening), 1);
  assert.equal(occurrenceCount(home, 'href="/notes/r0-71p.html"'), 2);
  for (const token of [
    'href="/notes/r0-71p.html"',
    'href="/notes/r0-71p.pdf"',
    'href="/figures/r0-71p-positive-entry-batching.pdf"',
    "research/certificates/r071p",
    "research/r071p_report-source.md",
    "research/r071p_literature_audit.md",
    "research/r071p_gap_matrix.md",
    "research/r071p_independent_audit.md",
    "figures/r071p-positive-entry-batching/fig-r071p-positive-entry-batching",
    'href="/recap-r0-61-r0-72d.html"',
    'href="/recap-r0-61-r0-72d.pdf"',
  ]) {
    assert.ok(card.includes(token), token);
  }
  assert.match(card, /R0\.71Q 已完成/);

  for (const token of [
    'href="/notes/r0-71p.pdf"',
    'href="/recap-r0-61-r0-71p.html"',
    'href="/recap-r0-61-r0-71p.pdf"',
    'src="/figures/r0-71p-positive-entry-batching.svg"',
    "research/r071p_report-source.md",
    "research/r071p_literature_audit.md",
    "research/r071p_independent_audit.md",
    "research/r071p_gap_matrix.md",
    "research/r071p_exact_audit.py",
    "research/r071p_independent_audit.py",
    "research/certificates/r071p",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(recap, /href="\/notes\/r0-71p\.html"/);
  assert.match(recap, /href="\/figures\/r0-71p-positive-entry-batching\.pdf"/);
  assert.match(literature, /<header><b>R0\.71P<\/b>/);
});

test("states the half-open segmented ledger, relaxed measure, spatial batch, and temporal boundary", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "K=[a,b)",
    "I^+_{j,Q}(K)",
    "V^+_{\\rm seg}(a_{j,Q};K)",
    "A_+-(A_+-A_-)^+=\\min(A_+,A_-)",
    "componentwise relaxed positive-entry measure",
    "\\eta^+_\\Lambda",
    "\\mathbf1_{\\operatorname{supp}\\chi_Q}F_j",
    "\\|L(t)\\|_{\\dot H^{-1}}^2",
    "d\\mathfrak n_\\Lambda",
    "\\overline K=[a,b]\\Subset I_{\\rm strong}",
    "t=2k\\pi/N",
    "\\varepsilon_N=N^{-4}",
    "初始 filtered vorticity",
    "c=C_t(0)=2F(0)",
    "N_C(D(t_*,r))",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(note, /不是 signed weak limit 或 signed aggregate 的正 Jordan 部/);
  assert.match(note, /right endpoint|右端 .*不计入|右观测端点不计入/);
  assert.match(note, /extended positive Borel measure/);
  assert.match(note, /不是 NSE 多-face 构造/);
  assert.match(note, /一侧初始 jet，不是内部 crossing/);
  assert.match(note, /不作新颖性、优先权或发表级别声明/);
  assert.match(note, /未证明：继续性、有限时奇性、三维全局正则性或千禧年问题结论/);
  assert.match(home, /逐 shell–cell.*relaxed 正原子/s);
  assert.match(recap, /distinct entry-time counting measure/);
  assert.match(literature, /相邻框架，不推出本节的 BV 引理/is);
});

test("verifies exact and independent R0.71P certificates", async () => {
  const [exact, independent, report] = await Promise.all([
    readFile(new URL("result.json", certificatesRoot), "utf8").then(JSON.parse),
    readFile(new URL("independent-result.json", certificatesRoot), "utf8").then(JSON.parse),
    readFile(new URL("research/r071p_report-source.md", root), "utf8"),
  ]);
  await Promise.all([
    access(new URL("SHA256SUMS", certificatesRoot)),
    access(new URL("research/r071p_gap_matrix.md", root)),
    access(new URL("research/r071p_literature_audit.md", root)),
  ]);

  assert.equal(exact.release, "R0.71P");
  assert.equal(exact.status, "passed");
  assert.ok(Object.values(exact.checks).every((check) => check.passed));
  const boundary = exact.checks.positiveMeasureLedger.observationBoundaryConvention;
  assert.equal(boundary.window, "[a,b)");
  assert.equal(boundary.entryMassAfterSubtractingInitialTrace, "0");
  assert.match(exact.checks.positiveMeasureLedger.monotonicity, /need not equal.*positive Jordan/i);
  assert.equal(exact.checks.oscillatoryTemporalPacking.path.interval, "[0,2*pi)");
  assert.equal(exact.checks.oscillatoryTemporalPacking.samples.at(-1).hardPositiveEntryMass, 64);
  assert.equal(exact.checks.nseSharpInitialBatch.rightEntryAtom, "1/4");
  assert.equal(exact.checks.nseSharpInitialBatch.normInitialFilteredVorticitySquared, "0");
  assert.equal(exact.checks.nseSharpInitialBatch.normInitialFilteredViscousJetSquared, "0");

  assert.equal(independent.release, "R0.71P");
  assert.equal(independent.status, "passed");
  assert.ok(Object.values(independent.checks).every((check) => check.passed));
  assert.equal(independent.checks.randomOverlapLedgers.trialCount, 64);
  assert.equal(independent.checks.oscillatoryEntries.maximumEntryCountError, 0);
  assert.ok(independent.checks.oscillatoryEntries.maximumSoftRelativeError < 2e-15);
  assert.equal(independent.checks.oscillatoryEntries.rows.at(-1).rightEndpointExcluded, true);
  assert.equal(independent.checks.nseSharpInitialEntry.gridOrder, 32);
  assert.equal(independent.checks.nseSharpInitialEntry.rightEntryAtom, 0.25);
  assert.equal(independent.checks.nseSharpInitialEntry.maximumResidual, 0);

  assert.match(report, /half open|half-open/i);
  assert.match(report, /componentwise relaxed positive-entry measure/i);
  assert.match(report, /distinct entry-time counting measure/i);
  assert.match(report, /no uniform NSE\s+zero count/i);
});

test("ships synchronized PDFs, byte-identical figure mirrors, and continuous releases", async () => {
  const [
    { home, note, recap, literature },
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
    instructions,
  ] = await Promise.all([
    publishedPages(),
    readFile(new URL("notes/r0-71p.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71p.pdf", publicRoot)),
    readFile(new URL("figures/r0-71p-positive-entry-batching.svg", publicRoot)),
    readFile(new URL("figures/r0-71p-positive-entry-batching.pdf", publicRoot)),
    readFile(new URL("figures/r0-71p-positive-entry-batching.png", publicRoot)),
    readFile(new URL("figure.svg", figureSourceRoot)),
    readFile(new URL("figure.pdf", figureSourceRoot)),
    readFile(new URL("figure.png", figureSourceRoot)),
    readFile(new URL("manifest.json", figureSourceRoot), "utf8").then(JSON.parse),
    readFile(new URL("validation.json", figureSourceRoot), "utf8").then(JSON.parse),
    readFile(new URL("independent-validation.json", figureSourceRoot), "utf8").then(JSON.parse),
    readFile(new URL("AGENTS.md", root), "utf8"),
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
  assert.equal(manifest.release, "R0.71P");
  assert.equal(manifest.figureId, "fig-r071p-positive-entry-batching");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 118);
  assert.equal(manifest.figure.outputs.find((output) => output.path === "figure.png").dpi, 600);
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.automaticCheckCount, 95);
  assert.equal(manifest.qa.independentCheckCount, 84);
  assert.equal(manifest.computation.pdeTimeStepping, false);
  assert.equal(manifest.computation.dns, false);
  assert.match(manifest.claimBoundary, /abstract smooth Hilbert path, not a coupled NSE/i);
  assert.equal(validation.release, "R0.71P");
  assert.equal(validation.status, "passed");
  assert.equal(independentValidation.release, "R0.71P");
  assert.equal(independentValidation.status, "passed");
  if (manifest.status === "formal") {
    assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
    assert.equal(manifest.git.certificateCommit, manifest.git.sourceCommit);
    assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  } else {
    assert.equal(manifest.status, "draft");
  }

  const routeMatch = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72D">([\s\S]*?)<\/nav>/,
  );
  assert.ok(routeMatch);
  const releases = releaseSequence();
  assert.equal(releases.length, 42);
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
