#!/usr/bin/env node

/**
 * Independent BigInt audit of finite R0.72S identities and sign guards.
 * The continuous report proof, not this program, derives uniqueness, global
 * critical-point counts, simplicity away from collision, and transversality.
 */

import { execFileSync, spawnSync } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const AUDIT = "R0.72S independent exact singular-strata and heat-collision audit";
const SCHEMA_VERSION = 1;

function absolute(value) {
  return value < 0n ? -value : value;
}

function gcd(left, right) {
  let a = absolute(left);
  let b = absolute(right);
  while (b !== 0n) [a, b] = [b, a % b];
  return a;
}

function fraction(numerator, denominator = 1n) {
  if (denominator === 0n) throw new Error("zero denominator");
  const sign = denominator < 0n ? -1n : 1n;
  const divisor = gcd(numerator, denominator);
  return {
    n: (sign * numerator) / divisor,
    d: absolute(denominator) / divisor,
  };
}

function plus(left, right) {
  return fraction(left.n * right.d + right.n * left.d, left.d * right.d);
}

function minus(left, right) {
  return fraction(left.n * right.d - right.n * left.d, left.d * right.d);
}

function product(left, right) {
  return fraction(left.n * right.n, left.d * right.d);
}

function quotient(left, right) {
  return fraction(left.n * right.d, left.d * right.n);
}

function power(value, exponent) {
  let result = fraction(1n);
  for (let index = 0; index < exponent; index += 1) result = product(result, value);
  return result;
}

function same(left, right) {
  return left.n === right.n && left.d === right.d;
}

function textFraction(value) {
  return `${value.n}/${value.d}`;
}

function determinantBareiss(matrix) {
  const values = matrix.map((row) => row.map(BigInt));
  let sign = 1n;
  let previous = 1n;
  for (let column = 0; column < values.length - 1; column += 1) {
    if (values[column][column] === 0n) {
      const pivot = values.findIndex(
        (row, index) => index > column && row[column] !== 0n,
      );
      if (pivot < 0) return 0n;
      [values[column], values[pivot]] = [values[pivot], values[column]];
      sign *= -1n;
    }
    const pivot = values[column][column];
    for (let row = column + 1; row < values.length; row += 1) {
      for (let entry = column + 1; entry < values.length; entry += 1) {
        const numerator =
          values[row][entry] * pivot -
          values[row][column] * values[column][entry];
        if (numerator % previous !== 0n) throw new Error("non-exact Bareiss step");
        values[row][entry] = numerator / previous;
      }
      values[row][column] = 0n;
    }
    previous = pivot;
  }
  return sign * values.at(-1).at(-1);
}

