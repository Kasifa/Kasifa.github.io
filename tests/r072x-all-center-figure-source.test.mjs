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
const figure = "figures/r072x-all-center/fig-r072x-all-center-transfer";
const figureId = "fig-r072x-all-center-transfer";
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
const generatedFiles = [
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
      .map((entry) => entry.name)
      .sort(),
  );
}


test("R0.72X source contract pins the full exact all-center diagnostic", async () => {
  const [config, contract, caption, readme, report, generator, validator] = await Promise.all([
    json(figure + "/config.json"),
    json(figure + "/contract.json"),
    text(figure + "/caption.md"),
    text(figure + "/README.md"),
    text("research/r072x_report-source.md"),
    text("scripts/generate_r072x_figure.py"),
    text(figure + "/validate.py"),
  ]);
  assert.equal(config.figureId, figureId);
  assert.deepEqual(
    {
      width: config.widthMillimetres,
      height: config.heightMillimetres,
      dpi: config.pngDpi,
    },
    { width: 178, height: 150, dpi: 600 },
  );
  assert.equal(config.panelA.physicalCenters.length, 10);
  assert.ok(Math.abs(config.panelA.physicalCenters[0] + Math.log(2)) < 1e-15);
  assert.ok(Math.abs(config.panelA.physicalCenters.at(-1) - (1 - Math.log(2))) < 1e-15);
  assert.ok(config.panelA.physicalCenters.includes(0));
  assert.deepEqual(config.panelA.alphas, [1, 0.75, 0.5, 0.35, 0.25]);
  assert.deepEqual(config.panelA.levels, [
    { label: "coarse", spatialModes: 256, timeSteps: 400 },
    { label: "medium", spatialModes: 512, timeSteps: 800 },
    { label: "fine", spatialModes: 1024, timeSteps: 1600 },
  ]);
  assert.deepEqual(config.panelA.lanczosRitzPolicy, {
    minDimension: 8,
    maxDimension: 32,
    checkEvery: 4,
    relativeResidualTolerance: 1e-10,
    reorthogonalizationPasses: 2,
  });
  assert.deepEqual(config.panelB.qaThresholds, {
    maxRelativeToFine: 0.0005,
    maxAdjointDefect: 1e-10,
    maxRitzResidual: 1e-8,
    maxRayleighNormDefect: 1e-10,
  });
  assert.match(config.panelB.aggregation, /global maxima over the full alpha-center-resolution scan/);
  assert.equal(config.panelA.workers, 4);
  assert.equal(config.panelA.randomSeed, null);
  assert.equal(config.panelA.diagnosticOnly, true);
  assert.equal(config.panelC.expectedPowers.pre, 1);
  assert.equal(config.panelC.expectedPowers.post, 2);
  assert.equal(config.panelC.guidesAreFits, false);
  assert.equal(config.panelD.qEvaluatedNumerically, false);
  assert.equal(contract.stage, "source-only");
  assert.equal(contract.numericalDiagnosticPlanned, true);
  assert.equal(contract.simulationPerformedAtSourceStage, false);
  for (const key of [
    "allCenterExactFamilyGraphCoercivityProvedInBoundReport",
    "allStartExactPathSemigroupProvedInBoundReport",
    "fixedMarginA1EnhancedDissipationImportedInBoundReport",
    "exactA2PathBlochUniformProvedInBoundReport",
    "periodicRepresentativeBetaZeroExactA1A2A1ConcatenationProvedInBoundReport",
    "shrinkingInterfaceFixedShapeA1HypothesesFalseInBoundReport",
  ]) assert.equal(contract.claimBoundary[key], true, key);
  for (const key of [
    "numericalDiagnosticIsProof",
    "numericalDiagnosticEvaluatesAnalyticQ",
    "numericalDiagnosticIsInfiniteDimensionalOperatorNorm",
    "forcedHMinusOneTransferProved",
    "completeLinearizedShearSubsystemProved",
    "a1A2A1ConcatenationBlochUniform",
    "allPhysicalRowsUniformContraction",
    "nonlinearNavierStokesClosureProved",
    "clayMillenniumProblemSolved",
  ]) assert.equal(contract.claimBoundary[key], false, key);
  assert.equal(Object.keys(contract.claimBoundary).length, 15);
  assert.match(caption, /numerical diagnostics only/i);
  assert.match(caption, /periodic\s+representative\s+\\\(\\beta=0\\\)/i);
  assert.match(caption, /not uniformly over Bloch twists/i);
  assert.match(caption, /remain open/i);
  assert.match(
    caption,
    /one fixed deterministic seed[\s\S]*does not independently certify the global largest singular value/,
  );
  assert.match(
    readme,
    /single fixed seed[\s\S]*not that the seed saw the top eigenspace/,
  );
  assert.match(
    readme,
    /Krylov breakdown before dimension 8[\s\S]*rejected\s+conservatively/,
  );
  assert.match(
    report,
    /one fixed deterministic starting vector[\s\S]*seed orthogonal to the top\s+eigenspace/,
  );
  assert.match(
    report,
    /Krylov breakdown before dimension 8[\s\S]*rejected conservatively/,
  );
  for (const token of [
    "PHYSICAL_CENTERS = (",
    "DIAGNOSTIC_ALPHAS = (1.0, 0.75, 0.5, 0.35, 0.25)",
    '("coarse", 256, 400)',
    '("medium", 512, 800)',
    '("fine", 1024, 1600)',
    "LANCZOS_RITZ_POLICY = {",
    '"minDimension": 8',
    '"maxDimension": 32',
    '"checkEvery": 4',
    '"relativeResidualTolerance": 1.0e-10',
    '"reorthogonalizationPasses": 2',
    'CONFIG = PACKAGE / "config.json"',
    "WORKERS = 4",
    "ProcessPoolExecutor",
    "multiprocessing.get_context(\"spawn\")",
    "np.complex128",
    "np.fft.fft",
    "np.fft.ifft",
    "def _lanczos_ritz_largest(",
    "for _ in range(passes)",
    "for basis_vector in basis",
    "actual_image = apply_normal(ritz_vector)",
    "actual_image - ritz_value * ritz_vector",
    "def _direct_norm_audit(",
    "direct_norm = float(np.linalg.norm(transformed))",
    '"rayleighNormDefect"',
    '"allNumericalRowsFinite"',
    '"fineRelativeToFineExactlyZero"',
    "failed relativeResidualTolerance by maxDimension",
    "def _policy_self_test(",
    "policy_result = _policy_self_test()",
    "DIAGNOSTIC_LIMITATIONS = [",
    'result["earlyBreakdownRejected"] = early_breakdown_rejected',
    "full exact shifted V_alpha",
    "deterministic numerical diagnostic only; not proof",
    '"kind": "simulation"',
    '"monitoring"',
    '"reportIntervalSeconds"',
    '"trackedFields"',
    '"memoryGiB"',
    '"extractionCommand"',
    '"scalesAndUnitsInspected"',
  ]) assert.ok(generator.includes(token), token);
  for (const token of [
    "EXPECTED_LANCZOS_RITZ_POLICY = {",
    "EXPECTED_QA_THRESHOLDS = {",
    "EXPECTED_CLAIM_BOUNDARY = {",
    "EXPECTED_DIAGNOSTIC_LIMITATIONS = [",
    'manifest.get("claimBoundary") != EXPECTED_CLAIM_BOUNDARY',
    'manifest.get("diagnosticLimitations") != EXPECTED_DIAGNOSTIC_LIMITATIONS',
    'int(row["krylovDimension"])',
    'float(row["ritzResidual"])',
    'float(row["rayleighNormDefect"])',
    'finite_fields = (',
    'math.isfinite(value)',
    'row["series"] == "fine" and float(row["relativeToFine"]) != 0.0',
    'row Krylov dimension violates the exact range or stride',
    'row actual Ritz residual exceeds the stopping tolerance',
    'validation.get("qaThresholds") != EXPECTED_QA_THRESHOLDS',
  ]) assert.ok(validator.includes(token), token);
});


