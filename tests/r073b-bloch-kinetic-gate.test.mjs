import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificate = "research/certificates/r073b";
const figure = "figures/r073b/fig-r073b-bloch-kinetic-transient";
const markdownTick = String.fromCharCode(96);
const expectedSourceStage = {
  release: "r073b",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r073b_report-source.md",
  problemFreeze: "research/r073b_problem_freeze.md",
  literatureAudit: "research/r073b_literature_audit.md",
  gapMatrix: "research/r073b_gap_matrix.md",
  analyticProof: "research/r073b_kinetic_form_proof.md",
  independentAudit: "research/r073b_independent_analytic_audit.md",
  independentAnalyticAudit: "research/r073b_independent_analytic_audit.md",
  producer: certificate + "/generate_certificate.py",
  independentProducer: certificate + "/independent_recompute.py",
  comparator: certificate + "/validate_certificate.py",
  certificateDirectory: certificate,
  experimentDirectory: "experiments/r073b",
  figureDirectory: figure,
  generator: "scripts/generate_r073b_release.py",
  translationScript: "scripts/add-r073b-translations.mjs",
  translationSnapshot: "scripts/i18n-snapshots/r073b-missing.json",
  releaseGate: "tests/r073b-bloch-kinetic-gate.test.mjs",
  publicationTest: "tests/r073b-release.test.mjs",
  certificateSourceTest: "tests/r073b-deterministic-certificate-source.test.mjs",
  figureSourceTest: "tests/r073b-bloch-kinetic-transient-figure-source.test.mjs",
};

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

function compact(value) {
  return value.replace(/\s+/g, "");
}

test("R0.73B closes the exact selected-carrier Bloch cancellation with endpoint and forcing qualifiers", async () => {
  const [report, audit, freeze] = await Promise.all([
    text("research/r073b_report-source.md"),
    text("research/r073b_independent_analytic_audit.md"),
    text("research/r073b_problem_freeze.md"),
  ]);
  const joined = compact(report + audit + freeze);
  for (const token of [
    "h=\\Pi_0(\\mathcalL^{-1}q)",
    "r=Q_0q",
    "q=gh+r",
    "\\Pi_0\\!\\left(Wr+W_{xx}\\mathcalL^{-1}r\\right)",
    "g\\Pi_0(W\\mathcalL^{-1}r)",
    "2i\\beta\\Pi_0(W_x\\mathcalL^{-1}r)",
    "\\frac{2c\\beta}{g}",
    "\\left|\\frac{2c\\beta}{g}\\right|\\le|\\Lambda|",
    "\\beta\\in[-1/2,1/2)",
    "g^{-1}\\Pi_0F_q",
  ]) assert.ok(joined.includes(compact(token)), token);
  assert.match(report, /zero-lattice\s+Bloch carrier coordinate/i);
  assert.match(report, /not.*unique.*slow mode/is);
  assert.match(audit, /both integrations by parts and the.*sign are exact/is);
});

test("R0.73B closes the complete physical kinetic row and direct sum at viscous rates", async () => {
  const [report, proof, audit] = await Promise.all([
    text("research/r073b_report-source.md"),
    text("research/r073b_kinetic_form_proof.md"),
    text("research/r073b_independent_analytic_audit.md"),
  ]);
  const joined = compact(report + proof + audit);
  for (const token of [
    "\\frac12\\frac d{dd}\\|u\\|_2^2",
    "\\|A_\\betau\\|_2^2+\\mu\\|u\\|_2^2",
    "\\|W_x(d)\\|_\\infty=\\frac12(e^{-d}+e^{-4d})",
    "K(s,d)=\\int_s^d\\|W_x(\\tau)\\|_\\infty",
    "=\\frac12(e^{-s}-e^{-d})+\\frac18(e^{-4s}-e^{-4d})",
    "\\|U_j(d,s)\\|",
    "-g_j(d-s)+\\frac{|\\Lambda|}{2}K(s,d)",
    "\\|u\\|_2^2=\\mu^{-1}",
    "\\|\\mathcalL^{-1/2}q\\|_2^2+\\|\\eta\\|_2^2",
    "e^{5|\\Lambda|e^{-s}/16}",
  ]) assert.ok(joined.includes(compact(token)), token);
  assert.match(report, /finite set of rows.*monotone convergence/is);
  assert.match(report, /orthogonal direct integral/i);
  assert.match(report, /projected forcing.*L\^1/is);
  assert.match(audit, /no missing factor two/i);
});

test("R0.73B proves the sharp shear-form limit and path-qualified negative results", async () => {
  const [report, proof, audit, gap] = await Promise.all([
    text("research/r073b_report-source.md"),
    text("research/r073b_kinetic_form_proof.md"),
    text("research/r073b_independent_analytic_audit.md"),
    text("research/r073b_gap_matrix.md"),
  ]);
  const joined = compact(report + proof + audit + gap);
  for (const token of [
    "S=-i\\left(W_x\\partial_x+\\frac12W_{xx}\\right)",
    "\\rho_\\mu(d)=\\sqrt\\mu\\left\\|\\mathcalL_\\mu^{-1/2}S",
    "\\lim_{\\mu\\downarrow0}\\rho_\\mu(d)=\\frac12\\|W_x(d)\\|_2",
    "0.188106027072",
    "\\Lambda^2A^2>4\\muB",
    "|\\Lambda|=\\frac{|c|}{\\sqrt\\mu}",
    "\\mu^{-1/2}",
  ]) assert.ok(joined.includes(compact(token)), token);
  assert.match(proof, /operator norm, not merely\s+entrywise/is);
  assert.match(audit, /four-mode projection stays nonzero/i);
  assert.match(report + proof, /not (?:the )?exact maximum transient\s+gain/is);
});

