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
const certificate = resolve(root, "research/certificates/r073c");
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || (existsSync(bundledPython) ? bundledPython : "python3");
const run = promisify(execFile);

const text = (name) => readFile(resolve(certificate, name), "utf8");
const json = async (name) => JSON.parse(await text(name));
const sha = async (path) => createHash("sha256").update(await readFile(path)).digest("hex");

test("R0.73C certificate producer and validator pin the exact C3/C4 theorem and C5/C6 boundary", async () => {
  const [producer, validator] = await Promise.all([
    text("generate_certificate.py"), text("validate_certificate.py"),
  ]);
  for (const source of [producer, validator]) {
    for (const token of [
      "exactCubicNeutralSpectrum", "infiniteDimensionalFrozenRayleighInstability",
      "frozenInstabilityFastTimeTransfer", "superPolynomialCompleteRowNoGo",
      "interval_run_a.json", "interval_run_b.json",
      "decimal_interval_validation.json", "independent_fourier_validation.json",
      "sourceBindings", "SHA256SUMS",
      "scripts/generate_r073c_release.py", "tests/r073c-release.test.mjs",
      "tests/r073c-rayleigh-instability-gate.test.mjs",
    ]) assert.ok(source.includes(token), token);
    assert.match(source, /--self-test/);
  }
  assert.match(producer, /--source-stage/);
  assert.match(producer, /--formal/);
  assert.match(producer, /--source-commit/);
  assert.match(validator, /--require-source-stage/);
  assert.match(validator, /--require-formal/);
  assert.equal(producer.includes("import validate_certificate"), false);
  assert.equal(validator.includes("import generate_certificate"), false);
});

test("R0.73C Python certificate sources parse and source self-tests write nothing", async () => {
  for (const name of ["generate_certificate.py", "validate_certificate.py"]) {
    await run(python, ["-c",
      "import ast,pathlib,sys; ast.parse(pathlib.Path(sys.argv[1]).read_text())",
      resolve(certificate, name)], { cwd: root });
  }
  const before = (await readdir(certificate)).sort();
  const first = await run(python, [resolve(certificate, "generate_certificate.py"), "--self-test"], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" }, maxBuffer: 16 * 1024 * 1024,
  });
  const second = await run(python, [resolve(certificate, "generate_certificate.py"), "--self-test"], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" }, maxBuffer: 16 * 1024 * 1024,
  });
  assert.equal(first.stdout, second.stdout);
  assert.equal(JSON.parse(first.stdout).status, "passed");
  const independent = await run(python, [resolve(certificate, "validate_certificate.py"), "--self-test"], {
    cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" }, maxBuffer: 16 * 1024 * 1024,
  });
  assert.equal(JSON.parse(independent.stdout).status, "passed");
  assert.deepEqual((await readdir(certificate)).sort(), before);
});

test("R0.73C generated certificate validates at its declared source or formal stage", async (context) => {
  try {
    await access(resolve(certificate, "certificate.json"));
  } catch (error) {
    if (error && error.code === "ENOENT") {
      context.skip("certificate outputs are not generated yet");
      return;
    }
    throw error;
  }
  const [payload, manifest, crosscheck] = await Promise.all([
    json("certificate.json"), json("manifest.json"), json("crosscheck.json"),
  ]);
  assert.ok(["source-stage", "formal"].includes(payload.certificateStage));
  assert.equal(manifest.status, payload.certificateStage === "formal" ? "formal" : "source-stage");
  assert.equal(crosscheck.status, "passed");
  assert.equal(payload.claimBoundary.exactCubicNeutralSpectrumClosed, true);
  assert.equal(payload.claimBoundary.infiniteDimensionalFrozenRayleighInstabilityClosed, true);
  assert.equal(payload.claimBoundary.frozenInstabilityFastTimeTransferProved, false);
  assert.equal(payload.claimBoundary.superPolynomialCompleteRowNoGo, "conditional-on-C5");
  const flag = payload.certificateStage === "formal" ? "--require-formal" : "--require-source-stage";
  const result = await run(python, [resolve(certificate, "validate_certificate.py"), flag], {
    cwd: root, maxBuffer: 16 * 1024 * 1024,
  });
  assert.equal(JSON.parse(result.stdout).status, "passed");
});

test("R0.73C certificate hash ledger is flat, sorted, complete, and exact", async (context) => {
  try {
    await access(resolve(certificate, "SHA256SUMS"));
  } catch (error) {
    if (error && error.code === "ENOENT") {
      context.skip("certificate hash ledger is not generated yet");
      return;
    }
    throw error;
  }
  const rows = (await text("SHA256SUMS")).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, row);
    assert.equal(await sha(resolve(certificate, match[2])), match[1], match[2]);
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(certificate, { withFileTypes: true });
  assert.deepEqual(
    names,
    entries.filter((entry) => entry.isFile() && entry.name !== "SHA256SUMS")
      .map((entry) => entry.name).sort(),
  );
});
