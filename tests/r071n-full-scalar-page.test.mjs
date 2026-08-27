import assert from "node:assert/strict";
import { access, readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificatesRoot = new URL("research/certificates/r071n/", root);
const figureSourceRoot = new URL(
  "figures/r071n-full-scalar/fig-r071n-square-residual-boundary/",
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
  for (let code = "a".charCodeAt(0); code <= "n".charCodeAt(0); code += 1) {
    values.push("r0-71" + String.fromCharCode(code));
  }
  return values;
}

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71n.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71n.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("keeps the historical R0.71N release, v0.99 note, and 78-node recap reachable", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.ok(noteNames.filter((name) => name.endsWith(".html")).length >= 138);
  assert.match(home, /href="\/notes\/r0-71n\.html"/);
  assert.match(home, /data-release="r071n"/);

  const currentRoute = [...home.matchAll(
    /<nav class="route-note-links"[^>]*>([\s\S]*?)<\/nav>/g,
  )].find((match) => match[1].includes('href="/notes/r0-71n.html"'));
  assert.ok(currentRoute);
  assert.equal(occurrenceCount(currentRoute[1], 'href="/notes/r0-71n.html"'), 1);

  assert.equal(occurrenceCount(recap, '<article class="phase">'), 12);
  assert.match(recap, /收录节点：78/);
  assert.match(recap, /回顾截止时公开笔记：138/);
  assert.match(recap, /回顾截止节点：R0\.71N/);
  assert.match(recap, /R0\.71O/);
  assert.match(literature, /<header><b>R0\.71N<\/b>/);

  for (const [page, minimum] of [
    [home, 10],
    [note, 16],
    [recap, 8],
    [literature, 49],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71N/);
    assert.match(page, /src="\/i18n-en\.js\?v=\d+\.\d+"/);
  }
  for (const page of [note, recap]) {
    assert.match(page, /src="\/i18n-en\.js\?v=0\.99"/);
  }
});

test("keeps one R0.71N card, exactly two homepage note links, and all release links", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071n" data-release="r071n"';
  const homeCard = sliceReleaseCard(home, opening);

  assert.equal(occurrenceCount(home, opening), 1);
  assert.equal(
    occurrenceCount(home, 'href="/notes/r0-71n.html"'),
    2,
  );
  for (const token of [
    'href="/notes/r0-71n.html"',
    'href="/notes/r0-71n.pdf"',
    'href="/figures/r0-71n-full-scalar.pdf"',
    "research/certificates/r071n",
    "research/r071n_report-source.md",
    "research/r071n_literature_audit.md",
    "figures/r071n-full-scalar/fig-r071n-square-residual-boundary",
  ]) {
    assert.ok(homeCard.includes(token), token);
  }
  assert.match(homeCard, /href="\/recap-r0-61-r0-72o\.html"/);
  assert.match(homeCard, /href="\/recap-r0-61-r0-72o\.pdf"/);
  assert.match(homeCard, /<strong>结论边界：<\/strong>/);
  assert.match(homeCard, /(?:下一步 R0\.71O|R0\.71O 已完成)/);

  assert.match(
    note,
    /<title>R0\.71N｜完整标量的平方—余项分解与二阶边界<\/title>/,
  );
  for (const token of [
    'href="/notes/r0-71n.pdf"',
    'href="/recap-r0-61-r0-71n.html"',
    'href="/recap-r0-61-r0-71n.pdf"',
    'src="/figures/r0-71n-full-scalar.svg"',
    "research/r071n_report-source.md",
    "research/r071n_literature_audit.md",
    "research/r071n_independent_audit.md",
    "research/r071n_gap_matrix.md",
    "research/r071n_exact_audit.py",
    "research/r071n_independent_audit.py",
    "research/certificates/r071n",
    "figures/r071n-full-scalar/fig-r071n-square-residual-boundary",
  ]) {
    assert.ok(note.includes(token), token);
  }

  const recapNeedle = 'href="/notes/r0-71n.html"';
  const recapNeedleIndex = recap.indexOf(recapNeedle);
  const recapCardStart = recap.lastIndexOf(
    '<article class="phase">',
    recapNeedleIndex,
  );
  const recapCardEnd = recap.indexOf("</article>", recapNeedleIndex);
  assert.ok(recapNeedleIndex >= 0);
  assert.ok(recapCardStart >= 0);
  assert.ok(recapCardEnd > recapCardStart);
  const recapCard = recap.slice(recapCardStart, recapCardEnd);
  assert.match(recapCard, /平方—余项|square.*residual|second.?jet/i);
  assert.match(recapCard, /href="\/figures\/r0-71n-full-scalar\.pdf"/);
  assert.match(recapCard, /research\/certificates\/r071n/);

  const literatureMarker = "<header><b>R0.71N</b>";
  const literatureMarkerIndex = literature.indexOf(literatureMarker);
  const literatureCardStart = literature.lastIndexOf(
    '<div class="route-step',
    literatureMarkerIndex,
  );
  const literatureCardEnd = literature.indexOf(
    "</div>",
    literatureMarkerIndex,
  );
  assert.ok(literatureMarkerIndex >= 0);
  assert.ok(literatureCardStart >= 0);
  assert.ok(literatureCardEnd > literatureCardStart);
  const literatureCard = literature.slice(
    literatureCardStart,
    literatureCardEnd,
  );
  assert.match(literatureCard, /href="\/notes\/r0-71n\.html"/);
  assert.match(literatureCard, /平方|second.?jet|residual/i);
});

