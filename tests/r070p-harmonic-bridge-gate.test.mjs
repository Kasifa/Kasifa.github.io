import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFile } from "node:child_process";
import { readFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const root = new URL("../", import.meta.url);
const research = new URL("research/", root);
const certificateRoot = new URL("certificates/r070p/", research);

test("locks the finite R0.70P scope without promoting analytic theorems", async () => {
  const [producer, readme, environment] = await Promise.all([
    readFile(new URL("r070p_exact_audit.py", research), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("environment.txt", certificateRoot), "utf8"),
  ]);

  for (const token of [
    "B_{ij}=\\partial_i u_j",
    "Rademacher orthogonality",
    "unbounded sequence of weights",
    "finite-dimensional analysis/synthesis bridge",
    "T_\\star=\\Pi_0",
    "\\Pi_0(P\\omega)=[\\Pi_0,P]\\omega",
    "does **not** prove a Calderón reproducing theorem",
    "mere local boundedness",
  ]) {
    assert.ok(readme.includes(token), token);
  }
  assert.match(producer, /does not\n\+?prove a Calderon reproducing theorem/i);
  assert.match(environment, /claim_boundary=finite projector/);
  assert.match(environment, /not a Calderon theorem/);
  assert.match(environment, /not[\s\S]{0,120}PDE continuation theorem/);
});

test("locks the periodic zero-mode repair and conditional theorem boundary", async () => {
  const [
    report,
    commutatorAudit,
    projectorAudit,
    literatureAudit,
    independentAudit,
  ] =
    await Promise.all([
      readFile(new URL("r070p_report-source.md", research), "utf8"),
      readFile(new URL("r070p_commutator_audit.md", research), "utf8"),
      readFile(new URL("r070p_projector_miller_audit.md", research), "utf8"),
      readFile(new URL("r070p_literature_audit.md", research), "utf8"),
      readFile(new URL("r070p_independent_audit.md", research), "utf8"),
    ]);

  for (const token of [
    "T_\\star=\\Pi_0",
    "whose mean need not vanish",
    "\\mathcal I_{\\mathbb T}",
    "[\\Pi_0,A]f=\\Pi_0(Af)",
    "Suppose \\(T_{\\max}<\\infty\\)",
    "R_K(t)=",
    "No public-page update or GitHub publication is authorized",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(commutatorAudit, /PASS for the canonical unweighted/);
  assert.match(commutatorAudit, /FAIL for arbitrary weights/);
  assert.match(projectorAudit, /Audit decision:\*\* CONDITIONAL PASS/);
  assert.match(literatureAudit, /no\s+priority or novelty claim/i);
  assert.match(independentAudit, /none at BLOCKER, MAJOR, or MINOR level/);
  assert.match(independentAudit, /Periodic zero-mode blocker — resolved/);
  assert.match(report, /not a solution of the Navier--Stokes Millennium problem/);
});

test("keeps every R0.70P analytic note structurally auditable", async () => {
  const names = [
    "r070p_report-source.md",
    "r070p_commutator_audit.md",
    "r070p_projector_miller_audit.md",
    "r070p_literature_audit.md",
    "r070p_independent_audit.md",
  ];
  for (const name of names) {
    const source = await readFile(new URL(name, research), "utf8");
    const tags = [...source.matchAll(/\\tag\{([^}]+)\}/g)].map(
      (match) => match[1],
    );
    assert.equal(tags.length, new Set(tags).size, name + " duplicate tags");
    assert.equal(
      (source.match(/\\\[/g) ?? []).length,
      (source.match(/\\\]/g) ?? []).length,
      name + " display delimiters",
    );
    assert.equal(
      (source.match(/\\\(/g) ?? []).length,
      (source.match(/\\\)/g) ?? []).length,
      name + " inline delimiters",
    );
    assert.doesNotMatch(source, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
    const withoutMarkdownHardBreaks = source.replace(/ {2}$/gm, "");
    assert.doesNotMatch(withoutMarkdownHardBreaks, /[ \t]+$/m);
  }
});

test("reproduces the five-group exact R0.70P producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070p_exact_audit.py", research));
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70P");
  assert.equal(archived.status, "exact-harmonic-projector-bridge-audit");
  assert.equal(Object.keys(archived.checks).length, 5);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the projector and periodic integration identities", async () => {
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );

  assert.equal(archived.projectorIdentityLedger.symbolicFamily.residual, "0");
  assert.equal(
    archived.projectorIdentityLedger.symbolicFamily.freeGradientParameters,
    8,
  );
  assert.equal(
    archived.projectorIdentityLedger.symbolicFamily.freeDirectionParameters,
    2,
  );
  for (const sample of archived.projectorIdentityLedger.traceFreeRationalSamples) {
    assert.equal(sample.residual, "0");
    assert.equal(sample.left, sample.right);
  }

  const periodic = archived.periodicIntegrationByPartsLedger;
  assert.equal(periodic.divergence, "0");
  assert.equal(periodic.constantProjector.rightAverage, "0");
  assert.equal(periodic.constantProjector.strainAverage, "2/9");
  assert.equal(
    periodic.constantProjector.quarterTransverseVorticityAverage,
    "2/9",
  );
  assert.equal(periodic.variableProjector.rightAverage, "1/8");
  assert.equal(periodic.variableProjector.correctionAverage, "1/8");
  assert.equal(periodic.variableProjector.strainAverage, "3/16");
  assert.equal(
    periodic.variableProjector.quarterTransverseVorticityAverage,
    "1/16",
  );
  assert.equal(periodic.variableProjector.integratedResidual, "0");
  assert.equal(periodic.variableProjector.projectorIsPeriodic, true);
  assert.equal(periodic.variableProjector.localLiftChangesSignAroundXCycle, true);
});

