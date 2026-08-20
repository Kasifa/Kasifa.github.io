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
  "../research/quartic_time_layer_transfer_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/quartic_time_layer_transfer_audit.py",
  import.meta.url,
);
const certificateRoot = new URL("../research/certificates/r063/", import.meta.url);
const probeNames = [
  "m4096-t292.json",
  "m8192-t7643.json",
  "m16384-t2388.json",
  "m32768-t30583.json",
  "m65536-t5291.json",
  "m131072-t122331.json",
];

test("states the exact R0.63 time-layer factorization and lifted transfer boundary", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);

  assert.match(note, /R0\.63 — Time-layer factorization and the lifted Rudin--Shapiro transfer/);
  assert.ok(note.includes("S_{4,m}=\\int_{\\Delta_T}"));
  assert.ok(note.includes("C_{n+1}^{\\boldsymbol\\sigma}"));
  assert.ok(note.includes("(-1)^{\\boldsymbol\\sigma\\cdot\\boldsymbol\\varepsilon}"));
  assert.match(note, /cubic carrier product closes\s+on eight states/);
  assert.match(note, /target sign gives a natural sixteen-state\s+lift/);
  assert.match(note, /do \*\*not\*\* prove \(1\.1\)/);
  assert.match(note, /does not solve the Navier--Stokes Millennium problem/);
  assert.match(audit, /exact algebraic transfer regression plus finite long-double stress tests/);
  assert.doesNotMatch(note, /我们|攻关|主攻|突破千禧年/);
});

test("reproduces the exact time-layer and eight-state transfer regressions", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r063-transfer-"));
  const output = join(scratch, "audit.json");
  const auditArguments = [
    auditUrl.pathname,
    "--output",
    output,
    "--max-lift-level",
    "8",
  ];
  for (const name of probeNames) {
    auditArguments.push("--probe", new URL(name, certificateRoot).pathname);
  }
  await execFileAsync(process.env.CODEX_PYTHON || "python3", auditArguments, {
    cwd: repository,
  });
  const report = JSON.parse(await readFile(output, "utf8"));
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.ok(report.timeLayerAudit.maximumRelativeResidual < 5e-14);
  assert.equal(report.timeLayerAudit.comparisons, 27);
  assert.equal(report.cubicLift.baseStates, 2);
  assert.equal(report.cubicLift.cubicStates, 8);
  assert.equal(report.cubicLift.targetSignedStates, 16);
  assert.deepEqual(report.cubicLift.carryShifts, [-1, 0, 1, 2]);
  assert.equal(report.hostileWeightedProbes.length, 6);
  assert.equal(report.hostileWeightedProbes.at(-1).M, 131072);
  assert.equal(report.hostileWeightedProbes.at(-1).orderedQuarticPaths, 28977859974);
});

test("archives the R0.63 transfer certificate with valid hashes", async () => {
  const [reportText, sumsText] = await Promise.all([
    readFile(new URL("time-layer-transfer-audit.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const report = JSON.parse(reportText);
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.cubicLift.exactLevelsChecked, 10);
  assert.equal(report.hostileWeightedProbes.length, 6);
  assert.ok(
    Math.max(...report.hostileWeightedProbes.map((record) => record.S4OverM)) < 0.02,
  );

  const entries = sumsText.trim().split("\n").map((line) => {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "Malformed SHA256SUMS line: " + line);
    return { expected: match[1], file: match[2] };
  });
  assert.equal(entries.length, 8);
  for (const entry of entries) {
    const payload = await readFile(new URL(entry.file, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, entry.expected, entry.file + " hash mismatch");
  }
});
