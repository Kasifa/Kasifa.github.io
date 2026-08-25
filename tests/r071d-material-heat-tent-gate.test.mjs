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
const certificateRoot = new URL("certificates/r071d/", research);

async function archivedJson(name) {
  return JSON.parse(await readFile(new URL(name, certificateRoot), "utf8"));
}

let reproductionPromise;

function reproduceBoth() {
  reproductionPromise ??= (async () => {
    const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));
    const options = {
      cwd: fileURLToPath(root),
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    };
    const [exact, independent] = await Promise.all([
      execFileAsync(
        python,
        [fileURLToPath(new URL("r071d_exact_audit.py", research))],
        options,
      ),
      execFileAsync(
        python,
        [fileURLToPath(new URL("r071d_independent_audit.py", research))],
        options,
      ),
    ]);
    return { exact, independent };
  })();
  return reproductionPromise;
}

test("locks the R0.71D theorem, literature boundary, and exact scope", async () => {
  const [report, literature, independent, producer, checker] = await Promise.all([
    readFile(new URL("r071d_report-source.md", research), "utf8"),
    readFile(new URL("r071d_literature_audit.md", research), "utf8"),
    readFile(new URL("r071d_independent_audit.md", research), "utf8"),
    readFile(new URL("r071d_exact_audit.py", research), "utf8"),
    readFile(new URL("r071d_independent_audit.py", research), "utf8"),
  ]);

  for (const token of [
    "R0.71D — Complete material heat tents and the critical viscous refinement obstruction",
    "The complete material heat-tent ledger",
    "Exact smooth NSE material witness",
    "Theorem 11.1 — material heat-tent critical obstruction",
    "The parabolic box saturates R0.71C",
    "Next justified gate: R0.71E",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /no Millennium-problem claim/i);
  assert.match(report, /does \*\*not\*\* show that every adaptive tent defect diverges/i);
  assert.match(literature, /不是数学上的不存在证明，也不是新颖性或优先权证明/);
  assert.match(literature, /Runlong Yu 2026 年的预印本/);
  assert.match(literature, /Yang 型 skewed-cylinder 覆盖理论/);
  assert.match(independent, /pointwise material/i);
  assert.match(independent, /imports no project audit module/i);
  assert.match(producer, /material-heat-tent-critical-defect-gate/);
  assert.match(checker, /deliberately imports no project audit module/);
});

test("reproduces both archived R0.71D certificates byte for byte", async () => {
  const [exactText, independentText, reproduced] = await Promise.all([
    readFile(new URL("result.json", certificateRoot), "utf8"),
    readFile(new URL("independent-result.json", certificateRoot), "utf8"),
    reproduceBoth(),
  ]);

  assert.equal(reproduced.exact.stderr, "");
  assert.equal(reproduced.independent.stderr, "");
  assert.equal(reproduced.exact.stdout, exactText);
  assert.equal(reproduced.independent.stdout, independentText);
});

test("locks the material shear, critical defect, and vertical ledger", async () => {
  const archived = await archivedJson("result.json");

  assert.equal(archived.release, "R0.71D");
  assert.equal(archived.status, "material-heat-tent-critical-defect-gate");
  assert.equal(Object.keys(archived.checks).length, 15);
  assert.ok(Object.values(archived.checks).every(Boolean));
  assert.equal(archived.completeTentIdentity.verticalFluxIdentityResidual, "0");
  assert.equal(archived.materialChildren.parentSignedLedger, "0");
  assert.equal(
    archived.materialChildren.normalizedFineLedger,
    "k**2*nu**2*rho**2/(rho + 2)",
  );
  assert.equal(archived.parabolicBox.cauchyResidual, "0");
  assert.equal(
    archived.bottomCommutator.plusThreeModeCoefficient,
    "-mode_amplitude*multiplier*rho/4",
  );
  assert.match(archived.routeDecision.nextGate, /transport-filter and pressure sectors/);
});

test("locks the independent pointwise-material reconstruction", async () => {
  const independent = await archivedJson("independent-result.json");

  assert.equal(independent.version, "R0.71D-independent");
  assert.equal(independent.status, "pass");
  assert.equal(independent.materialShear.weights.pointwiseMaterial, true);
  assert.equal(independent.materialShear.weights.materialDerivativePlus, "0");
  assert.equal(independent.materialShear.localLedger.parentSignedBeta, "0");
  assert.equal(
    independent.materialShear.localLedger.fineLedgerOverTotalY,
    "nu^2*k^2*rho^2/(2+rho)",
  );
  assert.equal(independent.materialShear.parabolicInterval.equalityResidual, "0");
  assert.equal(independent.materialShear.parabolicInterval.scaleIndependentInK, true);
  assert.ok(
    independent.embedded2DStressCheck.numericQuadrature.maxAbsError < 2e-13,
  );
  assert.match(independent.claimBoundary.scope, /not a general no-go theorem/);
});

test("verifies every listed R0.71D certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");
  assert.equal(lines.length, 10);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    assert.equal(createHash("sha256").update(payload).digest("hex"), match[1]);
  }
});
