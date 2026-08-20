import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const repository = new URL("..", import.meta.url).pathname;
const noteUrl = new URL(
  "../research/sixth_order_affine_moment_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/sixth_order_affine_moment_audit.py",
  import.meta.url,
);

test("states the exact R0.67B affine lift and strict resolvent boundary", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);

  assert.match(note, /R0\.67B — The exact mass-plus-affine lift/);
  assert.ok(note.includes("A+B+C-D-E=Q"));
  assert.ok(note.includes("2\\cdot32\\cdot5=320"));
  assert.ok(note.includes("\\ell'_j=\\frac1{16}\\bigl(W\\ell_j+E_jm\\bigr)"));
  assert.ok(note.includes("\\mathcal M R=0"));
  assert.ok(note.includes("26<256<300<\\mu"));
  assert.ok(note.includes("\\le\\frac1{\\mu-256}"));
  assert.ok(note.includes("factor \\(q_4^4\\) in (4.2) is retained"));
  assert.match(note, /complete heat-projection sign.*remain open/s);
  assert.match(note, /No conclusion about all Picard orders, norm\s+inflation, singularity, or global regularity/);
  assert.match(audit, /does not certify the sign of the\s+complete heat-weighted five-simplex projection/);
});

test("reproduces the exact R0.67B mass-plus-four-first-moment lift", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r067b-affine-"));
  const output = join(scratch, "affine-moment.json");
  const python = process.env.CODEX_PYTHON || "python3";
  await execFileAsync(
    python,
    [
      auditUrl.pathname,
      "--max-direct-level",
      "4",
      "--output",
      output,
    ],
    { cwd: repository, maxBuffer: 30 * 1024 * 1024 },
  );
  const certificate = JSON.parse(await readFile(output, "utf8"));
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(certificate.stateSpace.states, 320);
  assert.equal(certificate.stateSpace.finiteLiftDimension, 1600);
  assert.deepEqual(certificate.stateSpace.freeSpatialCoordinates, ["A", "B", "C", "D"]);
  assert.equal(certificate.exactLift.massMatrixNonzeros, 20808);
  assert.equal(certificate.exactLift.shiftMatrices.A.nonzeros, 20542);
  assert.equal(certificate.exactLift.shiftMatrices.D.nonzeros, 20898);
  assert.equal(certificate.spectralSeparation.zeroAffineC11RemainderScale, 256);
  assert.equal(certificate.spectralSeparation.strictOrdering, "26 < 256 < 300 < mu");
  assert.equal(certificate.directConvolutionAudit.length, 4);
});
