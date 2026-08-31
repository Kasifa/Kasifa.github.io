import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const json = (relative) => JSON.parse(read(relative));
const sha256 = (payload) => createHash("sha256").update(payload).digest("hex");

const analyticPaths = [
  "research/r073p_problem_freeze.md",
  "research/r073p_critical_frequency_proof.md",
  "research/r073p_delayed_synchronization_proof.md",
  "research/r073p_literature_audit.md",
  "research/r073p_primary_literature_addendum.md",
  "research/r073p_independent_analytic_audit.md",
  "research/r073p_claim_source_ledger.md",
  "research/r073p_gap_matrix.md",
  "research/r073p_report-source.md",
  "research/r073p_bilingual_dictionary.md",
];
const corpus = analyticPaths.map(read).join("\n");
const figureRoot = "research/figures/r073p/fig-r073p-critical-frequency-gate";

test("R0.73P freezes the three positive lanes and the three open boundaries", () => {
  for (const token of [
    "globalCriticalH12OrbitStability=CLOSED_AS_CLASSICAL_COROLLARY",
    "bandLimitedL2ThresholdNMinusHalf=CLOSED_AS_COROLLARY",
    "oneSidedDelayedL2ToH3Synchronization=CLOSED_AFTER_AUDIT",
    "uniformL2OnlyStrongThreshold=OPEN_COLLISION_SENSITIVE",
    "earlyWeakIntervalRegularity=OPEN",
    "clayConclusion=OPEN",
  ]) {
    assert.ok(corpus.includes(token), `missing boundary token: ${token}`);
  }
});

test("periodic normalization and the alpha=1/2 specialization stay explicit", () => {
  const proof = read("research/r073p_critical_frequency_proof.md");
  for (const token of [
    "[0,2\\pi]^3",
    "(2\\pi)^{-3}",
    "\\alpha=1/2",
    "K_2^c",
    "K_3^c",
    "(2\\pi)^6",
    "R_{1/2}[u]",
  ]) {
    assert.ok(proof.includes(token), `normalization/specialization drift: ${token}`);
  }
});

test("N^-1/2 norm-transfer sharpness is not promoted to PDE necessity", () => {
  const report = read("research/r073p_report-source.md");
  const dictionary = read("research/r073p_bilingual_dictionary.md");
  assert.ok(report.includes("|w_N|_{1/2}=r"));
  assert.ok(report.includes("|w_N|_3=rN^{5/2}\\to\\infty"));
  assert.ok(dictionary.includes("normTransferNMinusHalfSharp=CLOSED"));
  assert.ok(dictionary.includes("PDEDynamicalNMinusHalfSharp=NOT_CLAIMED"));
  assert.ok(dictionary.includes("finiteAnalyticFigureProvesPDEThresholdNecessity=FALSE"));
});

test("delayed synchronization remains one-sided and does not erase the early weak interval", () => {
  const proof = read("research/r073p_delayed_synchronization_proof.md");
  for (const token of [
    "T_3(M)",
    "oneSidedDelayedL2ToH3Synchronization=CLOSED_AFTER_AUDIT",
    "backwardRegularityInference=NOT_AVAILABLE",
  ]) {
    assert.ok(proof.includes(token), `delayed boundary drift: ${token}`);
  }
  assert.ok(corpus.includes("earlyWeakIntervalRegularity=OPEN"));
});

test("finite figure is an exact formula diagnostic, not a Navier--Stokes simulation", () => {
  const config = json(`${figureRoot}/config.json`);
  const contract = json(`${figureRoot}/contract.json`);
  const results = json(`${figureRoot}/results.json`);
  const validation = json(`${figureRoot}/validation.json`);
  assert.equal(config.figureId, "fig-r073p-critical-frequency-gate");
  assert.equal(contract.figureId, config.figureId);
  assert.equal(results.figureId, config.figureId);
  assert.equal(validation.figureId, config.figureId);
  assert.equal(results.rowCount, 790);
  assert.equal(results.formulas.directH3Threshold, "N^-3 after normalized radius");
  assert.equal(results.formulas.criticalHhalfThreshold, "N^-1/2 after normalized radius");
  assert.equal(results.isFormulaDiagnostic, true);
  assert.equal(results.isNavierStokesSimulation, false);
  assert.equal(contract.claimBoundary.navierStokesSimulation, false);
  assert.equal(contract.claimBoundary.nonlinearDuhamelControl, false);
  assert.equal(contract.claimBoundary.globalRegularityTheorem, false);
  assert.equal(contract.claimBoundary.clayProblemSolved, false);
  assert.equal(validation.allAutomatedChecksPass, true);
  assert.ok(Object.values(validation.checks).every((value) => value === true));
});

test("figure source-data hash and row accounting are internally bound", () => {
  const source = readFileSync(resolve(root, figureRoot, "source-data.csv"));
  const results = json(`${figureRoot}/results.json`);
  const record = results.outputs.find((row) => row.path === "source-data.csv");
  assert.ok(record);
  assert.equal(record.bytes, source.length);
  assert.equal(record.sha256, sha256(source));
  assert.equal(
    results.facts.panelA.rowCount + results.facts.panelB.rowCount + results.facts.panelC.rowCount,
    results.rowCount,
  );
});
