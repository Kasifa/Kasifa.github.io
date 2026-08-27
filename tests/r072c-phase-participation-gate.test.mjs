import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readdir, readFile, stat } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificateRoot = resolve(root, "research/certificates/r072c");
const figureRoot = resolve(
  root,
  "figures/r072c-phase-participation/fig-r072c-phase-participation",
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

async function verifyChecksumLedger(directory, expectedRows) {
  const ledger = await readFile(resolve(directory, "SHA256SUMS"), "utf8");
  const rows = ledger.trim().split("\n");
  assert.equal(rows.length, expectedRows);
  const paths = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, row);
    paths.push(match[2]);
    assert.equal(
      await sha256(resolve(directory, match[2])),
      match[1],
      match[2],
    );
  }
  assert.equal(new Set(paths).size, paths.length, "duplicate checksum path");
}

function readPngMetadata(buffer) {
  const signature = Buffer.from([137, 80, 78, 71, 13, 10, 26, 10]);
  assert.ok(buffer.subarray(0, 8).equals(signature), "PNG signature");

  let offset = 8;
  let width;
  let height;
  let pixelsPerMetreX;
  let pixelsPerMetreY;
  let unit;
  while (offset + 12 <= buffer.length) {
    const length = buffer.readUInt32BE(offset);
    const type = buffer.subarray(offset + 4, offset + 8).toString("ascii");
    const dataStart = offset + 8;
    const dataEnd = dataStart + length;
    assert.ok(dataEnd + 4 <= buffer.length, `${type}: truncated PNG chunk`);
    if (type === "IHDR") {
      width = buffer.readUInt32BE(dataStart);
      height = buffer.readUInt32BE(dataStart + 4);
    } else if (type === "pHYs") {
      pixelsPerMetreX = buffer.readUInt32BE(dataStart);
      pixelsPerMetreY = buffer.readUInt32BE(dataStart + 4);
      unit = buffer[dataStart + 8];
    }
    offset = dataEnd + 4;
    if (type === "IEND") break;
  }

  assert.equal(unit, 1, "PNG pHYs must use metres");
  return {
    width,
    height,
    dpiX: pixelsPerMetreX * 0.0254,
    dpiY: pixelsPerMetreY * 0.0254,
  };
}

