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

const certificateRoot = "research/certificates/r073m";
const figureId = "fig-r073m-prescribed-action-departure";
const figureRoot = `figures/r073m/${figureId}`;
const mirrorRoot = `public/${figureRoot}`;
const publicFigureRoot = `public/assets/r073m/${figureId}`;
const figureFiles = [
  "README.md", "SHA256SUMS", "caption.md", "chart-contract-and-source-data.md",
  "command.txt", "config.json", "contract.json", "environment.json", "figure.pdf",
  "figure.png", "figure.svg", "manifest.json", "plot.py", "progress.ndjson",
  "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "qa-protocol.md",
  "qa-report.md", "requirements.txt", "resource-log.ndjson", "results.json",
  "source-data.csv", "validate.py", "validation.json",
];
const publicPages = {
  note: "public/notes/r0-73m.html",
  recap: "public/recap-r0-61-r0-73m.html",
  home: "public/research-review.html",
  literature: "public/literature-review.html",
  index: "public/notes/index.html",
};
const target = {
  version: "1.53",
  latest: "r073m",
  notes: 189,
  recap: 129,
  published: 91,
  sealed: 67,
  backlog: 24,
  next: "r073n",
};
const closedClaims = [
  "physicalKineticSelectedGainConjugacy=CLOSED",
  "fixedEndpointBackwardLocalization=CLOSED",
  "prescribedActionSeedWindow=CLOSED",
  "twoDimensionalNonlinearDeparture=CLOSED",
  "fixedDistanceEndpoint=CLOSED",
  "selectedPlanarOrbitGlobalSmoothness=CLOSED",
];
const finiteClaims = [
  "finiteDiagnosticPackage=CLOSED",
  "primaryPrescribedActionCases=15",
  "independentLinearSentinels=5",
  "independentHierarchySentinels=3",
  "formalFigurePackage=PASS",
  "finiteDimensionDoesNotCertifyContinuum=TRUE",
];
const openClaims = [
  "prefactorLimit=OPEN",
  "twoTermWKB=OPEN",
  "singleFixedBackgroundLyapunovInstability=OPEN",
  "transverseThreeDimensionalClosure=OPEN",
  "finiteTimeSingularity=OPEN",
  "Clay=OPEN",
];
const forbidden = [
  "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  "颠覆性", "世界首个", "接近解决", "解决了千禧年", "证明了全局正则性",
  "原创性定理", "首次证明",
];
const expectedClaimBoundary = {
  finiteInviscidActionProxyComputed: true,
  finiteViscousActionComputedSeparately: true,
  finitePrescribedActionRecodingComputed: true,
  finiteABCoefficientsComputed: true,
  continuumActionCertifiedByFiniteComputation: false,
  continuumGainPrefactorCertifiedByFiniteComputation: false,
  prefactorLimitCertified: false,
  twoTermWKBCertified: false,
  uniformTaylorRadiusCertified: false,
  fourthOrderRemainderCertified: false,
  fullNonlinearNavierStokesTrajectoryComputed: false,
  finiteCutoffAgreementIsTailProof: false,
  singleFixedBackgroundLyapunovInstabilityCertified: false,
  transverseThreeDimensionalClosureCertified: false,
  finiteTimeSingularityCertified: false,
  clayProblemSolved: false,
};

