import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const noteUrl = new URL(
  "../research/critical_resolvent_restart_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/critical_resolvent_restart_audit.py",
  import.meta.url,
);
const certificateRoot = new URL(
  "../research/certificates/r069e/",
  import.meta.url,
);

test("states the exact R0.69E critical-resolvent gluing theorem", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.ok(note.includes("a:=2C_B\\|v\\|_{X_\\tau}"));
  assert.ok(note.includes("b_\\lambda:=2C_SV_\\tau\\sqrt{\\frac\\pi\\lambda}"));
  assert.ok(note.includes("\\Gamma(\\tau,T,\\lambda)"));
  assert.ok(note.includes("\\frac1{(1-a)(1-b_\\lambda)}"));
  assert.ok(note.includes("A_{10}z_0(t)=e^{(t-\\tau)\\Delta}(A_{00}z_0)(\\tau)"));
  assert.ok(note.includes("\\ell_k=\\eta(\\sqrt k-\\sqrt{k-1})"));
  assert.match(note, /Every smooth periodic\s+reference solution therefore has a finite critical linearized resolvent/i);
  assert.match(note, /strong quantitative restart norm/i);
  assert.match(note, /does not establish global regularity/i);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("reproduces the R0.69E symbolic and finite-slab audit", () => {
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
  assert.equal(Object.keys(payload.checks).length, 18);
  assert.ok(Object.values(payload.checks).every(Boolean));
  assert.equal(
    payload.theorem.formulas.inverseRowSum,
    "1/((1-a)(1-b_lambda))",
  );
  assert.equal(payload.finitePartition.scenarios.length, 16);
  assert.ok(
    payload.finitePartition.scenarios.every(
      (record) => record.directEqualsForwardSubstitution,
    ),
  );
  assert.match(payload.decision.remainingGate, /singular endpoint/i);
});

test("archives the source-locked R0.69E certificate", async () => {
  const [certificateText, readme, sumsText] = await Promise.all([
    readFile(new URL("critical-resolvent-restart.json", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.keys(certificate.checks).length, 18);
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(
    certificate.provenance.sourceCommit,
    "2d49cf91a29c2a2ecd19edbe97356a924b958917",
  );
  assert.match(readme, /18 checks, all passed/);
  assert.match(readme, /not[\s\S]*solve the Navier--Stokes Millennium problem/i);

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