test("certifies the R0.72C physical-phase ledger through independent paths", async () => {
  const [producer, independent, producerScript, independentScript] =
    await Promise.all([
      readJson(resolve(certificateRoot, "result.json")),
      readJson(resolve(certificateRoot, "independent-result.json")),
      readFile(resolve(root, "research/r072c_exact_audit.py"), "utf8"),
      readFile(resolve(root, "research/r072c_independent_audit.py"), "utf8"),
    ]);

  assert.equal(producer.release, "R0.72C");
  assert.equal(producer.schemaVersion, "r072c-physical-phase-producer-v1");
  assert.equal(producer.allPassed, true);
  assert.equal(producer.checkCount, 12);
  assert.equal(producer.passedCheckCount, 12);
  assert.equal(producer.checks.length, 12);
  assert.ok(producer.checks.every((row) => row.passed));
  assert.equal(producer.arithmetic.intervalArithmetic, false);
  assert.equal(producer.scope.provesNSERegularity, false);
  assert.equal(producer.scope.constructsNormalizedLowerFamily, false);

  assert.equal(independent.release, "R0.72C");
  assert.equal(
    independent.schemaVersion,
    "r072c-phase-sensitive-independent-v1",
  );
  assert.equal(independent.allPassed, true);
  assert.equal(independent.checkCount, 11);
  assert.equal(independent.passedCheckCount, 11);
  assert.equal(independent.checks.length, 11);
  assert.ok(independent.checks.every((row) => row.passed));
  assert.equal(independent.arithmetic.intervalArithmetic, false);
  assert.equal(independent.scope.provesNSERegularity, false);
  assert.equal(independent.scope.provesCompleteRootLowerBound, false);

  assert.equal(independent.independence.importsProducer, false);
  assert.equal(independent.independence.readsProducerResult, false);
  assert.equal(independent.independence.rawParametersRepeatedLocally, true);
  assert.match(
    independent.independence.rudinShapiroSecondPath,
    /overlapping binary 11-pair parity/,
  );
  assert.doesNotMatch(
    producerScript,
    /(?:from|import)\s+.*r072c_independent_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /(?:from|import)\s+.*r072c_exact_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /research\/certificates\/r072c\/result\.json/,
  );
  near(producer.parameters.Kz, 1, 1e-80, "producer Kz");
  near(independent.parameters.Kz, 1.25, 1e-15, "independent Kz");
  near(producer.parameters.fixedT, 0.01, 1e-80, "producer fixed t");
  near(
    independent.parameters.fixedTEqualsKappaA0,
    0.036,
    1e-15,
    "independent fixed t",
  );

  assert.match(producer.analyticLedger.physicalPairing, /conj\(w_l\)/);
  assert.equal(Number(producer.complexModels.pairedSkewDefect), 0);
  assert.ok(Number(producer.complexModels.naiveSkewDefect) > 1);
  near(
    producer.complexModels.halfEnergyDerivative,
    1,
    1e-80,
    "naive complex energy-growth witness",
  );
  assert.equal(independent.matrixStructure.conjugatePairedSkewDefect, 0);
  assert.equal(independent.matrixStructure.naiveComplexHermitianDefect, 0);
  assert.ok(independent.matrixStructure.naiveWitnessEnergyDerivative > 0);
  assert.ok(independent.matrixStructure.rhoRelativeDefect < 3e-15);
  assert.ok(independent.matrixStructure.qRowRelativeDefect < 3e-15);

  assert.ok(
    producer.jointInequality.rows.every(
      (row) =>
        Number(row.leftOverRight) <= 1 &&
        Number(row.identityResidual) < 1e-80,
    ),
  );
  assert.ok(
    Number(
      producer.heatParticipation.subcarrier.rows.at(-1).defectFromOne,
    ) <
      Number(producer.heatParticipation.subcarrier.rows[0].defectFromOne),
  );
  assert.ok(
    Number(producer.heatParticipation.critical.rows.at(-1).absoluteDefect) <
      Number(producer.heatParticipation.critical.rows[0].absoluteDefect),
  );
  assert.ok(
    Number(
      producer.heatParticipation.effectiveCarrier.rows.at(-1).absoluteDefect,
    ) <
      Number(
        producer.heatParticipation.effectiveCarrier.rows[0].absoluteDefect,
      ),
  );

  assert.equal(producer.analyticLedger.exactLaunchPower, "-8/3");
  assert.equal(producer.analyticLedger.fixedPositivePower, "-3");
  near(
    producer.rudinShapiro.oddGenerationExactFamily.fittedTailPower,
    -8 / 3,
    2e-3,
    "producer Rudin-Shapiro power",
  );
  near(
    independent.rudinShapiro.summary.fittedTailPower,
    -8 / 3,
    2.5e-4,
    "independent Rudin-Shapiro power",
  );
  near(
    producer.fixedPositiveSharpness.fittedTailPower,
    -3,
    2e-3,
    "producer fixed-positive power",
  );
  near(
    independent.fixedPositiveLayer.fittedTailPower,
    -3,
    3e-5,
    "independent fixed-positive power",
  );

  const producerRudinShapiro =
    producer.rudinShapiro.oddGenerationExactFamily.rows;
  assert.equal(producerRudinShapiro.at(-1).generation, 13);
  assert.equal(producerRudinShapiro.at(-1).M, 8192);
  assert.ok(
    producerRudinShapiro.every(
      (row) =>
        Number(row.chi) === 0.25 &&
        Number(row.endpointResidual) === 0 &&
        Number(row.OmegaIdentityResidual) === 0 &&
        Number(row.PhiIdentityResidual) < 1e-80,
    ),
  );
  assert.equal(independent.rudinShapiro.rows.at(-1).generation, 19);
  assert.equal(independent.rudinShapiro.rows.at(-1).M, 2 ** 19);
  assert.ok(
    independent.rudinShapiro.rows.every(
      (row) =>
        row.chi === 0.25 &&
        row.sumQ === 0 &&
        row.sumPSquaredOver2M === 1 &&
        row.coefficientEnergyExact &&
        row.recursiveEqualsBinaryPath,
    ),
  );

  const producerBoundary = (regime, beta) =>
    producer.phaseBoundaries.find(
      (row) => row.regime === regime && row.beta === beta,
    ).certifiedAlphaBoundaryDecimal;
  near(
    producerBoundary("exact-launch-phase-uniform", "0"),
    8 / 7,
    2e-15,
    "producer exact-launch beta-zero endpoint",
  );
  near(
    producerBoundary("exact-launch-phase-uniform", "2"),
    2,
    2e-15,
    "producer exact-launch cap",
  );
  near(
    producerBoundary("fixed-positive-layer", "0"),
    9 / 7,
    2e-15,
    "producer fixed-positive beta-zero endpoint",
  );
  near(
    producerBoundary("fixed-positive-layer", "9/4"),
    9 / 4,
    2e-15,
    "producer fixed-positive cap",
  );

  const independentBetaZero = independent.phaseBoundary.find(
    (row) => row.beta === 0,
  );
  const independentExactCap = independent.phaseBoundary.find(
    (row) => row.beta === 2,
  );
  const independentFixedCap = independent.phaseBoundary.find(
    (row) => row.beta === 2.25,
  );
  const independentCoherentCap = independent.phaseBoundary.find(
    (row) => row.beta === 3,
  );
  near(
    independentBetaZero.exactLaunchArbitraryPhase,
    8 / 7,
    2e-15,
    "independent exact-launch beta-zero endpoint",
  );
  near(
    independentBetaZero.fixedPositiveLayer,
    9 / 7,
    2e-15,
    "independent fixed-positive beta-zero endpoint",
  );
  near(
    independentBetaZero.coherentExactLaunchReference,
    10 / 7,
    2e-15,
    "independent coherent beta-zero reference",
  );
  near(
    independentExactCap.exactLaunchArbitraryPhase,
    2,
    2e-15,
    "independent exact-launch cap",
  );
  near(
    independentFixedCap.fixedPositiveLayer,
    9 / 4,
    2e-15,
    "independent fixed-positive cap",
  );
  near(
    independentCoherentCap.coherentExactLaunchReference,
    5 / 2,
    2e-15,
    "independent coherent cap",
  );
});

