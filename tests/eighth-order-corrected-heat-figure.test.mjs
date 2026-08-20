import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL(
  "../figures/r068b2fgh-corrected-heat/fig-r068b2fgh-corrected-heat/",
  import.meta.url,
);

test("archives the formal R0.68B-2f/g/h corrected-heat figure", async () => {
  const [manifestText, budget, svg, png, pdf] = await Promise.all([
    readFile(new URL("manifest.json", root), "utf8"),
    readFile(new URL("sign-budget.csv", root), "utf8"),
    readFile(new URL("figure.svg", root), "utf8"),
    readFile(new URL("figure.png", root)),
    readFile(new URL("figure.pdf", root)),
  ]);
  const manifest = JSON.parse(manifestText);
  assert.equal(manifest.figureId, "fig-r068b2fgh-corrected-heat");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.qa.finalSizeInspected, true);
  assert.equal(manifest.qa.grayscaleInspected, true);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 105);
  assert.equal(manifest.figure.outputs.at(-1).dpi, 600);
  assert.equal(manifest.compute.formalDefectThreads, 18);
  assert.match(manifest.supportedClaim, /strictly negative upper endpoint/);
  assert.match(manifest.claimBoundary, /all Picard orders/);
  assert.match(budget, /heat magnitude,1\.49238243184751290E-8/);
  assert.match(budget, /strict margin,2\.87321129703704757E-9/);
  assert.match(svg, /Certification chain for one fixed eighth-order/);
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");

  const outputs = new Map(manifest.figure.outputs.map((record) => [record.path, record]));
  for (const [name, payload] of [["figure.svg", Buffer.from(svg)], ["figure.png", png], ["figure.pdf", pdf]]) {
    const actual = createHash("sha256").update(payload).digest("hex");
    assert.equal(actual, outputs.get(name).sha256);
  }
});
