import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync, spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFileSync(resolve(root, path));
const text = (path) => read(path).toString("utf8");
const sha = (path) => createHash("sha256").update(read(path)).digest("hex");
const python = process.env.CODEX_PYTHON || process.env.PYTHON || "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";

test("R0.74S frozen Step 1–5 sources and audits retain their exact boundary", () => {
  const hashes = {
    "research/r074s_one_sided_ball_clock_no_gain.md": "178c3431f808fa0bb7c8bbf116bd2fdf8c7335eea75e93ba11f51d7eeba7f1af",
    "research/r074s_one_sided_ball_clock_certificate.json": "1afcea511445b75c05da034130c4f1719f4b129c1df496ba5b3f65025ff57219",
    "research/r074s_one_sided_ball_clock_primary_audit.md": "83093d667b0f0ac0af919651c4dd45f87e60b8d2ebde59017f8abdfbd33041b9",
    "research/r074s_one_sided_ball_clock_independent_audit.md": "5ee63f78699891801151171f7fa68e103e52b04d2cc07b20ce48c1d3dd31b209",
  };
  for (const [path, expected] of Object.entries(hashes)) assert.equal(sha(path), expected, path);
  const source = text("research/r074s_one_sided_ball_clock_no_gain.md");
  for (const marker of [
    "route rejection",
    "counterexample built from a Navier--Stokes solution",
    "dynamical sign",
    "fixed-scale inequality",
    "NOT CLAY",
  ]) assert.match(source, new RegExp(marker, "i"), marker);
});

test("R0.74S frozen Step 6 sources and dual audits retain their exact boundary", () => {
  const hashes = {
    "research/r074s_cross_channel_recombination_no_gain.md": "c24d3673a5e3315777b47fa9751f8546a7df99538b6b22df7566ceb8fdce2e03",
    "scripts/r074s_cross_channel_recombination_certificate.py": "88644cdb311987755777fb951d1eb2ce5e0bdf0e6b829399832def0d9c54cb7c",
    "scripts/r074s_cross_channel_recombination_certificate_independent.rb": "cd5d7afadbaa9a257681f82d9e373777ac735c7675359310fb3a6efffc10ecef",
    "research/r074s_cross_channel_recombination_certificate.json": "5cd6ce5ba59586154c39cdfc5904eec4894dd51370d0cb02c0cd51bff58f4a63",
    "research/r074s_cross_channel_recombination_certificate_report.md": "548a68ca6ae82ea5f18e22504ee41da507569da4c283dbb8506f24b384aba189",
  };
  for (const [path, expected] of Object.entries(hashes)) assert.equal(sha(path), expected, path);
  const source = text("research/r074s_cross_channel_recombination_no_gain.md");
  for (const marker of ["circular", "three-channel", "scalar completed-clock algebra", "PDE counterexample", "NOT CLAY"]) assert.match(source, new RegExp(marker, "i"), marker);
});

test("R0.74S frozen Step 7 sources and dual audits retain their exact boundary", () => {
  const hashes = {
    "research/r074s_dissipation_rayleigh_gate.md": "e835a104f4a6f4d2281bef877dd6bfeb73f1c2396f6bd28203bb0812f7f8e3d3",
    "research/r074s_dissipation_rayleigh_primary_audit.md": "304bc2b87b9eb97d4f46d8bc4a77da3b1f11e2c37e95e20956504bb4681b2175",
    "research/r074s_dissipation_rayleigh_independent_audit.md": "efc30eb21e8d4e125d4b189455d4419bca9b5d1f1effeb265edba1cdf4a48233",
    "scripts/r074s_dissipation_rayleigh_certificate.py": "61bb1322151b66fc0cf780d2dfc15e0e06dde9a6cc59cc192be1b8c9e8d5e76a",
    "scripts/r074s_dissipation_rayleigh_certificate_independent.rb": "a4ce5bb0d3f20f549e70b7196487fd9540a5ff7be658d4cd52573d65f1a77ff3",
    "research/r074s_dissipation_rayleigh_certificate.json": "4f26fefe25ec92cdae86c2a45f384d0ed87ab3afe83a7d9ef7829ff829be6be1",
    "research/r074s_dissipation_rayleigh_certificate_report.md": "5c566f53e378c9f3fba2a690c3962051142ac00990c1177548b9ae3e956b14cb",
  };
  for (const [path, expected] of Object.entries(hashes)) assert.equal(sha(path), expected, path);
  const source = text("research/r074s_dissipation_rayleigh_gate.md");
  for (const marker of ["low-Rayleigh", "high-Rayleigh", "anomalous-defect", "finite-exception", "NOT CLAY"]) {
    assert.match(source, new RegExp(marker, "i"), marker);
  }
});

