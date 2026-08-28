import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { existsSync } from "node:fs";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || (existsSync(bundledPython) ? bundledPython : "python3");
const run = promisify(execFile);
const certificate = "research/certificates/r072y";
const generated = [
  "certificate.json",
  "independent.json",
  "crosscheck.json",
  "manifest.json",
  "SHA256SUMS",
];
const completeBoundSources = [
  "research/r072y_report-source.md",
  "research/r072y_gap_matrix.md",
  "research/r072y_literature_audit.md",
  "research/r072y_full_row_independent_audit.md",
  "research/r072y_forced_transfer_independent_audit.md",
  "research/r072y_independent_audit.md",
  "research/certificates/r072y/generate_certificate.py",
  "research/certificates/r072y/independent_recompute.py",
  "research/certificates/r072y/validate_certificate.py",
  "research/certificates/r072y/README.md",
  "research/certificates/r072y/command.txt",
  "research/certificates/r072y/environment.txt",
  "research/release-manifest.json",
  "scripts/generate_r072y_release.py",
  "scripts/add-r072y-translations.mjs",
  "figures/r072y/fig-r072y-full-row-forced-transfer/README.md",
  "figures/r072y/fig-r072y-full-row-forced-transfer/caption.md",
  "figures/r072y/fig-r072y-full-row-forced-transfer/command.txt",
  "figures/r072y/fig-r072y-full-row-forced-transfer/config.json",
  "figures/r072y/fig-r072y-full-row-forced-transfer/contract.json",
  "figures/r072y/fig-r072y-full-row-forced-transfer/environment.txt",
  "figures/r072y/fig-r072y-full-row-forced-transfer/figure-contract.md",
  "figures/r072y/fig-r072y-full-row-forced-transfer/plot.py",
  "figures/r072y/fig-r072y-full-row-forced-transfer/qa-protocol.md",
  "figures/r072y/fig-r072y-full-row-forced-transfer/requirements.txt",
  "figures/r072y/fig-r072y-full-row-forced-transfer/validate.py",
  "tests/r072y-deterministic-certificate-source.test.mjs",
  "tests/r072y-full-row-forced-gate.test.mjs",
  "tests/r072y-full-row-forced-transfer-figure-source.test.mjs",
  "tests/r072y-release.test.mjs",
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

async function snapshot() {
  return Object.fromEntries(await Promise.all(generated.map(async (name) => [
    name,
    await sha(certificate + "/" + name),
  ])));
}

async function absent(relative) {
  await assert.rejects(
    access(resolve(root, relative)),
    (error) => error?.code === "ENOENT",
    relative,
  );
}

async function verifyFlatHashLedger() {
  const directory = resolve(root, certificate);
  const rows = (await text(certificate + "/SHA256SUMS")).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, "malformed SHA256SUMS row: " + row);
    assert.equal(await sha(certificate + "/" + match[2]), match[1], match[2]);
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries
      .filter((entry) => entry.isFile() && entry.name !== "SHA256SUMS")
      .map((entry) => entry.name).sort(),
  );
}