test("states the complete derivative, square-residual cancellation, second jet, and claim boundary", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "z_Q=\\frac{B_Q}{\\sqrt{Yd_Q}}",
    "\\mathcal J_Q",
    "\\frac{B_{Q,t}+\\lambda_jB_Q}{\\sqrt{Yd_Q}}",
    "\\frac{Y_t}{Y}+\\frac{d_{Q,t}}{d_Q}",
    "Y_t=2\\langle\\omega,\\operatorname{curl}L\\rangle",
    "-2\\nu\\|\\nabla\\omega\\|_2^2",
    "\\langle P_QF_j,P_QM_Q\\rangle",
    "\\frac12d_{Q,t}+\\lambda_jd_Q",
    "\\mathcal P_Q^\\square=\\int\\chi_Q\\left|G_j+\\frac\\nu2H_j\\right|^2\\ge0",
    "\\mathfrak R_Q",
    "B_Q=e_{Q,t}+\\nu D_Q^\\chi",
    "e_{Q,tt}+\\nu(D_Q^\\chi)_t",
    "\\lambda_j(e_{Q,t}+\\nu D_Q^\\chi)",
    "\\kappa_j^{-2}z_Q^+\\mathcal J_Q^+",
    "R_\\varepsilon=\\sqrt{d_Q+\\varepsilon}",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(note, /它不是相关系数/);
  assert.ok(note.includes("没有 \\(|z_Q|\\le1\\) 的普遍界"));
  assert.match(note, /把二维恒等式误用于三维/);
  assert.match(note, /两个名义率完全消去/);
  assert.match(note, /正平方在完整标量中完全消失/);
  assert.match(note, /精确、有符号、二阶时间\/混合归一化 residual/);
  assert.match(note, /不是新的 coercive payment/);
  assert.match(note, /两个 .*smooth NSE initial jets.*双号/);
  assert.match(note, /尚不是 outward-rounded interval sign theorem/);
  assert.match(note, /没有新的 continuation criterion/);
  assert.match(note, /未证明：second-jet residual/);
  assert.match(note, /未证明：faces、refresh、moving cells/);
  assert.match(note, /不作新颖性、优先权或发表级别声明/);
  assert.match(note, /对千禧年问题没有直接解答/);

  assert.match(home, /square|平方|second.?jet|二阶余项/i);
  assert.match(recap, /square|平方|second.?jet|二阶余项/i);
  assert.match(
    literature,
    /完整 fixed-cell 标量只留下临界 signed second jet/i,
  );
  assert.match(
    literature,
    /不作新颖性、优先权或 NSE 正则性声明/,
  );
});

