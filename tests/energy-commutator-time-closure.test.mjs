import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the R0.69O dissipation-assisted pressure closure and boundary", async () => {
  const note = await readFile(
    new URL("../research/energy_commutator_time_closure_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("\\sigma_v^2\\leq C\\mu_v\\mathcal D_v^{1/2}"));
  assert.ok(note.includes("\\varepsilon^{-3}\\mu_v^4\\sigma_v^2"));
  assert.ok(note.includes("\\mathsf A_v^2\\mathsf E_v"));
  assert.ok(note.includes("\\frac{27}{256}\\varepsilon^{-3}\\mu^4"));
  assert.ok(note.includes("\\int\\mathcal D_A\\,d\\tau\\geq cA^2"));
  assert.ok(note.includes("\\mu^{14/3}"));
  assert.ok(note.includes("\\mu^{18/5}"));
  assert.ok(note.includes("B_\\infty\\leq\\mathfrak M_2/120"));
  assert.ok(note.includes("\\sigma^6"));
  assert.match(note, /localized cubic strain\/vorticity stretching/i);
  assert.match(note, /does not solve the Millennium Problem/i);
  assert.match(note, /R0\.69P will test/i);
});

test("reproduces the R0.69O exponent and sharpness audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/energy_commutator_time_closure_audit.py", import.meta.url).pathname],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.equal(result.status, "passed");
  assert.equal(Object.keys(result.checks).length, 16);
  assert.ok(Object.values(result.checks).every(Boolean));
  assert.equal(result.leadingClosure.kineticExponent, "4");
  assert.equal(result.leadingClosure.enstrophyExponent, "2");
  assert.equal(result.leadingClosure.epsilonExponent, "-3");
  assert.equal(result.timeSpike.minimumDissipationMass, "A**2");
  assert.equal(
    result.lowerTerms.muHalfSigmaFiveHalves.muAfterYoung,
    "14/3",
  );
  assert.equal(
    result.lowerTerms.muThreeHalvesSigmaThreeHalves.muAfterYoung,
    "18/5",
  );
  assert.equal(result.remainingObstruction.youngRemainder, "sigma^6");
});

test("archives the source-locked R0.69O certificate", async () => {
  const certificateRoot = new URL("../research/certificates/r069o/", import.meta.url);
  const [certificateText, sumsText, readme, resources] = await Promise.all([
    readFile(new URL("energy-commutator-time-closure.json", certificateRoot), "utf8"),
    readFile(new URL("SHA256SUMS", certificateRoot), "utf8"),
    readFile(new URL("README.md", certificateRoot), "utf8"),
    readFile(new URL("resources.csv", certificateRoot), "utf8"),
  ]);
  const certificate = JSON.parse(certificateText);
  assert.equal(certificate.status, "passed");
  assert.equal(Object.keys(certificate.checks).length, 18);
  assert.ok(Object.values(certificate.checks).every(Boolean));
  assert.equal(
    certificate.provenance.sourceCommit,
    "46f217d0d6cb29f3a60e8c5a101e92c6f7e8e560",
  );
  assert.match(readme, /quadratic enstrophy/i);
  assert.match(resources, /exited:0/);

  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
