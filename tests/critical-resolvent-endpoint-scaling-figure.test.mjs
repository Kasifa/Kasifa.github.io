import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "../figures/r069f-endpoint-scaling/fig-r069f-endpoint-scaling/",
  import.meta.url,
);
const publicRoot = new URL("../public/figures/", import.meta.url);

test("archives the formal R0.69F endpoint-scaling figure", async () => {
  const [manifestText, validationText, caption, contract] = await Promise.all([
    readFile(new URL("manifest.json", figureRoot), "utf8"),
    readFile(new URL("validation.json", figureRoot), "utf8"),
    readFile(new URL("caption.md", figureRoot), "utf8"),
    readFile(new URL("figure-contract.md", figureRoot), "utf8"),
  ]);
  const manifest = JSON.parse(manifestText);
  const validation = JSON.parse(validationText);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figureId, "fig-r069f-endpoint-scaling");
  assert.equal(manifest.git.sourceCommit,
    "c3f3d94620f6852e48e07525cc81f2c94ee1511d");
  assert.equal(manifest.git.certificateCommit,
    "53aa9dfc5a58264df349e219c5a3cfe97c80dbe8");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 92);
  assert.equal(manifest.figure.outputs.length, 3);
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 8);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.match(caption, /classical type-I scale/i);
  assert.match(contract, /neither excludes nor constructs a singularity/i);

  for (const output of manifest.figure.outputs) {
    const payload = await readFile(new URL(output.path, figureRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, output.sha256, output.path + " hash mismatch");
  }
});

test("the R0.69F figure package passes the strict validator", () => {
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

test("publishes byte-exact mirrors of the R0.69F figure", async () => {
  for (const extension of ["pdf", "svg", "png"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL("figure." + extension, figureRoot)),
      readFile(
        new URL("r0-69f-endpoint-scaling." + extension, publicRoot),
      ),
    ]);
    assert.equal(
      createHash("sha256").update(published).digest("hex"),
      createHash("sha256").update(archived).digest("hex"),
      extension + " public mirror differs from archived figure",
    );
  }
});
