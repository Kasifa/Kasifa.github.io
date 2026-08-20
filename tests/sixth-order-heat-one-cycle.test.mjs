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
const noteUrl = new URL(
  "../research/sixth_order_heat_one_cycle_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/sixth_order_heat_one_cycle_audit.py",
  import.meta.url,
);
const certificateRoot = new URL("../research/certificates/r067c1/", import.meta.url);

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

test("states the exact finite R0.67C-1 sign and its asymptotic boundary", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);

  assert.match(note, /R0\.67C-1: an exact first-cycle sign/);
  assert.ok(note.includes("34,690 valid quadruples"));
  assert.ok(note.includes("346,900"));
  assert.ok(note.includes("\\max\\beta_j=67014"));
  assert.ok(note.includes("S_{6,q}^{(M=16)}>0"));
  assert.match(note, /does \*\*not\*\* determine the\s+sign of the dominant asymptotic coefficient/);
  assert.match(audit, /finite-scale sign certificate/);
  assert.match(audit, /not a certificate for the\s+dominant asymptotic heat projection/);
});

test("reproduces the complete one-cycle five-simplex interval", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r067c1-heat-"));
  const output = join(scratch, "one-cycle.json");
  const python = process.env.CODEX_PYTHON || "python3";
  await execFileAsync(
    python,
    [auditUrl.pathname, "--output", output, "--order", "32"],
    { cwd: repository, maxBuffer: 30 * 1024 * 1024 },
  );
  const certificate = JSON.parse(await readFile(output, "utf8"));
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(certificate.parameters.validCarrierTuples, 34690);
  assert.equal(certificate.parameters.signedPaths, 346900);
  assert.equal(certificate.heatRates.maximumIntegerRate, 67014);
  assert.ok(Number(certificate.exactTaylor.finalLowerDisplay) > 0.05166);
  assert.ok(Number(certificate.exactTaylor.finalUpperDisplay) < 0.05168);
  assert.ok(Number(certificate.exactTaylor.absoluteTailBoundDisplay) < 2e-12);
});

test("locks the formal R0.67C-1 certificate and monitored resources", async () => {
  const [jsonBuffer, stdoutBuffer, stderrBuffer, resourcesBuffer, checksumText] =
    await Promise.all([
      readFile(new URL("sixth-order-heat-one-cycle-audit.json", certificateRoot)),
      readFile(new URL("sixth-order-heat-one-cycle-audit.stdout", certificateRoot)),
      readFile(new URL("sixth-order-heat-one-cycle-audit.stderr", certificateRoot)),
      readFile(new URL("resources.csv", certificateRoot)),
      readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    ]);
  const certificate = JSON.parse(jsonBuffer.toString("utf8"));
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(
    certificate.provenance.sourceCommit,
    "b898179036990a352a6b73e04f2a733905f9dc32",
  );
  assert.deepEqual(jsonBuffer, stdoutBuffer);
  assert.match(stderrBuffer.toString("utf8"), /maximum resident set size/);
  assert.match(stderrBuffer.toString("utf8"), /\b0\s+swaps/);
  assert.match(resourcesBuffer.toString("utf8"), /346900,count/);

  const expected = new Map(
    checksumText
      .trim()
      .split("\n")
      .map((line) => {
        const [digest, name] = line.trim().split(/\s+/);
        return [name, digest];
      }),
  );
  assert.equal(sha256(jsonBuffer), expected.get("sixth-order-heat-one-cycle-audit.json"));
  assert.equal(sha256(stdoutBuffer), expected.get("sixth-order-heat-one-cycle-audit.stdout"));
  assert.equal(sha256(stderrBuffer), expected.get("sixth-order-heat-one-cycle-audit.stderr"));
  assert.equal(sha256(resourcesBuffer), expected.get("resources.csv"));
});
