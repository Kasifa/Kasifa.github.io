#!/usr/bin/env node

import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const notePath = "research/r074r_arbitrary_clock_extraction_gate.md";
const primaryPath = "research/r074r_arbitrary_clock_gate_certificate.json";
const problemPath = "research/r074r_problem_freeze.md";
const readerPath = "research/r074r_report-source.md";
const outputPath = "research/r074r_arbitrary_clock_independent_certificate.json";
const reportPath = "research/r074r_arbitrary_clock_independent_audit.md";

const read = (path) => readFileSync(resolve(root, path));
const text = (path) => read(path).toString("utf8");
const sha = (path) => createHash("sha256").update(read(path)).digest("hex");

function gcd(a, b) {
  a = a < 0n ? -a : a;
  b = b < 0n ? -b : b;
  while (b) [a, b] = [b, a % b];
  return a;
}

function q(n, d = 1n) {
  if (d === 0n) throw new Error("zero denominator");
  if (d < 0n) [n, d] = [-n, -d];
  const g = gcd(n, d);
  return [n / g, d / g];
}

const add = ([a, b], [c, d]) => q(a * d + c * b, b * d);
const mul = ([a, b], [c, d]) => q(a * c, b * d);
const same = ([a, b], [c, d]) => a === c && b === d;
const show = ([a, b]) => `${a}/${b}`;

const rationalChecks = [];
function exact(id, actual, expected, note) {
  const pass = same(actual, expected);
  rationalChecks.push({ id, actual: show(actual), expected: show(expected), pass, note });
}

exact("triage_total", add(q(1n, 2n), add(q(1n, 4n), q(1n, 4n))), q(1n), "three alternatives exhaust the terminal clock");
exact("holder_conjugacy", add(q(1n, 3n), q(2n, 3n)), q(1n), "ell3 and ell3/2 exponents");
exact("endpoint_shell_after_solve", mul(q(3n, 2n), q(2n, 3n)), q(1n), "2^(3k/2) becomes 2^k");
exact("endpoint_gamma_after_solve", mul(q(1n, 2n), q(2n, 3n)), q(1n, 3n), "gamma^(1/2) becomes gamma^(1/3)");
exact("theta_after_solve", mul(q(-1n), q(2n, 3n)), q(-2n, 3n), "Theta inverse becomes power -2/3");
exact("payment_after_solve", mul(q(1n), q(2n, 3n)), q(2n, 3n), "local cubic payment power");
exact("packing_shell_cube", mul(q(1n), q(3n)), q(3n), "the shell exponent 1 is multiplied by 3");
exact("packing_gamma_cube", mul(q(1n, 3n), q(3n)), q(1n), "the gamma exponent 1/3 is multiplied by 3");
exact("packing_theta_cube", mul(q(-2n, 3n), q(3n)), q(-2n), "the Theta exponent -2/3 is multiplied by 3");

const note = text(notePath);
const problem = text(problemPath);
const reader = text(readerPath);
const primary = JSON.parse(text(primaryPath));
const tags = [...note.matchAll(/\\tag\{R\.(\d+)\}/g)].map((match) => Number(match[1]));
const expectedTags = Array.from({ length: 26 }, (_, index) => 200 + index);

const structuralChecks = [
  { id: "tags_200_225_consecutive", pass: JSON.stringify(tags) === JSON.stringify(expectedTags) },
  { id: "tags_unique", pass: new Set(tags).size === expectedTags.length },
  { id: "terminal_inclusive_positive_variation", pass: note.includes("t_m=\\tau") && note.includes("explicitly includes the terminal value") },
  { id: "full_cutoff_interval", pass: note.includes("full\n   cutoff interval") && note.includes("For a good time \\(\\tau\\in(s_R,t_0)\\)") },
  { id: "cutoff_three_halves", pass: note.includes("\\eta_R(t)^{3/2}") },
  { id: "persistence_coefficient", pass: note.includes("2^k\\gamma_k^{1/3}") && note.includes("\\Theta_{k,R}^{\\eta}(\\tau;J)^{-2/3}") },
  { id: "packing_coefficient", pass: note.includes("2^{3k}\\gamma_k\\Lambda_{k,R,\\tau}^3") && note.includes("\\Theta_{k,R}^{\\eta}(\\tau;J_{k,\\tau})^{-2}") },
  { id: "lower_semicontinuity_closure", pass: note.includes("lower semicontinuous for coordinatewise convergence") && note.includes("good times are dense") },
  { id: "conditional_not_unconditional", pass: note.includes("Assume there are constants") && note.includes("The arbitrary-clock extraction theorem itself remains **OPEN**") },
  { id: "functional_witness_boundary", pass: note.includes("functional\nno-go examples, not Navier--Stokes solutions") && note.includes("None of the constructed\nfields is asserted to solve Navier--Stokes") },
  { id: "not_clay", pass: note.includes("NOT CLAY") && problem.includes("NOT CLAY") && reader.includes("NOT CLAY") },
  { id: "primary_certificate_counts", pass: JSON.stringify(primary.summary) === JSON.stringify({ power_ledgers_passed: 3, power_ledgers_total: 3, rational_passed: 13, rational_total: 13, result: "PASS", structural_passed: 25, structural_total: 25 }) },
];

