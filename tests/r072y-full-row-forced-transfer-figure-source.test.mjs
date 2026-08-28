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
const figure = "figures/r072y/fig-r072y-full-row-forced-transfer";
const figureId = "fig-r072y-full-row-forced-transfer";
const sourceFiles = [
  "README.md",
  "caption.md",
  "command.txt",
  "config.json",
  "contract.json",
  "environment.txt",
  "figure-contract.md",
  "plot.py",
  "qa-protocol.md",
  "requirements.txt",
  "validate.py",
];
const generatedFiles = [
  "SHA256SUMS",
  "data.csv",
  "figure.pdf",
  "figure.png",
  "figure.svg",
  "manifest.json",
  "qa-final-size.png",
  "qa-grayscale.png",
  "qa-pdf.png",
  "qa-report.md",
  "results.json",
  "validation.json",
];

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function maybeJson(relative) {
  try {
    return await json(relative);
  } catch (error) {
    if (error?.code === "ENOENT") return null;
    throw error;
  }
}

async function sha(relative) {
  return createHash("sha256")
    .update(await readFile(resolve(root, relative)))
    .digest("hex");
}

async function absent(relative) {
  await assert.rejects(
    access(resolve(root, relative)),
    (error) => error?.code === "ENOENT",
    relative,
  );
}

async function stage() {
  return (await maybeJson(figure + "/manifest.json"))?.status || "source";
}

async function verifyHashLedger() {
  const rows = (await text(figure + "/SHA256SUMS")).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, "malformed SHA256SUMS row: " + row);
    assert.equal(await sha(figure + "/" + match[2]), match[1], match[2]);
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(resolve(root, figure), { withFileTypes: true });
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries
      .filter((entry) => entry.name !== "SHA256SUMS")
      .map((entry) => entry.name).sort(),
  );
}

test("R0.72Y source contract pins the exact three-panel figure", async () => {
  const [config, contract, caption, readme, plot, validator] = await Promise.all([
    json(figure + "/config.json"),
    json(figure + "/contract.json"),
    text(figure + "/caption.md"),
    text(figure + "/README.md"),
    text(figure + "/plot.py"),
    text(figure + "/validate.py"),
  ]);
  assert.equal(config.figureId, figureId);
  assert.deepEqual(
    {
      width: config.widthMillimetres,
      height: config.heightMillimetres,
      dpi: config.pngDpi,
    },
    { width: 178, height: 145, dpi: 600 },
  );
  assert.equal(config.panelA.muPositiveOnlyForOSSquire, true);
  assert.equal(config.panelA.scalarInvariantEmbeddingClosed, true);
  assert.equal(config.panelA.strongFullRowA2EstimateOpen, true);
  assert.equal(config.panelA.uniformStrictContractionFalse, true);
  assert.equal(config.panelB.sampleCountPerSeries, 121);
  assert.deepEqual(config.panelB.series, [
    { label: "xi=0, Lambda=2", xi: 0, Lambda: 2 },
    { label: "xi=0.5, Lambda=8", xi: 0.5, Lambda: 8 },
    { label: "xi=1, Lambda=16", xi: 1, Lambda: 16 },
  ]);
  assert.equal(config.panelB.diagnosticOnly, true);
  assert.equal(config.panelB.counterexampleToUniformStrictContraction, true);
  assert.equal(config.panelC.sampleCountPerSeries, 41);
  assert.deepEqual(config.panelC.series, [
    { label: "standard H^-1 spacetime", power: 1 },
    { label: "semiclassical H^-1 spacetime", power: 2 },
    { label: "standard H^-1 endpoint", power: 0 },
  ]);
  assert.equal(config.panelC.guidesAreFits, false);
  assert.equal(config.panelC.analyticProofElsewhere, true);
  assert.equal(contract.stage, "source-plus-draft-render");
  assert.equal(contract.chartContract.finalSurface.startsWith("178 mm"), true);
  assert.equal(contract.palette.hardChromaticRootCap, 2);
  for (const key of [
    "exactThreeDimensionalLinearizationClosedInBoundReport",
    "exactPressurePoissonFactorTwoClosedInBoundReport",
    "exactOSSquireTriangularizationForMuPositiveClosedInBoundReport",
    "scalarA2InvariantEmbeddingClosedInBoundReport",
    "exactZeroCouplingLiftUpFormulaClosedInBoundReport",
    "strongRowStandardHMinusOneSpacetimeAlphaClosedInBoundReport",
    "strongRowSemiclassicalHMinusOneSpacetimeAlphaSquaredClosedInBoundReport",
  ]) assert.equal(contract.claimBoundary[key], true, key);
  for (const key of [
    "standardHMinusOneEndpointAlphaGain",
    "allPhysicalRowsUniformStrictContraction",
    "strongFullRowA2Estimate",
    "completeLinearizedShearSubsystemProved",
    "nonlinearNavierStokesClosureProved",
    "clayMillenniumProblemSolved",
    "figureIsAnalyticProof",
    "ratesAreFitted",
  ]) assert.equal(contract.claimBoundary[key], false, key);
  assert.equal(Object.keys(contract.claimBoundary).length, 15);
  assert.match(caption, /strong full-row.*remains open/is);
  assert.match(caption, /exact diagnostics/i);
  assert.match(caption, /no exponent is fitted/i);
  assert.match(readme, /No PDE solver, regression, random\s+seed, or fitted exponent/i);
  for (const token of [
    "def lift_up_ratio",
    "def build_rows",
    "def build_scene",
    "render_svg",
    "render_pdf",
    "render_png",
    "make_qa_previews",
    "check_formal_lineage",
    "--source-commit",
    "--certificate-commit",
    "--visual-inspected",
    '"claimBoundary"',
    '"publication"',
  ]) assert.ok(plot.includes(token), token);
  for (const token of [
    "EXPECTED_FIELDS",
    "validate_data",
    "validate_svg",
    "validate_pdf",
    "validate_pngs",
    "validate_lineage",
    "validate_publication",
    "--require-formal",
    "claim boundary differs from the source contract",
  ]) assert.ok(validator.includes(token), token);
});

