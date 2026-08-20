import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";

const recapUrl = new URL("../public/recap-r0-60.html", import.meta.url);
const homeUrl = new URL("../public/research-review.html", import.meta.url);

test("publishes a bilingual R0.00-R0.60 stage recap with strict claim boundaries", async () => {
  const [recap, home] = await Promise.all([
    readFile(recapUrl, "utf8"),
    readFile(homeUrl, "utf8"),
  ]);

  assert.match(home, /href="\/recap-r0-60\.html"/);
  assert.match(home, /R0\.00–R0\.60 · RECAP/);
  assert.match(recap, /六十轮之后/);
  assert.match(recap, /After sixty rounds/);
  assert.match(recap, /原问题仍未解决/);
  assert.match(recap, /The original problem remains open/);
  assert.match(recap, /对数学研究有价值；对 Clay 问题的直接推进仍低/);
  assert.match(recap, /Mathematically useful; still low in direct value for the Clay problem/);
  assert.match(recap, /data-recap-language="zh"/);
  assert.match(recap, /data-recap-language="en"/);
  assert.match(recap, /navier-stokes-language-v1/);
  assert.match(recap, /href="\/notes\/r0-60\.html"/);
  assert.match(recap, /href="\/notes\/r0-60\.html\?lang=en"/);
  assert.match(recap, /href="\/figures\/r0-60-invariant-shear-picard\.pdf"/);
  assert.doesNotMatch(recap, /我们|攻关|主攻|突破千禧年/);
  assert.doesNotMatch(recap, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
});
