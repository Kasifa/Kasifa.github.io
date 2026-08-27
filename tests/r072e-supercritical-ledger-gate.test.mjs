import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readdir, readFile, stat } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

import {
  containsChinese,
  extractProtectedTokens,
  extractTranslatableStrings,
} from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certRoot = resolve(root, "research/certificates/r072e");
const figureRoot = resolve(
  root,
  "figures/r072e-supercritical-ledger/fig-r072e-supercritical-ledger",
);
const publicRoot = resolve(root, "public");
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));
const sha256 = async (path) =>
  createHash("sha256").update(await readFile(path)).digest("hex");
const near = (actual, expected, tolerance, label) =>
  assert.ok(
    Math.abs(Number(actual) - expected) <= tolerance,
    `${label}: ${actual} versus ${expected}`,
  );

async function verifyHashes(directory, expectedRows) {
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trim()
    .split("\n");
  assert.equal(rows.length, expectedRows);
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/]+)$/);
    assert.ok(match, row);
    names.push(match[2]);
    assert.equal(
      await sha256(resolve(directory, match[2])),
      match[1],
      match[2],
    );
  }
  assert.equal(new Set(names).size, names.length);
  return names;
}

async function readNdjson(path) {
  const lines = (await readFile(path, "utf8"))
    .trim()
    .split("\n")
    .filter(Boolean);
  assert.ok(lines.length > 1, path);
  return lines.map((line) => JSON.parse(line));
}

function pngMetadata(buffer) {
  const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  assert.ok(buffer.subarray(0, 8).equals(signature));
  let offset = 8;
  const result = {};
  while (offset + 12 <= buffer.length) {
    const length = buffer.readUInt32BE(offset);
    const type = buffer.subarray(offset + 4, offset + 8).toString("ascii");
    const start = offset + 8;
    const end = start + length;
    assert.ok(end + 4 <= buffer.length, type);
    if (type === "IHDR") {
      result.width = buffer.readUInt32BE(start);
      result.height = buffer.readUInt32BE(start + 4);
    }
    if (type === "pHYs") {
      result.dpiX = buffer.readUInt32BE(start) * 0.0254;
      result.dpiY = buffer.readUInt32BE(start + 4) * 0.0254;
      assert.equal(buffer[start + 8], 1);
    }
    offset = end + 4;
    if (type === "IEND") break;
  }
  return result;
}

function parseCompiledTranslations(source) {
  const prefix = "globalThis.NS_EN_TRANSLATIONS = Object.freeze(";
  assert.ok(source.startsWith(prefix));
  assert.ok(source.trimEnd().endsWith(");"));
  return JSON.parse(source.trim().slice(prefix.length, -2));
}

