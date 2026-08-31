import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const json = (relative) => JSON.parse(read(relative));

const analyticPaths = [
  "research/r073q_problem_freeze.md",
  "research/r073q_heat_flow_stability_proof.md",
  "research/r073q_endpoint_no_go.md",
  "research/r073q_primary_literature_audit.md",
  "research/r073q_independent_literature_readback.md",
  "research/r073q_independent_analytic_audit.md",
  "research/r073q_claim_source_ledger.md",
  "research/r073q_gap_matrix.md",
  "research/r073q_report-source.md",
  "research/r073q_bilingual_dictionary.md",
];
const corpus = analyticPaths.map(read).join("\n");

test("R0.73Q freezes the heat-flow theorem and exact open boundaries", () => {
  for (const token of [
    "periodicOseenHLS=CLOSED_AFTER_AUDIT",
    "linearizedVolterraInverse=CLOSED_AFTER_AUDIT",
    "uniformAllRestartRadius=CLOSED_AFTER_AUDIT",
    "H3SerrinBridge=CLOSED_AFTER_AUDIT",
    "periodicHeatFlowTube=CLOSED_AFTER_AUDIT",
    "strictExtensionByUnion=CLOSED",
    "heatFlowBallContainsEntirePublishedH12Ball=NOT_PROVED",
    "bareKatoSupFromL4L6=BLOCKED_BY_ENDPOINT",
    "fullKochTataruTheory=NOT_REFUTED",
    "uniformL2Only=OPEN",
    "nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN",
    "clayConclusion=OPEN",
    "noveltyOrPriorityClaim=FORBIDDEN",
  ]) {
    assert.ok(corpus.includes(token), `missing boundary token: ${token}`);
  }
  assert.ok(corpus.includes("ABSTRACT_ONLY_COLLISION"));
  assert.ok(!corpus.includes("largeBMOUniqueness="));
});

test("the analytic proof keeps the periodic HLS, Volterra, and strict-union interfaces", () => {
  const proof = read("research/r073q_heat_flow_stability_proof.md");
  for (const token of [
    "[0,2\\pi]^3",
    "Hardy--Littlewood--Sobolev inequality with order \\(1/4\\)",
    "L^2_t\\to L^4_t",
    "\\varepsilon_B:={1\\over4C_B}",
    "K[u]",
    "{1\\over8C_BK[u]^2}",
    "L^4((t_0,T_*);L^6)",
    "classical Serrin continuation criterion",
    "\\mathcal D_Q[u]",
    "\\supsetneq",
    "N^{-3/4}",
    "N^{1/4}",
  ]) {
    assert.ok(proof.replaceAll(" ", "").includes(token.replaceAll(" ", "")), token);
  }
});

test("the bare Kato-sup obstruction is exact and scoped", () => {
  const noGo = read("research/r073q_endpoint_no_go.md");
  for (const token of [
    "I_{1/4}:L^4\\to L^\\infty",
    "1-\\frac{\\log2}{n}",
    "n^{3/4}-n^{-1/4}\\log2",
    "fullKochTataruBilinearTheory=NOT_REFUTED",
  ]) {
    assert.ok(noGo.includes(token), token);
  }
});

test("the finite certificate binds 25 shear rows and 7 endpoint rows without PDE overclaim", () => {
  const base = "research/certificates/r073q";
  const manifest = json(`${base}/manifest.json`);
  const diagnostic = json(`${base}/diagnostic.json`);
  const certificate = json(`${base}/certificate.json`);
  assert.equal(manifest.schemaVersion, "r073q-finite-heat-flow-manifest-v1");
  assert.equal(manifest.status, "sealed");
  assert.equal(manifest.finalSeal, true);
  assert.deepEqual(manifest.checkInventory, { independent: 35, primary: 118, structural: 40 });
  assert.equal(diagnostic.totalRows, 32);
  assert.equal(diagnostic.modeRows, 25);
  assert.equal(diagnostic.timeMapRows, 7);
  assert.equal(certificate.formulaStatements.heatL4L6, "c6 4^(-1/4) N^(-3/4)");
  assert.equal(certificate.formulaStatements.timeMapFractionalValue, "n^(3/4)-n^(-1/4) log(2)");
  assert.equal(manifest.claimBoundary.finiteFormulaDiagnosticOnly, true);
  for (const key of [
    "navierStokesSimulation",
    "pdeEvolutionComputed",
    "globalRegularityEstablished",
    "clayProblemSolved",
  ]) {
    assert.equal(manifest.claimBoundary[key], false, key);
  }
  assert.equal(read(`${base}/source-data.csv`).trimEnd().split("\n").length, 33);
});

test("the formal figure interface uses the heat-flow separation id and 53 formula rows", () => {
  const base = "research/figures/r073q/fig-r073q-heat-flow-separation";
  const manifest = json(`${base}/manifest.json`);
  const results = json(`${base}/results.json`);
  const contract = json(`${base}/contract.json`);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figureId, "fig-r073q-heat-flow-separation");
  assert.equal(results.mode, "render-preseal");
  assert.equal(results.rowCount, 53);
  assert.equal(results.facts.shear.rowCount, 33);
  assert.equal(results.facts.endpoint.rowCount, 20);
  assert.equal(results.isNavierStokesSimulation, false);
  assert.equal(contract.claimBoundary.oldAndNewRadiiOrdered, false);
  assert.equal(contract.claimBoundary.fullKochTataruTheoryRefuted, false);
  assert.equal(contract.claimBoundary.clayProblemSolved, false);
});
