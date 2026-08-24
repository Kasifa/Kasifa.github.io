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
const certificateRoot = new URL("certificates/r070t/", research);

async function archivedResult() {
  return JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
}

function everyEntryEquals(matrix, expected) {
  return matrix.flat(Infinity).every((value) => value === expected);
}

test("locks the R0.70T theorem scopes and curvature convention", async () => {
  const [report, readme, producer, environment] = await Promise.all([
    readFile(new URL("r070t_report-source.md", research), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("r070t_exact_audit.py", research), "utf8"),
    readFile(new URL("environment.txt", certificateRoot), "utf8"),
  ]);

  for (const token of [
    "R0.70T — Exact frame stretching and a sharp fixed-frame divergence defect",
    "[T_\\alpha,S]\\omega",
    "global simple-top hypothesis",
    "\\mathcal R_Q",
    "exact half-curvature normalization",
    "|\\nabla P|_F^2=2",
    "T_{\\max}<\\infty",
    "without assuming that both possible indices are active",
    "tautological, not progress",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /smooth\s+global unforced periodic Navier--Stokes solution/);
  assert.match(
    report,
    /only a reassembly[\s\S]{0,80}original\s+stretching identity/,
  );
  assert.match(report, /No public-page\s+update or GitHub publication/);

  for (const token of [
    "whole-torus Section 5 ledger without its global simple-top hypothesis",
    "half-curvature convention",
    "both \\(T_{\\max}<\\infty\\)",
  ]) {
    assert.ok(readme.includes(token), token);
  }
  assert.match(readme, /does not verify those\s+hypotheses from initial data/);
  assert.match(readme, /identically\s+zero vortex stretching/);

  assert.match(producer, /not inferred from these\s+finite checks/);
  assert.match(environment, /not uniform near-rank propagation/);
  assert.doesNotMatch(report, /common-origin realization is a separate gate/i);
  assert.doesNotMatch(report, /common-vorticity fixed-frame realization.*not proved/i);
  assert.doesNotMatch(report, /proves (a )?finite-time singularity/i);
  assert.doesNotMatch(report, /proves unconditional global regularity/i);
});

test("reproduces the five-group exact R0.70T producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070t_exact_audit.py", research));
  const archived = await archivedResult();
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70T");
  assert.equal(
    archived.status,
    "exact-frame-stretching-divergence-defect-audit",
  );
  assert.equal(Object.keys(archived.checks).length, 5);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the nonzero rational Parseval commutator", async () => {
  const ledger = (await archivedResult()).finiteParsevalLedger;

  assert.deepEqual(ledger.parsevalResolution, [
    ["1", "0"],
    ["0", "1"],
  ]);
  assert.equal(ledger.leftSide, "10");
  assert.deepEqual(ledger.covarianceTerms, ["12242/4225", "28448/4225"]);
  assert.equal(ledger.covarianceTotal, "626/65");
  assert.deepEqual(ledger.commutatorTerms, ["1176/4225", "384/4225"]);
  assert.equal(ledger.commutatorTotal, "24/65");
  assert.notEqual(ledger.commutatorTotal, "0");
  assert.equal(ledger.splitResidual, "0");
  assert.match(ledger.scope, /not a proof of the countable/);
});

test("locks the nonzero periodic signs and cancellation polynomial", async () => {
  const archived = await archivedResult();
  const periodic = archived.periodicProductRuleLedger;
  const cancellation = archived.amplitudeCancellationLedger;

  assert.equal(periodic.velocityDivergence, "0");
  assert.equal(periodic.vorticityDivergence, "0");
  assert.deepEqual(periodic.divQMinusOmegaDotGradOmega, ["0", "0", "0"]);
  assert.equal(periodic.normalizedIntegralSColonQ, "2");
  assert.equal(periodic.normalizedIntegralBColonQ, "2");
  assert.equal(periodic.normalizedIntegralMinusUDotDivQ, "2");

  assert.ok(everyEntryEquals(cancellation.covarianceExpansionResidual, "0"));
  assert.deepEqual(cancellation.spectralCrossResidual, ["0", "0", "0"]);
  assert.deepEqual(cancellation.LDivLResidual, ["0", "0", "0"]);
  assert.deepEqual(cancellation.reflectionDecompositionResidual, ["0", "0", "0"]);
  assert.equal(cancellation.polynomialResidual, "0");
  assert.match(cancellation.polynomialCertificate, /2\*sum\(a\*c\)/);
  assert.deepEqual(cancellation.orientationFlipResidual, ["0", "0", "0"]);
  assert.equal(cancellation.sharpSOSResidual, "0");
  assert.equal(cancellation.sharpWitnessSlack, "0");
});

