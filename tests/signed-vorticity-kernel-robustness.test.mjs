import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const noteUrl = new URL(
  "../research/signed_vorticity_kernel_robustness_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/signed_vorticity_kernel_robustness_audit.py",
  import.meta.url,
);

test("states the exact R0.69G kernel and robustness boundary", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.ok(note.includes("\\alpha(x)"));
  assert.ok(note.includes("\\partial_{\\ell j}G(z)"));
  assert.ok(note.includes("D(e_1,e_2,e_3)"));
  assert.ok(note.includes("\\|K_{x,t}\\|_{L^\\infty(A)}"));
  assert.match(note, /direction-only signed annular averaging is not robust/i);
  assert.match(note, /pressure-Hessian term/i);
  assert.match(note, /does not prove regularity/i);
  assert.match(note, /Preprint; not independently validated here/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("reproduces the R0.69G symbolic Fourier and angular audit", () => {
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
  assert.equal(Object.keys(payload.checks).length, 14);
  assert.ok(Object.values(payload.checks).every(Boolean));
  assert.equal(payload.periodicFourierAudit.modeCount, 10);
  assert.equal(payload.angularAudit.magnitudeBiasScenarios.length, 4);
  assert.match(payload.decision.closedBranch, /direction-only/i);
  assert.match(payload.decision.nextBranch, /pressure-Hessian/i);
});
