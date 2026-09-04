#!/usr/bin/env node

// Render and cryptographically bind the Chinese R0.75W note and cumulative recap.
// The prior R0.75A and R0.75V recaps remain byte-exact; this analytic release has no formal figure.

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
  const address = server.address();
  const jobs = [
    {
      kind: "note",
      htmlRelative: "public/notes/r0-75w.html",
      pdfRelative: "public/notes/r0-75w.pdf",
      provenanceRelative: "research/r075w_note_pdf_render.json",
      bindingRelative: "research/r075w_pdf_bindings.json",
      publicPath: "/notes/r0-75w.html",
      title: "R0.75W｜单个 dyadic 二谐波剪切的全载频 signed-flux 付款",
      schemaVersion: "r075w-step48-note-synchronized-pdf-binding-v1",
      bindingKind: "full-frequency-exact-dyadic-two-harmonic-signed-flux-note",
    },
    {
      kind: "recap",
      htmlRelative: "public/recap-r0-61-r0-75w.html",
      pdfRelative: "public/recap-r0-61-r0-75w.pdf",
      provenanceRelative: "research/r075w_recap_pdf_render.json",
      bindingRelative: "research/r075w_recap_pdf_bindings.json",
      publicPath: "/recap-r0-61-r0-75w.html",
      title: "R0.61–R0.75W 累计里程碑回顾｜从 clock compression 到 full-frequency exact-pair signed flux",
      schemaVersion: "r075w-step48-cumulative-recap-synchronized-pdf-binding-v1",
      bindingKind: "cumulative-r061-r075w-exact-pair-flux-recap",
    },
  ];

  const outputs = [];
  for (const job of jobs) {
    const url = `http://127.0.0.1:${address.port}${job.publicPath}?lang=zh`;
    await run(process.execPath, [
      "scripts/render-note-pdf.mjs", url, job.pdfRelative, "-", job.htmlRelative, job.provenanceRelative,
    ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

    const [html, pdf, provenanceBytes] = await Promise.all([
      readFile(resolve(root, job.htmlRelative)),
      readFile(resolve(root, job.pdfRelative)),
      readFile(resolve(root, job.provenanceRelative)),
    ]);
    const structure = inspectPdf(pdf, job.pdfRelative);
    if (structure.title !== job.title) throw new Error(`${job.kind} PDF title drift: ${structure.title}`);
    const provenance = JSON.parse(provenanceBytes);
    if (
      provenance.loadedDocument?.equalsSourceHtml !== true
      || provenance.loadedDocument?.sha256 !== sha256(html)
      || provenance.source?.publicOrigin !== "https://kasifa.github.io"
    ) throw new Error(`${job.kind} render provenance mismatch`);

    const binding = {
      schemaVersion: job.schemaVersion,
      release: "R0.75W",
      step: 48,
      kind: job.bindingKind,
      publicChineseHtml: { path: job.htmlRelative, bytes: html.length, sha256: sha256(html) },
      publicPdf: {
        path: job.pdfRelative,
        bytes: pdf.length,
        sha256: sha256(pdf),
        pageCount: structure.pageCount,
        title: structure.title,
        structure,
      },
      provenance: {
        path: job.provenanceRelative,
        bytes: provenanceBytes.length,
        sha256: sha256(provenanceBytes),
        sourceUrl: provenance.source.url,
        loadedMainDocumentEqualsSourceHtml: true,
      },
      frozenAuthority: {
        sourceRepository: "/Users/kasifa/Documents/Math/navier-stokes-r074m",
        sourceCommit: "e8e48a510db0c0ed86626c238e4c81c281bcc998",
        handoffCommit: null,
        coreParentCommit: "038abd31f55795198ed8bebd9ba96823337c1621",
        handoffSha256: "8fa54b5d2bea00d24d53ab8cfde2693df41c0c1f7d66428ba575a26e53366aee",
        handoffIndependentAuditSha256: "8e700fd1647fca55168ad341f50a34379f62bb977a473c738323b059a77c1e54",
        frozenFileCount: 12,
      },
      claimBoundary: {
        completeChinesePublication: true,
        htmlAndPdfCryptographicallyBound: true,
        pdfBindingCertifiesMathematicalCorrectness: false,
        harmonicScope: "EXACTLY_TWO_REAL_HARMONICS_ONE_DYADIC_PAIR",
        dyadicPairCondition: "ONE_LE_M_LT_K_LE_2M",
        highCarrierCondition: "PROVED_BY_FROZEN_R075V_INPUT_MA_R_GE_C0",
        lowCarrierCondition: "PROVED_W31_MA_R_LT_C0",
        carrierPartition: "EXHAUSTIVE_W7_AND_W31",
        spatialCollarCoercivity: "PROVED_T",
        differenceFrequencyComponent: "PROVED_U4",
        confluentSpatialObservation: "PROVED_W12_W14_WITH_REPEATED_ROOTS",
        frequencyGapFreeTerminalTrace: "PROVED_W15_W19_TURAN_NAZAROV",
        scaledRadialPrimitive: "PROVED_W20_W23",
        localEnergyIdentity: "PROVED_W24_W29_NO_DIVISION_BY_V_OR_GAP",
        combinedSelfAndSumFrequencyBlock: "PROVED_V3",
        completeTwoHarmonicSignedFluxPayment: "PROVED_W2_ALL_CARRIERS_EXACT_PAIR_ONLY",
        normalizedExactPairEstimate: "PROVED_W3_W4_R_POWERS_CANCEL",
        exactL2Rate: "MINUS_2_OVER_11907",
        exactSmoothUnforcedShearSolution: "PROVED_W32",
        versionMSameVelocityInclusion: "CONDITIONAL_W33_REALIZED_SUBCLASS_AND_LEDGER_ALIGNMENT",
        finiteChecksAsContinuumProof: false,
        lowCarrierPair: "PROVED_W31_EXACT_PAIR_ONLY",
        threeOrMoreHarmonics: "OPEN_NOT_PROVED",
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
        exemptionManifest: "research/r075w_freeze_manifest.json",
      },
      cumulativeRecap: {
        required: true,
        updatedThrough: "R0.75W",
        terminalStep: 48,
        nodeCount: 191,
        previousR075ARecapPreserved: true,
        previousHtmlSha256: "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0",
        previousPdfSha256: "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62",
        previousR075VRecapPreserved: true,
        previousR075VHtmlSha256: "297c95300a2e983cce2ab201142f24297a70cc5eb9552cc3f2daee009025bee5",
        previousR075VPdfSha256: "bc0de2db711729bf1e202cff1b2f2d5cd1568ba5cd4f28f1bfb68b6ebc85e7eb",
      },
    };
    await writeFile(resolve(root, job.bindingRelative), `${JSON.stringify(binding, null, 2)}\n`);
    outputs.push({
      kind: job.kind,
      pageCount: structure.pageCount,
      pdfBytes: pdf.length,
      pdfSha256: binding.publicPdf.sha256,
      sourceHtmlSha256: binding.publicChineseHtml.sha256,
    });
  }
  process.stdout.write(`${JSON.stringify({
    status: "bound",
    release: "R0.75W",
    step: 48,
    outputs,
    formalScientificFigure: false,
    recapUpdated: true,
    previousRecapPreserved: true,
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
