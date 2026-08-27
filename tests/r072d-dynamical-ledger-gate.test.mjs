import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readdir, readFile, stat } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certRoot = resolve(root, "research/certificates/r072d");
const figRoot = resolve(
  root,
  "figures/r072d-dynamical-ledger/fig-r072d-dynamical-ledger",
);
const publicRoot = resolve(root, "public");
const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));
const sha256 = async (path) =>
  createHash("sha256").update(await readFile(path)).digest("hex");
const near = (actual, expected, tolerance, label) =>
  assert.ok(
    Math.abs(Number(actual) - expected) <= tolerance,
    label + ": " + actual + " versus " + expected,
  );

async function verifyHashes(directory, expectedRows) {
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trim()
    .split("\n");
  assert.equal(rows.length, expectedRows);
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, row);
    assert.equal(
      await sha256(resolve(directory, match[2])),
      match[1],
      match[2],
    );
  }
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

test("certifies the R0.72D lower family through two independent paths", async () => {
  const [producer, independent, producerScript, independentScript] =
    await Promise.all([
      readJson(resolve(certRoot, "result.json")),
      readJson(resolve(certRoot, "independent-result.json")),
      readFile(resolve(root, "research/r072d_exact_audit.py"), "utf8"),
      readFile(resolve(root, "research/r072d_independent_audit.py"), "utf8"),
    ]);

  assert.equal(producer.release, "R0.72D");
  assert.equal(
    producer.schemaVersion,
    "r072d-dynamical-ledger-producer-v1",
  );
  assert.equal(producer.allPassed, true);
  assert.equal(producer.checkCount, 11);
  assert.equal(producer.passedCheckCount, 11);
  assert.ok(producer.checks.every((row) => row.passed));
  assert.equal(producer.arithmetic.decimalDigits, 90);
  assert.equal(producer.arithmetic.intervalArithmetic, false);
  assert.equal(producer.scope.provesNSERegularity, false);
  assert.equal(producer.scope.analyticProofInJson, false);
  assert.equal(producer.scope.finiteMatrixDNS, false);
  assert.equal(producer.scope.intervalArithmetic, false);
  assert.equal(producer.scope.corroboratesInteriorRootConstruction, false);
  assert.equal(producer.scope.corroboratesNormalizedScaling, true);
  assert.match(producer.scope.note, /finite algebra and asymptotic bookkeeping/);
  assert.equal(
    producer.normalizedFamily.exactFormulas.Ks,
    "M(2M-1)(7M-1)/6",
  );
  assert.equal(
    producer.normalizedFamily.exactFormulas.chargeUpper,
    "(3/4)*(delta*a)^2/Ks",
  );
  assert.ok(
    producer.normalizedFamily.rows.every(
      (row) =>
        row.Ks === row.KsClosed &&
        Number(row.launchVectorNormSquared) === row.M &&
        Number(row.rowAlignmentResidual) === 0 &&
        Math.abs(Number(row.S2KfOverP2Kv) - 3) < 1e-80,
    ),
  );
  near(
    producer.normalizedFamily.fittedPowers.Phi,
    -8 / 3,
    2e-3,
    "producer phase power",
  );
  near(
    producer.normalizedFamily.fittedPowers.eta,
    2,
    1e-12,
    "producer coupling power",
  );

  assert.equal(independent.release, "R0.72D");
  assert.equal(
    independent.schemaVersion,
    "r072d-dynamical-ledger-independent-v1",
  );
  assert.equal(independent.allPassed, true);
  assert.equal(independent.checkCount, 14);
  assert.equal(independent.passedCheckCount, 14);
  assert.ok(independent.checks.every((row) => row.passed));
  assert.equal(independent.scope.provesNSERegularity, false);
  assert.equal(independent.scope.provesInfiniteLattice, false);
  assert.equal(independent.scope.provesAllGenerations, false);
  assert.equal(independent.scope.rigorousUnknownConstantLowerBound, false);
  assert.equal(independent.scope.intervalArithmetic, false);
  assert.equal(independent.arithmetic.intervalArithmetic, false);
  assert.match(independent.scope.note, /corroborate the analytic scales/);
  assert.equal(independent.independence.importsProducer, false);
  assert.equal(independent.independence.readsProducerResult, false);
  assert.match(independent.independence.rudinShapiroPath, /binary 11-pair/);
  assert.doesNotMatch(
    producerScript,
    /(?:from|import)\s+.*r072d_independent_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /(?:from|import)\s+.*r072d_exact_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /research\/certificates\/r072d\/result\.json/,
  );
  near(
    independent.heatMultiplierFFT.fittedObservedL1Power,
    -1.5,
    1e-3,
    "FFT L1 power",
  );
  near(
    independent.heatMultiplierFFT.fittedObservedL2SquarePower,
    -1,
    1e-3,
    "FFT L2-square power",
  );
  near(
    independent.finiteODE.fittedPowers.zetaAbsolute,
    -0.5,
    2e-2,
    "zeta power",
  );
  assert.deepEqual(
    independent.finiteODE.rows.map((row) => row.M),
    [8, 16, 32, 64],
  );
  assert.ok(
    independent.finiteODE.rows.every(
      (row) =>
        row.relativeRootResidual < 1e-16 &&
        row.slopeIdentityRelativeDefect < 1e-12 &&
        Math.abs(row.normalizedLaunchNormSquared - row.M) < 3e-14 &&
        Math.abs(row.S2KfOverP2Kv - 3) < 1e-14 &&
        row.hTauAbsoluteOverH0 > 0.9 &&
        row.terminalOverInitialNormSquared <= 1,
    ),
  );
  assert.ok(
    independent.finiteODE.pressureTest.maximumHRatioRelativeDefect < 2e-9,
  );
  assert.ok(
    independent.finiteODE.pressureTest.maximumZetaRelativeDefect < 2e-9,
  );
  await verifyHashes(certRoot, 14);
});

