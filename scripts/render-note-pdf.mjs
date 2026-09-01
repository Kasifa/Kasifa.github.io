#!/usr/bin/env node

// Render one synchronized HTML page and, when SOURCE_HTML and PROVENANCE_JSON
// are supplied, seal the exact HTML/PDF/renderer bytes into a deterministic
// sidecar. The PDF parser is dependency-free so the binding pass can repeat
// every structural check.

import { createHash } from "node:crypto";
import { constants as fsConstants } from "node:fs";
import { lstat, mkdir, open, readFile, rename, unlink } from "node:fs/promises";
import { createRequire } from "node:module";
import { dirname, isAbsolute, relative, resolve, sep } from "node:path";
import { fileURLToPath, pathToFileURL } from "node:url";

const usage =
  "usage: render-note-pdf.mjs URL OUTPUT_PDF [FULL_PAGE_SCREENSHOT] " +
  "[SOURCE_HTML] [PROVENANCE_JSON]";
const operationRoot = resolve(process.env.PDF_RENDER_ROOT ?? process.cwd());

function sha256(payload) {
  return createHash("sha256").update(payload).digest("hex");
}

function assertInsideOperationRoot(path, label) {
  const offset = relative(operationRoot, path);
  if (!offset || offset === ".." || offset.startsWith(`..${sep}`) || isAbsolute(offset)) {
    throw new Error(label + " escaped PDF_RENDER_ROOT");
  }
}

async function assertSafeDirectoryChain(directory, label) {
  const chain = [];
  let cursor = resolve(directory);
  while (true) {
    chain.push(cursor);
    const parent = dirname(cursor);
    if (parent === cursor) break;
    cursor = parent;
  }
  for (const path of chain.reverse()) {
    let info;
    try {
      info = await lstat(path);
    } catch (error) {
      throw new Error(`${label}: missing or dangling ancestor ${path}: ${error.code}`);
    }
    if (info.isSymbolicLink() || !info.isDirectory()) {
      throw new Error(`${label}: unsafe non-directory or symlink ancestor ${path}`);
    }
  }
}

async function assertSafeFileTarget(path, label, allowMissing = false) {
  assertInsideOperationRoot(path, label);
  await assertSafeDirectoryChain(dirname(path), label);
  try {
    const info = await lstat(path);
    if (info.isSymbolicLink() || !info.isFile()) {
      throw new Error(`${label}: expected regular nonsymlink file ${path}`);
    }
  } catch (error) {
    if (allowMissing && error?.code === "ENOENT") return;
    throw error;
  }
}

async function safeRead(path, label) {
  await assertSafeFileTarget(path, label);
  const handle = await open(path, fsConstants.O_RDONLY | fsConstants.O_NOFOLLOW);
  try {
    const info = await handle.stat();
    if (!info.isFile()) throw new Error(label + ": opened path is not regular");
    return await handle.readFile();
  } finally {
    await handle.close();
  }
}

async function atomicWrite(path, payload, label) {
  await assertSafeFileTarget(path, label, true);
  const temporary = resolve(
    dirname(path), `.${path.split(sep).at(-1)}.${process.pid}-${process.hrtime.bigint()}.tmp`,
  );
  try {
    const handle = await open(
      temporary,
      fsConstants.O_WRONLY | fsConstants.O_CREAT | fsConstants.O_EXCL | fsConstants.O_NOFOLLOW,
      0o644,
    );
    try {
      await handle.writeFile(payload);
      await handle.sync();
    } finally {
      await handle.close();
    }
    await assertSafeFileTarget(path, label + " rename target", true);
    await assertSafeFileTarget(temporary, label + " rename source");
    await rename(temporary, path);
    await assertSafeFileTarget(path, label + " installed output");
  } finally {
    try {
      const info = await lstat(temporary);
      if (info.isSymbolicLink() || !info.isFile()) throw new Error(label + ": unsafe scratch");
      await unlink(temporary);
    } catch (error) {
      if (error?.code !== "ENOENT") throw error;
    }
  }
}

