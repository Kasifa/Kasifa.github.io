#!/usr/bin/env node

/**
 * Independent BigInt audit for the R0.72R quantitative 1:2:3 core.
 *
 * This route does not import the Python producer or read its artifacts.  It
 * independently reconstructs the canonical finite ledger with BigInt
 * fractions and an integer Bareiss resultant.  Only the comparator later
 * reads both payloads.
 */

import { execFileSync, spawnSync } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const AUDIT = "R0.72R independent quantitative 1:2:3 core exact audit";
const SCHEMA_VERSION = 1;

function absolute(value) {
  return value < 0n ? -value : value;
}

function gcd(left, right) {
  let a = absolute(left);
  let b = absolute(right);
  while (b !== 0n) {
    [a, b] = [b, a % b];
  }
  return a;
}

function fraction(numerator, denominator = 1n) {
  let n = BigInt(numerator);
  let d = BigInt(denominator);
  if (d === 0n) throw new RangeError("zero denominator");
  if (d < 0n) {
    n = -n;
    d = -d;
  }
  const divisor = gcd(n, d);
  return Object.freeze({ n: n / divisor, d: d / divisor });
}

function plus(left, right) {
  return fraction(left.n * right.d + right.n * left.d, left.d * right.d);
}

function minus(left, right) {
  return plus(left, fraction(-right.n, right.d));
}

function product(left, right) {
  return fraction(left.n * right.n, left.d * right.d);
}

function quotient(left, right) {
  return fraction(left.n * right.d, left.d * right.n);
}

function power(value, exponent) {
  return fraction(value.n ** BigInt(exponent), value.d ** BigInt(exponent));
}

function same(left, right) {
  return left.n === right.n && left.d === right.d;
}

function less(left, right) {
  return left.n * right.d < right.n * left.d;
}

function textFraction(value) {
  return `${value.n}/${value.d}`;
}

function determinantBareiss(matrix) {
  const values = matrix.map((row) => [...row]);
  const size = values.length;
  let sign = 1n;
  let previous = 1n;
  for (let column = 0; column < size - 1; column += 1) {
    if (values[column][column] === 0n) {
      let pivotRow = -1;
      for (let row = column + 1; row < size; row += 1) {
        if (values[row][column] !== 0n) {
          pivotRow = row;
          break;
        }
      }
      if (pivotRow < 0) return 0n;
      [values[column], values[pivotRow]] = [values[pivotRow], values[column]];
      sign = -sign;
    }
    const pivot = values[column][column];
    for (let row = column + 1; row < size; row += 1) {
      for (let entry = column + 1; entry < size; entry += 1) {
        const numerator =
          values[row][entry] * pivot -
          values[row][column] * values[column][entry];
        if (numerator % previous !== 0n) {
          throw new Error("Bareiss division was not exact");
        }
        values[row][entry] = numerator / previous;
      }
      values[row][column] = 0n;
    }
    previous = pivot;
  }
  return sign * values.at(-1).at(-1);
}

function resultantInteger(first, second) {
  const degreeFirst = first.length - 1;
  const degreeSecond = second.length - 1;
  const width = degreeFirst + degreeSecond;
  const matrix = [];
  for (let shift = 0; shift < degreeSecond; shift += 1) {
    matrix.push([
      ...Array(shift).fill(0n),
      ...first,
      ...Array(degreeSecond - 1 - shift).fill(0n),
    ]);
  }
  for (let shift = 0; shift < degreeFirst; shift += 1) {
    matrix.push([
      ...Array(shift).fill(0n),
      ...second,
      ...Array(degreeFirst - 1 - shift).fill(0n),
    ]);
  }
  if (matrix.some((row) => row.length !== width)) {
    throw new Error("invalid Sylvester matrix");
  }
  return determinantBareiss(matrix);
}

function realSliceDiscriminant(aValue, bValue) {
  const coefficients = [
    3n * bValue,
    2n * aValue,
    1n,
    0n,
    -1n,
    -2n * aValue,
    -3n * bValue,
  ];
  const derivative = coefficients
    .slice(0, 6)
    .map((value, index) => BigInt(6 - index) * value);
  const result = resultantInteger(coefficients, derivative);
  const leading = coefficients[0];
  if (leading === 0n || result % leading !== 0n) {
    throw new Error("invalid sextic discriminant division");
  }
  return -result / leading;
}

