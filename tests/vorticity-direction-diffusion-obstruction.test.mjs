import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);

test("states the exact R0.69Q polar identities and strict boundary", async () => {
  const note = await readFile(
    new URL("../research/vorticity_direction_diffusion_obstruction_note.md", import.meta.url),
    "utf8",
  );
  assert.ok(note.includes("=\\rho\\alpha-\\nu\\rho|\\nabla\\xi|^2"));
  assert.ok(note.includes("(I-\\xi\\otimes\\xi)\\Delta\\xi"));
  assert.ok(note.includes("|\\nabla\\omega|^2\n =|\\nabla\\rho|^2+\\rho^2|\\nabla\\xi|^2"));
  assert.ok(note.includes("\\rho^2\\alpha=\\sqrt{\\frac23}\\,s w^2>0"));
  assert.ok(note.includes("\\frac{D_\\xi(T)}{T}\\longrightarrow0"));
  assert.ok(note.includes("\\frac{D_\\omega(T)}{T}\\longrightarrow0"));
  assert.match(note, /does not solve the Millennium Problem/i);
  assert.match(note, /R0\.69R will keep the nonlocal difference/i);
});

test("reproduces the R0.69Q exact symbolic audit", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/vorticity_direction_diffusion_obstruction_audit.py", import.meta.url).pathname],
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
  assert.equal(result.affineCore.positiveStretching, "sqrt(6)*s*w**2/3");
  assert.equal(result.scalingObstruction.ratio, "L**2*P*a/(D*nu)");
  assert.equal(result.shortTimeObstruction.fullDissipationAverageLimit, "0");
});

test("archives the source-locked R0.69Q certificate", async () => {
  const certificateRoot = new URL("../research/certificates/r069q/", import.meta.url);
  const [certificateText, sumsText, readme, resources] = await Promise.all([
    readFile(new URL("vorticity-direction-diffusion-obstruction.json", certificateRoot), "utf8"),
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
    "c5e19140c3dc79d22eb368e63dc2014681afff18",
  );
  assert.match(readme, /radial--angular split/i);
  assert.match(readme, /short-time interior-dissipation obstruction/i);
  assert.match(resources, /exited:0/);

  for (const line of sumsText.trim().split("\n")) {
    const [expected, fileName] = line.trim().split(/\s+/, 2);
    const payload = await readFile(new URL(fileName, certificateRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, expected, fileName + " hash mismatch");
  }
});
