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
