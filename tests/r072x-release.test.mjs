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
const certificate = "research/certificates/r072x";
const figure = "figures/r072x-all-center/fig-r072x-all-center-transfer";
const figureId = "fig-r072x-all-center-transfer";

const expectedSourceStage = {
  release: "r072x",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072x_report-source.md",
  literatureAudit: "research/r072x_literature_audit.md",
  gapMatrix: "research/r072x_gap_matrix.md",
  independentAudit: "research/r072x_independent_audit.md",
  producer: "research/certificates/r072x/generate_certificate.py",
  independentProducer: "research/certificates/r072x/independent_recompute.py",
  comparator: "research/certificates/r072x/validate_certificate.py",
  certificateDirectory: certificate,
  figureDirectory: figure,
  generator: "scripts/generate_r072x_release.py",
  translationScript: "scripts/add-r072x-translations.mjs",
  releaseGate: "tests/r072x-exact-path-gate.test.mjs",
  publicationTest: "tests/r072x-release.test.mjs",
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

function boundaryTokens(value) {
  return value.match(/\b(?:CLOSED|OPEN|FALSE)\b/g) ?? [];
}

function assertPublicVoice(value, label) {
  for (const phrase of ["我们", "攻关", "主攻", "突破"]) {
    assert.ok(!value.includes(phrase), `${label}: ${phrase}`);
  }
}

async function verifyFlatHashLedger(relative) {
  const directory = resolve(root, relative);
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
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

async function inspectPdf(relative) {
  const pdf = await readFile(resolve(root, relative));
  const source = pdf.toString("latin1");
  return {
    bytes: pdf.length,
    pages: [...source.matchAll(/\/Type\s*\/Page\b/g)].length,
    source,
  };
}

test("R0.72X release source freezes counters, names, and write order", async () => {
  const [generator, translationScript, snapshot] = await Promise.all([
    text("scripts/generate_r072x_release.py"),
    text("scripts/add-r072x-translations.mjs"),
    json("scripts/i18n-snapshots/r072x-missing.json"),
  ]);
  for (const token of [
    "从任意起点传播精确碰撞族：",
    "外区 A1 与中心 A2 的无损拼接",
    "figures/r072x-all-center",
    figureId,
    '"siteVersion": "1.37"',
    '"notes": 174',
    '"recapNodes": 114',
    '"published": 76',
    '"formalSealed": 52',
    '"legacyBacklog": 24',
    '"phases": 33',
    '"routeNotes": 84',
    '"next": "R0.72Y"',
    '(ROOT / "VERSION").write_text("1.37\\n"',
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
  assert.equal((generator.match(/^def _validate_source_stage_manifest/gm) ?? []).length, 1);
  assert.ok(generator.indexOf("validate_inputs()") < generator.indexOf("build_note()"));
  assert.match(generator, /q_\{K,T\}\^\{-1\}/);
  assert.match(generator, /allPhysicalRowsUniformContraction=FALSE/);
  assert.ok(generator.includes("uniformTwistedPeriodicGraph=CLOSED，但该结论只用于 A2 exact path"));
  assert.ok(generator.includes("periodic representative \\(\\beta=0\\)"));
  assert.ok(generator.includes("periodicRepresentativeBetaZeroExactA1A2A1ConcatenationProvedInBoundReport"));
  assert.ok(!generator.includes('"exactA1A2A1ConcatenationProvedInBoundReport"'));
  assert.ok(generator.includes('"a1A2A1ConcatenationBlochUniform": False'));
  assert.ok(generator.includes("if set(claims) != set(expected_claims):"));
  assert.ok(!generator.includes("拼接保留 Bloch twist"));
  assert.ok(!snapshot.some((entry) => entry.zh.includes("拼接保留 Bloch twist")));
  assert.match(translationScript, /R072X_RELEASE_ROOT/);
  assert.match(translationScript, /i18n-en\.js\?v=1\.37/);
  assert.match(translationScript, /__DERIVED_FROM_R072W_ROUTE__/);
  assert.equal(snapshot.length, 119);
  assert.equal(new Set(snapshot.map((entry) => entry.zh)).size, 119);
  assertPublicVoice(generator, "generator");
});

test("R0.72X source and formal lifecycle never mix counters", async () => {
  const [manifest, site, archive] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    json("research/formal-archive-inventory.json"),
  ]);
  if (manifest.latestCompletedRelease === "r072w") {
    assert.deepEqual({
      version: manifest.siteVersion,
      notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount,
      next: manifest.nextRelease,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, { version: "1.36", notes: 173, recap: 113, next: "r072x", published: 75, sealed: 51, backlog: 24 });
    if (manifest.nextReleaseSourceStage !== undefined) {
      assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
    }
    assert.deepEqual(site, {
      schemaVersion: "research-site-version-v1",
      version: "1.36",
      latestRelease: "R0.72W",
      publicHtmlNoteCount: 173,
      publishedDate: "2026-08-28",
    });
    assert.deepEqual({
      latest: archive.latestPublishedRelease,
      published: archive.publishedReleaseCount,
      sealed: archive.formalSealedReleaseCount,
      backlog: archive.legacyFormalFigureBacklogCount,
    }, { latest: "r072w", published: 75, sealed: 51, backlog: 24 });
    for (const relative of [
      "public/notes/r0-72x.html",
      "public/notes/r0-72x.pdf",
      "public/recap-r0-61-r0-72x.html",
      "public/recap-r0-61-r0-72x.pdf",
      `public/assets/r072x/${figureId}.svg`,
      `public/assets/r072x/${figureId}.pdf`,
      `public/assets/r072x/${figureId}.png`,
      "VERSION",
    ]) await absent(relative);
    return;
  }
  assert.equal(manifest.latestCompletedRelease, "r072x");
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
    version: "1.37", notes: 174, recap: 114, next: "r072y",
    gate: "tests/r072x-exact-path-gate.test.mjs",
    publicationTest: "tests/r072x-release.test.mjs",
    published: 76, sealed: 52, backlog: 24,
  });
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.37",
    latestRelease: "R0.72X",
    publicHtmlNoteCount: 174,
    publishedDate: "2026-08-28",
  });
  assert.equal(await text("VERSION"), "1.37\n");
  assert.deepEqual({
    latest: archive.latestPublishedRelease,
    published: archive.publishedReleaseCount,
    sealed: archive.formalSealedReleaseCount,
    backlog: archive.legacyFormalFigureBacklogCount,
  }, { latest: "r072x", published: 76, sealed: 52, backlog: 24 });
  assert.equal(archive.publishedReleases.at(-1), "r072x");
  assert.equal(archive.formalSealedReleases.at(-1), "r072x");
});

