import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import test from "node:test";

const homeUrl = new URL("../public/research-review.html", import.meta.url);
const noteUrl = new URL("../public/notes/r0-67.html", import.meta.url);
const translationUrl = new URL("../public/i18n-en.js", import.meta.url);
const noteStyleUrl = new URL("../public/note-retro.css", import.meta.url);
const publicFigureRoot = new URL("../public/figures/", import.meta.url);
const archiveFigureRoot = new URL(
  "../figures/r067-sixth-order-cycle/fig-r067-sixth-order-cycle/",
  import.meta.url,
);

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

test("publishes the exact R0.67A theorem with its open heat boundary", async () => {
  const [home, note, translations, noteStyle] = await Promise.all([
    readFile(homeUrl, "utf8"),
    readFile(noteUrl, "utf8"),
    readFile(translationUrl, "utf8"),
    readFile(noteStyleUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-67\.html"/);
  assert.ok(home.includes("R0.67A 已完成："));
  assert.ok(home.includes("下一步 R0.67C："));
  assert.ok(home.includes("综述 v0.52 · 2026-08-20"));

  assert.match(note, /研究笔记 R0\.67A/);
  assert.match(note, /14 项证书检查全通过/);
  assert.match(note, /直接状态：320/);
  assert.match(note, /像空间维数：36/);
  assert.match(note, /直接卷积：7 层全状态/);
  assert.ok(note.includes("A+B+C-D-E=Q"));
  assert.ok(note.includes("2\\times32\\times5=320"));
  assert.ok(note.includes("\\chi_{\\rm im}(x)=x^5(x-256)^5q_4(x)^4q_{10}(x)"));
  assert.ok(note.includes("402.425429345624&lt;\\mu&lt;402.4254293456256"));
  assert.ok(note.includes("Y_r=C_{6,0}\\mu^r+O(300^r)"));
  assert.ok(note.includes("-0.013063396815425&lt;C_{6,0}&lt;-0.013063396815144"));
  assert.ok(note.includes("\\frac{|Y_r|}{M_r^2}\\longrightarrow\\infty"));
  assert.ok(note.includes("A_{\\rm abs}w=65536w"));
  assert.match(note, /这里的“如果”不能删除/);
  assert.match(note, /没有证明完整热加权六阶主投影非零/);
  assert.match(note, /没有解决三维 Navier--Stokes 千禧年问题/);
  assert.match(note, /r0-67-sixth-order-cycle\.svg/);
  assert.match(note, /r0-67-sixth-order-cycle\.png/);
  assert.match(note, /r0-67-sixth-order-cycle\.pdf/);
  assert.match(note, /8da878e5f7b07fd4e58f039d8abee458cd3eb122/);
  assert.match(note, /03aaf0af31b74207b9d9a068e4331424a5e84957/);
  assert.match(note, /765c13ac5456325e08bdac3c2e0aa8b0db54f469/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f]/);
  assert.doesNotMatch(note, /我们|攻关|主攻|杀死错误想法|突破/);

  assert.match(translations, /Exact spectral theorem for the zero-time sixth-order cycle/);
  assert.match(translations, /the complete heat-kernel projection remains to be proved/);
  assert.match(noteStyle, /\.hero-inner>\*\{min-width:0\}/);
  assert.match(noteStyle, /\.lead\{max-width:100%;margin:0;overflow-x:auto;overflow-y:hidden/);
});

test("publishes byte-exact mirrors of the formal R0.67A figure", async () => {
  for (const [publicName, archiveName] of [
    ["r0-67-sixth-order-cycle.svg", "figure.svg"],
    ["r0-67-sixth-order-cycle.png", "figure.png"],
    ["r0-67-sixth-order-cycle.pdf", "figure.pdf"],
  ]) {
    const [published, archived] = await Promise.all([
      readFile(new URL(publicName, publicFigureRoot)),
      readFile(new URL(archiveName, archiveFigureRoot)),
    ]);
    assert.equal(sha256(published), sha256(archived), publicName);
  }
});

test("keeps every R0.67A note navigation target resolvable", async () => {
  const note = await readFile(noteUrl, "utf8");
  const targets = new Set(
    [...note.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const links = [...note.matchAll(/\shref="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(links.length >= 10);
  for (const target of links) {
    assert.ok(targets.has(target), `Missing R0.67A target: #${target}`);
  }
});