function assertPublicVoice(value, label) {
  for (const phrase of forbidden) {
    assert.equal(value.includes(phrase), false, `${label}: ${phrase}`);
  }
  assert.doesNotMatch(
    value,
    /\b(?:we|our|ours|ourselves|us)\b/i,
    `${label}: collective English voice`,
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
  assert.ok(value.length > 10_000, `${relative}: substantive PDF`);
  assert.equal(value.subarray(0, 4).toString(), "%PDF", relative);
  const match = value.toString("latin1").match(/\/Title\s*<([0-9A-Fa-f]+)>/);
  assert.ok(match, `${relative}: hexadecimal PDF title metadata`);
  assert.equal(decodeUtf16Be(Buffer.from(match[1], "hex")), expectedTitle, relative);
}

test("R0.73M pins the v1.53 accounting endpoint", async () => {
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
    "tests/r073m-prescribed-action-departure-gate.test.mjs",
  );
  assert.equal(release.latestReleasePublicationTest, "tests/r073m-release.test.mjs");
  assert.deepEqual(release.formalArchiveInventory, {
    path: "research/formal-archive-inventory.json",
    sha256: sha256(inventoryBytes),
  });
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.53",
    latestRelease: "R0.73M",
    publicHtmlNoteCount: 189,
    publishedDate: "2026-08-31",
  });
  assert.deepEqual({
    latest: inventory.latestPublishedRelease,
    published: inventory.publishedReleaseCount,
    sealed: inventory.formalSealedReleaseCount,
    backlog: inventory.legacyFormalFigureBacklogCount,
  }, { latest: "r073m", published: 91, sealed: 67, backlog: 24 });
  assert.equal(inventory.publishedReleases.length, 91);
  assert.equal(inventory.formalSealedReleases.length, 67);
  assert.equal(inventory.publishedReleases.at(-1), "r073m");
  assert.equal(inventory.formalSealedReleases.at(-1), "r073m");
  assert.equal(version, "1.53\n");
});

test("R0.73M five-page route and exact claim boundary are complete", async () => {
  const [note, recap, home, literature, index] =
    await Promise.all(Object.values(publicPages).map(text));
  for (const [label, value] of Object.entries({ note, recap, home, literature, index })) {
    assert.ok(value.includes("R0.73M"), `${label}: release label`);
    assert.ok(value.includes("/i18n-en.js?v=1.53"), `${label}: i18n v1.53`);
    assertPublicVoice(value, `${label} HTML`);
  }

  for (const token of [
    ...closedClaims,
    ...finiteClaims,
    ...openClaims,
    "NOT CLAY",
    "1/450",
    "1/1800",
    "\\tfrac1{1500}",
    "\\tfrac1{1000}",
    "\\tfrac{21}{125}",
    "15 个主案例",
    "1,170",
    "28/28",
    "0.9960745297",
    "0.9965850278",
    "故终点 selected-pair 范数 \\(\\ge(c_L/2)\\rho\\)",
    "R0.73N",
  ]) assert.ok(note.includes(token), `note token ${token}`);
  for (const href of [
    "/notes/r0-73m.pdf",
    "/recap-r0-61-r0-73m.html",
    "/recap-r0-61-r0-73m.pdf",
    `/assets/r073m/${figureId}.pdf`,
    `/assets/r073m/${figureId}.svg`,
    `/assets/r073m/${figureId}.png`,
  ]) assert.ok(note.includes(`href="${href}"`), `note link ${href}`);

  const nodes = recapNodes(recap);
  assert.equal(nodes.length, 129);
  assert.equal(new Set(nodes).size, 129);
  assert.equal(nodes[0], "r0-61");
  assert.equal(nodes.at(-1), "r0-73m");
  assert.equal(recap.match(/<article class="phase">/g)?.length, 48);
  assert.ok(recap.includes("回顾截止节点：R0.73M"));
  assert.ok(recap.includes("R0.70A–R0.73M 的 91 个版本已经公开"));
  assert.ok(recap.includes("67 节完整封存"));
  assert.ok(recap.includes("24 节旧档待回补"));
  assert.ok(recap.includes(
    '<li style="break-inside:avoid;page-break-inside:avoid">R0.73L 闭合共同定义域演化',
  ));
  for (const token of [...closedClaims, ...finiteClaims, ...openClaims, "R0.73N"]) {
    assert.ok(recap.includes(token), `recap token ${token}`);
  }

  assert.ok(home.includes("LATEST RELEASE · R0.73M"));
  assert.ok(home.includes("当前端点 R0.73M"));
  assert.ok(home.includes("NEXT · R0.73N"));
  assert.ok(home.includes("<strong>2026-08-31</strong>最近修订"));
  assert.ok(home.includes(
    "<strong>prescribed-action planar departure / fixed-background feasibility audit</strong>当前方向",
  ));
  assert.equal(home.includes("<strong>2026-08-30</strong>最近修订"), false);
  assert.equal(
    home.includes("<strong>non-selfadjoint adiabatic tracking / bounded prefactor</strong>当前方向"),
    false,
  );
  assert.ok(home.includes('data-release="r073m"'));
  assert.ok(home.includes("finite diagnostic: 15 primary / 5 linear / 3 hierarchy / 27 figure rows / 28 checks"));
  assert.equal(home.match(/data-release="r073m"/g)?.length, 1);
  const route = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.73M">([\s\S]*?)<\/nav>/,
  );
  assert.ok(route, "R0.69P--R0.73M route block");
  const routeLinks = [...route[1].matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(routeLinks.length, 99);
  assert.equal(new Set(routeLinks).size, 99);
  assert.equal(routeLinks.at(-1), "r0-73m");

  assert.ok(literature.includes('id="r073m-boundary"'));
  assert.ok(literature.includes('class="route-r073m-deck-update"'));
  assert.ok(literature.includes("开放接口 · R0.73N"));
  for (const token of [...closedClaims, ...finiteClaims, ...openClaims]) {
    assert.ok(literature.includes(token), `literature token ${token}`);
  }
  for (const number of [125, 126, 127, 129, 134, 135, 136, 137, 173, 174]) {
    assert.equal(
      [...literature.matchAll(new RegExp(`id="ref-${number}"`, "g"))].length,
      1,
      `ref-${number}`,
    );
  }
  assert.ok(literature.includes("2863–2946"), "LMZ page range");
  assert.ok(literature.includes("10.1002/cpa.22183"), "LMZ DOI");
  assert.equal(literature.includes("3387--3452"), false, "stale LMZ page range");
  const literatureIds = [...literature.matchAll(/\bid="([^"]+)"/g)]
    .map((match) => match[1]);
  assert.equal(new Set(literatureIds).size, literatureIds.length, "literature ids unique");

  assert.ok(index.includes('data-site-version="1.53"'));
  assert.ok(index.includes('data-note="r0-73m"'));
  assert.ok(index.includes("189 篇公开研究笔记"));
  assert.ok(index.includes('href="/notes/r0-73m.html"'));
  assert.ok(index.includes('href="/notes/r0-73m.pdf"'));
  assert.ok(index.includes('href="/recap-r0-61-r0-73m.html"'));
});

