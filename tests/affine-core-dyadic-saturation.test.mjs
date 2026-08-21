import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the R0.69U core-saturation theorem and full-space boundary", async () => {
  const note = await readFile(
    new URL("../research/affine_core_dyadic_saturation_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("\\Gamma_{\\rm core}(R)"));
  assert.ok(note.includes("=\\frac52+E"));
  assert.ok(note.includes("=\\frac52-E"));
  assert.ok(note.includes("\\Gamma_{\\rm ann}(u_R)=\\Gamma_{\\rm ann}(u_1)"));
  assert.ok(note.includes("only \\(j=m-1,m\\) can contribute"));
  assert.match(note, /shape, not merely scale/i);
  assert.match(note, /does not solve the Millennium Problem/i);
});

test("reproduces the exact R0.69U symbolic and rational audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/affine_core_dyadic_saturation_audit.py", import.meta.url).pathname],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 17);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.equal(result.cutoffConstruction.energyBound, "50/21");
  assert.equal(result.limitingCarrier.outerRadialMargin, "5/42");
  assert.equal(result.limitingCarrier.outerShareLowerBound, "1/42");
  assert.equal(result.limitingCarrier.eventualCoreCancellationRatio, "1");
  assert.equal(result.fullSpaceScaling.ratio, "Gamma_ann(u_R)=Gamma_ann(u_1)");
});

test("archives the source-locked R0.69U certificate and resource record", async () => {
  const certificateRoot = new URL("../research/certificates/r069u/", import.meta.url);
  const [certificateText, sumsText, readme, resources] = await Promise.all([
    readFile(new URL("affine-core-dyadic-saturation.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("resources.csv", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.keys(certificate.checks).length, 19);
  assert.ok(Object.values(certificate.checks).every(Boolean));
  assert.equal(
    certificate.provenance.sourceCommit,
    "9748c451e9d1cc8d6e7e2bcd732f79691b1c13ca",
  );
  assert.match(readme, /eventual exact saturation/i);
  assert.match(readme, /full-space annular cancellation ratio unchanged/i);
  assert.match(resources, /exited:0/);

  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
