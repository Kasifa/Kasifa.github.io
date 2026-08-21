import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the sharp R0.69P stretching geometry and claim boundary", async () => {
  const note = await readFile(
    new URL("../research/vorticity_stretching_sign_structure_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("\\sqrt{\\frac23}\\,|S|\\,|\\omega|^2"));
  assert.ok(note.includes("v_A=\\nabla\\times(\\chi B_A)"));
  assert.ok(note.includes("\\int\\omega\\cdot S\\omega\\,dx\n =-4\\int\\det S\\,dx"));
  assert.ok(note.includes("-4\\det S\\leq 2\\lambda_2^+|S|^2"));
  assert.ok(note.includes("\\lambda_2^+\\leq\\frac{|S|}{\\sqrt6}"));
  assert.ok(note.includes("\\frac{27}{256}\\varepsilon^{-3}\\sigma^6"));
  assert.match(note, /does not solve the Millennium Problem/i);
  assert.match(note, /R0\.69Q will therefore test/i);
});

test("reproduces the R0.69P symbolic and local-realization audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/vorticity_stretching_sign_structure_audit.py", import.meta.url).pathname],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 18);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.equal(result.sharpPointwiseStretching.constant, "sqrt(2/3)");
  assert.equal(result.betchov.sharpSupremum, "2");
  assert.equal(result.energyOnlyEndpoint.power, "sigma^6");
  assert.equal(
    result.energyOnlyEndpoint.youngRemainder,
    "27*sigma**6/(256*epsilon**3)",
  );
});

test("archives the source-locked R0.69P certificate", async () => {
  const certificateRoot = new URL("../research/certificates/r069p/", import.meta.url);
  const [certificateText, sumsText, readme, resources] = await Promise.all([
    readFile(new URL("vorticity-stretching-sign-structure.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("resources.csv", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.keys(certificate.checks).length, 20);
  assert.ok(Object.values(certificate.checks).every(Boolean));
  assert.equal(
    certificate.provenance.sourceCommit,
    "1471752c76624699c0f5a40d523bdc484a49cbd3",
  );
  assert.match(readme, /sqrt\(2\/3\)/i);
  assert.match(readme, /sextic remainder/i);
  assert.match(resources, /exited:0/);

  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
