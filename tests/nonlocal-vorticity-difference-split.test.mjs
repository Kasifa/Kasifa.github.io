import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the exact R0.69R optimized difference split and boundary", async () => {
  const note = await readFile(
    new URL("../research/nonlocal_vorticity_difference_split_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("\\omega(x)\\times\\bigl(\\omega(x+z)-\\omega(x)\\bigr)"));
  assert.ok(note.includes("C_{\\rm n}rA^{1/2}B^{5/2}"));
  assert.ok(note.includes("C_{\\rm f}r^{-3/2}A^3"));
  assert.ok(note.includes("\\boxed{p=q=\\frac32.}"));
  assert.ok(note.includes("\\frac{27C_*^4}{256\\varepsilon^3}A^6"));
  assert.match(note, /does not[\s\S]*solve the Millennium Problem/i);
  assert.match(note, /R0\.69S will test a signed, scale-local flux defect/i);
});

test("reproduces the R0.69R exact optimization and scaling audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/nonlocal_vorticity_difference_split_audit.py", import.meta.url).pathname],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 13);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.deepEqual(result.scalingUniqueness.solution, { p: "3/2", q: "3/2" });
  assert.equal(result.youngEndpoint.enstrophyNormPower, 6);
  assert.equal(
    result.nearFarSplit.optimalRadius,
    "2**(3/5)*3**(2/5)*A*C_f**(2/5)/(2*B*C_n**(2/5))",
  );
});

test("archives the source-locked R0.69R certificate", async () => {
  const certificateRoot = new URL("../research/certificates/r069r/", import.meta.url);
  const [certificateText, sumsText, readme, resources] = await Promise.all([
    readFile(new URL("nonlocal-vorticity-difference-split.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("resources.csv", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.keys(certificate.checks).length, 15);
  assert.ok(Object.values(certificate.checks).every(Boolean));
  assert.equal(
    certificate.provenance.sourceCommit,
    "97cfa19f962309bb62ae3fab0e4dcaef9f9eca38",
  );
  assert.match(readme, /unique homogeneous exponents/i);
  assert.match(readme, /signed cross-scale cancellation/i);
  assert.match(resources, /exited:0/);

  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
