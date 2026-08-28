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
const figure = (
  "figures/r072w-exact-periodic/"
  + "fig-r072w-exact-tail-transfer"
);
const figureId = "fig-r072w-exact-tail-transfer";
const sourceFiles = [
  "README.md",
  "caption.md",
  "command.txt",
  "config.json",
  "contract.json",
  "environment.txt",
  "plot.py",
  "qa-protocol.md",
  "requirements.txt",
  "validate.py",
];
const generated = [
  "data.csv",
  "results.json",
  "validation.json",
  "progress.ndjson",
  "resource-log.ndjson",
  "qa-report.md",
  "figure.svg",
  "figure.pdf",
  "figure.png",
  "qa-final-size.png",
  "qa-grayscale.png",
  "qa-pdf.png",
  "manifest.json",
  "SHA256SUMS",
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


async function figureStage() {
  return (await maybeJson(figure + "/manifest.json"))?.status || "source";
}


async function generatedSnapshot() {
  return Object.fromEntries(await Promise.all(generated.map(async (name) => [
    name,
    await sha(figure + "/" + name),
  ])));
}


async function assertNoPublicOutputs() {
  for (const extension of ["pdf", "svg", "png"]) {
    await absent(
      "public/assets/r072w/" + figureId + "." + extension,
    );
  }
}


async function assertNoFigureOutputs() {
  for (const name of generated) await absent(figure + "/" + name);
  await assertNoPublicOutputs();
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
    entries
      .filter((entry) => entry.isFile() && entry.name !== "SHA256SUMS")
      .map((entry) => entry.name)
      .sort(),
  );
}


test("R0.72W source contract separates exact theorems from the diagnostic", async () => {
  const [config, contract, caption, readme] = await Promise.all([
    json(figure + "/config.json"),
    json(figure + "/contract.json"),
    text(figure + "/caption.md"),
    text(figure + "/README.md"),
  ]);
  assert.equal(config.figureId, figureId);
  assert.deepEqual(
    {
      width: config.widthMillimetres,
      height: config.heightMillimetres,
      dpi: config.pngDpi,
    },
    { width: 178, height: 98, dpi: 600 },
  );
  assert.deepEqual(config.panelA.coefficientCurve, {
    a0: "2*(cos(z)-cos(2*z))",
    a1: "2*(-cos(z)+4*cos(2*z))",
    zRange: [-Math.PI, Math.PI],
  });
  assert.equal(config.panelA.noGoRatiosAtYPi.h5Over4, "5*pi^2/12");
  assert.equal(
    config.panelA.noGoRatiosAtYPi.combinedH5H7,
    "abs(-5*pi^2/12+7*pi^4/120)",
  );
  assert.equal(config.panelB.compactCondition, "alpha*R -> 0");
  assert.equal(config.panelB.escapingScale, "R=y/alpha");
  assert.equal(config.panelB.termwiseAbsorption, false);
  assert.deepEqual(config.panelC.alphas, [1, 0.75, 0.5, 0.35, 0.25]);
  assert.deepEqual(config.panelC.levels, [
    { label: "coarse", spatialModes: 512, timeSteps: 1000 },
    { label: "medium", spatialModes: 1024, timeSteps: 2000 },
    { label: "fine", spatialModes: 2048, timeSteps: 4000 },
  ]);
  assert.equal(config.panelC.powerIterations, 32);
  assert.equal(config.panelC.precision, "float64/complex128");
  assert.equal(config.panelC.randomSeed, null);
  assert.equal(config.panelC.diagnosticOnly, true);

  assert.equal(contract.stage, "source-only");
  assert.equal(contract.numericalDiagnosticPlanned, true);
  assert.equal(contract.simulationPerformedAtSourceStage, false);
  for (const key of [
    "weightedNonabsorbedRemainderEstimateProved",
    "growingCoreAbsorptionProved",
    "globalTermwiseRemainderAbsorptionFalse",
    "exactFamilyUnitCellCoercivityProved",
    "exactWholeLineGraphCoercivityProved",
    "exactPeriodicGraphCoercivityProved",
    "exactPeriodicBlockContractionProved",
  ]) assert.equal(contract.claimBoundary[key], true, key);
  for (const key of [
    "numericalDiagnosticIsProof",
    "numericalDiagnosticDeterminesAnalyticConstant",
    "outerTimeConcatenationProved",
    "timeLengthUniformity",
    "nonlinearNavierStokesClosureProved",
    "clayMillenniumProblemSolved",
  ]) assert.equal(contract.claimBoundary[key], false, key);
  assert.match(caption, /numerical diagnostic only/i);
  assert.ok(caption.includes("does not evaluate \\(C_T\\)"));
  assert.match(caption, /outer-time concatenation.*remain open/is);
  assert.match(readme, /writes\s+nothing/i);
});


