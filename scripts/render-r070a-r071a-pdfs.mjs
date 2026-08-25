#!/usr/bin/env node

import { mkdir } from "node:fs/promises";
import { createRequire } from "node:module";
import { resolve } from "node:path";

const require = createRequire(import.meta.url);
const { chromium } = require(
  "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright",
);

const baseUrl = process.argv[2] ?? "http://127.0.0.1:8765";
const root = resolve(import.meta.dirname, "..");
const previewDir = resolve(root, ".qa", "r086-pdf-previews");
const slugs = [
  ...Array.from({ length: 26 }, (_, index) =>
    `r0-70${String.fromCharCode(97 + index)}`,
  ),
  "r0-71a",
];
const jobs = [
  ...slugs.map((slug) => ({
    url: `${baseUrl}/notes/${slug}.html`,
    output: resolve(root, "public", "notes", `${slug}.pdf`),
    preview: ["r0-70a", "r0-70z", "r0-71a"].includes(slug)
      ? resolve(previewDir, `${slug}.png`)
      : null,
  })),
  {
    url: `${baseUrl}/recap-r0-61-r0-71a.html`,
    output: resolve(root, "public", "recap-r0-61-r0-71a.pdf"),
    preview: resolve(previewDir, "recap-r0-61-r0-71a.png"),
  },
];

await mkdir(previewDir, { recursive: true });
const executablePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
const browser = await chromium.launch({ executablePath, headless: true });
try {
  const page = await browser.newPage({
    viewport: { width: 1440, height: 1000 },
    deviceScaleFactor: 1,
  });
  for (const [index, job] of jobs.entries()) {
    const started = Date.now();
    await page.goto(job.url, { waitUntil: "networkidle", timeout: 60_000 });
    await page.evaluate(async () => {
      await document.fonts.ready;
      if (globalThis.MathJax?.startup?.promise) await globalThis.MathJax.startup.promise;
    });
    if (job.preview) await page.screenshot({ path: job.preview, fullPage: true });
    await page.emulateMedia({ media: "print" });
    await page.pdf({
      path: job.output,
      format: "A4",
      preferCSSPageSize: true,
      printBackground: true,
      displayHeaderFooter: false,
    });
    await page.emulateMedia({ media: "screen" });
    const seconds = ((Date.now() - started) / 1000).toFixed(1);
    console.log(`[${index + 1}/${jobs.length}] ${job.output} (${seconds}s)`);
  }
} finally {
  await browser.close();
}
