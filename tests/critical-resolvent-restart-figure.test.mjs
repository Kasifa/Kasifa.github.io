import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const packageRoot = new URL(
  "../figures/r069e-resolvent-restart/fig-r069e-resolvent-restart/",
  import.meta.url,
);
const publicRoot = new URL("../public/", import.meta.url);
const sha256 = (payload) => createHash("sha256").update(payload).digest("hex");

test("archives the formal R0.69E resolvent-gluing figure", async () => {
  const [manifestText, surface, gluing, validationText, svg, png, pdf] =
    await Promise.all([
      readFile(new URL("manifest.json", packageRoot), "utf8"),
      readFile(new URL("two-block-surface.csv", packageRoot), "utf8"),
      readFile(new URL("equal-slab-gluing.csv", packageRoot), "utf8"),
      readFile(new URL("validation.json", packageRoot), "utf8"),
      readFile(new URL("figure.svg", packageRoot), "utf8"),
      readFile(new URL("figure.png", packageRoot)),
      readFile(new URL("figure.pdf", packageRoot)),
    ]);
  const manifest = JSON.parse(manifestText);
  const validation = JSON.parse(validationText);

  assert.equal(manifest.figureId, "fig-r069e-resolvent-restart");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.finalSizeInspected, true);
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 92);
  assert.equal(manifest.figure.outputs.at(-1).dpi, 600);
  assert.equal(manifest.git.sourceCommit.length, 40);
  assert.equal(manifest.git.certificateCommit.length, 40);
  assert.match(manifest.supportedClaim, /lower-triangular Volterra/i);
  assert.match(manifest.claimBoundary, /not a continuation/i);
  assert.equal(surface.trim().split("\n").length, 96 * 96 + 1);
  assert.equal(gluing.trim().split("\n").length, 4 * 64 + 1);
  assert.equal(validation.status, "passed");
  assert.ok(Object.values(validation.checks).every(Boolean));
  assert.match(svg, /positive-time Volterra gluing makes the regular-interval resolvent finite/i);
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");

  const outputs = new Map(
    manifest.figure.outputs.map((record) => [record.path, record]),
  );
  for (const [name, payload] of [
    ["figure.svg", Buffer.from(svg)],
    ["figure.png", png],
    ["figure.pdf", pdf],
  ]) {
    assert.equal(sha256(payload), outputs.get(name).sha256);
  }
});

test("publishes byte-exact mirrors of the R0.69E figure", async () => {
  for (const extension of ["svg", "png", "pdf"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL("figure." + extension, packageRoot)),
      readFile(
        new URL("figures/r0-69e-resolvent-restart." + extension, publicRoot),
      ),
    ]);
    assert.equal(sha256(published), sha256(archived));
  }
});
