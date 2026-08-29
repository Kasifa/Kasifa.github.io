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
const figure = "figures/r073a/fig-r073a-hidden-mean-transient-spectral";
const figureId = "fig-r073a-hidden-mean-transient-spectral";
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
async function sha256(path) {
  return createHash("sha256").update(await readFile(path)).digest("hex");
}

test("R0.73A source contract pins path-sensitive and finite-only boundaries", async () => {
  const [config, contract, draft, caption, readme, figureContract, plot, validator] =
    await Promise.all([
      json("config.json"), json("contract.json"), json("manifest-draft.json"),
      text("caption.md"), text("README.md"), text("figure-contract.md"),
      text("plot.py"), text("validate.py"),
    ]);
  assert.equal(config.figureId, figureId);
  assert.deepEqual([config.widthMillimetres, config.heightMillimetres, config.pngDpi],
    [178, 145, 600]);
  assert.deepEqual(config.panelA.dSeries, [0, 0.25, 1, 2]);
  assert.equal(config.panelA.muSampleCount, 61);
  assert.equal(config.panelB.sampleCountPerSeries, 81);
  assert.equal(config.panelB.certificateBoundTolerance, 2e-8);
  assert.equal(config.panelB.certificateOverlayRequiredForFormal, true);
  assert.equal(config.panelB.certificateAvailableAtSourceFreeze, true);
  assert.equal(config.panelC.N, 40);
  assert.equal(config.panelC.expectedRows, 30);
  assert.deepEqual(config.panelC.displayDomains["frozen-spectral-edge"], [-0.25, 5]);
  assert.deepEqual(config.panelC.displayDomains["frozen-numerical-abscissa"], [-0.25, 8]);
  assert.ok(config.panelC.displayTicks["frozen-spectral-edge"].includes(0));
  assert.ok(config.panelC.displayTicks["frozen-numerical-abscissa"].includes(0));
  assert.equal(config.panelC.minimumDisplayPadding, 0.2);
  assert.equal(config.panelC.finiteDimensionalOnly, true);
  assert.equal(config.panelC.galerkinTailBoundAvailable, false);
  assert.equal(contract.stage, "source-ready-for-formal-certificate");
  assert.equal(contract.chartContract.dataSufficiency,
    "851 analytic/audited metric rows plus 120 deterministic certificate-overlay rows at source freeze");
  assert.equal(contract.claimBoundary.exactNormalizedHiddenMeanBracketClosedInBoundDraft, true);
  assert.equal(contract.claimBoundary.nonzeroHiddenDerivativeLimitAlongCmuToNonzeroPath, true);
  assert.equal(contract.claimBoundary.fixedLambdaHiddenDerivativeLimitDecided, false);
  assert.equal(contract.claimBoundary.instantaneousLiftedLineInvariantAtPositiveGap, false);
  assert.equal(contract.claimBoundary.finiteFrozenGalerkinScreenValidated, true);
  assert.equal(contract.claimBoundary.certifiedXmuPropagatorGainAvailableAtSourceFreeze, true);
  for (const key of [
    "rankOneAbstractTangentClosesPhysicalLongWaveLimit",
    "fixedProjectionUniformlyStabilizesFrozenScreen",
    "continuousTimeMaximumTransientGainProved",
    "infiniteDimensionalFrozenSpectrumProved", "galerkinTailBoundProved",
    "lowGapPhysicalKineticPropagatorProved", "BlochUniformPhysicalVelocityDirectSumProved",
    "nonlinearNavierStokesClosureProved", "clayMillenniumProblemSolved",
    "figureContainsSyntheticCertificateData", "figureIsAnalyticProof",
  ]) assert.equal(contract.claimBoundary[key], false, key);
  assert.equal(contract.palette.hardChromaticRootCap, 2);
  assert.equal(draft.dependency.available, true);
  assert.equal(draft.dependency.syntheticSubstitutionAllowed, false);
  assert.equal(draft.dependency.formalBlocked, true);
  for (const prose of [caption, readme, figureContract]) {
    assert.match(prose, /c_mu\s*->\s*c0\s*!=\s*0/i);
    assert.match(prose, /fixed\s+`?Lambda`?.*(undecided|not decide)/is);
  }
  assert.match(caption, /instantaneous lifted line is not invariant/i);
  assert.match(caption, /120 deterministic `X_mu` propagator-gain certificate rows/i);
  assert.match(readme, /black cross markers/i);
  assert.match(figureContract, /120 propagator-certificate rows \(971 total\)/i);
  for (const token of [
    "def hidden_mean", "def hidden_limit", "def transient_j",
    "def transient_envelope", "def signed_log", "def build_rows", "def build_scene",
    "certificateRequiredSchema", "formal render requires the certified X_mu",
    "CERTIFICATE_BOUND_TOLERANCE = 2e-8",
    "render_svg", "render_pdf", "render_png", "FIELDS",
  ]) assert.ok(plot.includes(token), token);
  for (const token of [
    "EXPECTED_FIELDS", "validate_data", "validate_svg", "validate_pdf",
    "validate_pngs", "validate_lineage", "validate_publication", "STALE_RELEASE_TOKENS",
    "stale R0.72Z token", "851 + len(certificate)", "--require-formal",
    "CERTIFICATE_BOUND_TOLERANCE = 2e-8",
  ]) assert.ok(validator.includes(token), token);
});

