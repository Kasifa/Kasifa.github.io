import assert from "node:assert/strict";
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
