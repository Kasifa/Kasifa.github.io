import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the sharp R0.69P stretching geometry and claim boundary", async () => {
  const note = await readFile(
    new URL("../research/vorticity_stretching_sign_structure_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("\\sqrt{\\frac23}\\,|S|\\,|\\omega|^2"));
  assert.ok(note.includes("v_A=\\nabla\\times(\\chi B_A)"));
  assert.ok(note.includes("\\int\\omega\\cdot S\\omega\\,dx\n =-4\\int\\det S\\,dx"));
  assert.ok(note.includes("-4\\det S\\leq 2\\lambda_2^+|S|^2"));
  assert.ok(note.includes("\\lambda_2^+\\leq\\frac{|S|}{\\sqrt6}"));
  assert.ok(note.includes("\\frac{27}{256}\\varepsilon^{-3}\\sigma^6"));
  assert.match(note, /does not solve the Millennium Problem/i);
  assert.match(note, /R0\.69Q will therefore test/i);
});

test("reproduces the R0.69P symbolic and local-realization audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/vorticity_stretching_sign_structure_audit.py", import.meta.url).pathname],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 18);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.equal(result.sharpPointwiseStretching.constant, "sqrt(2/3)");
  assert.equal(result.betchov.sharpSupremum, "2");
  assert.equal(result.energyOnlyEndpoint.power, "sigma^6");
  assert.equal(
    result.energyOnlyEndpoint.youngRemainder,
    "27*sigma**6/(256*epsilon**3)",
  );
});
