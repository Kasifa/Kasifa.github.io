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
const git = (...args) => execFileSync("git", args, {
  cwd: root, encoding: "utf8", maxBuffer: 32 * 1024 * 1024,
}).trim();
const gitBytes = (commit, relative) => execFileSync(
  "git", ["show", `${commit}:${relative}`],
  { cwd: root, maxBuffer: 32 * 1024 * 1024 },
);

const title =
  "R0.73W | Signed subfilter production: heat-plane characteristics, " +
  "the energy-class boundary, and exact counterexamples";
const publicTitle =
  "R0.73W｜带符号亚滤波 production：heat-plane 特征线、能量类边界与精确反例";
const certificateSourceCommit = "b9f3b3943df1e2abf6abc2f51c1fb25d1f1e8440";
const certificatePackageCommit = "68893eccd7f5b6047bf2b00c5262913e23fadbc3";
const contentCommit = "855e341e371302f315c5535006193f8ce0703740";
const figureSourceCommit = "ac6293ac4d0c46c696d2ec8e29d3fb1350e341f1";
const figurePackageCommit = "60b0e869bbaa3a0ace185bf450e067d79fcd79b3";
const figureId = "fig-r073w-signed-production";

const canonicalPaths = [
  "research/r073w_problem_freeze.md",
  "research/r073w_signed_production_heat_characteristic.md",
  "research/r073w_independent_analytic_audit.md",
  "research/r073w_primary_literature_audit.md",
  "research/r073w_claim_source_ledger.md",
  "research/r073w_evidence_gap_matrix.md",
  "research/r073w_finite_diagnostic_audit.md",
  "research/r073w_report-source.md",
  "research/r073w_bilingual_dictionary.md",
];
const corpus = canonicalPaths.map(read).join("\n");
const conflictCopy = (name) => / [234](?=\.[^.]+$|$)/.test(name);

function assertCommitTree(commit, relativeRoot, expectedPaths) {
  assert.equal(git("cat-file", "-t", commit), "commit");
  const committed = git("ls-tree", "-r", "--name-only", commit, relativeRoot)
    .split("\n").filter(Boolean).sort();
  assert.deepEqual(committed, [...expectedPaths].sort());
  for (const relative of expectedPaths) {
    assert.deepEqual(gitBytes(commit, relative), bytes(relative), relative);
  }
}

test("R0.73W freezes the exact reader title and a SEALED_COMMIT_BOUND figure boundary", () => {
  const report = read("research/r073w_report-source.md");
  const dictionary = read("research/r073w_bilingual_dictionary.md");
  assert.ok(report.startsWith(`# ${title}\n`));
  assert.ok(report.includes(`**Public title (zh):** ${publicTitle}`));
  const compactDictionary = dictionary.replace(/\s+/g, " ");
  assert.ok(compactDictionary.includes(`**Release title:** ${title}`));
  assert.ok(compactDictionary.includes(`**Public title (zh):** ${publicTitle}`));

  for (const token of [
    "gaussianStressDuhamel=VERIFIED_CLASSICAL_REDERIVED",
    "heatPlaneCharacteristicIdentity=INTERNAL_EXACT_AUDITED",
    "energyClassFixedScaleEstimate=INTERNAL_UNCONDITIONAL_AUDITED",
    "centeredIncrementSplit=INTERNAL_EXACT_AUDITED",
    "gradientCovarianceCarreDuChamp=INTERNAL_EXACT_AUDITED",
    "criticalHalfScaleAverage=INTERNAL_CRITICAL_AUDITED",
    "universalProductionSign=FALSE",
    "amplitudeIndependentQuadraticAbsorption=FALSE",
    "formalFiniteCertificate=SEALED_COMMIT_BOUND",
    "formalFigurePackage=SEALED_COMMIT_BOUND",
    "formalFigureChecks=49",
    "formalFigureRows=1416",
    `figureSourceCommit=${figureSourceCommit}`,
    `figurePackageCommit=${figurePackageCommit}`,
    "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
    "dgxUsed=false",
    "localizedScaleCriticalControl=OPEN",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN",
    "clayConclusion=OPEN",
    "NOT CLAY",
  ]) assert.ok(corpus.includes(token), token);

  assert.ok(report.includes("## 10. 下一步：R0.73X"));
  assert.equal(corpus.includes("formalFigurePackage=PENDING"), false);
  assert.equal(corpus.includes("formalFigurePackage=PASS"), false);
  for (const forbidden of [
    "universalProductionSign=TRUE",
    "amplitudeIndependentQuadraticAbsorption=TRUE",
    "localizedScaleCriticalControl=CLOSED",
    "clayConclusion=SOLVED",
  ]) assert.equal(corpus.includes(forbidden), false, forbidden);
});

