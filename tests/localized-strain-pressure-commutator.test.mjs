import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const noteUrl = new URL(
  "../research/localized_strain_pressure_commutator_note.md",
  import.meta.url,
);

test("states the exact R0.69I localized strain identities and boundary", async () => {
  const note = await readFile(noteUrl, "utf8");
  assert.ok(note.includes("\\int_{\\mathbb T^3}\\phi S:H\\,dx"));
  assert.ok(note.includes("(\\Delta p)u\\cdot\\nabla\\phi"));
  assert.ok(note.includes("\\left(\\frac12qu-A^2u\\right)\\cdot\\nabla\\phi"));
  assert.ok(note.includes("+2\\int\\phi\\det S"));
  assert.ok(note.includes("=-\\frac{676}{40425}"));
  assert.ok(note.includes("=\\frac{228}{2695}\\ne0"));
  assert.match(note, /both localized commutators are genuinely nonzero/i);
  assert.match(note, /closes only the bare-localization route/i);
  assert.match(note, /does not solve the Millennium Problem/i);
  assert.match(note, /R0\.69J will split the pressure on a ball/);
});

test("reproduces the exact R0.69I Fourier and scaling audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [
      new URL(
        "../research/localized_strain_pressure_commutator_audit.py",
        import.meta.url,
      ).pathname,
    ],
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
  assert.equal(result.exactValues.localizedPressurePairing, "-676/40425");
  assert.equal(result.exactValues.localizedBetchovPairing, "228/2695");
  assert.equal(result.exactValues.globalPressurePairing, "0");
  assert.equal(result.exactValues.globalBetchovPairing, "0");
  assert.deepEqual(new Set(Object.values(result.scalingDegrees)), new Set([3]));
  assert.deepEqual(result.weight.pressureMode, [0, 0, 1]);
  assert.deepEqual(result.weight.betchovMode, [1, 0, 0]);
});

test("archives the source-locked R0.69I certificate", async () => {
  const certificateRoot = new URL(
    "../research/certificates/r069i/",
    import.meta.url,
  );
  const [certificateText, sumsText, readme, resources] = await Promise.all([
    readFile(new URL("localized-strain-pressure-commutator.json", certificateRoot), "utf8"),
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
    "b03985d6d2fd1f55ba5d600cb75859efb694876b",
  );
  assert.match(readme, /bare cutoff localization/i);
  assert.match(resources, /exited:0/);

  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
