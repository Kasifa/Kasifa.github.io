import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const homeUrl = new URL("../public/research-review.html", import.meta.url);
const noteUrl = new URL("../public/notes/r0-69f.html", import.meta.url);

test("publishes R0.69F with the exact no-go theorem and boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(homeUrl, "utf8"),
    readFile(noteUrl, "utf8"),
  ]);
  assert.match(home, /id="r069f"/);
  assert.match(home, /\/notes\/r0-69f\.html/);
  assert.match(home, /综述 v0\.65 · 2026-08-21/);
  assert.match(home, /i18n-en\.js\?v=0\.65/);
  assert.match(home, /下一步 R0\.69G/);
  assert.ok(note.includes("G(x)=E_{1/2}(x)"));
  assert.ok(note.includes("e^{x^2}\\operatorname{erfc}(-x)"));
  assert.ok(note.includes("\\theta_A^3=2A(1-\\theta_A)"));
  assert.ok(note.includes(
    "\\limsup_{j\\to\\infty}V_j\\sqrt{h_j}",
  ));
  assert.ok(note.includes("标准 \\(L^\\infty\\) 局部存在已经给出更强的每壳下界"));
  assert.match(note, /严格负结果/);
  assert.match(note, /没有构造或排除有限时奇性/);
  assert.match(note, /没有解决三维 Navier–Stokes 千禧年问题/);
  assert.match(note, /R0\.69G 的通过标准/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("keeps every R0.69F navigation target resolvable", async () => {
  const note = await readFile(noteUrl, "utf8");
  const ids = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const hashes = [
    ...note.matchAll(/href="#([^"]+)"/g),
  ].map((match) => match[1]);
  assert.ok(hashes.length >= 9);
  for (const hash of hashes) {
    assert.ok(ids.has(hash), "missing target #" + hash);
  }
});

test("lists the R0.69F translations in the bilingual build", async () => {
  const script = await readFile(
    new URL("../public/i18n-en.js", import.meta.url),
    "utf8",
  );
  assert.match(script, /R0\.69F \| Classical-scale barrier for endpoint-resolvent optimization/);
});
