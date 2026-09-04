#!/usr/bin/env node

import assert from "node:assert/strict";
import { createReadStream } from "node:fs";
import { mkdir } from "node:fs/promises";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { extname, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const outputRoot = resolve(process.env.R076I_STEP60_BROWSER_QA_OUTPUT ?? "/tmp/r076i-step60-browser-qa");
const externalBase = process.env.R076I_PUBLIC_BASE_URL;
const require = createRequire(import.meta.url);
const { chromium } = require("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");

const types = new Map([[".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"], [".css", "text/css; charset=utf-8"], [".pdf", "application/pdf"], [".json", "application/json"]]);
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
  await new Promise((ok, fail) => { server.once("error", fail); server.listen(0, "127.0.0.1", ok); });
  baseUrl = new URL(`http://127.0.0.1:${server.address().port}/`);
}

const targets = [
  {
    id: "note", path: "/notes/r0-76i.html", minMath: 100,
    h1Zh: /切比雪夫尺度的完整平台增长模态窗口/,
    h1En: /Chebyshev-scale growing-mode window on the full plateau/i,
  },
  {
    id: "recap", path: "/recap-r0-61-r0-76i.html", minMath: 1,
    h1Zh: /从 exp\(Cq\) 障碍到条件性切比雪夫尺度窗口/,
    h1En: /From the exp\(Cq\) barrier to a conditional Chebyshev-scale window/i,
  },
];
const scenarios = [
  { id: "desktop-light-zh", viewport: { width: 1440, height: 900 }, colorScheme: "light", lang: "zh" },
  { id: "desktop-dark-en", viewport: { width: 1440, height: 900 }, colorScheme: "dark", lang: "en" },
  { id: "mobile-light-en", viewport: { width: 390, height: 844 }, colorScheme: "light", lang: "en" },
  { id: "mobile-dark-zh", viewport: { width: 390, height: 844 }, colorScheme: "dark", lang: "zh" },
];

