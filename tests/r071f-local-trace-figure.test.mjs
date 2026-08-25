import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "figures/r071f-local-trace/fig-r071f-local-trace/",
  root,
);

test("archives the formal 178 by 104 mm R0.71F local-trace figure", async () => {
  const [
    manifest,
    validation,
    independent,
    metadata,
    data,
    contract,
    caption,
    environment,
  ] = await Promise.all([
    readFile(new URL("manifest.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("validation.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("independent-validation.json", figureRoot), "utf8").then(
      JSON.parse,
    ),
    readFile(new URL("figure-data-metadata.json", figureRoot), "utf8").then(
      JSON.parse,
    ),
    readFile(new URL("data.csv", figureRoot), "utf8"),
    readFile(new URL("figure-contract.md", figureRoot), "utf8"),
    readFile(new URL("caption.md", figureRoot), "utf8"),
    readFile(new URL("environment.txt", figureRoot), "utf8"),
  ]);

  assert.equal(manifest.release, "R0.71F");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figureId, "fig-r071f-local-trace");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 104);
  for (const extension of ["pdf", "svg", "png"]) {
    assert.ok(
      manifest.figure.outputs.some((entry) => entry.path === `figure.${extension}`),
      extension,
    );
  }
  const png = manifest.figure.outputs.find((entry) => entry.path === "figure.png");
  assert.equal(png.dpi, 600);
  assert.match(png.pixels, /^420[45] by 245[67]$/);
  assert.equal(manifest.compute.dgx, "not used");
  assert.equal(manifest.compute.gpu, "not used");
  assert.equal(manifest.qa.status, "passed");
  assert.match(manifest.claimBoundary, /no DNS/i);
  assert.match(manifest.claimBoundary, /no[\s\S]*critical-trace rejection/i);

  assert.equal(validation.release, "R0.71F");
  assert.equal(validation.status, "pass");
  assert.equal(Object.keys(validation.checks).length, 22);
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.equal(independent.release, "R0.71F-independent-figure");
  assert.equal(independent.status, "pass");
  assert.equal(Object.keys(independent.checks).length, 27);
  assert.ok(Object.values(independent.checks).every(Boolean));

  assert.equal(metadata.release, "R0.71F");
  assert.equal(metadata.rows, 526);
  assert.equal(metadata.dns, false);
  assert.equal(metadata.pdeTimeStepping, false);
  assert.equal(metadata.randomSeed, null);
  assert.equal(data.trim().split("\n").length - 1, 526);
  assert.match(contract, /exactly 178 by 104 millimetres/i);
  assert.match(contract, /600 dpi/i);
  assert.ok(caption.includes("\\(2/(1-e^{-2\\theta})\\)"));
  assert.match(caption, /not DNS/i);
  assert.ok(caption.includes("reject a critical \\(Cr^{-2}\\) estimate"));
  assert.match(environment, /DGX: not used/);
  assert.match(environment, /GPU: not used/);
});

test("keeps the three archived R0.71F figure formats valid", async () => {
  const [pdf, svg, png] = await Promise.all([
    readFile(new URL("figure.pdf", figureRoot)),
    readFile(new URL("figure.svg", figureRoot), "utf8"),
    readFile(new URL("figure.png", figureRoot)),
  ]);

  assert.equal(pdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.match(svg, /<svg/);
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.ok(pdf.length > 10_000);
  assert.ok(svg.length > 10_000);
  assert.ok(png.length > 100_000);
});

test("keeps every archived R0.71F figure payload SHA-256 exact", async () => {
  const sums = await readFile(new URL("SHA256SUMS", figureRoot), "utf8");
  const lines = sums.trim().split("\n");
  assert.equal(lines.length, 18);
  for (const required of [
    "figure.pdf",
    "figure.svg",
    "figure.png",
    "validation.json",
    "independent-validation.json",
    "manifest.json",
  ]) {
    assert.ok(lines.some((line) => line.endsWith(`  ${required}`)), required);
  }
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, line);
    const payload = await readFile(new URL(match[2], figureRoot));
    assert.equal(createHash("sha256").update(payload).digest("hex"), match[1]);
  }
});

test("publishes byte-exact web copies of all R0.71F figure formats", async () => {
  for (const extension of ["svg", "pdf", "png"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL(`figure.${extension}`, figureRoot)),
      readFile(new URL(`public/figures/r0-71f-local-trace.${extension}`, root)),
    ]);
    assert.deepEqual(published, archived, extension);
  }
});
