import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const certificateRoot = new URL(
  "../research/certificates/r069u-dyadic-qmc/",
  import.meta.url,
);

test("archives the monitored R0.69U finite-radius QMC evidence", async () => {
  const [resultText, profileText, summaryText, resources, progress, readme] =
    await Promise.all([
      readFile(new URL("result.json", certificateRoot), "utf8"),
      readFile(new URL("profile.json", certificateRoot), "utf8"),
      readFile(new URL("summary.csv", certificateRoot), "utf8"),
      readFile(new URL("resources.csv", certificateRoot), "utf8"),
      readFile(new URL("progress.ndjson", certificateRoot), "utf8"),
      readFile(new URL("README.md", certificateRoot), "utf8"),
    ]);
  const result = JSON.parse(resultText);
  const profile = JSON.parse(profileText);
  assert.equal(result.status, "passed");
  assert.equal(result.method.replicates, 16);
  assert.equal(result.method.pointsPerReplicate, 2 ** 18);
  assert.equal(result.method.pairsPerRadius, 16 * 2 ** 18);
  assert.deepEqual(result.method.radiusPowers, [0, 1, 2, 3, 4, 5, 6]);
  assert.equal(
    result.provenance.sourceCommit,
    "29ca62f2667816cb26564b2791251a9d2e68197c",
  );
  assert.equal(
    result.provenance.scriptSha256,
    "3516720be82e4c7c97e42295c5e86ad6c6199b6a0c8cfe74b33d738dd6cc7828",
  );
  assert.equal(result.audits.partitionResidualMax, 0);
  assert.ok(result.audits.sampleReconstructionResidualMax < 1e-12);
  assert.equal(result.audits.energyBelowRigorousBound, true);
  assert.equal(result.audits.limitingOuterPositive, true);
  assert.equal(result.audits.sourceCommitMatchesHead, true);
  assert.equal(profile.limitingCoreRatio, 1);
  assert.ok(profile.transitionEnergy < profile.rigorousEnergyUpperBound);
  assert.ok(profile.limitingOuterCarrier > 0.08);
  assert.match(summaryText, /64,3\.4201322121361635/);
  assert.match(resources, /exited:0/);
  assert.match(progress, /"event": "finished"/);
  assert.match(readme, /29,360,128 evaluated pairs/);
  assert.match(readme, /not an interval enclosure/i);
});

test("resolves the two positive principal annuli at R=64", async () => {
  const result = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const radius64 = result.summaries.find((entry) => entry.radius === 64);
  assert.ok(radius64);
  assert.equal(radius64.coreCancellationRatio, 1);
  assert.ok(radius64.innerAnnulusMean > 0);
  assert.ok(radius64.outerAnnulusMean > 0);
  assert.equal(radius64.nonprincipalSignedMean, 0);
  assert.ok(
    Math.abs(radius64.absoluteError) < 4 * radius64.totalScrambleSe,
    "R=64 mean should agree with the exact core value within four scramble SE",
  );
});

test("locks every R0.69U QMC payload by SHA-256", async () => {
  const sumsText = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
