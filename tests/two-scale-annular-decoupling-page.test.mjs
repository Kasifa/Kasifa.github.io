import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const figureRoot = new URL(
  "figures/r069v-two-scale/fig-r069v-two-scale/",
  root,
);

test("publishes R0.69V with the exact theorem and randomized boundary separated", async () => {
  const [review, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69v.html", publicRoot), "utf8"),
  ]);
  assert.match(review, /id="r069v"/);
  assert.match(review, /href="\/notes\/r0-69v\.html"/);
  assert.match(review, /综述 v0\.82 · 2026-08-24/);
  const card = review.slice(review.indexOf('id="r069v"'), review.indexOf('id="r069w"'));
  assert.match(card, /下一步 R0\.69W/);
  assert.ok(note.includes("\\sup_{0\\le a\\le1}"));
  assert.ok(note.includes("\\Gamma_{\\rm ann}(u_{\\varepsilon,a})-\\Gamma_q"));
  assert.ok(note.includes("\\varepsilon^3ab^2C_q"));
  assert.ok(note.includes("不存在 \\(a^2b\\) 项"));
  assert.ok(note.includes("\\|X_{\\varepsilon,a}\\|_{\\ell^1}"));
  assert.match(note, /293,601,280/);
  assert.match(note, /0\.9635537051/);
  assert.match(note, /不是同时置信带，更不是严格区间证明/);
  assert.match(note, /没有证明全局正则性、有限时奇性或解决千禧年问题/);
});

test("keeps every R0.69V target, source, and published figure resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69v.html", publicRoot), "utf8");
  const ids = new Set([...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]));
  const targets = [...note.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.ok(targets.length >= 14);
  for (const target of targets) assert.ok(ids.has(target), "missing #" + target);
  for (const source of [
    "https://doi.org/10.1002/cpa.3160460604",
    "https://arxiv.org/abs/2606.27560",
    "https://www.claymath.org/millennium/navier-stokes-equation/",
    "research/certificates/r069v-polynomial-qmc",
    "research/certificates/r069v-zonepair-polynomial-qmc",
  ]) assert.ok(note.includes(source), source);
  for (const extension of ["pdf", "svg", "png"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL("figure." + extension, figureRoot)),
      readFile(new URL("figures/r0-69v-two-scale." + extension, publicRoot)),
    ]);
    assert.deepEqual(published, archived, extension);
  }
});

test("lists the R0.69V translations in the bilingual build", async () => {
  const [translations, generated] = await Promise.all([
    readFile(new URL("translations/en.json", root), "utf8"),
    readFile(new URL("i18n-en.js", publicRoot), "utf8"),
  ]);
  for (const phrase of [
    "R0.69V | Two-scale deformation returns to baseline at infinite separation",
    "Research note R0.69V · Exact decoupling of two-scale affine annuli",
    "The next step is not a broader scan, but rigorous enclosure",
  ]) {
    assert.ok(translations.includes(phrase), phrase);
    assert.ok(generated.includes(phrase), phrase);
  }
});
