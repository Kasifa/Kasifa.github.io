import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificate = "research/certificates/r073a";
const csvPath = "experiments/r073a/xmu_propagator_certificate.csv";
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || bundledPython;
const run = promisify(execFile);
const protectedOutputs = [
  `${certificate}/certificate.json`, `${certificate}/crosscheck.json`,
  `${certificate}/manifest.json`, `${certificate}/SHA256SUMS`, csvPath,
];

const completeBoundSources = [
  "research/r073a_problem_freeze.md",
  "research/r073a_transient_proof.md",
  "research/r073a_report-source.md",
  "research/r073a_gap_matrix.md",
  "research/r073a_literature_audit.md",
  "research/r073a_independent_analytic_audit.md",
  "research/r073a_projection_derivation_agent.md",
  "research/r073a_projection_independent_audit.md",
  "research/r073a_spectral_audit_agent.md",
  "experiments/r073a/frozen_os_spectral_audit.py",
  "experiments/r073a/validate_frozen_os_spectral_audit.py",
  "experiments/r073a/validation.json",
  "experiments/r073a/manifest.json",
  "experiments/r073a/requirements.txt",
  "experiments/r073a/command.txt",
  "experiments/r073a/environment.json",
  "experiments/r073a/progress.ndjson",
  "research/certificates/r073a/generate_certificate.py",
  "research/certificates/r073a/independent_recompute.py",
  "research/certificates/r073a/validate_certificate.py",
  "research/certificates/r073a/README.md",
  "research/certificates/r073a/command.txt",
  "research/certificates/r073a/environment.txt",
  "research/certificates/r073a/progress.ndjson",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/README.md",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/caption.md",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/command.txt",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/config.json",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/contract.json",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/environment.txt",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/figure-contract.md",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/manifest-draft.json",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/plot.py",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/qa-protocol.md",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/requirements.txt",
  "figures/r073a/fig-r073a-hidden-mean-transient-spectral/validate.py",
  "scripts/generate_r073a_release.py",
  "scripts/add-r073a-translations.mjs",
  "scripts/i18n-snapshots/r073a-missing.json",
  "research/release-manifest.json",
  "tests/r073a-fourier-matrix-gate.test.mjs",
  "tests/r073a-transient-certificate.test.mjs",
  "tests/r073a-hidden-mean-gate.test.mjs",
  "tests/r073a-release.test.mjs",
  "tests/r073a-deterministic-certificate-source.test.mjs",
  "tests/r073a-hidden-mean-transient-spectral-figure-source.test.mjs",
];

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function maybeJson(relative) {
  try {
    return JSON.parse(await text(relative));
  } catch (error) {
    if (error?.code === "ENOENT") return null;
    throw error;
  }
}

async function sha(relative) {
  return createHash("sha256").update(await readFile(resolve(root, relative))).digest("hex");
}

async function maybeSha(relative) {
  try {
    return await sha(relative);
  } catch (error) {
    if (error?.code === "ENOENT") return null;
    throw error;
  }
}

async function snapshot() {
  return Object.fromEntries(await Promise.all(protectedOutputs.map(async (relative) => [
    relative, await maybeSha(relative),
  ])));
}

async function verifyFlatHashLedger() {
  const directory = resolve(root, certificate);
  const rows = (await text(`${certificate}/SHA256SUMS`)).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
    assert.equal(await sha(`${certificate}/${match[2]}`), match[1], match[2]);
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries.filter((entry) => entry.name !== "SHA256SUMS").map((entry) => entry.name).sort(),
  );
}

test("R0.73A source exposes both finite algorithms and every strict scope ledger", async () => {
  const [producer, independent, validator, readme] = await Promise.all([
    text(`${certificate}/generate_certificate.py`),
    text(`${certificate}/independent_recompute.py`),
    text(`${certificate}/validate_certificate.py`),
    text(`${certificate}/README.md`),
  ]);
  for (const token of [
    "original_q_symbolic", "conjugate_by_hidden_mean", "derived_hr_symbolic",
    "matrixSimilarity", "meanCancellation", "hiddenMeanDerivative",
    "supporting_algebra_records", "orthogonalProjectionSpeed", "adjointPressureG",
    "twoModeLeakage", "positiveGapDualConstant", "numerical_crosscheck",
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "does not import or execute the main certificate producer", "q_generator",
    "raw_propagator", "xmu_gain", "analytic_bound", "FLOAT_TOLERANCE = 2e-8",
  ]) assert.ok(independent.includes(token), token);
  assert.ok(!/\bfrom\s+generate_certificate\s+import\b/.test(independent));
  assert.ok(!/\bimport\s+generate_certificate\b/.test(independent));
  for (const token of [
    "never loads the producer module", "raw_q_matrix", "transformed_matrix_direct",
    "independent_propagator_audit", "validate_source_bindings", "validate_external_csv",
    "validate_sha256_ledger", "source binding inventory mismatch",
  ]) assert.ok(validator.includes(token), token);
  assert.match(readme, /finite Fourier matrices/i);
  assert.match(readme, /does \*\*not\*\* prove the\s+infinite-dimensional/i);
  assert.match(readme, /fail(?:s)? closed/i);
});