test("R0.72X legacy top-three slow spectral clusters pass the exact Lanczos-Ritz policy", async () => {
  const result = await run(
    python,
    ["scripts/generate_r072x_figure.py", "--calibration-test"],
    { cwd: root, maxBuffer: 1024 * 1024 },
  );
  const calibration = JSON.parse(result.stdout);
  assert.equal(calibration.status, "passed");
  assert.equal(calibration.outputsWritten, false);
  assert.deepEqual(calibration.policy, {
    minDimension: 8,
    maxDimension: 32,
    checkEvery: 4,
    relativeResidualTolerance: 1e-10,
    reorthogonalizationPasses: 2,
  });
  assert.equal(calibration.records.length, 3);
  assert.deepEqual(
    calibration.records.map((row) => [row.alpha, row.physicalCenter]),
    [
      [0.35, -0.25],
      [0.25, -0.125],
      [0.5, -0.5],
    ],
  );
  for (const row of calibration.records) {
    assert.ok(row.krylovDimension >= 8 && row.krylovDimension <= 32);
    assert.equal((row.krylovDimension - 8) % 4, 0);
    assert.ok(row.ritzResidual <= 1e-10);
    assert.ok(row.rayleighNormDefect <= 1e-10);
    for (const field of [
      "normEstimate", "ritzResidual", "rayleighNormDefect", "adjointDefect",
    ]) assert.equal(Number.isFinite(row[field]), true, field);
  }
});


