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
  "../research/quartic_weighted_cycle_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/quartic_weighted_cycle_audit.py",
  import.meta.url,
);
const certificateRoot = new URL("../research/certificates/r065/", import.meta.url);
const figureRoot = new URL(
  "../figures/r065-weighted-cycle/fig-r065-weighted-cycle/",
  import.meta.url,
);

test("states the exact R0.65 moment enclosure and finite inference boundary", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);

  assert.match(note, /R0\.65 — Exact moment enclosures/);
  assert.ok(note.includes("q_r=2\\frac{16^r-1}{15}"));
  assert.ok(note.includes("S_r<0,&14\\le r\\le24"));
  assert.ok(note.includes("\\frac{|S_r|}{|S_{r-1}|}>16"));
  assert.ok(note.includes("25.29<\\frac{|S_{24}|}{|S_{23}|}<25.30"));
  assert.ok(note.includes("T=\\frac{\\log2}{2}=\\operatorname{atanh}\\frac13"));
  assert.match(note, /do \*\*not\*\* by themselves prove/);
  assert.match(note, /does not solve the\s+Navier--Stokes Millennium problem/);
  assert.match(audit, /exact integer moment transport and exact rational Taylor enclosure/);
  assert.doesNotMatch(note, /我们|攻关|主攻|突破千禧年/);
});

test("reproduces a quick exact-moment and rational-tail regression", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r065-weighted-"));
  const output = join(scratch, "audit.json");
  await execFileAsync(
    process.env.CODEX_PYTHON || "python3",
    [
      auditUrl.pathname,
      "--profile",
      "quick",
      "--max-r",
      "5",
      "--order",
      "20",
      "--output",
      output,
    ],
    { cwd: repository, maxBuffer: 20 * 1024 * 1024 },
  );
  const report = JSON.parse(await readFile(output, "utf8"));
  assert.equal(report.status, "passed");
  assert.equal(report.profile, "quick");
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.exactMomentTransport.states, 48);
  assert.equal(report.exactMomentTransport.maximumTotalDegree, 40);
  assert.equal(report.scales.length, 5);
  assert.equal(report.scales[0].J0, 66);
  assert.equal(report.scales[4].signCertified, "positive");
});

test("archives the R0.65 publication certificate with valid hashes", async () => {
  const [reportText, sumsText] = await Promise.all([
    readFile(new URL("weighted-cycle-audit.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const report = JSON.parse(reportText);
  assert.equal(report.status, "passed");
  assert.equal(report.profile, "publication");
  assert.equal(Object.values(report.checks).every(Boolean), true);
  assert.equal(report.simplexSeries.order, 48);
  assert.equal(report.exactMomentTransport.maximumTotalDegree, 96);
  assert.equal(report.scales.length, 24);
  assert.equal(report.certifiedSummary.firstSignChangeR, 14);
  assert.deepEqual(report.certifiedSummary.consecutiveSupercriticalBlocks, [15, 24]);
  assert.equal(report.scales.at(-1).signCertified, "negative");
  assert.equal(report.independentLongDoubleProbes.length, 4);

  const entries = sumsText.trim().split("\n").map((line) => {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "Malformed SHA256SUMS line: " + line);
    return { expected: match[1], file: match[2] };
  });
  assert.equal(entries.length, 6);
  for (const entry of entries) {
    const payload = await readFile(new URL(entry.file, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, entry.expected, entry.file + " hash mismatch");
  }
});

test("archives the formal R0.65 weighted-cycle figure", async () => {
  const manifest = JSON.parse(
    await readFile(new URL("manifest.json", figureRoot), "utf8"),
  );
  assert.equal(manifest.figureId, "fig-r065-weighted-cycle");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 96);
  assert.equal(manifest.figure.outputs.length, 3);
  assert.match(manifest.supportedClaim, /sign changes at r=14/);
  assert.match(manifest.supportedClaim, /finite certificate does not prove asymptotic growth/i);

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
