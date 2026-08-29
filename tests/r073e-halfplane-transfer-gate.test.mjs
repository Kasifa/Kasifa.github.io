import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const sha256 = async (relative) => createHash("sha256")
  .update(await readFile(resolve(root, relative))).digest("hex");

const closed = [
  "fixedPositiveHalfPlaneNoPollution",
  "allModesRightOfBProjectionNormPersistence",
  "topInviscidClusterExists",
  "topViscousClusterPersistence",
  "topReducedHalfPlaneResolventUniform",
  "frozenTopClusterRelativeDichotomy",
  "fixedFrozenGeneratorVolterraTransfer",
  "logFastTimeTransfer",
  "superPolynomialCompleteRowNoGo",
];

const open = [
  "certifiedSigmaStarIsRightmost",
  "selectedSigmaStarComplementDichotomy",
  "uniformHalfPlaneBoundAtBEqualsZero",
  "globalRightHalfPlaneNoPollution",
  "absoluteUniformComplementDecay",
  "explicitHalfPlaneGap",
  "explicitViscosityThreshold",
  "quantitativeEigenvalueRate",
  "movingProfileUniformContour",
  "graphDomainKatoTransport",
  "movingProfileEvolutionDichotomy",
  "inviscidRootUnique",
  "inviscidEigenvalueSimple",
  "completeOSSquireA2DirectSum",
  "fixedWindowExponentialLowerLaw",
  "nonlinearNavierStokes",
  "Clay",
];

async function verifyManifestHashes(relative) {
  const manifest = await json(relative);
  let count = 0;
  for (const group of [
    "sources", "inputs", "outputs",
    "sourceBindings", "outputBindings", "packageBindings",
  ]) {
    for (const row of manifest[group] ?? []) {
      if (typeof row !== "object") continue;
      const direct = row.path;
      const local = relative.slice(0, relative.lastIndexOf("/") + 1) + row.path;
      let actual;
      try { actual = await sha256(direct); } catch { actual = await sha256(local); }
      assert.equal(actual, row.sha256, `${relative}: ${row.path}`);
      count += 1;
    }
  }
  assert.ok(count > 0, relative);
  return manifest;
}

test("R0.73E analytic chain closes exactly nine one-row statements", async () => {
  const [freeze, proof, report, audit, gap] = await Promise.all([
    text("research/r073e_problem_freeze.md"),
    text("research/r073e_halfplane_transfer_proof.md"),
    text("research/r073e_report-source.md"),
    text("research/r073e_independent_analytic_audit.md"),
    text("research/r073e_gap_matrix.md"),
  ]);
  for (const key of closed) {
    for (const [source, label] of [[freeze, "freeze"], [report, "report"], [audit, "audit"], [gap, "gap"]]) {
      assert.ok(source.includes(`${key}=CLOSED`), `${label}: ${key}`);
    }
  }
  for (const key of open) {
    for (const [source, label] of [[freeze, "freeze"], [report, "report"], [gap, "gap"]]) {
      assert.ok(source.includes(`${key}=OPEN`), `${label}: ${key}`);
    }
  }
  for (const token of [
    "B_\\varepsilon=M+K-\\varepsilon L",
    "O(|\\tau|^{-1})",
    "Bromwich",
    "M\\log(1/\\varepsilon)",
    "49}{4}",
    "G_{1/2}",
  ]) assert.ok(proof.includes(token) || report.includes(token), token);
  assert.match(audit, /PASS/);
  assert.match(audit, /complete-row consequence/);
  assert.match(report, /No originality or priority claim is made/);
  assert.doesNotMatch(report, /Clay=(?:CLOSED|TRUE)/);
});

