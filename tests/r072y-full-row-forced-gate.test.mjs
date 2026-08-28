import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificate = "research/certificates/r072y";
const figure = "figures/r072y/fig-r072y-full-row-forced-transfer";
const figureId = "fig-r072y-full-row-forced-transfer";

const expectedSourceStage = {
  release: "r072y",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072y_report-source.md",
  literatureAudit: "research/r072y_literature_audit.md",
  gapMatrix: "research/r072y_gap_matrix.md",
  independentAudit: "research/r072y_independent_audit.md",
  producer: "research/certificates/r072y/generate_certificate.py",
  independentProducer: "research/certificates/r072y/independent_recompute.py",
  comparator: "research/certificates/r072y/validate_certificate.py",
  certificateDirectory: certificate,
  figureDirectory: figure,
  generator: "scripts/generate_r072y_release.py",
  translationScript: "scripts/add-r072y-translations.mjs",
  releaseGate: "tests/r072y-full-row-forced-gate.test.mjs",
  publicationTest: "tests/r072y-release.test.mjs",
};

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function exists(relative) {
  try {
    await access(resolve(root, relative));
    return true;
  } catch (error) {
    if (error?.code === "ENOENT") return false;
    throw error;
  }
}

function compact(value) {
  return value.replace(/\s+/g, "");
}

test("R0.72Y freezes the exact claim boundary without promoting the full row", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072y_report-source.md"),
    text("research/r072y_gap_matrix.md"),
    text("research/r072y_independent_audit.md"),
  ]);
  for (const [label, status] of [
    ["exactThreeDimensionalLinearization", "CLOSED"],
    ["exactPressurePoissonFactorTwo", "CLOSED"],
    ["exactBlochLerayNormalization", "CLOSED"],
    ["exactFourierRowDirectSum", "CLOSED"],
    ["exactOSSquireTriangularization", "CLOSED"],
    ["exactVelocityReconstruction", "CLOSED"],
    ["fullRowEnergyIdentity", "CLOSED"],
    ["dampingDominatedFullRows", "CLOSED"],
    ["muZeroRowsSeparated", "CLOSED"],
    ["exactZeroCouplingLiftUpFormula", "CLOSED"],
    ["meanZeroLiftUpCounterexample", "CLOSED"],
    ["scalarA2InvariantEmbedding", "CLOSED"],
    ["strongRowL2ForcingDuhamelAlpha2", "CLOSED"],
    ["strongRowStandardHMinusOneTransferAlpha", "CLOSED"],
    ["strongRowSemiclassicalHMinusOneTransferAlpha2", "CLOSED"],
    ["strongRowForcedEndpointStandardScaleOne", "CLOSED"],
    ["strongForcedDirectSumNoCountLoss", "CLOSED"],
    ["weakZeroFiniteHistoryEnergyLedger", "CLOSED"],
    ["scalarA2EqualsCompleteRow", "FALSE"],
    ["epsilonOnlyFullRowClosure", "FALSE"],
    ["allPhysicalRowsUniformStrictContraction", "FALSE"],
    ["standardHMinusOneTransferAlpha2", "FALSE"],
    ["HMinusOneEndpointAlphaGain", "FALSE"],
    ["allRowsStrongScaleForcedGain", "FALSE"],
    ["strongFullRowA2Estimate", "OPEN"],
    ["scaleSharpOSPressureAbsorption", "OPEN"],
    ["orientationUniformSquireTransfer", "OPEN"],
    ["lowGapWeakFullRows", "OPEN"],
    ["completeLinearizedShearSubsystem", "OPEN"],
    ["nonlinearNavierStokes", "OPEN"],
    ["Clay", "OPEN"],
  ]) {
    assert.ok(
      report.includes("\\texttt{" + label + "}&=\\texttt{" + status + "}"),
      label + "=" + status,
    );
  }
  assert.ok(gap.includes("| Complete strong-row \\(A_2\\) estimate | **OPEN** |"));
  assert.ok(gap.includes(
    "| Mean-zero full-row contraction based only on \\(\\varepsilon_j\\) | **FALSE** |",
  ));
  assert.match(audit, /\*\*Outcome:\*\* \*\*PASS\*\*/);
  assert.match(audit, /\*\*Final verdict:\*\* R0\.72Y is mathematically publishable/);
  assert.match(audit, /not a full-row enhanced-dissipation theorem/);
});

