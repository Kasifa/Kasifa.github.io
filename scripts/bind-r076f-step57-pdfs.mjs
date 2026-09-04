#!/usr/bin/env node

// Render and cryptographically bind the Chinese R0.76F note.
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
  const htmlRelative = "public/notes/r0-76f.html";
  const pdfRelative = "public/notes/r0-76f.pdf";
  const provenanceRelative = "research/r076f_note_pdf_render.json";
  const bindingRelative = "research/r076f_pdf_bindings.json";
  const url = `http://127.0.0.1:${address.port}/notes/r0-76f.html?lang=zh`;
  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.76F｜继承空间观测的指数下界";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);
  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r076f-step57-note-synchronized-pdf-binding-v1",
    release: "R0.76F",
    step: 57,
    kind: "exponential-spatial-observation-lower-bound-exact-real-dyadic-shear-note",
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
      sourceCommit: "ff0254315b2fc4f2aaab1ee6f3f2ddcaaeac7366",
      handoffCommit: "52ee189e3dfaa2ea0924ed44cd2e1196b2ec3a5b",
      coreParentCommit: "01473589257b882c5b35e0d04fb58a71b36c9093",
      handoffSha256: "5bf493b8703bb33233d846d4db8d1c621320d565a80e02a339b17431325bf06c",
      handoffIndependentAuditSha256: "8a2ee0b0d69aa5002119da6db10f685230d2af48e2ed09f099fcd5c5153ca45b",
      frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      harmonicScope: "Q_AT_LEAST_TWO_EXACT_REAL_POSITIVE_FREQUENCY_DYADIC_BAND",
      integerModes: "N_J_EQUALS_Q_PLUS_J_MINUS_ONE",
      realPhases: "PHASE_ALIGNED_REAL_PART",
      nonnegativeAmplitudes: "BINOMIAL_COEFFICIENTS",
      spacing: "ZERO_LT_DELTA_LE_TWO_PI_OVER_THREE",
      nestedIntervals: "I_MINUS_HALF_TO_HALF_J_MINUS_THREE_HALVES_TO_THREE_HALVES",
      spatialObservationLowerBound: "AT_LEAST_TWO_TO_Q_MINUS_ONE",
      observationConstant: "LOG_C_Q_AT_LEAST_Q_MINUS_ONE_TIMES_LOG_TWO",
      uniformOrPolynomialQDependence: false,
      upperLowerOrderMatch: "EXP_THETA_Q_ONLY_NO_OPTIMAL_BASE_CLAIM",
      arbitraryPacketTheorem: false,
      exactShearEmbedding: "SMOOTH_UNFORCED_CONSTANT_PRESSURE_WITH_B_ZERO",
      completeTransportFlux: "ZERO_FOR_REALIZING_EXAMPLE",
      completeCollarFluxLowerBound: false,
      alternativeFullSpaceTimeCancellationExcluded: false,
      quadraticModeDensity: "CHANGES_EXACT_NORMALIZED_COEFFICIENT_ALONG_SUBSEQUENCE",
      smallQuadraticDensityMayRemainNegative: true,
      externalInputs: "GENERAL_TURAN_NAZAROV_AND_TRIGONOMETRIC_REMEZ_SHARPNESS_CONTEXT",
      localDeductions: "EXPLICIT_BINOMIAL_DYADIC_REAL_SHEAR_SPECIALIZATION_AND_TWO_TO_Q_MINUS_ONE_BOUND",
      finiteCertificateIsContinuumProof: false,
      arbitraryGrowingPackets: "OPEN_NOT_PROVED",
      nonconstantOrVerticalShear: "OPEN_NOT_PROVED",
      e24: "OPEN_NOT_PROVED",
      completeVersionMExtraction: "OPEN_NOT_PROVED",
      fixedDeletion: "OPEN_NOT_PROVED",
      suitableWeakTransfer: "OPEN_NOT_PROVED",
      regularityOrSingularityClaim: false,
      literatureScreen: "NAZAROV_FRIEDLAND_TIKHONOV_YUDITSKII_AND_ERDELYI_CONTEXT_NO_NOVELTY_CLAIM",
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
      exemptionManifest: "research/r076f_freeze_manifest.json",
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
    release: "R0.76F",
    step: 57,
    output: {
      pageCount: structure.pageCount,
      pdfBytes: pdf.length,
      pdfSha256: binding.publicPdf.sha256,
      sourceHtmlSha256: binding.publicChineseHtml.sha256,
    },
    formalScientificFigure: false,
    spatialObservationLowerBound: "TWO_TO_Q_MINUS_ONE",
    observationOrderSharpness: "EXP_THETA_Q",
    completeFluxLowerBoundClaim: false,
    arbitraryGrowingPacketClaim: false,
    arbitraryFieldClaim: false,
    unconditionalVersionMClaim: false,
    recapUpdated: false,
    retainedRecap: "R0.75W",
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
