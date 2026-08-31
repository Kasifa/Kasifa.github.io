import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { readFileSync, readdirSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const bytes = (relative) => readFileSync(resolve(root, relative));
const json = (relative) => JSON.parse(read(relative));
const sha256 = (payload) => createHash("sha256").update(payload).digest("hex");
const compact = (value) => value.replace(/\s+/g, "");
const git = (...args) => execFileSync("git", args, { cwd: root, encoding: "utf8" }).trim();

const title =
  "R0.73V | A pressure-aware signed third-order heat lift: exact scale " +
  "generation and the 3→4 physical-time boundary";
const publicTitle =
  "R0.73V｜压力感知的有符号三阶热提升：精确尺度生成律与 3→4 物理时间边界";
const analyticCommit = "25636c886f1ee2449418b5548b42f9f0fa269b47";
const certificateSourceCommit = "7c445c522a241bdc8b867b6fce0f0fed9b82e97d";
const certificatePackageCommit = "b34d91ea96c257b943f11d134e8024138e5f3cb0";
const figureSourceCommit = "f94915332ff405ae723711e8041acc2af07e896b";
const figurePackageCommit = "ae679d5afa5f3cfacfe79c4d7b8a462baca2c195";
const finalContentCommit = "482905ed7a9dcc3cc337d5ba17f73af5ac61c60f";
const figureId = "fig-r073v-signed-third-order-interface";

const canonicalPaths = [
  "research/r073v_problem_freeze.md",
  "research/r073v_signed_third_order_heat_lift.md",
  "research/r073v_independent_analytic_audit.md",
  "research/r073v_primary_literature_audit.md",
  "research/r073v_claim_source_ledger.md",
  "research/r073v_evidence_gap_matrix.md",
  "research/r073v_finite_diagnostic_audit.md",
  "research/r073v_report-source.md",
  "research/r073v_bilingual_dictionary.md",
];
const corpus = canonicalPaths.map(read).join("\n");

test("R0.73V freezes the exact title and the narrow claim boundary", () => {
  const report = read("research/r073v_report-source.md");
  const dictionary = read("research/r073v_bilingual_dictionary.md");
  assert.ok(report.startsWith(`# ${title}\n`));
  assert.ok(report.includes(`**Public title (zh):** ${publicTitle}`));
  assert.ok(dictionary.replace(/\s+/g, " ").includes(`**Release title:** ${title}`));
  assert.ok(dictionary.includes(`**Public title (zh):** ${publicTitle}`));

  for (const token of [
    "pressureAwareSignedHeatLift=INTERNAL_EXACT_AUDITED",
    "signedCrossCovarianceScalePDE=INTERNAL_EXACT_AUDITED",
    "germanoStressEquation=VERIFIED_CLASSICAL_INDEX_AUDITED",
    "conditionalKappaCriticalRow=INTERNAL_CONDITIONAL_AUDITED",
    "conditionalPressureVelocityCriticalRow=INTERNAL_CONDITIONAL_AUDITED",
    "pressureStrainCriticalRow=OPEN",
    "rawAndCompressedThreeToFour=INTERNAL_EXACT_AUDITED",
    "fourSiteCoefficientOrderSeparation=INTERNAL_EXACT_FINITE_SEALED",
    "sixSiteSameOutputPressureWitness=INTERNAL_EXACT_FINITE_SEALED",
    "selectedQuarticNextLevelRemainder=INTERNAL_EXACT_FINITE_SEALED",
    "formalFiniteCertificateChecks=66",
    "formalFigureChecks=147",
    "formalFigureRows=158",
    "signedLiftInformationTheoreticMinimality=NOT_ESTABLISHED",
    "signedLiftComponentwiseMinimality=NOT_ESTABLISHED",
    "signedLiftUniqueness=NOT_ESTABLISHED",
    "fullThirdCumulantStateNonAutonomy=NOT_ESTABLISHED",
    "wholeFieldKappaCollision=NOT_ESTABLISHED",
    "fourthOrderNonClosure=NOT_ESTABLISHED",
    "finiteMomentHierarchyNoGo=NOT_ESTABLISHED",
    "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
    "dgxUsed=FALSE",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN",
    "clayConclusion=OPEN",
    "NOT CLAY",
  ]) assert.ok(corpus.includes(token), token);

  for (const forbidden of [
    "signedLiftInformationTheoreticMinimality=TRUE",
    "signedLiftInformationTheoreticMinimality=ESTABLISHED",
    "wholeFieldKappaCollision=CLOSED_EXACT",
    "fourthOrderNonClosure=CLOSED_EXACT",
    "finiteMomentHierarchyNoGo=CLOSED_EXACT",
    "clayConclusion=SOLVED",
  ]) assert.equal(corpus.includes(forbidden), false, forbidden);
  assert.doesNotMatch(report, /我们|攻关|主攻|突破|首次证明|原创性定理/);
});

test("the analytic source contains the compressed and transparent exact interfaces", () => {
  const proof = compact(read("research/r073v_signed_third_order_heat_lift.md"));
  for (const token of [
    "\\mathcalC_s=P_s(u\\odotN)",
    "\\chi_s=\\mathcalC_s-v_s\\odotN_s",
    "(\\partial_s-\\Delta)\\chi_s",
    "(\\partial_t-\\nu\\partial_s)\\Theta_s",
    "L_s\\kappa_{ijk,s}=2\\sum_\\ell",
    "Q_{i,s}=\\tau_s(p,u_i)",
    "R_{ij,s}=\\tau_s(p,S_{ij})",
    "J_{k,s}={1\\over2}\\kappa_{iik,s}+Q_{k,s}",
    "(\\partial_t-\\nu\\partial_s)M_{ijk,s}",
    "(\\partial_t-\\nu\\partial_s)\\chi_s",
    "\\kappa_{ijk,s}=2s^2",
    "\\chi_s=2s\\sum_\\ell",
  ]) assert.ok(proof.includes(compact(token)), token);
  assert.match(corpus, /does not prove fourth-order non-closure/i);
  assert.match(corpus, /does not prove[^]*finite[^]*hierarchy/i);
});

test("the sealed two-path exact certificate closes 66 checks and only coefficientwise claims", () => {
  const base = "research/certificates/r073v";
  const manifest = json(`${base}/manifest.json`);
  const checklist = json(`${base}/audit-checklist.json`);
  const results = json(`${base}/results.json`);
  const independent = json(`${base}/independent-results.json`);

  assert.equal(manifest.schemaVersion, "r073v-signed-third-order-exact-manifest-v1");
  assert.equal(manifest.release, "R0.73V");
  assert.equal(manifest.status, "sealed");
  assert.equal(manifest.finalSeal, true);
  assert.equal(manifest.sourceCommitAssigned, true);
  assert.equal(manifest.sourceCommit, certificateSourceCommit);
  assert.deepEqual(manifest.checkInventory,
    { exact: 66, required: 66, twoPathComparisons: 2 });
  assert.deepEqual(manifest.inventory, {
    boundFileCount: 10,
    generatedFileCount: 4,
    packageFileCount: 12,
    sha256SumsLineCount: 11,
    sourceFileCount: 8,
  });
  assert.equal(manifest.scopeFlags.coefficientwiseNonRecoveryOnly, true);
  assert.equal(manifest.scopeFlags.cAloneInformationTheoreticallyInsufficient, "OPEN");
  assert.equal(manifest.scopeFlags.clayConclusion, "OPEN");
  assert.equal(manifest.scopeFlags.notClay, true);
  assert.equal(checklist.requiredChecks.length, 66);
  assert.equal(results.audit.required, 66);
  assert.equal(results.audit.passed, 66);
  assert.equal(results.audit.results.length, 66);
  assert.ok(results.audit.results.every(({ pass }) => pass === true));
  assert.deepEqual(results.commonCore, independent.commonCore);
  assert.equal(results.commonCore.tableDigest,
    "a7494d44f45b1249a513ac4d44476b7ce5af622b0d59928f4e4631d9715c22f7");

  assert.equal(results.fourSite.target.localKappaFlux[0][0].smallS.order, 2);
  assert.equal(results.fourSite.target.pressureDiffusion[0][0].smallS.order, 1);
  assert.deepEqual(results.fourSite.target.pressureStrainXi[0][0].coefficients,
    { 3: "-4", 5: "4" });
  assert.deepEqual(results.sixSite.zeroMode.contractedKappaFlux[0][0].coefficients, {});
  assert.deepEqual(results.sixSite.zeroMode.pressureStrainXi[0][0].coefficients,
    { 0: "-48", 4: "48" });
  assert.deepEqual(results.quartic.coefficient.coefficients,
    { 2: "2*i", 4: "-4*i", 6: "2*i" });
  assert.equal(results.quartic.finiteEpsilonAtQHalf.extractedLinearCoefficient, "9/32*i");
  assert.equal(results.compressedLift.dilationAtSThetaOverLSquaredFrobeniusSignDifference,
    "2*sqrt(6)*L*(exp(-3*theta)-exp(-5*theta))");
  assert.equal(results.producer.standardLibraryOnly, true);
  assert.equal(results.producer.dgx, "not used");
  assert.equal(results.scope.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");

  assert.equal(manifest.files.length, 10);
  for (const row of manifest.files) {
    const payload = bytes(`${base}/${row.path}`);
    assert.equal(payload.length, row.bytes, row.path);
    assert.equal(sha256(payload), row.sha256, row.path);
  }
  const sums = read(`${base}/SHA256SUMS`).trimEnd().split("\n");
  assert.equal(sums.length, 11);
});

test("the source-bound formal figure has 158 rows, 147 checks, and all no-go flags false", () => {
  const base = `figures/r073v/${figureId}`;
  const manifest = json(`${base}/manifest.json`);
  const contract = json(`${base}/contract.json`);
  const results = json(`${base}/results.json`);
  const validation = json(`${base}/validation.json`);
  const rows = read(`${base}/source-data.csv`).trimEnd().split("\n");
  const files = readdirSync(resolve(root, base)).sort();

  assert.equal(manifest.schemaVersion, "research-figure-manifest-v1");
  assert.equal(manifest.figureSchemaVersion,
    "r073v-signed-third-order-interface-manifest-v1");
  assert.equal(manifest.figureId, figureId);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.publicationStatus, "staged");
  assert.equal(manifest.seal.figureSourceCommitAssigned, true);
  assert.equal(manifest.seal.figureSourceCommit, figureSourceCommit);
  assert.equal(manifest.seal.requiresParentFigureSourceCommitFinalReseal, false);
  assert.equal(manifest.seal.state, "formal-figure-source-seal");
  assert.equal(manifest.git.certificateSourceCommit, certificateSourceCommit);
  assert.equal(manifest.git.certificateCommit, certificatePackageCommit);
  assert.equal(manifest.git.figureSourceCommit, figureSourceCommit);
  assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  assert.equal(manifest.qa.validationChecks, 147);
  assert.equal(manifest.qa.status, "passed");

  assert.equal(validation.schemaVersion,
    "r073v-signed-third-order-interface-validation-v1");
  assert.equal(validation.status, "PASS");
  assert.equal(validation.passed, 147);
  assert.equal(validation.required, 147);
  assert.equal(validation.checks.length, 147);
  assert.ok(validation.checks.every(({ pass }) => pass === true));
  assert.deepEqual(
    validation.checks.find(({ id }) => id === "csv-evidence-aware-reconstruction"),
    {
      exactRows: 57,
      id: "csv-evidence-aware-reconstruction",
      pass: true,
      rendererRows: 101,
      rendererYAbsoluteTolerance: "2e-16",
      rendererYMaximumUlpDistance: 256,
    },
  );
  assert.equal(
    validation.checks.some(({ id }) => id === "csv-exact-reconstruction"),
    false,
  );
  assert.equal(validation.visualQaConfirmed, true);
  assert.equal(results.schemaVersion,
    "r073v-signed-third-order-interface-figure-results-v1");
  assert.equal(results.rowCount, 158);
  assert.equal(results.series.total, 158);
  assert.equal(rows.length - 1, 158);
  assert.equal(files.length, 25);
  assert.equal(read(`${base}/SHA256SUMS`).trimEnd().split("\n").length, 24);
  assert.equal(contract.compute.dgxUsed, false);
  assert.equal(contract.compute.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");

  for (const key of [
    "informationTheoreticMinimalityEstablished",
    "wholeFieldNonRecoveryEstablished",
    "fourthOrderNonClosureEstablished",
    "finiteHierarchyNoGoEstablished",
    "pdeClosureEstablished",
    "globalRegularityEstablished",
    "clayProblemSolved",
  ]) assert.equal(contract.claimBoundary[key], false, key);
  assert.deepEqual(results.claimBoundary, contract.claimBoundary);
  assert.deepEqual(manifest.claimBoundary, contract.claimBoundary);

  const sumRows = read(`${base}/SHA256SUMS`).trimEnd().split("\n");
  for (const row of sumRows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/]+)$/);
    assert.ok(match, row);
    assert.equal(sha256(bytes(`${base}/${match[2]}`)), match[1], match[2]);
  }
});

