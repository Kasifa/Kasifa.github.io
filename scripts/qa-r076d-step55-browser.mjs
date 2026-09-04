#!/usr/bin/env node

import assert from "node:assert/strict";
import { createReadStream } from "node:fs";
import { mkdir } from "node:fs/promises";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { extname, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const outputRoot = resolve(process.env.R076D_STEP55_BROWSER_QA_OUTPUT ?? "/tmp/r076d-step55-browser-qa");
const externalBase = process.env.R076D_PUBLIC_BASE_URL;
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
  path: "/notes/r0-76d.html",
  h1Zh: /精确剪切的定量增长模态熵窗口/,
  h1En: /Quantitative growing-mode entropy window for exact shears/i,
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
    url.searchParams.set("qa", "r076d-step55");
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
        step55MathJaxErrors: document.querySelectorAll("#s-433 mjx-merror, #s-434 mjx-merror, #s-435 mjx-merror, #s-436 mjx-merror, #s-437 mjx-merror, #s-438 mjx-merror, #s-439 mjx-merror, #s-440 mjx-merror, #s-441 mjx-merror").length,
        rawInlineDelimiters: (visibleText.match(/\\\(/g) ?? []).length,
        rawDisplayDelimiters: (visibleText.match(/\\\[/g) ?? []).length,
        chineseCharactersOutsideSwitcher: (visibleText.match(/[\u3400-\u9fff\uf900-\ufaff]/gu) ?? []).length,
        chineseTextSamples: [...bodyCopy.querySelectorAll("*")]
          .filter((node) => node.children.length === 0 && /[\u3400-\u9fff\uf900-\ufaff]/u.test(node.textContent ?? ""))
          .slice(0, 12)
          .map((node) => node.textContent.trim().slice(0, 240)),
        imageCount: document.images.length,
        figureSections: document.querySelectorAll('#figure, [src*="assets/r076d"], [href*="assets/r076d"]').length,
        exactShear: /EXACT REAL CONSTANT SHEAR|exact real constant-shear|精确剪切/i.test(visibleText),
        modalEntropy: /EXP\(C Q LOG\(Q\+1\)\)|exp\(C_\* q log\(q\+1\)\)|模态熵/i.test(visibleText),
        growingWindow: /GROWING-MODE WINDOW|q\(L\) log\(q\(L\)\+1\)=o\(L\^2\)|增长窗口/i.test(visibleText),
        alphaPlusQ: /ALPHA\+Q DERIVATIVE|alpha\+q|空间导数/i.test(visibleText),
        endpointFactor: /\(5\/4\)\^M ENDPOINT|\(5\/4\)\^m|endpoint comparison/i.test(visibleText),
        factorialTail: /COUNTED FACTORIAL TAIL|\(m\+1\)!\/4|factorial tail/i.test(visibleText),
        weightedPower: /LAMBDA\^\(-1\/3\) WEIGHTED|lambda\^\(-1\/3\)|lambda 的正确幂/i.test(visibleText),
        terminalPower: /LAMBDA\^0 TERMINAL|terminal[^\n]{0,80}lambda\^0|终端[^\n]{0,80}lambda\^0/i.test(visibleText),
        completeSquare: /COMPLETE REAL SQUARE|complete real square|完整实场平方/i.test(visibleText),
        externalInputs: /Turan--Nazarov[^\n]{0,120}Erdelyi[^\n]{0,120}(?:external inputs|外部输入)/i.test(visibleText),
        localDeductions: /(?:placement|spatial placement)[^\n]{0,200}factorial tail[^\n]{0,200}(?:scale conversion|尺度换算)/i.test(visibleText),
        finiteBoundary: /finite certificate[^\n]{0,100}(?:not a continuum proof|does not replace|不是 continuum proof)|有限证书[^\n]{0,100}(?:不替代|不是)/i.test(visibleText),
        arbitraryPacketsOpen: /arbitrary growing packets[^\n]{0,180}(?:OPEN|open|remain)|任意增长包[^\n]{0,180}(?:开放|仍开放)/i.test(visibleText),
        versionM: /B!=0 VERSION-M CONDITIONAL|when B!=0[^\n]{0,200}Version-M|当 B!=0[^\n]{0,200}Version-M/i.test(visibleText),
        noveltyBoundary: /NO NOVELTY CLAIM/.test(visibleText),
        clayBoundary: /NOT CLAY/.test(visibleText),
      };
    });

    assert.equal(audit.selectedLanguage, scenario.lang, `${id} selected language`);
    assert.equal(audit.documentLanguage, scenario.lang === "en" ? "en" : "zh-CN", `${id} document language`);
    assert.equal(audit.horizontalOverflow, false, `${id} horizontal overflow ${audit.scrollWidth}/${audit.viewportWidth}`);
    assert.ok(audit.mathJaxContainers > 100, `${id} MathJax coverage`);
    assert.equal(audit.step55MathJaxErrors, 0, `${id} Step 55 MathJax errors`);
    assert.equal(audit.pageWideMathJaxErrors, scenario.lang === "en" ? 6 : 0, `${id} inherited page-wide MathJax errors`);
    assert.equal(audit.rawInlineDelimiters, 0, `${id} raw inline TeX`);
    assert.equal(audit.rawDisplayDelimiters, 0, `${id} raw display TeX`);
    assert.equal(audit.imageCount, 0, `${id} analytic publication has no images`);
    assert.equal(audit.figureSections, 0, `${id} no R0.76D formal figure`);
    for (const key of ["exactShear", "modalEntropy", "growingWindow", "alphaPlusQ", "endpointFactor", "factorialTail", "weightedPower", "terminalPower", "completeSquare", "externalInputs", "localDeductions", "finiteBoundary", "arbitraryPacketsOpen", "versionM", "noveltyBoundary", "clayBoundary"])
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
    await page.evaluate(() => window.scrollTo(0, 0));
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
