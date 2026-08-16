import assert from "node:assert/strict";
import test from "node:test";

import {
  buildDensePacket,
  packetDiagnostics,
  runDensePacketAudit,
} from "../research/dense-critical-packet.mjs";

test("the central near-diagonal triad has nonzero critical transfer", () => {
  const { centralTriad } = runDensePacketAudit([]);
  const closure = centralTriad.wavevectors.reduce(
    (sum, vector) => sum.map((value, axis) => value + vector[axis]),
    [0, 0, 0],
  );

  assert.deepEqual(closure, [0, 0, 0]);
  assert.deepEqual(centralTriad.closure, [0, 0, 0]);
  assert.ok(centralTriad.divergenceResiduals.every((value) => value === 0));
  assert.deepEqual(centralTriad.modalTransfers, [2, -3, 1]);
  assert.equal(centralTriad.energyTransfer, 0);
  assert.ok(Math.abs(centralTriad.criticalTransfer - (Math.SQRT2 - 1)) < 1e-15);
});

test("sampled packets are real, divergence free, and purely near diagonal", () => {
  const record = packetDiagnostics(80);

  assert.ok(record.modeCount > 800);
  assert.ok(record.realityResidual < 1e-15);
  assert.ok(record.divergenceResidual < 1e-14);
  assert.ok(record.minimumFrequency > 0.95);
  assert.ok(record.maximumFrequency < 1.46);
  assert.ok(record.annulusRatio < 2);
  assert.ok(Math.abs(record.energyTrilinear) < 1e-18);
});

test("the number of active Fourier modes has cubic lattice density", () => {
  const { profile } = runDensePacketAudit([]);
  const record = packetDiagnostics(120);

  assert.ok(record.modeCount > 2700);
  assert.ok(
    Math.abs(record.normalizedModeCount - profile.expectedModeDensity) /
      profile.expectedModeDensity < 0.02,
  );
});

test("critical norm and trilinear rescalings stabilize without an N-decay", () => {
  const lower = packetDiagnostics(80);
  const upper = packetDiagnostics(120);
  const relativeDifference = (left, right) => Math.abs(left / right - 1);

  assert.ok(relativeDifference(lower.rescaledHHalf, upper.rescaledHHalf) < 0.01);
  assert.ok(relativeDifference(lower.rescaledHThreeHalf, upper.rescaledHThreeHalf) < 0.01);
  assert.ok(relativeDifference(lower.rescaledTrilinear, upper.rescaledTrilinear) < 0.03);
  assert.ok(relativeDifference(lower.criticalRatio, upper.criticalRatio) < 0.03);
  assert.ok(upper.criticalRatio > 2.8e-5);
});

test("dense packet construction has exact conjugate lattice support", () => {
  const packet = buildDensePacket(40);
  const keys = new Set(packet.map(({ wavevector }) => wavevector.join(",")));

  for (const { wavevector } of packet) {
    assert.ok(keys.has(wavevector.map((value) => -value).join(",")));
  }
});