test("R0.74S frozen final Step 8 sources and dual audits retain the corrected no-exception boundary", () => {
  const hashes = {
    "research/r074s_defect_relaxed_total_rayleigh_excess.md": "0a79f2c5bb59644eca710b3d9341776853ceb4d1f65a36869c2465073f8c08ab",
    "research/r074s_defect_relaxed_total_rayleigh_primary_audit.md": "dbcba5ea68899faf74e4d38c232c58fdd3a71f1b2dcefb1eb007fcf102cd4f73",
    "research/r074s_defect_relaxed_total_rayleigh_independent_audit.md": "d7cb626b07b735b6ef19c8ca20fff670795e32768f3224a756901b230183d875",
    "scripts/r074s_defect_relaxed_total_rayleigh_certificate.py": "18735df5a8eff96167ef6314dad04150636c800c276e2fcffc7cbd8177fce9cf",
    "scripts/r074s_defect_relaxed_total_rayleigh_certificate_independent.rb": "b18b0a0b9937b106c5879a9e28996dd6892ab53f19decb7bca4db38c70a11343",
    "research/r074s_defect_relaxed_total_rayleigh_certificate.json": "3639edbccfddd97781805ed121fc91407771b9bf051ffefae5a17ad80087c69c",
    "research/r074s_defect_relaxed_total_rayleigh_certificate_report.md": "3a6d1e263daa7041edc4083a76c38af44f4fbcd7d2efc8f57592eecbd19ec55a",
  };
  for (const [path, expected] of Object.entries(hashes)) assert.equal(sha(path), expected, path);
  const source = text("research/r074s_defect_relaxed_total_rayleigh_excess.md");
  for (const marker of ["S.197", "S.198", "S.199", "universal antecedent", "fixed best-", "conditional implication \\(S\\.38\\)", "NOT CLAY"]) {
    assert.match(source, new RegExp(marker, "i"), marker);
  }
});

test("R0.74S frozen Step 9 best-N last-exit sources and dual audits retain the no-gain boundary", () => {
  const hashes = {
    "research/r074s_best_n_last_exit_equivalence.md": "85003b3fdfdf28618a82a57d241e86c086704ea3ed3a9b192de223f3b8c3a4dd",
    "research/r074s_best_n_last_exit_primary_audit.md": "0d326d0b77e499c36aa10fac64db66d4c40e6f0599640df65c915ca8de5f58d1",
    "research/r074s_best_n_last_exit_independent_audit.md": "e67b0f6cfcfa15f8e0b7f4f96670e10a843aabd753dd25d7ce5684e6c993a634",
    "scripts/r074s_best_n_last_exit_certificate.py": "0f04b79049ecd92c4a366ad9916fc8b6da9220b2f5baee34726aef2d4feaee65",
    "scripts/r074s_best_n_last_exit_certificate_independent.rb": "d9c0674b79bc532c10366d317ccb10550f0bfd2a825127e87a4ef24633d3ae66",
    "research/r074s_best_n_last_exit_certificate.json": "26ee76d969d3aec5eec55d9fa981bce195538cc3e2464fc0ece2c46b7c4accf0",
    "research/r074s_best_n_last_exit_certificate_report.md": "1108b72113d84b90ebc5570c2c7b4bfaa1ccdc299525c557979b564109ab6481",
  };
  for (const [path, expected] of Object.entries(hashes)) assert.equal(sha(path), expected, path);
  const source = text("research/r074s_best_n_last_exit_equivalence.md");
  for (const marker of ["S.207", "S.214", "S.218", "theta<3/4", "no-gain", "residual full tail", "NOT CLAY"]) {
    assert.match(source, new RegExp(marker, "i"), marker);
  }
});

