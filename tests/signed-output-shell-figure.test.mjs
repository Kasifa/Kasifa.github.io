import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "../figures/r069s-single-shell/fig-r069s-single-shell/",
  import.meta.url,
);

test("archives the formal R0.69S single-shell obstruction figure", async () => {
  const [manifestText, validationText, caption, contract] = await Promise.all(
    ["manifest.json", "validation.json", "caption.md", "figure-contract.md"].map(
      (fileName) => readFile(new URL(fileName, figureRoot), "utf8"),
    ),
  );
  const manifest = JSON.parse(manifestText);
  const validation = JSON.parse(validationText);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figureId, "fig-r069s-single-shell");
  assert.equal(manifest.git.sourceCommit, "3bbbb660949181380420ebba9f103e901e560043");
  assert.equal(manifest.git.certificateCommit, "8b242ef41057aee2a08ece71f33682a7a50f077d");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 82);
  assert.equal(manifest.figure.outputs.find((entry) => entry.path === "figure.png").dpi, 600);
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 10);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.match(caption, /cancellation ratio is\s+exactly 'Gamma=1'/i);
  assert.match(caption, /physical-space annuli/i);
  assert.match(contract, /no universal deficit\s+factor below one/i);

  for (const output of manifest.figure.outputs) {
    const payload = await readFile(new URL(output.path, figureRoot));
    assert.equal(createHash("sha256").update(payload).digest("hex"), output.sha256);
    const extension = output.path.split(".").at(-1);
    const published = await readFile(
      new URL("../public/figures/r0-69s-single-shell." + extension, import.meta.url),
    );
    assert.deepEqual(published, payload);
  }
});

test("the R0.69S figure package passes the strict validator", () => {
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

test("pins a deterministic R0.69S SVG hash salt", async () => {
  const plot = await readFile(new URL("plot.py", figureRoot), "utf8");
  assert.match(plot, /rcParams\["svg\.hashsalt"\] = FIGURE_ID/);
});
