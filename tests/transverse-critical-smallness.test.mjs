import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const noteUrl = new URL(
  "../research/transverse_critical_smallness_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/transverse_critical_smallness_audit.py",
  import.meta.url,
);
const certificateRoot = new URL(
  "../research/certificates/r069b/",
  import.meta.url,
);

test("states the exact R0.69B transverse critical-smallness gate", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.match(note, /\\|U_r\\(0\\)\\|_\{BMO\^\{-1\}_\{\\rm per\}\}/);
  assert.match(note, /6\+4\\sqrt\{2\}/);
  assert.match(note, /50303178668203/);
  assert.match(note, /0\.7975855452903290<\\rho<0\.7975855452903292/);
  assert.ok(note.includes("\\((w\\cdot\\nabla)U_r\\)"));
  assert.match(note, /critical small-data threshold/);
  assert.match(note, /order-one/);
  assert.match(
    note,
    /not a resolution of the general three-dimensional\s+problem/i,
  );
});

test("reproduces the source-bound R0.69B interval audit", () => {
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
  assert.ok(Object.values(payload.checks).every(Boolean));
  assert.equal(payload.criticalNormBound.firstDepthStrictlyBelow["1"], 11);
  assert.equal(payload.criticalNormBound.firstDepthStrictlyBelow["1e-1"], 22);
  assert.equal(payload.criticalNormBound.firstDepthStrictlyBelow["1e-2"], 32);
  assert.equal(payload.criticalNormBound.firstDepthStrictlyBelow["1e-3"], 42);
  assert.match(payload.criticalNormBound.rho.upper, /^0\.797585545290329/);
  assert.match(payload.perturbationEquation.criticalBallCondition, /eta_KT_per/);
  assert.match(payload.boundary.at(-1), /not a solution/i);
});

test("archives the source-locked R0.69B certificate", async () => {
  const [certificateText, readme, sumsText] = await Promise.all([
    readFile(new URL("transverse-critical-smallness.json", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(
    certificate.provenance.sourceCommit,
    "3342fb092b454df34255b82e142bfd796e5e522d",
  );
  assert.equal(
    certificate.criticalNormBound.firstDepthStrictlyBelow["1e-6"],
    72,
  );
  assert.notEqual(
    certificate.criticalNormBound.rho.lower,
    certificate.criticalNormBound.rho.upper,
  );
  assert.match(readme, /assigns no\s+numerical value/i);
  assert.match(readme, /not a solution of the\s+Navier--Stokes Millennium problem/i);

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
