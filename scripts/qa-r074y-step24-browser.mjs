#!/usr/bin/env node

import assert from "node:assert/strict";
import { createReadStream } from "node:fs";
import { mkdir } from "node:fs/promises";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { extname, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const outputRoot = resolve(process.env.R074Y_STEP24_BROWSER_QA_OUTPUT ?? "/tmp/r074y-step24-browser-qa");
const require = createRequire(import.meta.url);
const { chromium } = require(
  "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright",
);

function contentType(path) {
  return new Map([
    [".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"],
    [".css", "text/css; charset=utf-8"], [".svg", "image/svg+xml"],
    [".png", "image/png"], [".pdf", "application/pdf"], [".json", "application/json"],
    [".md", "text/markdown; charset=utf-8"], [".csv", "text/csv; charset=utf-8"],
  ]).get(extname(path).toLowerCase()) ?? "application/octet-stream";
}

const server = createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
  const relative = pathname === "/" ? "research-review.html" : pathname.replace(/^\/+/, "");
  const target = resolve(publicRoot, relative);
  if (!target.startsWith(`${publicRoot}/`)) { response.writeHead(403).end(); return; }
  response.setHeader("Content-Type", contentType(target));
  const stream = createReadStream(target);
  stream.on("error", () => response.writeHead(404).end());
  stream.pipe(response);
});

await mkdir(outputRoot, { recursive: true });
await new Promise((resolvePromise, reject) => {
  server.once("error", reject);
  server.listen(0, "127.0.0.1", resolvePromise);
});

const browser = await chromium.launch({
  executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
  headless: true,
});
const scenarios = [
  { id: "desktop-light-zh", viewport: { width: 1440, height: 900 }, colorScheme: "light", lang: "zh" },
  { id: "desktop-dark-en", viewport: { width: 1440, height: 900 }, colorScheme: "dark", lang: "en" },
  { id: "mobile-light-en", viewport: { width: 390, height: 844 }, colorScheme: "light", lang: "en" },
  { id: "mobile-dark-zh", viewport: { width: 390, height: 844 }, colorScheme: "dark", lang: "zh" },
];
const results = [];

