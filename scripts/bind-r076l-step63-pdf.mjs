#!/usr/bin/env node

// Render and cryptographically bind the Chinese R0.76L note. The I recap stays byte-exact.

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
const protectedRecaps = {
  "public/recap-r0-61-r0-76i.html": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9",
  "public/recap-r0-61-r0-76i.pdf": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98",
  "public/recap-r0-61-r0-75w.html": "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc",
  "public/recap-r0-61-r0-75w.pdf": "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce",
  "public/notes/r0-76j.html": "501371270954bb64dae9db784c6981a945730f346d5db971550f3b9d85505de2",
  "public/notes/r0-76j.pdf": "d264c951c9e3e43ab02181ebc4827513a1f6abe0ff37b07bb89ca9d2c6351d87",
  "public/notes/r0-76k.html": "d4960ea6616b718a4a9edf217f53cbfc276df9fe0662b107f10bca8bf779042d",
  "public/notes/r0-76k.pdf": "b3dce39a5d020a3c2d74133bdfd5c0324e46aefe8b34471b0acb349f90ddc7e1",
};

function run(executable, arguments_, options = {}) {
  return new Promise((resolvePromise, reject) => {
    const child = spawn(executable, arguments_, { cwd: root, env: { ...process.env, ...options.env }, stdio: ["ignore", "pipe", "pipe"] });
    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8"); child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", reject);
    child.on("close", (status) => status === 0 ? resolvePromise({ stdout, stderr })
      : reject(new Error(`${executable} ${arguments_.join(" ")} failed (${status}): ${stderr || stdout}`)));
  });
}

function contentType(filePath) {
  return new Map([[".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"],
    [".css", "text/css; charset=utf-8"], [".svg", "image/svg+xml"], [".png", "image/png"],
    [".pdf", "application/pdf"], [".json", "application/json"]]).get(extname(filePath).toLowerCase()) ?? "application/octet-stream";
}

async function verifyRecaps(stage) {
  for (const [relative, expected] of Object.entries(protectedRecaps)) {
    if (sha256(await readFile(resolve(root, relative))) !== expected) throw new Error(`protected recap drift ${stage}: ${relative}`);
  }
}

await verifyRecaps("before PDF binding");
const server = createServer((request, response) => {
  const pathname = decodeURIComponent(new URL(request.url, "http://127.0.0.1").pathname);
  const relative = pathname === "/" ? "research-review.html" : pathname.replace(/^\/+/, "");
  const target = resolve(publicRoot, relative);
  if (!target.startsWith(`${publicRoot}/`)) { response.writeHead(403).end(); return; }
  response.setHeader("Content-Type", contentType(target));
  const stream = createReadStream(target);
  stream.on("error", () => response.writeHead(404).end());
  stream.pipe(response);
});
await new Promise((ok, reject) => { server.once("error", reject); server.listen(0, "127.0.0.1", ok); });

