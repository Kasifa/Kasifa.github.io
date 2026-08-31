import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const bytes = (relative) => readFileSync(resolve(root, relative));
const json = (relative) => JSON.parse(read(relative));
const sha256 = (payload) => createHash("sha256").update(payload).digest("hex");
const compact = (value) => value.replace(/\s+/g, "");

const title =
  "R0.73U | Full tensors in the heat hierarchy: pressure is recoverable, " +
  "but the even quadratic state is not dynamically closed";
const publicTitle =
  "R0.73U｜完整张量进入热层级：压力可以恢复，但偶二次状态的动力学并不闭合";
const analyticCommit = "84e808dae473f6381cbf9df55a71f5fe81a1cfce";
const certificateSourceCommit = "6c79f23152116f5d420be6ff03653500ab02ef0e";
const certificatePackageCommit = "044bfb3f7e5af98e2615f60747c9e5109ef12d7c";
const figureId = "fig-r073u-tensor-heat-hierarchy";

const canonicalPaths = [
  "research/r073u_problem_freeze.md",
  "research/r073u_tensor_heat_hierarchy.md",
  "research/r073u_independent_analytic_audit.md",
  "research/r073u_primary_literature_audit.md",
  "research/r073u_claim_source_ledger.md",
  "research/r073u_evidence_gap_matrix.md",
  "research/r073u_report-source.md",
  "research/r073u_bilingual_dictionary.md",
  "research/r073u_finite_diagnostic_audit.md",
  "research/r073u_figure_source_audit.md",
  "research/r073u_figure_source_reaudit.md",
];
const corpus = canonicalPaths.map(read).join("\n");

test("R0.73U freezes the precise title and separates exact, classical, and open claims", () => {
  const report = read("research/r073u_report-source.md");
  const dictionary = read("research/r073u_bilingual_dictionary.md");
  assert.ok(report.startsWith(`# ${title}\n`));
  assert.ok(report.includes(`**Public title (zh):** ${publicTitle}`));
  assert.ok(dictionary.replace(/\s+/g, " ").includes(`**Release title:** ${title}`));
  assert.ok(dictionary.includes(`**Public title (zh):** ${publicTitle}`));
  for (const token of [
    "localProductTensorDistinctFromKHM=TRUE",
    "instantaneousPressureFromLocalProductTensor=VERIFIED_CLASSICAL",
    "heatCovariancePSD=INTERNAL_EXACT",
    "heatCovarianceScalePDE=INTERNAL_EXACT",
    "filteredEquation=VERIFIED_CLASSICAL_RECONSTRUCTION",
    "criticalTensorStressRow=INTERNAL_COROLLARY",
    "criticalTensorStressRowAssumesL4tL6x=TRUE",
    "energyOnlyFixedScaleStress=INTERNAL_COROLLARY",
    "energyOnlyUniformAsSToZero=FALSE",
    "centeredPressureVarianceDirectClassicalCollision=TRUE",
    "fourSiteParityWitness=INTERNAL_EXACT",
    "formalFiniteCertificateChecks=75",
    "formalFigureChecks=325",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN",
    "clayConclusion=OPEN",
    "NOT CLAY",
  ]) assert.ok(corpus.includes(token), token);
  for (const phrase of [
    "not a physical-time stress closure",
    "is circular for arbitrary-data global regularity",
    "is not uniform control at zero scale",
    "does not certify the continuum PDE proof",
    "non-detection is not proof of novelty, priority, non-existence, or first authorship",
    "Clay Millennium problem remain open",
  ]) assert.ok(corpus.replace(/\s+/g, " ").includes(phrase), phrase);
  assert.doesNotMatch(report, /我们|攻关|主攻|突破|首次证明|原创性定理/);
  const obsoleteFigure = ["fig-r073u", "dynamic", "autocorrelation"].join("-");
  assert.equal(corpus.toLowerCase().includes(obsoleteFigure), false);
});

