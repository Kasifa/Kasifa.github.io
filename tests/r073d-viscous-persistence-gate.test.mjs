import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";


const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");

const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const sha256 = async (relative) => createHash("sha256")
  .update(await readFile(resolve(root, relative))).digest("hex");

function assertIncludesAll(source, tokens, label) {
  for (const token of tokens) {
    assert.ok(source.includes(token), `${label}: missing ${token}`);
  }
}

function exactKeys(value, keys, label) {
  assert.ok(value && typeof value === "object" && !Array.isArray(value), `${label}: object`);
  assert.deepEqual(Object.keys(value).sort(), [...keys].sort(), `${label}: exact keys`);
}

function statusAssignments(source) {
  return [...source.matchAll(/\b([A-Za-z][A-Za-z0-9]*)=(CLOSED|OPEN|CONDITIONAL)\b/g)]
    .map((match) => [match[1], match[2]]);
}

test("R0.73D freezes exactly d=0, gamma=1/2, s=+1 and preserves the singular domains", async () => {
  const [freeze, proof, report, audit] = await Promise.all([
    text("research/r073d_problem_freeze.md"),
    text("research/r073d_viscous_persistence_proof.md"),
    text("research/r073d_report-source.md"),
    text("research/r073d_independent_analytic_audit.md"),
  ]);

  assert.ok(freeze.includes(
    "**One permitted target:** the fixed profile \\(d=0\\), row \\(\\gamma=1/2\\),\n"
      + "sign \\(s=+1\\)",
  ));
  assert.ok(proof.includes(
    "**Scope:** the frozen periodic row \\(\\gamma=1/2\\), \\(d=0\\), and the sign\n"
      + "\\(s=+1\\)",
  ));
  assertIncludesAll(proof, [
    "let \\(X=X_{1/4}\\) be the completion of \\(L^2\\)",
    "A=-\\frac i2\\bigl(M_{W_0}+M_{W_0''}L^{-1}\\bigr)\\in\\mathcal B(X)",
    "B_\\varepsilon=A-\\varepsilon L",
    "D_X(B_\\varepsilon)=H^1_{\\rm per}",
    "D(H_\\varepsilon)=H^2_{\\rm per}\\quad(\\varepsilon>0)",
    "D(H_0)=L^2",
  ], "proof space/domain contract");
  assertIncludesAll(freeze, [
    "U=2L^{-1/2}:X\\to L^2",
    "U D_X(L)=H^2_{\\rm per}",
    "\\varepsilon L\\) is unbounded there for every \\(\\varepsilon>0\\)",
    "No bounded-operator perturbation theorem may be applied directly",
  ], "problem-freeze domain contract");
  assertIncludesAll(audit, [
    "defines \\(X\\) as the\ncompletion of \\(L^2\\)",
    "D(H_\\varepsilon)=H^2_{\\rm per}\\quad(\\varepsilon>0)",
    "D(H_0)=L^2",
    "The domain statement in the proof is correct.",
  ], "independent domain audit");
  assert.ok(report.includes("The term \\(-\\varepsilon L\\) is unbounded on \\(X\\)"));
  assert.ok(report.includes(
    "The proof therefore cannot use bounded-operator norm\nperturbation of \\(A\\)",
  ));
});

