#!/usr/bin/env node

// Render and cryptographically bind the Chinese R0.75Y note.
// The R0.75W milestone recap remains byte-exact; this analytic release has no formal figure.

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { createReadStream } from "node:fs";
import { createServer } from "node:http";
import { readFile, writeFile } from "node:fs/promises";
import { extname, resolve } from "node:path";
import { inspectPdf } from "./render-note-pdf.mjs";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const recapExpected = {
  "public/recap-r0-61-r0-75w.html": "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc",
  "public/recap-r0-61-r0-75w.pdf": "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce",
};

function run(executable, arguments_, options = {}) {
  return new Promise((resolvePromise, reject) => {
    const child = spawn(executable, arguments_, {
      cwd: root,
      env: { ...process.env, ...options.env },
      stdio: ["ignore", "pipe", "pipe"],
    });
    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", reject);
    child.on("close", (status) => status === 0
      ? resolvePromise({ stdout, stderr })
      : reject(new Error(`${executable} ${arguments_.join(" ")} failed (${status}): ${stderr || stdout}`)));
  });
}

function contentType(filePath) {
  return new Map([
    [".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"],
    [".css", "text/css; charset=utf-8"], [".svg", "image/svg+xml"],
    [".png", "image/png"], [".pdf", "application/pdf"], [".json", "application/json"],
  ]).get(extname(filePath).toLowerCase()) ?? "application/octet-stream";
}

for (const [relative, expected] of Object.entries(recapExpected)) {
  if (sha256(await readFile(resolve(root, relative))) !== expected) throw new Error(`W recap drift before PDF binding: ${relative}`);
}

const server = createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
  const relative = pathname === "/" ? "research-review.html" : pathname.replace(/^\/+/, "");
  const target = resolve(publicRoot, relative);
  if (!target.startsWith(`${publicRoot}/`)) {
    response.writeHead(403).end();
    return;
  }
  response.setHeader("Content-Type", contentType(target));
  const stream = createReadStream(target);
  stream.on("error", () => response.writeHead(404).end());
  stream.pipe(response);
});

await new Promise((resolvePromise, reject) => {
  server.once("error", reject);
  server.listen(0, "127.0.0.1", resolvePromise);
});

