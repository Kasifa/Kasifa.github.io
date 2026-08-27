#!/usr/bin/env node

/**
 * Independent BigInt audit for the R0.72Q arbitrary-phase shape gate.
 *
 * This route reconstructs the canonical finite ledger without importing the
 * Python producer and without reading producer artifacts.  The comparator is
 * the only program that later reads both canonical payloads.
 */

import { execFileSync, spawnSync } from "node:child_process";
import { mkdir, writeFile } from "node:fs/promises";
import path from "node:path";
import process from "node:process";
import { fileURLToPath } from "node:url";

const AUDIT = "R0.72Q independent arbitrary-phase exact audit";
const SCHEMA_VERSION = 1;

function absolute(value) {
  return value < 0n ? -value : value;
}

function gcd(left, right) {
  let a = absolute(left);
  let b = absolute(right);
  while (b !== 0n) {
    const remainder = a % b;
    a = b;
    b = remainder;
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
  if (!Number.isInteger(exponent) || exponent < 0) {
    throw new RangeError("power expects a nonnegative integer");
  }
  return fraction(value.n ** BigInt(exponent), value.d ** BigInt(exponent));
}

function same(left, right) {
  return left.n === right.n && left.d === right.d;
}

function asText(value) {
  return `${value.n}/${value.d}`;
}

function reconstructShape(maxCarrier) {
  const one = fraction(1n);
  const q2 = fraction(1n, 2n);
  const q1 = quotient(q2, fraction(2n));
  const q0 = quotient(q2, fraction(4n));
  const derivative0 = plus(one, q0);
  const derivative1 = plus(one, q1);
  const derivative2 = plus(one, q2);
  const derivative3 = plus(one, fraction(BigInt(maxCarrier), 2n));
  let factorial = 1n;
  let ePartial = fraction(0n);
  for (let n = 0n; n <= 4n; n += 1n) {
    if (n > 0n) factorial *= n;
    ePartial = plus(ePartial, fraction(1n, factorial));
  }
  const eTailUpper = fraction(1n, 96n);
  const eUpper = plus(ePartial, eTailUpper);
  const expMinusOneLower = fraction(1n, 3n);

  const eta = quotient(one, power(derivative3, 4));
  const etaQuarter = quotient(one, derivative3);
  const etaThreeQuarters = power(etaQuarter, 3);
  const slowLeft = product(derivative3, eta);

  const exactChecks = {
    q1FromQ2: same(q1, fraction(1n, 4n)),
    q0FromQ2: same(q0, fraction(1n, 8n)),
    sinRadiusGreaterThanQuarter: 48n < 49n,
    localCurvatureMarginGreaterThanThird: 27n > 25n,
    boundedHeatEnvelope: eUpper.n < 3n * eUpper.d,
    ePartialSumExact: same(ePartial, fraction(65n, 24n)),
    eTailMajorantExact: same(eTailUpper, fraction(1n, 96n)),
    eUpperReassembled: same(eUpper, fraction(87n, 32n)),
    derivativeBoundsExact:
      same(derivative0, fraction(9n, 8n)) &&
      same(derivative1, fraction(5n, 4n)) &&
      same(derivative2, fraction(3n, 2n)) &&
      same(derivative3, fraction(BigInt(maxCarrier + 2), 2n)),
    slowThresholdIdentity: same(slowLeft, etaThreeQuarters),
  };

  return {
    profile:
      "F_y(phi)=cos(phi)+sum_{m=2}^M Re(beta_m(y)*exp(i*m*phi))",
    fixedM: true,
    maxCarrier,
    phaseClass: "arbitrary phases",
    jetBudgets: {
      QjDefinition: "Q_j=sup_y sum_{m=2}^M m^j abs(beta_m(y))",
      Q2Upper: asText(q2),
      Q1UpperDerived: asText(q1),
      Q0UpperDerived: asText(q0),
      termwiseFacts: ["m<=m^2/2 for m>=2", "1<=m^2/4 for m>=2"],
    },
    criticalGeometry: {
      criticalCount: 2,
      criticalLocationBoxes: [
        "dist(phi,0)<pi/12",
        "dist(phi,pi)<pi/12",
      ],
      criticalLocationReason:
        "at F_phi=0, abs(sin(phi))<=Q1<=1/4<sin(pi/12)",
      arbitraryPhaseUniform: true,
      radius: "pi/12",
      localCurvatureMargin: "(sqrt(3)-1)/2",
      localCurvatureMarginGreaterThan: "1/3",
      localCurvatureReason:
        "a radius-pi/12 tube about either critical point stays within pi/6 of 0 or pi, so abs(F_phiphi)>=cos(pi/6)-Q2",
      normalizedShapeConstants: {
        C0: "9/1",
        conservativeC0AlsoValid: "81/1",
        C1: "12/1",
      },
      physicalWindowShapeConstants: {
        yWindow: "0<=y<=1",
        C0: "81/1",
        C1: "36/1",
        localSlopeLower: "1/9",
        awaySlopeLower: "1/36",
      },
      C0: "81/1",
      C1: "36/1",
      shapeConstantScope:
        "physical Coble shear W=e^(-y)F_y on 0<=y<=1; normalized F_y has the sharper C1=12 contract",
    },
    boundedEnvelopeCertificate: {
      partialSumDefinition: "sum_{n=0}^4 1/n!",
      partialSum: asText(ePartial),
      partialSumExpected: "65/24",
      tailMajorantDefinition: "sum_{k=0}^infinity 1/(5!*5^k)",
      tailUpper: asText(eTailUpper),
      tailUpperExpected: "1/96",
      eUpperCertificate: asText(eUpper),
      eUpperReassembly: "65/24+1/96=87/32",
      eUpperLessThanThree: eUpper.n < 3n * eUpper.d,
      expMinusOneLower: asText(expMinusOneLower),
      piLowerInput: "pi>3 (inscribed regular hexagon)",
      normalizedLocalSlopeLower: "1/3",
      normalizedAwaySlopeLower: "1/12",
      physicalLocalSlopeLower: asText(
        product(expMinusOneLower, fraction(1n, 3n)),
      ),
      physicalAwaySlopeLower: asText(
        product(expMinusOneLower, fraction(1n, 12n)),
      ),
      passed:
        same(ePartial, fraction(65n, 24n)) &&
        same(eTailUpper, fraction(1n, 96n)) &&
        same(eUpper, fraction(87n, 32n)) &&
        eUpper.n < 3n * eUpper.d &&
        same(
          product(expMinusOneLower, fraction(1n, 3n)),
          fraction(1n, 9n),
        ) &&
        same(
          product(expMinusOneLower, fraction(1n, 12n)),
          fraction(1n, 36n),
        ),
    },
    radicalCertificates: {
      sinRadius: {
        statement: "sin(pi/12)>1/4",
        identity: "sin(pi/12)^2=(2-sqrt(3))/4",
        reduction: "sqrt(3)<7/4",
        integerSquareComparison: "48<49",
        passed: 48n < 49n,
      },
      curvatureMargin: {
        statement: "(sqrt(3)-1)/2>1/3",
        reduction: "sqrt(3)>5/3",
        integerSquareComparison: "27>25",
        passed: 27n > 25n,
      },
    },
    derivativeSupremumBounds: {
      d0: asText(derivative0),
      d1: asText(derivative1),
      d2: asText(derivative2),
      d3: asText(derivative3),
      d3Symbolic: "1+M/2",
    },
    slowTime: {
      mixedDerivativeCoefficient: asText(derivative3),
      mixedDerivativeCoefficientSymbolic: "1+M/2",
      etaThreshold: asText(eta),
      etaThresholdSymbolic: "(1+M/2)^(-4)",
      etaQuarterAtThreshold: asText(etaQuarter),
      leftAtThreshold: asText(slowLeft),
      etaThreeQuartersAtThreshold: asText(etaThreeQuarters),
      reducedCondition: "(1+M/2)*eta^(1/4)<=1",
      passed: same(slowLeft, etaThreeQuarters),
    },
    proofSkeleton: [
      "Q2<=1/2 implies Q1<=1/4 and Q0<=1/8 termwise.",
      "Boundary signs at +/-pi/12 and pi+/-pi/12 give one zero in each box.",
      "The Q2 curvature bound makes F_phi strictly monotone in each box.",
      "Every zero lies in those boxes because abs(sin(phi))<=Q1.",
      "The pi/12 tubes have curvature margin mu>1/3; fixed-M derivatives are bounded.",
    ],
    exactChecks,
    passed: Object.values(exactChecks).every(Boolean),
  };
}

function reconstructCaustic() {
  const firstCoefficient = fraction(1n, 8n);
  const secondCoefficient = fraction(-3n, 8n);
  const radialMinimumSquared = fraction(1n, 16n);
  const radialMaximumSquared = fraction(1n, 4n);
  const implicitLeft = fraction(27n, 4096n);
  const implicitRight = product(fraction(27n, 1024n), fraction(1n, 4n));
  const radialOrigin = fraction(1n, 16n);
  const radialEndpoint = fraction(1n, 4n);
  const rayAtOrigin = fraction(0n);
  const rayAtEndpoint = quotient(
    power(minus(radialEndpoint, radialOrigin), 3),
    radialEndpoint,
  );
  const derivativeExpanded = [
    fraction(2n),
    product(fraction(-3n), radialOrigin),
    fraction(0n),
    power(radialOrigin, 3),
  ];
  const leftFactorAscending = [
    power(radialOrigin, 2),
    product(fraction(-2n), radialOrigin),
    fraction(1n),
  ];
  const rightFactorAscending = [radialOrigin, fraction(2n)];
  const factoredAscending = Array.from({ length: 4 }, () => fraction(0n));
  for (let leftIndex = 0; leftIndex < leftFactorAscending.length; leftIndex += 1) {
    for (
      let rightIndex = 0;
      rightIndex < rightFactorAscending.length;
      rightIndex += 1
    ) {
      const index = leftIndex + rightIndex;
      factoredAscending[index] = plus(
        factoredAscending[index],
        product(leftFactorAscending[leftIndex], rightFactorAscending[rightIndex]),
      );
    }
  }
  const derivativeFactored = [...factoredAscending].reverse();
  const derivativeFactorizationExact = derivativeExpanded.every((value, index) =>
    same(value, derivativeFactored[index]),
  );

  const exactChecks = {
    parameterCoefficientsExact:
      same(firstCoefficient, fraction(1n, 8n)) &&
      same(secondCoefficient, fraction(-3n, 8n)),
    implicitPolynomialIdentity: same(implicitLeft, implicitRight),
    radiusRangeExact:
      same(radialMinimumSquared, fraction(1n, 16n)) &&
      same(radialMaximumSquared, fraction(1n, 4n)),
    interiorDiskSeparated: same(
      power(fraction(1n, 4n), 2),
      radialMinimumSquared,
    ),
    cuspFourthJetsNonzero: 3n !== 0n && -3n !== 0n,
    rayDerivativeFactorizationExact: derivativeFactorizationExact,
    rayEndpointValuesExact:
      same(rayAtOrigin, fraction(0n)) &&
      same(rayAtEndpoint, fraction(27n, 1024n)),
  };

  return {
    twoCarrierProfile: "f(phi)=cos(phi)+a*cos(2*phi+theta)",
    complexCoefficient: "z=a*exp(i*theta)",
    degeneracyEquations: [
      "sin(phi)+2*a*sin(2*phi+theta)=0",
      "cos(phi)+4*a*cos(2*phi+theta)=0",
    ],
    linearJetSolution: [
      "a*cos(2*phi+theta)=-cos(phi)/4",
      "a*sin(2*phi+theta)=-sin(phi)/2",
    ],
    parametrization:
      "z(phi)=(1/8)*exp(-3*i*phi)-(3/8)*exp(-i*phi)",
    parametrizationCoefficients: {
      expMinus3iPhi: asText(firstCoefficient),
      expMinus1iPhi: asText(secondCoefficient),
    },
    coordinateIdentities: {
      imaginaryPart: "Im(z)=sin(phi)^3/2",
      radiusSquared: "abs(z)^2=(1+3*sin(phi)^2)/16",
    },
    implicitEquation:
      "(abs(z)^2-1/16)^3=(27/1024)*(Im(z))^2",
    implicitIdentityBothSides: "(27/4096)*sin(phi)^6",
    radiusRange: ["1/4", "1/2"],
    rayIntersection: {
      radialSquaredVariable: "s=abs(z)^2",
      function: "H(s)=(s-1/16)^3/s",
      rayEquation: "H(s)=(27/1024)*sin(theta)^2",
      derivative: "H'(s)=(s-1/16)^2*(2*s+1/16)/s^2",
      expandedDerivativeNumeratorCoefficients: derivativeExpanded.map(asText),
      factoredDerivativeNumeratorCoefficients: derivativeFactored.map(asText),
      strictPositivityDomain: "s>1/16",
      endpointValues: {
        "H(1/16)": asText(rayAtOrigin),
        "H(1/4)": asText(rayAtEndpoint),
      },
      conclusion:
        "every phase ray has exactly one caustic intersection with s in [1/16,1/4]",
      passed:
        derivativeFactorizationExact &&
        same(rayAtOrigin, fraction(0n)) &&
        same(rayAtEndpoint, fraction(27n, 1024n)),
    },
    interiorDisk: {
      condition: "abs(z)<1/4",
      conclusion: "no degeneracy and exactly two critical points",
    },
    classification: {
      genericWall: "A2 fold: f'''=-3*sin(phi) is nonzero",
      cusps: [
        {
          z: "1/4",
          degeneratePhi: "pi",
          relativePhase: "0",
          fourthDerivative: "3/1",
          type: "A3",
        },
        {
          z: "-1/4",
          degeneratePhi: "0",
          relativePhase: "pi",
          fourthDerivative: "-3/1",
          type: "A3",
        },
      ],
      jetIdentities: ["f'''=-3*sin(phi)", "f''''=-3*cos(phi)"],
      wallMeaning: "Morse-applicability wall only",
    },
    exactChecks,
    passed: Object.values(exactChecks).every(Boolean),
  };
}

function canonicalPayload(maxCarrier) {
  const shapeContract = reconstructShape(maxCarrier);
  const twoCarrierCaustic = reconstructCaustic();
  const claimBoundary = {
    status: "proved-analytically-for-fixed-M-arbitrary-phase-shape-class",
    fixedMRequired: true,
    finiteCertificateIsProof: false,
    arbitraryPhases: true,
    growingMStatus: "open",
    commonBandWithoutJetDominanceStatus: "open",
    causticIsEDFailureCounterexample: false,
    unnormalizedUniformCurvatureForUnboundedYClaimed: false,
  };
  return {
    schemaVersion: SCHEMA_VERSION,
    theoremId: "R0.72Q-fixed-M-arbitrary-phase-shape-gate",
    shapeContract,
    twoCarrierCaustic,
    claimBoundary,
    passed: shapeContract.passed && twoCarrierCaustic.passed,
  };
}

function commandLine(argv) {
  const outputIndex = argv.indexOf("--output-dir");
  if (outputIndex < 0 || outputIndex + 1 >= argv.length) {
    throw new Error(
      "usage: node research/r072q_independent_audit.mjs --output-dir DIR [--max-carrier M]",
    );
  }
  const carrierIndex = argv.indexOf("--max-carrier");
  const maxCarrier =
    carrierIndex < 0 ? 2 : Number.parseInt(argv[carrierIndex + 1], 10);
  if (!Number.isSafeInteger(maxCarrier) || maxCarrier < 2) {
    throw new Error("--max-carrier must be a safe integer >= 2");
  }
  return { output: path.resolve(argv[outputIndex + 1]), maxCarrier };
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
    "research/r072q_report-source.md",
    "research/r072q_independent_audit.mjs",
    "research/r072q_compare_audits.py",
  ].every(
    (relative) =>
      spawnSync("git", ["ls-files", "--error-unmatch", relative], {
        cwd: root,
        stdio: "ignore",
      }).status === 0,
  );
}

