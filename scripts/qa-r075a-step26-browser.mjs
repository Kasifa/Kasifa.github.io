#!/usr/bin/env node

import assert from "node:assert/strict";
import { createReadStream } from "node:fs";
import { mkdir } from "node:fs/promises";
import { createServer } from "node:http";
import { createRequire } from "node:module";
import { extname, resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const outputRoot = resolve(process.env.R075A_STEP26_BROWSER_QA_OUTPUT ?? "/tmp/r075a-step26-browser-qa");
const externalBase = process.env.R075A_PUBLIC_BASE_URL;
const figureId = "fig-r075a-local-persistence-payment";
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
const documents = [
  { kind: "note", path: "/notes/r0-75a.html" },
  { kind: "recap", path: "/recap-r0-61-r0-75a.html" },
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
    for (const document of documents) {
      const page = await context.newPage();
      const pageErrors = [];
      page.on("pageerror", (error) => pageErrors.push(error.message));
      const url = new URL(document.path, baseUrl);
      url.searchParams.set("lang", scenario.lang);
      url.searchParams.set("qa", "r075a-step26");
      const response = await page.goto(url.href, { waitUntil: "networkidle" });
      assert.equal(response?.status(), 200, `${scenario.id} ${document.kind}`);
      await page.waitForFunction(() => document.documentElement.dataset.language);
      await page.waitForFunction(
        () => typeof globalThis.MathJax?.version === "string" && Boolean(globalThis.MathJax?.startup?.promise),
        null,
        { timeout: 30_000 },
      );
      await page.evaluate(async () => {
        await document.fonts.ready;
        await globalThis.MathJax.startup.promise;
        await Promise.all([...document.images].map((image) => image.complete
          ? Promise.resolve()
          : new Promise((resolvePromise) => image.addEventListener("load", resolvePromise, { once: true }))));
      });

      const audit = await page.evaluate(({ expectedFigureId, kind }) => {
        const bodyCopy = document.body.cloneNode(true);
        bodyCopy.querySelectorAll(".language-switcher").forEach((node) => node.remove());
        const visibleText = bodyCopy.innerText;
        const style = getComputedStyle(document.documentElement);
        const figureImage = document.querySelector(`#figure img[src*="${expectedFigureId}"]`);
        const nodeIndex = document.querySelector(".node-links");
        return {
          kind,
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
          figureSections: document.querySelectorAll("#figure").length,
          figureLoaded: Boolean(figureImage?.complete && figureImage?.naturalWidth > 0),
          figureCurrentSource: figureImage?.currentSrc ?? "",
          localDichotomy: /LOCAL DICHOTOMY|local persistence\/payment dichotomy|\u5c40\u90e8\u6301\u7eed.{0,20}\u4ed8\u6b3e\u4e8c\u5206/i.test(visibleText),
          completeClockOpen: /complete K|complete[- ]clock|\u5b8c\u6574 K/i.test(visibleText) && /OPEN/.test(visibleText),
          noveltyBoundary: /NO NOVELTY CLAIM|not novelty evidence|\u4e0d\u8bc1\u660e novelty/i.test(visibleText),
          clayBoundary: /NOT CLAY/.test(visibleText),
          cardCount: document.querySelectorAll("article.card.node").length,
          nodeLinkCount: nodeIndex?.querySelectorAll('a[href^="/notes/r0-"][href$=".html"]').length ?? 0,
          a63Open: /A\.63/.test(visibleText) && /OPEN|\u5f00\u653e/.test(visibleText),
          chinesePdfLabels: document.querySelectorAll(".pdf-language-label").length,
        };
      }, { expectedFigureId: figureId, kind: document.kind });

      assert.equal(audit.selectedLanguage, scenario.lang, `${scenario.id} ${document.kind} selected language`);
      assert.equal(audit.documentLanguage, scenario.lang === "en" ? "en" : "zh-CN", `${scenario.id} ${document.kind} document language`);
      assert.equal(audit.horizontalOverflow, false, `${scenario.id} ${document.kind} horizontal overflow ${audit.scrollWidth}/${audit.viewportWidth}`);
      assert.equal(audit.rawInlineDelimiters, 0, `${scenario.id} ${document.kind} raw inline TeX`);
      assert.equal(audit.rawDisplayDelimiters, 0, `${scenario.id} ${document.kind} raw display TeX`);
      assert.equal(audit.localDichotomy, true, `${scenario.id} ${document.kind} local dichotomy`);
      assert.equal(audit.completeClockOpen, true, `${scenario.id} ${document.kind} complete-clock boundary`);
      assert.equal(audit.noveltyBoundary, true, `${scenario.id} ${document.kind} novelty boundary`);
      assert.equal(audit.clayBoundary, true, `${scenario.id} ${document.kind} Clay boundary`);
      assert.equal(audit.a63Open, true, `${scenario.id} ${document.kind} A.63 open boundary`);
      assert.equal(audit.sitePaper, scenario.colorScheme === "dark" ? "#181714" : "#f3ecd8", `${scenario.id} ${document.kind} colour scheme`);
      if (document.kind === "note") {
        assert.ok(audit.mathJaxContainers > 100, `${scenario.id} note MathJax coverage`);
        assert.equal(audit.imageCount, 1, `${scenario.id} one formal figure image`);
        assert.equal(audit.figureSections, 1, `${scenario.id} one formal figure section`);
        assert.equal(audit.figureLoaded, true, `${scenario.id} formal figure loaded`);
        assert.match(audit.figureCurrentSource, /r075a\/fig-r075a-local-persistence-payment\.svg/);
      } else {
        assert.ok(audit.mathJaxContainers >= 3, `${scenario.id} recap MathJax coverage`);
        assert.equal(audit.cardCount, 12, `${scenario.id} P-A cards`);
        assert.equal(audit.nodeLinkCount, 169, `${scenario.id} cumulative node index`);
      }
      if (scenario.lang === "en") {
        assert.equal(audit.chineseCharactersOutsideSwitcher, 0, `${scenario.id} ${document.kind} untranslated Chinese`);
        assert.equal(audit.switcher, "中文");
        if (document.kind === "note") assert.ok(audit.chinesePdfLabels >= 1, `${scenario.id} Chinese-PDF label`);
      } else {
        assert.equal(audit.switcher, "English");
        if (document.kind === "note") assert.equal(audit.chinesePdfLabels, 0);
      }
      assert.deepEqual(pageErrors, [], `${scenario.id} ${document.kind} page errors`);
      const screenshot = resolve(outputRoot, `${scenario.id}-${document.kind}.png`);
      await page.screenshot({ path: screenshot, fullPage: false });
      results.push({ ...scenario, ...audit, screenshot, pageErrors });
      await page.close();
    }
    await context.close();
  }
} finally {
  await browser.close();
  if (server) await new Promise((resolvePromise) => server.close(resolvePromise));
}

process.stdout.write(`${JSON.stringify({ status: "PASS", baseUrl: baseUrl.href, pageChecks: results.length, scenarios: results }, null, 2)}\n`);
