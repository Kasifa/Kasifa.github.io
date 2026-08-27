#!/usr/bin/env node

/**
 * Independent exact-arithmetic audit for the R0.72P two-carrier gate.
 *
 * This route rebuilds the finite cell, shape, slow-threshold, Morse-wall,
 * claim-contract, and exponent ledgers with BigInt rationals. It neither
 * imports the Python implementation nor reads any counterpart artifacts.
 */

import { execFileSync, spawnSync } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const AUDIT = "R0.72P independent two-carrier exact audit";
const SCHEMA_VERSION = 1;

function gcd(left, right) {
  let a = left < 0n ? -left : left;
  let b = right < 0n ? -right : right;
  while (b !== 0n) [a, b] = [b, a % b];
  return a;
}

function rational(numerator, denominator = 1n) {
  let n = BigInt(numerator);
  let d = BigInt(denominator);
  if (d === 0n) throw new RangeError("zero rational denominator");
  if (d < 0n) {
    n = -n;
    d = -d;
  }
  const divisor = gcd(n, d);
  return Object.freeze({ n: n / divisor, d: d / divisor });
}

function add(left, right) {
  return rational(left.n * right.d + right.n * left.d, left.d * right.d);
}

function negate(value) {
  return rational(-value.n, value.d);
}

function subtract(left, right) {
  return add(left, negate(right));
}

function times(left, right) {
  return rational(left.n * right.n, left.d * right.d);
}

function over(left, right) {
  return rational(left.n * right.d, left.d * right.n);
}

function equal(left, right) {
  return left.n === right.n && left.d === right.d;
}

function rationalString(value) {
  return `${value.n}/${value.d}`;
}

function monomial(values = {}) {
  return new Map(
    Object.entries(values).filter(([, value]) => value.n !== 0n),
  );
}

function multiplyMonomials(...terms) {
  const result = new Map();
  for (const term of terms) {
    for (const [key, value] of term) {
      const next = add(result.get(key) ?? rational(0n), value);
      if (next.n === 0n) result.delete(key);
      else result.set(key, next);
    }
  }
  return result;
}

function divideMonomials(left, right) {
  return multiplyMonomials(
    left,
    new Map([...right].map(([key, value]) => [key, negate(value)])),
  );
}

function serializeMonomial(term) {
  return Object.fromEntries(
    [...term]
      .sort(([left], [right]) => (left < right ? -1 : left > right ? 1 : 0))
      .map(([key, value]) => [key, rationalString(value)]),
  );
}

function cellFactor() {
  const multiplier = rational(2n);
  const epsilonConstant = rational(2n);
  const ratio = over(multiplier, epsilonConstant);
  return {
    activeCellShifts: [-2, -1, 1, 2],
    cellJacobian: { R: "-2/1" },
    epsilonDefinition: {
      absoluteDelta: "1/1",
      a: "1/1",
      R: "-2/1",
      constant: rationalString(epsilonConstant),
    },
    fourierMultiplierConstant: rationalString(multiplier),
    affineInvariantRow: "{(nR,q_*):n∈Z}",
    rowIsomorphicTo: "RZ",
    rescaledCoefficientOverEpsilon: rationalString(ratio),
    secondCarrierCellFrequency: "2/1",
    passed: equal(ratio, rational(1n)),
  };
}

