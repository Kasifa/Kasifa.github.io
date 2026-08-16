import { pathToFileURL } from "node:url";

const DEFAULT_DELTA = 0.04;

const centers = [
  [1, 0, 0],
  [0, 1, 0],
  [-1, -1, 0],
];

// These central coefficients are divergence free and define a real Fourier
// triad after adjoining their conjugates at the negative wavevectors. The
// corresponding modal transfers are (2,-3,1), so the H^{1/2} weighted
// transfer is sqrt(2)-1.
const centralAmplitudes = [
  [[0, 0], [1, 0], [-1, -1]],
  [[-1, 0], [0, 0], [-1, 0]],
  [[-1, -1], [1, 1], [1, 0]],
];

const addWavevectors = (left, right) =>
  left.map((value, index) => value + right[index]);
const scaleWavevector = (factor, vector) =>
  vector.map((value) => factor * value);
const wavevectorNorm = (vector) => Math.hypot(...vector);
const wavevectorKey = (vector) => vector.join(",");
const conjugate = (value) => [value[0], -value[1]];
const complexAdd = (left, right) => [left[0] + right[0], left[1] + right[1]];
const complexMultiply = (left, right) => [
  left[0] * right[0] - left[1] * right[1],
  left[0] * right[1] + left[1] * right[0],
];
const complexScale = (factor, value) => [factor * value[0], factor * value[1]];
const complexMagnitude = (value) => Math.hypot(...value);
const complexVectorMagnitudeSquared = (vector) =>
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
const complexBilinearDot = (left, right) =>
  left.reduce(
    (sum, value, index) => complexAdd(sum, complexMultiply(value, right[index])),
    [0, 0],
  );

export function centralTriadAudit() {
  const modalTransfers = centers.map((_, index) => {
    const second = (index + 1) % 3;
    const third = (index + 2) % 3;
    const first = complexMultiply(
      realDotComplex(centers[third], centralAmplitudes[second]),
      complexBilinearDot(centralAmplitudes[index], centralAmplitudes[third]),
    );
    const next = complexMultiply(
      realDotComplex(centers[second], centralAmplitudes[third]),
      complexBilinearDot(centralAmplitudes[index], centralAmplitudes[second]),
    );
    return first[1] + next[1];
  });
  return {
    wavevectors: centers,
    amplitudes: centralAmplitudes,
    closure: centers.reduce(addWavevectors, [0, 0, 0]),
    divergenceResiduals: centers.map((center, index) =>
      complexMagnitude(realDotComplex(center, centralAmplitudes[index])),
    ),
    modalTransfers,
    energyTransfer: modalTransfers.reduce((sum, value) => sum + value, 0),
    criticalTransfer: modalTransfers.reduce(
      (sum, value, index) => sum + wavevectorNorm(centers[index]) * value,
      0,
    ),
  };
}

function smoothBump(distanceSquared, delta) {
  const normalized = distanceSquared / delta ** 2;
  if (normalized >= 1) return 0;
  return Math.exp(1 - 1 / (1 - normalized));
}

function projectDivergenceFree(frequency, amplitude) {
  const lengthSquared = frequency.reduce((sum, value) => sum + value ** 2, 0);
  const longitudinal = realDotComplex(frequency, amplitude);
  return amplitude.map((value, index) =>
    complexAdd(value, complexScale(-frequency[index] / lengthSquared, longitudinal)),
  );
}

function profileAt(frequency, delta) {
  const result = [[0, 0], [0, 0], [0, 0]];
  for (let index = 0; index < centers.length; index += 1) {
    for (const sign of [1, -1]) {
      const center = scaleWavevector(sign, centers[index]);
      const displacement = frequency.map((value, axis) => value - center[axis]);
      const bump = smoothBump(
        displacement.reduce((sum, value) => sum + value ** 2, 0),
        delta,
      );
      if (bump === 0) continue;
      const amplitude = sign === 1
        ? centralAmplitudes[index]
        : centralAmplitudes[index].map(conjugate);
      const projected = projectDivergenceFree(frequency, amplitude);
      for (let axis = 0; axis < 3; axis += 1) {
        result[axis] = complexAdd(result[axis], complexScale(bump, projected[axis]));
      }
    }
  }
  return result;
}

export function buildDensePacket(N, delta = DEFAULT_DELTA) {
  if (!Number.isInteger(N) || N < 1) throw new RangeError("N must be a positive integer.");
  if (!(delta > 0 && delta < 1 && (Math.SQRT2 + delta) / (1 - delta) < 2)) {
    throw new RangeError("delta must keep the six spectral lobes inside an annulus of ratio <2.");
  }

  const candidates = new Map();
  const latticeRadius = delta * N;
  for (const center of centers) {
    for (const sign of [1, -1]) {
      const latticeCenter = scaleWavevector(sign * N, center);
      const lower = latticeCenter.map((value) => Math.ceil(value - latticeRadius));
      const upper = latticeCenter.map((value) => Math.floor(value + latticeRadius));
      for (let k0 = lower[0]; k0 <= upper[0]; k0 += 1) {
        for (let k1 = lower[1]; k1 <= upper[1]; k1 += 1) {
          for (let k2 = lower[2]; k2 <= upper[2]; k2 += 1) {
            const wavevector = [k0, k1, k2];
            candidates.set(wavevectorKey(wavevector), wavevector);
          }
        }
      }
    }
  }

  const normalization = N ** -1.5;
  const records = [];
  for (const wavevector of candidates.values()) {
    const frequency = scaleWavevector(1 / N, wavevector);
    const profile = profileAt(frequency, delta);
    if (complexVectorMagnitudeSquared(profile) === 0) continue;
    records.push({
      wavevector,
      coefficient: profile.map((value) => complexScale(normalization, value)),
    });
  }
  records.sort((left, right) =>
    left.wavevector.findIndex((value, index) => value !== right.wavevector[index]) === -1
      ? 0
      : left.wavevector.join(",").localeCompare(right.wavevector.join(",")),
  );
  return records;
}

