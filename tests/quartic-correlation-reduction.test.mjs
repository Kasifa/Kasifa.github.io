import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const repository = new URL("..", import.meta.url).pathname;
const noteUrl = new URL(
  "../research/quartic_correlation_reduction_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/quartic_correlation_reduction_audit.py",
  import.meta.url,
);
const certificateRoot = new URL("../research/certificates/r062/", import.meta.url);

test("states the R0.62 all-index quartic ceiling and its exact boundary", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);

  assert.match(
    note,
    /R0\.62 — Quartic correlation reduction and the first all-index remainder bound/,
  );
  assert.ok(note.includes("k\\in\\{-1,0,1\\}"));
  assert.ok(note.includes("\\sum_{k=-1}^{1} I_{L,k}O_{M,m-1,k}"));
  assert.ok(note.includes("\\Bigl(\\frac mM\\Bigr)^2\\sqrt M"));
  assert.ok(note.includes("C_4<7.9"));
  assert.match(note, /one square-root factor remains/);
  assert.match(note, /does not solve the Clay Millennium problem/);
  assert.match(audit, /finite enumeration is a regression/i);
  assert.doesNotMatch(note, /我们|攻关|主攻|突破千禧年/);
});

test("reproduces the exact three-carry factorization on finite dyadic boxes", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r062-correlation-"));
  const output = join(scratch, "audit.json");
  await execFileAsync(
    process.env.CODEX_PYTHON || "python3",
    [
      auditUrl.pathname,
      "--maximum-level",
      "3",
      "--check",
      "--output",
      output,
    ],
    { cwd: repository },
  );
  const report = JSON.parse(await readFile(output, "utf8"));
  assert.equal(report.status, "passed");
  assert.equal(report.checks.onlyThreeCarriesOccur, true);
  assert.equal(report.checks.directCorrelationEqualsCarryFactorization, true);
  assert.equal(report.coverage.parameterBoxes, 16);
  assert.equal(report.coverage.targetBlocks, 60);
  assert.equal(report.coverage.directCarrierTriples, 228225);
  assert.ok(Number(report.analyticConstants.C_quartic) < 7.9);
  assert.match(report.analyticConstants.bound, /sqrt\(M\)/);
});

test("archives the extended R0.62 full-target scans", async () => {
  const [aggregateText, correlationText, sumsText] = await Promise.all([
    readFile(new URL("extended-quartic-exploration.json", certificateRoot), "utf8"),
    readFile(new URL("correlation-reduction-audit.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const aggregate = JSON.parse(aggregateText);
  const correlation = JSON.parse(correlationText);

  assert.equal(aggregate.status, "passed");
  assert.equal(aggregate.coverage.distinctParameterTargetTriples, 4042);
  assert.equal(aggregate.coverage.orderedQuarticPathsAcrossDistinctTriples, 27082065198);
  assert.deepEqual(aggregate.observations.maximumNormalizedSignedRatio, {
    L: 4,
    M: 64,
    target: 64,
    value: 0.0013286562612066827,
  });
  assert.equal(correlation.status, "passed");
  assert.ok(Number(correlation.analyticConstants.C_quartic) < 7.9);

  const entries = sumsText.trim().split("\n").map((line) => {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "Malformed SHA256SUMS line: " + line);
    return { expected: match[1], file: match[2] };
  });
  assert.equal(entries.length, 15);
  for (const entry of entries) {
    const payload = await readFile(new URL(entry.file, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, entry.expected, entry.file + " hash mismatch");
  }
});