await mkdir(outputRoot, { recursive: true });
const browser = await chromium.launch({ executablePath: "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome", headless: true });
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
    url.searchParams.set("qa", "r076i-step60");
    const response = await page.goto(url.href, { waitUntil: "networkidle" });
    assert.equal(response?.status(), 200, `${id} main document`);
    const staticHtml = await response.text();
    await page.waitForFunction(() => document.documentElement.dataset.language);
    await page.waitForFunction(() => typeof globalThis.MathJax?.version === "string" && Boolean(globalThis.MathJax?.startup?.promise), null, { timeout: 30_000 });
    await page.evaluate(async () => { await document.fonts.ready; await globalThis.MathJax.startup.promise; });
    const audit = await page.evaluate((staticHtml) => {
      const bodyCopy = document.body.cloneNode(true);
      bodyCopy.querySelectorAll(".language-switcher").forEach((node) => node.remove());
      const text = bodyCopy.innerText;
      const source = document.body.innerHTML;
      return {
        selectedLanguage: document.documentElement.dataset.language,
        documentLanguage: document.documentElement.lang,
        h1: document.querySelector("h1")?.textContent?.trim(),
        switcher: document.querySelector(".language-switcher")?.textContent?.trim(),
        sitePaper: getComputedStyle(document.documentElement).getPropertyValue("--paper").trim(),
        horizontalOverflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        viewportWidth: window.innerWidth,
        scrollWidth: document.documentElement.scrollWidth,
        mathJaxContainers: document.querySelectorAll("mjx-container").length,
        pageWideMathJaxErrors: document.querySelectorAll("mjx-merror").length,
        step60MathJaxErrors: document.querySelectorAll("#s-472 mjx-merror, #s-473 mjx-merror, #s-474 mjx-merror, #s-475 mjx-merror, #s-476 mjx-merror, #s-477 mjx-merror, #s-478 mjx-merror, #s-479 mjx-merror, #s-480 mjx-merror, #i-window mjx-merror").length,
        rawInlineDelimiters: (text.match(/\\\(/g) ?? []).length,
        rawDisplayDelimiters: (text.match(/\\\[/g) ?? []).length,
        chineseCharactersOutsideSwitcher: (text.match(/[\u3400-\u9fff\uf900-\ufaff]/gu) ?? []).length,
        chineseTextSamples: [...bodyCopy.querySelectorAll("*")].filter((node) => node.children.length === 0 && /[\u3400-\u9fff\uf900-\ufaff]/u.test(node.textContent ?? "")).slice(0, 8).map((node) => node.textContent.trim().slice(0, 180)),
        imageCount: document.images.length,
        figureLeak: document.querySelectorAll('#figure, [src*="assets/r076i"], [href*="assets/r076i"]').length,
        literature: /LITERATURE/i.test(text),
        provedLocally: /PROVED LOCALLY/i.test(text),
        conditional: /CONDITIONAL-LITERATURE/i.test(text),
        finite: /FINITE COMPUTATION|finite checks/i.test(text),
        open: /\bOPEN\b/i.test(text),
        zhang: /Zhang[^\n]{0,100}Proposition 4\.2/i.test(text),
        chebyshevWindow: /q=o\(L\^\(5\/2\)\)/i.test(text),
        spatialCost: /q[²2][^\n]{0,80}exp\(12√2q√Δ_a\)|q\^2[^\n]{0,120}(?:exp\(?|e\^\{?)12(?:√2|\\sqrt2)/i.test(`${text}\n${source}\n${staticHtml}`),
        completeCost: /q[⁷7][^\n]{0,80}exp\(12√2q√Δ_a\)|q\^7[^\n]{0,120}(?:exp\(?|e\^\{?)12(?:√2|\\sqrt2)/i.test(`${text}\n${source}\n${staticHtml}`),
        normalizedRate: /-2\/11907/.test(text),
        exactScope: /exact real one-band constant shear|exact real one-band constant-shear/i.test(text),
        noFullSharpness: /NO FULL-CLASS SHARPNESS CLAIM|does not prove sharpness of I\.5/i.test(text),
        laterUnauthorized: /Later (?:material|versions?) remain unauthorized|not authorized, unread, and unpublished|后续版本未授权/i.test(text),
        laterReleaseLeak: /R0\.76J/i.test(text),
        clayBoundary: /NOT CLAY/.test(text),
      };
    }, staticHtml);
    assert.equal(audit.selectedLanguage, scenario.lang, `${id} selected language`);
    assert.equal(audit.documentLanguage, scenario.lang === "en" ? "en" : "zh-CN", `${id} document language`);
    assert.equal(audit.horizontalOverflow, false, `${id} horizontal overflow ${audit.scrollWidth}/${audit.viewportWidth}`);
    assert.ok(audit.mathJaxContainers >= target.minMath, `${id} MathJax coverage`);
    assert.equal(audit.step60MathJaxErrors, 0, `${id} Step 60 MathJax errors`);
    assert.equal(audit.pageWideMathJaxErrors, target.id === "note" && scenario.lang === "en" ? 6 : 0, `${id} inherited page-wide MathJax errors`);
    assert.equal(audit.rawInlineDelimiters, 0, `${id} raw inline TeX`);
    assert.equal(audit.rawDisplayDelimiters, 0, `${id} raw display TeX`);
    assert.equal(audit.imageCount, 0, `${id} analytic publication has no images`);
    assert.equal(audit.figureLeak, 0, `${id} no formal figure`);
    for (const key of ["literature", "provedLocally", "conditional", "finite", "open", "zhang", "chebyshevWindow", "completeCost", "normalizedRate", "exactScope", "noFullSharpness", "laterUnauthorized", "clayBoundary"]) assert.equal(audit[key], true, `${id} ${key}`);
    if (target.id === "note") assert.equal(audit.spatialCost, true, `${id} spatialCost`);
    assert.equal(audit.laterReleaseLeak, false, `${id} later release leakage`);
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
  if (server) await new Promise((ok) => server.close(ok));
}

process.stdout.write(`${JSON.stringify({ status: "PASS", baseUrl: baseUrl.href, pageChecks: results.length, scenarios: results }, null, 2)}\n`);
