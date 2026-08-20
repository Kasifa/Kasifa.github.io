import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const packageRoot = new URL(
  "../figures/r069a-full-picard-closure/fig-r069a-full-picard-closure/",
  import.meta.url,
);
const publicRoot = new URL("../public/", import.meta.url);

const sha256 = (payload) =>
  createHash("sha256").update(payload).digest("hex");

test("archives the formal R0.69A complete-Picard figure", async () => {
  const [manifestText, interval, rates, envelopes, svg, png, pdf] =
    await Promise.all([
      readFile(new URL("manifest.json", packageRoot), "utf8"),
      readFile(new URL("limit-interval.csv", packageRoot), "utf8"),
      readFile(new URL("decay-rates.csv", packageRoot), "utf8"),
      readFile(new URL("rate-envelopes.csv", packageRoot), "utf8"),
      readFile(new URL("figure.svg", packageRoot), "utf8"),
      readFile(new URL("figure.png", packageRoot)),
      readFile(new URL("figure.pdf", packageRoot)),
    ]);
  const manifest = JSON.parse(manifestText);

  assert.equal(manifest.figureId, "fig-r069a-full-picard-closure");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.finalSizeInspected, true);
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 103);
  assert.equal(manifest.figure.outputs.at(-1).dpi, 600);
  assert.equal(manifest.git.sourceCommit.length, 40);
  assert.equal(manifest.git.certificateCommit.length, 40);
  assert.equal(manifest.computation.kind, "exact-audit plus high-precision presentation sampling");
  assert.match(manifest.supportedClaim, /strictly greater-than-one interval/);
  assert.match(manifest.claimBoundary, /globally smooth invariant-shear class/);
  assert.match(interval, /2\.5937453534608412212067659494829142669246594802315e-08/);
  assert.match(interval, /1\.0000000261408362683195721926534985686005932565849/);
  assert.match(rates, /sixth/);
  assert.match(rates, /eighth/);
  assert.match(rates, /orders at least ten/);
  assert.equal(envelopes.trim().split("\n").length, 22);
  assert.match(svg, /Every Picard order closes on one periodic target coefficient/);
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

test("publishes byte-exact mirrors of the R0.69A figure", async () => {
  for (const extension of ["svg", "png", "pdf"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL("figure." + extension, packageRoot)),
      readFile(
        new URL("figures/r0-69a-full-picard-closure." + extension, publicRoot),
      ),
    ]);
    assert.equal(sha256(published), sha256(archived));
  }
});
