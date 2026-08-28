import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificate = "research/certificates/r072z";
const figure = "figures/r072z/fig-r072z-os-squire-threshold";
const figureId = "fig-r072z-os-squire-threshold";

const expectedSourceStage = {
  release: "r072z",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072z_report-source.md",
  literatureAudit: "research/r072z_literature_audit.md",
  gapMatrix: "research/r072z_gap_matrix.md",
  independentAudit: "research/r072z_independent_audit.md",
  producer: "research/certificates/r072z/generate_certificate.py",
  independentProducer: "research/certificates/r072z/independent_recompute.py",
  comparator: "research/certificates/r072z/validate_certificate.py",
  certificateDirectory: certificate,
  figureDirectory: figure,
  generator: "scripts/generate_r072z_release.py",
  translationScript: "scripts/add-r072z-translations.mjs",
  releaseGate: "tests/r072z-os-squire-gate.test.mjs",
  publicationTest: "tests/r072z-release.test.mjs",
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

test("R0.72Z freezes the scoped claim boundary without promoting low-gap rows", async () => {
  const [report, gap, audit] = await Promise.all([
    text("research/r072z_report-source.md"),
    text("research/r072z_gap_matrix.md"),
    text("research/r072z_independent_audit.md"),
  ]);
  const compactReport = compact(report);
  for (const [label, status] of [
    ["exactOSFeedbackCommutatorIdentity", "CLOSED"],
    ["signedRelativeFormOSAbsorption", "CLOSED"],
    ["highGapOSPrefactorOneDecay", "CLOSED"],
    ["highGapOSForcedScaleLedger", "CLOSED"],
    ["alphaMinusTwoOSGapSufficiency", "CLOSED"],
    ["highModeOSGapExponentSharpness", "CLOSED"],
    ["exactGaplessOSTangentMode", "CLOSED"],
    ["exactSquireDuhamel", "CLOSED"],
    ["exactKineticOrientationNormalization", "CLOSED"],
    ["optimalInstantaneousSquireCoefficient", "CLOSED"],
    ["orientationUniformWithLambdaPayment", "CLOSED"],
    ["ordinaryGapSquireHistoryTransfer", "CLOSED"],
    ["strongKernelConditionalSquireTransfer", "CLOSED"],
    ["dampingGapConvolutionFormula", "CLOSED"],
    ["fixedRowOSSquireGraphRegularity", "CLOSED"],
    ["scalarA2AutomaticallyAbsorbsOSFeedbackAllStrongRows", "FALSE"],
    ["epsilonOnlyOSBoundedPerturbationGate", "FALSE"],
    ["allStrongRowsOSPrefactorOneContraction", "FALSE"],
    ["abstractGaplessOSA2StrictContraction", "FALSE"],
    ["rawOrientationUniformFromCOnly", "FALSE"],
    ["epsilonOnlySquireTransfer", "FALSE"],
    ["backgroundUniformEnergyBoundWithoutLambdaPayment", "FALSE"],
    ["uniformlyEquivalentLambdaIndependentContractiveNorm", "FALSE"],
    ["equalRateUniformGapDenominator", "FALSE"],
    ["instantaneousQEndpointAloneControlsEta", "FALSE"],
    ["lowGapOSTransientA2Propagator", "OPEN"],
    ["collisionScaleOSLimitingAbsorption", "OPEN"],
    ["unconditionalStrongFullRowA2Estimate", "OPEN"],
    ["BlochUniformPhysicalVelocityDirectSum", "OPEN"],
    ["lowGapWeakFullRows", "OPEN"],
    ["completeLinearizedShearSubsystem", "OPEN"],
    ["nonlinearNavierStokes", "OPEN"],
    ["Clay", "OPEN"],
  ]) {
    assert.ok(
      compactReport.includes("\\texttt{" + label + "}&=\\texttt{" + status + "}"),
      label + "=" + status,
    );
  }
  assert.ok(gap.includes("| `highGapOSPrefactorOneDecay` | CLOSED |"));
  assert.ok(gap.includes("| `lowGapOSTransientA2Propagator` | OPEN |"));
  assert.ok(gap.includes("| `rawOrientationUniformFromCOnly` | FALSE |"));
  assert.match(audit, /pressure commutator and sign \| PASS/);
  assert.match(audit, /full physical direct sum \| NOT PROVED/);
  assert.match(audit, /complete low-gap OS propagator/);
});

test("R0.72Z exact pressure form, threshold, and alpha power are present", async () => {
  const [report, osAudit] = await Promise.all([
    text("research/r072z_report-source.md"),
    text("research/r072z_os_independent_audit.md"),
  ]);
  const source = compact(report);
  for (const token of [
    "[D_\\beta,f]=-ih",
    "D_\\beta W_{xxx}+W_{xxx}D_\\beta",
    "\\Theta_K(c,\\beta,\\mu)",
    "\\|U_{\\rm OS}(d,s)\\|_{2\\to2}",
    "e^{-\\omega g(d-s)}",
    "g\\ge\\left(\\frac{|c|M_{3,K}}{\\theta_0}\\right)^{2/5}",
    "\\alpha^{-2}",
    "(\\xi^2+\\gamma^2+\\rho^2)^{5/2}",
  ]) assert.ok(source.includes(compact(token)), token);
  assert.match(osAudit, /commutator/i);
  assert.match(osAudit, /2\/5/);
  assert.match(osAudit, /strict scalar-style block factor/i);
});

test("R0.72Z keeps both exact negative OS witnesses scoped", async () => {
  const [report, audit] = await Promise.all([
    text("research/r072z_report-source.md"),
    text("research/r072z_independent_audit.md"),
  ]);
  const source = compact(report);
  for (const token of [
    "q_*(d)=W_{xx}(d)",
    "\\mathcal L_0^{-1}q_*=-W",
    "(q_*)_d=W_{xxxx}",
    "unprojected abstract Orr--Sommerfeld equation",
    "prefactor-one OS contraction is false",
  ]) assert.ok(source.includes(compact(token)), token);
  assert.match(audit, /exact tangent residual \| PASS/);
  assert.match(audit, /low-gap.*sharpness.*REJECTED/);
  assert.match(audit, /transient/i);
});

test("R0.72Z Squire transfer pays orientation, background, and history", async () => {
  const [report, squireAudit] = await Promise.all([
    text("research/r072z_report-source.md"),
    text("research/r072z_squire_independent_audit.md"),
  ]);
  const source = compact(report);
  for (const token of [
    "\\eta(d)={}&U_c(d,s)\\eta(s)",
    "a_j(d)=|\\xi\\Lambda|b_j(d)",
    "\\chi_j=\\frac{|\\xi|}{\\sqrt{\\xi^2+\\gamma^2+\\rho^2}}\\le1",
    "\\ell_j=\\min\\{g^{-1},A_\\vartheta\\alpha^2\\}",
    "m_j=\\min\\{(2g)^{-1/2},\\sqrt{B_\\vartheta}\\alpha\\}",
    "\\tau e^{-a\\tau}",
  ]) assert.ok(source.includes(compact(token)), token);
  assert.match(squireAudit, /orientation/i);
  assert.match(squireAudit, /history/i);
  assert.match(squireAudit, /equal-rate/i);
});

test("R0.72Z literature audit preserves primary precedents and search limits", async () => {
  const literature = await text("research/r072z_literature_audit.md");
  for (const token of [
    "Li--Wei--Zhang",
    "Jerome--Chomaz",
    "Jia",
    "Beekie--Chen--Jia",
    "Ding--Lin",
    "Wei--Zhang",
    "NOT FOUND IN THIS SEARCH",
  ]) assert.ok(literature.includes(token), token);
  assert.match(literature, /critical-point collision/i);
  assert.match(literature, /Squire/i);
  assert.match(literature, /no\s+priority claim/i);
});

test("R0.72Z source package binds the agreed release names", async () => {
  for (const relative of [
    "research/r072z_report-source.md",
    "research/r072z_gap_matrix.md",
    "research/r072z_literature_audit.md",
    "research/r072z_independent_audit.md",
    certificate + "/generate_certificate.py",
    certificate + "/independent_recompute.py",
    certificate + "/validate_certificate.py",
    figure + "/contract.json",
    figure + "/config.json",
    figure + "/README.md",
    figure + "/caption.md",
    "scripts/generate_r072z_release.py",
    "scripts/add-r072z-translations.mjs",
    "tests/r072z-deterministic-certificate-source.test.mjs",
    "tests/r072z-os-squire-figure-source.test.mjs",
    "tests/r072z-os-squire-gate.test.mjs",
    "tests/r072z-release.test.mjs",
  ]) assert.equal(await exists(relative), true, relative);
  const [contract, config, generator] = await Promise.all([
    json(figure + "/contract.json"),
    json(figure + "/config.json"),
    text("scripts/generate_r072z_release.py"),
  ]);
  assert.equal(contract.figureId, figureId);
  assert.equal(config.figureId, figureId);
  assert.ok(generator.includes('FIGURE_ID = "' + figureId + '"'));
  assert.ok(generator.includes('FIGURE_RELATIVE = f"figures/r072z/{FIGURE_ID}"'));
});

test("R0.72Z manifest is exact at source or formal lifecycle", async () => {
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
  if (observed.latest === "r072y") {
    assert.deepEqual(observed, {
      latest: "r072y", version: "1.38", notes: 175, recap: 115, next: "r072z",
      gate: "tests/r072y-full-row-forced-gate.test.mjs",
      publicationTest: "tests/r072y-release.test.mjs",
      published: 77, sealed: 53, backlog: 24,
    });
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
  } else {
    assert.deepEqual(observed, {
      latest: "r072z", version: "1.39", notes: 176, recap: 116, next: "r073a",
      gate: "tests/r072z-os-squire-gate.test.mjs",
      publicationTest: "tests/r072z-release.test.mjs",
      published: 78, sealed: 54, backlog: 24,
    });
    assert.equal(manifest.nextReleaseSourceStage, undefined);
  }
  if (process.env.R072Z_REQUIRE_SOURCE_STAGE === "1") {
    assert.equal(observed.latest, "r072y");
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
  }
});
