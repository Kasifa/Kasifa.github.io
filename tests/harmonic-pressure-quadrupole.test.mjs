import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the R0.69J harmonic quadrupole obstruction and boundary", async () => {
  const note = await readFile(
    new URL("../research/harmonic_pressure_quadrupole_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("Q_R:=\\nabla^2p_{\\mathrm{far}}(0)"));
  assert.ok(note.includes("\\frac{3}{2\\pi R^3}\\operatorname{diag}(1,-1,0)"));
  assert.ok(note.includes("S_0:Q_R=\\frac{3}{\\pi R^3}\\ne0"));
  assert.match(note, /remainder gains one scale ratio/i);
  assert.match(note, /signed scalar pressure source, not yet a construction/i);
  assert.match(note, /closes the naive harmonic-subtraction route/i);
  assert.match(note, /does\s+not solve the Millennium Problem/i);
  assert.match(note, /R0\.69K will treat the shellwise quadrupole coefficients/);
});

test("reproduces the exact R0.69J four-source audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/harmonic_pressure_quadrupole_audit.py", import.meta.url).pathname],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 10);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.deepEqual(result.source.weights, [1, 1, -1, -1]);
  assert.deepEqual(result.source.firstMoment, ["0", "0", "0"]);
  assert.deepEqual(result.centerJet.fourPiHessian, [
    ["6/R**3", "0", "0"],
    ["0", "-6/R**3", "0"],
    ["0", "0", "0"],
  ]);
  assert.equal(result.centerJet.actualStrainHessianPairing, "3/(pi*R**3)");
});

test("archives the source-locked R0.69J certificate", async () => {
  const certificateRoot = new URL(
    "../research/certificates/r069j/",
    import.meta.url,
  );
  const [certificateText, sumsText, readme, resources] = await Promise.all([
    readFile(new URL("harmonic-pressure-quadrupole.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("resources.csv", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.keys(certificate.checks).length, 12);
  assert.ok(Object.values(certificate.checks).every(Boolean));
  assert.equal(
    certificate.provenance.sourceCommit,
    "7271dd542389ab22b24f6f54980e7d2763188c2f",
  );
  assert.match(readme, /signed scalar pressure source/i);
  assert.match(resources, /exited:0/);

  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
