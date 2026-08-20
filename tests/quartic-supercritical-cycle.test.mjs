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
  "../research/quartic_supercritical_cycle_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/quartic_supercritical_cycle_audit.py",
  import.meta.url,
);
const certificateRoot = new URL("../research/certificates/r064/", import.meta.url);
const figureRoot = new URL(
  "../figures/r064-supercritical-cycle/fig-r064-supercritical-cycle/",
  import.meta.url,
);

test("states the exact R0.64 supercritical cycle and its boundary", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);

  assert.match(note, /R0\.64 — An exact supercritical cycle/);
  assert.ok(note.includes("x^{42}(x-16)^2"));
  assert.ok(note.includes("\\lambda\\in(25,26)"));
  assert.ok(note.includes("q_r=2\\frac{16^r-1}{15}"));
  assert.match(note, /no common vector norm/);
  assert.match(note, /does not disprove the integrated estimate/);
  assert.match(note, /does not solve the Navier--Stokes\s+Millennium problem/);
  assert.match(audit, /pointwise common norm/);
  assert.doesNotMatch(note, /我们|攻关|主攻|突破千禧年/);
});

test("reproduces the exact forty-eight-state cycle certificate", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r064-cycle-"));
  const output = join(scratch, "audit.json");
  await execFileAsync(
    process.env.CODEX_PYTHON || "python3",
    [auditUrl.pathname, "--output", output, "--max-direct-level", "8"],
    { cwd: repository },
  );
  const report = JSON.parse(await readFile(output, "utf8"));
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.stateSpace.dimension, 48);
  assert.deepEqual(report.stateSpace.digitTransferRanks, [12, 12]);
  assert.equal(report.cycle.rank, 6);
  assert.equal(report.cycle.fourLevelThreshold, 16);
  assert.ok(report.cycle.dominantEigenvalueDisplayOnly > 25);
  assert.ok(report.cycle.dominantEigenvalueDisplayOnly < 26);
  assert.ok(report.reachableTargetFamily.growthExponentLog16LambdaDisplayOnly > 1);
  assert.equal(report.directAudit.exactLevelsChecked, 8);
});

test("archives the R0.64 exact certificate with valid hashes", async () => {
  const [reportText, sumsText] = await Promise.all([
    readFile(new URL("supercritical-cycle-audit.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const report = JSON.parse(reportText);
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.directAudit.exactLevelsChecked, 10);
  assert.equal(report.cycle.fullCharacteristicPolynomial.includes("x^42"), true);

  const entries = sumsText.trim().split("\n").map((line) => {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "Malformed SHA256SUMS line: " + line);
    return { expected: match[1], file: match[2] };
  });
  assert.equal(entries.length, 1);
  for (const entry of entries) {
    const payload = await readFile(new URL(entry.file, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, entry.expected, entry.file + " hash mismatch");
  }
});

test("archives the formal R0.64 supercritical-cycle figure", async () => {
  const manifest = JSON.parse(
    await readFile(new URL("manifest.json", figureRoot), "utf8"),
  );
  assert.equal(manifest.figureId, "fig-r064-supercritical-cycle");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 96);
  assert.equal(manifest.figure.outputs.length, 3);
  assert.match(manifest.supportedClaim, /reachable real eigenvalue 25\.151589/);
  assert.match(manifest.supportedClaim, /heat-integrated estimate remains open/i);
  assert.equal(manifest.computation.monitoring.failedAttempts.length, 2);

  for (const entry of [...manifest.data, ...manifest.figure.outputs]) {
    const payload = await readFile(new URL(entry.path, figureRoot));
    assert.equal(payload.length, entry.bytes, entry.path + " byte mismatch");
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, entry.sha256, entry.path + " hash mismatch");
  }
  for (const name of manifest.computation.monitoring.resourceLogs) {
    const text = await readFile(new URL(name, figureRoot), "utf8");
    assert.match(text, /exited:0/);
  }
});