test("certifies the fixed-q0 R0.72E ledger through two independent paths", async () => {
  const [
    producer,
    independent,
    config,
    producerScript,
    independentScript,
    producerProgress,
    producerResource,
    independentProgress,
    independentResource,
  ] = await Promise.all([
    readJson(resolve(certRoot, "result.json")),
    readJson(resolve(certRoot, "independent-result.json")),
    readJson(resolve(certRoot, "config.json")),
    readFile(resolve(root, "research/r072e_exact_audit.py"), "utf8"),
    readFile(resolve(root, "research/r072e_independent_audit.py"), "utf8"),
    readNdjson(resolve(certRoot, "producer-progress.ndjson")),
    readNdjson(resolve(certRoot, "producer-resource.ndjson")),
    readNdjson(resolve(certRoot, "independent-progress.ndjson")),
    readNdjson(resolve(certRoot, "independent-resource.ndjson")),
  ]);

  assert.equal(producer.auditId, "R0.72E-exact-producer-audit");
  assert.equal(producer.schemaVersion, 1);
  assert.equal(producer.status, "passed");
  assert.equal(producer.allRequiredChecksPassed, true);
  assert.equal(producer.defaultGridComplete, true);
  assert.equal(Object.keys(producer.checks).length, 16);
  assert.ok(Object.values(producer.checks).every((row) => row.passed));
  assert.equal(producer.inputPolicy.certificateInputsRead, false);
  assert.equal(producer.inputPolicy.externalResearchInputsRead, false);
  assert.equal(producer.rawParameters.q0, 4);
  assert.equal(producer.configuration.q0, 4);
  assert.deepEqual(producer.configuration.besselCounts, [8, 16, 32, 64]);
  assert.deepEqual(producer.configuration.deltas, [16, 32, 64, 128, 256, 512]);
  assert.equal(producer.configuration.fourierModes, 512);
  assert.equal(producer.configuration.xMax, 6);
  assert.equal(producer.configuration.phaseStep, 0.06);
  assert.equal(producer.configuration.maxStep, 0.01);
  assert.equal(producer.checks.defaultBesselGrid.passed, true);
  assert.equal(producer.checks.defaultDeltaGrid.passed, true);

  assert.equal(independent.release, "R0.72E");
  assert.equal(independent.schemaVersion, "r072e-independent-audit-v1");
  assert.equal(independent.smokeMode, false);
  assert.equal(independent.allPassed, true);
  assert.equal(independent.checks.length, 16);
  assert.ok(independent.checks.every((row) => row.passed));
  assert.equal(independent.algorithm.importsProducer, false);
  assert.equal(independent.algorithm.readsProducerOutput, false);
  assert.match(independent.algorithm.rootIntegrator, /fixed-step classical RK4/);
  assert.match(independent.algorithm.actionIntegrator, /BDF/);
  assert.match(independent.algorithm.actionIntegrator, /sparse tridiagonal/);
  assert.equal(independent.configuration.q0, 4);
  assert.equal(independent.configuration.mu, 1 / 16);
  assert.deepEqual(independent.configuration.RValues, [8, 16, 32, 64]);
  assert.deepEqual(independent.configuration.actionDeltas, [16, 32, 64, 128]);
  assert.equal(independent.configuration.rootStep, 0.004);
  assert.equal(independent.configuration.actionFinalX, 1);
  assert.equal(independent.configuration.actionRadius, 64);
  assert.equal(independent.configuration.actionCheckRadius, 88);
  assert.equal(independent.configuration.actionRtol, 2e-9);
  assert.equal(independent.configuration.actionAtol, 2e-11);
  assert.equal(independent.scope.intervalArithmetic, false);
  assert.equal(independent.scope.provesInfiniteLattice, false);
  assert.equal(independent.scope.provesMalliavinDensityBound, false);
  assert.equal(independent.scope.provesNSERegularity, false);

  assert.equal(config.analyticModel.fixedQ0, 4);
  assert.equal(config.analyticModel.deltaR, "R^4");
  assert.equal(config.producer.randomness, false);
  assert.equal(config.independent.randomness, false);
  assert.deepEqual(config.producer.besselCounts, [8, 16, 32, 64]);
  assert.deepEqual(config.producer.deltas, [16, 32, 64, 128, 256, 512]);
  assert.deepEqual(config.independent.rootCounts, [8, 16, 32, 64]);
  assert.deepEqual(config.independent.actionDeltas, [16, 32, 64, 128]);
  assert.equal(config.scope.intervalArithmetic, false);
  assert.equal(config.scope.provesNSERegularity, false);
  assert.equal(config.scope.provesNSESingularity, false);

  assert.doesNotMatch(
    producerScript,
    /(?:from|import)\s+.*r072e_independent_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /(?:from|import)\s+.*r072e_exact_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /certificates\/r072e\/result\.json/,
  );

  const producerBessel = producer.bessel.prefixRows;
  assert.deepEqual(
    producerBessel.map((row) => row.R),
    [8, 16, 32, 64],
  );
  near(producerBessel[0].targetEightOverPiSquared, 8 / Math.PI ** 2, 2e-15, "8/pi^2");
  assert.ok(producer.bessel.rootResidual.maximumAbsJ1AtRoot < 1e-14);
  assert.ok(producerBessel.at(-1).relativeTargetError < 0.06);
  assert.deepEqual(
    independent.rootFiniteLattice.map((row) => row.R),
    [8, 16, 32, 64],
  );
  assert.ok(
    independent.rootFiniteLattice.every(
      (row) =>
        row.q0 === 4 &&
        row.roots.length === row.R &&
        row.maximumTargetResidual < 2e-12 &&
        row.maximumNorm <= 1 + 1e-8,
    ),
  );
  assert.ok(
    independent.rootFiniteLattice.every(
      (row, index) =>
        Math.abs(row.besselMass - producerBessel[index].selectedSlopeMass) <
        2e-14,
    ),
  );
  assert.ok(
    Math.abs(independent.rootFiniteLattice.at(-1).relativeMassDifference) <
      5e-5,
  );

  const producerActions = producer.negativeSobolevAction.rows;
  const independentActions = independent.actionFiniteLattice;
  assert.deepEqual(
    producerActions.map((row) => row.delta),
    [16, 32, 64, 128, 256, 512],
  );
  assert.deepEqual(
    independentActions.map((row) => row.delta),
    [16, 32, 64, 128],
  );
  for (const rows of [producerActions, independentActions]) {
    assert.ok(rows.every((row) => Number(row.Q ?? row.actionFine) > 0));
    assert.ok(
      rows.slice(1).every(
        (row, index) =>
          Number(row.Q ?? row.actionFine) <
          Number(rows[index].Q ?? rows[index].actionFine),
      ),
    );
  }
  assert.ok(
    producerActions.every((row) => row.fineCoarseRelativeDifference < 3e-5),
  );
  assert.ok(
    independentActions.every(
      (row) =>
        row.q0 === 4 &&
        row.radius === 64 &&
        row.maximumNorm <= 1 + 2e-6 &&
        row.quadratureRelativeDefect < 2e-4,
    ),
  );
  const sharedActionRelativeDifferences = independentActions.map(
    (row, index) =>
      Math.abs(row.actionFine - producerActions[index].Q) /
      producerActions[index].Q,
  );
  assert.ok(Math.max(...sharedActionRelativeDifferences) < 0.003);
  assert.ok(independent.actionRadiusCheck.relativeDifference < 1e-6);
  assert.ok(independent.actionToleranceCheck.relativeDifference < 1e-6);
  assert.ok(producer.checks.deltaQOverLogDeltaBounded.maxToMin < 1.1);
  const independentNormalizedActions = independentActions.map(
    (row) => row.deltaActionOverOnePlusLog,
  );
  assert.ok(
    Math.max(...independentNormalizedActions) /
      Math.min(...independentNormalizedActions) <
      1.25,
  );

  assert.deepEqual(
    independent.physicalLedger.q0FactorAudit.threeQ0MinusTwoFactors,
    [1 / 16, 1 / 16, 1 / 16],
  );
  assert.equal(independent.physicalLedger.q0FactorAudit.theirProduct, 1 / 4096);
  assert.equal(
    independent.physicalLedger.q0FactorAudit.expectedProduct,
    1 / 4096,
  );
  assert.equal(
    independent.physicalLedger.q0FactorAudit.afterPhysicalTimeAverageAtX1,
    1 / 256,
  );
  assert.equal(producer.physicalLedger.expectedPowers.DInDelta, 2);
  assert.equal(producer.physicalLedger.expectedPowers.DOneThirdInDelta, 2 / 3);
  assert.equal(producer.physicalLedger.expectedPowers.rootLedgerInDelta, 1);
  assert.equal(producer.physicalLedger.expectedPowers.ratioInDelta, 1 / 3);
  assert.equal(producer.physicalLedger.expectedPowers.ratioInR, 4 / 3);
  near(
    producer.physicalLedger.fitsAgainstDelta.purePowerRatio.slope,
    1 / 3,
    0.01,
    "producer one-third exponent",
  );
  assert.equal(
    independent.physicalLedger.exactExponentLedger.ratioDeltaPower,
    "1/3",
  );
  assert.equal(
    independent.physicalLedger.exactExponentLedger.ratioRPower,
    "4/3",
  );
  near(
    independent.physicalLedger.empiricalDataDeltaExponent,
    2,
    2e-4,
    "independent data exponent",
  );
  near(
    independent.physicalLedger.empiricalLedgerRatioDeltaExponent,
    1 / 3,
    0.02,
    "independent ledger ratio exponent",
  );

  for (const rows of [
    producerProgress,
    producerResource,
    independentProgress,
    independentResource,
  ]) {
    assert.ok(rows.every((row) => row.elapsedSeconds >= 0));
    assert.ok(rows.every((row) => row.logicalCpus > 0 || rows === producerProgress));
  }
  assert.equal(producerProgress.at(-1).status, "passed");
  assert.equal(producerResource.at(-1).status, "passed");
  assert.equal(independentProgress.at(-1).status, "completed");
  assert.equal(independentProgress.at(-1).allPassed, true);
  assert.equal(independentResource.at(-1).status, "completed");

  const expectedCertificateFiles = [
    "README.md",
    "SHA256SUMS",
    "build_hashes.py",
    "command.txt",
    "config.json",
    "environment.txt",
    "independent-monitor.log",
    "independent-progress.ndjson",
    "independent-resource.ndjson",
    "independent-result.json",
    "producer-monitor.log",
    "producer-progress.ndjson",
    "producer-resource.ndjson",
    "result.json",
    "seed.txt",
  ];
  assert.deepEqual((await readdir(certRoot)).sort(), expectedCertificateFiles);
  const certificateHashes = await verifyHashes(certRoot, 14);
  assert.deepEqual(
    [...certificateHashes, "SHA256SUMS"].sort(),
    expectedCertificateFiles,
  );
});

