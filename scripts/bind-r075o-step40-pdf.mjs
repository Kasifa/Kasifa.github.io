#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.75O Step 40 note.
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
  const htmlRelative = "public/notes/r0-75o.html";
  const pdfRelative = "public/notes/r0-75o.pdf";
  const provenanceRelative = "research/r075o_note_pdf_render.json";
  const bindingRelative = "research/r075o_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-75o.html?lang=zh`;

  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.75O｜常剪切下竖向扩散保留 packet flux 增益";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r075o-step40-note-synchronized-pdf-binding-v1",
    release: "R0.75O",
    step: 40,
    kind: "constant-shear-vertical-diffusion-packet-gain-note",
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
      sourceCommit: "9ad6873ca91c756309d009ffba142e4545f6c4c3",
      handoffCommit: "9bf705522928d390472e062f8d244d6b8b5220a0",
      coreParentCommit: "43a9b617df0b2478dbdfa649335d6b4040e926b7",
      handoffSha256: "f0f5e667dca7be397782a750d8dff80b3e9c4c6fe13294846cfdf1a4d60d7cb5",
      independentHandoffAuditSha256: "b68ad69da2d06796faf577a9bb9ea7297c9caf2c19c3e28dc4d72e4f664567a8",
      frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      constantShearModel: "PROVED_O4_TO_O12",
      arbitraryVerticalFrequencyEnergyRow: "PROVED_WITHOUT_UPPER_VERTICAL_CAP_O4_TO_O12",
      diagonalCancellation: "REMOVED_BEFORE_ABSOLUTE_VALUES_O9_TO_O12",
      verticalHeatSemigroup: "L2_CONTRACTION_O10",
      energyFluxConstant: "ABS_T_LE_ABS_B_W_INFINITY_E0_OVER_4K2_O12",
      totalFrequencyCappedRealPacket: "GAMMA_K_O13_TO_O17",
      shortTimeCubicLowerBound: "E_MINUS_3_OVER_2_E0_3_OVER_2_OVER_16PIK2_O17",
      packetFluxGain: "K_MINUS_2_OVER_3_O2_O20",
      strictKappaThreshold: "KAPPA_GT_98605_OVER_71442_O22",
      frozenKappa: "THREE_OVER_TWO_CLOSES_O23_O24",
      paymentScope: "PACKET_OWN_FULL_T2_ATOM_ONLY_NOT_VERSION_M",
      physicalCollarLocalization: "OPEN",
      interPacketSummation: "OPEN",
      nonconstantShear: "OPEN",
      lowHorizontalDifferenceSector: "OPEN",
      removalOfTotalUpperFrequencyCap: "OPEN",
      e24: "OPEN",
      completeClock: "OPEN",
      fixedDeletion: "OPEN",
      suitableWeakTransfer: "OPEN",
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
      exemptionManifest: "research/r075o_freeze_manifest.json",
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
