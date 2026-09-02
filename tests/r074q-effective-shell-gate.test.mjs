import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFileSync, statSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFileSync(resolve(root, path));
const text = (path) => read(path).toString("utf8");
const sha = (path) => createHash("sha256").update(read(path)).digest("hex");
const python = process.env.CODEX_PYTHON || process.env.PYTHON || "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";

test("R0.74Q frozen analytic package and both exact certificates pass", () => {
  assert.equal(sha("research/r074q_freeze_manifest.json"), "8cb1d3c9089e9694ef753655c8a7e06d69c7e9a3838a35ea3b5f93219b4e4d01");
  const freeze = JSON.parse(text("research/r074q_freeze_manifest.json"));
  assert.equal(Object.keys(freeze.artifacts).length, 18);
  for (const artifact of Object.values(freeze.artifacts)) {
    assert.equal(statSync(resolve(root, artifact.path)).size, artifact.bytes, artifact.path);
    assert.equal(sha(artifact.path), artifact.sha256, artifact.path);
  }
  assert.equal(freeze.claim_status.terminal_effective_shell_reduction, "PROVED");
  assert.equal(freeze.claim_status.finite_common_shear_exact_nse, "PROVED_MECHANISM_KNOWN_NOT_NOVELTY_CLAIM");
  assert.equal(freeze.claim_status.frozen_angle_common_B_obstruction, "PROVED_FOR_SPECIFIED_ASYMPTOTIC_GEOMETRY_NOT_UNIVERSAL_NO_GO");
  assert.equal(freeze.claim_status.relaxed_calibration_and_common_terminal_geometry, "PROVED_FOR_EXPLICIT_GROWING_FINITE_FAMILY");
  assert.equal(freeze.claim_status.outer_velocity_cubic_payment, "PROVED_TRUE_NONNEGATIVE_LOWER_BOUND");
  assert.equal(freeze.claim_status.full_square_function_matching_upper, "OPEN_NOT_CLAIMED");
  assert.equal(freeze.claim_status.signed_cumulative_flux_order_NT, "OPEN_NOT_CLAIMED");
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.simulation_or_dns, "NOT_USED");
  assert.equal(freeze.claim_status.dgx, "NOT_USED");
  assert.equal(freeze.publication_handoff.target_primary_figure, null);

  for (const [script, certificate, expected] of [
    ["scripts/r074q_common_shear_gate_certificate.py", "research/r074q_common_shear_gate_certificate.json", { rational_passed: 21, rational_total: 21, result: "PASS", structural_passed: 19, structural_total: 19 }],
    ["scripts/r074q_relaxed_multipacket_certificate.py", "research/r074q_relaxed_multipacket_certificate.json", { rational_passed: 22, rational_total: 22, result: "PASS", structural_passed: 41, structural_total: 41 }],
  ]) {
    const produced = execFileSync(python, [resolve(root, script)]);
    assert.deepEqual(produced, read(certificate), `${certificate}: fresh producer bytes`);
    assert.deepEqual(JSON.parse(produced).summary, expected);
  }
});

test("R0.74Q frozen sources preserve equations, scope, and literature boundary", () => {
  const problem = text("research/r074q_problem_freeze.md");
  const reader = text("research/r074q_report-source.md");
  const literature = text("research/r074q_primary_literature_boundary.md");
  assert.equal(new Set(problem.match(/\\tag\{[^}]+\}/g) ?? []).size, 28);
  for (const marker of ["terminal effective-shell", "共同剪切", "all-lobe", "cubic payment", "signed flux", "NOT CLAY"]) {
    assert.ok(reader.toLowerCase().includes(marker.toLowerCase()), marker);
  }
  assert.match(literature, /2D3C/);
  assert.match(literature, /not a novelty|不证明新颖性/i);
});