test("R0.72Y pressure, Leray, OS--Squire, and recovery signs are exact", async () => {
  const [report, audit, producer] = await Promise.all([
    text("research/r072y_report-source.md"),
    text("research/r072y_independent_audit.md"),
    text(certificate + "/generate_certificate.py"),
  ]);
  const reportCompact = compact(report);
  for (const token of [
    "\\Delta_Kp=-2iK_zV_yv",
    "\\operatorname{div}_j\\nabla_j=-\\mathcal L",
    "\\mathbb P_j=I+\\nabla_j\\mathcal L^{-1}\\operatorname{div}_j",
    "q_d=(-\\mathcal L-icW)q-icW_{xx}\\mathcal L^{-1}q",
    "\\eta_d=(-\\mathcal L-icW)\\eta",
    "+i\\xi\\Lambda W_x\\mathcal L^{-1}q",
    "u_1=\\frac{i}{\\mu}",
    "u_3=\\frac{i}{\\mu}",
    "\\frac1\\mu",
  ]) assert.ok(reportCompact.includes(compact(token)), token);
  for (const token of [
    "Pressure and Leray signs",
    "Orr--Sommerfeld--Squire audit",
    "Recovery and exceptional-row audit",
    "\\mu=0",
  ]) assert.ok(audit.includes(token), token);
  for (const token of [
    '"pressureFactorTwo"',
    '"blochLaplacianSign"',
    '"lerayDivergenceCancellation"',
    '"osCoefficientCancellation"',
    '"squirePressureCancellation"',
    '"velocityMatrixIdentity"',
  ]) assert.ok(producer.includes(token), token);
});

test("R0.72Y preserves the exact lift-up counterexample including mean-zero rows", async () => {
  const [report, audit, producer] = await Promise.all([
    text("research/r072y_report-source.md"),
    text("research/r072y_independent_audit.md"),
    text(certificate + "/generate_certificate.py"),
  ]);
  const reportCompact = compact(report);
  for (const token of [
    "v(d_2)=e^{-\\xi^2\\tau}v_0",
    "u_3(d_2,x)=-\\Lambda\\tau e^{-\\xi^2\\tau}W_x(d_2,x)v_0",
    "\\frac{\\Lambda^2\\tau^2}{8}",
    "e^{-2d_2}+e^{-8d_2}",
    "\\xi>0",
    "spatially mean-zero",
  ]) assert.ok(reportCompact.includes(compact(token)), token);
  assert.match(audit, /Exact lift-up counterexample/);
  assert.match(audit, /spatially mean\s+zero/);
  for (const token of [
    '"zeroCouplingLiftUp"',
    '"u2ResidualCoefficient"',
    '"u3ResidualAfterCommonFactor"',
    '"meanSquareCoefficientsForExpMinus2dAndExpMinus8d"',
    '"liftUpResidual"',
    '"liftUpNorm"',
  ]) assert.ok(producer.includes(token), token);
});

test("R0.72Y distinguishes every scalar forcing topology and endpoint", async () => {
  const [report, audit, producer] = await Promise.all([
    text("research/r072y_report-source.md"),
    text("research/r072y_independent_audit.md"),
    text(certificate + "/generate_certificate.py"),
  ]);
  const reportCompact = compact(report);
  for (const token of [
    "\\frac{1-e^{-p\\mu h}}{p\\mu(1-q^pe^{-p\\mu h})}",
    "\\frac h{1-q^p}",
    "A_q=\\frac{2T}{1-q}",
    "B_q=\\frac{2T}{1-q^2}",
    "\\alpha^2\\|F\\|_{L_d^2\\mathcal H^{-1}_{\\alpha,\\beta}}",
    "\\alpha\\|F\\|_{L_d^2H^{-1}_\\beta}",
    "\\max\\left\\{",
    "C_q'=\\max",
  ]) assert.ok(reportCompact.includes(compact(token)), token);
  assert.match(audit, /Causal-kernel audit/);
  assert.match(audit, /Negative-Sobolev duality audit/);
  assert.match(audit, /Endpoint-constant audit/);
  for (const token of [
    '"causalKernelGeometricAlgebra"',
    '"causalKernelZeroDampingAlgebra"',
    '"standardSemiclassicalFourierWeightComparison"',
    '"strongRowStandardHMinusOneTransferAlpha"',
    '"strongRowSemiclassicalHMinusOneTransferAlpha2"',
    '"HMinusOneEndpointNoAlphaGainSharpness"',
  ]) assert.ok(producer.includes(token), token);
});

