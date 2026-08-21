import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the exact R0.69S one-shell no-cancellation theorem", async () => {
  const note = await readFile(
    new URL("../research/signed_output_shell_no_cancellation_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("\\mathcal F_0(u)=2"));
  assert.ok(note.includes("\\Gamma(u)=1"));
  assert.ok(note.includes("(T_k,T_p,T_q)=(2,-3,1)"));
  assert.ok(note.includes("\\int_{\\mathbb T^3}\\omega\\cdot S\\omega\\,dx=2>0"));
  assert.match(note, /does not solve\s+the Millennium Problem/i);
  assert.match(note, /R0\.69T will test the fourth option/i);
});

test("reproduces the R0.69S exact Fourier and shell audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/signed_output_shell_no_cancellation_audit.py", import.meta.url).pathname],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 15);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.deepEqual(result.witness.modalTransfers, ["2", "-3", "1"]);
  assert.equal(result.witness.fullVortexStretching, "2");
  assert.equal(result.shellDecomposition.cancellationRatio, "1");
});
