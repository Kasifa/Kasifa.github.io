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

test("documents the exact all-multiindex derivative certificate", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);
  assert.match(note, /4368/);
  assert.match(note, /35/);
  assert.match(note, /2\.567\\times10\^\{-6\}/);
  assert.match(note, /not establish global regularity/);
  assert.match(audit, /GMP rational arithmetic/);
  assert.match(audit, /allDerivativeMultiindicesArePresent/);
  assert.match(audit, /exactVectorSha256/);
});
