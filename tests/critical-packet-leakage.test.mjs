import assert from "node:assert/strict";
import test from "node:test";

import { packetDiagnostics } from "../research/dense-critical-packet.mjs";
import {
  fixedInjectionCandidateAmplitudes,
  packetLeakageDiagnostics,
} from "../research/critical-packet-leakage.mjs";

test("leakage convolution reproduces the static critical transfer", () => {
  const staticPacket = packetDiagnostics(30, 0.04);
  const leakage = packetLeakageDiagnostics(30, 0.04);
  assert.ok(Math.abs(leakage.transfer - staticPacket.trilinear) < 1e-15);
  assert.ok(Math.abs(leakage.l2Pairing) < 1e-15);
  assert.ok(leakage.maximumDivergenceResidual < 1e-14);
});

test("the packet nonlinear vector field has a nonzero normal component", () => {
  const leakage = packetLeakageDiagnostics(30, 0.04);
  assert.ok(leakage.nonlinearOutsideModeCount > 0);
  assert.ok(leakage.rescaledOutsideHHalf > 0);
  assert.ok(leakage.leakageFraction > 0.5);
  assert.ok(leakage.escapePerInjection > 1);
});

test("dimensionless leakage diagnostics remain bounded across sampled scales", () => {
  const diagnostics = [30, 60, 80].map((N) => packetLeakageDiagnostics(N, 0.04));
  for (const result of diagnostics) {
    assert.ok(result.leakageFraction > 0.5 && result.leakageFraction < 1);
    assert.ok(Number.isFinite(result.closureRatio));
    assert.ok(Number.isFinite(result.injectionEfficiency));
    assert.ok(Number.isFinite(result.escapePerInjection));
  }
  const ratio = diagnostics.at(-1).rescaledOutsideHHalf /
    diagnostics.at(-2).rescaledOutsideHHalf;
  assert.ok(ratio > 0.5 && ratio < 2);
});

test("the fixed-injection variational candidate improves dense-packet escape", () => {
  const original = packetLeakageDiagnostics(60, 0.04);
  const candidate = packetLeakageDiagnostics(
    60,
    0.04,
    fixedInjectionCandidateAmplitudes,
  );
  assert.ok(Math.abs(candidate.rescaledTransfer) > 0);
  assert.ok(candidate.escapePerInjection < original.escapePerInjection / 5);
  assert.ok(candidate.leakageFraction < original.leakageFraction);
});
