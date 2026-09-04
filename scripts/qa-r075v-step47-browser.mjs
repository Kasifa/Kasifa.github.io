#!/usr/bin/env node

import assert from "node:assert/strict";
import { createReadStream } from "node:fs";
import { mkdir } from "node:fs/promises";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { extname, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const outputRoot = resolve(process.env.R075V_STEP47_BROWSER_QA_OUTPUT ?? "/tmp/r075v-step47-browser-qa");
const externalBase = process.env.R075V_PUBLIC_BASE_URL;
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
const targets = [
  { id: "note", path: "/notes/r0-75v.html", h1Zh: /单个 dyadic 二谐波剪切的完整 signed-flux 付款/, h1En: /Complete signed-flux payment for one dyadic two-harmonic shear/ },
  { id: "recap", path: "/recap-r0-61-r0-75v.html", h1Zh: /exact high-carrier pair 的完整 signed flux/, h1En: /complete signed flux for an exact high-carrier pair/i },
];
const results = [];

try {
  for (const scenario of scenarios) {
    for (const target of targets) {
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
      url.searchParams.set("qa", "r075v-step47");
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
          step47MathJaxErrors: document.querySelectorAll("#s-364 mjx-merror, #s-365 mjx-merror, #s-366 mjx-merror, #s-367 mjx-merror, #s-368 mjx-merror, #s-369 mjx-merror, #s-370 mjx-merror, #s-371 mjx-merror, #s-372 mjx-merror, #s-373 mjx-merror").length,
          rawInlineDelimiters: (visibleText.match(/\\\(/g) ?? []).length,
          rawDisplayDelimiters: (visibleText.match(/\\\[/g) ?? []).length,
          chineseCharactersOutsideSwitcher: (visibleText.match(/[\u3400-\u9fff\uf900-\ufaff]/gu) ?? []).length,
          chineseTextSamples: [...bodyCopy.querySelectorAll("*")]
            .filter((node) => node.children.length === 0 && /[\u3400-\u9fff\uf900-\ufaff]/u.test(node.textContent ?? ""))
            .slice(0, 12)
            .map((node) => node.textContent.trim().slice(0, 240)),
          imageCount: document.images.length,
          figureSections: document.querySelectorAll('#figure, [src*="assets/r075v"], [href*="assets/r075v"]').length,
          exactPair: /EXACTLY TWO HARMONICS|exact high-carrier pair/i.test(visibleText),
          selfSumPaid: /SELF \+ SUM BLOCK PAID|coupled self\/sum payment/i.test(visibleText),
          fullFlux: /FULL EXACT-PAIR FLUX|complete signed flux|完整 signed flux/i.test(visibleText),
          tuv: /T[^\n]*spatial coercivity[\s\S]*U[^\n]*difference[\s\S]*V/i.test(visibleText),
          noveltyBoundary: /NO NOVELTY CLAIM/.test(visibleText),
          clayBoundary: /NOT CLAY/.test(visibleText),
        };
      });

      assert.equal(audit.selectedLanguage, scenario.lang, `${id} selected language`);
      assert.equal(audit.documentLanguage, scenario.lang === "en" ? "en" : "zh-CN", `${id} document language`);
      assert.equal(audit.horizontalOverflow, false, `${id} horizontal overflow ${audit.scrollWidth}/${audit.viewportWidth}`);
      assert.ok(audit.mathJaxContainers > (target.id === "note" ? 100 : 2), `${id} MathJax coverage`);
      if (target.id === "note") assert.equal(audit.step47MathJaxErrors, 0, `${id} Step 47 MathJax errors`);
      else assert.equal(audit.pageWideMathJaxErrors, 0, `${id} recap MathJax errors`);
      assert.equal(audit.rawInlineDelimiters, 0, `${id} raw inline TeX`);
      assert.equal(audit.rawDisplayDelimiters, 0, `${id} raw display TeX`);
      assert.equal(audit.imageCount, 0, `${id} analytic publication has no images`);
      assert.equal(audit.figureSections, 0, `${id} no R0.75V formal figure`);
      for (const key of target.id === "note"
        ? ["exactPair", "selfSumPaid", "fullFlux", "noveltyBoundary", "clayBoundary"]
        : ["exactPair", "selfSumPaid", "fullFlux", "tuv", "noveltyBoundary", "clayBoundary"]
      ) assert.equal(audit[key], true, `${id} ${key}`);
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
  }
} finally {
  await browser.close();
  if (server) await new Promise((resolvePromise) => server.close(resolvePromise));
}

process.stdout.write(`${JSON.stringify({ status: "PASS", baseUrl: baseUrl.href, pageChecks: results.length, scenarios: results }, null, 2)}\n`);