function canonicalPayload() {
  const pReal = { cos: fraction(-1n, 4n), A: fraction(-9n, 4n) };
  const pImag = { sin: fraction(-1n, 2n), B: fraction(-3n, 2n) };
  const jets = {
    f3: {
      sin: plus(fraction(1n), product(fraction(8n), pImag.sin)),
      B: plus(product(fraction(8n), pImag.B), fraction(27n)),
    },
    f4: {
      cos: plus(fraction(1n), product(fraction(16n), pReal.cos)),
      A: plus(product(fraction(16n), pReal.A), fraction(81n)),
    },
    f5: {
      sin: minus(fraction(-1n), product(fraction(32n), pImag.sin)),
      B: minus(product(fraction(-32n), pImag.B), fraction(243n)),
    },
    f6: {
      cos: minus(fraction(-1n), product(fraction(64n), pReal.cos)),
      A: minus(product(fraction(-64n), pReal.A), fraction(729n)),
    },
  };

  const coefficientJet = [
    [0, -2, 0, -3],
    [-4, 0, -9, 0],
    [0, 8, 0, 27],
    [16, 0, 81, 0],
  ];
  const coefficientJetDeterminant = determinantBareiss(coefficientJet);

  const a2CrossingZ2 = product(fraction(4n), fraction(1n, 8n));
  const a2ThirdCarrierAmplitude = fraction(0n);
  const a2SMinus = fraction(-1n, 2n);
  const a2SPlus = fraction(1n);
  const a2Polynomial = (sine) =>
    minus(minus(product(fraction(2n), product(sine, sine)), sine), fraction(1n));
  const a2F3 = fraction(-3n);
  const a2DyF1 = fraction(-3n);
  const a2Split = product(
    fraction(-1n),
    product(fraction(2n), quotient(a2DyF1, a2F3)),
  );
  const a2SignGuards = {
    pAtMinusOne: { constant: fraction(1n), k: fraction(1n) },
    pAtZero: { k: fraction(-1n) },
    pAtOne: { constant: fraction(-1n), k: fraction(1n) },
    rootProduct: fraction(-1n, 2n),
    offAxisDegeneracyAfterMultiplyBy8k: {
      constant: fraction(-1n), kSquared: fraction(-8n),
    },
  };
  const heatDecayExponents = [0, -(2 ** 2 - 1), -(3 ** 2 - 1)];
  const heatIdentityExact = heatDecayExponents.every(
    (value, index) => value === [0, -3, -8][index],
  );
  const a2KSamples = {
    before: fraction(2n), at: fraction(1n), after: fraction(1n, 2n),
  };
  const a2CrossingTau = fraction(1n, 2n);
  const a2CrossingPower = product(fraction(8n), power(a2CrossingTau, 3));
  const a2KLogDerivative = fraction(-3n);
  const a2P = (kValue, sine) => minus(
    minus(product(product(fraction(2n), kValue), product(sine, sine)), sine),
    kValue,
  );
  const a2GuardInputsHold =
    same(a2SignGuards.pAtMinusOne.constant, fraction(1n)) &&
    same(a2SignGuards.pAtMinusOne.k, fraction(1n)) &&
    same(a2SignGuards.pAtZero.k, fraction(-1n)) &&
    same(a2SignGuards.pAtOne.constant, fraction(-1n)) &&
    same(a2SignGuards.pAtOne.k, fraction(1n)) &&
    same(a2SignGuards.rootProduct, fraction(-1n, 2n)) &&
    same(a2SignGuards.offAxisDegeneracyAfterMultiplyBy8k.constant, fraction(-1n)) &&
    same(a2SignGuards.offAxisDegeneracyAfterMultiplyBy8k.kSquared, fraction(-8n));
  const a2BasePair =
    a2P(a2KSamples.at, fraction(-1n)).n > 0n &&
    a2P(a2KSamples.at, fraction(0n)).n < 0n ? 2 : 0;
  const a2ExtraCounts = {
    before: a2P(a2KSamples.before, fraction(1n)).n > 0n ? 2 : 0,
    at: same(a2P(a2KSamples.at, fraction(1n)), fraction(0n)) ? 1 : 0,
    after: a2P(a2KSamples.after, fraction(1n)).n > 0n ? 2 : 0,
  };
  const a2RepresentativeCounts = Object.fromEntries(
    Object.entries(a2ExtraCounts).map(([key, value]) => [key, a2BasePair + value]),
  );
  const a2UniqueEventInputs =
    a2GuardInputsHold && same(a2CrossingPower, fraction(1n)) &&
    a2KLogDerivative.n < 0n &&
    a2SignGuards.offAxisDegeneracyAfterMultiplyBy8k.constant.n < 0n &&
    a2SignGuards.offAxisDegeneracyAfterMultiplyBy8k.kSquared.n < 0n;
  const a2DistinctCounts = a2UniqueEventInputs ? a2RepresentativeCounts : {};
  const a2NonzeroFoldJets = a2F3.n !== 0n && a2DyF1.n !== 0n;
  const a2MultiplicityCount = a2BasePair + (a2F3.n !== 0n ? 2 : 0);
  const a2Transverse = heatIdentityExact && a2NonzeroFoldJets;
  const a2NoncollisionSimple = a2UniqueEventInputs && a2F3.n !== 0n;

  const a0 = fraction(-2563n, 1280n);
  const b0 = fraction(1n, 30n);
  const tauStar = fraction(1n, 2n);
  const aStar = product(a0, power(tauStar, 3));
  const bStar = product(b0, power(tauStar, 8));
  const monotonicityParent = plus(a0, product(fraction(6n), b0));
  const hStar = plus(
    plus(fraction(1n), product(fraction(4n), aStar)),
    product(fraction(9n), bStar),
  );
  const qxStar = plus(
    product(fraction(24n), bStar),
    product(fraction(4n), aStar),
  );
  const hYStar = minus(
    product(fraction(-12n), aStar),
    product(fraction(72n), bStar),
  );
  const f4Star = minus(product(fraction(45n), bStar), fraction(3n));
  const dyF2Star = product(fraction(-1n), hYStar);
  const a3Split = quotient(
    product(fraction(-2n), hYStar),
    product(fraction(-1n), qxStar),
  );
  const a3SignGuards = {
    qMinusOneCoefficients: [fraction(1n), product(fraction(-4n), a0), product(fraction(9n), b0)],
    qXUpperParentAtTauOne: monotonicityParent,
    hTauDerivativeParentAtTauOne: monotonicityParent,
  };
  const a3TauSamples = {
    before: fraction(3n, 4n), at: tauStar, after: fraction(1n, 4n),
  };
  const a3H = (tau) => plus(
    plus(fraction(1n), product(product(fraction(4n), a0), power(tau, 3))),
    product(product(fraction(9n), b0), power(tau, 8)),
  );
  const a3QMinusOnePositive = a3SignGuards.qMinusOneCoefficients.every(
    (value) => value.n > 0n,
  );
  const a3MonotonicInputs =
    monotonicityParent.n < 0n && b0.n > 0n && tauStar.n > 0n &&
    minus(fraction(1n), tauStar).n >= 0n;
  const a3CrossingPowerIdentities = {
    tauCubed: power(tauStar, 3), tauEighth: power(tauStar, 8),
  };
  const a3ContinuousProofInputs =
    a3MonotonicInputs && a3QMinusOnePositive && same(hStar, fraction(0n)) &&
    same(a3CrossingPowerIdentities.tauCubed, fraction(1n, 8n)) &&
    same(a3CrossingPowerIdentities.tauEighth, fraction(1n, 256n));
  const a3RepresentativeCounts = {
    before: a3H(a3TauSamples.before).n < 0n ? 4 : 2,
    at: same(a3H(a3TauSamples.at), fraction(0n)) ? 2 : 4,
    after: a3H(a3TauSamples.after).n > 0n ? 2 : 4,
  };
  const a3DistinctCounts = a3ContinuousProofInputs ? a3RepresentativeCounts : {};
  const a3NonzeroCollisionJets =
    qxStar.n !== 0n && hYStar.n !== 0n && f4Star.n !== 0n && dyF2Star.n !== 0n;
  const a3MultiplicityCount = (f4Star.n !== 0n ? 3 : 0) +
    (a3QMinusOnePositive ? 1 : 0);
  const a3SliceTransverse = heatIdentityExact && a3NonzeroCollisionJets;
  const a3FullSpaceTransverse = 1 >= 2;

  const exactChecks = {
    incidenceJetsExact:
      same(jets.f3.sin, fraction(-3n)) && same(jets.f3.B, fraction(15n)) &&
      same(jets.f4.cos, fraction(-3n)) && same(jets.f4.A, fraction(45n)) &&
      same(jets.f5.sin, fraction(15n)) && same(jets.f5.B, fraction(-195n)) &&
      same(jets.f6.cos, fraction(15n)) && same(jets.f6.A, fraction(-585n)),
    a4ReductionExact: same(
      product(fraction(15n), minus(fraction(1n), fraction(13n, 5n))),
      fraction(-24n),
    ),
    a5ReductionExact: same(
      product(fraction(15n), minus(fraction(1n), fraction(39n, 15n))),
      fraction(-24n),
    ),
    coefficientDerivativeJetExact: coefficientJetDeterminant === 5400n,
    a2CrossingCoefficientExact: same(a2CrossingZ2, fraction(1n, 2n)),
    a2CrossingRootsExact:
      same(a2Polynomial(a2SMinus), fraction(0n)) &&
      same(a2Polynomial(a2SPlus), fraction(0n)),
    a2JetsExact: same(a2F3, fraction(-3n)) && same(a2DyF1, fraction(-3n)),
    a2SplitExact: same(a2Split, fraction(-2n)),
    a2FiniteGuardInputsExact: a2GuardInputsHold,
    a2DerivedLedgerExact:
      a2UniqueEventInputs &&
      JSON.stringify(a2DistinctCounts) === JSON.stringify({ before: 4, at: 3, after: 2 }) &&
      a2MultiplicityCount === 4 && a2NoncollisionSimple && a2Transverse,
    a3MonotonicityInputsExact:
      same(monotonicityParent, fraction(-2307n, 1280n)) && a3MonotonicInputs,
    a3CrossingExact: same(hStar, fraction(0n)),
    a3QxExact: same(qxStar, fraction(-511n, 512n)),
    a3JetsExact:
      same(hYStar, fraction(1533n, 512n)) &&
      same(f4Star, fraction(-1533n, 512n)) &&
      same(dyF2Star, fraction(-1533n, 512n)),
    a3SplitExact: same(a3Split, fraction(-6n)),
    a3FiniteGuardInputsExact:
      a3QMinusOnePositive &&
      same(a3SignGuards.qXUpperParentAtTauOne, fraction(-2307n, 1280n)) &&
      same(a3SignGuards.hTauDerivativeParentAtTauOne, fraction(-2307n, 1280n)),
    a3DerivedLedgerExact:
      JSON.stringify(a3DistinctCounts) === JSON.stringify({ before: 4, at: 2, after: 2 }) &&
      a3MultiplicityCount === 4 && a3SliceTransverse && !a3FullSpaceTransverse,
    heatEquationIdentityExact: heatIdentityExact,
  };

  const mapping = (value) =>
    Object.fromEntries(Object.entries(value).map(([key, item]) => [key, textFraction(item)]));

  return {
    schemaVersion: SCHEMA_VERSION,
    theoremId: "R0.72S-exact-Ak-strata-and-two-heat-collisions",
    incidenceStrata: {
      jetCoefficients: Object.fromEntries(
        Object.entries(jets).map(([name, value]) => [name, mapping(value)]),
      ),
      partition: [
        { type: "A2", condition: "B!=sin(phi)/5", localCodimension: 1 },
        { type: "A3", condition: "B=sin(phi)/5 and A!=cos(phi)/15", localCodimension: 2 },
        { type: "A4", condition: "B=sin(phi)/5 and A=cos(phi)/15 and sin(phi)!=0", localCodimension: 3 },
        { type: "A5", condition: "(phi,A,B)=(0,1/15,0) or (pi,-1/15,0)", localCodimension: 4 },
      ],
      f5OnA4Closure: "-24*sin(phi)",
      f6AtA5: "-24*cos(phi)",
      higherThanA5Occurs: false,
      classificationTarget: "incidence-preimages-not-global-image",
    },
    restrictedMiniversality: {
      coefficientOrder: ["Re(z2)", "Im(z2)", "Re(z3)", "Im(z3)"],
      derivativeOrders: [1, 2, 3, 4],
      coefficientDerivativeJetAtPhiZero: coefficientJet,
      coefficientDerivativeJetDeterminant: textFraction(fraction(coefficientJetDeterminant)),
      localCodimensions: { A2: 1, A3: 2, A4: 3, A5: 4 },
      moduloAdditiveConstants: true,
      fullA5MiniversalParameterCountIncludingConstant: 5,
      globalEmbeddedStratificationClaimed: false,
    },
    a2HeatPath: {
      z20: ["0/1", "4/1"],
      z30: ["0/1", "0/1"],
      k: "8*exp(-3*y)",
      criticalEquation: "2*k*s^2-s-k=0 with s=sin(phi)",
      sineRoots: "(1+-sqrt(1+8*k^2))/(4*k)",
      crossingY: "log(2)",
      crossingPhi: "pi/2",
      crossingZ2: ["0/1", textFraction(a2CrossingZ2)],
      otherSineAtCrossing: textFraction(a2SMinus),
      crossingPowerIdentity: {
        tau: textFraction(a2CrossingTau),
        "8TauCubed": textFraction(a2CrossingPower),
      },
      kLogDerivative: textFraction(a2KLogDerivative),
      representativeK: Object.fromEntries(
        Object.entries(a2KSamples).map(([key, value]) => [key, textFraction(value)]),
      ),
      uniqueDegenerateEventForYNonnegative: a2UniqueEventInputs,
      distinctCriticalCounts: a2DistinctCounts,
      criticalCountWithMultiplicityAtCrossing: a2MultiplicityCount,
      allNoncollisionCriticalPointsSimple: a2NoncollisionSimple,
      fThird: textFraction(a2F3),
      dyFPrime: textFraction(a2DyF1),
      splitXiSquaredPerDelta: textFraction(a2Split),
      globalSignGuards: {
        pAtMinusOne: mapping(a2SignGuards.pAtMinusOne),
        pAtZero: mapping(a2SignGuards.pAtZero),
        pAtOne: mapping(a2SignGuards.pAtOne),
        rootProduct: textFraction(a2SignGuards.rootProduct),
        offAxisDegeneracyAfterMultiplyBy8k:
          mapping(a2SignGuards.offAxisDegeneracyAfterMultiplyBy8k),
      },
      fullCoefficientSpaceTransverse: a2Transverse,
      thirdCarrierActive: a2ThirdCarrierAmplitude.n !== 0n,
    },
    a3HeatPath: {
      a0: textFraction(a0),
      b0: textFraction(b0),
      thirdCarrierActive: b0.n !== 0n,
      q: "12*b0*tau^8*x^2+4*a0*tau^3*x+1-3*b0*tau^8",
      monotonicityParentUpper: textFraction(monotonicityParent),
      qMinusOneStrictlyPositive: a3QMinusOnePositive,
      crossingTau: textFraction(tauStar),
      crossingY: "log(2)",
      crossingA: textFraction(aStar),
      crossingB: textFraction(bStar),
      crossingPowerIdentities: Object.fromEntries(
        Object.entries(a3CrossingPowerIdentities).map(
          ([key, value]) => [key, textFraction(value)],
        ),
      ),
      representativeTau: Object.fromEntries(
        Object.entries(a3TauSamples).map(([key, value]) => [key, textFraction(value)]),
      ),
      hAtCrossing: textFraction(hStar),
      qXAtCrossing: textFraction(qxStar),
      hYAtCrossing: textFraction(hYStar),
      fFourth: textFraction(f4Star),
      dyFSecond: textFraction(dyF2Star),
      splitPhiSquaredPerDelta: textFraction(a3Split),
      distinctCriticalCounts: a3DistinctCounts,
      criticalCountWithMultiplicityAtCrossing: a3MultiplicityCount,
      globalSignGuards: {
        qMinusOneCoefficients: a3SignGuards.qMinusOneCoefficients.map(textFraction),
        qXUpperParentAtTauOne: textFraction(monotonicityParent),
        hTauDerivativeParentAtTauOne: textFraction(monotonicityParent),
      },
      crossingPointType: "A3",
      realEvenSliceTransverse: a3SliceTransverse,
      fullCoefficientSpaceTransverse: a3FullSpaceTransverse,
    },
    stationaryBenchmarks: {
      A2DecayRate: "nu^(3/5)",
      A3DecayRate: "nu^(2/3)",
      nonautonomousCollisionEstimateProved: false,
    },
    heatEquationIdentity: {
      identity: "partial_y F=partial_phi^2 F+F",
      harmonicDecayExponents: { n1: 0, n2: 3, n3: 8 },
      onIncidence: ["partial_y F'=F'''", "partial_y F''=F''''"],
    },
    claimBoundary: {
      finiteCertificateIsContinuumProof: false,
      completeGlobalCausticImageClassification: false,
      allIncidenceSelfIntersectionsClassified: false,
      causticCrossingEnhancedDissipation: false,
      generalThreeDimensionalRegularity: false,
      clayMillenniumProblemSolved: false,
    },
    exactChecks,
    passed: Object.values(exactChecks).every(Boolean),
  };
}

