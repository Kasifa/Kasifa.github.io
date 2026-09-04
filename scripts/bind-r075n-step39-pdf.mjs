#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.75N Step 39 note.
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
  const htmlRelative = "public/notes/r0-75n.html";
  const pdfRelative = "public/notes/r0-75n.pdf";
  const provenanceRelative = "research/r075n_note_pdf_render.json";
  const bindingRelative = "research/r075n_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-75n.html?lang=zh`;

  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.75N｜径向 collar 平均后的 Wiener row 无 R^(-1) 损失";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r075n-step39-note-synchronized-pdf-binding-v1",
    release: "R0.75N",
    step: 39,
    kind: "canonical-radial-collar-averaged-wiener-row-note",
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
      sourceCommit: "90a0d654447ba40865797669e5e5ad21ad9baa54",
      handoffCommit: "43a9b617df0b2478dbdfa649335d6b4040e926b7",
      handoffSha256: "07995870a834c9999f952443b71b46c13e9931187c7a04850f8db17c4b82a9d4",
      independentHandoffAuditSha256: "f0690d04ad983a22669764dfd9066f2e584774854206362095a6c3d1149b4a8c",
      frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      canonicalRadialCutoff: "SELECTABLE_ALLOWED_REPRESENTATIVE_N1_N5",
      fourierSignAndZeroMode: "D_ELL_PLUS_I_ELL_XI_ELL_AND_D0_ZERO_N5",
      samplingLemma: "LOW_HIGH_TWO_IBP_R_NU_MINUS_ONE_N6_N9",
      coefficientwiseSupremumOrder: "SUM_ELL_SUP_X3_PROVED_N2_N13",
      x1AveragedRow: "O_L_WITHOUT_R_NEGATIVE_POWER_N2",
      fullyAveragedRow: "O_L_SQUARED_R_N3_N16",
      sphericalTangency: "INCLUDED_BY_4_PI_A_DELTA_CAP_N12",
      frequencyThreshold: "K_GE_R_MINUS_3_OVER_2_DIAGNOSTIC_N17",
      theoremScope: "ONE_SELECTABLE_CANONICAL_RADIAL_COLLAR_CENTRAL_TORUS_CHART",
      universalCutoffTheorem: "OPEN",
      dynamicalFluxTheorem: "OPEN",
      interPacketSummation: "OPEN",
      bufferedCollarLocalCubicPayment: "OPEN",
      verticalDiffusion: "OPEN",
      nonconstantShear: "OPEN",
      lowDifferenceFrequencySector: "OPEN",
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
      exemptionManifest: "research/r075n_freeze_manifest.json",
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
