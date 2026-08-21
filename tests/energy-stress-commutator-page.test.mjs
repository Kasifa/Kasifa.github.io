import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69N with the energy commutator and strict claim boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69n.html", publicRoot), "utf8"),
  ]);
  assert.match(home, /id="r069n"/);
  assert.match(home, /href="\/notes\/r0-69n\.html"/);
  assert.match(home, /综述 v0\.74 · 2026-08-21/);
  assert.match(home, /i18n-en\.js\?v=0\.74/);
  assert.match(home, /下一步 R0\.69O/);
  assert.match(note, /\\mathcal T\(S\[v\]\)=0/);
  assert.match(note, /X_q\\bigl\(D_A\^\{1\/2\}\+\\sigma_A\+\\mu_A\\bigr\)/);
  assert.match(note, /\\mu_v\\sigma_v\^3/);
  assert.match(note, /s\(3\/s\)=3/);
  assert.match(note, /s=3\/2/);
  assert.match(note, /\\int\\sigma_A\^2\\,dt=1/);
  assert.match(note, /\\int\\mu_A\\sigma_A\^3\\,dt=A\\longrightarrow\\infty/);
  assert.match(note, /尚未得到正则性闭合/);
  assert.match(note, /没有解决千禧年问题/);
});

test("keeps every R0.69N navigation target and source asset resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69n.html", publicRoot), "utf8");
  const ids = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const localTargets = [...note.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(localTargets.length >= 12);
  for (const target of localTargets) {
    assert.ok(ids.has(target), "missing #" + target);
  }
  for (const source of [
    "https://numdam.org/item/SEDP_1989-1990____A16_0/",
    "https://doi.org/10.1007/s002090000130",
    "https://arxiv.org/abs/2106.11852",
    "https://arxiv.org/abs/math/0607114",
  ]) {
    assert.ok(note.includes(source), source);
  }
  for (const asset of [
    "figures/r0-69n-energy-commutator.pdf",
    "figures/r0-69n-energy-commutator.svg",
    "figures/r0-69n-energy-commutator.png",
  ]) {
    const payload = await readFile(new URL(asset, publicRoot));
    assert.ok(payload.byteLength > 1000, asset);
  }
});

test("lists the R0.69N translations in the bilingual build", async () => {
  const translations = await readFile(
    new URL("../translations/en.json", import.meta.url),
    "utf8",
  );
  assert.match(
    translations,
    /R0\.69N \| The spatial commutator closes, but the time exponent remains one step short/,
  );
  const generated = await readFile(new URL("i18n-en.js", publicRoot), "utf8");
  assert.match(
    generated,
    /R0\.69N \| The spatial commutator closes, but the time exponent remains one step short/,
  );
});