test("R0.73M sealed finite certificate binds 15 cases and 28 independent checks", async () => {
  const [manifest, primary, independentLinear, independentHierarchy, validation,
    certificate, config, configBytes, entries, ledgerText] = await Promise.all([
    json(`${certificateRoot}/manifest.json`),
    json(`${certificateRoot}/primary_results.json`),
    json(`${certificateRoot}/independent_linear.json`),
    json(`${certificateRoot}/independent_hierarchy.json`),
    json(`${certificateRoot}/validation.json`),
    json(`${certificateRoot}/certificate.json`),
    json(`${certificateRoot}/config.json`),
    bytes(`${certificateRoot}/config.json`),
    readdir(resolve(root, certificateRoot), { withFileTypes: true }),
    text(`${certificateRoot}/SHA256SUMS`),
  ]);
  assert.equal(manifest.schemaVersion, "r073m-sealed-package-manifest-v1");
  assert.equal(primary.schemaVersion, "r073m-primary-finite-diagnostic-v1");
  assert.equal(independentLinear.schemaVersion, "r073m-independent-linear-action-v1");
  assert.equal(independentHierarchy.schemaVersion, "r073m-independent-vorticity-fft-v1");
  assert.equal(validation.schemaVersion, "r073m-independent-package-validation-v1");
  assert.equal(certificate.schemaVersion, "r073m-finite-certificate-v1");
  assert.equal(config.schemaVersion, "r073m-prescribed-action-finite-config-v1");
  assert.equal(manifest.release, "R0.73M");
  assert.equal(manifest.smokeMode, false);
  assert.equal(manifest.allPrerequisiteChecksPass, true);
  assert.equal(manifest.sourceCommit, "7a4d7706d7a50525611b6267061aea0a79f9fd04");
  assert.equal(
    sha256(configBytes),
    "d0f757c41ce96971e64860e028e55d9378166ef1df6de28b7c0c2527c6bbb7d4",
  );
  assert.deepEqual(manifest.inventory, {
    sourceFileCount: 11,
    generatedFileCount: 19,
    manifestBoundFileCount: 30,
    sha256SumsLineCount: 31,
  });
  for (const [label, payload] of Object.entries({
    primary, independentLinear, independentHierarchy, validation, certificate,
  })) {
    assert.equal(payload.allChecksPass, true, `${label}.allChecksPass`);
    if (payload.status !== undefined) assert.equal(payload.status, "passed", `${label}.status`);
    if (payload.checks !== undefined) {
      assert.ok(Object.values(payload.checks).every(Boolean), `${label}.checks`);
    }
    assert.deepEqual(payload.claimBoundary, expectedClaimBoundary, `${label}.claimBoundary`);
  }
  assert.deepEqual(manifest.claimBoundary, expectedClaimBoundary);
  assert.deepEqual(config.claimBoundary, expectedClaimBoundary);
  assert.deepEqual(primary.parameters.cutoffs, [40, 48, 64]);
  assert.equal(primary.caseCount, 15);
  assert.equal(primary.cases.length, 15);
  assert.equal(validation.observations.caseCount, 15);
  assert.equal(validation.observations.actionNodeCount, 1170);
  assert.equal(independentLinear.validations.length, 5);
  assert.equal(independentHierarchy.validations.length, 3);
  assert.equal(Object.keys(validation.checks).length, 28);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.deepEqual(
    [Math.min(...primary.cases.map((row) => row.finiteInviscidActionPrefactor)),
      Math.max(...primary.cases.map((row) => row.finiteInviscidActionPrefactor))],
    [0.9960745296895327, 0.9965850277770183],
  );
  assert.ok(independentLinear.maximums.gainRelative < 2.1e-9);
  assert.ok(independentLinear.maximums.finiteInviscidActionPrefactorAbsolute < 2.2e-9);
  assert.ok(independentHierarchy.maximumCoefficientRelativeError < 8.4e-10);

  const actualFiles = entries.filter((entry) => entry.isFile()).map((entry) => entry.name).sort();
  assert.equal(actualFiles.length, 32);
  const ledger = ledgerText.trim().split("\n");
  assert.equal(ledger.length, 31);
  const ledgerNames = [];
  for (const row of ledger) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `certificate ledger row ${row}`);
    ledgerNames.push(match[2]);
    assert.equal(sha256(await bytes(`${certificateRoot}/${match[2]}`)), match[1], match[2]);
  }
  assert.deepEqual(ledgerNames, actualFiles.filter((name) => name !== "SHA256SUMS"));
});

