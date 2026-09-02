#!/usr/bin/env node

import { mkdir, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { resolve } from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");
const executablePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const base = process.argv[2] ?? "http://127.0.0.1:4179";
const output = process.argv[3] ?? "/private/tmp/r074n-browser-qa";
await mkdir(output, { recursive: true });

const browser = await chromium.launch({ executablePath, headless: true });
const cases = [
  { id: "note-zh-desktop", path: "/notes/r0-74n.html?lang=zh", width: 1440, height: 1000, lang: "zh" },
  { id: "note-en-desktop", path: "/notes/r0-74n.html?lang=en", width: 1440, height: 1000, lang: "en" },
  { id: "note-zh-mobile", path: "/notes/r0-74n.html?lang=zh", width: 390, height: 844, lang: "zh" },
  { id: "note-en-mobile", path: "/notes/r0-74n.html?lang=en", width: 390, height: 844, lang: "en" },
  { id: "home-zh-desktop", path: "/research-review.html?lang=zh#r074n", width: 1440, height: 1000, lang: "zh" },
  { id: "home-en-mobile", path: "/research-review.html?lang=en#r074n", width: 390, height: 844, lang: "en" },
];
const results = [];
try {
  for (const item of cases) {
    const context = await browser.newContext({ viewport: { width: item.width, height: item.height } });
    const page = await context.newPage();
    const failures = [];
    page.on("requestfailed", (request) => failures.push({ url: request.url(), error: request.failure()?.errorText ?? "unknown" }));
    await page.goto(base + item.path, { waitUntil: "networkidle", timeout: 30000 });
    if (item.id.startsWith("note-")) {
      await page.waitForFunction(() => document.querySelectorAll("mjx-container").length >= 7, null, { timeout: 20000 });
    }
    await page.screenshot({ path: resolve(output, `${item.id}.png`), fullPage: true });
    const state = await page.evaluate(({ expectedLang, isNote }) => {
      const body = document.body.innerText;
      const englishResidue = expectedLang === "en" ? body.replace(/中文/g, "").match(/[\u3400-\u9fff\uf900-\ufaff]/g) ?? [] : [];
      const card = document.querySelector('[data-release="r074n"]');
      return {
        title: document.title,
        documentLang: document.documentElement.lang,
        h1: document.querySelector("h1")?.innerText ?? null,
        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        scrollWidth: document.documentElement.scrollWidth,
        clientWidth: document.documentElement.clientWidth,
        bodyWidth: document.body.getBoundingClientRect().width,
        mathCount: document.querySelectorAll("mjx-container").length,
        rawTexVisible: /\\\[|\\\]|\\\(|\\\)/.test(body),
        images: [...document.images].map((image) => ({ src: image.currentSrc || image.src, complete: image.complete, naturalWidth: image.naturalWidth })),
        evidenceLabels: [...document.querySelectorAll(".label")].map((node) => node.textContent.trim()),
        englishChineseResidueCount: englishResidue.length,
        exactLawVisible: !isNote || Boolean(document.querySelector("#s-04 .equation mjx-container")?.getBoundingClientRect().width),
        noDissipationLowerBoundVisible: /no matching lower bound|没有匹配下界/i.test(body) || !isNote,
        notClayVisible: body.includes("NOT CLAY") || !isNote,
        cardPresent: Boolean(card),
        cardText: card?.innerText ?? null,
      };
    }, { expectedLang: item.lang, isNote: item.id.startsWith("note-") });
    const pass = state.overflow <= 1 && state.images.every((image) => image.complete && image.naturalWidth > 0) && failures.length === 0 && (!item.id.startsWith("note-") || (state.mathCount >= 7 && !state.rawTexVisible && state.exactLawVisible && state.noDissipationLowerBoundVisible && state.notClayVisible)) && (item.lang !== "en" || state.englishChineseResidueCount === 0) && (!item.id.startsWith("home-") || state.cardPresent);
    results.push({ ...item, pass, failures, state });
    await context.close();
  }
} finally {
  await browser.close();
}

const report = { schemaVersion: "r074n-browser-qa-v1", base, output, cases: results, allPass: results.every((item) => item.pass) };
await writeFile(resolve(output, "report.json"), JSON.stringify(report, null, 2) + "\n");
process.stdout.write(JSON.stringify(report, null, 2) + "\n");
if (!report.allPass) process.exitCode = 1;