try {
  const address = server.address();
  for (const scenario of scenarios) {
    const context = await browser.newContext({
      viewport: scenario.viewport,
      colorScheme: scenario.colorScheme,
      locale: scenario.lang === "zh" ? "zh-CN" : "en-US",
      deviceScaleFactor: 1,
    });
    const page = await context.newPage();
    const pageErrors = [];
    page.on("pageerror", (error) => pageErrors.push(error.message));
    const response = await page.goto(
      `http://127.0.0.1:${address.port}/notes/r0-74y.html?lang=${scenario.lang}`,
      { waitUntil: "networkidle" },
    );
    assert.equal(response?.status(), 200, `${scenario.id} main document`);
    await page.waitForFunction(() => document.documentElement.dataset.language);
    await page.waitForFunction(
      () => typeof globalThis.MathJax?.version === "string" && Boolean(globalThis.MathJax?.startup?.promise),
      null,
      { timeout: 30_000 },
    );
    await page.evaluate(async () => {
      await document.fonts.ready;
      await globalThis.MathJax.startup.promise;
    });

    const audit = await page.evaluate(() => {
      const bodyCopy = document.body.cloneNode(true);
      bodyCopy.querySelectorAll(".language-switcher").forEach((node) => node.remove());
      const visibleText = bodyCopy.innerText;
      const style = getComputedStyle(document.documentElement);
      return {
        documentLanguage: document.documentElement.lang,
        selectedLanguage: document.documentElement.dataset.language,
        title: document.title,
        h1: document.querySelector("h1")?.textContent?.trim(),
        switcher: document.querySelector(".language-switcher")?.textContent?.trim(),
        sitePaper: style.getPropertyValue("--paper").trim(),
        viewportWidth: window.innerWidth,
        scrollWidth: document.documentElement.scrollWidth,
        horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        mathJaxContainers: document.querySelectorAll("mjx-container").length,
        rawInlineDelimiters: (visibleText.match(/\\\(/g) ?? []).length,
        rawDisplayDelimiters: (visibleText.match(/\\\[/g) ?? []).length,
        chineseCharactersOutsideSwitcher: (visibleText.match(/[\u3400-\u9fff\uf900-\ufaff]/gu) ?? []).length,
        imageCount: document.images.length,
        formalFigureSections: document.querySelectorAll('#figure, [src*="r074y"], [href*="assets/r074y"]').length,
        routeScreenLabels: [...document.querySelectorAll(".label")].filter((node) => node.textContent.includes("ROUTE SCREEN")).length,
        frozenNoGo: /FROZEN.{0,40}NO-GO.{0,40}PROVED/i.test(visibleText),
        formalWindow: /FORMAL.{0,80}(NECESSARY|window)/i.test(visibleText),
        y57NotProved: /Y\.57.{0,80}(NOT PROVED|OPEN|not prove)/i.test(visibleText),
        clayBoundary: /NOT CLAY/.test(visibleText),
        chinesePdfLabels: document.querySelectorAll(".pdf-language-label").length,
      };
    });

    assert.equal(audit.selectedLanguage, scenario.lang, `${scenario.id} selected language`);
    assert.equal(audit.documentLanguage, scenario.lang === "en" ? "en" : "zh-CN", `${scenario.id} document language`);
    assert.equal(audit.horizontalOverflow, false, `${scenario.id} horizontal overflow ${audit.scrollWidth}/${audit.viewportWidth}`);
    assert.ok(audit.mathJaxContainers > 100, `${scenario.id} MathJax coverage`);
    assert.equal(audit.rawInlineDelimiters, 0, `${scenario.id} raw inline TeX`);
    assert.equal(audit.rawDisplayDelimiters, 0, `${scenario.id} raw display TeX`);
    assert.equal(audit.imageCount, 0, `${scenario.id} route-screen note has no figure images`);
    assert.equal(audit.formalFigureSections, 0, `${scenario.id} no R0.74Y formal figure`);
    assert.equal(audit.routeScreenLabels, 1, `${scenario.id} route-screen prominence`);
    assert.equal(audit.frozenNoGo, true, `${scenario.id} frozen no-go boundary`);
    assert.equal(audit.formalWindow, true, `${scenario.id} formal-window boundary`);
    assert.equal(audit.y57NotProved, true, `${scenario.id} Y.57 boundary`);
    assert.equal(audit.clayBoundary, true, `${scenario.id} Clay boundary`);
    assert.equal(audit.sitePaper, scenario.colorScheme === "dark" ? "#181714" : "#f3ecd8", `${scenario.id} colour scheme`);
    if (scenario.lang === "en") {
      assert.equal(audit.chineseCharactersOutsideSwitcher, 0, `${scenario.id} untranslated Chinese`);
      assert.match(audit.h1, /Payment-compatible two-coordinate route screen/);
      assert.equal(audit.switcher, "中文");
      assert.ok(audit.chinesePdfLabels >= 1, `${scenario.id} Chinese-PDF label`);
    } else {
      assert.match(audit.h1, /付款兼容的双坐标路线筛选/);
      assert.equal(audit.switcher, "English");
      assert.equal(audit.chinesePdfLabels, 0);
    }
    assert.deepEqual(pageErrors, [], `${scenario.id} page errors`);
    const screenshot = resolve(outputRoot, `${scenario.id}.png`);
    await page.screenshot({ path: screenshot, fullPage: false });
    results.push({ ...scenario, screenshot, ...audit, pageErrors });
    await context.close();
  }
} finally {
  await browser.close();
  await new Promise((resolvePromise) => server.close(resolvePromise));
}

process.stdout.write(`${JSON.stringify({ status: "PASS", scenarios: results }, null, 2)}\n`);
