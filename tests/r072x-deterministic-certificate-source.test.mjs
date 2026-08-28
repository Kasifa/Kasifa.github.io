import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const python = process.env.CODEX_PYTHON || "python3";
const run = promisify(execFile);
const certificate = "research/certificates/r072x";
const sourceFiles = [
  certificate + "/generate_certificate.py",
  certificate + "/independent_recompute.py",
  certificate + "/validate_certificate.py",
  certificate + "/README.md",
  certificate + "/command.txt",
  certificate + "/environment.txt",
  "tests/r072x-deterministic-certificate-source.test.mjs",
];
const generated = [
  "certificate.json",
  "independent.json",
  "crosscheck.json",
  "manifest.json",
  "SHA256SUMS",
];


async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}


async function absent(relative) {
  await assert.rejects(
    access(resolve(root, relative)),
    (error) => error?.code === "ENOENT",
    relative,
  );
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


async function certificateIsFormal() {
  return (await maybeJson(certificate + "/manifest.json"))?.status === "formal";
}


async function generatedSnapshot() {
  return Object.fromEntries(await Promise.all(generated.map(async (name) => [
    name,
    await sha(certificate + "/" + name),
  ])));
}


async function assertNoCertificateOutputs() {
  for (const name of generated) await absent(certificate + "/" + name);
}


async function verifyFlatHashLedger(relative) {
  const directory = resolve(root, relative);
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, "malformed SHA256SUMS row: " + row);
    const [, expected, name] = match;
    assert.equal(await sha(relative + "/" + name), expected, name);
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries.filter((entry) => entry.isFile() && entry.name !== "SHA256SUMS")
      .map((entry) => entry.name).sort(),
  );
}


test("R0.72X source freezes common-zero, jet, interface, block, Bloch, damping, and zero-row ledgers", async () => {
  const [producer, independent, validator, readme] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/independent_recompute.py"),
    text(certificate + "/validate_certificate.py"),
    text(certificate + "/README.md"),
  ]);
  for (const token of [
    '"onlyCommonZero": "D=0 and theta=0 mod 2*pi"',
    '"jacobianAtOrigin": jacobian',
    '"jacobianDeterminant": q(',
    '"g": "3*theta+O(|D*theta|+|theta|^3)"',
    '"f": "3*D+(3/2)*theta^2+O(D^2+|D|*theta^2+theta^4)"',
    '"preA1DiagnosticRate": q(pre_rate)',
    '"postMonotoneDiagnosticRate": q(post_rate)',
    '"hCoefficientsThroughTwo": [q(value) for value in post_gradient_coefficients]',
    '"fullBlockCount": "N=floor(L/(2*T*alpha^2))"',
    '"prefactorOneAllGapExponential": False',
    '"physicalIntegratedEnergyBound": "2*T*alpha^2/(1-q^2)*E(d_1)"',
    '"boundaryPhaseExponent": "alpha*beta*L_alpha=2*pi*beta"',
    '"twistedBoundary": "w(X+L_alpha)=exp(2*pi*i*beta)*w(X)"',
    '"normDampingFactor": "exp(-mu*L)"',
    '"squaredEnergyDampingFactor": "exp(-2*mu*L)"',
    '"datum": "G(d,x)=(2*pi)^(-1/2)"',
    '"constantEquationChecked": constant_equation_checked',
    '"strictContraction": not constant_equation_checked',
  ]) assert.ok(producer.includes(token), token);

  for (const token of [
    "does not import the producer",
    "s*(2c^2+1)=0",
    "kappa-first power accounting",
    "divmod(numerator, denominator)",
    "finite_sum = sum",
    "direct derivative table",
  ]) assert.ok(independent.includes(token), token);
  assert.ok(!/\bimport\s+generate_certificate\b/.test(independent));
  assert.ok(!/\bfrom\s+generate_certificate\s+import\b/.test(independent));

  for (const token of [
    '"D*theta": "-15/1"',
    '"D^2*theta": "63/2"',
    '"postAwayGradientFloor": "2/1"',
    '"matchedRate") != "2/5"',
    '"energyExponentToNormExponent") != 2',
    "zero-coupling constant counterexample drifted",
  ]) assert.ok(validator.includes(token), token);
  assert.match(readme, /source stage/i);
  assert.match(readme, /does \*\*not\*\*\s+machine-check compactness/i);
});