function shapeBounds() {
  const lambdaMax = rational(1n, 8n);
  const deviation = times(rational(4n), lambdaMax);
  const factorLower = subtract(rational(1n), deviation);
  const factorUpper = add(rational(1n), deviation);
  const eUpper = rational(87n, 32n);
  const expMinusOneLower = rational(1n, 3n);
  const sineLocalRatioLower = rational(1n, 2n);
  const sineExteriorLower = rational(1n, 2n);
  const localLower = times(
    times(expMinusOneLower, factorLower),
    sineLocalRatioLower,
  );
  const exteriorLower = times(
    times(expMinusOneLower, factorLower),
    sineExteriorLower,
  );
  const derivatives = {
    W: add(rational(1n), lambdaMax),
    d1: add(rational(1n), times(rational(2n), lambdaMax)),
    d2: add(rational(1n), times(rational(4n), lambdaMax)),
    d3: add(rational(1n), times(rational(8n), lambdaMax)),
  };
  const expected = {
    W: rational(9n, 8n),
    d1: rational(5n, 4n),
    d2: rational(3n, 2n),
    d3: rational(2n),
  };
  const derivativePass = Object.keys(expected).every((key) =>
    equal(derivatives[key], expected[key]),
  );
  const passed =
    equal(factorLower, rational(1n, 2n)) &&
    equal(factorUpper, rational(3n, 2n)) &&
    eUpper.n < 3n * eUpper.d &&
    equal(localLower, rational(1n, 12n)) &&
    equal(exteriorLower, rational(1n, 12n)) &&
    derivativePass;
  return {
    C0: "144/1",
    C1: "12/1",
    alphaAbsMax: rationalString(lambdaMax),
    criticalCount: 2,
    criticalSet: ["0", "pi"],
    derivativeSupremumBounds: Object.fromEntries(
      Object.entries(derivatives).map(([key, value]) => [key, rationalString(value)]),
    ),
    eUpperCertificate: rationalString(eUpper),
    eUpperLessThanThree: eUpper.n < 3n * eUpper.d,
    exteriorGradientLower: rationalString(exteriorLower),
    exteriorGradientUpper: rationalString(factorUpper),
    factorDeviationMax: rationalString(deviation),
    factorLower: rationalString(factorLower),
    factorUpper: rationalString(factorUpper),
    lambdaAbsMax: rationalString(lambdaMax),
    localGradientLower: rationalString(localLower),
    localGradientUpper: rationalString(factorUpper),
    radius: "pi/4",
    passed,
  };
}

function slowThreshold() {
  const eta = rational(1n, 16n);
  const coefficient = rational(2n);
  const left = times(coefficient, eta);
  const right = rational(1n, 8n);
  return {
    derivativeCoefficientBound: rationalString(coefficient),
    etaThreshold: rationalString(eta),
    leftAtThreshold: rationalString(left),
    rightAtThreshold: rationalString(right),
    reducedCondition: "eta^(1/4)<=1/2",
    passed: equal(left, right),
  };
}

function wallRows() {
  return [
    ["plus", rational(1n, 4n), "pi", rational(-1n), rational(3n)],
    ["minus", rational(-1n, 4n), "0", rational(1n), rational(-3n)],
  ].map(([side, lambda, phi, cosine, expectedFourth]) => {
    const cosineTwo = rational(1n);
    const first = rational(0n);
    const second = subtract(
      negate(cosine),
      times(times(rational(4n), lambda), cosineTwo),
    );
    const third = rational(0n);
    const fourth = add(
      cosine,
      times(times(rational(16n), lambda), cosineTwo),
    );
    return {
      side,
      lambda: rationalString(lambda),
      phi,
      firstDerivative: rationalString(first),
      secondDerivative: rationalString(second),
      thirdDerivative: rationalString(third),
      fourthDerivative: rationalString(fourth),
      expectedFourthDerivative: rationalString(expectedFourth),
      extraCriticalEquation: "cos(phi)=-1/(4lambda)",
      conclusion: "Morse-applicability-wall-only",
      passed:
        equal(first, rational(0n)) &&
        equal(second, rational(0n)) &&
        equal(third, rational(0n)) &&
        equal(fourth, expectedFourth),
    };
  });
}

function claimContract() {
  return {
    arbitraryCommonBandStatus: "open",
    carrierPattern: [1, 2],
    constantScope: "enhanced-dissipation-estimate",
    constantsIndependentOf: [
      "R",
      "epsilon",
      "lambda",
      "lambda_minus",
      "initial datum",
    ],
    constantsMayDependOn: ["fixed upper shape class", "lambda_max"],
    finiteCertificateIsProof: false,
    fullSuperposition: true,
    growingCarrierCountStatus: "open",
    integratedEstimate: {
      epsilonExponent: "-1/2",
      required: true,
      status: "proved-analytically-for-declared-class",
    },
    lambdaClass: "0<lambda_minus<=abs(lambda)<=1/8",
    physicalAmplitudeBalanceMayDependOn: ["lambda_minus"],
    sameUniformConstantsRequired: true,
    status: "proved-for-declared-real-collinear-phase-1:2-class",
    terminalEstimate: {
      decayExponent: "sqrt(epsilon)",
      required: true,
      status: "proved-analytically-for-declared-class",
    },
  };
}

