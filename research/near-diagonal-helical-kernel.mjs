import { pathToFileURL } from "node:url";

const add = (left, right) => left.map((value, index) => value + right[index]);
const scale = (factor, vector) => vector.map((value) => factor * value);
const cross = (left, right) => [
  left[1] * right[2] - left[2] * right[1],
  left[2] * right[0] - left[0] * right[2],
  left[0] * right[1] - left[1] * right[0],
];
const norm = (vector) => Math.hypot(...vector);
const unit = (vector) => scale(1 / norm(vector), vector);

const complexMultiply = (left, right) => [
  left[0] * right[0] - left[1] * right[1],
  left[0] * right[1] + left[1] * right[0],
];
const complexAdd = (left, right) => [left[0] + right[0], left[1] + right[1]];
const complexScale = (factor, value) => [factor * value[0], factor * value[1]];
const complexMagnitude = (value) => Math.hypot(...value);
const complexDot = (left, right) =>
  left.reduce(
    (sum, value, index) => complexAdd(sum, complexMultiply(value, right[index])),
    [0, 0],
  );
const complexCross = (left, right) => [
  complexAdd(
    complexMultiply(left[1], right[2]),
    complexScale(-1, complexMultiply(left[2], right[1])),
  ),
  complexAdd(
    complexMultiply(left[2], right[0]),
    complexScale(-1, complexMultiply(left[0], right[2])),
  ),
  complexAdd(
    complexMultiply(left[0], right[1]),
    complexScale(-1, complexMultiply(left[1], right[0])),
  ),
];

export const HELICITY_CLASSES = [
  { id: "+++", signs: [1, 1, 1] },
  { id: "++-", signs: [1, 1, -1] },
  { id: "+-+", signs: [1, -1, 1] },
  { id: "+--", signs: [1, -1, -1] },
];

export function triangleArea(K, P, Q) {
  const product = (K + P + Q) * (-K + P + Q) * (K - P + Q) * (K + P - Q);
  return 0.25 * Math.sqrt(Math.max(0, product));
}

export function geometricFactorMagnitude(magnitudes, signs) {
  const [K, P, Q] = magnitudes;
  const [sK, sP, sQ] = signs;
  return (
    (triangleArea(K, P, Q) / (K * P * Q)) *
    Math.abs(sK * K + sP * P + sQ * Q)
  );
}

export function criticalWeight(magnitudes, signs) {
  const [K, P, Q] = magnitudes;
  const [sK, sP, sQ] = signs;
  return (
    K * (sP * P - sQ * Q) +
    P * (sQ * Q - sK * K) +
    Q * (sK * K - sP * P)
  );
}

export function criticalKernel(magnitudes, signs) {
  return geometricFactorMagnitude(magnitudes, signs) * Math.abs(criticalWeight(magnitudes, signs));
}

function helicalBasisConjugate(wavevector, sign, normal) {
  const transverse = cross(normal, unit(wavevector));
  return transverse.map((value, index) => [value, -sign * normal[index]]);
}

export function directGeometricFactor(wavevectors, signs) {
  const [k, p, q] = wavevectors;
  const normal = unit(cross(p, q));
  const hK = helicalBasisConjugate(k, signs[0], normal);
  const hP = helicalBasisConjugate(p, signs[1], normal);
  const hQ = helicalBasisConjugate(q, signs[2], normal);
  return complexScale(-0.5, complexDot(complexCross(hP, hQ), hK));
}

export function wavevectorTriangle(x, y) {
  if (!(x > 0 && y >= 1 && y < 1 + x)) {
    throw new RangeError("Require x>0 and 1<=y<1+x for a nondegenerate ordered triangle.");
  }
  const cosine = (y ** 2 - x ** 2 - 1) / (2 * x);
  const sine = Math.sqrt(Math.max(0, 1 - cosine ** 2));
  const k = [x * cosine, x * sine, 0];
  const p = [1, 0, 0];
  const q = scale(-1, add(k, p));
  return [k, p, q];
}

