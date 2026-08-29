import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");

const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));

function decimalInterval(value) {
  const match = String(value).match(/^\[([^,]+),\s*([^\]]+)\]$/);
  assert.ok(match, value);
  return [Number(match[1]), Number(match[2])];
}

test("R0.73C closes the exact cubic neutral spectrum in the periodic Sobolev domain", async () => {
  const [report, freeze, gap] = await Promise.all([
    text("research/r073c_report-source.md"),
    text("research/r073c_problem_freeze.md"),
    text("research/r073c_gap_matrix.md"),
  ]);
  for (const token of [
    "exactCubicNeutralSpectrum=CLOSED",
    "\\gamma_0=\\frac{\\sqrt7}{2}",
    "|\\sin(x/2)|^3",
    "C^2\\cap H^2_{\\rm per}",
    "not \\(C^3\\)",
    "-\\frac74",
    "\\frac{(n+3)^2-16}{4}",
    "unique negative",
  ]) assert.ok(report.includes(token) || freeze.includes(token), token);
  assert.match(gap, /C3[^\n]*unique negative singular threshold[^\n]*CLOSED/);
  assert.doesNotMatch(report, /exactCubicNeutralSpectrum=(?:OPEN|CONDITIONAL)/);
});

test("R0.73C exact monodromy bridge has determinant one, real trace, and the correct growth sign", async () => {
  const proof = await text("research/r073c_monodromy_proof.md");
  for (const token of [
    "\\det M=1",
    "M^{-1}=S\\overline M S",
    "\\operatorname{tr}M",
    "\\det(M-I)=2-\\operatorname{tr}M",
    "F(\\eta):=\\operatorname{tr}M(\\eta)-2",
    "\\sigma=-ic/2",
    "\\sigma=\\eta/2>0",
    "0.17035",
    "0.17050",
  ]) assert.ok(proof.includes(token), token);
  assert.match(proof, /periodic solution if and only if[\s\S]*F\(\\eta\):=[\s\S]*=0/);
  assert.match(proof, /existence, not root uniqueness or algebraic simplicity/);
});

test("two primary interval runs certify the same infinite-dimensional endpoint signs", async () => {
  const runs = await Promise.all([
    json("experiments/r073c/interval_run_a.json"),
    json("experiments/r073c/interval_run_b.json"),
  ]);
  assert.deepEqual(runs.map((run) => run.status), ["passed", "passed"]);
  assert.deepEqual(runs.map((run) => [run.results[0].steps, run.results[0].order, run.dps]), [
    [1024, 10, 40], [768, 12, 55],
  ]);
  for (const run of runs) {
    assert.equal(run.environment.mpmath, "1.3.0");
    assert.match(run.environment.source.sha256, /^[0-9a-f]{64}$/);
    assert.deepEqual(run.results.map((row) => row.eta), ["0.3407", "0.3410"]);
    assert.deepEqual(run.results.map((row) => row.sign), ["negative", "positive"]);
    for (const row of run.results) {
      assert.equal(row.infiniteDimensionalPeriodicOde, true);
      assert.equal(row.fourierTruncationUsed, false);
      assert.equal(row.traceImagContainsZero, true);
    }
    const low = decimalInterval(run.results[0].traceMinusTwo.decimal);
    const high = decimalInterval(run.results[1].traceMinusTwo.decimal);
    assert.ok(low[1] < 0, JSON.stringify(low));
    assert.ok(high[0] > 0, JSON.stringify(high));
  }
});

test("the independent Decimal enclosure repeats the signs without importing the primary arithmetic", async () => {
  const result = await json("experiments/r073c/decimal_interval_validation.json");
  assert.equal(result.status, "passed");
  assert.equal(result.arithmetic.lowerRounding, "ROUND_FLOOR");
  assert.equal(result.arithmetic.upperRounding, "ROUND_CEILING");
  assert.equal(result.arithmetic.transcendentalLibraryUsed, false);
  assert.equal(result.arithmetic.workingPrecisionDigits, 80);
  assert.deepEqual(result.results.map((row) => row.sign), ["negative", "positive"]);
  assert.equal(result.checks.endpointSignsOpposite, true);
  assert.equal(result.checks.allDeterminantIntervalsContainOne, true);
  assert.equal(result.checks.allTraceImaginaryIntervalsContainZero, true);
  assert.equal(result.checks.criticalDecimalFlagsClear, true);
  assert.equal(result.claimBoundary.infiniteDimensionalPeriodicOdeBracketValidated, true);
  assert.equal(result.claimBoundary.fourierTruncationUsed, false);
  assert.equal(result.claimBoundary.nonautonomousTransferProved, false);
  assert.equal(result.claimBoundary.nonlinearNavierStokesProved, false);
});

test("finite Fourier diagnostics agree numerically while remaining explicitly non-probative", async () => {
  const [primary, independent] = await Promise.all([
    json("experiments/r073c/fourier_screen.json"),
    json("experiments/r073c/independent_fourier_validation.json"),
  ]);
  assert.equal(primary.claimBoundary.finiteFourierSpectrumComputed, true);
  assert.equal(primary.claimBoundary.infiniteDimensionalEigenvalueEnclosed, false);
  assert.equal(primary.claimBoundary.ordinaryCutoffConvergenceIsProof, false);
  assert.equal(primary.claimBoundary.fredholmInverseIntervalValidated, false);
  assert.equal(independent.status, "passed");
  assert.ok(Object.values(independent.checks).every(Boolean));
  assert.equal(independent.claimBoundary.infiniteDimensionalSpectrumProved, false);
  assert.equal(independent.claimBoundary.continuousContourEnclosed, false);
  assert.equal(independent.claimBoundary.fourierTailRieszCertificateValidated, false);
  assert.ok(independent.maximumErrors.leadingEigenvalueAbsolute < 2e-12);
  const n128 = independent.recomputedSentinels.find((row) => row.N === 128 && row.gamma === 0.5);
  assert.ok(n128);
  assert.ok(Math.abs(n128.leadingReal - 0.170407976920434) < 2e-12);
});

test("R0.73C keeps C5 open and C6 conditional in the same final ledger", async () => {
  const [report, gap, freeze] = await Promise.all([
    text("research/r073c_report-source.md"),
    text("research/r073c_gap_matrix.md"),
    text("research/r073c_problem_freeze.md"),
  ]);
  for (const token of [
    "infiniteDimensionalFrozenRayleighInstability=CLOSED",
    "frozenInstabilityFastTimeTransfer=OPEN",
    "superPolynomialCompleteRowNoGo=CONDITIONAL",
    "sharpLargeLambdaGrowthLaw=OPEN",
    "completeOSSquireA2DirectSum=OPEN",
    "nonlinearNavierStokes=OPEN",
    "Clay=OPEN",
  ]) assert.ok(report.includes(token), token);
  assert.match(report, /unbounded[\s\S]*sectorial generator/);
  assert.match(gap, /C5[\s\S]*OPEN[\s\S]*eigenvalue, Riesz, dichotomy, graph-domain package/);
  assert.match(gap, /C6[\s\S]*CONDITIONAL on C5/);
  assert.match(freeze, /may not be treated as a small bounded\s+perturbation/);
  assert.equal(report.includes("TO_PROVE"), false);
  assert.equal(report.includes("TO_DISPROVE"), false);
});