test("R0.73D closes the compact-Fredholm and Riesz-projection chain, not a bounded Kato perturbation", async () => {
  const [proof, audit, gap, certificate] = await Promise.all([
    text("research/r073d_viscous_persistence_proof.md"),
    text("research/r073d_independent_analytic_audit.md"),
    text("research/r073d_gap_matrix.md"),
    json("research/certificates/r073d/certificate.json"),
  ]);

  assertIncludesAll(proof, [
    "U_\\mu A_\\gamma U_\\mu^{-1}=M+K",
    "L_\\mu^{-1/2}[M_W,L_\\mu^{1/2}]",
    "L_\\mu^{-1/2}M_{W''}L_\\mu^{-1/2}",
    "The diagonal multiplier \\(L_\\mu^{-1/2}\\) is compact",
    "Hence both terms in (2.4) are compact, and so is \\(K\\)",
    "R_\\varepsilon(z)\\longrightarrow R_0(z)",
    "uniform strong convergence of the\nadjoint resolvents as well",
    "F_\\varepsilon(z)=I-R_\\varepsilon(z)K",
    "G_\\varepsilon(z):=(z-\\widetilde B_\\varepsilon)^{-1}",
    "G_\\varepsilon-R_\\varepsilon\n =G_\\varepsilon K R_\\varepsilon",
    "\\int_{\\Gamma_*}R_\\varepsilon(z)\\,dz=0",
    "\\|P_\\varepsilon-P_0\\|_{\\mathcal B(X)}\\longrightarrow0",
    "\\operatorname{rank}P_\\varepsilon\n =\\operatorname{rank}P_0=m_*",
    "repeat the same fixed-contour proof on every smaller circle",
  ], "operator proof chain");
  assert.ok(proof.includes("Strong resolvent convergence alone would not imply (1.3)"));
  assert.ok(proof.includes("The first term tends to zero in norm because \\(K\\) is compact"));
  assert.ok(proof.includes("the second\ndoes so by (4.7)"));

  assert.match(audit, /\*\*Decision:\*\* PASS for one fixed inviscid spectral cluster/);
  assertIncludesAll(audit, [
    "strong and adjoint-strong convergence",
    "compact sandwich converges in operator norm",
    "Adjoint-strong convergence is exactly what is needed",
    "This excludes spectral pollution inside the audited fixed disk",
  ], "independent analytic audit");
  assert.match(audit, /It does\s+not exclude new viscous spectrum elsewhere in the right half-plane/);

  for (let index = 1; index <= 8; index += 1) {
    assert.match(gap, new RegExp(`\\| D${index} \\|[^\\n]+\\| CLOSED \\|`), `gap D${index}`);
  }
  assert.deepEqual(certificate.checks, {
    analyticBaseContourIntegralZero: true,
    baseResolventStrongAndAdjointStrong: true,
    commutatorCompactnessPresent: true,
    fastTimeRemainsOpen: true,
    finiteEvidenceFailClosed: true,
    finiteIndependentChecksPass: true,
    finitePrimaryChecksPass: true,
    fredholmFactorPresent: true,
    generalPrecedentAcknowledged: true,
    independentAnalyticAuditPass: true,
    kineticSpaceDefinedByCompletion: true,
    multiplicityPreserved: true,
    nonlinearAndClayRemainOpen: true,
    projectionNormConvergenceProved: true,
    singularDomainJumpPresent: true,
    unitaryTransformPresent: true,
  });
});

