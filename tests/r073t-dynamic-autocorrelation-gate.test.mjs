import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const json = (relative) => JSON.parse(read(relative));

const canonicalPaths = [
  "research/r073t_problem_freeze.md",
  "research/r073t_dynamic_autocorrelation_budget.md",
  "research/r073t_no_go_audit.md",
  "research/r073t_crosscheck_no_go.md",
  "research/r073t_independent_analytic_audit.md",
  "research/r073t_primary_literature_audit.md",
  "research/r073t_parent_draft_audit.md",
  "research/r073t_claim_source_ledger.md",
  "research/r073t_evidence_gap_matrix.md",
  "research/r073t_report-source.md",
  "research/r073t_bilingual_dictionary.md",
  "research/r073t_finite_diagnostic_audit.md",
];
const corpus = canonicalPaths.map(read).join("\n");

test("R0.73T keeps its internal, exact, classical, and open boundaries separate", () => {
  const report = read("research/r073t_report-source.md");
  for (const token of [
    "exactAutocorrelationEvolution=VERIFIED_CLASSICAL_RECONSTRUCTION",
    "dynamicAQUpperInequality=INTERNAL_COROLLARY",
    "criticalAIntegral=INTERNAL_EXACT_SCALING",
    "criticalAIntegralControl=OPEN",
    "carrierScaleNonAutonomy=CLOSED_EXACT",
    "signedVelocityPhaseInPressurePairing=CLOSED_EXACT",
    "pressureTensorNeededForGeneralReconstruction=VERIFIED_CLASSICAL",
    "finiteFormulaDiagnosticChecks=55",
    "formalFigureChecks=106",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN",
    "clayConclusion=OPEN",
    "NOT CLAY",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.doesNotMatch(report, /exactAutocorrelationEvolution=INTERNAL_EXACT(?:\r?\n|$)/);
  for (const phrase of [
    "not asserted as a new regularity criterion",
    "not a new dynamical theorem",
    "not a Navier--Stokes simulation",
    "non-detection is not proof of novelty, priority, or non-existence",
    "Clay Millennium problem remain open",
  ]) {
    assert.ok(corpus.replace(/\s+/g, " ").includes(phrase), phrase);
  }
  assert.doesNotMatch(report, /我们|攻关|主攻|突破|首次证明|原创性定理/);
});

test("the analytic source contains the exact law, quartic balance, AQ corollary, and closure boundary", () => {
  const proof = read("research/r073t_dynamic_autocorrelation_budget.md").replace(/\s+/g, "");
  for (const token of [
    "\\dotC_h=-\\nu|h|^2C_h",
    "-2\\nu\\widehat{|\\nablau|^2}(h)",
    "-ih\\cdot\\widehat{u(w+2p)}(h)",
    "Q'+4\\nuY+2\\nuX^2",
    "Q'+4\\nuY+\\nuX^2",
    "{4C_R^2\\over\\nu}AQ",
    "A\\inL_t^1",
    "u\\inL_t^2L_x^\\infty",
    "p=R_iR_jT_{ij}",
    "D^+",
    "(\\partial_t-\\nu\\partial_s)",
  ]) {
    assert.ok(proof.includes(token.replaceAll(" ", "")), token);
  }
  assert.ok(proof.includes("hasnotweakenedtheknowncriticalcontinuationthreshold"));
});

test("the sign pair isolates signed velocity phase and is not a tensor-or-pressure witness", () => {
  const report = read("research/r073t_report-source.md").replace(/\s+/g, " ");
  const dictionary = read("research/r073t_bilingual_dictionary.md").replace(/\s+/g, " ");
  assert.ok(report.includes("(-u_L)\\otimes(-u_L)=u_L\\otimes u_L"));
  assert.ok(report.includes("p[-u_L]=p[u_L]"));
  assert.ok(dictionary.includes(
    "The pair \\(u_L,-u_L\\) has the same \\(u\\otimes u\\) and the same \\(p\\)"));
  assert.ok(dictionary.includes("signed velocity phase entering the pressure pairing"));
  assert.ok(dictionary.includes(
    "is not a witness that \\(p\\) or the quadratic tensor \\(u\\otimes u\\) differs"));
  assert.ok(report.includes("pressureTensorNeededForGeneralReconstruction=VERIFIED_CLASSICAL"));
  assert.ok(report.includes("必须与该符号对证书分开陈述"));
});

test("the finite exact package closes 55 checks and no continuum PDE claim", () => {
  const base = "research/certificates/r073t";
  const results = json(`${base}/results.json`);
  const checklist = json(`${base}/audit-checklist.json`);
  const manifest = json(`${base}/manifest.json`);
  assert.equal(manifest.schemaVersion, "r073t-exact-no-go-manifest-v1");
  assert.equal(manifest.status, "sealed");
  assert.equal(manifest.finalSeal, true);
  assert.equal(manifest.sourceCommitAssigned, true);
  assert.equal(manifest.sourceCommit, "05c55d21f060a17a0a4db04c12e89e7271b03d30");
  assert.deepEqual(manifest.checkInventory, { exact: 55, required: 55 });
  assert.deepEqual(manifest.inventory, {
    boundFileCount: 7,
    generatedFileCount: 3,
    packageFileCount: 9,
    sha256SumsLineCount: 8,
    sourceFileCount: 6,
  });
  assert.equal(checklist.requiredChecks.length, 55);
  assert.equal(results.audit.passed, 55);
  assert.equal(results.audit.required, 55);
  assert.equal(results.audit.results.every((entry) => entry.pass), true);
  assert.equal(results.sixMode.finiteIdentities.E, "42");
  assert.equal(results.sixMode.finiteIdentities.Q, "2918");
  assert.equal(results.sixMode.finiteIdentities.A, "164");
  assert.equal(results.sixMode.finiteIdentities.D_C, 15);
  assert.equal(results.sixMode.finiteIdentities.X2, "4296");
  assert.equal(results.sixMode.finiteIdentities.Y, "1986");
  assert.equal(results.sixMode.finiteIdentities.N4, "-384");
  assert.equal(results.sixMode.finiteIdentities.N4MinusU, "384");
  assert.equal(results.sixMode.dilation.qDerivativeU, "-16536*nu*L^2-384*L");
  assert.equal(results.sixMode.dilation.qDerivativeMinusU, "-16536*nu*L^2+384*L");
  assert.equal(results.rotatingShear.completeAutocorrelation,
    "C_N(h)=1 if h=0, otherwise 0");
  assert.equal(results.rotatingShear.c0Derivative, "-2*nu*N^2");
  assert.match(manifest.claimBoundary, /no generic PDE integration.*global regularity.*Clay/i);
});

test("the formal figure binds 28 exact rows and 106 checks without strengthening the claim", () => {
  const base = "research/figures/r073t/fig-r073t-dynamic-autocorrelation";
  const manifest = json(`${base}/manifest.json`);
  const contract = json(`${base}/contract.json`);
  const validation = json(`${base}/validation.json`);
  const rows = read(`${base}/source-data.csv`).trimEnd().split("\n");
  assert.equal(manifest.schemaVersion, "r073t-dynamic-autocorrelation-figure-manifest-v1");
  assert.equal(manifest.figureId, "fig-r073t-dynamic-autocorrelation");
  assert.equal(manifest.allChecksPass, true);
  assert.equal(manifest.validationCheckCount, 106);
  assert.equal(manifest.visualQaConfirmed, true);
  assert.equal(manifest.sourceCommit, "05c55d21f060a17a0a4db04c12e89e7271b03d30");
  assert.equal(manifest.inventory.packageFileCount, 25);
  assert.equal(manifest.inventory.sourceFileCount, 10);
  assert.equal(manifest.inventory.rawFileCount, 11);
  assert.equal(rows.length - 1, 28);
  assert.equal(validation.checkCount, 106);
  assert.equal(validation.allChecksPass, true);
  assert.equal(validation.checks.every((entry) => entry.pass), true);
  assert.equal(contract.compute.dgxUsed, false);
  for (const key of [
    "clayProblemSolved",
    "fittedScalingLaw",
    "globalRegularityEstablished",
    "navierStokesSimulation",
    "regularityCriterionImproved",
    "singularSolution",
  ]) {
    assert.equal(manifest.claimBoundary[key], false, key);
  }
});

test("the primary-source audit records the direct collisions and adaptation boundary", () => {
  const audit = read("research/r073t_primary_literature_audit.md");
  for (const token of [
    "10.1017/jfm.2020.1033",
    "Tran",
    "Yu",
    "Dritschel",
    "10.1090/tran/8708",
    "Li--Sire",
    "Theorem 4.2",
    "10.1090/proc/16615",
    "Ambrose",
  ]) {
    assert.ok(audit.includes(token), token);
  }
  assert.match(audit, /componentwise|逐分量/);
  assert.match(audit, /not.*novelty|不是.*新颖性/i);
});
