import { pathToFileURL } from "node:url";

import { buildDensePacket } from "./dense-critical-packet.mjs";

const addWavevectors = (left, right) =>
  left.map((value, index) => value + right[index]);
const wavevectorKey = (vector) => vector.join(",");
const wavevectorNorm = (vector) => Math.hypot(...vector);
const conjugate = (value) => [value[0], -value[1]];
const complexAdd = (left, right) => [left[0] + right[0], left[1] + right[1]];
const complexMultiply = (left, right) => [
  left[0] * right[0] - left[1] * right[1],
  left[0] * right[1] + left[1] * right[0],
];
const complexScale = (factor, value) => [factor * value[0], factor * value[1]];
const complexMagnitude = (value) => Math.hypot(...value);
const realDotComplex = (real, complex) =>
  complex.reduce(
    (sum, value, index) => complexAdd(sum, complexScale(real[index], value)),
    [0, 0],
  );
const hermitianDot = (left, right) =>
  left.reduce(
    (sum, value, index) =>
      complexAdd(sum, complexMultiply(conjugate(value), right[index])),
    [0, 0],
  );
const vectorMagnitudeSquared = (vector) =>
  vector.reduce((sum, value) => sum + value[0] ** 2 + value[1] ** 2, 0);

function kahanAdd(state, value) {
  const corrected = value - state.correction;
  const next = state.sum + corrected;
  state.correction = (next - state.sum) - corrected;
  state.sum = next;
}

function preparePacket(N, delta) {
  const records = buildDensePacket(N, delta).map((record) => ({
    ...record,
    magnitude: wavevectorNorm(record.wavevector),
    magnitudeSquared: record.wavevector.reduce(
      (sum, value) => sum + value ** 2,
      0,
    ),
  }));
  const lookup = new Map(records.map((record) => [wavevectorKey(record.wavevector), record]));
  const triads = [];

  for (const left of records) {
    for (const right of records) {
      const output = lookup.get(wavevectorKey(addWavevectors(left.wavevector, right.wavevector)));
      if (!output) continue;
      const derivative = realDotComplex(right.wavevector, left.coefficient);
      const nonlinear = right.coefficient.map((value) =>
        complexMultiply([0, 1], complexMultiply(derivative, value)),
      );
      const innerProduct = hermitianDot(output.coefficient, nonlinear);
      const weighted = complexScale(output.magnitude, innerProduct);
      triads.push({
        signedContribution: weighted[0],
        absoluteContribution: complexMagnitude(weighted),
        scaledHeatRate:
          (left.magnitudeSquared + right.magnitudeSquared + output.magnitudeSquared) /
          N ** 2,
      });
    }
  }

  return { records, triads };
}

function heatSnapshot(packet, N, tau, viscosity) {
  const hHalfSquared = { sum: 0, correction: 0 };
  const hThreeHalfSquared = { sum: 0, correction: 0 };
  for (const record of packet.records) {
    const heatSquared = Math.exp(
      (-2 * viscosity * tau * record.magnitudeSquared) / N ** 2,
    );
    const coefficientSize = vectorMagnitudeSquared(record.coefficient) * heatSquared;
    kahanAdd(hHalfSquared, record.magnitude * coefficientSize);
    kahanAdd(hThreeHalfSquared, record.magnitude ** 3 * coefficientSize);
  }

  const trilinear = { sum: 0, correction: 0 };
  for (const triad of packet.triads) {
    const heat = Math.exp(-viscosity * tau * triad.scaledHeatRate);
    kahanAdd(trilinear, heat * triad.signedContribution);
  }
  const hHalf = Math.sqrt(hHalfSquared.sum);
  const hThreeHalf = Math.sqrt(hThreeHalfSquared.sum);
  return {
    tau,
    rescaledHHalf: hHalf / Math.sqrt(N),
    rescaledHThreeHalf: hThreeHalf / N ** 1.5,
    rescaledTrilinear: trilinear.sum / N ** 3.5,
    criticalRatio: Math.abs(trilinear.sum) / (hHalf * hThreeHalf ** 2),
    trilinear: trilinear.sum,
  };
}

export function heatFlowDiagnostics(
  N,
  delta = 0.04,
  times = [0, 0.05, 0.1, 0.25, 0.5, 1, 2],
  viscosity = 1,
) {
  if (!(viscosity > 0)) throw new RangeError("viscosity must be positive.");
  if (!times.every((tau) => tau >= 0)) throw new RangeError("heat times must be nonnegative.");

  const packet = preparePacket(N, delta);
  const snapshots = times.map((tau) => heatSnapshot(packet, N, tau, viscosity));
  const initial = snapshots.find((snapshot) => snapshot.tau === 0) ??
    heatSnapshot(packet, N, 0, viscosity);
  const absoluteMajorant = packet.triads.reduce(
    (sum, triad) => sum + triad.absoluteContribution,
    0,
  );
  const heatLipschitzMajorant = packet.triads.reduce(
    (sum, triad) => sum + triad.scaledHeatRate * triad.absoluteContribution,
    0,
  );
  const guaranteedHalfLife =
    Math.abs(initial.trilinear) / (2 * viscosity * heatLipschitzMajorant);
  const criticalAmplitude =
    initial.trilinear < 0
      ? (viscosity * Math.sqrt(N) * (initial.rescaledHThreeHalf * N ** 1.5) ** 2) /
        -initial.trilinear
      : null;

  return {
    N,
    delta,
    viscosity,
    modeCount: packet.records.length,
    supportedOrderedPairs: packet.triads.length,
    rescaledAbsoluteMajorant: absoluteMajorant / N ** 3.5,
    rescaledHeatLipschitzMajorant: heatLipschitzMajorant / N ** 3.5,
    guaranteedHalfLife,
    criticalAmplitude,
    criticalNormAtThreshold:
      criticalAmplitude === null
        ? null
        : criticalAmplitude * initial.rescaledHHalf,
    snapshots: snapshots.map((snapshot) => ({
      ...snapshot,
      transferRetention: snapshot.trilinear / initial.trilinear,
    })),
  };
}

export function runHeatFlowAudit(
  scales = [60, 80, 100, 120],
  delta = 0.04,
  times = [0, 0.05, 0.1, 0.25, 0.5, 1, 2],
  viscosity = 1,
) {
  return {
    convention:
      "a_tau(k/N)=exp(-nu*tau*|k/N|^2)a(k/N), with tau=N^2 t; nu=viscosity.",
    scales: scales.map((N) => heatFlowDiagnostics(N, delta, times, viscosity)),
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.stdout.write(`${JSON.stringify(runHeatFlowAudit(), null, 2)}\n`);
}
