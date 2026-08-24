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
const certificateRoot = new URL("certificates/r070x/", research);

async function archivedResult() {
  return JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
}

function everyEntryEquals(value, expected) {
  if (Array.isArray(value)) {
    return value.every((entry) => everyEntryEquals(entry, expected));
  }
  return value === expected;
}

test("locks the R0.70X decision and claim boundary", async () => {
  const [report, audit, readme, producer, environment] = await Promise.all([
    readFile(new URL("r070x_report-source.md", research), "utf8"),
    readFile(new URL("r070x_independent_audit.md", research), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("r070x_exact_audit.py", research), "utf8"),
    readFile(new URL("environment.txt", certificateRoot), "utf8"),
  ]);

  for (const token of [
    "R0.70X — Cyclic null structure",
    "|n|^2A_n+|p|^2A_p+|q|^2A_q=0",
    "\\operatorname{rank}Q\\le1",
    "G_Q\\equiv0",
    "\\frac{81(62+1639\\kappa)}{32780}",
    "one power is sharp",
    "response-slope",
    "nonnegative cutoff",
    "uniformly positive top covariance eigenvalue",
    "not a novelty or",
  ]) {
    assert.ok(report.includes(token), token);
  }

  assert.match(report, /No public-page update or GitHub\s+publication/);
  assert.match(report, /not a novelty or\s+priority\s+claim/);
  assert.match(report, /does not prove an enstrophy estimate/);
  assert.match(audit, /\*\*Verdict:\*\* \*\*PASS\*\*/);
  assert.match(audit, /zero blocker, zero major issue, and zero minor issue/);
  assert.match(audit, /No publication, public-page update/);
  assert.match(readme, /thirty-six vorticity modes/);
  assert.match(readme, /nonnegative-frame branch/);
  assert.match(producer, /do(?:es)? not prove a vector-valued trilinear/);
  assert.match(environment, /DGX not used/);

  assert.doesNotMatch(report, /first ever|for the first time|proves novelty/i);
  assert.doesNotMatch(report, /proves unconditional global regularity/i);
  assert.doesNotMatch(report, /solves? the Millennium problem/i);
  assert.doesNotMatch(report, /我们|攻关|主攻|杀死错误想法/);
});

test("reproduces the six-group exact R0.70X producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070x_exact_audit.py", research));
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
  assert.equal(archived.release, "R0.70X");
  assert.equal(
    archived.status,
    "cyclic-null-and-rank-at-most-one-signed-obstruction",
  );
  assert.equal(Object.keys(archived.checks).length, 6);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the cyclic triad identity and beta oscillation", async () => {
  const ledger = (await archivedResult()).cyclicLedger;

  assert.equal(ledger.frequencyConstraint, "n+p+q=0");
  assert.deepEqual(ledger.divergenceResiduals, ["0", "0", "0"]);
  assert.equal(
    ledger.identity,
    "|n|^2*A_n+|p|^2*A_p+|q|^2*A_q=0",
  );
  assert.equal(ledger.identityResidual, "0");
  assert.equal(ledger.differenceResidual, "0");
  assert.match(ledger.orderedFormula, /\(1\/2\)/);
  assert.match(ledger.cyclicFormula, /\(1\/6\)/);
  assert.match(ledger.betaDefinition, /K\(p,q\)\/\|n\|\^2/);
  assert.match(ledger.physicalNullIdentity, /-Delta S\(v\)/);
});

