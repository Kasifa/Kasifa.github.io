import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const certificatesRoot = new URL("research/certificates/r071l/", root);
const figureSourceRoot = new URL(
  "figures/r071l-viscous-fusion/fig-r071l-viscous-fusion-gap/",
  root,
);

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
  return html.slice(start, end);
}

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71l.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71l.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("keeps the R0.71L v0.97 note and 76-node recap archived", async () => {
  const { home, note, recap, literature } = await publishedPages();

  assert.equal((home.match(/href="\/notes\/r0-71l\.html"/g) ?? []).length, 2);

  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 12);
  assert.match(recap, /收录节点：76/);
  assert.match(recap, /回顾截止时公开笔记：136/);
  assert.match(recap, /回顾截止节点：R0\.71L/);

  for (const [page, minimum] of [
    [home, 10],
    [note, 16],
    [recap, 8],
    [literature, 49],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71L/);
  }
  for (const page of [note, recap]) {
    assert.match(page, /src="\/i18n-en\.js\?v=0\.97"/);
  }
});

test("gives R0.71L independent release surfaces on home, note, recap, and literature", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071l" data-release="r071l"';
  const homeCard = sliceReleaseCard(home, opening);

  assert.equal((home.match(new RegExp(opening, "g")) ?? []).length, 1);
  for (const token of [
    'href="/notes/r0-71l.html"',
    'href="/notes/r0-71l.pdf"',
    'href="/figures/r0-71l-viscous-fusion.pdf"',
    "research/certificates/r071l",
    "research/r071l_report-source.md",
    "figures/r071l-viscous-fusion/fig-r071l-viscous-fusion-gap",
  ]) {
    assert.ok(homeCard.includes(token), token);
  }
  assert.match(homeCard, /<strong>结论边界：<\/strong>/);

  assert.match(note, /<title>R0\.71L｜黏性 collar 精确融合/);
  assert.match(note, /href="\/notes\/r0-71l\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-71l\.html"/);

  const recapNeedle = 'href="/notes/r0-71l.html"';
  const recapNeedleIndex = recap.indexOf(recapNeedle);
  const recapCardStart = recap.lastIndexOf(
    '<article class="phase">',
    recapNeedleIndex,
  );
  const recapCardEnd = recap.indexOf("</article>", recapNeedleIndex);
  const recapCard = recap.slice(recapCardStart, recapCardEnd);
  assert.ok(recapNeedleIndex >= 0);
  assert.ok(recapCardStart >= 0);
  assert.match(recapCard, /黏性融合|viscous fusion/i);
  assert.match(recapCard, /href="\/figures\/r0-71l-viscous-fusion\.pdf"/);
  assert.match(recapCard, /research\/certificates\/r071l/);

  const literatureMarker = "<header><b>R0.71L</b>";
  const literatureMarkerIndex = literature.indexOf(literatureMarker);
  const literatureCardStart = literature.lastIndexOf(
    '<div class="route-step',
    literatureMarkerIndex,
  );
  const literatureCardEnd = literature.indexOf(
    "</div>",
    literatureMarkerIndex,
  );
  const literatureCard = literature.slice(
    literatureCardStart,
    literatureCardEnd,
  );
  assert.ok(literatureMarkerIndex >= 0);
  assert.ok(literatureCardStart >= 0);
  assert.match(literatureCard, /href="\/notes\/r0-71l\.html"/);
  assert.ok(
    literatureCard.includes(
      "\\(\\nu\\mathsf A_Q(\\Delta+\\kappa^2)W_j\\)",
    ),
  );
});

