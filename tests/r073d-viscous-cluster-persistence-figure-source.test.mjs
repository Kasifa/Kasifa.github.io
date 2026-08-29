import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const figureRelative =
  "figures/r073d/fig-r073d-viscous-cluster-persistence";
const figureDirectory = resolve(root, figureRelative);
const figureId = "fig-r073d-viscous-cluster-persistence";
const sourceCommit = "7c94b136601264c35667084fbcaad627ad40fb59";
const certificateCommit = "6e4a8bd8aca404fc1d0eff050fe4e0809117072d";
const certificateRelative = "research/certificates/r073d/certificate.json";
const experimentRelative = "experiments/r073d/viscous_cluster_diagnostic.json";

const boundary = {
  clayProblemSolved: false,
  explicitContourRadius: false,
  finiteCurvesAreContinuumProof: false,
  fixedClusterRieszProjectionNormConvergence: true,
  inviscidEigenvalueSimple: false,
  logFastTimeTransfer: false,
  nonlinearNavierStokes: false,
  staticVanishingViscosityPersistence: true,
};

const text = (name) => readFile(resolve(figureDirectory, name), "utf8");
const json = async (name) => JSON.parse(await text(name));
const shaBuffer = (value) => createHash("sha256").update(value).digest("hex");
const shaFile = async (path) => shaBuffer(await readFile(path));

function git(args, label) {
  const result = spawnSync("git", args, {
    cwd: root,
    encoding: null,
    maxBuffer: 16 * 1024 * 1024,
  });
  assert.equal(result.error, undefined, label + ": git process error");
  assert.equal(
    result.status,
    0,
    label + ": " + Buffer.from(result.stderr ?? []).toString("utf8"),
  );
  return Buffer.from(result.stdout ?? []);
}

function pngMetrics(bytes) {
  assert.deepEqual(
    [...bytes.subarray(0, 8)],
    [137, 80, 78, 71, 13, 10, 26, 10],
    "PNG signature",
  );
  const metrics = {
    width: bytes.readUInt32BE(16),
    height: bytes.readUInt32BE(20),
    pixelsPerMetreX: null,
    pixelsPerMetreY: null,
    physicalUnit: null,
  };
  let offset = 8;
  while (offset + 12 <= bytes.length) {
    const length = bytes.readUInt32BE(offset);
    const type = bytes.subarray(offset + 4, offset + 8).toString("ascii");
    const data = offset + 8;
    assert.ok(data + length + 4 <= bytes.length, "truncated PNG chunk " + type);
    if (type === "pHYs") {
      assert.equal(length, 9, "PNG pHYs length");
      metrics.pixelsPerMetreX = bytes.readUInt32BE(data);
      metrics.pixelsPerMetreY = bytes.readUInt32BE(data + 4);
      metrics.physicalUnit = bytes[data + 8];
    }
    offset = data + length + 4;
    if (type === "IEND") break;
  }
  return metrics;
}

function pdfMetrics(bytes) {
  assert.equal(bytes.subarray(0, 5).toString("ascii"), "%PDF-", "PDF header");
  const latin = bytes.toString("latin1");
  const pages = [...latin.matchAll(/\/Type\s*\/Page\b/g)].length;
  const media = latin.match(
    /\/MediaBox\s*\[\s*0(?:\.0+)?\s+0(?:\.0+)?\s+([0-9.]+)\s+([0-9.]+)\s*\]/,
  );
  assert.ok(media, "PDF MediaBox");
  return { pages, points: [Number(media[1]), Number(media[2])] };
}

