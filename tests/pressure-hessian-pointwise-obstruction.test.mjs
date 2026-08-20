import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const noteUrl = new URL(
  "../research/pressure_hessian_pointwise_obstruction_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/pressure_hessian_pointwise_obstruction_audit.py",
  import.meta.url,
);

test("states the exact R0.69H pointwise pressure-sign obstruction", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.ok(note.includes("-\\Delta p=q"));
  assert.ok(note.includes("\\widehat H_{ij}(k)"));
  assert.ok(note.includes("H_{11}^{-}(0)=-1-\\frac{54}{85}t^2"));
  assert.ok(note.includes("H_{11}^{+}(0)=-1+\\frac{54}{85}t^2"));
  assert.ok(note.includes("S(0)=\\operatorname{diag}(1,-1,0)"));
  assert.match(
    note,
    /data do not determine even the sign of the}[\s\S]*pressure-Hessian component/i,
  );
  assert.match(note, /does not prove regularity or singularity/i);
  assert.match(note, /localize the exact strain-space\s+orthogonality/i);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("reproduces the exact R0.69H symbolic and Fourier audit", () => {
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
  assert.equal(Object.keys(payload.checks).length, 15);
  assert.ok(Object.values(payload.checks).every(Boolean));
  assert.equal(payload.witnessAudit.exactThresholdTSquared, "85/54");
  assert.equal(payload.witnessAudit.pressureAtTEqualsTwo.minus, "-301/85");
  assert.equal(payload.witnessAudit.pressureAtTEqualsTwo.plus, "131/85");
  assert.match(payload.decision.closedBranch, /pointwise pressure/i);
  assert.match(payload.decision.nextBranch, /strain-space orthogonality/i);
});
