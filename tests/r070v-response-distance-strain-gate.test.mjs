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
const certificateRoot = new URL("certificates/r070v/", research);

async function archivedResult() {
  return JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
}

function everyEntryEquals(matrix, expected) {
  return matrix.flat(Infinity).every((value) => value === expected);
}

test("locks the R0.70V theorem and claim scope", async () => {
  const [report, readme, producer, environment] = await Promise.all([
    readFile(new URL("r070v_report-source.md", research), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("r070v_exact_audit.py", research), "utf8"),
    readFile(new URL("environment.txt", certificateRoot), "utf8"),
  ]);

  for (const token of [
    "R0.70V — Response-distance decomposition",
    "K(p,q)=\\frac12\\|V(p)-V(q)\\|_{\\ell^2}^2",
    "\\widehat{\\mathcal D_\\times}(0)=0",
    "\\min\\{2,2M_\\varphi^2\\delta^2\\}",
    "\\frac{17A^2B^2}{225N^2}",
    "\\mathfrak X_\\times",
    "\\le\\frac12\\|D\\|_{\\dot H^{-1}_\\#,F}^2",
    "\\mathfrak X_{\\times,\\varepsilon}=\\Theta(\\varepsilon^2)",
    "C_\\varphi=2+2M_\\varphi",
    "C_{\\varphi,\\sigma}",
    "dyadic Navier--Stokes dilation",
    "differ by two frequency degrees",
    "No theorem of the form",
  ]) {
    assert.ok(report.includes(token), token);
  }

  assert.match(report, /no positive power of[\s\S]{0,40}controls the full tensor/);
  assert.match(report, /viscosity-absorption ledger, not a closure/);
  assert.match(report, /search result, not a novelty or\s+priority claim/);
  assert.match(report, /No public-page update or GitHub publication/);
  assert.match(readme, /counterexample only to full-tensor residual\s+control/);
  assert.match(readme, /ambient symmetric-tensor class/);
  assert.match(producer, /not inferred from this finite certificate/);
  assert.match(environment, /DGX not used/);
  assert.match(environment, /not a shell summation/);

  assert.doesNotMatch(report, /first ever|for the first time|proves novelty/i);
  assert.doesNotMatch(report, /\\mathfrak X_\\times\s*\\lesssim\s*r\s*\\tag/);
  assert.doesNotMatch(report, /proves unconditional global regularity/i);
  assert.doesNotMatch(report, /solves? the Millennium problem/i);
});

test("reproduces the six-group exact R0.70V producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070v_exact_audit.py", research));
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
  assert.equal(archived.release, "R0.70V");
  assert.equal(
    archived.status,
    "response-distance-and-strain-projection-exact-audit",
  );
  assert.equal(Object.keys(archived.checks).length, 6);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the response chord and area identities", async () => {
  const ledger = (await archivedResult()).gramLedger;

  assert.equal(ledger.unitConstraintRemainder, "0");
  assert.equal(ledger.wedgeLagrangeResidual, "0");
  assert.equal(ledger.chordAreaResidual, "0");
  assert.equal(ledger.ratioSquareResidual, "0");
  assert.equal(
    ledger.ratioPremise,
    "-1<gamma<1; the quotient is not defined at either endpoint",
  );
  assert.deepEqual(ledger.gammaPlusEndpoint, {
    d: "0",
    kappa: "0",
    reading: "0/0 ratio is undefined; the frame-defect pair itself vanishes",
  });
  assert.deepEqual(ledger.gammaMinusEndpoint, {
    d: "2",
    kappa: "0",
    reading: "response chord is nonzero while covariance area vanishes",
  });
  assert.match(ledger.kernel, /1 - gamma/);
  assert.match(ledger.kernel, /V\(p\)-V\(q\)/);
  assert.match(ledger.area, /1 - gamma\^2/);
  assert.match(ledger.antiCorrelationBoundary, /sigma>0/);
});

test("locks the actual fixed-frame two-shell tensor obstruction", async () => {
  const ledger = (await archivedResult()).twoShellLedger;

  assert.match(ledger.field, /cos\(N\*x1\)/);
  assert.match(ledger.responseSupport, /radius-N and radius-4N/);
  assert.match(ledger.covariance, /Q=e3 tensor e3/);
  assert.match(ledger.topGapBoundary, /globally positive rank one/);
  assert.equal(ledger.residual, "r identically 0");
  assert.equal(ledger.trigonometricResidual, "0");
  assert.equal(ledger.hdotMinusOneSquared, ledger.hdotMinusOneExpected);
  assert.equal(ledger.hdotMinusOneSquared, "17*A**2*B**2/(225*N**2)");
  assert.equal(ledger.strainProjection, "0");
  assert.equal(ledger.shearContraction, "0");
});