test("R0.73D figure fixes the four-panel 178 x 132 mm, 600 dpi publication surface", async () => {
  const [config, contract, results, manifest, validation, svg, png, pdf] =
    await Promise.all([
      json("config.json"),
      json("contract.json"),
      json("results.json"),
      json("manifest.json"),
      json("validation.json"),
      text("figure.svg"),
      readFile(resolve(figureDirectory, "figure.png")),
      readFile(resolve(figureDirectory, "figure.pdf")),
    ]);

  assert.equal(config.figureId, figureId);
  assert.equal(contract.figureId, figureId);
  assert.equal(results.figureId, figureId);
  assert.equal(manifest.figureId, figureId);
  assert.equal(contract.release, "R0.73D");
  assert.equal(results.release, "R0.73D");
  assert.equal(manifest.release, "R0.73D");
  assert.equal(manifest.status, "formal");
  assert.deepEqual(
    [config.widthMillimetres, config.heightMillimetres, config.pngDpi],
    [178, 132, 600],
  );
  assert.deepEqual(
    [
      manifest.figure.widthMillimetres,
      manifest.figure.heightMillimetres,
      manifest.figure.pngDpi,
    ],
    [178, 132, 600],
  );
  assert.equal(
    manifest.figure.layout,
    "four-panel operator, finite diagnostic, and boundary figure",
  );

  const panelTitles = [
    ["A", "Exact kinetic-space reduction"],
    ["B", "Finite eigenvalue diagnostic as viscosity vanishes"],
    ["C", "Finite projector diagnostic in the kinetic norm"],
    ["D", "Closed theorem and exact remaining boundary"],
  ];
  for (const [label, title] of panelTitles) {
    assert.equal(
      (svg.match(new RegExp(">" + label + "<\\/text>", "g")) ?? []).length,
      1,
      "one visible panel label " + label,
    );
    assert.ok(svg.includes(">" + title + "</text>"), "panel title " + label);
  }
  assert.equal(svg.includes("<image"), false, "SVG remains vector text");

  const pngInfo = pngMetrics(png);
  assert.deepEqual([pngInfo.width, pngInfo.height], [4204, 3118]);
  assert.equal(pngInfo.physicalUnit, 1, "PNG pHYs uses metres");
  assert.ok(
    Math.abs(pngInfo.pixelsPerMetreX * 0.0254 - 600) < 0.01 &&
      Math.abs(pngInfo.pixelsPerMetreY * 0.0254 - 600) < 0.01,
    JSON.stringify(pngInfo),
  );
  assert.deepEqual(manifest.figure.outputs[2].pixels, [4204, 3118]);
  assert.equal(manifest.figure.outputs[2].dpi, 600);
  assert.deepEqual(validation.pngPixels, [4204, 3118]);

  const pdfInfo = pdfMetrics(pdf);
  assert.equal(pdfInfo.pages, 1);
  assert.deepEqual(pdfInfo.points, [504.5688, 374.1768]);
  assert.deepEqual(validation.pdfPoints, pdfInfo.points);
  assert.ok(
    Math.abs(pdfInfo.points[0] - (178 / 25.4) * 72) < 0.01 &&
      Math.abs(pdfInfo.points[1] - (132 / 25.4) * 72) < 0.01,
    JSON.stringify(pdfInfo),
  );
});

test("R0.73D figure preserves the complete fail-closed theorem boundary and sealed inputs", async () => {
  const [config, contract, results, manifest, validation] = await Promise.all([
    json("config.json"),
    json("contract.json"),
    json("results.json"),
    json("manifest.json"),
    json("validation.json"),
  ]);
  assert.deepEqual(contract.claimBoundary, boundary);
  assert.deepEqual(results.claimBoundary, boundary);
  assert.deepEqual(manifest.claimBoundary, boundary);
  assert.deepEqual(validation.claimBoundary, boundary);
  assert.equal(
    manifest.supportedClaim.includes(
      "simplicity, rates, complement control, fast-time transfer, nonlinear Navier--Stokes control, and Clay remain open",
    ),
    true,
  );

  const expectedInputs = [
    experimentRelative,
    certificateRelative,
  ];
  assert.deepEqual(
    manifest.inputBindings.map((row) => row.path),
    expectedInputs,
  );
  assert.deepEqual(manifest.sourceData, manifest.inputBindings);
  assert.deepEqual(results.inputs, manifest.inputBindings);
  assert.equal(config.experiment, experimentRelative);
  assert.equal(config.certificate, certificateRelative);
  for (const row of manifest.inputBindings) {
    const path = resolve(root, row.path);
    assert.equal(await shaFile(path), row.sha256, row.path);
  }
  assert.deepEqual(
    results.outputs.map((row) => ({ path: row.path, bytes: row.bytes, sha256: row.sha256 })),
    manifest.figure.outputs.map((row) => ({ path: row.path, bytes: row.bytes, sha256: row.sha256 })),
  );

  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.equal(manifest.qa.status, "passed");
  for (const key of [
    "visualInspectionExplicit",
    "finalSizeInspected",
    "grayscaleInspected",
    "labelsAndLegendsInspected",
    "scalesAndUnitsInspected",
    "dataCrossChecked",
  ]) {
    assert.equal(manifest.qa[key], true, key);
  }
});