test("R0.72X claim boundary is explicit and machine-honest", async () => {
  const [producer, validator] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/validate_certificate.py"),
  ]);
  for (const token of [
    '"finiteExactAlgebraCertified": True',
    '"analyticAllCenterExactFamilyGraphCoercivityProvedInBoundReport": True',
    '"analyticAllStartExactPathSemigroupProvedInBoundReport": True',
    '"analyticAllStartIntegratedA2ScaleProvedInBoundReport": True',
    '"analyticUniformTwistedPeriodicGraphProvedInBoundReport": True',
    '"analyticStrongRowDirectSumNoCountLossProvedInBoundReport": True',
    '"analyticFixedMarginA1EnhancedDissipationImportedInBoundReport": True',
    '"analyticPeriodicRepresentativeA1A2A1ConcatenationProvedInBoundReport": True',
    '"compactnessArgumentMachineChecked": False',
    '"boundedCenterGraphLimitMachineChecked": False',
    '"scalarEndpointTracePassageMachineChecked": False',
    '"twistedHMinusOneDirectSumMachineChecked": False',
    '"nonautonomousEvolutionExistenceMachineChecked": False',
    '"cobleHeTheoremMachineChecked": False',
    '"cobleHeApplicationHypothesesMachineChecked": False',
    '"shrinkingInterfaceFixedShapeA1Hypotheses": False',
    '"prefactorOneAllGapExponential": False',
    '"blochUniformFastA1ConcatenationProved": False',
    '"allPhysicalRowsUniformContraction": False',
    '"forcedHMinusOneTransferProved": False',
    '"completeLinearizedShearSubsystemProved": False',
    '"nonlinearNavierStokesClosureProved": False',
    '"clayMillenniumProblemSolved": False',
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "validate_claim_boundary",
    "claim boundary key set drifted",
    "manifest claim boundary drift",
    '"cobleHeTheoremMachineChecked"',
    '"allPhysicalRowsUniformContraction"',
    '"nonlinearNavierStokesClosureProved"',
    '"clayMillenniumProblemSolved"',
  ]) assert.ok(validator.includes(token), token);
  assert.ok(producer.includes('"claimBoundary": certificate["claimBoundary"]'));
});


test("R0.72X producer and independent source paths agree before sealing", async () => {
  const comparison = String.raw`
import importlib.util
from pathlib import Path
root = Path("research/certificates/r072x")
def load(name):
    spec = importlib.util.spec_from_file_location(name, root / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module
producer_module = load("generate_certificate")
validator_module = load("validate_certificate")
producer = producer_module.payload()
independent = load("independent_recompute").compute()
sections = (
    "commonZeroAndLocalJet",
    "shrinkingInterfacePowers",
    "blockTilingAndIntegratedEnergy",
    "blochTwist",
    "scalarDamping",
    "zeroCouplingCounterexample",
    "claimBoundary",
)
if producer["status"] != "passed" or not all(producer["exactChecks"].values()):
    raise SystemExit("producer checks failed")
for section in sections:
    if producer[section] != independent[section]:
        raise SystemExit(f"independent section mismatch: {section}")
if producer["producerMethod"] == independent["method"]:
    raise SystemExit("producer and independent method labels unexpectedly coincide")
if producer_module.SOURCE_FILES != validator_module.EXPECTED_SOURCE_FILES:
    raise SystemExit("producer/validator source inventory mismatch")
if len(producer_module.SOURCE_FILES) != len(set(producer_module.SOURCE_FILES)):
    raise SystemExit("duplicate source binding")
if "research/release-manifest.json" in producer_module.SOURCE_FILES:
    raise SystemExit("mutable release manifest must not be source-bound")
print("source-stage independent comparison passed")
`;
  const result = await run(python, ["-c", comparison], {
    cwd: root,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.match(result.stdout, /source-stage independent comparison passed/);
});


test("R0.72X formal lifecycle binds the complete frozen source set", async () => {
  const [producer, validator] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/validate_certificate.py"),
  ]);
  for (const token of [
    "SOURCE_FILES",
    "gitBlob",
    "workingTreeBlobMatches",
    "--source-commit",
    "source commit must equal clean HEAD",
    "refusing to overwrite existing certificate outputs",
    "research/r072x_report-source.md",
    "research/r072x_gap_matrix.md",
    "research/r072x_literature_audit.md",
    "research/r072x_independent_audit.md",
    "scripts/generate_r072x_figure.py",
    "scripts/generate_r072x_release.py",
    "scripts/add-r072x-translations.mjs",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/README.md",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/caption.md",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/contract.json",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/config.json",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/command.txt",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/environment.txt",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/requirements.txt",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/qa-protocol.md",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/plot.py",
    "figures/r072x-all-center/fig-r072x-all-center-transfer/validate.py",
    "tests/r072x-deterministic-certificate-source.test.mjs",
    "tests/r072x-exact-path-gate.test.mjs",
    "tests/r072x-all-center-figure-source.test.mjs",
    "tests/r072x-release.test.mjs",
  ]) assert.ok(producer.includes(token), token);
  assert.ok(!producer.includes('"research/release-manifest.json"'));
  assert.ok(!validator.includes('"research/release-manifest.json"'));
  for (const token of [
    "EXPECTED_SOURCE_FILES",
    "complete frozen source set",
    "formal source binding drift",
    "SHA256SUMS must cover every flat regular file exactly once",
  ]) assert.ok(validator.includes(token), token);
});


