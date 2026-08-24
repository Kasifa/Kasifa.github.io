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
const certificateRoot = new URL("certificates/r070s/", research);

async function archivedResult() {
  return JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
}

test("locks the R0.70S majorant theorem and quantified boundary", async () => {
  const [report, readme, producer, environment] = await Promise.all([
    readFile(new URL("r070s_report-source.md", research), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("r070s_exact_audit.py", research), "utf8"),
    readFile(new URL("environment.txt", certificateRoot), "utf8"),
  ]);

  for (const token of [
    "R0.70S — An energy-level no-go for the near-rank palinstrophy majorant",
    "coefficient-level majorant",
    "\\mathscr T=\\{T_\\star=\\Pi_0\\}",
    "Theorem 7.1 — Vanishing structural inputs and divergent palinstrophy majorant",
    "F_{T,\\nu,\\eta_0,\\mathscr T}",
    "\\sup_{z\\in[0,\\delta]^4}",
    "signed deficit",
    "initial enstrophy",
    "No public-page update or GitHub publication",
  ]) {
    assert.ok(report.includes(token), token);
  }
  for (const token of [
    "does **not** assert that the signed deficit",
    "does not prove a singularity",
  ]) {
    assert.ok(readme.includes(token), token);
  }
  assert.match(readme, /positive\s+coefficient-level majorant/);
  assert.match(readme, /initial \\\(H\^1\\\)/);
  assert.match(producer, /not the signed[\s\S]{0,40}diffusion deficit/);
  assert.match(environment, /not a signed-deficit lower bound/);
  assert.doesNotMatch(report, /proves (a )?finite-time singularity/i);
  assert.doesNotMatch(report, /proves global regularity/i);
});

test("reproduces the four-group exact R0.70S producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070s_exact_audit.py", research));
  const archived = await archivedResult();
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });

  assert.equal(stderr, "");
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70S");
  assert.equal(
    archived.status,
    "exact-energy-palinstrophy-majorant-audit",
  );
  assert.equal(Object.keys(archived.checks).length, 4);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the exact global shear and disjoint complete-frame blocks", async () => {
  const archived = await archivedResult();
  const definitions = archived.definitions;
  const ledger = archived.globalShearLedger;

  assert.equal(
    definitions.completeFrame,
    "{T_star=Pi_0} union {T_j:j in Z}",
  );
  assert.match(definitions.frameHypotheses, /real, even, radial, smooth/);
  assert.match(definitions.frameHypotheses, /sum_j\|phi/);
  assert.deepEqual(ledger.curlResidual, ["0", "0", "0"]);
  assert.deepEqual(ledger.heatEquationResidual, ["0", "0", "0"]);
  assert.deepEqual(ledger.vorticityHeatEquationResidual, ["0", "0", "0"]);
  assert.deepEqual(ledger.advectiveNonlinearity, ["0", "0", "0"]);
  assert.equal(ledger.velocityDivergence, "0");
  assert.equal(ledger.vorticityDivergence, "0");
  assert.equal(ledger.initialKineticEnergy, "65537*A_N**2/(65536*N**2)");
  assert.equal(ledger.initialEnstrophy, "257*A_N**2/256");
  assert.deepEqual(ledger.lowActiveOffsets, [0]);
  assert.deepEqual(ledger.highActiveOffsets, [4]);
  assert.equal(ledger.activeIndexIntersection, "empty");
  assert.equal(ledger.lowResponseSquare, "1");
  assert.equal(ledger.highResponseSquare, "1");
  assert.match(ledger.responseSquareDerivation, /not numerically evaluated/);
  assert.deepEqual(ledger.zeroModeOfVorticity, ["0", "0", "0"]);
  assert.match(ledger.zeroModeLedger, /\[Pi_0,P_N\]/);
  assert.match(ledger.solutionBoundary, /smooth global/);
});

test("locks the exact spectrum, relative gap, eta, and positive point", async () => {
  const ledger = (await archivedResult()).covarianceSpectrumLedger;

  assert.equal(ledger.directionDotProduct, "sin(17*N*x1)");
  assert.equal(ledger.characteristicResidual, "0");
  assert.equal(ledger.qAtTimeZero, "1/256");
  assert.equal(ledger.qLogDerivative, "-510*N**2*nu");
  assert.equal(ledger.relativeGapBound, "(lambda1-lambda2)/E>=255/257");
  assert.equal(ledger.etaEndpointBound, "0<=eta<=1/257");
  assert.equal(ledger.cEtaBound, "0<=c_eta<=1/15");
  assert.equal(ledger.cEtaMonotonicityLedger.dcDzetaResidual, "0");
  assert.equal(ledger.cEtaMonotonicityLedger.dEtaOddsResidual, "0");
  assert.equal(ledger.positivePoint.eta, "1/257");
  assert.equal(ledger.positivePoint.cEta, "1/15");
  assert.equal(ledger.positivePoint.normalizedGradientDensity, "2");
  assert.equal(ledger.positivePoint.normalizedMajorantIntegrand, "2/15");
  assert.equal(ledger.baseMajorantUpperIntegral, "257/(7680*nu)");
  assert.match(ledger.baseMajorantStatus, /0<I_1\(infinity\)<infinity/);
  assert.match(ledger.continuityCertificate, /positive-measure/);
  assert.equal(ledger.projectorDerivativeSampleNormSquared, "512*N**2/225");
});

