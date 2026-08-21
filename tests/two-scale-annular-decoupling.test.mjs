import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import { fileURLToPath } from "node:url";
import test from "node:test";

const root = new URL("../", import.meta.url);
const noteUrl = new URL(
  "research/two_scale_annular_decoupling_note.md",
  root,
);
const auditUrl = new URL(
  "research/two_scale_annular_decoupling_audit.py",
  root,
);
const polynomialUrl = new URL(
  "research/two_scale_annular_polynomial_qmc.py",
  root,
);

test("states the R0.69V exact cubic law and uniform annular decoupling", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.ok(note.includes("u_{\\varepsilon,a}=aU_1+bU_\\varepsilon"));
  assert.ok(note.includes("\\varepsilon^3ab^2C_q"));
  assert.ok(note.includes("No \\(a^2b\\) term occurs"));
  assert.ok(note.includes("\\Gamma_{\\rm ann}(u_{\\varepsilon,a})-\\Gamma_q"));
  assert.ok(note.includes("\\varepsilon\\bigl(1+\\log(1/\\varepsilon)\\bigr)"));
  assert.ok(note.includes("finite-\\(N\\) saturating parameter"));
  assert.match(note, /do\s+not solve the Millennium Problem/);
});

test("reproduces the R0.69V symbolic and deterministic audit", () => {
  const output = new URL("tmp/r069v-test-audit.json", root);
  const run = spawnSync(
    fileURLToPath(new URL("tmp/r068b-venv/bin/python", root)),
    [
      fileURLToPath(auditUrl),
      "--output",
      fileURLToPath(output),
    ],
    {
      cwd: fileURLToPath(new URL(".", root)),
      encoding: "utf8",
      timeout: 30_000,
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(result.checkCount, 21);
  assert.equal(result.passedCount, 21);
  assert.equal(result.coefficients.C21Exact, 0);
  assert.ok(result.coefficients.VReference > 1.9);
  assert.ok(result.coefficients.C12Reference < -2.7);
});

test("keeps both complete and annulus-importance QMC implementations", async () => {
  const [complete, importance] = await Promise.all([
    readFile(new URL("research/two_scale_full_annular_qmc.py", root), "utf8"),
    readFile(
      new URL("research/two_scale_annular_importance_qmc.py", root),
      "utf8",
    ),
  ]);
  assert.match(complete, /all unordered zone pairs/);
  assert.match(complete, /transition--transition/);
  assert.match(importance, /sample\s+the displacement z=y-x directly/);
  assert.match(importance, /transitionTransitionPairsRetained/);
  assert.match(importance, /y_zone_indices >= x_zone_index/);
});

test("reconstructs every R0.69V annulus as a common-sample cubic", () => {
  const output = new URL("tmp/r069v-polynomial-test/", root);
  const run = spawnSync(
    fileURLToPath(new URL("tmp/r068b-venv/bin/python", root)),
    [
      fileURLToPath(polynomialUrl),
      "--output-root",
      fileURLToPath(output),
      "--replicates",
      "2",
      "--power",
      "8",
      "--separation",
      "2",
      "--j-padding",
      "4",
      "--amplitude-grid",
      "101",
    ],
    {
      cwd: fileURLToPath(new URL(".", root)),
      encoding: "utf8",
      timeout: 30_000,
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(
    readFileSync(new URL("result.json", output), "utf8"),
  );
  assert.equal(result.status, "passed");
  assert.equal(result.method.amplitudeNodes.length, 4);
  assert.ok(result.audits.vandermondeResidualMax < 1e-13);
  assert.ok(result.audits.sampleNodeReconstructionResidualMax < 1e-11);
  assert.ok(result.audits.deterministicNodeResidualMax < 1e-6);
  assert.equal(result.audits.transitionTransitionPairsRetained, true);
  assert.equal(
    Number.isFinite(result.candidate.exactTotalOverAnnularL1OfMeans),
    true,
  );
  assert.equal(Number.isFinite(result.candidate.exactSignedTotal), true);
  assert.equal(result.candidate.annuli.length, 8);
});
