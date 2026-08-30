import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile, readdir, stat } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFile(resolve(root, relative));
const text = async (relative) => (await read(relative)).toString("utf8");
const json = async (relative) => JSON.parse(await text(relative));
const sha256 = async (relative) => createHash("sha256").update(await read(relative)).digest("hex");

const frozen = {
  analytic: ["research/r073j_analytic_proof.md", "81061d6f77e97fca33dafa0643820ab3860ae02b4042fe742eac1d91f1f108f0"],
  analyticAudit: ["research/r073j_analytic_audit.md", "f134d4a828ed0f91c62899a41e9640b8e5ed211f375a4a92913e76a1f537de5e"],
  overlapAnalytic: ["research/r073j_overlap_analytic_proof.md", "89c94e9d3ab9cd892f4f20ff8d2a3932b3f5fef6e82135ea2e64f39148c42f02"],
  contour: ["experiments/r073j/contour_certificate.json", "60c770beaf0dc9a3da99ba6ab7bff234b506aa7d8bc72a0aad7b55471b571a38"],
  overlap: ["experiments/r073j/overlap_certificate.json", "12e1505cacb807d83a611b96d5b928bd4302c9faef16030566d3e178234180ab"],
  contourAudit: ["experiments/r073j/independent_validation.json", "203b7af48933cdb49c0a0b59751c0b0435cf26ae48ea01e08f203900ad554d57"],
  naturalInitial: ["experiments/r073j/natural_box_validation.json", "2d92b6055ba847ffeda2a36a11d7c294df6d65925fd5e7dd00ec0cf6f7645c9a"],
  naturalDeep: ["experiments/r073j/natural_box_refinement_deep.json", "269d0b3860d7961c73f262d91ee48d4ef24219f0e34f0f775b21c437f609782f"],
};

test("R0.73J frozen analytic and interval inputs retain exact bytes", async () => {
  for (const [label, [relative, expected]] of Object.entries(frozen)) {
    assert.equal(await sha256(relative), expected, label);
  }
});

