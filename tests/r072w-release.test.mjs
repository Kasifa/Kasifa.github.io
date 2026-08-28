import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import { collectSiteStrings, extractProtectedTokens } from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");
const run = promisify(execFile);
const python = process.env.CODEX_PYTHON || "python3";
const certificate = "research/certificates/r072w";
const figure = "figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer";
const figureId = "fig-r072w-exact-tail-transfer";

const expectedSourceStage = {
  release: "r072w",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072w_report-source.md",
  literatureAudit: "research/r072w_literature_audit.md",
  gapMatrix: "research/r072w_gap_matrix.md",
  independentAudit: "research/r072w_independent_audit.md",
  producer: "research/certificates/r072w/generate_certificate.py",
  independentProducer: "research/certificates/r072w/independent_recompute.py",
  comparator: "research/certificates/r072w/validate_certificate.py",
  certificateDirectory: "research/certificates/r072w",
  figureDirectory: figure,
  generator: "scripts/generate_r072w_release.py",
  translationScript: "scripts/add-r072w-translations.mjs",
  releaseGate: "tests/r072w-exact-periodic-gate.test.mjs",
  publicationTest: "tests/r072w-release.test.mjs",
};

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function absent(relative) {
  await assert.rejects(
    access(resolve(root, relative)),
    (error) => error?.code === "ENOENT",
    relative,
  );
}

function nodeIndex(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  return recap.slice(start, end);
}

async function assertSourceStage() {
  const [manifest, site, archive, noteFiles, home, recap] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    json("research/formal-archive-inventory.json"),
    readdir(resolve(publicRoot, "notes")),
    text("public/research-review.html"),
    text("public/recap-r0-61-r0-72v.html"),
  ]);
  assert.deepEqual({
    latest: manifest.latestCompletedRelease,
    version: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount,
    recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease,
    gate: manifest.latestReleaseGate,
    publicationTest: manifest.latestReleasePublicationTest,
    published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  }, {
    latest: "r072v", version: "1.35", notes: 172, recap: 112,
    next: "r072w",
    gate: "tests/r072v-whole-line-graph-gate.test.mjs",
    publicationTest: "tests/r072v-release.test.mjs",
    published: 74, sealed: 50, backlog: 24,
  });
  assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.35",
    latestRelease: "R0.72V",
    publicHtmlNoteCount: 172,
    publishedDate: "2026-08-28",
  });
  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 172);
  assert.match(home, /<strong>172<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72V<\/strong>最新研究节点/);
  assert.match(home, /NEXT · R0\.72W/);
  assert.doesNotMatch(home, /data-release="r072w"/);
  const links = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(links.length, 112);
  assert.equal(new Set(links).size, 112);
  assert.equal([...recap.matchAll(/<article class="phase">/g)].length, 31);
  assert.deepEqual({
    latest: archive.latestPublishedRelease,
    published: archive.publishedReleaseCount,
    sealed: archive.formalSealedReleaseCount,
    backlog: archive.legacyFormalFigureBacklogCount,
  }, { latest: "r072v", published: 74, sealed: 50, backlog: 24 });
  for (const relative of [
    "research/certificates/r072w/certificate.json",
    "research/certificates/r072w/independent.json",
    "research/certificates/r072w/crosscheck.json",
    "research/certificates/r072w/manifest.json",
    "research/certificates/r072w/SHA256SUMS",
    figure + "/data.csv",
    figure + "/results.json",
    figure + "/validation.json",
    figure + "/figure.svg",
    figure + "/figure.pdf",
    figure + "/figure.png",
    figure + "/manifest.json",
    figure + "/SHA256SUMS",
    "public/assets/r072w",
    "public/notes/r0-72w.html",
    "public/notes/r0-72w.pdf",
    "public/recap-r0-61-r0-72w.html",
    "public/recap-r0-61-r0-72w.pdf",
  ]) await absent(relative);
}

async function inspectPdf(relative) {
  const pdf = await readFile(resolve(root, relative));
  const source = pdf.toString("latin1");
  const pages = [...source.matchAll(/\/Type\s*\/Page\b/g)].length;
  const titleHex = source.match(/\/Title\s*<([0-9a-f]+)>/i)?.[1];
  assert.ok(titleHex, relative + ": hexadecimal PDF title metadata");
  const bytes = Buffer.from(titleHex, "hex");
  const units = [];
  if (bytes[0] === 0xfe && bytes[1] === 0xff) {
    for (let index = 2; index + 1 < bytes.length; index += 2) {
      units.push(bytes.readUInt16BE(index));
    }
  }
  return {
    pages,
    title: units.length ? String.fromCharCode(...units) : bytes.toString("latin1"),
    bytes: pdf.length,
    source,
  };
}

