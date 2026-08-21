import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69M with the criterion comparison and claim boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69m.html", publicRoot), "utf8"),
  ]);
  assert.match(home, /id="r069m"/);
  assert.match(home, /href="\/notes\/r0-69m\.html"/);
  assert.match(home, /综述 v0\.78 · 2026-08-21/);
  assert.match(home, /i18n-en\.js\?v=0\.78/);
  assert.match(home, /下一步 R0\.69N/);
  assert.match(note, /B_\\infty\(r\)/);
  assert.match(note, /=\\frac1\{120\}\\mathfrak M_2\(r\)/);
  assert.match(note, /\\ge2\^\{4k-1\}\\longrightarrow\\infty/);
  assert.match(note, /a_N=N\^\{-1\/2\}/);
  assert.match(note, /N_1\\ge cN/);
  assert.match(note, /=cN\^\{1\/2\}/);
  assert.match(note, /3\/3\+2\/3=5\/3&lt;2/);
  assert.match(note, /当前形式不是新的/);
  assert.match(note, /没有解决千禧年问题/);
});

test("keeps every R0.69M navigation target and source asset resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69m.html", publicRoot), "utf8");
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
    "https://arxiv.org/abs/math/0607114",
    "https://arxiv.org/abs/math/0607537",
    "https://www.mathnet.ru/eng/rm609",
    "https://arxiv.org/abs/1805.04841",
  ]) {
    assert.ok(note.includes(source), source);
  }
  for (const asset of [
    "figures/r0-69m-criterion.pdf",
    "figures/r0-69m-criterion.svg",
    "figures/r0-69m-criterion.png",
  ]) {
    const payload = await readFile(new URL(asset, publicRoot));
    assert.ok(payload.byteLength > 1000, asset);
  }
});

test("lists the R0.69M translations in the bilingual build", async () => {
  const translations = await readFile(
    new URL("../translations/en.json", import.meta.url),
    "utf8",
  );
  assert.match(
    translations,
    /R0\.69M \| The far tail is controlled, but the near norm is still too strong/,
  );
  const generated = await readFile(new URL("i18n-en.js", publicRoot), "utf8");
  assert.match(
    generated,
    /R0\.69M \| The far tail is controlled, but the near norm is still too strong/,
  );
});
