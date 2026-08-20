import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const noteUrl = new URL(
  "../research/eighth_order_cycle_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/eighth_order_cycle_audit.py",
  import.meta.url,
);
const requirementsUrl = new URL(
  "../research/requirements-r068b.txt",
  import.meta.url,
);
const certificateRoot = new URL(
  "../research/certificates/r068b1/",
  import.meta.url,
);

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

test("states the exact R0.68B-1 eighth-order spectrum and heat boundary", async () => {
  const [note, audit, requirements] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
    readFile(requirementsUrl, "utf8"),
  ]);

  assert.match(note, /R0\.68B-1 — The exact zero-time eighth-order image spectrum/);
  assert.ok(note.includes("A+B+C+D-E-F-G=Q"));
  assert.ok(note.includes("2\\times128\\times7=1792"));
  assert.ok(note.includes("\\operatorname{rank}W_8=204"));
  assert.ok(note.includes("x^{56}(x-4096)^{14}"));
  assert.ok(note.includes("q_{4,256}(x)^{14}"));
  assert.ok(note.includes("q_{10,16}(x)^6q_{18}(x)"));
  assert.ok(note.includes("Y_{8,r}=C_{8,0}\\nu^r+O(4800^r)"));
  assert.ok(note.includes("-0.02612679363405570"));
  assert.ok(note.includes("\\left(\\frac{41}{100}\\right)^r"));
  assert.ok(note.includes("not yet a bound on \\(S_{8,m}\\)"));
  assert.match(note, /globally smooth invariant parallel-shear class/);
  assert.match(note, /does not.*solve the Navier--Stokes Millennium problem/s);
  assert.match(audit, /not a certificate\s+for the complete heat-weighted seven-simplex observable/);
  assert.match(requirements, /scipy==1\.18\.0/);
  assert.match(requirements, /sympy==1\.14\.0/);
});

test("locks the formal R0.68B-1 certificate and monitored resources", async () => {
  const [jsonBuffer, stdoutBuffer, stderrBuffer, resourcesBuffer, checksumText] =
    await Promise.all([
      readFile(new URL("eighth-order-cycle-audit.json", certificateRoot)),
      readFile(new URL("eighth-order-cycle-audit.stdout.log", certificateRoot)),
      readFile(new URL("eighth-order-cycle-audit.stderr.log", certificateRoot)),
      readFile(new URL("resources.csv", certificateRoot)),
      readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    ]);
  const certificate = JSON.parse(jsonBuffer.toString("utf8"));
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(Object.keys(certificate.checks).length, 17);
  assert.equal(certificate.stateSpace.dimension, 1792);
  assert.deepEqual(certificate.stateSpace.carries, [-3, -2, -1, 0, 1, 2, 3]);
  assert.deepEqual(certificate.stateSpace.digitExactRanks, [448, 448]);
  assert.deepEqual(certificate.cycle.exactRanksByPower, [204, 148, 148]);
  assert.equal(certificate.cycle.imageDimension, 204);
  assert.equal(certificate.cycle.stableImageDimension, 148);
  assert.equal(
    certificate.cycle.imageCharacteristicSha256,
    "2a1ac6b6b2c0fc5b6939492425fd13709592b9eea14cae3d24a24f2bd248d75d",
  );
  assert.match(
    certificate.cycle.imageCharacteristicFactorization,
    /x\^56 \(x-4096\)\^14 q4_256\(x\)\^14 q10_16\(x\)\^6 q18\(x\)/,
  );
  assert.equal(
    certificate.reachableTargetFamily.vectorRecurrenceFromR34IsExact,
    true,
  );
  assert.equal(
    certificate.reachableTargetFamily.generatingGcdAscending[0],
    1,
  );
  assert.equal(
    certificate.reachableTargetFamily.dominantProjection
      .coefficientIsStrictlyNegative,
    true,
  );
  assert.ok(
    Number(
      certificate.reachableTargetFamily.dominantProjection
        .coefficientUpperDisplay,
    ) < -0.026,
  );
  assert.equal(
    certificate.reachableTargetFamily.coarseCertifiedProbeRateUpper,
    "256/625",
  );
  assert.equal(certificate.directAudit.exactLevelsChecked, 6);
  assert.equal(
    certificate.provenance.sourceCommit,
    "3ddf6d30965837311c0b659d5fb21e41c3b80f14",
  );
  assert.deepEqual(jsonBuffer, stdoutBuffer);
  assert.match(stderrBuffer.toString("utf8"), /restricting exact image dimension=204/);
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
    ["eighth-order-cycle-audit.json", jsonBuffer],
    ["eighth-order-cycle-audit.stdout.log", stdoutBuffer],
    ["eighth-order-cycle-audit.stderr.log", stderrBuffer],
    ["resources.csv", resourcesBuffer],
  ]) {
    assert.equal(sha256(buffer), expected.get(name));
  }
});