function decodeUtf16Be(payload) {
  const start = payload.length >= 2 && payload[0] === 0xfe && payload[1] === 0xff ? 2 : 0;
  if ((payload.length - start) % 2 !== 0) throw new Error("odd UTF-16BE PDF title length");
  const littleEndian = Buffer.alloc(payload.length - start);
  for (let index = start; index < payload.length; index += 2) {
    littleEndian[index - start] = payload[index + 1];
    littleEndian[index - start + 1] = payload[index];
  }
  return littleEndian.toString("utf16le");
}

function decodePdfString(payload) {
  if (payload.length >= 2 && payload[0] === 0xfe && payload[1] === 0xff) {
    return decodeUtf16Be(payload);
  }
  if (payload.length >= 2 && payload[0] === 0xff && payload[1] === 0xfe) {
    return payload.subarray(2).toString("utf16le");
  }
  return payload.toString("latin1");
}

function parseLiteralString(value, offset, label) {
  let depth = 1;
  let index = offset + 1;
  const bytes = [];
  while (index < value.length) {
    const code = value.charCodeAt(index) & 0xff;
    if (code === 0x5c) {
      index += 1;
      if (index >= value.length) throw new Error(label + ": unterminated PDF title escape");
      const escaped = value.charCodeAt(index) & 0xff;
      const controls = new Map([
        [0x6e, 0x0a], [0x72, 0x0d], [0x74, 0x09],
        [0x62, 0x08], [0x66, 0x0c],
      ]);
      if (controls.has(escaped)) {
        bytes.push(controls.get(escaped));
        index += 1;
        continue;
      }
      if (escaped === 0x0d || escaped === 0x0a) {
        if (escaped === 0x0d && value.charCodeAt(index + 1) === 0x0a) index += 1;
        index += 1;
        continue;
      }
      if (escaped >= 0x30 && escaped <= 0x37) {
        let octal = String.fromCharCode(escaped);
        index += 1;
        while (octal.length < 3 && index < value.length &&
               value.charCodeAt(index) >= 0x30 && value.charCodeAt(index) <= 0x37) {
          octal += value[index];
          index += 1;
        }
        bytes.push(Number.parseInt(octal, 8));
        continue;
      }
      bytes.push(escaped);
      index += 1;
      continue;
    }
    if (code === 0x28) {
      depth += 1;
      bytes.push(code);
      index += 1;
      continue;
    }
    if (code === 0x29) {
      depth -= 1;
      if (depth === 0) {
        return { bytes: Buffer.from(bytes), encoding: "literal" };
      }
      bytes.push(code);
      index += 1;
      continue;
    }
    bytes.push(code);
    index += 1;
  }
  throw new Error(label + ": unterminated literal PDF title");
}

function parseInfoTitle(infoBody, label) {
  const marker = /\/Title\b/.exec(infoBody);
  if (!marker) throw new Error(label + ": /Title is absent from the trailer /Info object");
  let offset = marker.index + marker[0].length;
  while (/\s/.test(infoBody[offset] ?? "")) offset += 1;
  if (infoBody[offset] === "<" && infoBody[offset + 1] !== "<") {
    const end = infoBody.indexOf(">", offset + 1);
    if (end < 0) throw new Error(label + ": unterminated hexadecimal PDF title");
    const hex = infoBody.slice(offset + 1, end).replace(/\s+/g, "");
    if (!/^[0-9A-Fa-f]*$/.test(hex) || hex.length % 2 !== 0) {
      throw new Error(label + ": invalid hexadecimal PDF title");
    }
    return { title: decodePdfString(Buffer.from(hex, "hex")), encoding: "hex" };
  }
  if (infoBody[offset] === "(") {
    const parsed = parseLiteralString(infoBody, offset, label);
    return { title: decodePdfString(parsed.bytes), encoding: parsed.encoding };
  }
  throw new Error(label + ": /Title must be a hexadecimal or literal PDF string");
}

