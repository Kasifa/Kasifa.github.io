import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readdir, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certRoot = resolve(root, "research/certificates/r072f");
const figureRoot = resolve(
  root,
  "figures/r072f-critical-log-window/fig-r072f-critical-log-window",
);
const publicRoot = resolve(root, "public");

async function readJson(path) {
  return JSON.parse(await readFile(path, "utf8"));
}

async function readNdjson(path) {
  return (await readFile(path, "utf8"))
    .trim()
    .split("\n")
    .map((line) => JSON.parse(line));
}

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

function releaseToActionRows(rows) {
  return new Map(rows.map((row) => [row.delta, row.actions]));
}

test("states the analytic R0.72F screen and its complete-root boundary", async () => {
  const [report, gapMatrix, independentAudit, literatureAudit] =
    await Promise.all([
      readFile(resolve(root, "research/r072f_report-source.md"), "utf8"),
      readFile(resolve(root, "research/r072f_gap_matrix.md"), "utf8"),
      readFile(resolve(root, "research/r072f_independent_audit.md"), "utf8"),
      readFile(resolve(root, "research/r072f_literature_audit.md"), "utf8"),
    ]);

  assert.match(report, /R0\.72F -- the critical-log initial-layer repair/);
  assert.match(
    report,
    /\\mathscr A_\{\\beta,\\gamma\}[\s\S]*\\frac1T\\int_a\^\{a\+T\}/,
  );
  assert.match(
    report,
    /0\\le\\beta<\\frac12[\s\S]*Leray energy inequality/,
  );
  assert.match(
    report,
    /\\left\\\{\\frac13<\\beta<\\frac12,[\s\S]*\\beta=\\frac13,[\s\S]*\\gamma\\ge1/,
  );
  assert.match(
    report,
    /w_\*\(s\)=s\^\{-1\/3\}\[1\+\\log\(1\/s\)\][\s\S]*=75/,
  );
  assert.match(
    report,
    /2a\+c\+\\beta>1[\s\S]*2a\+c\+\\beta=1[\s\S]*\\gamma\\ge1/,
  );
  assert.match(report, /The endpoint \\\(\\beta=0\\\) is separate/);
  assert.match(report, /Let \\\(\\theta\\ge0\\\)/);
  assert.match(report, /\\alpha=4\/9/);
  assert.match(report, /### Not proved[\s\S]*complete-root candidate/);
  assert.match(report, /R0\.72G should test \\\(w_\*\\\)/);
  assert.match(report, /### Not proved[\s\S]*Finite-time singularity or global regularity/);
  assert.doesNotMatch(report, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);

  for (const token of [
    "F11",
    "F12",
    "F20",
    "F21",
    "F22",
    "complete-root",
  ]) {
    assert.ok(gapMatrix.includes(token), token);
  }
  assert.match(independentAudit, /allRequiredChecksPassed: true/);
  assert.match(independentAudit, /不是区间算术证明/);
  assert.match(independentAudit, /selected roots[\s\S]*complete roots/);
  assert.match(literatureAudit, /有界一手文献非碰撞审计/);
  assert.match(literatureAudit, /原创性或优先权[\s\S]*独立的系统检索/);
});

test("keeps the producer and independent R0.72F certificates genuinely separate", async () => {
  const [producer, independent, config, producerScript, independentScript,
    producerProgress, producerResource, independentProgress,
    independentResource] = await Promise.all([
    readJson(resolve(certRoot, "result.json")),
    readJson(resolve(certRoot, "independent-result.json")),
    readJson(resolve(certRoot, "config.json")),
    readFile(resolve(root, "research/r072f_exact_audit.py"), "utf8"),
    readFile(resolve(root, "research/r072f_independent_audit.py"), "utf8"),
    readNdjson(resolve(certRoot, "producer-progress.ndjson")),
    readNdjson(resolve(certRoot, "producer-resource.ndjson")),
    readNdjson(resolve(certRoot, "independent-progress.ndjson")),
    readNdjson(resolve(certRoot, "independent-resource.ndjson")),
  ]);

  assert.equal(producer.auditId, "R0.72F-critical-log-producer");
  assert.equal(producer.schemaVersion, "r072f-producer-audit-v1");
  assert.equal(producer.allRequiredChecksPassed, true);
  assert.ok(producer.checks.every((row) => row.passed));
  assert.equal(producer.scope.intervalArithmetic, false);
  assert.equal(producer.scope.completeRootUpperBound, false);
  assert.equal(producer.scope.provesNSERegularity, false);

  assert.equal(independent.auditId, "R0.72F-critical-log-independent");
  assert.equal(independent.schemaVersion, "r072f-independent-audit-v1");
  assert.equal(independent.allRequiredChecksPassed, true);
  assert.ok(independent.checks.every((row) => row.passed));
  assert.equal(independent.scope.importsProducer, false);
  assert.equal(independent.scope.readsProducerOutput, false);
  assert.equal(independent.scope.intervalArithmetic, false);
  assert.equal(independent.scope.completeRootUpperBound, false);
  assert.equal(independent.scope.provesNSERegularity, false);

  assert.equal(config.analyticModel.fixedQ0, 4);
  assert.equal(config.analyticModel.criticalWeightL2Squared, 75);
  assert.match(config.analyticModel.criticalWeight, /s\^\(-1\/3\)/);
  assert.match(
    config.analyticModel.positiveBetaRawFrontier,
    /2\*a\+c\+beta>1/,
  );
  assert.match(config.analyticModel.betaZeroRawFrontier, /2\*a\+c>=1/);
  assert.match(
    config.analyticModel.positiveBetaWeightedAtomFrontier,
    /3\*alpha\/4/,
  );
  assert.match(
    config.analyticModel.betaZeroWeightedAtomFrontier,
    /3\*alpha\/4/,
  );
  assert.deepEqual(config.producer.deltas, [16, 32, 64, 128, 256, 512]);
  assert.deepEqual(config.independent.deltas, config.producer.deltas);

  assert.doesNotMatch(
    producerScript,
    /(?:from|import)\s+.*r072f_independent_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /(?:from|import)\s+.*r072f_exact_audit/,
  );
  assert.doesNotMatch(
    independentScript,
    /certificates\/r072f\/(?:result|producer)/,
  );

  const producerRows = releaseToActionRows(producer.weightedActionRows);
  const independentRows = releaseToActionRows(independent.weightedActionRows);
  assert.deepEqual([...producerRows.keys()], [16, 32, 64, 128, 256, 512]);
  assert.deepEqual([...independentRows.keys()], [...producerRows.keys()]);
  let maximumRelativeDifference = 0;
  for (const [delta, producerActions] of producerRows) {
    const independentActions = independentRows.get(delta);
    assert.ok(independentActions, "independent row delta=" + delta);
    for (const [label, producerValue] of Object.entries(producerActions)) {
      const independentValue = independentActions[label];
      const relative = Math.abs(producerValue - independentValue) /
        Math.max(Math.abs(producerValue), Math.abs(independentValue));
      maximumRelativeDifference = Math.max(maximumRelativeDifference, relative);
    }
  }
  assert.ok(maximumRelativeDifference < 5e-4);
  assert.ok(Math.abs(maximumRelativeDifference - 0.0004758500247706425) < 1e-14);
  assert.equal(
    producer.checks.find((row) => row.name === "critical_weight_l2_identity")
      .value,
    75,
  );
  assert.equal(independent.criticalWeightL2.value, 75);
  assert.ok(
    producer.checks.find((row) => row.name === "fine_coarse_stability").value <
      0.0013,
  );
  assert.ok(
    independent.checks.find((row) => row.name === "quadrature_pressure").value <
      2e-8,
  );

  for (const log of [producerProgress, independentProgress]) {
    assert.equal(log[0].stage, "start");
    assert.equal(log.at(-1).stage, "complete");
    assert.equal(log.at(-1).passed, true);
  }
  for (const log of [producerResource, independentResource]) {
    assert.ok(log.length >= 10);
    assert.ok(log.every((row) => Number.isFinite(row.elapsedSeconds)));
  }
});

test("archives and mirrors the formal R0.72F journal figure", async () => {
  const [manifest, validation, config, contract, results] = await Promise.all([
    readJson(resolve(figureRoot, "manifest.json")),
    readJson(resolve(figureRoot, "validation.json")),
    readJson(resolve(figureRoot, "config.json")),
    readJson(resolve(figureRoot, "contract.json")),
    readJson(resolve(figureRoot, "results.json")),
  ]);

  assert.equal(manifest.schemaVersion, "r072f-figure-manifest-v1");
  assert.equal(manifest.release, "R0.72F");
  assert.equal(manifest.figureId, "R0.72F-1");
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(manifest.dataSummary.criticalWeightL2Squared, 75);
  assert.equal(manifest.dataSummary.maximumRelativeCrossAuditGap,
    0.0004758500247706425);
  assert.deepEqual(manifest.dataSummary.panelCounts, { A: 10, B: 18, C: 3 });
  assert.equal(manifest.dataSummary.rowCount, 31);
  assert.equal(manifest.dataSummary.rootAtomChangesLHS, true);
  assert.match(manifest.claimBoundary, /complete-root upper bound/);
  assert.match(manifest.claimBoundary, /Millennium-problem solution/);

  assert.equal(validation.schemaVersion, "r072f-figure-validation-v1");
  assert.equal(validation.allPassed, true);
  assert.equal(validation.checkCount, 19);
  assert.equal(validation.passedCheckCount, 19);
  assert.equal(validation.checks.length, 19);
  assert.ok(validation.checks.every((row) => row.passed));
  assert.equal(
    validation.checks.find((row) => row.name === "public assets are byte-identical")
      .value.pdf,
    true,
  );

  assert.equal(config.release, "R0.72F");
  assert.equal(config.figure.widthMillimetres, 178);
  assert.equal(config.figure.heightMillimetres, 94);
  assert.equal(config.figure.pngDpi, 600);
  assert.equal(contract.release, "R0.72F");
  assert.equal(contract.widthMm, 178);
  assert.equal(contract.pngDpi, 600);
  assert.deepEqual(contract.outputs, ["figure.pdf", "figure.svg", "figure.png"]);
  assert.equal(results.rowCount, 31);
  assert.deepEqual(results.panelCounts, { A: 10, B: 18, C: 3 });
  assert.equal(results.panels.C.rootAtomChangesLHS, true);

  for (const asset of manifest.assets) {
    const archived = await readFile(resolve(figureRoot, asset.path));
    assert.equal(archived.length, asset.bytes, asset.path + ": byte count");
    assert.equal(sha256(archived), asset.sha256, asset.path + ": sha256");
  }
  for (const source of manifest.sourceFiles) {
    const archived = await readFile(resolve(root, source.path));
    assert.equal(sha256(archived), source.sha256, source.path + ": lineage");
  }

  for (const extension of ["pdf", "svg", "png"]) {
    const [archived, published] = await Promise.all([
      readFile(resolve(figureRoot, "figure." + extension)),
      readFile(
        resolve(publicRoot, "figures/r0-72f-critical-log-window." + extension),
      ),
    ]);
    assert.equal(Buffer.compare(archived, published), 0, extension);
  }
  const [pdf, svg, png] = await Promise.all([
    readFile(resolve(figureRoot, "figure.pdf")),
    readFile(resolve(figureRoot, "figure.svg"), "utf8"),
    readFile(resolve(figureRoot, "figure.png")),
  ]);
  assert.equal(pdf.subarray(0, 4).toString(), "%PDF");
  assert.match(svg, /<svg/);
  assert.deepEqual([...png.subarray(0, 8)], [137, 80, 78, 71, 13, 10, 26, 10]);
});

test("retains R0.72F after R0.72J advances the synchronized site counts", async () => {
  const [home, note, recap, literature, releaseManifest, archiveInventory,
    siteVersion, noteFiles] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72f.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72j.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    readJson(resolve(root, "research/release-manifest.json")),
    readJson(resolve(root, "research/formal-archive-inventory.json")),
    readJson(resolve(publicRoot, "site-version.json")),
    readdir(resolve(publicRoot, "notes")),
  ]);

  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 160);
  assert.match(home, /<html lang="zh-CN" data-site-version="1\.23">/);
  assert.match(home, /<strong>v1\.23<\/strong>网页版本/);
  assert.match(home, /<strong>160<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72J<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72J<\/span>/);
  assert.match(home, /展开 70 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72K/);
  assert.match(home, /累计回顾收录 100 个节点；全站现有 160 篇公开研究笔记/);
  assert.match(home, /62 个版本已公开/);
  assert.match(home, /38 个按当前 formal-figure 合同完整封存|38 个完整封存/);
  assert.match(home, /24 个旧版附图档案仍列入回补清单/);
  assert.doesNotMatch(home, /60 个已公开并封存版本/);
  assert.equal((home.match(/href="\/notes\/r0-72f\.html"/g) ?? []).length, 2);
  assert.equal((home.match(/data-release="r072f"/g) ?? []).length, 1);

  assert.match(note, /研究笔记 R0\.72F/);
  assert.match(note, /\\|w_\*\\|_2\^2=75/);
  assert.match(note, /complete-root estimate: OPEN/);
  assert.match(note, /R0\.72G 只检查完整根/);
  assert.match(note, /r0-72f-critical-log-window\.svg/);
  assert.match(note, /research\/certificates\/r072f/);
  assert.match(note, /href="\/recap-r0-61-r0-72f\.html"/);

  assert.match(recap, /R0\.61–R0\.72J 的 100 节公开笔记/);
  assert.match(recap, /回顾截止时公开笔记：160/);
  assert.match(recap, /R0\.70A–R0\.72J 已公开版本/);
  assert.match(recap, /38<\/strong><span>当前 formal-figure 合同下完整封存/);
  assert.match(recap, /24<\/strong><span>旧版 formal-figure 档案待回补/);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 26);
  assert.match(recap, /R0\.72F(?:–R0\.72G)? · 临界对数/);
  assert.match(recap, /R0\.72H/);

  assert.match(literature, /R0\.69P–R0\.72J/);
  assert.match(literature, /id="r072f-boundary"/);
  assert.match(literature, /href="\/notes\/r0-72f\.html"/);
  assert.match(literature, /开放接口 · R0\.72K/);
  assert.match(literature, /bounded non-collision check/);

  assert.equal(releaseManifest.latestCompletedRelease, "r072j");
  assert.equal(releaseManifest.siteVersion, "1.23");
  assert.equal(releaseManifest.publicHtmlNoteCount, 160);
  assert.equal(releaseManifest.postR060RecapNodeCount, 100);
  assert.equal(releaseManifest.postR070APublishedReleaseCount, 62);
  assert.equal(releaseManifest.postR070AFormalSealedReleaseCount, 38);
  assert.equal(releaseManifest.legacyFormalFigureBacklogCount, 24);
  assert.equal(releaseManifest.nextRelease, "r072k");
  assert.equal(
    releaseManifest.latestReleaseGate,
    "tests/r072j-mixed-parity-gate.test.mjs",
  );
  assert.equal(archiveInventory.latestPublishedRelease, "r072j");
  assert.equal(archiveInventory.publishedReleaseCount, 62);
  assert.equal(archiveInventory.formalSealedReleaseCount, 38);
  assert.equal(archiveInventory.legacyFormalFigureBacklogCount, 24);
  assert.equal(siteVersion.version, "1.23");
  assert.equal(siteVersion.latestRelease, "R0.72J");
  assert.equal(siteVersion.publicHtmlNoteCount, 160);

  for (const page of [home, recap, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.23"/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  }
  assert.match(note, /src="\/i18n-en\.js\?v=1\.19"/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
});
