import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const root = new URL("../", import.meta.url);
const research = new URL("research/", root);
const certificateRoot = new URL("certificates/r070q/", research);

async function archivedResult() {
  return JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
}

test("locks the finite R0.70Q scope and its claim boundary", async () => {
  const [producer, readme, environment] = await Promise.all([
    readFile(new URL("r070q_exact_audit.py", research), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("environment.txt", certificateRoot), "utf8"),
  ]);

  for (const token of [
    "B_{ij}=\\partial_i u_j",
    "-2\\nu\\sum_k\\partial_k\\Omega\\otimes\\partial_k\\Omega",
    "curvature sign is negative",
    "a_N=(1+N^2)^{-1/2}",
    "does not prove",
    "does not rule out estimates that use",
  ]) {
    assert.ok(readme.includes(token), token);
  }
  assert.match(producer, /does not prove propagation for a covariance PDE/);
  assert.match(producer, /does not rule out estimates[\s\S]{0,80}higher Sobolev norms/);
  assert.match(environment, /not covariance-PDE propagation/);
  assert.match(environment, /not a higher-Sobolev obstruction/);
});

test("locks the canonical covariance ledger and aligned-state boundary", async () => {
  const report = await readFile(
    new URL("r070q_report-source.md", research),
    "utf8",
  );

  for (const token of [
    "\\mathscr L_\\nu\\omega=B^{\\mathsf T}\\omega",
    "\\mathscr L_\\nu Q",
    "=B^{\\mathsf T}Q+QB+\\mathcal F_Q-2\\nu\\mathcal H_Q",
    "\\mathscr L_\\nu r",
    "=P:\\mathscr L_\\nu Q+2\\nu\\mathcal K_Q",
    "Proposition 4.1 — Sharp rank-one diffusion absorption",
    "sharp aligned-state",
    "R,\\mathfrak C_P\\in L^2(0,T_{\\max})",
    "not a solution of the Navier--Stokes",
    "No public-page update or GitHub publication is authorized",
  ]) {
    assert.ok(report.includes(token), token);
  }

  assert.match(
    report,
    /\\mathcal K_Q[\s\S]{0,600}\\leq\\sum_\{\\alpha,k\}\|P\\partial_k\\Omega_\\alpha\|\^2/,
  );
  assert.match(
    report,
    /-2\\nu\\sum_\{\\alpha,k\}\|P\\partial_k\\Omega_\\alpha\|\^2[\s\S]{0,120}\+2\\nu\\mathcal K_Q\\leq0/,
  );
  assert.doesNotMatch(report, /proves global regularity/i);
});

test("reproduces the four-group exact R0.70Q producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070q_exact_audit.py", research));
  const archived = await archivedResult();
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70Q");
  assert.equal(archived.status, "exact-covariance-evolution-curvature-audit");
  assert.equal(Object.keys(archived.checks).length, 4);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the row-gradient covariance product rule", async () => {
  const archived = await archivedResult();
  const ledger = archived.singleBlockCovarianceLedger;

  assert.match(ledger.convention, /B_ij=partial_i u_j/);
  assert.match(ledger.convention, /B\^T\*omega/);
  assert.equal(ledger.viscousGradientSquareSign, "negative");
  assert.deepEqual(ledger.symbolicResidual, [
    ["0", "0", "0"],
    ["0", "0", "0"],
    ["0", "0", "0"],
  ]);
  assert.equal(ledger.traceResidual, "0");
  assert.equal(ledger.directPolynomialSample.nu, "2/7");
  assert.deepEqual(ledger.directPolynomialSample.residual, [
    ["0", "0", "0"],
    ["0", "0", "0"],
    ["0", "0", "0"],
  ]);
  assert.deepEqual(
    ledger.directPolynomialSample.leftAtPoint,
    ledger.directPolynomialSample.rightAtPoint,
  );
});

