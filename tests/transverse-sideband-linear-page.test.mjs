import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69C with the exact linearized gate and boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69c.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r069c"/);
  assert.match(home, /\/notes\/r0-69c\.html/);
  assert.match(home, /综述 v0\.69 · 2026-08-21/);
  assert.match(home, /下一步 R0\.69D/);
  assert.ok(note.includes("[\\mathscr T_{R,m,s}]"));
  assert.ok(note.includes("-Rs/Q"));
  assert.ok(note.includes("\\le d=|k|"));
  assert.ok(note.includes("=2R^2"));
  assert.ok(note.includes("\\frac{|A|}{2R}"));
  assert.ok(note.includes("\\kappa_r:=4C_BC_HC_0\\rho^r"));
  assert.match(note, /18 \/ 18 通过/);
  assert.match(note, /线性化传播子与自由热流的临界算子差仍只有/);
  assert.match(note, /没有解决三维 Navier–Stokes 千禧年问题/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("keeps every R0.69C navigation target resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69c.html", publicRoot), "utf8");
  const targets = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  for (const match of note.matchAll(/href="#([^"]+)"/g)) {
    assert.ok(targets.has(match[1]), "Missing R0.69C target: #" + match[1]);
  }
});

test("lists the R0.69C note in bilingual site discovery", async () => {
  const { listSiteHtmlFiles } = await import("../scripts/i18n-lib.mjs");
  const files = await listSiteHtmlFiles(
    new URL("../public", import.meta.url).pathname,
  );
  assert.ok(files.some((file) => file.endsWith("/notes/r0-69c.html")));
});
