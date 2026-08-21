import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69A with the exact theorem and claim boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69a.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r069a"/);
  assert.match(home, /\/notes\/r0-69a\.html/);
  assert.match(home, /综述 v0\.69 · 2026-08-21/);
  assert.match(home, /下一步 R0\.69B/);
  assert.match(note, /1\.00000002593745353460841221206765949/);
  assert.match(note, /2\.6140836268319572193\\times10\^\{-8\}/);
  assert.match(note, /没有未计算的 Picard 阶/);
  assert.match(note, /全局光滑的不变剪切类/);
  assert.match(note, /三维横向扰动/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("keeps every R0.69A note navigation target resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69a.html", publicRoot), "utf8");
  const targets = new Set([...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]));
  for (const match of note.matchAll(/href="#([^"]+)"/g)) {
    assert.ok(targets.has(match[1]), "Missing R0.69A target: #" + match[1]);
  }
});

test("lists the R0.69A note in bilingual site discovery", async () => {
  const { listSiteHtmlFiles } = await import("../scripts/i18n-lib.mjs");
  const files = await listSiteHtmlFiles(new URL("../public", import.meta.url).pathname);
  assert.ok(files.some((file) => file.endsWith("/notes/r0-69a.html")));
});
