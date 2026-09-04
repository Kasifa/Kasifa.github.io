#!/usr/bin/env node

// Render and cryptographically bind the Chinese R0.76G note.
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
  const htmlRelative = "public/notes/r0-76g.html";
  const pdfRelative = "public/notes/r0-76g.pdf";
  const provenanceRelative = "research/r076g_note_pdf_render.json";
  const bindingRelative = "research/r076g_pdf_bindings.json";
  const url = `http://127.0.0.1:${address.port}/notes/r0-76g.html?lang=zh`;
  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.76G｜完整时钟中心纤维通量的指数下界";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);
  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r076g-step58-note-synchronized-pdf-binding-v1",
    release: "R0.76G",
    step: 58,
    kind: "complete-clock-central-fibre-signed-flux-lower-bound-exact-real-dyadic-shear-note",
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
      sourceCommit: "17b366e477c46d11b4caa5e2026381bbf08e7d62",
      handoffCommit: "6f203611dc13b7343005bcab3a429b6c68b10add",
      coreParentCommit: "52ee189e3dfaa2ea0924ed44cd2e1196b2ec3a5b",
      handoffSha256: "2f1811e02b4fc6685dd543ae9844382f3bac077df58d9bae9395f49864a2c1ea",
      handoffIndependentAuditSha256: "7b1230ec13b4ea894e19eef372a8816a947eda2af73262328aa7d62362f54a22",
      frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      harmonicScope: "Q_EQUALS_TWO_M_PLUS_ONE_EXACT_REAL_POSITIVE_FREQUENCY_DYADIC_BAND",
      integerModes: "TWO_M_THROUGH_FOUR_M",
      dyadicEndpoint: "FOUR_M_EQUALS_TWO_TIMES_TWO_M",
      mRule: "FLOOR_A_SQUARED_OVER_1024",
      beta: "ONE_OVER_100",
      scaledClock: "ZERO_TO_FOUR_TERMINAL_THREE_TO_FOUR",
      completeClock: true,
      signedFluxLowerBound: "C_STAR_BETA_TIMES_NINE_SEVENTHS_TO_FOUR_M",
      centralFibreProxy: true,
      modeDensity: "Q_OVER_L_SQUARED_TO_TWO_OVER_3969",
      normalizedRate: "LIMINF_GT_TWO_OVER_35721",
      optimalExponentialBaseClaim: false,
      arbitraryPacketTheorem: false,
      exactShearEmbedding: "SMOOTH_UNFORCED_CONSTANT_PRESSURE_WITH_NONZERO_DRIFT",
      completeTransportFlux: "EXPONENTIAL_LOWER_BOUND_AGAINST_CENTRAL_FIBRE_PROXY",
      completeCollarFluxLowerBound: true,
      fullPhysicalPlateauLowerBound: false,
      r076eE24OrVersionMCounterexample: false,
      externalInputs: "HEAT_OBSERVABILITY_AND_REMEZ_CONTEXT_ONLY_NO_THEOREM_IMPORTED",
      localDeductions: "EXPLICIT_PERIODIC_GAUSSIAN_EXPECTATION_AND_ELEMENTARY_MOMENT_ESTIMATES",
      finiteCertificateIsContinuumProof: false,
      arbitraryGrowingPackets: "OPEN_NOT_PROVED",
      nonconstantOrVerticalShear: "OPEN_NOT_PROVED",
      e24: "OPEN_NOT_PROVED",
      completeVersionMExtraction: "OPEN_NOT_PROVED",
      fixedDeletion: "OPEN_NOT_PROVED",
      suitableWeakTransfer: "OPEN_NOT_PROVED",
      regularityOrSingularityClaim: false,
      literatureScreen: "WANG_EGIDI_MILLER_LAURENT_NAZAROV_TIKHONOV_CONTEXT_NO_NOVELTY_CLAIM",
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
      exemptionManifest: "research/r076g_freeze_manifest.json",
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
    release: "R0.76G",
    step: 58,
    output: {
      pageCount: structure.pageCount,
      pdfBytes: pdf.length,
      pdfSha256: binding.publicPdf.sha256,
      sourceHtmlSha256: binding.publicChineseHtml.sha256,
    },
    formalScientificFigure: false,
    completeClockSignedFluxLowerBound: "C_STAR_BETA_TIMES_NINE_SEVENTHS_TO_FOUR_M",
    centralFibreProxyOnly: true,
    fullPlateauLowerBoundClaim: false,
    completeFluxLowerBoundClaim: true,
    arbitraryGrowingPacketClaim: false,
    arbitraryFieldClaim: false,
    unconditionalVersionMClaim: false,
    recapUpdated: false,
    retainedRecap: "R0.75W",
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
