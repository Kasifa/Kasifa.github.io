import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const packageRoot = new URL(
  "../figures/r069b-transverse-smallness/fig-r069b-transverse-smallness/",
  import.meta.url,
);
const publicRoot = new URL("../public/", import.meta.url);
const sha256 = (payload) =>
  createHash("sha256").update(payload).digest("hex");

test("archives the formal R0.69B transverse-smallness figure", async () => {
  const [manifestText, scales, decisions, crossings, svg, png, pdf] =
    await Promise.all([
      readFile(new URL("manifest.json", packageRoot), "utf8"),
      readFile(new URL("scale-separation.csv", packageRoot), "utf8"),
      readFile(new URL("decision-depth.csv", packageRoot), "utf8"),
      readFile(new URL("certified-crossings.csv", packageRoot), "utf8"),
      readFile(new URL("figure.svg", packageRoot), "utf8"),
      readFile(new URL("figure.png", packageRoot)),
      readFile(new URL("figure.pdf", packageRoot)),
    ]);
  const manifest = JSON.parse(manifestText);

  assert.equal(manifest.figureId, "fig-r069b-transverse-smallness");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.finalSizeInspected, true);
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 92);
  assert.equal(manifest.figure.outputs.at(-1).dpi, 600);
  assert.equal(manifest.git.sourceCommit.length, 40);
  assert.equal(manifest.git.certificateCommit.length, 40);
  assert.match(manifest.supportedClaim, /fixed critical ball/);
  assert.match(manifest.claimBoundary, /not a singularity/);
  assert.equal(scales.trim().split("\n").length, 52);
  assert.equal(decisions.trim().split("\n").length, 122);
  assert.match(crossings, /1e-6,72/);
  assert.match(svg, /Critical smallness excludes infinitesimal transverse singularity routes/);
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

test("publishes byte-exact mirrors of the R0.69B figure", async () => {
  for (const extension of ["svg", "png", "pdf"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL("figure." + extension, packageRoot)),
      readFile(
        new URL("figures/r0-69b-transverse-smallness." + extension, publicRoot),
      ),
    ]);
    assert.equal(sha256(published), sha256(archived));
  }
});
