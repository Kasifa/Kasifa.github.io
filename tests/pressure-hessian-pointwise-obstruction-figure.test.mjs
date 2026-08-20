import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "../figures/r069h-pressure-obstruction/fig-r069h-pressure-obstruction/",
  import.meta.url,
);

test("archives the formal R0.69H pressure-obstruction figure", async () => {
  const [manifestText, validationText, caption, contract] = await Promise.all([
    readFile(new URL("manifest.json", figureRoot), "utf8"),
    readFile(new URL("validation.json", figureRoot), "utf8"),
    readFile(new URL("caption.md", figureRoot), "utf8"),
    readFile(new URL("figure-contract.md", figureRoot), "utf8"),
  ]);
  const manifest = JSON.parse(manifestText);
  const validation = JSON.parse(validationText);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figureId, "fig-r069h-pressure-obstruction");
  assert.equal(
    manifest.git.sourceCommit,
    "86ac684e2a2564f56d42d9c216918ed659652846",
  );
  assert.equal(
    manifest.git.certificateCommit,
    "33ca9d4f8f2893cc12828895e36ac0e787077af0",
  );
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 86);
  assert.equal(manifest.figure.outputs.length, 3);
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 8);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.match(caption, /identical local velocity gradients do not determine/i);
  assert.match(
    contract,
    /neither proves Navier-+Stokes regularity nor constructs\s+a\s+singularity/i,
  );

  for (const output of manifest.figure.outputs) {
    const payload = await readFile(new URL(output.path, figureRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, output.sha256, output.path + " hash mismatch");

    const extension = output.path.split(".").at(-1);
    const publicPayload = await readFile(
      new URL(
        `../public/figures/r0-69h-pressure-obstruction.${extension}`,
        import.meta.url,
      ),
    );
    assert.deepEqual(
      publicPayload,
      payload,
      output.path + " public mirror mismatch",
    );
  }
});

test("the R0.69H figure package passes the strict validator", () => {
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