test("R0.73M formal figure binds 27 rows, 25 files, and byte-identical mirrors", async () => {
  const [manifest, contract, config, results, validation, entries, ledgerText] =
    await Promise.all([
      json(`${figureRoot}/manifest.json`),
      json(`${figureRoot}/contract.json`),
      json(`${figureRoot}/config.json`),
      json(`${figureRoot}/results.json`),
      json(`${figureRoot}/validation.json`),
      readdir(resolve(root, figureRoot), { withFileTypes: true }),
      text(`${figureRoot}/SHA256SUMS`),
    ]);
  assert.equal(manifest.schemaVersion, "r073m-prescribed-action-figure-manifest-v1");
  assert.equal(contract.schemaVersion, "r073m-prescribed-action-figure-contract-v1");
  assert.equal(config.schemaVersion, "r073m-prescribed-action-figure-config-v1");
  assert.equal(results.schemaVersion, "r073m-figure-results-v1");
  assert.equal(validation.schemaVersion, "r073m-figure-validation-v1");
  assert.equal(manifest.release, "R0.73M");
  assert.equal(manifest.figureId, figureId);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.publicationStatus, "published");
  assert.equal(manifest.qa.status, "passed");
  for (const key of [
    "finalSizeInspected", "grayscaleInspected", "labelsAndLegendsInspected",
    "scalesAndUnitsInspected", "dataCrossChecked", "visualInspectionExplicit",
  ]) assert.equal(manifest.qa[key], true, `manifest QA ${key}`);
  assert.equal(manifest.publication.publicCopiesComplete, true);
  assert.equal(manifest.publication.byteIdentityRequired, true);
  assert.equal(manifest.publication.assets.length, 3);
  assert.deepEqual(manifest.packageInventory, {
    chartContractSourceDataNote: "chart-contract-and-source-data.md",
    expectedFileCount: 25,
    generatedFileCount: 15,
    paths: figureFiles,
    sourceFileCount: 10,
  });
  const expectedFigureBoundary = {
    ...expectedClaimBoundary,
    formalValidatedDiagnosticFigure: true,
    independentFiniteRecomputationPassed: true,
    sealedUpstreamCertificatePassed: true,
    finiteDimensionalDiagnostic: true,
  };
  delete expectedFigureBoundary.finiteViscousActionComputedSeparately;
  assert.deepEqual(manifest.claimBoundary, expectedFigureBoundary);

  assert.equal(results.status, "passed");
  assert.equal(results.allChecksPass, true);
  assert.equal(results.finiteCaseRows, 15);
  assert.equal(results.gateComponentRows, 12);
  assert.equal(results.sourceRows, 27);
  assert.deepEqual(
    results.summary.finiteInviscidActionPrefactorRange,
    [0.9960745296895327, 0.9965850277770183],
  );
  assert.equal(results.summary.largestGateFamilyRatio, 0.11582529656770109);
  assert.equal(results.summary.gateFamilyMaximums.length, 4);
  assert.ok(results.summary.gateFamilyMaximums.every((row) => row.ratioToTolerance < 1));

  assert.equal(validation.status, "passed");
  assert.equal(validation.allChecksPass, true);
  assert.equal(Object.keys(validation.checks).length, 10);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.deepEqual(validation.details.sourceData, {
    finiteCaseRows: 15,
    gateComponentRows: 12,
    gateFamilyMaximums: {
      cutoff: 5.421010862427522e-8,
      independent: 0.041599078041835616,
      "physical-kinetic": 0.0013032639323169652,
      step: 0.11582529656770109,
    },
    totalRows: 27,
  });
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
    assert.ok(match, `figure ledger row ${row}`);
    ledgerNames.push(match[2]);
    assert.equal(sha256(await bytes(`${figureRoot}/${match[2]}`)), match[1], match[2]);
  }
  assert.deepEqual(ledgerNames, actualFiles.filter((name) => name !== "SHA256SUMS"));

  for (const name of figureFiles) {
    assert.deepEqual(
      await bytes(`${mirrorRoot}/${name}`),
      await bytes(`${figureRoot}/${name}`),
      `archive mirror ${name}`,
    );
  }
  const outputs = new Map(manifest.figure.outputs.map((row) => [row.path, row]));
  const assets = new Map(
    manifest.publication.assets.map((row) => [row.path.split(".").at(-1), row]),
  );
  for (const suffix of ["pdf", "svg", "png"]) {
    const source = await bytes(`${figureRoot}/figure.${suffix}`);
    const published = await bytes(`${publicFigureRoot}.${suffix}`);
    assert.deepEqual(published, source, `${suffix} public master`);
    assert.equal(outputs.get(`figure.${suffix}`).sha256, sha256(source));
    assert.equal(assets.get(suffix).sha256, sha256(source));
    assert.equal(assets.get(suffix).path, `${publicFigureRoot}.${suffix}`);
  }
});

