import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificatesRoot = new URL("research/certificates/r071q/", root);
const figureSourceRoot = new URL(
  "figures/r071q-jensen-window-audit/fig-r071q-jensen-window-audit/",
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
  for (let code = "a".charCodeAt(0); code <= "q".charCodeAt(0); code += 1) {
    values.push("r0-71" + String.fromCharCode(code));
  }
  return values;
}

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71q.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71q.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("retains the R0.71Q package after R0.72G becomes current", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 157);
  assert.match(home, /<strong>v1\.20<\/strong>网页版本/);
  assert.match(home, /<strong>157<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72G<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72G<\/span>/);
  assert.match(home, /展开 67 篇公开笔记/);
  assert.match(home, /累计回顾收录 97 个节点；全站现有 157 篇公开研究笔记/);
  assert.match(home, /R0\.70A–R0\.72G 共 59 个版本已公开；按当前 formal-figure 合同有 35 个完整封存，24 个旧版附图档案列入回补清单/);
  assert.match(home, /NEXT · R0\.72H/);

  const currentRoute = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72G">([\s\S]*?)<\/nav>/,
  );
  assert.ok(currentRoute);
  assert.equal(occurrenceCount(currentRoute[1], 'href="/notes/'), 67);
  assert.ok(occurrenceCount(recap, '<article class="phase">') >= 12);
  assert.match(recap, /收录节点：81/);
  assert.match(recap, /回顾截止时公开笔记：141/);
  assert.match(recap, /R0\.70A–R0\.71Q 完成版本/);
  assert.match(literature, /R0\.69P–R0\.72G/);
  assert.match(literature, /开放接口 · R0\.72H/);

  for (const [page, minimum, i18nVersion] of [
    [home, 10, "1.20"],
    [note, 16, "1.02"],
    [recap, 8, "1.02"],
    [literature, 49, "1.20"],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71Q/);
    assert.ok(page.includes('src="/i18n-en.js?v=' + i18nVersion + '"'));
  }
});

test("ships one R0.71Q release card and the complete research package", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071q" data-release="r071q"';
  const card = sliceReleaseCard(home, opening);

  assert.equal(occurrenceCount(home, opening), 1);
  assert.equal(occurrenceCount(home, 'href="/notes/r0-71q.html"'), 2);
  for (const token of [
    'href="/notes/r0-71q.html"',
    'href="/notes/r0-71q.pdf"',
    'href="/figures/r0-71q-jensen-window-audit.pdf"',
    "research/certificates/r071q",
    "research/r071q_report-source.md",
    "research/r071q_literature_audit.md",
    "research/r071q_gap_matrix.md",
    "research/r071q_independent_audit.md",
    "figures/r071q-jensen-window-audit/fig-r071q-jensen-window-audit",
    'href="/recap-r0-61-r0-72g.html"',
    'href="/recap-r0-61-r0-72g.pdf"',
  ]) {
    assert.ok(card.includes(token), token);
  }
  assert.match(card, /R0\.71R 已完成/);

  for (const token of [
    'href="/notes/r0-71q.pdf"',
    'href="/recap-r0-61-r0-71q.html"',
    'href="/recap-r0-61-r0-71q.pdf"',
    'src="/figures/r0-71q-jensen-window-audit.svg"',
    "research/r071q_report-source.md",
    "research/r071q_literature_audit.md",
    "research/r071q_independent_audit.md",
    "research/r071q_gap_matrix.md",
    "research/r071q_exact_audit.py",
    "research/r071q_independent_audit.py",
    "research/certificates/r071q",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(recap, /href="\/notes\/r0-71q\.html"/);
  assert.match(recap, /href="\/figures\/r0-71q-jensen-window-audit\.pdf"/);
  assert.match(literature, /<header><b>R0\.71Q<\/b>/);

  await Promise.all(
    [
      "research/r071q_report-source.md",
      "research/r071q_literature_audit.md",
      "research/r071q_gap_matrix.md",
      "research/r071q_independent_audit.md",
      "research/r071q_exact_audit.py",
      "research/r071q_independent_audit.py",
      "research/certificates/r071q/README.md",
      "research/certificates/r071q/result.json",
      "research/certificates/r071q/independent-result.json",
      "research/certificates/r071q/SHA256SUMS",
      "figures/r071q-jensen-window-audit/fig-r071q-jensen-window-audit/README.md",
      "figures/r071q-jensen-window-audit/fig-r071q-jensen-window-audit/manifest.json",
      "figures/r071q-jensen-window-audit/fig-r071q-jensen-window-audit/data.csv",
      "figures/r071q-jensen-window-audit/fig-r071q-jensen-window-audit/caption.md",
      "figures/r071q-jensen-window-audit/fig-r071q-jensen-window-audit/figure.pdf",
      "figures/r071q-jensen-window-audit/fig-r071q-jensen-window-audit/figure.svg",
      "figures/r071q-jensen-window-audit/fig-r071q-jensen-window-audit/figure.png",
      "figures/r071q-jensen-window-audit/fig-r071q-jensen-window-audit/SHA256SUMS",
    ].map((path) => access(new URL(path, root))),
  );
});

test("states the anchor, truncation, cover, and pointwise-envelope boundary", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "N_C(D(t_*,r))",
    "D(T/4,T/64)",
    "T_1(R)=\\frac{K_\\nu}{(1+R^2)^2}",
    "R_o=\\frac{T_\\sharp}{128}",
    "r_i=\\frac{T_\\sharp}{256}",
    "a_{\\alpha m}=\\|C_\\alpha(t_m)\\|_2&gt;0",
    "J_{\\alpha m}",
    "H_m=\\sup_{t\\in K_m}\\mathcal H(t)",
    "\\sum_{\\alpha\\in\\Lambda^*}",
    "\\log\\frac{M_\\alpha}{a_{\\alpha m}}",
  ]) {
    assert.ok(note.includes(token), token);
  }

  for (const boundary of [
    /锚点|anchor/i,
    /截断|truncation/i,
    /覆盖|cover/i,
    /逐窗口点态上界|pointwise envelope|H_m/i,
  ]) {
    assert.match(note, boundary);
  }
  assert.match(note, /有限条件定理|conditional finite theorem/i);
  assert.match(note, /不是.*Navier.?Stokes|not (?:an? )?NSE trajectory/is);
  assert.match(note, /未证明.*全局正则性|no uniform NSE zero count|no .*global regularity/is);
  assert.match(home, /锚点|anchor/i);
  assert.match(recap, /component.*union|分量.*并集|截断税/is);
  assert.match(literature, /相邻框架，不推出本节的 BV 引理/is);
});

