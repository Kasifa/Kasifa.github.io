import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const figureRoot = "figures/r073l/fig-r073l-adiabatic-tracking";

const researchFiles = [
  "research/r073l_problem_freeze.md",
  "research/r073l_gap_matrix.md",
  "research/r073l_literature_audit.md",
  "research/r073l_adiabatic_tracking_proof.md",
  "research/r073l_independent_analytic_audit.md",
  "research/r073l_adversarial_audit.md",
  "research/r073l_finite_diagnostic_audit.md",
  "research/r073l_report-source.md",
];

function rejectUndelimitedInlineMath(markdown) {
  let display = false;
  let fence = false;
  for (const [index, line] of markdown.split("\n").entries()) {
    if (line.trim().startsWith("```")) {
      fence = !fence;
      continue;
    }
    if (fence) continue;
    if (line.trim() === "\\[") {
      display = true;
      continue;
    }
    if (line.trim() === "\\]") {
      display = false;
      continue;
    }
    if (display) continue;
    const residual = line.replace(/\\\([^\n]*?\\\)/g, "");
    assert.doesNotMatch(
      residual,
      /(^|[^\\])\([^)]*\\(?:varepsilon|lambda|Phi|nu|times|exp|in|le|ge|to|mathcal|mathrm|text|delta|gamma|sup|int|frac|left|right|\|)/,
      "undelimited inline math at line " + String(index + 1),
    );
  }
}

test("R0.73L continuum theorem closes the frozen L1--L8 obligations", async () => {
  const [freeze, gap, literature, proof, analytic, adversarial, report] =
    await Promise.all([
      text(researchFiles[0]), text(researchFiles[1]), text(researchFiles[2]),
      text(researchFiles[3]), text(researchFiles[4]), text(researchFiles[5]),
      text(researchFiles[7]),
    ]);
  for (const token of [
    "0<\\varepsilon_L\\le\\varepsilon_K",
    "[P,\\mathcal K]=-P'",
    "+\\mathcal K(d)",
    "-\\int_0^dU^{\\rm a}",
    "Q_K\\delta_T(\\varepsilon)",
    "4M_W^3P_K\\kappa_KD_*C_Q\\varepsilon_L\\le1",
    "vector-level relative tracking estimate",
    "real-analytic dependence",
  ]) assert.ok(proof.includes(token), token);
  assert.match(proof, /No backward evolution of .*Q\(d\)H.* is used/s);
  assert.match(analytic, /\*\*Status:\*\* PASS/);
  assert.match(adversarial, /\*\*Status:\*\* PASS/);
  for (let index = 1; index <= 8; index += 1) {
    assert.match(gap, new RegExp("\\| L" + index + " \\|[^\\n]+\\| CLOSED"), "L" + index);
  }
  assert.match(gap, /\| F1 \|[^\n]+\| PRIMARY PASS; independent validation PASS; FIGURE PASS/);
  assert.match(freeze, /\| L8 \| theorem-boundary and literature audit/);
  for (const stale of ["待完成", "R0.73L seeks", "Subject to the two", "closes this gap directly"]) {
    for (const source of [literature, proof, report]) {
      assert.equal(source.includes(stale), false, stale);
    }
  }
  rejectUndelimitedInlineMath(report);
});

