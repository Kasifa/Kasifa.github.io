import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const siteUrl = new URL("../public/research-review.html", import.meta.url);
const firstNoteUrl = new URL("../public/notes/r0-1.html", import.meta.url);
const secondNoteUrl = new URL("../public/notes/r0-2.html", import.meta.url);
const thirdNoteUrl = new URL("../public/notes/r0-3.html", import.meta.url);
const fourthNoteUrl = new URL("../public/notes/r0-4.html", import.meta.url);
const fifthNoteUrl = new URL("../public/notes/r0-5.html", import.meta.url);
const sixthNoteUrl = new URL("../public/notes/r0-6.html", import.meta.url);
const seventhNoteUrl = new URL("../public/notes/r0-7.html", import.meta.url);
const eighthNoteUrl = new URL("../public/notes/r0-8.html", import.meta.url);
const ninthNoteUrl = new URL("../public/notes/r0-9.html", import.meta.url);
const tenthNoteUrl = new URL("../public/notes/r0-10.html", import.meta.url);

test("ships the complete Chinese research review as static HTML", async () => {
  const html = await readFile(siteUrl, "utf8");

  assert.match(html, /<html lang="zh-CN">/);
  assert.match(html, /Navier–Stokes 开放研究日志/);
  assert.match(html, /这个问题要求证明什么/);
  assert.match(html, /目前已经知道什么/);
  assert.match(html, /接下来的工作计划/);
  assert.match(html, /当前研究进展/);
  assert.match(html, /08 \/ Selected sources/);
  assert.doesNotMatch(html, /id="publish"|href="#publish"|Open publication/);
  assert.doesNotMatch(html, /codex-preview|SkeletonPreview|react-loading-skeleton/);
});

test("keeps all in-page navigation targets resolvable", async () => {
  const html = await readFile(siteUrl, "utf8");
  const targets = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const internalLinks = [
    ...html.matchAll(/\shref="#([^"]+)"/g),
  ].map((match) => match[1]);

  assert.ok(internalLinks.length >= 10);
  for (const target of internalLinks) {
    assert.ok(targets.has(target), `Missing in-page target: #${target}`);
  }
});

test("labels the unresolved and preprint status explicitly", async () => {
  const html = await readFile(siteUrl, "utf8");

  assert.match(html, /尚未解决/);
  assert.match(html, /预印本主张/);
  assert.match(html, /不能等同于已经过同行评议和独立复核的定理/);
  assert.match(html, /https:\/\/www\.claymath\.org\/wp-content/);
  assert.match(html, /https:\/\/arxiv\.org\/abs\/2509\.25116/);
});

test("publishes and links the first auditable research note", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(firstNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-1\.html"/);
  assert.match(note, /研究笔记 R0\.1/);
  assert.match(note, /Leray 投影/);
  assert.match(note, /\\dot H\^\{1\/2\}/);
  assert.match(note, /\(T_k,T_p,T_q\)=\(1,-4,3\)/);
  assert.match(note, /不是新定理/);
});

test("publishes and links the dyadic-helical locality audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(secondNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-2\.html"/);
  assert.match(note, /研究笔记 R0\.2/);
  assert.match(note, /2\^{-2M\}/);
  assert.match(note, /high–high→low/);
  assert.match(note, /同号高频螺旋/);
  assert.match(note, /异号高频螺旋/);
  assert.match(note, /近对角区仍然没有小因子/);
  assert.match(note, /不是新的定理/);
});

test("publishes and links the exact near-diagonal helical-kernel audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(thirdNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-3\.html"/);
  assert.match(note, /研究笔记 R0\.3/);
  assert.match(note, /\\mathcal C_s=\|g_\{kpq\}W_s\|/);
  assert.match(note, /\\sqrt\{15\}\/16/);
  assert.match(note, /0\.6354564734866010/);
  assert.match(note, /同号类有精确抵消/);
  assert.match(note, /不存在一个仅由单三元组几何产生/);
  assert.match(note, /不是新定理/);
});

test("publishes and links the dense near-diagonal packet argument", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fourthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-4\.html"/);
  assert.match(note, /研究笔记 R0\.4/);
  assert.match(note, /\\widehat u_N\(k\)=N\^\{-3\/2\}a\(k\/N\)/);
  assert.match(note, /\\#\\operatorname\{supp\}\\widehat u_N\\asymp N\^3/);
  assert.match(note, /六维 Riemann 和/);
  assert.match(note, /不存在只依赖高频尺度/);
  assert.match(note, /动力学可持续性/);
  assert.match(note, /不是奇性构造/);
});

test("publishes and links the short-time critical-packet dynamics audit", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(fifthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-5\.html"/);
  assert.match(note, /研究笔记 R0\.5/);
  assert.match(note, /\\tau=N\^2t/);
  assert.match(note, /热流同号引理/);
  assert.match(note, /Fourier–Galerkin/);
  assert.match(note, /83\.72%/);
  assert.match(note, /时间步减半/);
  assert.match(note, /不是 PDE 证明/);
});

