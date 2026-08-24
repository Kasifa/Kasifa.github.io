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
const certificateRoot = new URL("certificates/r070w/", research);

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

test("locks the R0.70W decision and claim boundary", async () => {
  const [report, audit, readme, producer, environment] = await Promise.all([
    readFile(new URL("r070w_report-source.md", research), "utf8"),
    readFile(new URL("r070w_independent_audit.md", research), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("r070w_exact_audit.py", research), "utf8"),
    readFile(new URL("environment.txt", certificateRoot), "utf8"),
  ]);

  for (const token of [
    "R0.70W — A far-shell rank-one obstruction",
    "\\Omega_\\alpha\\times\\Omega_\\beta\\equiv0",
    "\\frac{2}{729}\\varepsilon^2",
    "\\mathfrak E_S(\\omega_\\varepsilon)",
    "pair-dependent multiplier",
    "scale-correct candidate",
    "direct signed trilinear",
    "\\frac{\\varepsilon^2M^2}{(M^2+2)^3}",
    "negative control",
    "\\mathcal C_m",
    "\\mathcal U_{-2}",
    "classical cubic-enstrophy scale",
    "not a novelty or",
  ]) {
    assert.ok(report.includes(token), token);
  }

  assert.match(report, /information-loss obstruction/);
  assert.match(report, /does not have a uniformly positive top eigenvalue/);
  assert.match(report, /Neither \(9\.4\) nor \(9\.5\) is proved here/);
  assert.match(report, /No public-page update or\s+GitHub publication/);
  assert.match(audit, /\*\*Verdict:\*\* \*\*PASS\*\*/);
  assert.match(audit, /zero blocker, zero major issue, and zero minor issue/);
  assert.match(audit, /Full repository Node suite \| \*\*673\/673 PASS\*\*/);
  assert.match(audit, /No publication, public-page update/);
  assert.match(readme, /does not rule out\s+a direct signed trilinear area estimate/);
  assert.match(producer, /does not prove a bilinear multiplier/);
  assert.match(environment, /DGX not used/);

  assert.doesNotMatch(report, /first ever|for the first time|proves novelty/i);
  assert.doesNotMatch(report, /proves unconditional global regularity/i);
  assert.doesNotMatch(report, /solves? the Millennium problem/i);
});

test("reproduces the seven-group exact R0.70W producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070w_exact_audit.py", research));
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
  assert.equal(archived.release, "R0.70W");
  assert.equal(
    archived.status,
    "far-shell-rank-one-projected-summation-obstruction",
  );
  assert.equal(Object.keys(archived.checks).length, 7);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the exact projected-wedge identity", async () => {
  const ledger = (await archivedResult()).projectedWedgeLedger;

  assert.equal(ledger.frequencyConstraint, "n=p+q");
  assert.deepEqual(ledger.divergenceResiduals, ["0", "0"]);
  assert.ok(everyEntryEquals(ledger.identityResidual, "0"));
  assert.match(ledger.identity, /a x b/);
  assert.match(ledger.identity, /\(q-p\)/);
  assert.match(ledger.defectFormula, /K\(p,q\)/);
  assert.match(ledger.defectFormula, /\(2\|n\|\)\^-1/);
  assert.ok(everyEntryEquals(ledger.currentPairResidual, "0"));
  assert.ok(everyEntryEquals(ledger.currentProjectionResidual, "0"));
  assert.match(ledger.currentDefinition, /partial_m omega/);
  assert.match(ledger.currentFourier, /q-p/);
  assert.match(ledger.currentProjection, /Chat\(n\)-Chat\(n\)\^T/);
});

test("locks the separated radii and rank-one covariance", async () => {
  const archived = await archivedResult();
  const field = archived.fieldLedger;
  const covariance = archived.covarianceLedger;

  assert.equal(field.divergenceW, "0");
  assert.equal(field.divergenceH, "0");
  assert.equal(field.lowRadiusSquared, "1");
  assert.equal(field.highRadiusSquared, "17");
  assert.equal(field.strictFactorFourSquaredSlack, "1");
  assert.equal(field.lowModeCount, 4);
  assert.equal(field.highModeCount, 8);

  assert.ok(everyEntryEquals(covariance.covarianceResidual, "0"));
  assert.ok(everyEntryEquals(covariance.twoByTwoMinors, "0"));
  assert.deepEqual(covariance.physicalCrossProduct, ["0", "0", "0"]);
  assert.match(covariance.responseReading, /Gamma\(1,sqrt\(17\)\)=0/);
  assert.match(covariance.rank, /rank\(Q\)<=1/);
  assert.match(covariance.eigenvalueResidual, /lambda2\+lambda3=0/);
  assert.match(covariance.covarianceArea, /lambda1\*r\+lambda2\*lambda3=0/);
});