test("R0.72Y finite certificate freezes every exact algebra ledger", async () => {
  const [producer, independent, validator, readme] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/independent_recompute.py"),
    text(certificate + "/validate_certificate.py"),
    text(certificate + "/README.md"),
  ]);
  for (const token of [
    '"identity": "W_d=W_xx"',
    '"factorTwo"',
    '"coefficientSum"',
    '"identityResidual"',
    '"divergenceOfProjectionSum"',
    '"orrSommerfeldCoefficientTableInUnitsOfIc"',
    '"squirePressureSum"',
    '"squireLiftCoefficient"',
    '"matrixIdentityResidual"',
    '"u3ResidualAfterCommonFactor"',
    '"meanSquareWx"',
    '"finiteGeometricIdentityChecked"',
    '"zeroDampingLimit"',
    '"standardWeight"',
    '"semiclassicalWeight"',
    '"energyExponent"',
    '"normExponent"',
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "does not import the producer",
    "def pressure_factor_record",
    "def os_squire_record",
    "def lift_up_record",
    "def fourier_weight_record",
  ]) assert.ok(independent.includes(token), token);
  assert.ok(!/\bimport\s+generate_certificate\b/.test(independent));
  assert.ok(!/\bfrom\s+generate_certificate\s+import\b/.test(independent));
  for (const token of [
    "def validate_exact_ledger",
    "def validate_claim_boundary",
    "def validate_claim_ledger",
    "def validate_sha256_ledger",
  ]) assert.ok(validator.includes(token), token);
  assert.match(readme, /finite-algebra/i);
  assert.match(readme, /does\s+\*\*not\*\*\s+machine-check/i);
});

test("R0.72Y certificate boundary is exhaustive and machine-honest", async () => {
  const [producer, validator] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/validate_certificate.py"),
  ]);
  for (const token of [
    '"finiteExactAlgebraCertified": True',
    '"functionalAnalysisMachineChecked": False',
    '"sharpnessProofsMachineChecked": False',
    '"infiniteSeriesConvergenceMachineChecked": False',
    '"galerkinLimitMachineChecked": False',
    '"endpointTraceMachineChecked": False',
    '"nonautonomousEvolutionExistenceMachineChecked": False',
    '"completeLinearizedShearSubsystemProved": False',
    '"nonlinearNavierStokesClosureProved": False',
    '"clayMillenniumProblemSolved": False',
    '"standardHMinusOneTransferAlpha2"',
    '"HMinusOneEndpointAlphaGain"',
    '"strongFullRowA2Estimate"',
    '"scaleSharpOSPressureAbsorption"',
    '"orientationUniformSquireTransfer"',
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "validate_claim_boundary",
    "claim boundary is incomplete or has drifted",
    "validate_claim_ledger",
    "negative-result-keys",
    "open-keys",
  ]) assert.ok(validator.includes(token), token);
});

test("R0.72Y producer and independent routes agree in memory", async () => {
  const comparison = [
    "import importlib.util",
    "from pathlib import Path",
    'root = Path("research/certificates/r072y")',
    "def load(name):",
    '    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")',
    "    module = importlib.util.module_from_spec(spec)",
    "    spec.loader.exec_module(module)",
    "    return module",
    'producer_module = load("generate_certificate")',
    'validator_module = load("validate_certificate")',
    "producer = producer_module.payload()",
    'independent = load("independent_recompute").compute()',
    "sections = (",
    '    "heatShearIdentity", "pressurePoissonFactorTwo", "blochLerayIdentity",',
    '    "osSquireSignLedger", "velocityReconstruction", "zeroCouplingLiftUp",',
    '    "causalKernel", "fourierWeights", "dampingGap", "claimLedger", "claimBoundary",',
    ")",
    'if producer["status"] != "passed" or not all(producer["exactChecks"].values()):',
    '    raise SystemExit("producer checks failed")',
    "for section in sections:",
    "    if producer[section] != independent[section]:",
    '        raise SystemExit(f"independent section mismatch: {section}")',
    'if producer["producerMethod"] == independent["method"]:',
    '    raise SystemExit("producer and independent method labels unexpectedly coincide")',
    "if producer_module.SOURCE_FILES != validator_module.EXPECTED_SOURCE_FILES:",
    '    raise SystemExit("producer/validator source inventory mismatch")',
    'print("R0.72Y source-stage independent comparison passed")',
  ].join("\n");
  const result = await run(python, ["-c", comparison], {
    cwd: root,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.match(result.stdout, /source-stage independent comparison passed/);
});

test("R0.72Y formal lifecycle binds the complete frozen source set and two-stage CLI", async () => {
  const [producer, validator] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/validate_certificate.py"),
  ]);
  for (const relative of completeBoundSources) {
    assert.ok(producer.includes('"' + relative + '"'), relative);
    assert.ok(validator.includes('"' + relative + '"'), relative);
  }
  for (const token of [
    "--formal",
    "--formal-source-commit",
    "formal source commit must equal clean HEAD",
    "workingTreeBlobMatches",
    "gitBlob",
    "temporaryUnsealedSourceAllowed",
    "formalSourceReady",
    "refusing to overwrite a formal R0.72Y certificate",
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "--require-formal",
    "validate_formal_bindings",
    "formal source binding drift",
    "SHA256SUMS must cover every flat regular file exactly once",
  ]) assert.ok(validator.includes(token), token);
  assert.ok(!producer.includes("--source-commit"));
});

