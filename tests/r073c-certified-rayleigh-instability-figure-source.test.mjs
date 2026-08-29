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
const figure = "figures/r073c/fig-r073c-certified-rayleigh-instability";
const figureId = "fig-r073c-certified-rayleigh-instability";
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || (existsSync(bundledPython) ? bundledPython : "python3");
const run = promisify(execFile);

const text = (name) => readFile(resolve(root, figure, name), "utf8");
const json = async (name) => JSON.parse(await text(name));
const sha = async (path) => createHash("sha256").update(await readFile(path)).digest("hex");

test("R0.73C figure contract pins the exact four-panel surface and fail-closed boundaries", async () => {
  const [config, contract, results, caption, readme, figureContract] = await Promise.all([
    json("config.json"), json("contract.json"), json("results.json"),
    text("caption.md"), text("README.md"), text("figure-contract.md"),
  ]);
  assert.equal(config.figureId, figureId);
  assert.deepEqual([config.widthMillimetres, config.heightMillimetres, config.pngDpi], [178, 132, 600]);
  assert.deepEqual(config.panels, ["A", "B", "C", "D"]);
  assert.equal(config.randomness, "none");
  assert.equal(contract.release, "R0.73C");
  assert.equal(contract.figureId, figureId);
  assert.deepEqual(contract.certifiedElements.etaBracket, ["0.3407", "0.3410"]);
  assert.deepEqual(contract.certifiedElements.sigmaBracket, ["0.17035", "0.17050"]);
  assert.deepEqual(contract.certifiedElements.endpointSigns, ["negative", "positive"]);
  assert.equal(contract.claimBoundary.exactCubicNeutralSpectrum, true);
  assert.equal(contract.claimBoundary.infiniteDimensionalFrozenRayleighInstability, true);
  for (const key of [
    "smoothTraceCurveItselfIsCertified", "finiteFourierRowsAreTheorem",
    "rootUniqueness", "algebraicSimplicity", "viscousSpectralPersistence",
    "nonautonomousTransfer", "nonlinearNavierStokesClosure",
    "clayMillenniumProblemSolved",
  ]) assert.equal(contract.claimBoundary[key], false, key);
  assert.equal(results.figureId, figureId);
  assert.equal(results.claimBoundary.endpointSignsCertifiedByInput, true);
  for (const key of [
    "finiteFourierRowsAreTheorem", "smoothTraceCurveCertified",
    "viscousTransferProved", "nonlinearNavierStokesProved", "clayProblemSolved",
  ]) assert.equal(results.claimBoundary[key], false, key);
  for (const prose of [caption, readme]) {
    assert.match(prose, /C3|neutral/i);
    assert.match(prose, /C4|Rayleigh/i);
  }
  for (const prose of [caption, readme, figureContract]) {
    assert.match(prose, /C5|viscous|transfer/i);
    assert.match(prose, /(?:finite|Fourier)/i);
  }
});

test("R0.73C figure binds primary interval and independent finite diagnostics by SHA-256", async () => {
  const manifest = await json("manifest.json");
  assert.equal(manifest.release, "R0.73C");
  assert.equal(manifest.figureId, figureId);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.git.repository, "Kasifa/Kasifa.github.io");
  assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
  assert.match(manifest.git.certificateCommit, /^[0-9a-f]{40}$/);
  assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  assert.equal(manifest.figure.outputs.length, 3);
  assert.equal(manifest.qa.finalSizeInspected, true);
  assert.equal(manifest.qa.dataCrossChecked, true);
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.equal(manifest.publication.assets.length, 3);
  const expected = new Set([
    "experiments/r073c/interval_run_b.json",
    "experiments/r073c/fourier_screen.json",
    "experiments/r073c/independent_fourier_validation.json",
  ]);
  assert.deepEqual(new Set(manifest.inputBindings.map((row) => row.path)), expected);
  for (const row of manifest.inputBindings) {
    assert.equal(await sha(resolve(root, row.path)), row.sha256, row.path);
  }
});

test("R0.73C figure package inventory and SHA-256 ledger cover every ordinary file exactly once", async () => {
  const entries = await readdir(resolve(root, figure), { withFileTypes: true });
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  const names = entries.filter((entry) => entry.name !== "SHA256SUMS").map((entry) => entry.name).sort();
  const rows = (await text("SHA256SUMS")).trimEnd().split("\n");
  const ledgerNames = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, row);
    assert.equal(await sha(resolve(root, figure, match[2])), match[1], match[2]);
    ledgerNames.push(match[2]);
  }
  assert.deepEqual(ledgerNames, [...new Set(ledgerNames)].sort());
  assert.deepEqual(ledgerNames, names);
});

test("R0.73C figure source parses and the sealed validator reports complete visual QA", async () => {
  for (const name of ["plot.py", "validate.py"]) {
    await run(python, ["-c",
      "import ast,pathlib,sys; ast.parse(pathlib.Path(sys.argv[1]).read_text())",
      resolve(root, figure, name)], { cwd: root });
  }
  const [manifest, validation] = await Promise.all([json("manifest.json"), json("validation.json")]);
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.visualInspectionExplicit, true);
  assert.equal(manifest.publication.directory, "public/assets/r073c");
  assert.equal(manifest.publication.byteIdentityRequired, true);
  assert.deepEqual(manifest.masters, ["figure.pdf", "figure.svg", "figure.png"]);
  assert.deepEqual(validation.pdfPoints, [504, 373.68]);
  assert.deepEqual(validation.pngPixels, [4200, 3114]);
});
