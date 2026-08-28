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
  "figures/r072v-whole-line-transfer/"
  + "fig-r072v-unit-chart-globalization"
);
const figureId = "fig-r072v-unit-chart-globalization";
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


async function figureStage() {
  return (await maybeJson(figure + "/manifest.json"))?.status || "source";
}


async function generatedSnapshot() {
  return Object.fromEntries(await Promise.all(generated.map(async (name) => [
    name,
    await sha(figure + "/" + name),
  ])));
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


async function absent(relative) {
  await assert.rejects(
    access(resolve(root, relative)),
    (error) => error?.code === "ENOENT",
    relative,
  );
}


async function assertNoPublicOutputs() {
  for (const extension of ["pdf", "svg", "png"]) {
    await absent(
      "public/assets/r072v/" + figureId + "." + extension,
    );
  }
}


async function assertNoFigureOutputs() {
  for (const name of generated) await absent(figure + "/" + name);
  await assertNoPublicOutputs();
}


test("R0.72V contract pins exact analytic content and boundaries", async () => {
  const [config, contract, caption, figureContract] = await Promise.all([
    json(figure + "/config.json"),
    json(figure + "/contract.json"),
    text(figure + "/caption.md"),
    text(figure + "/figure-contract.md"),
  ]);
  assert.equal(config.figureId, figureId);
  assert.deepEqual(
    {
      width: config.widthMillimetres,
      height: config.heightMillimetres,
      dpi: config.pngDpi,
    },
    { width: 178, height: 82, dpi: 600 },
  );
  assert.equal(
    config.panelA.formula,
    "kappa(theta)=cos(theta)^2*(5/6292)+sin(theta)^2*(1/44)",
  );
  assert.deepEqual(config.panelA.moments, {
    mu2: "1/44",
    mu4: "3/2288",
    varianceY2: "5/6292",
  });
  assert.equal(config.panelA.floor, "5/6292");
  assert.equal(config.panelB.relation, "b=a^2/3+6*c");
  assert.deepEqual(config.panelB.centres, [-2, 0, 2]);
  assert.deepEqual(config.panelB.integerKRange, [-4, 4]);
  assert.equal(config.panelC.ratio, "r=s/(1+s)");
  assert.equal(config.panelC.sDefinition, "s=C_T^2/T");
  assert.equal(config.panelC.symbolicFormulaOnly, true);
  assert.equal(config.pdeSimulation, false);
  assert.equal(contract.stage, "source-only");
  assert.equal(contract.simulationPerformed, false);
  assert.equal(contract.plannedPublicationDirectory, "public/assets/r072v");
  assert.deepEqual(contract.requiredFormats, ["svg", "pdf", "png-600dpi"]);
  assert.equal(
    contract.claimBoundary.analyticWholeLineTheoremProvedInBoundReport,
    true,
  );
  assert.equal(
    contract.claimBoundary.analyticEnergyBlockContractionProvedForDeclaredClass,
    true,
  );
  assert.equal(
    contract.claimBoundary.finiteCertificateMachineChecksFunctionalAnalysis,
    false,
  );
  assert.equal(contract.claimBoundary.periodicTransferProved, false);
  assert.equal(contract.claimBoundary.clayMillenniumProblemSolved, false);
  assert.match(caption, /5\/6292/);
  assert.match(caption, /C_T.*not been numerically evaluated/i);
  assert.match(
    figureContract,
    /whole-line block contraction: CLOSED \(exact cubic energy model\)/,
  );
  assert.match(figureContract, /periodic \/ Clay: OPEN/);
});


test("R0.72V source uses two chromatic roots and redundant encodings", async () => {
  const [contract, generator, protocol] = await Promise.all([
    json(figure + "/contract.json"),
    text("scripts/generate_r072v_figure.py"),
    text(figure + "/qa-protocol.md"),
  ]);
  assert.equal(contract.palette.hardChromaticRootCap, 2);
  assert.deepEqual(
    contract.palette.chromaticRoots,
    ["#285f8f", "#a6781f"],
  );
  assert.deepEqual(contract.researchBlossom, {
    carriesData: false,
    lockedAnchor: "top-right-header",
    petalCount: 5,
  });
  for (const token of [
    'BLUE = "#285f8f"',
    'GOLD = "#a6781f"',
    "Locked five-petal research blossom",
    '"9,5"',
    '"3,4"',
    "markers: exact k in {-4,...,4}",
    "formula only; C_T not evaluated",
    "whole-line block contraction: CLOSED (exact cubic energy model)",
    "periodic / Clay: OPEN",
    "pdeSimulation=false",
  ]) assert.ok(generator.includes(token), token);
  for (const forbidden of ["#a9413a", "#2d7563"]) {
    assert.equal(generator.includes(forbidden), false, forbidden);
  }
  assert.match(protocol, /no semantic distinction may rely only on hue/i);
  assert.match(protocol, /five-petal blossom/i);
});


test("R0.72V package and certificate use exactly eleven source files", async () => {
  const stage = await figureStage();
  const entries = await readdir(resolve(root, figure), {
    withFileTypes: true,
  });
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  const names = entries.map((entry) => entry.name).sort();
  assert.equal(sourceFiles.length, 11);
  for (const name of sourceFiles) assert.ok(names.includes(name), name);
  if (stage === "source") {
    assert.deepEqual(names, sourceFiles);
    await assertNoFigureOutputs();
  } else {
    assert.ok(["draft", "formal"].includes(stage), stage);
    for (const name of generated) assert.ok(names.includes(name), name);
    await verifyFlatHashLedger(figure);
  }

  const [producer, validator] = await Promise.all([
    text("research/certificates/r072v/generate_certificate.py"),
    text("research/certificates/r072v/validate_certificate.py"),
  ]);
  for (const name of sourceFiles) {
    const token = '"' + figure + "/" + name + '"';
    assert.ok(producer.includes(token), "producer binding " + name);
    assert.ok(validator.includes(token), "validator binding " + name);
  }
  for (const pair of [
    ["scripts/generate_r072v_figure.py", producer],
    ["scripts/generate_r072v_figure.py", validator],
    ["tests/r072v-unit-chart-globalization-figure-source.test.mjs", producer],
    ["tests/r072v-unit-chart-globalization-figure-source.test.mjs", validator],
  ]) {
    const [relative, content] = pair;
    assert.ok(content.includes('"' + relative + '"'), relative);
  }
});


test("R0.72V self-test is zero-write in every lifecycle stage", async () => {
  const stage = await figureStage();
  if (stage === "source") await assertNoFigureOutputs();
  const before = stage === "source" ? null : await generatedSnapshot();
  const result = await run(
    python,
    ["scripts/generate_r072v_figure.py", "--self-test"],
    { cwd: root },
  );
  assert.match(
    result.stdout,
    /passed \(2592 in-memory rows; no outputs written\)/,
  );
  if (stage === "source") await assertNoFigureOutputs();
  else assert.deepEqual(await generatedSnapshot(), before);
});


test("R0.72V generator enforces lineage and no overwrite", async () => {
  const generator = await text("scripts/generate_r072v_figure.py");
  for (const token of [
    "formal figure generation requires a completely clean tree",
    "certificateCommit must be distinct from the frozen sourceCommit",
    "certificateCommit does not descend from sourceCommit",
    "refusing to overwrite pre-existing figure outputs",
    "formal figure generation requires --visual-inspected",
    "working certificate differs from",
    "public/assets/r072v",
  ]) assert.ok(generator.includes(token), token);
});


test("R0.72V strict validator is fail-closed until formal", async () => {
  const stage = await figureStage();
  if (stage === "source") {
    await assertNoFigureOutputs();
    await assert.rejects(run(
      python,
      [figure + "/validate.py", "--require-formal"],
      { cwd: root },
    ));
    await assert.rejects(run(
      python,
      ["scripts/generate_r072v_figure.py", "--draft"],
      { cwd: root },
    ));
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
    await run(
      python,
      ["research/validate_figure_package.py", figure],
      { cwd: root },
    );
    return;
  }

  assert.equal(stage, "formal");
  const [manifest, results] = await Promise.all([
    json(figure + "/manifest.json"),
    json(figure + "/results.json"),
  ]);
  assert.equal(manifest.figureId, figureId);
  assert.equal(manifest.release, "R0.72V");
  assert.equal(manifest.qa.visualInspectionExplicit, true);
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.equal(manifest.publication.directory, "public/assets/r072v");
  assert.notEqual(manifest.git.sourceCommit, manifest.git.certificateCommit);
  assert.equal(results.pdeSimulation, false);
  assert.equal(results.presentationOnly, true);
  await run(
    python,
    [figure + "/validate.py", "--require-formal"],
    { cwd: root },
  );
  for (const extension of ["pdf", "svg", "png"]) {
    const master = await readFile(
      resolve(root, figure, "figure." + extension),
    );
    const published = await readFile(
      resolve(root, "public/assets/r072v/" + figureId + "." + extension),
    );
    assert.equal(Buffer.compare(master, published), 0, extension);
  }
});
