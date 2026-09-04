#!/usr/bin/env node

import assert from "node:assert/strict";
import { createReadStream } from "node:fs";
import { mkdir } from "node:fs/promises";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { extname, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const outputRoot = resolve(process.env.R075P_STEP41_BROWSER_QA_OUTPUT ?? "/tmp/r075p-step41-browser-qa");
const externalBase = process.env.R075P_PUBLIC_BASE_URL;
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
    const url = new URL("/notes/r0-75p.html", baseUrl);
    url.searchParams.set("lang", scenario.lang);
    url.searchParams.set("qa", "r075p-step41");
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
        pageWideMathJaxErrors: document.querySelectorAll("mjx-merror").length,
        step41MathJaxErrors: document.querySelectorAll("#s-321 mjx-merror, #s-322 mjx-merror, #s-323 mjx-merror, #s-324 mjx-merror, #s-325 mjx-merror, #s-326 mjx-merror, #s-327 mjx-merror").length,
        mathJaxErrorContexts: [...document.querySelectorAll("mjx-merror")].map((node) => ({
          section: node.closest("section")?.id,
          text: node.parentElement?.textContent?.trim().slice(0, 240),
        })),
        rawInlineDelimiters: (visibleText.match(/\\\(/g) ?? []).length,
        rawDisplayDelimiters: (visibleText.match(/\\\[/g) ?? []).length,
        chineseCharactersOutsideSwitcher: (visibleText.match(/[\u3400-\u9fff\uf900-\ufaff]/gu) ?? []).length,
        chineseTextSamples: [...bodyCopy.querySelectorAll("*")]
          .filter((node) => node.children.length === 0 && /[\u3400-\u9fff\uf900-\ufaff]/u.test(node.textContent ?? ""))
          .slice(0, 12)
          .map((node) => node.textContent.trim().slice(0, 240)),
        imageCount: document.images.length,
        figureSections: document.querySelectorAll('#figure, [src*="r075p"], [href*="assets/r075p"]').length,
        constantShear: /CONSTANT SHEAR/.test(visibleText),
        entranceConcentration: /ENTRANCE CONCENTRATION/.test(visibleText),
        movingCutoff: /MOVING CUTOFF/.test(visibleText),
        localEnergyIdentity: /LOCAL ENERGY IDENTITY/.test(visibleText),
        radialPlateauFibres: /RADIAL PLATEAU FIBRES/.test(visibleText),
        collarCubic: /3D COLLAR CUBIC/.test(visibleText),
        muFiveHalves: /MU\^5\/2/.test(visibleText),
        packetGain: /K\^-2\/3 GAIN/.test(visibleText),
        strictThreshold: /SIGMA < 8558\/178605/.test(visibleText),
        strictEndpoint: /STRICT ENDPOINT/.test(visibleText),
        actualComponentOnly: /ACTUAL COMPONENT ONLY/.test(visibleText),
        projectionExcluded: /PROJECTION EXCLUDED/.test(visibleText),
        lowConcentrationOpen: /LOW CONCENTRATION OPEN/.test(visibleText),
        e24Open: /E\.24 OPEN/.test(visibleText),
        noveltyBoundary: /NO NOVELTY CLAIM/.test(visibleText),
        clayBoundary: /NOT CLAY/.test(visibleText),
        noFigureBoundary: /NO FIGURE \/ NO DNS/.test(visibleText),
        chinesePdfLabels: document.querySelectorAll(".pdf-language-label").length,
      };
    });

    assert.equal(audit.selectedLanguage, scenario.lang, `${scenario.id} selected language`);
    assert.equal(audit.documentLanguage, scenario.lang === "en" ? "en" : "zh-CN", `${scenario.id} document language`);
    assert.equal(audit.horizontalOverflow, false, `${scenario.id} horizontal overflow ${audit.scrollWidth}/${audit.viewportWidth}`);
    assert.ok(audit.mathJaxContainers > 100, `${scenario.id} MathJax coverage`);
    assert.equal(audit.step41MathJaxErrors, 0, `${scenario.id} Step 41 MathJax errors: ${JSON.stringify(audit.mathJaxErrorContexts.filter((entry) => /^s-32[1-7]$/.test(entry.section ?? "")))}`);
    assert.equal(audit.rawInlineDelimiters, 0, `${scenario.id} raw inline TeX`);
    assert.equal(audit.rawDisplayDelimiters, 0, `${scenario.id} raw display TeX`);
    assert.equal(audit.imageCount, 0, `${scenario.id} analytic note has no images`);
    assert.equal(audit.figureSections, 0, `${scenario.id} no R0.75P formal figure`);
    for (const key of [
      "constantShear", "entranceConcentration", "movingCutoff", "localEnergyIdentity", "radialPlateauFibres",
      "collarCubic", "muFiveHalves", "packetGain", "strictThreshold", "strictEndpoint",
      "actualComponentOnly", "projectionExcluded", "lowConcentrationOpen", "e24Open",
      "noveltyBoundary", "clayBoundary", "noFigureBoundary",
    ]) assert.equal(audit[key], true, `${scenario.id} ${key}`);
    assert.equal(audit.sitePaper, scenario.colorScheme === "dark" ? "#181714" : "#f3ecd8", `${scenario.id} colour scheme`);
    if (scenario.lang === "en") {
      assert.equal(audit.chineseCharactersOutsideSwitcher, 0, `${scenario.id} untranslated Chinese: ${JSON.stringify(audit.chineseTextSamples)}`);
      assert.match(audit.h1, /Buffered-collar payment/);
      assert.equal(audit.switcher, "中文");
      assert.ok(audit.chinesePdfLabels >= 1, `${scenario.id} Chinese-PDF label`);
    } else {
      assert.match(audit.h1, /入口浓度/);
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
