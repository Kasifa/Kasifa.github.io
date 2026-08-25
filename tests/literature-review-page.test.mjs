import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const pageUrl = new URL("../public/literature-review.html", import.meta.url);
const homeUrl = new URL("../public/research-review.html", import.meta.url);

test("publishes a source-backed literature review with four technical topologies", async () => {
  const html = await readFile(pageUrl, "utf8");

  assert.match(html, /三维 Navier–Stokes[\s\S]*全局正则性问题/);
  assert.equal((html.match(/技术拓扑图 [1-4]/g) ?? []).length, 4);
  assert.match(html, /问题的逻辑层级/);
  assert.match(html, /文献主干/);
  assert.match(html, /候选爆破排除树/);
  assert.match(html, /本站路线与文献接口/);
  assert.match(html, /R0\.69W/);
  assert.match(html, /R0\.70A–I/);
  assert.match(html, /R0\.70P–Z/);
  assert.match(html, /R0\.71A/);
  assert.match(html, /OPEN BRIDGE · R0\.71B/);
  assert.match(html, /common-response 的有符号尺度补偿/);
  assert.match(html, /prefers-color-scheme: dark/);
  assert.match(html, /\/i18n-en\.js/);
  assert.match(html, /\/bilingual\.js/);
  assert.equal((html.match(/<li id="ref-\d+">/g) ?? []).length, 30);
  assert.doesNotMatch(html, /已经解决|接近解决千禧年问题/);
  assert.doesNotMatch(html, /08 \/ Research judgment|08 · 研究判断|id="judgment"|DGX/);
  assert.doesNotMatch(html, /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法/);
});

test("keeps the top and side literature directories identical", async () => {
  const html = await readFile(pageUrl, "utf8");
  const top = html.match(/<nav class="topnav" data-section-nav[\s\S]*?<\/nav>/)?.[0];
  const side = html.match(/<ol data-section-nav>[\s\S]*?<\/ol>/)?.[0];
  assert.ok(top, "top directory should exist");
  assert.ok(side, "side directory should exist");

  const links = (block) =>
    [...block.matchAll(/<a href="(#[^"]+)">([^<]+)<\/a>/g)].map((match) => ({
      href: match[1],
      label: match[2].trim(),
    }));

  assert.deepEqual(links(top), links(side));
  assert.deepEqual(
    links(top).map(({ href }) => href),
    [
      "#problem",
      "#critical",
      "#map",
      "#foundations",
      "#blowup",
      "#recent",
      "#route",
      "#references",
    ],
  );
});

test("uses the research home page archival visual language", async () => {
  const html = await readFile(pageUrl, "utf8");
  assert.match(html, /--paper: #f2eddf/);
  assert.match(html, /--orange: #8a302c/);
  assert.match(html, /border-bottom: 3px double var\(--ink\)/);
  assert.match(html, /font-family: Georgia, "Songti SC"/);
  assert.match(html, /@media \(prefers-color-scheme: dark\)/);
});

test("places the language switcher in the literature review top bar", async () => {
  const html = await readFile(pageUrl, "utf8");
  assert.match(html, /<div class="bar-actions">[\s\S]*data-language-switcher-slot[\s\S]*<\/div>/);
  assert.match(html, /\.top-language-switcher\s*\{/);
  assert.match(html, /\.bar-language\s*\{[\s\S]*position: absolute;[\s\S]*right: 18px;/);
});

test("links the literature review from the research home page", async () => {
  const home = await readFile(homeUrl, "utf8");
  assert.ok(
    (home.match(/href="\/literature-review\.html"/g) ?? []).length >= 3,
    "home page should expose the review in navigation, route actions, and the review section",
  );
});