try {
  const address = server.address();
  const htmlRelative = "public/notes/r0-75y.html";
  const pdfRelative = "public/notes/r0-75y.pdf";
  const provenanceRelative = "research/r075y_note_pdf_render.json";
  const bindingRelative = "research/r075y_pdf_bindings.json";
  const url = `http://127.0.0.1:${address.port}/notes/r0-75y.html?lang=zh`;
  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.75Y｜强分离多谐波族的完整 signed-flux 付款";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);
  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r075y-step50-note-synchronized-pdf-binding-v1",
    release: "R0.75Y",
    step: 50,
    kind: "strongly-separated-multimode-signed-flux-note",
    publicChineseHtml: { path: htmlRelative, bytes: html.length, sha256: sha256(html) },
    publicPdf: {
      path: pdfRelative,
      bytes: pdf.length,
      sha256: sha256(pdf),
      pageCount: structure.pageCount,
      title: structure.title,
      structure,
    },
    provenance: {
      path: provenanceRelative,
      bytes: provenanceBytes.length,
      sha256: sha256(provenanceBytes),
      sourceUrl: provenance.source.url,
      loadedMainDocumentEqualsSourceHtml: true,
    },
    frozenAuthority: {
      sourceRepository: "/Users/kasifa/Documents/Math/navier-stokes-r074m",
      sourceCommit: "cb150f97a6c2595066360c0d4c6aca3c4062bdbe",
      handoffCommit: null,
      coreParentCommit: "4d12592f991e2cbb7db65f5470579783c2791fab",
      handoffSha256: "945d918d54b0309c340b8aa3048e0ddd2f624c302eb687331b8a9312807a1c17",
      handoffIndependentAuditSha256: "327cefd9cefe0c1878c5f5b2b4ba96105e2a1b0376a23a29cb8d3acb65ee0763",
      frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      harmonicScope: "STRONGLY_SEPARATED_FINITE_REAL_FAMILY_ONE_DYADIC_BAND",
      dyadicBandCondition: "ONE_LE_N1_LT_DOTS_LT_NQ_LE_2N1",
      signedSpectrumGap: "DELTA_N_MIN_OF_2N1_AND_POSITIVE_PAIRWISE_DIFFERENCES",
      strongSeparationCondition: "A_R_DELTA_N_GE_8Q",
      growingQClass: "INCREASINGLY_SPARSE_N1_A_R_GE_8Q_Q_MINUS_1_FOR_Q_GE_2",
      signedSpectrumGram: "PROVED_Y15_Y19_PHASE_UNIFORM_HALF_DIAGONAL",
      phaseFreeCompleteClock: "PROVED_Y20_Y25_WITH_ETA_ZERO_ONSET_AND_PHYSICAL_R_MINUS_4_OVER_3_ROW_SCALE",
      modalRowCount: "EXACTLY_Q_SQUARED_SELF_DIFFERENCE_SUM_ROWS",
      explicitModeCountCost: "Q_SQUARED_NO_HIDDEN_Q_CONSTANT",
      physicalPayment: "C_Q_SQUARED_A_TO_2_OVER_3_R_MINUS_1_OVER_3_M_PLAT_TO_2_OVER_3",
      normalizedEstimate: "C_Q_SQUARED_A_TO_2_OVER_3_OMEGA_TO_1_OVER_3_P_PLAT_TO_2_OVER_3",
      exactL2Rate: "MINUS_2_OVER_11907_FIXED_Q",
      growingQRate: "MINUS_2_OVER_11907_IF_LOG_Q_O_L_SQUARED_AND_STRONG_SEPARATION_CONTINUES",
      exactSmoothUnforcedShearSolution: "PROVED_Y38",
      versionMSameVelocityInclusion: "CONDITIONAL_MEASUREMENT_WEIGHT_REALIZED_SUBCLASS_ACTUAL_COMPONENT_LEDGER_ALIGNMENT",
      finiteChecksAsContinuumProof: false,
      unresolvedHighCarrierClusters: "OPEN_A_R_DELTA_N_LT_8Q",
      weakenedSeparation: "OPEN_NOT_PROVED",
      arbitraryPacketsAndInterPacketAggregation: "OPEN_NOT_PROVED",
      projectionFromLargerVelocity: "OPEN_NOT_PROVED",
      nonconstantOrVerticallyDependentShear: "OPEN_NOT_PROVED",
      e24: "OPEN_NOT_PROVED",
      completeVersionMExtraction: "OPEN_NOT_PROVED",
      fixedDeletion: "OPEN_NOT_PROVED",
      suitableWeakTransfer: "OPEN_NOT_PROVED",
      regularityOrSingularityClaim: false,
      literatureScreen: "bounded finite non-hit only",
      noveltyPriorityCorrectnessOrPublishabilityClaim: false,
      formalScientificFigure: false,
      pdeData: false,
      dns: false,
      simulation: false,
      dgxUsed: false,
      clayClaim: false,
    },
    formalFigure: {
      required: false,
      status: "NOT APPLICABLE",
      exemptionManifest: "research/r075y_freeze_manifest.json",
    },
    cumulativeRecap: {
      required: false,
      updatedThrough: "R0.75W",
      terminalStep: 48,
      nodeCount: 191,
      retainedHtmlPath: "public/recap-r0-61-r0-75w.html",
      retainedHtmlSha256: recapExpected["public/recap-r0-61-r0-75w.html"],
      retainedPdfPath: "public/recap-r0-61-r0-75w.pdf",
      retainedPdfSha256: recapExpected["public/recap-r0-61-r0-75w.pdf"],
    },
  };
  await writeFile(resolve(root, bindingRelative), `${JSON.stringify(binding, null, 2)}\n`);

  for (const [relative, expected] of Object.entries(recapExpected)) {
    if (sha256(await readFile(resolve(root, relative))) !== expected) throw new Error(`W recap drift after PDF binding: ${relative}`);
  }
  process.stdout.write(`${JSON.stringify({
    status: "bound",
    release: "R0.75Y",
    step: 50,
    output: {
      pageCount: structure.pageCount,
      pdfBytes: pdf.length,
      pdfSha256: binding.publicPdf.sha256,
      sourceHtmlSha256: binding.publicChineseHtml.sha256,
    },
    formalScientificFigure: false,
    recapUpdated: false,
    retainedRecap: "R0.75W",
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
