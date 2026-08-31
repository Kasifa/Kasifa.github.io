import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");

function runPython(...argumentsList) {
  return spawnSync("python3", argumentsList, {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
}

function pythonJson(...argumentsList) {
  const result = runPython(...argumentsList);
  assert.equal(result.status, 0, result.stderr || result.stdout);
  return JSON.parse(result.stdout);
}

test("release-content source check is read-only and keeps the exact R boundary", () => {
  const result = pythonJson("scripts/r073r_release_content.py", "--check-only");
  assert.equal(result.release, "R0.73R");
  assert.equal(result.title, "R0.73R | A shellwise phase certificate for the critical heat trace");
  assert.equal(result.publicationReady, true);
  assert.equal(result.canonicalSources, 10);
  assert.equal(result.canonicalSourcesPlanned, 10);
  assert.deepEqual(result.missingCanonicalSources, []);
  assert.equal(result.uniformL2OnlyStrongRadius, "OPEN");
  assert.equal(result.zeroNonlinearityBoundary, "CLOSED");
  assert.equal(result.translationPath, "LOCAL_DIRECT_NO_DGX");
  assert.match(result.readinessDetail, /periodicHeatBesovEquivalence=VERIFIED_CLASSICAL/);
  assert.match(result.readinessDetail, /formalFigurePackage=PASS/);
  assert.equal(result.writes, 0);
});

test("release generator source-dry-run exposes R accounting without public writes", () => {
  const generator = read("scripts/generate_r073r_release.py");
  const releaseSourcePinned = /RELEASE_SOURCE_COMMIT = "[0-9a-f]{40}"/.test(generator);
  const result = pythonJson("scripts/generate_r073r_release.py", "--source-dry-run");
  assert.equal(result.release, "R0.73R");
  assert.equal(result.siteVersion, "1.58");
  assert.deepEqual(result.targetAccounting, {
    latestCompletedRelease: "r073r",
    siteVersion: "1.58",
    publicHtmlNoteCount: 194,
    postR060RecapNodeCount: 134,
    nextRelease: "r073s",
    postR070APublishedReleaseCount: 96,
    postR070AFormalSealedReleaseCount: 72,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.equal(result.canonicalSources, 10);
  assert.equal(result.finalContentReady, true);
  assert.deepEqual(result.finalContentPending, []);
  assert.equal(result.figureSourcePresent, true);
  assert.equal(result.certificateSourcePresent, true);
  assert.equal(result.commitPinsReady, releaseSourcePinned);
  assert.equal(result.uniformL2OnlyStrongRadius, "OPEN");
  assert.equal(result.zeroNonlinearityBoundary, "CLOSED");
  assert.equal(result.translationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(result.clayConclusion, "OPEN");
  assert.ok(result.coreOutputsPlanned.includes("public/notes/r0-73r.html"));
  assert.ok(result.coreOutputsPlanned.includes("public/recap-r0-61-r0-73r.html"));
  assert.ok(result.laterStageOutputsPlanned.includes("research/r073r_pdf_bindings.json"));
  assert.equal(result.writes, 0);
});

test("reviewed A--D pins are exact and the release-source slot is normalized", () => {
  const generator = read("scripts/generate_r073r_release.py");
  assert.match(generator, /RELEASE_BASELINE_COMMIT = "66a523bcc49aadc4df81ab39542fc4dfdbac14d0"/);
  assert.match(generator, /ANALYTIC_SOURCE_COMMIT = "25b20d225202359de2fd2d95ed86dd4b372d23a5"/);
  assert.match(generator, /FINITE_PACKAGE_COMMIT = "6809fc92a2d1338fb77fb3bf5a72d16ed158d807"/);
  assert.match(generator, /FIGURE_PACKAGE_COMMIT = "f3d8ac3b04aa122a44f112d554c4991ecfb6f36e"/);
  assert.match(generator, /FINAL_CONTENT_COMMIT = "fb0ea0dfaf753de4c19b9155daf320b4fca8cb6a"/);
  assert.match(generator, /RELEASE_SOURCE_COMMIT = (?:ZERO_COMMIT|"[0-9a-f]{40}")/);
  assert.ok(generator.includes('RELEASE_SOURCE_COMMIT = "__NORMALIZED_RELEASE_SOURCE_COMMIT__"'));
  assert.ok(generator.includes('("R0.73Q release baseline", RELEASE_BASELINE_COMMIT)'));
  assert.ok(generator.includes('"tests/r073r-shell-phase-gate.test.mjs"'));
});

test("check-only fails closed before it can stage or write public outputs", () => {
  const generator = read("scripts/generate_r073r_release.py");
  if (/RELEASE_SOURCE_COMMIT = "[0-9a-f]{40}"/.test(generator)) {
    assert.ok(true, "release-source pin has been assigned; full check belongs to the final release stage");
    return;
  }
  const result = runPython("scripts/generate_r073r_release.py", "--check-only");
  assert.notEqual(result.status, 0);
  assert.match(result.stderr, /R0\.73R release source: unsealed 40-zero commit pin/);
  assert.match(result.stderr, /binding remains fail-closed/);
});

test("canonical inventories bind the R proof, classical collision audit, certificate, and figure", () => {
  const content = read("scripts/r073r_release_content.py");
  const generator = read("scripts/generate_r073r_release.py");
  for (const relative of [
    "research/r073r_problem_freeze.md",
    "research/r073r_shell_concentration_candidate.md",
    "research/r073r_lp_caloric_certificate_proof.md",
    "research/r073r_primary_literature_audit.md",
    "research/r073r_independent_analytic_audit.md",
    "research/r073r_claim_source_ledger.md",
    "research/r073r_evidence_gap_matrix.md",
    "research/r073r_finite_diagnostic_audit.md",
    "research/r073r_report-source.md",
    "research/r073r_bilingual_dictionary.md",
  ]) {
    assert.ok(content.includes(`"${relative}"`), `content inventory missing ${relative}`);
  }
  assert.ok(generator.includes('FINITE_EXACT_ROOTS = ("research/certificates/r073r",)'));
  assert.ok(generator.includes("FIGURE_EXACT_ROOTS = (FIGURE_SOURCE_RELATIVE,)"));
  assert.ok(content.includes('FIGURE_ID = "fig-r073r-phase-coherence"'));
});

test("reader-facing sources keep classical collision, zero nonlinearity, local translation, and NOT CLAY", () => {
  const report = read("research/r073r_report-source.md");
  const dictionary = read("research/r073r_bilingual_dictionary.md");
  for (const source of [report, dictionary]) {
    assert.ok(source.includes("translationPath=LOCAL_DIRECT_NO_DGX"));
    assert.doesNotMatch(source, /我们|攻关|主攻|突破|首次证明|原创性定理/);
  }
  assert.ok((report + dictionary).includes("NOT CLAY"));
  assert.ok(report.includes("函数空间内容是经典的周期负指标 Besov 热半群刻画，不是\n新定理"));
  assert.ok(report.includes("(W_{R,m}\\cdot\\nabla)W_{R,m}"));
  assert.ok(dictionary.includes("DGX is not used for translation"));
});