test("the analytic source contains the heat covariance, pressure, stress, and no-go formulas", () => {
  const proof = compact(read("research/r073u_tensor_heat_hierarchy.md"));
  const report = compact(read("research/r073u_report-source.md"));
  for (const token of [
    "\\tau_s=\\Theta_s-v_s\\otimesv_s",
    "\\partial_s\\tau_s&=\\Delta\\Theta_s",
    "=\\Delta\\tau_s+2\\sum_\\ell",
    "\\tau_{s+r}(u)=P_r\\tau_s(u)+\\tau_r(P_su)",
    "p_s=R_iR_j\\Theta_{s,ij}",
    "\\partial_tv_s+\\mathbbP\\nabla\\!\\cdot(v_s\\otimesv_s+\\tau_s)=\\nu\\Deltav_s",
    "\\Pi_s=-\\tau_s:\\nablav_s",
    "Q'+4\\nuY+(2-\\vartheta)\\nuX^2",
    "\\mathcalP_*=\\intw(p-\\barp_w)^2d\\mu",
    "\\Theta_s(-u)=\\Theta_s(u)",
    "2e^{-5s}K",
    "2\\sqrt6\\,Le^{-5\\theta}=2\\sqrt{6\\theta}\\,e^{-5\\theta}s^{-1/2}",
  ]) assert.ok(proof.includes(compact(token)), token);
  for (const token of [
    "\\sup_{s\\ge0}\\|\\tau_s\\|_{L_t^2L_x^3}",
    "\\|\\tau_s\\|_{L_t^2(0,T;L_x^3)}",
    "K(h_*)=\\begin{pmatrix}-2&1&0\\\\1&0&0\\\\0&0&0\\end{pmatrix}",
    "t=0",
  ]) assert.ok(report.includes(compact(token)), token);
});

test("the sign-pair claim is explicitly initial-time and not a trajectory symmetry", () => {
  const dictionary = read("research/r073u_bilingual_dictionary.md");
  const ledger = read("research/r073u_claim_source_ledger.md");
  const finiteAudit = read("research/r073u_finite_diagnostic_audit.md");
  const exactSentence =
    "The comparison concerns Navier--Stokes tangents at the same initial time " +
    "for \\(u\\) and \\(-u\\); it is not a trajectory symmetry.";
  assert.ok(dictionary.includes(exactSentence));
  assert.ok(ledger.includes("At the initial time \\(t=0\\)"));
  assert.match(ledger, /initial-state separation, not a trajectory symmetry/);
  assert.ok(finiteAudit.includes(
    "same initial time \\(t=0\\), not between two symmetric"));
  assert.match(finiteAudit, /not a numerical PDE trajectory/);
});

