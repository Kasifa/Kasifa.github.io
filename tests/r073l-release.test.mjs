import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readdir, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { containsChinese, extractProtectedTokens } from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const bytes = (relative) => readFile(resolve(root, relative));
const sha256 = (payload) => createHash("sha256").update(payload).digest("hex");

const figureId = "fig-r073l-adiabatic-tracking";
const figureRoot = "figures/r073l/" + figureId;
const mirrorRoot = "public/" + figureRoot;
const publicFigureRoot = "public/assets/r073l/" + figureId;
const figureFiles = [
  "README.md", "SHA256SUMS", "caption.md", "command.txt", "config.json",
  "contract.json", "environment.json", "figure.pdf", "figure.png", "figure.svg",
  "manifest.json", "plot.py", "progress.ndjson", "qa-final-size.png",
  "qa-grayscale.png", "qa-pdf.png", "qa-protocol.md", "qa-report.md",
  "requirements.txt", "resource-log.ndjson", "results.json", "source-data.csv",
  "validate.py", "validation.json",
];
const publicPages = {
  note: "public/notes/r0-73l.html",
  recap: "public/recap-r0-61-r0-73l.html",
  home: "public/research-review.html",
  literature: "public/literature-review.html",
  index: "public/notes/index.html",
};
const target = {
  version: "1.52",
  latest: "r073l",
  notes: 188,
  recap: 128,
  published: 90,
  sealed: 66,
  backlog: 24,
  next: "r073m",
};
const closedClaims = [
  "commonDomainEvolution=CLOSED",
  "katoIntertwining=CLOSED",
  "movingComplementRelativeStability=CLOSED",
  "nonselfadjointAdiabaticTracking=CLOSED",
  "matchingSelectedGainAction=CLOSED",
  "actionResolvedBackwardLocalization=CLOSED",
];
const finiteClaims = [
  "finiteDiagnosticPackage=CLOSED",
  "primaryAdiabaticCases=15",
  "independentFiniteReconstruction=PASS",
  "formalFigurePackage=PASS",
  "finiteDimensionDoesNotCertifyContinuum=TRUE",
];
const openClaims = [
  "explicitAdiabaticThreshold=OPEN",
  "prefactorLimit=OPEN",
  "twoTermWKB=OPEN",
  "nonlinearNavierStokes=OPEN",
  "transverseThreeDimensionalClosure=OPEN",
  "finiteTimeSingularity=OPEN",
  "Clay=OPEN",
];
const forbidden = [
  "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  "颠覆性", "世界首个", "接近解决", "解决了千禧年", "证明了全局正则性",
  "原创性定理", "首次证明",
];

function assertPublicVoice(value, label) {
  for (const phrase of forbidden) {
    assert.equal(value.includes(phrase), false, label + ": " + phrase);
  }
  assert.doesNotMatch(
    value,
    /\b(?:we|our|ours|ourselves|us)\b/i,
    label + ": collective English voice",
  );
}

function machineLedgerAssignments(value) {
  return [...value.matchAll(/\b([A-Za-z][A-Za-z0-9]*)=([A-Z0-9][A-Z0-9_]*)\b/g)]
    .map((match) => match[0]);
}

function recapNodes(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start, "recap node-index section");
  return [...recap.slice(start, end).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
}

function decodeUtf16Be(payload) {
  const start = payload[0] === 0xfe && payload[1] === 0xff ? 2 : 0;
  assert.equal((payload.length - start) % 2, 0, "even UTF-16BE byte count");
  const littleEndian = Buffer.alloc(payload.length - start);
  for (let index = start; index < payload.length; index += 2) {
    littleEndian[index - start] = payload[index + 1];
    littleEndian[index - start + 1] = payload[index];
  }
  return littleEndian.toString("utf16le");
}

async function assertPdf(relative, expectedTitle) {
  const value = await bytes(relative);
  assert.ok(value.length > 10_000, relative + ": substantive PDF");
  assert.equal(value.subarray(0, 4).toString(), "%PDF", relative);
  const match = value.toString("latin1").match(/\/Title\s*<([0-9A-Fa-f]+)>/);
  assert.ok(match, relative + ": hexadecimal PDF title metadata");
  assert.equal(decodeUtf16Be(Buffer.from(match[1], "hex")), expectedTitle, relative);
}