test("immutable commit pins exist and bind the current analytic, certificate, and figure trees", () => {
  for (const commit of [
    analyticCommit, certificateSourceCommit, certificatePackageCommit,
    figureSourceCommit, figurePackageCommit, finalContentCommit,
  ]) assert.equal(git("rev-parse", commit), commit);
  assert.equal(git("merge-base", "--is-ancestor", analyticCommit, figureSourceCommit), "");
  assert.equal(git("merge-base", "--is-ancestor", figureSourceCommit, figurePackageCommit), "");
  for (const path of [
    "research/r073v_independent_analytic_audit.md",
    "research/r073v_primary_literature_audit.md",
  ]) assert.equal(git("show", `${analyticCommit}:${path}`), read(path).trimEnd());
  assert.equal(
    git("show", `${finalContentCommit}:research/r073v_signed_third_order_heat_lift.md`),
    read("research/r073v_signed_third_order_heat_lift.md").trimEnd(),
  );
});

test("release tooling binds the exact paths and forbids DGX translation", () => {
  const content = read("scripts/r073v_release_content.py");
  const generator = read("scripts/generate_r073v_release.py");
  const translation = read("scripts/add-r073v-translations.mjs");
  const binder = read("scripts/bind-r073v-pdfs.mjs");
  const tooling = [content, generator, translation, binder].join("\n");

  for (const token of [
    title, publicTitle, figureId,
    "research/r073v_signed_third_order_heat_lift.md",
    analyticCommit, certificateSourceCommit, certificatePackageCommit,
    figureSourceCommit, figurePackageCommit, finalContentCommit,
    "LOCAL_DIRECT_NO_DGX",
  ]) assert.ok(tooling.includes(token), token);
  assert.ok(generator.includes("R073U_BASELINE"));
  assert.equal(generator.includes("R073T_BASELINE"), false);
  assert.ok(generator.includes(
    "tests/r073v-signed-third-order-interface-gate.test.mjs"));
  assert.equal(tooling.includes("fig-r073v-tensor-heat-hierarchy"), false);
  assert.equal(tooling.includes("research/r073v_tensor_heat_hierarchy.md"), false);
  assert.equal(translation.includes("node:child_process"), false);
  assert.doesNotMatch(translation, /\bfetch\s*\(|https?\.request|\bspawn\s*\(|\bexec\s*\(/);
  assert.ok(translation.includes("dgxUsed: false"));
  assert.ok(binder.includes("dgxUsed: false"));
});