test("locks the strain-projection constants and their ambient scope", async () => {
  const ledger = (await archivedResult()).strainLedger;

  assert.equal(ledger.projectionSquare, "d12**2 + d13**2");
  assert.equal(
    ledger.frobeniusMinusTwiceProjection,
    ledger.expectedNonnegativeSlack,
  );
  assert.equal(ledger.workAbsolute, "1/2");
  assert.equal(ledger.palinstrophy, "1/2");
  assert.equal(ledger.projectedDefect, "1/2");
  assert.equal(ledger.hdotMinusOneFrobenius, "1");
  assert.equal(ledger.cauchyEqualityResidual, "0");
  assert.equal(ledger.frobeniusEqualityResidual, "0");
  assert.match(ledger.sharpnessScope, /ambient symmetric tensor class only/);
  assert.match(ledger.sharpnessScope, /not certified inside/);
});

test("locks the R0.70U projected critical subtotal", async () => {
  const ledger = (await archivedResult()).criticalLedger;

  assert.match(ledger.parameterPremise, /integer m>=2/);
  assert.match(ledger.parameterPremise, /A>delta>0/);
  assert.ok(everyEntryEquals(ledger.exactFrameDefectResidual, "0"));
  assert.equal(ledger.uPlusMinusKSubtotal, ledger.uPlusMinusKExpected);
  assert.equal(
    ledger.uPlusMinusKExpected,
    "delta**2*m**2/(2*(m**2 + 1)**4)",
  );
  assert.match(ledger.uProjectedReading, /epsilon\^2\*\(1-gamma\)\^2/);
  assert.deepEqual(ledger.orders, {
    X: "epsilon^2",
    r: "epsilon^2",
    signedWork: "epsilon",
    sqrtX: "abs(epsilon)",
  });
  assert.equal(ledger.residualThetaRatioPower, "1 - 2*theta");
  assert.match(ledger.ordersSource, /r and signedWork are inherited/);
});

test("locks the exact divergence-free triad-area identity", async () => {
  const archived = await archivedResult();
  const ledger = archived.triadLedger;

  assert.equal(ledger.frequencyConstraint, "n+k+l=0");
  assert.deepEqual(ledger.divergenceResiduals, ["0", "0", "0"]);
  assert.equal(ledger.identityResidual, "0");
  assert.match(ledger.identity, /\(l-k\)x\(nu_n x c\)/);
  assert.match(ledger.pairwiseBound, /\|a x b\|/);
  assert.match(ledger.responseWeightedConstant, /2\+2\*M_phi/);
  assert.match(ledger.areaWeightedBoundary, /sqrt\(sigma\)/);

  assert.match(archived.scalingLedger.premise, /dyadic mu=2\^J/);
  assert.equal(archived.scalingLedger.wholeSpaceXDegree, "3");
  assert.equal(archived.scalingLedger.wholeSpaceAreaIntegralDegree, "5");
  assert.equal(archived.scalingLedger.wholeSpaceDegreeGap, "2");
  assert.equal(archived.scalingLedger.fixedTorusXDegree, "6");
  assert.equal(archived.scalingLedger.fixedTorusAreaIntegralDegree, "8");
  assert.equal(archived.scalingLedger.fixedTorusDegreeGap, "2");
  assert.match(archived.scalingLedger.reading, /two inverse-frequency degrees/);
});

test("locks the narrow-band algebra and analytic boundaries", async () => {
  const archived = await archivedResult();
  const ledger = archived.narrowBandLedger;

  assert.ok(everyEntryEquals(ledger.expansionConstraintResidual, "0"));
  assert.equal(ledger.unitSphereQuadraticResidual, "0");
  assert.match(ledger.operatorReading, /beta\^2/);
  assert.match(ledger.finalAnalyticConstant, /2\*M_phi\^2\*delta\^2/);

  for (const token of [
    "star=Pi_0 block",
    "infinite-frame reconstruction",
    "global simple top gap",
    "does not calculate every nonnegative output",
    "no vector-valued shell summation",
  ]) {
    assert.ok(
      archived.analyticDependencies.some((item) => item.includes(token)),
      token,
    );
  }

  for (const token of [
    "no estimate X_cross<=C*r",
    "no a priori time integrability",
    "principal covariance stretching",
    "enstrophy closure",
    "Millennium problem",
  ]) {
    assert.ok(archived.claimBoundary.some((item) => item.includes(token)), token);
  }
});

test("locks every R0.70V certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 5);
  assert.match(sums, /\.\.\/\.\.\/r070v_exact_audit\.py/);
  assert.deepEqual(
    lines.map((line) => line.slice(66)),
    [
      "README.md",
      "command.txt",
      "environment.txt",
      "result.json",
      "../../r070v_exact_audit.py",
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
