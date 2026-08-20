import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const noteUrl = new URL(
  "../research/critical_resolvent_endpoint_scaling_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/critical_resolvent_endpoint_scaling_audit.py",
  import.meta.url,
);
const certificateRoot = new URL(
  "../research/certificates/r069f/",
  import.meta.url,
);

test("states the R0.69F fractional-Volterra endpoint no-go theorem", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.ok(note.includes("G(x)=E_{1/2}(x)"));
  assert.ok(note.includes("e^{x^2}\\operatorname{erfc}(-x)"));
  assert.ok(note.includes("\\beta=256"));
  assert.ok(note.includes(
    "\\mathfrak M_v^{\\,c}(t_r)",
  ));
  assert.ok(note.includes(
    "\\theta_A^3=2A(1-\\theta_A)",
  ));
  assert.ok(note.includes(
    "\\limsup_{j\\to\\infty}V_j\\sqrt{h_j}",
  ));
  assert.match(note, /does not improve the classical continuation\s+rate/i);
  assert.match(note, /reference-resolvent branch is therefore stopped/i);
  assert.match(note, /does not solve the three-dimensional Navier--Stokes Millennium problem/i);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("reproduces the R0.69F exact and high-precision audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [
      auditUrl.pathname,
      "--source-commit",
      "0000000000000000000000000000000000000000",
      "--check",
    ],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr);
  const payload = JSON.parse(run.stdout);
  assert.equal(payload.status, "passed");
  assert.equal(Object.keys(payload.checks).length, 22);
  assert.ok(Object.values(payload.checks).every(Boolean));
  assert.equal(payload.mittagLeffler.scenarios.length, 8);
  assert.equal(payload.bieleckiOptimization.scenarios.length, 6);
  assert.equal(
    payload.theorem.packetConstants.remainingTimeOverSlabLength,
    "256/255",
  );
  assert.match(payload.decision.closedBranch, /cannot improve/i);
  assert.match(payload.decision.comparison, /classical/i);
});

test("archives the source-locked R0.69F certificate", async () => {
  const [certificateText, readme, sumsText] = await Promise.all([
    readFile(
      new URL("critical-resolvent-endpoint-scaling.json", certificateRoot),
      "utf8",
    ),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.keys(certificate.checks).length, 22);
  assert.ok(Object.values(certificate.checks).every(Boolean));
  assert.equal(
    certificate.provenance.sourceCommit,
    "c3f3d94620f6852e48e07525cc81f2c94ee1511d",
  );
  assert.match(readme, /22 checks, all passed/);
  assert.match(readme, /classical local continuation/i);
  assert.match(readme, /not[\s\S]*solve the Navier--Stokes Millennium/i);

  const records = sumsText.trim().split("\n");
  assert.equal(records.length, 3);
  for (const record of records) {
    const match = record.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, "malformed SHA256SUMS line: " + record);
    const payload = await readFile(new URL(match[2], certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, match[1], match[2] + " hash mismatch");
  }
});
