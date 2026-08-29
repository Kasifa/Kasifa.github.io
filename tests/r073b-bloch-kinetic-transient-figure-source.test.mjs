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
const figure = "figures/r073b/fig-r073b-bloch-kinetic-transient";
const figureId = "fig-r073b-bloch-kinetic-transient";
const bundledPython = "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3";
const python = process.env.CODEX_PYTHON || (existsSync(bundledPython) ? bundledPython : "python3");
const run = promisify(execFile);
const sourceFiles = [
  "README.md", "caption.md", "command.txt", "config.json", "contract.json",
  "environment.txt", "figure-contract.md", "manifest-draft.json", "plot.py",
  "qa-protocol.md", "requirements.txt", "validate.py",
];
const generatedFiles = [
  "SHA256SUMS", "data.csv", "figure.pdf", "figure.png", "figure.svg",
  "manifest.json", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png",
  "qa-report.md", "results.json", "validation.json",
];

async function text(name) {
  return readFile(resolve(root, figure, name), "utf8");
}

async function json(name) {
  return JSON.parse(await text(name));
}

async function absent(name) {
  await assert.rejects(access(resolve(root, figure, name)),
    (error) => error && error.code === "ENOENT", name);
}

async function sha256(path) {
  return createHash("sha256").update(await readFile(path)).digest("hex");
}

test("R0.73B source contract pins the exact four-panel journal surface and evidence boundary", async () => {
  const [config, contract, draft, caption, readme, figureContract, plot, validator] =
    await Promise.all([
      json("config.json"), json("contract.json"), json("manifest-draft.json"),
      text("caption.md"), text("README.md"), text("figure-contract.md"),
      text("plot.py"), text("validate.py"),
    ]);
  assert.equal(config.figureId, figureId);
  assert.equal(config.release, "R0.73B");
  assert.deepEqual(
    [config.widthMillimetres, config.heightMillimetres, config.pngDpi],
    [178, 150, 600],
  );
  assert.equal(config.panelA.minimumDistinctMuPerSeries, 13);
  assert.equal(config.panelA.series.length, 3);
  assert.deepEqual(config.panelB.lambdaValues, [0.25, 1, 4, 16]);
  assert.equal(config.panelB.relativeLimitTolerance, 8e-9);
  assert.equal(config.panelC.muSampleCount, 61);
  assert.equal(config.panelC.lowGapFormula, "||W_x||_2/2");
  assert.deepEqual(config.panelD.weights, [0, 0.5, 1, 1.5]);
  assert.deepEqual(config.panelD.pValues, [0, 0.5]);
  assert.equal(contract.stage, "source-draft");
  assert.equal(contract.chartContract.dataSufficiency.validatedMainRows, 1960);
  assert.equal(contract.chartContract.dataSufficiency.targetedAsymptoticRows, 245);
  assert.equal(contract.chartContract.dataSufficiency.minimumPanelCMuPoints, 41);
  assert.equal(contract.researchBlossom.carriesData, false);
  assert.equal(contract.palette.hardChromaticRootCap, 2);
  assert.deepEqual(contract.palette.chromaticRoots, ["#285F8F", "#A6781F"]);
  assert.equal(contract.claimBoundary.physicalKineticFixedLambdaUniformAnalyticTheorem, true);
  assert.equal(contract.claimBoundary.sharpOSCoefficientLowGapLimit, true);
  for (const key of [
    "finiteDimensionalRowsAreTheorem", "fixedCUniformKineticTheorem",
    "prefactorOneContraction", "exactMaximumTransientGain", "galerkinTailBound",
    "enhancedDissipationA2DirectSum", "nonlinearNavierStokesClosure",
    "clayMillenniumProblemSolved",
  ]) assert.equal(contract.claimBoundary[key], false, key);
  assert.equal(draft.dependency.mainRows, 1960);
  assert.equal(draft.dependency.targetedRows, 245);
  assert.equal(draft.dependency.syntheticSubstitutionAllowed, false);
  assert.equal(draft.dependency.formalBlocked, true);
  for (const prose of [caption, readme, figureContract]) {
    assert.match(prose, /finite.*N=10/is);
    assert.match(prose, /(?:no.*Galerkin tail|without a tail bound)/is);
    assert.match(prose, /(?:A2.*open|no[\s\S]{0,160}enhanced\s+dissipation[\s\S]{0,80}is asserted)/is);
    assert.match(prose, /(?:Clay.*open|no[\s\S]{0,240}Clay implication[\s\S]{0,40}is asserted)/is);
  }
  for (const token of [
    "def upstream_gate", "def heat_shear_k", "def energy_envelope",
    "def triangular_gain", "def predicted_exponent", "def build_rows",
    "def build_scene", "def render_svg", "def render_pdf", "def render_png",
    "def row_checks", "def visible_checks", "def check_formal_lineage",
    "def build_manifest", "def write_sums", "--self-test", "--formal",
    "FINITE N=10 DIAGNOSTICS - NO GALERKIN TAIL",
    "ANALYTIC ENERGY ENVELOPE - UPPER BOUND",
    "EXACT MAXIMUM TRANSIENT: NOT CLAIMED",
    "A2 DIRECT SUM / NONLINEAR / CLAY: OPEN",
  ]) assert.ok(plot.includes(token), token);
  for (const token of [
    "validate_inventory", "validate_upstream", "validate_data",
    "validate_svg", "validate_pdf", "validate_pngs",
    "FINITE N=10", "exactMaximumTransientGain",
  ]) assert.ok(validator.includes(token), token);
});

