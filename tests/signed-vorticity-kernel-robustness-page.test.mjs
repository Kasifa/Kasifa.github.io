import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const homeUrl = new URL("../public/research-review.html", import.meta.url);
const noteUrl = new URL("../public/notes/r0-69g.html", import.meta.url);

test("publishes R0.69G with the exact positive-weight barrier", async () => {
  const [home, note] = await Promise.all([
    readFile(homeUrl, "utf8"),
    readFile(noteUrl, "utf8"),
  ]);

  assert.match(home, /id="r069g"/);
  assert.match(home, /\/notes\/r0-69g\.html/);

  assert.match(home, /i18n-en\.js(?:\?[^"]*)?/);
  assert.match(home, /下一步 R0\.69H/);
  assert.ok(note.includes("\\sup_{\\substack{g\\ge0\\\\ \\int_Ag=1}}"));
  assert.ok(note.includes("=\\|K_{x,t}\\|_{L^\\infty(A)}"));
  assert.ok(note.includes("D=-\\sin\\varphi\\,\\widehat z_2\\widehat z_3"));
  assert.ok(note.includes("\\nabla\\cdot(|\\omega|\\xi)=0"));
  assert.match(note, /它排除的是一种证明架构/);
  assert.match(note, /不证明任意选择权重可由散度为零的涡量实现/);
  assert.match(note, /不验证两篇 2026 预印本的完整证明/);
  assert.match(note, /没有解决三维 Navier–Stokes 千禧年问题/);
  assert.match(note, /R0\.69H 的通过标准/);
  assert.doesNotMatch(note, /方向-only/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("keeps every R0.69G navigation target resolvable", async () => {
  const note = await readFile(noteUrl, "utf8");
  const ids = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const hashes = [...note.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(hashes.length >= 9);
  for (const hash of hashes) {
    assert.ok(ids.has(hash), "missing target #" + hash);
  }
});

test("lists the R0.69G translations in the bilingual build", async () => {
  const script = await readFile(
    new URL("../public/i18n-en.js", import.meta.url),
    "utf8",
  );
  assert.match(script, /R0\.69G \| Magnitude-coupling barrier for the signed vorticity kernel/);
});
