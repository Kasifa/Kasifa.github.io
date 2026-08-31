#!/usr/bin/env node

// Cryptographically bind the synchronized R0.73S PDFs to their HTML sources
// and independently parse hexadecimal UTF-16BE PDF title metadata.  This is a
// publication-integrity check, never a mathematical-correctness certificate.

import { createHash } from "node:crypto";
import { lstat, open, readFile, rename, unlink } from "node:fs/promises";
import { dirname, relative, resolve } from "node:path";

const usage = "usage: bind-r073s-pdfs.mjs (--apply | --check-only)";
const selected = process.argv.slice(2);
if (selected.includes("--help") || selected.includes("-h")) {
  console.log(usage);
  process.exit(0);
}
if (selected.length !== 1 || !["--apply", "--check-only"].includes(selected[0])) {
  throw new Error(usage);
}

const root = resolve(process.env.R073S_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const outputPath = resolve(root, "research/r073s_pdf_bindings.json");
const reportPath = resolve(root, "research/r073s_report-source.md");
const dictionaryPath = resolve(root, "research/r073s_bilingual_dictionary.md");
const rendererRelative = "scripts/render-note-pdf.mjs";
const apply = selected[0] === "--apply";
const releaseTitle = "R0.73S | From triple convolution to autocorrelation: one computable certificate and two hard limits";
const publicTitle = "R0.73S｜把三重卷积降到自相关：一个可算证书，两条不能越过的边界";
const documentTitle = "R0.73S｜From triple convolution to autocorrelation: one computable certificate and two hard limits";
const recapTitle = "R0.61–R0.73S｜R0.60 之后的研究回顾";
const figureId = "fig-r073s-quadratic-certificate";

function sha256(payload) {
  return createHash("sha256").update(payload).digest("hex");
}

function assertInsideRoot(path, label) {
  const offset = relative(root, path);
  if (!offset || offset === ".." || offset.startsWith("../") || offset.startsWith("..\\")) {
    throw new Error(label + " escaped R073S_RELEASE_ROOT");
  }
}

async function regularBytes(relativeOrAbsolute) {
  const path = relativeOrAbsolute.startsWith(root)
    ? relativeOrAbsolute
    : resolve(root, relativeOrAbsolute);
  assertInsideRoot(path, "PDF binding input");
  const info = await lstat(path);
  if (!info.isFile() || info.isSymbolicLink()) {
    throw new Error(path + ": expected a regular nonsymlink file");
  }
  return readFile(path);
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
  assertInsideRoot(path, "PDF binding output");
  const parent = await lstat(dirname(path));
  if (!parent.isDirectory() || parent.isSymbolicLink()) {
    throw new Error("unsafe PDF binding parent: " + dirname(path));
  }
  const temporary = resolve(
    dirname(path),
    `.${path.split("/").at(-1)}.r073s-${process.pid}-${Date.now()}-${process.hrtime.bigint()}.tmp`,
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

const report = (await regularBytes(reportPath)).toString("utf8");
const dictionary = (await regularBytes(dictionaryPath)).toString("utf8");
if (/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(report + dictionary)) {
  throw new Error("R0.73S canonical report or dictionary contains control characters");
}
if (!report.startsWith("# " + releaseTitle + "\n") ||
    !report.includes("**Public title (zh):** " + publicTitle)) {
  throw new Error("R0.73S canonical report title ledger drift");
}
const boundaryCorpus = (report + "\n" + dictionary).replace(/\s+/g, " ");
for (const phrase of [
  "direct classical collision",
  "not a new harmonic analysis theorem",
  "does not prove a universal runtime lower bound",
  "not the complete finite autocorrelation",
  "zero-nonlinearity shear flows",
  "not a Clay result",
]) {
  if (!boundaryCorpus.includes(phrase)) {
    throw new Error("R0.73S canonical sources missing boundary phrase: " + phrase);
  }
}

const releaseManifest = JSON.parse((await regularBytes("research/release-manifest.json")).toString("utf8"));
const siteVersion = JSON.parse((await regularBytes("public/site-version.json")).toString("utf8"));
if (
  releaseManifest.latestCompletedRelease !== "r073s" ||
  releaseManifest.siteVersion !== "1.59" ||
  releaseManifest.publicHtmlNoteCount !== 195 ||
  releaseManifest.postR060RecapNodeCount !== 135 ||
  releaseManifest.nextRelease !== "r073t" ||
  releaseManifest.postR070APublishedReleaseCount !== 97 ||
  releaseManifest.postR070AFormalSealedReleaseCount !== 73 ||
  releaseManifest.legacyFormalFigureBacklogCount !== 24 ||
  siteVersion.latestRelease !== "R0.73S" ||
  siteVersion.version !== "1.59" ||
  siteVersion.publicHtmlNoteCount !== 195
) {
  throw new Error("R0.73S HTML/accounting apply must precede PDF binding");
}

const documents = [
  {
    kind: "research-note",
    html: "public/notes/r0-73s.html",
    pdf: "public/notes/r0-73s.pdf",
    title: documentTitle,
    htmlMarkers: [publicTitle, "quadraticAutocorrelationBound=VERIFIED_CLASSICAL", figureId],
  },
  {
    kind: "cumulative-recap",
    html: "public/recap-r0-61-r0-73s.html",
    pdf: "public/recap-r0-61-r0-73s.pdf",
    title: recapTitle,
    htmlMarkers: ["R0.73S", "135", "universalRuntimeLowerBound=NOT_PROVED"],
  },
];

const renderer = await regularBytes(rendererRelative);
const rows = [];
for (const document of documents) {
  const [html, pdf] = await Promise.all([
    regularBytes(document.html),
    regularBytes(document.pdf),
  ]);
  const htmlText = html.toString("utf8");
  for (const marker of document.htmlMarkers) {
    if (!htmlText.includes(marker)) throw new Error(document.html + ": missing " + marker);
  }
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
  schemaVersion: "r073s-synchronized-pdf-bindings-v1",
  release: "R0.73S",
  canonicalTitleSource: {
    path: "research/r073s_report-source.md",
    sha256: sha256(Buffer.from(report)),
    releaseTitle,
    publicChineseTitle: publicTitle,
  },
  canonicalBoundarySource: {
    path: "research/r073s_bilingual_dictionary.md",
    sha256: sha256(Buffer.from(dictionary)),
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
    quadraticAutocorrelationBound: "VERIFIED_CLASSICAL",
    differenceSupportNikolskii: "VERIFIED_CLASSICAL",
    selectedShiftMagnitudeTailCertificate: "CLOSED_EXACT",
    fixedAnnulusDifferenceSupportObstruction: "CLOSED_EXACT",
    lowSummaryNonIdentifiability: "CLOSED_EXACT",
    completeAutocorrelationDeterminesL6: "VERIFIED_CLASSICAL",
    zeroNonlinearityWitnesses: "CLOSED",
    finiteFormulaCertificateOnly: true,
    heatFlowIntegralComputed: false,
    navierStokesSimulation: false,
    runtimeBenchmark: false,
    universalRuntimeLowerBound: "NOT_PROVED",
    failureOfEntranceImpliesUnsafeDynamics: false,
    uniformL2OnlyStrongRadius: "OPEN",
    arbitraryThreeDimensionalGlobalRegularity: "OPEN",
    clayConclusion: "OPEN",
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
  if (!current.equals(payload)) throw new Error("R0.73S PDF binding manifest is stale");
}

console.log(JSON.stringify({
  applied: apply,
  checked: !apply,
  documents: rows.length,
  output: "research/r073s_pdf_bindings.json",
}));