test("formal R0.72X pages preserve the exact boundary and cumulative route", async (t) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r072x") return t.skip("source stage");
  const [note, recap, home, literature, noteFiles] = await Promise.all([
    text("public/notes/r0-72x.html"),
    text("public/recap-r0-61-r0-72x.html"),
    text("public/research-review.html"),
    text("public/literature-review.html"),
    readdir(resolve(publicRoot, "notes")),
  ]);
  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 174);
  for (const [label, status] of [
    ["allStartExactPathSemigroup", "CLOSED"],
    ["exactA1A2A1TimeConcatenation", "CLOSED"],
    ["shrinkingInterfaceFixedShapeA1Hypotheses", "FALSE"],
    ["prefactorOneAllGapExponential", "FALSE"],
    ["allPhysicalRowsUniformContraction", "FALSE"],
    ["forcedHMinusOneTransfer", "OPEN"],
    ["completeLinearizedShearSubsystem", "OPEN"],
    ["nonlinearNavierStokes", "OPEN"],
    ["Clay", "OPEN"],
  ]) assert.ok(note.includes(`${label}=${status}`), `${label}=${status}`);
  assert.match(note, /q_\{K,T\}\^\{-1\}/);
  assert.match(note, /2T\\alpha\^2/);
  assert.match(note, new RegExp(`/assets/r072x/${figureId}\\.svg`));
  assert.match(note, /R0\.72Y：恢复完整线性化 row ledger/);
  assert.match(note, /uniformTwistedPeriodicGraph=CLOSED，但该结论只用于 A2 exact path/);
  assert.ok(note.includes(
    "A1--A2--A1 cocycle 只声明 periodic representative \\(\\beta=0\\)",
  ));
  const links = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(links.length, 114);
  assert.equal(new Set(links).size, 114);
  assert.equal(links.at(-1), "r0-72x");
  assert.equal([...recap.matchAll(/<article class="phase">/g)].length, 33);
  assert.match(recap, /R0\.69P–R0\.72X/);
  assert.match(recap, /76 节已公开；52 节完整封存；24 节旧档待回补/);
  assert.match(recap, /uniformTwistedPeriodicGraph=CLOSED 只属于 exact A2 path/);
  assert.match(recap, /A1--A2--A1 fast history 只声明 periodic representative beta=0/);
  assert.match(home, /data-site-version="1\.37"/);
  assert.match(home, /<strong>174<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72X<\/strong>最新研究节点/);
  assert.equal((home.match(/data-release="r072x"/g) ?? []).length, 1);
  assert.match(home, /all-start、integrated scale 与 Bloch twists 只属于 A2 exact path/);
  assert.match(home, /fast-history cocycle 只声明 periodic representative beta=0/);
  const route = home.match(/<nav class="route-note-links" aria-label="R0\.69P–R0\.72X">([\s\S]*?)<\/nav>/)?.[1];
  assert.ok(route);
  assert.equal((route.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length, 84);
  assert.match(literature, /开放接口 · R0\.72Y/);
  assert.match(literature, /id="r072x-boundary"/);
  assert.match(literature, /Coble--He Theorem 1\.2/);
  assert.match(literature, /all-center、all-start 与 Bloch-uniformity 只属于 exact A2 path/);
  assert.match(literature, /periodic representative beta=0 的 fixed-margin A1 propagation/);
  for (const [value, label] of [[note, "note"], [recap, "recap"], [home, "home"], [literature, "literature"]]) {
    assertPublicVoice(value, label);
    assert.match(value, /\/i18n-en\.js\?v=1\.37/);
    assert.ok(!value.includes("拼接保留 Bloch twist"), `${label}: stale Bloch-scope sentence`);
  }
});

