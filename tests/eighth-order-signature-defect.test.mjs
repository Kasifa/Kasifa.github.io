import assert from "node:assert/strict";
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

test("states the strict corrected heat sign and its all-order boundary", async () => {
  const [note, prepare, engine] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(prepareUrl, "utf8"),
    readFile(engineUrl, "utf8"),
  ]);
  assert.match(note, /-2\.87321129703704757\\times10\^\{-9\}/);
  assert.match(note, /product of the four entrywise-absolute/);
  assert.match(note, /does not control all Picard orders/);
  assert.match(note, /does not solve the Navier--Stokes Millennium problem/);
  assert.match(prepare, /EXPECTED_CLASSES = 44_514/);
  assert.match(prepare, /absolute-cycle\.data\.i32/);
  assert.match(prepare, /derivative-upper\.f64/);
  assert.match(engine, /correctedDominantHeatIntervalIsStrictlyNegative/);
  assert.match(engine, /CARRY_WEIGHTS/);
  assert.match(engine, /absolute-cycle\.indptr\.i64/);
});
