#!/usr/bin/env node

// Cryptographically bind the synchronized R0.73T PDFs to their HTML sources
// and independently parse hexadecimal UTF-16BE PDF title metadata. This is a
// publication-integrity check, never a mathematical-correctness certificate.

import { createHash } from "node:crypto";
import { constants as fsConstants } from "node:fs";
import { lstat, open, rename, unlink } from "node:fs/promises";
import { basename, dirname, isAbsolute, relative, resolve, sep } from "node:path";

const usage =
  "usage: bind-r073t-pdfs.mjs (--apply | --check-only | " +
  "--structure-check PDF EXPECTED_TITLE)";
const selected = process.argv.slice(2);
if (selected.includes("--help") || selected.includes("-h")) {
  console.log(usage);
  process.exit(0);
}
const structureCheck = selected[0] === "--structure-check";
if ((!structureCheck && (selected.length !== 1 ||
     !["--apply", "--check-only"].includes(selected[0]))) ||
    (structureCheck && selected.length !== 3)) {
  throw new Error(usage);
}

const root = resolve(process.env.R073T_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const outputPath = resolve(root, "research/r073t_pdf_bindings.json");
const reportPath = resolve(root, "research/r073t_report-source.md");
const dictionaryPath = resolve(root, "research/r073t_bilingual_dictionary.md");
const rendererRelative = "scripts/render-note-pdf.mjs";
const apply = selected[0] === "--apply";
const releaseTitle = "R0.73T | Dynamic autocorrelation and the pressure-tensor barrier";
const publicTitle = "R0.73T｜自相关进入动力学：一个临界一侧估计与压力张量障碍";
const documentTitle = "R0.73T｜Dynamic autocorrelation and the pressure-tensor barrier";
const recapTitle = "R0.61–R0.73T｜R0.60 之后的研究回顾";
const figureId = "fig-r073t-dynamic-autocorrelation";

function sha256(payload) {
  return createHash("sha256").update(payload).digest("hex");
}

function assertInsideRoot(path, label) {
  const offset = relative(root, path);
  if (!offset || offset === ".." || offset.startsWith("../") || offset.startsWith("..\\")) {
    throw new Error(label + " escaped R073T_RELEASE_ROOT");
  }
}

function rootedPath(relativeOrAbsolute, label) {
  const path = isAbsolute(relativeOrAbsolute)
    ? resolve(relativeOrAbsolute)
    : resolve(root, relativeOrAbsolute);
  assertInsideRoot(path, label);
  return path;
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
  await assertSafeDirectoryChain(dirname(path), label);
  try {
    const info = await lstat(path);
    if (info.isSymbolicLink() || !info.isFile()) {
      throw new Error(`${label}: expected regular nonsymlink file ${path}`);
    }
    return true;
  } catch (error) {
    if (allowMissing && error?.code === "ENOENT") return false;
    throw error;
  }
}

async function regularBytes(relativeOrAbsolute) {
  const path = rootedPath(relativeOrAbsolute, "PDF binding input");
  await assertSafeFileTarget(path, "PDF binding input");
  const handle = await open(path, fsConstants.O_RDONLY | fsConstants.O_NOFOLLOW);
  try {
    const info = await handle.stat();
    if (!info.isFile()) throw new Error(path + ": opened input is not a regular file");
    return await handle.readFile();
  } finally {
    await handle.close();
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

function literalTitle(value, offset, label) {
  const bytes = [];
  let depth = 1;
  for (let index = offset + 1; index < value.length;) {
    const code = value.charCodeAt(index) & 0xff;
    if (code === 0x5c) {
      index += 1;
      if (index >= value.length) throw new Error(label + ": unterminated title escape");
      const escaped = value.charCodeAt(index) & 0xff;
      const controls = { 0x6e: 0x0a, 0x72: 0x0d, 0x74: 0x09, 0x62: 0x08, 0x66: 0x0c };
      if (escaped in controls) {
        bytes.push(controls[escaped]);
        index += 1;
      } else if (escaped === 0x0d || escaped === 0x0a) {
        if (escaped === 0x0d && value.charCodeAt(index + 1) === 0x0a) index += 1;
        index += 1;
      } else if (escaped >= 0x30 && escaped <= 0x37) {
        let octal = String.fromCharCode(escaped);
        index += 1;
        while (octal.length < 3 && value.charCodeAt(index) >= 0x30 &&
               value.charCodeAt(index) <= 0x37) {
          octal += value[index];
          index += 1;
        }
        bytes.push(Number.parseInt(octal, 8));
      } else {
        bytes.push(escaped);
        index += 1;
      }
    } else if (code === 0x28) {
      depth += 1;
      bytes.push(code);
      index += 1;
    } else if (code === 0x29) {
      depth -= 1;
      if (depth === 0) return { title: decodePdfString(Buffer.from(bytes)), encoding: "literal" };
      bytes.push(code);
      index += 1;
    } else {
      bytes.push(code);
      index += 1;
    }
  }
  throw new Error(label + ": unterminated literal title");
}

function infoTitle(infoBody, label) {
  const marker = /\/Title\b/.exec(infoBody);
  if (!marker) throw new Error(label + ": /Title absent from /Info object");
  let offset = marker.index + marker[0].length;
  while (/\s/.test(infoBody[offset] ?? "")) offset += 1;
  if (infoBody[offset] === "<" && infoBody[offset + 1] !== "<") {
    const end = infoBody.indexOf(">", offset + 1);
    const hex = end < 0 ? "!" : infoBody.slice(offset + 1, end).replace(/\s+/g, "");
    if (!/^[0-9A-Fa-f]*$/.test(hex) || hex.length % 2 !== 0) {
      throw new Error(label + ": invalid hexadecimal title");
    }
    return { title: decodePdfString(Buffer.from(hex, "hex")), encoding: "hex" };
  }
  if (infoBody[offset] === "(") return literalTitle(infoBody, offset, label);
  throw new Error(label + ": /Title is not a hex or literal string");
}

function inspectPdf(payload, label) {
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
  const dictionaryStart = latin.indexOf("<<", trailerOffset);
  const dictionaryEnd = latin.indexOf(">>", dictionaryStart + 2);
  if (trailerOffset < startxref || dictionaryStart < 0 || dictionaryEnd < 0 ||
      dictionaryEnd > tail.index) {
    throw new Error(label + ": malformed trailer preceding startxref");
  }
  const info = /\/Info\s+(\d+)\s+(\d+)\s+R\b/.exec(
    latin.slice(dictionaryStart + 2, dictionaryEnd),
  );
  if (!info) throw new Error(label + ": trailer /Info reference is absent");
  const infoObject = `${info[1]} ${info[2]} R`;
  const object = new RegExp(
    String.raw`(?:^|[\r\n])${info[1]}\s+${info[2]}\s+obj\b([\s\S]*?)endobj\b`,
  ).exec(latin);
  if (!object) throw new Error(label + ": referenced /Info object is absent");
  const parsed = infoTitle(object[1], label);
  return {
    header: "%PDF", eof: true, startxref, xrefKeyword: "xref", pageCount,
    infoObject, title: parsed.title, titleEncoding: parsed.encoding,
  };
}

async function atomicWrite(path, payload) {
  path = rootedPath(path, "PDF binding output");
  await assertSafeFileTarget(path, "PDF binding output", true);
  const temporary = resolve(
    dirname(path),
    `.${basename(path)}.r073t-${process.pid}-${Date.now()}-${process.hrtime.bigint()}.tmp`,
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
    await assertSafeFileTarget(path, "PDF binding rename target", true);
    await assertSafeFileTarget(temporary, "PDF binding rename source");
    await rename(temporary, path);
    await assertSafeFileTarget(path, "PDF binding installed output");
    const directory = await open(
      dirname(path), fsConstants.O_RDONLY | fsConstants.O_NOFOLLOW,
    );
    try {
      await directory.sync();
    } finally {
      await directory.close();
    }
  } finally {
    try {
      const info = await lstat(temporary);
      if (info.isSymbolicLink() || !info.isFile()) {
        throw new Error("unsafe PDF binding scratch path: " + temporary);
      }
      await unlink(temporary);
    } catch (error) {
      if (error?.code !== "ENOENT") throw error;
    }
  }
}

if (structureCheck) {
  const payload = await regularBytes(selected[1]);
  const structure = inspectPdf(payload, selected[1]);
  if (structure.title !== selected[2]) {
    throw new Error("structure-check title drift: " + JSON.stringify(structure.title));
  }
  console.log(JSON.stringify(structure));
  process.exit(0);
}

const report = (await regularBytes(reportPath)).toString("utf8");
const dictionary = (await regularBytes(dictionaryPath)).toString("utf8");
if (/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(report + dictionary)) {
  throw new Error("R0.73T canonical report or dictionary contains control characters");
}
if (!report.startsWith("# " + releaseTitle + "\n") ||
    !report.includes("**Public title (zh):** " + publicTitle)) {
  throw new Error("R0.73T canonical report title ledger drift");
}
const boundaryCorpus = (report + "\n" + dictionary).replace(/\s+/g, " ");
for (const phrase of [
  "not asserted as a new regularity criterion",
  "not a new dynamical theorem",
  "has the same \\(u\\otimes u\\) and the same \\(p\\)",
  "not a witness that \\(p\\) or the quadratic tensor \\(u\\otimes u\\) differs",
  "reconstructing \\(p\\) requires the tensor",
  "not a Navier--Stokes simulation",
  "non-detection is not proof of novelty, priority, or non-existence",
  "Clay Millennium problem remain open",
]) {
  if (!boundaryCorpus.includes(phrase)) {
    throw new Error("R0.73T canonical sources missing boundary phrase: " + phrase);
  }
}
for (const token of [
  "exactAutocorrelationEvolution=VERIFIED_CLASSICAL_RECONSTRUCTION",
  "dynamicAQUpperInequality=INTERNAL_COROLLARY",
  "criticalAIntegralControl=OPEN",
  "carrierScaleNonAutonomy=CLOSED_EXACT",
  "signedVelocityPhaseInPressurePairing=CLOSED_EXACT",
  "pressureTensorNeededForGeneralReconstruction=VERIFIED_CLASSICAL",
  "finiteFormulaDiagnosticChecks=55",
  "formalFigureChecks=106",
  "arbitraryThreeDimensionalGlobalRegularity=OPEN",
  "clayConclusion=OPEN",
]) {
  if (!report.includes(token)) throw new Error("R0.73T report missing " + token);
}

const releaseManifest = JSON.parse((await regularBytes("research/release-manifest.json")).toString("utf8"));
const siteVersion = JSON.parse((await regularBytes("public/site-version.json")).toString("utf8"));
if (
  releaseManifest.latestCompletedRelease !== "r073t" ||
  releaseManifest.siteVersion !== "1.60" ||
  releaseManifest.publicHtmlNoteCount !== 196 ||
  releaseManifest.postR060RecapNodeCount !== 136 ||
  releaseManifest.nextRelease !== "r073u" ||
  releaseManifest.postR070APublishedReleaseCount !== 98 ||
  releaseManifest.postR070AFormalSealedReleaseCount !== 74 ||
  releaseManifest.legacyFormalFigureBacklogCount !== 24 ||
  siteVersion.latestRelease !== "R0.73T" ||
  siteVersion.version !== "1.60" ||
  siteVersion.publicHtmlNoteCount !== 196
) {
  throw new Error("R0.73T HTML/accounting apply must precede PDF binding");
}

const documents = [
  {
    kind: "research-note",
    html: "public/notes/r0-73t.html",
    pdf: "public/notes/r0-73t.pdf",
    provenance: "research/r073t_note_pdf_render.json",
    route: "/notes/r0-73t.html",
    title: documentTitle,
    htmlMarkers: [publicTitle, "dynamicAQUpperInequality=INTERNAL_COROLLARY", figureId],
  },
  {
    kind: "cumulative-recap",
    html: "public/recap-r0-61-r0-73t.html",
    pdf: "public/recap-r0-61-r0-73t.pdf",
    provenance: "research/r073t_recap_pdf_render.json",
    route: "/recap-r0-61-r0-73t.html",
    title: recapTitle,
    htmlMarkers: ["R0.73T", "136", "tensorHeatClosure=OPEN"],
  },
];

const renderer = await regularBytes(rendererRelative);
const rows = [];
for (const document of documents) {
  const [html, pdf, provenanceBytes] = await Promise.all([
    regularBytes(document.html),
    regularBytes(document.pdf),
    regularBytes(document.provenance),
  ]);
  const htmlText = html.toString("utf8");
  for (const marker of document.htmlMarkers) {
    if (!htmlText.includes(marker)) throw new Error(document.html + ": missing " + marker);
  }
  if (pdf.length <= 10_000) {
    throw new Error(document.pdf + ": malformed or unexpectedly small PDF");
  }
  const structure = inspectPdf(pdf, document.pdf);
  if (structure.title !== document.title) {
    throw new Error(document.pdf + ": PDF title drift: " + JSON.stringify(structure.title));
  }
  let provenance;
  try {
    provenance = JSON.parse(provenanceBytes.toString("utf8"));
  } catch (error) {
    throw new Error(document.provenance + ": invalid JSON: " + error.message);
  }
  if (provenance?.schemaVersion !== "synchronized-pdf-render-provenance-v1") {
    throw new Error(document.provenance + ": schema drift");
  }
  const sourceUrl = new URL(provenance.source?.url ?? "about:blank");
  if (
    sourceUrl.pathname !== document.route ||
    sourceUrl.searchParams.get("lang") !== "zh" ||
    provenance.source?.origin !== sourceUrl.origin ||
    provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) {
    throw new Error(document.provenance + ": URL/origin provenance drift");
  }
  const htmlRecord = { path: document.html, bytes: html.length, sha256: sha256(html) };
  const pdfRecord = {
    path: document.pdf, bytes: pdf.length, sha256: sha256(pdf),
    pageCount: structure.pageCount, title: structure.title,
  };
  const rendererRecord = {
    path: rendererRelative, bytes: renderer.length, sha256: sha256(renderer),
  };
  const recordsEqual = (actual, expected) => Object.entries(expected).every(
    ([key, value]) => actual?.[key] === value,
  );
  if (!recordsEqual(provenance.html, htmlRecord) ||
      !recordsEqual(provenance.pdf, pdfRecord) ||
      !recordsEqual(provenance.renderer, rendererRecord) ||
      !recordsEqual(provenance.loadedDocument, {
        bytes: html.length, sha256: sha256(html), equalsSourceHtml: true,
      }) ||
      JSON.stringify(provenance.structure) !== JSON.stringify(structure)) {
    throw new Error(document.provenance + ": current HTML/PDF/renderer/structure mismatch");
  }
  rows.push({
    kind: document.kind,
    html: htmlRecord,
    pdf: { ...pdfRecord, structure },
    provenance: {
      path: document.provenance,
      bytes: provenanceBytes.length,
      sha256: sha256(provenanceBytes),
      schemaVersion: provenance.schemaVersion,
      url: sourceUrl.href,
      origin: sourceUrl.origin,
      publicOrigin: provenance.source.publicOrigin,
    },
  });
}

const manifest = {
  schemaVersion: "r073t-synchronized-pdf-bindings-v1",
  release: "R0.73T",
  canonicalTitleSource: {
    path: "research/r073t_report-source.md",
    sha256: sha256(Buffer.from(report)),
    releaseTitle,
    publicChineseTitle: publicTitle,
  },
  canonicalBoundarySource: {
    path: "research/r073t_bilingual_dictionary.md",
    sha256: sha256(Buffer.from(dictionary)),
  },
  renderer: {
    path: rendererRelative,
    bytes: renderer.length,
    sha256: sha256(renderer),
    language: "zh",
    format: "A4",
  },
  documents: rows,
  claimBoundary: {
    htmlAndPdfBytesCryptographicallyBound: true,
    renderProvenanceSidecarsBound: true,
    loadedMainDocumentEqualsSourceHtml: true,
    pdfHeaderAndEofValidated: true,
    pdfStartxrefPointsToXref: true,
    pdfPageCountValidated: true,
    pdfTrailerInfoReferenceValidated: true,
    pdfTitleIndependentlyParsed: true,
    exactAutocorrelationEvolution: "VERIFIED_CLASSICAL_RECONSTRUCTION",
    dynamicAQUpperInequality: "INTERNAL_COROLLARY",
    criticalAIntegral: "INTERNAL_EXACT_SCALING",
    criticalAIntegralControl: "OPEN",
    carrierScaleNonAutonomy: "CLOSED_EXACT",
    signPairTensorAndPressureIdentical: "CLOSED_EXACT",
    signedVelocityPhaseInPressurePairing: "CLOSED_EXACT",
    pressureTensorNeededForGeneralReconstruction: "VERIFIED_CLASSICAL",
    finiteFormulaCertificateOnly: true,
    finiteFormulaDiagnosticChecks: 55,
    formalFigureChecks: 106,
    navierStokesSimulation: false,
    finiteWitnessImpliesSingularity: false,
    regularityCriterionImproved: false,
    arbitraryThreeDimensionalGlobalRegularity: "OPEN",
    tensorHeatClosure: "OPEN",
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
  if (!current.equals(payload)) throw new Error("R0.73T PDF binding manifest is stale");
}

console.log(JSON.stringify({
  applied: apply,
  checked: !apply,
  documents: rows.length,
  output: "research/r073t_pdf_bindings.json",
}));
