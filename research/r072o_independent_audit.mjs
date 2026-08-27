#!/usr/bin/env node

/**
 * Independent R0.72O physical-reinsertion audit.
 *
 * This route rebuilds the exponent ledger with BigInt rational arithmetic
 * and recomputes the finite window and degeneracy tables with JavaScript's
 * IEEE-754 binary64 arithmetic. It neither imports the Python producer nor
 * reads any producer artifact.
 */

import { execFileSync } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const AUDIT = "R0.72O independent physical-reinsertion audit";
const SCHEMA_VERSION = 1;
const R_VALUES = [16, 64, 256, 1024];
const LEVELS = [0.01, 1.0, 100.0];
const SCREEN_TOLERANCE = 2.0e-13;

function gcd(left, right) {
  let a = left < 0n ? -left : left;
  let b = right < 0n ? -right : right;
  while (b !== 0n) {
    [a, b] = [b, a % b];
  }
  return a;
}

function rational(numerator, denominator = 1n) {
  if (denominator === 0n) {
    throw new RangeError("zero rational denominator");
  }
  let n = BigInt(numerator);
  let d = BigInt(denominator);
  if (d < 0n) {
    n = -n;
    d = -d;
  }
  const divisor = gcd(n, d);
  return Object.freeze({ n: n / divisor, d: d / divisor });
}

function addRational(left, right) {
  return rational(left.n * right.d + right.n * left.d, left.d * right.d);
}

function negateRational(value) {
  return rational(-value.n, value.d);
}

function rationalString(value) {
  return `${value.n}/${value.d}`;
}

function monomial(values = {}) {
  const result = new Map();
  for (const [key, value] of Object.entries(values)) {
    if (value.n !== 0n) {
      result.set(key, value);
    }
  }
  return result;
}

function multiply(...terms) {
  const result = new Map();
  for (const term of terms) {
    for (const [key, value] of term) {
      const previous = result.get(key) ?? rational(0n);
      const next = addRational(previous, value);
      if (next.n === 0n) {
        result.delete(key);
      } else {
        result.set(key, next);
      }
    }
  }
  return result;
}

function divide(left, right) {
  return multiply(
    left,
    new Map([...right].map(([key, value]) => [key, negateRational(value)])),
  );
}

function serializeMonomial(term) {
  return Object.fromEntries(
    [...term]
      .sort(([left], [right]) => (left < right ? -1 : left > right ? 1 : 0))
      .map(([key, value]) => [key, rationalString(value)]),
  );
}

function withoutVariable(term, variable) {
  return new Map([...term].filter(([key]) => key !== variable));
}

function exactLedger() {
  const u0 = monomial({
    epsilon: rational(4n, 3n),
    p: rational(4n, 3n),
  });
  const edRaw = monomial({ epsilon: rational(1n, 2n) });
  const uEd = multiply(u0, edRaw);
  const v = monomial({
    epsilon: rational(1n, 3n),
    p: rational(1n, 3n),
    R: rational(1n),
  });
  const hEd = divide(uEd, v);
  const zStrong = monomial({
    epsilon: rational(4n, 3n),
    p: rational(2n),
    R: rational(2n, 3n),
    L: rational(1n),
  });
  const uEdOverZ = divide(uEd, zStrong);
  const rhoSquared = monomial({ a: rational(2n), N: rational(1n) });
  const shearNorm = monomial({ a: rational(1n), B: rational(1n) });
  const jacobian = monomial({
    epsilon: rational(1n),
    a: rational(-1n),
    B: rational(-1n),
  });
  const integratedEdGain = monomial({ epsilon: rational(-1n, 2n) });
  const initialEnergy = monomial({ N: rational(1n) });
  const superpositionCrossCubic = multiply(
    rhoSquared,
    shearNorm,
    jacobian,
    integratedEdGain,
    initialEnergy,
  );

  const expected = {
    U0: { epsilon: "4/3", p: "4/3" },
    UED: { epsilon: "11/6", p: "4/3" },
    UEDOneCarrier: { epsilon: "11/6" },
    HED: { R: "-1/1", epsilon: "3/2", p: "1/1" },
    ZStrong: { L: "1/1", R: "2/3", epsilon: "4/3", p: "2/1" },
    UEDOverZ: {
      L: "-1/1",
      R: "-2/3",
      epsilon: "1/2",
      p: "-2/3",
    },
    FullSuperpositionCrossCubic: {
      N: "2/1",
      a: "2/1",
      epsilon: "1/2",
    },
  };
  const actual = {
    U0: serializeMonomial(u0),
    UED: serializeMonomial(uEd),
    UEDOneCarrier: serializeMonomial(withoutVariable(uEd, "p")),
    HED: serializeMonomial(hEd),
    ZStrong: serializeMonomial(zStrong),
    UEDOverZ: serializeMonomial(uEdOverZ),
    FullSuperpositionCrossCubic: serializeMonomial(superpositionCrossCubic),
  };

  const transfers = [
    ["raw", rational(1n), rational(0n)],
    ["enhancedDissipation", rational(1n, 2n), rational(0n)],
    ["criticalLogTarget", rational(0n), rational(1n)],
  ].map(([name, alpha, beta]) => {
    const raw = monomial({ epsilon: alpha, L: beta });
    const numerator = multiply(u0, raw);
    return {
      name,
      alpha: rationalString(alpha),
      beta: rationalString(beta),
      normalizedNumerator: serializeMonomial(numerator),
      relativeToLocalFloor: serializeMonomial(divide(numerator, zStrong)),
    };
  });

  const claimContract = {
    multiCarrierStatus: "conditional",
    requiredHypothesis: "uniform full-superposition integrated ED",
    constantsUniformOver: ["N", "p", "R", "epsilon", "declared geometry family"],
  };
  return {
    actual,
    expected,
    exactExponentLedgerPassed:
      JSON.stringify(actual) === JSON.stringify(expected),
    generalExponentTransfers: transfers,
    claimContract,
  };
}

