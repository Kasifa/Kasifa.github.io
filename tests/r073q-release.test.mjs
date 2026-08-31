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

test("release-content source check is read-only and keeps the exact Q boundary", () => {
  const result = pythonJson("scripts/r073q_release_content.py", "--check-only");
  assert.equal(result.release, "R0.73Q");
  assert.equal(result.title, "R0.73Q | A critical heat-flow tube beyond the \\(H^{1/2}\\) entrance");
  assert.equal(result.publicationReady, true);
  assert.equal(result.canonicalSources, 11);
  assert.equal(result.canonicalSourcesPlanned, 11);
  assert.deepEqual(result.missingCanonicalSources, []);
  assert.equal(result.uniformL2Only, "OPEN");
  assert.equal(result.nonperturbativeBMOInverseUniqueness, "FALSE_IN_GENERAL");
  assert.match(result.readinessDetail, /periodicHeatFlowTube=CLOSED_AFTER_AUDIT/);
  assert.match(result.readinessDetail, /formalFigurePackage=PASS/);
  assert.equal(result.writes, 0);
});

test("release generator source-dry-run exposes Q accounting without public writes", () => {
  const result = pythonJson("scripts/generate_r073q_release.py", "--source-dry-run");
  assert.equal(result.release, "R0.73Q");
  assert.equal(result.siteVersion, "1.57");
  assert.deepEqual(result.targetAccounting, {
    latestCompletedRelease: "r073q",
    siteVersion: "1.57",
    publicHtmlNoteCount: 193,
    postR060RecapNodeCount: 133,
    nextRelease: "r073r",
    postR070APublishedReleaseCount: 95,
    postR070AFormalSealedReleaseCount: 71,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.equal(result.canonicalSources, 11);
  assert.equal(result.finalContentReady, true);
  assert.deepEqual(result.finalContentPending, []);
  assert.equal(result.figureSourcePresent, true);
  assert.equal(result.certificateSourcePresent, true);
  assert.equal(result.commitPinsReady, false);
  assert.equal(result.uniformL2Only, "OPEN");
  assert.equal(result.nonperturbativeBMOInverseUniqueness, "FALSE_IN_GENERAL");
  assert.equal(result.clayConclusion, "OPEN");
  assert.ok(result.coreOutputsPlanned.includes("public/notes/r0-73q.html"));
  assert.ok(result.coreOutputsPlanned.includes("public/recap-r0-61-r0-73q.html"));
  assert.ok(result.laterStageOutputsPlanned.includes("research/r073q_pdf_bindings.json"));
  assert.equal(result.writes, 0);
});

test("immutable reviewed pins are exact and the release-source zero pin fails closed", () => {
  const generator = read("scripts/generate_r073q_release.py");
  assert.match(generator, /RELEASE_BASELINE_COMMIT = "dfec6fa047c8dd9f498aa798df23c525812951b6"/);
  assert.match(generator, /ANALYTIC_SOURCE_COMMIT = "cb9511c3af08a4beb0b31284e96e2a9c47a23d04"/);
  assert.match(generator, /FINITE_PACKAGE_COMMIT = "a0b00c0ef7f425443c88445a5284381469ce4046"/);
  assert.match(generator, /FIGURE_PACKAGE_COMMIT = "6da152412e36c647449675cb3cfaf3c4dab4542f"/);
  assert.match(generator, /FINAL_CONTENT_COMMIT = "14803d7299473359a64c2c08d183d4f2a8152b1c"/);
  assert.match(generator, /RELEASE_SOURCE_COMMIT = ZERO_COMMIT/);
  assert.ok(generator.includes('(\"R0.73P release baseline\", RELEASE_BASELINE_COMMIT)'));
  assert.ok(generator.includes('"tests/r073q-critical-heat-flow-gate.test.mjs"'));

  const result = runPython("scripts/generate_r073q_release.py", "--check-only");
  assert.notEqual(result.status, 0);
  assert.match(
    `${result.stdout}\n${result.stderr}`,
    /R0\.73Q release source: unsealed 40-zero commit pin; binding remains fail-closed/,
  );
});

test("canonical inventories bind the Q proof, literature readback, finite audit, and figure", () => {
  const content = read("scripts/r073q_release_content.py");
  const generator = read("scripts/generate_r073q_release.py");
  for (const relative of [
    "research/r073q_problem_freeze.md",
    "research/r073q_heat_flow_stability_proof.md",
    "research/r073q_endpoint_no_go.md",
    "research/r073q_primary_literature_audit.md",
    "research/r073q_independent_literature_readback.md",
    "research/r073q_independent_analytic_audit.md",
    "research/r073q_claim_source_ledger.md",
    "research/r073q_gap_matrix.md",
    "research/r073q_finite_diagnostic_audit.md",
    "research/r073q_report-source.md",
    "research/r073q_bilingual_dictionary.md",
  ]) {
    assert.ok(content.includes(`\"${relative}\"`), `content inventory missing ${relative}`);
  }
  assert.ok(generator.includes('FINITE_EXACT_ROOTS = ("research/certificates/r073q",)'));
  assert.ok(generator.includes("FIGURE_EXACT_ROOTS = (FIGURE_SOURCE_RELATIVE,)"));
  assert.ok(content.includes('FIGURE_ID = "fig-r073q-heat-flow-separation"'));
});

test("translation and PDF binding preserve reviewed-local provenance and the Q boundary", () => {
  const translation = read("scripts/add-r073q-translations.mjs");
  const binding = read("scripts/bind-r073q-pdfs.mjs");
  for (const source of [translation, binding]) {
    assert.ok(source.includes("periodicHeatFlowTube=CLOSED_AFTER_AUDIT"));
    assert.ok(source.includes("bareKatoSupFromL4L6=BLOCKED_BY_ENDPOINT"));
    assert.ok(source.includes("fullKochTataruTheory=NOT_REFUTED"));
    assert.ok(source.includes("uniformL2Only=OPEN"));
    assert.ok(source.includes("nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL"));
    assert.ok(source.includes('nextRelease !== "r073r"'));
  }
  assert.ok(translation.includes("arbitraryThreeDimensionalGlobalRegularity=OPEN"));
  assert.ok(translation.includes('reviewed-local-direct-no-dgx-no-network'));
  assert.ok(translation.includes("has no network client, calls no translation service"));
  assert.ok(translation.includes("never\n// invokes DGX"));
  assert.ok(translation.includes('"notes/r0-73q.html"'));
  assert.ok(binding.includes('html: "public/notes/r0-73q.html"'));
  assert.ok(binding.includes('html: "public/recap-r0-61-r0-73q.html"'));
  assert.ok(binding.includes('R0.61–R0.73Q｜R0.60 之后的研究回顾'));
  assert.ok(binding.includes("pdfBindingCertifiesMathematicalCorrectness: false"));
  assert.ok(binding.includes("pdfBindingEstablishesNoveltyOrPriority: false"));
  assert.ok(binding.includes("clayProblemSolved: false"));
});
