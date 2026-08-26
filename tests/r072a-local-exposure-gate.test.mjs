import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile, stat } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const certificateRoot = resolve(root, "research/certificates/r072a");
const figureRoot = resolve(
  root,
  "figures/r072a-local-bessel/fig-r072a-local-bessel",
);
const publicRoot = resolve(root, "public");

const readJson = async (path) =>
  JSON.parse(await readFile(path, "utf8"));
const sha256 = async (path) =>
  createHash("sha256").update(await readFile(path)).digest("hex");

test("certifies the R0.72A local-exposure phase boundary and selected Bessel mass", async () => {
  const [producer, independent, figureResults] = await Promise.all([
    readJson(resolve(certificateRoot, "result.json")),
    readJson(resolve(certificateRoot, "independent-result.json")),
    readJson(resolve(figureRoot, "results.json")),
  ]);

  assert.equal(producer.allPassed, true);
  assert.equal(independent.allPassed, true);
  assert.ok(producer.checks.every((row) => row.passed));
  assert.ok(independent.checks.every((row) => row.passed));
  assert.ok(
    producer.checks.some((row) => row.name === "selected_root_brackets"),
  );
  assert.ok(
    !producer.checks.some((row) => row.name === "all_root_brackets"),
  );

  assert.equal(figureResults.phaseBoundary.fixedLength, 6 / 7);
  assert.equal(figureResults.phaseBoundary.fastShrinking, 3 / 2);
  assert.equal(
    figureResults.phaseBoundary.formula,
    "min(3/2,(6+3 beta)/7)",
  );
  assert.ok(
    Math.abs(
      figureResults.bessel.leadingCoefficient - 8 / Math.PI ** 2,
    ) < 2e-16,
  );

  const producerMass = producer.finiteLattice.map(
    (row) => row.exactSelectedMass,
  );
  const producerLayers = producer.finiteLattice.map(
    (row) => row.layerLength,
  );
  assert.ok(producerMass.every((value, index) =>
    index === 0 || value > producerMass[index - 1]));
  assert.ok(producerLayers.every((value, index) =>
    index === 0 || value < producerLayers[index - 1]));
  assert.ok(
    Math.max(...figureResults.crossAudit.map((row) => row.massDifference)) <
      4e-10,
  );
  assert.ok(
    Math.max(
      ...figureResults.crossAudit.map((row) => row.maximumRootDifference),
    ) < 4e-9,
  );
});

test("verifies the R0.72A certificate checksum ledger", async () => {
  const ledger = await readFile(resolve(certificateRoot, "SHA256SUMS"), "utf8");
  const rows = ledger.trim().split("\n");
  assert.equal(rows.length, 10);
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  (.+)$/);
    assert.ok(match, row);
    assert.equal(
      await sha256(resolve(certificateRoot, match[2])),
      match[1],
      match[2],
    );
  }
});

test("archives a formal R0.72A journal figure with physical x-coordinate QA", async () => {
  const [manifest, validation] = await Promise.all([
    readJson(resolve(figureRoot, "manifest.json")),
    readJson(resolve(figureRoot, "validation.json")),
  ]);
  assert.equal(manifest.status, "formal");
  assert.match(manifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(validation.status, "passed");
  assert.equal(validation.checkCount, 16);
  assert.ok(validation.checks.every((row) => row.passed));
  assert.equal(
    validation.checks.find(
      (row) => row.name === "physical_root_displacement",
    )?.value,
    0,
  );
  assert.match(manifest.claimBoundary, /not divided by Omega\^2/);
  assert.match(manifest.claimBoundary, /selected positive target roots/);

  for (const asset of manifest.assets) {
    const path = resolve(figureRoot, asset.path);
    assert.equal((await stat(path)).size, asset.bytes, asset.path);
    assert.equal(await sha256(path), asset.sha256, asset.path);
  }
  assert.ok((await stat(resolve(figureRoot, "figure.png"))).size > 400_000);
  assert.ok((await stat(resolve(figureRoot, "figure.svg"))).size > 90_000);
  assert.ok((await stat(resolve(figureRoot, "figure.pdf"))).size > 40_000);
});

test("publishes the R0.72A note, full post-R0.60 recap, and literature boundary", async () => {
  const [home, literature, note, recap] = await Promise.all([
    readFile(resolve(publicRoot, "research-review.html"), "utf8"),
    readFile(resolve(publicRoot, "literature-review.html"), "utf8"),
    readFile(resolve(publicRoot, "notes/r0-72a.html"), "utf8"),
    readFile(resolve(publicRoot, "recap-r0-61-r0-72a.html"), "utf8"),
  ]);

  assert.match(home, /<strong>151<\/strong>公开研究笔记/);
  assert.match(home, /展开 61 篇公开笔记/);
  assert.match(home, /NEXT · R0\.72B/);
  assert.equal((home.match(/href="\/notes\/r0-72a\.html"/g) ?? []).length, 2);
  assert.match(recap, /R0\.61–R0\.72A 的 91 节公开笔记/);
  assert.match(recap, /十八个研究阶段/);
  assert.match(recap, /R0\.70A–R0\.72A 完成版本/);
  assert.match(literature, /开放接口 · R0\.72B/);
  assert.match(literature, /10\.4007\/annals\.2008\.168\.643/);
  assert.match(literature, /10\.1007\/s00205-017-1099-y/);
  assert.match(literature, /10\.1112\/jlms\.12782/);

  assert.match(note, /G_R\^\{\\rm sel\}/);
  assert.match(note, /G_\{R,\\rm all\}\^\{\\rm ex\}/);
  assert.match(note, /\\ge1\+G_R\^\{\\rm sel\}/);
  assert.match(note, /physical root displacement/);
  assert.match(note, /相图给的是 upper bound 仍趋零的充分区域/);
  assert.match(note, /不是一般三维正则性定理/);
  assert.match(note, /\/i18n-en\.js\?v=1\.14/);
  assert.match(recap, /\/i18n-en\.js\?v=1\.14/);

  const forbidden = /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/;
  for (const [name, html] of Object.entries({ home, literature, note, recap })) {
    assert.doesNotMatch(html, forbidden, name);
  }

  for (const relative of [
    "notes/r0-72a.pdf",
    "recap-r0-61-r0-72a.pdf",
    "figures/r0-72a-local-bessel.pdf",
    "figures/r0-72a-local-bessel.png",
    "figures/r0-72a-local-bessel.svg",
  ]) {
    assert.ok((await stat(resolve(publicRoot, relative))).size > 10_000, relative);
  }
});