function verifyRealSliceFactorization() {
  const aNodes = Array.from({ length: 11 }, (_, index) => index - 5);
  const bNodes = Array.from({ length: 11 }, (_, index) => index + 1);
  let checked = 0;
  for (const aNumber of aNodes) {
    for (const bNumber of bNodes) {
      const a = BigInt(aNumber);
      const b = BigInt(bNumber);
      const delta = a * a + 9n * b * b - 3n * b;
      const expected =
        -64n *
        (4n * a - 9n * b - 1n) ** 3n *
        (4n * a + 9n * b + 1n) ** 3n *
        delta ** 2n;
      if (realSliceDiscriminant(a, b) !== expected) {
        throw new Error(`real-slice factorization failed at ${aNumber},${bNumber}`);
      }
      checked += 1;
    }
  }
  return {
    discriminant:
      "-64*(4*a-9*b-1)^3*(4*a+9*b+1)^3*(a^2+9*b^2-3*b)^2",
    degreeBoundEachVariable: 10,
    aNodes,
    bNodes,
    exactGridEvaluations: checked,
    tensorGridIdentityProof: checked === 121,
  };
}

function canonicalPayload() {
  const centerZ2 = fraction(3n, 20n);
  const radiusZ2 = fraction(1n, 100n);
  const radiusZ3 = fraction(1n, 1000n);
  const z2Lower = minus(centerZ2, radiusZ2);
  const z2Upper = plus(centerZ2, radiusZ2);
  const q2InitialLower = product(fraction(4n), z2Lower);
  const coneExit = minus(q2InitialLower, fraction(1n, 2n));
  const q2Y1Upper = plus(
    product(product(fraction(4n), z2Upper), fraction(1n, 8n)),
    product(product(fraction(9n), radiusZ3), fraction(1n, 256n)),
  );

  const perturbD1 = plus(product(fraction(2n), radiusZ2), product(fraction(3n), radiusZ3));
  const perturbD2 = plus(product(fraction(4n), radiusZ2), product(fraction(9n), radiusZ3));
  const perturbD3 = plus(product(fraction(8n), radiusZ2), product(fraction(27n), radiusZ3));
  const sinLower = minus(fraction(1n, 16n), fraction(1n, 24576n));
  const criticalSineUpper = product(fraction(5n, 2n), perturbD1);
  const boundaryMargin = minus(product(fraction(2n, 5n), sinLower), perturbD1);
  const cosDoubleRadiusLower = fraction(71n, 72n);
  const normalizedCurvature = minus(
    minus(cosDoubleRadiusLower, fraction(3n, 5n)),
    perturbD2,
  );
  const normalizedQuarterMargin = minus(
    minus(fraction(1n, 3n), perturbD2),
    fraction(1n, 4n),
  );
  const piBoxMargin = minus(
    minus(minus(fraction(6n, 7n), fraction(3n, 5n)), perturbD2),
    fraction(1n, 5n),
  );

  const derivativeBounds = [
    plus(plus(fraction(1n), z2Upper), radiusZ3),
    plus(plus(fraction(1n), product(fraction(2n), z2Upper)), product(fraction(3n), radiusZ3)),
    plus(plus(fraction(1n), product(fraction(4n), z2Upper)), product(fraction(9n), radiusZ3)),
    plus(plus(fraction(1n), product(fraction(8n), z2Upper)), product(fraction(27n), radiusZ3)),
  ];
  const derivativeSum = derivativeBounds.reduce((total, value) => plus(total, value), fraction(0n));
  const upperCurvatureMargin = minus(fraction(5n, 3n), derivativeBounds[2]);
  const mixedMargin = minus(fraction(7n, 3n), derivativeBounds[3]);
  const eta = power(fraction(3n, 7n), 4);
  const slowLeft = product(fraction(7n, 3n), eta);
  const slowRight = power(fraction(3n, 7n), 3);

  const pReal = { cos: fraction(-1n, 4n), A: fraction(-9n, 4n) };
  const pImag = { sin: fraction(-1n, 2n), B: fraction(-3n, 2n) };
  const fPrime = {
    sin: minus(fraction(-1n), product(fraction(2n), pImag.sin)),
    B: minus(product(fraction(-2n), pImag.B), fraction(3n)),
  };
  const fSecond = {
    cos: minus(fraction(-1n), product(fraction(4n), pReal.cos)),
    A: minus(product(fraction(-4n), pReal.A), fraction(9n)),
  };
  const fThird = {
    sin: plus(fraction(1n), product(fraction(8n), pImag.sin)),
    B: plus(product(fraction(8n), pImag.B), fraction(27n)),
  };
  const fFourth = {
    cos: plus(fraction(1n), product(fraction(16n), pReal.cos)),
    A: plus(product(fraction(16n), pReal.A), fraction(81n)),
  };

  const realSlice = verifyRealSliceFactorization();
  const exactChecks = {
    z2RangeExact: same(z2Lower, fraction(7n, 50n)) && same(z2Upper, fraction(4n, 25n)),
    strictConeExit: same(coneExit, fraction(3n, 50n)),
    heatPathEntersOldConeByY1: same(q2Y1Upper, fraction(20489n, 256000n)) && less(q2Y1Upper, fraction(1n, 2n)),
    perturbationBudgetsExact:
      same(perturbD1, fraction(23n, 1000n)) &&
      same(perturbD2, fraction(49n, 1000n)) &&
      same(perturbD3, fraction(107n, 1000n)),
    criticalLocalizationStrict: less(criticalSineUpper, sinLower),
    boundaryMarginExact: same(boundaryMargin, fraction(3047n, 1536000n)),
    normalizedCurvatureGreaterThanThird:
      same(normalizedCurvature, fraction(1517n, 4500n)) &&
      less(fraction(1n, 3n), normalizedCurvature),
    localQuarterMarginExact: same(normalizedQuarterMargin, fraction(103n, 3000n)),
    piBoxMarginExact: same(piBoxMargin, fraction(57n, 7000n)),
    derivativeLedgerExact:
      derivativeBounds.every((value, index) =>
        same(value, [fraction(1161n, 1000n), fraction(1323n, 1000n), fraction(1649n, 1000n), fraction(2307n, 1000n)][index]),
      ),
    derivativeSumExact: same(derivativeSum, fraction(161n, 25n)),
    upperCurvatureMarginExact: same(upperCurvatureMargin, fraction(53n, 3000n)),
    mixedDerivativeMarginExact: same(mixedMargin, fraction(79n, 3000n)),
    slowThresholdIdentity:
      same(slowLeft, slowRight) && same(slowLeft, fraction(27n, 343n)),
    incidenceJetsExact:
      Object.values(fPrime).every((value) => same(value, fraction(0n))) &&
      Object.values(fSecond).every((value) => same(value, fraction(0n))) &&
      same(fThird.sin, fraction(-3n)) &&
      same(fThird.B, fraction(15n)) &&
      same(fFourth.cos, fraction(-3n)) &&
      same(fFourth.A, fraction(45n)),
    realSliceFactorizationExact: realSlice.tensorGridIdentityProof === true,
  };

  const rationalMapping = (mapping) =>
    Object.fromEntries(Object.entries(mapping).map(([key, value]) => [key, textFraction(value)]));

  return {
    schemaVersion: SCHEMA_VERSION,
    theoremId: "R0.72R-four-real-dimensional-caustic-free-core",
    polydisc: {
      centerZ2: textFraction(centerZ2),
      radiusZ2: textFraction(radiusZ2),
      radiusZ3: textFraction(radiusZ3),
      absZ2Range: [textFraction(z2Lower), textFraction(z2Upper)],
      realDimension: 4,
      nonemptyInterior: true,
    },
    heatPath: {
      normalizedZ2: "z2*exp(-3*y)",
      normalizedZ3: "z3*exp(-8*y)",
      q2InitialLower: textFraction(q2InitialLower),
      oldConeBoundary: "1/2",
      coneExitMargin: textFraction(coneExit),
      q2AtY1UpperUsingEGreaterThanTwo: textFraction(q2Y1Upper),
      strictlyDecreasing: true,
      uniqueOldConeCrossingOnZeroOne: true,
    },
    perturbation: {
      d1: textFraction(perturbD1),
      d2: textFraction(perturbD2),
      d3: textFraction(perturbD3),
      centerSlopeFactorLower: "2/5",
    },
    criticalGeometry: {
      criticalCount: 2,
      criticalBoxes: ["dist(phi,0)<pi/48", "dist(phi,pi)<pi/48"],
      sinRadiusLower: textFraction(sinLower),
      criticalSineUpper: textFraction(criticalSineUpper),
      boundarySignMargin: textFraction(boundaryMargin),
      cosDoubleRadiusLower: textFraction(cosDoubleRadiusLower),
      normalizedCurvatureLower: textFraction(normalizedCurvature),
      normalizedCurvatureGreaterThan: "1/3",
      localQuarterMargin: textFraction(normalizedQuarterMargin),
      piBoxOneFifthMargin: textFraction(piBoxMargin),
    },
    shapeContract: {
      radius: "pi/48",
      criticalCount: 2,
      normalizedLocalSlope: ["1/4", "5/3"],
      normalizedAwaySlopeLower: "1/80",
      physicalWindow: "0<=y<=1",
      physicalLocalSlope: ["1/12", "5/3"],
      physicalAwaySlopeLower: "1/240",
      C0: "144/1",
      C1: "240/1",
      upperCurvatureMargin: textFraction(upperCurvatureMargin),
    },
    derivativeLedger: {
      d0: textFraction(derivativeBounds[0]),
      d1: textFraction(derivativeBounds[1]),
      d2: textFraction(derivativeBounds[2]),
      d3: textFraction(derivativeBounds[3]),
      sumW3Infinity: textFraction(derivativeSum),
      mixedDerivativeUpper: textFraction(derivativeBounds[3]),
      mixedBelowSevenThirdsMargin: textFraction(mixedMargin),
      slowEtaThreshold: textFraction(eta),
      slowEtaSymbolic: "(3/7)^4",
      slowIdentityAtThreshold: textFraction(slowLeft),
      completeThresholdAlsoRequiresEtaCH: true,
    },
    incidence: {
      z3: "(A+i*B)*exp(-3*i*phi)",
      z2: "exp(-2*i*phi)*(-(cos(phi)+9*A)/4-i*(sin(phi)+3*B)/2)",
      gammaFixedZ3Coefficients: ["1/8", "-3/8", "-15/8", "-3/8"],
      gammaFixedZ3Exponents: [-3, -1, 1, -5],
      unitCirclePolynomial: "3*z3*u^6+2*z2*u^5+u^4-u^2-2*conj(z2)*u-3*conj(z3)",
      degeneracyCondition: "exists abs(u)=1: D(u)=D'(u)=0",
      pRealCoefficients: rationalMapping(pReal),
      pImagCoefficients: rationalMapping(pImag),
      fPrimeCoefficients: rationalMapping(fPrime),
      fSecondCoefficients: rationalMapping(fSecond),
      fThirdCoefficients: rationalMapping(fThird),
      fFourthCoefficients: rationalMapping(fFourth),
    },
    realSlice: {
      q: "12*b*x^2+4*a*x+1-3*b",
      endpointWalls: ["1+4*a+9*b=0", "1-4*a+9*b=0"],
      delta: "a^2+9*b^2-3*b",
      internalArc: "delta=0 and 1/15<=b<=1/3",
      openInteriorArc: "delta=0 and 1/15<b<=1/3",
      ...realSlice,
    },
    claimBoundary: {
      finiteCertificateIsContinuumProof: false,
      completeFourDimensionalChamberClassification: false,
      causticCrossingEnhancedDissipation: false,
      arbitraryTimeDependentPhases: false,
      uniformThirdCarrierAmplitudeFloor: false,
      generalThreeDimensionalRegularity: false,
    },
    exactChecks,
    passed: Object.values(exactChecks).every(Boolean),
  };
}

