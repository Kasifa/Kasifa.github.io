import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the R0.69M criterion comparison and route decision", async () => {
  const note = await readFile(
    new URL("../research/criterion_comparison_pressure_budget_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("B_\\infty(r)"));
  assert.ok(note.includes("=\\frac1{120}\\mathfrak M_2(r)"));
  assert.ok(note.includes("\\frac{\\mathfrak M_2(r)}{B_\\infty}\\geq2^{4k-1}"));
  assert.ok(note.includes("a_N=N^{-1/2}"));
  assert.ok(note.includes("N_1\\to\\infty"));
  assert.ok(note.includes("grows like \\(N^{1/2}\\)"));
  assert.ok(note.includes("r^3\\left|\\int\\phi S:\\nabla^2(-\\Delta)^{-1}q_0"));
  assert.ok(note.includes("3/3+2/3=5/3<2"));
  assert.match(note, /not a new epsilon-regularity\s+criterion/i);
  assert.match(note, /functional counterexample at\s+one time/i);
  assert.match(note, /does\s+not solve the Millennium Problem/i);
  assert.match(note, /R0\.69N will test/i);
});

test("reproduces the R0.69M exponent and Morrey audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/criterion_comparison_pressure_budget_audit.py", import.meta.url).pathname],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 12);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.equal(result.morreyComparison.geometricSeriesConstant, "1/120");
  assert.equal(result.highFrequencyWitness.powerExponents.nearL2Source, "1");
  assert.equal(result.highFrequencyWitness.powerExponents.absoluteAnnularUQ, "1/2");
  assert.equal(result.lowerExponentRepair.mixedGradientExponentSum, "5/3");
});

test("archives the source-locked R0.69M certificate", async () => {
  const certificateRoot = new URL("../research/certificates/r069m/", import.meta.url);
  const [certificateText, sumsText, readme, resources] = await Promise.all([
    readFile(new URL("criterion-comparison-pressure-budget.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("resources.csv", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.keys(certificate.checks).length, 14);
  assert.ok(Object.values(certificate.checks).every(Boolean));
  assert.equal(
    certificate.provenance.sourceCommit,
    "dd6411d1386328a3b873c410dfe5d52e89596591",
  );
  assert.match(readme, /not a new epsilon-regularity criterion/i);
  assert.match(resources, /exited:0/);

  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