test("R0.72Y figure inventory is exact at source, draft, or formal stage", async () => {
  const currentStage = await stage();
  const entries = await readdir(resolve(root, figure), { withFileTypes: true });
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  const names = entries.map((entry) => entry.name).sort();
  if (currentStage === "source") {
    assert.deepEqual(names, sourceFiles);
    for (const name of generatedFiles) await absent(figure + "/" + name);
    return;
  }
  assert.ok(["draft", "formal"].includes(currentStage));
  assert.deepEqual(names, [...sourceFiles, ...generatedFiles].sort());
  await verifyHashLedger();
});

test("R0.72Y figure self-test is zero-write", async () => {
  const currentStage = await stage();
  const before = currentStage === "source"
    ? null
    : Object.fromEntries(await Promise.all(generatedFiles.map(async (name) => [
      name,
      await sha(figure + "/" + name),
    ])));
  const result = await run(
    python,
    [figure + "/plot.py", "--self-test"],
    { cwd: root },
  );
  const summary = JSON.parse(result.stdout);
  assert.equal(summary.status, "passed");
  assert.equal(Object.values(summary.checks).every(Boolean), true);
  if (currentStage === "source") {
    for (const name of generatedFiles) await absent(figure + "/" + name);
  } else {
    const after = Object.fromEntries(await Promise.all(generatedFiles.map(async (name) => [
      name,
      await sha(figure + "/" + name),
    ])));
    assert.deepEqual(after, before);
  }
});

test("R0.72Y draft data recomputes the exact formulas and visible boundaries", async (t) => {
  const currentStage = await stage();
  if (currentStage === "source") return t.skip("source stage");
  const [manifest, results, validation, data] = await Promise.all([
    json(figure + "/manifest.json"),
    json(figure + "/results.json"),
    json(figure + "/validation.json"),
    text(figure + "/data.csv"),
  ]);
  assert.equal(manifest.figureId, figureId);
  assert.equal(manifest.release, "R0.72Y");
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.visualInspectionExplicit, true);
  assert.equal(manifest.computation.randomSeed, null);
  assert.equal(manifest.computation.solver, "direct closed-form evaluation; no PDE discretization");
  assert.equal(manifest.claimBoundary.strongFullRowA2Estimate, false);
  assert.equal(manifest.claimBoundary.clayMillenniumProblemSolved, false);
  assert.equal(results.rowCount, 494);
  assert.equal(results.panelA.strongFullRowA2Estimate, "OPEN");
  assert.equal(results.panelA.allPhysicalRowsUniformStrictContraction, "FALSE");
  assert.deepEqual(results.panelC.powers, {
    "semiclassical H^-1 spacetime": 2,
    "standard H^-1 endpoint": 0,
    "standard H^-1 spacetime": 1,
  });
  assert.equal(results.panelC.fittedQuantities.length, 0);
  assert.equal(validation.status, "passed");
  assert.equal(validation.rowCount, 494);
  assert.equal(Object.values(validation.checks).every(Boolean), true);
  assert.equal(data.trimEnd().split("\n").length, 495);
  await run(python, [figure + "/validate.py"], { cwd: root });
});

test("R0.72Y formal validator fails closed until two-commit lineage is sealed", async () => {
  const currentStage = await stage();
  if (currentStage !== "formal") {
    await assert.rejects(run(
      python,
      [figure + "/validate.py", "--require-formal"],
      { cwd: root },
    ));
    return;
  }
  const manifest = await json(figure + "/manifest.json");
  assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
  assert.match(manifest.git.certificateCommit, /^[0-9a-f]{40}$/);
  assert.notEqual(manifest.git.sourceCommit, manifest.git.certificateCommit);
  assert.equal(manifest.publication.directory, "public/assets/r072y");
  assert.equal(manifest.publication.byteIdenticalToArchive, true);
  await run(python, [figure + "/validate.py", "--require-formal"], { cwd: root });
  for (const extension of ["pdf", "svg", "png"]) {
    assert.deepEqual(
      await readFile(resolve(root, figure, "figure." + extension)),
      await readFile(resolve(root, "public/assets/r072y", figureId + "." + extension)),
    );
  }
});