test("publishes and links the fixed-injection leakage optimization", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(sixthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-6\.html"/);
  assert.match(note, /研究笔记 R0\.6/);
  assert.match(note, /一阶频谱泄漏公式/);
  assert.match(note, /C\^2=\\sqrt2 A\^2/);
  assert.match(note, /32\.22030867/);
  assert.match(note, /58\.24/);
  assert.match(note, /6\.248/);
  assert.match(note, /14\.1\\%/);
  assert.match(note, /不是奇性轨道/);
});

test("publishes and links the full six-mode coercivity note", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(seventhNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-7\.html"/);
  assert.match(note, /研究笔记 R0\.7/);
  assert.match(note, /六模态强制性不等式/);
  assert.match(note, /9\.7253\\times10\^\{-8\}/);
  assert.match(note, /2D3C 分裂/);
  assert.match(note, /0\.07013115/);
  assert.match(note, /0\.06782090/);
  assert.match(note, /中心模型本身不能成为 Navier-Stokes 奇性轨道/);
});

test("publishes and links the minimal non-coplanar butterfly note", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(eighthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-8\.html"/);
  assert.match(note, /研究笔记 R0\.8/);
  assert.match(note, /最小性命题/);
  assert.match(note, /\\mathfrak S=-\(\\sqrt2\+1\)\\mathfrak T/);
  assert.match(note, /0\.0545359/);
  assert.match(note, /0\.0156872/);
  assert.match(note, /生成模态把增长区间延长了约 3\.5 倍/);
  assert.match(note, /没有给出 Galerkin 截断趋于无穷时的解析误差界/);
});

test("publishes and links the exact cone-chain Duhamel note", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(ninthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-9\.html"/);
  assert.match(note, /研究笔记 R0\.9/);
  assert.match(note, /c_j\+e_j\+a_\{j\+1\}=0/);
  assert.match(note, /3J\+2/);
  assert.match(note, /4\^\{5j\}H_j/);
  assert.match(note, /81\/\(173056\\sqrt3\)/);
  assert.match(note, /m_N\/N\^3/);
  assert.match(note, /必要，不是充分/);
  assert.match(note, /不是完整动力学近似/);
});

test("publishes and links the dense cross-shell packet note", async () => {
  const [home, note] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(tenthNoteUrl, "utf8"),
  ]);

  assert.match(home, /href="\/notes\/r0-10\.html"/);
  assert.match(note, /研究笔记 R0\.10/);
  assert.match(note, /N\^\{-2\}a_\\delta\(k\/N\)/);
  assert.match(note, /136\\pi\\sqrt6/);
  assert.match(note, /688905/);
  assert.match(note, /O\(\\delta\^5\)/);
  assert.match(note, /\\operatorname\{span\}\(1,-1,-1\)/);
  assert.match(note, /一维极化像/);
  assert.match(note, /没有估计第二 Picard/);
});

test("follows the operating system light and dark color scheme", async () => {
  const html = await readFile(siteUrl, "utf8");

  assert.match(html, /color-scheme:\s*light dark/);
  assert.match(html, /prefers-color-scheme:\s*dark/);
  assert.match(
    html,
    /name="theme-color" content="#171816" media="\(prefers-color-scheme: dark\)"/,
  );
});

test("uses a plain first-person research voice", async () => {
  const [home, firstNote, secondNote, thirdNote, fourthNote, fifthNote, sixthNote, seventhNote, eighthNote, ninthNote, tenthNote] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(firstNoteUrl, "utf8"),
    readFile(secondNoteUrl, "utf8"),
    readFile(thirdNoteUrl, "utf8"),
    readFile(fourthNoteUrl, "utf8"),
    readFile(fifthNoteUrl, "utf8"),
    readFile(sixthNoteUrl, "utf8"),
    readFile(seventhNoteUrl, "utf8"),
    readFile(eighthNoteUrl, "utf8"),
    readFile(ninthNoteUrl, "utf8"),
    readFile(tenthNoteUrl, "utf8"),
  ]);

  assert.match(home, /这是我整理的/);
  assert.match(home, /我目前/);
  assert.doesNotMatch(
    home,
    /我们|攻关|主攻|研究纪律|杀死错误想法|宏大新泛函|三重审计/,
  );
  assert.match(firstNote, /这里没有新定理/);
  assert.doesNotMatch(
    firstNote,
    /本笔记的职责|本轮|审计规则|准确停止|本轮真正得到/,
  );
  assert.match(secondNote, /我把 R0\.1/);
  assert.doesNotMatch(
    secondNote,
    /Research packet|AUDIT STATUS|我们|本轮|成果边界|研究判定|极值审计/,
  );
  assert.match(thirdNote, /我继续检查 R0\.2/);
  assert.doesNotMatch(
    thirdNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(fourthNote, /我把 R0\.3/);
  assert.doesNotMatch(
    fourthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(fifthNote, /我把 R0\.4/);
  assert.doesNotMatch(
    fifthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(sixthNote, /我把 R0\.5/);
  assert.doesNotMatch(
    sixthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(seventhNote, /我把 R0\.6/);
  assert.doesNotMatch(
    seventhNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(eighthNote, /我把 R0\.7/);
  assert.doesNotMatch(
    eighthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(ninthNote, /我把 R0\.8/);
  assert.doesNotMatch(
    ninthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.match(tenthNote, /我把 R0\.9/);
  assert.doesNotMatch(
    tenthNote,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
});
