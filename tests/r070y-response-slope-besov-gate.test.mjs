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
const certificateRoot = new URL("certificates/r070y/", research);

async function archivedResult() {
  return JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
}

test("locks the R0.70Y decision, literature, audit, and claim boundary", async () => {
  const [report, literature, audit, readme, producer, environment] =
    await Promise.all([
      readFile(new URL("r070y_report-source.md", research), "utf8"),
      readFile(new URL("r070y_literature_audit.md", research), "utf8"),
      readFile(new URL("r070y_independent_audit.md", research), "utf8"),
      readFile(new URL("README.md", certificateRoot), "utf8"),
      readFile(new URL("r070y_exact_audit.py", research), "utf8"),
      readFile(new URL("environment.txt", certificateRoot), "utf8"),
    ]);

  for (const token of [
    "R0.70Y — Response-slope factorization",
    "response difference and an",
    "inverse-square metric difference",
    "\\|\\omega\\|_{B^0_{3,3}}^3",
    "\\|\\omega\\|_{B^0_{\\infty,\\infty}}",
    "\\lambda_1(Q_{\\Lambda})\\ge\\frac1{41210}",
    "principal-eigengap branch",
    "q=3\\) is sharp",
  ]) {
    assert.ok(report.includes(token), token);
  }

  assert.match(literature, /PASS with a strict no-priority boundary/);
  assert.match(literature, /not evidence of priority/);
  assert.match(audit, /\*\*Verdict:\*\* \*\*PASS\*\*/);
  assert.match(audit, /zero blocker, zero major issue, and zero minor issue/);
  assert.match(audit, /689\/689 PASS/);
  assert.match(audit, /No publication, public-page update/);
  assert.match(report, /No\s+public-page update or GitHub publication/);
  assert.match(readme, /forty-mode Fourier\/Parseval reconstruction/);
  assert.match(producer, /do not prove the periodic Coifman--Meyer theorem/);
  assert.match(environment, /DGX used: no/);
  assert.match(environment, /GitHub publication: no/);

  assert.doesNotMatch(report, /first ever|for the first time|proves novelty/i);
  assert.doesNotMatch(report, /proves unconditional global regularity/i);
  assert.doesNotMatch(report, /solves? the Millennium problem/i);
  assert.doesNotMatch(report, /我们|攻关|主攻|杀死错误想法/);
});

test("reproduces the six-group exact R0.70Y producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070y_exact_audit.py", research));
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
  assert.equal(archived.release, "R0.70Y");
  assert.equal(
    archived.status,
    "response-slope-besov-and-top-eigenvalue-gate",
  );
  assert.equal(Object.keys(archived.checks).length, 6);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the response-slope and metric-response identities", async () => {
  const ledger = (await archivedResult()).responseLedger;

  assert.match(ledger.slopeDefinition, /V\(p\)-V\(q\)/);
  assert.match(ledger.betaDefinition, /\(1\/2\)/);
  assert.match(ledger.weightedClosure, /\|n\|d_n/);
  assert.equal(ledger.twoLegResidual, "0");
  assert.equal(ledger.symmetricResidual, "0");
  assert.equal(ledger.metricResponseResidual, "0");
  assert.equal(ledger.wedgeNormResidual, "0");
  assert.equal(ledger.gramTraceResidual, "0");
  assert.match(ledger.metricResponseSplit, /x_n-x_p/);
});

test("locks the actual radial-frame Gram-area obstruction", async () => {
  const ledger = (await archivedResult()).gramAreaFamilyLedger;

  assert.equal(ledger.parameterPremise, "integer M>=4");
  assert.deepEqual(ledger.n, ["1", "1", "0"]);
  assert.deepEqual(ledger.responseK, ["0", "1", "1"]);
  assert.equal(ledger.affineResponseAreaSquare, "0");
  assert.equal(ledger.responseGramDeterminant, "0");
  assert.equal(ledger.cyclicResidual, "0");
  assert.equal(ledger.cyclicBlock, ledger.cyclicBlockExpected);
  assert.match(ledger.cyclicBlock, /-2\*\(2\*M \+ 1\)/);
  assert.match(ledger.conclusion, /neither the affine response area/);
});