test("states exact viscous and projective fusion with the aligned, denominator, Leray, and scaling boundaries", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "I=[t_0,t_1]",
    "\\chi_Q\\in W^{3,\\infty}",
    "r_Q(t)=\\|\\nabla\\times(\\chi_QW_j)(t)\\|_2&gt;0",
    "\\nu\\left[(\\Delta+\\kappa^2)C_Q",
    "-\\nabla\\times(\\mathcal K_{\\chi_Q}W_j)\\right]",
    "=\\nu\\mathsf A_Q(\\Delta+\\kappa^2)W_j.",
    "M_Q:=C_{Q,t}+\\nu\\kappa^2C_Q",
    "\\mathsf A_Q\\!\\left[\\nu(\\Delta+\\kappa^2)W_j+\\mathcal G_j\\right]",
    "(\\Delta+1)C=(0,0,-3\\varepsilon\\cos2x_1)",
    "x_{j,t}+\\lambda x_j",
    "E_{Q,t}=\\frac{P_QM_Q}{r_Q}",
    "=z_{Q,t}+\\lambda z_Q.",
    "(z_Q^+(t))^2-(z_Q^+(s))^2",
    "|\\mathcal Q_K|=K^3",
    "B_Q^\\partial=\\langle F_j,\\nabla\\chi_Q\\times W_j\\rangle",
    "\\sum_QB_Q^\\partial",
    "B_Q^\\partial=0.",
    "N^{-1}D_j\\le D_{\\rm loc}\\le C_{\\rm part}D_j.",
    "D_-:=\\frac12\\min_{0\\le\\theta\\le\\theta_*}D_0(\\theta)&gt;0",
    "D_+:=2\\max_{0\\le\\theta\\le\\theta_*}D_0(\\theta)&lt;\\infty",
    "D_-K^4\\le D_j(t)\\le D_+K^4",
    "I_{K,\\nu}:=[0,\\theta_*/(\\nu K^2)]",
    "\\frac{D_-}{N}K\\le d_Q\\le C_{\\rm part}D_+K.",
    "\\nu\\int\\sum_{j,Q}\\kappa_j^{-2}d_{j,Q}\\,dt",
    "\\kappa_j^{-6}\\|\\mathcal V_{j,Q}\\|_2^2dt",
    "\\Gamma_{j,Q}=\\frac{\\|M_{j,Q}^\\nu\\|_2}{\\nu\\kappa_j^2r_{j,Q}}",
    "\\operatorname{supp}\\chi_Q\\subset U_Q",
    "\\|\\nabla^m\\chi_Q\\|_\\infty\\le C_m\\kappa^m",
    "|z_{j,Q}|\\le\\frac{\\|1_{U_Q}F_j\\|_2}{\\sqrt Y}",
    "\\sum_j\\|F_j\\|_2^2\\le C_{\\rm frame}\\|L\\|_2^2",
    "\\int_I\\frac{\\|\\mathbb P(u\\times\\omega)\\|_2^2}{\\|\\omega\\|_2^2}dt",
    "z_Q=K^{-3/2}\\bigl(\\zeta(\\theta)+O_\\nu(K^{-1})\\bigr)",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(note, /raw collar 与局部 Laplacian 的交换子部分精确抵消/);
  assert.ok(note.includes("投影到 \\(E_Q^\\perp\\) 的余秩一正交投影"));
  assert.ok(note.includes("\\(I-P_Q=E_Q\\otimes E_Q\\) 才是秩一投影"));
  assert.ok(!note.includes("这里 \\(P_Q\\) 是 \\(L^2\\) Hilbert 空间中的秩一正交投影"));
  assert.match(note, /取开邻域/);
  assert.match(note, /cutoff–curl numerator 逐格精确为零/);
  assert.ok(note.includes("因为 \\(\\mathcal Q_K\\) 有限"));
  assert.match(note, /不是任意 Leray 解所有小区的 denominator floor/);
  assert.ok(note.includes("量词顺序是“固定 \\(\\nu\\)，再取充分大 \\(K\\)”"));
  assert.match(note, /仅由这两个已写出的不等式不能推出/);
  assert.match(note, /absolute viscous-tangent target/);
  assert.match(note, /这个判断只针对上述 direct estimate，不是 Leray-level no-go theorem/);
  assert.match(note, /Lamb 商的时间积分是尺度不变量，而能量与总耗散按/);
  assert.ok(note.includes("\\lambda^{-1}\\) 缩放"));
  assert.match(note, /严格排除的只是.*普适、齐次、线性的标准能量界/);
  assert.match(note, /A：.*exact algebra/);
  assert.match(note, /B：.*diagnostic，不是连续符号证书/);
  assert.match(note, /C：.*analytic \+ diagnostic mixed evidence/);
  assert.match(home, /当前 direct tangent Cauchy.*尚未从标准能量不等式推出/);
  assert.match(recap, /rowwise absolute collar route 关闭，但更深的 signed critical estimate 没有被排除/);
  assert.match(recap, /当前 direct estimate.*尚未从标准能量不等式推出/);
  assert.match(literature, /Dascaliuc|Leitmeyer/);
});

