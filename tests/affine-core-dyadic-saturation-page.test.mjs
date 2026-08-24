import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const figureRoot = new URL(
  "figures/r069u-dyadic-saturation/fig-r069u-dyadic-saturation/",
  root,
);

test("publishes R0.69U with exact core saturation and the full-space boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69u.html", publicRoot), "utf8"),
  ]);
  assert.match(home, /id="r069u"/);
  assert.match(home, /href="\/notes\/r0-69u\.html"/);
  assert.match(home, /综述 v0\.84 · 2026-08-25/);
  const card = home.slice(home.indexOf('id="r069u"'), home.indexOf('id="r069v"'));
  assert.match(card, /下一步 R0\.69V/);
  assert.ok(note.includes("\\Gamma_{\\rm core}(R)"));
  assert.ok(note.includes("\\frac{50}{21}"));
  assert.ok(note.includes("I_+\\ge5/42&gt;0"));
  assert.ok(note.includes("\\mathcal A_{m+k}(u_R)=R^3\\mathcal A_k(u_1)"));
  assert.match(note, /29,360,128/);
  assert.match(note, /不是全空间双增量比值的饱和定理/);
  assert.match(note, /没有解决千禧年问题/);
});

test("keeps every R0.69U target and published figure byte-exact", async () => {
  const note = await readFile(new URL("notes/r0-69u.html", publicRoot), "utf8");
  const ids = new Set([...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]));
  const targets = [...note.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.ok(targets.length >= 14);
  for (const target of targets) assert.ok(ids.has(target), "missing #" + target);
  for (const source of [
    "https://doi.org/10.1002/cpa.3160460604",
    "https://arxiv.org/abs/2606.27560",
    "https://www.claymath.org/millennium/navier-stokes-equation/",
  ]) assert.ok(note.includes(source), source);
  for (const extension of ["pdf", "svg", "png"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL("figure." + extension, figureRoot)),
      readFile(new URL("figures/r0-69u-dyadic-saturation." + extension, publicRoot)),
    ]);
    assert.deepEqual(published, archived, extension);
  }
});

test("lists the R0.69U translations in the bilingual build", async () => {
  const [translations, generated] = await Promise.all([
    readFile(new URL("translations/en.json", root), "utf8"),
    readFile(new URL("i18n-en.js", publicRoot), "utf8"),
  ]);
  for (const phrase of [
    "R0.69U | The fixed-core carrier eventually saturates exactly",
    "Research note R0.69U · dyadic affine-core saturation and the critical dilation obstruction",
  ]) {
    assert.ok(translations.includes(phrase), phrase);
    assert.ok(generated.includes(phrase), phrase);
  }
});
