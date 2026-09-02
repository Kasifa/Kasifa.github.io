import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
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

test("R0.74S deterministic certificate producers rerun byte-identically", () => {
  const cases = [
    ["scripts/r074s_boundary_mismatch_certificate.py", "research/r074s_boundary_mismatch_certificate.json", { exact_passed: 14, exact_total: 14, finite_passed: 4, finite_total: 4, result: "PASS", structural_passed: 38, structural_total: 38 }],
    ["scripts/r074s_actual_collar_decomposition_certificate.py", "research/r074s_actual_collar_decomposition_certificate.json", { exact_passed: 6, exact_total: 6, finite_passed: 2, finite_total: 2, result: "PASS", structural_passed: 23, structural_total: 23 }],
    ["scripts/r074s_terminal_upcrossing_certificate.py", "research/r074s_terminal_upcrossing_certificate.json", { exact_passed: 5, exact_total: 5, finite_passed: 1, finite_total: 1, result: "PASS", structural_passed: 19, structural_total: 19 }],
    ["scripts/r074s_weighted_abel_certificate.py", "research/r074s_weighted_abel_certificate.json", { exact_passed: 6, exact_total: 6, finite_passed: 2, finite_total: 2, result: "PASS", structural_passed: 16, structural_total: 16 }],
    ["scripts/r074s_one_sided_ball_clock_certificate.py", "research/r074s_one_sided_ball_clock_certificate.json", { exact_passed: 5, exact_total: 5, finite_passed: 7, finite_total: 7, negative_passed: 4, negative_total: 4, result: "PASS", structural_passed: 55, structural_total: 55 }],
    ["scripts/r074s_cross_channel_recombination_certificate.py", "research/r074s_cross_channel_recombination_certificate.json", { exact_passed: 4, exact_total: 4, finite_passed: 8, finite_total: 8, negative_passed: 10, negative_total: 10, result: "PASS", structural_passed: 58, structural_total: 58 }],
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