test("archives and mirrors the formal R0.72D figure", async () => {
  const [manifest, validation, results] = await Promise.all([
    readJson(resolve(figRoot, "manifest.json")),
    readJson(resolve(figRoot, "validation.json")),
    readJson(resolve(figRoot, "results.json")),
  ]);
  assert.equal(manifest.release, "R0.72D");
  assert.equal(manifest.schemaVersion, "r072d-figure-manifest-v1");
  assert.equal(manifest.figureId, "R0.72D-1");
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(manifest.assets.length, 27);
  assert.equal(manifest.dataSummary.rowCount, 628);
  assert.deepEqual(manifest.dataSummary.panelCounts, { A: 605, B: 23 });
  assert.equal(manifest.dataSummary.maximumInitialCrossAuditAbsoluteDefect, 0);
  assert.ok(manifest.dataSummary.maximumRootResidual < 1e-16);
  assert.equal(manifest.computation.phaseGridSize, 32768);
  assert.equal(manifest.computation.finiteLatticeRadiusFactor, 6);
  assert.equal(manifest.computation.rootTime, "tau_M=M^-3");
  assert.equal(manifest.computation.intervalArithmetic, false);
  assert.equal(manifest.computation.pdeDNS, false);
  assert.equal(manifest.computation.regressionUsedForPlottedClaim, false);
  assert.equal(manifest.computation.gpu, false);
  assert.equal(manifest.computation.dgx, false);
  assert.match(manifest.supportedClaim, /order one/);
  assert.match(manifest.claimBoundary, /finite diagnostics/);
  assert.match(manifest.claimBoundary, /do not prove/);
  assert.match(manifest.claimBoundary, /No interval arithmetic, PDE DNS/);
  assert.match(manifest.claimBoundary, /Millennium-problem solution/);
  assert.equal(validation.allPassed, true);
  assert.equal(validation.schemaVersion, "r072d-figure-validation-v1");
  assert.equal(validation.checkCount, 15);
  assert.equal(validation.passedCheckCount, 15);
  assert.equal(results.rowCount, 628);
  assert.equal(results.randomness, false);
  assert.equal(results.regressionUsedForPlottedClaim, false);
  assert.equal(
    results.mixedExposure.scope,
    "finite phase-grid proxy on s<=16 plus a separate analytic tail upper bound",
  );
  assert.deepEqual(results.rootPanel.carrierCounts, [8, 16, 32, 64]);
  assert.equal(results.rootPanel.latticeRadiusFactor, 6);
  assert.ok(results.rootPanel.maximumRelativeRootResidual < 1e-16);
  assert.ok(results.rootPanel.minimumSlopeRatio > 0.9);
  assert.ok(results.rootPanel.terminalSlopeRatio > 0.98);
  for (const asset of manifest.assets) {
    const path = resolve(figRoot, asset.path);
    assert.equal((await stat(path)).size, asset.bytes, asset.path);
    assert.equal(await sha256(path), asset.sha256, asset.path);
  }
  await verifyHashes(figRoot, 28);
  for (const extension of ["pdf", "png", "svg"]) {
    const archive = resolve(figRoot, "figure." + extension);
    const mirror = resolve(
      publicRoot,
      "figures/r0-72d-dynamical-ledger." + extension,
    );
    assert.equal((await stat(mirror)).size, (await stat(archive)).size);
    assert.equal(await sha256(mirror), await sha256(archive));
  }
  const png = await readFile(resolve(figRoot, "figure.png"));
  const metadata = pngMetadata(png);
  assert.deepEqual([metadata.width, metadata.height], [4200, 2028]);
  near(metadata.dpiX, 600, 0.01, "PNG horizontal dpi");
  near(metadata.dpiY, 600, 0.01, "PNG vertical dpi");
});

