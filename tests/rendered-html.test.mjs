import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const siteUrl = new URL("../public/research-review.html", import.meta.url);
const firstNoteUrl = new URL("../public/notes/r0-1.html", import.meta.url);

test("ships the complete Chinese research review as static HTML", async () => {
  const html = await readFile(siteUrl, "utf8");

  assert.match(html, /<html lang="zh-CN">/);
  assert.match(html, /Navier–Stokes 开放研究日志/);
  assert.match(html, /我们究竟要证明什么/);
  assert.match(html, /研究综述：我们已经站在哪里/);
  assert.match(html, /详细研究计划/);
  assert.match(html, /第一项任务已经明确/);
  assert.match(html, /GitHub Pages 是合适的第一选择/);
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
  assert.match(note, /Research packet R0\.1/);
  assert.match(note, /Leray 投影/);
  assert.match(note, /\\dot H\^\{1\/2\}/);
  assert.match(note, /\(T_k,T_p,T_q\)=\(1,-4,3\)/);
  assert.match(note, /不是新定理/);
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
