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
const node = process.env.CODEX_NODE || process.execPath;

test("R0.74R frozen analytic package and three exact certificates pass", () => {
  assert.equal(sha("research/r074r_freeze_manifest.json"), "a1643ff56c0393edc378f5889dc451aa4d31ea2bfccbbf4dcd8edc9a3304b583");
  const freeze = JSON.parse(text("research/r074r_freeze_manifest.json"));
  assert.equal(Object.keys(freeze.artifacts).length, 19);
  for (const artifact of Object.values(freeze.artifacts)) {
    assert.equal(statSync(resolve(root, artifact.path)).size, artifact.bytes, artifact.path);
    assert.equal(sha(artifact.path), artifact.sha256, artifact.path);
  }
  assert.equal(freeze.claim_status.terminal_window_lobe_packing, "PROVED");
  assert.equal(freeze.claim_status.first_shell_concentration, "PROVED_IN_FROZEN_TARGET_FAMILY");
  assert.equal(freeze.claim_status.three_way_arbitrary_clock_triage, "PROVED");
  assert.equal(freeze.claim_status.persistence_to_cubic_payment, "PROVED");
  assert.equal(freeze.claim_status.arbitrary_clock_to_Q1, "PROVED_IMPLICATION_CONDITIONAL_INPUT");
  assert.equal(freeze.claim_status.universal_extraction_hypotheses, "OPEN_NOT_CLAIMED");
  assert.equal(freeze.claim_status.functional_no_go_witnesses, "PROVED_ABSTRACT_OR_FUNCTIONAL_NOT_NSE_SOLUTIONS");
  assert.equal(freeze.claim_status.fixed_scale_Q1, "OPEN");
  assert.equal(freeze.claim_status.formal_figure, "REQUIRED_FOR_PUBLICATION_DERIVED_FROM_FROZEN_ANALYTIC_SOURCE");
  assert.equal(freeze.claim_status.simulation_or_dns, "NOT_USED");
  assert.equal(freeze.claim_status.dgx, "NOT_USED");
  assert.equal(freeze.publication_handoff.target_primary_figure, "/assets/r074r/fig-r074r-clock-triage.svg");

  for (const [script, certificate, expected] of [
    ["scripts/r074r_persistent_lobe_certificate.py", "research/r074r_persistent_lobe_certificate.json", { power_ledger_passed: true, rational_passed: 21, rational_total: 21, result: "PASS", structural_passed: 22, structural_total: 22 }],
    ["scripts/r074r_arbitrary_clock_gate_certificate.py", "research/r074r_arbitrary_clock_gate_certificate.json", { power_ledgers_passed: 3, power_ledgers_total: 3, rational_passed: 13, rational_total: 13, result: "PASS", structural_passed: 25, structural_total: 25 }],
  ]) {
    const before = sha(certificate);
    execFileSync(python, [resolve(root, script)], { cwd: root });
    assert.equal(sha(certificate), before, `${certificate}: deterministic producer bytes`);
    assert.deepEqual(JSON.parse(text(certificate)).summary, expected);
  }

  const independent = execFileSync(node, [resolve(root, "scripts/r074r_arbitrary_clock_independent_audit.mjs")], { cwd: root });
  assert.deepEqual(independent, read("research/r074r_arbitrary_clock_independent_certificate.json"));
  assert.deepEqual(JSON.parse(independent).summary, { rational_passed: 9, rational_total: 9, structural_passed: 12, structural_total: 12, finite_passed: 5, finite_total: 5, result: "PASS" });
});

test("R0.74R frozen sources preserve equations, scope, and literature boundary", () => {
  const problem = text("research/r074r_problem_freeze.md");
  const lobe = text("research/r074r_persistent_lobe_cubic_packing.md");
  const clock = text("research/r074r_arbitrary_clock_extraction_gate.md");
  const reader = text("research/r074r_report-source.md");
  const literature = text("research/r074r_primary_literature_boundary.md");
  assert.equal(new Set(problem.match(/\\tag\{R\.[0-9]+\}/g) ?? []).size, 28);
  assert.equal(new Set(lobe.match(/\\tag\{R\.1[0-9]{2}\}/g) ?? []).size, 39);
  assert.equal(new Set(clock.match(/\\tag\{R\.2[0-9]{2}\}/g) ?? []).size, 26);
  for (const marker of ["窗口情形 PROVED", "CONDITIONAL / PROVED IMPLICATION", "三个不能绕过的 no-go 检验", "NOT CLAY"]) assert.ok(reader.includes(marker), marker);
  for (const marker of ["Neustupa", "Barker", "Yu", "finite non-hit statement", "not a novelty", "NOT CLAY"]) assert.match(literature, new RegExp(marker, "i"));
});
