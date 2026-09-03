#!/usr/bin/env node

import assert from "node:assert/strict";
import { createReadStream } from "node:fs";
import { mkdir } from "node:fs/promises";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { extname, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const outputRoot = resolve(process.env.R075C_STEP28_BROWSER_QA_OUTPUT ?? "/tmp/r075c-step28-browser-qa");
const externalBase = process.env.R075C_PUBLIC_BASE_URL;
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

let server;
let baseUrl;
if (externalBase) {
  baseUrl = new URL(externalBase);
} else {
  server = createServer((request, response) => {
    const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
    const relative = pathname === "/" ? "research-review.html" : pathname.replace(/^\/+/, "");
    const target = resolve(publicRoot, relative);
    if (!target.startsWith(`${publicRoot}/`)) { response.writeHead(403).end(); return; }
    response.setHeader("Content-Type", contentType(target));
    const stream = createReadStream(target);
    stream.on("error", () => response.writeHead(404).end());
    stream.pipe(response);
  });
  await new Promise((resolvePromise, reject) => {
    server.once("error", reject);
    server.listen(0, "127.0.0.1", resolvePromise);
  });
  baseUrl = new URL(`http://127.0.0.1:${server.address().port}/`);
}

await mkdir(outputRoot, { recursive: true });
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
    const url = new URL("/notes/r0-75c.html", baseUrl);
    url.searchParams.set("lang", scenario.lang);
    url.searchParams.set("qa", "r075c-step28");
    const response = await page.goto(url.href, { waitUntil: "networkidle" });
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
        figureSections: document.querySelectorAll('#figure, [src*="r075c"], [href*="assets/r075c"]').length,
        b44Disproved: /B\.44.{0,80}(DISPROVED|disproved|\u5426\u5b9a)/i.test(visibleText),
        shearPaid: /shear dissipation.{0,100}(PAID|paid|\u5df2\u652f\u4ed8)/i.test(visibleText),
        packingFalsePositive: /packing false positive|packing \u5047\u9633\u6027/i.test(visibleText),
        b45Undecided: /B\.45.{0,100}(NEITHER PROVED NOR DISPROVED|neither proved nor disproved|\u65e2\u672a\u8bc1\u4e5f\u672a\u5426)/i.test(visibleText),
        passiveOpen: /passive (row|dissipation)[\s\S]{0,160}OPEN/i.test(visibleText),
        notNseCounterexample: /not (an )?(NSE|Navier--Stokes) counterexample|\u4e0d\u662f Navier--Stokes counterexample/i.test(visibleText),
        noveltyBoundary: /NO NOVELTY CLAIM|establishes neither novelty|\u4e0d\u6784\u6210 novelty/i.test(visibleText),
        clayBoundary: /NOT CLAY/.test(visibleText),
        noFigureBoundary: /NO FIGURE|formal figure.{0,30}NOT APPLICABLE|\u6b63\u5f0f\u56fe\u4ef6.{0,30}NOT APPLICABLE/i.test(visibleText),
        chinesePdfLabels: document.querySelectorAll(".pdf-language-label").length,
      };
    });

    assert.equal(audit.selectedLanguage, scenario.lang, `${scenario.id} selected language`);
    assert.equal(audit.documentLanguage, scenario.lang === "en" ? "en" : "zh-CN", `${scenario.id} document language`);
    assert.equal(audit.horizontalOverflow, false, `${scenario.id} horizontal overflow ${audit.scrollWidth}/${audit.viewportWidth}`);
    assert.ok(audit.mathJaxContainers > 100, `${scenario.id} MathJax coverage`);
    assert.equal(audit.rawInlineDelimiters, 0, `${scenario.id} raw inline TeX`);
    assert.equal(audit.rawDisplayDelimiters, 0, `${scenario.id} raw display TeX`);
    assert.equal(audit.imageCount, 0, `${scenario.id} analytic note has no images`);
    assert.equal(audit.figureSections, 0, `${scenario.id} no R0.75C formal figure`);
    assert.equal(audit.b44Disproved, true, `${scenario.id} B.44 boundary`);
    assert.equal(audit.shearPaid, true, `${scenario.id} shear-payment boundary`);
    assert.equal(audit.packingFalsePositive, true, `${scenario.id} packing false-positive boundary`);
    assert.equal(audit.b45Undecided, true, `${scenario.id} B.45 boundary`);
    assert.equal(audit.passiveOpen, true, `${scenario.id} passive boundary`);
    assert.equal(audit.notNseCounterexample, true, `${scenario.id} NSE-counterexample boundary`);
    assert.equal(audit.noveltyBoundary, true, `${scenario.id} novelty boundary`);
    assert.equal(audit.clayBoundary, true, `${scenario.id} Clay boundary`);
    assert.equal(audit.noFigureBoundary, true, `${scenario.id} no-figure boundary`);
    assert.equal(audit.sitePaper, scenario.colorScheme === "dark" ? "#181714" : "#f3ecd8", `${scenario.id} colour scheme`);
    if (scenario.lang === "en") {
      assert.equal(audit.chineseCharactersOutsideSwitcher, 0, `${scenario.id} untranslated Chinese`);
      assert.match(audit.h1, /Background-shear packing false positive/);
      assert.equal(audit.switcher, "中文");
      assert.ok(audit.chinesePdfLabels >= 1, `${scenario.id} Chinese-PDF label`);
    } else {
      assert.match(audit.h1, /背景剪切的 packing 假阳性/);
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
  if (server) await new Promise((resolvePromise) => server.close(resolvePromise));
}

process.stdout.write(`${JSON.stringify({ status: "PASS", baseUrl: baseUrl.href, pageChecks: results.length, scenarios: results }, null, 2)}\n`);
