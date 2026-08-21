import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const figureRoot = new URL(
  "figures/r069t-affine-annuli/fig-r069t-affine-annuli/",
  root,
);

test("publishes R0.69T with the exact annular theorem and numerical boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69t.html", publicRoot), "utf8"),
  ]);
  assert.match(home, /id="r069t"/);
  assert.match(home, /href="\/notes\/r0-69t\.html"/);
  assert.match(home, /综述 v0\.79 · 2026-08-21/);
  assert.match(home, /下一步 R0\.69U/);
  assert.ok(note.includes("\\sum_{j\\in\\mathbb Z}\\mathcal A_j(u)"));
  assert.ok(note.includes("e_{xy}\\cdot\\delta\\omega"));
  assert.ok(note.includes("\\frac{8\\pi}{3\\sqrt6}"));
  assert.match(note, /67,108,864/);
  assert.match(note, /0\.99647808/);
  assert.match(note, /不是区间包络/);
  assert.match(note, /没有解决千禧年问题/);
});

test("keeps every R0.69T navigation target and source asset resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69t.html", publicRoot), "utf8");
  const ids = new Set([...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]));
  const targets = [...note.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.ok(targets.length >= 14);
  for (const target of targets) assert.ok(ids.has(target), "missing #" + target);
  for (const source of [
    "https://doi.org/10.1002/cpa.3160460604",
    "https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.qmc.Sobol.html",
    "https://www.claymath.org/millennium/navier-stokes-equation/",
  ]) assert.ok(note.includes(source), source);
  for (const extension of ["pdf", "svg", "png"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL("figure." + extension, figureRoot)),
      readFile(new URL("figures/r0-69t-affine-annuli." + extension, publicRoot)),
    ]);
    assert.deepEqual(published, archived, extension);
  }
});

test("lists the R0.69T translations in the bilingual build", async () => {
  const [translations, generated] = await Promise.all([
    readFile(new URL("translations/en.json", root), "utf8"),
    readFile(new URL("i18n-en.js", publicRoot), "utf8"),
  ]);
  for (const phrase of [
    "R0.69T | Two vorticity increments give an exact annular decomposition",
    "Research note R0.69T · physical-space annuli and the affine-core boundary carrier",
  ]) {
    assert.match(translations, new RegExp(phrase.replaceAll(".", "\\.")));
    assert.match(generated, new RegExp(phrase.replaceAll(".", "\\.")));
  }
});
