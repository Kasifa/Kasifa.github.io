import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const directory = resolve(root, "experiments/r073f");
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const sha256 = async (relative) => createHash("sha256")
  .update(await readFile(resolve(root, relative))).digest("hex");

const falseBoundaries = [
  "diagnosticDIsCertifiedD0",
  "finiteTopEqualsContinuumTop",
  "ordinaryCutoffAgreementIsTailProof",
  "finiteGainProvesContinuumDichotomy",
  "sampledTimeIsContinuousTimeBound",
  "finiteRateEqualsAnalyticKappa",
  "counterexamplesDescribeExactFourierRow",
  "nonlinearNavierStokes",
  "Clay",
];

test("R0.73F primary finite diagnostic passes every declared sentinel without escaping its boundary", async () => {
  const [summary, config, environment] = await Promise.all([
    json("experiments/r073f/summary.json"),
    json("experiments/r073f/config.json"),
    json("experiments/r073f/environment.json"),
  ]);
  assert.equal(summary.allPrimaryChecksPass, true);
  assert.ok(Object.values(summary.checks).every(Boolean));
  assert.equal(summary.diagnosticPhysicalEndpoint, 0.01);
  assert.equal(summary.diagnosticEndpointIsCertifiedD0, false);
  assert.equal(summary.primaryGrid.N, 96);
  assert.deepEqual(summary.primaryGrid.epsilons, [0.01, 0.005, 0.002, 0.001, 0.0005, 0.0003, 0.0002, 0.0001]);
  assert.deepEqual(config.cutoffComparison.cutoffs, [24, 48, 96]);
  assert.equal(summary.finiteSentinels.maximumFinestStepPairLogDifference < 9e-12, true);
  assert.equal(summary.finiteSentinels.maximumProjectorIdempotenceResidual < 1e-14, true);
  assert.equal(summary.finiteSentinels.maximumProjectorCommutatorResidual < 2e-14, true);
  assert.equal(summary.finiteSentinels.sign.generatorConjugacyDefect, 0);
  assert.equal(summary.counterexamples.rotatingPositiveEdge.exactMinimumPointwiseMaximum, 0.25);
  assert.equal(summary.counterexamples.rotatingPositiveEdge.exactBranchIntegral, -0.25);
  assert.equal(environment.dgxUsed, false);
  assert.match(environment.dgxReason, /193 by 193/);
  assert.equal(summary.claimBoundary.finiteBinary64Diagnostic, true);
  for (const key of falseBoundaries) assert.equal(summary.claimBoundary[key], false, key);
});

test("R0.73F independent implementation reconstructs matrices and selected gains", async () => {
  const independent = await json("experiments/r073f/independent_validation.json");
  assert.equal(independent.allChecksPass, true);
  assert.ok(Object.values(independent.checks).every(Boolean));
  assert.equal(independent.validator.importsPrimaryProducer, false);
  assert.equal(independent.maximums.matrixConstructionAbsolute < 6e-17, true);
  assert.equal(independent.maximums.logGainAbsolute < 9e-12, true);
  assert.equal(independent.maximums.normalizedRateAbsolute < 3e-12, true);
  const endpoint = independent.validations.find((row) => row.N === 96 && row.epsilon === 0.0001);
  assert.ok(endpoint);
  assert.ok(Math.abs(endpoint.actual.logFullNorm - 17.373903829670912) < 2e-12);
  assert.ok(Math.abs(endpoint.actual.logTopConorm - 16.857560069249697) < 2e-12);
  assert.ok(Math.abs(endpoint.actual.normalizedFullRate - 0.17373903829670911) < 2e-14);
  assert.ok(Math.abs(endpoint.actual.normalizedTopRate - 0.16857560069249697) < 2e-14);
  for (const key of falseBoundaries) assert.equal(independent.claimBoundary[key], false, key);
});

test("R0.73F finite package has a complete content-addressed inventory", async () => {
  const [manifest, rows, names] = await Promise.all([
    json("experiments/r073f/manifest.json"),
    text("experiments/r073f/SHA256SUMS"),
    readdir(directory),
  ]);
  assert.equal(manifest.status, "validated");
  assert.equal(manifest.inventoryPolicy.benchmarkIncluded, true);
  assert.equal(manifest.inventoryPolicy.cacheDirectoriesForbidden, true);
  assert.deepEqual(manifest.inventoryPolicy.sha256LedgerExcludes, ["SHA256SUMS"]);
  const ledger = rows.trim().split("\n").map((row) => {
    const match = row.match(/^([0-9a-f]{64})  ([^/]+)$/);
    assert.ok(match, row);
    return { sha: match[1], name: match[2] };
  });
  const actual = names.filter((name) => name !== "SHA256SUMS").sort();
  assert.deepEqual(ledger.map((row) => row.name).sort(), actual);
  for (const row of ledger) {
    assert.equal(await sha256(`experiments/r073f/${row.name}`), row.sha, row.name);
  }
  const manifestNames = manifest.files.map((row) => row.path.split("/").at(-1)).sort();
  assert.deepEqual(manifestNames, actual.filter((name) => name !== "manifest.json"));
  assert.equal(manifest.claimBoundary.diagnosticDIsCertifiedD0, false);
});