test("R0.74S frozen Step 10 paid-branch residual sources and dual audits retain the shared-gate boundary", () => {
  const hashes = {
    "research/r074s_paid_branch_last_exit_residual.md": "9eb5f2a794021b49894adfc167d350f58d93c266e6be319ce835c58db2e0d74c",
    "research/r074s_paid_branch_last_exit_primary_audit.md": "cf7bbfcb01a5389878a2a9f65ffa0e083863f8f6478986bc10110cfd24e6446c",
    "research/r074s_paid_branch_last_exit_independent_audit.md": "cb33dd2a1fed8a58f285bdb3e7a053480c40b06a899d1a1bd3a18549b6b8125a",
    "scripts/r074s_paid_branch_last_exit_certificate.py": "2763b3fa575ce723a400b6c7e5654d0a64c8a9db470d79097dc5a77769a365a9",
    "research/r074s_paid_branch_last_exit_certificate.json": "8f37a8ce4d6513406297e6ce1e676ceaafa39776723bba839074120f206314de",
    "research/r074s_paid_branch_last_exit_certificate_report.md": "6e25a07a417f96907e5e17da6b561830b75aa1a44d0b4b13fa56107dc31e4a5f",
    "scripts/r074s_paid_branch_last_exit_certificate_independent.rb": "15b77560f41aa22d00447821be501ab5d3c992afa1001063c3ce986f2e9938c9",
  };
  for (const [path, expected] of Object.entries(hashes)) assert.equal(sha(path), expected, path);
  const source = text("research/r074s_paid_branch_last_exit_residual.md");
  for (const marker of ["S.225", "S.233", "S.240", "S.243", "one complete cubic", "NOT CLAY"]) {
    assert.match(source, new RegExp(marker, "i"), marker);
  }
  assert.ok(source.includes("one complete \\(Q\\)-ledger"));
});

test("R0.74S deterministic certificate producers rerun byte-identically", () => {
  const cases = [
    ["scripts/r074s_boundary_mismatch_certificate.py", "research/r074s_boundary_mismatch_certificate.json", { exact_passed: 14, exact_total: 14, finite_passed: 4, finite_total: 4, result: "PASS", structural_passed: 38, structural_total: 38 }],
    ["scripts/r074s_actual_collar_decomposition_certificate.py", "research/r074s_actual_collar_decomposition_certificate.json", { exact_passed: 6, exact_total: 6, finite_passed: 2, finite_total: 2, result: "PASS", structural_passed: 23, structural_total: 23 }],
    ["scripts/r074s_terminal_upcrossing_certificate.py", "research/r074s_terminal_upcrossing_certificate.json", { exact_passed: 5, exact_total: 5, finite_passed: 1, finite_total: 1, result: "PASS", structural_passed: 19, structural_total: 19 }],
    ["scripts/r074s_weighted_abel_certificate.py", "research/r074s_weighted_abel_certificate.json", { exact_passed: 6, exact_total: 6, finite_passed: 2, finite_total: 2, result: "PASS", structural_passed: 16, structural_total: 16 }],
    ["scripts/r074s_one_sided_ball_clock_certificate.py", "research/r074s_one_sided_ball_clock_certificate.json", { exact_passed: 5, exact_total: 5, finite_passed: 7, finite_total: 7, negative_passed: 4, negative_total: 4, result: "PASS", structural_passed: 55, structural_total: 55 }],
    ["scripts/r074s_cross_channel_recombination_certificate.py", "research/r074s_cross_channel_recombination_certificate.json", { exact_passed: 4, exact_total: 4, finite_passed: 8, finite_total: 8, negative_passed: 10, negative_total: 10, result: "PASS", structural_passed: 58, structural_total: 58 }],
    ["scripts/r074s_dissipation_rayleigh_certificate.py", "research/r074s_dissipation_rayleigh_certificate.json", { exact_passed: 16, exact_total: 16, finite_passed: 8, finite_total: 8, negative_mutations_passed: 9, negative_mutations_total: 9, structural_passed: 52, structural_total: 52 }],
    ["scripts/r074s_defect_relaxed_total_rayleigh_certificate.py", "research/r074s_defect_relaxed_total_rayleigh_certificate.json", { exact_passed: 16, exact_total: 16, finite_passed: 19, finite_total: 19, negative_mutations_passed: 20, negative_mutations_total: 20, structural_passed: 75, structural_total: 75 }],
    ["scripts/r074s_best_n_last_exit_certificate.py", "research/r074s_best_n_last_exit_certificate.json", { exact_passed: 9, exact_total: 9, finite_passed: 8, finite_total: 8, negative_mutations_passed: 18, negative_mutations_total: 18, structural_passed: 57, structural_total: 57 }],
    ["scripts/r074s_paid_branch_last_exit_certificate.py", "research/r074s_paid_branch_last_exit_certificate.json", { exact_total: 12, exact_passed: 12, finite_total: 10, finite_passed: 10, structural_total: 79, structural_passed: 79, negative_mutations_total: 47, negative_mutations_passed: 47 }],
  ];
  for (const [script, certificate, expected] of cases) {
    const before = sha(certificate);
    execFileSync(python, [resolve(root, script)], { cwd: root });
    assert.equal(sha(certificate), before, `${certificate}: deterministic producer bytes`);
    assert.deepEqual(JSON.parse(text(certificate)).summary, expected);
  }
});

