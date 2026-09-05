import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha256 = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("Clay-B frozen ledger binds the 7+2 research package and handoff envelope", () => {
  const ledger = JSON.parse(read("research/clay_b_two_scale_frozen_ledger_20260905.json"));
  assert.equal(ledger.schemaVersion, "clay-b-two-scale-frozen-ledger-v1");
  assert.equal(ledger.releaseId, "ClayB-TwoScale-20260905");
  assert.equal(ledger.sourceCommit, "59e628a44e71b5bc54317db16758d9e6efd91334");
  assert.equal(ledger.baseContractCommit, "bbe05cfc584b550d52b5f2c899dfc5e32491114d");
  assert.equal(ledger.handoffCommit, "a09229a714247c6f6e959661ba428e91c1cb3ab1");
  assert.equal(ledger.scientificFileCount, 7);
  assert.equal(ledger.dependencyFileCount, 2);
  assert.equal(ledger.files.length, 9);
  assert.equal(ledger.handoffEnvelope.length, 2);
  for (const row of [...ledger.files, ...ledger.handoffEnvelope]) {
    assert.equal(sha256(row.path), row.sha256, row.path);
  }
  const manifest = JSON.parse(read("research/clay_b_two_scale_release_20260905.json"));
  assert.equal(manifest.release_id, ledger.releaseId);
  assert.equal(manifest.source_commit, ledger.sourceCommit);
  assert.equal(manifest.status, "research-frozen");
  assert.deepEqual(manifest.scientific_figures, []);
  assert.equal(manifest.scientific_figure_required, false);
  assert.equal(manifest.simulation_required, false);
  assert.equal(manifest.recap_required, false);
  assert.equal(manifest.claim_boundaries.NOT_CLAY, true);
});

test("Clay-B analytic sources preserve all D and E formula tags and limitations", () => {
  const d = read("research/clay_b_two_scale_energy_working_20260905.md");
  const e = read("research/clay_b_two_scale_paid_budget_20260905.md");
  for (let index = 1; index <= 25; index += 1) {
    assert.match(d, new RegExp(`\\\\tag\\{D\\.${index}(?:-false)?\\}`), `D.${index}`);
  }
  for (let index = 1; index <= 10; index += 1) {
    assert.match(e, new RegExp(`\\\\tag\\{E\\.${index}\\}`), `E.${index}`);
  }
  for (const marker of [
    "R^{-2}||g||_2^2", "允许常数依赖初值", "有限时间累计后的抵消",
    "主合同 G 的核心未证假设", "不提供 E_{r}<=lambda E_R+e_R",
  ]) assert.ok(`${d}\n${e}`.includes(marker), marker);
});

test("exact rational Fourier regression reproduces the frozen finite certificate", () => {
  const python = process.env.CLAY_B_PYTHON ?? "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
  const actual = JSON.parse(execFileSync(python, ["scripts/clay_b_two_scale_fourier_check.py"], {
    cwd: root,
    encoding: "utf8",
  }));
  const frozen = JSON.parse(read("research/clay_b_two_scale_fourier_certificate_20260905.json"));
  for (const key of [
    "status", "arithmetic", "normalization", "energy_coefficients_by_squared_wave_number",
    "dissipation_coefficients_by_squared_wave_number", "nonlinear_production_coefficients_by_squared_wave_number",
    "initial_L2_squared", "initial_gradient_L2_squared", "initial_H1_squared",
    "small_R_production_over_dissipation_per_A",
    "small_R_production_over_energy_plus_dissipation_per_A", "input_sensitivity", "not_checked",
  ]) assert.deepEqual(actual[key], frozen[key], key);
  assert.equal(actual.runtime.precision, "exact rational");
  assert.equal(actual.runtime.workers, 1);
  assert.equal(actual.runtime.seed, null);
});
