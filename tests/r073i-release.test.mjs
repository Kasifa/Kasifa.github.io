import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  containsChinese,
  extractProtectedTokens,
} from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const bytes = (relative) => readFile(resolve(root, relative));

const figureId = "fig-r073i-action-boundary";
const figureRoot = `figures/r073i/${figureId}`;
const publicFigureRoot = `public/assets/r073i/${figureId}`;
const publicPages = {
  note: "public/notes/r0-73i.html",
  recap: "public/recap-r0-61-r0-73i.html",
  home: "public/research-review.html",
  literature: "public/literature-review.html",
  index: "public/notes/index.html",
};

const releaseTarget = {
  version: "1.49",
  latest: "r073i",
  notes: 185,
  recap: 125,
  published: 87,
  sealed: 63,
  backlog: 24,
  next: "r073j",
};

const forbiddenPublicPhrases = [
  "我们",
  "攻关",
  "主攻",
  "突破",
  "研究纪律",
  "三重审计",
  "杀死错误想法",
  "颠覆性",
  "世界首个",
  "接近解决",
  "解决了千禧年",
  "证明了全局正则性",
  "原创性定理",
  "首次证明",
];

function assertPublicVoice(value, label) {
  for (const phrase of forbiddenPublicPhrases) {
    assert.equal(value.includes(phrase), false, `${label}: ${phrase}`);
  }
  assert.doesNotMatch(
    value,
    /\b(?:we|our|ours|ourselves|us)\b/i,
    `${label}: collective English voice`,
  );
}

function recapNodes(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start, "recap node-index section");
  return [...recap.slice(start, end).matchAll(
    /href="\/notes\/(r0-[^"]+)\.html"/g,
  )].map((match) => match[1]);
}

function section(html, id) {
  const start = html.indexOf(`<section id="${id}">`);
  const end = html.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start, `section #${id}`);
  return html.slice(start, end);
}

function assertCommitReference(value, label) {
  assert.match(value, /^[0-9a-f]{40}$/, `${label} sourceCommit`);
}

async function assertPdf(relative) {
  const value = await bytes(relative);
  assert.ok(value.length > 4, `${relative}: nonempty PDF`);
  assert.equal(value.subarray(0, 4).toString(), "%PDF", relative);
}

test("R0.73I release manifest pins the v1.49 accounting endpoint", async () => {
  const [release, site, inventory, version] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    json("research/formal-archive-inventory.json"),
    text("VERSION"),
  ]);

  assert.equal(release.schemaVersion, "research-release-manifest-v1");
  assert.deepEqual({
    version: release.siteVersion,
    latest: release.latestCompletedRelease,
    notes: release.publicHtmlNoteCount,
    recap: release.postR060RecapNodeCount,
    published: release.postR070APublishedReleaseCount,
    sealed: release.postR070AFormalSealedReleaseCount,
    backlog: release.legacyFormalFigureBacklogCount,
    next: release.nextRelease,
  }, releaseTarget);

  assert.equal(site.schemaVersion, "research-site-version-v1");
  assert.deepEqual({
    version: site.version,
    latest: site.latestRelease,
    notes: site.publicHtmlNoteCount,
  }, {
    version: "1.49",
    latest: "R0.73I",
    notes: 185,
  });
  assert.equal(inventory.latestPublishedRelease, "r073i");
  assert.equal(inventory.legacyFormalFigureBacklogCount, 24);
  assert.equal(version, "1.49\n");
});