test("R0.73L pins the v1.52 accounting endpoint", async () => {
  const [release, site, inventory, version, inventoryBytes] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    json("research/formal-archive-inventory.json"),
    text("VERSION"),
    bytes("research/formal-archive-inventory.json"),
  ]);
  assert.deepEqual({
    version: release.siteVersion,
    latest: release.latestCompletedRelease,
    notes: release.publicHtmlNoteCount,
    recap: release.postR060RecapNodeCount,
    published: release.postR070APublishedReleaseCount,
    sealed: release.postR070AFormalSealedReleaseCount,
    backlog: release.legacyFormalFigureBacklogCount,
    next: release.nextRelease,
  }, target);
  assert.equal(
    release.latestReleaseGate,
    "tests/r073l-adiabatic-tracking-gate.test.mjs",
  );
  assert.equal(release.latestReleasePublicationTest, "tests/r073l-release.test.mjs");
  assert.deepEqual(release.formalArchiveInventory, {
    path: "research/formal-archive-inventory.json",
    sha256: sha256(inventoryBytes),
  });
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.52",
    latestRelease: "R0.73L",
    publicHtmlNoteCount: 188,
    publishedDate: "2026-08-31",
  });
  assert.deepEqual({
    latest: inventory.latestPublishedRelease,
    published: inventory.publishedReleaseCount,
    sealed: inventory.formalSealedReleaseCount,
    backlog: inventory.legacyFormalFigureBacklogCount,
  }, { latest: "r073l", published: 90, sealed: 66, backlog: 24 });
  assert.equal(inventory.publishedReleases.length, 90);
  assert.equal(inventory.formalSealedReleases.length, 66);
  assert.equal(inventory.publishedReleases.at(-1), "r073l");
  assert.equal(inventory.formalSealedReleases.at(-1), "r073l");
  assert.equal(version, "1.52\n");
});