test("R0.73M synchronized note and recap PDFs are cryptographically bound", async () => {
  const noteTitle = "R0.73M｜Prescribed-action planar nonlinear departure";
  const recapTitle = "R0.61–R0.73M｜R0.60 之后的研究回顾";
  await assertPdf("public/notes/r0-73m.pdf", noteTitle);
  await assertPdf("public/recap-r0-61-r0-73m.pdf", recapTitle);

  const binding = await json("research/r073m_pdf_bindings.json");
  assert.equal(binding.schemaVersion, "r073m-synchronized-pdf-bindings-v1");
  assert.equal(binding.release, "R0.73M");
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
        html: "public/notes/r0-73m.html",
        pdf: "public/notes/r0-73m.pdf",
        title: noteTitle,
      },
      {
        kind: "cumulative-recap",
        html: "public/recap-r0-61-r0-73m.html",
        pdf: "public/recap-r0-61-r0-73m.pdf",
        title: recapTitle,
      },
    ],
  );
  for (const row of binding.documents) {
    for (const record of [row.html, row.pdf]) {
      const payload = await bytes(record.path);
      assert.equal(payload.length, record.bytes, `${record.path}: bytes`);
      assert.equal(sha256(payload), record.sha256, `${record.path}: sha256`);
    }
  }
  const check = spawnSync(
    process.execPath,
    ["scripts/bind-r073m-pdfs.mjs", "--check-only"],
    { cwd: root, encoding: "utf8" },
  );
  assert.equal(check.status, 0, check.stderr);
});

