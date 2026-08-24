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
const certificateRoot = new URL("certificates/r070r/", research);

async function archivedResult() {
  return JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
}

test("locks the finite R0.70R scope and curvature convention", async () => {
  const [producer, readme, environment] = await Promise.all([
    readFile(new URL("r070r_exact_audit.py", research), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("environment.txt", certificateRoot), "utf8"),
  ]);

  for (const token of [
    "half-curvature",
    "c(\\rho)=\\frac{\\sqrt\\rho}{1-\\sqrt\\rho}",
    "D-\\mathcal K_Q\\ge-c(\\rho)(D+C)",
    "valid smooth Navier--Stokes initial",
    "does not prove that a single Navier--Stokes/LP evolution",
    "does not close the covariance PDE",
  ]) {
    assert.ok(readme.includes(token), token);
  }
  assert.match(producer, /pointwise covariance jet/);
  assert.match(producer, /does not[\s\S]{0,120}preserved by one Navier--Stokes\/Littlewood--Paley evolution/);
  assert.match(environment, /not preservation by one NSE\/LP evolution/);
  assert.match(environment, /not covariance-PDE closure/);
});

test("locks the canonical theorem, sharpness, and PDE boundary", async () => {
  const report = await readFile(
    new URL("r070r_report-source.md", research),
    "utf8",
  );

  for (const token of [
    "Theorem 4.1 — Quantitative diffusion-deficit bound",
    "(\\Omega_\\alpha)_\\alpha\\in\\ell^2",
    "\\mathcal D_P-\\mathcal K_Q",
    "-\\frac{\\sqrt\\rho}{1-\\sqrt\\rho}",
    "Exact sharpness inside the pinned frame",
    "u(t)=e^{\\nu t\\Delta}u_0",
    "\\int_{\\{E>0,\\ r/E\\leq\\eta_0\\}}",
    "\\geq-c_\\eta\\mathcal G",
    "does not close the Navier--Stokes problem",
    "No public-page",
    "global regularity or finite-time singularity",
  ]) {
    assert.ok(report.includes(token), token);
  }

  assert.match(
    report,
    /\\mathcal K_Q[\s\S]{0,220}\\leq[\s\S]{0,220}\\sqrt\{\\lambda_1\\mathcal D_P\}[\s\S]{0,220}\\sqrt\{\\lambda_2\\mathcal D_L\}/,
  );
  assert.doesNotMatch(report, /proves global regularity/i);
});

test("reproduces the four-group exact R0.70R producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070r_exact_audit.py", research));
  const archived = await archivedResult();
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70R");
  assert.equal(archived.status, "exact-near-rank-diffusion-jet-audit");
  assert.equal(Object.keys(archived.checks).length, 4);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the candidate curvature-bound decomposition", async () => {
  const archived = await archivedResult();
  const definitions = archived.definitions;
  const ledger = archived.candidateBoundLedger;

  assert.match(definitions.curvatureConvention, /half-curvature/);
  assert.equal(definitions.D, "sum_alpha,k |h_alpha_k|^2");
  assert.equal(definitions.C, "sum_alpha,k |c_alpha_k|^2");
  assert.equal(
    definitions.derivativePartition,
    "D+C=sum_alpha,k |partial_k Omega_alpha|^2",
  );
  assert.match(ledger.offDiagonalIdentity, /P\*\(partial_k Q\)\*v1/);
  assert.equal(ledger.minkowskiGramSOSCount, 6);
  assert.equal(ledger.minkowskiGramIdentityResidual, "0");
  assert.match(ledger.candidate, /sqrt\(lambda1\)\*sqrt\(D\)/);
  assert.equal(ledger.nonalignedRationalCase.D, "25");
  assert.equal(ledger.nonalignedRationalCase.C, "16");
  assert.doesNotMatch(ledger.nonalignedRationalCase.candidateSlack, /^-/);
  assert.doesNotMatch(ledger.nonalignedRationalCase.deficitSlack, /^-/);
});

test("locks the near-rank scalar square slack", async () => {
  const archived = await archivedResult();
  const ledger = archived.nearRankDeficitLedger;

  assert.match(ledger.cRho, /A_second/);
  assert.equal(ledger.inequality, "D-K_Q>=-c(rho)*(D+C)");
  assert.equal(ledger.exactScalarSlack, ledger.sumOfSquares);
  assert.equal(
    ledger.equalityConditionForPositiveAmplitudes,
    "sqrt(D)=sqrt(C)",
  );
});

test("locks the two-block sharp jet and attained constant", async () => {
  const archived = await archivedResult();
  const ledger = archived.twoBlockSharpJetLedger;
  const sample = ledger.rationalInstance;

  assert.equal(ledger.candidateEqualityResidual, "0");
  assert.equal(ledger.sharpDeficitResidual, "0");
  assert.deepEqual(sample.Q, [
    ["9", "0", "0"],
    ["0", "1", "0"],
    ["0", "0", "0"],
  ]);
  assert.equal(sample.D, "4");
  assert.equal(sample.C, "4");
  assert.equal(sample.KQ, "8");
  assert.equal(sample.rho, "1/9");
  assert.equal(sample.cRho, "1/2");
  assert.equal(sample.DminusKQ, "-4");
  assert.equal(sample.minusCRhoTimesDplusC, "-4");
});

test("locks the periodic disjoint-frame initial realization", async () => {
  const archived = await archivedResult();
  const ledger = archived.periodicRealizationLedger;
  const point = ledger.atX1Zero;
  const sample = ledger.farSeparatedRationalInstance;

  assert.equal(ledger.vorticityDivergence, "0");
  assert.equal(ledger.velocityDivergence, "0");
  assert.deepEqual(ledger.curlResidual, ["0", "0", "0"]);
  assert.equal(ledger.activeIndexIntersection, "empty");
  assert.equal(ledger.kGroupCoefficientSquareSum, "1");
  assert.equal(ledger.ellGroupCoefficientSquareSum, "1");
  assert.equal(point.D, "p**2");
  assert.equal(point.C, "q**2");
  assert.equal(point.sharpDeficitResidual, "0");
  assert.equal(sample.k, "2");
  assert.equal(sample.ell, "32");
  assert.equal(sample.D, "4");
  assert.equal(sample.C, "4");
  assert.equal(sample.KQ, "8");
  assert.match(ledger.initialDatumBoundary, /valid smooth NSE initial datum/);
  assert.match(ledger.initialDatumBoundary, /does not assert preservation/);
});

test("locks every R0.70R certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070r_exact_audit\.py/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});
