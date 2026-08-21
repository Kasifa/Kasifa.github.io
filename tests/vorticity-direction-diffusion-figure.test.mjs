import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "../figures/r069q-direction-diffusion/fig-r069q-direction-diffusion/",
  import.meta.url,
);

test("archives the formal R0.69Q direction-diffusion figure", async () => {
  const [manifestText, validationText, caption, contract] = await Promise.all(
    ["manifest.json", "validation.json", "caption.md", "figure-contract.md"].map(
      (fileName) => readFile(new URL(fileName, figureRoot), "utf8"),
    ),
  );
  const manifest = JSON.parse(manifestText);
  const validation = JSON.parse(validationText);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figureId, "fig-r069q-direction-diffusion");
  assert.equal(manifest.git.sourceCommit, "c5e19140c3dc79d22eb368e63dc2014681afff18");
  assert.equal(manifest.git.certificateCommit, "502c4f56f660e7c7a0c916815f9142f781e36d81");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 82);
  assert.equal(manifest.figure.outputs.find((entry) => entry.path === "figure.png").dpi, 600);
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 10);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.match(caption, /same open ball/i);
  assert.match(caption, /a L\^2\/nu/i);
  assert.match(contract, /nonlocal magnitude--direction\s+estimates remain open/i);

  for (const output of manifest.figure.outputs) {
    const payload = await readFile(new URL(output.path, figureRoot));
    assert.equal(createHash("sha256").update(payload).digest("hex"), output.sha256);
    const extension = output.path.split(".").at(-1);
    const published = await readFile(
      new URL("../public/figures/r0-69q-direction-diffusion." + extension, import.meta.url),
    );
    assert.deepEqual(published, payload);
  }
});

test("the R0.69Q figure package passes the strict validator", () => {
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

test("pins a deterministic R0.69Q SVG hash salt", async () => {
  const plot = await readFile(new URL("plot.py", figureRoot), "utf8");
  assert.match(plot, /rcParams\["svg\.hashsalt"\] = FIGURE_ID/);
});
