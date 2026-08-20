import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

test("publishes the R0.68B-2d/e page with strict evidence boundaries", async () => {
  const [home, note, svg, png, pdf] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-68b2de.html", publicRoot), "utf8"),
    readFile(new URL("figures/r0-68b2de-strict-components.svg", publicRoot), "utf8"),
    readFile(new URL("figures/r0-68b2de-strict-components.png", publicRoot)),
    readFile(new URL("figures/r0-68b2de-strict-components.pdf", publicRoot)),
  ]);

  assert.match(home, /id="r068b2de"/);
  assert.match(home, /\/notes\/r0-68b2de\.html/);
  assert.match(home, /综述 v0\.58 · 2026-08-21/);
  assert.match(note, /4,368/);
  assert.match(note, /1,792/);
  assert.match(note, /2\.567\\times10\^{-6\}/);
  assert.match(note, /2\.873211297037509\\times10\^{-9\}/);
  assert.match(note, /最终热符号：尚未完成/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.doesNotMatch(note, /我们|攻关|主攻|杀死错误想法|突破/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.match(svg, /Strict derivative and dominant-mass components/);
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
});

test("lists compound research-note filenames for bilingual builds", async () => {
  const { listSiteHtmlFiles } = await import("../scripts/i18n-lib.mjs");
  const files = await listSiteHtmlFiles(new URL("../public", import.meta.url).pathname);
  assert.ok(files.some((file) => file.endsWith("/notes/r0-68b2de.html")));
});
