#!/usr/bin/env node

// Cryptographically bind the two synchronized R0.73O PDFs to their HTML
// sources and independently parse PDF title metadata.  This is a publication
// integrity check, never a mathematical-correctness certificate.

import { createHash } from "node:crypto";
import { lstat, open, readFile, rename, unlink } from "node:fs/promises";
import { dirname, resolve } from "node:path";

const usage = "usage: bind-r073o-pdfs.mjs (--apply | --check-only)";
const selected = process.argv.slice(2);
if (selected.includes("--help") || selected.includes("-h")) {
  console.log(usage);
  process.exit(0);
}
if (selected.length !== 1 || !["--apply", "--check-only"].includes(selected[0])) {
  throw new Error(usage);
}

const root = resolve(process.env.R073O_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const outputPath = resolve(root, "research/r073o_pdf_bindings.json");
const dictionaryPath = resolve(root, "research/r073o_bilingual_dictionary.md");
const rendererRelative = "scripts/render-note-pdf.mjs";
const apply = selected[0] === "--apply";

function sha256(payload) {
  return createHash("sha256").update(payload).digest("hex");
}

async function regularBytes(relativeOrAbsolute) {
  const path = relativeOrAbsolute.startsWith(root)
    ? relativeOrAbsolute
    : resolve(root, relativeOrAbsolute);
  const info = await lstat(path);
  if (!info.isFile() || info.isSymbolicLink()) {
    throw new Error(path + ": expected a regular nonsymlink file");
  }
  return readFile(path);
}

function canonicalTitles(dictionary) {
  if (/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(dictionary)) {
    throw new Error("R0.73O bilingual dictionary contains control characters");
  }
  const releaseTitle = dictionary.match(/^\*\*Release title:\*\*\s*\*?(.+?)\*?\s*$/m)?.[1]
    ?.replace(/^\*|\*$/g, "").trim();
  const synchronized = dictionary.match(
    /^## \d+\. Synchronized title\s*\n\s*```text\s*\n([^\n]+)\n([^\n]+)\n```/m,
  );
  if (!synchronized) throw new Error("R0.73O synchronized-title ledger missing");
  if (synchronized[1].trim() !== releaseTitle) {
    throw new Error("R0.73O release-title ledgers disagree");
  }
  for (const token of [
    "unforcedGlobalOrbitH3Stability=CLOSED_CONDITIONALLY_AFTER_AUDIT",
    "unforcedH3InputL2Output=CLOSED_AS_COROLLARY",
    "uniformL2OnlyInputThreshold=OPEN_COLLISION_SENSITIVE",
    "forcedKolmogorovH3InputL2Escape=CLOSED_BY_COMPOSITE_PRIMARY_SOURCE_CHAIN_AFTER_AUDIT",
    "finiteFourierDiagnostic=PASS",
    "finiteComputationProvesInfiniteDimensionalSpectrum=FALSE",
    "finiteDiagnosticValidation=PASS",
    "finiteDiagnosticPackage=CLOSED",
    "sourceCommitAssigned=TRUE",
    "finalSeal=TRUE",
    "formalFigurePackage=PASS",
    "publicReleaseContent=READY",
  ]) {
    if (!dictionary.includes(token)) throw new Error("R0.73O dictionary missing " + token);
  }
  if (dictionary.includes("finiteDiagnosticValidation=VALIDATED_PRESEAL") ||
      /\bpublicRelease=/.test(dictionary)) {
    throw new Error("R0.73O dictionary still carries prepublication provenance");
  }
  return {
    note: synchronized[1].trim().replace(" | ", "｜"),
    publicChinese: synchronized[2].trim(),
    recap: "R0.61–R0.73O｜R0.60 之后的研究回顾",
  };
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
  const match = payload.toString("latin1").match(/\/Title\s*<([0-9A-Fa-f]+)>/);
  if (!match) throw new Error(label + ": hexadecimal PDF title metadata is absent");
  return decodeUtf16Be(Buffer.from(match[1], "hex"));
}

async function atomicWrite(path, payload) {
  const temporary = resolve(
    dirname(path),
    `.${path.split("/").at(-1)}.r073o-${process.pid}-${Date.now()}-${process.hrtime.bigint()}.tmp`,
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

const dictionary = (await regularBytes(dictionaryPath)).toString("utf8");
const titles = canonicalTitles(dictionary);
const releaseManifest = JSON.parse((await regularBytes("research/release-manifest.json")).toString("utf8"));
const siteVersion = JSON.parse((await regularBytes("public/site-version.json")).toString("utf8"));
if (
  releaseManifest.latestCompletedRelease !== "r073o" ||
  releaseManifest.siteVersion !== "1.55" ||
  releaseManifest.nextRelease !== "r073p" ||
  siteVersion.latestRelease !== "R0.73O" ||
  siteVersion.version !== "1.55"
) {
  throw new Error("R0.73O HTML/accounting apply must precede PDF binding");
}
const documents = [
  {
    kind: "research-note",
    html: "public/notes/r0-73o.html",
    pdf: "public/notes/r0-73o.pdf",
    title: titles.note,
  },
  {
    kind: "cumulative-recap",
    html: "public/recap-r0-61-r0-73o.html",
    pdf: "public/recap-r0-61-r0-73o.pdf",
    title: titles.recap,
  },
];

const renderer = await regularBytes(rendererRelative);
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
  schemaVersion: "r073o-synchronized-pdf-bindings-v1",
  release: "R0.73O",
  canonicalTitleSource: {
    path: "research/r073o_bilingual_dictionary.md",
    sha256: sha256(Buffer.from(dictionary)),
    publicChineseTitle: titles.publicChinese,
  },
  renderer: {
    path: rendererRelative,
    sha256: sha256(renderer),
    language: "zh",
    format: "A4",
  },
  documents: rows,
  claimBoundary: {
    htmlAndPdfBytesCryptographicallyBound: true,
    pdfTitleIndependentlyParsed: true,
    uniformL2OnlyInputThreshold: "OPEN_COLLISION_SENSITIVE",
    finiteComputationProvesInfiniteDimensionalSpectrum: false,
    pdfBindingCertifiesMathematicalCorrectness: false,
    pdfBindingEstablishesNoveltyOrPriority: false,
    clayProblemSolved: false,
  },
};
const payload = Buffer.from(JSON.stringify(manifest, null, 2) + "\n");

if (apply) {
  await atomicWrite(outputPath, payload);
} else {
  const current = await regularBytes(outputPath);
  if (!current.equals(payload)) throw new Error("R0.73O PDF binding manifest is stale");
}

console.log(JSON.stringify({
  applied: apply,
  checked: !apply,
  documents: rows.length,
  output: "research/r073o_pdf_bindings.json",
}));