test("verifies the complete R0.72C certificate checksum ledger", async () => {
  await verifyChecksumLedger(certificateRoot, 14);
});

test("archives, validates, and mirrors the formal R0.72C figure", async () => {
  const [manifest, validation, figureResults] = await Promise.all([
    readJson(resolve(figureRoot, "manifest.json")),
    readJson(resolve(figureRoot, "validation.json")),
    readJson(resolve(figureRoot, "results.json")),
  ]);

  assert.equal(manifest.release, "R0.72C");
  assert.equal(manifest.schemaVersion, "r072c-figure-manifest-v1");
  assert.equal(manifest.figureId, "R0.72C-1");
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(manifest.assets.length, 26);
  assert.equal(manifest.dataSummary.rowCount, 523);
  assert.equal(manifest.dataSummary.certificateCrossAudit.producerRowCount, 7);
  assert.equal(
    manifest.dataSummary.certificateCrossAudit.independentRowCount,
    9,
  );
  assert.equal(manifest.computation.intervalArithmetic, false);
  assert.equal(manifest.computation.pdeDNS, false);
  assert.match(manifest.supportedClaim, /M\^-8\/3/);
  assert.match(manifest.supportedClaim, /M\^-3/);
  assert.match(manifest.claimBoundary, /algebraic/);
  assert.match(manifest.claimBoundary, /remaining tail/);
  assert.match(manifest.claimBoundary, /no DNS or general Navier-Stokes/);

  assert.equal(validation.allPassed, true);
  assert.equal(validation.checkCount, 15);
  assert.equal(validation.passedCheckCount, 15);
  assert.equal(validation.checks.length, 15);
  assert.ok(validation.checks.every((row) => row.passed));
  const validationEndpoints = validation.checks.find(
    (row) => row.name === "phase boundary endpoints",
  ).value;
  near(validationEndpoints.arbitraryBetaZero, 8 / 7, 2e-15, "figure 8/7");
  near(validationEndpoints.fixedBetaZero, 9 / 7, 2e-15, "figure 9/7");
  near(validationEndpoints.coherentBetaZero, 10 / 7, 2e-15, "figure 10/7");
  near(validationEndpoints.arbitraryCap, 2, 2e-15, "figure cap 2");
  near(validationEndpoints.fixedCap, 9 / 4, 2e-15, "figure cap 9/4");
  near(validationEndpoints.coherentCap, 5 / 2, 2e-15, "figure cap 5/2");

  assert.equal(figureResults.rowCount, 523);
  assert.equal(figureResults.sourceStatus.producerAllPassed, true);
  assert.equal(figureResults.sourceStatus.independentAllPassed, true);
  assert.equal(figureResults.randomness, false);
  assert.equal(figureResults.regressionOrFittedMaximumUsed, false);
  assert.equal(figureResults.exactLaunchPrefactors.coherentPower, "-10/3");
  assert.equal(
    figureResults.exactLaunchPrefactors.rudinShapiroPower,
    "-8/3",
  );
  assert.equal(
    figureResults.phaseBoundaries.fixedPositiveTimeTail,
    "min(9/4,(9+3 beta)/7)",
  );

  for (const asset of manifest.assets) {
    const path = resolve(figureRoot, asset.path);
    assert.equal((await stat(path)).size, asset.bytes, asset.path);
    assert.equal(await sha256(path), asset.sha256, asset.path);
  }
  await verifyChecksumLedger(figureRoot, 27);

  const pngAsset = manifest.assets.find((asset) => asset.path === "figure.png");
  assert.deepEqual(pngAsset.pixels, [4200, 2028]);
  near(pngAsset.dpi[0], 600, 0.01, "manifest PNG horizontal dpi");
  near(pngAsset.dpi[1], 600, 0.01, "manifest PNG vertical dpi");

  const minimumBytes = { pdf: 40_000, png: 400_000, svg: 70_000 };
  for (const extension of ["pdf", "png", "svg"]) {
    const archive = resolve(figureRoot, `figure.${extension}`);
    const mirror = resolve(
      publicRoot,
      `figures/r0-72c-phase-participation.${extension}`,
    );
    assert.ok((await stat(archive)).size > minimumBytes[extension], archive);
    assert.equal((await stat(mirror)).size, (await stat(archive)).size, mirror);
    assert.equal(await sha256(mirror), await sha256(archive), mirror);
  }

  const [pdf, png, svg] = await Promise.all([
    readFile(resolve(figureRoot, "figure.pdf")),
    readFile(resolve(figureRoot, "figure.png")),
    readFile(resolve(figureRoot, "figure.svg"), "utf8"),
  ]);
  assert.equal(pdf.subarray(0, 4).toString(), "%PDF");
  assert.match(svg, /<svg\b/);
  const pngMetadata = readPngMetadata(png);
  assert.equal(pngMetadata.width, 4200);
  assert.equal(pngMetadata.height, 2028);
  near(pngMetadata.dpiX, 600, 0.01, "PNG horizontal dpi");
  near(pngMetadata.dpiY, 600, 0.01, "PNG vertical dpi");
});

