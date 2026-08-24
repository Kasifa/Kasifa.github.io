import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const homeUrl = new URL("../public/research-review.html", import.meta.url);
const noteUrl = new URL("../public/notes/r0-69j.html", import.meta.url);

test("publishes R0.69J with the exact harmonic quadrupole obstruction", async () => {
  const [home, note] = await Promise.all([
    readFile(homeUrl, "utf8"),
    readFile(noteUrl, "utf8"),
  ]);
  assert.match(home, /id="r069j"/);
  assert.match(home, /\/notes\/r0-69j\.html/);
  assert.match(home, /综述 v0\.82 · 2026-08-24/);
  assert.match(home, /i18n-en\.js(?:\?[^"]*)?/);
  assert.match(home, /下一步 R0\.69K/);
  assert.ok(note.includes("Q_R:=\\nabla^2p_{\\mathrm{far}}(0)"));
  assert.ok(note.includes("\\frac{3}{2\\pi R^3}\\operatorname{diag}(1,-1,0)"));
  assert.ok(note.includes("\\frac{3}{\\pi R^3}\\ne0"));
  assert.match(note, /余项有真实尺度增益/);
  assert.match(note, /见证目前是标量压力源/);
  assert.match(note, /没有解决三维 Navier–Stokes 千禧年问题/);
  assert.match(note, /R0\.69K 的通过标准/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/);
});

test("keeps every R0.69J navigation target resolvable", async () => {
  const note = await readFile(noteUrl, "utf8");
  const ids = new Set([...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]));
  const hashes = [...note.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.ok(hashes.length >= 9);
  for (const hash of hashes) assert.ok(ids.has(hash), "missing target #" + hash);
});

test("lists the R0.69J translations in the bilingual build", async () => {
  const script = await readFile(new URL("../public/i18n-en.js", import.meta.url), "utf8");
  assert.match(script, /R0\.69J \| Far-field remainder decays while the leading quadrupole remains/);
});
