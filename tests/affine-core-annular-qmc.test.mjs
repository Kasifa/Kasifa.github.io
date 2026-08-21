import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";

const root = new URL("../", import.meta.url);
const certificateRoot = new URL("research/certificates/r069t-affine-qmc/", root);

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

test("archives the monitored R0.69T affine-core annular QMC evidence", async () => {
  const result = JSON.parse(await readFile(new URL("result.json", certificateRoot), "utf8"));
  assert.equal(result.classification, "exploratory scrambled-Sobol quadrature");
  assert.equal(result.quadrature.dimension, 5);
  assert.equal(result.quadrature.replicates, 16);
  assert.equal(result.quadrature.pointsPerReplicate, 2 ** 22);
  assert.equal(result.quadrature.totalFinestPoints, 67_108_864);
  assert.equal(result.source.sha256, "27047478eba4ee817190c77cf07904d3067b56b7141015ee9eb941f01ed42e99");
  assert.equal(result.allChecksPass, true);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.ok(Math.abs(result.finest.zScore) < 4);
  assert.ok(result.finest.annularCancellationRatioWithoutNearTail > 0.996);
  assert.ok(result.finest.annularCancellationRatioWithoutNearTail < 0.997);
  const outer = result.annularFinest.find((row) => row.index === 1);
  assert.ok(outer.ci95Upper < 0);
  assert.match(result.claimBoundary.join(" "), /not an interval enclosure/i);
});

test("locks every R0.69T QMC certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const records = sums.trim().split("\n").map((line) => {
    const [digest, name] = line.split(/\s{2}/);
    return [name, digest];
  });
  assert.equal(records.length, 7);
  for (const [name, expected] of records) {
    const buffer = await readFile(new URL(name, certificateRoot));
    assert.equal(sha256(buffer), expected, name);
  }
});

test("records scientific progress and independent process-tree monitoring", async () => {
  const [progress, resources, readme] = await Promise.all([
    readFile(new URL("progress.ndjson", certificateRoot), "utf8"),
    readFile(new URL("resources.csv", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
  ]);
  assert.equal(progress.trim().split("\n").length, 18);
  assert.match(progress, /"event": "completed"/);
  assert.match(resources, /exited:0/);
  assert.match(resources, /2045\.141/);
  assert.match(readme, /67,108,864 pairs total/);
  assert.match(readme, /not an interval enclosure/i);
});
