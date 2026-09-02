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

test("R0.74S deterministic certificate producers rerun byte-identically", () => {
  const cases = [
    ["scripts/r074s_boundary_mismatch_certificate.py", "research/r074s_boundary_mismatch_certificate.json", { exact_passed: 14, exact_total: 14, finite_passed: 4, finite_total: 4, result: "PASS", structural_passed: 38, structural_total: 38 }],
    ["scripts/r074s_actual_collar_decomposition_certificate.py", "research/r074s_actual_collar_decomposition_certificate.json", { exact_passed: 6, exact_total: 6, finite_passed: 2, finite_total: 2, result: "PASS", structural_passed: 23, structural_total: 23 }],
    ["scripts/r074s_terminal_upcrossing_certificate.py", "research/r074s_terminal_upcrossing_certificate.json", { exact_passed: 5, exact_total: 5, finite_passed: 1, finite_total: 1, result: "PASS", structural_passed: 19, structural_total: 19 }],
    ["scripts/r074s_weighted_abel_certificate.py", "research/r074s_weighted_abel_certificate.json", { exact_passed: 6, exact_total: 6, finite_passed: 2, finite_total: 2, result: "PASS", structural_passed: 16, structural_total: 16 }],
    ["scripts/r074s_one_sided_ball_clock_certificate.py", "research/r074s_one_sided_ball_clock_certificate.json", { exact_passed: 5, exact_total: 5, finite_passed: 7, finite_total: 7, negative_passed: 4, negative_total: 4, result: "PASS", structural_passed: 55, structural_total: 55 }],
  ];
  for (const [script, certificate, expected] of cases) {
    const before = sha(certificate);
    execFileSync(python, [resolve(root, script)], { cwd: root });
    assert.equal(sha(certificate), before, `${certificate}: deterministic producer bytes`);
    assert.deepEqual(JSON.parse(text(certificate)).summary, expected);
  }
});
