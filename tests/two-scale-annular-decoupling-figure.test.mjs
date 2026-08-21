import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "../figures/r069v-two-scale/fig-r069v-two-scale/",
  import.meta.url,
);

test("archives the formal R0.69V two-scale journal figure", async () => {
  const [manifest, metadata, validation, caption, contract] = await Promise.all([
    readFile(new URL("manifest.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("figure-data-metadata.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("validation.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("caption.md", figureRoot), "utf8"),
    readFile(new URL("figure-contract.md", figureRoot), "utf8"),
  ]);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 86);
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(metadata.primaryPointPairs, 167772160);
  assert.equal(metadata.fixedPointPairs, 83886080);
  assert.equal(metadata.rootGapPointPairs, 41943040);
  assert.equal(metadata.candidateRatio, 0.9635537051236769);
  assert.ok(metadata.fixedJ0Mean / metadata.fixedJ0StandardError < -50);
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 14);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.match(caption, /randomized diagnostic/i);
  assert.match(contract, /not rigorous\s+interval enclosures/i);
});

test("the R0.69V figure passes the strict package validator", () => {
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
  const result = JSON.parse(run.stdout);
  assert.deepEqual(result.errors, []);
  assert.deepEqual(result.warnings, []);
});

test("pins the final R0.69V journal outputs by SHA-256", async () => {
  const expected = new Map([
    ["figure.pdf", "0d0fef428ee0c25d2cd456f697286f2df20574ee44c697f0713f93595a65af22"],
    ["figure.svg", "2acb59edde24747b938f18c253c792947a28748fa75c8545082300ac89cbac5a"],
    ["figure.png", "43fd17608b180d4fc975a9fb2de3df3565fed6c8fd6398107f2ac270abb87eda"],
  ]);
  for (const [fileName, digest] of expected) {
    const payload = await readFile(new URL(fileName, figureRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, digest, fileName + " hash mismatch");
  }
});

test("locks every R0.69V certificate payload by SHA-256", async () => {
  for (const directory of [
    "r069v",
    "r069v-polynomial-qmc",
    "r069v-zonepair-qmc",
    "r069v-zonepair-polynomial-qmc",
  ]) {
    const certificateRoot = new URL(
      "../research/certificates/" + directory + "/",
      import.meta.url,
    );
    const sums = await readFile(new URL("SHA256SUMS", certificateRoot), "utf8");
    for (const line of sums.trim().split("\n")) {
      const match = line.match(/^([0-9a-f]{64})\s+(.+)$/);
      assert.ok(match, "malformed SHA256SUMS line in " + directory + ": " + line);
      const payload = await readFile(new URL(match[2], certificateRoot));
      const actual = createHash("sha256").update(payload).digest("hex");
      assert.equal(actual, match[1], directory + "/" + match[2] + " hash mismatch");
    }
  }
});