test("locks the complete projected H-minus-one sum", async () => {
  const ledger = (await archivedResult()).defectLedger;

  assert.ok(everyEntryEquals(ledger.defectResidual, "0"));
  assert.equal(ledger.fourierModeCount, 18);
  assert.equal(ledger.projectedNonzeroModeCount, 8);
  assert.equal(ledger.X, "2*epsilon**2/729");
  assert.equal(ledger.X, ledger.XExpected);

  for (const mode of ledger.projectedNonzeroModes) {
    assert.equal(mode.frequencySquared, "18");
    assert.equal(mode.projectedSquared, "epsilon**2/162");
    assert.equal(mode.XContribution, "epsilon**2/2916");
    assert.deepEqual(mode.defectCoefficient, [
      ["0", "-epsilon/4", "0"],
      ["-epsilon/4", "0", "0"],
      ["0", "0", "0"],
    ]);
  }
});

test("locks physical wedge cancellation and tensor addition", async () => {
  const ledger = (await archivedResult()).cancellationLedger;

  assert.deepEqual(ledger.output, [1, 1, 4]);
  assert.deepEqual(ledger.firstCross, ["0", "0", "-1/8"]);
  assert.deepEqual(ledger.secondCross, ["0", "0", "1/8"]);
  assert.deepEqual(ledger.crossSum, ["0", "0", "0"]);
  assert.deepEqual(ledger.tensorSum, ledger.tensorExpected);
  assert.equal(ledger.tensorSum[0][1], "-epsilon/4");
  assert.equal(ledger.tensorSum[1][0], "-epsilon/4");
  assert.match(ledger.reading, /wedge pairs cancel/i);
});

test("locks the signed boundary and resonant negative control", async () => {
  const archived = await archivedResult();
  const signed = archived.signedLedger;
  const resonant = archived.resonantLedger;

  assert.equal(signed.omegaSupportCount, 12);
  assert.equal(signed.defectSupportCount, 18);
  assert.deepEqual(signed.supportOverlap, []);
  assert.match(signed.signedWork, /= 0/);
  assert.match(signed.reading, /but not a direct signed trilinear/);

  assert.equal(
    resonant.generalExactRankX,
    "M**2*epsilon**2/(M**2 + 2)**3",
  );
  assert.equal(resonant.generalExactRankX, resonant.generalExactRankXExpected);
  assert.equal(resonant.generalDefectModeCount, 18);
  assert.equal(resonant.generalProjectedModeCount, 8);
  assert.equal(resonant.generalProjectedModes.length, 8);
  for (const mode of resonant.generalProjectedModes) {
    assert.equal(mode.frequencySquared, "M**2 + 2");
    assert.match(mode.XContribution, /M\*\*2\*epsilon\*\*2/);
  }
  assert.deepEqual(resonant.resonantPolarization, ["1", "-1", "0"]);
  assert.equal(
    resonant.signedWork,
    "-M*epsilon*eta/(2*(M**2 + 1)*(M**2 + 2))",
  );
  assert.equal(resonant.signedWork, resonant.signedWorkExpected);
  assert.equal(resonant.signedWorkAdjacentResponseDerivative, "0");
  assert.equal(resonant.A13, resonant.A13Expected);
  assert.equal(resonant.A23, resonant.A23Expected);
  assert.equal(resonant.responseArea13, "1");
  assert.match(resonant.responseArea23, /gamma_23/);
  assert.equal(resonant.responseWedgeMixed, "0");
  assert.equal(resonant.physicalAreaMixed, "0");
  assert.equal(
    resonant.areaHdotMinusOne,
    resonant.areaHdotMinusOneExpected,
  );
  assert.equal(resonant.areaHdotMinusOneResidual, "0");
  assert.match(resonant.asymptoticReading, /does not disprove/);
});

test("locks the exact-order universal majorant boundary", async () => {
  const ledger = (await archivedResult()).universalMajorantLedger;

  assert.equal(ledger.pairRadius, "R=max(|p|,|q|)");
  assert.match(ledger.farCase, /12\/R/);
  assert.match(ledger.nearCase, /3\*M_phi\^2\/R/);
  assert.equal(ledger.constant, "C0=max(12,3*M_phi^2)");
  assert.match(ledger.majorant, /U_-2/);
  assert.equal(ledger.projectedBound, "X_cross<=C0^2*U_-2");
  assert.match(ledger.sobolevBound, /Hdot\(1\/4\)/);
  assert.equal(ledger.quarterSobolevDegree, "3/4");
  assert.equal(ledger.quarterSobolevFourthDegree, "3");
  assert.deepEqual(ledger.signedInterpolationPowers, {
    L2: "3/2",
    H1: "3/2",
  });
  assert.match(ledger.closureBoundary, /not a large-data closure/);
});

test("locks every R0.70W certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070w_exact_audit\.py/);
  assert.deepEqual(
    lines.map((line) => line.slice(66)),
    [
      "README.md",
      "command.txt",
      "environment.txt",
      "result.json",
      "../../r070w_exact_audit.py",
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
