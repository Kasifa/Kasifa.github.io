#!/usr/bin/env node
"use strict";

const fs = require("fs");
const path = require("path");
const sharp = require("sharp");
const { chromium } = require("playwright");
const { PDFDocument } = require("pdf-lib");

async function main() {
  const packageDir = __dirname;
  const svgPath = path.join(packageDir, "figure.svg");
  const pngPath = path.join(packageDir, "figure.png");
  const pdfPath = path.join(packageDir, "figure.pdf");
  const svg = fs.readFileSync(svgPath);
  const targetDpi = 600;
  const targetWidth = Math.round((178 / 25.4) * targetDpi);
  const targetHeight = Math.round((72 / 25.4) * targetDpi);
  // Sharp/libvips applies density twice when an SVG combines physical units
  // with a viewBox.  Rasterize at the SVG baseline density, then request the
  // exact 178 mm x 72 mm pixel dimensions required at 600 dpi.
  await sharp(svg, { density: 72 })
    .resize({ width: targetWidth, height: targetHeight, fit: "fill" })
    .withMetadata({ density: targetDpi })
    .png({ compressionLevel: 9 })
    .toFile(pngPath);
  const browser = await chromium.launch({ headless: true });
  try {
    const page = await browser.newPage({ viewport: { width: 1780, height: 720 } });
    await page.setContent(`<!doctype html><html><head><style>@page{size:178mm 72mm;margin:0}html,body{margin:0;padding:0;width:178mm;height:72mm;overflow:hidden}svg{display:block}</style></head><body>${svg.toString("utf8")}</body></html>`);
    await page.pdf({
      path: pdfPath,
      width: "178mm",
      height: "72mm",
      printBackground: true,
      margin: { top: "0", right: "0", bottom: "0", left: "0" },
      preferCSSPageSize: true,
    });
  } finally {
    await browser.close();
  }
  const rawPdf = fs.readFileSync(pdfPath);
  const datePattern = /D:\d{14}\+00'00'/g;
  const rawPdfText = rawPdf.toString("latin1");
  const dateMatches = rawPdfText.match(datePattern) || [];
  if (dateMatches.length !== 2) {
    throw new Error(`expected two Chromium PDF timestamps, found ${dateMatches.length}`);
  }
  fs.writeFileSync(
    pdfPath,
    Buffer.from(
      rawPdfText.replace(datePattern, "D:20000101000000+00'00'"),
      "latin1",
    ),
  );
  const metadata = await sharp(pngPath).metadata();
  if (
    metadata.format !== "png" ||
    metadata.width !== targetWidth ||
    metadata.height !== targetHeight ||
    metadata.density !== targetDpi
  ) {
    throw new Error(`PNG gate failed: ${JSON.stringify(metadata)}`);
  }
  const pdf = await PDFDocument.load(fs.readFileSync(pdfPath));
  if (pdf.getPageCount() !== 1) {
    throw new Error(`PDF page-count gate failed: ${pdf.getPageCount()}`);
  }
  const pageSize = pdf.getPage(0).getSize();
  const expectedWidthPoints = (178 / 25.4) * 72;
  const expectedHeightPoints = (72 / 25.4) * 72;
  if (
    Math.abs(pageSize.width - expectedWidthPoints) > 1.0 ||
    Math.abs(pageSize.height - expectedHeightPoints) > 1.0
  ) {
    throw new Error(`PDF size gate failed: ${JSON.stringify(pageSize)}`);
  }
  process.stdout.write(JSON.stringify({
    verdict: "PASS",
    pngPixels: [metadata.width, metadata.height],
    density: metadata.density,
    pdfPages: pdf.getPageCount(),
    pdfPoints: [pageSize.width, pageSize.height],
    outputs: ["figure.svg", "figure.pdf", "figure.png"],
  }) + "\n");
}

main().catch((error) => {
  process.stderr.write(String(error.stack || error) + "\n");
  process.exit(1);
});