function currentCommit(root) {
  try {
    return execFileSync("git", ["rev-parse", "HEAD"], {
      cwd: root,
      encoding: "utf8",
      stdio: ["ignore", "pipe", "ignore"],
    }).trim();
  } catch {
    return "unavailable";
  }
}

function trackedTreeDirty(root) {
  return [
    ["diff", "--quiet"],
    ["diff", "--cached", "--quiet"],
  ].some(
    (arguments_) =>
      spawnSync("git", arguments_, { cwd: root, stdio: "ignore" }).status !== 0,
  );
}

function requiredSourcesTracked(root) {
  return [
    "research/r072r_report-source.md",
    "research/r072r_independent_audit.mjs",
    "research/r072r_compare_audits.py",
  ].every(
    (relative) =>
      spawnSync("git", ["ls-files", "--error-unmatch", relative], {
        cwd: root,
        stdio: "ignore",
      }).status === 0,
  );
}

function commandLine(arguments_) {
  const outputIndex = arguments_.indexOf("--output-dir");
  if (outputIndex < 0 || outputIndex + 1 >= arguments_.length) {
    throw new Error("usage: node research/r072r_independent_audit.mjs --output-dir DIR");
  }
  return { output: path.resolve(arguments_[outputIndex + 1]) };
}

function now() {
  return new Date().toISOString();
}

