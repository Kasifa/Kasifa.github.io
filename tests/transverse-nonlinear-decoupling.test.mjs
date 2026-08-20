import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const noteUrl = new URL(
  "../research/transverse_nonlinear_decoupling_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/transverse_nonlinear_decoupling_audit.py",
  import.meta.url,
);
const certificateRoot = new URL(
  "../research/certificates/r069d/",
  import.meta.url,
);

test("states the exact R0.69D conditional nonlinear theorem", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.ok(note.includes("\\mathcal A_vz:=\\mathcal B(v,z)+\\mathcal B(z,v)"));
  assert.ok(note.includes("\\chi_r:=4C_BM_T^2C_H\\delta_r"));
  assert.ok(note.includes("1-\\sqrt{1-\\chi_r}"));
  assert.ok(note.includes("\\mathcal B(z_r,z_r)"));
  assert.ok(note.includes("\\le2M_TC_HC_0\\rho^r"));
  assert.match(note, /unique fixed point in the\s+closed/);
  assert.match(note, /bounded critical\s+path norm and bounded critical linearized resolvent are distinct/i);
  assert.match(note, /does not prove global regularity/i);
});

test("reproduces the exact R0.69D symbolic audit", () => {
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
  assert.equal(
    payload.majorant.formulas.contractionFactor,
    "q_r=1-sqrt(1-chi_r)",
  );
  assert.match(payload.majorant.formulas.geometricEnvelope, /rho\^r/);
  assert.match(payload.referenceGate.hypothesis, /boundedly invertible/);
  assert.match(payload.boundary.at(-1), /not a solution/i);
});

test("archives the source-locked R0.69D certificate", async () => {
  const [certificateText, readme, sumsText] = await Promise.all([
    readFile(new URL("transverse-nonlinear-decoupling.json", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.match(certificate.provenance.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(Object.keys(certificate.checks).length, 18);
  assert.match(readme, /18, all passed/);
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
