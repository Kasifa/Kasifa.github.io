import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const certificatesRoot = new URL("research/certificates/r071m/", root);
const figureSourceRoot = new URL(
  "figures/r071m-increment-commutator/fig-r071m-increment-commutator-boundary/",
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
    readFile(new URL("notes/r0-71m.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71m.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("keeps note PDF rendering Chinese by default while preserving an explicit language", async () => {
  const renderer = await readFile(
    new URL("scripts/render-note-pdf.mjs", root),
    "utf8",
  );
  assert.match(renderer, /const renderUrl = new URL\(url\);/);
  assert.match(
    renderer,
    /if \(!renderUrl\.searchParams\.has\("lang"\)\) renderUrl\.searchParams\.set\("lang", "zh"\);/,
  );
  assert.match(renderer, /page\.goto\(renderUrl\.href,/);
});

test("keeps the R0.71M v0.98 note and 77-node recap archived", async () => {
  const { home, note, recap, literature } = await publishedPages();

  assert.equal((home.match(/href="\/notes\/r0-71m\.html"/g) ?? []).length, 2);
  const routeBlocks = [
    ...home.matchAll(/<nav class="route-note-links"[^>]*>([\s\S]*?)<\/nav>/g),
  ];
  assert.equal(
    routeBlocks.filter((match) =>
      match[1].includes('href="/notes/r0-71m.html"'),
    ).length,
    1,
  );

  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 12);
  assert.match(recap, /收录节点：77/);
  assert.match(recap, /回顾截止时公开笔记：137/);
  assert.match(recap, /回顾截止节点：R0\.71M/);

  for (const [page, minimum] of [
    [home, 10],
    [note, 17],
    [recap, 8],
    [literature, 49],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71M/);
  }
  for (const page of [note, recap]) {
    assert.match(page, /src="\/i18n-en\.js\?v=0\.98"/);
  }
});

test("enforces the R0.71M per-section publication invariant and one-card two-link homepage rule", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071m" data-release="r071m"';
  const homeCard = sliceReleaseCard(home, opening);

  assert.equal((home.match(new RegExp(opening, "g")) ?? []).length, 1);
  assert.equal((home.match(/href="\/notes\/r0-71m\.html"/g) ?? []).length, 2);
  for (const token of [
    'href="/notes/r0-71m.html"',
    'href="/notes/r0-71m.pdf"',
    'href="/figures/r0-71m-increment-commutator.pdf"',
    "research/certificates/r071m",
    "research/r071m_report-source.md",
    "figures/r071m-increment-commutator/fig-r071m-increment-commutator-boundary",
  ]) {
    assert.ok(homeCard.includes(token), token);
  }
  assert.match(homeCard, /<strong>结论边界：<\/strong>/);

  assert.match(note, /<title>R0\.71M｜增量交换子的精确公式与四行切向边界<\/title>/);
  assert.match(note, /href="\/notes\/r0-71m\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-71m\.html"/);
  assert.match(note, /href="\/recap-r0-61-r0-71m\.pdf"/);

  const recapNeedle = 'href="/notes/r0-71m.html"';
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
  assert.match(
    recapCard,
    /增量交换子|increment commutator|annular-filter Lamb commutator/i,
  );
  assert.match(recapCard, /href="\/figures\/r0-71m-increment-commutator\.pdf"/);
  assert.match(recapCard, /research\/certificates\/r071m/);

  const literatureMarker = "<header><b>R0.71M</b>";
  const literatureMarkerIndex = literature.indexOf(literatureMarker);
  const literatureCardStart = literature.lastIndexOf(
    '<div class="route-step',
    literatureMarkerIndex,
  );
  const literatureCardEnd = literature.indexOf("</div>", literatureMarkerIndex);
  assert.ok(literatureMarkerIndex >= 0);
  assert.ok(literatureCardStart >= 0);
  assert.ok(literatureCardEnd > literatureCardStart);
  const literatureCard = literature.slice(
    literatureCardStart,
    literatureCardEnd,
  );
  assert.match(literatureCard, /href="\/notes\/r0-71m\.html"/);
  assert.match(literatureCard, /四行|four-row/i);
});

