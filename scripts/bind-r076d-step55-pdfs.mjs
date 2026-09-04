#!/usr/bin/env node

// Render and cryptographically bind the Chinese R0.76D note.
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
  const htmlRelative = "public/notes/r0-76d.html";
  const pdfRelative = "public/notes/r0-76d.pdf";
  const provenanceRelative = "research/r076d_note_pdf_render.json";
  const bindingRelative = "research/r076d_pdf_bindings.json";
  const url = `http://127.0.0.1:${address.port}/notes/r0-76d.html?lang=zh`;
  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.76D｜精确剪切的定量增长模态熵窗口";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);
  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r076d-step55-note-synchronized-pdf-binding-v1",
    release: "R0.76D",
    step: 55,
    kind: "quantitative-growing-mode-entropy-window-exact-real-constant-shear-note",
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
      sourceCommit: "c0cfe20b1970d9abbc32c191a5fad71dfdad1465",
      handoffCommit: null,
      coreParentCommit: "675638c96b204b7d853407fc2b0ace64ba5e061d",
      handoffSha256: "8fb0b43aea6958a5fa40c36e118aa5dc7a9d275597f6ecb07ca9b719d97d9452",
      handoffIndependentAuditSha256: "1231b3bf4de7e097f9e3cec947fa16716a5f4e3772365bfcecd2a3b6905f279e",
      frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      harmonicScope: "EACH_FIXED_INTEGER_Q_EXACT_REAL_DYADIC_BAND",
      integerModes: "REQUIRED_POSITIVE_INTEGERS",
      realPhases: "REQUIRED_REAL_NUMBERS",
      sufficientlyLargeFrozenL: true,
      allCarriers: "INHERITED_EXACT_REAL_CONSTANT_SHEAR_FAMILY_WITH_QUANTIFIED_Q_LOSS",
      modalEntropyLoss: "EXP_CSTAR_Q_LOG_Q_PLUS_1_REQUIRED_NOT_SUPPRESSED",
      growingModeWindow: "Q_OF_L_LOG_Q_OF_L_PLUS_1_IS_O_OF_L_SQUARED",
      frozenCoefficientRate: "MINUS_TWO_OVER_11907_RETAINED_IN_WINDOW",
      qUniformGrowingEstimate: false,
      arbitraryPacketTheorem: false,
      spatialDerivative: "ALPHA_PLUS_Q_FACTOR_RETAINED",
      maximumSpatialFrequencyDependence: "EXPLICIT_ALPHA_DEPENDENCE_RETAINED_NO_GAP_DENOMINATOR",
      temporalFamily: "EVERY_TIME_FIBRE_EXPONENTIAL_POLYNOMIAL_REAL_PARTS_MINUS4_TO_MINUS1",
      factorialTail: "M_PLUS_ONE_FACTORIAL_OVER_FOUR",
      endpointComparison: "FIVE_OVER_FOUR_TO_THE_M_FACTOR_RETAINED",
      weightedLambdaPower: "MINUS_ONE_THIRD",
      terminalLambdaPower: "ZERO",
      completeRealSquare: "RETAINED_BEFORE_ABSOLUTE_VALUES",
      spectralSeparationUsed: false,
      externalInputs: "TURAN_NAZAROV_AND_ERDELYI",
      localDeductions: "PLACEMENT_FACTORIAL_TAIL_ENDPOINT_COMPARISON_LAMBDA_BRANCHES_ENERGY_PAYMENT_SCALE_CONVERSION",
      finiteCertificateIsContinuumProof: false,
      arbitraryGrowingPackets: "OPEN_NOT_PROVED_GROWING_WINDOW_NOT_ARBITRARY_PACKET_THEOREM",
      nonconstantOrVerticalShear: "OPEN_NOT_PROVED",
      projectionFromLargerVelocity: "OPEN_NOT_PROVED",
      versionMSameVelocityInclusion: "CONDITIONAL_SAME_COMPONENT_SAME_MEASUREMENT_ROW",
      e24: "OPEN_NOT_PROVED",
      versionMWhenBNonzero: "WHEN_B_NONZERO_BACKGROUND_NOT_SHOWN_IN_FROZEN_MEAN_ZERO_INVERSION_PAIRED_SUBCLASS",
      completeVersionMExtraction: "OPEN_NOT_PROVED",
      fixedDeletion: "OPEN_NOT_PROVED",
      suitableWeakTransfer: "OPEN_NOT_PROVED",
      regularityOrSingularityClaim: false,
      literatureScreen: "TURAN_NAZAROV_AND_ERDELYI_PRIMARY_SUPPORT_BOUNDED_NON_HIT_ONLY",
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
      exemptionManifest: "research/r076d_freeze_manifest.json",
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
    release: "R0.76D",
    step: 55,
    output: {
      pageCount: structure.pageCount,
      pdfBytes: pdf.length,
      pdfSha256: binding.publicPdf.sha256,
      sourceHtmlSha256: binding.publicChineseHtml.sha256,
    },
    formalScientificFigure: false,
    modalEntropyLoss: "EXP_CSTAR_Q_LOG_Q_PLUS_1",
    growingModeWindow: "Q_LOG_Q_PLUS_1_IS_O_L_SQUARED",
    arbitraryGrowingPacketClaim: false,
    arbitraryFieldClaim: false,
    unconditionalVersionMClaim: false,
    recapUpdated: false,
    retainedRecap: "R0.75W",
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