test("R0.73L five-page route and exact claim boundary are complete", async () => {
  const [note, recap, home, literature, index] =
    await Promise.all(Object.values(publicPages).map(text));
  for (const [label, value] of Object.entries({ note, recap, home, literature, index })) {
    assert.ok(value.includes("R0.73L"), label + ": release label");
    assert.ok(value.includes("/i18n-en.js?v=1.52"), label + ": i18n v1.52");
    assertPublicVoice(value, label + " HTML");
  }

  for (const token of [
    ...closedClaims,
    ...finiteClaims,
    ...openClaims,
    "NOT CLAY",
    "1/450",
    "0.12",
    "0.16",
    "15 条主轨迹",
    "0.9993290525",
    "0.9998284900",
    "1.0281276",
    "6.711726",
    "R0.73M",
  ]) assert.ok(note.includes(token), "note token " + token);
  for (const href of [
    "/notes/r0-73l.pdf",
    "/recap-r0-61-r0-73l.html",
    "/recap-r0-61-r0-73l.pdf",
    "/assets/r073l/" + figureId + ".pdf",
    "/assets/r073l/" + figureId + ".svg",
    "/assets/r073l/" + figureId + ".png",
  ]) assert.ok(note.includes(`href="${href}"`), "note link " + href);

  const nodes = recapNodes(recap);
  assert.equal(nodes.length, 128);
  assert.equal(new Set(nodes).size, 128);
  assert.equal(nodes[0], "r0-61");
  assert.equal(nodes.at(-1), "r0-73l");
  assert.equal(recap.match(/<article class="phase">/g)?.length, 47);
  assert.ok(recap.includes("回顾截止节点：R0.73L"));
  assert.ok(recap.includes("R0.70A–R0.73L 的 90 节已公开"));
  assert.ok(recap.includes("66 节完整封存"));
  assert.ok(recap.includes("24 节旧档待回补"));
  for (const token of [...closedClaims, ...finiteClaims, ...openClaims, "R0.73M"]) {
    assert.ok(recap.includes(token), "recap token " + token);
  }

  assert.ok(home.includes("LATEST RELEASE · R0.73L"));
  assert.ok(home.includes("当前端点 R0.73L"));
  assert.ok(home.includes("NEXT · R0.73M"));
  assert.ok(home.includes('data-release="r073l"'));
  assert.ok(home.includes("15 条主轨迹、5 条独立重算、346 行附图源数据"));
  assert.equal(home.match(/data-release="r073l"/g)?.length, 1);
  const route = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.73L">([\s\S]*?)<\/nav>/,
  );
  assert.ok(route, "R0.69P--R0.73L route block");
  const routeLinks = [...route[1].matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(routeLinks.length, 98);
  assert.equal(new Set(routeLinks).size, 98);
  assert.equal(routeLinks.at(-1), "r0-73l");

  assert.ok(literature.includes('id="r073l-boundary"'));
  assert.ok(literature.includes('class="route-r073l-deck-update"'));
  assert.ok(literature.includes("开放接口 · R0.73M"));
  for (const token of [...closedClaims, ...finiteClaims, ...openClaims]) {
    assert.ok(literature.includes(token), "literature token " + token);
  }
  for (let number = 167; number <= 172; number += 1) {
    assert.equal(
      [...literature.matchAll(new RegExp('id="ref-' + number + '"', "g"))].length,
      1,
      "ref-" + number,
    );
  }
  const literatureIds = [...literature.matchAll(/\bid="([^"]+)"/g)]
    .map((match) => match[1]);
  assert.equal(new Set(literatureIds).size, literatureIds.length, "literature ids unique");

  assert.ok(index.includes('data-site-version="1.52"'));
  assert.ok(index.includes('data-note="r0-73l"'));
  assert.ok(index.includes("188 篇公开研究笔记"));
  assert.ok(index.includes('href="/notes/r0-73l.html"'));
  assert.ok(index.includes('href="/notes/r0-73l.pdf"'));
  assert.ok(index.includes('href="/recap-r0-61-r0-73l.html"'));
});

test("R0.73L sealed finite package contains 15 primary and 5 independent cases", async () => {
  const [manifest, primary, independent, validation] = await Promise.all([
    json("experiments/r073l/manifest.json"),
    json("experiments/r073l/adiabatic_diagnostic.json"),
    json("experiments/r073l/independent_validation.json"),
    json("experiments/r073l/package_validation.json"),
  ]);
  assert.equal(manifest.schemaVersion, "r073l-finite-diagnostic-manifest-v1");
  assert.equal(manifest.release, "R0.73L");
  assert.equal(manifest.status, "sealed");
  assert.ok(Object.values(manifest.checks).every(Boolean));
  assert.deepEqual(manifest.claimBoundary, {
    clayProblemSolved: false,
    continuumTheoremCertifiedByManifest: false,
    finiteDimensionalDiagnosticSealed: true,
  });

  assert.equal(primary.schemaVersion, "r073l-adiabatic-diagnostic-v1");
  assert.equal(primary.status, "passed");
  assert.equal(primary.allChecksPass, true);
  assert.ok(Object.values(primary.checks).every(Boolean));
  assert.equal(primary.cases.length, 15);
  assert.equal(primary.crossCutoffComparisons.length, 10);
  assert.equal(primary.claimBoundary.finiteScalingIsContinuumProof, false);
  assert.equal(primary.claimBoundary.finiteCutoffAgreementIsContinuumProof, false);
  assert.equal(primary.claimBoundary.clayProblemSolved, false);
  assert.ok(primary.maximums.backwardActionResidualAbs < 6.72e-4);
  assert.ok(primary.maximums.largestPairTerminalNormalizedGainDifference < 7.0e-15);
  assert.ok(primary.maximums.largestPairTerminalLeakageRatioDifference < 3.2e-15);
  assert.ok(
    Math.abs(
      primary.epsilonScalingByCutoff["64"].terminalLeakageTailThreeLogLogSlope
      - 1.0281276356834264,
    ) < 1e-13,
  );
  assert.deepEqual(
    primary.epsilonScalingByCutoff["64"].terminalNormalizedGainRange,
    [0.9993290525496814, 0.9998284900372003],
  );

  assert.equal(independent.schemaVersion, "r073l-independent-validation-v1");
  assert.equal(independent.status, "passed");
  assert.equal(independent.allChecksPass, true);
  assert.equal(independent.method, "piecewise midpoint matrix-exponential product");
  assert.equal(independent.cases.length, 5);
  assert.ok(Object.values(independent.checks).every(Boolean));
  assert.deepEqual(independent.claimBoundary, {
    continuumProof: false,
    independentFiniteReconstruction: true,
  });
  assert.ok(independent.maximums.finestVsPrimaryNormalizedGain < 1.9e-9);
  assert.ok(independent.maximums.finestVsPrimaryLeakage < 1.8e-9);
  assert.ok(independent.maximums.lastTwoNormalizedGain < 5.6e-9);
  assert.ok(independent.maximums.lastTwoLeakage < 5.2e-9);

  assert.equal(validation.schemaVersion, "r073l-package-validation-v1");
  assert.equal(validation.status, "passed");
  assert.equal(validation.allChecksPass, true);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.deepEqual(
    [validation.details.checksumFiles, validation.details.manifestFiles],
    [16, 15],
  );
});

