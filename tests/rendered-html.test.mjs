import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const siteUrl = new URL("../public/research-review.html", import.meta.url);
const firstNoteUrl = new URL("../public/notes/r0-1.html", import.meta.url);
const secondNoteUrl = new URL("../public/notes/r0-2.html", import.meta.url);

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
  const [home, firstNote, secondNote] = await Promise.all([
    readFile(siteUrl, "utf8"),
    readFile(firstNoteUrl, "utf8"),
    readFile(secondNoteUrl, "utf8"),
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
});