test("R0.73A pins the independently audited finite source bytes", async () => {
  const config = await json("config.json");
  assert.equal(await sha256(resolve(root, config.panelC.sourceCsv)),
    config.panelC.sourceSha256);
  assert.equal(await sha256(resolve(root, config.panelC.validationJson)),
    config.panelC.validationSha256);
  const upstream = JSON.parse(await readFile(resolve(root, config.panelC.validationJson), "utf8"));
  assert.equal(upstream.status, "passed");
  assert.ok(Object.values(upstream.checks).every(Boolean));
});

test("R0.73A package inventory is exact at source or generated stage", async () => {
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

test("R0.73A Python sources parse and self-test without rendering or writes", async () => {
  for (const name of ["plot.py", "validate.py"]) {
    await run(python, ["-c",
      "import ast,pathlib,sys; ast.parse(pathlib.Path(sys.argv[1]).read_text())",
      resolve(root, figure, name)], { cwd: root });
  }
  const before = (await readdir(resolve(root, figure))).sort();
  const { stdout } = await run(python,
    [resolve(root, figure, "plot.py"), "--self-test"], { cwd: root });
  assert.equal(JSON.parse(stdout).status, "passed");
  assert.deepEqual((await readdir(resolve(root, figure))).sort(), before);
});

test("R0.73A visible boundaries are complete and R0.72Z tokens are absent", async () => {
  const plot = await text("plot.py");
  for (const phrase of [
    "BRACKET mu->0: NONZERO IF c_mu->c0 != 0",
    "ABSTRACT TANGENT: NO HIDDEN COORDINATE",
    "FIXED Lambda (c_mu->0): UNDECIDED",
    "bracket limit (c_mu factor excluded)",
    "ANALYTIC UPPER ENVELOPE - NOT OBSERVED GAIN",
    "J start:",
    "E mu/|c|/s:",
    "CERTIFIED X_mu GAIN: PENDING - NOT PLOTTED",
    "FORMAL SEAL BLOCKED; NO SYNTHETIC CURVE",
    "FINITE GALERKIN N=40 - NOT INFINITE-DIMENSIONAL",
    "FIXED PROJECTION SUFFICIENT: FALSE IN SCREEN",
    "NO GALERKIN TAIL BOUND",
    "LOW-GAP KINETIC / BLOCH DIRECT SUM / NONLINEAR: OPEN",
    "CLAY PROBLEM: OPEN",
    "Three matrix variants across ten low-gap target cases",
  ]) assert.ok(plot.includes(phrase), phrase);
  for (const check of [
    "panelCDomainsContainAllDataWithPadding",
    "formulaAnnotationsOutsideDataRects",
    "panelBJLegendVisible",
    "panelBEnvelopeLegendVisible",
  ]) assert.ok(plot.includes(check), check);
  for (const stale of [
    "Squire payment", "g ~ |c|^(2/5)", "CLOSED HIGH-GAP CLASS",
    "ALL-GAP PREFACTOR-ONE", "history-L2-multiplier", "kinetic-orientation",
  ]) assert.equal(plot.includes(stale), false, stale);
  assert.equal(plot.includes("Three deletions across ten low-gap target cases"), false);
});