test("retains the R0.72C note and recap after the homepage advances to R0.72E", async () => {
  const [home, note, recap, literature, notePdf, recapPdf] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72c.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72c.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72c.pdf")),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72c.pdf")),
  ]);

  for (const [label, html, i18nVersion] of [
    ["homepage", home, "1.18"],
    ["note", note, "1.16"],
    ["recap", recap, "1.16"],
    ["literature", literature, "1.18"],
  ]) {
    assert.ok(
      html.includes(`src="/i18n-en.js?v=${i18nVersion}"`),
      `${label}: i18n version`,
    );
    assert.match(html, /R0\.72C/, label);
    assert.match(html, /R0\.72D/, label);
    assert.ok(html.includes(String.raw`M^{-8/3}`), `${label}: M^-8/3`);
    assert.ok(html.includes(String.raw`M^{-3}`), `${label}: M^-3`);
    assert.ok(html.includes(String.raw`实 \(\delta\)`), `${label}: real delta`);
    assert.ok(
      html.includes(String.raw`\delta\ne0`),
      `${label}: nonzero delta branch`,
    );
    assert.match(html, /共轭/, label);
    assert.match(html, /pre(?:-ledger|\/tail)/, label);
    assert.match(html, /tail/, label);
    assert.match(
      html,
      /(?:不是一般三维|没有一般 NSE|一般 NSE 结论|一般 Navier–Stokes 正则性仍开放|不触及一般三维正则性)/,
      label,
    );
  }

  assert.match(home, /<html lang="zh-CN" data-site-version="1\.18">/);
  assert.match(home, /src="\/site-refresh\.js\?v=1\.18"/);
  assert.match(home, /<strong>v1\.18<\/strong>网页版本/);
  assert.match(home, /<strong>155<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72E<\/strong>最新研究节点/);
  assert.match(home, /展开 65 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72F/);
  assert.match(home, /R0\.70A–R0\.72E 共 57 个已公开并封存版本/);
  assert.match(home, /按二十二个阶段组织/);
  assert.match(home, /累计回顾收录 95 个节点/);
  assert.equal((home.match(/href="\/notes\/r0-72c\.html"/g) ?? []).length, 2);
  assert.equal((home.match(/data-release="r072c"/g) ?? []).length, 1);
  assert.match(
    home,
    /<div class="task-one" id="r072c" data-release="r072c"/,
  );
  assert.match(home, /recap-r0-61-r0-72e\.html/);
  assert.match(home, /recap-r0-61-r0-72e\.pdf/);

  assert.match(note, /producer certificate: 12\/12 PASS/);
  assert.match(note, /independent certificate: 11\/11 PASS/);
  assert.match(note, /对每个实 \\\(\\delta\\\)/);
  assert.ok(note.includes(String.raw`\delta\ne0`));
  assert.match(note, /href="\/notes\/r0-72c\.pdf"/);
  assert.match(note, /\/figures\/r0-72c-phase-participation\.png/);
  assert.match(note, /\/figures\/r0-72c-phase-participation\.svg/);
  assert.match(note, /\/figures\/r0-72c-phase-participation\.pdf/);
  assert.match(note, /research\/certificates\/r072c/);

  assert.match(recap, /R0\.61–R0\.72C 的 93 节公开笔记/);
  assert.match(recap, /收录节点：93/);
  assert.match(recap, /回顾截止时公开笔记：153/);
  assert.match(recap, /href="\/recap-r0-61-r0-72c\.pdf"/);
  const nodeIndexStart = recap.indexOf('<section id="node-index">');
  const nodeIndexEnd = recap.indexOf("</section>", nodeIndexStart);
  assert.ok(nodeIndexStart >= 0 && nodeIndexEnd > nodeIndexStart);
  const nodeIndex = recap.slice(nodeIndexStart, nodeIndexEnd);
  assert.equal(
    (nodeIndex.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length,
    93,
  );

  assert.match(literature, /id="r072c-boundary"/);
  assert.match(literature, /href="\/notes\/r0-72c\.html"/);
  assert.match(literature, /R0\.69P–R0\.72E/);
  assert.match(literature, /开放接口 · R0\.72F/);
  for (const arxiv of [
    "2309.15738",
    "2410.05657",
    "2501.16905",
    "2603.14624",
    "2105.12308",
    "2311.04395",
    "1909.08777",
  ]) {
    assert.match(literature, new RegExp(`arxiv\\.org/abs/${arxiv}`), arxiv);
  }

  for (const [label, pdf] of Object.entries({ notePdf, recapPdf })) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label);
    assert.ok(pdf.length > 10_000, label);
  }
});

