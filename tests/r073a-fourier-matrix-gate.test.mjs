import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { existsSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificate = "research/certificates/r073a";
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || (existsSync(bundledPython) ? bundledPython : "python3");
const run = promisify(execFile);

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

test("R0.73A source freezes the four requested finite-matrix audits", async () => {
  const [producer, validator, readme] = await Promise.all([
    text(`${certificate}/generate_certificate.py`),
    text(`${certificate}/validate_certificate.py`),
    text(`${certificate}/README.md`),
  ]);
  for (const token of [
    "original_q_symbolic", "conjugate_by_hidden_mean", "derived_hr_symbolic",
    "meanCancellation", "matrixSimilarity", "hiddenMeanDerivative",
    "normalizedCellMeasure", "numerical_crosscheck", "--source-stage",
    "--formal", "--source-commit", "working source differs byte-for-byte",
    "supporting_algebra_records", "orthogonalProjectionSpeed",
    "adjointPressureG", "twoModeLeakage", "positiveGapDualConstant",
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "never loads the producer module", "raw_q_matrix",
    "transformed_matrix_direct", "similarity_audit", "exact_formula_audit",
    "integrate_raw_q", "independent_propagator_audit",
    "--require-source-stage", "--require-formal", "validate_external_csv",
    "supporting_algebra_audit", "supporting exact algebra disagrees",
  ]) assert.ok(validator.includes(token), token);
  assert.ok(!/\bfrom\s+generate_certificate\s+import\b/.test(validator));
  assert.ok(!/\bimport\s+generate_certificate\b/.test(validator));
  assert.match(readme, /finite Fourier matrices/i);
  assert.match(readme, /does \*\*not\*\* prove the\s+infinite-dimensional/i);
  assert.match(readme, /no self-referential certificate commit/i);
});

test("R0.73A producer and independent validator pass without writing", async () => {
  const [producer, validator] = await Promise.all([
    run(python, [`${certificate}/generate_certificate.py`, "--self-test"], {
      cwd: root,
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
      maxBuffer: 8 * 1024 * 1024,
    }),
    run(python, [`${certificate}/validate_certificate.py`, "--self-test"], {
      cwd: root,
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
      maxBuffer: 8 * 1024 * 1024,
    }),
  ]);
  assert.match(producer.stdout, /passed \(no outputs written\)/);
  assert.match(validator.stdout, /independent validator self-test passed/);
});

test("R0.73A sources use no random generator", async () => {
  const [producer, independent, validator, environment] = await Promise.all([
    text(`${certificate}/generate_certificate.py`),
    text(`${certificate}/independent_recompute.py`),
    text(`${certificate}/validate_certificate.py`),
    text(`${certificate}/environment.txt`),
  ]);
  for (const source of [producer, independent, validator]) {
    assert.doesNotMatch(source, /\b(?:random|rand|randn|default_rng)\s*\(/);
  }
  assert.match(environment, /random_numbers_used=false/);
});