test("R0.74S Step 6 Ruby audit independently reconstructs and cross-checks the producer", () => {
  const output = execFileSync("ruby", [resolve(root, "scripts/r074s_cross_channel_recombination_certificate_independent.rb")], { cwd: root, encoding: "utf8" });
  const summary = JSON.parse(output).summary;
  assert.deepEqual(summary, { result: "PASS", independent_passed: 9, independent_total: 9, mutations_passed: 8, mutations_total: 8, producer_cross_check: "PASS" });
});

test("R0.74S Step 7 Ruby audit independently reconstructs and cross-checks the producer", () => {
  const output = execFileSync("ruby", [resolve(root, "scripts/r074s_dissipation_rayleigh_certificate_independent.rb")], { cwd: root, encoding: "utf8" });
  const summary = JSON.parse(output).summary;
  assert.deepEqual(summary, { result: "PASS", independent_passed: 6, independent_total: 6, structural_passed: 31, structural_total: 31, mutations_passed: 9, mutations_total: 9, producer_cross_check: "PASS" });
});

test("R0.74S final Step 8 Ruby audit independently reconstructs the corrected gate", () => {
  const output = execFileSync("ruby", [resolve(root, "scripts/r074s_defect_relaxed_total_rayleigh_certificate_independent.rb")], { cwd: root, encoding: "utf8" });
  const summary = JSON.parse(output).summary;
  assert.deepEqual(summary, {
    independent_checks_passed: 14, independent_checks_total: 14,
    exact_rows_passed: 22, exact_rows_total: 22,
    structural_passed: 61, structural_total: 61,
    source_mutations_rejected: 14, source_mutations_total: 14,
    artifact_mutations_rejected: 10, artifact_mutations_total: 10,
    report_checks_passed: 6, report_checks_total: 6,
  });
});

test("R0.74S Step 9 Ruby audit independently reconstructs the best-N last-exit boundary", () => {
  const output = execFileSync("ruby", [resolve(root, "scripts/r074s_best_n_last_exit_certificate_independent.rb")], { cwd: root, encoding: "utf8" });
  const summary = JSON.parse(output).summary;
  assert.deepEqual(summary, {
    independent_groups_passed: 12, independent_groups_total: 12,
    independent_finite_cases: 91396,
    structural_passed: 49, structural_total: 49,
    source_mutations_rejected: 21, source_mutations_total: 21,
    artifact_mutations_rejected: 15, artifact_mutations_total: 15,
    report_checks_passed: 6, report_checks_total: 6,
  });
});

test("R0.74S Step 10 Ruby audit independently reconstructs the paid-branch residual boundary", () => {
  const result = spawnSync("ruby", [resolve(root, "scripts/r074s_paid_branch_last_exit_certificate_independent.rb")], {
    cwd: root,
    encoding: "utf8",
  });
  assert.equal(result.status, 0, `Step 10 Ruby audit failed:\n${result.stdout}\n${result.stderr}`);
  const output = result.stdout;
  assert.equal(createHash("sha256").update(output).digest("hex"), "4877dc3a0de2c2f605641736c7355672f0a7a68cb97a37849d4a7c28495e8bbd");
  const parsed = JSON.parse(output);
  assert.equal(parsed.pass, true);
  assert.deepEqual(parsed.summary, {
    independent_groups_passed: 9, independent_groups_total: 9,
    independent_cases: 65681,
    artifact_hashes_passed: 6, artifact_hashes_total: 6,
    dependency_hashes_passed: 7, dependency_hashes_total: 7,
    note_checks_passed: 16, note_checks_total: 16,
    parser_checks_passed: 3, parser_checks_total: 3,
    contract_mutations_rejected: 21, contract_mutations_total: 21,
    report_checks_passed: 13, report_checks_total: 13,
    audit_bindings_passed: 15, audit_bindings_total: 15,
  });
});
