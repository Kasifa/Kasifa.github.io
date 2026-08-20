import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const noteUrl = new URL(
  "../research/eighth_order_heat_defect_pilot_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/eighth_order_heat_defect_pilot.py",
  import.meta.url,
);
const archiveRoot = new URL(
  "../research/certificates/r068b2c-pilot/",
  import.meta.url,
);

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

test("states the degree-ten defect improvement and complete mixed-derivative scan", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);
  assert.match(note, /44514/);
  assert.match(note, /16777216/);
  assert.match(note, /8008/);
  assert.match(note, /30\.23448650536/);
  assert.match(note, /0\.00469566611239/);
  assert.match(note, /2\.5663266368\\times10\^\{-6\}/);
  assert.match(note, /4368/);
  assert.match(note, /not yet a theorem/i);
  assert.match(note, /does not solve the Navier--Stokes Millennium problem/i);
  assert.match(audit, /fourteen-component/);
  assert.match(audit, /all 4,368 multiindices/);
  assert.match(note, /max_\{\|\\alpha\|=11\}/);
});

test("locks the monitored degree-ten defect pilot archive", async () => {
  const [jsonBuffer, stdoutBuffer, stderrBuffer, resourcesBuffer, checksumText] =
    await Promise.all([
      readFile(new URL("eighth-order-heat-defect-pilot.json", archiveRoot)),
      readFile(new URL("eighth-order-heat-defect-pilot.stdout.log", archiveRoot)),
      readFile(new URL("eighth-order-heat-defect-pilot.stderr.log", archiveRoot)),
      readFile(new URL("resources.csv", archiveRoot)),
      readFile(new URL("SHA256SUMS", archiveRoot), "utf8"),
    ]);
  const report = JSON.parse(jsonBuffer.toString("utf8"));
  assert.equal(report.status, "exploratory-passed");
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.parameters.jetDegree, 10);
  assert.equal(report.parameters.channelsPerState, 8008);
  assert.equal(report.parameters.totalMomentCoordinates, 14350336);
  assert.equal(report.signatureCompression.signatureClasses, 44514);
  assert.equal(report.signatureCompression.processedFreeShifts, 16777216);
  assert.equal(report.signatureCompression.maximumAbsoluteSignatureEntry, 1);
  assert.ok(report.defect.observableAggregated < 30.235);
  assert.ok(report.resolvent.observableUpper < 0.004696);
  assert.ok(
    report.pureDerivativeMajorants.maximumPureBound <
      report.gapDiagnostics.requiredGlobalDerivativeUpper,
  );
  assert.match(
    report.pureDerivativeMajorants.scope,
    /mixed multiindices are not certified/,
  );
  assert.equal(
    report.provenance.sourceCommit,
    "d05886b831dc51b14abefe62f34f6340b141dc1d",
  );
  assert.deepEqual(jsonBuffer, stdoutBuffer);
  assert.match(stderrBuffer.toString("utf8"), /classes=44514/);
  assert.match(stderrBuffer.toString("utf8"), /monitor: finished returncode=0/);
  assert.match(resourcesBuffer.toString("utf8"), /exited:0/);

  const expected = new Map(
    checksumText
      .trim()
      .split("\n")
      .map((line) => {
        const [digest, name] = line.trim().split(/\s+/);
        return [name, digest];
      }),
  );
  for (const [name, buffer] of [
    ["eighth-order-heat-defect-pilot.json", jsonBuffer],
    ["eighth-order-heat-defect-pilot.stdout.log", stdoutBuffer],
    ["eighth-order-heat-defect-pilot.stderr.log", stderrBuffer],
    ["resources.csv", resourcesBuffer],
  ]) {
    assert.equal(sha256(buffer), expected.get(name));
  }
});
