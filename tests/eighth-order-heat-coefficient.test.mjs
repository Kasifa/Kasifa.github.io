import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const noteUrl = new URL(
  "../research/eighth_order_heat_coefficient_note.md",
  import.meta.url,
);
const prepareUrl = new URL(
  "../research/prepare_eighth_order_heat_coefficient.py",
  import.meta.url,
);
const engineUrl = new URL(
  "../research/eighth_order_heat_coefficient_engine.cpp",
  import.meta.url,
);
const verifierUrl = new URL(
  "../research/verify_eighth_order_heat_coefficient_output.cpp",
  import.meta.url,
);
const archiveRoot = new URL(
  "../research/certificates/r068b2g-heat-jet/",
  import.meta.url,
);

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

test("states the guarded heat-jet sign and its unresolved defect boundary", async () => {
  const [note, prepare, engine, verifier] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(prepareUrl, "utf8"),
    readFile(engineUrl, "utf8"),
    readFile(verifierUrl, "utf8"),
  ]);
  assert.match(note, /1\.07451892110713391\\times10\^\{-25\}/);
  assert.match(note, /Q=\\frac\{605\}\{16\}/);
  assert.match(note, /signature-compressed spatial Taylor defect/);
  assert.match(note, /does not solve the\s+Navier--Stokes Millennium problem/);
  assert.match(prepare, /maximum_rate_l1 != Fraction\(605, 16\)/);
  assert.match(prepare, /successiveRatioUpper/);
  assert.match(engine, /degreeTenHeatJetIsStrictlyNegative/);
  assert.match(engine, /lower_difference/);
  assert.match(engine, /upper_sum/);
  assert.match(verifier, /binary64ReferenceMaximumDifferenceUpper/);
});

test("locks the formal guarded degree-ten heat-jet certificate", async () => {
  const [report, verification, metadata, payloadManifest, resources, sums] =
    await Promise.all([
      readFile(new URL("heat-jet.json", archiveRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-verification.json", archiveRoot), "utf8").then(JSON.parse),
      readFile(new URL("heat-data-metadata.json", archiveRoot), "utf8").then(JSON.parse),
      readFile(new URL("heat-payload-manifest.sha256", archiveRoot)),
      readFile(new URL("resources.csv", archiveRoot), "utf8"),
      readFile(new URL("SHA256SUMS", archiveRoot), "utf8"),
    ]);
  assert.equal(report.status, "strict-passed");
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.parameters.maximumDegree, 10);
  assert.equal(report.parameters.channels, 8008);
  assert.equal(report.parameters.shuffleCount, 35);
  assert.equal(
    report.provenance.sourceCommit,
    "014a9e604c65b405ebc7684cf3913c74ef19a55e",
  );
  assert.equal(
    report.provenance.heatPayloadManifestSha256,
    "7fe9ffa660701c3f2314c32cbad803b3973ce33a0e26f475802260c583cf91f0",
  );
  assert.equal(report.degreeTenHeatJet.upper < 0, true);
  assert.equal(report.degreeTenHeatJet.radius < 1.08e-25, true);
  assert.equal(report.uniformCoefficientTailUpper < 2.627e-25, true);
  assert.equal(verification.status, "verified");
  assert.equal(verification.coefficientCount, 8008);
  assert.equal(verification.strictlyNegative, true);
  assert.equal(metadata.maximumRateCoefficientL1.numerator, "605");
  assert.equal(metadata.maximumRateCoefficientL1.denominator, "16");
  assert.equal(metadata.tail.firstOmittedOrder, 65);
  assert.equal(sha256(payloadManifest), report.provenance.heatPayloadManifestSha256);
  assert.match(resources, /41\.642,exited:0,1211,469596,20/);

  for (const line of sums.trim().split("\n")) {
    const [expected, filename] = line.split(/\s+/, 2);
    const contents = await readFile(new URL(filename, archiveRoot));
    assert.equal(sha256(contents), expected, filename);
  }
});
