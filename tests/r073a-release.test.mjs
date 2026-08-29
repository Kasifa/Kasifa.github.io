import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "../scripts/i18n-lib.mjs";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");
const certificate = "research/certificates/r073a";
const figure = "figures/r073a/fig-r073a-hidden-mean-transient-spectral";
const figureId = "fig-r073a-hidden-mean-transient-spectral";
const run = promisify(execFile);

const expectedSourceStage = {
  release: "r073a",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r073a_report-source.md",
  problemFreeze: "research/r073a_problem_freeze.md",
  literatureAudit: "research/r073a_literature_audit.md",
  gapMatrix: "research/r073a_gap_matrix.md",
  analyticProof: "research/r073a_transient_proof.md",
  projectionDerivation: "research/r073a_projection_derivation_agent.md",
  projectionIndependentAudit: "research/r073a_projection_independent_audit.md",
  independentAnalyticAudit: "research/r073a_independent_analytic_audit.md",
  spectralAudit: "research/r073a_spectral_audit_agent.md",
  producer: `${certificate}/generate_certificate.py`,
  independentProducer: `${certificate}/independent_recompute.py`,
  comparator: `${certificate}/validate_certificate.py`,
  certificateDirectory: certificate,
  experimentDirectory: "experiments/r073a",
  figureDirectory: figure,
  generator: "scripts/generate_r073a_release.py",
  translationScript: "scripts/add-r073a-translations.mjs",
  translationSnapshot: "scripts/i18n-snapshots/r073a-missing.json",
  releaseGate: "tests/r073a-hidden-mean-gate.test.mjs",
  publicationTest: "tests/r073a-release.test.mjs",
  certificateSourceTest: "tests/r073a-deterministic-certificate-source.test.mjs",
  figureSourceTest: "tests/r073a-hidden-mean-transient-spectral-figure-source.test.mjs",
};

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function absent(relative) {
  await assert.rejects(access(resolve(root, relative)), (error) => error?.code === "ENOENT", relative);
}

async function sha(relative) {
  return createHash("sha256").update(await readFile(resolve(root, relative))).digest("hex");
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
  for (const phrase of ["我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法"]) {
    assert.ok(!value.includes(phrase), `${label}: ${phrase}`);
  }
}

async function verifyFlatHashLedger(relative) {
  const directory = resolve(root, relative);
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8")).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
    assert.equal(await sha(`${relative}/${match[2]}`), match[1], match[2]);
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries.filter((entry) => entry.isFile() && entry.name !== "SHA256SUMS").map((entry) => entry.name).sort(),
  );
}

async function inspectPdf(relative) {
  const bytes = await readFile(resolve(root, relative));
  const latin = bytes.toString("latin1");
  return { bytes: bytes.length, pages: [...latin.matchAll(/\/Type\s*\/Page\b/g)].length };
}

