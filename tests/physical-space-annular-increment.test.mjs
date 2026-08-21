import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the exact R0.69T annular increment and affine-core identities", async () => {
  const note = await readFile(
    new URL("../research/physical_space_annular_increment_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("\\sum_{j\\in\\mathbb Z}\\mathcal A_j(u)=\\mathcal V(u)"));
  assert.ok(note.includes("(e_{xy}\\cdot\\delta\\omega)"));
  assert.ok(note.includes("\\mathcal A_j(u_{2^\\ell})"));
  assert.ok(note.includes("|B_1|\\,\\omega_A\\cdot S_A\\omega_A"));
  assert.match(note, /entire core production arrives through pairs crossing the/i);
  assert.match(note, /does not solve the Millennium Problem/i);
});

test("reproduces the R0.69T symbolic pair-exchange and scaling audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/physical_space_annular_increment_audit.py", import.meta.url).pathname],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 10);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.equal(result.scaling.navierStokesExponent, 3);
  assert.equal(result.affineCore.interiorPairContribution, "zero");
  assert.match(result.exactIdentities.pairSymmetrizedNumerator, /delta_omega/);
});