test("R0.73L finite package passes independently and remains finite-only", async () => {
  const [manifest, primary, independent, packageValidation] = await Promise.all([
    json("experiments/r073l/manifest.json"),
    json("experiments/r073l/adiabatic_diagnostic.json"),
    json("experiments/r073l/independent_validation.json"),
    json("experiments/r073l/package_validation.json"),
  ]);
  assert.equal(manifest.schemaVersion, "r073l-finite-diagnostic-manifest-v1");
  assert.equal(manifest.status, "sealed");
  assert.ok(Object.values(manifest.checks).every(Boolean));
  assert.equal(manifest.claimBoundary.finiteDimensionalDiagnosticSealed, true);
  assert.equal(manifest.claimBoundary.continuumTheoremCertifiedByManifest, false);
  assert.equal(manifest.claimBoundary.clayProblemSolved, false);
  assert.equal(primary.status, "passed");
  assert.equal(primary.allChecksPass, true);
  assert.equal(primary.cases.length, 15);
  assert.equal(primary.claimBoundary.finiteScalingIsContinuumProof, false);
  assert.equal(primary.claimBoundary.finiteCutoffAgreementIsContinuumProof, false);
  assert.equal(primary.claimBoundary.nonlinearNavierStokesProvedHere, false);
  assert.equal(primary.claimBoundary.clayProblemSolved, false);
  assert.ok(Math.abs(primary.maximums.backwardActionResidualAbs - 6.711726362969017e-4) < 1e-15);
  assert.ok(Math.abs(primary.epsilonScalingByCutoff["64"].terminalLeakageTailThreeLogLogSlope - 1.0281276356834264) < 1e-13);
  assert.deepEqual(primary.epsilonScalingByCutoff["64"].terminalNormalizedGainRange,
    [0.9993290525496814, 0.9998284900372003]);
  assert.ok(primary.maximums.largestPairTerminalNormalizedGainDifference < 7e-15);
  assert.ok(primary.maximums.largestPairTerminalLeakageRatioDifference < 3.2e-15);
  assert.equal(independent.status, "passed");
  assert.equal(independent.cases.length, 5);
  assert.equal(independent.claimBoundary.continuumProof, false);
  assert.ok(independent.maximums.finestVsPrimaryNormalizedGain < 1.9e-9);
  assert.ok(independent.maximums.finestVsPrimaryLeakage < 1.8e-9);
  assert.equal(packageValidation.status, "passed");
  assert.equal(packageValidation.allChecksPass, true);
  assert.ok(Object.values(packageValidation.checks).every(Boolean));
});

test("R0.73L formal figure is sealed, vector, 600 dpi, and diagnostic-only", async () => {
  const [manifest, results, validation] = await Promise.all([
    json(figureRoot + "/manifest.json"),
    json(figureRoot + "/results.json"),
    json(figureRoot + "/validation.json"),
  ]);
  assert.equal(manifest.figureId, "fig-r073l-adiabatic-tracking");
  assert.equal(manifest.release, "R0.73L");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figure.outputs.length, 3);
  assert.equal(manifest.figure.outputs.find((row) => row.path === "figure.png").dpi, 600);
  assert.equal(manifest.claimBoundary.finiteDimensionalDiagnostic, true);
  for (const key of [
    "continuumAdiabaticTheoremCertifiedByFigure",
    "explicitContinuumEpsilonThresholdCertified", "prefactorLimitCertified",
    "nonlinearNavierStokesCertified", "transverseThreeDimensionalClosureCertified",
    "finiteTimeSingularityCertified", "clayProblemSolved",
  ]) assert.equal(manifest.claimBoundary[key], false, key);
  assert.equal(results.status, "passed");
  assert.equal(results.allChecksPass, true);
  assert.equal(results.sourceRows, 346);
  assert.equal(validation.status, "passed");
  assert.equal(validation.allChecksPass, true);
  assert.ok(Object.values(validation.checks).every(Boolean));

  const python = process.env.CODEX_PYTHON || "python3";
  const run = spawnSync(
    python,
    ["research/validate_figure_package.py", figureRoot],
    { cwd: root, encoding: "utf8" },
  );
  assert.ifError(run.error);
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const report = JSON.parse(run.stdout);
  assert.deepEqual(report.errors, []);
  assert.deepEqual(report.warnings, []);
});

test("R0.73L reader-facing research sources use restrained individual voice", async () => {
  const sources = await Promise.all(researchFiles.map(text));
  for (const phrase of ["我们", "攻关", "主攻", "突破", "杀死错误想法"]) {
    for (const source of sources) assert.equal(source.includes(phrase), false, phrase);
  }
});
