import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the R0.69K velocity-generated shell gain and boundary", async () => {
  const note = await readFile(
    new URL("../research/velocity_generated_shell_quadrupole_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("q:=\\operatorname{tr}((\\nabla u)^2)"));
  assert.ok(note.includes("\\partial_i\\partial_j(u_i u_j)"));
  assert.ok(note.includes("\\frac{C}{R_m^5}"));
  assert.ok(note.includes("\\int y_a y_bq_m(y)\\,dy"));
  assert.ok(note.includes("\\operatorname{diag}(0,6,-6)"));
  assert.ok(note.includes("-\\frac{3}{2\\pi R^5}\\ne0"));
  assert.match(note, /two powers of shell distance better/i);
  assert.match(note, /positive-semidefinite energy tensor/i);
  assert.match(note, /not the same as the naive scalar localization/i);
  assert.match(note, /does\s+not solve the Millennium Problem/i);
  assert.match(note, /R0\.69L will retain a\s+near pressure region/i);
});

test("reproduces the exact R0.69K fourth-derivative audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [
      new URL(
        "../research/velocity_generated_shell_quadrupole_audit.py",
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
  assert.deepEqual(result.identity.secondMoment, [
    ["2", "0", "0"],
    ["0", "4", "0"],
    ["0", "0", "0"],
  ]);
  assert.deepEqual(result.witness.fourPiQuadrupole, [
    ["0", "0", "0"],
    ["0", "6/R**5", "0"],
    ["0", "0", "-6/R**5"],
  ]);
  assert.equal(result.witness.actualStrainPairing, "-3/(2*pi*R**5)");
  assert.equal(result.witness.streamfunctionEnergyRatio, "2");
});