test("locks Rademacher orthogonality and exact weight scaling", async () => {
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const rademacher = archived.rademacherLedger;
  assert.equal(rademacher.signCount, 16);
  assert.deepEqual(rademacher.signSecondMomentMatrix, [
    ["1", "0", "0", "0"],
    ["0", "1", "0", "0"],
    ["0", "0", "1", "0"],
    ["0", "0", "0", "1"],
  ]);
  assert.equal(rademacher.symbolicResidual, "0");
  assert.equal(rademacher.rationalVectorAverage, rademacher.rationalVectorSquareSum);

  const bounded = archived.weightScalingLedger.boundedWeights;
  assert.equal(bounded.unweightedSquareSum, "176/105");
  assert.equal(bounded.weightedSquareSum, "13777/10080");
  assert.equal(bounded.exactSlack, "3119/10080");
  assert.equal(bounded.symbolicSlackIdentityResidual, "0");

  const unbounded = archived.weightScalingLedger.unboundedWeightsNearSingleFrequency;
  assert.equal(unbounded.inputHomogeneousHMinusOneNormSquared, "1");
  assert.equal(unbounded.projectorDerivativeFrobeniusNormSquared, "2");
  assert.deepEqual(unbounded.projectorFrequencyShifts, ["-2", "0", "+2"]);
  assert.equal(unbounded.profileDerivativeAtOneHalf, "24/25");
  assert.equal(unbounded.normalizedCentralFrequency, "rho=n/(2*n)=1/2");
  assert.match(unbounded.profileNondegeneracy, /24\/25!=0/);
  assert.equal(unbounded.limit, "144/625");
  assert.equal(unbounded.dyadicSubsequence, "n_J=2^(J-1), so m_n(k)=phi(2^(-J)*k)");
  assert.equal(unbounded.unboundedWeightChoice, "w_J=n_J=2^(J-1)");
  assert.equal(unbounded.weightedSquaredLimit, "oo");
  assert.equal(unbounded.finiteFrequencySamples.length, 5);
  assert.deepEqual(
    unbounded.finiteFrequencySamples.map((sample) => sample.n),
    [2, 4, 8, 16, 32],
  );
});

test("locks finite bridge adversaries and rational cases", async () => {
  const archived = JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
  const bridge = archived.finiteDimensionalBridgeLedger;
  const zeroMode = bridge.periodicZeroModeCompletion;
  assert.match(zeroMode.domain, /normalized Haar measure/);
  assert.match(zeroMode.FourierConvention, /\|D\|/);
  assert.equal(zeroMode.frameCompletion.startsWith("T_star=Pi_0"), true);
  assert.deepEqual(zeroMode.inputMean, ["0", "0", "0"]);
  assert.deepEqual(zeroMode.projectedInputMean, ["0", "-1/4", "0"]);
  assert.deepEqual(zeroMode.commutator, ["0", "-1/4", "0"]);
  assert.equal(zeroMode.commutatorNormSquared, "1/16");
  assert.equal(zeroMode.oscillatoryCoefficient, "-cos(2*x_one)/2");
  assert.equal(zeroMode.dualityPairing, "-1/4");
  assert.equal(zeroMode.inputHomogeneousHMinusOneNormSquared, "1/8");
  assert.equal(zeroMode.coefficientHomogeneousHOneNormSquared, "1/2");
  assert.equal(zeroMode.homogeneousDualityCauchySlack, "0");
  assert.deepEqual(zeroMode.directTstarVorticityBlock, ["0", "0", "0"]);
  assert.deepEqual(zeroMode.directQstarCovarianceContribution, [
    ["0", "0", "0"],
    ["0", "0", "0"],
    ["0", "0", "0"],
  ]);
  assert.equal(zeroMode.directRstarResidualContribution, "0");
  assert.match(zeroMode.canonicalPeriodicBridge, /\[Pi_0,P\]/);

  assert.equal(bridge.positiveModel.synthesisConstant, "1");
  assert.equal(bridge.positiveModel.randomSeed, 70070);
  assert.equal(bridge.positiveModel.randomRationalCases.length, 6);
  let noncommutingCases = 0;
  for (const sample of bridge.positiveModel.randomRationalCases) {
    assert.equal(sample.blockEnergyIdentityResidual, "0");
    assert.deepEqual(sample.reconstructed, sample.target);
    assert.doesNotMatch(sample.cauchySlack, /^-/);
    if (sample.commutatorSquareSum !== "0") noncommutingCases += 1;
  }
  assert.ok(noncommutingCases >= 4);

  assert.equal(bridge.commutatorEssentialAdversary.targetEnergy, "1");
  assert.equal(bridge.commutatorEssentialAdversary.observedEnergy, "0");
  assert.equal(bridge.commutatorEssentialAdversary.commutatorEnergy, "1");
  assert.deepEqual(
    bridge.commutatorEssentialAdversary.reconstructed,
    bridge.commutatorEssentialAdversary.input,
  );
  assert.equal(bridge.missingReconstructionAdversary.targetEnergy, "1");
  assert.equal(bridge.missingReconstructionAdversary.observedEnergy, "0");
  assert.equal(
    bridge.missingReconstructionAdversary.reconstructionHypothesisSatisfied,
    false,
  );
  assert.equal(bridge.projectorYoungStep.rationalCases[0].slack, "0");
});

test("locks every R0.70P certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070p_exact_audit\.py/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});
