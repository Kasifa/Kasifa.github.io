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
  "../research/quartic_weighted_cycle_spectral_note.md",
  import.meta.url,
);
const finiteAuditUrl = new URL(
  "../research/quartic_weighted_cycle_finite_iterate.py",
  import.meta.url,
);
const spectralAuditUrl = new URL(
  "../research/quartic_weighted_cycle_spectral_audit.py",
  import.meta.url,
);
const certificateRoot = new URL("../research/certificates/r066/", import.meta.url);

test("states the R0.66 nonzero spectral projection and exact claim boundary", async () => {
  const [note, finiteAudit, spectralAudit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(finiteAuditUrl, "utf8"),
    readFile(spectralAuditUrl, "utf8"),
  ]);

  assert.match(note, /R0\.66 — A nonzero dominant spectral projection/);
  assert.ok(note.includes("S_r=C_*\\lambda^r+O(r16^r)"));
  assert.ok(note.includes("\\frac{|S_r|}{M_r}\\longrightarrow\\infty"));
  assert.ok(note.includes("-2.3044567988960\\times10^{-5}"));
  assert.ok(note.includes("Aw=256w"));
  assert.ok(note.includes("\\|\\mathcal P\\zeta\\|_{KR,w}\\le16"));
  assert.match(note, /does not\s+show that the full mild solution becomes singular/);
  assert.match(finiteAudit, /exact integer moment iterate/);
  assert.match(spectralAudit, /weighted Kantorovich contraction/);
  assert.doesNotMatch(note, /我们|攻关|主攻|突破千禧年/);
});

test("reproduces a quick staged affine-block regression", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r066-spectral-"));
  const finiteOutput = join(scratch, "finite.json");
  const spectralOutput = join(scratch, "spectral.json");
  const python = process.env.CODEX_PYTHON || "python3";
  await execFileAsync(
    python,
    [
      finiteAuditUrl.pathname,
      "--cycles",
      "4",
      "--order",
      "8",
      "--output",
      finiteOutput,
    ],
    { cwd: repository, maxBuffer: 20 * 1024 * 1024 },
  );
  await execFileAsync(
    python,
    [
      spectralAuditUrl.pathname,
      "--profile",
      "quick",
      "--cycles",
      "4",
      "--order",
      "8",
      "--finite-input",
      finiteOutput,
      "--output",
      spectralOutput,
    ],
    { cwd: repository, maxBuffer: 20 * 1024 * 1024 },
  );
  const [finite, spectral] = await Promise.all([
    readFile(finiteOutput, "utf8").then(JSON.parse),
    readFile(spectralOutput, "utf8").then(JSON.parse),
  ]);
  assert.equal(finite.status, "passed");
  assert.equal(Object.values(finite.checks).every(Boolean), true);
  assert.equal(finite.degree, 16);
  assert.equal(spectral.checks.cycleMatrixMatchesAffineBranchMasses, true);
  assert.equal(spectral.checks.exactImageCharacteristicPolynomialMatches, true);
  assert.equal(spectral.checks.absoluteBranchMatrixHasExactPositiveWeight256, true);
  assert.equal(spectral.checks.zeroMassKantorovichGrowthPerBlockIsAtMost16, true);
  assert.equal(spectral.checks.quickProfileDoesNotClaimPublicationProjectionSign, true);
  assert.equal(spectral.stationaryBlockOperator.affineBranchRecords, 12288);
});

test("archives the R0.66 asymptotic certificate with valid hashes", async () => {
  const [finiteText, spectralText, sumsText] = await Promise.all([
    readFile(new URL("exact-finite-iterate.json", certificateRoot), "utf8"),
    readFile(new URL("spectral-audit.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const finite = JSON.parse(finiteText);
  const spectral = JSON.parse(spectralText);
  assert.equal(finite.status, "passed");
  assert.equal(finite.cycles, 100);
  assert.equal(finite.order, 24);
  assert.equal(finite.degree, 48);
  assert.equal(Object.values(finite.checks).every(Boolean), true);
  assert.equal(spectral.status, "passed");
  assert.equal(spectral.profile, "publication");
  assert.equal(Object.values(spectral.checks).every(Boolean), true);
  assert.equal(spectral.certifiedTheorem.coefficientSign, "negative");
  assert.match(spectral.certifiedTheorem.asymptoticFormula, /O\(r 16\^r\)/);
  assert.match(spectral.certifiedTheorem.consequence, /tends to infinity/);
  assert.ok(Number(spectral.certifiedTheorem.coefficientUpperDisplay) < -2e-5);
  assert.ok(Number(spectral.errorBudget.total) < 9e-8);

  const entries = sumsText.trim().split("\n").map((line) => {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "Malformed SHA256SUMS line: " + line);
    return { expected: match[1], file: match[2] };
  });
  assert.ok(entries.length >= 4);
  for (const entry of entries) {
    const payload = await readFile(new URL(entry.file, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, entry.expected, entry.file + " hash mismatch");
  }
});
