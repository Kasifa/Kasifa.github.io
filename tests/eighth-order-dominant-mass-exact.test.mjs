import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const noteUrl = new URL(
  "../research/eighth_order_dominant_mass_exact_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/eighth_order_dominant_mass_exact_audit.py",
  import.meta.url,
);
const archiveRoot = new URL(
  "../research/certificates/r068b2e-exact/",
  import.meta.url,
);

test("documents exact dominant-mass interval reconstruction", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);
  assert.match(note, /1,792/);
  assert.match(note, /degree-33/);
  assert.match(note, /10\^\{-60\}/);
  assert.match(note, /does not prove the Navier--Stokes\s+Millennium statement/);
  assert.match(audit, /canonicalIntervalVectorSha256/);
  assert.match(audit, /reachableVectorRecurrenceIsExact/);
  assert.match(audit, /fractions\.Fraction exact rational arithmetic/);
});

test("locks the monitored exact dominant-mass certificate", async () => {
  const report = JSON.parse(
    await readFile(
      new URL("eighth-order-dominant-mass-exact.json", archiveRoot),
      "utf8",
    ),
  );
  const [stderr, resources] = await Promise.all([
    readFile(new URL("eighth-order-dominant-mass-exact.stderr.log", archiveRoot), "utf8"),
    readFile(new URL("resources.csv", archiveRoot), "utf8"),
  ]);
  assert.equal(report.status, "strict-passed");
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.parameters.states, 1792);
  assert.equal(report.parameters.rootBisections, 192);
  assert.equal(
    report.dominantMass.canonicalIntervalVectorSha256,
    "bf424dfb3c9ce85d1e47d2270b329f6cb4af51e32e665663949d6c53cf6f0e53",
  );
  assert.match(report.dominantRoot.width.decimal, /^4\.0783152924990778/);
  assert.match(report.dominantMass.maximumCoordinateWidth.decimal, /^2\.1768798118304410/);
  assert.equal(
    report.provenance.sourceCommit,
    "b80c0f197e91da00673e1b4fd04f0801fe51be2d",
  );
  assert.match(stderr, /exact recurrence verified degree=33 states=1792/);
  assert.match(stderr, /monitor: finished returncode=0/);
  assert.match(resources, /exited:0/);
});
