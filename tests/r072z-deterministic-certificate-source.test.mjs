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
const certificate = "research/certificates/r072z";
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || (existsSync(bundledPython) ? bundledPython : "python3");
const run = promisify(execFile);
const generated = [
  "certificate.json", "independent.json", "crosscheck.json", "manifest.json", "SHA256SUMS",
];
const completeBoundSources = [
  "research/r072z_report-source.md",
  "research/r072z_gap_matrix.md",
  "research/r072z_literature_audit.md",
  "research/r072z_os_independent_audit.md",
  "research/r072z_squire_independent_audit.md",
  "research/r072z_independent_audit.md",
  "research/certificates/r072z/generate_certificate.py",
  "research/certificates/r072z/independent_recompute.py",
  "research/certificates/r072z/validate_certificate.py",
  "research/certificates/r072z/README.md",
  "research/certificates/r072z/command.txt",
  "research/certificates/r072z/environment.txt",
  "research/release-manifest.json",
  "scripts/generate_r072z_release.py",
  "scripts/add-r072z-translations.mjs",
  "scripts/i18n-snapshots/r072z-missing.json",
  "figures/r072z/fig-r072z-os-squire-threshold/README.md",
  "figures/r072z/fig-r072z-os-squire-threshold/caption.md",
  "figures/r072z/fig-r072z-os-squire-threshold/command.txt",
  "figures/r072z/fig-r072z-os-squire-threshold/config.json",
  "figures/r072z/fig-r072z-os-squire-threshold/contract.json",
  "figures/r072z/fig-r072z-os-squire-threshold/environment.txt",
  "figures/r072z/fig-r072z-os-squire-threshold/figure-contract.md",
  "figures/r072z/fig-r072z-os-squire-threshold/manifest-draft.json",
  "figures/r072z/fig-r072z-os-squire-threshold/plot.py",
  "figures/r072z/fig-r072z-os-squire-threshold/qa-protocol.md",
  "figures/r072z/fig-r072z-os-squire-threshold/requirements.txt",
  "figures/r072z/fig-r072z-os-squire-threshold/validate.py",
  "tests/r072z-deterministic-certificate-source.test.mjs",
  "tests/r072z-os-squire-figure-source.test.mjs",
  "tests/r072z-os-squire-gate.test.mjs",
  "tests/r072z-release.test.mjs",
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
    name, await sha(certificate + "/" + name),
  ])));
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
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries.filter((entry) => entry.name !== "SHA256SUMS").map((entry) => entry.name).sort(),
  );
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
    '"lowGapOSTransientA2Propagator"', '"BlochUniformPhysicalVelocityDirectSum"',
    '"nonlinearNavierStokes"', '"Clay"',
  ]) assert.ok(producer.includes(token), token);
});

test("R0.72Z producer and independent algorithms agree in memory", async () => {
  const script = [
    "import importlib.util", "from pathlib import Path",
    'base=Path("research/certificates/r072z")',
    "def load(name):",
    ' spec=importlib.util.spec_from_file_location(name,base/f"{name}.py")',
    " module=importlib.util.module_from_spec(spec)",
    " spec.loader.exec_module(module)", " return module",
    'pm=load("generate_certificate")', 'im=load("independent_recompute")',
    'vm=load("validate_certificate")', "p=pm.payload()", "i=im.compute()",
    "result=vm.validate_payloads(p,i)", 'assert result["status"]=="passed"',
    'assert p["producerMethod"]!=i["method"]',
    "assert pm.SOURCE_FILES == im.INPUTS == vm.EXPECTED_SOURCE_FILES",
    "assert len(pm.SOURCE_FILES) == 32",
    'print("R0.72Z source-stage dual-route comparison passed")',
  ].join("\n");
  const result = await run(python, ["-c", script], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    maxBuffer: 8 * 1024 * 1024,
  });
  assert.match(result.stdout, /dual-route comparison passed/);
});

test("R0.72Z formal lifecycle binds the complete 32-file source package", async () => {
  const [producer, independent, validator] = await Promise.all([
    text(certificate + "/generate_certificate.py"),
    text(certificate + "/independent_recompute.py"),
    text(certificate + "/validate_certificate.py"),
  ]);
  assert.equal(completeBoundSources.length, 32);
  for (const relative of completeBoundSources) {
    assert.ok(producer.includes('"' + relative + '"'), relative + " producer");
    assert.ok(independent.includes('"' + relative + '"'), relative + " independent");
    assert.ok(validator.includes('"' + relative + '"'), relative + " validator");
  }
  for (const token of [
    "--self-test", "--draft", "--formal", "--formal-source-commit",
    "formal source commit must equal clean HEAD", "workingTreeBlobMatches", "gitBlob",
    "temporaryUnsealedSourceAllowed", "formalSourceReady",
    "refusing to overwrite a formal R0.72Z certificate",
  ]) assert.ok(producer.includes(token), token);
  for (const token of [
    "--require-draft", "--require-formal", "validate_formal_bindings",
    "formal source binding drift", "publication-state manifest drift must be clean-committed",
    "advanced publication-state manifest is accepted only at a completely clean descendant publication commit",
  ]) assert.ok(validator.includes(token), token);
});

