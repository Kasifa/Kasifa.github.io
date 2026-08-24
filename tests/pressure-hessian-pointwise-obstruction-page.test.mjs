import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const homeUrl = new URL("../public/research-review.html", import.meta.url);
const noteUrl = new URL("../public/notes/r0-69h.html", import.meta.url);

test("publishes R0.69H with the exact pressure-sign obstruction", async () => {
  const [home, note] = await Promise.all([
    readFile(homeUrl, "utf8"),
    readFile(noteUrl, "utf8"),
  ]);

  assert.match(home, /id="r069h"/);
  assert.match(home, /\/notes\/r0-69h\.html/);
  assert.match(home, /综述 v0\.81 · 2026-08-24/);
  assert.match(home, /i18n-en\.js\?v=0\.81/);
  assert.match(home, /下一步 R0\.69I/);
  assert.ok(note.includes("H_{11}^{-}(0)=-1-\\frac{54}{85}t^2"));
  assert.ok(note.includes("H_{11}^{+}(0)=-1+\\frac{54}{85}t^2"));
  assert.ok(note.includes("(\\partial_t+u\\cdot\\nabla-\\Delta)\\lambda_1"));
  assert.ok(note.includes("\\int_{\\mathbb T^3}S:\\nabla^2p\\,dx=0"));
  assert.match(note, /不存在只读取局部/);
  assert.match(note, /二维嵌入，因此全局光滑/);
  assert.match(note, /不排除非局部或积分压力机制/);
  assert.match(note, /没有解决三维 Navier–Stokes 千禧年问题/);
  assert.match(note, /R0\.69I 的通过标准/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/);
});

test("keeps every R0.69H navigation target resolvable", async () => {
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

test("lists the R0.69H translations in the bilingual build", async () => {
  const script = await readFile(
    new URL("../public/i18n-en.js", import.meta.url),
    "utf8",
  );
  assert.match(script, /R0\.69H \| Pointwise sign obstruction for the pressure Hessian/);
});
