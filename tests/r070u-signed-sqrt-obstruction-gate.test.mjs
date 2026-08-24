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
const certificateRoot = new URL("certificates/r070u/", research);

async function archivedResult() {
  return JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
}

function everyEntryEquals(matrix, expected) {
  return matrix.flat(Infinity).every((value) => value === expected);
}

test("locks the R0.70U theorem and claim scope", async () => {
  const [report, readme, producer, environment] = await Promise.all([
    readFile(new URL("r070u_report-source.md", research), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("r070u_exact_audit.py", research), "utf8"),
    readFile(new URL("environment.txt", certificateRoot), "utf8"),
  ]);

  for (const token of [
    "R0.70U — A fixed-frame square-root obstruction",
    "\\|r_\\varepsilon\\|_{L^p}=\\Theta(\\varepsilon^2)",
    "\\theta>1/2",
    "\\Phi(s)=o(\\sqrt{s})",
    "not a universal consequence of \\(\\operatorname{rank}Q=1\\)",
    "No exact-rank universal cancellation is used below",
    "\\mathfrak E_S(\\varepsilon)\n =2\\varepsilon(1-\\gamma)I",
    "=-\\frac{(1-\\gamma)A\\delta a^2b}{K^3}\\varepsilon",
    "\\(\\gamma=-1\\), and only the first",
    "\\mathcal A_L(\\widetilde Q_\\varepsilon)=0",
    "\\|Q_\\varepsilon-\\widetilde Q_\\varepsilon\\|_{C^1}",
    "\\|\\mathcal A_{L_\\varepsilon}\\|_{C^0}",
    "\\|H_\\varepsilon\\|_{C^0}=O(\\varepsilon^2)",
    "\\mathfrak R_{\\mathrm{sgn}}(\\omega_\\varepsilon)\n =-\\frac{(1-\\gamma)A\\delta a^2b}{K^3}\\varepsilon",
  ]) {
    assert.ok(report.includes(token), token);
  }

  assert.match(report, /instantaneous smooth initial\s+datum/);
  assert.match(report, /No public-page update or GitHub\s+publication/);
  assert.match(report, /search result, not a\s+novelty or priority claim/);
  assert.match(report, /does not\s+exclude a coefficient that itself diverges/);
  assert.match(readme, /infers a universal commutator\s+cancellation/);
  assert.match(readme, /fixed-frequency, instantaneous obstruction/);
  assert.match(producer, /not inferred from this\s+finite certificate/);
  assert.match(environment, /not a numerical cutoff\/m certificate/);

  assert.doesNotMatch(report, /first ever|for the first time|proves novelty/i);
  assert.doesNotMatch(report, /exact-rank(?:ed)? covariance always cancels/i);
  assert.doesNotMatch(report, /three-mode exact Navier--Stokes solution/i);
  assert.doesNotMatch(report, /proves unconditional global regularity/i);
  assert.doesNotMatch(report, /solves? the Millennium problem/i);
});

test("reproduces the four-group exact R0.70U producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070u_exact_audit.py", research));
  const archivedText = await readFile(
    new URL("result.json", certificateRoot),
    "utf8",
  );
  const archived = JSON.parse(archivedText);
  const { stdout, stderr } = await execFileAsync(python, [producer], {
    cwd: fileURLToPath(root),
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });

  assert.equal(stderr, "");
  assert.equal(stdout, archivedText);
  assert.deepEqual(JSON.parse(stdout), archived);
  assert.equal(archived.release, "R0.70U");
  assert.equal(
    archived.status,
    "fixed-frame-signed-square-root-obstruction-audit",
  );
  assert.equal(Object.keys(archived.checks).length, 4);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the Pythagorean triad and Biot--Savart convention", async () => {
  const ledger = (await archivedResult()).triadLedger;

  assert.equal(
    ledger.parameterPremise,
    "integer m>=2 and amplitudes A>delta>0",
  );
  assert.equal(ledger.a, "(m - 1)*(m + 1)");
  assert.equal(ledger.b, "2*m");
  assert.equal(ledger.K, "m**2 + 1");
  assert.equal(ledger.pythagoreanResidual, "0");
  assert.deepEqual(ledger.qMinusKPlusP, ["0", "0", "0"]);
  assert.equal(ledger.nNormResidual, "0");
  assert.equal(ledger.kDotN, "0");
  assert.equal(ledger.w1HelicitySign, "curl(w1)=-K*w1");
  assert.equal(ledger.allFourierDivergenceResiduals, "0");
  assert.equal(ledger.curlUwMinusWResiduals, "0");
  assert.equal(ledger.curlUhMinusHResiduals, "0");
});

