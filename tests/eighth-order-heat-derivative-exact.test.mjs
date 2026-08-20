import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const noteUrl = new URL(
  "../research/eighth_order_heat_derivative_exact_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/eighth_order_heat_derivative_exact_audit.py",
  import.meta.url,
);
const archiveRoot = new URL(
  "../research/certificates/r068b2d-exact/",
  import.meta.url,
);

test("documents the exact all-multiindex derivative certificate", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);
  assert.match(note, /4368/);
  assert.match(note, /35/);
  assert.match(note, /2\.567\\times10\^\{-6\}/);
  assert.match(note, /2\.56632663673508065521/);
  assert.match(note, /2b742828cfa00097b/);
  assert.match(note, /not establish global regularity/);
  assert.match(audit, /GMP rational arithmetic/);
  assert.match(audit, /allDerivativeMultiindicesArePresent/);
  assert.match(audit, /exactVectorSha256/);
});

test("locks the monitored exact derivative-majorant certificate", async () => {
  const [jsonText, stderr, resources] = await Promise.all([
    readFile(new URL("eighth-order-heat-derivative-exact.json", archiveRoot), "utf8"),
    readFile(new URL("eighth-order-heat-derivative-exact.stderr.log", archiveRoot), "utf8"),
    readFile(new URL("resources.csv", archiveRoot), "utf8"),
  ]);
  const report = JSON.parse(jsonText);
  assert.equal(report.status, "strict-passed");
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.derivativeMajorant.multiindexCount, 4368);
  assert.deepEqual(report.derivativeMajorant.maximumMultiindex, [0, 0, 0, 11, 0, 0]);
  assert.equal(
    report.derivativeMajorant.exactVectorSha256,
    "2b742828cfa00097b2ea1dc2203cae4da8c30164d9422a734bd12da8d6a468ee",
  );
  assert.match(
    report.derivativeMajorant.maximumUpper.decimal,
    /^2\.566326636735080655209837298880261917219e-06$/,
  );
  assert.equal(
    report.provenance.sourceCommit,
    "516768bc5dbdbb557e156af5e7141ca2374327c3",
  );
  assert.match(stderr, /shuffle=35\/35 multiindices=4368/);
  assert.match(stderr, /monitor: finished returncode=0/);
  assert.match(resources, /exited:0/);
});
