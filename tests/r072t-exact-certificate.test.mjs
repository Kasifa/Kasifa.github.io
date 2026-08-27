import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const cert = resolve(root, "research/certificates/r072t");
const run = promisify(execFile);
const json = async (name) => JSON.parse(await readFile(resolve(cert, name), "utf8"));

test("R0.72T exact certificate fixes the heat, scale, action, and claim-boundary ledgers", async () => {
  const [certificate, independent, crosscheck, manifest] = await Promise.all([
    json("certificate.json"), json("independent.json"), json("crosscheck.json"), json("manifest.json"),
  ]);
  assert.equal(certificate.status, "passed");
  assert.ok(Object.values(certificate.exactChecks).every(Boolean));
  assert.deepEqual(certificate.heatProfile.collisionTaylor, {
    x: "0/1", "x^3": "-1/4", "x^5": "1/16", "x^7": "-1/160",
  });
  assert.match(certificate.heatProfile.heatIdentity, /partial_d W=partial_x\^2 W/);
  assert.deepEqual(certificate.scaling.solution, {
    alpha: "-3/5", beta: "-2/5", gamma: "1/5", delta: "-1/5",
  });
  assert.equal(independent.actionFifthCoefficient, "1/720");
  assert.equal(certificate.driftOnlyCalibration.qZeroNorm, "1/1");
  assert.equal(certificate.gaugeAndInviscid.timeOnlyPhaseRemovable, true);
  for (const key of ["blockContractionProved", "periodicTransferProved", "allStartSemigroupEstimateProved", "combinedCubicAndTimeDriftEstimateProved", "clayMillenniumProblemSolved"]) {
    assert.equal(certificate.claimBoundary[key], false, key);
  }
  assert.equal(crosscheck.status, "passed");
  assert.ok(Object.values(crosscheck.checks).every(Boolean));
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.ok(Array.isArray(manifest.sourceBindings) && manifest.sourceBindings.length > 0);
  assert.equal(crosscheck.formalSourceReady, true);
  assert.equal(crosscheck.sourceCommit, manifest.sourceCommit);
  assert.deepEqual(crosscheck.sourceBindings, manifest.sourceBindings);
  const rows = (await readFile(resolve(cert, "SHA256SUMS"), "utf8")).trim().split("\n");
  const names = [];
  for (const row of rows) {
    const [, expected, name] = row.match(/^([0-9a-f]{64})  ([^/]+)$/);
    assert.equal(createHash("sha256").update(await readFile(resolve(cert, name))).digest("hex"), expected);
    names.push(name);
  }
  assert.deepEqual(names, (await readdir(cert)).filter((name) => name !== "SHA256SUMS").sort());
  await run(process.env.CODEX_PYTHON || "python3", ["research/certificates/r072t/validate_certificate.py", "--require-formal"], { cwd: root });
});