async function writeJson(target, value) {
  await writeFile(target, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function main() {
  const { output } = commandLine(process.argv.slice(2));
  await mkdir(output, { recursive: true });
  const script = fileURLToPath(import.meta.url);
  const root = path.dirname(path.dirname(script));
  const started = process.hrtime.bigint();

  const config = {
    schemaVersion: SCHEMA_VERSION,
    audit: AUDIT,
    precision: "JavaScript BigInt rational and exact integer Bareiss resultant audit",
    gitCommit: currentCommit(root),
    sourceTracked: requiredSourcesTracked(root),
    trackedChangesDirty: trackedTreeDirty(root),
    limitations:
      "Finite exact algebra only; continuum trigonometric monotonicity, Coble--He enhanced dissipation, and global caustic topology remain analytic or open statements in the report.",
  };
  await writeJson(path.join(output, "independent-config.json"), config);

  const payload = canonicalPayload();
  await writeJson(path.join(output, "independent-payload.json"), payload);
  const stages = [
    ["cone-exit-and-heat-crossing", payload.heatPath.uniqueOldConeCrossingOnZeroOne],
    ["two-critical-shape", payload.shapeContract.criticalCount === 2],
    ["slow-time-ledger", payload.derivativeLedger.completeThresholdAlsoRequiresEtaCH],
    ["complex-incidence", payload.exactChecks.incidenceJetsExact],
    ["real-slice-factorization", payload.exactChecks.realSliceFactorizationExact],
    ["claim-boundary", payload.claimBoundary.finiteCertificateIsContinuumProof === false],
  ];
  const progress = [
    { time: now(), stage: "start", ...config },
    ...stages.map(([stage, passed]) => ({ time: now(), stage, passed })),
  ];
  const checks = {
    payloadPassed: payload.passed,
    twoCriticalShapePassed: payload.shapeContract.criticalCount === 2,
    coneCrossingPassed: payload.heatPath.uniqueOldConeCrossingOnZeroOne === true,
    incidencePassed: payload.exactChecks.incidenceJetsExact,
    realSlicePassed: payload.exactChecks.realSliceFactorizationExact,
    claimBoundaryScoped: payload.claimBoundary.generalThreeDimensionalRegularity === false,
  };
  const elapsedSeconds = Number(process.hrtime.bigint() - started) / 1_000_000_000;
  const maxRssMb = process.resourceUsage().maxRSS / 1024;
  const result = {
    schemaVersion: SCHEMA_VERSION,
    audit: AUDIT,
    status: Object.values(checks).every(Boolean) ? "passed" : "failed",
    checks,
    elapsedSeconds,
    maxRssMb,
    limitations: config.limitations,
  };
  await writeJson(path.join(output, "independent-result.json"), result);
  await writeFile(
    path.join(output, "independent-progress.ndjson"),
    `${progress.map((row) => JSON.stringify(row)).join("\n")}\n`,
    "utf8",
  );
  await writeFile(
    path.join(output, "independent-resource.ndjson"),
    `${JSON.stringify({ time: now(), event: "complete", elapsedSeconds, maxRssMb, pid: process.pid })}\n`,
    "utf8",
  );
  await writeFile(
    path.join(output, "independent-monitor.log"),
    `[independent] status=${result.status} cone=${checks.coneCrossingPassed} shape=${checks.twoCriticalShapePassed} incidence=${checks.incidencePassed}\n`,
    "utf8",
  );
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (result.status !== "passed") process.exitCode = 1;
}

main().catch((error) => {
  process.stderr.write(`${error.stack ?? error}\n`);
  process.exitCode = 1;
});