test("verifies exact and independent certificates, including opposite J signs and declared thresholds", async () => {
  const { note } = await publishedPages();
  const linkedSources = [
    "research/r071n_report-source.md",
    "research/r071n_literature_audit.md",
    "research/r071n_independent_audit.md",
    "research/r071n_gap_matrix.md",
    "research/r071n_exact_audit.py",
    "research/r071n_independent_audit.py",
  ];
  for (const source of linkedSources) assert.ok(note.includes(source), source);

  await Promise.all([
    ...linkedSources.map((source) => access(new URL(source, root))),
    access(new URL("result.json", certificatesRoot)),
    access(new URL("independent-result.json", certificatesRoot)),
    access(new URL("SHA256SUMS", certificatesRoot)),
  ]);

  const [report, exactCertificate, independentCertificate] =
    await Promise.all([
      readFile(new URL("research/r071n_report-source.md", root), "utf8"),
      readFile(new URL("result.json", certificatesRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(
        new URL("independent-result.json", certificatesRoot),
        "utf8",
      ).then(JSON.parse),
    ]);

  assert.match(report, /complete fixed-cell scalar/i);
  assert.match(report, /square--residual|square.?residual/i);
  assert.match(report, /second-jet|second jet/i);
  assert.match(report, /bounded primary-source search/i);
  assert.match(report, /not (?:a )?correlation coefficient/i);
  assert.match(
    report,
    /No continuation, regularity, or singularity conclusion follows/i,
  );

  assert.equal(exactCertificate.release, "R0.71N");
  assert.equal(exactCertificate.status, "passed");
  assert.ok(
    Object.values(exactCertificate.checks).every(
      (value) => value.passed === true,
    ),
  );
  const fusion = exactCertificate.checks.fullScalarFusion;
  assert.equal(fusion.nominalProjective, "-" + fusion.nominalRadial);
  assert.match(fusion.squarePlusResidual, /Y\*\*\(3\/2\).*d\*\*\(3\/2\)/);
  assert.match(fusion.boundary, /remain signed/);
  const localFusion = exactCertificate.checks.localEnstrophyFusion;
  assert.equal(localFusion.localBalance, "B=e_t+nu*D_chi");
  assert.match(localFusion.conclusion, /positive square cancels exactly/i);
  assert.match(localFusion.conclusion, /signed second-time/i);
  assert.equal(exactCertificate.checks.scalingLedger.JExponent, "3");
  assert.equal(
    exactCertificate.checks.scalingLedger
      .kappaMinus2_z_J_dt_Exponent,
    "0",
  );
  assert.ok(
    exactCertificate.checks.domainBoundary.notCovered.includes(
      "one-sided denominator faces",
    ),
  );
  assert.match(exactCertificate.claimBoundary, /neither a sign or energy bound/);
  assert.match(exactCertificate.claimBoundary, /global-regularity result/);

  assert.equal(independentCertificate.release, "R0.71N");
  assert.equal(independentCertificate.status, "passed");
  assert.deepEqual(independentCertificate.configuration.gridOrders, [48, 64, 80]);
  assert.equal(independentCertificate.configuration.randomness, false);
  assert.equal(independentCertificate.configuration.timeStepping, false);

  const thresholds = independentCertificate.configuration.thresholds;
  assert.ok(thresholds.algebraRelativeResidual <= 5e-11);
  assert.ok(thresholds.resolutionRelativeResidual <= 5e-11);
  assert.ok(thresholds.positiveZMargin >= 1e-4);
  assert.ok(thresholds.signedJMargin >= 0.5);

  const positive = independentCertificate.witnesses.positiveJ_seed49.find(
    (entry) => entry.order === 64,
  );
  const negative = independentCertificate.witnesses.negativeJ_seed5.find(
    (entry) => entry.order === 64,
  );
  assert.ok(positive);
  assert.ok(negative);
  assert.ok(positive.cell.z > thresholds.positiveZMargin);
  assert.ok(negative.cell.z > thresholds.positiveZMargin);
  assert.ok(positive.J.direct > thresholds.signedJMargin);
  assert.ok(negative.J.direct < -thresholds.signedJMargin);
  assert.ok(positive.signedFusion.signedResidual > 0);
  assert.ok(negative.signedFusion.signedResidual < 0);

  for (const witness of [positive, negative]) {
    assert.ok(
      witness.checks.maxJRepresentationRelativeResidual <
        thresholds.algebraRelativeResidual,
    );
    assert.ok(
      witness.checks.squareCancellationRelativeResidual <
        thresholds.algebraRelativeResidual,
    );
    for (const residual of Object.values(
      witness.checks.JRepresentationRelativeResiduals,
    )) {
      assert.ok(residual < thresholds.algebraRelativeResidual);
    }
  }

  for (const agreement of Object.values(
    independentCertificate.resolutionAgreement,
  )) {
    assert.equal(agreement.passed, true);
    assert.ok(
      agreement.maximumRelativeResidual <
        thresholds.resolutionRelativeResidual,
    );
    assert.equal(
      agreement.tolerance,
      thresholds.resolutionRelativeResidual,
    );
  }
  assert.deepEqual(independentCertificate.checkedObservations, {
    bothWitnessesHavePositiveZ: true,
    positiveJ_seed49HasPositiveJ: true,
    negativeJ_seed5HasNegativeJ: true,
    positiveSquareIsCanceledInCompleteSecondJetLedger: true,
  });
  assert.match(independentCertificate.claimBoundary, /no time stepping/i);
  assert.match(independentCertificate.claimBoundary, /originality claim/);
  assert.match(independentCertificate.claimBoundary, /Millennium-problem/);
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
    readFile(new URL("notes/r0-71n.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71n.pdf", publicRoot)),
    readFile(new URL("figures/r0-71n-full-scalar.svg", publicRoot)),
    readFile(new URL("figures/r0-71n-full-scalar.pdf", publicRoot)),
    readFile(new URL("figures/r0-71n-full-scalar.png", publicRoot)),
    readFile(new URL("figure.svg", figureSourceRoot)),
    readFile(new URL("figure.pdf", figureSourceRoot)),
    readFile(new URL("figure.png", figureSourceRoot)),
    readFile(new URL("manifest.json", figureSourceRoot), "utf8").then(
      JSON.parse,
    ),
    readFile(new URL("validation.json", figureSourceRoot), "utf8").then(
      JSON.parse,
    ),
    readFile(
      new URL("independent-validation.json", figureSourceRoot),
      "utf8",
    ).then(JSON.parse),
  ]);

  await access(new URL("SHA256SUMS", figureSourceRoot));
  assert.match(note, /src="\/figures\/r0-71n-full-scalar\.svg"/);
  assert.match(note, /href="\/notes\/r0-71n\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-71n\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-71n\.pdf"/);
  assert.match(home, /href="\/notes\/r0-71n\.pdf"/);
  assert.match(home, /href="\/recap-r0-61-r0-72o\.pdf"/);
  assert.match(home, /href="\/figures\/r0-71n-full-scalar\.pdf"/);

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

  assert.equal(manifest.release, "R0.71N");
  assert.equal(manifest.figureId, "fig-r071n-square-residual-boundary");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 118);
  assert.deepEqual(
    manifest.figure.outputs.map((output) => output.path).sort(),
    ["figure.pdf", "figure.png", "figure.svg"],
  );
  assert.equal(
    manifest.figure.outputs.find((output) => output.path === "figure.png").dpi,
    600,
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.computation.dns, false);
  assert.equal(manifest.computation.fittedData, false);
  assert.equal(manifest.computation.pdeTimeStepping, false);
  assert.equal(manifest.computation.intervalCertified, false);
  assert.match(manifest.claimBoundary, /not interval theorems/i);
  assert.match(manifest.claimBoundary, /No no-go/);

  assert.equal(validation.release, "R0.71N");
  assert.equal(validation.status, "pass");
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.ok(validation.metrics.resolutionMaximumRelativeResidual < 5e-11);
  assert.equal(independentValidation.release, "R0.71N");
  assert.equal(independentValidation.status, "pass");
  assert.ok(Object.values(independentValidation.checks).every(Boolean));

  if (manifest.status === "formal") {
    assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
    assert.equal(manifest.git.certificateCommit, manifest.git.sourceCommit);
    assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  } else {
    assert.equal(manifest.status, "draft");
    assert.equal(manifest.git.sourceCommit, "pending");
    assert.equal(manifest.git.certificateCommit, "pending");
    assert.equal(manifest.git.dirtyAtCertifiedRun, true);
  }
});