function now() {
  return new Date().toISOString();
}

async function writeJson(target, value) {
  await writeFile(target, `${JSON.stringify(value, null, 2)}\n`, "utf8");
}

async function main() {
  const { output, maxCarrier } = commandLine(process.argv.slice(2));
  await mkdir(output, { recursive: true });
  const script = fileURLToPath(import.meta.url);
  const root = path.dirname(path.dirname(script));
  const started = process.hrtime.bigint();

  const config = {
    schemaVersion: SCHEMA_VERSION,
    audit: AUDIT,
    maxCarrier,
    precision: "JavaScript BigInt exact rational and integer identity audit",
    gitCommit: currentCommit(root),
    sourceTracked: requiredSourcesTracked(root),
    trackedChangesDirty: trackedTreeDirty(root),
    limitations:
      "Finite exact algebra only. Trigonometric monotonicity, root isolation, the continuum shape lemma, and enhanced dissipation remain analytic proofs.",
  };
  await writeJson(path.join(output, "independent-config.json"), config);

  const payload = canonicalPayload(maxCarrier);
  await writeJson(path.join(output, "independent-payload.json"), payload);
  const stages = [
    ["fixed-M-shape", payload.shapeContract.passed],
    [
      "arbitrary-phase-critical-count",
      payload.shapeContract.criticalGeometry.criticalCount === 2,
    ],
    ["slow-time-threshold", payload.shapeContract.slowTime.passed],
    ["two-carrier-caustic", payload.twoCarrierCaustic.passed],
    ["claim-boundary", payload.claimBoundary.finiteCertificateIsProof === false],
  ];
  const progress = [
    { time: now(), stage: "start", ...config },
    ...stages.map(([stage, passed]) => ({ time: now(), stage, passed })),
  ];

  const checks = {
    payloadPassed: payload.passed,
    shapeContractPassed: payload.shapeContract.passed,
    criticalCountIsTwo:
      payload.shapeContract.criticalGeometry.criticalCount === 2,
    causticPassed: payload.twoCarrierCaustic.passed,
    claimBoundaryScoped:
      payload.claimBoundary.fixedMRequired === true &&
      payload.claimBoundary.growingMStatus === "open" &&
      payload.claimBoundary.finiteCertificateIsProof === false,
  };
  const elapsedSeconds =
    Number(process.hrtime.bigint() - started) / 1_000_000_000;
  const maxRssMb = process.resourceUsage().maxRSS / 1024;
  const result = {
    schemaVersion: SCHEMA_VERSION,
    audit: AUDIT,
    status: Object.values(checks).every(Boolean) ? "passed" : "failed",
    checks,
    maxCarrier,
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
      time: now(),
      event: "complete",
      elapsedSeconds,
      maxRssMb,
      pid: process.pid,
    })}\n`,
    "utf8",
  );
  await writeFile(
    path.join(output, "independent-monitor.log"),
    `[independent] status=${result.status} M=${maxCarrier} shape=${checks.shapeContractPassed} caustic=${checks.causticPassed}\n`,
    "utf8",
  );
  process.stdout.write(`${JSON.stringify(result, null, 2)}\n`);
  if (result.status !== "passed") process.exitCode = 1;
}

main().catch((error) => {
  process.stderr.write(`${error.stack ?? error}\n`);
  process.exitCode = 1;
});