test("keeps the current manifest and refresh contract synchronized after R0.72E", async () => {
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
  assert.equal(manifest.latestCompletedRelease, "r072e");
  assert.equal(manifest.siteVersion, "1.18");
  assert.equal(manifest.publicHtmlNoteCount, 155);
  assert.equal(manifest.postR060RecapNodeCount, 95);
  assert.equal(manifest.postR070ASealedReleaseCount, 57);
  assert.equal(manifest.nextRelease, "r072f");
  assert.equal(
    manifest.latestReleaseGate,
    "tests/r072e-supercritical-ledger-gate.test.mjs",
  );
  assert.match(manifest.completionRule, /certificates/);
  assert.match(manifest.completionRule, /independent audit/);
  assert.match(manifest.completionRule, /synchronized HTML\/PDF/);
  assert.match(manifest.completionRule, /publication tests pass/);

  assert.equal(siteVersion.schemaVersion, "research-site-version-v1");
  assert.equal(siteVersion.version, manifest.siteVersion);
  assert.equal(siteVersion.latestRelease, "R0.72E");
  assert.equal(siteVersion.publicHtmlNoteCount, manifest.publicHtmlNoteCount);
  assert.equal(siteVersion.publishedDate, "2026-08-27");
  assert.equal(
    noteFiles.filter((file) => file.endsWith(".html")).length,
    155,
  );
  assert.equal(
    (home.match(/data-release="r0\d{2}[a-z]"/g) ?? []).length,
    57,
  );

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
