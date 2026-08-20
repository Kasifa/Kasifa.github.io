import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const repository = new URL("..", import.meta.url).pathname;
const noteUrl = new URL("../research/sixth_order_cycle_note.md", import.meta.url);
const auditUrl = new URL("../research/sixth_order_cycle_audit.py", import.meta.url);

test("states the R0.67A zero-time sixth-order theorem and heat boundary", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);

  assert.match(note, /R0\.67A — The exact zero-time sixth-order cycle/);
  assert.ok(note.includes("A+B+C-D-E=Q"));
  assert.ok(note.includes("2\\times32\\times5=320"));
  assert.ok(note.includes("\\mu=16\\lambda"));
  assert.ok(note.includes("Y_r=C_{6,0}\\mu^r+O(300^r)"));
  assert.ok(note.includes("\\frac{|Y_r|}{M_r^2}\\longrightarrow\\infty"));
  assert.ok(note.includes("A_{\\rm abs}w=65536w"));
  assert.ok(note.includes("256\\|\\zeta\\|_{(C^{1,1})^*,w}"));
  assert.match(note, /do \*\*not\*\* yet prove.*complete five-simplex heat observable/s);
  assert.match(note, /No result here proves norm inflation, singularity, or global regularity/);
  assert.match(audit, /not a certificate for the complete five-simplex heat observable/);
});

test("reproduces the exact R0.67A five-carrier transfer certificate", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r067-sixth-"));
  const output = join(scratch, "sixth-order-cycle.json");
  const python = process.env.CODEX_PYTHON || "python3";
  await execFileAsync(
    python,
    [
      auditUrl.pathname,
      "--max-direct-level",
      "4",
      "--sequence-terms",
      "32",
      "--output",
      output,
    ],
    { cwd: repository, maxBuffer: 30 * 1024 * 1024 },
  );
  const certificate = JSON.parse(await readFile(output, "utf8"));
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(certificate.stateSpace.dimension, 320);
  assert.deepEqual(certificate.stateSpace.carries, [-2, -1, 0, 1, 2]);
  assert.equal(certificate.cycle.imageDimension, 36);
  assert.match(certificate.cycle.imageCharacteristicFactorization, /x\^5 \(x-256\)\^5/);
  assert.match(certificate.cycle.imageCharacteristicFactorization, /x\^4-400x\^3/);
  assert.equal(
    certificate.reachableTargetFamily.dominantProjection.coefficientIsNegative,
    true,
  );
  assert.ok(
    Number(
      certificate.reachableTargetFamily.dominantProjection
        .coefficientUpperDisplay,
    ) < -0.013,
  );
  assert.equal(certificate.absoluteTransfer.eigenvalue, 65536);
  assert.equal(certificate.absoluteTransfer.C2ZeroAffineThreshold, 256);
  assert.equal(certificate.directAudit.exactLevelsChecked, 4);
});
