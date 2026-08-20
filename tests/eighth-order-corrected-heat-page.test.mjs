import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes the R0.68B-2f/g/h fixed-coefficient sign certificate", async () => {
  const [home, note, svg, png, pdf] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-68b2fgh.html", publicRoot), "utf8"),
    readFile(new URL("figures/r0-68b2fgh-corrected-heat.svg", publicRoot), "utf8"),
    readFile(new URL("figures/r0-68b2fgh-corrected-heat.png", publicRoot)),
    readFile(new URL("figures/r0-68b2fgh-corrected-heat.pdf", publicRoot)),
  ]);

  assert.match(home, /id="r068b2fgh"/);
  assert.match(home, /\/notes\/r0-68b2fgh\.html/);
  assert.match(home, /综述 v0\.66 · 2026-08-21/);
  assert.match(note, /14,350,336/);
  assert.match(note, /44,514/);
  assert.match(note, /16,777,216/);
  assert.match(note, /-2\.87321129703704757\\times10\^\{-9\}/);
  assert.match(note, /全部 Picard 阶/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.match(svg, /Certification chain for one fixed eighth-order/);
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("lists the R0.68B-2f/g/h note in bilingual site discovery", async () => {
  const { listSiteHtmlFiles } = await import("../scripts/i18n-lib.mjs");
  const files = await listSiteHtmlFiles(new URL("../public", import.meta.url).pathname);
  assert.ok(files.some((file) => file.endsWith("/notes/r0-68b2fgh.html")));
});