test("R0.73A release source freezes counters, semantics, and fail-closed write order", async () => {
  const [generator, translationScript] = await Promise.all([
    text("scripts/generate_r073a_release.py"),
    text("scripts/add-r073a-translations.mjs"),
  ]);
  for (const token of [
    "R072Z_RELEASE_BASELINE", "SOURCE_STAGE_CONTRACT",
    "exactPhysicalMeanOSCancellation=CLOSED",
    "exactPhysicalTangentLiftedLineNoninvariance=CLOSED",
    "rankOneAbstractTangentClosesPhysicalLongWaveLimit=FALSE",
    "lifted one-dimensional invariant-state meaning",
    "fixedTwoHarmonicOSInvariance=FALSE 只在 \\(c\\ne0\\)",
    "common dense domain \\(D\\)", "strong \\(C^1\\) solution", "adjoint-domain compatibility",
    "不单独断言 standalone quotient 的 well-posedness",
    "raw \\(Q^*\\mathscr B^*\\psi\\)", "实际 OS off-block 还乘 \\(|c|\\)",
    "\\inf_d\\|\\phi(d)\\|_2>0", "|c|/g\\to\\infty",
    "不声称无共同空间识别时 \\(g=0\\) 与 \\(g>0\\) 的算子范数不连续",
    "c_\\mu\\to c_0\\ne0", "fixed \\(\\Lambda\\)", "X_\\mu", "viscous-rate",
    "lowGapPhysicalKineticPropagator=OPEN", "lowGapOSSquirePropagator=OPEN",
    "BlochUniformPhysicalVelocityDirectSum=OPEN", "nonlinearNavierStokes=OPEN", "Clay=OPEN",
    "壁法向平均速度", "隐藏均值、analytic envelope", "fixed-\\(\\Lambda\\)",
    "certificateBoundCrosscheckTolerance", "2e-8",
    '"bound-by-figure-manifest"',
    '"siteVersion": "1.40"', '"notes": 177', '"recapNodes": 117',
    '"published": 79', '"formalSealed": 55', '"legacyBacklog": 24',
    '"phases": 36', '"routeNotes": 87', '"next": "R0.73B"',
    '(ROOT / "VERSION").write_text("1.40\\n"',
  ]) assert.ok(generator.includes(token), token);
  const article = generator.match(/NOTE_ARTICLE = r'''([\s\S]*?)'''/)?.[1] ?? "";
  assert.ok(article.length > 1000);
  for (const stale of [
    "fig-r072z-os-squire-threshold", "压力反馈的高间隙阈值", "必须支付的 Squire 方向代价",
  ]) assert.ok(!article.includes(stale), stale);
  assert.ok(!generator.includes("物理均速"));
  const main = generator.slice(generator.indexOf("def main() -> None:"));
  const calls = [
    "preflight_release_state()", "validate_inputs()", "build_note()", "build_recap()",
    "update_home()", "update_literature()", "update_manifests()",
  ].map((call) => main.indexOf(call));
  assert.ok(calls.every((index) => index >= 0));
  assert.deepEqual(calls, [...calls].sort((left, right) => left - right));
  assert.ok(generator.indexOf("validate_inputs()") < generator.indexOf("build_note()"));
  assert.ok(generator.includes('subprocess.run([sys.executable, str(certificate / "validate_certificate.py"), "--require-formal"]'));
  assert.doesNotMatch(generator, /(?:weasyprint|wkhtmltopdf|playwright|chromium).*pdf/i);
  assert.match(translationScript, /R073A_RELEASE_ROOT/);
  assert.match(translationScript, /i18n-en\.js\?v=1\.40/);
  assert.match(translationScript, /i18n-snapshots\/r073a-missing\.json/);
  assert.match(translationScript, /r073a\$\{String\(index \+ 1\)/);
  assert.match(translationScript, /\bwe\|our\|ours\|ourselves\|us\b/);
  assertPublicVoice(article, "R0.73A article source");
  for (const relative of ["scripts/generate_r073a_release.py", "scripts/add-r073a-translations.mjs"]) {
    const bytes = await readFile(resolve(root, relative));
    for (const byte of bytes) assert.ok(byte === 9 || byte === 10 || byte === 13 || byte >= 32, `${relative}: control byte ${byte}`);
  }
});

test("R0.73A source and formal lifecycle never mix public counters", async () => {
  const [manifest, site, archive] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    json("research/formal-archive-inventory.json"),
  ]);
  if (manifest.latestCompletedRelease === "r072z") {
    assert.deepEqual({
      version: manifest.siteVersion, notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount, next: manifest.nextRelease,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, { version: "1.39", notes: 176, recap: 116, next: "r073a", published: 78, sealed: 54, backlog: 24 });
    assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
    assert.deepEqual(site, {
      schemaVersion: "research-site-version-v1", version: "1.39", latestRelease: "R0.72Z",
      publicHtmlNoteCount: 176, publishedDate: "2026-08-28",
    });
    assert.deepEqual({
      latest: archive.latestPublishedRelease, published: archive.publishedReleaseCount,
      sealed: archive.formalSealedReleaseCount, backlog: archive.legacyFormalFigureBacklogCount,
    }, { latest: "r072z", published: 78, sealed: 54, backlog: 24 });
    for (const relative of [
      "public/notes/r0-73a.html", "public/notes/r0-73a.pdf",
      "public/recap-r0-61-r0-73a.html", "public/recap-r0-61-r0-73a.pdf",
    ]) await absent(relative);
    assert.equal(await text("VERSION"), "1.39\n");
    return;
  }
  assert.deepEqual({
    latest: manifest.latestCompletedRelease, version: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount, recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease, gate: manifest.latestReleaseGate,
    publicationTest: manifest.latestReleasePublicationTest,
    published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  }, {
    latest: "r073a", version: "1.40", notes: 177, recap: 117, next: "r073b",
    gate: "tests/r073a-hidden-mean-gate.test.mjs",
    publicationTest: "tests/r073a-release.test.mjs",
    published: 79, sealed: 55, backlog: 24,
  });
  assert.equal(manifest.nextReleaseSourceStage, undefined);
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1", version: "1.40", latestRelease: "R0.73A",
    publicHtmlNoteCount: 177, publishedDate: "2026-08-29",
  });
  assert.equal(await text("VERSION"), "1.40\n");
  assert.deepEqual({
    latest: archive.latestPublishedRelease, published: archive.publishedReleaseCount,
    sealed: archive.formalSealedReleaseCount, backlog: archive.legacyFormalFigureBacklogCount,
  }, { latest: "r073a", published: 79, sealed: 55, backlog: 24 });
  assert.equal(archive.publishedReleases.at(-1), "r073a");
  assert.equal(archive.formalSealedReleases.at(-1), "r073a");
});

