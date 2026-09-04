#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.75U Step 46 note.
// The R0.75A milestone recap remains byte-exact; this analytic release has no formal figure.

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { createReadStream } from "node:fs";
import { createServer } from "node:http";
import { readFile, writeFile } from "node:fs/promises";
import { extname, resolve } from "node:path";
import { inspectPdf } from "./render-note-pdf.mjs";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

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
  const htmlRelative = "public/notes/r0-75u.html";
  const pdfRelative = "public/notes/r0-75u.pdf";
  const provenanceRelative = "research/r075u_note_pdf_render.json";
  const bindingRelative = "research/r075u_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-75u.html?lang=zh`;

  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.75U｜单个二谐波 dyadic pair 的差频项完整时钟付款";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r075u-step46-note-synchronized-pdf-binding-v1",
    release: "R0.75U",
    step: 46,
    kind: "two-harmonic-difference-frequency-complete-clock-payment-note",
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
      sourceCommit: "4bc33028aa27e6f47fb3464022a500556f3e34e4",
      handoffCommit: "73bcc4cd928370a7355b88f953e96082c58ebf69",
      coreParentCommit: "a7d599bf9068f346e4d02c4bfce8324e2f4a823a",
      handoffSha256: "33ae9d6d7d5b10aa5878e2b9e24c2f2f8bf1c5b1b668874dcac35d8e5cacf653",
      handoffIndependentAuditSha256: "6991ed0b3d0d3ca4db923f9b816dd91a2adc196f61de88fb10461c5708889259",
      frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      harmonicScope: "EXACTLY_TWO_REAL_HARMONICS_ONE_DYADIC_PAIR",
      dyadicPairCondition: "ONE_LE_M_LT_K_LE_2M",
      highCarrierCondition: "MA_R_GE_C0_REQUIRED",
      differenceFrequencyComponentOnly: "PROVED_U4",
      radialQuotient: "PROVED_U10_ALL_INTEGER_N_GE_1",
      weightedMovingPhaseLemma: "PROVED_U13_ALL_LAMBDA_GE_0_ALL_SIGMA_AND_PHASE",
      slowFastAndWeakStrongHeatRegimes: "PROVED_U14_U20",
      exactScalingAndAmplitudeCancellation: "PROVED_U21_U24",
      normalizedDifferenceFrequencyEstimate: "PROVED_U6_U7_R_POWERS_CANCEL",
      exactL2Rate: "MINUS_2_OVER_11907",
      exactSmoothUnforcedShearSolution: "PROVED_U27",
      versionMSameVelocityInclusion: "CONDITIONAL_U28_SAME_AS_R075S",
      fixedGridFastPhaseQuadrature: "EXCLUDED_FROM_PROOF_EVIDENCE",
      weightedTemporalDifferenceFrequencyEstimate: "PROVED_U4_CLOSES_T31_DIFFERENCE_ROW_ONLY",
      combinedSelfAndSumFrequencyBlock: "OPEN_NOT_PROVED",
      completeTwoHarmonicTemporalPayment: "OPEN_NOT_PROVED",
      completeTwoHarmonicSignedFluxPayment: "OPEN_NOT_PROVED",
      lowCarrierPair: "OPEN_NOT_PROVED",
      threeOrMoreHarmonics: "OPEN_NOT_PROVED",
      arbitraryPacketsAndInterPacketAggregation: "OPEN_NOT_PROVED",
      projectionFromLargerVelocity: "OPEN_NOT_PROVED",
      nonconstantShear: "OPEN_NOT_PROVED",
      verticallyDependentShear: "OPEN_NOT_PROVED",
      e24: "OPEN_NOT_PROVED",
      completeVersionMExtraction: "OPEN_NOT_PROVED",
      fixedDeletion: "OPEN_NOT_PROVED",
      suitableWeakTransfer: "OPEN_NOT_PROVED",
      regularityOrSingularityClaim: false,
      literatureScreen: "bounded finite non-hit only",
      noveltyPriorityCorrectnessOrPublishabilityClaim: false,
      formalScientificFigure: false,
      formalFigureApplicability: "NOT APPLICABLE",
      pdeData: false,
      dns: false,
      simulation: false,
      dgxUsed: false,
      clayClaim: false,
    },
    formalFigure: {
      required: false,
      status: "NOT APPLICABLE",
      exemptionManifest: "research/r075u_freeze_manifest.json",
    },
    cumulativeRecap: {
      required: false,
      updated: false,
      preservedThrough: "R0.75A",
      nodeCount: 169,
      preservedHtmlSha256: "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0",
      preservedPdfSha256: "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62",
    },
  };
  await writeFile(resolve(root, bindingRelative), `${JSON.stringify(binding, null, 2)}\n`);
  process.stdout.write(`${JSON.stringify({
    status: "bound",
    release: binding.release,
    step: binding.step,
    pageCount: structure.pageCount,
    pdfSha256: binding.publicPdf.sha256,
    sourceHtmlSha256: binding.publicChineseHtml.sha256,
    formalScientificFigure: false,
    recapPreserved: true,
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