test("R0.72W source pins the exact deterministic forward-adjoint method", async () => {
  const [generator, environment, requirements, protocol] = await Promise.all([
    text("scripts/generate_r072w_figure.py"),
    text(figure + "/environment.txt"),
    text(figure + "/requirements.txt"),
    text(figure + "/qa-protocol.md"),
  ]);
  for (const token of [
    "DIAGNOSTIC_ALPHAS = (1.0, 0.75, 0.5, 0.35, 0.25)",
    '("coarse", 512, 1000)',
    '("medium", 1024, 2000)',
    '("fine", 2048, 4000)',
    "POWER_ITERATIONS = 32",
    "np.complex128",
    "np.fft.fft",
    "np.fft.ifft",
    "def forward(vector",
    "def adjoint(vector",
    "forward-adjoint power iteration degenerated",
    "deterministic numerical diagnostic only; not proof",
    "randomSeed",
    "progress.ndjson",
    "resource-log.ndjson",
    '"kind": "simulation"',
    '"configuration"',
    '"formalCommand"',
    '"reportIntervalSeconds"',
    '"trackedFields"',
    '"memoryGiB"',
    '"extractionCommand"',
    '"scalesAndUnitsInspected"',
    '"coarse": (MUTED, "3,4", "N=512, NS=1000", 44)',
    '"medium": (GOLD, "9,5", "N=1024, NS=2000", 16)',
    '"fine": (BLUE, None, "N=2048, NS=4000", -14)',
    "+ label_offset",
  ]) assert.ok(generator.includes(token), token);
  assert.match(environment, /full\s+exact trigonometric potential/i);
  assert.match(environment, /no randomness/i);
  assert.match(requirements, /^numpy==2\.3\.5$/m);
  assert.match(requirements, /^Pillow==12\.3\.0$/m);
  assert.match(requirements, /^reportlab==4\.4\.9$/m);
  assert.match(protocol, /relative-to-finest audit/i);
  assert.match(protocol, /hue alone is insufficient/i);
  assert.match(protocol, /NOT PROOF/);
});


test("R0.72W uses exactly ten source files and no source-stage outputs", async () => {
  const stage = await figureStage();
  const entries = await readdir(resolve(root, figure), { withFileTypes: true });
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  const names = entries.map((entry) => entry.name).sort();
  assert.equal(sourceFiles.length, 10);
  if (stage === "source") {
    assert.deepEqual(names, sourceFiles);
    await assertNoFigureOutputs();
  } else {
    assert.ok(["draft", "formal"].includes(stage), stage);
    assert.deepEqual(names, [...sourceFiles, ...generated].sort());
    await verifyFlatHashLedger(figure);
  }

  const [generator, validator] = await Promise.all([
    text("scripts/generate_r072w_figure.py"),
    text(figure + "/validate.py"),
  ]);
  for (const name of sourceFiles) {
    assert.ok(generator.includes('"' + name + '"'), "generator " + name);
    assert.ok(validator.includes('"' + name + '"'), "validator " + name);
  }
  assert.equal(generator.includes('"figure-contract.md"'), false);
  assert.equal(validator.includes('"figure-contract.md"'), false);
});


