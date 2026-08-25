import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const homeUrl = new URL("../public/research-review.html", import.meta.url);
const noteUrl = new URL("../public/notes/r0-69i.html", import.meta.url);

test("publishes R0.69I with the exact localization obstruction", async () => {
  const [home, note] = await Promise.all([
    readFile(homeUrl, "utf8"),
    readFile(noteUrl, "utf8"),
  ]);

  assert.match(home, /id="r069i"/);
  assert.match(home, /\/notes\/r0-69i\.html/);

  assert.match(home, /i18n-en\.js(?:\?[^"]*)?/);
  assert.match(home, /下一步 R0\.69J/);
  assert.ok(note.includes("\\int\\phi S:\\nabla^2p"));
  assert.ok(note.includes("\\left(\\frac12qu-A^2u\\right)\\cdot\\nabla\\phi"));
  assert.ok(note.includes("+2\\int\\phi\\det S"));
  assert.ok(note.includes("-\\frac{676}{40425}"));
  assert.ok(note.includes("\\frac{228}{2695}"));
  assert.match(note, /六个局部化项的缩放次数全部等于三/);
  assert.match(note, /只关闭裸空间截断/);
  assert.match(note, /没有解决三维 Navier–Stokes 千禧年问题/);
  assert.match(note, /R0\.69J 的通过标准/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/);
});

test("keeps every R0.69I navigation target resolvable", async () => {
  const note = await readFile(noteUrl, "utf8");
  const ids = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const hashes = [...note.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(hashes.length >= 10);
  for (const hash of hashes) {
    assert.ok(ids.has(hash), "missing target #" + hash);
  }
});

test("lists the R0.69I translations in the bilingual build", async () => {
  const script = await readFile(
    new URL("../public/i18n-en.js", import.meta.url),
    "utf8",
  );
  assert.match(script, /R0\.69I \| Localization transfers global cancellation to same-order commutators/);
});
