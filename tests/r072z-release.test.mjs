import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "../scripts/i18n-lib.mjs";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");
const certificate = "research/certificates/r072z";
const figure = "figures/r072z/fig-r072z-os-squire-threshold";
const figureId = "fig-r072z-os-squire-threshold";

const expectedSourceStage = {
  release: "r072z",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072z_report-source.md",
  literatureAudit: "research/r072z_literature_audit.md",
  gapMatrix: "research/r072z_gap_matrix.md",
  independentAudit: "research/r072z_independent_audit.md",
  producer: "research/certificates/r072z/generate_certificate.py",
  independentProducer: "research/certificates/r072z/independent_recompute.py",
  comparator: "research/certificates/r072z/validate_certificate.py",
  certificateDirectory: certificate,
  figureDirectory: figure,
  generator: "scripts/generate_r072z_release.py",
  translationScript: "scripts/add-r072z-translations.mjs",
  releaseGate: "tests/r072z-os-squire-gate.test.mjs",
  publicationTest: "tests/r072z-release.test.mjs",
};

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function exists(relative) {
  try {
    await access(resolve(root, relative));
    return true;
  } catch (error) {
    if (error?.code === "ENOENT") return false;
    throw error;
  }
}

async function absent(relative) {
  await assert.rejects(access(resolve(root, relative)), (error) => error?.code === "ENOENT", relative);
}

function nodeIndex(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  return recap.slice(start, end);
}

function boundaryTokens(value) {
  return value.match(/\b(?:CLOSED|OPEN|FALSE)\b/g) ?? [];
}

function assertPublicVoice(value, label) {
  for (const phrase of ["我们", "攻关", "主攻", "突破", "三重审计", "杀死错误想法"]) {
    assert.ok(!value.includes(phrase), label + ": " + phrase);
  }
}

async function verifyFlatHashLedger(relative) {
  const directory = resolve(root, relative);
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8")).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, "malformed SHA256SUMS row: " + row);
    const actual = createHash("sha256").update(await readFile(resolve(directory, match[2]))).digest("hex");
    assert.equal(actual, match[1], match[2]);
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(names, entries.filter((entry) => entry.isFile() && entry.name !== "SHA256SUMS").map((entry) => entry.name).sort());
}

async function inspectPdf(relative) {
  const pdf = await readFile(resolve(root, relative));
  const source = pdf.toString("latin1");
  return { bytes: pdf.length, pages: [...source.matchAll(/\/Type\s*\/Page\b/g)].length, source };
}