test("archives, validates, hashes, and mirrors the formal R0.72E figure", async () => {
  const [manifest, validation, results, metadata, config, contract] =
    await Promise.all([
      readJson(resolve(figureRoot, "manifest.json")),
      readJson(resolve(figureRoot, "validation.json")),
      readJson(resolve(figureRoot, "results.json")),
      readJson(resolve(figureRoot, "figure-data-metadata.json")),
      readJson(resolve(figureRoot, "config.json")),
      readJson(resolve(figureRoot, "contract.json")),
    ]);

  assert.equal(manifest.release, "R0.72E");
  assert.equal(manifest.schemaVersion, "r072e-figure-manifest-v1");
  assert.equal(manifest.figureId, "R0.72E-1");
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.ok(manifest.assets.length >= 25);
  assert.equal(new Set(manifest.assets.map((asset) => asset.path)).size, manifest.assets.length);
  assert.equal(manifest.dataSummary.rowCount, 32);
  assert.deepEqual(manifest.dataSummary.panelCounts, { A: 10, B: 10, C: 12 });
  assert.deepEqual(manifest.dataSummary.RValues, [8, 16, 32, 64]);
  assert.deepEqual(
    manifest.dataSummary.producerActionDeltas,
    [16, 32, 64, 128, 256, 512],
  );
  assert.deepEqual(
    manifest.dataSummary.independentActionDeltas,
    [16, 32, 64, 128],
  );
  assert.equal(manifest.dataSummary.randomness, false);
  assert.equal(manifest.computation.q0, 4);
  assert.equal(manifest.computation.intervalArithmetic, false);
  assert.equal(manifest.computation.pdeDNS, false);
  assert.equal(manifest.computation.regressionUsedForPlottedClaim, false);
  assert.equal(manifest.computation.gpu, false);
  assert.equal(manifest.computation.dgx, false);
  assert.match(manifest.supportedClaim, /Bessel/i);
  assert.match(manifest.supportedClaim, /action/i);
  assert.match(manifest.supportedClaim, /ledger/i);
  assert.match(manifest.claimBoundary, /finite/i);
  assert.match(manifest.claimBoundary, /do not prove|does not prove/i);
  assert.match(manifest.claimBoundary, /Malliavin/i);
  assert.match(manifest.claimBoundary, /Navier-Stokes/i);
  assert.match(manifest.claimBoundary, /Millennium/i);

  assert.equal(config.release, "R0.72E");
  assert.equal(config.figureId, "R0.72E-1");
  assert.equal(config.expected.q0, 4);
  assert.deepEqual(config.expected.besselR, [8, 16, 32, 64]);
  assert.deepEqual(config.expected.producerActionDeltas, [16, 32, 64, 128, 256, 512]);
  assert.deepEqual(config.expected.independentActionDeltas, [16, 32, 64, 128]);
  assert.deepEqual(config.expected.ratioR, [8, 16, 32, 64]);
  assert.equal(config.figure.widthMillimetres, 178);
  assert.equal(config.figure.heightMillimetres, 88);
  assert.equal(config.figure.pngDpi, 600);
  assert.equal(contract.release, "R0.72E");
  assert.match(contract.question, /q0=4/);
  assert.equal(contract.widthMm, 178);
  assert.equal(contract.pngDpi, 600);
  assert.equal(contract.renderer, "python-matplotlib");

  assert.equal(validation.schemaVersion, "r072e-figure-validation-v1");
  assert.equal(validation.allPassed, true);
  assert.equal(validation.checkCount, validation.checks.length);
  assert.equal(validation.passedCheckCount, validation.checkCount);
  assert.ok(validation.checks.every((row) => row.passed));
  assert.equal(results.schemaVersion, "r072e-figure-results-v1");
  assert.equal(results.rowCount, 32);
  assert.deepEqual(results.panelCounts, { A: 10, B: 10, C: 12 });
  assert.equal(results.randomness, false);
  assert.equal(results.regressionUsedForPlottedClaim, false);
  assert.equal(results.finiteFitsAreDiagnostics, true);
  assert.equal(results.sourceStatus.producerPassed, true);
  assert.equal(results.sourceStatus.independentPassed, true);
  assert.deepEqual(results.panels.A.RValues, [8, 16, 32, 64]);
  assert.deepEqual(
    results.panels.B.producerDeltas,
    [16, 32, 64, 128, 256, 512],
  );
  assert.deepEqual(results.panels.B.independentDeltas, [16, 32, 64, 128]);
  assert.equal(results.panels.B.producerFinalX, 6);
  assert.equal(results.panels.B.independentFinalX, 1);
  assert.deepEqual(results.panels.C.RValues, [8, 16, 32, 64]);
  assert.equal(results.panels.C.analyticReferenceExponent, 4 / 3);
  assert.equal(metadata.rowCount, 32);
  assert.equal(metadata.randomness, false);
  for (const source of metadata.sourceFiles) {
    assert.match(source.sha256, /^[0-9a-f]{64}$/);
    assert.equal(await sha256(resolve(root, source.path)), source.sha256, source.path);
  }
  for (const [path, hash] of Object.entries(metadata.dataFiles)) {
    assert.equal(await sha256(resolve(figureRoot, path)), hash, path);
  }

  const requiredAssets = [
    "README.md",
    "build_figure.py",
    "build_hashes.py",
    "build_manifest.py",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "data.csv",
    "environment.txt",
    "figure-contract.md",
    "figure-data-metadata.json",
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "progress.ndjson",
    "publish_assets.py",
    "qa-final-size.png",
    "qa-grayscale.png",
    "qa-pdf.png",
    "qa-report.md",
    "qa_images.py",
    "requirements.txt",
    "resource-log.ndjson",
    "results.json",
    "validate.py",
    "validation.json",
  ];
  const assetPaths = manifest.assets.map((asset) => asset.path).sort();
  for (const path of requiredAssets) assert.ok(assetPaths.includes(path), path);
  for (const asset of manifest.assets) {
    assert.doesNotMatch(asset.path, /[/\\]|\.\./);
    const path = resolve(figureRoot, asset.path);
    assert.equal((await stat(path)).size, asset.bytes, asset.path);
    assert.equal(await sha256(path), asset.sha256, asset.path);
  }
  const figureHashes = await verifyHashes(figureRoot, manifest.assets.length + 1);
  assert.deepEqual(
    [...figureHashes, "SHA256SUMS"].sort(),
    (await readdir(figureRoot)).sort(),
  );
  assert.deepEqual(
    [...assetPaths, "manifest.json", "SHA256SUMS"].sort(),
    (await readdir(figureRoot)).sort(),
  );

  for (const extension of ["pdf", "png", "svg"]) {
    const archive = resolve(figureRoot, `figure.${extension}`);
    const mirror = resolve(
      publicRoot,
      `figures/r0-72e-supercritical-ledger.${extension}`,
    );
    assert.equal((await stat(mirror)).size, (await stat(archive)).size, extension);
    assert.equal(await sha256(mirror), await sha256(archive), extension);
  }
  const [pdf, png, svg, data] = await Promise.all([
    readFile(resolve(figureRoot, "figure.pdf")),
    readFile(resolve(figureRoot, "figure.png")),
    readFile(resolve(figureRoot, "figure.svg"), "utf8"),
    readFile(resolve(figureRoot, "data.csv"), "utf8"),
  ]);
  assert.equal(pdf.subarray(0, 4).toString(), "%PDF");
  assert.ok(pdf.length > 10_000);
  assert.match(svg, /<svg\b/);
  assert.ok(Buffer.byteLength(svg) > 10_000);
  assert.equal(data.trim().split("\n").length, results.rowCount + 1);
  const pngInfo = pngMetadata(png);
  assert.ok(Math.abs(pngInfo.width - 4205) <= 5, pngInfo.width);
  assert.ok(Math.abs(pngInfo.height - 2079) <= 5, pngInfo.height);
  near(pngInfo.dpiX, 600, 0.01, "PNG horizontal dpi");
  near(pngInfo.dpiY, 600, 0.01, "PNG vertical dpi");
});

