import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile, stat } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificateRoot = resolve(root, "research/certificates/r072b");
const figureRoot = resolve(
  root,
  "figures/r072b-row-coherence/fig-r072b-row-coherence",
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

test("certifies the R0.72B target-row and coherent-carrier ledger twice", async () => {
  const [producer, independent, producerScript, independentScript] =
    await Promise.all([
      readJson(resolve(certificateRoot, "result.json")),
      readJson(resolve(certificateRoot, "independent-result.json")),
      readFile(resolve(root, "research/r072b_exact_audit.py"), "utf8"),
      readFile(resolve(root, "research/r072b_independent_audit.py"), "utf8"),
    ]);

  for (const [label, result] of Object.entries({ producer, independent })) {
    assert.equal(result.release, "R0.72B", label);
    assert.equal(result.allPassed, true, label);
    assert.equal(result.checkCount, 9, label);
    assert.equal(result.passedCheckCount, 9, label);
    assert.equal(result.checks.length, 9, label);
    assert.ok(result.checks.every((row) => row.passed), label);
    assert.equal(result.arithmetic.intervalArithmetic, false, label);
    assert.equal(result.scope.provesNSERegularity, false, label);
    assert.equal(result.scope.constructsNormalizedLowerFamily, false, label);
  }

  assert.equal(independent.independence.importsProducer, false);
  assert.equal(independent.independence.readsProducerResult, false);
  assert.doesNotMatch(producerScript, /import\s+.*r072b_independent/);
  assert.doesNotMatch(
    independentScript,
    /(?:from|import)\s+.*r072b_exact|open\([^)]*(?:result|producer)/,
  );

  near(producer.constants.qRhoCauchyConstant, 3, 1e-70, "q_rho constant");
  assert.ok(Number(producer.constants.CcrossIdentityResidual) < 1e-70);
  near(
    producer.equalCarrierLedger.fittedTailPower,
    -10 / 3,
    3e-5,
    "producer equal-carrier power",
  );
  near(
    independent.equalCarrierLedger.fittedTailPower,
    -10 / 3,
    3e-5,
    "independent equal-carrier power",
  );
  near(
    producer.comparableAmplitudeLedger.fittedTailPower,
    -10 / 3,
    3e-5,
    "producer comparable-amplitude power",
  );
  near(
    independent.comparableAmplitudeLedger.fittedTailPower,
    -10 / 3,
    3e-5,
    "independent comparable-amplitude power",
  );

  const terminalEqual = producer.equalCarrierLedger.rows.at(-1);
  assert.equal(terminalEqual.M, 2 ** 20);
  near(terminalEqual.twoMChi, 1, 1e-38, "2M chi identity");
  near(
    terminalEqual.MToTenThirdsTimesPrefactor,
    3.4341361775614086,
    2e-14,
    "scaled canonical prefactor",
  );
  assert.ok(
    producer.comparableAmplitudeLedger.rows.every(
      (row) =>
        Number(row.chiOverUpper) <= 1 &&
        Number(row.multiplierRatioOverUpper) <= 1,
    ),
  );
  assert.ok(
    independent.comparableAmplitudeLedger.rows.every(
      (row) =>
        row.chiOverUpper <= 1 && row.multiplierRatioOverUpper <= 1,
    ),
  );

  const betaZero = producer.phaseBoundary.find((row) => row.beta === 0);
  const betaCap = producer.phaseBoundary.find((row) => row.beta === 2.5);
  near(
    betaZero.coherentMMinusTenThirds,
    10 / 7,
    2e-15,
    "fixed-layer coherent boundary",
  );
  near(
    betaCap.coherentMMinusTenThirds,
    5 / 2,
    2e-15,
    "coherent first-term cap",
  );

  assert.ok(independent.finiteTargetRow.rhoRelativeDefect < 2e-15);
  assert.ok(independent.finiteTargetRow.qIntegralOverReportedPayment < 0.1);
  near(
    independent.finiteTargetRow.qCauchyOverReportedPayment,
    1,
    3e-15,
    "independent Q Cauchy payment",
  );

  const bessel512 = producer.besselNoGo.rows.find((row) => row.R === 512);
  near(
    bessel512.ThetaLayerTimesFrozenRate,
    7.890686432459986e-5,
    2e-18,
    "Theta_512",
  );
  near(
    bessel512.heatFreezingXi,
    9.42977761740735e-6,
    2e-19,
    "Xi_512",
  );
  near(
    bessel512.energyLossUpper,
    0.020280111462214846,
    2e-16,
    "energy-loss upper bound at R=512",
  );
  assert.match(
    producer.besselNoGo.enhancedDissipationScope,
    /does not erase slope mass accumulated before burn-in/,
  );
  assert.match(
    independent.besselNoGo.enhancedDissipationScope,
    /pre-burn-in slope ledger remains part of the total/,
  );
});

test("verifies the complete R0.72B certificate checksum ledger", async () => {
  await verifyChecksumLedger(certificateRoot, 14);
});

test("archives and mirrors the formal R0.72B figure in three formats", async () => {
  const [manifest, validation, figureResults] = await Promise.all([
    readJson(resolve(figureRoot, "manifest.json")),
    readJson(resolve(figureRoot, "validation.json")),
    readJson(resolve(figureRoot, "results.json")),
  ]);

  assert.equal(manifest.release, "R0.72B");
  assert.equal(manifest.figureId, "R0.72B-1");
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.match(manifest.claimBoundary, /not interval arithmetic/);
  assert.match(manifest.claimBoundary, /cannot remove pre-burn-in slope mass/);

  assert.equal(validation.allPassed, true);
  assert.equal(validation.checkCount, 9);
  assert.equal(validation.passedCheckCount, 9);
  assert.ok(validation.checks.every((row) => row.passed));
  assert.equal(figureResults.rowCount, 567);
  assert.equal(figureResults.phaseBoundary.coherentFixedLayer, 10 / 7);
  assert.equal(figureResults.phaseBoundary.coherentCap, 5 / 2);
  assert.equal(figureResults.equalCarrier.normalizedGeometricPower, "-10/3");
  assert.equal(figureResults.equalCarrier.largestM, 2 ** 20);
  assert.equal(figureResults.bessel.largestR, 512);

  for (const asset of manifest.assets) {
    const path = resolve(figureRoot, asset.path);
    assert.equal((await stat(path)).size, asset.bytes, asset.path);
    assert.equal(await sha256(path), asset.sha256, asset.path);
  }
  await verifyChecksumLedger(figureRoot, 27);

  const minimumBytes = { pdf: 40_000, png: 400_000, svg: 90_000 };
  for (const extension of ["pdf", "png", "svg"]) {
    const archive = resolve(figureRoot, `figure.${extension}`);
    const mirror = resolve(
      publicRoot,
      `figures/r0-72b-row-coherence.${extension}`,
    );
    assert.ok((await stat(archive)).size > minimumBytes[extension], archive);
    assert.equal((await stat(mirror)).size, (await stat(archive)).size, mirror);
    assert.equal(await sha256(mirror), await sha256(archive), mirror);
  }
});

test("retains the R0.72B package while R0.72K is current", async () => {
  const [home, note, recap, literature, notePdf, recapPdf] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72b.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72b.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72b.pdf")),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72b.pdf")),
  ]);

  assert.match(home, /<strong>v1\.26<\/strong>网页版本/);
  assert.match(home, /<strong>163<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72M<\/strong>最新研究节点/);
  assert.match(home, /展开 73 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72N/);
  assert.match(home, /R0\.70A–R0\.72M 共 65 个版本已公开；41 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单/);
  assert.match(home, /二十八个(?:问题)?阶段/);
  assert.match(home, /累计回顾收录 103 个节点/);
  assert.equal((home.match(/href="\/notes\/r0-72b\.html"/g) ?? []).length, 2);
  assert.equal((home.match(/data-release="r072b"/g) ?? []).length, 1);
  assert.match(
    home,
    /<div class="task-one" id="r072b" data-release="r072b"/,
  );
  assert.match(home, /M\^{-10\/3\}/);
  assert.match(home, /recap-r0-61-r0-72m\.html/);

  assert.ok(note.includes(String.raw`G_{\rm all}^{\rm ex}`));
  assert.ok(note.includes(String.raw`M\rho_A^2`));
  assert.ok(
    note.includes(
      String.raw`C_\times=\frac{\pi}{\sqrt2\,45^{1/4}\nu d^2}`,
    ),
  );
  assert.ok(note.includes(String.raw`M^{-10/3}`));
  assert.ok(
    note.includes(
      String.raw`\alpha&lt;\min\left\{\frac52,\frac{10+3\beta}{7}\right\}`,
    ),
  );
  assert.match(note, /不能抹去 launch 以来已经累计的根质量/);
  assert.match(note, /terminal decay 不会消除 pre-ledger/);
  assert.match(note, /href="\/notes\/r0-72b\.pdf"/);
  assert.match(note, /\/figures\/r0-72b-row-coherence\.png/);
  assert.match(note, /\/figures\/r0-72b-row-coherence\.svg/);
  assert.match(note, /\/figures\/r0-72b-row-coherence\.pdf/);
  assert.match(note, /research\/certificates\/r072b/);

  assert.match(recap, /R0\.61–R0\.72B 的 92 节公开笔记/);
  assert.match(recap, /收录节点：92/);
  assert.match(recap, /R0\.70A–R0\.72B 完成版本/);
  assert.ok(
    recap.includes(
      String.raw`C_\times=\sqrt{C_\kappa/(2\kappa)}`,
    ),
  );
  assert.ok(recap.includes(String.raw`carrier prefactor 为 \(M^{-10/3}\)`));
  assert.match(recap, /不能把 92 个节点解释成对千禧年问题完成了某个比例/);
  const nodeIndexStart = recap.indexOf('<section id="node-index">');
  const nodeIndexEnd = recap.indexOf("</section>", nodeIndexStart);
  assert.ok(nodeIndexStart >= 0 && nodeIndexEnd > nodeIndexStart);
  const nodeIndex = recap.slice(nodeIndexStart, nodeIndexEnd);
  assert.equal(
    (nodeIndex.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length,
    92,
  );
  assert.match(recap, /href="\/recap-r0-61-r0-72b\.pdf"/);

  assert.match(literature, /R0\.72B 怎样接入 time-dependent shear literature/);
  assert.match(literature, /href="\/notes\/r0-72b\.html"/);
  assert.match(literature, /id="r072b-boundary"/);
  assert.match(literature, /10\.4310\/CMS\.2024\.v22\.n6\.a10/);
  assert.match(literature, /arxiv\.org\/abs\/2309\.15738/);
  assert.match(literature, /arxiv\.org\/abs\/2410\.05657/);
  assert.match(literature, /arxiv\.org\/abs\/2105\.12308/);
  assert.match(literature, /launch-inclusive root-slope ledger/);

  assert.match(home, /src="\/i18n-en\.js\?v=1\.26"/);
  assert.match(literature, /src="\/i18n-en\.js\?v=1\.26"/);
  assert.match(note, /src="\/i18n-en\.js\?v=1\.15"/);
  assert.match(recap, /src="\/i18n-en\.js\?v=1\.15"/);

  for (const [label, html] of Object.entries({
    homepage: home,
    note,
    recap,
    literature,
  })) {
    assert.doesNotMatch(
      html,
      /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
      label,
    );
  }

  for (const [label, pdf] of Object.entries({ notePdf, recapPdf })) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label);
    assert.ok(pdf.length > 10_000, label);
  }
});
