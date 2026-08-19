import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { readFile } from "node:fs/promises";
import { promisify } from "node:util";
import test from "node:test";

const execute = promisify(execFile);
const auditUrl = new URL(
  "../research/fourier_critical_charge_bridge_audit.py",
  import.meta.url,
);
const noteUrl = new URL(
  "../research/fourier_critical_charge_bridge_note.md",
  import.meta.url,
);
const projectRoot = new URL("..", import.meta.url);

test("states the R0.55 critical bridge and scalar-charge no-go with strict scope", async () => {
  const [audit, note] = await Promise.all([
    readFile(auditUrl, "utf8"),
    readFile(noteUrl, "utf8"),
  ]);

  assert.match(audit, /X\^{-1\} is scale critical/);
  assert.match(audit, /high--high-to-low saturation family/);
  assert.match(audit, /additive under Fourier convolution/);
  assert.match(note, /\\|P\(u\\cdot\\nabla v\)\\\|_\{\\mathcal X\^\{-1\}\}/);
  assert.match(note, /M\(z\)=z\+M\(z\)\^2/);
  assert.match(note, /Every map satisfying \(6\.1\)--\(6\.2\) is identically zero/);
  assert.match(note, /No\s+continuity or measurability assumption is needed/);
  assert.match(note, /Nothing here proves[\s\S]*three-dimensional Navier--Stokes/);
  assert.match(note, /must not be compared numerically with the R0\.54\s+radius/);
});

test("reproduces the exact R0.55 finite regressions", async () => {
  const { stdout, stderr } = await execute(
    "python3",
    [
      auditUrl.pathname,
      "--max-triad-index",
      "1000",
      "--max-catalan-degree",
      "64",
      "--rotation-radius",
      "3",
      "--check",
    ],
    {
      cwd: projectRoot.pathname,
      maxBuffer: 10 * 1024 * 1024,
    },
  );
  const certificate = JSON.parse(stdout);

  assert.match(stderr, /"status": "passed"/);
  assert.equal(certificate.checks.formalXminusOneScalingExponentIsZero, true);
  assert.equal(certificate.checks.formalTriadSymbolIdentityIsExactlyOne, true);
  assert.equal(certificate.checks.finiteTriadRegressionPassed, true);
  assert.equal(
    certificate.exactSaturationFamily.finiteRegression.checkedTriads,
    1000,
  );
  assert.equal(
    certificate.exactSaturationFamily.finiteRegression.allRatiosExactlyOne,
    true,
  );
  assert.equal(
    certificate.scalarChargeNoGo.finiteRegression.allWitnessesInSO3,
    true,
  );
  assert.equal(certificate.scalarDegreeMajorant.exactRadius.numerator, "1");
  assert.equal(certificate.scalarDegreeMajorant.exactRadius.denominator, "4");
  assert.equal(
    certificate.bridgeDecision.fullPdeToCriticalScalarDegreeMajorant,
    "finite constant; passes",
  );
});
