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
const certificate = "research/certificates/r073b";
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || (existsSync(bundledPython) ? bundledPython : "python3");
const run = promisify(execFile);

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function sha(relative) {
  return createHash("sha256").update(await readFile(resolve(root, relative))).digest("hex");
}

async function snapshot() {
  const entries = await readdir(resolve(root, certificate), { withFileTypes: true });
  const names = entries.filter((entry) => entry.isFile()).map((entry) => entry.name).sort();
  return Object.fromEntries(await Promise.all(names.map(async (name) => [
    name, await sha(certificate + "/" + name),
  ])));
}

async function verifyFlatHashLedger() {
  const rows = (await text(certificate + "/SHA256SUMS")).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, row);
    assert.equal(await sha(certificate + "/" + match[2]), match[1], match[2]);
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
}

test("R0.73B producer and validator independently pin exact algebra and finite-only boundaries", async () => {
  const [producer, independent, validator, readme] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/independent_recompute.py"),
    text(certificate + "/validate_certificate.py"),
    text(certificate + "/README.md"),
  ]);
  for (const token of [
    "exact_bloch_records", "raw_bloch_matrix", "conjugate_bloch",
    "direct_bloch_hr_matrix", "exact_energy_records", "exact_scaling_records",
    "experiment_crosscheck", "finitePropagatorGridChecked",
    "analyticInfiniteDimensionalEnergyProofReplacedByCertificate",
    "completeOSSquireA2DirectSumProved", "nonlinearNavierStokesProved",
    "clayMillenniumProblemSolved",
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "No producer module is imported", "targeted_asymptotics.csv",
    "selectedObservedExponents", "fixedLambdaTriangularGains",
    "producerImported", "infiniteDimensionalLimitProved",
  ]) assert.ok(independent.includes(token), token);
  assert.doesNotMatch(independent, /\b(?:from|import)\s+generate_certificate\b/);
  for (const token of [
    "never imports the producer", "redo_rational_algebra",
    "validate_source_bindings", "targeted_exponent", "triangular_gain",
    "source binding validation failed", "finiteExperimentValidation",
    "infiniteDimensionalTheoremProvedByThisValidator",
  ]) assert.ok(validator.includes(token), token);
  assert.match(readme, /finite.*(?:Fourier|matrices|sampled)/is);
  assert.match(readme, /does\s+not prove.*infinite-dimensional/is);
  assert.match(producer + validator, /fail(?:s)?[- ]closed/i);
});

test("R0.73B formal lifecycle binds every release source needed by the publication generator", async () => {
  const [producer, validator] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/validate_certificate.py"),
  ]);
  const requiredSources = [
    "research/r073b_problem_freeze.md", "research/r073b_kinetic_form_proof.md",
    "research/r073b_report-source.md", "research/r073b_literature_audit.md",
    "research/r073b_gap_matrix.md", "research/r073b_independent_analytic_audit.md",
    "experiments/r073b/weighted_kinetic_screen.py",
    "experiments/r073b/validate_weighted_kinetic_screen.py",
    "experiments/r073b/manifest.json", "experiments/r073b/validation.json",
    "research/certificates/r073b/generate_certificate.py",
    "research/certificates/r073b/independent_recompute.py",
    "research/certificates/r073b/validate_certificate.py",
    "scripts/generate_r073b_release.py", "scripts/add-r073b-translations.mjs",
    "scripts/i18n-snapshots/r073b-missing.json",
    "tests/r073b-bloch-kinetic-gate.test.mjs", "tests/r073b-release.test.mjs",
    "tests/r073b-deterministic-certificate-source.test.mjs",
    "tests/r073b-bloch-kinetic-transient-figure-source.test.mjs",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/contract.json",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/config.json",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/caption.md",
    "figures/r073b/fig-r073b-bloch-kinetic-transient/README.md",
  ];
  for (const relative of requiredSources) {
    assert.ok(producer.includes('"' + relative + '"'), relative + ": producer");
    assert.ok(validator.includes('"' + relative + '"'), relative + ": validator");
  }
  for (const token of [
    "--self-test", "--source-stage", "--formal", "--source-commit",
    "validate_commit", "gitBlob", "workingTreeBytesMatch",
    "stale or incomplete formal source commit fails closed",
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "--self-test", "--require-source-stage", "--require-formal",
    "formal source commit malformed", "formal source commit does not resolve",
    "gitBlob",
  ]) assert.ok(validator.includes(token), token);
});