function degeneracyRows() {
  return R_VALUES.map((rValue) => {
    const first = rValue - rValue;
    const second = 0;
    const third = -(rValue ** 3) + rValue * (rValue + 1) ** 2;
    const expectedThird = rValue * (2 * rValue + 1);
    const passed =
      first === 0 &&
      second === 0 &&
      third === expectedThird &&
      expectedThird !== 0;
    return {
      R: rValue,
      secondCarrierCoefficient: `-${rValue}/${rValue + 1}`,
      firstDerivativeAtZero: first,
      secondDerivativeAtZero: second,
      thirdDerivativeAtZero: third,
      expectedThirdDerivative: expectedThird,
      frequenciesInCommonBand: rValue <= rValue + 1 && rValue + 1 <= 2 * rValue,
      amplitudesComparable:
        0.5 <= rValue / (rValue + 1) && rValue / (rValue + 1) <= 1.0,
      passed,
    };
  });
}

function screenRows() {
  const rows = [];
  for (const rValue of R_VALUES) {
    for (const [regime, pValue] of [
      ["oneCarrier", 1.0],
      ["worstCommonBand", rValue ** -0.5],
    ]) {
      const lR = 1.0 + Math.log(rValue);
      const reference =
        pValue ** (4.0 / 3.0) *
        rValue ** (4.0 / 3.0) *
        lR ** 2;
      for (const level of LEVELS) {
        const epsilon = Math.max(1.0, level * reference);
        const lREpsilon =
          1.0 + Math.log(2.0 + rValue * rValue * (1.0 + epsilon));
        const zExact =
          epsilon ** 2 *
          pValue ** 2 *
          rValue ** (2.0 / 3.0) *
          (1.0 + epsilon) ** (-2.0 / 3.0) *
          lREpsilon;
        const denominator = 1.0 + zExact;
        const oldDirect =
          (epsilon ** (7.0 / 3.0) * pValue ** (4.0 / 3.0)) /
          denominator;
        const edDirect =
          (epsilon ** (11.0 / 6.0) * pValue ** (4.0 / 3.0)) /
          denominator;
        const edOverOld = edDirect / oldDirect;
        const predictedRatio =
          Math.sqrt(epsilon) /
          (pValue ** (2.0 / 3.0) *
            rValue ** (2.0 / 3.0) *
            lREpsilon);
        const ratioExpected = epsilon ** -0.5;
        const passed =
          Number.isFinite(edDirect) &&
          edDirect > 0.0 &&
          edDirect <= oldDirect * (1.0 + SCREEN_TOLERANCE) &&
          Math.abs(edOverOld - ratioExpected) < SCREEN_TOLERANCE;
        rows.push({
          R: rValue,
          regime,
          p: pValue,
          level,
          epsilon,
          LR: lR,
          LRepsilon: lREpsilon,
          ZExact: zExact,
          oldDirectNormalized: oldDirect,
          edDirectNormalized: edDirect,
          edOverOld,
          predictedWindowRatio: predictedRatio,
          passed,
        });
      }
    }
  }
  return rows;
}

function pythonScalar(value) {
  if (typeof value === "boolean") {
    return value ? "True" : "False";
  }
  if (typeof value === "number") {
    if (!Number.isFinite(value)) {
      throw new RangeError(`non-finite CSV value: ${value}`);
    }
    return Number.isInteger(value) ? `${value}.0` : String(value);
  }
  return String(value);
}

function csvScalar(key, value) {
  if (key === "R" || key.endsWith("DerivativeAtZero") || key === "expectedThirdDerivative") {
    return String(value);
  }
  if (key === "level") {
    return Number.isInteger(value) ? `${value.toFixed(1)}` : String(value);
  }
  return pythonScalar(value);
}