export function inspectPdf(payload, label = "PDF") {
  if (!Buffer.isBuffer(payload)) throw new TypeError(label + ": expected a Buffer");
  if (!payload.subarray(0, 5).equals(Buffer.from("%PDF-"))) {
    throw new Error(label + ": %PDF header is absent");
  }
  const latin = payload.toString("latin1");
  const tail = /startxref\s+(\d+)\s+%%EOF\s*$/.exec(latin);
  if (!tail) throw new Error(label + ": terminal startxref/%%EOF sequence is absent");
  const startxref = Number.parseInt(tail[1], 10);
  if (!Number.isSafeInteger(startxref) || startxref < 0 || startxref + 4 > payload.length ||
      payload.subarray(startxref, startxref + 4).toString("ascii") !== "xref") {
    throw new Error(label + ": last startxref does not point to xref");
  }
  const pageCount = (latin.match(/\/Type\s*\/Page\b/g) ?? []).length;
  if (pageCount < 1) throw new Error(label + ": no /Type /Page object found");
  const trailerOffset = latin.lastIndexOf("trailer", tail.index);
  if (trailerOffset < startxref) throw new Error(label + ": trailer preceding startxref is absent");
  const dictionaryStart = latin.indexOf("<<", trailerOffset);
  const dictionaryEnd = latin.indexOf(">>", dictionaryStart + 2);
  if (dictionaryStart < 0 || dictionaryEnd < 0 || dictionaryEnd > tail.index) {
    throw new Error(label + ": malformed trailer dictionary");
  }
  const trailer = latin.slice(dictionaryStart + 2, dictionaryEnd);
  const info = /\/Info\s+(\d+)\s+(\d+)\s+R\b/.exec(trailer);
  if (!info) throw new Error(label + ": trailer /Info reference is absent");
  const infoObject = `${info[1]} ${info[2]} R`;
  const objectPattern = new RegExp(
    String.raw`(?:^|[\r\n])${info[1]}\s+${info[2]}\s+obj\b([\s\S]*?)endobj\b`,
  );
  const object = objectPattern.exec(latin);
  if (!object) throw new Error(label + ": referenced trailer /Info object is absent");
  const parsedTitle = parseInfoTitle(object[1], label);
  return {
    header: "%PDF",
    eof: true,
    startxref,
    xrefKeyword: "xref",
    pageCount,
    infoObject,
    title: parsedTitle.title,
    titleEncoding: parsedTitle.encoding,
  };
}

function evidencePath(path) {
  const absolute = resolve(path);
  const offset = relative(process.cwd(), absolute);
  if (offset && offset !== ".." && !offset.startsWith(`..${sep}`) && !isAbsolute(offset)) {
    return offset.split(sep).join("/");
  }
  return absolute;
}

