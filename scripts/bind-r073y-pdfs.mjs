#!/usr/bin/env node

// Cryptographically bind the synchronized R0.73Y PDFs to their HTML sources
// and independently parse hexadecimal UTF-16BE PDF title metadata. This is a
// publication-integrity check, never a mathematical-correctness certificate.

import { createHash } from "node:crypto";
import { constants as fsConstants } from "node:fs";
import { lstat, open, readdir, rename, unlink } from "node:fs/promises";
import { basename, dirname, isAbsolute, relative, resolve, sep } from "node:path";

const usage =
  "usage: bind-r073y-pdfs.mjs (--apply | --check-only | " +
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

const root = resolve(process.env.R073Y_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const outputPath = resolve(root, "research/r073y_pdf_bindings.json");
const reportPath = resolve(root, "research/r073y_report-source.md");
const dictionaryPath = resolve(root, "research/r073y_bilingual_dictionary.md");
const correctionPath = resolve(root, "research/r073y_reader_quantifier_correction.md");
const rendererRelative = "scripts/render-note-pdf.mjs";
const apply = selected[0] === "--apply";
const releaseTitle = "R0.73Y | Exact shear class rules out production-only coercivity";
const publicTitle = "R0.73Y｜Exact shear 类否定 production-only coercivity";
const documentTitle = "R0.73Y｜Exact shear class rules out production-only coercivity";
const figureId = "fig-r073y-exact-shear-obstruction";
const figureSourceCommit = "e37bf12cb5c2a8eb975e5097229dbc48fa597b35";
const figurePackageCommit = "05fdbc717a02be9f88fafc2b67a658e706b40be4";
const protectedHistorical = new Map([
  ["public/notes/r0-73x.html", "5e98103df24a01b690fca104938c65dec96ad00f7d40e2c9798e7dc859d6afcb"],
  ["public/notes/r0-73x.pdf", "0c1c97a754fe2c15310dff184c2d3ed142c40c53e400f5ba4895757808e267c7"],
  ["public/recap-r0-61-r0-73x.html", "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776"],
  ["public/recap-r0-61-r0-73x.pdf", "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa"],
  ["research/r073x_pdf_bindings.json", "e255810c20c13c8c90020847685048a1dde88bf513b33e7440bb7ccec5507f87"],
  ["research/r073x_recap_pdf_render.json", "a19ca701c402504e4e0b93d2ca442fdd665aa93219caa726d64f3f5ff3c00101"],
]);
const protectedRecapAssetCount = 154;
const protectedRecapLedgerSha256 = "f76860a8a3d8f1b3cd83b98e566bc3ffd09461175c234dfffe35864f05b5d643";

function sha256(payload) {
  return createHash("sha256").update(payload).digest("hex");
}

function assertInsideRoot(path, label) {
  const offset = relative(root, path);
  if (!offset || offset === ".." || offset.startsWith("../") || offset.startsWith("..\\")) {
    throw new Error(label + " escaped R073Y_RELEASE_ROOT");
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
    `.${basename(path)}.r073y-${process.pid}-${Date.now()}-${process.hrtime.bigint()}.tmp`,
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
const correction = (await regularBytes(correctionPath)).toString("utf8");
if (/[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]/.test(report + dictionary + correction)) {
  throw new Error("R0.73Y canonical report, dictionary, or reader correction contains control characters");
}
if (!report.startsWith("# " + publicTitle + "\n") ||
    !dictionary.includes("**Release title:** " + releaseTitle) ||
    !dictionary.includes("**Public title (zh):** " + publicTitle) ||
    !dictionary.includes("**Latest recap release:** r073x")) {
  throw new Error("R0.73Y canonical report title ledger drift");
}
const boundaryCorpus = (report + "\n" + dictionary)
  .replace(/^>\s?/gm, "")
  .replace(/\s+/g, " ");
for (const token of [
  "typesettingNormalization=EXACT_COUNTED_NONSEMANTIC_REPAIRS",
  "zeroProduction=ALL_REAL_A",
  "strictGradientCovariance=ONLY_A_NE_0",
  "zeroAmplitudeGradientCovariance=0",
]) {
  if (!correction.includes(token)) {
    throw new Error("R0.73Y reader correction missing " + token);
  }
}
for (const phrase of [
  "production-only 形式下是假的",
  "production-only no-go package",
  "直接重合",
  "不能申报为新发现",
  "本节对整个 Clay 问题的直接推进很小",
  "LOCAL_DIRECT_NO_DGX",
  "NOT CLAY",
]) {
  if (!boundaryCorpus.includes(phrase)) {
    throw new Error("R0.73Y canonical sources missing boundary phrase: " + phrase);
  }
}
for (const token of [
  "exactShearNSE=PROVED_ANALYTICALLY",
  "allPositiveHeatScalesZeroProduction=PROVED_ANALYTICALLY",
  "gradientCovarianceStrictlyPositiveForAneq0AndSgt0=PROVED_ANALYTICALLY",
  "zeroAmplitudeMemberCovariance=ZERO",
  "positiveSizeCubicHomogeneity=PROVED_ANALYTICALLY",
  "productionOnlyCoercivity=REFUTED_FOR_ZERO_PRESERVING_FUNCTIONALS",
  "singleFourierCertificate=FINITE_CROSS_CHECK_ONLY",
  "strictPositivityFromSampling=FALSE",
  "basicShearNoveltyOrPriority=NOT_CLAIMED",
  "quotientCoercivity=OPEN",
  "pressureActiveInvisibleFamily=OPEN",
  "suitableWeakZeroScaleEndpoint=OPEN",
  "epsilonRegularity=OPEN",
  "formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED",
  "formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES",
  "navierStokesSimulation=NOT_RUN",
  "directNumericalSimulation=NOT_RUN",
  "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
  "dgxUsed=false",
  "latestPublishedRelease=r073y",
  "latestRecapRelease=r073x",
  "recapPolicy=MILESTONE_ONLY",
  "arbitraryThreeDimensionalGlobalRegularity=OPEN",
  "clayConclusion=OPEN",
  "NOT CLAY",
]) {
  if (!boundaryCorpus.includes(token)) throw new Error("R0.73Y canonical boundary missing " + token);
}

const releaseManifest = JSON.parse((await regularBytes("research/release-manifest.json")).toString("utf8"));
const siteVersion = JSON.parse((await regularBytes("public/site-version.json")).toString("utf8"));
if (
  releaseManifest.latestCompletedRelease !== "r073y" ||
  releaseManifest.siteVersion !== "1.65" ||
  releaseManifest.publicHtmlNoteCount !== 201 ||
  releaseManifest.postR060PublishedNodeCount !== 141 ||
  releaseManifest.postR060RecapNodeCount !== 140 ||
  releaseManifest.latestRecapRelease !== "r073x" ||
  releaseManifest.nextRelease !== "r073z" ||
  releaseManifest.postR070APublishedReleaseCount !== 103 ||
  releaseManifest.postR070AFormalSealedReleaseCount !== 79 ||
  releaseManifest.legacyFormalFigureBacklogCount !== 24 ||
  releaseManifest.publicPdfNoteCount !== 158 ||
  siteVersion.latestRelease !== "R0.73Y" ||
  siteVersion.version !== "1.65" ||
  siteVersion.publicHtmlNoteCount !== 201 ||
  siteVersion.postR060PublishedNodeCount !== 141 ||
  siteVersion.postR060RecapNodeCount !== 140 ||
  siteVersion.latestRecapRelease !== "R0.73X" ||
  siteVersion.publicPdfNoteCount !== 158
) {
  throw new Error("R0.73Y HTML/accounting apply must precede PDF binding");
}

const certificateManifest = JSON.parse((await regularBytes(
  "research/certificates/r073y/manifest.json",
)).toString("utf8"));
const certificateChecklist = JSON.parse((await regularBytes(
  "research/certificates/r073y/audit-checklist.json",
)).toString("utf8"));
const figureValidation = JSON.parse((await regularBytes(
  `research/figures/r073y/${figureId}/validation.json`,
)).toString("utf8"));
const figureResults = JSON.parse((await regularBytes(
  `research/figures/r073y/${figureId}/results.json`,
)).toString("utf8"));
const figureManifest = JSON.parse((await regularBytes(
  `research/figures/r073y/${figureId}/manifest.json`,
)).toString("utf8"));
const figureContract = JSON.parse((await regularBytes(
  `research/figures/r073y/${figureId}/contract.json`,
)).toString("utf8"));
const certificateChecks = Array.isArray(certificateChecklist.checks)
  ? certificateChecklist.checks.length : null;
const figureChecks = figureValidation.required ?? figureValidation.checksRequired ??
  figureValidation.checkCount;
const figurePassed = figureValidation.passed ?? figureValidation.checksPassed ??
  figureValidation.passCount ??
  (figureValidation.allChecksPass === true && Array.isArray(figureValidation.checks)
    ? figureValidation.checks.length : null);
const figureRows = figureResults.rowCounts?.total;
const panelRowCounts = figureResults.rowCounts;
const certificateInventory = certificateManifest.inventory;
const certificateInventoryKeys = certificateInventory && typeof certificateInventory === "object" &&
  !Array.isArray(certificateInventory) ? Object.keys(certificateInventory).sort() : [];
if (
  certificateManifest.schema !== "r073y-formal-certificate-manifest-v1" ||
  certificateManifest.status !== "SEALED" ||
  certificateManifest.source?.git_commit_sha1 !== "1ecc6fe20a921db9d0876dbd4484a3aa4ca7ec66" ||
  JSON.stringify(certificateInventoryKeys) !== JSON.stringify([
    "manifest_entry_count", "package_file_count", "sha256sums_entry_count",
  ]) ||
  certificateInventory.package_file_count !== 13 ||
  certificateInventory.manifest_entry_count !== 11 ||
  certificateInventory.sha256sums_entry_count !== 12 ||
  !Number.isInteger(certificateChecks) || certificateChecks <= 0 ||
  certificateChecklist.schema !== "r073y-formal-certificate-audit-v1" ||
  certificateChecklist.status !== "PASS" ||
  certificateChecklist.not_clay !== true ||
  certificateManifest.claim_boundary?.production_only_coercive_bridge !== "FALSE_BY_EXACT_NSE_FAMILY" ||
  certificateManifest.claim_boundary?.clay_problem_solved !== false ||
  figureManifest.seal?.figureSourceCommit !== figureSourceCommit ||
  figureManifest.git?.figureSourceCommit !== figureSourceCommit ||
  figureManifest.publication?.figureSourceCommit !== figureSourceCommit ||
  figureManifest.publication?.figurePackageCommit !== figurePackageCommit ||
  figureContract.claimBoundary?.strictGradientCovarianceRequiresNonzeroAmplitude !== true ||
  figureContract.claimBoundary?.zeroAmplitudeMemberCovariance !== "zero" ||
  figureValidation.schemaVersion !== "r073y-exact-shear-validation-v3" ||
  figureValidation.status !== "PASS" ||
  figureValidation.sealState !== "formal-figure-source-seal" ||
  figurePassed !== figureChecks ||
  figureValidation.checks?.length !== figureChecks ||
  figureResults.schema !== "r073y-exact-shear-results-v2" ||
  figureResults.status !== "PASS" ||
  figureResults.claimBoundary?.analyticExactWitness !== true ||
  figureResults.claimBoundary?.dns !== false ||
  figureResults.claimBoundary?.notClay !== true ||
  !panelRowCounts ||
  panelRowCounts.A + panelRowCounts.B + panelRowCounts.C !== figureRows ||
  !Number.isInteger(figureChecks) || figureChecks <= 0 ||
  !Number.isInteger(figureRows) || figureRows <= 0
) {
  throw new Error("R0.73Y sealed certificate/figure accounting drifted");
}

const documents = [
  {
    kind: "research-note",
    html: "public/notes/r0-73y.html",
    pdf: "public/notes/r0-73y.pdf",
    provenance: "research/r073y_note_pdf_render.json",
    route: "/notes/r0-73y.html",
    title: documentTitle,
    htmlMarkers: [
      publicTitle,
      "productionOnlyCoercivity=REFUTED_FOR_ZERO_PRESERVING_FUNCTIONALS",
      "production 对所有实振幅为零",
      "gradient covariance：STRICTLY POSITIVE FOR A ≠ 0; ZERO FOR A = 0",
      "A = 0 时为平凡零场",
      figureId,
      "NOT CLAY",
    ],
  },
];

const recapDirectoryEntries = await readdir(rootedPath("public", "recap directory"), {
  withFileTypes: true,
});
for (const entry of recapDirectoryEntries) {
  if (/^recap-[^/]+\.(?:html|pdf)$/.test(entry.name) && !entry.isFile()) {
    throw new Error("unsafe public recap artifact: public/" + entry.name);
  }
}
const researchDirectoryEntries = await readdir(rootedPath("research", "research directory"), {
  withFileTypes: true,
});
for (const entry of researchDirectoryEntries) {
  if (/^r073y.*recap/i.test(entry.name)) {
    throw new Error("note-only R0.73Y release contains an undeclared recap artifact: research/" + entry.name);
  }
}
const protectedRecapPaths = recapDirectoryEntries
  .filter((entry) => entry.isFile() && /^recap-[^/]+\.(?:html|pdf)$/.test(entry.name))
  .map((entry) => "public/" + entry.name);
protectedRecapPaths.push(
  "research/r073x_pdf_bindings.json",
  "research/r073x_recap_pdf_render.json",
);
protectedRecapPaths.sort();
if (protectedRecapPaths.length !== protectedRecapAssetCount) {
  throw new Error("protected recap-asset inventory drifted");
}
const protectedRecapLedgerRows = [];
for (const path of protectedRecapPaths) {
  protectedRecapLedgerRows.push(`${sha256(await regularBytes(path))}  ${path}`);
}
const actualRecapLedgerSha256 = sha256(
  Buffer.from(protectedRecapLedgerRows.join("\n") + "\n", "utf8"),
);
if (actualRecapLedgerSha256 !== protectedRecapLedgerSha256) {
  throw new Error("protected 154-file recap SHA ledger drifted");
}

for (const [path, expected] of protectedHistorical) {
  const payload = await regularBytes(path);
  if (sha256(payload) !== expected) {
    throw new Error("protected R0.73X note/recap/PDF binding drifted: " + path);
  }
}

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
  schemaVersion: "r073y-synchronized-pdf-bindings-v1",
  release: "R0.73Y",
  canonicalTitleSource: {
    path: "research/r073y_report-source.md",
    sha256: sha256(Buffer.from(report)),
    releaseTitle,
    publicChineseTitle: publicTitle,
  },
  canonicalBoundarySource: {
    path: "research/r073y_bilingual_dictionary.md",
    sha256: sha256(Buffer.from(dictionary)),
  },
  canonicalCorrectionSource: {
    path: "research/r073y_reader_quantifier_correction.md",
    sha256: sha256(Buffer.from(correction)),
    typesettingNormalization: "EXACT_COUNTED_NONSEMANTIC_REPAIRS",
    zeroProduction: "ALL_REAL_A",
    strictGradientCovariance: "ONLY_A_NE_0",
    zeroAmplitudeGradientCovariance: 0,
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
    exactShearNSE: "PROVED_ANALYTICALLY",
    allPositiveHeatScalesZeroProduction: "PROVED_ANALYTICALLY",
    gradientCovarianceStrictlyPositiveForAneq0AndSgt0: "PROVED_ANALYTICALLY",
    zeroAmplitudeMemberCovariance: "ZERO",
    zeroProduction: "ALL_REAL_A",
    strictGradientCovariance: "ONLY_A_NE_0",
    zeroAmplitudeGradientCovariance: 0,
    positiveSizeCubicHomogeneity: "PROVED_ANALYTICALLY",
    productionOnlyCoercivity: "REFUTED_FOR_ZERO_PRESERVING_FUNCTIONALS",
    singleFourierCertificate: "FINITE_CROSS_CHECK_ONLY",
    strictPositivityFromSampling: false,
    basicShearNoveltyOrPriority: "NOT_CLAIMED",
    quotientCoercivity: "OPEN",
    pressureActiveInvisibleFamily: "OPEN",
    suitableWeakZeroScaleEndpoint: "OPEN",
    epsilonRegularity: "OPEN",
    formalEvidenceCertificate: "SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED",
    formalEvidenceAuditFields: certificateChecks,
    formalFigureChecks: figureChecks,
    formalFigureRows: figureRows,
    navierStokesSimulation: false,
    directNumericalSimulation: false,
    arbitraryThreeDimensionalGlobalRegularity: "OPEN",
    ordinaryTranslationPath: "LOCAL_DIRECT_NO_DGX",
    dgxUsed: false,
    clayConclusion: "OPEN",
    pdfBindingCertifiesMathematicalCorrectness: false,
    pdfBindingEstablishesNoveltyOrPriority: false,
    figureScope: "ANALYTIC_EXACT_WITNESS_NOT_DNS",
    latestRecapRelease: "R0.73X",
    recapGenerated: false,
    clayProblemSolved: false,
  },
};
const payload = Buffer.from(JSON.stringify(manifest, null, 2) + "\n");

if (apply) {
  await atomicWrite(outputPath, payload);
} else {
  const current = await regularBytes(outputPath);
  if (!current.equals(payload)) throw new Error("R0.73Y PDF binding manifest is stale");
}

console.log(JSON.stringify({
  applied: apply,
  checked: !apply,
  documents: rows.length,
  output: "research/r073y_pdf_bindings.json",
  translationPath: "LOCAL_DIRECT_NO_DGX",
  dgxUsed: false,
}));
