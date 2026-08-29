import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificate = "research/certificates/r073a";
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || (existsSync(bundledPython) ? bundledPython : "python3");
const run = promisify(execFile);
const csvPath = "experiments/r073a/xmu_propagator_certificate.csv";

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function sha(relative) {
  return createHash("sha256").update(await readFile(resolve(root, relative))).digest("hex");
}

test("R0.73A generated certificate records exact claims and strict boundaries", async () => {
  const [payload, crosscheck, manifest] = await Promise.all([
    json(`${certificate}/certificate.json`),
    json(`${certificate}/crosscheck.json`),
    json(`${certificate}/manifest.json`),
  ]);
  assert.equal(payload.release, "R0.73A");
  assert.equal(payload.status, "passed");
  assert.ok(payload.exactChecks.matrixSimilarity.every((row) => row.entrywiseExact));
  assert.ok(payload.exactChecks.meanCancellation.every(
    (row) => row.modes.every((mode) => mode.exact),
  ));
  assert.equal(payload.exactChecks.hiddenMeanDerivative.limitEquals, "Pi0(W(s)^2)");
  const supporting = payload.exactChecks.supportingAlgebra;
  assert.equal(supporting.orthogonalProjectionSpeed.maximum, "3/2");
  assert.equal(supporting.orthogonalProjectionSpeed.equalityD, "log(2)/3");
  assert.deepEqual(
    supporting.adjointPressureG.fourierCoefficients.map((row) => row.sum),
    ["-3/16", "3/32", "-37/144", "3/32"],
  );
  assert.equal(supporting.twoModeLeakage.kernelLine, "a*x2+2*b*x1=0");
  assert.equal(supporting.twoModeLeakage.noninvarianceRequires, "c!=0");
  assert.ok(supporting.positiveGapDualConstant.samples.every(
    (row) => row.equalsOneOverG,
  ));
  assert.equal(supporting.positiveGapDualConstant.fullOperatorTheoremProved, false);
  assert.equal(
    supporting.positiveGapDualConstant.operatorNormDiscontinuityDirectlyProved,
    false,
  );
  assert.equal(payload.scope.finiteFourierMatricesOnly, true);
  assert.equal(payload.scope.infiniteDimensionalTheoremMachineChecked, false);
  assert.equal(payload.scope.numericsUsedAsProof, false);
  for (const key of [
    "supportingAlgebraPromotedToFullOperatorTheorem",
    "infiniteDimensionalPropagatorProvedByCertificate",
    "lowGapA2EnhancedDissipationProved", "physicalKineticPropagatorProved",
    "OSSquirePropagatorProved", "nonlinearNavierStokesProved",
    "clayMillenniumProblemSolved",
  ]) assert.equal(payload.claimBoundary[key], false, key);
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.randomNumbersUsed, false);
  assert.equal(crosscheck.finiteMatrixOnly, true);
  assert.equal(crosscheck.caseCount, 120);
  assert.ok(crosscheck.worstRatio <= 1 + crosscheck.tolerance);
  assert.ok(["source-stage", "formal"].includes(manifest.status));
  if (manifest.status === "source-stage") {
    assert.equal(manifest.sourceCommit, null);
  } else {
    assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  }
  assert.equal(manifest.externalOutputs[0].path, csvPath);
});

test("R0.73A independent CSV has exact schema and stage-consistent lineage", async () => {
  const manifest = await json(`${certificate}/manifest.json`);
  const rows = (await text(csvPath)).trimEnd().split("\n");
  assert.equal(
    rows[0],
    "certificateId,s,d,mu,c,gain,bound,sourceCommit,certificateCommit",
  );
  assert.equal(rows.length, 121);
  for (const row of rows.slice(1)) {
    const columns = row.split(",");
    assert.equal(columns.length, 9);
    assert.equal(
      columns[7],
      manifest.status === "formal" ? manifest.sourceCommit : "pending",
    );
    assert.equal(columns[8], "pending");
    assert.ok(Number(columns[5]) <= Number(columns[6]) + 2e-8);
  }
});

test("R0.73A source bindings and flat SHA ledger are exhaustive", async () => {
  const manifest = await json(`${certificate}/manifest.json`);
  for (const binding of manifest.sourceBindings) {
    assert.equal(await sha(binding.path), binding.sha256, binding.path);
    assert.equal((await readFile(resolve(root, binding.path))).byteLength, binding.bytes);
  }
  const directory = resolve(root, certificate);
  const rows = (await text(`${certificate}/SHA256SUMS`)).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
    assert.equal(await sha(`${certificate}/${match[2]}`), match[1], match[2]);
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries.filter((entry) => entry.name !== "SHA256SUMS").map((entry) => entry.name).sort(),
  );
});

test("R0.73A strict independent validator accepts the generated package", async () => {
  const manifest = await json(`${certificate}/manifest.json`);
  const flag = manifest.status === "formal" ? "--require-formal" : "--require-source-stage";
  const result = await run(python, [
    `${certificate}/validate_certificate.py`, flag,
  ], {
    cwd: root,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    maxBuffer: 8 * 1024 * 1024,
  });
  assert.match(
    result.stdout,
    new RegExp(`strict ${manifest.status} certificate validation passed`),
  );
});

test("R0.73A formal mode fails closed on an unfrozen or stale source tree", async () => {
  const head = (await run("git", ["rev-parse", "HEAD"], { cwd: root })).stdout.trim();
  const protectedPaths = [
    `${certificate}/certificate.json`, `${certificate}/crosscheck.json`,
    `${certificate}/manifest.json`, `${certificate}/SHA256SUMS`, csvPath,
  ];
  const before = Object.fromEntries(await Promise.all(protectedPaths.map(async (path) => [
    path, await sha(path),
  ])));
  await assert.rejects(run(python, [
    `${certificate}/generate_certificate.py`, "--formal", "--source-commit", head,
  ], {
    cwd: root,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    maxBuffer: 8 * 1024 * 1024,
  }));
  const after = Object.fromEntries(await Promise.all(protectedPaths.map(async (path) => [
    path, await sha(path),
  ])));
  assert.deepEqual(after, before);
});