test("locks the sharp high-high-low family", async () => {
  const ledger = (await archivedResult()).sharpLedger;

  assert.deepEqual(ledger.n, ["1", "0", "0"]);
  assert.deepEqual(ledger.p, ["M", "M", "0"]);
  assert.deepEqual(ledger.q, ["-M - 1", "-M", "0"]);
  assert.deepEqual(ledger.A, [
    "-M/sqrt(2*M**2 + 2*M + 1)",
    "-(M + 1)/sqrt(2*M**2 + 2*M + 1)",
    "M/sqrt(2*M**2 + 2*M + 1)",
  ]);
  assert.equal(ledger.cyclicResidual, "0");
  assert.equal(ledger.block, ledger.blockExpected);
  assert.match(ledger.block, /M\*kappa_M \+ 1/);
  assert.match(ledger.lowerBound, /kappa_M>=0/);
  assert.match(ledger.sharpness, /cannot improve beyond t\/R/);
});

test("locks the planar field and complete-frame rank-one geometry", async () => {
  const archived = await archivedResult();
  const field = archived.fieldLedger;
  const covariance = archived.covarianceLedger;

  assert.deepEqual(field.axis, ["1", "-1", "1"]);
  assert.deepEqual(field.planeResonanceResidual, ["0", "0", "0"]);
  assert.equal(field.divergenceW, "0");
  assert.equal(field.axisDotW, "0");
  assert.deepEqual(field.eigenResidual, ["0", "0", "0"]);
  assert.equal(field.psiCubeMean, "3/2");
  assert.equal(field.ARepresentationResidual, "0");
  assert.equal(field.Amean, "81/2");

  assert.deepEqual(covariance.singleShellRadiiSquared, ["5", "110", "149"]);
  assert.deepEqual(covariance.strictFactorFourSquaredSlacks, ["30", "69"]);
  assert.equal(covariance.defectScalar, covariance.defectExpected);
  assert.ok(everyEntryEquals(covariance.twoByTwoMinors, "0"));
  assert.match(covariance.rank, /rank\(Q\)<=1/);
  assert.equal(covariance.covarianceArea, "G_Q=0 everywhere");
  assert.match(covariance.topGapBoundary, /no uniformly positive/);
});

test("locks the physical and Fourier signed-work obstruction", async () => {
  const archived = await archivedResult();
  const signed = archived.signedLedger;
  const fourier = archived.fourierLedger;

  assert.deepEqual(signed.radiiSquared, ["5", "110", "149"]);
  assert.equal(signed.Amean, "81/2");
  assert.equal(signed.adjacentFreePart, "-62/8195");
  assert.equal(signed.generalWork, signed.generalWorkExpected);
  assert.equal(
    signed.fixedWork,
    "-81*(1639*kappa + 62)/32780",
  );
  assert.equal(signed.fixedWork, signed.fixedWorkExpected);
  assert.match(signed.sign, /kappa>=0 imply E_S<0/);

  assert.equal(fourier.modeCount, 36);
  assert.deepEqual(fourier.radiiByShell, {
    1: [5],
    6: [110],
    7: [149],
  });
  assert.equal(fourier.defectOutputCount, 228);
  assert.equal(fourier.nonzeroSignedContributionCount, 36);
  assert.equal(fourier.nonzeroSignedContributions.length, 36);
  assert.equal(fourier.signedWork, signed.fixedWork);
  assert.equal(fourier.signedWork, fourier.signedWorkExpected);
  assert.equal(fourier.difference, "0");
  assert.equal(fourier.placementCyclicResidual, "0");
  assert.equal(fourier.placementWeightedBlock, fourier.placementExpected);
});

test("locks the R0.70X analytic and claim boundaries", async () => {
  const archived = await archivedResult();

  assert.ok(
    archived.analyticDependencies.some((entry) =>
      entry.includes("nonnegative cutoff"),
    ),
  );
  assert.ok(
    archived.analyticDependencies.some((entry) =>
      entry.includes("no G_Q estimate"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("nonnegative-frame branch"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("does not rule out an estimate under a uniformly positive"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("does not prove an enstrophy closure"),
    ),
  );
});

test("locks every R0.70X certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070x_exact_audit\.py/);
  assert.deepEqual(
    lines.map((line) => line.slice(66)),
    [
      "README.md",
      "command.txt",
      "environment.txt",
      "result.json",
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