test("retains R0.72E, its 95-node recap, and bilingual package after R0.72G", async () => {
  const [
    home,
    note,
    recap,
    literature,
    report,
    audit,
    notePdf,
    recapPdf,
    translationRows,
    compiledSource,
  ] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72e.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72e.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    readFile(resolve(root, "research/r072e_report-source.md"), "utf8"),
    readFile(resolve(root, "research/r072e_independent_audit.md"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72e.pdf")),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72e.pdf")),
    readJson(resolve(root, "translations/en.json")),
    readFile(resolve(publicRoot, "i18n-en.js"), "utf8"),
  ]);

  for (const [label, html, i18nVersion] of [
    ["homepage", home, "1.20"],
    ["note", note, "1.18"],
    ["recap", recap, "1.18"],
    ["literature", literature, "1.20"],
  ]) {
    assert.ok(
      html.includes(`src="/i18n-en.js?v=${i18nVersion}"`),
      `${label}: i18n version`,
    );
    assert.match(html, /R0\.72E/, label);
    assert.doesNotMatch(
      html,
      /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
      label,
    );
    assert.doesNotMatch(
      html,
      /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/,
      label,
    );
    assert.doesNotMatch(html, /\t/, label);
  }

  assert.match(home, /<html lang="zh-CN" data-site-version="1\.20">/);
  assert.match(home, /src="\/site-refresh\.js\?v=1\.20"/);
  assert.match(home, /<strong>v1\.20<\/strong>网页版本/);
  assert.match(home, /<strong>157<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72G<\/strong>最新研究节点/);
  assert.match(home, /展开 67 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72H/);
  assert.match(home, /R0\.70A–R0\.72G 共 59 个版本已公开；按当前 formal-figure 合同有 35 个完整封存，24 个旧版附图档案列入回补清单/);
  assert.match(home, /二十三个(?:问题)?阶段/);
  assert.equal((home.match(/href="\/notes\/r0-72e\.html"/g) ?? []).length, 2);
  assert.equal((home.match(/data-release="r072e"/g) ?? []).length, 1);
  assert.match(home, /recap-r0-61-r0-72g\.html/);
  assert.match(home, /recap-r0-61-r0-72g\.pdf/);

  assert.ok(
    note.includes(String.raw`候选 \(D^{1/3}\Lambda_1\) payment 被排除`),
  );
  assert.match(note, /PRODUCER · 16\/16 PASS/);
  assert.match(note, /INDEPENDENT · 16\/16 PASS/);
  assert.ok(note.includes(String.raw`fixed-\(q_0\)`));
  assert.ok(note.includes(String.raw`Q_{\delta,q_0}(X)`));
  assert.ok(note.includes(String.raw`q_0^6`));
  assert.ok(note.includes(String.raw`R^{4/3}`));
  assert.match(note, /full-frequency charge/);
  assert.match(note, /Kusuoka–Stroock Part II/);
  assert.match(note, /这个定理严格排除的是.*不是正则性本身/);
  assert.match(note, /href="\/notes\/r0-72e\.pdf"/);
  for (const extension of ["png", "svg", "pdf"]) {
    assert.match(
      note,
      new RegExp(`/figures/r0-72e-supercritical-ledger\\.${extension}`),
    );
  }
  assert.match(note, /research\/certificates\/r072e/);

  assert.match(recap, /R0\.61–R0\.72E 的 95 节公开笔记/);
  assert.match(recap, /收录节点：95/);
  assert.match(recap, /回顾截止时公开笔记：155/);
  assert.match(recap, /R0\.70A–R0\.72E 已公开并封存版本/);
  assert.match(recap, /二十二个研究阶段/);
  assert.match(recap, /问题状态：仍未解决/);
  assert.match(recap, /R0\.72F 寻找最小 frequency-sensitive repair/);
  assert.match(recap, /href="\/recap-r0-61-r0-72e\.pdf"/);
  const nodeIndexStart = recap.indexOf('<section id="node-index">');
  const nodeIndexEnd = recap.indexOf("</section>", nodeIndexStart);
  assert.ok(nodeIndexStart >= 0 && nodeIndexEnd > nodeIndexStart);
  assert.equal(
    (
      recap
        .slice(nodeIndexStart, nodeIndexEnd)
        .match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []
    ).length,
    95,
  );

  assert.match(literature, /id="r072e-boundary"/);
  assert.match(literature, /href="\/notes\/r0-72e\.html"/);
  assert.match(literature, /R0\.69P–R0\.72G/);
  assert.match(literature, /开放接口 · R0\.72H/);
  assert.match(literature, /doi\.org\/10\.15083\/00039520/);
  assert.match(literature, /dlmf\.nist\.gov\/10\.21/);
  assert.match(literature, /Kusuoka|Stroock/);
  assert.match(literature, /Part II/);

  assert.ok(report.includes(String.raw`Q_{\delta,q_0}(X)`));
  assert.ok(report.includes(String.raw`S_R^2=\frac{\delta_R}{\log(2+\delta_R)}`));
  assert.ok(report.includes(String.raw`q_0^6`));
  assert.ok(report.includes(String.raw`R^{4/3}`));
  assert.match(report, /Part II/);
  assert.match(report, /does not prove a\s+finite-time singularity/i);
  assert.match(audit, /exact constant-diagonal conjugacy/);
  assert.match(audit, /Part II rather than Part III/);
  assert.ok(audit.includes(String.raw`R^{4/3}`));

  for (const [label, pdf] of Object.entries({ notePdf, recapPdf })) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label);
    assert.ok(pdf.length > 10_000, label);
  }

  const translationMap = new Map(
    translationRows.map((row) => [row.zh, String(row.en ?? "").trim()]),
  );
  assert.equal(translationMap.size, translationRows.length);
  const compiled = parseCompiledTranslations(compiledSource);
  const pageStrings = new Set(
    [home, note, recap, literature].flatMap((html) =>
      extractTranslatableStrings(html),
    ),
  );
  assert.ok(pageStrings.size > 100);
  for (const source of pageStrings) {
    assert.ok(translationMap.has(source), `missing translation: ${source}`);
    const translated = translationMap.get(source);
    assert.ok(translated, `empty translation: ${source}`);
    assert.equal(containsChinese(translated), false, source);
    assert.deepEqual(
      extractProtectedTokens(translated),
      extractProtectedTokens(source),
      source,
    );
    assert.equal(compiled[source], translated, `compiled cache: ${source}`);
  }
});