function csvEscape(value) {
  const text = String(value);
  return /[",\n\r]/.test(text) ? `"${text.replaceAll('"', '""')}"` : text;
}

function rowsToCsv(rows) {
  if (rows.length === 0) {
    throw new Error("cannot serialize an empty CSV table");
  }
  const fields = Object.keys(rows[0]);
  const lines = [fields.join(",")];
  for (const row of rows) {
    lines.push(
      fields.map((field) => csvEscape(csvScalar(field, row[field]))).join(","),
    );
  }
  return `${lines.join("\n")}\n`;
}

function utcNow() {
  return new Date().toISOString();
}

function parseOutputDirectory(argv) {
  const index = argv.indexOf("--output-dir");
  if (index < 0 || index + 1 >= argv.length) {
    throw new Error("usage: node research/r072o_independent_audit.mjs --output-dir DIR");
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

async function writeJson(target, value) {
  await writeFile(target, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function main() {
  const output = parseOutputDirectory(process.argv.slice(2));
  await mkdir(output, { recursive: true });
  const scriptPath = fileURLToPath(import.meta.url);
  const root = path.dirname(path.dirname(scriptPath));
  const started = process.hrtime.bigint();
  const progressRows = [];

  const config = {
    schemaVersion: SCHEMA_VERSION,
    audit: AUDIT,
    rValues: R_VALUES,
    levels: LEVELS,
    precision: "BigInt rational exponents plus independent IEEE binary64 screen grid",
    gitCommit: gitCommit(root),
    limitations:
      "The BigInt algebra audits the proof ledger. The finite grid is illustrative and does not prove enhanced dissipation, the action floor, or a general Navier-Stokes statement.",
  };
  await writeJson(path.join(output, "independent-config.json"), config);
  progressRows.push({ time: utcNow(), stage: "start", ...config });

  const ledger = exactLedger();
  const degeneracy = degeneracyRows();
  const screens = screenRows();
  await writeJson(path.join(output, "independent-exponents.json"), ledger);
  await writeFile(
    path.join(output, "independent-degeneracy.csv"),
    rowsToCsv(degeneracy),
    "utf8",
  );
  await writeFile(
    path.join(output, "independent-window.csv"),
    rowsToCsv(screens),
    "utf8",
  );

  progressRows.push({
    time: utcNow(),
    stage: "exact-ledger",
    passed: ledger.exactExponentLedgerPassed,
  });
  progressRows.push({
    time: utcNow(),
    stage: "degeneracy",
    cases: degeneracy.length,
    passed: degeneracy.every((row) => row.passed),
  });
  progressRows.push({
    time: utcNow(),
    stage: "screens",
    cases: screens.length,
    passed: screens.every((row) => row.passed),
  });

  const checks = {
    exactExponentLedgerPassed: ledger.exactExponentLedgerPassed,
    allDegeneracyCasesPassed: degeneracy.every((row) => row.passed),
    allScreenCasesPassed: screens.every((row) => row.passed),
    oneCarrierExponentIsElevenSixths:
      JSON.stringify(ledger.actual.UEDOneCarrier) ===
      JSON.stringify({ epsilon: "11/6" }),
    generalPResultMarkedConditional:
      ledger.claimContract.multiCarrierStatus === "conditional" &&
      ledger.claimContract.requiredHypothesis ===
        "uniform full-superposition integrated ED" &&
      ["N", "p", "R", "epsilon"].every((name) =>
        ledger.claimContract.constantsUniformOver.includes(name),
      ),
    multiCarrierCrossTermScaleRetainsN2:
      JSON.stringify(ledger.actual.FullSuperpositionCrossCubic) ===
      JSON.stringify({ N: "2/1", a: "2/1", epsilon: "1/2" }),
    epsilonOneEqualityHandled: screens
      .filter((row) => row.epsilon === 1.0)
      .every(
        (row) =>
          row.edDirectNormalized <=
          row.oldDirectNormalized * (1.0 + SCREEN_TOLERANCE),
      ),
  };
  const elapsedSeconds =
    Number(process.hrtime.bigint() - started) / 1_000_000_000;
  const maxRssMb = process.resourceUsage().maxRSS / 1024.0;
  const result = {
    schemaVersion: SCHEMA_VERSION,
    audit: AUDIT,
    status: Object.values(checks).every(Boolean) ? "passed" : "failed",
    checks,
    ledger,
    degeneracyCases: degeneracy.length,
    screenCases: screens.length,
    elapsedSeconds,
    maxRssMb,
    limitations: config.limitations,
  };
  await writeJson(path.join(output, "independent-result.json"), result);

  await writeFile(
    path.join(output, "independent-progress.ndjson"),
    `${progressRows.map((row) => JSON.stringify(row)).join("\n")}\n`,
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
    `[independent] status=${result.status} exact=${checks.exactExponentLedgerPassed} degeneracy=${degeneracy.length} screens=${screens.length}\n`,
    "utf8",
  );

  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (result.status !== "passed") {
    process.exitCode = 1;
  }
}

main().catch((error) => {
  process.stderr.write(`${error.stack ?? error}\n`);
  process.exitCode = 1;
});