test("R0.73D exposes exactly five CLOSED theorem claims and keeps every extrapolation OPEN or CONDITIONAL", async () => {
  const [freeze, proof, report, gap, certificate, primary, independent] = await Promise.all([
    text("research/r073d_problem_freeze.md"),
    text("research/r073d_viscous_persistence_proof.md"),
    text("research/r073d_report-source.md"),
    text("research/r073d_gap_matrix.md"),
    json("research/certificates/r073d/certificate.json"),
    json("experiments/r073d/viscous_cluster_diagnostic.json"),
    json("experiments/r073d/independent_validation.json"),
  ]);

  const closed = [
    "staticVanishingViscosityPersistence",
    "fixedContourResolventUniform",
    "fixedClusterRieszProjectionNormConvergence",
    "fixedClusterAlgebraicMultiplicityPreserved",
    "fixedClusterEigenvaluesConverge",
  ];
  const finalBoundary = {
    inviscidRootUnique: "OPEN",
    inviscidEigenvalueSimple: "OPEN",
    explicitContourRadius: "OPEN",
    explicitViscosityThreshold: "OPEN",
    quantitativeEigenvalueRate: "OPEN",
    globalRightHalfPlaneNoPollution: "OPEN",
    uniformComplementaryDichotomy: "OPEN",
    movingProfileUniformContour: "OPEN",
    logFastTimeTransfer: "OPEN",
    superPolynomialCompleteRowNoGo: "CONDITIONAL",
    completeOSSquireA2DirectSum: "OPEN",
    nonlinearNavierStokes: "OPEN",
    Clay: "OPEN",
  };

  const allReportStates = statusAssignments(report);
  assert.deepEqual(
    [...new Set(allReportStates.filter(([, state]) => state === "CLOSED").map(([name]) => name))].sort(),
    [...closed].sort(),
  );
  for (const name of closed) {
    assert.equal(certificate.theorem[name], "CLOSED", `certificate theorem ${name}`);
  }
  assert.deepEqual(
    Object.fromEntries(statusAssignments(report.slice(report.indexOf("## 12. Final boundary")))),
    finalBoundary,
  );
  assert.deepEqual(
    Object.fromEntries(statusAssignments(freeze.slice(freeze.indexOf("## 7. Explicitly excluded")))),
    {
      inviscidRootUnique: "OPEN",
      inviscidEigenvalueSimple: "OPEN",
      quantitativeEigenvalueRate: "OPEN",
      movingProfileUniformContour: "OPEN",
      uniformComplementaryDichotomy: "OPEN",
      graphDomainKatoTransport: "OPEN",
      logFastTimeTransfer: "OPEN",
      completeOSSquireA2DirectSum: "OPEN",
      nonlinearNavierStokes: "OPEN",
      Clay: "OPEN",
    },
  );
  assert.equal(certificate.theorem.contourRadiusExplicit, false);
  assert.equal(certificate.theorem.viscosityThresholdExplicit, false);
  assert.equal(certificate.theorem.inviscidAlgebraicMultiplicityKnown, false);
  assert.deepEqual(certificate.claimBoundary, {
    clayProblemSolved: false,
    completeOSSquireA2DirectSum: false,
    globalRightHalfPlaneNoPollution: false,
    inviscidEigenvalueSimple: false,
    inviscidRootUnique: false,
    logFastTimeTransfer: false,
    movingProfileUniformContour: false,
    nonlinearNavierStokes: false,
    quantitativeEigenvalueRate: false,
    uniformComplementaryDichotomy: false,
  });

  // The inherited R0.73C radius 0.06 is not an R0.73D certified contour.
  assert.equal(Object.hasOwn(primary.parameters, "contourRadius"), false);
  assert.equal(primary.claimBoundary.inviscidClusterRadiusCertifiedHere, false);
  assert.match(gap, /existential contour; no certified numerical radius/);
  assert.doesNotMatch(
    `${freeze}\n${proof}\n${report}`,
    /(?:explicitContourRadius|contourRadius)\s*=\s*(?:0\.06|CLOSED)/i,
  );

  assert.equal(primary.claimBoundary.algebraicSimplicityProvedHere, false);
  assert.equal(independent.claimBoundary.rankOneContinuumClusterCertified, false);
  assert.match(report, /spectral cluster and not a unique rank-one branch/);
  assert.ok(report.includes(
    "No finite Fourier calculation, no one-row linear spectral theorem, and no\n"
      + "fixed-profile result is presented as a solution of the three-dimensional\n"
      + "Navier--Stokes regularity problem.",
  ));
  assert.match(proof, /No priority or strict-strengthening claim/);
  assert.doesNotMatch(
    `${freeze}\n${proof}\n${report}\n${gap}`,
    /\b(?:inviscidRootUnique|inviscidEigenvalueSimple|nonlinearNavierStokes|Clay)=(?:CLOSED|TRUE)\b/i,
  );
});

