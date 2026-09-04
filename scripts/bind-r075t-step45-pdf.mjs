#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.75T Step 45 note.
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
  const htmlRelative = "public/notes/r0-75t.html";
  const pdfRelative = "public/notes/r0-75t.pdf";
  const provenanceRelative = "research/r075t_note_pdf_render.json";
  const bindingRelative = "research/r075t_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-75t.html?lang=zh`;

  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.75T｜单个二谐波 dyadic pair 的空间 collar coercivity";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r075t-step45-note-synchronized-pdf-binding-v1",
    release: "R0.75T",
    step: 45,
    kind: "spatial-two-harmonic-dyadic-pair-collar-coercivity-note",
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
      sourceCommit: "985b09647f726c420593d4d7fd61b7e9d045a80d",
      handoffCommit: "a7d599bf9068f346e4d02c4bfce8324e2f4a823a",
      coreParentCommit: "1c7432ac79521f26aab3b32a0dd4a272484f2776",
      handoffSha256: "3432f8214ccd529fd50cf902d5a1cbddc5bd63b7bca8235ec779b27c2e423c0b",
      handoffIndependentAuditSha256: "1f461acd199a6a698035d600af0254e23a7b8de5036bb04f1c6aa471b3de19bc",
      frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      harmonicScope: "EXACTLY_TWO_REAL_HARMONICS_ONE_DYADIC_PAIR",
      dyadicPairCondition: "ONE_LE_M_LT_K_LE_2M",
      highCarrierCondition: "MA_R_GE_C0_REQUIRED",
      spatialTwoHarmonicCollarCoercivity: "PROVED_T3",
      exactPlateauFibre: "PROVED_T10",
      slowEnvelopeSampling: "PROVED_T13",
      unresolvedBeatDefect: "PROVED_T21_T24",
      resolvedBeatGap: "PROVED_T25_T27",
      sharpDegeneracy: "PROVED",
      diffusiveTimeSliceCorollary: "PROVED_T6_UNEQUAL_HEAT_RATES_RETAINED",
      fourFrequencyFluxIdentity: "PROVED_T30",
      weightedTemporalDifferenceFrequencyEstimate: "OPEN_T31_NOT_PROVED",
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
      exemptionManifest: "research/r075t_freeze_manifest.json",
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
