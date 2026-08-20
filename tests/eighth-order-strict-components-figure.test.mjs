import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL(
  "../figures/r068b2de-strict-components/fig-r068b2de-strict-components/",
  import.meta.url,
);

test("archives the formal strict-component figure with its evidence boundary", async () => {
  const [manifestText, svg, png, pdf] = await Promise.all([
    readFile(new URL("manifest.json", root), "utf8"),
    readFile(new URL("figure.svg", root), "utf8"),
    readFile(new URL("figure.png", root)),
    readFile(new URL("figure.pdf", root)),
  ]);
  const manifest = JSON.parse(manifestText);
  assert.equal(manifest.figureId, "fig-r068b2de-strict-components");
  assert.equal(manifest.qa.status, "passed");
  assert.match(manifest.supportedClaim, /4,368/);
  assert.match(manifest.supportedClaim, /1,792/);
  assert.match(manifest.claimBoundary, /not a final heat-sign theorem/);
  assert.match(svg, /Strict derivative and dominant-mass components/);
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});