test("formal R0.73A pages preserve the 117-node route and scoped claims", async (t) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073a") return t.skip("source stage");
  const [note, recap, home, literature, noteFiles] = await Promise.all([
    text("public/notes/r0-73a.html"), text("public/recap-r0-61-r0-73a.html"),
    text("public/research-review.html"), text("public/literature-review.html"),
    readdir(resolve(publicRoot, "notes")),
  ]);
  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 177);
  for (const [claim, status] of [
    ["exactPhysicalMeanOSCancellation", "CLOSED"],
    ["exactPhysicalTangentLiftedLineNoninvariance", "CLOSED"],
    ["exactMovingTangentQuotientAlgebra", "CLOSED"],
    ["rankOneAbstractTangentClosesPhysicalLongWaveLimit", "FALSE"],
    ["lowGapOSTransientA2Propagator", "OPEN"],
    ["lowGapPhysicalKineticPropagator", "OPEN"],
    ["lowGapOSSquirePropagator", "OPEN"],
    ["BlochUniformPhysicalVelocityDirectSum", "OPEN"],
    ["nonlinearNavierStokes", "OPEN"], ["Clay", "OPEN"],
  ]) assert.ok(note.includes(`${claim}=${status}`), `${claim}=${status}`);
  for (const token of [
    "隐藏均值、analytic envelope", "c_\\mu\\to c_0\\ne0", "fixed \\(\\Lambda\\)",
    "X_\\mu", "viscous-rate", "lifted one-dimensional invariant-state meaning",
    "common dense domain \\(D\\)", "strong \\(C^1\\) solution",
    "adjoint-domain compatibility", "standalone quotient 的 well-posedness",
    "当 \\(c\\ne0\\) 时不是完整 OS 不变子空间", "|c|/g\\to\\infty",
  ]) assert.ok(note.includes(token), token);
  for (const stale of [
    "fig-r072z-os-squire-threshold", "压力反馈的高间隙阈值", "必须支付的 Squire 方向代价",
  ]) assert.ok(!note.includes(stale), stale);
  const index = nodeIndex(recap);
  const links = [...index.matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map((match) => match[1]);
  assert.equal(links.length, 117);
  assert.equal(new Set(links).size, 117);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 36);
  assert.ok(index.includes('/notes/r0-73a.html'));
  assert.match(home, /data-site-version="1\.40"/);
  assert.match(home, /<strong>177<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.73A<\/strong>最新研究节点/);
  assert.equal((home.match(/data-release="r073a"/g) ?? []).length, 1);
  assert.equal((home.match(/<strong style="color:var\(--gold\)">下一步 R0\.73B：/g) ?? []).length, 1);
  assert.equal((home.match(/<strong style="color:var\(--gold\)">下一步 R0\.73A：/g) ?? []).length, 0);
  assert.equal((home.match(/当时的下一步 R0\.73A：/g) ?? []).length, 1);
  const route = home.match(/<nav class="route-note-links" aria-label="R0\.69P–R0\.73A">([\s\S]*?)<\/nav>/)?.[1] ?? "";
  assert.equal((route.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length, 87);
  assert.ok(literature.includes('id="r073a-boundary"'));
  assert.ok(literature.includes("bounded primary-source search"));
  for (const [label, value] of [["note", note], ["recap", recap], ["home", home], ["literature", literature]]) {
    assertPublicVoice(value, label);
    assert.ok(value.includes('/i18n-en.js?v=1.40'), `${label}: i18n cache`);
  }
});

