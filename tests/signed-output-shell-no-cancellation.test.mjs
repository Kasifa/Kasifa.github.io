import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the exact R0.69S one-shell no-cancellation theorem", async () => {
  const note = await readFile(
    new URL("../research/signed_output_shell_no_cancellation_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("\\mathcal F_0(u)=2"));
  assert.ok(note.includes("\\Gamma(u)=1"));
  assert.ok(note.includes("(T_k,T_p,T_q)=(2,-3,1)"));
  assert.ok(note.includes("\\int_{\\mathbb T^3}\\omega\\cdot S\\omega\\,dx=2>0"));
  assert.match(note, /does not solve\s+the Millennium Problem/i);
  assert.match(note, /R0\.69T will test the fourth option/i);
});

test("reproduces the R0.69S exact Fourier and shell audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/signed_output_shell_no_cancellation_audit.py", import.meta.url).pathname],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 15);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.deepEqual(result.witness.modalTransfers, ["2", "-3", "1"]);
  assert.equal(result.witness.fullVortexStretching, "2");
  assert.equal(result.shellDecomposition.cancellationRatio, "1");
});

test("archives the source-locked R0.69S certificate", async () => {
  const certificateRoot = new URL("../research/certificates/r069s/", import.meta.url);
  const [certificateText, sumsText, readme, resources] = await Promise.all([
    readFile(new URL("signed-output-shell-no-cancellation.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("resources.csv", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.keys(certificate.checks).length, 17);
  assert.ok(Object.values(certificate.checks).every(Boolean));
  assert.equal(
    certificate.provenance.sourceCommit,
    "3bbbb660949181380420ebba9f103e901e560043",
  );
  assert.match(readme, /shell-cancellation ratio/i);
  assert.match(readme, /physical-space annular cancellation/i);
  assert.match(resources, /exited:0/);

  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