test("the exact certificate closes 75 checks and binds both immutable source layers", () => {
  const base = "research/certificates/r073u";
  const manifest = json(`${base}/manifest.json`);
  const checklist = json(`${base}/audit-checklist.json`);
  const results = json(`${base}/results.json`);
  assert.equal(manifest.schemaVersion, "r073u-exact-tensor-heat-manifest-v1");
  assert.equal(manifest.release, "R0.73U");
  assert.equal(manifest.status, "sealed");
  assert.equal(manifest.finalSeal, true);
  assert.equal(manifest.allPrerequisiteChecksPass, true);
  assert.equal(manifest.sourceCommitAssigned, true);
  assert.equal(manifest.sourceCommit, analyticCommit);
  assert.equal(manifest.analyticSourceCommit, analyticCommit);
  assert.equal(manifest.certificateSourceCommitAssigned, true);
  assert.equal(manifest.certificateSourceCommit, certificateSourceCommit);
  assert.deepEqual(manifest.checkInventory, { exact: 75, required: 75 });
  assert.deepEqual(manifest.inventory, {
    analyticSourceFileCount: 4,
    boundFileCount: 7,
    generatedFileCount: 3,
    packageFileCount: 9,
    sha256SumsLineCount: 8,
    sourceFileCount: 6,
  });
  assert.equal(checklist.requiredChecks.length, 75);
  assert.equal(results.audit.required, 75);
  assert.equal(results.audit.passed, 75);
  assert.equal(results.audit.results.length, 75);
  assert.equal(results.audit.results.every(({ pass }) => pass === true), true);
  assert.deepEqual(results.witness.field.physical,
    ["2*sin(x+y)", "2*sin(x)-2*sin(x+y)", "0"]);
  assert.equal(results.witness.field.siteCount, 4);
  assert.deepEqual(results.witness.target.mode, [1, 2, 0]);
  assert.deepEqual(results.witness.target.K,
    [["-2", "1", "0"], ["1", "0", "0"], ["0", "0", "0"]]);
  assert.equal(results.witness.target.KSquaredFrobenius, "6");
  assert.deepEqual(results.witness.target.T,
    [["0", "0", "0"], ["0", "0", "0"], ["0", "0", "0"]]);
  assert.deepEqual(results.witness.target.V, results.witness.target.T);
  assert.equal(results.witness.parity.TEven, true);
  assert.equal(results.witness.parity.pressureEven, true);
  assert.equal(results.witness.parity.KOdd, true);
  assert.equal(results.witness.dilation.heatFilteredDifference,
    "2*L*exp(-5*s*L^2)*K");
  assert.equal(results.producer.standardLibraryOnly, true);
  assert.equal(results.producer.dgx, "not used");
  assert.equal(results.producer.gpu, "not used");
  assert.equal(results.producer.network, "not used");
  assert.equal(results.producer.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");
  assert.match(manifest.claimBoundary, /no generic PDE integration.*global regularity.*Clay/i);
  assert.ok(corpus.includes(`finitePackageCommit=${certificatePackageCommit}`));

  assert.equal(manifest.files.length, 7);
  for (const row of manifest.files) {
    const payload = bytes(`${base}/${row.path}`);
    assert.equal(payload.length, row.bytes, row.path);
    assert.equal(sha256(payload), row.sha256, row.path);
  }
});

test("the figure binds 138 rows and 325 checks without turning initial data into a trajectory claim", () => {
  const base = `research/figures/r073u/${figureId}`;
  const manifest = json(`${base}/manifest.json`);
  const contract = json(`${base}/contract.json`);
  const environment = json(`${base}/environment.json`);
  const results = json(`${base}/results.json`);
  const validation = json(`${base}/validation.json`);
  const caption = read(`${base}/caption.md`);
  const rows = read(`${base}/source-data.csv`).trimEnd().split("\n");
  assert.equal(manifest.schemaVersion, "r073u-tensor-heat-hierarchy-manifest-v1");
  assert.equal(manifest.figureId, figureId);
  assert.equal(manifest.finalSeal, true);
  assert.equal(manifest.sourceCommitAssigned, true);
  assert.equal(manifest.sourceCommit, analyticCommit);
  assert.deepEqual(manifest.validation,
    { checksPassed: 325, checksRequired: 325, status: "PASS" });
  assert.equal(manifest.files.length, 23);
  assert.equal(validation.schemaVersion, "r073u-tensor-heat-hierarchy-validation-v1");
  assert.equal(validation.status, "PASS");
  assert.equal(validation.checksPassed, 325);
  assert.equal(validation.checksRequired, 325);
  assert.equal(validation.checks.length, 325);
  assert.equal(validation.checks.every(({ pass }) => pass === true), true);
  assert.equal(validation.visualQaConfirmed, true);
  assert.equal(results.rowCount, 138);
  assert.equal(rows.length - 1, 138);
  assert.deepEqual(results.series, {
    analyticCurveSamples: 111,
    analyticSchematic: 4,
    exactFiniteDiagnostic: 22,
    exactPeak: 1,
  });
  assert.deepEqual(results.exactConstants.totalMatrix, [[-2, 1], [1, 0]]);
  assert.equal(results.exactConstants.totalMatrixFrobeniusSquared, 6);
  assert.equal(contract.compute.dgxUsed, false);
  assert.equal(contract.compute.gpu, "not used");
  assert.equal(contract.compute.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(environment.execution.network, "not used");
  assert.equal(environment.execution.dgxUsed, false);
  assert.equal(environment.execution.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");
  for (const key of [
    "fittedScalingLaw", "navierStokesSimulation", "singularSolution",
    "regularityCriterionImproved", "globalRegularityEstablished", "clayProblemSolved",
  ]) assert.equal(contract.claimBoundary[key], false, key);
  assert.equal(contract.claimBoundary.exactFormulaAndFiniteDiagnosticOnly, true);
  assert.equal(contract.normalization.evaluationTime, "initial time t=0");
  assert.equal(contract.claimBoundary.initialTimeTangentOnly, true);
  assert.equal(contract.claimBoundary.trajectorySymmetryClaim, false);
  assert.deepEqual(manifest.claimBoundary, contract.claimBoundary);
  assert.deepEqual(results.claimBoundary, contract.claimBoundary);

  const initialTime = /(?:initial[- ](?:time|state)|t\s*=\s*0)/i;
  assert.match(caption, initialTime);
  assert.match(caption, /not a trajectory symmetry/i);
  assert.doesNotMatch(caption, /trajectory symmetry\s*[.;]?\s*$/i);

  for (const row of manifest.files) {
    const payload = bytes(`${base}/${row.path}`);
    assert.equal(payload.length, row.bytes, row.path);
    assert.equal(sha256(payload), row.sha256, row.path);
  }
});

test("the literature ledger cites primary collisions without promoting the bounded search", () => {
  const audit = read("research/r073u_primary_literature_audit.md");
  for (const token of [
    "10.1098/rspa.1938.0013",
    "10.1017/S0022112001003949",
    "10.1017/S0022112092001733",
    "chao-dyn/9602018",
    "10.1007/BF02099744",
    "10.1088/0951-7715/13/1/312",
    "10.1017/jfm.2026.11485",
    "Zambrano--Duraisamy",
  ]) assert.ok(audit.includes(token), token);
  const pressureCollision = read("research/r073u_bilingual_dictionary.md");
  assert.ok(pressureCollision.includes("10.1017/jfm.2020.1033"));
  assert.ok(pressureCollision.includes("Tran--Yu--Dritschel"));
  assert.match(audit, /not.*novelty|does not establish novelty|不是.*新颖性/i);
});
