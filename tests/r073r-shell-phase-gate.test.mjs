import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const json = (relative) => JSON.parse(read(relative));

const canonicalPaths = [
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
];
const corpus = canonicalPaths.map(read).join("\n");

test("R0.73R freezes the shell-phase theorem and exact open boundaries", () => {
  for (const token of [
    "periodicHeatBesovEquivalence=VERIFIED_CLASSICAL",
    "ell4ShellExponent=CLOSED_AFTER_AUDIT",
    "exactVectorTripleConvolution=CLOSED_EXACT_EVALUATION",
    "additiveMultiplicityCertificate=CLOSED",
    "supportCardinalityCertificate=CLOSED_SHARP_FROM_SUPPORT_ONLY",
    "matchedSupportMagnitudeQuadraticData=CLOSED_EXACT",
    "matchedPhaseHeatTraceSeparation=CLOSED_AFTER_AUDIT",
    "zeroNonlinearityBoundary=CLOSED",
    "exactConvolutionIsCheapAPrioriProxy=FALSE",
    "failureOfEntranceImpliesUnsafeDynamics=FALSE",
    "uniformL2OnlyStrongRadius=OPEN",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN",
    "clayConclusion=OPEN",
    "noveltyOrPriorityClaim=FORBIDDEN",
    "translationPath=LOCAL_DIRECT_NO_DGX",
  ]) {
    assert.ok(corpus.includes(token), `missing boundary token: ${token}`);
  }
  assert.ok(corpus.includes("NOT CLAY"));
});

test("the analytic proof keeps the two-sided ell4 trace and three certificate levels", () => {
  const proof = read("research/r073r_lp_caloric_certificate_proof.md").replace(/\s+/g, "");
  for (const token of [
    "\\|e^{t\\Delta}f\\|_{L^4((0,\\infty);L^6)}",
    "\\sum_{j\\ge0}2^{-2j}\\|P_jf\\|_6^4",
    "4^j+4^k",
    "2^{-|j-k|}",
    "T_{j,m}",
    "R_j^{1/6}E_j",
    "M_j^{1/3}E_j",
    "{11m^5+5m^3+4m\\over20}",
    "m^{2/3}",
    "g\\,\\partial_3(e_3g)=0",
  ]) {
    assert.ok(proof.includes(token.replaceAll(" ", "")), token);
  }
});

test("the literature ledger marks the heat-Besov mechanism as a direct classical collision", () => {
  const ledger = read("research/r073r_claim_source_ledger.md");
  assert.ok(ledger.includes("Chemin--Gallagher 2006"));
  assert.ok(ledger.includes("Rudin 1959"));
  assert.ok(ledger.includes("VERIFIED_CLASSICAL"));
  assert.ok(ledger.includes("not a novelty or priority result"));
});

test("the final certificate binds 16 rows without PDE or Clay overclaim", () => {
  const base = "research/certificates/r073r";
  const manifest = json(`${base}/manifest.json`);
  const diagnostic = json(`${base}/diagnostic.json`);
  const certificate = json(`${base}/certificate.json`);
  assert.equal(manifest.schemaVersion, "r073r-matched-phase-shell-manifest-v1");
  assert.equal(manifest.status, "sealed");
  assert.equal(manifest.finalSeal, true);
  assert.equal(manifest.sourceCommit, "25b20d225202359de2fd2d95ed86dd4b372d23a5");
  assert.deepEqual(manifest.checkInventory, { independent: 65, primary: 114, structural: 115 });
  assert.equal(diagnostic.rowCount, 16);
  assert.equal(certificate.rowCount, 16);
  assert.equal(certificate.formulaStatements.supportSize, "2*m^2");
  assert.equal(certificate.formulaStatements.dirichletUnivariateL6Sixth, "(11*m^5+5*m^3+4*m)/20");
  assert.equal(manifest.claimBoundary.finiteFormulaDiagnosticOnly, true);
  assert.equal(manifest.claimBoundary.matchedFourierSupportAndMagnitudes, true);
  for (const key of [
    "navierStokesSimulation",
    "heatFlowIntegralComputed",
    "pdeNecessityEstablished",
    "globalRegularityEstablished",
    "clayProblemSolved",
  ]) {
    assert.equal(manifest.claimBoundary[key], false, key);
  }
  assert.equal(read(`${base}/source-data.csv`).trimEnd().split("\n").length, 17);
});

test("the formal figure binds 141 analytic rows and the zero-convection boundary", () => {
  const base = "research/figures/r073r/fig-r073r-phase-coherence";
  const manifest = json(`${base}/manifest.json`);
  const results = json(`${base}/results.json`);
  const contract = json(`${base}/contract.json`);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figureId, "fig-r073r-phase-coherence");
  assert.equal(manifest.git.sourceCommit, "25b20d225202359de2fd2d95ed86dd4b372d23a5");
  assert.equal(results.mode, "render-preseal");
  assert.equal(results.rowCount, 141);
  assert.equal(results.facts.panelA.positivePacketRowCount, 128);
  assert.equal(results.facts.scaling.rowCount, 13);
  assert.equal(results.isNavierStokesSimulation, false);
  assert.equal(results.dgxUsed, false);
  assert.equal(contract.claimBoundary.fieldsHaveZeroConvection, true);
  assert.equal(contract.claimBoundary.unsafeDynamics, false);
  assert.equal(contract.claimBoundary.clayProblemSolved, false);
});