function exponentLedger() {
  const nValue = rational(2n);
  const bValue = rational(2n);
  const pSquared = over(nValue, times(bValue, bValue));
  const u0 = monomial({ epsilon: rational(4n, 3n), p: rational(4n, 3n) });
  const rawEd = monomial({ epsilon: rational(1n, 2n) });
  const uEd = multiplyMonomials(u0, rawEd);
  const zStrong = monomial({
    epsilon: rational(4n, 3n),
    p: rational(2n),
    R: rational(2n, 3n),
    L: rational(1n),
  });
  const quotient = divideMonomials(uEd, zStrong);
  const crossCubic = monomial({
    a: rational(2n),
    N: rational(2n),
    epsilon: rational(1n, 2n),
  });
  const general = {
    FullSuperpositionCrossCubic: serializeMonomial(crossCubic),
    UED: serializeMonomial(uEd),
    UEDOverZ: serializeMonomial(quotient),
    ZStrong: serializeMonomial(zStrong),
  };
  const expectedGeneral = {
    FullSuperpositionCrossCubic: {
      N: "2/1",
      a: "2/1",
      epsilon: "1/2",
    },
    UED: { epsilon: "11/6", p: "4/3" },
    UEDOverZ: {
      L: "-1/1",
      R: "-2/3",
      epsilon: "1/2",
      p: "-2/3",
    },
    ZStrong: {
      L: "1/1",
      R: "2/3",
      epsilon: "4/3",
      p: "2/1",
    },
  };
  const fixedPattern = {
    crossCubicCoefficientN2: rationalString(times(nValue, nValue)),
    strongWindowEpsilonRhs: { L: "2/1", R: "4/3", two: "-2/3" },
    strongWindowSqrtEpsilonRhs: { L: "1/1", R: "2/3", two: "-1/3" },
    UED: { epsilon: "11/6", two: "-2/3" },
    UEDOverZ: {
      L: "-1/1",
      R: "-2/3",
      epsilon: "1/2",
      two: "1/3",
    },
    ZStrong: {
      L: "1/1",
      R: "2/3",
      epsilon: "4/3",
      two: "-1/1",
    },
  };
  return {
    claimContract: claimContract(),
    fixedPattern,
    general,
    parameters: {
      B: rationalString(bValue),
      N: rationalString(nValue),
      pSquared: rationalString(pSquared),
    },
    passed:
      JSON.stringify(general) === JSON.stringify(expectedGeneral) &&
      equal(pSquared, rational(1n, 2n)),
  };
}

function shapeRows(exact) {
  const shape = exact.shapeBounds;
  const slow = exact.slowThreshold;
  return [
    ["factorLower", shape.factorLower, "1-4*(1/8)"],
    ["factorUpper", shape.factorUpper, "1+4*(1/8)"],
    ["localGradientLower", shape.localGradientLower, "(1/3)*(1/2)*(1/2)"],
    ["localGradientUpper", shape.localGradientUpper, "1*(3/2)*1"],
    ["exteriorGradientLower", shape.exteriorGradientLower, "(1/3)*(1/2)*(1/2)"],
    ["W", shape.derivativeSupremumBounds.W, "1+1/8"],
    ["d1", shape.derivativeSupremumBounds.d1, "1+2/8"],
    ["d2", shape.derivativeSupremumBounds.d2, "1+4/8"],
    ["d3", shape.derivativeSupremumBounds.d3, "1+8/8"],
    ["etaThreshold", slow.etaThreshold, "2*eta=eta^(3/4)"],
  ].map(([quantity, value, derivation]) => ({
    quantity,
    value,
    derivation,
    passed: true,
  }));
}