export function maximizingRoot(iterations = 100) {
  let left = 1;
  let right = 2;
  const polynomial = (value) => 3 * value ** 3 - 2 * value ** 2 - 8 * value + 4;
  for (let index = 0; index < iterations; index += 1) {
    const middle = (left + right) / 2;
    if (polynomial(middle) > 0) right = middle;
    else left = middle;
  }
  return (left + right) / 2;
}

export function analyticMaxima() {
  const root = maximizingRoot();
  const sharedMaximum = 0.5 * root * (root - 1) * Math.sqrt(4 - root ** 2);
  return {
    "+++": { maximum: 0, point: [1, 1], zeroSet: "entire domain" },
    "++-": {
      maximum: Math.sqrt(15) / 16,
      point: [0.5, 1],
      zeroSet: "x=1 or y=1+x",
    },
    "+-+": {
      maximum: sharedMaximum,
      point: [1, root],
      zeroSet: "(x,y)=(1,1) or y=1+x",
    },
    "+--": {
      maximum: sharedMaximum,
      point: [1, root],
      zeroSet: "y=1 or y=1+x",
    },
    root,
    rootPolynomialResidual: 3 * root ** 3 - 2 * root ** 2 - 8 * root + 4,
  };
}

export function gridAudit(resolution = 600) {
  const records = Object.fromEntries(
    HELICITY_CLASSES.map(({ id }) => [id, { lowerBound: -Infinity, point: null }]),
  );
  for (let i = 0; i <= resolution; i += 1) {
    const x = 0.5 + (0.5 * i) / resolution;
    for (let j = 0; j <= resolution; j += 1) {
      const y = 1 + (x * j) / resolution;
      for (const { id, signs } of HELICITY_CLASSES) {
        const value = criticalKernel([x, 1, y], signs);
        if (value > records[id].lowerBound) records[id] = { lowerBound: value, point: [x, y] };
      }
    }
  }
  return records;
}

export function runNearDiagonalAudit() {
  const maxima = analyticMaxima();
  const directChecks = [
    [0.5, 1],
    [0.75, 1.2],
    [1, maxima.root],
  ].flatMap(([x, y]) => {
    const wavevectors = wavevectorTriangle(x, y);
    const magnitudes = wavevectors.map(norm);
    return HELICITY_CLASSES.map(({ id, signs }) => {
      const direct = directGeometricFactor(wavevectors, signs);
      const closed = geometricFactorMagnitude(magnitudes, signs);
      return {
        class: id,
        point: [x, y],
        closureResidual: norm(wavevectors.reduce(add, [0, 0, 0])),
        directMagnitude: complexMagnitude(direct),
        closedMagnitude: closed,
        formulaResidual: Math.abs(complexMagnitude(direct) - closed),
      };
    });
  });

  return {
    domain: "P=1, 1/2<=x=K/P<=1, 1<=y=Q/P<=1+x",
    convention: "|g|=Delta/(KPQ)|s_K K+s_P P+s_Q Q|; critical kernel=|g W|.",
    maxima,
    grid: gridAudit(),
    directChecks,
    proofCertificates: {
      classA:
        "For fixed x, the ++- squared kernel increases with t=x+1-y; at y=1 it decreases for x>=1/2.",
      classB:
        "With a=x+1-y, b=x+y-1, c=1+y-x and a+c=2, d/db log[b^3(b+2)/((a+b)^2(b+c)^2)]>0.",
      classC:
        "For fixed a, d/db log[b(b+2)(b-a)^2/(b+c)^2]>0; hence b=c and x=1.",
      oneVariable:
        "At x=1, maximize y(y-1)sqrt(4-y^2)/2; its interior critical point solves 3y^3-2y^2-8y+4=0.",
    },
  };
}

if (process.argv[1] && import.meta.url === pathToFileURL(process.argv[1]).href) {
  process.stdout.write(`${JSON.stringify(runNearDiagonalAudit(), null, 2)}\n`);
}
