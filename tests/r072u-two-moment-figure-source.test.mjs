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
const figure = "figures/r072u-local-observability/fig-r072u-two-moment-coercivity";
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
  return createHash("sha256").update(await readFile(resolve(root, relative))).digest("hex");
}


async function figureStage() {
  return (await maybeJson(`${figure}/manifest.json`))?.status || "source";
}


async function generatedSnapshot() {
  return Object.fromEntries(await Promise.all(generated.map(async (name) => [
    name,
    await sha(`${figure}/${name}`),
  ])));
}


async function verifyFlatHashLedger(relative) {
  const directory = resolve(root, relative);
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
    const [, expected, name] = match;
    assert.equal(await sha(`${relative}/${name}`), expected, name);
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries.filter((entry) => entry.isFile() && entry.name !== "SHA256SUMS")
      .map((entry) => entry.name).sort(),
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
    await absent(`public/assets/r072u/fig-r072u-two-moment-coercivity.${extension}`);
  }
}


async function assertNoFigureOutputs() {
  for (const name of generated) await absent(`${figure}/${name}`);
  await assertNoPublicOutputs();
}


test("R0.72U figure source contract pins the exact three-panel content", async () => {
  const [config, contract, caption, figureContract] = await Promise.all([
    json(`${figure}/config.json`),
    json(`${figure}/contract.json`),
    text(`${figure}/caption.md`),
    text(`${figure}/figure-contract.md`),
  ]);
  assert.equal(config.figureId, "fig-r072u-two-moment-coercivity");
  assert.deepEqual(
    { width: config.widthMillimetres, height: config.heightMillimetres, dpi: config.pngDpi },
    { width: 178, height: 76, dpi: 600 },
  );
  assert.equal(config.panelA.formula, "rho(X)=(315/256)*(1-X^2)^4*1_{[-1,1]}(X)");
  assert.deepEqual(config.panelA.moments, { mu2: "1/11", mu4: "3/143" });
  assert.equal(config.panelB.coefficient, "K_c(s)=3/143+6*(c+s)/11");
  assert.equal(config.panelB.sufficientThreshold, "27/13");
  assert.equal(config.panelC.floor, "4/5");
  assert.equal(config.pdeSimulation, false);
  assert.equal(contract.stage, "source-only");
  assert.equal(contract.plannedPublicationDirectory, "public/assets/r072u");
  assert.deepEqual(contract.requiredFormats, ["svg", "pdf", "png-600dpi"]);
  assert.equal(contract.claimBoundary.wholeLineBlockContractionProved, false);
  assert.match(caption, /81\/143/);
  assert.match(caption, /4\/5/);
  assert.match(caption, /different statements/i);
  assert.match(figureContract, /whole-line block contraction: OPEN/);
});


test("R0.72U figure uses two chromatic roots and redundant non-colour encodings", async () => {
  const [contract, generator, protocol] = await Promise.all([
    json(`${figure}/contract.json`),
    text("scripts/generate_r072u_figure.py"),
    text(`${figure}/qa-protocol.md`),
  ]);
  assert.equal(contract.palette.hardChromaticRootCap, 2);
  assert.deepEqual(contract.palette.chromaticRoots, ["#285f8f", "#a6781f"]);
  assert.deepEqual(contract.researchBlossom, {
    carriesData: false,
    lockedAnchor: "top-right-header",
    petalCount: 5,
  });
  for (const token of [
    'BLUE = "#285f8f"',
    'GOLD = "#a6781f"',
    "Locked five-petal research blossom",
    '"8,5"',
    '"3,4"',
    '"-81/143"',
    "whole-line block contraction: OPEN",
  ]) assert.ok(generator.includes(token), token);
  for (const forbidden of ["#a9413a", "#2d7563"]) {
    assert.equal(generator.includes(forbidden), false, forbidden);
  }
  assert.match(protocol, /no semantic distinction relies on hue/i);
  assert.match(protocol, /five-petal research blossom/i);
});


test("R0.72U package has the complete source set in every lifecycle stage", async () => {
  const stage = await figureStage();
  const entries = (await readdir(resolve(root, figure), { withFileTypes: true }));
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  const names = entries.map((entry) => entry.name).sort();
  for (const name of sourceFiles) assert.ok(names.includes(name), name);
  if (stage === "source") {
    assert.deepEqual(names, sourceFiles);
    await assertNoFigureOutputs();
  } else {
    assert.ok(["draft", "formal"].includes(stage), stage);
    for (const name of generated) assert.ok(names.includes(name), name);
    await verifyFlatHashLedger(figure);
  }
});


test("R0.72U figure self-test builds in memory and never mutates its lifecycle stage", async () => {
  const stage = await figureStage();
  if (stage === "source") await assertNoFigureOutputs();
  const before = stage === "source" ? null : await generatedSnapshot();
  const result = await run(python, [
    "scripts/generate_r072u_figure.py", "--self-test",
  ], { cwd: root });
  assert.match(result.stdout, /passed \(2406 in-memory rows; no outputs written\)/);
  if (stage === "source") await assertNoFigureOutputs();
  else assert.deepEqual(await generatedSnapshot(), before);
});


test("R0.72U strict figure validator is fail-closed until formal and exhaustive afterward", async () => {
  const stage = await figureStage();
  if (stage === "source") {
    await assertNoFigureOutputs();
    await assert.rejects(run(python, [
      `${figure}/validate.py`, "--require-formal",
    ], { cwd: root }));
    await assertNoFigureOutputs();
    return;
  }
  await verifyFlatHashLedger(figure);
  if (stage === "draft") {
    await assertNoPublicOutputs();
    await assert.rejects(run(python, [
      `${figure}/validate.py`, "--require-formal",
    ], { cwd: root }));
    await run(python, ["research/validate_figure_package.py", figure], { cwd: root });
    return;
  }
  assert.equal(stage, "formal");
  const manifest = await json(`${figure}/manifest.json`);
  assert.equal(manifest.figureId, "fig-r072u-two-moment-coercivity");
  assert.equal(manifest.release, "R0.72U");
  assert.equal(manifest.qa.visualInspectionExplicit, true);
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.equal(manifest.publication.directory, "public/assets/r072u");
  await run(python, [
    `${figure}/validate.py`, "--require-formal",
  ], { cwd: root });
  for (const extension of ["pdf", "svg", "png"]) {
    const master = await readFile(resolve(root, figure, `figure.${extension}`));
    const published = await readFile(resolve(
      root, `public/assets/r072u/fig-r072u-two-moment-coercivity.${extension}`,
    ));
    assert.equal(Buffer.compare(master, published), 0, extension);
  }
});