test("states the exact increment, projective pairing, four-row bound, heat exponents, and claim boundary", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "\\mathcal R_j=T_j(u\\times\\omega)-u\\times W_j.",
    "\\frac12|\\delta_hu(x)|^2\\nabla_h\\phi_j(h)",
    "-\\bigl(\\nabla_h\\phi_j(h)\\cdot\\delta_hu(x)\\bigr)\\delta_hu(x)",
    "A_j+D_j=G_j=T_j\\operatorname{curl}(u\\times\\omega)",
    "\\langle P_QF_j,P_QM_Q\\rangle",
    "G_j-\\frac{B_Q}{d_Q}\\operatorname{curl}C_Q",
    "G_j+\\nu H_j",
    "\\frac12d_{Q,t}+\\nu\\kappa_j^2d_Q",
    "\\gamma_{j,Q}=\\frac{\\kappa_jB_Q^+}{Yd_Q}",
    "\\Theta_{j,Q}=\\gamma_{j,Q}\\kappa_j^{-3}",
    "3\\gamma_{j,Q}\\kappa_j^{-3}",
    "\\frac32\\gamma_{j,Q}\\kappa_j^{-3}",
    "\\|u_r(T)\\|_2^2+2\\nu\\int_0^T\\|\\nabla u_r\\|_2^2dt=1",
    "s_c-s_E=\\frac12",
    "\\mathcal J_Q=z_{Q,t}+\\nu\\kappa_j^2z_Q",
    "B_{Q,t}",
    "d_{Q,t}",
    "Y_t",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(note, /57\.17\\%.*上缘/);
  assert.ok(note.includes("\\(57.17\\%\\)"));
  assert.ok(note.includes("\\(O(\\kappa_j)\\)"));
  assert.ok(!note.includes("有 (57.17\\%\\)"));
  assert.ok(!note.includes("一般的 (O(\\kappa_j))"));
  assert.ok(!note.includes("audit：PASS"));
  assert.ok(!note.includes("</a>、<a"));
  assert.ok(!note.includes("</a>给出"));
  assert.ok(!note.includes("</a> 的 filtered"));
  const r071mLiteratureStart = literature.indexOf("<header><b>R0.71M</b>");
  const r071mLiteratureEnd = literature.indexOf("</div>", r071mLiteratureStart);
  const r071mLiteratureCard = literature.slice(
    r071mLiteratureStart,
    r071mLiteratureEnd,
  );
  assert.ok(!r071mLiteratureCard.includes("</a>、<a"));
  assert.ok(!r071mLiteratureCard.includes("</a>给出"));
  assert.ok(!r071mLiteratureCard.includes("</a>控制"));
  assert.ok(!home.includes("</a>允许"));
  assert.ok(!home.includes("</a>由 Hou"));
  assert.ok(!home.includes("</em>三维"));
  assert.ok(!literature.includes("保留在<a"));
  assert.ok(note.includes("一般没有 \\(O(\\kappa_j)\\) 的上频率支撑"));
  assert.match(note, /四行依次是 resolved transport、微分增量交换子、投影分母几何和黏性环带失配/);
  assert.match(note, /形式局部 Euclidean NSE 缩放/);
  assert.ok(
    note.includes("不是固定 \\(\\mathbb T^3\\) 与固定 cutoff 的连续对称性"),
  );
  assert.ok(note.includes("分别按 \\(r^{-2}\\)、\\(r^{-1}\\) 增长"));
  assert.ok(note.includes("normalized projected-Lamb 积分也按 \\(r^{-1}\\) 增长"));
  assert.match(note, /热包是线性热流，不是非线性 NSE 解族/);
  assert.match(note, /标准能量插值.*恰少半阶/);
  assert.match(note, /没有证明增量缺陷在逻辑上不能蕴含切向估计/);
  assert.match(note, /四行是当前直接 Cauchy 产生的充分账本，不是必要条件/);
  assert.match(note, /不是千禧年问题的解答/);
  assert.match(note, /不作新颖性、优先权或发表级别声明/);
  assert.ok(
    note.includes("R0.71N 从完整 \\(\\mathcal J_Q\\) 出发，同时保留三个时间导数"),
  );

  assert.match(home, /Cauchy\/Bernstein split/);
  assert.match(home, /R0\.71N/);
  assert.match(recap, /四行|four-row/i);
  assert.match(recap, /直接绝对估计产生四行临界充分账本/);
  assert.match(recap, /R0\.71N/);
  assert.match(literature, /Constantin|Duchon|Eyink|Yu/);
});

