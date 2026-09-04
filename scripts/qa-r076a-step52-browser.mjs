#!/usr/bin/env node

import assert from "node:assert/strict";
import { createReadStream } from "node:fs";
import { mkdir } from "node:fs/promises";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { extname, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const outputRoot = resolve(process.env.R076A_STEP52_BROWSER_QA_OUTPUT ?? "/tmp/r076a-step52-browser-qa");
const externalBase = process.env.R076A_PUBLIC_BASE_URL;
const require = createRequire(import.meta.url);
const { chromium } = require(
  "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright",
);

function contentType(filePath) {
  return new Map([
    [".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"],
    [".css", "text/css; charset=utf-8"], [".svg", "image/svg+xml"],
    [".png", "image/png"], [".pdf", "application/pdf"], [".json", "application/json"],
    [".md", "text/markdown; charset=utf-8"], [".csv", "text/csv; charset=utf-8"],
  ]).get(extname(filePath).toLowerCase()) ?? "application/octet-stream";
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
    if (!target.startsWith(`${publicRoot}/`)) {
      response.writeHead(403).end();
      return;
    }
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
const target = {
  id: "note",
  path: "/notes/r0-76a.html",
  h1Zh: /完整时钟局部载频电流负号障碍/,
  h1En: /Complete-clock localized carrier-current sign obstruction/i,
};
const results = [];

try {
  for (const scenario of scenarios) {
    const id = `${target.id}-${scenario.id}`;
    const context = await browser.newContext({
      viewport: scenario.viewport,
      colorScheme: scenario.colorScheme,
      locale: scenario.lang === "zh" ? "zh-CN" : "en-US",
      deviceScaleFactor: 1,
    });
    const page = await context.newPage();
    const pageErrors = [];
    page.on("pageerror", (error) => pageErrors.push(error.message));
    const url = new URL(target.path, baseUrl);
    url.searchParams.set("lang", scenario.lang);
    url.searchParams.set("qa", "r076a-step52");
    const response = await page.goto(url.href, { waitUntil: "networkidle" });
    assert.equal(response?.status(), 200, `${id} main document`);
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
        pageWideMathJaxErrors: document.querySelectorAll("mjx-merror").length,
        step52MathJaxErrors: document.querySelectorAll("#s-409 mjx-merror, #s-410 mjx-merror, #s-411 mjx-merror, #s-412 mjx-merror, #s-413 mjx-merror, #s-414 mjx-merror, #s-415 mjx-merror").length,
        rawInlineDelimiters: (visibleText.match(/\\\(/g) ?? []).length,
        rawDisplayDelimiters: (visibleText.match(/\\\[/g) ?? []).length,
        chineseCharactersOutsideSwitcher: (visibleText.match(/[\u3400-\u9fff\uf900-\ufaff]/gu) ?? []).length,
        chineseTextSamples: [...bodyCopy.querySelectorAll("*")]
          .filter((node) => node.children.length === 0 && /[\u3400-\u9fff\uf900-\ufaff]/u.test(node.textContent ?? ""))
          .slice(0, 12)
          .map((node) => node.textContent.trim().slice(0, 240)),
        imageCount: document.images.length,
        figureSections: document.querySelectorAll('#figure, [src*="assets/r076a"], [href*="assets/r076a"]').length,
        profileAssumption: /0 < DELTA_0 < DELTA|0<delta_0<delta|ZERO_LT_DELTA0_LT_DELTA/i.test(visibleText),
        completeClock: /COMPLETE CLOCK|complete-clock|完整时钟/i.test(visibleText),
        strictCurrent: /LOCAL CURRENT STRICTLY NEGATIVE|localized current[^\n]{0,120}strict[^\n]{0,30}negative|局部载频电流[^\n]{0,80}严格为负/i.test(visibleText),
        strictCorrection: /CORRECTION ROW STRICTLY NEGATIVE|correction row[^\n]{0,120}strict[^\n]{0,30}negative/i.test(visibleText),
        densityRetained: /CARRIER DENSITY RETAINED|positive carrier-density row[^\n]{0,80}retained|保留 positive carrier-density row/i.test(visibleText),
        signDroppingOnly: /SIGN-DROPPING CLOSED|SIGN-DROPPING ONLY|sign-dropping[^\n]{0,120}(?:only|closed)|只排除[^\n]{0,120}sign-dropping/i.test(visibleText),
        wIntact: /W TWO-MODE PAYMENT INTACT|W[^\n]{0,80}two-mode[^\n]{0,80}(?:intact|valid)|W 的[^\n]{0,80}两模态通量[^\n]{0,80}(?:保持|不受影响)/i.test(visibleText),
        generalPaymentOpen: /GENERAL CLUSTER PAYMENT|general cluster payment[^\n]{0,100}(?:OPEN|open)|一般簇支付[^\n]{0,80}开放/i.test(visibleText),
        versionM: /VERSION-M CONDITIONAL|Version-M[^\n]{0,160}(?:conditional|requires|要求)/i.test(visibleText),
        noveltyBoundary: /NO NOVELTY CLAIM/.test(visibleText),
        clayBoundary: /NOT CLAY/.test(visibleText),
      };
    });

    assert.equal(audit.selectedLanguage, scenario.lang, `${id} selected language`);
    assert.equal(audit.documentLanguage, scenario.lang === "en" ? "en" : "zh-CN", `${id} document language`);
    assert.equal(audit.horizontalOverflow, false, `${id} horizontal overflow ${audit.scrollWidth}/${audit.viewportWidth}`);
    assert.ok(audit.mathJaxContainers > 100, `${id} MathJax coverage`);
    assert.equal(audit.step52MathJaxErrors, 0, `${id} Step 52 MathJax errors`);
    assert.equal(audit.pageWideMathJaxErrors, scenario.lang === "en" ? 6 : 0, `${id} inherited page-wide MathJax errors`);
    assert.equal(audit.rawInlineDelimiters, 0, `${id} raw inline TeX`);
    assert.equal(audit.rawDisplayDelimiters, 0, `${id} raw display TeX`);
    assert.equal(audit.imageCount, 0, `${id} analytic publication has no images`);
    assert.equal(audit.figureSections, 0, `${id} no R0.76A formal figure`);
    for (const key of ["profileAssumption", "completeClock", "strictCurrent", "strictCorrection", "densityRetained", "signDroppingOnly", "wIntact", "generalPaymentOpen", "versionM", "noveltyBoundary", "clayBoundary"])
      assert.equal(audit[key], true, `${id} ${key}`);
    assert.equal(audit.sitePaper, scenario.colorScheme === "dark" ? "#181714" : "#f3ecd8", `${id} colour scheme`);
    if (scenario.lang === "en") {
      assert.equal(audit.chineseCharactersOutsideSwitcher, 0, `${id} untranslated Chinese: ${JSON.stringify(audit.chineseTextSamples)}`);
      assert.match(audit.h1, target.h1En);
      assert.equal(audit.switcher, "中文");
    } else {
      assert.match(audit.h1, target.h1Zh);
      assert.equal(audit.switcher, "English");
    }
    assert.deepEqual(pageErrors, [], `${id} page errors`);
    const screenshot = resolve(outputRoot, `${id}.png`);
    await page.screenshot({ path: screenshot, fullPage: false });
    results.push({ target: target.id, ...scenario, screenshot, ...audit, pageErrors });
    await context.close();
  }
} finally {
  await browser.close();
  if (server) await new Promise((resolvePromise) => server.close(resolvePromise));
}

process.stdout.write(`${JSON.stringify({ status: "PASS", baseUrl: baseUrl.href, pageChecks: results.length, scenarios: results }, null, 2)}\n`);