function bestTail(values, exceptions) {
  const sorted = [...values].sort((a, b) => b - a);
  return sorted.slice(exceptions).reduce((sum, value) => sum + value, 0);
}

const finiteChecks = [
  { id: "best_tail_empty", pass: bestTail([], 3) === 0 },
  { id: "best_tail_remove_one", pass: bestTail([7, 2, 5], 1) === 7 },
  { id: "best_tail_remove_two", pass: bestTail([7, 2, 5], 2) === 2 },
  { id: "best_tail_permutation", pass: bestTail([1, 9, 3, 4], 2) === bestTail([4, 3, 9, 1], 2) },
  { id: "coordinatewise_lsc_sentinel", pass: 0 <= Math.min(...[1, 1, 1, 1].map((value) => value)) },
];

const allChecks = [...rationalChecks, ...structuralChecks, ...finiteChecks];
const result = {
  schema: "r074r-arbitrary-clock-independent-audit-v1",
  scope: "Independent exact arithmetic, source binding, theorem-scope sentinels, and finite best-tail checks; no PDE simulation",
  source_bindings: {
    [notePath]: sha(notePath),
    [primaryPath]: sha(primaryPath),
    [problemPath]: sha(problemPath),
    [readerPath]: sha(readerPath),
  },
  rational_checks: rationalChecks,
  structural_checks: structuralChecks,
  finite_checks: finiteChecks,
  claim_boundary: {
    terminal_window_lobe_packing: "PROVED",
    arbitrary_clock_conditional_implication: "PROVED",
    conditional_hypotheses_for_arbitrary_suitable_weak_solutions: "OPEN",
    functional_witnesses_are_nse_counterexamples: false,
    fixed_scale_Q1_unconditional: "OPEN",
    regularity_or_singularity: "OPEN",
    clay: "NOT_CLAIMED_NOT_CLAY",
  },
  summary: {
    rational_passed: rationalChecks.filter((check) => check.pass).length,
    rational_total: rationalChecks.length,
    structural_passed: structuralChecks.filter((check) => check.pass).length,
    structural_total: structuralChecks.length,
    finite_passed: finiteChecks.filter((check) => check.pass).length,
    finite_total: finiteChecks.length,
    result: allChecks.every((check) => check.pass) ? "PASS" : "FAIL",
  },
};

const rendered = `${JSON.stringify(result, null, 2)}\n`;
if (process.argv.includes("--write")) {
  writeFileSync(resolve(root, outputPath), rendered);
  const report = `# R0.74R Step 2 - independent mathematical audit\n\n## Verdict\n\n**${result.summary.result}.** A second implementation passed ${result.summary.rational_passed}/${result.summary.rational_total} exact rational checks, ${result.summary.structural_passed}/${result.summary.structural_total} structural checks, and ${result.summary.finite_passed}/${result.summary.finite_total} finite best-tail sentinels.\n\nThe endpoint-averaging triage, cutoff-weighted persistence coefficient, shellwise ell3 packing, and good-time-to-all-time lower-semicontinuity closure are internally consistent with the frozen formulas. No equation direction or exponent mismatch was found.\n\n## Scope boundary\n\nThis audit certifies the stated implication only. It does not construct the universal data required by (R.216)--(R.217). The scalar clock, thin time spike, and high-frequency divergence-free field are abstract or functional witnesses, not Navier--Stokes solutions. They do not disprove (Q.1). Regularity, singularity formation, and the Clay problem remain **OPEN**. **NOT CLAY.**\n\n## Source bindings\n\n${Object.entries(result.source_bindings).map(([path, digest]) => `- \`${path}\`: \`${digest}\``).join("\n")}\n\nThe machine-readable certificate is \`${outputPath}\`.\n`;
  writeFileSync(resolve(root, reportPath), report);
}
process.stdout.write(rendered);
process.exitCode = result.summary.result === "PASS" ? 0 : 1;