test("keeps all 40 R0.70A-R0.71N releases continuous in HTML, PDF, route, and card publication", async () => {
  const { home } = await publishedPages();
  const routeMatch = [...home.matchAll(
    /<nav class="route-note-links"[^>]*>([\s\S]*?)<\/nav>/g,
  )].find((match) => match[1].includes('href="/notes/r0-71n.html"'));
  assert.ok(routeMatch);
  const releases = releaseSequence();
  assert.equal(releases.length, 40);

  const pdfs = await Promise.all(
    releases.map((slug) => readFile(new URL("notes/" + slug + ".pdf", publicRoot))),
  );
  await Promise.all(
    releases.map((slug) => access(new URL("notes/" + slug + ".html", publicRoot))),
  );

  for (let index = 0; index < releases.length; index += 1) {
    const slug = releases[index];
    const releaseId = slug.replaceAll("-", "");
    const link = 'href="/notes/' + slug + '.html"';
    const opening =
      '<div class="task-one" id="' +
      releaseId +
      '" data-release="' +
      releaseId +
      '"';
    assert.equal(occurrenceCount(home, opening), 1, releaseId);
    assert.equal(occurrenceCount(home, link), 2, slug);
    assert.equal(occurrenceCount(routeMatch[1], link), 1, "route " + slug);
    assert.equal(
      occurrenceCount(sliceReleaseCard(home, opening), link),
      1,
      "card " + slug,
    );
    assert.equal(
      pdfs[index].subarray(0, 5).toString("ascii"),
      "%PDF-",
      slug,
    );
    assert.ok(pdfs[index].length > 10_000, slug);
  }
});