test("publishes the Blaschke, union, and local-cover counterfamilies with primary sources", async () => {
  const [{ note }, sourceAudit] = await Promise.all([
    publishedPages(),
    readFile(new URL("research/r071q_literature_audit.md", root), "utf8"),
  ]);

  for (const token of [
    "a_{N,k}=\\frac{2N^2-k}{4N^2}",
    "B_N(z)=\\prod_{k=1}^N\\frac{z-a_{N,k}}{1-a_{N,k}z}",
    "\\widetilde C_N(z)=B_N(z)^2e",
    "g_q(z)=z-b_q",
    "C_N(z)=\\left(\\frac{\\sin(\\pi Nz)}{\\pi N}\\right)^2e",
    "Y_N(t)=N(1-Nt)_+",
    "\\cosh^2(3\\pi/4)",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /\\lceil N\/2\\rceil/);
  assert.match(note, /all N zeros have|全部 N 个零点|每个零点.*A_\+=1/is);
  assert.match(note, /union.*exactly Q|并集.*Q 个/is);
  assert.match(note, /N windows|N 个窗口/is);
  assert.match(note, /abstract analytic|解析 Hilbert 路径|不是 NSE/is);

  for (const source of [
    "epubs.siam.org/doi/10.1137/1.9781611970050.ch7",
    "doi.org/10.1007/BF02417878",
    "doi.org/10.1016/j.physd.2008.03.007",
    "doi.org/10.1016/j.jfa.2020.108563",
    "doi.org/10.1016/j.jmaa.2022.126428",
    "doi.org/10.3792/pja/1195521421",
    "archiv.saw-leipzig.de",
  ]) {
    assert.ok(sourceAudit.includes(source), source);
    assert.ok(note.includes(source), "public note source: " + source);
  }
  assert.match(sourceAudit, /bounded\s+negative finding/i);
  assert.match(sourceAudit, /not a claim that no such theorem exists/i);
});

test("verifies exact and independent R0.71Q certificates", async () => {
  const [exact, independent, report, independentAudit] = await Promise.all([
    readFile(new URL("result.json", certificatesRoot), "utf8").then(JSON.parse),
    readFile(new URL("independent-result.json", certificatesRoot), "utf8").then(JSON.parse),
    readFile(new URL("research/r071q_report-source.md", root), "utf8"),
    readFile(new URL("research/r071q_independent_audit.md", root), "utf8"),
  ]);
  await Promise.all([
    access(new URL("SHA256SUMS", certificatesRoot)),
    access(new URL("research/r071q_gap_matrix.md", root)),
    access(new URL("research/r071q_literature_audit.md", root)),
  ]);

  assert.equal(exact.release, "R0.71Q");
  assert.equal(exact.status, "passed");
  assert.ok(Object.values(exact.checks).every((check) => check.passed));
  assert.equal(exact.checks.temamLobeDisk.extractedDisk, "D(T_1/4,T_1/64)");
  assert.equal(exact.checks.temamLobeDisk.nestedJensenRadii.radiusMargin, "log 2");
  const exactBlaschke = exact.checks.rationalBlaschkeFamily.rows.at(-1);
  assert.equal(exactBlaschke.N, 64);
  assert.equal(exactBlaschke.distinctRealZeroCount, 64);
  assert.equal(exactBlaschke.positiveDerivativeZeroCount, 32);
  assert.equal(exactBlaschke.squaredFamily.positiveEntryCountForFEqualsEAndYEqualsOne, 64);
  assert.ok(exactBlaschke.jensenMultiplicityBoundAtInnerRadiusOneHalf < 65);
  assert.equal(
    exact.checks.observableUnionTax.rows.at(-1).distinctUnionZeroCount,
    64,
  );
  assert.equal(
    exact.checks.localWindowCoverTax.rows.at(-1).ownedWindowCount,
    64,
  );
  assert.equal(
    exact.checks.localWindowCoverTax.rows.at(-1).entryCountOnHalfOpenUnitWindow,
    64,
  );
  assert.equal(
    exact.checks.lerayCoveringBudgetSeparation.rows.at(-1).integralYSquared,
    "64/3",
  );

  assert.equal(independent.release, "R0.71Q");
  assert.equal(independent.status, "passed");
  assert.ok(Object.values(independent.checks).every((check) => check.passed));
  assert.equal(independent.checks.blaschkeChecks.circleSampleCount, 8192);
  assert.ok(independent.checks.blaschkeChecks.maximumBoundaryModulusError < 2e-14);
  assert.equal(independent.checks.blaschkeChecks.maximumZeroResidual, 0);
  assert.equal(independent.checks.lobeDiskSampling.seed, 71072);
  assert.equal(independent.checks.lobeDiskSampling.sampleCount, 200000);
  assert.equal(independent.checks.unionTaxChecks.rows.at(-1).distinctUnionZeroCount, 64);
  assert.equal(independent.checks.localWindowFamilyChecks.rows.at(-1).ownedWindowCount, 64);
  assert.equal(independent.checks.coveringScaleChecks.rows.at(-1).inverseScale, 66049);

  assert.match(report, /finite anchor-taxed entry packing/i);
  assert.match(report, /pointwise batch envelope/i);
  assert.match(report, /no uniform Navier--Stokes\s+zero count/i);
  assert.match(independentAudit, /no\s+Navier--Stokes time integration/i);
});

test("ships synchronized PDFs, hash-identical figure mirrors, and 43 continuous releases", async () => {
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
    readFile(new URL("notes/r0-71q.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71q.pdf", publicRoot)),
    readFile(new URL("figures/r0-71q-jensen-window-audit.svg", publicRoot)),
    readFile(new URL("figures/r0-71q-jensen-window-audit.pdf", publicRoot)),
    readFile(new URL("figures/r0-71q-jensen-window-audit.png", publicRoot)),
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

  assert.equal(manifest.release, "R0.71Q");
  assert.equal(manifest.figureId, "fig-r071q-jensen-window-audit");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 118);
  assert.equal(manifest.figure.outputs.find((output) => output.path === "figure.png").dpi, 600);
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.automaticCheckCount, 6);
  assert.equal(manifest.qa.independentCheckCount, 8);
  assert.equal(manifest.computation.pdeTimeStepping, false);
  assert.equal(manifest.computation.dns, false);
  assert.match(manifest.claimBoundary, /not Navier-Stokes trajectories/i);
  assert.equal(validation.status, "passed");
  assert.equal(validation.checkCount, 6);
  assert.equal(independentValidation.status, "passed");
  assert.equal(independentValidation.checkCount, 8);

  for (const [path, publicValue, sourceValue] of [
    ["figure.svg", svg, sourceSvg],
    ["figure.pdf", figurePdf, sourceFigurePdf],
    ["figure.png", png, sourcePng],
  ]) {
    const expected = manifest.figure.outputs.find((output) => output.path === path);
    assert.ok(expected, path);
    assert.equal(sha256(publicValue), expected.sha256, "public hash " + path);
    assert.equal(sha256(sourceValue), expected.sha256, "source hash " + path);
  }

  if (manifest.status === "formal") {
    assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
    assert.equal(manifest.git.certificateCommit, manifest.git.sourceCommit);
    assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  } else {
    assert.equal(manifest.status, "draft");
  }

  const routeMatch = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72G">([\s\S]*?)<\/nav>/,
  );
  assert.ok(routeMatch);
  const releases = releaseSequence();
  assert.equal(releases.length, 43);
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