test("R0.72X package has one canonical figure identity and exact lifecycle inventory", async () => {
  const currentStage = await stage();
  const entries = await readdir(resolve(root, figure), { withFileTypes: true });
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  const names = entries.map((entry) => entry.name).sort();
  if (currentStage === "source") {
    assert.deepEqual(names, sourceFiles);
    for (const name of generatedFiles) await absent(figure + "/" + name);
  } else {
    assert.ok(["draft", "formal"].includes(currentStage));
    assert.deepEqual(names, [...sourceFiles, ...generatedFiles].sort());
    await verifyHashLedger();
  }
  const allPaths = await run("rg", [
    "--files",
    "figures/r072x-all-center",
  ], { cwd: root });
  assert.doesNotMatch(allPaths.stdout, /all-center-path-transfer/);
  assert.equal((await text("scripts/generate_r072x_figure.py")).includes("all-center-path-transfer"), false);
});


test("R0.72X self-test is zero-write at every lifecycle stage", async () => {
  const currentStage = await stage();
  const before = currentStage === "source"
    ? null
    : Object.fromEntries(await Promise.all(generatedFiles.map(async (name) => [
      name,
      await sha(figure + "/" + name),
    ])));
  const result = await run(
    python,
    ["scripts/generate_r072x_figure.py", "--self-test"],
    { cwd: root },
  );
  assert.match(result.stdout, /passed \(20 exact in-memory rows; no outputs written\)/);
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


test("R0.72X formal validator is fail-closed until the package is sealed", async () => {
  const currentStage = await stage();
  if (currentStage === "source") {
    await assert.rejects(run(
      python,
      [figure + "/validate.py", "--require-formal"],
      { cwd: root },
    ));
    return;
  }
  await verifyHashLedger();
  if (currentStage === "draft") {
    await assert.rejects(run(
      python,
      [figure + "/validate.py", "--require-formal"],
      { cwd: root },
    ));
    return;
  }
  const [manifest, results, validation, config, data] = await Promise.all([
    json(figure + "/manifest.json"),
    json(figure + "/results.json"),
    json(figure + "/validation.json"),
    json(figure + "/config.json"),
    text(figure + "/data.csv"),
  ]);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.release, "R0.72X");
  assert.equal(manifest.simulation.kind, "simulation");
  assert.equal(manifest.simulation.diagnosticOnly, true);
  assert.equal(manifest.simulation.randomSeed, null);
  assert.deepEqual(manifest.simulation.lanczosRitzPolicy, {
    minDimension: 8,
    maxDimension: 32,
    checkEvery: 4,
    relativeResidualTolerance: 1e-10,
    reorthogonalizationPasses: 2,
  });
  assert.equal(manifest.simulation.physicalCenters.length, 10);
  assert.equal(manifest.simulation.alphas.length, 5);
  assert.equal(manifest.simulation.levels.length, 3);
  assert.equal(manifest.compute.processes, 4);
  assert.equal(manifest.compute.threadsPerProcess, 1);
  assert.ok(manifest.compute.memoryGiB > 0);
  assert.ok(manifest.simulation.monitoring.reportIntervalSeconds > 0);
  assert.ok(manifest.simulation.monitoring.trackedFields.length > 0);
  assert.equal(manifest.qa.visualInspectionExplicit, true);
  assert.equal(manifest.qa.scalesAndUnitsInspected, true);
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.equal(results.pdeSimulation, true);
  assert.equal(results.diagnosticOnly, true);
  assert.equal(results.randomSeed, null);
  assert.ok(results.claimsNotMade.some((value) =>
    value.includes("single fixed seed")
    && value.includes("global largest singular value")
  ));
  assert.deepEqual(manifest.diagnosticLimitations, [
    "single fixed seed and a small actual Ritz residual do not certify the global largest singular value of the finite propagator",
    "Krylov breakdown before dimension 8 is conservatively rejected even if it could be a happy exact closure",
  ]);
  assert.equal(validation.rowCount, 170);
  assert.equal(validation.checks.centerRangeCovered, true);
  assert.equal(validation.checks.resolutionAuditWithinThreshold, true);
  assert.equal(validation.checks.adjointAuditWithinThreshold, true);
  assert.equal(validation.checks.ritzAuditWithinThreshold, true);
  assert.equal(validation.checks.rayleighNormAuditWithinThreshold, true);
  assert.equal(validation.checks.allNumericalRowsFinite, true);
  assert.equal(validation.checks.fineRelativeToFineExactlyZero, true);
  assert.equal(validation.checks.ritzStoppingToleranceMet, true);
  assert.equal(validation.checks.krylovDimensionsFollowPolicy, true);
  assert.deepEqual(validation.qaThresholds, config.panelB.qaThresholds);
  assert.ok(results.numericalSummary.maxRelativeToFine <= 0.0005);
  assert.ok(results.numericalSummary.maxAdjointDefect <= 1e-10);
  assert.ok(results.numericalSummary.maxRitzResidual <= 1e-10);
  assert.ok(results.numericalSummary.maxRayleighNormDefect <= 1e-10);
  assert.ok(results.numericalSummary.minKrylovDimension >= 8);
  assert.ok(results.numericalSummary.maxKrylovDimension <= 32);
  const csvLines = data.trimEnd().split("\n");
  const csvHeader = csvLines[0].split(",");
  const numericalRows = csvLines.slice(1)
    .filter((row) => row.includes("full-exact-block-forward-adjoint-norm"));
  assert.equal(numericalRows.length, 150);
  assert.ok(numericalRows.every((row) => {
    const fields = row.split(",");
    const value = (name) => Number(fields[csvHeader.indexOf(name)]);
    const dimension = value("krylovDimension");
    const residual = value("ritzResidual");
    return dimension >= 8 && dimension <= 32
      && (dimension - 8) % 4 === 0
      && residual <= 1e-10
      && [
        "normEstimate", "ritzResidual", "rayleighNormDefect",
        "adjointDefect", "relativeToFine",
      ].every((name) => Number.isFinite(value(name)))
      && (fields[csvHeader.indexOf("series")] !== "fine"
        || value("relativeToFine") === 0);
  }));
  const validatorResult = await run(
    python,
    [figure + "/validate.py", "--require-formal"],
    { cwd: root },
  );
  const validatorSummary = JSON.parse(validatorResult.stdout);
  assert.equal(
    validatorSummary.maxRelativeToFine,
    validation.numericalSummary.maxRelativeToFine,
  );
  assert.equal(
    validatorSummary.maxRelativeToFine,
    results.numericalSummary.maxRelativeToFine,
  );
  assert.notEqual(
    validatorSummary.maxRelativeToFine,
    manifest.simulation.monitoring.reportIntervalSeconds,
  );
  await run(
    python,
    ["research/validate_figure_package.py", figure],
    { cwd: root },
  );
  for (const extension of ["pdf", "svg", "png"]) {
    assert.deepEqual(
      await readFile(resolve(root, figure, "figure." + extension)),
      await readFile(resolve(root, "public/assets/r072x", figureId + "." + extension)),
    );
  }
});
