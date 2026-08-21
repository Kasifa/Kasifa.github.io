import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the R0.69N energy-level commutator bridge and time gap", async () => {
  const note = await readFile(
    new URL("../research/energy_stress_commutator_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("r^3|\\mathcal P_{v,r}|"));
  assert.ok(note.includes("X_q\\bigl(D_A^{1/2}+\\sigma_A+\\mu_A\\bigr)"));
  assert.ok(note.includes("\\mu_v^{1/2}\\sigma_v^{3/2}"));
  assert.ok(note.includes("\\varepsilon D_A+C_\\varepsilon\\mu_v\\sigma_v^3"));
  assert.ok(note.includes("\\mathcal T(S[v])=0"));
  assert.ok(note.includes("\\mathcal H^1"));
  assert.ok(note.includes("\\dot W^{s,\\,3/s}"));
  assert.ok(note.includes("s\\left(\\frac3s\\right)=3"));
  assert.ok(note.includes("\\int\\sigma_A^2\\,dt=1"));
  assert.ok(note.includes("\\int\\mu_A\\sigma_A^3\\,dt=A"));
  assert.match(note, /Hardy--BMO duality wall/i);
  assert.match(note, /functional exponent\s+witness only/i);
  assert.match(note, /does\s+not solve the Millennium Problem/i);
  assert.match(note, /R0\.69O will test/i);
});

test("reproduces the R0.69N exponent and duality audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/energy_stress_commutator_audit.py", import.meta.url).pathname],
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
  assert.equal(result.energyCommutatorFamily.q4.p, "2");
  assert.equal(result.energyCommutatorFamily.q4.theta, "3/4");
  assert.equal(result.energyCommutatorFamily.q4.sigmaAfterYoung, "3");
  assert.equal(result.energyCommutatorFamily.q6.sigmaAfterYoung, "4");
  assert.equal(result.hardyDualityFrontier.criticalProduct, "3");
  assert.equal(result.hardyDualityFrontier.hilbertDerivativeOrder, "3/2");
  assert.equal(result.timeSpike.quadraticMass, "1");
  assert.equal(result.timeSpike.cubicMass, "A");
});

test("archives the source-locked R0.69N certificate", async () => {
  const certificateRoot = new URL("../research/certificates/r069n/", import.meta.url);
  const [certificateText, sumsText, readme, resources] = await Promise.all([
    readFile(new URL("energy-stress-commutator.json", certificateRoot), "utf8"),
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
    "eb80615c8efe45dd26cdbb6ecb1c6e78ab264b4e",
  );
  assert.match(readme, /energy-level replacement/i);
  assert.match(resources, /exited:0/);

  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