test("R0.72W self-test is zero-write in every lifecycle stage", async () => {
  const stage = await figureStage();
  if (stage === "source") await assertNoFigureOutputs();
  const before = stage === "source" ? null : await generatedSnapshot();
  const result = await run(
    python,
    ["scripts/generate_r072w_figure.py", "--self-test"],
    { cwd: root },
  );
  assert.match(
    result.stdout,
    /passed \(729 analytic in-memory rows; no outputs written\)/,
  );
  if (stage === "source") await assertNoFigureOutputs();
  else assert.deepEqual(await generatedSnapshot(), before);
});


test("R0.72W source enforces certificate lineage and no overwrite", async () => {
  const generator = await text("scripts/generate_r072w_figure.py");
  for (const token of [
    "formal R0.72W certificate is absent",
    "formal figure generation requires a completely clean tree",
    "certificateCommit must be distinct from the frozen sourceCommit",
    "certificateCommit does not descend from sourceCommit",
    "refusing to overwrite pre-existing figure outputs",
    "formal figure generation requires --visual-inspected",
    "working certificate differs from",
    "public/assets/r072w",
  ]) assert.ok(generator.includes(token), token);
});


test("R0.72W strict validator is fail-closed until a formal package exists", async () => {
  const stage = await figureStage();
  if (stage === "source") {
    await assertNoFigureOutputs();
    await assert.rejects(run(
      python,
      [figure + "/validate.py", "--require-formal"],
      { cwd: root },
    ));
    const certificateManifest = await maybeJson(
      "research/certificates/r072w/manifest.json",
    );
    if (certificateManifest?.status !== "formal") {
      await assert.rejects(run(
        python,
        ["scripts/generate_r072w_figure.py", "--draft"],
        { cwd: root },
      ));
    }
    await assertNoFigureOutputs();
    return;
  }

  await verifyFlatHashLedger(figure);
  if (stage === "draft") {
    await assertNoPublicOutputs();
    await assert.rejects(run(
      python,
      [figure + "/validate.py", "--require-formal"],
      { cwd: root },
    ));
    return;
  }

  assert.equal(stage, "formal");
  const [manifest, results, validation] = await Promise.all([
    json(figure + "/manifest.json"),
    json(figure + "/results.json"),
    json(figure + "/validation.json"),
  ]);
  assert.equal(manifest.figureId, figureId);
  assert.equal(manifest.release, "R0.72W");
  assert.equal(manifest.qa.visualInspectionExplicit, true);
  assert.equal(manifest.qa.scalesAndUnitsInspected, true);
  assert.equal(manifest.computation.kind, "simulation");
  assert.ok(manifest.computation.configuration);
  assert.ok(manifest.computation.formalCommand);
  assert.ok(manifest.computation.monitoring.reportIntervalSeconds > 0);
  assert.ok(manifest.computation.monitoring.trackedFields.length > 0);
  assert.ok(manifest.compute.memoryGiB > 0);
  assert.ok(manifest.sourceData.every((record) => record.extractionCommand));
  assert.ok(manifest.data.some((record) => record.path === "progress.ndjson"));
  assert.ok(manifest.data.some((record) => record.path === "resource-log.ndjson"));
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.notEqual(manifest.git.sourceCommit, manifest.git.certificateCommit);
  assert.equal(results.pdeSimulation, true);
  assert.equal(results.diagnosticOnly, true);
  assert.equal(results.randomSeed, null);
  assert.equal(validation.rowCount, 744);
  assert.equal(validation.checks.numericalRowCount, true);
  await run(
    python,
    [figure + "/validate.py", "--require-formal"],
    { cwd: root },
  );
  for (const extension of ["pdf", "svg", "png"]) {
    assert.deepEqual(
      await readFile(resolve(root, figure, "figure." + extension)),
      await readFile(resolve(
        root,
        "public/assets/r072w",
        figureId + "." + extension,
      )),
    );
  }
});
