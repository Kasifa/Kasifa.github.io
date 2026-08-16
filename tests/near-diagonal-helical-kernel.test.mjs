import assert from "node:assert/strict";
import test from "node:test";

import {
  HELICITY_CLASSES,
  analyticMaxima,
  criticalKernel,
  directGeometricFactor,
  geometricFactorMagnitude,
  gridAudit,
  wavevectorTriangle,
} from "../research/near-diagonal-helical-kernel.mjs";

const magnitude = (vector) => Math.hypot(...vector);
const complexMagnitude = (value) => Math.hypot(...value);

test("closed side-length formula matches the direct helical basis coefficient", () => {
  for (const [x, y] of [[0.5, 1], [0.75, 1.2], [1, 1.7537162153241575]]) {
    const wavevectors = wavevectorTriangle(x, y);
    const magnitudes = wavevectors.map(magnitude);
    for (const { signs } of HELICITY_CLASSES) {
      const direct = complexMagnitude(directGeometricFactor(wavevectors, signs));
      const closed = geometricFactorMagnitude(magnitudes, signs);
      assert.ok(Math.abs(direct - closed) < 2e-15);
    }
  }
});

test("homochiral triads conserve the positive H-half quadratic quantity", () => {
  for (const [x, y] of [[0.5, 1], [0.8, 1.3], [1, 1.7]]) {
    assert.ok(Math.abs(criticalKernel([x, 1, y], [1, 1, 1])) < 1e-15);
  }
});

test("analytic near-diagonal maxima agree with their exact maximizing points", () => {
  const maxima = analyticMaxima();
  assert.ok(Math.abs(maxima.rootPolynomialResidual) < 2e-14);
  for (const { id, signs } of HELICITY_CLASSES) {
    const record = maxima[id];
    const value = criticalKernel([record.point[0], 1, record.point[1]], signs);
    assert.ok(Math.abs(value - record.maximum) < 2e-14, `${id}: ${value} != ${record.maximum}`);
  }
  assert.ok(Math.abs(maxima["++-"].maximum - Math.sqrt(15) / 16) < 1e-15);
  assert.ok(Math.abs(maxima["+-+"].maximum - 0.635456473486601) < 2e-15);
  assert.equal(maxima["+-+"].maximum, maxima["+--"].maximum);
});

test("dense grid lower bounds stay below and approach the analytic maxima", () => {
  const maxima = analyticMaxima();
  const grid = gridAudit(500);
  for (const { id } of HELICITY_CLASSES) {
    assert.ok(grid[id].lowerBound <= maxima[id].maximum + 2e-14);
    assert.ok(maxima[id].maximum - grid[id].lowerBound < 2e-5);
  }
});

test("critical-kernel zero sets have the stated representative checks", () => {
  assert.ok(criticalKernel([1, 1, 1.4], [1, 1, -1]) < 1e-15);
  assert.ok(criticalKernel([1, 1, 1], [1, -1, 1]) < 1e-15);
  assert.ok(criticalKernel([0.7, 1, 1], [1, -1, -1]) < 1e-15);
  assert.ok(criticalKernel([0.7, 1, 1.2], [1, -1, 1]) > 0.1);
});
