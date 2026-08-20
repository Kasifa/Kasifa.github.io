import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const auditUrl = new URL(
  "../research/eighth_order_moment_interval_audit.py",
  import.meta.url,
);
const noteUrl = new URL(
  "../research/eighth_order_moment_interval_note.md",
  import.meta.url,
);
const prepareUrl = new URL(
  "../research/prepare_eighth_order_quad_moment.py",
  import.meta.url,
);
const engineUrl = new URL(
  "../research/eighth_order_quad_moment_engine.cpp",
  import.meta.url,
);
const verifierUrl = new URL(
  "../research/verify_eighth_order_quad_moment_output.cpp",
  import.meta.url,
);
const archiveRoot = new URL(
  "../research/certificates/r068b2f-moments/",
  import.meta.url,
);

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

test("documents the rejected binary64 baseline and guarded binary128 route", async () => {
  const [audit, note, prepare, engine, verifier] = await Promise.all([
    readFile(auditUrl, "utf8"),
    readFile(noteUrl, "utf8"),
    readFile(prepareUrl, "utf8"),
    readFile(engineUrl, "utf8"),
    readFile(verifierUrl, "utf8"),
  ]);
  assert.match(audit, /EXPECTED_NORMAL_INFINITY_NORM = 2_024_341_504/);
  assert.match(audit, /gamma_bound/);
  assert.match(audit, /residual_enclosure/);
  assert.match(audit, /solution_error_radii/);
  assert.match(audit, /precision-baseline-rejected/);
  assert.doesNotMatch(audit, /"status": "certified-passed"/);
  assert.match(note, /\\|C\\^\\mathsf TC\\|_\\infty=2024341504/);
  assert.match(note, /does not solve the\s+Navier--Stokes Millennium problem/);
  assert.match(prepare, /double_double_interval/);
  assert.match(prepare, /dominantMassIntervalVectorSha256/);
  assert.match(prepare, /write_payload_manifest/);
  assert.match(engine, /using f128 = _Float128/);
  assert.match(engine, /gamma_bound/);
  assert.match(engine, /residual_solution_radii/);
  assert.match(engine, /roundingModeIsNearest/);
  assert.match(engine, /validate_interval_vectors/);
  assert.match(engine, /payloadManifestSha256/);
  assert.match(verifier, /EXPECTED_VALUES = 14350336/);
  assert.match(verifier, /allRadiiNonnegative/);
});

test("locks the source-bound degree-ten binary128 moment certificate", async () => {
  const [report, verification, metadata, payloadManifest, outputHashes, sizes, resources, sums] =
    await Promise.all([
      readFile(new URL("moment-enclosure.json", archiveRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-verification.json", archiveRoot), "utf8").then(JSON.parse),
      readFile(new URL("sparse-bundle-metadata.json", archiveRoot), "utf8").then(JSON.parse),
      readFile(new URL("payload-manifest.sha256", archiveRoot)),
      readFile(new URL("output-array-SHA256SUMS", archiveRoot), "utf8"),
      readFile(new URL("output-array-sizes.txt", archiveRoot), "utf8"),
      readFile(new URL("resources.csv", archiveRoot), "utf8"),
      readFile(new URL("SHA256SUMS", archiveRoot), "utf8"),
    ]);

  assert.equal(report.status, "certified-passed");
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.maximumDegree, 10);
  assert.equal(report.channelsPerState, 8008);
  assert.equal(report.stateDimension, 1792);
  assert.equal(report.totalCoordinates, 14350336);
  assert.equal(
    report.provenance.sourceCommit,
    "2d4c9e1c4150034b8204cea32d19238ca3013190",
  );
  assert.equal(
    report.provenance.payloadManifestSha256,
    "e80e5224aba65c8493bd8b89d21b3413d96427caa7aa9db6d48ba3d0884cf3b1",
  );
  assert.equal(report.centredMaximumRadius < 1.89e-20, true);
  assert.equal(report.degrees[10].maximumRadius < 7.92e-22, true);

  assert.equal(verification.status, "verified");
  assert.equal(verification.valuesPerArray, 14350336);
  assert.equal(verification.allValuesFinite, true);
  assert.equal(verification.allRadiiNonnegative, true);
  assert.equal(metadata.payloadManifest.fileCount, 410);
  assert.equal(metadata.payloadManifest.totalBytes, 58913830);
  assert.equal(sha256(payloadManifest), report.provenance.payloadManifestSha256);
  assert.match(outputHashes, /9a416a0912b28205263a755cac89b62664b513b8ba705bbd908effb0a78cfa44  raw-centre\.f128/);
  assert.match(outputHashes, /437a8f18234fb8c07ea23661a77e3413eee4dbb674e4dcefd83a17d386a268bf  centred-radius\.f128/);
  assert.equal((sizes.match(/229605376/g) ?? []).length, 4);
  assert.match(resources, /512\.856,exited:0,1763,1960264,20/);

  for (const line of sums.trim().split("\n")) {
    const [expected, filename] = line.split(/\s+/, 2);
    const contents = await readFile(new URL(filename, archiveRoot));
    assert.equal(sha256(contents), expected, filename);
  }
});