test("R0.73B Python certificate sources parse with no duplicate literal keys or control bytes", async () => {
  const paths = [
    certificate + "/generate_certificate.py",
    certificate + "/independent_recompute.py",
    certificate + "/validate_certificate.py",
  ];
  for (const relative of paths) {
    const bytes = await readFile(resolve(root, relative));
    for (const byte of bytes) {
      assert.ok(byte === 9 || byte === 10 || byte === 13 || byte >= 32,
        relative + ": control byte " + String(byte));
    }
  }
  const source = [
    "import ast", "from pathlib import Path", "paths=[",
    ...paths.map((relative) => " Path(" + JSON.stringify(relative) + "),"), "]",
    "for path in paths:",
    ' tree=ast.parse(path.read_text(encoding="utf-8"),filename=str(path))',
    " for node in ast.walk(tree):",
    "  if not isinstance(node,ast.Dict): continue",
    "  keys=[key.value for key in node.keys if isinstance(key,ast.Constant) and isinstance(key.value,str)]",
    "  if len(keys)!=len(set(keys)): raise SystemExit('duplicate literal dictionary key')",
    'print("duplicate-key audit passed")',
  ].join("\n");
  const result = await run(python, ["-c", source], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.match(result.stdout, /duplicate-key audit passed/);
});

test("R0.73B producer and validator self-tests are deterministic and write nothing", async () => {
  const before = await snapshot();
  const [producerResult, validatorResult] = await Promise.all([
    run(python, [certificate + "/generate_certificate.py", "--self-test"], {
      cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
      maxBuffer: 8 * 1024 * 1024,
    }),
    run(python, [certificate + "/validate_certificate.py", "--self-test"], {
      cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
      maxBuffer: 8 * 1024 * 1024,
    }),
  ]);
  assert.match(producerResult.stdout, /"status": "passed"/);
  assert.match(validatorResult.stdout, /"status": "passed"/);
  assert.deepEqual(await snapshot(), before);
});

test("R0.73B current certificate validates exactly at its declared stage", async () => {
  const manifest = await json(certificate + "/manifest.json");
  assert.ok(["source-stage", "formal"].includes(manifest.status), manifest.status);
  const flag = manifest.status === "formal" ? "--require-formal" : "--require-source-stage";
  const result = await run(python, [certificate + "/validate_certificate.py", flag], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    maxBuffer: 8 * 1024 * 1024,
  });
  assert.match(result.stdout, new RegExp('"stage": "' + manifest.status + '"'));
  assert.match(result.stdout, /"status": "passed"/);
  await verifyFlatHashLedger();
  const validation = await json(certificate + "/validation.json");
  assert.equal(validation.status, "passed");
  assert.equal(validation.claimBoundary.infiniteDimensionalTheoremProvedByThisValidator, false);
  assert.equal(validation.claimBoundary.nonlinearNavierStokesProved, false);
});

test("R0.73B formal mode fails closed on a stale or incomplete source commit", async () => {
  const head = (await run("git", ["rev-parse", "HEAD"], { cwd: root })).stdout.trim();
  const before = await snapshot();
  await assert.rejects(run(python, [
    certificate + "/generate_certificate.py", "--formal", "--source-commit", head,
  ], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    maxBuffer: 8 * 1024 * 1024,
  }));
  assert.deepEqual(await snapshot(), before);
});