test("locks the simple-spectrum curvature signs", async () => {
  const archived = await archivedResult();
  const ledger = archived.simpleSpectrumLedger;
  const curvature = ledger.laplacianCurvature;

  assert.equal(ledger.firstDerivatives.symbolicValueInEigenbasis, "h11");
  assert.equal(
    ledger.firstDerivatives.residualValueInEigenbasis,
    "h22 + h33",
  );
  assert.equal(curvature.largestEigenvalueCurvatureSignUnderDelta, "positive");
  assert.equal(curvature.residualCurvatureSignUnderDelta, "negative");
  assert.equal(curvature.largestEigenvalueCurvatureSignUnderDNu, "negative");
  assert.equal(curvature.residualCurvatureSignUnderDNu, "positive");
  assert.equal(curvature.certificateConvention, "K=2*K_Q");

  const sample = ledger.rationalThreeCoordinateSample;
  assert.equal(sample.curvatureKQ, "3");
  assert.equal(sample.curvatureK, "6");
  assert.equal(sample.laplacianLargestEigenvalue, "11");
  assert.equal(sample.laplacianResidual, "-5");
  assert.equal(sample.tracePartitionResidual, "0");
});

test("locks the rotating Beltrami tight-frame identities", async () => {
  const archived = await archivedResult();
  const ledger = archived.rotatingBeltramiLedger;

  assert.equal(ledger.divergence, "0");
  assert.deepEqual(ledger.nonlinearity, ["0", "0", "0"]);
  assert.deepEqual(ledger.heatEquationResidual, ["0", "0", "0"]);
  assert.deepEqual(ledger.vorticityStretching, ["0", "0", "0"]);
  assert.equal(
    ledger.supportRestrictedScalarTightFrame.coefficientSquareSum,
    "1",
  );
  assert.equal(ledger.bestLineResidual, "0");
  assert.equal(ledger.relativeGap, "1");
  assert.equal(
    ledger.curvatureK,
    `2*${ledger.curvatureKQ}`,
  );
  assert.equal(ledger.projectorGradientFrobeniusSquared, "2*N**2");
  assert.equal(
    ledger.normalizedCovarianceGradientFrobeniusSquared,
    "2*N**2",
  );
  assert.equal(ledger.covarianceParabolicResidual.flat().every((x) => x === "0"), true);
  assert.equal(ledger.largestEigenvalueParabolicResidual, "0");
  assert.equal(ledger.transverseResidualParabolicResidual, "0");
});

test("locks the energy and H1 norm-map obstruction", async () => {
  const archived = await archivedResult();
  const ledger = archived.normMapObstructionLedger;

  assert.equal(ledger.amplitudeOne.initialL2NormSquared, "1");
  assert.equal(ledger.amplitudeOne.energyIdentityValue, "1");
  assert.equal(ledger.h1Normalized.initialH1NormSquared, "1");
  assert.equal(ledger.h1Normalized.bestLineResidual, "0");
  assert.equal(ledger.h1Normalized.relativeGap, "1");
  assert.equal(ledger.h1Normalized.projectorIsAmplitudeIndependent, true);
  assert.deepEqual(ledger.h1Normalized.nonlinearity, ["0", "0", "0"]);
  assert.deepEqual(ledger.h1Normalized.heatEquationResidual, ["0", "0", "0"]);
  assert.equal(ledger.unboundedness.projectorGradientLimit, "oo");
  assert.equal(ledger.unboundedness.normalizedCovarianceGradientLimit, "oo");
  assert.deepEqual(
    ledger.unboundedness.finiteFrequencySamples.map((sample) => sample.N),
    [1, 2, 4, 8, 16, 32],
  );
  assert.equal(ledger.higherSobolevBoundary.limit, "oo");
  assert.match(ledger.higherSobolevBoundary.meaning, /does not rule out/);
});

test("locks every R0.70Q certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070q_exact_audit\.py/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});
