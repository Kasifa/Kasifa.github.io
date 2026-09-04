#!/usr/bin/env node

// Render and cryptographically bind the Chinese R0.75Z note.
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
  const htmlRelative = "public/notes/r0-75z.html";
  const pdfRelative = "public/notes/r0-75z.pdf";
  const provenanceRelative = "research/r075z_note_pdf_render.json";
  const bindingRelative = "research/r075z_pdf_bindings.json";
  const url = `http://127.0.0.1:${address.port}/notes/r0-75z.html?lang=zh`;
  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.75Z｜未解簇正规形与载频电流门";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);
  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r075z-step51-note-synchronized-pdf-binding-v1",
    release: "R0.75Z",
    step: 51,
    kind: "unresolved-cluster-carrier-current-gate-note",
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
      sourceCommit: "85e633132cbcde89ec78bfef465f3c0393c27994",
      handoffCommit: null,
      coreParentCommit: "d1d9f261425804ecb53aa99ddb56705c87267c24",
      handoffSha256: "295af460aa6f15624a1d41adeeb6c0974acb3ee4f2c194f47777755d41c7b639",
      handoffIndependentAuditSha256: "8aa60590a884f4be7ac85167f693420a934bc3e57d3ce4a8a7571088ab53d6ab",
      frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      harmonicScope: "FIXED_Q_FINITE_REAL_FAMILY_ONE_DYADIC_BAND",
      xyzPartition: "EXHAUSTIVE_X_LOW_Y_STRONGLY_SEPARATED_Z_CLUSTERED_HIGH",
      xSector: "N1_ELL_LT_8Q",
      ySector: "N1_ELL_GE_8Q_AND_ALL_ADJACENT_GAPS_TIMES_ELL_GE_8Q",
      zSector: "N1_ELL_GE_8Q_AND_SOME_ADJACENT_GAP_TIMES_ELL_LT_8Q",
      equalityConvention: "GAP_TIMES_ELL_EQ_8Q_IS_Y_SEPARATOR",
      maximalClusters: "PROVED_UNIQUE_STRICT_INTERNAL_GAP_WIDTH",
      carrierEnvelopeEquation: "PROVED_COMPLEX_WITH_MINUS_2_I_N_DY_DRIFT",
      densityCarrierSplit: "PROVED_ONE_CLUSTER_SQUARE_ONLY",
      localCurrentIdentity: "PROVED_WITH_MINUS_4_N_J",
      fullPeriodCurrentSign: "NONNEGATIVE_GLOBAL_ONLY_NOT_POINTWISE",
      pointwiseAbsorption: "NO_CARRIER_UNIFORM_2N_ABS_J_BY_Q_PLUS_ABS_ZY_SQUARED",
      naiveRecursiveXStrategy: "CLOSED_ONLY_AFTER_POINTWISE_ABSOLUTE_CURRENT",
      fullClusteredSectorPayment: "OPEN_NOT_PROVED_OR_DISPROVED",
      clusterAdditivity: "OPEN_NOT_PROVED",
      fullFieldMassControlsEachCluster: "OPEN_NOT_PROVED",
      crossClusterProductsAndPayment: "OPEN_NOT_PROVED",
      counterexampleToFinalClusterFlux: false,
      versionMSameVelocityInclusion: "CONDITIONAL_MEASUREMENT_WEIGHT_REALIZED_SUBCLASS_ACTUAL_COMPONENT_LEDGER_ALIGNMENT",
      arbitraryPackets: "OPEN_NOT_PROVED",
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
      exemptionManifest: "research/r075z_freeze_manifest.json",
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
    release: "R0.75Z",
    step: 51,
    output: {
      pageCount: structure.pageCount,
      pdfBytes: pdf.length,
      pdfSha256: binding.publicPdf.sha256,
      sourceHtmlSha256: binding.publicChineseHtml.sha256,
    },
    formalScientificFigure: false,
    fullClusterPaymentClaim: false,
    counterexampleClaim: false,
    recapUpdated: false,
    retainedRecap: "R0.75W",
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
