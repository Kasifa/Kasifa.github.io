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
const certificateRoot = new URL("certificates/r070z/", research);

async function archivedResult() {
  return JSON.parse(
    await readFile(new URL("result.json", certificateRoot), "utf8"),
  );
}

test("locks the R0.70Z report, literature, audit, and claim boundary", async () => {
  const [report, literature, audit, readme, producer, environment] =
    await Promise.all([
      readFile(new URL("r070z_report-source.md", research), "utf8"),
      readFile(new URL("r070z_literature_audit.md", research), "utf8"),
      readFile(new URL("r070z_independent_audit.md", research), "utf8"),
      readFile(new URL("README.md", certificateRoot), "utf8"),
      readFile(new URL("r070z_exact_audit.py", research), "utf8"),
      readFile(new URL("environment.txt", certificateRoot), "utf8"),
    ]);

  for (const token of [
    "R0.70Z — Principal-eigengap sign no-go",
    "same covariance at every point",
    "\\lambda_1-\\lambda_2\\ge8\\Lambda^2",
    "\\frac{\\lambda_1-\\lambda_2}{\\lambda_1}\\ge\\frac23",
    "\\frac{\\lambda_1-\\lambda_2}{\\operatorname{tr}Q}\\ge\\frac12",
    "\\frac{9\\sqrt{41}}{164}\\Lambda^3",
    "\\chi_Q",
    "two-channel pre-convolution response lift",
    "common-response channel remains order one",
  ]) {
    assert.ok(report.includes(token), token);
  }

  assert.match(literature, /PASS with a strict no-priority boundary/);
  assert.match(literature, /not evidence of priority/i);
  assert.match(audit, /\*\*Verdict:\*\* \*\*PASS\*\*/);
  assert.match(audit, /zero blocker, zero major issue, and zero minor issue/);
  assert.match(audit, /No publication, public-page update/);
  assert.match(readme, /same pointwise \\?\(Q\\?\)/);
  assert.match(producer, /do not prove a projector-coherence regularity/);
  assert.match(environment, /DGX used: no/);
  assert.match(environment, /GitHub publication: no/);
  assert.match(report, /No public-page update or GitHub publication/);

  assert.doesNotMatch(report, /first ever|for the first time|proves novelty/i);
  assert.doesNotMatch(report, /proves unconditional global regularity/i);
  assert.doesNotMatch(report, /solves? the Millennium problem/i);
  assert.doesNotMatch(report, /fixed normalized torus[^.]*exactly invariant/i);
});

test("reproduces the six-group exact R0.70Z producer", async () => {
  const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
  const producer = fileURLToPath(new URL("r070z_exact_audit.py", research));
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
  assert.equal(archived.release, "R0.70Z");
  assert.equal(archived.status, "principal-eigengap-sign-no-go");
  assert.equal(Object.keys(archived.checks).length, 6);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
});

test("locks the spectral split and the projector derivative", async () => {
  const archived = await archivedResult();
  const spectral = archived.spectralLedger;
  const projector = archived.projectorLedger;

  assert.equal(spectral.traceFreeSplitResidual, "0");
  assert.ok(
    spectral.axisymmetricBiaxialResidual.every((entry) => entry === "0"),
  );
  assert.equal(
    spectral.anisotropyNormSquare,
    spectral.anisotropyNormSquareExpected,
  );
  assert.match(spectral.positiveContraction, /2\*lambda_1/);
  assert.match(spectral.interpretation, /does not determine the sign/);

  assert.ok(projector.idempotenceResidual.every((entry) => entry === "0"));
  assert.ok(projector.eigenEquationResidual.every((entry) => entry === "0"));
  assert.match(projector.derivative, /lambda_1-lambda_j/);
  assert.match(projector.bestGapBound, /lambda_1-lambda_2/);
  assert.equal(projector.exactGeometricCoefficient, "|grad P_1|_F");
  assert.match(projector.criticalCoefficient, /sufficient upper majorant/);
  assert.match(projector.criticalCoefficient, /not an exact or necessary/);
  assert.match(projector.navierStokesScaling, /dimensionally critical/);
  assert.match(projector.navierStokesScaling, /fixed-torus L3 norm/);
});

