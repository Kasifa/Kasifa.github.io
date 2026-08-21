import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { spawnSync } from "node:child_process";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "../figures/r069u-dyadic-saturation/fig-r069u-dyadic-saturation/",
  import.meta.url,
);

test("archives the formal R0.69U dyadic saturation figure", async () => {
  const [manifestText, metadataText, validationText, caption, contract, script] =
    await Promise.all([
      readFile(new URL("manifest.json", figureRoot), "utf8"),
      readFile(new URL("figure-data-metadata.json", figureRoot), "utf8"),
      readFile(new URL("validation.json", figureRoot), "utf8"),
      readFile(new URL("caption.md", figureRoot), "utf8"),
      readFile(new URL("figure-contract.md", figureRoot), "utf8"),
      readFile(new URL("plot.py", figureRoot), "utf8"),
    ]);
  const manifest = JSON.parse(manifestText);
  const metadata = JSON.parse(metadataText);
  const validation = JSON.parse(validationText);
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 82);
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(metadata.pairsPerRadius, 16 * 2 ** 18);
  assert.equal(metadata.analyticTwoAnnulusCondition, "R>40, hence every dyadic R>=64");
  assert.equal(validation.status, "passed");
  assert.equal(Object.keys(validation.checks).length, 13);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.match(caption, /display floor is not a measured bound/i);
  assert.match(caption, /full-space two-increment annular ratio is\s+unchanged/i);
  assert.match(contract, /No time-series or fitted-rate inference/i);
  assert.match(script, /svg\.hashsalt/);
});

test("the R0.69U figure passes the strict package validator", () => {
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

test("pins the final R0.69U journal outputs by SHA-256", async () => {
  const expected = new Map([
    ["figure.pdf", "9bab7a55847620484781c6df5c01183c1e977cd59318d86c63dc52003e530576"],
    ["figure.svg", "ecb39f0f60d7be75a7b872ec3a5755d62f03fe893167711bfbe1e9c59a823d20"],
    ["figure.png", "dffd7a1d0218dc9c58708c0359676467d4391fc2e4ed156d824e150496515f01"],
  ]);
  for (const [fileName, digest] of expected) {
    const payload = await readFile(new URL(fileName, figureRoot));
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, digest, fileName + " hash mismatch");
  }
});
