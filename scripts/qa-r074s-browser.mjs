#!/usr/bin/env node

import { mkdir, writeFile } from "node:fs/promises";
import { createRequire } from "node:module";
import { resolve } from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require("/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright");
const executablePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const base = process.argv[2] ?? "http://127.0.0.1:4179";
const output = process.argv[3] ?? "/private/tmp/r074s-browser-qa";
await mkdir(output, { recursive: true });

const cases = [
  { id: "note-zh-desktop", path: "/notes/r0-74s.html?lang=zh", width: 1440, height: 1000, lang: "zh", kind: "note" },
  { id: "note-en-desktop", path: "/notes/r0-74s.html?lang=en", width: 1440, height: 1000, lang: "en", kind: "note" },
  { id: "note-zh-mobile", path: "/notes/r0-74s.html?lang=zh", width: 390, height: 844, lang: "zh", kind: "note" },
  { id: "note-en-mobile", path: "/notes/r0-74s.html?lang=en", width: 390, height: 844, lang: "en", kind: "note" },
  { id: "home-zh-desktop", path: "/research-review.html?lang=zh#r074s", width: 1440, height: 1000, lang: "zh", kind: "home" },
  { id: "home-en-mobile", path: "/research-review.html?lang=en#r074s", width: 390, height: 844, lang: "en", kind: "home" },
  { id: "literature-en-desktop", path: "/literature-review.html?lang=en#r074s-boundary", width: 1440, height: 1000, lang: "en", kind: "literature" },
];

const browser = await chromium.launch({ executablePath, headless: true });
const results = [];
try {
  for (const item of cases) {
    const context = await browser.newContext({ viewport: { width: item.width, height: item.height } });
    const page = await context.newPage();
    const failures = [];
    page.on("requestfailed", (request) => failures.push({ url: request.url(), error: request.failure()?.errorText ?? "unknown" }));
    await page.goto(base + item.path, { waitUntil: "load", timeout: 30000 });
    if (item.kind === "note") await page.waitForFunction(() => document.querySelectorAll("mjx-container").length >= 20, null, { timeout: 20000 });
    if (item.kind === "home") await page.locator('[data-release="r074s"]').scrollIntoViewIfNeeded();
    if (item.kind === "literature") await page.locator("#r074s-boundary").scrollIntoViewIfNeeded();
    await page.screenshot({ path: resolve(output, `${item.id}.png`), fullPage: false });
    const state = await page.evaluate(({ expectedLang, kind }) => {
      const body = document.body.innerText;
      const residue = expectedLang === "en" ? body.replace(/中文/g, "").match(/[\u3400-\u9fff\uf900-\ufaff]/g) ?? [] : [];
      const card = document.querySelector('[data-release="r074s"]');
      return {
        title: document.title,
        documentLang: document.documentElement.lang,
        overflow: document.documentElement.scrollWidth - document.documentElement.clientWidth,
        mathCount: document.querySelectorAll("mjx-container").length,
        mathErrors: document.querySelectorAll("mjx-merror").length,
        rawTexVisible: /\\\[|\\\]|\\\(|\\\)/.test(body),
        englishChineseResidueCount: residue.length,
        notClayVisible: kind !== "note" || body.includes("NOT CLAY"),
        openBoundaryVisible: kind !== "note" || /S\.243/.test(body) && /residual/i.test(body) && /OPEN|开放/.test(body),
        noGoBoundaryVisible: kind !== "note" || /no-go/i.test(body) && /exact family|精确族/i.test(body) && /REFUTED|否定|refute/i.test(body),
        formalFigureVisible: kind !== "note" || /figure|期刊主图/i.test(body),
        cardPresent: kind !== "home" || Boolean(card),
        cardCharacters: card?.textContent?.length ?? 0,
        literatureBoundaryPresent: kind !== "literature" || Boolean(document.querySelector("#r074s-boundary")),
      };
    }, { expectedLang: item.lang, kind: item.kind });
    const pass = state.overflow <= 1
      && failures.length === 0
      && (item.kind !== "note" || (state.mathCount >= 20 && state.mathErrors === 0 && !state.rawTexVisible && state.notClayVisible && state.openBoundaryVisible && state.noGoBoundaryVisible && state.formalFigureVisible))
      && (item.lang !== "en" || state.englishChineseResidueCount === 0)
      && state.cardPresent
      && (item.kind !== "home" || state.cardCharacters < 450)
      && state.literatureBoundaryPresent;
    results.push({ ...item, pass, failures, state });
    await context.close();
  }
} finally {
  await browser.close();
}

const report = { schemaVersion: "r074s-browser-qa-v1", base, output, cases: results, allPass: results.every((item) => item.pass) };
await writeFile(resolve(output, "report.json"), JSON.stringify(report, null, 2) + "\n");
process.stdout.write(JSON.stringify(report, null, 2) + "\n");
if (!report.allPass) process.exitCode = 1;
