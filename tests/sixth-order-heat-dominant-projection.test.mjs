import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { promisify } from "node:util";
import test from "node:test";

const execFileAsync = promisify(execFile);
const repository = new URL("..", import.meta.url).pathname;
const noteUrl = new URL(
  "../research/sixth_order_heat_dominant_projection_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/sixth_order_heat_dominant_projection_audit.py",
  import.meta.url,
);
const certificateRoot = new URL("../research/certificates/r067c2/", import.meta.url);
const figureRoot = new URL(
  "../figures/r067c2-dominant-heat/fig-r067c2-dominant-heat/",
  import.meta.url,
);

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

test("states the guarded R0.67C-2 dominant heat theorem and its boundary", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);
  assert.match(note, /R0\.67C-2 — A strict sign for the dominant sixth-order heat projection/);
  assert.ok(note.includes("320\\times210=67{,}200"));
  assert.ok(note.includes("=\\frac1{4096}"));
  assert.ok(note.includes("5.1612521669\\times10^{-5}"));
  assert.ok(note.includes("-1.71549\\times10^{-6}"));
  assert.ok(note.includes("-2.02514\\times10^{-7}"));
  assert.match(note, /one even order, not the full nonlinear Picard series/);
  assert.match(note, /globally smooth invariant shear class/);
  assert.match(audit, /not a result\s+about all Picard orders or Navier--Stokes regularity/);
});

test("locks the formal R0.67C-2 certificate and monitored resources", async () => {
  const [jsonBuffer, stdoutBuffer, stderrBuffer, resourcesBuffer, checksumText] =
    await Promise.all([
      readFile(new URL("sixth-order-heat-dominant-projection-audit.json", certificateRoot)),
      readFile(new URL("sixth-order-heat-dominant-projection-audit.stdout.log", certificateRoot)),
      readFile(new URL("sixth-order-heat-dominant-projection-audit.stderr.log", certificateRoot)),
      readFile(new URL("resources.csv", certificateRoot)),
      readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    ]);
  const certificate = JSON.parse(jsonBuffer.toString("utf8"));
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(Object.keys(certificate.checks).length, 14);
  assert.equal(certificate.finiteJet.degree, 6);
  assert.equal(certificate.finiteJet.channelsPerState, 210);
  assert.equal(certificate.finiteJet.totalDimension, 67200);
  assert.equal(certificate.resolvent.remainderTransferScale.numerator, "1");
  assert.equal(certificate.resolvent.remainderTransferScale.denominator, "4096");
  assert.ok(certificate.analyticDerivativeBound.rawMaximum < 6e-5);
  assert.ok(certificate.conclusion.dominantHeatProjectionUpper < 0);
  assert.equal(
    certificate.provenance.sourceCommit,
    "ed153f5919f040c7fc16b169685b05fc574f3d17",
  );
  assert.deepEqual(jsonBuffer, stdoutBuffer);
  assert.match(stderrBuffer.toString("utf8"), /shuffle=10\/10/);
  assert.match(stderrBuffer.toString("utf8"), /\b0\s+swaps/);
  assert.match(resourcesBuffer.toString("utf8"), /exited:0/);

  const expected = new Map(
    checksumText
      .trim()
      .split("\n")
      .map((line) => {
        const [digest, name] = line.trim().split(/\s+/);
        return [name, digest];
      }),
  );
  for (const [name, buffer] of [
    ["sixth-order-heat-dominant-projection-audit.json", jsonBuffer],
    ["sixth-order-heat-dominant-projection-audit.stdout.log", stdoutBuffer],
    ["sixth-order-heat-dominant-projection-audit.stderr.log", stderrBuffer],
    ["resources.csv", resourcesBuffer],
  ]) {
    assert.equal(sha256(buffer), expected.get(name));
  }
});

test("archives a formal journal figure for the R0.67C-2 sign certificate", async () => {
  const python = process.env.CODEX_PYTHON || "python3";
  const validator = new URL("../research/validate_figure_package.py", import.meta.url);
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
  assert.equal(manifest.figureId, "fig-r067c2-dominant-heat");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 105);
  assert.equal(manifest.figure.outputs.at(-1).dpi, 600);
  assert.equal(manifest.figure.outputs.at(-1).pixels, "4204 by 2480");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.match(manifest.supportedClaim, /strict negative interval/);
  assert.match(manifest.claimBoundary, /all Picard orders/);
});