test("R0.73D figure ledger is flat, sorted, complete, and its public masters are byte-identical", async () => {
  const manifest = await json("manifest.json");
  const rows = (await text("SHA256SUMS")).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, "malformed flat SHA256SUMS row: " + row);
    assert.equal(
      await shaFile(resolve(figureDirectory, match[2])),
      match[1],
      match[2],
    );
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(figureDirectory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()), "figure symlink");
  assert.deepEqual(
    names,
    entries
      .filter((entry) => entry.isFile() && entry.name !== "SHA256SUMS")
      .map((entry) => entry.name)
      .sort(),
    "every ordinary package file appears exactly once",
  );

  assert.equal(manifest.publication.directory, "public/assets/r073d");
  assert.equal(manifest.publication.fileStem, figureId);
  assert.equal(manifest.publication.byteIdentityRequired, true);
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.deepEqual(
    manifest.publication.assets.map((row) => row.path),
    [
      "public/assets/r073d/" + figureId + ".pdf",
      "public/assets/r073d/" + figureId + ".svg",
      "public/assets/r073d/" + figureId + ".png",
    ],
  );
  const outputs = new Map(
    manifest.figure.outputs.map((row) => [row.path.split(".").at(-1), row]),
  );
  for (const published of manifest.publication.assets) {
    const suffix = published.path.split(".").at(-1);
    const master = outputs.get(suffix);
    assert.ok(master, "archival master " + suffix);
    const [masterBytes, publicBytes] = await Promise.all([
      readFile(resolve(figureDirectory, master.path)),
      readFile(resolve(root, published.path)),
    ]);
    assert.equal(Buffer.compare(masterBytes, publicBytes), 0, suffix);
    assert.equal(masterBytes.length, master.bytes, suffix + " master bytes");
    assert.equal(publicBytes.length, published.bytes, suffix + " public bytes");
    assert.equal(shaBuffer(masterBytes), master.sha256, suffix + " master hash");
    assert.equal(shaBuffer(publicBytes), published.sha256, suffix + " public hash");
    assert.equal(master.sha256, published.sha256, suffix + " ledger agreement");
  }
});

test("R0.73D figure binds plot.py and certificate.json to real historical commits", async () => {
  const manifest = await json("manifest.json");
  assert.deepEqual(manifest.git, {
    certificateCommit,
    dirtyAtCertifiedRun: false,
    repository: "Kasifa/Kasifa.github.io",
    sourceCommit,
  });

  for (const [commit, label] of [
    [sourceCommit, "figure source commit"],
    [certificateCommit, "certificate commit"],
  ]) {
    assert.equal(git(["cat-file", "-t", commit], label).toString("utf8").trim(), "commit");
    git(["merge-base", "--is-ancestor", commit, "HEAD"], label + " ancestry");
  }

  const plotRelative = figureRelative + "/plot.py";
  const plotAtCommit = git(["show", sourceCommit + ":" + plotRelative], "sealed plot.py");
  const plotBinding = manifest.files.find((row) => row.path === plotRelative);
  assert.ok(plotBinding, "plot.py manifest binding");
  assert.equal(shaBuffer(plotAtCommit), plotBinding.sha256);
  assert.equal(plotAtCommit.length, plotBinding.bytes);
  assert.equal(await shaFile(resolve(root, plotRelative)), plotBinding.sha256);

  const certificateAtCommit = git(
    ["show", certificateCommit + ":" + certificateRelative],
    "sealed certificate.json",
  );
  const certificateBinding = manifest.inputBindings.find(
    (row) => row.path === certificateRelative,
  );
  assert.ok(certificateBinding, "certificate input binding");
  assert.equal(shaBuffer(certificateAtCommit), certificateBinding.sha256);
  assert.equal(await shaFile(resolve(root, certificateRelative)), certificateBinding.sha256);
});
