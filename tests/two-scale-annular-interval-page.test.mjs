import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const figureRoot = new URL("../figures/r069w-interval-obstruction/fig-r069w-interval-obstruction/", import.meta.url);

test("publishes R0.69W as a rigorous static obstruction with an explicit boundary", async () => {
  const [review, note, notePdf] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69w.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69w.pdf", publicRoot)),
  ]);
  assert.match(review, /id="r069w"/);
  assert.match(review, /href="\/notes\/r0-69w\.html"/);
  assert.match(review, /href="\/notes\/r0-69w\.pdf"/);
  assert.match(note, /href="\/notes\/r0-69w\.pdf"/);
  assert.ok(note.includes("\\mathcal A_0(u_a)=a\\,q(a)"));
  assert.ok(note.includes("\\Delta=c_2^2-4c_1c_3"));
  assert.match(note, /浮点求积节点：0/);
  assert.match(note, /下一阶段已暂停/);
  assert.match(note, /没有证明全局正则性或构造有限时奇性/);
  assert.doesNotMatch(note, /时间为 \\texttt/);
  assert.doesNotMatch(note, /__[A-Z0-9_]+__/);
  assert.equal(notePdf.subarray(0, 4).toString(), "%PDF");
  assert.ok(notePdf.length > 100_000);
});

test("keeps the R0.69W targets, sources, and public figure mirror complete", async () => {
  const note = await readFile(new URL("notes/r0-69w.html", publicRoot), "utf8");
  const ids = new Set([...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]));
  const targets = [...note.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.ok(targets.length >= 11);
  for (const target of targets) assert.ok(ids.has(target), "missing #" + target);
  for (const source of [
    "research/certificates/r069w",
    "research/two_scale_annular_interval_note.md",
    "figures/r069w-interval-obstruction/fig-r069w-interval-obstruction",
    "https://www.claymath.org/millennium/navier-stokes-equation/",
  ]) assert.ok(note.includes(source), source);
  for (const extension of ["pdf", "svg", "png"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL("figure." + extension, figureRoot)),
      readFile(new URL("figures/r0-69w-interval-obstruction." + extension, publicRoot)),
    ]);
    assert.deepEqual(published, archived, extension);
  }
});

test("lists the R0.69W translations in the bilingual build", async () => {
  const [translations, generated] = await Promise.all([
    readFile(new URL("translations/en.json", root), "utf8"),
    readFile(new URL("i18n-en.js", publicRoot), "utf8"),
  ]);
  for (const phrase of [
    "R0.69W | The entire two-scale amplitude family at scale ratio four is rigorously excluded",
    "Research note R0.69W · A rigorous interval obstruction at finite two-scale separation",
    "The value is to upgrade the randomized finite-separation obstruction into an auditable theorem",
  ]) {
    assert.ok(translations.includes(phrase), phrase);
    assert.ok(generated.includes(phrase), phrase);
  }
});