test("R0.72Y literature audit does not erase existing forced/vector precedents", async () => {
  const literature = await text("research/r072y_literature_audit.md");
  for (const token of [
    "Coble--He",
    "Wei--Zhang",
    "Propositions 3.3--3.5",
    "nonautonomous forced enhanced-dissipation estimates",
    "vector/triangular coupling",
    "\\partial_yV=0",
    "不是穷尽性 novelty search",
    "不能改写成“全球首次”",
  ]) assert.ok(literature.includes(token), token);
  assert.match(literature, /critical-point collision\/change of count/);
  assert.match(literature, /complete linearized vector row/);
});

test("R0.72Y source package binds the agreed names", async () => {
  for (const relative of [
    "research/r072y_report-source.md",
    "research/r072y_gap_matrix.md",
    "research/r072y_literature_audit.md",
    "research/r072y_independent_audit.md",
    certificate + "/generate_certificate.py",
    certificate + "/independent_recompute.py",
    certificate + "/validate_certificate.py",
    figure + "/contract.json",
    figure + "/config.json",
    figure + "/README.md",
    figure + "/caption.md",
    "scripts/generate_r072y_release.py",
    "scripts/add-r072y-translations.mjs",
    "tests/r072y-deterministic-certificate-source.test.mjs",
    "tests/r072y-full-row-forced-gate.test.mjs",
    "tests/r072y-full-row-forced-transfer-figure-source.test.mjs",
    "tests/r072y-release.test.mjs",
  ]) assert.equal(await exists(relative), true, relative);
  const [contract, config, generator] = await Promise.all([
    json(figure + "/contract.json"),
    json(figure + "/config.json"),
    text("scripts/generate_r072y_release.py"),
  ]);
  assert.equal(contract.figureId, figureId);
  assert.equal(config.figureId, figureId);
  assert.ok(generator.includes('FIGURE_ID = "' + figureId + '"'));
  assert.ok(generator.includes('FIGURE_RELATIVE = f"figures/r072y/{FIGURE_ID}"'));
});

test("R0.72Y manifest is exact at source or formal lifecycle", async () => {
  const manifest = await json("research/release-manifest.json");
  const observed = {
    latest: manifest.latestCompletedRelease,
    version: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount,
    recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease,
    gate: manifest.latestReleaseGate,
    publicationTest: manifest.latestReleasePublicationTest,
    published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  };
  if (observed.latest === "r072x") {
    assert.deepEqual(observed, {
      latest: "r072x", version: "1.37", notes: 174, recap: 114,
      next: "r072y",
      gate: "tests/r072x-exact-path-gate.test.mjs",
      publicationTest: "tests/r072x-release.test.mjs",
      published: 76, sealed: 52, backlog: 24,
    });
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
  } else {
    assert.deepEqual(observed, {
      latest: "r072y", version: "1.38", notes: 175, recap: 115,
      next: "r072z",
      gate: "tests/r072y-full-row-forced-gate.test.mjs",
      publicationTest: "tests/r072y-release.test.mjs",
      published: 77, sealed: 53, backlog: 24,
    });
    assert.equal(manifest.nextReleaseSourceStage, undefined);
  }
  if (process.env.R072Y_REQUIRE_SOURCE_STAGE === "1") {
    assert.equal(observed.latest, "r072x");
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
  }
});