test("locks the conditional fixed-frame shear and sharp point", async () => {
  const ledger = (await archivedResult()).fixedFrameShearLedger;

  assert.equal(ledger.M, 16);
  assert.equal(ledger.lowShellRadius, 5);
  assert.equal(ledger.highShellRadius, 80);
  assert.deepEqual(ledger.lowPossibleIndices, [2, 3]);
  assert.deepEqual(ledger.highPossibleIndices, [6, 7]);
  assert.equal(ledger.possibleIndexIntersection, "empty");
  assert.match(ledger.activeSetBoundary, /neither possible index is asserted/);
  assert.equal(ledger.responseSymbols.rho, "phi(5/4)");
  assert.equal(ledger.responseSymbols.sigma, "phi(5/8)");
  assert.equal(ledger.responseSymbols.tightPremise, "rho^2+sigma^2=1");
  assert.match(ledger.framePremiseBoundary, /not numerically evaluated/);
  assert.ok(everyEntryEquals(ledger.frameCovarianceFactorResidual, "0"));

  assert.deepEqual(ledger.originLowValue, ["1", "0", "0"]);
  assert.deepEqual(ledger.originHighValue, ["0", "1/16", "0"]);
  assert.deepEqual(ledger.originCovariance, [
    ["1", "0", "0"],
    ["0", "1/256", "0"],
    ["0", "0", "0"],
  ]);
  assert.ok(everyEntryEquals(ledger.originProjectorDerivatives, "0"));
  assert.deepEqual(ledger.originDivL, ["0", "0", "0"]);
  assert.equal(ledger.originEnergy, "257/256");
  assert.equal(ledger.originResidual, "1/256");
  assert.equal(ledger.originAbsoluteGap, "255/256");
  assert.equal(ledger.originRelativeGap, "255/257");
  assert.equal(ledger.originResidualRatio, "1/257");
  assert.equal(ledger.gradientDensityRaw, "258*rho**2 + 258*sigma**2");
  assert.equal(ledger.gradientDensityUnderTightPremise, "258");

  assert.deepEqual(ledger.projectedBlockDivergences, ["rho", "sigma", "0", "0"]);
  assert.equal(ledger.JRaw, "rho**2 + sigma**2");
  assert.equal(ledger.JUnderTightPremise, "1");
  assert.deepEqual(ledger.ALRaw, ["-2*rho**2 - 2*sigma**2", "0", "0"]);
  assert.deepEqual(ledger.ALUnderTightPremise, ["-2", "0", "0"]);
  assert.deepEqual(ledger.conditionalALResidual, ["0", "0", "0"]);
  assert.equal(ledger.sharpSlackModuloTightness, "0");

  for (const key of [
    "curlResidual",
    "heatEquationResidual",
    "vorticityHeatEquationResidual",
    "advectiveNonlinearity",
    "vortexStretching",
  ]) {
    assert.deepEqual(ledger[key], ["0", "0", "0"], key);
  }
  assert.match(ledger.solutionBoundary, /pointwise at t=0/);
  assert.match(ledger.solutionBoundary, /stretching is identically zero/);
});

test("locks the isolated rank-one boundary and no-overclaim ledger", async () => {
  const archived = await archivedResult();
  const ledger = archived.rankOneBoundaryLedger;

  assert.deepEqual(ledger.blockDivergences, ["0", "0"]);
  assert.deepEqual(ledger.originCovariance, [
    ["2", "0", "0"],
    ["0", "0", "0"],
    ["0", "0", "0"],
  ]);
  assert.ok(everyEntryEquals(ledger.originCovarianceDerivatives, "0"));
  assert.ok(everyEntryEquals(ledger.originProjectedValues, "0"));
  assert.deepEqual(ledger.originProjectedDivergences, ["1", "-1"]);
  assert.equal(ledger.originJ, "2");
  assert.deepEqual(ledger.originAL, ["0", "0", "0"]);
  assert.match(ledger.boundary, /isolated smooth rank-one point/);

  assert.ok(
    archived.analyticDependencies.some((item) =>
      item.includes("half-curvature normalization K_Q"),
    ),
  );
  for (const token of [
    "pointwise residual ratio 1/(M^2+1)",
    "does not assert uniform near rank",
    "nonzero vortex stretching",
    "does not verify the Section 8 continuation hypotheses",
    "unconditional global regularity",
    "Millennium problem",
  ]) {
    assert.ok(archived.claimBoundary.includes(token), token);
  }
});

test("locks every R0.70T certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070t_exact_audit\.py/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});
