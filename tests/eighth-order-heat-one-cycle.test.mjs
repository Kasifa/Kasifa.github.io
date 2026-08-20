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
  "../research/eighth_order_heat_one_cycle_note.md",
  import.meta.url,
);
const auditUrl = new URL(
  "../research/eighth_order_heat_one_cycle_audit.py",
  import.meta.url,
);
const certificateRoot = new URL(
  "../research/certificates/r068b2a/",
  import.meta.url,
);

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

test("states the exact finite R0.68B-2a sign and its asymptotic boundary", async () => {
  const [note, audit] = await Promise.all([
    readFile(noteUrl, "utf8"),
    readFile(auditUrl, "utf8"),
  ]);

  assert.match(note, /R0\.68B-2a — An exact first-cycle sign/);
  assert.ok(note.includes("7{,}823{,}536"));
  assert.ok(note.includes("273{,}823{,}760"));
  assert.ok(note.includes("J_0=35\\times11{,}896=416{,}360"));
  assert.ok(note.includes("\\max\\beta_j=114888"));
  assert.ok(note.includes("0.00741508936"));
  assert.ok(note.includes("{8+6\\choose6}=3003"));
  assert.ok(note.includes("\\frac{16^6}{16^9}=\\frac1{4096}"));
  assert.match(note, /not the sign of the\s+dominant asymptotic projection/);
  assert.match(audit, /finite-scale sign certificate/);
  assert.match(audit, /not a certificate for the\s+dominant asymptotic heat projection/);
});

test("reproduces the complete first-cycle seven-simplex interval", async () => {
  const scratch = await mkdtemp(join(tmpdir(), "r068b2a-heat-"));
  const output = join(scratch, "one-cycle.json");
  const python = process.env.CODEX_PYTHON || "python3";
  await execFileAsync(
    python,
    [auditUrl.pathname, "--output", output, "--order", "32"],
    { cwd: repository, maxBuffer: 80 * 1024 * 1024 },
  );
  const certificate = JSON.parse(await readFile(output, "utf8"));
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(certificate.parameters.validCarrierTuples, 7823536);
  assert.equal(certificate.parameters.signedPaths, 273823760);
  assert.equal(certificate.dynamicProgram.finalStates, 4178);
  assert.equal(certificate.heatRates.maximumIntegerRate, 114888);
  assert.ok(Number(certificate.exactTaylor.finalLowerDisplay) > 0.0070);
  assert.ok(Number(certificate.exactTaylor.finalUpperDisplay) < 0.0078);
  assert.ok(Number(certificate.exactTaylor.absoluteTailBoundDisplay) < 0.001);
});

test("locks the formal R0.68B-2a certificate and monitored resources", async () => {
  const [jsonBuffer, stdoutBuffer, stderrBuffer, resourcesBuffer, checksumText] =
    await Promise.all([
      readFile(new URL("eighth-order-heat-one-cycle-audit.json", certificateRoot)),
      readFile(new URL("eighth-order-heat-one-cycle-audit.stdout.log", certificateRoot)),
      readFile(new URL("eighth-order-heat-one-cycle-audit.stderr.log", certificateRoot)),
      readFile(new URL("resources.csv", certificateRoot)),
      readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    ]);
  const certificate = JSON.parse(jsonBuffer.toString("utf8"));
  assert.equal(certificate.status, "passed");
  assert.equal(Object.values(certificate.checks).every(Boolean), true);
  assert.equal(certificate.parameters.TaylorOrder, 44);
  assert.equal(certificate.provenance.sourceCommit.length, 40);
  assert.deepEqual(jsonBuffer, stdoutBuffer);
  assert.match(stderrBuffer.toString("utf8"), /depth=7\/7 states=4178/);
  assert.match(stderrBuffer.toString("utf8"), /monitor: finished returncode=0/);
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
    ["eighth-order-heat-one-cycle-audit.json", jsonBuffer],
    ["eighth-order-heat-one-cycle-audit.stdout.log", stdoutBuffer],
    ["eighth-order-heat-one-cycle-audit.stderr.log", stderrBuffer],
    ["resources.csv", resourcesBuffer],
  ]) {
    assert.equal(sha256(buffer), expected.get(name));
  }
});
