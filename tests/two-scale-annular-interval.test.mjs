import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const certificateRoot = new URL("../research/certificates/r069w/", import.meta.url);

test("certifies the complete R0.69W amplitude-family obstruction", async () => {
  const [result, verifier] = await Promise.all([
    readFile(new URL("result.json", certificateRoot), "utf8").then(JSON.parse),
    readFile(new URL("verifier.json", certificateRoot), "utf8").then(JSON.parse),
  ]);
  assert.equal(result.release, "R0.69W");
  assert.equal(result.status, "passed");
  assert.equal(result.decision.j0ConstantContainsExactZero, true);
  assert.equal(result.decision.j0LeadingCoefficientStrictlyNegative, true);
  assert.equal(result.decision.j0QuadraticDiscriminantStrictlyNegative, true);
  assert.equal(result.decision.jMinus2AtZeroStrictlyNegative, true);
  assert.equal(result.decision.allPositiveAmplitudesHaveNegativeJ0, true);
  assert.equal(result.decision.endpointHasNegativeJMinus2, true);
  assert.equal(result.decision.entireAmplitudeFamilyExcluded, true);
  assert.ok(result.coefficientIntervals.j0.c3[1] < 0);
  assert.ok(result.decision.j0QuadraticDiscriminantInterval[1] < 0);
  assert.ok(result.coefficientIntervals.jMinus2.c0[1] < 0);
  assert.equal(verifier.passed, true);
  assert.deepEqual(verifier.failed, []);
  assert.ok(Object.values(verifier.checks).every(Boolean));
});

test("locks the true convolution, sixth-order endpoints, and formal grid", async () => {
  const result = JSON.parse(await readFile(new URL("result.json", certificateRoot), "utf8"));
  assert.equal(result.provenance.sourceCommit, "2b3141a333d3dea0c4b7a241c11f9adbca31d1b4");
  assert.equal(result.provenance.requestedSourceCommit, result.provenance.sourceCommit);
  assert.equal(result.provenance.sourceTreeDirty, false);
  assert.equal(result.mollifier.trueConvolutionCertified, true);
  assert.equal(result.mollifier.floatingQuadratureNodesUsed, 0);
  assert.equal(result.mollifier.endpointDistributionTermsThroughOrderSix, true);
  assert.equal(result.mollifier.distanceCellCutoffRangesUseMonotoneEndpointInterpolation, true);
  assert.match(result.mollifier.cutoffPointInterpolation, /cubic Hermite/);
  assert.equal(result.mollifier.centerMomentDerivativesUseCertifiedPointTaylor, true);
  assert.match(result.mollifier.cutoffPointDerivatives, /fourth-derivative remainder/);
  assert.equal(result.mollifier.distanceMomentGridUsesExactDyadicEndpoints, true);
  assert.equal(result.method.maximumCertifiedCutoffDerivativeOrder, 6);
  assert.equal(result.method.rawMomentPower, 19);
  assert.equal(result.method.cutoffCells, 2048);
  assert.equal(result.method.transitionCells, 512);
  assert.equal(result.method.momentPower, 22);
  assert.equal(result.method.coreCells, 128);
  assert.equal(result.method.plateauCells, 256);
  assert.equal(result.method.boundaryRefinement, 4);
  assert.equal(result.method.arbPrecisionBits, 256);
  assert.equal(result.method.workers, 20);
  assert.equal(result.partial.allRowsCoveredExactlyOnce, true);
  for (const index of ["0", "-2"]) {
    assert.equal(result.integrationAudits[index].allRowsCoveredExactlyOnce, true);
    assert.ok(result.integrationAudits[index].selectedThirdOrderBoxesByCoefficient.some(Number.isFinite));
    assert.ok(result.integrationAudits[index].selectedFourthOrderBoxesByCoefficient.some(Number.isFinite));
  }
});

test("locks every archived R0.69W payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");
  assert.ok(lines.length >= 80, "expected merged files plus four payloads for each of 20 workers");
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})\s+(.+)$/);
    assert.ok(match, "malformed SHA256SUMS line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2] + " hash mismatch");
  }
});

test("documents the exact polynomial proof and hybrid remainder", async () => {
  const note = await readFile(new URL("../research/two_scale_annular_interval_note.md", import.meta.url), "utf8");
  assert.ok(note.includes("c_3<0"));
  assert.ok(note.includes("\\Delta=c_2^2-4c_1c_3<0"));
  assert.ok(note.includes("D^6S="));
  assert.ok(note.includes("smaller of (4.1) and (4.2)"));
  assert.match(note, /not a theorem about Navier--Stokes time evolution/);
});
