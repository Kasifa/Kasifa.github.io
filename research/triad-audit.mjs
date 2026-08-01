import { pathToFileURL } from "node:url";

const add = (left, right) => left.map((value, index) => value + right[index]);
const scale = (factor, vector) => vector.map((value) => factor * value);
const realDotComplex = (real, complex) =>
  complex.reduce(
    (sum, value, index) => [
      sum[0] + real[index] * value[0],
      sum[1] + real[index] * value[1],
    ],
    [0, 0],
  );
const complexBilinearDot = (left, right) =>
  left.reduce(
    (sum, value, index) => [
      sum[0] + value[0] * right[index][0] - value[1] * right[index][1],
      sum[1] + value[0] * right[index][1] + value[1] * right[index][0],
    ],
    [0, 0],
  );
const multiply = (left, right) => [
  left[0] * right[0] - left[1] * right[1],
  left[0] * right[1] + left[1] * right[0],
];
const norm = (vector) => Math.hypot(...vector);
const vectorKey = (vector) => vector.join(",");

const wavevectors = [
  [1, 0, 0],
  [0, 2, 0],
  [-1, -2, 0],
];

// Complex Fourier coefficients. The coefficient at -k is the conjugate of
// the coefficient at k, so these data define a real-valued velocity field.
const coefficients = [
  [
    [0, 0],
    [1, 0],
    [0, 0],
  ],
  [
    [1, 0],
    [0, 0],
    [0, 0],
  ],
  [
    [0, 2],
    [0, -1],
    [0, 0],
  ],
];

function modalTransfer(index) {
  const second = (index + 1) % 3;
  const third = (index + 2) % 3;
  const firstTerm = multiply(
    realDotComplex(wavevectors[third], coefficients[second]),
    complexBilinearDot(coefficients[index], coefficients[third]),
  );
  const secondTerm = multiply(
    realDotComplex(wavevectors[second], coefficients[third]),
    complexBilinearDot(coefficients[index], coefficients[second]),
  );

  return firstTerm[1] + secondTerm[1];
}

function mixedShellResonances(base, shellScales) {
  const records = [];
  for (const [shell, shellScale] of shellScales.entries()) {
    for (const vector of base) {
      records.push({ shell, vector: scale(shellScale, vector) });
      records.push({ shell, vector: scale(-shellScale, vector) });
    }
  }

  const lookup = new Map(records.map((record) => [vectorKey(record.vector), record]));
  const mixed = [];
  for (const left of records) {
    for (const right of records) {
      const output = lookup.get(vectorKey(add(left.vector, right.vector)));
      if (
        output &&
        (left.shell !== right.shell ||
          right.shell !== output.shell ||
          output.shell !== left.shell)
      ) {
        mixed.push({
          left: left.vector,
          right: right.vector,
          output: output.vector,
        });
      }
    }
  }
  return mixed;
}

export function runTriadAudit() {
  const divergenceResiduals = wavevectors.map((wavevector, index) =>
    realDotComplex(wavevector, coefficients[index]),
  );
  const closure = wavevectors
    .reduce((sum, wavevector) => add(sum, wavevector), [0, 0, 0])
    .map(Math.abs);
  const transfers = wavevectors.map((_, index) => modalTransfer(index));
  const energyTransfer = transfers.reduce((sum, value) => sum + value, 0);
  const hHalfTransfer = transfers.reduce(
    (sum, value, index) => sum + norm(wavevectors[index]) * value,
    0,
  );
  const separatedShellScales = [1, 8, 64];
  const crossShellResonances = mixedShellResonances(
    wavevectors,
    separatedShellScales,
  );

  return {
    wavevectors,
    transfers,
    energyTransfer,
    hHalfTransfer,
    expectedHHalfTransfer: 1 - 8 + 3 * Math.sqrt(5),
    closure,
    divergenceResiduals,
    separatedShellScales,
    crossShellResonances,
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.stdout.write(`${JSON.stringify(runTriadAudit(), null, 2)}\n`);
}
