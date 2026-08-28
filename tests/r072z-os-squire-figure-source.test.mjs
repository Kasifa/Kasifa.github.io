import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { existsSync } from "node:fs";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const figure = "figures/r072z/fig-r072z-os-squire-threshold";
const figureId = "fig-r072z-os-squire-threshold";
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

async function text(name) { return readFile(resolve(root, figure, name), "utf8"); }
async function json(name) { return JSON.parse(await text(name)); }
async function absent(name) {
  await assert.rejects(access(resolve(root, figure, name)),
    (error) => error?.code === "ENOENT", name);
}

test("R0.72Z source contract pins the exact three-panel claim boundary", async () => {
  const [config, contract, draft, caption, readme, plot, validator] = await Promise.all([
    json("config.json"), json("contract.json"), json("manifest-draft.json"),
    text("caption.md"), text("README.md"), text("plot.py"), text("validate.py"),
  ]);
  assert.equal(config.figureId, figureId);
  assert.deepEqual([config.widthMillimetres, config.heightMillimetres, config.pngDpi],
    [178, 145, 600]);
  assert.deepEqual(config.panelA.highModeNRange, [1, 80]);
  assert.equal(config.panelA.theta0, 0.5);
  assert.deepEqual(config.panelB.cAbsSeries, [4, 32]);
  assert.equal(config.panelB.tangentAbstractNotPhysicalMuZeroVelocity, true);
  assert.deepEqual(config.panelC.rhoOverGammaSeries, [0, 1, 3]);
  assert.equal(config.panelC.LambdaPaymentExplicit, true);
  assert.equal(config.panelC.conditionalOnQHistory, true);
  assert.equal(contract.stage, "source");
  assert.equal(contract.palette.hardChromaticRootCap, 2);
  for (const key of [
    "signedRelativeFormOSAbsorptionClosedInBoundReport",
    "highGapOSPrefactorOneDecayClosedInBoundReport",
    "alphaMinusTwoOSGapSufficiencyClosedInBoundReport",
    "highModeOSGapExponentSharpnessClosedInBoundReport",
    "exactGaplessOSTangentModeClosedInBoundReport",
    "exactKineticOrientationNormalizationClosedInBoundReport",
    "orientationUniformWithLambdaPaymentClosedInBoundReport",
    "strongKernelConditionalSquireTransferClosedInBoundReport",
  ]) assert.equal(contract.claimBoundary[key], true, key);
  for (const key of [
    "allStrongRowsOSPrefactorOneContraction", "abstractGaplessOSA2StrictContraction",
    "lambdaIndependentSquireTransfer", "lowGapOSTransientA2Propagator",
    "BlochUniformPhysicalVelocityDirectSum", "nonlinearNavierStokesClosureProved",
    "clayMillenniumProblemSolved", "figureIsAnalyticProof",
    "figureContainsPDESimulation", "exponentsAreFitted",
  ]) assert.equal(contract.claimBoundary[key], false, key);
  assert.equal(Object.keys(contract.claimBoundary).length, 18);
  assert.equal(draft.status, "source-template-only");
  assert.equal(draft.computation.solver, "none; no PDE discretization");
  assert.match(caption, /coarse\s+sufficient constant is not claimed optimal/i);
  assert.match(caption, /not a\s+physical `mu=0` velocity-row claim/i);
  assert.match(caption, /conditional on the declared\s+`Q` history/i);
  assert.match(readme, /no\s+PDE time-stepper, eigenvalue solver, optimization, regression/i);
  for (const token of [
    "def signed_envelope", "def high_mode_scaled", "def low_mode_growth",
    "def tangent_ratio", "def kinetic_chi", "def build_rows", "def build_scene",
    "render_svg", "render_pdf", "render_png", "--source-commit",
    "--certificate-commit", "--visual-inspected", "FIELDS",
  ]) assert.ok(plot.includes(token), token);
  for (const token of [
    "EXPECTED_FIELDS", "validate_data", "validate_svg", "validate_pdf",
    "validate_pngs", "validate_lineage", "validate_publication", "--require-formal",
  ]) assert.ok(validator.includes(token), token);
});

test("R0.72Z package inventory is exact at source or generated stage", async () => {
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

test("R0.72Z Python sources parse without rendering or writes", async () => {
  for (const name of ["plot.py", "validate.py"]) {
    await run(python, ["-c",
      "import ast,pathlib,sys; ast.parse(pathlib.Path(sys.argv[1]).read_text())",
      resolve(root, figure, name)], { cwd: root });
  }
  for (const name of generatedFiles) {
    if (!(await readdir(resolve(root, figure))).includes("manifest.json")) await absent(name);
  }
});

test("R0.72Z source text exposes every required visible boundary", async () => {
  const plot = await text("plot.py");
  for (const phrase of [
    "CLOSED HIGH-GAP CLASS | COARSE CONSTANT NOT OPTIMAL",
    "g ~ |c|^(2/5) = alpha^(-2): SHARP POWER",
    "ALL-GAP PREFACTOR-ONE L2_q CONTRACTION: FALSE",
    "ABSTRACT TANGENT - NOT PHYSICAL mu=0 ROW",
    "|Lambda| PAID | Q HISTORY REQUIRED",
    "EXACT FORMULAS - NO PDE SIMULATION | LOW-GAP OS PROPAGATOR: OPEN",
    "CLAY PROBLEM: OPEN",
  ]) assert.ok(plot.includes(phrase), phrase);
});