test("links and verifies the report, two audits, exact certificates, and journal figure package", async () => {
  const { note } = await publishedPages();
  const linkedSources = [
    "research/r071m_report-source.md",
    "research/r071m_literature_audit.md",
    "research/r071m_independent_audit.md",
    "research/r071m_gap_matrix.md",
    "research/r071m_exact_audit.py",
    "research/r071m_independent_audit.py",
    "research/certificates/r071m",
    "figures/r071m-increment-commutator/fig-r071m-increment-commutator-boundary",
  ];
  for (const source of linkedSources) assert.ok(note.includes(source), source);

  const sourceFiles = [
    "research/r071m_report-source.md",
    "research/r071m_literature_audit.md",
    "research/r071m_independent_audit.md",
    "research/r071m_gap_matrix.md",
    "research/r071m_exact_audit.py",
    "research/r071m_independent_audit.py",
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

  const [
    report,
    exactCertificate,
    independentCertificate,
    manifest,
    validation,
    independentValidation,
  ] = await Promise.all([
    readFile(new URL("research/r071m_report-source.md", root), "utf8"),
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

  assert.match(report, /Theorem 2\.1 — exact increment and projective bridge/);
  assert.ok(report.includes("\\Theta^{\\mathrm{abs}}_{j,Q}"));
  assert.ok(report.includes("\\gamma^{\\mathrm{abs}}_{j,Q}"));
  assert.match(
    report,
    /formal local Euclidean\s+scaling, co-scaling the filter length and physical cutoff/,
  );
  assert.match(
    report,
    /No such .*upper-frequency support\s+holds in general/,
  );
  assert.match(report, /Derivative-compatible quartic increment defect/);
  assert.ok(
    report.includes("\\mathbb P(\\Phi\\times\\operatorname{curl}\\Phi)\\ne0"),
  );
  assert.match(
    report,
    /not a\s+logical non-implication between the increment defect and the tangent/,
  );
  assert.match(
    report,
    /extra sufficient\s+critical hypothesis, not a necessary condition/,
  );
  assert.match(report, /No regularity or singularity conclusion follows/);

  assert.equal(exactCertificate.release, "R0.71M");
  assert.equal(exactCertificate.status, "passed");
  assert.equal(exactCertificate.lambIncrementIdentity.passed, true);
  assert.deepEqual(exactCertificate.lambIncrementIdentity.residual, ["0", "0", "0"]);
  assert.equal(exactCertificate.projectivePairingIdentity.passed, true);
  assert.equal(exactCertificate.projectivePairingIdentity.residual, "0");
  assert.equal(exactCertificate.absoluteFourRowEnvelope.passed, true);
  assert.equal(
    exactCertificate.absoluteFourRowEnvelope.bound,
    "Theta_abs_Q <= gamma_abs_Q*kappa^-3*[3(A_Q^2+D_Q^2)+(3/2)(K_Q^2+V_Q^2)]",
  );
  assert.equal(exactCertificate.heatPacketSeparation.uniformEnergyExponent, "0");
  assert.deepEqual(exactCertificate.heatPacketSeparation.divergentCriticalBudgets, {
    YuDerivativeCompatibleDefect: "-2",
    criticalCubicIncrementEnvelope: "-3/2",
    normalizedProjectedLambIntegral: "-1",
    velocitySquareCarlesonMass: "-1",
  });
  assert.equal(exactCertificate.heatPacketSeparation.interpolationGap, "s_critical-s_energy=1/2 in dimension three");
  assert.equal(exactCertificate.scaleLedger.gammaExponent, "0");
  assert.equal(exactCertificate.scaleLedger.kappaMinus3SourceSquareExponent, "0");
  assert.equal(exactCertificate.scaleLedger.weightedTangentExponent, "0");
  assert.match(exactCertificate.scaleLedger.scalingBoundary, /formal local Euclidean scaling/);
  assert.match(exactCertificate.claimBoundary, /no continuation criterion/);
  assert.match(exactCertificate.claimBoundary, /Millennium-problem result/);

  assert.equal(independentCertificate.release, "R0.71M");
  assert.equal(independentCertificate.status, "passed");
  assert.equal(independentCertificate.configuration.gridOrder, 64);
  assert.equal(independentCertificate.configuration.randomness, false);
  assert.equal(independentCertificate.configuration.timeStepping, false);
  assert.ok(independentCertificate.checks.incrementIdentityRelativeResidual < 1e-14);
  assert.ok(independentCertificate.checks.resolvedIncrementFusionRelativeResidual < 2e-14);
  assert.equal(independentCertificate.checks.projectivePairingRelativeResidual, 0);
  assert.ok(independentCertificate.checks.radialPairingRelativeResidual < 1e-14);
  assert.ok(
    Math.abs(
      independentCertificate.checks.commutatorHighOffBandEnergyFraction -
        0.5716554933770541,
    ) < 1e-15,
  );
  assert.ok(
    independentCertificate.checks.tangentEnvelope <
      independentCertificate.checks.fourRowUpperBound,
  );
  assert.match(independentCertificate.claimBoundary, /No PDE trajectory/);
  assert.match(independentCertificate.claimBoundary, /regularity result/);

  assert.equal(validation.status, "pass");
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.equal(validation.metrics.offBandEnergyFraction, 0.5716554933770541);
  assert.equal(independentValidation.status, "pass");
  assert.ok(Object.values(independentValidation.checks).every(Boolean));

  assert.equal(manifest.release, "R0.71M");
  assert.equal(manifest.figureId, "fig-r071m-increment-commutator-boundary");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 112);
  assert.equal(manifest.figure.outputs.find((output) => output.path === "figure.png").dpi, 600);
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.computation.dns, false);
  assert.equal(manifest.computation.fittedData, false);
  assert.equal(manifest.computation.pdeTimeStepping, false);
  assert.match(manifest.claimBoundary, /not claimed necessary/);
  assert.match(manifest.claimBoundary, /not an NSE solution counterexample/);
  assert.match(manifest.claimBoundary, /No logical defect-to-tangent non-implication/);
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
    readFile(new URL("notes/r0-71m.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71m.pdf", publicRoot)),
    readFile(new URL("figures/r0-71m-increment-commutator.svg", publicRoot)),
    readFile(new URL("figures/r0-71m-increment-commutator.pdf", publicRoot)),
    readFile(new URL("figures/r0-71m-increment-commutator.png", publicRoot)),
    readFile(new URL("figure.svg", figureSourceRoot)),
    readFile(new URL("figure.pdf", figureSourceRoot)),
    readFile(new URL("figure.png", figureSourceRoot)),
  ]);

  assert.match(note, /src="\/figures\/r0-71m-increment-commutator\.svg"/);
  assert.match(note, /href="\/notes\/r0-71m\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-71m\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-71m\.pdf"/);
  assert.match(home, /href="\/notes\/r0-71m\.pdf"/);
  assert.match(home, /href="\/figures\/r0-71m-increment-commutator\.pdf"/);

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

test("keeps R0.71M claims factual, scoped, and free of control characters or broken TeX escapes", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const forbiddenInflation =
    /攻关|主攻|研究纪律|三重审计|杀死错误想法|重大突破|颠覆性|世界首个|接近解决|解决了千禧年|证明了全局正则性|原创性定理|首次证明/;
  const brokenTex =
    /(^|\n)u K\^|(^|\n)abla\b|(^|\n)imes\b|(^|\n)rac\b|\\!left\b|,qquad\b/m;

  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, forbiddenInflation);
    assert.doesNotMatch(page, /我们/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /\t/);
    assert.doesNotMatch(page, brokenTex);
  }

  assert.match(note, /已关闭的是这一条直接插入，不是增量信息本身/);
  assert.match(note, /这只是已检查证明路线的结论/);
  assert.match(note, /未证明：已知增量缺陷在逻辑上不能控制 signed tangent/);
  assert.match(note, /未证明：四行账本是必要条件/);
  assert.match(note, /没有得到无条件继续性判据/);
  assert.match(recap, /Clay 正式问题仍然开放/);
  assert.match(literature, /不把计算或笔记外推成正则性定理/);
});
