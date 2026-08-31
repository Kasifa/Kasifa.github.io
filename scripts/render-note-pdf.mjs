#!/usr/bin/env node

import { mkdir } from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, resolve } from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require(
  "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright",
);

const [url, outputArgument, screenshotArgument] = process.argv.slice(2);
if (!url || !outputArgument) {
  throw new Error(
    "usage: render-note-pdf.mjs URL OUTPUT_PDF [FULL_PAGE_SCREENSHOT]",
  );
}

const output = resolve(outputArgument);
const screenshot = screenshotArgument ? resolve(screenshotArgument) : null;
const renderUrl = new URL(url);
const publicOrigin = process.env.PDF_PUBLIC_ORIGIN ?? "https://kasifa.github.io";
if (!renderUrl.searchParams.has("lang")) renderUrl.searchParams.set("lang", "zh");
await mkdir(dirname(output), { recursive: true });
if (screenshot) await mkdir(dirname(screenshot), { recursive: true });

const executablePath =
  "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const browser = await chromium.launch({ executablePath, headless: true });
try {
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1000 },
    deviceScaleFactor: 1,
  });
  await page.goto(renderUrl.href, { waitUntil: "networkidle" });
  await page.evaluate(async () => {
    await document.fonts.ready;
    if (globalThis.MathJax?.startup?.promise) {
      await globalThis.MathJax.startup.promise;
    }
  });
  await page.evaluate((origin) => {
    for (const anchor of document.querySelectorAll("a[href]")) {
      const href = anchor.getAttribute("href");
      if (href?.startsWith("/")) anchor.href = new URL(href, origin).href;
    }
  }, publicOrigin);
  await page.addStyleTag({
    content: `
      @media print {
        body {
          zoom: 0.995;
        }
        .metric {
          break-inside: avoid;
          page-break-inside: avoid;
        }
      }
    `,
  });
  if (screenshot) {
    await page.screenshot({ path: screenshot, fullPage: true });
  }
  await page.emulateMedia({ media: "print" });
  await page.pdf({
    path: output,
    format: "A4",
    preferCSSPageSize: true,
    printBackground: true,
    displayHeaderFooter: false,
  });
} finally {
  await browser.close();
}
