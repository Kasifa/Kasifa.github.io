import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { mkdtemp, readFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { join } from "node:path";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const repository = new URL("..", import.meta.url).pathname;
const noteUrl = new URL("../research/sixth_order_cycle_note.md", import.meta.url);
const auditUrl = new URL("../research/sixth_order_cycle_audit.py", import.meta.url);
const certificateUrl = new URL(
  "../research/certificates/r067/sixth-order-cycle-audit.json",
  import.meta.url,
);
const certificateStdoutUrl = new URL(
  "../research/certificates/r067/sixth-order-cycle-audit.stdout.log",
  import.meta.url,
);
const certificateStderrUrl = new URL(
  "../research/certificates/r067/sixth-order-cycle-audit.stderr.log",
  import.meta.url,
);
const checksumsUrl = new URL(
  "../research/certificates/r067/SHA256SUMS",
  import.meta.url,
);
const figureRoot = new URL(
  "../figures/r067-sixth-order-cycle/fig-r067-sixth-order-cycle/",
  import.meta.url,
);

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

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

test("locks the formal R0.67A certificate, logs, and resource record", async () => {
  const [jsonBuffer, stdoutBuffer, stderrBuffer, checksumText] =
    await Promise.all([
      readFile(certificateUrl),
      readFile(certificateStdoutUrl),
      readFile(certificateStderrUrl),
      readFile(checksumsUrl, "utf8"),
    ]);
  const certificate = JSON.parse(jsonBuffer.toString("utf8"));
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(certificate.directAudit.exactLevelsChecked, 7);
  assert.deepEqual(jsonBuffer, stdoutBuffer);
  assert.match(stderrBuffer.toString("utf8"), /isolating reachable scalar/);
  assert.match(stderrBuffer.toString("utf8"), /maximum resident set size/);
  assert.match(stderrBuffer.toString("utf8"), /\b0\s+swaps/);

  const expected = new Map(
    checksumText
      .trim()
      .split("\n")
      .map((line) => {
        const [digest, name] = line.trim().split(/\s+/);
        return [name, digest];
      }),
  );
  assert.equal(
    sha256(jsonBuffer),
    expected.get("sixth-order-cycle-audit.json"),
  );
  assert.equal(
    sha256(stdoutBuffer),
    expected.get("sixth-order-cycle-audit.stdout.log"),
  );
  assert.equal(
    sha256(stderrBuffer),
    expected.get("sixth-order-cycle-audit.stderr.log"),
  );
});

test("archives a formal journal figure for the R0.67A theorem", async () => {
  const python = process.env.CODEX_PYTHON || "python3";
  const validator = new URL(
    "../research/validate_figure_package.py",
    import.meta.url,
  );
  const { stdout } = await execFileAsync(
    python,
    [validator.pathname, figureRoot.pathname],
    { cwd: repository },
  );
  const validation = JSON.parse(stdout);
  assert.deepEqual(validation.errors, []);
  assert.deepEqual(validation.warnings, []);

  const manifest = JSON.parse(
    await readFile(new URL("manifest.json", figureRoot), "utf8"),
  );
  assert.equal(manifest.figureId, "fig-r067-sixth-order-cycle");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 108);
  assert.equal(manifest.figure.outputs.length, 3);
  assert.equal(manifest.figure.outputs.at(-1).dpi, 600);
  assert.equal(manifest.figure.outputs.at(-1).pixels, "4204 by 2551");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.match(manifest.supportedClaim, /Y_r=C6,0 mu\^r\+O\(300\^r\)/);
  assert.match(manifest.supportedClaim, /complete heat-weighted five-simplex projection is not certified/);
});
