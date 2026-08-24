import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { readdir, readFile, stat } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "figures/r070o-rank-bridge/fig-r070o-rank-bridge/",
  root,
);
const python = fileURLToPath(new URL("tmp/r068b-venv/bin/python", root));

test("archives the corrected R0.70O formal rank-bridge figure", async () => {
  const files = (await readdir(figureRoot)).sort();
  const expectedFiles = [
    "caption.md",
    "contract.json",
    "data.csv",
    "figure-contract.md",
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "manifest.json",
    "plot.py",
    "qa-grayscale.png",
    "qa-original.png",
    "validation.json",
  ].sort();
  assert.deepEqual(files, expectedFiles);

  const [manifest, validation, contract, caption] = await Promise.all([
    readFile(new URL("manifest.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("validation.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("contract.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("caption.md", figureRoot), "utf8"),
  ]);

  assert.equal(manifest.figureId, "fig-r070o-rank-bridge");
  assert.equal(manifest.release, "R0.70O");
  assert.equal(manifest.status, "formal");
  assert.equal(
    manifest.git.commit,
    "1e52e81a1b869ee6bd283693e52ae4ad17025874",
  );
  assert.equal(manifest.git.dirty, false);
  assert.equal(manifest.computation.kind, "exact-audit");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.outputs.length, 5);
  assert.equal(manifest.outputs.length, 10);
  assert.equal(
    manifest.sourceData[0].sha256,
    "33c8361bdfed507526aa948fc6c74d964292c79015949ba2c748190bd4ba1134",
  );

  const source = await readFile(new URL(manifest.source, figureRoot));
  assert.equal(
    createHash("sha256").update(source).digest("hex"),
    manifest.sourceSha256,
  );
  for (const record of [...manifest.data, ...manifest.figure.outputs]) {
    const payload = await readFile(new URL(record.path, figureRoot));
    assert.equal(
      createHash("sha256").update(payload).digest("hex"),
      record.sha256,
      record.path,
    );
  }

  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 35);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.equal(validation.diagnostics.dataRows, 1070);
  assert.equal(validation.diagnostics.feasibleAreaExact, "1/12");
  assert.equal(validation.diagnostics.coerciveAreaExact, "289/4800");
  assert.equal(validation.diagnostics.nearLineAreaExact, "7/400");
  assert.equal(validation.diagnostics.nearPlaneAreaExact, "9/1600");
  assert.equal(validation.diagnostics.nearLineGapConstant, 0.2);
  assert.equal(validation.diagnostics.nearPlaneGapConstant, 0.3);
  assert.match(validation.visualQa.originalResolution, /passed/i);
  assert.match(validation.visualQa.grayscale, /passed/i);

  assert.equal(contract.data.rowCount, 1070);
  assert.match(contract.panels[2].takeaway, /horizontal threshold y=eta/i);
  assert.match(caption, /y\\le\\eta/);
  assert.match(caption, /1-2\\eta/);
  assert.match(caption, /\\eta-2\\delta/);
  assert.doesNotMatch(caption, /y\\le\\delta|9E\/10|7E\/20/);
  for (const name of ["figure.pdf", "figure.svg", "figure.png"]) {
    const info = await stat(new URL(name, figureRoot));
    assert.ok(info.size > 10_000, name);
  }
});

test("the R0.70O figure passes the strict package validator", () => {
  const run = spawnSync(
    python,
    [
      fileURLToPath(new URL("research/validate_figure_package.py", root)),
      fileURLToPath(figureRoot),
    ],
    {
      cwd: fileURLToPath(root),
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  assert.equal(run.status, 0, run.stderr || run.stdout);
  const result = JSON.parse(run.stdout);
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.warnings, []);
});