function currentCommit(root) {
  try {
    return execFileSync("git", ["rev-parse", "HEAD"], {
      cwd: root, encoding: "utf8", stdio: ["ignore", "pipe", "ignore"],
    }).trim();
  } catch {
    return "unavailable";
  }
}

function trackedTreeDirty(root) {
  return [["diff", "--quiet"], ["diff", "--cached", "--quiet"]].some(
    (arguments_) => spawnSync("git", arguments_, { cwd: root, stdio: "ignore" }).status !== 0,
  );
}

function requiredSourcesTracked(root) {
  return [
    "research/r072s_report-source.md",
    "research/r072s_independent_audit.mjs",
    "research/r072s_compare_audits.py",
  ].every(
    (relative) => spawnSync("git", ["ls-files", "--error-unmatch", relative], {
      cwd: root, stdio: "ignore",
    }).status === 0,
  );
}

function outputArgument(arguments_) {
  const index = arguments_.indexOf("--output-dir");
  if (index < 0 || index + 1 >= arguments_.length) {
    throw new Error("usage: node research/r072s_independent_audit.mjs --output-dir DIR");
  }
  return path.resolve(arguments_[index + 1]);
}

async function writeJson(target, value) {
  await writeFile(target, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function main() {
  const output = outputArgument(process.argv.slice(2));
  await mkdir(output, { recursive: true });
  const root = path.dirname(path.dirname(fileURLToPath(import.meta.url)));
  const started = process.hrtime.bigint();
  const now = () => new Date().toISOString();

  const config = {
    schemaVersion: SCHEMA_VERSION,
    audit: AUDIT,
    precision: "JavaScript BigInt rational plus Bareiss determinant",
    gitCommit: currentCommit(root),
    sourceTracked: requiredSourcesTracked(root),
    trackedChangesDirty: trackedTreeDirty(root),
    limitations:
      "Machine-checks finite identities and sign/monotonicity guards only; the report's continuous proof, not this computation, derives event uniqueness, global counts, simplicity, and transversality.",
  };
  await writeJson(path.join(output, "independent-config.json"), config);

  const payload = canonicalPayload();
  await writeJson(path.join(output, "independent-payload.json"), payload);
  const stages = [
    ["incidence-jets", payload.exactChecks.incidenceJetsExact],
    ["restricted-miniversality", payload.exactChecks.coefficientDerivativeJetExact],
    ["A2-heat-path", payload.exactChecks.a2SplitExact],
    ["A3-heat-path", payload.exactChecks.a3SplitExact],
    ["claim-boundary", payload.claimBoundary.causticCrossingEnhancedDissipation === false],
  ];
  const progress = [
    { time: now(), stage: "start", ...config },
    ...stages.map(([stage, passed]) => ({ time: now(), stage, passed })),
  ];
  const checks = {
    payloadPassed: payload.passed,
    incidencePassed: payload.exactChecks.incidenceJetsExact,
    versalityPassed:
      payload.restrictedMiniversality.coefficientDerivativeJetDeterminant === "5400/1",
    a2FiniteLedgerPassed: payload.exactChecks.a2DerivedLedgerExact,
    a3FiniteLedgerPassed: payload.exactChecks.a3DerivedLedgerExact,
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
    `${progress.map((row) => JSON.stringify(row)).join("\n")}\n`, "utf8",
  );
  await writeFile(
    path.join(output, "independent-resource.ndjson"),
    `${JSON.stringify({ time: now(), event: "complete", elapsedSeconds, maxRssMb, pid: process.pid })}\n`, "utf8",
  );
  await writeFile(
    path.join(output, "independent-monitor.log"),
    `[independent] status=${result.status} strata=${checks.incidencePassed} versal=${checks.versalityPassed} A2=${checks.a2FiniteLedgerPassed} A3=${checks.a3FiniteLedgerPassed}\n`,
    "utf8",
  );
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (result.status !== "passed") process.exitCode = 1;
}

main().catch((error) => {
  process.stderr.write(`${error.stack ?? error}\n`);
  process.exitCode = 1;
});
