import assert from "node:assert/strict";
import test from "node:test";

import {
  dyadicTail,
  runDyadicHelicalAudit,
} from "../research/dyadic-helical-audit.mjs";

test("helical transfer coefficients conserve energy and helicity", () => {
  const audit = runDyadicHelicalAudit();
  assert.equal(audit.allInvariantsPass, true);
});

test("same-high-helicity nonlocal transfer is suppressed on the integer family", () => {
  const audit = runDyadicHelicalAudit();
  const scaled = audit.integerTriads.map(
    (record) => record.sameHighHelicity.scaledRatio,
  );

  for (const record of audit.integerTriads) {
    assert.ok(record.sameHighHelicity.lowToHighRatio < 1 / record.N ** 2);
    assert.ok(record.oppositeHighHelicity.lowToHighRatio > 1);
  }
  assert.ok(Math.min(...scaled) > 0.45);
  assert.ok(Math.max(...scaled) < 0.6);
});

test("dyadic remote tails decay with the claimed shell separation", () => {
  assert.ok(Math.abs(dyadicTail(2, 5) / dyadicTail(2, 4) - 1 / 4) < 1e-14);
  assert.ok(Math.abs(dyadicTail(3, 5) / dyadicTail(3, 4) - 1 / 8) < 1e-14);
});