test("R0.73I public current/latest chain and 125-node recap are complete", async () => {
  const [note, recap, home, literature, index] = await Promise.all(
    Object.values(publicPages).map(text),
  );
  const pages = { note, recap, home, literature, index };

  for (const [label, value] of Object.entries(pages)) {
    assert.ok(value.includes("R0.73I"), `${label}: R0.73I`);
    assert.ok(value.includes("/i18n-en.js?v=1.49"), `${label}: i18n v1.49`);
    assertPublicVoice(value, `${label} HTML`);
  }

  assert.ok(note.includes("状态 · R0.73I 完成"));
  assert.ok(note.includes(`/assets/r073i/${figureId}.svg`));
  assert.ok(note.includes(`/assets/r073i/${figureId}.pdf`));
  assert.ok(note.includes(`/assets/r073i/${figureId}.png`));
  assert.ok(section(note, "next").includes("R0.73J"));

  const nodes = recapNodes(recap);
  assert.equal(nodes.length, 125);
  assert.equal(new Set(nodes).size, 125);
  assert.equal(nodes[0], "r0-61");
  assert.equal(nodes.at(-1), "r0-73i");
  for (const required of [
    "r0-61", "r0-69v", "r0-69w", "r0-70a", "r0-73i",
  ]) assert.ok(nodes.includes(required), `recap node ${required}`);
  assert.ok(recap.includes("回顾截止节点：R0.73I"));
  assert.ok(recap.includes("收录节点：125"));

  assert.ok(home.includes("LATEST RELEASE · R0.73I"));
  assert.ok(home.includes("当前端点 R0.73I"));
  assert.ok(home.includes("NEXT · R0.73J"));
  assert.ok(home.includes('/notes/r0-73i.pdf'));
  assert.ok(home.includes('/recap-r0-61-r0-73i.html'));
  assert.doesNotMatch(home, /LATEST RELEASE · R0\.73H/);
  assert.doesNotMatch(home, /当前端点 R0\.73H/);
  assert.doesNotMatch(home, /class="route-map-latest" href="\/notes\/r0-73h\.pdf"/);

  const literatureH = literature.indexOf('id="r073h-boundary"');
  const literatureI = literature.indexOf('id="r073i-boundary"');
  assert.ok(literatureH >= 0, "literature retains R0.73H history");
  assert.ok(literatureI > literatureH, "literature advances through R0.73I");
  assert.ok(literature.includes('/notes/r0-73i.html'));
  assert.ok(literature.includes('/recap-r0-61-r0-73i.html'));

  const indexI = index.indexOf('data-note="r0-73i"');
  const indexH = index.indexOf('data-note="r0-73h"');
  assert.ok(indexI >= 0 && indexH > indexI, "index is latest-first at R0.73I");
  assert.ok(index.includes("185 篇公开研究笔记"));
  assert.ok(index.includes("最新节点 R0.73I"));
  assert.ok(index.includes('/recap-r0-61-r0-73i.html'));
  assert.doesNotMatch(
    index,
    /<strong>R0\.73H<\/strong><span>最新研究节点<\/span>/,
  );
});

test("R0.73I public figure and synchronized PDFs preserve release bytes", async () => {
  for (const suffix of ["pdf", "svg", "png"]) {
    assert.deepEqual(
      await bytes(`${publicFigureRoot}.${suffix}`),
      await bytes(`${figureRoot}/figure.${suffix}`),
      `${suffix} byte identity`,
    );
  }
  await assertPdf("public/notes/r0-73i.pdf");
  await assertPdf("public/recap-r0-61-r0-73i.pdf");
});

test("R0.73I HTML, translation source, and browser bundle are bilingual and public-safe", async () => {
  const [translations, bundle, ...htmlPages] = await Promise.all([
    json("translations/en.json"),
    text("public/i18n-en.js"),
    ...Object.values(publicPages).map(text),
  ]);
  assert.ok(Array.isArray(translations));

  const rows = translations.filter((entry) => /^r073i\d+$/.test(entry.id));
  assert.ok(rows.length > 0, "R0.73I translation rows");
  assert.equal(new Set(rows.map((entry) => entry.id)).size, rows.length);
  assert.equal(new Set(rows.map((entry) => entry.zh)).size, rows.length);
  assert.ok(rows.some((entry) => entry.zh.includes("R0.73I")));
  assert.ok(rows.some((entry) => entry.en.includes("R0.73I")));
  assert.ok(rows.some((entry) => entry.zh.includes("R0.73J")));
  assert.ok(rows.some((entry) => entry.en.includes("R0.73J")));

  for (const [index, entry] of rows.entries()) {
    const label = `R0.73I translation row ${index + 1}`;
    assert.equal(typeof entry.zh, "string", `${label}: zh`);
    assert.ok(typeof entry.en === "string" && entry.en.trim(), `${label}: en`);
    assert.equal(containsChinese(entry.en), false, `${label}: Chinese in English`);
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i, label);
    assert.deepEqual(
      extractProtectedTokens(entry.en),
      extractProtectedTokens(entry.zh),
      `${label}: protected tokens`,
    );
    assert.ok(
      bundle.includes(`${JSON.stringify(entry.zh)}: ${JSON.stringify(entry.en)}`),
      `${label}: browser bundle mapping`,
    );
  }

  assert.ok(bundle.includes("R0.73I"));
  assert.ok(bundle.includes("R0.73J"));
  assertPublicVoice(JSON.stringify(translations), "translations/en.json");
  assertPublicVoice(bundle, "public/i18n-en.js");
  for (const [index, value] of htmlPages.entries()) {
    assert.ok(value.includes("R0.73I"), `public HTML ${index + 1}: R0.73I`);
    assertPublicVoice(value, `public HTML ${index + 1}`);
  }
});

