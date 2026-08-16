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
const vectorMagnitudeSquared = (vector) =>
  vector.reduce((sum, value) => sum + value[0] ** 2 + value[1] ** 2, 0);
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

function projectDivergenceFree(wavevector, coefficient) {
  const lengthSquared = wavevector.reduce((sum, value) => sum + value ** 2, 0);
  if (lengthSquared === 0) return coefficient.map(() => [0, 0]);
  const longitudinal = realDotComplex(wavevector, coefficient);
  return coefficient.map((value, axis) =>
    complexAdd(value, complexScale(-wavevector[axis] / lengthSquared, longitudinal)),
  );
}

function addToCoefficientMap(map, wavevector, contribution) {
  const key = wavevectorKey(wavevector);
  const record = map.get(key);
  if (record) {
    for (let axis = 0; axis < 3; axis += 1) {
      record.coefficient[axis] = complexAdd(record.coefficient[axis], contribution[axis]);
    }
    return;
  }
  map.set(key, {
    wavevector,
    coefficient: contribution.map((value) => [...value]),
  });
}

// Analytic large-root optimizer in the symmetric 2D3C subfamily, rescaled to
// the H^(1/2) energy of the original central amplitudes. It has the same
// central critical transfer as the original profile.
const fixedHorizontalAmplitude = 0.4199676960322196;
const fixedVerticalAmplitude = 2.383859931814685;
const fixedClosingAmplitude = 0.4994285721928156;
export const fixedInjectionCandidateAmplitudes = [
  [
    [0, 0],
    [fixedHorizontalAmplitude, 0],
    [-fixedVerticalAmplitude, 0],
  ],
  [
    [fixedHorizontalAmplitude, 0],
    [0, 0],
    [-fixedVerticalAmplitude, 0],
  ],
  [
    [0, 0],
    [0, 0],
    [0, -fixedClosingAmplitude],
  ],
];

export function packetLeakageDiagnostics(
  N,
  delta = 0.04,
  amplitudes = undefined,
) {
  const packet = buildDensePacket(N, delta, amplitudes);
  const support = new Map(packet.map((record) => [wavevectorKey(record.wavevector), record]));
  const nonlinearRaw = new Map();

  for (const left of packet) {
    for (const right of packet) {
      const output = addWavevectors(left.wavevector, right.wavevector);
      if (output.every((value) => value === 0)) continue;
      const derivative = realDotComplex(right.wavevector, left.coefficient);
      const contribution = right.coefficient.map((value) =>
        complexMultiply([0, 1], complexMultiply(derivative, value)),
      );
      addToCoefficientMap(nonlinearRaw, output, contribution);
    }
  }

  let inputHHalfSquared = 0;
  for (const record of packet) {
    inputHHalfSquared +=
      wavevectorNorm(record.wavevector) * vectorMagnitudeSquared(record.coefficient);
  }

  let insideHHalfSquared = 0;
  let outsideHHalfSquared = 0;
  let insideModeCount = 0;
  let outsideModeCount = 0;
  let transfer = 0;
  let l2Pairing = 0;
  let maximumDivergenceResidual = 0;
  const activeThreshold = 1e-28;

  for (const raw of nonlinearRaw.values()) {
    const projected = projectDivergenceFree(raw.wavevector, raw.coefficient);
    const coefficientSize = vectorMagnitudeSquared(projected);
    if (coefficientSize <= activeThreshold) continue;
    const magnitude = wavevectorNorm(raw.wavevector);
    const weightedSize = magnitude * coefficientSize;
    const input = support.get(wavevectorKey(raw.wavevector));
    maximumDivergenceResidual = Math.max(
      maximumDivergenceResidual,
      complexMagnitude(realDotComplex(raw.wavevector, projected)),
    );
    if (input) {
      insideModeCount += 1;
      insideHHalfSquared += weightedSize;
      transfer += magnitude * hermitianDot(input.coefficient, projected)[0];
      l2Pairing += hermitianDot(input.coefficient, projected)[0];
    } else {
      outsideModeCount += 1;
      outsideHHalfSquared += weightedSize;
    }
  }

  const inputHHalf = Math.sqrt(inputHHalfSquared);
  const insideHHalf = Math.sqrt(insideHHalfSquared);
  const outsideHHalf = Math.sqrt(outsideHHalfSquared);
  const totalHHalf = Math.hypot(insideHHalf, outsideHHalf);
  const absoluteTransfer = Math.abs(transfer);
  return {
    N,
    delta,
    inputModeCount: packet.length,
    nonlinearInsideModeCount: insideModeCount,
    nonlinearOutsideModeCount: outsideModeCount,
    maximumDivergenceResidual,
    l2Pairing,
    transfer,
    rescaledTransfer: transfer / N ** 3.5,
    rescaledInputHHalf: inputHHalf / Math.sqrt(N),
    rescaledInsideHHalf: insideHHalf / N ** 3,
    rescaledOutsideHHalf: outsideHHalf / N ** 3,
    leakageFraction: outsideHHalf / totalHHalf,
    closureRatio: outsideHHalf / insideHHalf,
    injectionEfficiency: absoluteTransfer / (inputHHalf * insideHHalf),
    escapePerInjection: (inputHHalf * outsideHHalf) / absoluteTransfer,
  };
}

export function runPacketLeakageAudit(
  scales = [30, 60, 80, 100, 120],
  delta = 0.04,
) {
  return {
    convention:
      "B(u,u)=P[(u dot grad)u]; leakage is the homogeneous H^(1/2) norm of P_(S^c)B for the original packet support S.",
    original: scales.map((N) => packetLeakageDiagnostics(N, delta)),
    fixedInjectionCandidate: scales.map((N) =>
      packetLeakageDiagnostics(N, delta, fixedInjectionCandidateAmplitudes)),
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.stdout.write(`${JSON.stringify(runPacketLeakageAudit(), null, 2)}\n`);
}