test("R0.73L formal figure binds 346 rows and byte-identical public mirrors", async () => {
  const [manifest, results, validation, entries, ledgerText] = await Promise.all([
    json(figureRoot + "/manifest.json"),
    json(figureRoot + "/results.json"),
    json(figureRoot + "/validation.json"),
    readdir(resolve(root, figureRoot), { withFileTypes: true }),
    text(figureRoot + "/SHA256SUMS"),
  ]);
  assert.equal(manifest.schemaVersion, "r073l-adiabatic-tracking-figure-manifest-v1");
  assert.equal(manifest.release, "R0.73L");
  assert.equal(manifest.figureId, figureId);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.qa.status, "passed");
  for (const key of [
    "finalSizeInspected", "grayscaleInspected", "labelsAndLegendsInspected",
    "scalesAndUnitsInspected", "dataCrossChecked",
  ]) assert.equal(manifest.qa[key], true, "manifest QA " + key);
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.equal(manifest.publication.byteIdentityRequired, true);
  assert.equal(manifest.publication.assets.length, 3);
  assert.equal(manifest.claimBoundary.finiteDimensionalDiagnostic, true);
  assert.equal(manifest.claimBoundary.continuumAdiabaticTheoremCertifiedByFigure, false);
  assert.equal(manifest.claimBoundary.explicitContinuumEpsilonThresholdCertified, false);
  assert.equal(manifest.claimBoundary.nonlinearNavierStokesCertified, false);
  assert.equal(manifest.claimBoundary.clayProblemSolved, false);

  assert.equal(results.schemaVersion, "r073l-figure-results-v1");
  assert.equal(results.status, "passed");
  assert.equal(results.allChecksPass, true);
  assert.equal(results.sourceRows, 346);
  assert.equal(results.summary.maximumBackwardActionResidualAbs, 0.0006711726362969017);
  assert.equal(results.summary.tailThreeLeakageSlope, 1.0281276356834264);
  assert.deepEqual(
    results.summary.terminalNormalizedGainRange,
    [0.9993290525496814, 0.9998284900372003],
  );
  assert.equal(results.summary.validationMetrics.length, 6);
  assert.ok(results.summary.validationMetrics.every((row) => row.ratioToTolerance < 1));

  assert.equal(validation.schemaVersion, "r073l-figure-validation-v1");
  assert.equal(validation.status, "passed");
  assert.equal(validation.allChecksPass, true);
  assert.equal(Object.keys(validation.checks).length, 7);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.deepEqual(validation.details.sourceRows, {
    display_trajectory: 325,
    terminal_case: 15,
    validation_metric: 6,
  });
  assert.equal(Object.values(validation.details.sourceRows).reduce((a, b) => a + b, 0), 346);
  assert.deepEqual(validation.details.exports.pngPixels, [4204, 3023]);
  assert.equal(validation.details.exports.pdfPages, 1);
  assert.equal(validation.details.exports.svgRasterImages, 0);

  const actualFiles = entries.filter((entry) => entry.isFile()).map((entry) => entry.name).sort();
  assert.deepEqual(actualFiles, [...figureFiles].sort());
  const ledger = ledgerText.trim().split("\n");
  assert.equal(ledger.length, figureFiles.length - 1);
  const ledgerNames = [];
  for (const row of ledger) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, "figure ledger row " + row);
    ledgerNames.push(match[2]);
    assert.equal(sha256(await bytes(figureRoot + "/" + match[2])), match[1], match[2]);
  }
  assert.deepEqual(ledgerNames, actualFiles.filter((name) => name !== "SHA256SUMS"));

  for (const name of figureFiles) {
    assert.deepEqual(
      await bytes(mirrorRoot + "/" + name),
      await bytes(figureRoot + "/" + name),
      "archive mirror " + name,
    );
  }
  const outputs = new Map(manifest.figure.outputs.map((row) => [row.path, row]));
  const assets = new Map(
    manifest.publication.assets.map((row) => [row.path.split(".").at(-1), row]),
  );
  for (const suffix of ["pdf", "svg", "png"]) {
    const source = await bytes(figureRoot + "/figure." + suffix);
    const published = await bytes(publicFigureRoot + "." + suffix);
    assert.deepEqual(published, source, suffix + " public master");
    assert.equal(outputs.get("figure." + suffix).sha256, sha256(source));
    assert.equal(assets.get(suffix).sha256, sha256(source));
    assert.equal(assets.get(suffix).path, publicFigureRoot + "." + suffix);
  }
});