test("formal R0.73A translation dictionary is complete and singular-voice", async (t) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073a") return t.skip("source stage");
  const [source, translations, snapshot] = await Promise.all([
    collectSiteStrings(publicRoot), json("translations/en.json"),
    json("scripts/i18n-snapshots/r073a-missing.json"),
  ]);
  const r073a = translations.filter((entry) => /^r073a\d+$/.test(entry.id));
  assert.equal(r073a.length, snapshot.length);
  assert.ok(r073a.length > 0);
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry.en]));
  assert.equal(byChinese.size, translations.length);
  for (const entry of source) {
    const en = byChinese.get(entry.zh);
    assert.ok(en, entry.zh);
    assert.equal(containsChinese(en), false, entry.zh);
    assert.deepEqual(extractProtectedTokens(en), extractProtectedTokens(entry.zh), entry.zh);
    assert.deepEqual(boundaryTokens(en), boundaryTokens(entry.zh), entry.zh);
    assert.doesNotMatch(en, /\b(?:we|our|ours|ourselves|us)\b/i, entry.zh);
  }
  const result = await run(process.execPath, ["scripts/add-r073a-translations.mjs", "--check-only"], {
    cwd: root, maxBuffer: 8 * 1024 * 1024,
  });
  assert.match(result.stdout, /"missingAfter":0/);
});

test("formal R0.73A certificate, experiment, figure, and publication assets remain lineage-bound", async (t) => {
  const release = await json("research/release-manifest.json");
  if (release.latestCompletedRelease !== "r073a") return t.skip("source stage");
  await Promise.all([verifyFlatHashLedger(certificate), verifyFlatHashLedger(figure)]);
  const [certManifest, crosscheck, experiment, figureManifest, figureContract] = await Promise.all([
    json(`${certificate}/manifest.json`), json(`${certificate}/crosscheck.json`),
    json("experiments/r073a/manifest.json"), json(`${figure}/manifest.json`),
    json(`${figure}/contract.json`),
  ]);
  assert.equal(certManifest.status, "formal");
  assert.match(certManifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(crosscheck.status, "passed");
  assert.equal(crosscheck.formalSourceReady, true);
  assert.equal(crosscheck.temporaryUnsealedSourceAllowed, false);
  assert.equal(crosscheck.sourceCommit, certManifest.sourceCommit);
  assert.deepEqual(crosscheck.sourceBindings, certManifest.sourceBindings);
  assert.ok(Object.values(crosscheck.checks).every(Boolean));
  assert.equal(experiment.status, "completed");
  assert.equal(experiment.finiteDimensionalOnly, true);
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.figureId, figureId);
  assert.equal(figureContract.chartContract.certificateBoundCrosscheckTolerance, 2e-8);
  assert.equal(figureManifest.dependency.available, true);
  assert.equal(figureManifest.dependency.syntheticSubstitutionAllowed, false);
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  const sourceCommit = certManifest.sourceCommit;
  const certificateCommit = figureManifest.git.certificateCommit;
  assert.equal(figureManifest.git.sourceCommit, sourceCommit);
  assert.match(certificateCommit, /^[0-9a-f]{40}$/);
  assert.notEqual(certificateCommit, sourceCommit);
  await run("git", ["merge-base", "--is-ancestor", sourceCommit, certificateCommit], { cwd: root });
  const csv = (await text("experiments/r073a/xmu_propagator_certificate.csv")).trimEnd().split("\n");
  assert.equal(csv[0], "certificateId,s,d,mu,c,gain,bound,sourceCommit,certificateCommit");
  assert.ok(csv.length > 1);
  for (const row of csv.slice(1)) {
    const cells = row.split(",");
    assert.equal(cells.length, 9);
    assert.equal(cells[7], sourceCommit);
    assert.ok(["pending", "bound-by-figure-manifest", certificateCommit].includes(cells[8]));
    assert.ok(Number(cells[5]) > 0 && Number(cells[5]) <= Number(cells[6]) + 2e-8);
  }
  for (const suffix of ["pdf", "svg", "png"]) {
    assert.equal(await sha(`${figure}/figure.${suffix}`), await sha(`public/assets/r073a/${figureId}.${suffix}`), suffix);
  }
  for (const relative of ["public/notes/r0-73a.pdf", "public/recap-r0-61-r0-73a.pdf"]) {
    const pdf = await inspectPdf(relative);
    assert.ok(pdf.bytes > 10_000, `${relative}: bytes`);
    assert.ok(pdf.pages >= 1, `${relative}: pages`);
  }
});