test("links and verifies the report, audits, exact certificates, and journal figure package", async () => {
  const { note } = await publishedPages();
  const linkedSources = [
    "research/r071l_report-source.md",
    "research/r071l_literature_audit.md",
    "research/r071l_independent_audit.md",
    "research/r071l_gap_matrix.md",
    "research/r071l_exact_audit.py",
    "research/r071l_independent_audit.py",
    "research/certificates/r071l",
    "figures/r071l-viscous-fusion/fig-r071l-viscous-fusion-gap",
  ];
  for (const source of linkedSources) assert.ok(note.includes(source), source);

  const sourceFiles = [
    "research/r071l_report-source.md",
    "research/r071l_literature_audit.md",
    "research/r071l_independent_audit.md",
    "research/r071l_gap_matrix.md",
    "research/r071l_exact_audit.py",
    "research/r071l_independent_audit.py",
  ];
  await Promise.all([
    ...sourceFiles.map((source) => access(new URL(source, root))),
    access(new URL("result.json", certificatesRoot)),
    access(new URL("independent-result.json", certificatesRoot)),
    access(new URL("SHA256SUMS", certificatesRoot)),
    access(new URL("manifest.json", figureSourceRoot)),
    access(new URL("validation.json", figureSourceRoot)),
    access(new URL("independent-validation.json", figureSourceRoot)),
    access(new URL("SHA256SUMS", figureSourceRoot)),
  ]);

  const [report, exactCertificate, independentCertificate, manifest, validation, independentValidation] =
    await Promise.all([
      readFile(new URL("research/r071l_report-source.md", root), "utf8"),
      readFile(new URL("result.json", certificatesRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-result.json", certificatesRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("manifest.json", figureSourceRoot), "utf8").then(JSON.parse),
      readFile(new URL("validation.json", figureSourceRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-validation.json", figureSourceRoot), "utf8").then(
        JSON.parse,
      ),
    ]);

  assert.match(report, /Theorem 2\.1 — fixed-cell recombination and the no-free-collar boundary/);
  assert.match(report, /Normalization and projective fusion/);
  assert.match(report, /zero cutoff--curl numerator cell by cell/);
  assert.match(report, /quantitative two-sided bound/);
  assert.match(report, /No global regularity or finite-time singularity conclusion follows/);

  assert.equal(
    exactCertificate.status,
    "fixed-cell-fusion-ledger-exact-algebra-passed",
  );
  assert.equal(exactCertificate.checks.fixedCutoffViscousFusion.passed, true);
  assert.equal(exactCertificate.checks.fixedCutoffViscousFusion.fusionResidual, "0");
  assert.equal(
    exactCertificate.checks.fixedCutoffViscousFusion.laplacianProductRuleResidual,
    "0",
  );
  assert.equal(
    exactCertificate.checks.fixedCutoffViscousFusion
      .explicitSingleEigenspaceCancellation.bothExpandedRowsNonzero,
    true,
  );
  assert.equal(
    exactCertificate.checks.fixedCutoffViscousFusion
      .explicitSingleEigenspaceCancellation.expandedResidual,
    "0",
  );
  assert.equal(
    exactCertificate.checks.normalizationProjectiveFiniteAlgebra.passed,
    true,
  );
  assert.deepEqual(
    exactCertificate.checks.normalizationProjectiveFiniteAlgebra
      .normalizationFusionResidual,
    ["0", "0", "0"],
  );
  assert.equal(
    exactCertificate.checks.normalizationProjectiveFiniteAlgebra.scalarResidual,
    "0",
  );
  assert.equal(
    exactCertificate.checks.normalizationProjectiveFiniteAlgebra.tangentResidual,
    "0",
  );
  assert.equal(exactCertificate.checks.helmholtzExactCancellation.passed, true);
  assert.deepEqual(
    exactCertificate.checks.helmholtzExactCancellation.curlCancellationResidual,
    ["0", "0", "0"],
  );
  assert.equal(exactCertificate.checks.alignedCutoffCurlNumerator.passed, true);
  assert.equal(
    exactCertificate.checks.alignedCutoffCurlNumerator.generalAlignedLogic
      .inferredCellBoundaryWork,
    "0",
  );
  assert.equal(exactCertificate.checks.denominatorTwoSidedScaleLedger.passed, true);
  assert.equal(
    exactCertificate.checks.denominatorTwoSidedScaleLedger.twoSidedCellBound,
    "D_minus*K/N_overlap <= d_Q <= C_part*D_plus*K",
  );
  assert.equal(
    exactCertificate.checks.denominatorTwoSidedScaleLedger.proofInputs.parentScale,
    "D_minus*K^4 <= D_parent <= D_plus*K^4",
  );
  assert.equal(
    exactCertificate.checks.denominatorTwoSidedScaleLedger.scalingExponentsInK
      .weightedCreationAllCells,
    "-2",
  );
  assert.equal(exactCertificate.checks.lerayPaymentBoundary.passed, true);
  assert.equal(
    exactCertificate.checks.lerayPaymentBoundary.normalizationBoundary
      .standardLerayLogEnstrophyBVProved,
    false,
  );
  assert.equal(
    exactCertificate.checks.lerayPaymentBoundary.rowwiseTangentYoungStep
      .identityResidual,
    "0",
  );
  assert.match(exactCertificate.claimBoundary, /does not prove a Leray-level no-go/);
  assert.match(exactCertificate.claimBoundary, /global regularity/);

  assert.equal(independentCertificate.status, "diagnostic-passed");
  assert.equal(independentCertificate.diagnosticOnly, true);
  assert.equal(independentCertificate.claims.fixedAlignedPartitionDiagnostic, true);
  assert.equal(independentCertificate.claims.viscousCollarRetained, true);
  assert.equal(independentCertificate.claims.arbitraryPartitionsChecked, false);
  assert.equal(independentCertificate.claims.continuousCollarSignCertified, false);
  assert.equal(independentCertificate.claims.finiteKNSETrajectoryComputed, false);
  assert.equal(independentCertificate.claims.lerayEnergyOnlyPaymentRejected, false);
  assert.equal(independentCertificate.claims.movingPartitionsChecked, false);
  assert.equal(independentCertificate.claims.regularityTheoremClaimed, false);
  assert.equal(independentCertificate.claims.signedFullFrameCancellationChecked, false);
  assert.equal(independentCertificate.sampledSignDiagnostics.continuousSignCertified, false);
  assert.equal(
    independentCertificate.scaling.pureHeatLeadingAggregate,
    "diagnostic coefficient*K^-2",
  );
  assert.equal(
    independentCertificate.scaling.finiteKTransfer.statement,
    "selected aggregate=coefficient*K^-2+O_nu(K^-3)",
  );
  assert.equal(
    independentCertificate.scaling.finiteKTransfer.zCell,
    "K^-3/2*(zeta+O_nu(K^-1))",
  );
  assert.equal(
    independentCertificate.scaling.finiteKTransfer.verifiedByThisChecker,
    false,
  );
  assert.ok(
    independentCertificate.identityDiagnostics.integratedScalarIdentityResidual <
      1e-18,
  );
  assert.ok(
    independentCertificate.identityDiagnostics.maximumScalarDifferentialResidual <
      1e-14,
  );
  assert.ok(
    independentCertificate.identityDiagnostics.maximumTangentFusionResidual <
      1e-14,
  );
  assert.match(independentCertificate.claimBoundary, /diagnostics, not interval proofs/);
  assert.match(independentCertificate.claimBoundary, /Navier-Stokes regularity/);

  assert.equal(validation.status, "pass");
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.equal(validation.metrics.maximumExactCancellationResidual, 0);
  assert.equal(independentValidation.status, "pass");
  assert.ok(Object.values(independentValidation.checks).every(Boolean));

  assert.equal(manifest.release, "R0.71L");
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.computation.dns, false);
  assert.equal(manifest.computation.fittedData, false);
  assert.equal(manifest.computation.pdeTimeStepping, false);
  assert.match(manifest.claimBoundary, /Millennium problem are not covered/);
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

test("ships synchronized note and recap PDFs plus byte-identical SVG, PDF, and PNG figure mirrors", async () => {
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
  ] = await Promise.all([
    publishedPages(),
    readFile(new URL("notes/r0-71l.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71l.pdf", publicRoot)),
    readFile(new URL("figures/r0-71l-viscous-fusion.svg", publicRoot)),
    readFile(new URL("figures/r0-71l-viscous-fusion.pdf", publicRoot)),
    readFile(new URL("figures/r0-71l-viscous-fusion.png", publicRoot)),
    readFile(new URL("figure.svg", figureSourceRoot)),
    readFile(new URL("figure.pdf", figureSourceRoot)),
    readFile(new URL("figure.png", figureSourceRoot)),
  ]);

  assert.match(note, /src="\/figures\/r0-71l-viscous-fusion\.svg"/);
  assert.match(note, /href="\/notes\/r0-71l\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-71l\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-71l\.pdf"/);
  assert.match(home, /href="\/notes\/r0-71l\.pdf"/);
  assert.match(home, /href="\/figures\/r0-71l-viscous-fusion\.pdf"/);

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
});

test("keeps R0.71L claims factual, scoped, and free of control characters or broken TeX escapes", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const forbiddenInflation =
    /攻关|主攻|研究纪律|三重审计|杀死错误想法|重大突破|颠覆性|世界首个|接近解决|解决了千禧年|证明了全局正则性|原创性定理|首次证明/;
  const brokenTex =
    /(^|\n)u K\^|(^|\n)abla\b|(^|\n)imes\b|(^|\n)rac\b|\\!left\b|,qquad\b/m;
  const absoluteR071LNoGo =
    /却不能支付剩余的归一化角速度乘积|却没有支付 fused projective tangent|却不支付 normalized projective tangent|却不能跨过局部分母/;

  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, forbiddenInflation);
    assert.doesNotMatch(page, /我们/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /\t/);
    assert.doesNotMatch(page, brokenTex);
    assert.doesNotMatch(page, absoluteR071LNoGo);
  }

  assert.match(note, /不是千禧年问题的解答/);
  assert.match(note, /不作新颖性、优先权或发表级别声明/);
  assert.match(note, /未证明：complete fused tangent/);
  assert.match(note, /未覆盖：general faces/);
  assert.match(recap, /Clay 正式问题仍然开放/);
  assert.match(literature, /不把计算或笔记外推成正则性定理/);
});