test("R0.73B source ledger separates ANALYTIC_PASS, FALSE, and OPEN without candidate states", async () => {
  const [report, gap] = await Promise.all([
    text("research/r073b_report-source.md"),
    text("research/r073b_gap_matrix.md"),
  ]);
  for (const claim of [
    "exactBlochNearCarrierCancellation", "exactBlochCarrierSystem",
    "blochNearCarrierFiniteTransient", "exactHeatShearGradientPrimitive",
    "completePhysicalKineticFiniteTransient", "completeOSSquireKineticFiniteTransient",
    "blochUniformPhysicalVelocityDirectSumAtViscousRates", "physicalKineticForcedDuhamel",
    "sharpKineticShearFormCoefficientAndLowGapLimit", "nearCarrierInstantaneousKineticGrowth",
  ]) {
    assert.ok(report.includes("\\texttt{" + claim + "}"), claim);
    assert.match(report, new RegExp("texttt\\{" + claim + "\\}[\\s\\S]{0,80}=\\\\texttt\\{ANALYTIC\\\\_PASS\\}"), claim);
    assert.ok(gap.includes("| " + markdownTick + claim + markdownTick + " | ANALYTIC PASS; CERT PENDING |"), claim);
  }
  for (const claim of [
    "lambdaIndependentKineticPrefactor", "fixedCUniformLowGapKineticPropagator",
    "allRowPrefactorOneKineticContraction",
  ]) {
    assert.match(report, new RegExp("texttt\\{" + claim + "\\}[\\s\\S]{0,80}=\\\\texttt\\{FALSE\\}"), claim);
    assert.ok(gap.includes("| " + markdownTick + claim + markdownTick + " | ANALYTICALLY FALSE; CERT PENDING |"), claim);
  }
  for (const claim of [
    "polynomiallySharpLambdaKineticPrefactor", "completeOSSquireA2DirectSum",
    "transportedAdjointPressureA2Modulation", "nonlinearNavierStokes", "Clay",
  ]) {
    assert.match(report, new RegExp("texttt\\{" + claim + "\\}[\\s\\S]{0,80}=\\\\texttt\\{OPEN\\}"), claim);
    assert.ok(gap.includes("| " + markdownTick + claim + markdownTick + " | OPEN |"), claim);
  }
  assert.equal(report.includes("TO_PROVE"), false);
  assert.equal(report.includes("TO_DISPROVE"), false);
});

test("R0.73B source-stage contract uses the same independent audit for both required keys", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r073a") {
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
    assert.deepEqual({
      version: manifest.siteVersion,
      notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount,
      next: manifest.nextRelease,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, {
      version: "1.40", notes: 177, recap: 117, next: "r073b",
      published: 79, sealed: 55, backlog: 24,
    });
  } else {
    assert.equal(manifest.latestCompletedRelease, "r073b");
    assert.equal(manifest.nextReleaseSourceStage, undefined);
  }
  assert.equal(expectedSourceStage.independentAudit, expectedSourceStage.independentAnalyticAudit);
  for (const relative of [
    ...new Set(Object.values(expectedSourceStage).filter((value) =>
      typeof value === "string" && value.includes("/"))),
    certificate + "/certificate.json", certificate + "/crosscheck.json",
    figure + "/contract.json", figure + "/config.json", figure + "/caption.md",
    figure + "/README.md", figure + "/plot.py", figure + "/validate.py",
  ]) await access(resolve(root, relative));
});

test("R0.73B finite experiment is complete, deterministic, and explicitly non-probative", async () => {
  const [manifest, contract, summary, validation] = await Promise.all([
    json("experiments/r073b/manifest.json"),
    json("experiments/r073b/contract.json"),
    json("experiments/r073b/summary.json"),
    json("experiments/r073b/validation.json"),
  ]);
  assert.equal(manifest.status, "completed");
  assert.equal(manifest.finiteDimensionalOnly, true);
  assert.deepEqual(manifest.configuration, { N: 10, caseCount: 280, dtMax: 0.0025, normCount: 7 });
  assert.equal(contract.expected.primaryRowCount, 1960);
  assert.equal(contract.expected.targetedRowCount, 245);
  assert.equal(contract.claimBoundary.infiniteDimensionalPropagatorProved, false);
  assert.equal(contract.claimBoundary.nonlinearNavierStokesProved, false);
  assert.equal(summary.caseCount, 280);
  assert.equal(summary.rowCount, 1960);
  assert.equal(summary.kineticFiniteBoundViolations, 0);
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.ok(validation.maximumStepRelativeDifference < 2e-12);
  assert.ok(validation.maximumModeRelativeDifference < 1e-14);
  assert.ok(validation.maximumTriangularLimitRelativeDifference < 8e-9);
});