async function main() {
  const [url, outputArgument, screenshotArgument, sourceHtmlArgument, provenanceArgument,
    ...extra] = process.argv.slice(2);
  if (!url || !outputArgument || extra.length || Boolean(sourceHtmlArgument) !== Boolean(provenanceArgument)) {
    throw new Error(usage + "; SOURCE_HTML and PROVENANCE_JSON must be supplied together");
  }
  const output = resolve(outputArgument);
  const screenshot = screenshotArgument && screenshotArgument !== "-"
    ? resolve(screenshotArgument) : null;
  const sourceHtml = sourceHtmlArgument ? resolve(sourceHtmlArgument) : null;
  const provenance = provenanceArgument ? resolve(provenanceArgument) : null;
  const formal = Boolean(sourceHtml && provenance);
  const renderUrl = new URL(url);
  const publicOrigin = new URL(
    process.env.PDF_PUBLIC_ORIGIN ?? "https://kasifa.github.io",
  ).origin;
  if (!renderUrl.searchParams.has("lang")) renderUrl.searchParams.set("lang", "zh");
  if (formal) {
    await assertSafeFileTarget(output, "PDF output", true);
    if (screenshot) await assertSafeFileTarget(screenshot, "PDF screenshot", true);
    await assertSafeFileTarget(provenance, "PDF provenance", true);
    await assertSafeFileTarget(sourceHtml, "PDF source HTML");
  } else {
    await mkdir(dirname(output), { recursive: true });
    if (screenshot) await mkdir(dirname(screenshot), { recursive: true });
  }
  const sourceHtmlBytes = sourceHtml ? await safeRead(sourceHtml, "PDF source HTML") : null;

  const require = createRequire(import.meta.url);
  const { chromium } = require(
    "/Users/kasifa/.cache/codex-runtimes/codex-primary-runtime/dependencies/node/node_modules/playwright",
  );
  const executablePath = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome";
  const browser = await chromium.launch({ executablePath, headless: true });
  try {
    const page = await browser.newPage({
      viewport: { width: 1440, height: 1000 },
      deviceScaleFactor: 1,
    });
    const response = await page.goto(renderUrl.href, { waitUntil: "networkidle" });
    if (!response) throw new Error("main-document response is absent: " + renderUrl.href);
    if (sourceHtmlBytes) {
      const loadedDocument = await response.body();
      if (!loadedDocument.equals(sourceHtmlBytes)) {
        throw new Error(
          "loaded main-document bytes differ from SOURCE_HTML: " +
          `${sha256(loadedDocument)} != ${sha256(sourceHtmlBytes)}`,
        );
      }
    }
    const expectsMathJax = await page.locator('script[src*="mathjax" i]').count() > 0;
    if (expectsMathJax) {
      await page.waitForFunction(
        () => typeof globalThis.MathJax?.version === "string" &&
          Boolean(globalThis.MathJax?.startup?.promise),
        null,
        { timeout: 30_000 },
      );
    }
    await page.evaluate(async () => {
      await document.fonts.ready;
      if (globalThis.MathJax?.startup?.promise) await globalThis.MathJax.startup.promise;
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
          body { zoom: 0.995; }
          .metric { break-inside: avoid; page-break-inside: avoid; }
        }
      `,
    });
    if (screenshot) await page.screenshot({ path: screenshot, fullPage: true });
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

  if (formal) {
    await assertSafeFileTarget(output, "rendered PDF output");
    if (screenshot) await assertSafeFileTarget(screenshot, "rendered PDF screenshot");
  }
  const pdf = formal ? await safeRead(output, "rendered PDF output") : await readFile(output);
  const structure = inspectPdf(pdf, evidencePath(output));
  if (sourceHtml && provenance) {
    const rendererPath = fileURLToPath(import.meta.url);
    await assertSafeFileTarget(rendererPath, "PDF renderer source");
    const renderer = await safeRead(rendererPath, "PDF renderer source");
    const html = sourceHtmlBytes;
    const sidecar = {
      schemaVersion: "synchronized-pdf-render-provenance-v1",
      source: { url: renderUrl.href, origin: renderUrl.origin, publicOrigin },
      html: { path: evidencePath(sourceHtml), bytes: html.length, sha256: sha256(html) },
      loadedDocument: { bytes: html.length, sha256: sha256(html), equalsSourceHtml: true },
      pdf: {
        path: evidencePath(output), bytes: pdf.length, sha256: sha256(pdf),
        pageCount: structure.pageCount, title: structure.title,
      },
      structure,
      renderer: {
        path: evidencePath(rendererPath), bytes: renderer.length, sha256: sha256(renderer),
      },
    };
    await atomicWrite(
      provenance,
      Buffer.from(JSON.stringify(sidecar, null, 2) + "\n"),
      "PDF provenance output",
    );
  }
}

const direct = process.argv[1] && import.meta.url === pathToFileURL(resolve(process.argv[1])).href;
if (direct) {
  main().catch((error) => {
    console.error(error?.stack ?? String(error));
    process.exitCode = 1;
  });
}
