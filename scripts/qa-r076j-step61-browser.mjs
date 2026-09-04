#!/usr/bin/env node

import assert from "node:assert/strict";
import { createReadStream } from "node:fs";
import { mkdir } from "node:fs/promises";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { extname, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const outputRoot = resolve(process.env.R076J_STEP61_BROWSER_QA_OUTPUT ?? "/tmp/r076j-step61-browser-qa");
const externalBase = process.env.R076J_PUBLIC_BASE_URL;
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
  { id: "note", path: "/notes/r0-76j.html", minMath: 120,
    h1Zh: /本地重构端点外推并解除 exact-shear 窗口的文献条件/,
    h1En: /Local endpoint extrapolation removes the literature condition/i },
  { id: "recap", path: "/recap-r0-61-r0-76i.html", minMath: 1,
    h1Zh: /从 exp\(Cq\) 障碍到条件性切比雪夫尺度窗口/,
    h1En: /From the exp\(Cq\) barrier to a conditional Chebyshev-scale window/i },
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
    url.searchParams.set("lang", scenario.lang); url.searchParams.set("qa", "r076j-step61");
    const response = await page.goto(url.href, { waitUntil: "networkidle" });
    assert.equal(response?.status(), 200, `${id} main document`);
    await page.waitForFunction(() => document.documentElement.dataset.language);
    await page.waitForFunction(() => typeof globalThis.MathJax?.version === "string" && Boolean(globalThis.MathJax?.startup?.promise), null, { timeout: 30_000 });
    await page.evaluate(async () => { await document.fonts.ready; await globalThis.MathJax.startup.promise; });
    const audit = await page.evaluate((targetId) => {
      const body = document.body.cloneNode(true);
      body.querySelectorAll(".language-switcher").forEach((node) => node.remove());
      const text = body.innerText;
      return {
        selectedLanguage: document.documentElement.dataset.language, documentLanguage: document.documentElement.lang,
        h1: document.querySelector("h1")?.textContent?.trim(), switcher: document.querySelector(".language-switcher")?.textContent?.trim(),
        sitePaper: getComputedStyle(document.documentElement).getPropertyValue("--paper").trim(),
        overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
        math: document.querySelectorAll("mjx-container").length,
        jErrors: document.querySelectorAll("#s-481 mjx-merror,#s-482 mjx-merror,#s-483 mjx-merror,#s-484 mjx-merror,#s-485 mjx-merror,#s-486 mjx-merror,#s-487 mjx-merror,#s-488 mjx-merror").length,
        rawInline: (text.match(/\\\(/g) ?? []).length, rawDisplay: (text.match(/\\\[/g) ?? []).length,
        chinese: (text.match(/[\u3400-\u9fff\uf900-\ufaff]/gu) ?? []).length,
        chineseSamples: [...body.querySelectorAll("*")].filter((node) => node.children.length === 0 && /[\u3400-\u9fff\uf900-\ufaff]/u.test(node.textContent ?? "")).slice(0, 10).map((node) => node.textContent.trim().slice(0, 200)),
        imageCount: document.images.length, figureLeak: document.querySelectorAll('#figure,[src*="assets/r076j"],[href*="assets/r076j"]').length,
        localTheorem: /PROVED LOCALLY FROM ESTABLISHED LITERATURE/i.test(text),
        historicalI: /CONDITIONAL-LITERATURE/i.test(text), finite: /FINITE COMPUTATION|finite checks/i.test(text),
        open: /\bOPEN\b/i.test(text), window: /q=o\(L\^\(5\/2\)\)/i.test(text), rate: /-2\/11907/.test(text),
        exactScope: /exact real one-band constant shear|exact real one-band constant-shear/i.test(text),
        laterUnauthorized: /Later (?:material|versions?) remain unauthorized|not authorized, unread, and unpublished|后续版本未授权/i.test(text),
        laterLeak: /R0\.76K/i.test(text), clay: /NOT CLAY/.test(text), recapHasJ: targetId === "recap" && /R0\.76J/.test(text),
      };
    }, target.id);
    assert.equal(audit.selectedLanguage, scenario.lang, `${id} language`);
    assert.equal(audit.documentLanguage, scenario.lang === "en" ? "en" : "zh-CN", `${id} document language`);
    assert.equal(audit.overflow, false, `${id} horizontal overflow`);
    assert.ok(audit.math >= target.minMath, `${id} MathJax coverage`);
    assert.equal(audit.jErrors, 0, `${id} J MathJax errors`);
    assert.equal(audit.rawInline, 0, `${id} raw inline TeX`); assert.equal(audit.rawDisplay, 0, `${id} raw display TeX`);
    assert.equal(audit.imageCount, 0, `${id} images`); assert.equal(audit.figureLeak, 0, `${id} figure leak`);
    for (const key of ["historicalI", "open", "window", "rate", "exactScope", "laterUnauthorized", "clay"]) assert.equal(audit[key], true, `${id} ${key}`);
    if (target.id === "note") for (const key of ["localTheorem", "finite"]) assert.equal(audit[key], true, `${id} ${key}`);
    assert.equal(audit.laterLeak, false, `${id} later release leak`); assert.equal(audit.recapHasJ, false, `${id} recap endpoint drift`);
    assert.equal(audit.sitePaper, scenario.colorScheme === "dark" ? "#181714" : "#f3ecd8", `${id} colour scheme`);
    if (scenario.lang === "en") { assert.equal(audit.chinese, 0, `${id} untranslated Chinese: ${JSON.stringify(audit.chineseSamples)}`); assert.match(audit.h1, target.h1En); assert.equal(audit.switcher, "中文"); }
    else { assert.match(audit.h1, target.h1Zh); assert.equal(audit.switcher, "English"); }
    assert.deepEqual(pageErrors, [], `${id} page errors`);
    const screenshot = resolve(outputRoot, `${id}.png`); await page.screenshot({ path: screenshot, fullPage: false });
    results.push({ target: target.id, scenario: scenario.id, screenshot, ...audit, pageErrors });
    await context.close();
  }
} finally {
  await browser.close();
  if (server) await new Promise((ok) => server.close(ok));
}
process.stdout.write(`${JSON.stringify({ status: "PASS", baseUrl: baseUrl.href, pageChecks: results.length, scenarios: results }, null, 2)}\n`);