test("R0.72Z Python sources have no duplicate literal dictionary keys or control bytes", async () => {
  const paths = [
    certificate + "/generate_certificate.py",
    certificate + "/independent_recompute.py",
    certificate + "/validate_certificate.py",
  ];
  for (const relative of paths) {
    const bytes = await readFile(resolve(root, relative));
    for (const byte of bytes) {
      assert.ok(byte === 9 || byte === 10 || byte === 13 || byte >= 32,
        relative + ": control byte " + byte);
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

test("R0.72Z self-tests never rewrite legacy, draft, or formal outputs", async () => {
  const before = await snapshot();
  const [producerRun, independentRun] = await Promise.all([
    run(python, [certificate + "/generate_certificate.py", "--self-test"], {
      cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    }),
    run(python, [certificate + "/independent_recompute.py", "--self-test"], {
      cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    }),
  ]);
  assert.match(producerRun.stdout, /passed \(no outputs written\)/);
  assert.match(independentRun.stdout, /passed \(no outputs written\)/);
  assert.deepEqual(await snapshot(), before);
});

test("R0.72Z computation is deterministic without writing output files", async () => {
  const script = [
    "import importlib.util,json", "from pathlib import Path",
    'base=Path("research/certificates/r072z")',
    "def load(name):",
    ' spec=importlib.util.spec_from_file_location(name,base/f"{name}.py")',
    " module=importlib.util.module_from_spec(spec)", " spec.loader.exec_module(module)", " return module",
    'p=load("generate_certificate")', 'i=load("independent_recompute")',
    "assert json.dumps(p.payload(),sort_keys=True)==json.dumps(p.payload(),sort_keys=True)",
    "assert json.dumps(i.compute(),sort_keys=True)==json.dumps(i.compute(),sort_keys=True)",
    'print("deterministic no-write recomputation passed")',
  ].join("\n");
  const result = await run(python, ["-c", script], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    maxBuffer: 8 * 1024 * 1024,
  });
  assert.match(result.stdout, /deterministic no-write recomputation passed/);
});

test("R0.72Z validator fails closed after an overclaim", async () => {
  const script = [
    "import copy,importlib.util", "from pathlib import Path",
    'base=Path("research/certificates/r072z")',
    "def load(name):",
    ' spec=importlib.util.spec_from_file_location(name,base/f"{name}.py")',
    " module=importlib.util.module_from_spec(spec)", " spec.loader.exec_module(module)", " return module",
    'p=load("generate_certificate").payload()', 'i=load("independent_recompute").compute()',
    'v=load("validate_certificate")', "tampered=copy.deepcopy(p)",
    'tampered["claimBoundary"]["nonlinearNavierStokesClosureProved"]=True',
    "try:", " v.validate_payloads(tampered,i,hashes=False)", "except ValueError:",
    ' print("fail-closed overclaim rejected")', "else:",
    ' raise SystemExit("validator accepted an overclaim")',
  ].join("\n");
  const result = await run(python, ["-c", script], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.match(result.stdout, /overclaim rejected/);
});

test("R0.72Z strict validator handles legacy, draft, and formal stages fail-closed", async () => {
  const manifest = await maybeJson(certificate + "/manifest.json");
  assert.ok(manifest, "legacy, draft, or formal certificate must exist");
  if (manifest.status === "formal") {
    const boundPaths = manifest.sourceBindings?.map((row) => row.path) ?? [];
    let frozenSourcesCurrent = JSON.stringify(boundPaths) === JSON.stringify(completeBoundSources);
    if (frozenSourcesCurrent) {
      for (const row of manifest.sourceBindings) {
        if (row.path === "research/release-manifest.json") continue;
        const path = resolve(root, row.path);
        if (!existsSync(path) || await sha(row.path) !== row.sha256) {
          frozenSourcesCurrent = false;
          break;
        }
      }
    }
    if (!frozenSourcesCurrent) {
      await assert.rejects(run(python, [
        certificate + "/validate_certificate.py", "--require-formal",
      ], { cwd: root }));
      return;
    }
    await verifyFlatHashLedger();
    const crosscheck = await maybeJson(certificate + "/crosscheck.json");
    assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
    assert.equal(crosscheck.status, "passed");
    assert.equal(crosscheck.formalSourceReady, true);
    assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
    assert.equal(crosscheck.sourceCommit, manifest.sourceCommit);
    assert.deepEqual(crosscheck.sourceBindings, manifest.sourceBindings);
    assert.deepEqual(manifest.sourceBindings.map((row) => row.path), completeBoundSources);
    assert.ok(Object.values(crosscheck.checks).every(Boolean));
    await run(python, [certificate + "/validate_certificate.py", "--require-formal"],
      { cwd: root });
    return;
  }
  if (manifest.status === "draft") {
    await verifyFlatHashLedger();
    await run(python, [certificate + "/validate_certificate.py", "--require-draft"],
      { cwd: root });
  } else {
    assert.equal(manifest.status, undefined, "unknown unsealed manifest status");
    await assert.rejects(run(python, [
      certificate + "/validate_certificate.py", "--require-draft",
    ], { cwd: root }));
  }
  await assert.rejects(run(python, [
    certificate + "/validate_certificate.py", "--require-formal",
  ], { cwd: root }));
});