test("locks the nonzero normalized resonant coefficient", async () => {
  const ledger = (await archivedResult()).resonanceLedger;

  assert.equal(ledger.normalizedI, ledger.expectedI);
  assert.equal(ledger.normalizedJ, ledger.expectedJ);
  assert.equal(ledger.commutatorDerivative, ledger.commutatorExpected);
  assert.equal(ledger.physicalHigherOrderResidual, "0");
  assert.equal(ledger.frameHigherOrderResidual, "0");
  assert.equal(ledger.commutatorHigherOrderResidual, "0");
  assert.match(ledger.physicalStretchingPolynomial, /^-A\*delta\*epsilon/);
  assert.match(ledger.commutatorPolynomial, /epsilon/);
  assert.match(ledger.normalizedI, /^-A\*delta\*m/);
  assert.match(ledger.commutatorDerivative, /\(gamma - 1\)/);
  assert.match(ledger.nonzeroPremises, /\|gamma\|<=3\/4/);

  assert.deepEqual(ledger.m3Anchor, {
    parameters: "m=3, a=8, b=6, K=10, A=2, delta=1",
    I: "-48/125",
    J: "3/10",
    physicalStretchingDerivative: "-117/250",
    commutatorDerivative: "96*(gamma - 1)/125",
    scope:
      "algebraic sign/coefficient anchor only; it does not certify |gamma|<=3/4 for the unspecified cutoff",
  });
});

test("locks covariance factorization and quadratic spectral residual", async () => {
  const ledger = (await archivedResult()).covarianceLedger;

  assert.ok(everyEntryEquals(ledger.factorizationResidual, "0"));
  assert.ok(everyEntryEquals(ledger.tensorDefectResidual, "0"));
  assert.equal(ledger.determinant, "0");
  assert.equal(ledger.traceMatrixResidual, "0");
  assert.equal(ledger.sigmaTwoMatrixResidual, "0");
  assert.equal(ledger.traceFromMatrix, ledger.traceExpectedFromVectors);
  assert.equal(ledger.sigmaTwoFromMatrix, ledger.sigmaTwoExpectedFromVectors);
  assert.equal(
    ledger.lambdaTwoOverEpsilonSquaredLimit,
    ledger.expectedResidualCoefficient,
  );
  assert.equal(ledger.originCrossSquare, ledger.originCrossExpected);
  assert.match(ledger.originCrossSquare, /4\*A\*\*2\*m\*\*2/);
  assert.equal(ledger.shiftedTwoEntryOverlapSOSResidual, "0");
});

test("locks the two sign-indefinite exact-rank branches", async () => {
  const ledger = (await archivedResult()).exactRankSignLedger;

  assert.ok(everyEntryEquals(ledger.gammaPlusCovarianceResidual, "0"));
  assert.ok(everyEntryEquals(ledger.gammaMinusCovarianceResidual, "0"));
  assert.ok(everyEntryEquals(ledger.gammaPlusPhysicalDefect, "0"));
  assert.ok(everyEntryEquals(ledger.gammaMinusPhysicalDefectResidual, "0"));
  assert.equal(ledger.gammaPlusCommutator, "0");
  assert.equal(
    ledger.gammaMinusCommutator,
    ledger.gammaMinusCommutatorExpected,
  );
  assert.notEqual(ledger.gammaMinusCommutator, "0");
  assert.match(ledger.boundary, /exact rank alone does not imply/);
});

test("locks the critical exponent and analytic boundaries", async () => {
  const archived = await archivedResult();
  const ledger = archived.exponentLedger;

  assert.equal(ledger.ratioPowerForResidualTheta, "1 - 2*theta");
  assert.equal(ledger.linearRatioPower, "-1");
  assert.equal(ledger.threeQuarterRatioPower, "-1/2");
  assert.equal(ledger.criticalRatioPower, "0");
  assert.match(ledger.analyticReading, /theta>1\/2/);

  for (const token of [
    "no numerical m is certified",
    "not a pointwise positive lower bound",
    "general modulus o(sqrt(s)) no-go",
    "every time-evolution or continuation interpretation",
  ]) {
    assert.ok(
      archived.analyticDependencies.some((item) => item.includes(token)),
      token,
    );
  }

  for (const token of [
    "does not numerically select m",
    "exclude the critical exponent 1/2",
    "time-integrated estimates",
    "unconditional global regularity",
    "Millennium problem",
  ]) {
    assert.ok(archived.claimBoundary.includes(token), token);
  }
});

test("locks every R0.70U certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070u_exact_audit\.py/);
  assert.deepEqual(
    lines.map((line) => line.slice(66)),
    [
      "README.md",
      "command.txt",
      "environment.txt",
      "result.json",
      "../../r070u_exact_audit.py",
    ],
  );
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "invalid checksum line: " + line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2]);
  }
});