test("R0.73A formal lifecycle binds the exact complete 46-file source package", async () => {
  const [producer, validator] = await Promise.all([
    text(`${certificate}/generate_certificate.py`),
    text(`${certificate}/validate_certificate.py`),
  ]);
  assert.equal(completeBoundSources.length, 46);
  for (const relative of completeBoundSources) {
    await access(resolve(root, relative));
    assert.ok(producer.includes(`"${relative}"`), `${relative}: producer`);
    assert.ok(validator.includes(`"${relative}"`), `${relative}: validator`);
  }
  for (const token of [
    "--self-test", "--source-stage", "--formal", "--source-commit",
    "formal source commit must equal clean HEAD", "gitBlob",
    "workingTreeBytesMatch", "temporaryUnsealedSourceAllowed", "formalSourceReady",
    "refusing to overwrite a formal R0.73A certificate",
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "--self-test", "--source-stage", "--formal", "--source-commit",
  ]) assert.ok((await text(`${certificate}/independent_recompute.py`)).includes(token), `independent ${token}`);
  for (const token of [
    "--require-source-stage", "--require-formal", "validate_source_bindings",
    "formal source binding drift", "formal sourceCommit",
  ]) assert.ok(validator.includes(token), token);
});

test("R0.73A Python sources have no duplicate literal keys or control bytes", async () => {
  const paths = [
    `${certificate}/generate_certificate.py`, `${certificate}/independent_recompute.py`,
    `${certificate}/validate_certificate.py`,
  ];
  for (const relative of paths) {
    const bytes = await readFile(resolve(root, relative));
    for (const byte of bytes) {
      assert.ok(byte === 9 || byte === 10 || byte === 13 || byte >= 32, `${relative}: control byte ${byte}`);
    }
  }
  const script = [
    "import ast", "from pathlib import Path", "paths=[",
    ...paths.map((relative) => ` Path(${JSON.stringify(relative)}),`), "]",
    "for path in paths:",
    ' tree=ast.parse(path.read_text(encoding="utf-8"),filename=str(path))',
    " for node in ast.walk(tree):", "  if not isinstance(node,ast.Dict): continue",
    "  keys=[key.value for key in node.keys if isinstance(key,ast.Constant) and isinstance(key.value,str)]",
    "  if len(keys)!=len(set(keys)): raise SystemExit(f'duplicate literal dictionary key in {path}:{node.lineno}')",
    'print("duplicate-key audit passed")',
  ].join("\n");
  const result = await run(python, ["-c", script], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.match(result.stdout, /duplicate-key audit passed/);
});

test("R0.73A all three self-tests are deterministic and never write outputs", async () => {
  const before = await snapshot();
  const [producerRun, independentRun, validatorRun] = await Promise.all([
    run(python, [`${certificate}/generate_certificate.py`, "--self-test"], {
      cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" }, maxBuffer: 8 * 1024 * 1024,
    }),
    run(python, [`${certificate}/independent_recompute.py`, "--self-test"], {
      cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" }, maxBuffer: 8 * 1024 * 1024,
    }),
    run(python, [`${certificate}/validate_certificate.py`, "--self-test"], {
      cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" }, maxBuffer: 8 * 1024 * 1024,
    }),
  ]);
  assert.match(producerRun.stdout, /passed \(no outputs written\)/);
  assert.match(independentRun.stdout, /passed \(120 cases; no output written\)/);
  assert.match(validatorRun.stdout, /passed .*no outputs written\)/);
  assert.deepEqual(await snapshot(), before);
});

test("R0.73A current certificate validates at exactly its declared stage", async () => {
  const manifest = await maybeJson(`${certificate}/manifest.json`);
  assert.ok(manifest, "certificate manifest missing");
  assert.ok(["source-stage", "formal"].includes(manifest.status), manifest.status);
  const flag = manifest.status === "formal" ? "--require-formal" : "--require-source-stage";
  const result = await run(python, [`${certificate}/validate_certificate.py`, flag], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" }, maxBuffer: 8 * 1024 * 1024,
  });
  assert.match(result.stdout, new RegExp(`strict ${manifest.status} certificate validation passed`));
  const validatorSource = await text(`${certificate}/validate_certificate.py`);
  assert.match(validatorSource, /merge-base", "--is-ancestor"/);
  assert.match(validatorSource, /current HEAD or its ancestor/);
  await verifyFlatHashLedger();
  assert.equal((await text(csvPath)).split("\n", 1)[0], "certificateId,s,d,mu,c,gain,bound,sourceCommit,certificateCommit");
});

test("R0.73A formal mode fails closed on stale or untracked source bytes", async () => {
  const head = (await run("git", ["rev-parse", "HEAD"], { cwd: root })).stdout.trim();
  const before = await snapshot();
  await assert.rejects(run(python, [
    `${certificate}/generate_certificate.py`, "--formal", "--source-commit", head,
  ], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" }, maxBuffer: 8 * 1024 * 1024,
  }));
  assert.deepEqual(await snapshot(), before);
});
