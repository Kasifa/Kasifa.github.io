import assert from "node:assert/strict";
import { execFile } from "node:child_process";
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