try {
  const address = server.address();
  const htmlRelative = "public/notes/r0-76l.html";
  const pdfRelative = "public/notes/r0-76l.pdf";
  const provenanceRelative = "research/r076l_note_pdf_render.json";
  const bindingRelative = "research/r076l_pdf_bindings.json";
  const title = "R0.76L｜抛物边缘平滑、完整时钟余项与 full-plateau 双边界";
  const url = `http://127.0.0.1:${address.port}/notes/r0-76l.html?lang=zh`;
  await run(process.execPath, ["scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative],
    { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });
  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)), readFile(resolve(root, pdfRelative)), readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);
  const provenance = JSON.parse(provenanceBytes);
  if (provenance.loadedDocument?.equalsSourceHtml !== true || provenance.loadedDocument?.sha256 !== sha256(html)
      || provenance.source?.publicOrigin !== "https://kasifa.github.io") throw new Error("note render provenance mismatch");
  const binding = {
    schemaVersion: "r076l-step63-note-synchronized-pdf-binding-v1", release: "R0.76L", step: 63,
    kind: "parabolic-edge-smoothing-complete-clock-sign-full-plateau-explicit-family-note",
    publicChineseHtml: { path: htmlRelative, bytes: html.length, sha256: sha256(html) },
    publicPdf: { path: pdfRelative, bytes: pdf.length, sha256: sha256(pdf), pageCount: structure.pageCount, title: structure.title, structure },
    provenance: { path: provenanceRelative, bytes: provenanceBytes.length, sha256: sha256(provenanceBytes), sourceUrl: provenance.source.url, loadedMainDocumentEqualsSourceHtml: true },
    frozenAuthority: {
      sourceRepository: "/Users/kasifa/Documents/Math/navier-stokes-r074m",
      initialSourceCommit: "6fe15fac7db9c3befbb3bab021787dfd6e76639e",
      sourceCommit: "b234b63c24c7b19efc703367e23b092385066a1c",
      certificateCommit: "2f3e0f466cc38fd2b61f2c79773352d95b2464e1",
      handoffCommit: "a5edefb014ebc6dd13ce052aad196ff5115b9629",
      predecessorHandoffCommit: "17bec49703836115f2e8a32a4bae516071433902",
      handoffSha256: "3a02aaf0544a5cf68250894ae608820c8027d2af3435497002bdf7675a55cdf4",
      handoffIndependentAuditSha256: "c6fb0cd85dd136088f4e4d6dfafa3de759024b49606a243626e303eb7e795b03", frozenFileCount: 24,
    },
    claimBoundary: {
      completeChinesePublication: true, htmlAndPdfCryptographicallyBound: true, pdfBindingCertifiesMathematicalCorrectness: false,
      theoremStatus: "PROVED_LOCAL_EXPLICIT_FAMILY_COMPLETE_CLOCK_POSITIVITY_AND_FULL_PLATEAU_TWO_SIDED_BOUND",
      literature: "CLASSICAL_POLYNOMIAL_HEAT_FLOW_GAUSSIAN_CONVOLUTION_CHEBYSHEV_GEGENBAUER_FACTS",
      packetScope: "EXPLICIT_START_PREPAID_REAL_INTEGER_ONE_DYADIC_BAND_FAMILY_ONLY",
      degreeWindow: "SQRT_A_LITTLE_O_M_AND_M_LITTLE_O_A_SQUARED",
      scale: "MU_EQUALS_M_SQUARED_OVER_A_TO_ONE_THIRD",
      fixedSliceEdgeScale: "MU_TO_THREE_HALVES",
      completeClockEdgeScale: "EXP_THETA_MU_WITH_POLYNOMIAL_PREFACTORS",
      completeClockSignedFlux: "EVENTUALLY_POSITIVE_FOR_THIS_FAMILY",
      fullPlateauQuotient: "TWO_SIDED_BOUND_PROVED_FOR_THIS_FAMILY",
      normalizedQuadraticLogRate: "MINUS_2_OVER_11907",
      candidateStatus: "RULED_OUT_FOR_THIS_EXPLICIT_FAMILY_IN_STATED_WINDOW",
      formalHighDegreePrediction: "M_COMPARABLE_KAPPA_A_TO_FOUR_OPEN_NOT_A_THEOREM",
      mComparableASquaredTransition: "OPEN_NOT_PROVED", arbitraryPackets: "OPEN_NOT_PROVED",
      versionMExtraction: "OPEN_NOT_PROVED", fixedDeletion: "OPEN_NOT_PROVED",
      suitableWeakTransfer: "OPEN_NOT_PROVED", regularityOrSingularityClaim: false,
      noveltyPriorityCorrectnessOrPublishabilityClaim: false, formalScientificFigure: true, pdeData: false,
      dns: false, simulation: false, dgxUsed: false, clayClaim: false,
    },
    formalFigure: {
      required: true, status: "PUBLISHED_FROM_FROZEN_PACKAGE", figureId: "fig-r076l-parabolic-edge",
      archivePath: "public/figures/r076l/fig-r076l-parabolic-edge", files: 12, bytes: 599429,
      svgSha256: "5e9061d5b76b03c60d58cac98320513dc442b7a595604ee9c59697b2e4190662",
      pdfSha256: "6de47c8df62ae35fc85e5b1ca2010038dd505d2e15b39caaa1f765b30cf4e7ea",
      pngSha256: "a5bff2596a6bf9ab0becc41cba0a985744c3b31878c6b11281ca2f4cf891fc75",
      finiteP075Tilt: "MOVES_SLIGHTLY_AWAY_FROM_LIMIT_ON_DISPLAYED_GRID_PREASYMPTOTIC",
    },
    cumulativeRecap: {
      required: false, updatedThrough: "R0.76I", terminalStep: 60, nodeCount: 203, preservedByteExact: true,
      excludesLaterReleases: ["R0.76J", "R0.76K", "R0.76L"],
      htmlPath: "public/recap-r0-61-r0-76i.html", htmlSha256: protectedRecaps["public/recap-r0-61-r0-76i.html"],
      pdfPath: "public/recap-r0-61-r0-76i.pdf", pdfSha256: protectedRecaps["public/recap-r0-61-r0-76i.pdf"],
    },
  };
  await writeFile(resolve(root, bindingRelative), `${JSON.stringify(binding, null, 2)}\n`);
  await verifyRecaps("after PDF binding");
  process.stdout.write(`${JSON.stringify({ status: "bound", release: "R0.76L", step: 63,
    output: { pageCount: structure.pageCount, pdfBytes: pdf.length, pdfSha256: binding.publicPdf.sha256, sourceHtmlSha256: binding.publicChineseHtml.sha256 },
    formalScientificFigure: true, theoremStatus: binding.claimBoundary.theoremStatus, recapUpdated: false, iRecapPreserved: true }, null, 2)}\n`);
} finally {
  await new Promise((ok) => server.close(ok));
}