test("keeps the current R0.72G site version and split release inventory", async () => {
  const [manifest, siteVersion, siteRefresh, home, noteFiles] =
    await Promise.all([
      readJson(resolve(root, "research/release-manifest.json")),
      readJson(resolve(publicRoot, "site-version.json")),
      readFile(resolve(publicRoot, "site-refresh.js"), "utf8"),
      readFile(resolve(publicRoot, "research-review.html"), "utf8"),
      readdir(resolve(publicRoot, "notes")),
    ]);

  assert.equal(manifest.schemaVersion, "research-release-manifest-v1");
  assert.equal(manifest.firstPdfRequiredRelease, "r070a");
  assert.equal(manifest.latestCompletedRelease, "r072g");
  assert.equal(manifest.siteVersion, "1.20");
  assert.equal(manifest.publicHtmlNoteCount, 157);
  assert.equal(manifest.postR060RecapNodeCount, 97);
  assert.equal(manifest.postR070APublishedReleaseCount, 59);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 35);
  assert.equal(manifest.legacyFormalFigureBacklogCount, 24);
  assert.equal(manifest.nextRelease, "r072h");
  assert.equal(
    manifest.latestReleaseGate,
    "tests/r072g-complete-root-packing-gate.test.mjs",
  );
  assert.match(manifest.completionRule, /certificates/);
  assert.match(manifest.completionRule, /independent audit/);
  assert.match(manifest.completionRule, /formal figure package/);
  assert.match(manifest.completionRule, /synchronized HTML\/PDF/);
  assert.match(manifest.completionRule, /publication tests pass/);

  assert.equal(siteVersion.schemaVersion, "research-site-version-v1");
  assert.equal(siteVersion.version, "1.20");
  assert.equal(siteVersion.latestRelease, "R0.72G");
  assert.equal(siteVersion.publicHtmlNoteCount, 157);
  assert.equal(siteVersion.publishedDate, "2026-08-27");
  assert.equal(
    noteFiles.filter((file) => file.endsWith(".html")).length,
    157,
  );
  assert.equal(
    (home.match(/data-release="r0\d{2}[a-z]"/g) ?? []).length,
    59,
  );
  assert.match(home, /NEXT · R0\.72H/);

  assert.match(siteRefresh, /document\.documentElement\.dataset\.siteVersion/);
  assert.match(siteRefresh, /\/site-version\.json\?check=/);
  assert.match(siteRefresh, /cache: "no-store"/);
  assert.match(siteRefresh, /research-site-refresh:/);
  assert.match(siteRefresh, /sessionStorage\.getItem/);
  assert.match(siteRefresh, /sessionStorage\.setItem/);
  assert.match(siteRefresh, /next\.searchParams\.set\("site", latest\.version\)/);
  assert.match(siteRefresh, /window\.location\.replace\(next\)/);
  assert.match(siteRefresh, /window\.setTimeout\(refreshIfStale, 15_000\)/);
  assert.match(siteRefresh, /addEventListener\("focus", refreshIfStale\)/);
  assert.match(
    siteRefresh,
    /addEventListener\("visibilitychange", refreshIfStale\)/,
  );
});
