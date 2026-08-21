import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "../figures/r069n-energy-commutator/fig-r069n-energy-commutator/",
  import.meta.url,
);

test("archives the formal R0.69N energy-commutator figure", async () => {
  const [manifestText, validationText, caption, contract] = await Promise.all(
    ["manifest.json", "validation.json", "caption.md", "figure-contract.md"].map(
      (path) => readFile(new URL(path, figureRoot), "utf8"),
    ),
  );
  const manifest = JSON.parse(manifestText);
  const validation = JSON.parse(validationText);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figureId, "fig-r069n-energy-commutator");
  assert.equal(manifest.git.sourceCommit, "eb80615c8efe45dd26cdbb6ecb1c6e78ab264b4e");
  assert.equal(manifest.git.certificateCommit, "5e7798168a831b0cf542d75bc457134592ff7b6c");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 82);
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 10);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.match(caption, /reaches spatial energy regularity/i);
  assert.match(contract, /not a Navier-+Stokes\s+solution/i);

  for (const output of manifest.figure.outputs) {
    const payload = await readFile(new URL(output.path, figureRoot));
    assert.equal(createHash("sha256").update(payload).digest("hex"), output.sha256);
    const extension = output.path.split(".").at(-1);
    const published = await readFile(
      new URL("../public/figures/r0-69n-energy-commutator." + extension, import.meta.url),
    );
    assert.deepEqual(published, payload);
  }
});

test("the R0.69N figure package passes the strict validator", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [
      new URL("../research/validate_figure_package.py", import.meta.url).pathname,
      figureRoot.pathname,
    ],
    {
      cwd: root.pathname,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const report = JSON.parse(run.stdout);
  assert.deepEqual(report.errors, []);
  assert.deepEqual(report.warnings, []);
});

test("pins a deterministic R0.69N SVG hash salt", async () => {
  const plot = await readFile(new URL("plot.py", figureRoot), "utf8");
  assert.match(plot, /rcParams\["svg\.hashsalt"\] = FIGURE_ID/);
});