test("R0.73L synchronized note/recap PDFs are cryptographically bound", async () => {
  const noteTitle = "R0.73L｜Parameter-uniform nonselfadjoint adiabatic tracking";
  const recapTitle = "R0.61–R0.73L｜R0.60 之后的研究回顾";
  await assertPdf("public/notes/r0-73l.pdf", noteTitle);
  await assertPdf("public/recap-r0-61-r0-73l.pdf", recapTitle);

  const binding = await json("research/r073l_pdf_bindings.json");
  assert.equal(binding.schemaVersion, "r073l-synchronized-pdf-bindings-v1");
  assert.equal(binding.release, "R0.73L");
  assert.deepEqual(
    binding.documents.map((row) => ({
      kind: row.kind,
      html: row.html.path,
      pdf: row.pdf.path,
      title: row.pdf.title,
    })),
    [
      {
        kind: "research-note",
        html: "public/notes/r0-73l.html",
        pdf: "public/notes/r0-73l.pdf",
        title: noteTitle,
      },
      {
        kind: "cumulative-recap",
        html: "public/recap-r0-61-r0-73l.html",
        pdf: "public/recap-r0-61-r0-73l.pdf",
        title: recapTitle,
      },
    ],
  );
  for (const row of binding.documents) {
    for (const record of [row.html, row.pdf]) {
      const payload = await bytes(record.path);
      assert.equal(payload.length, record.bytes, record.path + ": bytes");
      assert.equal(sha256(payload), record.sha256, record.path + ": sha256");
    }
  }
  const check = spawnSync(
    process.execPath,
    ["scripts/bind-r073l-pdfs.mjs", "--check-only"],
    { cwd: root, encoding: "utf8" },
  );
  assert.equal(check.status, 0, check.stderr);
});