test("R0.73D finite evidence is exactly the 4-by-12 binary64 diagnostic and remains fail closed", async () => {
  const [primary, independent, certificate, producer, validator] = await Promise.all([
    json("experiments/r073d/viscous_cluster_diagnostic.json"),
    json("experiments/r073d/independent_validation.json"),
    json("research/certificates/r073d/certificate.json"),
    text("research/r073d_viscous_cluster_diagnostic.py"),
    text("experiments/r073d/independent_validate.py"),
  ]);
  const cutoffs = [24, 48, 96, 128];
  const epsilons = [0, 0.01, 0.003, 0.001, 0.0003, 0.0001, 0.00003, 0.00001, 0.000003, 0.000001, 1e-7, 1e-8];

  assert.equal(primary.schemaVersion, "r073d-viscous-cluster-diagnostic-v1");
  assert.equal(primary.release, "R0.73D");
  assert.deepEqual(primary.parameters, {
    cutoffs,
    epsilons,
    gamma: 0.5,
    mu: 0.25,
    selectionRule: "largest real part of each finite compression",
    space: "U_mu X_mu = L2 finite Fourier compression",
  });
  assert.equal(primary.rows.length, 48);
  const rowKeys = new Set();
  for (const row of primary.rows) {
    exactKeys(row, [
      "N", "dimension", "embeddedResidual", "epsilon", "finiteDimensionalOnly",
      "kineticFiniteCompression", "lambdaImag", "lambdaReal", "leftRightPairingAbs",
      "projectorDifferenceFromEpsilonZero", "projectorNorm",
    ], `finite row N=${row.N}, epsilon=${row.epsilon}`);
    assert.ok(cutoffs.includes(row.N), `unexpected cutoff ${row.N}`);
    assert.ok(epsilons.includes(row.epsilon), `unexpected epsilon ${row.epsilon}`);
    assert.equal(row.dimension, 2 * row.N + 1);
    assert.equal(row.finiteDimensionalOnly, true);
    assert.equal(row.kineticFiniteCompression, true);
    for (const key of [
      "embeddedResidual", "lambdaImag", "lambdaReal", "leftRightPairingAbs",
      "projectorDifferenceFromEpsilonZero", "projectorNorm",
    ]) assert.ok(Number.isFinite(row[key]), `${row.N}/${row.epsilon}: finite ${key}`);
    const key = `${row.N}:${row.epsilon}`;
    assert.equal(rowKeys.has(key), false, `duplicate row ${key}`);
    rowKeys.add(key);
  }
  assert.deepEqual(
    [...rowKeys].sort(),
    cutoffs.flatMap((N) => epsilons.map((epsilon) => `${N}:${epsilon}`)).sort(),
  );
  assert.deepEqual(primary.checks, {
    largestCutoffMaximumEmbeddedResidualBelow1eMinus10: true,
    largestCutoffRowsRemainPositive: true,
    largestTwoCutoffsEigenvaluesAgreeBelow1eMinus9: true,
  });
  assert.deepEqual(primary.maximums, {
    embeddedResidualAllCutoffs: 1.029408853887337e-6,
    embeddedResidualLargestCutoff: 6.462810327332553e-15,
    largestTwoCutoffsEigenvalueDifference: 2.8322929587812264e-15,
  });
  assert.equal(primary.cutoffComparisons.length, epsilons.length);
  assert.deepEqual(primary.cutoffComparisons.map(({ epsilon }) => epsilon), epsilons);
  assert.equal(
    Math.max(...primary.rows.filter(({ N }) => N === 128).map(({ embeddedResidual }) => embeddedResidual)),
    primary.maximums.embeddedResidualLargestCutoff,
  );
  assert.ok(primary.maximums.embeddedResidualLargestCutoff < 1e-10);
  assert.ok(primary.maximums.largestTwoCutoffsEigenvalueDifference < 1e-9);

  const expectedSentinels = [
    [0, 0.17040797692043275, 1.6835042049174966, 0],
    [0.01, 0.1563164070149083, 1.486606332561653, 0.5623486117028229],
    [0.0001, 0.17026100524770876, 1.6756794461662503, 0.028188658273282464],
    [0.000001, 0.17040650660020246, 1.6834210770438685, 0.0003090500927697423],
    [1e-8, 0.17040796221717075, 1.6835033730864915, 0.000003093771501094026],
  ];
  assert.deepEqual(
    certificate.finiteDiagnostics.sentinels.map((row) => [
      row.epsilon, row.lambdaReal, row.projectorNorm, row.projectorDifference,
    ]),
    expectedSentinels,
  );
  for (const sentinel of certificate.finiteDiagnostics.sentinels) {
    assert.equal(sentinel.N, 128);
    assert.equal(sentinel.finiteDimensionalOnly, true);
    const row = primary.rows.find(({ N, epsilon }) => N === 128 && epsilon === sentinel.epsilon);
    assert.ok(row, `primary sentinel epsilon=${sentinel.epsilon}`);
    assert.deepEqual(
      [row.lambdaReal, row.projectorNorm, row.projectorDifferenceFromEpsilonZero],
      [sentinel.lambdaReal, sentinel.projectorNorm, sentinel.projectorDifference],
    );
  }
  assert.deepEqual(certificate.finiteDiagnostics.maximums, primary.maximums);
  assert.equal(certificate.finiteDiagnostics.largestCutoff, 128);
  assert.equal(certificate.finiteDiagnostics.evidenceClass, "finite diagnostic only");

  assert.equal(independent.schemaVersion, "r073d-independent-finite-validation-v1");
  assert.equal(independent.allChecksPass, true);
  assert.ok(Object.values(independent.checks).every((value) => value === true));
  assert.deepEqual(independent.maximumErrors, {
    eigenvalueAbsolute: 0,
    embeddedResidualAbsolute: 0,
    leftRightPairingAbsolute: 0,
    projectorDifferenceAbsolute: 0,
    projectorNormAbsolute: 0,
  });
  assert.deepEqual(certificate.finiteDiagnostics.independentMaximumErrors, independent.maximumErrors);
  assert.equal(independent.validator.importsPrimaryProducer, false);
  assert.deepEqual(primary.sourceBinding, {
    path: "research/r073d_viscous_cluster_diagnostic.py",
    sha256: await sha256("research/r073d_viscous_cluster_diagnostic.py"),
  });
  assert.equal(independent.primary.sha256, await sha256(independent.primary.path));
  assert.equal(independent.validator.sha256, await sha256(independent.validator.path));
  for (const sentinel of independent.sentinels) {
    const row = primary.rows.find(({ N, epsilon }) => N === sentinel.N && epsilon === sentinel.epsilon);
    assert.ok(row, `independent sentinel epsilon=${sentinel.epsilon}`);
    assert.deepEqual(
      [
        row.lambdaReal, row.lambdaImag, row.projectorNorm,
        row.projectorDifferenceFromEpsilonZero,
      ],
      [
        sentinel.lambdaReal, sentinel.lambdaImag, sentinel.projectorNorm,
        sentinel.projectorDifference,
      ],
    );
  }
  assert.match(producer, /dtype=np\.complex128/);
  assert.match(validator, /dtype=np\.complex128/);
  assert.deepEqual(primary.claimBoundary, {
    algebraicSimplicityProvedHere: false,
    clayProblemSolved: false,
    complementaryDichotomyProvedHere: false,
    finiteKineticCompressionComputed: true,
    finiteProjectorDifferencesComputed: true,
    finiteProjectorNormsComputed: true,
    infiniteDimensionalPersistenceProvedHere: false,
    inviscidClusterRadiusCertifiedHere: false,
    nonautonomousTransferProvedHere: false,
    nonlinearNavierStokesProvedHere: false,
    ordinaryCutoffConvergenceIsContinuumProof: false,
  });
  assert.deepEqual(independent.claimBoundary, {
    continuumTheoremCertifiedByThisValidator: false,
    fastTimeTransferCertified: false,
    independentFiniteRecomputation: true,
    rankOneContinuumClusterCertified: false,
  });
});