test("R0.72Y Python sources have no duplicate literal dictionary keys or control bytes", async () => {
  for (const relative of [
    certificate + "/generate_certificate.py",
    certificate + "/independent_recompute.py",
    certificate + "/validate_certificate.py",
  ]) {
    const bytes = await readFile(resolve(root, relative));
    for (const byte of bytes) {
      assert.ok(byte === 9 || byte === 10 || byte === 13 || byte >= 32, relative + ": control byte " + byte);
    }
  }
  const duplicateKeyAudit = [
    "import ast",
    "from pathlib import Path",
    "paths = [",
    '    Path("research/certificates/r072y/generate_certificate.py"),',
    '    Path("research/certificates/r072y/independent_recompute.py"),',
    '    Path("research/certificates/r072y/validate_certificate.py"),',
    "]",
    "for path in paths:",
    '    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))',
    "    for node in ast.walk(tree):",
    "        if not isinstance(node, ast.Dict):",
    "            continue",
    "        keys = [key.value for key in node.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)]",
    "        if len(keys) != len(set(keys)):",
    '            raise SystemExit(f"duplicate literal dictionary key in {path}:{node.lineno}")',
    'print("duplicate-key audit passed")',
  ].join("\n");
  const result = await run(python, ["-c", duplicateKeyAudit], { cwd: root });
  assert.match(result.stdout, /duplicate-key audit passed/);
});

test("R0.72Y self-tests never rewrite draft or formal outputs", async () => {
  const manifest = await maybeJson(certificate + "/manifest.json");
  if (!manifest) {
    for (const name of generated) await absent(certificate + "/" + name);
  }
  const before = manifest ? await snapshot() : null;
  const [producerRun, independentRun] = await Promise.all([
    run(python, [certificate + "/generate_certificate.py", "--self-test"], {
      cwd: root,
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    }),
    run(python, [certificate + "/independent_recompute.py", "--self-test"], {
      cwd: root,
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    }),
  ]);
  assert.match(producerRun.stdout, /passed \(no outputs written\)/);
  assert.match(independentRun.stdout, /passed \(no outputs written\)/);
  if (manifest) assert.deepEqual(await snapshot(), before);
});

test("R0.72Y strict validator fails closed before formal and is exhaustive after sealing", async () => {
  const manifest = await maybeJson(certificate + "/manifest.json");
  assert.ok(manifest, "draft or formal certificate must exist");
  await verifyFlatHashLedger();
  if (manifest.status !== "formal") {
    await assert.rejects(run(python, [
      certificate + "/validate_certificate.py", "--require-formal",
    ], { cwd: root }));
    return;
  }
  const crosscheck = await maybeJson(certificate + "/crosscheck.json");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.formalSourceReady, true);
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
  assert.equal(crosscheck.sourceCommit, manifest.sourceCommit);
  assert.deepEqual(crosscheck.sourceBindings, manifest.sourceBindings);
  assert.deepEqual(
    manifest.sourceBindings.map((row) => row.path),
    completeBoundSources,
  );
  await run(python, [
    certificate + "/validate_certificate.py", "--require-formal",
  ], { cwd: root });
});