test("R0.73L translations, snapshot, browser bundle, and terminology source agree", async () => {
  const [translations, snapshot, bundle, dictionary, ...htmlPages] = await Promise.all([
    json("translations/en.json"),
    json("scripts/i18n-snapshots/r073l-missing.json"),
    text("public/i18n-en.js"),
    text("research/r073l_bilingual_dictionary.md"),
    ...Object.values(publicPages).map(text),
  ]);
  const rows = translations.filter((entry) => /^r073l\d{3}$/.test(entry.id));
  assert.ok(rows.length > 0, "R0.73L translation rows");
  assert.equal(rows.length, snapshot.length);
  assert.equal(new Set(rows.map((entry) => entry.id)).size, rows.length);
  assert.equal(new Set(rows.map((entry) => entry.zh)).size, rows.length);
  assert.deepEqual(
    rows.map(({ zh, en }) => ({ zh, en })),
    snapshot,
    "translation snapshot order and values",
  );
  for (const [index, entry] of rows.entries()) {
    const label = "R0.73L translation row " + String(index + 1);
    assert.equal(entry.id, "r073l" + String(index + 1).padStart(3, "0"), label + ": id");
    assert.ok(typeof entry.en === "string" && entry.en.trim(), label + ": English");
    assert.equal(containsChinese(entry.en), false, label + ": Chinese in English");
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i, label);
    assert.deepEqual(
      extractProtectedTokens(entry.en),
      extractProtectedTokens(entry.zh),
      label + ": protected tokens",
    );
    assert.deepEqual(
      machineLedgerAssignments(entry.en),
      machineLedgerAssignments(entry.zh),
      label + ": machine ledgers",
    );
    assert.ok(
      bundle.includes(JSON.stringify(entry.zh) + ": " + JSON.stringify(entry.en)),
      label + ": browser bundle",
    );
  }
  assertPublicVoice(JSON.stringify(rows), "R0.73L translations");
  for (const [index, value] of htmlPages.entries()) {
    assertPublicVoice(value, "public HTML " + String(index + 1));
  }
  for (const token of [
    "R0.73L", "parameter-uniform nonselfadjoint adiabatic tracking",
    "Kato correction", "fixed fast-time block", "forward Volterra system",
    "bounded two-sided prefactor", "forward-orbit localization",
    ...closedClaims, ...finiteClaims, ...openClaims,
  ]) assert.ok(dictionary.includes(token), "terminology token " + token);
  assert.doesNotMatch(dictionary, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  assertPublicVoice(dictionary, "R0.73L terminology source");

  const check = spawnSync(
    process.execPath,
    ["scripts/add-r073l-translations.mjs", "--check-only"],
    { cwd: root, encoding: "utf8" },
  );
  assert.equal(check.status, 0, check.stderr);
});

test("R0.73L release generator pins the correct mathematical and publication gates", async () => {
  const generator = await text("scripts/generate_r073l_release.py");
  const block = generator.match(/RELEASE_SOURCE_EXACT_PATHS = \(\n([\s\S]*?)\n\)/);
  assert.ok(block, "RELEASE_SOURCE_EXACT_PATHS block");
  const pinned = [...block[1].matchAll(/^\s+"([^"]+)",$/gm)]
    .map((match) => match[1]);
  for (const relative of [
    "scripts/r073l_release_content.py",
    "scripts/add-r073l-translations.mjs",
    "scripts/generate_r073l_release.py",
    "scripts/bind-r073l-pdfs.mjs",
    "tests/r073l-adiabatic-tracking-gate.test.mjs",
    "tests/r073l-release.test.mjs",
    "tests/site-route-current-boundary.test.mjs",
  ]) assert.ok(pinned.includes(relative), "release-source pin " + relative);
  assert.equal(
    pinned.some((relative) => relative.includes("r073l-uniform-viscous-branch")),
    false,
  );
  for (const name of [
    "ANALYTIC_SOURCE_COMMIT", "EXPERIMENT_PACKAGE_COMMIT", "FIGURE_PACKAGE_COMMIT",
    "RELEASE_BASELINE_COMMIT", "RELEASE_SOURCE_COMMIT",
  ]) assert.match(generator, new RegExp(name + ' = "[0-9a-f]{40}"'));
  assert.match(
    generator,
    /normalized_release_generator\(git_bytes\(RELEASE_SOURCE_COMMIT, generator_relative\)\)/,
  );
});
