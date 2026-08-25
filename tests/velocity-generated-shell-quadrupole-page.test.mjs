import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";
const homeUrl=new URL("../public/research-review.html",import.meta.url);
const noteUrl=new URL("../public/notes/r0-69k.html",import.meta.url);
test("publishes R0.69K with the exact velocity-generated shell gain",async()=>{
 const [home,note]=await Promise.all([readFile(homeUrl,"utf8"),readFile(noteUrl,"utf8")]);
 assert.match(home,/id="r069k"/); assert.match(home,/\/notes\/r0-69k\.html/);
 assert.match(home,/综述 v0\.88 · 2026-08-25/); assert.match(home,/i18n-en\.js(?:\?[^"]*)?/);
 assert.match(home,/下一步 R0\.69L/);
 assert.ok(note.includes("q:=\\operatorname{tr}((\\nabla u)^2)"));
 assert.ok(note.includes("\\partial_i\\partial_j(u_i u_j)"));
 assert.ok(note.includes("\\frac{C}{R_m^5}"));
 assert.ok(note.includes("\\operatorname{diag}(0,6,-6)"));
 assert.ok(note.includes("-\\frac{3}{2\\pi R^5}\\ne0"));
 assert.match(note,/多出两个距离幂/); assert.match(note,/不是全局次临界估计/);
 assert.match(note,/没有解决三维 Navier–Stokes 千禧年问题/); assert.match(note,/R0\.69L 的通过标准/);
 assert.doesNotMatch(note,/[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
 assert.doesNotMatch(note,/我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/);
});
test("keeps every R0.69K navigation target resolvable",async()=>{
 const note=await readFile(noteUrl,"utf8");
 const ids=new Set([...note.matchAll(/\sid="([^"]+)"/g)].map(m=>m[1]));
 const hashes=[...note.matchAll(/href="#([^"]+)"/g)].map(m=>m[1]);
 assert.ok(hashes.length>=9); for(const hash of hashes) assert.ok(ids.has(hash),"missing target #"+hash);
});
test("lists the R0.69K translations in the bilingual build",async()=>{
 const script=await readFile(new URL("../public/i18n-en.js",import.meta.url),"utf8");
 assert.match(script,/R0\.69K \| Velocity generation adds two powers of far-field decay/);
});
