import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes R0.69D with the nonlinear gate and exact boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-69d.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r069d"/);
  assert.match(home, /\/notes\/r0-69d\.html/);
  assert.match(home, /综述 v0\.73 · 2026-08-21/);
  assert.match(home, /i18n-en\.js\?v=0\.73/);
  assert.match(home, /下一步 R0\.69E/);
  assert.ok(note.includes("\\mathcal A_vz=\\mathcal B(v,z)+\\mathcal B(z,v)"));
  assert.ok(note.includes("\\chi_r:=4C_BM_T^2C_H\\delta_r"));
  assert.ok(note.includes("1-\\sqrt{1-\\chi_r}"));
  assert.ok(note.includes("\\mathcal B(z_r,z_r)"));
  assert.ok(note.includes("\\le2M_TC_HC_0\\rho^r"));
  assert.match(note, /18 \/ 18 通过/);
  assert.match(note, /完整非线性解分支以 O\(rho\^r\) 收敛/);
  assert.match(note, /没有解决三维 Navier–Stokes 千禧年问题/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});

test("keeps every R0.69D navigation target resolvable", async () => {
  const note = await readFile(new URL("notes/r0-69d.html", publicRoot), "utf8");
  const targets = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  for (const match of note.matchAll(/href="#([^"]+)"/g)) {
    assert.ok(targets.has(match[1]), "Missing R0.69D target: #" + match[1]);
  }
});

test("lists the R0.69D note in bilingual site discovery", async () => {
  const { listSiteHtmlFiles } = await import("../scripts/i18n-lib.mjs");
  const files = await listSiteHtmlFiles(
    new URL("../public", import.meta.url).pathname,
  );
  assert.ok(files.some((file) => file.endsWith("/notes/r0-69d.html")));
});
