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
const certificateRoot = new URL("certificates/r071a/", research);

async function archivedResult() {
  return JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
}

test("locks the R0.71A report, literature, audit, and claim boundary", async () => {
  const [report, literature, audit, readme, producer, environment] =
    await Promise.all([
      readFile(new URL("r071a_report-source.md", research), "utf8"),
      readFile(new URL("r071a_literature_audit.md", research), "utf8"),
      readFile(new URL("r071a_independent_audit.md", research), "utf8"),
      readFile(new URL("README.md", certificateRoot), "utf8"),
      readFile(new URL("r071a_exact_audit.py", research), "utf8"),
      readFile(new URL("environment.txt", certificateRoot), "utf8"),
    ]);

  for (const token of [
    "R0.71A — A constant-projector no-go",
    "P_1(Q)=e_3\\otimes e_3",
    "\\nabla P_1=0",
    "\\lambda_1-\\lambda_2\\ge10\\Lambda^2",
    "\\frac{3\\sqrt2}{40}\\Lambda^3",
    "\\frac2q+\\frac3p=1",
    "\\|I_L\\|_{L_t^1}",
    "amplitude-normalized concentrating sequence",
    "\\mathfrak W_{L,p}",
    "method no-go",
  ]) {
    assert.ok(report.includes(token), token);
  }

  assert.match(literature, /not a systematic review and makes no priority claim/i);
  assert.match(literature, /Miller 2021, Remark 3\.3/);
  assert.match(literature, /physical vorticity direction/i);
  assert.match(literature, /CLMS does not manufacture its BMO partner/);
  assert.match(audit, /No blocker or major mathematical issue/);
  assert.match(audit, /amplitude-normalized concentrating sequence/);
  assert.match(audit, /kinematic test field as a Navier--Stokes solution/i);
  assert.match(readme, /kinematic route obstruction/);
  assert.match(producer, /not asserted as an NSE-solution counterexample/);
  assert.match(environment, /DGX used: no/);
  assert.match(environment, /GitHub publication: no/);

  assert.doesNotMatch(report, /first ever|for the first time|proves novelty/i);
  assert.doesNotMatch(report, /proves unconditional global regularity/i);
  assert.doesNotMatch(report, /solves? the Millennium problem/i);
  assert.doesNotMatch(report, /critical projector criterion is false/i);
});

test("reproduces the nine-group exact R0.71A producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r071a_exact_audit.py", research));
  const archivedText = await readFile(
    new URL("result.json", certificateRoot),
    "utf8",
  );
  const archived = JSON.parse(archivedText);
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });

  assert.equal(stderr, "");
  assert.equal(stdout, archivedText);
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.71A");
  assert.equal(archived.status, "projector-coherence-method-boundary");
  assert.equal(Object.keys(archived.checks).length, 9);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the constant-projector sign pair and residual boundary", async () => {
  const ledger = (await archivedResult()).constantProjectorLedger;

  assert.deepEqual(ledger.radiiSquared, [2, 34, 34, 576, 9409]);
  assert.deepEqual(ledger.strictFactorFourSquaredSlacks, [2, 32, 193]);
  assert.equal(ledger.modeCount, 10);
  assert.equal(ledger.fillerInvolvingResonanceCount, 0);
  assert.equal(ledger.covarianceDifference, "zero at every Fourier output");
  assert.equal(ledger.principalProjector, "P1=e3 tensor e3 at every point");
  assert.equal(ledger.projectorGradient, "0");
  assert.match(ledger.lowerProjectorFrameCommutator, /=0/);
  assert.equal(ledger.positiveWork, "3*sqrt(2)/40");
  assert.equal(ledger.negativeWork, "-3*sqrt(2)/40");
  assert.equal(ledger.baseFullWork, "6*sqrt(2)/85");
  assert.equal(ledger.baseDefectWork, "-3*sqrt(2)/680");
  assert.equal(ledger.baseMeanEnergy, "3/2");
  assert.match(ledger.transverseResidual, /\(3\/2\)\*Lambda\^2/);
  assert.match(ledger.finiteAngleLimit, /every finite Lp/);
  assert.match(ledger.angleBoundary, /not L-infinity/);
});

test("locks the exact strong eigengap", async () => {
  const gap = (await archivedResult()).eigengapLedger;

  assert.equal(gap.fillerAmplitudeSquare, "149775");
  assert.equal(gap.fillerEigenvalueLower, "15");
  assert.match(gap.fillerLowerLemma, />=1\/9985/);
  assert.match(gap.absoluteGap, />=10\*Lambda\^2/);
  assert.match(gap.topNormalizedGap, />=2\/3/);
  assert.match(gap.traceRelativeGap, />=1\/2/);
  assert.match(gap.blockStructure, /e3-perp/);
});

test("locks the critical L1 estimate and same-norm Ls obstruction", async () => {
  const critical = (await archivedResult()).criticalLineLedger;

  assert.equal(critical.timeHolderReciprocalSum, "1");
  assert.equal(critical.projectorCriticalNormScaling, "0");
  assert.equal(critical.errorL1Scaling, "-1");
  assert.equal(critical.errorL2Scaling, "0");
  assert.equal(critical.naturalEnergyRhsScaling, "-1");
  assert.equal(critical.sameNormErrorL1Scaling, "0");
  assert.equal(critical.sameNormErrorL2Scaling, "1");
  assert.equal(critical.sameNormErrorLsScaling, "lambda^(2-2/s)");
  assert.match(critical.sameNormSequence, /fixes both energy norms/);
  assert.match(critical.strongConclusion, /no finite function/);
  assert.match(critical.endpointP3, /q=infinity/);
  assert.match(critical.endpointPInfinity, /only L1_t/);
});

test("locks both nonzero projector-error seeds", async () => {
  const seed = (await archivedResult()).nonzeroSeedLedger;

  assert.deepEqual(seed.localVelocity, ["z", "0", "y"]);
  assert.equal(seed.localVelocityDivergence, "0");
  assert.deepEqual(seed.firstVariationVector, ["0", "0", "z"]);
  assert.equal(seed.firstVariationDivergence, "1");
  assert.match(seed.firstVariation, /positive part \(I_L\)_\+/);
  assert.equal(seed.periodicSeedWork, "delta/2");
});

test("locks analytic and claim boundaries", async () => {
  const archived = await archivedResult();

  assert.ok(
    archived.analyticDependencies.some((entry) =>
      entry.includes("zero-set parity lemma"),
    ),
  );
  assert.ok(
    archived.analyticDependencies.some((entry) =>
      entry.includes("not asserted as an NSE-solution counterexample"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("exactly constant covariance principal projector"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("finite Ls_t control function"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("does not prove a continuation criterion"),
    ),
  );
});

test("locks every R0.71A certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 9);
  assert.deepEqual(
    lines.map((line) => line.slice(66)),
    [
      "README.md",
      "command.txt",
      "environment.txt",
      "result.json",
      "../../r071a_exact_audit.py",
      "../../r070z_exact_audit.py",
      "../../r070x_exact_audit.py",
      "../../r070y_exact_audit.py",
      "../../r070y_report-source.md",
    ],
  );
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});