test("locks analytic dyadic lemmas and audited scale-factor arithmetic", async () => {
  const ledger = (await archivedResult()).dyadicScalingLedger;

  assert.equal(ledger.finiteL2SampleResidual, "0");
  assert.equal(ledger.finiteZeroModeSampleResidual, "0");
  assert.equal(ledger.multiplierArgumentResidual, "0");
  assert.equal(ledger.zeroModeIdentity, "Pi_0(S_N f)=Pi_0(f)");
  assert.equal(ledger.annularIndexShift, "T_j*S_N=S_N*T_(j-J)");
  assert.match(ledger.commutatorBlockIdentities.annular, /T_\(j-J\)/);
  assert.match(ledger.commutatorBlockIdentities.zeroMode, /Pi_0/);
  assert.match(
    ledger.commutatorBlockIdentities.baseConstantEvaluation,
    /not evaluated in closed form/,
  );
  assert.deepEqual(ledger.displayedFieldPullbackResiduals.vorticity, [
    "0",
    "0",
    "0",
  ]);
  assert.deepEqual(ledger.displayedFieldPullbackResiduals.velocity, [
    "0",
    "0",
    "0",
  ]);
  assert.ok(
    ledger.displayedFieldPullbackResiduals.covariance
      .flat()
      .every((value) => value === "0"),
  );
  assert.deepEqual(ledger.scaleFactorResiduals, {
    commutatorL2: "0",
    directionCost: "0",
    majorant: "0",
    residualL2: "0",
  });
  assert.match(ledger.certificateScope, /analytic report lemmas/);
  assert.match(ledger.finiteTimeIdentities.residual, /A_N\^2\/N/);
  assert.match(ledger.finiteTimeIdentities.commutator, /A_N\^2\/N/);
  assert.match(ledger.finiteTimeIdentities.directionCost, /A_N\^4\/N\^2/);
  assert.equal(
    ledger.finiteTimeIdentities.majorant,
    "I_N(T)=A_N^2*I_1(N^2*T)",
  );
});

test("locks the A_N=N^(1/4) exponent contradiction and H1 caveat", async () => {
  const archived = await archivedResult();
  const ledger = archived.exponentLedger;

  assert.equal(ledger.initialKineticEnergy, "65537/(65536*N**(3/2))");
  assert.equal(ledger.residualL2InfiniteHorizon, "C_R/sqrt(N)");
  assert.equal(
    ledger.commutatorL2InfiniteHorizon,
    "C_commutator/sqrt(N)",
  );
  assert.equal(ledger.directionCostInfiniteHorizon, "C_W/N");
  assert.equal(ledger.majorantInfiniteHorizon, "I_1*sqrt(N)");
  assert.equal(ledger.initialEnstrophy, "257*sqrt(N)/256");
  assert.equal(ledger.uniformEtaBound, "eta_N<=1/257");
  assert.deepEqual(ledger.limits, {
    commutatorL2: "0",
    directionCost: "0",
    kineticEnergy: "0",
    majorant: "+infinity",
    residualL2: "0",
  });
  assert.match(ledger.fixedTimeMajorantLowerBound, /I_1\(T\)>0/);
  assert.match(ledger.initialH1Boundary, /diverges like N\^\(1\/2\)/);
  for (const token of [
    "signed diffusion deficit",
    "initial H1",
    "enstrophy",
    "higher Sobolev norms",
    "does not prove singularity",
    "Millennium problem",
  ]) {
    assert.ok(archived.claimBoundary.includes(token), token);
  }
  for (const token of [
    "one function F fixed uniformly across all dyadic N",
    "T, nu, eta0=1/257",
    "pinned frame fixed",
    "named analytic Haar, frame, spectral, continuity, decay",
  ]) {
    assert.ok(archived.claimBoundary.includes(token), token);
  }
});

test("locks every R0.70S certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070s_exact_audit\.py/);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});
