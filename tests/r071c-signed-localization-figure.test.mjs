import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const figureRoot = new URL(
  "figures/r071c-signed-localization/fig-r071c-viscous-sign-creation/",
  root,
);

test("archives the formal R0.71C viscous sign-creation figure contract", async () => {
  const [manifest, validation, independent, data, contract, caption, environment] =
    await Promise.all([
      readFile(new URL("manifest.json", figureRoot), "utf8").then(JSON.parse),
      readFile(new URL("validation.json", figureRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-validation.json", figureRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("data.csv", figureRoot), "utf8"),
      readFile(new URL("figure-contract.md", figureRoot), "utf8"),
      readFile(new URL("caption.md", figureRoot), "utf8"),
      readFile(new URL("environment.txt", figureRoot), "utf8"),
    ]);

  assert.equal(manifest.release, "R0.71C");
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 92);
  const png = manifest.figure.outputs.find((entry) => entry.path === "figure.png");
  assert.equal(png.dpi, 600);
  assert.equal(png.pixels, "4204 by 2173");
  assert.equal(manifest.compute.dgx, "not used");
  assert.equal(manifest.compute.gpu, "not used");
  assert.match(manifest.claimBoundary, /does not prove a Navier-Stokes/);
  assert.equal(Object.keys(validation.checks).length, 32);
  assert.ok(Object.values(validation.checks).every((value) => value === true));
  assert.equal(Object.keys(independent.checks).length, 10);
  assert.ok(Object.values(independent.checks).every((value) => value === true));
  assert.equal(data.trim().split("\n").length - 1, 252);
  assert.match(contract, /E_.*fine.*E_.*root.*delta/s);
  assert.match(caption, /exact\s+Stokes witness/);
  assert.match(caption, /not a Navier--Stokes time-integrability estimate/);
  assert.match(environment, /DGX: not used/);
});

test("keeps every archived R0.71C figure payload SHA-256 exact", async () => {
  const sums = await readFile(new URL("SHA256SUMS", figureRoot), "utf8");
  const lines = sums.trim().split("\n");
  assert.ok(lines.length >= 18);
  for (const line of lines) {
    const match = line.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, line);
    const payload = await readFile(new URL(match[2], figureRoot));
    assert.equal(createHash("sha256").update(payload).digest("hex"), match[1]);
  }
});

test("publishes byte-exact web copies of every formal R0.71C figure format", async () => {
  for (const extension of ["svg", "pdf", "png"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL("figure." + extension, figureRoot)),
      readFile(
        new URL(
          "public/figures/r0-71c-viscous-sign-creation." + extension,
          root,
        ),
      ),
    ]);
    assert.deepEqual(published, archived, extension);
  }
});