test("screens the R0.71N publication against the discouraged wording in AGENTS.md", async () => {
  const [{ home, note, recap, literature }, instructions] = await Promise.all([
    publishedPages(),
    readFile(new URL("AGENTS.md", root), "utf8"),
  ]);
  for (const phrase of [
    "我们",
    "攻关",
    "主攻",
    "研究纪律",
    "三重审计",
    "杀死错误想法",
  ]) {
    assert.ok(instructions.includes(phrase), phrase);
  }

  const forbiddenInflation =
    /攻关|主攻|研究纪律|三重审计|杀死错误想法|重大突破|颠覆性|世界首个|接近解决|解决了千禧年|证明了全局正则性|原创性定理|首次证明/;
  const brokenTex =
    /(^|\n)u K\^|(^|\n)abla\b|(^|\n)imes\b|(^|\n)rac\b|\\!left\b|,qquad\b/m;

  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, forbiddenInflation);
    assert.doesNotMatch(page, /我们/);
    assert.doesNotMatch(
      page,
      /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/,
    );
    assert.doesNotMatch(page, /\t/);
    assert.doesNotMatch(page, brokenTex);
  }

  assert.match(note, /不是原创性、优先权或不存在性结论/);
  assert.match(note, /没有证明别的 NSE signed estimate 也会失败/);
  assert.match(note, /不是 outward-rounded interval sign theorem/);
  assert.match(note, /没有新的 continuation criterion/);
  assert.match(recap, /Clay 正式问题仍然开放/);
  assert.match(literature, /不把计算或笔记外推成正则性定理/);
});
