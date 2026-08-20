import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const noteUrl = new URL(
  "../research/eighth_order_signature_defect_note.md",
  import.meta.url,
);
const prepareUrl = new URL(
  "../research/prepare_eighth_order_signature_defect.py",
  import.meta.url,
);
const engineUrl = new URL(
  "../research/eighth_order_signature_defect_engine.cpp",
  import.meta.url,
);
const verifierUrl = new URL(
  "../research/verify_eighth_order_signature_defect_output.py",
  import.meta.url,
);
const certificateUrl = new URL(
  "../research/certificates/r068b2h-corrected-heat/",
  import.meta.url,
);

test("states the strict corrected heat sign and its all-order boundary", async () => {
  const [note, prepare, engine, verifier] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(prepareUrl, "utf8"),
    readFile(engineUrl, "utf8"),
    readFile(verifierUrl, "utf8"),
  ]);
  assert.match(note, /-2\.87321129703704757\\times10\^\{-9\}/);
  assert.match(note, /product of the four entrywise-absolute/);
  assert.match(note, /source-locked guarded run/);
  assert.match(note, /does not control all Picard orders/);
  assert.match(note, /does not solve the Navier--Stokes Millennium problem/);
  assert.match(prepare, /EXPECTED_CLASSES = 44_514/);
  assert.match(prepare, /absolute-cycle\.data\.i32/);
  assert.match(prepare, /derivative-upper\.f64/);
  assert.match(engine, /correctedDominantHeatIntervalIsStrictlyNegative/);
  assert.match(engine, /CARRY_WEIGHTS/);
  assert.match(engine, /absolute-cycle\.indptr\.i64/);
  assert.match(verifier, /allDefectPayloadHashesAndSizesMatch/);
  assert.match(verifier, /serializedCorrectedIntervalIsEightUlpConsistent/);
});

test("archives and independently verifies the source-locked R0.68B-2h certificate", async () => {
  const [summary, metadata, verification, readme, checksums] = await Promise.all([
    readFile(new URL("defect-sign.json", certificateUrl), "utf8").then(JSON.parse),
    readFile(new URL("defect-data-metadata.json", certificateUrl), "utf8").then(JSON.parse),
    readFile(new URL("independent-verification.json", certificateUrl), "utf8").then(JSON.parse),
    readFile(new URL("README.md", certificateUrl), "utf8"),
    readFile(new URL("SHA256SUMS", certificateUrl), "utf8"),
  ]);

  assert.equal(summary.status, "strict-passed");
  assert.equal(
    summary.provenance.sourceCommit,
    "efd0d828678ce99fcc5d0f40d751b1883d32f740",
  );
  assert.equal(summary.parameters.signatureClasses, 44_514);
  assert.equal(summary.parameters.coveredFreeShifts, 16 ** 6);
  assert.equal(summary.correctedDominantHeat.lower, -2.69744373399132142e-8);
  assert.equal(summary.correctedDominantHeat.upper, -2.87321129703704757e-9);
  assert.ok(summary.correctedDominantHeat.upper < 0);
  assert.deepEqual(metadata.absolutePathCycle, {
    rows: 1792,
    columns: 1792,
    nonzeros: 695_808,
    maximumEntry: 134_512,
    maximumRowSum: 54_210_304,
  });
  assert.equal(verification.status, "strict-passed");
  assert.ok(Object.values(verification.checks).every(Boolean));
  assert.match(readme, /does not control an infinite family of Picard orders/);
  assert.match(readme, /not a\s+solution of the Millennium problem/);

  const records = checksums.trim().split("\n");
  assert.equal(records.length, 9);
  for (const record of records) {
    const [expected, name] = record.split(/\s+/, 2);
    const payload = await readFile(new URL(name, certificateUrl));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, `checksum mismatch for ${name}`);
  }
});