test("locks the six-mode full, principal, and defect split", async () => {
  const base = (await archivedResult()).baseFieldLedger;

  assert.deepEqual(base.radiiSquared, [2, 41, 41]);
  assert.equal(base.strictFactorFourSquaredSlack, 9);
  assert.equal(base.modeCount, 6);
  assert.equal(base.principalWork, "9*sqrt(41)/164");
  assert.equal(base.principalWork, base.principalWorkExpected);
  assert.equal(base.defectWork, "-9*sqrt(41)/3362");
  assert.equal(base.fullWork, "351*sqrt(41)/6724");
  assert.equal(base.splitResidual, "0");
  assert.equal(base.lowEnergyUpper, "2");
  assert.equal(base.highPolarizationDot, "0");
  assert.equal(base.highEnergyUpper, "2");
  assert.equal(base.covarianceOperatorBound, "4");
});

test("locks identical covariance, opposite work, and the true eigengap", async () => {
  const archived = await archivedResult();
  const signPair = archived.signPairLedger;
  const gap = archived.eigengapLedger;

  assert.deepEqual(signPair.radiiSquared, [2, 41, 2401, 38809]);
  assert.deepEqual(signPair.strictFactorFourSquaredSlacks, [9, 1745, 393]);
  assert.equal(signPair.modeCount, 10);
  assert.equal(signPair.fillerInvolvingResonanceCount, 0);
  assert.equal(signPair.covarianceDifference, "0 at every Fourier output");
  assert.equal(signPair.positiveWork, "9*sqrt(41)/164");
  assert.equal(signPair.negativeWork, "-9*sqrt(41)/164");

  assert.equal(gap.fillerAmplitudeSquare, "494520");
  assert.equal(gap.fillerEigenvalueLower, "12");
  assert.equal(gap.baseOperatorUpper, "4");
  assert.equal(gap.absoluteGapCoefficient, "8");
  assert.equal(gap.topNormalizedGapCoefficient, "2/3");
  assert.equal(gap.traceRelativeGapCoefficient, "1/2");
  assert.match(gap.absoluteGap, /8\*Lambda\^2/);
  assert.match(gap.topNormalizedGap, />=2\/3/);
  assert.match(gap.traceRelativeGap, />=1\/2/);
});

test("locks the response lift and common-response obstruction", async () => {
  const lift = (await archivedResult()).responseLiftLedger;

  assert.ok(lift.operatorSplitResidual.every((entry) => entry === "0"));
  assert.deepEqual(lift.unitResponseTraces, {
    Hdelta: "1-Gamma(p,q)",
    Hminus: "Gamma(p,q)",
    Hplus: "1",
  });
  assert.equal(lift.r070x.modeCount, 36);
  assert.equal(lift.r070x.fullWork, "-137781/32780");
  assert.equal(lift.r070x.principalWork, "81*(kappa - 1)/20");
  assert.equal(
    lift.r070x.defectWork,
    "-81*(1639*kappa + 62)/32780",
  );
  assert.equal(lift.r070x.splitResidual, "0");
  assert.match(lift.sharpHHL.full, /M \+ 1/);
  assert.match(lift.sharpHHL.principal, /kappa_M - 1/);
  assert.match(lift.sharpHHL.defect, /M\*kappa_M \+ 1/);
  assert.match(lift.sequenceBoundary, /stays order one/);
  assert.match(lift.positiveEndpoint, /BMO/);
  assert.match(lift.positiveEndpoint, /other compensations are not excluded/);
});

test("locks analytic and claim boundaries", async () => {
  const archived = await archivedResult();

  assert.ok(
    archived.analyticDependencies.some((entry) =>
      entry.includes("zero-set parity lemma"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("identical pointwise frame covariance"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("common-response order-one channel"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("does not prove that projector coherence"),
    ),
  );
  assert.ok(
    archived.claimBoundary.some((entry) =>
      entry.includes("does not prove an enstrophy closure"),
    ),
  );
});

test("locks every R0.70Z certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");

  assert.equal(lines.length, 8);
  assert.deepEqual(
    lines.map((line) => line.slice(66)),
    [
      "README.md",
      "command.txt",
      "environment.txt",
      "result.json",
      "../../r070z_exact_audit.py",
      "../../r070x_exact_audit.py",
      "../../r070y_exact_audit.py",
      "../../r070y_report-source.md",
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