async function verifyFlatHashLedger(relative) {
  const directory = resolve(root, relative);
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, "malformed SHA256SUMS row: " + row);
    const [, expected, name] = match;
    const actual = createHash("sha256")
      .update(await readFile(resolve(directory, name))).digest("hex");
    assert.equal(actual, expected, name);
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries
      .filter((entry) => entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name))
      .map((entry) => entry.name).sort(),
  );
}

test("R0.72W release source freezes exact-tail identity, counters, and write order", async () => {
  const [generator, translationScript] = await Promise.all([
    text("scripts/generate_r072w_release.py"),
    text("scripts/add-r072w-translations.mjs"),
  ]);
  for (const token of [
    "保留解析尾项的精确周期块收缩：",
    "有界—逃逸胞元二分",
    "Exact-tail periodic contraction through the compact–escaping cell dichotomy",
    "figures/r072w-exact-periodic",
    "fig-r072w-exact-tail-transfer",
    '"siteVersion": "1.36"',
    '"notes": 173',
    '"recapNodes": 113',
    '"published": 75',
    '"formalSealed": 51',
    '"phases": 32',
    '"routeNotes": 83',
    '"next": "R0.72X"',
    "outer A1 plus A2 exact time concatenation",
  ]) assert.ok(generator.includes(token), token);
  const main = generator.slice(generator.indexOf("def main() -> None:"));
  const calls = [
    "preflight_release_state()",
    "validate_inputs()",
    "build_note()",
    "build_recap()",
    "update_home()",
    "update_literature()",
    "update_manifests()",
  ].map((call) => main.indexOf(call));
  assert.ok(calls.every((index) => index >= 0));
  assert.deepEqual(calls, [...calls].sort((left, right) => left - right));
  assert.ok(generator.indexOf("_validate_source_stage_manifest(release)") >= 0);
  assert.match(generator, /two-commit lineage/);
  assert.match(generator, /globalTermwiseRemainderAbsorptionFalse/);
  assert.match(generator, /outerTimeConcatenationProved/);
  for (const token of [
    "R072W_RELEASE_ROOT",
    "scripts/i18n-snapshots/r072w-missing.json",
    "/i18n-en.js?v=1.36",
    "notes/r0-72w.html",
    "recap-r0-61-r0-72w.html",
    "__DERIVED_FROM_R072V_ROUTE__",
    "R0.72W translations are stale",
  ]) assert.ok(translationScript.includes(token), token);
  assert.doesNotMatch(translationScript, /r072v-missing\.json|i18n-en\.js\?v=1\.35/);
});

test("R0.72W advances public state atomically to v1.36 / 173 / 113 / 32", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072v") {
    await assertSourceStage();
    return;
  }
  assert.equal(manifest.nextReleaseSourceStage, undefined);
  const [site, archive, noteFiles, home, recap] = await Promise.all([
    json("public/site-version.json"),
    json("research/formal-archive-inventory.json"),
    readdir(resolve(publicRoot, "notes")),
    text("public/research-review.html"),
    text("public/recap-r0-61-r0-72w.html"),
  ]);
  assert.deepEqual({
    latest: manifest.latestCompletedRelease,
    version: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount,
    recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease,
    gate: manifest.latestReleaseGate,
    publicationTest: manifest.latestReleasePublicationTest,
    published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  }, {
    latest: "r072w", version: "1.36", notes: 173, recap: 113,
    next: "r072x",
    gate: "tests/r072w-exact-periodic-gate.test.mjs",
    publicationTest: "tests/r072w-release.test.mjs",
    published: 75, sealed: 51, backlog: 24,
  });
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.36",
    latestRelease: "R0.72W",
    publicHtmlNoteCount: 173,
    publishedDate: "2026-08-28",
  });
  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 173);
  assert.match(home, /<strong>173<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72W<\/strong>最新研究节点/);
  assert.match(home, /NEXT · R0\.72X/);
  assert.match(home, /累计回顾收录 113 个节点；全站现有 173 篇公开研究笔记/);
  const links = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(links.length, 113);
  assert.equal(new Set(links).size, 113);
  assert.equal(links[0], "r0-61");
  assert.equal(links.at(-1), "r0-72w");
  assert.equal(links.filter((slug) => slug === "r0-72w").length, 1);
  assert.equal([...recap.matchAll(/<article class="phase">/g)].length, 32);
  assert.deepEqual({
    latest: archive.latestPublishedRelease,
    published: archive.publishedReleaseCount,
    sealed: archive.formalSealedReleaseCount,
    backlog: archive.legacyFormalFigureBacklogCount,
  }, { latest: "r072w", published: 75, sealed: 51, backlog: 24 });
  assert.equal(archive.publishedReleases.at(-1), "r072w");
  assert.equal(archive.formalSealedReleases.at(-1), "r072w");
});

