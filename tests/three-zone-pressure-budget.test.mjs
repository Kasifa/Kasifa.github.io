import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the R0.69L three-zone budget and parameter-migration obstruction", async () => {
  const note = await readFile(
    new URL("../research/three_zone_pressure_budget_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("r^3|\\mathcal P_r|"));
  assert.ok(note.includes("\\sigma_r(N_r+B_M)"));
  assert.ok(note.includes("2^{-5M}\\sum_{m\\geq M}e_m"));
  assert.ok(note.includes("\\inf_{M\\geq3}B_M"));
  assert.ok(note.includes("\\sum_{m\\geq2}2^{-5m}e_m"));
  assert.ok(note.includes("r^3|\\mathcal P_r|\\leq Cb_r"));
  assert.ok(note.includes("\\beta^2/\\alpha"));
  assert.match(note, /parameter-migration obstruction/i);
  assert.ok(note.includes("Finite energy and large \\(A\\) alone do\nnot imply"));
  assert.match(note, /does\s+not solve the Millennium Problem/i);
  assert.match(note, /R0\.69M will compare these quantities/i);
});

test("reproduces the exact R0.69L scaling and separation audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/three_zone_pressure_budget_audit.py", import.meta.url).pathname],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 12);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.equal(result.finiteSeparationModel.firstShellWeight, "1/1024");
  assert.equal(result.lengthExponents.rCubedPressurePairing, "0");
  assert.equal(result.lengthExponents.nearCost, "0");
  assert.equal(result.lengthExponents.firstBoundaryFlux, "0");
  assert.equal(result.lengthExponents.dissipation, "0");
  assert.equal(result.amplitudeAudit.ratio, "beta**2/alpha");
});

test("archives the source-locked R0.69L certificate", async () => {
  const certificateRoot = new URL("../research/certificates/r069l/", import.meta.url);
  const [certificateText, sumsText, readme, resources] = await Promise.all([
    readFile(new URL("three-zone-pressure-budget.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("resources.csv", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.keys(certificate.checks).length, 14);
  assert.ok(Object.values(certificate.checks).every(Boolean));
  assert.equal(
    certificate.provenance.sourceCommit,
    "SOURCE_COMMIT_PLACEHOLDER",
  );
  assert.match(readme, /parameter-migration obstruction/i);
  assert.match(resources, /exited:0/);

  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