test("the commit-bound certificate has 13 files, 9 sources, and two independent 56/56 paths", () => {
  const base = "research/certificates/r073w";
  const manifest = json(`${base}/manifest.json`);
  const checklist = json(`${base}/audit-checklist.json`);
  const primary = json(`${base}/results.json`);
  const independent = json(`${base}/independent-results.json`);
  const names = readdirSync(resolve(root, base)).sort();

  assert.equal(manifest.schemaVersion, "r073w-signed-production-exact-manifest-v1");
  assert.equal(manifest.release, "R0.73W");
  assert.equal(manifest.status, "SEALED_COMMIT_BOUND");
  assert.equal(manifest.finalSeal, true);
  assert.equal(manifest.sourceCommitAssigned, true);
  assert.equal(manifest.sourceCommit, certificateSourceCommit);
  assert.deepEqual(manifest.checkInventory,
    { exactPerPath: 56, requiredPerPath: 56, twoPathComparisons: 2 });
  assert.deepEqual(manifest.inventory, {
    boundFileCount: 11,
    generatedFileCount: 4,
    packageFileCount: 13,
    sha256SumsLineCount: 12,
    sourceFileCount: 9,
  });
  assert.equal(names.length, 13);
  assert.equal(names.some(conflictCopy), false);
  assert.equal(manifest.files.length, 11);
  assert.equal(manifest.sourceBindings.length, 9);
  assert.equal(manifest.sourceCommitBindings.length, 9);
  assert.equal(checklist.requiredChecks.length, 56);

  for (const result of [primary, independent]) {
    assert.equal(result.audit.required, 56);
    assert.equal(result.audit.passed, 56);
    assert.equal(result.audit.rows.length, 56);
    assert.ok(result.audit.rows.every(({ pass }) => pass === true));
  }
  assert.deepEqual(primary.commonCore, independent.commonCore);
  assert.equal(manifest.comparison.commonCoreByteIdentical, true);
  assert.equal(manifest.comparison.commonCoreSha256,
    "4c72251bde4bf12bb5cfe8c3c6b15c0e049dc440a2c41daa751eb0a5da9460f2");

  for (const row of manifest.files) {
    const payload = bytes(`${base}/${row.path}`);
    assert.equal(payload.length, row.bytes, row.path);
    assert.equal(sha256(payload), row.sha256, row.path);
  }
  for (const row of manifest.sourceCommitBindings) {
    assert.deepEqual(gitBytes(certificateSourceCommit, row.path), bytes(row.path), row.path);
    assert.equal(git("rev-parse", `${certificateSourceCommit}:${row.path}`), row.gitBlobObjectId);
  }
  assert.equal(read(`${base}/SHA256SUMS`).trimEnd().split("\n").length, 12);
  const expected = names.map((name) => `${base}/${name}`);
  assertCommitTree(certificatePackageCommit, base, expected);
  assert.equal(git("merge-base", "--is-ancestor",
    certificateSourceCommit, certificatePackageCommit), "");
});

