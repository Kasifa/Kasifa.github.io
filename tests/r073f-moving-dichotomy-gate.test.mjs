import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const text = (relative) => readFile(resolve(root, relative), "utf8");

const closed = [
  "boundedPerturbationRoughnessWithNoninvertibleStableSemigroup",
  "movingProfileUniformSpectralStrip",
  "movingProfileUniformContour",
  "movingInstantaneousProjectionNormC1",
  "movingProfileEvolutionDichotomy",
  "movingUnstableFiberStartsAtFrozenTopSpace",
  "fixedSmallEndpointExponentialLowerLaw",
  "fixedWindowExponentialLowerLaw",
  "fixedWindowLogGainThetaLambda",
];

const falseClaims = [
  "frozenSpectralGapImpliesUniformDichotomy",
  "spectralGapPlusBoundedC1PlusCommonDomainImpliesMovingDichotomy",
  "instantaneousPositiveSpectralAbscissaImpliesFixedWindowGrowth",
];

const open = [
  "explicitWindowSize",
  "sharpExponentialRate",
  "normalizedLogGainLimitExists",
  "arbitraryEndpointBeyondSmallWindow",
  "dynamicProjectionEqualsInstantaneousRieszProjection",
  "singleEpsilonIndependentInitialOrbit",
  "certifiedSigmaStarIsRightmost",
  "inviscidEigenvalueSimple",
  "completeOSSquireA2DirectSum",
  "nonlinearNavierStokes",
  "Clay",
];

function assertPublicVoice(value, label) {
  for (const phrase of ["我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法"]) {
    assert.equal(value.includes(phrase), false, `${label}: ${phrase}`);
  }
}

test("R0.73F analytic chain closes the moving-profile theorem with conservative constants", async () => {
  const [freeze, proof, report, audit, gap] = await Promise.all([
    text("research/r073f_problem_freeze.md"),
    text("research/r073f_moving_dichotomy_proof.md"),
    text("research/r073f_report-source.md"),
    text("research/r073f_independent_analytic_audit.md"),
    text("research/r073f_gap_matrix.md"),
  ]);

  for (const key of closed) {
    assert.ok(gap.includes(`${key}=CLOSED`), `gap: ${key}`);
    assert.ok(report.includes(`${key}=CLOSED`), `report: ${key}`);
  }
  for (const key of falseClaims) {
    assert.ok(gap.includes(`${key}=FALSE`), `gap: ${key}`);
    assert.ok(report.includes(`${key}=FALSE`), `report: ${key}`);
  }
  for (const key of open) {
    assert.ok(gap.includes(`${key}=OPEN`) || gap.includes(`${key}=OPEN_NOT_USED`), `gap: ${key}`);
    assert.ok(report.includes(`${key}=OPEN`) || report.includes(`${key}=OPEN_NOT_USED`), `report: ${key}`);
  }

  for (const token of [
    "\\rho<\\frac{\\nu}{16K^2}",
    "q<\\frac1{6K}\\le\\frac16",
    "\\eta=\\frac\\nu2",
    "E^u_{\\varepsilon,d}(0)=P_\\varepsilon H",
    "d_D=\\min\\{D,d_0\\}",
    "\\frac{\\log G_{1/2}(\\Lambda;D)}{|\\Lambda|}",
    "\\le\\frac5{16}",
  ]) assert.ok(proof.includes(token) || report.includes(token) || audit.includes(token), token);

  assert.match(audit, /\*\*FINAL PASS\.\*\*/);
  assert.match(audit, /not an independent recertification of\s+R0\.73B, R0\.73C, or R0\.73E/);
  assert.ok(freeze.includes("complete all-row OS--Squire \\(A_2\\) direct-sum closure"));
  assert.ok(report.includes("For \\(D>d_0\\), the certified lower bound occurs at"));
  assert.ok(report.includes("No originality or priority claim is made"));
  for (const [value, label] of [[freeze, "freeze"], [proof, "proof"], [report, "report"], [audit, "audit"], [gap, "gap"]]) {
    assertPublicVoice(value, label);
  }
});

test("R0.73F proof defines one instantaneous projection before the contour formula", async () => {
  const proof = await text("research/r073f_moving_dichotomy_proof.md");
  const definition = proof.indexOf("Denote it by \\(P_\\varepsilon^{\\rm inst}(d)\\)");
  const laplace = proof.indexOf("\\tag{4.5}");
  const contour = proof.indexOf("\\tag{4.8}");
  assert.ok(definition >= 0 && definition < laplace && laplace < contour);
  assert.equal(proof.includes("P_{\\varepsilon,d}^{\\rm inst}"), false);
  assert.equal(proof.includes("rank one fixed positive integer"), false);
  assert.ok(proof.includes("R_{\\varepsilon,d}(z)\n =(z-\\widetilde B_\\varepsilon(d))^{-1}"));
});

test("R0.73F literature ledger records exact theorem scopes", async () => {
  const literature = await text("research/r073f_literature_audit.md");
  for (const token of [
    "Reviews in Mathematical Physics 31",
    "(2019), no. 5, 1950014",
    "Proposition 2.17 does **not** construct",
    "comparison evolution exists",
    "Condition 2.9",
    "\\(\\omega=0\\)",
    "\\(P\\in W_*^{2,1}\\)",
    "conditions (P1) and (ED)",
    "\\(L\\|\\phi\\|_1<1\\)",
    "pp. 28--37",
    "finite-dimensional linear ordinary differential equations",
    "hypothesis H3",
    "contraction-semigroup\nshift",
  ]) assert.ok(literature.includes(token), token);
  assert.equal(literature.includes("Mathematical Methods in the Applied Sciences 42"), false);
  assert.equal(literature.includes("original and comparison evolution systems"), false);
});

test("R0.73F counterexamples reject two invalid inference patterns without becoming model evidence", async () => {
  const [proof, report, audit] = await Promise.all([
    text("research/r073f_moving_dichotomy_proof.md"),
    text("research/r073f_report-source.md"),
    text("research/r073f_independent_analytic_audit.md"),
  ]);
  for (const token of [
    "D_N=\\begin{pmatrix}-N&N^2",
    "\\frac{N}{e}",
    "\\lambda_j(d)",
    "\\exp\\left(-\\frac{D}{4\\varepsilon}\\right)",
  ]) assert.ok(proof.includes(token) || report.includes(token), token);
  assert.match(audit, /not evidence about the Navier--Stokes Fourier row itself/);
  assert.doesNotMatch(proof + report, /Clay=(?:CLOSED|TRUE)/);
  assert.doesNotMatch(proof + report, /nonlinearNavierStokes=(?:CLOSED|TRUE)/);
});