test("R0.73J contour count, local root, overlap and anchor decisions pass", async () => {
  const [contour, overlap, independent, independentOverlap] = await Promise.all([
    json("experiments/r073j/contour_certificate.json"),
    json("experiments/r073j/overlap_certificate.json"),
    json("experiments/r073j/independent_validation.json"),
    json("experiments/r073j/independent_overlap_validation.json"),
  ]);
  assert.equal(contour.status, "passed");
  assert.equal(contour.arithmetic.odePointCount, 21632);
  assert.equal(contour.decisions.globalBoundaryNonzeroForAllD, true);
  assert.equal(contour.decisions.localBoundaryNonzeroForAllD, true);
  assert.equal(contour.decisions.globalBasePositiveOrientationWinding, 1);
  assert.equal(contour.decisions.localBasePositiveOrientationWinding, 1);
  assert.match(contour.decisions.globalMinimumAbsoluteLower, /^\[5\.499484/);
  assert.match(contour.decisions.localMinimumAbsoluteLower, /^\[0\.164355/);

  assert.equal(overlap.status, "passed");
  assert.equal(overlap.arithmetic.pointCount, 841);
  assert.equal(overlap.decisions.auxiliaryRectangleKineticQuotientAtLeastOneHalf, true);
  assert.equal(overlap.decisions.auxiliaryRectanglePhaseAnchorNonzero, true);
  assert.match(overlap.decisions.minimumKineticOverlapLower, /^\[0\.585343/);
  assert.match(overlap.decisions.minimumAnchorAbsoluteLower, /^\[1\.841548/);

  assert.equal(independent.status, "passed");
  assert.equal(independent.classification, "independent-postprocessing-from-shared-raw-grid");
  assert.equal(independent.independentDecisions.globalBasePositiveOrientationWinding, 1);
  assert.equal(independent.independentDecisions.localBasePositiveOrientationWinding, 1);
  assert.match(independent.limitations.consequence, /shared raw values/);

  assert.equal(independentOverlap.status, "passed");
  assert.equal(
    independentOverlap.independenceBoundary.classification,
    "independent-post-processing-from-shared-raw-grid",
  );
  assert.match(independentOverlap.decisions.minimumKineticOverlapLower, /^\[0\.585009/);
  assert.match(independentOverlap.decisions.minimumStrictMarginAboveOneHalf, /^\[0\.085009/);
  assert.match(independentOverlap.independenceBoundary.limitation, /shared raw ODE grid/);
});

test("R0.73J natural-box history remains fail-closed and final selected-box audit passes", async () => {
  const [initial, shallow, deep] = await Promise.all([
    json("experiments/r073j/natural_box_validation.json"),
    json("experiments/r073j/natural_box_refinement.json"),
    json("experiments/r073j/natural_box_refinement_deep.json"),
  ]);
  assert.equal(initial.status, "failed");
  assert.equal(initial.decisions.passedBoxCount, 76);
  assert.equal(initial.decisions.failedBoxCount, 7);
  assert.match(initial.interpretation.failurePolicy, /recorded as failed/);

  assert.equal(shallow.status, "inconclusive");
  assert.equal(shallow.decisions.originalFailedParentCount, 7);
  assert.equal(shallow.decisions.secondLevelBoxCount, 112);
  assert.equal(shallow.decisions.secondLevelPassedBoxCount, 16);
  assert.equal(shallow.decisions.secondLevelFailedBoxCount, 96);

  assert.equal(deep.status, "passed");
  assert.equal(deep.decisions.allOriginal83NaturalBoxesCoveredDirectlyOrByPassingRefinedLeaves, true);
  assert.equal(deep.decisions.allSevenParentsCoveredByPassingLeaves, true);
  assert.equal(deep.decisions.finalLeafBoxCountAcrossSevenParents, 2896);
  assert.equal(deep.decisions.finalPassedLeafBoxCount, 2896);
  assert.equal(deep.decisions.finalInconclusiveLeafBoxCount, 0);
  assert.equal(deep.decisions.completedDepth, 5);
  assert.deepEqual(
    deep.decisions.layers.map((row) => [row.depth, row.boxCount, row.passedBoxCount, row.failedBoxCount]),
    [[3, 384, 64, 320], [4, 1280, 768, 512], [5, 2048, 2048, 0]],
  );
  assert.match(deep.decisions.minimumFinalPassedLeafEvansAbsoluteLower.value, /^\[0\.007149506/);
  assert.match(deep.interpretation.limitation, /cannot replace the uniform Clenshaw contour certificate/);
});

test("R0.73J theorem and audits preserve the exact mathematical and Clay boundary", async () => {
  const [theorem, gap, adversarial, failure] = await Promise.all([
    text("research/r073j_continuum_branch_theorem.md"),
    text("research/r073j_gap_matrix.md"),
    text("research/r073j_adversarial_audit.md"),
    json("experiments/r073j/failure_ledger.json"),
  ]);
  for (const token of [
    "\\lambda_0:[0,1/450]\\longrightarrow(167/1000,173/1000)",
    "\\operatorname{Re}z\\le\\frac{11}{100}",
    "g_*=\\frac1{20}",
    ">0.5853>\\frac12",
    "finite-time singularity or the Clay problem",
  ]) assert.ok(theorem.includes(token), token);
  for (let index = 0; index <= 11; index += 1) {
    assert.match(gap, new RegExp(`\\| J${index} \\|[^\n]+\\| \\*\\*CLOSED / PASS`));
  }
  assert.match(gap, /J12[^\n]+FINITE DIAGNOSTIC ONLY/);
  assert.match(gap, /J17[^\n]+OPEN/);
  assert.match(adversarial, /not two independent ODE proofs/);
  assert.match(adversarial, /Those boxes do not form a complete contour cover/);
  assert.equal(failure.entries.length, 2);
  assert.equal(failure.claimBoundary.rawGridWasSilentlyOverwritten, false);
});

test("R0.73J sealed experiment and journal figure inventories are exact", async () => {
  const [manifest, summary, figure] = await Promise.all([
    json("experiments/r073j/manifest.json"),
    json("experiments/r073j/summary.json"),
    json("figures/r073j/fig-r073j-continuum-branch-certificate/manifest.json"),
  ]);
  assert.equal(manifest.status, "passed");
  assert.equal(manifest.allChecksPass, true);
  assert.equal(manifest.diagnosticOnly, false);
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(manifest.sharedRawGridLimitationDeclared, true);
  assert.equal(manifest.naturalBoxAuditIsPrerequisite, false);
  assert.equal(summary.claimBoundary.continuumSpectralBranchCertified, true);
  assert.equal(summary.claimBoundary.viscousRankOneBranchCertified, false);
  assert.equal(summary.claimBoundary.clayProblemSolved, false);

  const ledger = (await text("experiments/r073j/SHA256SUMS")).trim().split("\n");
  const names = ledger.map((row) => row.slice(66));
  const actual = (await readdir(resolve(root, "experiments/r073j"), { withFileTypes: true }))
    .filter((entry) => entry.isFile() && entry.name !== "SHA256SUMS")
    .map((entry) => entry.name)
    .sort();
  assert.deepEqual(names, actual);
  for (const row of ledger) {
    const match = row.match(/^([0-9a-f]{64})  ([^/]+)$/);
    assert.ok(match, row);
    assert.equal(await sha256(`experiments/r073j/${match[2]}`), match[1], match[2]);
  }

  assert.equal(figure.status, "formal");
  assert.equal(figure.publicationStatus, "prepublication");
  assert.equal(figure.qa.status, "passed");
  assert.equal(figure.qa.visualInspectionExplicit, true);
  assert.equal(figure.claimBoundary.continuumSpectralBranchCountCertified, true);
  assert.equal(figure.claimBoundary.viscousBranchCertified, false);
  assert.equal(figure.claimBoundary.clayProblemSolved, false);
  for (const name of ["figure.pdf", "figure.svg", "figure.png"]) {
    const info = await stat(resolve(root, `figures/r073j/fig-r073j-continuum-branch-certificate/${name}`));
    assert.ok(info.size > 1000, name);
  }
});
