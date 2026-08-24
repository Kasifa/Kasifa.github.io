import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69B with the exact gate and claim boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69b.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r069b"/);
  assert.match(home, /\/notes\/r0-69b\.html/);
  assert.match(home, /综述 v0\.82 · 2026-08-24/);
  assert.match(home, /下一步 R0\.69C/);
  assert.match(note, /0\.7975855452903290&lt;\\rho&lt;0\.7975855452903292/);
  assert.ok(note.includes("(6+4\\sqrt{2})\\rho^r"));
  assert.ok(note.includes("\\eta_{\\rm KT}^{\\rm per}"));
  assert.match(note, /13 \/ 13 通过/);
  assert.match(note, /常数量级临界扰动仍然完全开放/);
  assert.match(note, /没有解决三维 Navier–Stokes 千禧年问题/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("keeps every R0.69B navigation target resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69b.html", publicRoot), "utf8");
  const targets = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  for (const match of note.matchAll(/href="#([^"]+)"/g)) {
    assert.ok(targets.has(match[1]), "Missing R0.69B target: #" + match[1]);
  }
});

test("lists the R0.69B note in bilingual site discovery", async () => {
  const { listSiteHtmlFiles } = await import("../scripts/i18n-lib.mjs");
  const files = await listSiteHtmlFiles(
    new URL("../public", import.meta.url).pathname,
  );
  assert.ok(files.some((file) => file.endsWith("/notes/r0-69b.html")));
});