function kahanAdd(state, value) {
  const corrected = value - state.correction;
  const next = state.sum + corrected;
  state.correction = (next - state.sum) - corrected;
  state.sum = next;
}

export function packetDiagnostics(N, delta = DEFAULT_DELTA) {
  const records = buildDensePacket(N, delta);
  const lookup = new Map(records.map((record) => [wavevectorKey(record.wavevector), record]));
  let minimumFrequency = Infinity;
  let maximumFrequency = 0;
  let divergenceResidual = 0;
  let realityResidual = 0;
  const hHalfSquared = { sum: 0, correction: 0 };
  const hThreeHalfSquared = { sum: 0, correction: 0 };

  for (const record of records) {
    const magnitude = wavevectorNorm(record.wavevector);
    minimumFrequency = Math.min(minimumFrequency, magnitude / N);
    maximumFrequency = Math.max(maximumFrequency, magnitude / N);
    divergenceResidual = Math.max(
      divergenceResidual,
      complexMagnitude(realDotComplex(record.wavevector, record.coefficient)),
    );
    const opposite = lookup.get(wavevectorKey(scaleWavevector(-1, record.wavevector)));
    for (let axis = 0; axis < 3; axis += 1) {
      const difference = complexAdd(
        opposite.coefficient[axis],
        complexScale(-1, conjugate(record.coefficient[axis])),
      );
      realityResidual = Math.max(realityResidual, complexMagnitude(difference));
    }
    const coefficientSize = complexVectorMagnitudeSquared(record.coefficient);
    kahanAdd(hHalfSquared, magnitude * coefficientSize);
    kahanAdd(hThreeHalfSquared, magnitude ** 3 * coefficientSize);
  }

  const trilinear = { sum: 0, correction: 0 };
  const energyTrilinear = { sum: 0, correction: 0 };
  let supportedOrderedPairs = 0;
  for (const left of records) {
    for (const right of records) {
      const output = lookup.get(
        wavevectorKey(addWavevectors(left.wavevector, right.wavevector)),
      );
      if (!output) continue;
      supportedOrderedPairs += 1;
      const derivative = realDotComplex(right.wavevector, left.coefficient);
      const nonlinear = right.coefficient.map((value) =>
        complexMultiply([0, 1], complexMultiply(derivative, value)),
      );
      const energySummand = hermitianDot(output.coefficient, nonlinear)[0];
      const summand = wavevectorNorm(output.wavevector) * energySummand;
      kahanAdd(energyTrilinear, energySummand);
      kahanAdd(trilinear, summand);
    }
  }

  const hHalf = Math.sqrt(hHalfSquared.sum);
  const hThreeHalf = Math.sqrt(hThreeHalfSquared.sum);
  const denominator = hHalf * hThreeHalf ** 2;
  return {
    N,
    delta,
    modeCount: records.length,
    normalizedModeCount: records.length / N ** 3,
    supportedOrderedPairs,
    minimumFrequency,
    maximumFrequency,
    annulusRatio: maximumFrequency / minimumFrequency,
    divergenceResidual,
    realityResidual,
    rescaledHHalf: hHalf / Math.sqrt(N),
    rescaledHThreeHalf: hThreeHalf / N ** 1.5,
    energyTrilinear: energyTrilinear.sum,
    trilinear: trilinear.sum,
    rescaledTrilinear: trilinear.sum / N ** 3.5,
    criticalRatio: Math.abs(trilinear.sum) / denominator,
  };
}

export function runDensePacketAudit(
  scales = [30, 60, 80, 100, 120, 150],
  delta = DEFAULT_DELTA,
) {
  return {
    convention:
      "u_N^(k)=N^(-3/2)a(k/N); T=<Lambda u_N,(u_N dot grad)u_N> on the 2pi torus.",
    centralTriad: centralTriadAudit(),
    profile: {
      delta,
      supportBound: [1 - delta, Math.SQRT2 + delta],
      supportRatioBound: (Math.SQRT2 + delta) / (1 - delta),
      expectedModeDensity: 8 * Math.PI * delta ** 3,
    },
    packets: scales.map((N) => packetDiagnostics(N, delta)),
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.stdout.write(`${JSON.stringify(runDensePacketAudit(), null, 2)}\n`);
}