test("locks the critical Besov theorem ledger and q=3 packet arithmetic", async () => {
  const archived = await archivedResult();
  const besov = archived.besovLedger;
  const sharp = archived.sharpnessLedger;
  const report = await readFile(
    new URL("r070y_report-source.md", research),
    "utf8",
  );

  assert.match(besov.theorem, /B\^0_\(3,3\)/);
  assert.match(besov.mixedTheorem, /infinity,infinity/);
  assert.match(besov.HHLNormalizedSymbol, /delta\*Mtilde_delta/);
  assert.match(besov.periodicKernel, /L1\(T\^6\)/);
  assert.match(besov.sequenceKernel, /ell1/);
  assert.match(report, /compact localized \$?\\?\(L\^1\\?\)? kernel/);
  assert.match(report, /h_m=2\^{-m\}/);

  assert.equal(sharp.scale, 64);
  assert.equal(sharp.oneTopSquaredSlack, "19884");
  assert.equal(sharp.twoTopSquaredSlack, "3947");
  assert.match(sharp.packet, /r0/);
  assert.match(sharp.signedWork, /N\*E_S\(W\)/);
  assert.match(sharp.contradiction, /q>3/);
});

test("locks the uniformly positive top eigenvalue and eigengap boundary", async () => {
  const archived = await archivedResult();
  const filler = archived.fillerLedger;
  const gap = archived.eigengapLedger;

  assert.deepEqual(filler.radiiSquared, [5, 110, 149, 2401, 38809]);
  assert.deepEqual(filler.strictFactorFourSquaredSlacks, ["17", "393"]);
  assert.match(filler.uniformLowerBound, /1\/41210/);
  assert.match(filler.topEigenvalue, /lambda_1/);
  assert.equal(filler.covarianceAreaResidual, "0");
  assert.equal(filler.gradientSquare, "1188*Lambda**2 + 20605");
  assert.equal(filler.gradientSquare, filler.gradientSquareExpected);

  assert.equal(gap.axialPhaseResidual, "0");
  assert.deepEqual(gap.oldFieldResidual, ["0", "0", "0"]);
  assert.equal(gap.covarianceScalarFromFrame, "2");
  assert.equal(gap.explicitLambda, "1/6");
  assert.equal(gap.explicitOldEigenvalue, "1");
  assert.equal(gap.explicitFillerEigenvalue, "1");
  assert.match(gap.consequence, /lambda_1=lambda_2/);
  assert.match(gap.boundary, /no absolute or relative principal eigengap/);
});

test("locks the forty-mode work polynomial and analytic boundaries", async () => {
  const archived = await archivedResult();
  const fourier = archived.fourierLedger;

  assert.equal(fourier.modeCount, 40);
  assert.equal(fourier.defectOutputCount, 376);
  assert.equal(fourier.nonzeroSignedContributionCount, 36);
  assert.equal(fourier.signedWork, fourier.signedWorkExpected);
  assert.equal(fourier.difference, "0");
  assert.deepEqual(fourier.LambdaPowers, {
    0: "0",
    1: "0",
    2: "0",
    3: "-81*(1639*kappa + 62)/32780",
  });

  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("uniform positive top covariance eigenvalue"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("does not rule out an estimate under a uniformly positive principal eigengap"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("does not control the principal covariance stretching"),
    ),
  );
});

test("locks every R0.70Y certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 6);
  assert.match(sums, /\.\.\/\.\.\/r070y_exact_audit\.py/);
  assert.match(sums, /\.\.\/\.\.\/r070x_exact_audit\.py/);
  assert.deepEqual(
    lines.map((line) => line.slice(66)),
    [
      "README.md",
      "command.txt",
      "environment.txt",
      "result.json",
      "../../r070y_exact_audit.py",
      "../../r070x_exact_audit.py",
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
