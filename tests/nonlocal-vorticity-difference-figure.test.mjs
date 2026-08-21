import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "../figures/r069r-nonlocal-difference/fig-r069r-nonlocal-difference/",
  import.meta.url,
);

test("archives the formal R0.69R nonlocal-difference figure", async () => {
  const [manifestText, validationText, caption, contract] = await Promise.all(
    ["manifest.json", "validation.json", "caption.md", "figure-contract.md"].map(
      (fileName) => readFile(new URL(fileName, figureRoot), "utf8"),
    ),
  );
  const manifest = JSON.parse(manifestText);
  const validation = JSON.parse(validationText);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figureId, "fig-r069r-nonlocal-difference");
  assert.equal(manifest.git.sourceCommit, "97cfa19f962309bb62ae3fab0e4dcaef9f9eca38");
  assert.equal(manifest.git.certificateCommit, "e1ea54cd2e6cecdcae71db5e87980ea5c939d4d2");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 82);
  assert.equal(manifest.figure.outputs.find((entry) => entry.path === "figure.png").dpi, 600);
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 10);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.match(caption, /unique intersection is `p=q=3\/2`/i);
  assert.match(caption, /signed cross-scale cancellation remains open/i);
  assert.match(contract, /sextic `A\^6` remainder/i);

  for (const output of manifest.figure.outputs) {
    const payload = await readFile(new URL(output.path, figureRoot));
    assert.equal(createHash("sha256").update(payload).digest("hex"), output.sha256);
    const extension = output.path.split(".").at(-1);
    const published = await readFile(
      new URL("../public/figures/r0-69r-nonlocal-difference." + extension, import.meta.url),
    );
    assert.deepEqual(published, payload);
  }
});

test("the R0.69R figure package passes the strict validator", () => {
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

test("pins a deterministic R0.69R SVG hash salt", async () => {
  const plot = await readFile(new URL("plot.py", figureRoot), "utf8");
  assert.match(plot, /rcParams\["svg\.hashsalt"\] = FIGURE_ID/);
});
