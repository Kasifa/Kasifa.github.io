import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "../figures/r069l-three-zone/fig-r069l-three-zone/",
  import.meta.url,
);

test("archives the formal R0.69L parameter-migration figure", async () => {
  const [manifestText, validationText, caption, contract] = await Promise.all(
    ["manifest.json", "validation.json", "caption.md", "figure-contract.md"].map(
      (path) => readFile(new URL(path, figureRoot), "utf8"),
    ),
  );
  const manifest = JSON.parse(manifestText);
  const validation = JSON.parse(validationText);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figureId, "fig-r069l-three-zone");
  assert.equal(
    manifest.git.sourceCommit,
    "e5bcd77e238edc7cabf49d9c96e792ef92a33aba",
  );
  assert.equal(
    manifest.git.certificateCommit,
    "2b65698e149c0a091608e90da5a5fbe7a0defcd0",
  );
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 86);
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 8);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.match(caption, /migrates the pressure\s+budget instead of eliminating it/i);
  assert.match(
    contract,
    /neither proves\s+Navier-+Stokes regularity nor constructs a singularity/i,
  );

  for (const output of manifest.figure.outputs) {
    const payload = await readFile(new URL(output.path, figureRoot));
    assert.equal(
      createHash("sha256").update(payload).digest("hex"),
      output.sha256,
    );
    const extension = output.path.split(".").at(-1);
    const published = await readFile(
      new URL("../public/figures/r0-69l-three-zone." + extension, import.meta.url),
    );
    assert.deepEqual(published, payload);
  }
});

test("the R0.69L figure package passes the strict validator", () => {
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

test("pins a deterministic R0.69L SVG hash salt", async () => {
  const plot = await readFile(new URL("plot.py", figureRoot), "utf8");
  assert.match(plot, /rcParams\["svg\.hashsalt"\] = FIGURE_ID/);
});
