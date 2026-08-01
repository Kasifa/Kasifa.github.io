import assert from "node:assert/strict";
import test from "node:test";

import { runTriadAudit } from "../research/triad-audit.mjs";

const tolerance = 1e-12;

test("the explicit Fourier triad is closed and divergence free", () => {
  const audit = runTriadAudit();

  assert.ok(audit.closure.every((value) => value === 0));
  for (const residual of audit.divergenceResiduals) {
    assert.ok(Math.abs(residual[0]) < tolerance);
    assert.ok(Math.abs(residual[1]) < tolerance);
  }
});

test("the triad conserves L2 energy but not H-half energy", () => {
  const audit = runTriadAudit();

  assert.deepEqual(audit.transfers, [1, -4, 3]);
  assert.ok(Math.abs(audit.energyTransfer) < tolerance);
  assert.ok(
    Math.abs(audit.hHalfTransfer - audit.expectedHHalfTransfer) < tolerance,
  );
  assert.ok(Math.abs(audit.hHalfTransfer) > 0.1);
});

test("widely separated copies have no cross-shell supported resonance", () => {
  const audit = runTriadAudit();

  assert.deepEqual(audit.separatedShellScales, [1, 8, 64]);
  assert.deepEqual(audit.crossShellResonances, []);
});