test("R0.73D records Shvydkoy-Friedlander as precedent and makes no priority claim", async () => {
  const [freeze, proof, report, literature, certificate] = await Promise.all([
    text("research/r073d_problem_freeze.md"),
    text("research/r073d_viscous_persistence_proof.md"),
    text("research/r073d_report-source.md"),
    text("research/r073d_literature_audit.md"),
    json("research/certificates/r073d/certificate.json"),
  ]);

  assertIncludesAll(literature, [
    "Shvydkoy and Friedlander prove",
    "decisive general precedent for periodic Euler/Navier--Stokes spectral persistence",
    "noveltyOfNormConvergence=NOT_CLAIMED",
    "relationToShvydkoyFriedlander=SELF_CONTAINED_SPECIALIZATION_WITH_EXPLICIT_NORM_PROOF",
  ], "literature boundary");
  assert.match(
    literature,
    /must not describe vanishing-viscosity spectral\s+persistence as a new general theorem/,
  );
  assert.match(freeze, /must cite Shvydkoy and Friedlander \(2008\) as the decisive general\nprecedent/);
  assert.match(proof, /No priority or strict-strengthening claim relative to the\ngeneral theorem of Shvydkoy--Friedlander is made/);
  assert.match(report, /No general priority claim is made/);
  assert.deepEqual(certificate.literatureBoundary, {
    fixedRowSelfContainedNormProof: true,
    generalPersistencePrecedent: "Shvydkoy-Friedlander 2008",
    generalPriorityClaimMade: false,
  });
});
