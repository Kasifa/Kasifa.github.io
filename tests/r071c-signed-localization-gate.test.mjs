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
const certificateRoot = new URL("certificates/r071c/", research);

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
        [fileURLToPath(new URL("r071c_exact_audit.py", research))],
        options,
      ),
      execFileAsync(
        python,
        [fileURLToPath(new URL("r071c_independent_audit.py", research))],
        options,
      ),
    ]);
    return { exact, independent };
  })();
  return reproductionPromise;
}

test("locks the R0.71C report, literature audit, and claim boundary", async () => {
  const [report, literature, audit, producer, checker] = await Promise.all([
    readFile(new URL("r071c_report-source.md", research), "utf8"),
    readFile(new URL("r071c_literature_audit.md", research), "utf8"),
    readFile(new URL("r071c_independent_audit.md", research), "utf8"),
    readFile(new URL("r071c_exact_audit.py", research), "utf8"),
    readFile(new URL("r071c_independent_audit.py", research), "utf8"),
  ]);

  for (const token of [
    "R0.71C — Signed refinement defects, discontinuous normalization, and viscous sign creation",
    "Theorem 3.1 — consumer and refinement monotonicity",
    "W_B'(0)=12\\nu\\varepsilon^3",
    "The full fine coefficient can also start at zero",
    "Conditional theorem 9.1",
    "Signed time boxes control the wrong side",
    "Next justified gate: R0.71D",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /no Millennium-problem claim/i);
  assert.match(report, /no unconditional estimate for \(A_\{\\rm sb,\+\}\)/i);
  assert.match(literature, /negative literature finding, not a novelty or priority claim/i);
  assert.match(literature, /compatible comparison is[\s\S]*\\nu\\Lambda\(t\)\^2/i);
  assert.match(literature, /transport--filter commutators/);
  assert.match(audit, /Finite signed-before-square ledgers are monotone under refinement/);
  assert.match(audit, /full convolution has 50 nonzero generated modes/);
  assert.match(audit, /does not prove[\s\S]*adaptive or PDE-specific localization/i);
  assert.match(producer, /signed-refinement-and-viscous-sign-creation-gate/);
  assert.match(checker, /deliberately imports no project audit module/);

  for (const text of [report, literature, audit]) {
    assert.doesNotMatch(text, /proves unconditional global regularity/i);
    assert.doesNotMatch(text, /solves? the Millennium problem/i);
  }
});

test("reproduces both archived R0.71C exact certificates byte for byte", async () => {
  const [exactText, independentText, reproduced] = await Promise.all([
    readFile(new URL("result.json", certificateRoot), "utf8"),
    readFile(new URL("independent-result.json", certificateRoot), "utf8"),
    reproduceBoth(),
  ]);

  assert.equal(reproduced.exact.stderr, "");
  assert.equal(reproduced.independent.stderr, "");
  assert.equal(reproduced.exact.stdout, exactText);
  assert.equal(reproduced.independent.stdout, independentText);
  assert.deepEqual(JSON.parse(reproduced.exact.stdout), JSON.parse(exactText));
  assert.deepEqual(
    JSON.parse(reproduced.independent.stdout),
    JSON.parse(independentText),
  );
});

test("locks the exact refinement, Stokes, true-NSE, and conditional ledgers", async () => {
  const archived = await archivedJson("result.json");

  assert.equal(archived.release, "R0.71C");
  assert.equal(
    archived.status,
    "signed-refinement-and-viscous-sign-creation-gate",
  );
  assert.equal(Object.keys(archived.checks).length, 15);
  assert.ok(Object.values(archived.checks).every((value) => value === true));
  assert.equal(
    archived.partitionLedger.treeIdentity,
    "E_leaves=E_root+sum_(internal v) delta_v",
  );
  assert.equal(archived.normalizationDiscontinuity.valueAtEtaZeroByConvention, "0");
  assert.equal(archived.twoTriadWitness.orderedZeroSumResonances, 24);
  assert.deepEqual(archived.twoTriadWitness.outputRadiiSquared, [4, 4]);
  assert.deepEqual(archived.twoTriadWitness.selectedWorks, ["2", "-2"]);
  assert.equal(archived.twoTriadWitness.coarseLedgerAtZero, "0");
  assert.equal(archived.twoTriadWitness.fineLedgerAtZero, "1/2");
  assert.equal(
    archived.StokesEvolution.parentWork,
    "2*(exp(-8*nu*t)-exp(-14*nu*t))",
  );
  assert.equal(
    archived.StokesEvolution.rootLedgerAtComparisonTime,
    "2**(2/3)/64",
  );
  assert.equal(
    archived.NavierStokesInitialTrace.parentDerivativeAtZero,
    "4*epsilon**3*(19*epsilon + 15*nu)/5",
  );
  assert.equal(
    archived.zeroToPositiveFineCoefficient.positiveOutputCoefficientAtZero,
    "0",
  );
  assert.match(
    archived.shellInjectionReduction.conditionalConclusion,
    /H1 continuation/,
  );
  assert.match(
    archived.shellInjectionReduction.direction,
    /<= integral_I/,
  );
});

test("locks the independent full-convolution reconstruction", async () => {
  const independent = await archivedJson("independent-result.json");

  assert.equal(independent.version, "R0.71C-independent");
  assert.equal(independent.status, "pass");
  assert.equal(independent.fourier.field.orderedZeroSumResonances, 24);
  assert.equal(independent.fourier.field.crossTriadResonances, 0);
  assert.equal(
    independent.fourier.navierStokesDerivative.nonlinearGeneratedModes,
    50,
  );
  assert.equal(
    independent.fourier.navierStokesDerivative.quarticParentRate,
    "76/5",
  );
  assert.equal(
    independent.fourier.navierStokesDerivative.directReconstructionResidual,
    "0",
  );
  assert.equal(
    independent.normalizationDiscontinuity.normalizedValueAtEtaZero,
    "0",
  );
  assert.equal(independent.balancedHHL.support.initialPositiveOutputCount, 0);
  assert.equal(independent.balancedHHL.support.allInitialOutputWorksZero, true);
  assert.equal(
    independent.shell.signedIntervalObstruction.notAnNSECounterexample,
    true,
  );
  assert.ok(
    independent.claimBoundary.notProved.some((entry) =>
      entry.includes("adaptive or PDE-specific localization"),
    ),
  );
});

test("verifies every listed R0.71C certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");
  assert.ok(lines.length >= 7);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    assert.equal(createHash("sha256").update(payload).digest("hex"), match[1]);
  }
});