test("R0.73M translations, snapshot, bundle, and terminology source agree", async () => {
  const [translations, snapshot, bundle, dictionary, ...htmlPages] = await Promise.all([
    json("translations/en.json"),
    json("scripts/i18n-snapshots/r073m-missing.json"),
    text("public/i18n-en.js"),
    text("research/r073m_bilingual_dictionary.md"),
    ...Object.values(publicPages).map(text),
  ]);
  const rows = translations.filter((entry) => /^r073m\d{3}$/.test(entry.id));
  assert.ok(rows.length > 0, "R0.73M translation rows");
  assert.equal(rows.length, snapshot.length);
  assert.equal(new Set(rows.map((entry) => entry.id)).size, rows.length);
  assert.equal(new Set(rows.map((entry) => entry.zh)).size, rows.length);
  assert.deepEqual(
    rows.map(({ zh, en }) => ({ zh, en })),
    snapshot,
    "translation snapshot order and values",
  );
  for (const [index, entry] of rows.entries()) {
    const label = `R0.73M translation row ${index + 1}`;
    assert.equal(entry.id, `r073m${String(index + 1).padStart(3, "0")}`, `${label}: id`);
    assert.ok(typeof entry.en === "string" && entry.en.trim(), `${label}: English`);
    assert.equal(containsChinese(entry.en), false, `${label}: Chinese in English`);
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i, label);
    assert.deepEqual(
      extractProtectedTokens(entry.en),
      extractProtectedTokens(entry.zh),
      `${label}: protected tokens`,
    );
    assert.deepEqual(
      machineLedgerAssignments(entry.en),
      machineLedgerAssignments(entry.zh),
      `${label}: machine ledgers`,
    );
    assert.ok(
      bundle.includes(`${JSON.stringify(entry.zh)}: ${JSON.stringify(entry.en)}`),
      `${label}: browser bundle`,
    );
  }
  assertPublicVoice(JSON.stringify(rows), "R0.73M translations");
  for (const [index, value] of htmlPages.entries()) {
    assertPublicVoice(value, `public HTML ${index + 1}`);
  }
  for (const token of [
    "R0.73M",
    "Prescribed-action planar nonlinear departure",
    "full inviscid action",
    "prescribed-action seed",
    "bounded two-sided prefactor",
    "harmonic energy hierarchy",
    "fixed-distance departure",
    "bounded-search gap",
    "R0.73N",
    "Feasibility and obstruction audit for fixed-background Lyapunov instability",
    ...closedClaims,
    ...finiteClaims,
    ...openClaims,
  ]) assert.ok(dictionary.includes(token), `terminology token ${token}`);
  assert.doesNotMatch(dictionary, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  assert.doesNotMatch(dictionary, /`\([^`\n]*`\)/, "malformed inline-math code spans");
  assert.ok(dictionary.includes("2863–2946"));
  assert.ok(dictionary.includes("10.1002/cpa.22183"));
  assertPublicVoice(dictionary, "R0.73M terminology source");

  const check = spawnSync(
    process.execPath,
    ["scripts/add-r073m-translations.mjs", "--check-only"],
    { cwd: root, encoding: "utf8" },
  );
  assert.equal(check.status, 0, check.stderr);
});

test("R0.73M release generator pins all mathematical and publication gates", async () => {
  const generator = await text("scripts/generate_r073m_release.py");
  const block = generator.match(/RELEASE_SOURCE_EXACT_PATHS = \(\n([\s\S]*?)\n\)/);
  assert.ok(block, "RELEASE_SOURCE_EXACT_PATHS block");
  const pinned = [...block[1].matchAll(/^\s+"([^"]+)",$/gm)]
    .map((match) => match[1]);
  for (const relative of [
    "scripts/r073m_release_content.py",
    "scripts/add-r073m-translations.mjs",
    "scripts/generate_r073m_release.py",
    "scripts/bind-r073m-pdfs.mjs",
    "research/r073m_bilingual_dictionary.md",
    "tests/r073m-prescribed-action-departure-gate.test.mjs",
    "tests/r073m-release.test.mjs",
    "tests/site-route-current-boundary.test.mjs",
  ]) assert.ok(pinned.includes(relative), `release-source pin ${relative}`);
  assert.equal(generator.includes('ANALYTIC_SOURCE_COMMIT = "aa4ca025c2ac01e24a9828101e9499f2f8e9052c"'), true);
  assert.equal(generator.includes('EXPERIMENT_PACKAGE_COMMIT = "aa4ca025c2ac01e24a9828101e9499f2f8e9052c"'), true);
  for (const name of [
    "ANALYTIC_SOURCE_COMMIT", "EXPERIMENT_PACKAGE_COMMIT", "FIGURE_PACKAGE_COMMIT",
    "RELEASE_BASELINE_COMMIT", "RELEASE_SOURCE_COMMIT",
  ]) assert.match(generator, new RegExp(`${name} = "[0-9a-f]{40}"`));
  assert.match(
    generator,
    /normalized_release_generator\(git_bytes\(RELEASE_SOURCE_COMMIT, generator_relative\)\)/,
  );
  for (const token of [
    '"chart-contract-and-source-data.md"',
    '"r073m-sealed-package-manifest-v1"',
    '"r073m-primary-finite-diagnostic-v1"',
    '"r073m-independent-linear-action-v1"',
    '"r073m-independent-vorticity-fft-v1"',
    '"r073m-independent-package-validation-v1"',
    '"r073m-finite-certificate-v1"',
    '"r073m-prescribed-action-figure-manifest-v1"',
    '"r073m-figure-results-v1"',
    '"r073m-figure-validation-v1"',
    "2863–2946",
    "10.1002/cpa.22183",
  ]) assert.ok(generator.includes(token), `generator token ${token}`);
  const figureBlock = generator.match(/FIGURE_PACKAGE_PATHS = \(\n([\s\S]*?)\n\)/);
  assert.ok(figureBlock, "FIGURE_PACKAGE_PATHS block");
  const figurePaths = [...figureBlock[1].matchAll(/^\s+"([^"]+)",$/gm)]
    .map((match) => match[1]);
  assert.deepEqual(figurePaths, figureFiles);

  const help = spawnSync(
    "python3",
    ["scripts/generate_r073m_release.py", "--help"],
    { cwd: root, encoding: "utf8" },
  );
  assert.equal(help.status, 0, help.stderr);
  assert.ok(help.stdout.includes("--check-only"));
  assert.ok(help.stdout.includes("--apply"));
});