test("R0.72X Python sources have no duplicate literal dictionary keys or control bytes", async () => {
  for (const relative of sourceFiles) {
    const bytes = await readFile(resolve(root, relative));
    for (const byte of bytes) {
      assert.ok(byte === 9 || byte === 10 || byte === 13 || byte >= 32, `${relative}: control byte ${byte}`);
    }
  }
  const duplicateKeyAudit = String.raw`
import ast
from pathlib import Path
paths = [
    Path("research/certificates/r072x/generate_certificate.py"),
    Path("research/certificates/r072x/independent_recompute.py"),
    Path("research/certificates/r072x/validate_certificate.py"),
]
for path in paths:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    for node in ast.walk(tree):
        if not isinstance(node, ast.Dict):
            continue
        keys = [key.value for key in node.keys if isinstance(key, ast.Constant) and isinstance(key.value, str)]
        if len(keys) != len(set(keys)):
            raise SystemExit(f"duplicate literal dictionary key in {path}:{node.lineno}")
print("duplicate-key audit passed")
`;
  const result = await run(python, ["-c", duplicateKeyAudit], { cwd: root });
  assert.match(result.stdout, /duplicate-key audit passed/);
});


test("R0.72X source stage exposes only non-mutating self-tests", async () => {
  const formal = await certificateIsFormal();
  if (!formal) await assertNoCertificateOutputs();
  const before = formal ? await generatedSnapshot() : null;
  await assert.rejects(run(python, [
    certificate + "/independent_recompute.py",
  ], { cwd: root }));
  await assert.rejects(run(python, [
    certificate + "/generate_certificate.py",
  ], { cwd: root }));
  const independentRun = await run(python, [
    certificate + "/independent_recompute.py", "--self-test",
  ], { cwd: root });
  assert.match(independentRun.stdout, /passed \(no outputs written\)/);
  const producerRun = await run(python, [
    certificate + "/generate_certificate.py", "--self-test",
  ], { cwd: root });
  assert.match(producerRun.stdout, /passed \(no outputs written\)/);
  if (formal) assert.deepEqual(await generatedSnapshot(), before);
  else await assertNoCertificateOutputs();
});


test("R0.72X strict validator fails closed at source and is exhaustive when formal", async () => {
  if (!(await certificateIsFormal())) {
    await assertNoCertificateOutputs();
    await assert.rejects(run(python, [
      certificate + "/validate_certificate.py", "--require-formal",
    ], { cwd: root }));
    await assertNoCertificateOutputs();
    return;
  }
  const [manifest, crosscheck] = await Promise.all([
    maybeJson(certificate + "/manifest.json"),
    maybeJson(certificate + "/crosscheck.json"),
  ]);
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.ok(Array.isArray(manifest.sourceBindings) && manifest.sourceBindings.length > 0);
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
  assert.equal(crosscheck.sourceCommit, manifest.sourceCommit);
  assert.deepEqual(crosscheck.sourceBindings, manifest.sourceBindings);
  await verifyFlatHashLedger(certificate);
  await run(python, [
    certificate + "/validate_certificate.py", "--require-formal",
  ], { cwd: root });
});