test("R0.72W public prose is bilingual-ready, individual, and claim-neutral", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072v") {
    await assertSourceStage();
    return;
  }
  const pages = await Promise.all([
    "public/notes/r0-72w.html",
    "public/recap-r0-61-r0-72w.html",
    "public/research-review.html",
    "public/literature-review.html",
  ].map(text));
  for (const page of pages) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.36"/);
    assert.doesNotMatch(page, /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /[A-Za-z0-9_}]\\\(/);
  }
  assert.match(pages.join("\n"), /我/);
  const [note, recap, home, literature] = pages;
  for (const token of [
    "weightedNonabsorbedRemainderEstimate",
    "growingCoreAbsorption",
    "globalTermwiseRemainderAbsorption",
    "exactFamilyUnitCellCoercivity",
    "exactWholeLineGraphCoercivity",
    "exactPeriodicGraphCoercivity",
    "exactPeriodicBlockContraction",
    "outerTimeConcatenation",
    "timeLengthUniformity",
    "full inherited", "maximal graph class", "constant-one direct-sum",
    "H_5", "H_7", "H_9", "R0.72X", "Clay",
  ]) assert.ok(note.includes(token), token);
  assert.match(note, /H_D\^\{-1\}\(J_\\ell\).*H_0\^1\(J_\\ell\)/s);
  assert.match(note, /v\\in L\^2\(I;H\^1\(J_\\ell\)\).*Qv\\in L\^2\(I;H_D\^\{-1\}\(J_\\ell\)\)/s);
  assert.match(note, /exactPeriodicGraphCoercivity\s*[:=]\s*CLOSED/);
  assert.match(note, /exactPeriodicBlockContraction\s*[:=]\s*CLOSED/);
  assert.match(note, /globalTermwiseRemainderAbsorption\s*[:=]\s*FALSE/);
  assert.match(note, /timeLengthUniformity\s*[:=]\s*FALSE/);
  assert.match(note, /outerTimeConcatenation\s*[:=]\s*OPEN/);
  assert.match(note, /exact periodic scalar collision-block contraction/i);
  assert.match(note, /numericalDiagnosticIsProof=FALSE/);
  assert.match(note, /every.*\\?\(L\^2\\?\)|every-torus-\\?\(L\^2\\?\)/i);
  assert.match(note, /compact--escaping|compact–escaping/);
  assert.match(recap, /R0\.61–R0\.72W/);
  assert.match(recap, /exact periodic.*collision-block contraction/is);
  assert.match(recap, /outerTimeConcatenation.*OPEN/is);
  assert.match(home, /data-release="r072w"/);
  assert.match(literature, /id="r072w-boundary"/);
  assert.match(literature, /开放接口 · R0\.72X/);
  assert.match(literature, /exactPeriodicGraphCoercivity=CLOSED/);
  assert.match(literature, /globalTermwiseRemainderAbsorption=FALSE/);
  assert.match(literature, /一般 Navier–Stokes 正则性仍开放/);
});

