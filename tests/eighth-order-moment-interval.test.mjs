import assert from "node:assert/strict";
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

test("documents the rejected binary64 baseline and guarded binary128 route", async () => {
  const [audit, note, prepare, engine] = await Promise.all([
    readFile(auditUrl, "utf8"),
    readFile(noteUrl, "utf8"),
    readFile(prepareUrl, "utf8"),
    readFile(engineUrl, "utf8"),
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
});
