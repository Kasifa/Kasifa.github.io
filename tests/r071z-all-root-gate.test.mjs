import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const certificateRoot = new URL("research/certificates/r071z/", root);

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

test("certifies the R0.71Z all-root algebra with independent producers", async () => {
  const [producer, independent, producerScript, independentScript] =
    await Promise.all([
      readFile(new URL("result.json", certificateRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-result.json", certificateRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("research/r071z_exact_audit.py", root), "utf8"),
      readFile(new URL("research/r071z_independent_audit.py", root), "utf8"),
    ]);

  assert.equal(producer.release, "R0.71Z");
  assert.equal(producer.status, "passed");
  assert.equal(producer.checks.length, 8);
  assert.ok(producer.checks.every((entry) => entry.passed));
  assert.equal(independent.release, "R0.71Z");
  assert.equal(independent.passed, true);
  assert.equal(independent.checkCount, 15);
  assert.equal(independent.passedCheckCount, 15);
  assert.ok(independent.checks.every((entry) => entry.passed));

  assert.ok(Math.abs(Number(producer.lattice.tailPower) + 2) < 2e-5);
  assert.ok(
    producer.boundedCouplingEnvelope.rows.every(
      (row) => Math.abs(Number(row.tailPowerInM) + 2) < 2e-5,
    ),
  );
  assert.equal(Number(producer.strongCouplingDiagnostic.algebraicMPower), 0);
  assert.ok(
    Math.abs(Number(producer.strongCouplingDiagnostic.fittedMPower)) < 2e-5,
  );
  assert.equal(Number(producer.amplitudeOptimizer.uStar), 3);
  assert.ok(
    Number(producer.fixedWindowRetention.rows.at(-1).log10ThetaI) < -900,
  );

  assert.equal(independent.independence.importsProducer, false);
  assert.equal(independent.independence.readsProducerResult, false);
  assert.equal(independent.finiteEvolution.maximumSkewAdjointDefect, 0);
  assert.ok(independent.finiteEvolution.energyIdentityRelativeDefect < 1e-11);
  assert.ok(independent.finiteEvolution.qIntegralOverReportedBound < 1);
  assert.ok(independent.multiplierIntegrals.L1OverBound < 1);
  assert.ok(independent.multiplierIntegrals.L2OverBound < 1);
  assert.ok(independent.complexBvSampling.leftOverRight < 1);

  assert.doesNotMatch(producerScript, /import\s+.*r071z_independent/);
  assert.doesNotMatch(
    independentScript,
    /(?:from|import)\s+.*r071z_exact|open\([^)]*result\.json/,
  );
});

test("states the theorem, mixed-window scope, and open boundaries", async () => {
  const [report, gap, literature, audit] = await Promise.all([
    readFile(new URL("research/r071z_report-source.md", root), "utf8"),
    readFile(new URL("research/r071z_gap_matrix.md", root), "utf8"),
    readFile(new URL("research/r071z_literature_audit.md", root), "utf8"),
    readFile(new URL("research/r071z_independent_audit.md", root), "utf8"),
  ]);

  for (const token of [
    "W^{2,1}",
    "G_{\\rm all}^{\\rm ex}",
    "independent of the root count",
    "skew-adjoint",
    "launch-inclusive",
    "launch-inclusive ledger",
    "M^{-2}",
    "M^{6/7}",
    "retention",
    "strong-coupling",
    "observation layer",
  ]) {
    assert.ok(report.includes(token), token);
  }

  assert.match(report, /does not prove.*Navier--Stokes/is);
  assert.match(report, /not a\s+construction of a strong-coupling/is);
  assert.match(gap, /all-root/i);
  assert.match(gap, /floor/i);
  assert.match(literature, /10\.1007\/s00365-008-9010-6/i);
  assert.match(literature, /10\.1090\/S0002-9947-1953-0054167-3/i);
  assert.match(audit, /Decision:\*\* PASS/i);
});

test("verifies the R0.71Z checksum ledger", async () => {
  const ledger = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
  const lines = ledger.trim().split("\n");
  assert.equal(lines.length, 12);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, line);
    const payload = await readFile(new URL(match[2], certificateRoot));
    assert.equal(sha256(payload), match[1], match[2]);
  }
});
