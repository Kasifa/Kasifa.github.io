import assert from "node:assert/strict";
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