test("R0.73E reader-facing source has no control characters or naked sentinel math", async () => {
  const content = await text("scripts/r073e_release_content.py");
  assert.doesNotMatch(content, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  assert.ok(content.includes("\\(\\varepsilon&gt;0\\)"));
  assert.ok(content.includes("\\(M\\log(1/\\varepsilon)\\)"));
  assert.ok(content.includes("\\(6.2430\\times10^{{-14}}\\)"));
  assert.equal(content.includes("6.2431"), false);
  assert.equal(content.includes("Kato--Schmid"), false);
});

test("R0.73E certificate is independently passed and bound to the audited report commit", async () => {
  const [certificate, independent, validation, manifest] = await Promise.all([
    json("research/certificates/r073e/certificate.json"),
    json("research/certificates/r073e/independent_recompute.json"),
    json("research/certificates/r073e/validation.json"),
    verifyManifestHashes("research/certificates/r073e/manifest.json"),
  ]);
  assert.equal(validation.allChecksPass, true);
  assert.equal(independent.allChecksPass, true);
  const theorem = certificate.theorem ?? certificate.claimLedger ?? certificate.closedClaims;
  for (const key of closed) assert.ok(["CLOSED", true].includes(theorem[key]), key);
  for (const key of open) assert.ok(["OPEN", false].includes(certificate.claimBoundary[key]), key);
  const commit = "803279d72c24a54db27c40dcdad97593636788fc";
  assert.equal(certificate.sourceCommit ?? manifest.sourceCommit, commit);
  assert.equal(manifest.sourceCommit, commit);
});

test("R0.73E finite diagnostic is reproducible but cannot certify a continuum theorem", async () => {
  const [primary, independent] = await Promise.all([
    json("experiments/r073e/complement_diagnostic.json"),
    json("experiments/r073e/independent_validation.json"),
  ]);
  assert.equal(primary.allChecksPass, true);
  assert.equal(independent.allChecksPass, true);
  assert.ok(Object.values(primary.checks).every(Boolean));
  assert.equal(primary.claimBoundary.finiteBinary64Diagnostic, true);
  assert.equal(primary.claimBoundary.ordinaryCutoffAgreementIsContinuumProof, false);
  assert.equal(primary.claimBoundary.continuumComplementaryDichotomyProvedHere, false);
  assert.equal(primary.claimBoundary.nonautonomousTransferProvedHere, false);
  const raw = JSON.stringify(primary);
  for (const value of [
    "0.170406506600201",
    "0.040536174080661",
    "0.176136754131769",
    "378.478",
    "56.299",
    "21.257",
  ]) assert.ok(raw.includes(value), value);
  const rows = (await text("experiments/r073e/SHA256SUMS")).trim().split("\n");
  const files = (await readdir(resolve(root, "experiments/r073e")))
    .filter((name) => name !== "SHA256SUMS").sort();
  assert.deepEqual(rows.map((row) => row.slice(66).split("/").at(-1)).sort(), files);
  for (const row of rows) assert.equal(await sha256(row.slice(66)), row.slice(0, 64));
});

test("R0.73E formal figure is source-bound and fail-closed", async () => {
  const [manifest, contract, validation] = await Promise.all([
    verifyManifestHashes("figures/r073e/fig-r073e-complement-transfer/manifest.json"),
    json("figures/r073e/fig-r073e-complement-transfer/contract.json"),
    json("figures/r073e/fig-r073e-complement-transfer/validation.json"),
  ]);
  assert.equal(manifest.release, "R0.73E");
  assert.equal(manifest.figureId, "fig-r073e-complement-transfer");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.git.sourceCommit, "645e862c06cf31c3d7551dac292af43eea3ec1b5");
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.equal(contract.claimBoundary.formalFiniteDiagnosticFigure, true);
  for (const key of [
    "finiteSpectrumIsContinuumSpectrum",
    "finiteResolventPeaksAreUniformHalfPlaneBound",
    "sampledSemigroupIsContinuousTimeBound",
    "nonautonomousTransferProvedHere",
    "nonlinearNavierStokesProvedHere",
    "clayProblemSolved",
  ]) assert.equal(contract.claimBoundary[key], false, key);
  const png = await readFile(resolve(root, "figures/r073e/fig-r073e-complement-transfer/figure.png"));
  assert.ok(png.length > 500_000);
  assert.equal(png.subarray(1, 4).toString("latin1"), "PNG");
});