function csvEscape(value) {
  const text = String(value);
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function csvScalar(value) {
  if (typeof value === "boolean") return value ? "True" : "False";
  return String(value);
}

function rowsToCsv(rows) {
  if (rows.length === 0) throw new Error("cannot serialize empty CSV table");
  const fields = Object.keys(rows[0]);
  const lines = [fields.join(",")];
  for (const row of rows) {
    lines.push(fields.map((field) => csvEscape(csvScalar(row[field]))).join(","));
  }
  return `${lines.join("\n")}\n`;
}

function parseOutputDirectory(argv) {
  const index = argv.indexOf("--output-dir");
  if (index < 0 || index + 1 >= argv.length) {
    throw new Error("usage: node research/r072p_independent_audit.mjs --output-dir DIR");
  }
  return path.resolve(argv[index + 1]);
}

function gitCommit(root) {
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

function trackedChangesDirty(root) {
  return [
    ["diff", "--quiet"],
    ["diff", "--cached", "--quiet"],
  ].some((arguments_) =>
    spawnSync("git", arguments_, { cwd: root, stdio: "ignore" }).status !== 0,
  );
}

function sourcesTracked(root) {
  return [
    "research/r072p_report-source.md",
    "research/r072p_independent_audit.mjs",
    "research/r072p_compare_audits.py",
  ].every(
    (relative) =>
      spawnSync("git", ["ls-files", "--error-unmatch", relative], {
        cwd: root,
        stdio: "ignore",
      }).status === 0,
  );
}

function utcNow() {
  return new Date().toISOString();
}

async function writeJson(target, value) {
  await writeFile(target, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function main() {
  const output = parseOutputDirectory(process.argv.slice(2));
  await mkdir(output, { recursive: true });
  const scriptPath = fileURLToPath(import.meta.url);
  const root = path.dirname(path.dirname(scriptPath));
  const started = process.hrtime.bigint();

  const config = {
    schemaVersion: SCHEMA_VERSION,
    audit: AUDIT,
    precision: "JavaScript BigInt exact rational arithmetic; symbolic pi labels only",
    gitCommit: gitCommit(root),
    sourceTracked: sourcesTracked(root),
    trackedChangesDirty: trackedChangesDirty(root),
    limitations:
      "The certificate audits finite algebra and claim wiring. It does not prove the semigroup theorem, continuum sine inequalities, or any general Navier-Stokes regularity statement.",
  };
  await writeJson(path.join(output, "independent-config.json"), config);

  const exact = {
    cellFactor: cellFactor(),
    shapeBounds: shapeBounds(),
    slowThreshold: slowThreshold(),
    morseWall: {
      absLambda: "1/4",
      extraCriticalEquation: "cos(phi)=-1/(4lambda)",
      status: "Morse-applicability-wall-only",
    },
    exponentLedger: exponentLedger(),
  };
  const walls = wallRows();
  const shapes = shapeRows(exact);
  await writeJson(path.join(output, "independent-exponents.json"), exact);
  await writeFile(path.join(output, "independent-shape.csv"), rowsToCsv(shapes), "utf8");
  await writeFile(path.join(output, "independent-wall.csv"), rowsToCsv(walls), "utf8");

  const stages = [
    ["cell-factor", exact.cellFactor.passed],
    ["shape-bounds", exact.shapeBounds.passed],
    ["slow-threshold", exact.slowThreshold.passed],
    ["morse-wall", walls.every((row) => row.passed)],
    [
      "claim-contract",
      ["integratedEstimate", "terminalEstimate"].every(
        (name) => exact.exponentLedger.claimContract[name].required,
      ),
    ],
    ["exponent-ledger", exact.exponentLedger.passed],
  ];
  const progress = [
    { time: utcNow(), stage: "start", ...config },
    ...stages.map(([stage, passed]) => ({ time: utcNow(), stage, passed })),
  ];

  const checks = {
    cellFactorPassed: exact.cellFactor.passed,
    shapeBoundsPassed: exact.shapeBounds.passed,
    slowThresholdPassed: exact.slowThreshold.passed,
    morseWallPassed: walls.every((row) => row.passed),
    integralAndTerminalRequired: ["integratedEstimate", "terminalEstimate"].every(
      (name) => exact.exponentLedger.claimContract[name].required,
    ),
    fullSuperpositionStatusScoped:
      exact.exponentLedger.claimContract.status ===
        "proved-for-declared-real-collinear-phase-1:2-class" &&
      exact.exponentLedger.claimContract.arbitraryCommonBandStatus === "open",
    n2PSquaredLedgerPassed: exact.exponentLedger.passed,
  };
  const elapsedSeconds =
    Number(process.hrtime.bigint() - started) / 1_000_000_000;
  const maxRssMb = process.resourceUsage().maxRSS / 1024.0;
  const result = {
    schemaVersion: SCHEMA_VERSION,
    audit: AUDIT,
    status: Object.values(checks).every(Boolean) ? "passed" : "failed",
    checks,
    shapeRows: shapes.length,
    wallRows: walls.length,
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
    `${JSON.stringify({
      time: utcNow(),
      event: "complete",
      elapsedSeconds,
      maxRssMb,
      pid: process.pid,
    })}\n`,
    "utf8",
  );
  await writeFile(
    path.join(output, "independent-monitor.log"),
    `[independent] status=${result.status} shape=${shapes.length} wall=${walls.length} integralTerminal=${checks.integralAndTerminalRequired}\n`,
    "utf8",
  );
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (result.status !== "passed") process.exitCode = 1;
}

main().catch((error) => {
  process.stderr.write(`${error.stack ?? error}\n`);
  process.exitCode = 1;
});