test("R0.73B figure source pins the complete upstream finite evidence and certificate lineage", async () => {
  const config = await json("config.json");
  for (const relative of Object.values(config.upstream)) {
    await access(resolve(root, relative));
  }
  const [experimentManifest, experimentValidation, certificate, certificateValidation] =
    await Promise.all([
      JSON.parse(await readFile(resolve(root, config.upstream.experimentManifest), "utf8")),
      JSON.parse(await readFile(resolve(root, config.upstream.experimentValidation), "utf8")),
      JSON.parse(await readFile(resolve(root, config.upstream.certificate), "utf8")),
      JSON.parse(await readFile(resolve(root, config.upstream.certificateValidation), "utf8")),
    ]);
  assert.equal(experimentManifest.status, "completed");
  assert.equal(experimentManifest.finiteDimensionalOnly, true);
  assert.equal(experimentValidation.status, "passed");
  assert.ok(Object.values(experimentValidation.checks).every(Boolean));
  assert.ok(["source-stage", "formal"].includes(certificate.certificateStage));
  assert.equal(certificateValidation.status, "passed");
  assert.equal(certificate.claimBoundary.finitePropagatorGridChecked, true);
  assert.equal(certificate.claimBoundary.analyticInfiniteDimensionalEnergyProofReplacedByCertificate, false);
});

test("R0.73B package inventory is exact at source or generated stage", async () => {
  const entries = await readdir(resolve(root, figure), { withFileTypes: true });
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  const names = entries.map((entry) => entry.name).sort();
  if (!names.includes("manifest.json")) {
    assert.deepEqual(names, sourceFiles);
    for (const name of generatedFiles) await absent(name);
  } else {
    assert.deepEqual(names, [...sourceFiles, ...generatedFiles].sort());
    assert.ok(["draft", "formal"].includes((await json("manifest.json")).status));
  }
});

test("R0.73B Python figure sources parse and source self-tests write nothing", async () => {
  for (const name of ["plot.py", "validate.py"]) {
    await run(python, ["-c",
      "import ast,pathlib,sys; ast.parse(pathlib.Path(sys.argv[1]).read_text())",
      resolve(root, figure, name)], { cwd: root });
  }
  const before = (await readdir(resolve(root, figure))).sort();
  const result = await run(python,
    [resolve(root, figure, "plot.py"), "--self-test"], {
      cwd: root, env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
      maxBuffer: 8 * 1024 * 1024,
    });
  const payload = JSON.parse(result.stdout);
  assert.equal(payload.status, "passed");
  assert.equal(payload.rowCount, 364);
  assert.ok(Object.values(payload.checks).every(Boolean));
  assert.deepEqual((await readdir(resolve(root, figure))).sort(), before);
});

test("R0.73B generated package has complete hashes, explicit QA, and no synthetic substitution", async (context) => {
  const entries = (await readdir(resolve(root, figure))).sort();
  if (!entries.includes("manifest.json")) {
    context.skip("source stage: generated figure outputs are intentionally absent");
    return;
  }
  const [manifest, validation, results] = await Promise.all([
    json("manifest.json"), json("validation.json"), json("results.json"),
  ]);
  assert.equal(results.rowCount, 364);
  assert.equal(results.panelA.finiteDimensionalOnly, true);
  assert.equal(results.panelB.exactMaximumTransientClaimed, false);
  assert.equal(results.panelC.computedTruncationPlottedAsExact, false);
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.equal(manifest.deterministic, true);
  assert.equal(manifest.randomSeed, null);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 150);
  assert.equal(manifest.figure.pngDpi, 600);
  assert.equal(manifest.claimBoundary.exactMaximumTransientGain, false);
  assert.equal(manifest.claimBoundary.nonlinearNavierStokes, false);
  assert.equal(manifest.claimBoundary.clayMillenniumProblemSolved, false);
  const ledger = (await text("SHA256SUMS")).trimEnd().split("\n");
  assert.equal(ledger.length, sourceFiles.length + generatedFiles.length - 1);
  for (const row of ledger) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, row);
    assert.equal(await sha256(resolve(root, figure, match[2])), match[1], match[2]);
  }
  if (manifest.status === "formal") {
    assert.equal(manifest.qa.status, "passed");
    assert.equal(manifest.qa.visualInspectionExplicit, true);
    assert.equal(manifest.publication.allowed, true);
    assert.equal(manifest.publication.directory, "public/assets/r073b");
    assert.equal(manifest.lineage.distinct, true);
    assert.equal(manifest.lineage.formalBlocked, false);
  }
});
