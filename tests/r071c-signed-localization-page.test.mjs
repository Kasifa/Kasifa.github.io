import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);

function assertLocalAnchorsResolve(html) {
  const ids = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const targets = [...html.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(targets.length >= 14);
  for (const target of targets) assert.ok(ids.has(target), target);
}

test("publishes the exact R0.71C signed-localization decision", async () => {
  const [home, note, recap] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71c.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71c.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r071c"/);
  assert.equal((home.match(/href="\/notes\/r0-71c\.html"/g) ?? []).length, 2);
  assert.match(recap, /R0\.71B–R0\.71C · 正输出系数和有符号传播/);
  for (const token of [
    "E_{\\rm leaves}=E_{\\rm root}+\\sum_{v\\ {\\rm internal}}\\delta_v",
    "\\Pi'\\succ\\Pi\\Longrightarrow E_\\Pi\\le E_{\\Pi'}",
    "\\frac{A^2B^2}{64}",
    "W_B(t)=2\\left(e^{-8\\nu t}-e^{-14\\nu t}\\right)",
    "W_B'(0)=12\\nu\\varepsilon^3+\\frac{76}{5}\\varepsilon^4",
    "\\mathcal T_+(\\delta\\Omega)=a_+(\\delta\\Omega)=0",
    "A_{{\\rm sb},+}",
    "(\\beta_{\\alpha,I}^+)^2",
  ]) {
    assert.ok(note.includes(token), token);
  }
});

test("keeps the conditional theorem and no-go boundaries explicit", async () => {
  const note = await readFile(new URL("notes/r0-71c.html", publicRoot), "utf8");

  assert.match(note, /没有得到新的无条件正则性定理/);
  assert.match(note, /不排除带加性热源或跨尺度通量源的估计/);
  assert.match(note, /该路径不是 NSE 反例/);
  assert.match(note, /不是新颖性或优先权证明/);
  assert.match(note, /对 Clay 问题的直接价值仍然有限/);
  assert.match(note, /没有证明一般 NSE 解上的 .* 发散或收敛/);
  assert.match(note, /R0\.71D：只检查通量平衡的物质抛物 tent/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note.slice(note.indexOf("<body")), /\\\\\\\(/);
  assertLocalAnchorsResolve(note);
});

test("links the complete R0.71C source and literature boundary", async () => {
  const note = await readFile(new URL("notes/r0-71c.html", publicRoot), "utf8");
  for (const source of [
    "research/r071c_report-source.md",
    "research/r071c_literature_audit.md",
    "research/r071c_independent_audit.md",
    "research/r071c_exact_audit.py",
    "research/r071c_independent_audit.py",
    "research/certificates/r071c",
    "figures/r071c-signed-localization/fig-r071c-viscous-sign-creation",
    "1710.05569",
    "s002090000130",
    "0708.3067",
    "1102.1944",
    "1108.1165",
  ]) {
    assert.ok(note.includes(source), source);
  }
});

test("ships the synchronized R0.71C PDF and journal figure copies", async () => {
  const [note, notePdf, svg, figurePdf, png] = await Promise.all([
    readFile(new URL("notes/r0-71c.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71c.pdf", publicRoot)),
    readFile(
      new URL("figures/r0-71c-viscous-sign-creation.svg", publicRoot),
      "utf8",
    ),
    readFile(new URL("figures/r0-71c-viscous-sign-creation.pdf", publicRoot)),
    readFile(new URL("figures/r0-71c-viscous-sign-creation.png", publicRoot)),
  ]);

  assert.match(note, /src="\/figures\/r0-71c-viscous-sign-creation\.svg"/);
  assert.match(note, /href="\/figures\/r0-71c-viscous-sign-creation\.pdf"/);
  assert.match(note, /href="\/figures\/r0-71c-viscous-sign-creation\.png"/);
  assert.match(note, /href="\/notes\/r0-71c\.pdf"/);
  assert.equal(notePdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.ok(notePdf.length > 100_000);
  assert.match(svg, /<svg/);
  assert.equal(figurePdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.ok(figurePdf.length > 10_000);
  assert.ok(png.length > 100_000);
});

test("retains the R0.71C recap while the live route advances through R0.71D", async () => {
  const [home, literature, recap] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71c.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /<strong>128<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.71D<\/strong>最新研究节点/);
  assert.match(home, /Research topology · R0\.1–R0\.71D/);
  assert.match(home, /展开 38 篇公开笔记/);
  assert.match(home, /NEXT · R0\.71E/);
  assert.match(home, /综述 v0\.89 · 2026-08-25/);
  assert.match(literature, /R0\.69P–R0\.71D/);
  assert.match(literature, /开放接口 · R0\.71E/);
  assert.match(literature, /文献综述 v0\.89 · 2026-08-25/);
  assert.match(recap, /收录节点：67/);
  assert.match(recap, /回顾截止时公开笔记：127/);
  assert.match(recap, /href="\/recap-r0-61-r0-71c\.pdf"/);
  assert.match(home, /src="\/i18n-en\.js\?v=0\.89"/);
  assert.match(literature, /src="\/i18n-en\.js\?v=0\.89"/);
  assert.match(recap, /src="\/i18n-en\.js\?v=0\.88"/);
});
