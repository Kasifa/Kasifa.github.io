import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");

function pythonJson(...argumentsList) {
  const result = spawnSync("python3", argumentsList, {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
  assert.equal(result.status, 0, result.stderr || result.stdout);
  return JSON.parse(result.stdout);
}

test("release-content source check is read-only and keeps the exact analytic boundary", () => {
  const result = pythonJson("scripts/r073p_release_content.py", "--check-only");
  assert.equal(result.release, "R0.73P");
  assert.equal(result.title, "R0.73P | Critical stability, the N^{-1/2} frequency gate, and the early-time regularity gap");
  assert.equal(result.uniformL2OnlyStrongThreshold, "OPEN_COLLISION_SENSITIVE");
  assert.equal(result.writes, 0);
  assert.equal(result.canonicalSources, result.canonicalSourcesPlanned - result.missingCanonicalSources.length);
  assert.match(result.readinessDetail, /globalCriticalH12OrbitStability=CLOSED_AS_CLASSICAL_COROLLARY/);
  assert.match(result.readinessDetail, /bandLimitedL2ThresholdNMinusHalf=CLOSED_AS_COROLLARY/);
  assert.match(result.readinessDetail, /oneSidedDelayedL2ToH3Synchronization=CLOSED_AFTER_AUDIT/);
});

test("release generator source-dry-run exposes P accounting without public writes", () => {
  const result = pythonJson("scripts/generate_r073p_release.py", "--source-dry-run");
  assert.equal(result.release, "R0.73P");
  assert.equal(result.siteVersion, "1.56");
  assert.deepEqual(result.targetAccounting, {
    latestCompletedRelease: "r073p",
    siteVersion: "1.56",
    publicHtmlNoteCount: 192,
    postR060RecapNodeCount: 132,
    nextRelease: "r073q",
    postR070APublishedReleaseCount: 94,
    postR070AFormalSealedReleaseCount: 70,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.equal(result.writes, 0);
  assert.equal(result.commitPinsReady, true);
  assert.equal(result.uniformL2OnlyStrongThreshold, "OPEN_COLLISION_SENSITIVE");
  assert.equal(result.earlyWeakIntervalRegularity, "OPEN");
  assert.equal(result.clayConclusion, "OPEN");
  assert.ok(result.coreOutputsPlanned.includes("public/notes/r0-73p.html"));
  assert.ok(result.coreOutputsPlanned.includes("public/recap-r0-61-r0-73p.html"));
  assert.ok(result.laterStageOutputsPlanned.includes("research/r073p_pdf_bindings.json"));
});

test("reviewed input pins are frozen and the normalized source pin is explicit", () => {
  const generator = read("scripts/generate_r073p_release.py");
  assert.match(generator, /RELEASE_BASELINE_COMMIT = "6f082823fffcab7c637143c065da63d08bc4cce0"/);
  assert.match(generator, /ANALYTIC_SOURCE_COMMIT = "c087845e65034d2ba92b8a8330d90e36e77704d3"/);
  assert.match(generator, /FINITE_PACKAGE_COMMIT = "93af4cd3e5cb75de7767dac7c81f22a163381dfb"/);
  assert.match(generator, /FIGURE_PACKAGE_COMMIT = "e233018d16e8b2cf348b6eac7876170c0f5f1eaf"/);
  assert.match(generator, /FINAL_CONTENT_COMMIT = "32319c4ae2fd461f8ee30654e140aa02db4ed6b0"/);
  assert.match(generator, /RELEASE_SOURCE_COMMIT = (?:ZERO_COMMIT|"[0-9a-f]{40}")/);
  assert.ok(generator.includes('(\"R0.73O release baseline\", RELEASE_BASELINE_COMMIT)'));
  assert.ok(generator.includes('"--confirm-visual-qa"'));
});

test("canonical release source inventory contains all P prose and future packages", () => {
  const content = read("scripts/r073p_release_content.py");
  const generator = read("scripts/generate_r073p_release.py");
  for (const relative of [
    "research/r073p_problem_freeze.md",
    "research/r073p_critical_frequency_proof.md",
    "research/r073p_delayed_synchronization_proof.md",
    "research/r073p_literature_audit.md",
    "research/r073p_primary_literature_addendum.md",
    "research/r073p_independent_analytic_audit.md",
    "research/r073p_claim_source_ledger.md",
    "research/r073p_gap_matrix.md",
    "research/r073p_finite_diagnostic_audit.md",
    "research/r073p_report-source.md",
    "research/r073p_bilingual_dictionary.md",
  ]) {
    assert.ok(content.includes(`\"${relative}\"`), `content inventory missing ${relative}`);
  }
  assert.ok(generator.includes('FINITE_EXACT_ROOTS = ("research/certificates/r073p",)'));
  assert.ok(generator.includes("FIGURE_EXACT_ROOTS = (FIGURE_SOURCE_RELATIVE,)"));
  assert.ok(content.includes('FIGURE_ID = "fig-r073p-critical-frequency-gate"'));
});

test("translation and PDF-binding stages preserve the P/Q and open-claim boundary", () => {
  const translation = read("scripts/add-r073p-translations.mjs");
  const binding = read("scripts/bind-r073p-pdfs.mjs");
  for (const source of [translation, binding]) {
    assert.ok(source.includes("globalCriticalH12OrbitStability=CLOSED_AS_CLASSICAL_COROLLARY"));
    assert.ok(source.includes("bandLimitedL2ThresholdNMinusHalf=CLOSED_AS_COROLLARY"));
    assert.ok(source.includes("oneSidedDelayedL2ToH3Synchronization=CLOSED_AFTER_AUDIT"));
    assert.ok(source.includes("uniformL2OnlyStrongThreshold=OPEN_COLLISION_SENSITIVE"));
    assert.ok(source.includes("earlyWeakIntervalRegularity=OPEN"));
    assert.ok(source.includes("finiteAnalyticFigureProvesPDEThresholdNecessity=FALSE"));
    assert.ok(source.includes('nextRelease !== "r073q"'));
  }
  assert.ok(translation.includes('"notes/r0-73p.html"'));
  assert.ok(binding.includes('html: "public/notes/r0-73p.html"'));
  assert.ok(binding.includes('html: "public/recap-r0-61-r0-73p.html"'));
  assert.ok(binding.includes("pdfBindingCertifiesMathematicalCorrectness: false"));
  assert.ok(binding.includes("pdfBindingEstablishesNoveltyOrPriority: false"));
  assert.ok(binding.includes("clayProblemSolved: false"));
});
