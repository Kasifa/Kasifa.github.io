import assert from "node:assert/strict";
import { mkdtemp, readFile, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const python = process.env.CODEX_PYTHON
  ?? "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const deps = process.env.R073I_DEPS_DIR ?? "/tmp/r073c-deps";
const producer = resolve(root, "experiments/r073i/selected_gain_action_diagnostic.py");
const validator = resolve(root, "experiments/r073i/validate.py");
const config = resolve(root, "experiments/r073i/config.json");

const run = (command, env = {}) => spawnSync(command[0], command.slice(1), {
  cwd: root,
  encoding: "utf8",
  env: {
    ...process.env,
    OPENBLAS_NUM_THREADS: "1",
    OMP_NUM_THREADS: "1",
    VECLIB_MAXIMUM_THREADS: "1",
    ...env,
  },
});

test("R0.73I finite producer smoke run is reproducible and fail-closed", async () => {
  const directory = await mkdtemp(resolve(tmpdir(), "r073i-smoke-"));
  try {
    const produced = run([
      python, producer, "--deps", deps, "--config", config,
      "--output-dir", directory, "--smoke", "--overwrite",
    ]);
    assert.equal(produced.status, 0, produced.stderr || produced.stdout);

    const checked = run([python, validator, "--directory", directory]);
    assert.equal(checked.status, 0, checked.stderr || checked.stdout);
    const validation = JSON.parse(checked.stdout);
    assert.equal(validation.allChecksPass, true);
    assert.ok(Object.values(validation.checks).every(Boolean));

    const summary = JSON.parse(await readFile(resolve(directory, "summary.json"), "utf8"));
    assert.equal(summary.schemaVersion, "r073i-finite-summary-v1");
    assert.equal(summary.diagnosticOnly, true);
    assert.equal(summary.counts.windowCount, 3);
    assert.equal(summary.allChecksPass, true);
    assert.equal(summary.claimBoundary.finiteBinary64GalerkinDiagnostic, true);
    for (const [key, value] of Object.entries(summary.claimBoundary)) {
      if (key !== "finiteBinary64GalerkinDiagnostic") assert.equal(value, false, key);
    }
    assert.deepEqual(
      summary.windowSummaries.map((row) => row.windowId),
      ["explicit-pilot", "analytic-upper-bound", "one-over-450"],
    );
    for (const row of summary.windowSummaries) assert.match(row.role, /not/i);
  } finally {
    await rm(directory, { recursive: true, force: true });
  }
});

test("R0.73I source schema names every required finite artifact and boundary", async () => {
  const [schema, configValue] = await Promise.all([
    readFile(resolve(root, "experiments/r073i/summary.schema.json"), "utf8").then(JSON.parse),
    readFile(config, "utf8").then(JSON.parse),
  ]);
  assert.equal(schema.properties.schemaVersion.const, "r073i-finite-summary-v1");
  assert.equal(schema.properties.diagnosticOnly.const, true);
  assert.deepEqual(configValue.action.cutoffs, [24, 48, 96]);
  assert.deepEqual(configValue.action.quadratureOrders, [32, 64]);
  assert.deepEqual(configValue.gain.stepComparison.fastSteps, [0.5, 0.25, 0.125]);
  assert.equal(configValue.claimBoundary.finiteActionIsContinuumAction, false);
  assert.equal(configValue.claimBoundary.analyticUpperBoundEqualsD0, false);
  assert.equal(configValue.claimBoundary.oneOver450IsTheoremEndpoint, false);
  assert.equal(configValue.claimBoundary.clayProblemSolved, false);
});
