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
const certificateRoot = new URL("certificates/r071f/", research);

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
        [fileURLToPath(new URL("r071f_exact_audit.py", research))],
        options,
      ),
      execFileAsync(
        python,
        [fileURLToPath(new URL("r071f_independent_audit.py", research))],
        options,
      ),
    ]);
    return { exact, independent };
  })();
  return reproductionPromise;
}

test("locks the R0.71F local-trace theorem and proof boundary", async () => {
  const [report, literature, audit, producer, checker] = await Promise.all([
    readFile(new URL("r071f_report-source.md", research), "utf8"),
    readFile(new URL("r071f_literature_audit.md", research), "utf8"),
    readFile(new URL("r071f_independent_audit.md", research), "utf8"),
    readFile(new URL("r071f_exact_audit.py", research), "utf8"),
    readFile(new URL("r071f_independent_audit.py", research), "utf8"),
  ]);

  for (const token of [
    "R0.71F — Skewed-cylinder localization preserves heat packing but not the bottom trace",
    "Complete ledger on a moving cutoff",
    "Projected and material ledgers are the same ledger",
    "Theorem 5.1 — matched local projected-Lamb continuation criterion",
    "Unconditional local heat packing",
    "Exact local cutoff witness",
    "A matched partition cannot hide the trace cost",
    "Theorem 9.1 — geometry-only subcritical trace no-go",
    "Next justified gate: R0.71G",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(report, /no full-frame two-sided estimate is claimed/i);
  assert.ok(
    report.includes(
      "The critical \\(Cr^{-2}\\) factor is saturated,\n   not disproved.",
    ),
  );
  assert.match(literature, /状态：bounded primary-source audit/);
  assert.match(
    literature,
    /不是全局文献不存在证明，也不是新颖性\s+或优先权结论/,
  );
  assert.match(audit, /\*\*Final status:\*\* \*\*PASS AFTER LISTED CORRECTIONS\*\*/);
  assert.match(audit, /does not claim originality or exhaustive nonexistence/i);
  assert.match(producer, /localized-heat-packing-and-sharp-bottom-trace-obstruction/);
  assert.match(checker, /does not import the exact producer/i);
});

test("reproduces both archived R0.71F certificates byte for byte", async () => {
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

test("locks all 9 exact checks, full-datum norms, trace, Gamma, and partition fields", async () => {
  const archived = await archivedJson("result.json");

  assert.equal(archived.release, "R0.71F");
  assert.equal(
    archived.status,
    "localized-heat-packing-and-sharp-bottom-trace-obstruction",
  );
  assert.equal(Object.keys(archived.checks).length, 9);
  assert.ok(Object.values(archived.checks).every(Boolean));

  assert.deepEqual(
    archived.lowBlockReconstruction.fullDatumNormsAtAEqualsKEqualsOne,
    { enstrophy: "8", velocityL2Squared: "6" },
  );
  assert.equal(
    archived.lowBlockReconstruction.normalizedAtAEqualsKEqualsOne.enstrophy,
    "4",
  );
  assert.equal(
    archived.lowBlockReconstruction.normalizedAtAEqualsKEqualsOne.palinstrophy,
    "4",
  );

  assert.equal(archived.heatTrace.qOfS, "q0*exp(-2*K**2*s)");
  assert.equal(
    archived.heatTrace.finiteHeightIntegral,
    "q0*(exp(K**2*h) - 1)*(exp(K**2*h) + 1)*exp(-2*K**2*h)/(2*K**2)",
  );
  assert.equal(
    archived.heatTrace.finiteTraceFactor,
    "2*K**2*exp(2*K**2*h)/((exp(K**2*h) - 1)*(exp(K**2*h) + 1))",
  );
  assert.equal(archived.heatTrace.matchedHeight, "h=theta/K**2");
  assert.equal(
    archived.heatTrace.alphaMoment,
    "q0*gamma(alpha)/(2**alpha*K**(2*alpha))",
  );
  assert.equal(
    archived.heatTrace.alphaMomentTraceFactor,
    "2**alpha*K**(2*alpha)/gamma(alpha)",
  );
  assert.deepEqual(archived.heatTrace.selectedMoments, {
    "alpha=1": "q0/(2*K**2)",
    "alpha=1/2": "sqrt(2)*sqrt(pi)*q0/(2*K)",
    "alpha=2": "q0/(4*K**4)",
  });

  assert.equal(
    archived.localizedIdentity.strictPositivity,
    "positive for every nonzero smooth phi >= 0 on the torus",
  );
  assert.equal(
    archived.matchedPartition.hypotheses.matchedRadius,
    "r=rho/K",
  );
  assert.equal(
    archived.matchedPartition.hypotheses.overlap,
    "sum_Q 1_supp(phi_Q) <= N",
  );
  assert.equal(
    archived.matchedPartition.denominatorSumUpper,
    "8*K**6*a**2*(C0*rho**2 + C1)/rho**2",
  );
  assert.equal(
    archived.matchedPartition.positiveQuotientSumLower,
    "K**6*a**4*rho**2/(2*(C0*rho**2 + C1))",
  );
  assert.equal(
    archived.matchedPartition.positiveQuotientSumUpper,
    "2*K**6*N*a**4",
  );
  assert.equal(archived.matchedPartition.positiveWorkSum, "2*K**6*a**3");
  assert.equal(
    archived.matchedPartition.fixedEnergySequenceAEqualsOneOverK
      .velocityL2Squared,
    "6",
  );
  assert.equal(
    archived.matchedPartition.fixedEnergySequenceAEqualsOneOverK
      .normalizedBottomLower,
    "rho**2/(16*(C0*rho**2 + C1))",
  );
  assert.equal(
    archived.matchedPartition.fixedEnergySequenceAEqualsOneOverK
      .normalizedInfiniteBulkUpper,
    "N/(8*K**2)",
  );
  assert.match(archived.routeDecision.nextGate, /R0\.71G/);
});

test("locks all 6 independent finite FFT and finite-height checks", async () => {
  const independent = await archivedJson("independent-result.json");

  assert.equal(independent.version, "R0.71F-independent");
  assert.equal(independent.status, "pass");
  assert.equal(Object.keys(independent.checks).length, 6);
  assert.ok(Object.values(independent.checks).every(Boolean));
  assert.deepEqual(
    independent.cases.map(({ K, a }) => ({ K, a })),
    [
      { K: 1, a: 1 },
      { K: 2, a: 0.5 },
      { K: 4, a: 0.25 },
      { K: 8, a: 0.125 },
    ],
  );
  for (const sample of independent.cases) {
    assert.equal(sample.grid, 48);
    assert.ok(sample.cutoffMinimum > 0);
    assert.ok(sample.lowOmegaMaxError < sample.tolerances.field);
    assert.ok(sample.lowProjectedLambMaxError < sample.tolerances.field);
    assert.ok(
      sample.maxHeatDecayRelativeError < sample.tolerances.decayRelative,
    );
    assert.ok(sample.workIdentityError < sample.tolerances.work);
    assert.ok(
      Math.abs(sample.finiteWindow.traceResidual) <
        sample.tolerances.finiteTraceRelative,
    );
  }
});

test("verifies every listed R0.71F certificate payload by SHA-256", async () => {
  const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = sums.trim().split("\n");
  assert.equal(lines.length, 10);
  assert.deepEqual(
    new Set(lines.map((line) => line.slice(66))),
    new Set([
      "README.md",
      "command.txt",
      "environment.txt",
      "result.json",
      "independent-result.json",
      "../../r071f_exact_audit.py",
      "../../r071f_independent_audit.py",
      "../../r071f_report-source.md",
      "../../r071f_literature_audit.md",
      "../../r071f_independent_audit.md",
    ]),
  );
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    assert.equal(createHash("sha256").update(payload).digest("hex"), match[1]);
  }
});
