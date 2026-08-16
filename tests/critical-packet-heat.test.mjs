import assert from "node:assert/strict";
import test from "node:test";

import { packetDiagnostics } from "../research/dense-critical-packet.mjs";
import { heatFlowDiagnostics } from "../research/critical-packet-heat.mjs";

test("heat audit agrees with the static packet at tau zero", () => {
  const staticPacket = packetDiagnostics(60, 0.04);
  const heat = heatFlowDiagnostics(60, 0.04, [0, 0.1]);
  const initial = heat.snapshots[0];

  assert.ok(Math.abs(initial.rescaledHHalf - staticPacket.rescaledHHalf) < 1e-14);
  assert.ok(
    Math.abs(initial.rescaledHThreeHalf - staticPacket.rescaledHThreeHalf) < 1e-14,
  );
  assert.ok(
    Math.abs(initial.rescaledTrilinear - staticPacket.rescaledTrilinear) < 1e-18,
  );
  assert.ok(Math.abs(initial.criticalRatio - staticPacket.criticalRatio) < 1e-14);
});

test("the explicit heat-flow sign interval is positive and verified directly", () => {
  const audit = heatFlowDiagnostics(80, 0.04, [0]);
  assert.ok(audit.guaranteedHalfLife > 0);
  const checked = heatFlowDiagnostics(
    80,
    0.04,
    [0, audit.guaranteedHalfLife],
  );
  assert.ok(checked.snapshots[1].transferRetention >= 0.5 - 1e-12);
  assert.ok(checked.criticalAmplitude > 8e5);
  assert.ok(checked.criticalAmplitude < 1.3e6);
  assert.ok(checked.criticalNormAtThreshold > 3e4);
  assert.ok(checked.criticalNormAtThreshold < 4e4);
});

test("the sampled heat flow keeps the transfer sign on the reported interval", () => {
  const audit = heatFlowDiagnostics(100, 0.04);
  for (const snapshot of audit.snapshots) {
    assert.ok(snapshot.transferRetention > 0);
    assert.ok(snapshot.criticalRatio > 0);
  }
});
