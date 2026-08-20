import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const noteUrl = new URL(
  "../research/localized_strain_pressure_commutator_note.md",
  import.meta.url,
);

test("states the exact R0.69I localized strain identities and boundary", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.ok(note.includes("\\int_{\\mathbb T^3}\\phi S:H\\,dx"));
  assert.ok(note.includes("(\\Delta p)u\\cdot\\nabla\\phi"));
  assert.ok(note.includes("\\left(\\frac12qu-A^2u\\right)\\cdot\\nabla\\phi"));
  assert.ok(note.includes("+2\\int\\phi\\det S"));
  assert.ok(note.includes("=-\\frac{676}{40425}"));
  assert.ok(note.includes("=\\frac{228}{2695}\\ne0"));
  assert.match(note, /both localized commutators are genuinely nonzero/i);
  assert.match(note, /closes only the bare-localization route/i);
  assert.match(note, /does not solve the Millennium Problem/i);
  assert.match(note, /R0\.69J will split the pressure on a ball/);
});

test("reproduces the exact R0.69I Fourier and scaling audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [
      new URL(
        "../research/localized_strain_pressure_commutator_audit.py",
        import.meta.url,
      ).pathname,
    ],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 12);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.equal(result.exactValues.localizedPressurePairing, "-676/40425");
  assert.equal(result.exactValues.localizedBetchovPairing, "228/2695");
  assert.equal(result.exactValues.globalPressurePairing, "0");
  assert.equal(result.exactValues.globalBetchovPairing, "0");
  assert.deepEqual(new Set(Object.values(result.scalingDegrees)), new Set([3]));
  assert.deepEqual(result.weight.pressureMode, [0, 0, 1]);
  assert.deepEqual(result.weight.betchovMode, [1, 0, 0]);
});