test("formal R0.72X figure and certificate retain formal byte lineage", async (t) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r072x") return t.skip("source stage");
  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  const [certificateManifest, crosscheck, figureManifest] = await Promise.all([
    json(`${certificate}/manifest.json`),
    json(`${certificate}/crosscheck.json`),
    json(`${figure}/manifest.json`),
  ]);
  assert.equal(certificateManifest.status, "formal");
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.formalSourceReady, true);
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.figureId, figureId);
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.git.sourceCommit, certificateManifest.sourceCommit);
  assert.match(figureManifest.git.certificateCommit, /^[0-9a-f]{40}$/);
  assert.notEqual(figureManifest.git.sourceCommit, figureManifest.git.certificateCommit);
  for (const extension of ["svg", "pdf", "png"]) {
    const master = await readFile(resolve(root, `${figure}/figure.${extension}`));
    const publication = await readFile(resolve(root, `public/assets/r072x/${figureId}.${extension}`));
    assert.deepEqual(publication, master, `public ${extension} must equal formal master`);
  }
});

test("formal R0.72X English coverage is exact and singular-voice", async (t) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r072x") return t.skip("source stage");
  const [translations, snapshot, source] = await Promise.all([
    json("translations/en.json"),
    json("scripts/i18n-snapshots/r072x-missing.json"),
    collectSiteStrings(publicRoot),
  ]);
  const batch = translations.filter((entry) => /^r072x\d{3}$/.test(entry.id));
  assert.equal(batch.length, snapshot.length);
  assert.equal(batch.length, 119);
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
  const bundle = await text("public/i18n-en.js");
  assert.match(bundle, /globalThis\.NS_EN_TRANSLATIONS = Object\.freeze/);
});

test("formal R0.72X synchronized PDFs are nontrivial", async (t) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r072x") return t.skip("source stage");
  const [note, recap] = await Promise.all([
    inspectPdf("public/notes/r0-72x.pdf"),
    inspectPdf("public/recap-r0-61-r0-72x.pdf"),
  ]);
  assert.ok(note.bytes > 100_000 && note.pages >= 4);
  assert.ok(recap.bytes > 100_000 && recap.pages >= 15);
  assert.match(note.source, /\/Title\s*</);
  assert.match(recap.source, /\/Title\s*</);
});
