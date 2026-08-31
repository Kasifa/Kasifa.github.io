#!/usr/bin/env node

// Cryptographically bind the two synchronized R0.73Q PDFs to their HTML
// sources and independently parse PDF title metadata.  This is a publication
// integrity check, never a mathematical-correctness certificate.

import { createHash } from "node:crypto";
import { lstat, open, readFile, rename, unlink } from "node:fs/promises";
import { dirname, resolve } from "node:path";

const usage = "usage: bind-r073q-pdfs.mjs (--apply | --check-only)";
const selected = process.argv.slice(2);
if (selected.includes("--help") || selected.includes("-h")) {
  console.log(usage);
  process.exit(0);
}
if (selected.length !== 1 || !["--apply", "--check-only"].includes(selected[0])) {
  throw new Error(usage);
}

const root = resolve(process.env.R073Q_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const outputPath = resolve(root, "research/r073q_pdf_bindings.json");
const dictionaryPath = resolve(root, "research/r073q_bilingual_dictionary.md");
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
    throw new Error("R0.73Q bilingual dictionary contains control characters");
  }
  const field = (label) => dictionary.match(
    new RegExp(`^\\*\\*${label}:\\*\\*\\s*(.+?)(?=\\n\\s*\\n)`, "ms"),
  )?.[1]?.replace(/\s+/g, " ").replace(/^\*|\*$/g, "").trim();
  const releaseTitle = field("Release title");
  const publicChinese = field("Public title \\(zh\\)");
  if (releaseTitle !== "R0.73Q | A critical heat-flow tube beyond the \\(H^{1/2}\\) entrance" ||
      publicChinese !== "R0.73Q｜越过 \\(H^{1/2}\\) 入口的临界热流稳定管") {
    throw new Error("R0.73Q canonical title ledger drift");
  }
  for (const token of [
    "periodicOseenHLS=CLOSED_AFTER_AUDIT",
    "linearizedVolterraInverse=CLOSED_AFTER_AUDIT",
    "uniformAllRestartRadius=CLOSED_AFTER_AUDIT",
    "periodicHeatFlowTube=CLOSED_AFTER_AUDIT",
    "strictExtensionByUnion=CLOSED",
    "heatFlowBallContainsEntirePublishedH12Ball=NOT_PROVED",
    "bareKatoSupFromL4L6=BLOCKED_BY_ENDPOINT",
    "fullKochTataruTheory=NOT_REFUTED",
    "uniformL2Only=OPEN",
    "nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL",
    "formulaDiagnosticValidation=PASS",
    "formulaDiagnosticPackage=CLOSED",
    "sourceCommitAssigned=TRUE",
    "finalSeal=TRUE",
    "formalFigurePackage=PASS",
    "publicReleaseContent=READY",
  ]) {
    if (!dictionary.includes(token)) throw new Error("R0.73Q dictionary missing " + token);
  }
  if (dictionary.includes("formulaDiagnosticValidation=PRESEAL_PENDING") ||
      dictionary.includes("formulaDiagnosticPackage=PRESEAL_PENDING") ||
      /\bpublicRelease=/.test(dictionary)) {
    throw new Error("R0.73Q dictionary still carries prepublication provenance");
  }
  return {
    note: releaseTitle.replace(/\\\((.*?)\\\)/g, "$1").replace(" | ", "｜"),
    publicChinese: publicChinese.replace(/\\\((.*?)\\\)/g, "$1"),
    recap: "R0.61–R0.73Q｜R0.60 之后的研究回顾",
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
    `.${path.split("/").at(-1)}.r073q-${process.pid}-${Date.now()}-${process.hrtime.bigint()}.tmp`,
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
  releaseManifest.latestCompletedRelease !== "r073q" ||
  releaseManifest.siteVersion !== "1.57" ||
  releaseManifest.nextRelease !== "r073r" ||
  siteVersion.latestRelease !== "R0.73Q" ||
  siteVersion.version !== "1.57"
) {
  throw new Error("R0.73Q HTML/accounting apply must precede PDF binding");
}
const documents = [
  {
    kind: "research-note",
    html: "public/notes/r0-73q.html",
    pdf: "public/notes/r0-73q.pdf",
    title: titles.note,
  },
  {
    kind: "cumulative-recap",
    html: "public/recap-r0-61-r0-73q.html",
    pdf: "public/recap-r0-61-r0-73q.pdf",
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
  schemaVersion: "r073q-synchronized-pdf-bindings-v1",
  release: "R0.73Q",
  canonicalTitleSource: {
    path: "research/r073q_bilingual_dictionary.md",
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
    uniformL2Only: "OPEN",
    nonperturbativeBMOInverseUniqueness: "FALSE_IN_GENERAL",
    fullKochTataruTheory: "NOT_REFUTED",
    finiteFormulaDiagnosticOnly: true,
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
  if (!current.equals(payload)) throw new Error("R0.73Q PDF binding manifest is stale");
}

console.log(JSON.stringify({
  applied: apply,
  checked: !apply,
  documents: rows.length,
  output: "research/r073q_pdf_bindings.json",
}));
