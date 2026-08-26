import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const certificateRoot = new URL("research/certificates/r071y/", root);

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

test("certifies the R0.71Y operator-sampling algebra independently", async () => {
  const [producer, independent, producerScript, independentScript] =
    await Promise.all([
      readFile(new URL("result.json", certificateRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-result.json", certificateRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("research/r071y_exact_audit.py", root), "utf8"),
      readFile(new URL("research/r071y_independent_audit.py", root), "utf8"),
    ]);

  assert.equal(producer.release, "R0.71Y");
  assert.equal(producer.status, "passed");
  assert.equal(producer.checks.length, 13);
  assert.ok(producer.checks.every((entry) => entry.passed));
  assert.equal(independent.release, "R0.71Y");
  assert.equal(independent.status, "passed");
  assert.equal(independent.checks.length, 12);
  assert.ok(independent.checks.every((entry) => entry.passed));

  assert.ok(Math.abs(producer.latticeTailPower + 1) < 0.002);
  assert.ok(
    Math.abs(producer.separatedRootEnvelope.fixedGapTailPower + 2) < 0.002,
  );
  assert.ok(
    Math.abs(producer.separatedRootEnvelope.quasiuniformGapTailPower + 1) <
      0.002,
  );
  assert.ok(Math.abs(producer.criticalCoupling.tailPower) < 0.002);
  assert.ok(
    Math.abs(producer.subcriticalCoupling.tailPower + 1 / 3) < 0.002,
  );
  assert.ok(
    producer.equalGridInverseLower.at(-1).log10InverseLower > 40,
  );

  assert.doesNotMatch(producerScript, /import\s+.*r071y_independent/);
  assert.doesNotMatch(
    independentScript,
    /(?:from|import)\s+.*r071y_exact|open\([^)]*result\.json/,
  );
});

test("states the exact theorem, corrigendum, and every mandatory boundary", async () => {
  const [report, gap, literature, audit, correctedX] = await Promise.all([
    readFile(new URL("research/r071y_report-source.md", root), "utf8"),
    readFile(new URL("research/r071y_gap_matrix.md", root), "utf8"),
    readFile(new URL("research/r071y_literature_audit.md", root), "utf8"),
    readFile(new URL("research/r071y_independent_audit.md", root), "utf8"),
    readFile(new URL("research/r071x_gap_matrix.md", root), "utf8"),
  ]);

  for (const token of [
    "\\delta_{\\mathrm{obs},N}^{4/3}}{N}",
    "G_N^{\\rm ex}",
    "skew-adjoint",
    "\\eta_{\\mathrm{Dyson},N}",
    "\\delta_{\\mathrm{obs},N}",
    "C_{A_0,\\nu,d}",
    "B_N=\\frac{b_0q}{Q}",
    "\\Lambda_1(I;u)",
    "\\Lambda_1",
    "\\mathscr S_N",
    "\\|\\mathsf M^{-1}\\|_2",
    "\\mathcal J_R",
    "quadratic proliferation",
  ]) {
    assert.ok(report.includes(token), token);
  }

  assert.match(report, /selected.*exact roots/is);
  assert.match(report, /real shear coefficients/is);
  assert.match(report, /unit carrier phases/is);
  assert.match(report, /matched to the full/is);
  assert.match(report, /does not prove.*all-root count/is);
  assert.match(report, /does not prove.*universal/is);
  assert.match(report, /A_\{0,N\}\\to0/);
  assert.match(gap, /Y17/);
  assert.match(audit, /13 of 13/);
  assert.match(audit, /12 of 12/);
  assert.match(literature, /10\.1007\/BF01398878/);
  assert.match(literature, /10\.3934\/dcdss\.2020082/);
  assert.match(literature, /10\.1137\/S0895479803438225/i);

  assert.match(correctedX, /heat-weighted/i);
  assert.match(correctedX, /no dimension-independent lower bound/i);
  assert.match(correctedX, /eta_\{\\mathrm\{Dyson\},N\}/);
  assert.doesNotMatch(
    correctedX,
    /c\\frac\{P\}\{q\^2\}\\\|z_N\\\|_2\s*\\le\s*\\delta_\{\\mathrm\{op\},N\}/,
  );
});

test("verifies the exact lattice identity and checksum ledger", async () => {
  for (const nValue of [1, 2, 4, 8, 16, 64]) {
    const mValue = 2 * nValue + 1;
    const ks = (mValue * (mValue + 1) * (2 * mValue + 1)) / 6;
    assert.ok((nValue * mValue) / ks <= 3 / (4 * nValue));
  }

  const ledger = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = ledger.trim().split("\n");
  assert.ok(lines.length >= 13);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    assert.equal(sha256(payload), match[1], match[2]);
  }
});
