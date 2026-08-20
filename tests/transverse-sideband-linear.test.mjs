import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const noteUrl = new URL(
  "../research/transverse_sideband_linear_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/transverse_sideband_linear_audit.py",
  import.meta.url,
);
const certificateRoot = new URL(
  "../research/certificates/r069c/",
  import.meta.url,
);

test("states the exact R0.69C transverse sideband theorem", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.match(note, /k_3=s/);
  assert.ok(note.includes("[\\mathscr T_{R,m,s}]"));
  assert.ok(note.includes("-\\dfrac{Rs}{Q}"));
  assert.ok(note.includes("\\|\\mathscr T_{R,m,s}\\|_{\\ell^2\\to\\ell^2}\\le d"));
  assert.ok(note.includes("|p|^2+|q|^2-|k|^2=R^2+(R^2+d^2)-d^2=2R^2"));
  assert.ok(note.includes("\\frac{|A|}{2R}"));
  assert.ok(note.includes("\\kappa_r:=4C_BC_HC_0\\rho^r<1"));
  assert.match(note, /converges in critical operator norm to the\s+free heat map/);
  assert.match(note, /does not resolve the Navier--Stokes Millennium problem/i);
});

test("reproduces the exact R0.69C symbolic audit", () => {
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
    payload.sideband.formulas.matrix,
    "[[m*d/Q,0],[-R*s/Q,m]]",
  );
  assert.match(payload.sideband.formulas.heatDenominator, /2R\^2/);
  assert.match(
    payload.criticalPropagator.differenceFromHeat,
    /kappa_r\/\(1-kappa_r\)/,
  );
  assert.match(payload.boundary.at(-1), /not a solution/i);
});

test("archives the source-locked R0.69C certificate", async () => {
  const [certificateText, readme, sumsText] = await Promise.all([
    readFile(new URL("transverse-sideband-linear.json", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.match(certificate.provenance.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(
    certificate.sideband.formulas.matrixGapDeterminant,
    "d^2*s^4/Q^2",
  );
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