test("R0.73I finite manifest, figure, and certificate remain fail-closed", async () => {
  const [finite, figure, certificate, certificateManifest] = await Promise.all([
    json("experiments/r073i/manifest.json"),
    json(`${figureRoot}/manifest.json`),
    json("research/certificates/r073i/certificate.json"),
    json("research/certificates/r073i/manifest.json"),
  ]);

  for (const [label, value] of Object.entries({
    finite,
    figure,
    certificate,
    certificateManifest,
  })) assertCommitReference(value.sourceCommit, label);

  const finiteBoundary = {
    analyticUpperBoundEqualsD0: false,
    clayProblemSolved: false,
    finiteActionIsContinuumAction: false,
    finiteBinary64GalerkinDiagnostic: true,
    finiteWkbCorrectionIsAsymptoticTheorem: false,
    matchingContinuumGainActionEstablished: false,
    oneOver450IsTheoremEndpoint: false,
    ordinaryCutoffAgreementIsTailProof: false,
    prescribedActionSeedDepartureEstablished: false,
    selectedFiniteBranchIsContinuumBranch: false,
  };
  assert.equal(finite.schemaVersion, "r073i-finite-manifest-v1");
  assert.equal(finite.diagnosticOnly, true);
  assert.equal(finite.allChecksPass, true);
  assert.equal(finite.smokeMode, false);
  assert.equal(
    finite.continuumConclusion,
    "none; finite binary64 Fourier--Galerkin diagnostics only",
  );
  assert.deepEqual(finite.claimBoundary, finiteBoundary);

  assert.equal(figure.schemaVersion, "r073i-action-boundary-manifest-v1");
  assert.equal(figure.status, "formal");
  assert.equal(figure.diagnosticOnly, true);
  assert.equal(figure.evidenceClass, "finite-binary64-galerkin-diagnostic-only");
  assert.deepEqual(figure.claimBoundary, {
    analyticUpperBoundEqualsD0: false,
    clayProblemSolved: false,
    experimentInputsPassedTheirFiniteValidator: true,
    finiteActionIsContinuumAction: false,
    finiteWkbCorrectionIsAsymptoticTheorem: false,
    formalFiniteDiagnosticFigure: true,
    inverseLambdaGuideIsFittedRateOrProof: false,
    matchingContinuumGainActionEstablished: false,
    oneOver450IsTheoremEndpoint: false,
    ordinaryCutoffAgreementIsTailProof: false,
  });

  assert.equal(certificate.schemaVersion, "r073i-exact-certificate-v1");
  assert.equal(certificate.allChecksPass, true);
  assert.deepEqual(certificate.finiteDiagnostic.claimBoundary, finiteBoundary);
  assert.deepEqual(certificate.claimLedger, {
    Clay: "OPEN",
    actionLimitAloneGivesBoundedPrefactor: "FALSE_AS_INFERENCE",
    canonicalSelectedBranch: "OPEN",
    finitePilotProvesContinuumAction: "FALSE_AS_INFERENCE",
    finiteTimeSingularity: "OPEN",
    fixedBackgroundLyapunovInstability: "OPEN",
    fixedWindowActionFromInheritedInputs: "FALSE_AS_INFERENCE",
    improvedContinuumUpperAction: "CLOSED",
    inheritedEndpointStrictlyBelowOneOver450: "CLOSED",
    matchingSelectedGainAction: "OPEN",
    prescribedActionSeedDeparture: "OPEN",
    transverseThreeDimensionalClosure: "OPEN",
    zeroWindowTangentAction: "CLOSED",
  });

  assert.equal(
    certificateManifest.schemaVersion,
    "r073i-certificate-manifest-v1",
  );
  assert.equal(certificateManifest.status, "formal");
  assert.equal(certificateManifest.allPrerequisiteChecksPass, true);
  assert.deepEqual(certificateManifest.evidenceBoundary, {
    ClayProblemSolved: false,
    exactArithmeticAndLogicalCounterexamples: true,
    finiteDiagnosticOnly: true,
    matchingContinuumGainActionEstablished: false,
  });
});
