#!/usr/bin/env node

import assert from "node:assert/strict";
import { createReadStream } from "node:fs";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { extname, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const externalBase = process.env.CLAY_B_SIGNED_SCALE_PUBLIC_BASE_URL;
const require = createRequire(import.meta.url);
const { chromium } = require("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");
const types = new Map([
  [".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"],
  [".css", "text/css; charset=utf-8"], [".svg", "image/svg+xml"],
  [".png", "image/png"], [".pdf", "application/pdf"], [".json", "application/json"],
]);

let server;
let baseUrl;
if (externalBase) {
  baseUrl = new URL(externalBase);
} else {
  server = createServer((request, response) => {
    const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
    const relative = pathname === "/" ? "research-review.html" : pathname.replace(/^\/+/, "");
    const target = resolve(publicRoot, relative);
    if (!target.startsWith(`${publicRoot}/`)) return response.writeHead(403).end();
    response.setHeader("Content-Type", types.get(extname(target).toLowerCase()) ?? "application/octet-stream");
    const stream = createReadStream(target);
    stream.on("error", () => response.writeHead(404).end());
    stream.pipe(response);
  });
  await new Promise((ok, fail) => {
    server.once("error", fail);
    server.listen(0, "127.0.0.1", ok);
  });
  baseUrl = new URL(`http://127.0.0.1:${server.address().port}/`);
}

const targets = [
  { id: "signed-note", path: "/notes/clay-b-signed-scale-20260905.html", h1Zh: /精确尺度相消与收缩定位的冲突/, h1En: /Exact scale cancellation conflicts with shrinking localization/i },
  { id: "roadmap", path: "/research-review.html", h1Zh: /全局正则性/, h1En: /Global\s*Regularity/i },
];
const scenarios = [
  { id: "desktop-light-zh", viewport: { width: 1440, height: 900 }, colorScheme: "light", lang: "zh" },
  { id: "desktop-dark-en", viewport: { width: 1440, height: 900 }, colorScheme: "dark", lang: "en" },
  { id: "mobile-light-en", viewport: { width: 390, height: 844 }, colorScheme: "light", lang: "en" },
  { id: "mobile-dark-zh", viewport: { width: 390, height: 844 }, colorScheme: "dark", lang: "zh" },
];

const browser = await chromium.launch({
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
});
const results = [];
try {
  for (const target of targets) for (const scenario of scenarios) {
    const id = `${target.id}-${scenario.id}`;
    const context = await browser.newContext({ viewport: scenario.viewport, colorScheme: scenario.colorScheme, locale: scenario.lang === "zh" ? "zh-CN" : "en-US" });
    const page = await context.newPage();
    const pageErrors = [];
    page.on("pageerror", (error) => pageErrors.push(error.message));
    const url = new URL(target.path, baseUrl);
    url.searchParams.set("lang", scenario.lang);
    url.searchParams.set("qa", "clay-b-signed-scale-20260905");
    const response = await page.goto(url.href, { waitUntil: "networkidle" });
    assert.equal(response?.status(), 200, `${id} main document`);
    await page.waitForFunction(() => document.documentElement.dataset.language);
    const audit = await page.evaluate((targetId) => {
      const body = document.body.cloneNode(true);
      body.querySelectorAll(".language-switcher").forEach((node) => node.remove());
      const selectedMain = document.querySelector(
        `main[data-language="${document.documentElement.dataset.language}"]`,
      );
      const text = targetId === "signed-note" ? selectedMain?.innerText ?? "" : body.innerText;
      return {
        selectedLanguage: document.documentElement.dataset.language,
        documentLanguage: document.documentElement.lang,
        h1: (targetId === "signed-note" ? selectedMain : document)?.querySelector("h1")?.textContent?.trim(),
        switcher: document.querySelector(".language-switcher")?.textContent?.trim(),
        overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        chinese: (text.match(/[\u3400-\u9fff\uf900-\ufaff]/gu) ?? []).length,
        imageCount: document.images.length,
        signedLink: Boolean(document.querySelector('a[href="/notes/clay-b-signed-scale-20260905.html"]')),
        integratedRoute: targetId === "roadmap" ? /Clay-B branch after the strategy change|策略调整后的 Clay-B 分支/.test(text) : true,
        ordinaryEndpoint: /ordinary smooth time|普通光滑时刻|普通终点/.test(text),
        h1Nonuniform: /H1 bound is not uniform|H¹[：:\s]+不统一|H1: nonuniform/.test(text),
        contractG: /contract G|合同 G/i.test(text),
        open: /\bOPEN\b/i.test(text),
        clay: /NOT CLAY/i.test(text),
      };
    }, target.id);
    assert.equal(audit.selectedLanguage, scenario.lang, `${id} language`);
    assert.equal(audit.documentLanguage, scenario.lang === "en" ? "en" : "zh-CN", `${id} document language`);
    assert.equal(audit.overflow, false, `${id} horizontal overflow`);
    assert.equal(audit.integratedRoute, true, `${id} integrated route`);
    assert.equal(audit.contractG, true, `${id} contract G`);
    assert.equal(audit.open, true, `${id} OPEN`);
    assert.equal(audit.clay, true, `${id} NOT CLAY`);
    if (target.id === "signed-note") {
      assert.equal(audit.imageCount, 0, `${id} images`);
      assert.equal(audit.ordinaryEndpoint, true, `${id} ordinary endpoint`);
      assert.equal(audit.h1Nonuniform, true, `${id} H1 limitation`);
    } else {
      assert.equal(audit.signedLink, true, `${id} signed-scale route link`);
    }
    if (scenario.lang === "en") {
      assert.equal(audit.chinese, 0, `${id} untranslated Chinese`);
      assert.match(audit.h1, target.h1En);
      assert.equal(audit.switcher, "中文");
    } else {
      assert.match(audit.h1, target.h1Zh);
      assert.equal(audit.switcher, "English");
    }
    assert.deepEqual(pageErrors, [], `${id} page errors`);
    results.push({ target: target.id, scenario: scenario.id, ...audit, pageErrors });
    await context.close();
  }
} finally {
  await browser.close();
  if (server) await new Promise((ok) => server.close(ok));
}

process.stdout.write(`${JSON.stringify({
  status: "PASS",
  releaseId: "ClayB-SignedScale-20260905",
  baseUrl: baseUrl.href,
  pageChecks: results.length,
  scenarios: results,
}, null, 2)}\n`);
