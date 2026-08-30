#!/usr/bin/env node

import { createHash } from "node:crypto";
import { lstat, open, readFile, rename, unlink } from "node:fs/promises";
import { dirname, resolve } from "node:path";

const root = resolve(process.env.R073M_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const outputPath = resolve(root, "research/r073m_pdf_bindings.json");
const rendererPath = resolve(root, "scripts/render-note-pdf.mjs");
const documents = [
  {
    kind: "research-note",
    html: "public/notes/r0-73m.html",
    pdf: "public/notes/r0-73m.pdf",
    title: "R0.73M｜Prescribed-action planar nonlinear departure",
  },
  {
    kind: "cumulative-recap",
    html: "public/recap-r0-61-r0-73m.html",
    pdf: "public/recap-r0-61-r0-73m.pdf",
    title: "R0.61–R0.73M｜R0.60 之后的研究回顾",
  },
];

const usage = "usage: bind-r073m-pdfs.mjs (--apply | --check-only)";
const selected = process.argv.slice(2);
if (selected.includes("--help") || selected.includes("-h")) {
  console.log(usage);
  process.exit(0);
}
if (selected.length !== 1 || !["--apply", "--check-only"].includes(selected[0])) {
  throw new Error(usage);
}
const apply = selected[0] === "--apply";

function sha256(payload) {
  return createHash("sha256").update(payload).digest("hex");
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

function pdfTitle(payload, label) {
  const source = payload.toString("latin1");
  const match = source.match(/\/Title\s*<([0-9A-Fa-f]+)>/);
  if (!match) throw new Error(label + ": hexadecimal PDF title metadata is absent");
  return decodeUtf16Be(Buffer.from(match[1], "hex"));
}

async function regularBytes(relative) {
  const path = resolve(root, relative);
  const info = await lstat(path);
  if (!info.isFile() || info.isSymbolicLink()) {
    throw new Error(relative + ": expected a regular nonsymlink file");
  }
  return readFile(path);
}

async function atomicWrite(path, payload) {
  const temporary = resolve(
    dirname(path),
    `.${path.split("/").at(-1)}.r073m-${process.pid}-${Date.now()}-${process.hrtime.bigint()}.tmp`,
  );
  try {
    const handle = await open(temporary, "wx", 0o644);
    try {
      await handle.writeFile(payload);
      await handle.sync();
    } finally {
      await handle.close();
    }
    await rename(temporary, path);
    const directory = await open(dirname(path), "r");
    try {
      await directory.sync();
    } finally {
      await directory.close();
    }
  } finally {
    try {
      await unlink(temporary);
    } catch (error) {
      if (error?.code !== "ENOENT") throw error;
    }
  }
}

const renderer = await regularBytes("scripts/render-note-pdf.mjs");
const rows = [];
for (const document of documents) {
  const [html, pdf] = await Promise.all([
    regularBytes(document.html),
    regularBytes(document.pdf),
  ]);
  if (!pdf.subarray(0, 4).equals(Buffer.from("%PDF")) || pdf.length <= 10_000) {
    throw new Error(document.pdf + ": malformed or unexpectedly small PDF");
  }
  const title = pdfTitle(pdf, document.pdf);
  if (title !== document.title) {
    throw new Error(document.pdf + ": PDF title drift: " + JSON.stringify(title));
  }
  rows.push({
    kind: document.kind,
    html: { path: document.html, bytes: html.length, sha256: sha256(html) },
    pdf: { path: document.pdf, bytes: pdf.length, sha256: sha256(pdf), title },
  });
}

const manifest = {
  schemaVersion: "r073m-synchronized-pdf-bindings-v1",
  release: "R0.73M",
  renderer: {
    path: "scripts/render-note-pdf.mjs",
    sha256: sha256(renderer),
    language: "zh",
    format: "A4",
  },
  documents: rows,
  claimBoundary: {
    htmlAndPdfBytesCryptographicallyBound: true,
    pdfTitleIndependentlyParsed: true,
    pdfBindingCertifiesMathematicalCorrectness: false,
  },
};
const payload = Buffer.from(JSON.stringify(manifest, null, 2) + "\n");

if (apply) {
  await atomicWrite(outputPath, payload);
} else {
  const current = await regularBytes("research/r073m_pdf_bindings.json");
  if (!current.equals(payload)) throw new Error("R0.73M PDF binding manifest is stale");
}

console.log(JSON.stringify({
  applied: apply,
  checked: !apply,
  documents: rows.length,
  output: "research/r073m_pdf_bindings.json",
}));