test("R0.72W publishes note+PDF and recap+PDF with formal figure bytes", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072v") {
    await assertSourceStage();
    return;
  }
  for (const [relative, tokens, bodyUris] of [
    ["public/notes/r0-72w.pdf", ["R0.72W"], [
      "https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072w_report-source.md",
      "https://kasifa.github.io/assets/r072w/fig-r072w-exact-tail-transfer.pdf",
      "https://kasifa.github.io/recap-r0-61-r0-72w.html",
    ]],
    ["public/recap-r0-61-r0-72w.pdf", ["R0.61", "R0.72W"], [
      "https://kasifa.github.io/notes/r0-72w.html",
      "https://kasifa.github.io/assets/r072w/fig-r072w-exact-tail-transfer.pdf",
    ]],
  ]) {
    const inspected = await inspectPdf(relative);
    assert.ok(inspected.bytes > 10_000);
    assert.ok(inspected.pages >= 2 && inspected.pages <= 40);
    for (const token of tokens) assert.ok(inspected.title.includes(token), relative + ": " + token);
    for (const uri of bodyUris) {
      assert.ok(inspected.source.includes(`/URI (${uri})`), relative + ": " + uri);
    }
  }

  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  const [certificateManifest, crosscheck, figureManifest] = await Promise.all([
    json(certificate + "/manifest.json"),
    json(certificate + "/crosscheck.json"),
    json(figure + "/manifest.json"),
  ]);
  assert.equal(certificateManifest.status, "formal");
  assert.match(certificateManifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.deepEqual(certificateManifest.claimBoundary, {
    finiteExactAlgebraCertified: true,
    analyticExactPeriodicUnitChartTheoremProvedInBoundReport: true,
    analyticTorusGraphTheoremProvedInBoundReport: true,
    analyticPeriodicScalarEnergyContractionProvedInBoundReport: true,
    exactPeriodicScalarTransferProved: true,
    heatSeriesBeyondH9MachineChecked: false,
    compactnessArgumentMachineChecked: false,
    scalarEndpointTracePassageMachineChecked: false,
    varyingCellGraphSpacePassageMachineChecked: false,
    torusHMinusOneDirectSumMachineChecked: false,
    nonautonomousEvolutionExistenceMachineChecked: false,
    timeLengthUniformity: false,
    nonlinearNavierStokesClosureProved: false,
    clayMillenniumProblemSolved: false,
  });
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.formalSourceReady, true);
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
  assert.equal(crosscheck.sourceCommit, certificateManifest.sourceCommit);
  assert.deepEqual(crosscheck.sourceBindings, certificateManifest.sourceBindings);
  assert.ok(Object.values(crosscheck.checks).every((value) => value === true));
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.release, "R0.72W");
  assert.equal(figureManifest.figureId, figureId);
  assert.equal(figureManifest.git.sourceCommit, certificateManifest.sourceCommit);
  assert.match(figureManifest.git.certificateCommit, /^[0-9a-f]{40}$/);
  assert.notEqual(figureManifest.git.certificateCommit, figureManifest.git.sourceCommit);
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  assert.equal(figureManifest.publication.directory, "public/assets/r072w");
  assert.deepEqual(figureManifest.claimBoundary, {
    weightedNonabsorbedRemainderEstimateProved: true,
    growingCoreAbsorptionProved: true,
    globalTermwiseRemainderAbsorptionFalse: true,
    exactFamilyUnitCellCoercivityProved: true,
    exactWholeLineGraphCoercivityProved: true,
    exactPeriodicGraphCoercivityProved: true,
    exactPeriodicBlockContractionProved: true,
    numericalDiagnosticIsProof: false,
    numericalDiagnosticDeterminesAnalyticConstant: false,
    outerTimeConcatenationProved: false,
    timeLengthUniformity: false,
    nonlinearNavierStokesClosureProved: false,
    clayMillenniumProblemSolved: false,
  });
  await run(python, [certificate + "/validate_certificate.py", "--require-formal"], { cwd: root });
  await run(python, [figure + "/validate.py", "--require-formal"], { cwd: root });

  const note = await text("public/notes/r0-72w.html");
  for (const suffix of ["pdf", "png", "svg"]) {
    const master = await readFile(resolve(root, figure, "figure." + suffix));
    const route = "/assets/r072w/" + figureId + "." + suffix;
    const published = await readFile(resolve(publicRoot, route.slice(1)));
    assert.equal(Buffer.compare(master, published), 0, suffix);
    assert.ok(note.includes(route), route);
  }
});

test("R0.72W bilingual dictionary covers every live Chinese string exactly", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072v") {
    await assertSourceStage();
    return;
  }
  const translations = await json("translations/en.json");
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry.en]));
  assert.equal(byChinese.size, translations.length);
  const source = await collectSiteStrings(publicRoot);
  const missing = source.filter((entry) => !byChinese.has(entry.zh));
  assert.deepEqual(missing, []);
  for (const entry of source) {
    const english = byChinese.get(entry.zh);
    assert.ok(english?.trim(), entry.zh);
    assert.doesNotMatch(english, /[\u3400-\u9fff]/);
    assert.doesNotMatch(english, /\b(?:we|our|ours|ourselves|us)\b/i);
    assert.deepEqual(extractProtectedTokens(english), extractProtectedTokens(entry.zh), entry.zh);
  }
  const bundle = await text("public/i18n-en.js");
  assert.match(bundle, /R0\.72W/);
  assert.match(bundle, /Exact-tail periodic contraction through the compact–escaping cell dichotomy/i);
  assert.match(bundle, /exactPeriodicBlockContraction/);
  assert.match(bundle, /outerTimeConcatenation/);
});
