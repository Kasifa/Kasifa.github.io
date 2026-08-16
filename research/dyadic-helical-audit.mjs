import { pathToFileURL } from "node:url";

const tolerance = 1e-12;

function dot(left, right) {
  return left.reduce((sum, value, index) => sum + value * right[index], 0);
}

export function helicalTransferCoefficients(
  magnitudes,
  signs,
) {
  const [K, P, Q] = magnitudes;
  const [sK, sP, sQ] = signs;
  const transfer = [
    sP * P - sQ * Q,
    sQ * Q - sK * K,
    sK * K - sP * P,
  ];
  const helicityWeights = [sK * K, sP * P, sQ * Q];

  return {
    magnitudes,
    signs,
    transfer,
    energyResidual: transfer.reduce((sum, value) => sum + value, 0),
    helicityResidual: dot(helicityWeights, transfer),
  };
}

export function dyadicTail(exponent, separation) {
  const firstWeight = 2 ** (-exponent * separation);
  return firstWeight / Math.sqrt(1 - 2 ** (-2 * exponent));
}

function actualIntegerTriadAudit(N) {
  // k=(1,0,0), p=(0,N,0), q=(-1,-N,0).
  const magnitudes = [1, N, Math.sqrt(N ** 2 + 1)];
  const sameHighHelicity = helicalTransferCoefficients(
    magnitudes,
    [1, 1, 1],
  );
  const oppositeHighHelicity = helicalTransferCoefficients(
    magnitudes,
    [1, 1, -1],
  );
  const highScale = (transfer) =>
    Math.max(Math.abs(transfer[1]), Math.abs(transfer[2]));

  return {
    N,
    magnitudes,
    sameHighHelicity: {
      ...sameHighHelicity,
      lowToHighRatio:
        Math.abs(sameHighHelicity.transfer[0]) /
        highScale(sameHighHelicity.transfer),
      scaledRatio: N ** 2 *
        Math.abs(sameHighHelicity.transfer[0]) /
        highScale(sameHighHelicity.transfer),
    },
    oppositeHighHelicity: {
      ...oppositeHighHelicity,
      lowToHighRatio:
        Math.abs(oppositeHighHelicity.transfer[0]) /
        highScale(oppositeHighHelicity.transfer),
    },
  };
}

export function runDyadicHelicalAudit() {
  const integerTriads = [8, 16, 32, 64, 128].map(actualIntegerTriadAudit);
  const separations = [2, 4, 6, 8].map((M) => ({
    M,
    lowHighL2Tail: dyadicTail(2, M),
    highHighToLowL2Tail: dyadicTail(3, M),
  }));

  const allInvariantsPass = integerTriads.every((record) =>
    [record.sameHighHelicity, record.oppositeHighHelicity].every(
      ({ energyResidual, helicityResidual }) =>
        Math.abs(energyResidual) < tolerance &&
        Math.abs(helicityResidual) < tolerance,
    ),
  );

  return {
    convention:
      "Transfer triples are the common phase/geometric scalar times the listed coefficients.",
    integerTriads,
    separations,
    allInvariantsPass,
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.stdout.write(`${JSON.stringify(runDyadicHelicalAudit(), null, 2)}\n`);
}
