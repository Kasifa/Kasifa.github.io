import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { existsSync } from "node:fs";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificate = "research/certificates/r072z";
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || (existsSync(bundledPython) ? bundledPython : "python3");
const run = promisify(execFile);

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

test("R0.72Z source exposes every finite certificate ledger", async () => {
  const [producer, independent, validator, readme] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/independent_recompute.py"),
    text(certificate + "/validate_certificate.py"),
    text(certificate + "/README.md"),
  ]);
  for (const token of [
    "def commutator_and_matrix_record", "energyPressureSign", "fourierCoefficients",
    "def m3_and_s_record", "M3Formula", "sBoundSamples", "def alpha_power_record",
    "def two_mode_record", "instantaneousGrowth", "sqrt(2)*exp(-d)/27",
    "def tangent_and_scaled_record", "imaginaryResidual", "VLimitCoefficients",
    "def orientation_record", "chiFormula", "latticeSum", "LambdaPaymentRequired",
    "def kernel_and_j_record", "strongKernelL1", "JFormula", "def claim_ledger",
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "does not import the producer", "def commutator_record", "directActionRows",
    "paired shells", "Poisson summation route", "def polynomial_scaled_record",
    "def simpson", "dampingGapConvolutions", "def claims",
  ]) assert.ok(independent.includes(token), token);
  assert.ok(!/\bimport\s+generate_certificate\b/.test(independent));
  assert.ok(!/\bfrom\s+generate_certificate\s+import\b/.test(independent));
  for (const token of [
    "def validate_schema", "def validate_claim_boundary", "def validate_claim_ledger",
    "def validate_source_hashes", "def validate_exact_ledger",
    "def validate_sha256_ledger", "source inventory mismatch", "escaped OPEN",
  ]) assert.ok(validator.includes(token), token);
  assert.match(readme, /\*\*does not\*\* machine-check/i);
  assert.match(readme, /fail-closed/i);
});

test("R0.72Z boundary keeps low-gap, direct-sum, and nonlinear claims unproved", async () => {
  const producer = await text(certificate + "/generate_certificate.py");
  const validator = await text(certificate + "/validate_certificate.py");
  for (const token of [
    '"lowGapOSTransientA2PropagatorProved": False',
    '"collisionScaleLimitingPropagatorProved": False',
    '"BlochUniformPhysicalVelocityDirectSumProved": False',
    '"completeLinearizedShearSubsystemProved": False',
    '"nonlinearNavierStokesClosureProved": False',
    '"clayMillenniumProblemSolved": False',
  ]) {
    assert.ok(producer.includes(token), token);
    assert.ok(validator.includes(token), token);
  }
  for (const token of [
    '"lowGapOSTransientA2Propagator"',
    '"BlochUniformPhysicalVelocityDirectSum"',
    '"nonlinearNavierStokes"',
    '"Clay"',
  ]) assert.ok(producer.includes(token), token);
});

test("R0.72Z producer and independent algorithms agree in memory", async () => {
  const script = [
    "import importlib.util",
    "from pathlib import Path",
    'base=Path("research/certificates/r072z")',
    "def load(name):",
    ' spec=importlib.util.spec_from_file_location(name,base/f"{name}.py")',
    " module=importlib.util.module_from_spec(spec)",
    " spec.loader.exec_module(module)",
    " return module",
    'p=load("generate_certificate").payload()',
    'i=load("independent_recompute").compute()',
    'v=load("validate_certificate")',
    "result=v.validate_payloads(p,i)",
    'assert result["status"]=="passed"',
    'assert p["producerMethod"]!=i["method"]',
    'print("R0.72Z source-stage dual-route comparison passed")',
  ].join("\n");
  const result = await run(python, ["-c", script], {
    cwd: root,
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    maxBuffer: 8 * 1024 * 1024,
  });
  assert.match(result.stdout, /dual-route comparison passed/);
});

test("R0.72Z certificate generation is deterministic", async () => {
  const temporary = await mkdtemp(resolve(tmpdir(), "r072z-certificate-"));
  const outputs = [resolve(temporary, "producer-a.json"), resolve(temporary, "producer-b.json"),
    resolve(temporary, "independent-a.json"), resolve(temporary, "independent-b.json")];
  for (const output of outputs.slice(0, 2)) {
    await run(python, [certificate + "/generate_certificate.py", "--output", output], { cwd: root });
  }
  for (const output of outputs.slice(2)) {
    await run(python, [certificate + "/independent_recompute.py", "--output", output], { cwd: root });
  }
  assert.equal(await readFile(outputs[0], "utf8"), await readFile(outputs[1], "utf8"));
  assert.equal(await readFile(outputs[2], "utf8"), await readFile(outputs[3], "utf8"));
});

test("R0.72Z validator fails closed after an overclaim", async () => {
  const script = [
    "import copy,importlib.util",
    "from pathlib import Path",
    'base=Path("research/certificates/r072z")',
    "def load(name):",
    ' spec=importlib.util.spec_from_file_location(name,base/f"{name}.py")',
    " module=importlib.util.module_from_spec(spec)",
    " spec.loader.exec_module(module)",
    " return module",
    'p=load("generate_certificate").payload()',
    'i=load("independent_recompute").compute()',
    'v=load("validate_certificate")',
    "tampered=copy.deepcopy(p)",
    'tampered["claimBoundary"]["nonlinearNavierStokesClosureProved"]=True',
    "try:",
    " v.validate_payloads(tampered,i,hashes=False)",
    "except ValueError:",
    ' print("fail-closed overclaim rejected")',
    "else:",
    ' raise SystemExit("validator accepted an overclaim")',
  ].join("\n");
  const result = await run(python, ["-c", script], { cwd: root });
  assert.match(result.stdout, /overclaim rejected/);
});
