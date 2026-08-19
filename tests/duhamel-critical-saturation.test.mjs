import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const auditUrl = new URL(
  "../research/duhamel_critical_saturation_audit.py",
  import.meta.url,
);
const noteUrl = new URL(
  "../research/duhamel_critical_saturation_note.md",
  import.meta.url,
);

test("states the exact R0.58 Duhamel theorem and its boundary", async () => {
  const note = await readFile(noteUrl, "utf8");

  assert.match(note, /d_L\(t;c\)/);
  assert.match(note, /1-e\^\{-2N\^2t\}/);
  assert.match(note, /\\frac1\{32L\}\\leq d_L\(t_L\)\\leq\\frac1\{2L\}/);
  assert.match(note, /C_\{\\rm RS\}=2\+\\sqrt2/);
  assert.match(note, /fixed-output .*Theta\(L\^\{-2\}\)/s);
  assert.match(note, /\\mathcal X\^\{-1\}.*Theta\(L\^\{-1\}\)/s);
  assert.match(note, /\\dot H\^\{1\/2\}.*Theta\(L\^\{-3\}\)/s);
  assert.match(note, /BMO\^\{-1\}_\{\\rm per\}.*Omega\(1\)/s);
  assert.match(note, /saturation theorem.*not a norm-inflation/s);
  assert.match(note, /Coiculescu and Palasek/);
  assert.match(note, /does \*\*not\*\* assert/);
  assert.match(note, /solution\s+of the Clay Millennium problem/);
});

test("reproduces the exact R0.58 integer regressions", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r058-audit-"));
  const output = join(scratch, "certificate.json");
  const { stdout, stderr } = await execFileAsync(
    "python3",
    [
      auditUrl.pathname,
      "--maximum-shell",
      "64",
      "--maximum-rs-level",
      "12",
      "--check",
      "--pretty",
      "--output",
      output,
    ],
    { cwd: new URL("..", import.meta.url).pathname },
  );

  assert.equal(stderr, "");
  assert.match(stdout, /"status": "passed"/);
  const certificate = JSON.parse(await readFile(output, "utf8"));
  assert.equal(certificate.checks.formalExactDuhamelCoefficientDerived, true);
  assert.equal(certificate.checks.formalRudinShapiroPrefixBound, true);
  assert.equal(
    certificate.checks.formalHeatBesovRatioHasUniformPositiveLowerBound,
    true,
  );
  assert.equal(
    certificate.checks.formalPeriodicBmoMinusOneRatioHasUniformPositiveLowerBound,
    true,
  );
  assert.equal(certificate.finiteRegressions.duhamelFamily.shellsChecked, 64);
  assert.equal(certificate.finiteRegressions.duhamelFamily.modesChecked, 2080);
  assert.equal(certificate.finiteRegressions.rudinShapiro.maximumLength, 4096);
  assert.equal(certificate.computation.floatingPointDecisionUse, false);
  assert.equal(certificate.computation.randomness, false);
  assert.equal(certificate.scope.notClaimed.length, 5);
});