test("retains R0.72D and its complete post-R0.60 recap", async () => {
  const [home, note, recap, literature, report, audit, notePdf, recapPdf] =
    await Promise.all([
      readFile(resolve(publicRoot, "research-review.html"), "utf8"),
      readFile(resolve(publicRoot, "notes/r0-72d.html"), "utf8"),
      readFile(resolve(publicRoot, "recap-r0-61-r0-72d.html"), "utf8"),
      readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
      readFile(resolve(root, "research/r072d_report-source.md"), "utf8"),
      readFile(resolve(root, "research/r072d_independent_audit.md"), "utf8"),
      readFile(resolve(publicRoot, "notes/r0-72d.pdf")),
      readFile(resolve(publicRoot, "recap-r0-61-r0-72d.pdf")),
    ]);
  for (const [label, html, i18nVersion] of [
    ["homepage", home, "1.23"],
    ["note", note, "1.17"],
    ["recap", recap, "1.17"],
    ["literature", literature, "1.23"],
  ]) {
    assert.ok(
      html.includes(`src="/i18n-en.js?v=${i18nVersion}"`),
      `${label}: i18n version`,
    );
    assert.match(html, /R0\.72D/, label);
    assert.doesNotMatch(html, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
    assert.doesNotMatch(
      html,
      /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/,
    );
    assert.doesNotMatch(html, /\t/);
  }
  assert.match(home, /<html lang="zh-CN" data-site-version="1\.23">/);
  assert.match(home, /<strong>160<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72J<\/strong>最新研究节点/);
  assert.match(home, /展开 70 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72K/);
  assert.match(home, /R0\.70A–R0\.72J 共 62 个版本已公开；38 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单/);
  assert.match(home, /二十六个(?:问题)?阶段/);
  assert.match(home, /累计回顾收录 100 个节点/);
  assert.match(home, /recap-r0-61-r0-72j\.html/);
  assert.equal((home.match(/href="\/notes\/r0-72d\.html"/g) ?? []).length, 2);
  assert.equal((home.match(/data-release="r072d"/g) ?? []).length, 1);
  assert.match(note, /PRODUCER · 11\/11 PASS/);
  assert.match(note, /INDEPENDENT · 14\/14 PASS/);
  assert.match(note, /完整归一化账本不再趋零，但也没有发散/);
  assert.match(note, /它不是 .*支付失败的反例，更不是一般三维奇性构造/);
  assert.ok(note.includes("\\tau_M=M^{-3}"));
  assert.ok(note.includes("\\mathbb P(u\\times\\omega)=(-vf_z,0,0)"));
  assert.ok(note.includes("\\gamma^{4/3}"));
  assert.match(note, /href="\/notes\/r0-72d\.pdf"/);
  assert.match(note, /\/figures\/r0-72d-dynamical-ledger\.(?:png|svg|pdf)/);
  assert.match(recap, /R0\.61–R0\.72D 的 94 节公开笔记/);
  assert.match(recap, /收录节点：94/);
  assert.match(recap, /回顾截止时公开笔记：154/);
  assert.match(recap, /二十一个阶段/);
  assert.match(recap, /问题状态：仍未解决/);
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  assert.equal(
    (recap.slice(start, end).match(/href="\/notes\/r0-[^"]+\.html"/g) ?? [])
      .length,
    94,
  );
  assert.match(literature, /id="r072d-boundary"/);
  assert.match(literature, /R0\.69P–R0\.72J/);
  assert.match(literature, /开放接口 · R0\.72K/);
  assert.match(literature, /doi\.org\/10\.1515\/crll\.1988\.390\.79/);
  assert.ok(report.includes("D_M^{1/3}\\le C"));
  assert.match(report, /K_f=c_M\^2K_s/);
  assert.match(report, /q=q_0/);
  assert.match(audit, /K_f=c_M\^2K_s/);
  for (const pdf of [notePdf, recapPdf]) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF");
    assert.ok(pdf.length > 10_000);
  }
});

test("locks the current R0.72J manifest while retaining R0.72D", async () => {
  const [manifest, siteVersion, home, noteFiles] = await Promise.all([
    readJson(resolve(root, "research/release-manifest.json")),
    readJson(resolve(publicRoot, "site-version.json")),
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readdir(resolve(publicRoot, "notes")),
  ]);
  assert.equal(manifest.latestCompletedRelease, "r072j");
  assert.equal(manifest.siteVersion, "1.23");
  assert.equal(manifest.publicHtmlNoteCount, 160);
  assert.equal(manifest.postR060RecapNodeCount, 100);
  assert.equal(manifest.postR070APublishedReleaseCount, 62);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 38);
  assert.equal(manifest.legacyFormalFigureBacklogCount, 24);
  assert.equal(manifest.nextRelease, "r072k");
  assert.match(
    manifest.completionRule,
    /analytic proof or stated negative result.*formal figure package.*synchronized HTML\/PDF.*publication tests pass/,
  );
  assert.equal(
    manifest.latestReleaseGate,
    "tests/r072j-mixed-parity-gate.test.mjs",
  );
  assert.equal(siteVersion.version, "1.23");
  assert.equal(siteVersion.latestRelease, "R0.72J");
  assert.equal(siteVersion.publicHtmlNoteCount, 160);
  assert.equal(
    noteFiles.filter((file) => file.endsWith(".html")).length,
    160,
  );
  assert.equal(
    (home.match(/data-release="r0\d{2}[a-z]"/g) ?? []).length,
    62,
  );
});
