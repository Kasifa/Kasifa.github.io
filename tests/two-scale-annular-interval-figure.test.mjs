import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL("../figures/r069w-interval-obstruction/fig-r069w-interval-obstruction/", import.meta.url);

test("archives the formal R0.69W interval-obstruction figure", async () => {
  const [manifest, metadata, validation, caption, contract] = await Promise.all([
    readFile(new URL("manifest.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("figure-data-metadata.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("validation.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("caption.md", figureRoot), "utf8"),
    readFile(new URL("figure-contract.md", figureRoot), "utf8"),
  ]);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.computation.kind, "exact-audit");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 86);
  assert.equal(manifest.git.sourceCommit, "2b3141a333d3dea0c4b7a241c11f9adbca31d1b4");
  assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  assert.equal(manifest.qa.status, "passed");
  assert.ok(Object.values(manifest.qa).every((value) => value === "passed" || value === true));
  assert.equal(metadata.status, "passed");
  assert.ok(metadata.coefficientIntervals.c3[1] < 0);
  assert.ok(metadata.discriminantInterval[1] < 0);
  assert.ok(metadata.endpointInterval[1] < 0);
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.match(caption, /rigorous interval enclosure/i);
  assert.match(contract, /static obstruction/i);
});

test("the R0.69W figure passes the strict package validator", () => {
  const run = spawnSync(
    process.env.PYTHON ?? "python3",
    [new URL("../research/validate_figure_package.py", import.meta.url).pathname, figureRoot.pathname],
    { cwd: root.pathname, encoding: "utf8", env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" } },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.warnings, []);
});

test("pins the final R0.69W journal outputs by manifest SHA-256", async () => {
  const manifest = JSON.parse(await readFile(new URL("manifest.json", figureRoot), "utf8"));
  for (const record of manifest.figure.outputs) {
    const payload = await readFile(new URL(record.path, figureRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, record.sha256, record.path + " hash mismatch");
  }
});