test("R0.72Z release source freezes counters, boundaries, and write order", async () => {
  const [generator, translationScript] = await Promise.all([
    text("scripts/generate_r072z_release.py"),
    text("scripts/add-r072z-translations.mjs"),
  ]);
  for (const token of [
    "压力反馈的高间隙阈值",
    "必须支付的 Squire 方向代价",
    "high-gap q graph: CLOSED",
    "low-gap physical row: OPEN",
    "figures/r072z",
    figureId,
    '"siteVersion": "1.39"',
    '"notes": 176',
    '"recapNodes": 116',
    '"published": 78',
    '"formalSealed": 54',
    '"legacyBacklog": 24',
    '"phases": 35',
    '"routeNotes": 86',
    '"next": "R0.73A"',
    '(ROOT / "VERSION").write_text("1.39\\n"',
    "overflow-wrap:anywhere",
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
  assert.ok(generator.indexOf("validate_inputs()") < generator.indexOf("build_note()"));
  assert.equal((generator.match(/^def _validate_source_stage_manifest/gm) ?? []).length, 1);
  assert.ok(generator.includes('certificate_manifest.get("status") != "formal"'));
  assert.ok(generator.includes("temporaryUnsealedSourceAllowed"));
  assert.ok(generator.includes("certificate_commit == source_commit"));
  assert.ok(generator.includes("expected_bound_sources"));
  assert.ok(generator.includes("expected_claims"));
  assert.ok(generator.includes("allStrongRowsOSPrefactorOneContraction"));
  assert.ok(generator.includes("lowGapOSTransientA2Propagator"));
  assert.ok(generator.includes("\\Theta_K(c,\\beta,\\mu)=\\sup_{d\\in K}\\lambda_{\\max}(-cH_{\\beta,\\mu}(d))"));
  assert.ok(generator.includes("\\Theta_K\\le\\widehat\\Theta_K:=|c|M_{3,K}g^{-3/2}s_{\\beta,\\mu}"));
  assert.ok(generator.includes("a_j(d)=|\\xi\\Lambda|b_j(d)"));
  assert.ok(generator.includes("\\chi_j=\\frac{|\\xi|}{\\sqrt g}\\le1"));
  assert.match(translationScript, /R072Z_RELEASE_ROOT/);
  assert.match(translationScript, /i18n-en\.js\?v=1\.39/);
  assert.match(translationScript, /r072z\$\{String\(index \+ 1\)/);
  assertPublicVoice(generator, "generator");
  const bytes = await readFile(resolve(root, "scripts/generate_r072z_release.py"));
  for (const byte of bytes) assert.ok(byte === 9 || byte === 10 || byte === 13 || byte >= 32, "generator control byte " + byte);
});

test("R0.72Z source and formal lifecycle never mix counters", async () => {
  const [manifest, site, archive] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    json("research/formal-archive-inventory.json"),
  ]);
  if (manifest.latestCompletedRelease === "r072y") {
    assert.deepEqual({
      version: manifest.siteVersion,
      notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount,
      next: manifest.nextRelease,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, { version: "1.38", notes: 175, recap: 115, next: "r072z", published: 77, sealed: 53, backlog: 24 });
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
    assert.deepEqual(site, {
      schemaVersion: "research-site-version-v1",
      version: "1.38",
      latestRelease: "R0.72Y",
      publicHtmlNoteCount: 175,
      publishedDate: "2026-08-28",
    });
    assert.deepEqual({
      latest: archive.latestPublishedRelease,
      published: archive.publishedReleaseCount,
      sealed: archive.formalSealedReleaseCount,
      backlog: archive.legacyFormalFigureBacklogCount,
    }, { latest: "r072y", published: 77, sealed: 53, backlog: 24 });
    for (const relative of [
      "public/notes/r0-72z.html",
      "public/notes/r0-72z.pdf",
      "public/recap-r0-61-r0-72z.html",
      "public/recap-r0-61-r0-72z.pdf",
    ]) await absent(relative);
    assert.equal(await text("VERSION"), "1.38\n");
    return;
  }
  assert.equal(manifest.latestCompletedRelease, "r072z");
  assert.equal(manifest.nextReleaseSourceStage, undefined);
  assert.deepEqual({
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
    version: "1.39", notes: 176, recap: 116, next: "r073a",
    gate: "tests/r072z-os-squire-gate.test.mjs",
    publicationTest: "tests/r072z-release.test.mjs",
    published: 78, sealed: 54, backlog: 24,
  });
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.39",
    latestRelease: "R0.72Z",
    publicHtmlNoteCount: 176,
    publishedDate: "2026-08-28",
  });
  assert.equal(await text("VERSION"), "1.39\n");
  assert.deepEqual({
    latest: archive.latestPublishedRelease,
    published: archive.publishedReleaseCount,
    sealed: archive.formalSealedReleaseCount,
    backlog: archive.legacyFormalFigureBacklogCount,
  }, { latest: "r072z", published: 78, sealed: 54, backlog: 24 });
  assert.equal(archive.publishedReleases.at(-1), "r072z");
  assert.equal(archive.formalSealedReleases.at(-1), "r072z");
});

test("formal R0.72Z pages preserve scoped boundaries and the cumulative route", async (t) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r072z") return t.skip("source stage");
  const [note, recap, home, literature, noteFiles] = await Promise.all([
    text("public/notes/r0-72z.html"),
    text("public/recap-r0-61-r0-72z.html"),
    text("public/research-review.html"),
    text("public/literature-review.html"),
    readdir(resolve(publicRoot, "notes")),
  ]);
  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 176);
  for (const [label, status] of [
    ["exactOSFeedbackCommutatorIdentity", "CLOSED"],
    ["signedRelativeFormOSAbsorption", "CLOSED"],
    ["highGapOSPrefactorOneDecay", "CLOSED"],
    ["exactSquireDuhamel", "CLOSED"],
    ["orientationUniformWithLambdaPayment", "CLOSED"],
    ["fixedRowOSSquireGraphRegularity", "CLOSED"],
    ["allStrongRowsOSPrefactorOneContraction", "FALSE"],
    ["rawOrientationUniformFromCOnly", "FALSE"],
    ["uniformlyEquivalentLambdaIndependentContractiveNorm", "FALSE"],
    ["lowGapOSTransientA2Propagator", "OPEN"],
    ["unconditionalStrongFullRowA2Estimate", "OPEN"],
    ["nonlinearNavierStokes", "OPEN"],
    ["Clay", "OPEN"],
  ]) assert.ok(note.includes(label + "=" + status), label + "=" + status);
  assert.match(note, /\\Theta_K\(c,\\beta,\\mu\)/);
  assert.match(note, /g\\gtrsim \|c\|\^\{2\/5\}/);
  assert.match(note, /\\chi_j=\\frac\{\|\\xi\|\}\{\\sqrt g\}/);
  assert.match(note, /\/assets\/r072z\/fig-r072z-os-squire-threshold\.svg/);
  assert.match(note, /R0\.73A：分离 tangent\/lift-up 子空间/);
  assert.match(note, /\.verdict-card p,[^{}]+\{overflow-wrap:anywhere;word-break:break-word\}/);
  const links = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map((match) => match[1]);
  assert.equal(links.length, 116);
  assert.equal(new Set(links).size, 116);
  assert.equal(links.at(-1), "r0-72z");
  assert.equal([...recap.matchAll(/<article class="phase">/g)].length, 35);
  assert.match(recap, /R0\.61–R0\.72Z/);
  assert.match(recap, /78 节已公开；54 节完整封存；24 节旧档待回补/);
  assert.match(recap, /lowGapOSTransientA2Propagator/);
  assert.match(home, /data-site-version="1\.39"/);
  assert.match(home, /<strong>176<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72Z<\/strong>最新研究节点/);
  assert.equal((home.match(/data-release="r072z"/g) ?? []).length, 1);
  const route = home.match(/<nav class="route-note-links" aria-label="R0\.69P–R0\.72Z">([\s\S]*?)<\/nav>/)?.[1];
  assert.ok(route);
  assert.equal((route.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length, 86);
  assert.match(literature, /开放接口 · R0\.73A/);
  assert.match(literature, /id="r072z-boundary"/);
  assert.match(literature, /Beekie--Chen--Jia/);
  assert.match(literature, /bounded primary-source search/);
  for (const [value, label] of [[note, "note"], [recap, "recap"], [home, "home"], [literature, "literature"]]) {
    assertPublicVoice(value, label);
    assert.match(value, /\/i18n-en\.js\?v=1\.39/);
  }
});

