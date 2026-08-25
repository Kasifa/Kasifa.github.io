import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69E with the regular-interval resolvent theorem and boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69e.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r069e"/);
  assert.match(home, /\/notes\/r0-69e\.html/);
  assert.match(home, /综述 v0\.87 · 2026-08-25/);
  assert.match(home, /i18n-en\.js(?:\?[^"]*)?/);
  assert.match(home, /下一步 R0\.69F/);
  assert.ok(note.includes("a=2C_B\\|v\\|_{X_\\tau}"));
  assert.ok(note.includes("b_\\lambda=2C_SV_\\tau\\sqrt{\\frac{\\pi}{\\lambda}}"));
  assert.ok(note.includes("\\Gamma(\\tau,T,\\lambda)"));
  assert.ok(note.includes("\\frac{\\Gamma(\\tau,T,\\lambda)}{(1-a)(1-b_\\lambda)}"));
  assert.ok(note.includes("A_{10}z_0(t)=e^{(t-\\tau)\\Delta}(A_{00}z_0)(\\tau)"));
  assert.ok(note.includes("\\ell_k=\\eta(\\sqrt k-\\sqrt{k-1})"));
  assert.match(note, /18 \/ 18 通过/);
  assert.match(note, /固定光滑参考区间上的临界线性化预解有限/);
  assert.match(note, /没有解决三维 Navier–Stokes 千禧年问题/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("keeps every R0.69E navigation target resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69e.html", publicRoot), "utf8");
  const targets = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  for (const match of note.matchAll(/href="#([^"]+)"/g)) {
    assert.ok(targets.has(match[1]), "Missing R0.69E target: #" + match[1]);
  }
});

test("lists the R0.69E note in bilingual site discovery", async () => {
  const { listSiteHtmlFiles } = await import("../scripts/i18n-lib.mjs");
  const files = await listSiteHtmlFiles(
    new URL("../public", import.meta.url).pathname,
  );
  assert.ok(files.some((file) => file.endsWith("/notes/r0-69e.html")));
});