test("the formal figure is source-bound at 49/49 and package-bound at 25 files", () => {
  const base = `figures/r073w/${figureId}`;
  const manifest = json(`${base}/manifest.json`);
  const validation = json(`${base}/validation.json`);
  const results = json(`${base}/results.json`);
  const contract = json(`${base}/contract.json`);
  const names = readdirSync(resolve(root, base)).sort();

  assert.equal(manifest.schemaVersion, "research-figure-manifest-v1");
  assert.equal(manifest.figureSchemaVersion, "r073w-signed-production-manifest-v1");
  assert.equal(manifest.figureId, figureId);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.publicationStatus, "staged");
  assert.equal(manifest.seal.state, "formal-figure-source-seal");
  assert.equal(manifest.seal.figureSourceCommitAssigned, true);
  assert.equal(manifest.seal.figureSourceCommit, figureSourceCommit);
  assert.equal(manifest.seal.requiresParentFigureSourceCommitFinalReseal, false);
  assert.equal(manifest.seal.certificateSourceCommit, certificateSourceCommit);
  assert.equal(manifest.seal.certificatePackageCommit, certificatePackageCommit);
  assert.equal(manifest.seal.figureSourceBindings.length, 21);
  assert.equal(manifest.git.figureSourceCommit, figureSourceCommit);
  assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.validationChecks, 49);

  assert.equal(validation.schemaVersion, "r073w-signed-production-validation-v1");
  assert.equal(validation.status, "PASS");
  assert.equal(validation.passed, 49);
  assert.equal(validation.required, 49);
  assert.equal(validation.checksPassed, 49);
  assert.equal(validation.checksRequired, 49);
  assert.equal(validation.checks.length, 49);
  assert.ok(validation.checks.every(({ pass }) => pass === true));
  for (const id of [
    "figure-source-commit-bound",
    "figure-source-blob-byte-identity",
    "figure-source-bound-scope-clean",
  ]) assert.ok(validation.checks.some((row) => row.id === id && row.pass === true), id);

  assert.equal(names.length, 25);
  assert.equal(names.some(conflictCopy), false);
  assert.equal(read(`${base}/SHA256SUMS`).trimEnd().split("\n").length, 24);
  assert.equal(read(`${base}/source-data.csv`).trimEnd().split("\n").length - 1, 1416);
  assert.equal(results.sourceDataRows, 1416);
  assert.deepEqual(results.panelRowCounts, { A: 327, B: 362, C: 484, D: 243 });
  assert.equal(results.certificate.rankThreeFrequencySupport, 3);
  assert.equal(results.exactConstants.productionPeakMagnitude, "1/16");
  assert.equal(results.exactConstants.productionPeakScale, "log(2)/2");
  assert.equal(results.exactConstants.absorptionZeroScaleLimit, "1/78");
  assert.equal(contract.compute.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(contract.compute.dgxUsed, false);
  assert.equal(results.scope.navierStokesSimulation, false);
  assert.equal(results.scope.fittedScalingLaw, false);
  assert.equal(results.scope.notClay, true);
  assert.deepEqual(contract.claimBoundary, manifest.claimBoundary);
  for (const key of [
    "navierStokesSimulation",
    "fittedScalingLaw",
    "genericTurbulenceClaim",
    "singularSolution",
    "regularityCriterionImproved",
    "globalRegularityEstablished",
    "clayProblemSolved",
  ]) assert.equal(contract.claimBoundary[key], false, key);

  for (const row of manifest.seal.figureSourceBindings) {
    assert.deepEqual(gitBytes(figureSourceCommit, row.path), bytes(row.path), row.path);
    assert.equal(git("rev-parse", `${figureSourceCommit}:${row.path}`), row.gitBlobObjectId);
  }
  for (const row of read(`${base}/SHA256SUMS`).trimEnd().split("\n")) {
    const match = row.match(/^([0-9a-f]{64})  ([^/]+)$/);
    assert.ok(match, row);
    assert.equal(sha256(bytes(`${base}/${match[2]}`)), match[1], match[2]);
  }
  const expected = names.map((name) => `${base}/${name}`);
  assertCommitTree(figurePackageCommit, base, expected);
  assert.equal(git("merge-base", "--is-ancestor", figureSourceCommit, figurePackageCommit), "");
});

test("immutable analytic and figure pins exist in ancestry order", () => {
  for (const commit of [
    certificateSourceCommit, certificatePackageCommit, contentCommit,
    figureSourceCommit, figurePackageCommit,
  ]) assert.equal(git("rev-parse", commit), commit);
  assert.equal(git("merge-base", "--is-ancestor", figurePackageCommit, contentCommit), "");
});

test("R0.73W source scopes contain no OneDrive conflict-copy names", () => {
  for (const relative of canonicalPaths) assert.equal(conflictCopy(relative), false);
  for (const directory of [
    "research/certificates/r073w",
    `figures/r073w/${figureId}`,
  ]) {
    assert.equal(readdirSync(resolve(root, directory)).some(conflictCopy), false, directory);
  }
  for (const directory of ["scripts", "tests", "research"]) {
    const bad = readdirSync(resolve(root, directory))
      .filter((name) => /r073w/i.test(name) && conflictCopy(name));
    assert.deepEqual(bad, [], directory);
  }
});