test("formal R0.72Z figure and certificate retain formal byte lineage", async (t) => {
  const release = await json("research/release-manifest.json");
  if (release.latestCompletedRelease !== "r072z") return t.skip("source stage");
  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  const [certificateManifest, crosscheck, figureManifest] = await Promise.all([
    json(certificate + "/manifest.json"),
    json(certificate + "/crosscheck.json"),
    json(figure + "/manifest.json"),
  ]);
  assert.equal(certificateManifest.status, "formal");
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.formalSourceReady, true);
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.figureId, figureId);
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.git.sourceCommit, certificateManifest.sourceCommit);
  assert.match(figureManifest.git.certificateCommit, /^[0-9a-f]{40}$/);
  assert.notEqual(figureManifest.git.sourceCommit, figureManifest.git.certificateCommit);
  for (const extension of ["svg", "pdf", "png"]) {
    assert.deepEqual(
      await readFile(resolve(root, figure, "figure." + extension)),
      await readFile(resolve(root, "public/assets/r072z", figureId + "." + extension)),
    );
  }
});

test("formal R0.72Z English coverage is exact and singular-voice", async (t) => {
  const release = await json("research/release-manifest.json");
  if (release.latestCompletedRelease !== "r072z") return t.skip("source stage");
  assert.equal(await exists("scripts/i18n-snapshots/r072z-missing.json"), true);
  const [translations, snapshot, source] = await Promise.all([
    json("translations/en.json"),
    json("scripts/i18n-snapshots/r072z-missing.json"),
    collectSiteStrings(publicRoot),
  ]);
  const batch = translations.filter((entry) => /^r072z\d{3}$/.test(entry.id));
  assert.equal(batch.length, snapshot.length);
  assert.ok(batch.length > 0);
  assert.deepEqual(batch.map((entry) => entry.zh), snapshot.map((entry) => entry.zh));
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry.en]));
  assert.equal(byChinese.size, translations.length);
  for (const entry of source) assert.ok(byChinese.has(entry.zh), entry.zh);
  for (const entry of batch) {
    assert.ok(entry.en.trim());
    assert.equal(containsChinese(entry.en), false, entry.zh);
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i, entry.zh);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh), entry.zh);
    assert.deepEqual(boundaryTokens(entry.en), boundaryTokens(entry.zh), entry.zh);
  }
  assert.match(await text("public/i18n-en.js"), /globalThis\.NS_EN_TRANSLATIONS = Object\.freeze/);
});

test("formal R0.72Z synchronized PDFs are nontrivial", async (t) => {
  const release = await json("research/release-manifest.json");
  if (release.latestCompletedRelease !== "r072z") return t.skip("source stage");
  const [note, recap] = await Promise.all([
    inspectPdf("public/notes/r0-72z.pdf"),
    inspectPdf("public/recap-r0-61-r0-72z.pdf"),
  ]);
  assert.ok(note.bytes > 100_000 && note.pages >= 4);
  assert.ok(recap.bytes > 100_000 && recap.pages >= 15);
  assert.match(note.source, /\/Title\s*</);
  assert.match(recap.source, /\/Title\s*</);
});
