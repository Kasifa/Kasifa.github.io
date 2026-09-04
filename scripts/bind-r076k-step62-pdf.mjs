#!/usr/bin/env node

// Render and cryptographically bind the Chinese R0.76K note. The I recap stays byte-exact.

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
  const htmlRelative = "public/notes/r0-76k.html";
  const pdfRelative = "public/notes/r0-76k.pdf";
  const provenanceRelative = "research/r076k_note_pdf_render.json";
  const bindingRelative = "research/r076k_pdf_bindings.json";
  const title = "R0.76K｜实单频带 edge 下界、exact heat-shear 与 signed-cap 单切片";
  const url = `http://127.0.0.1:${address.port}/notes/r0-76k.html?lang=zh`;
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
    schemaVersion: "r076k-step62-note-synchronized-pdf-binding-v1", release: "R0.76K", step: 62,
    kind: "real-one-dyadic-band-edge-sharpness-exact-heat-shear-signed-cap-single-slice-note",
    publicChineseHtml: { path: htmlRelative, bytes: html.length, sha256: sha256(html) },
    publicPdf: { path: pdfRelative, bytes: pdf.length, sha256: sha256(pdf), pageCount: structure.pageCount, title: structure.title, structure },
    provenance: { path: provenanceRelative, bytes: provenanceBytes.length, sha256: sha256(provenanceBytes), sourceUrl: provenance.source.url, loadedMainDocumentEqualsSourceHtml: true },
    frozenAuthority: {
      sourceRepository: "/Users/kasifa/Documents/Math/navier-stokes-r074m",
      sourceCommit: "8a89aee4fe0839de44e21a90ba827a9cc77b3062", handoffCommit: "17bec49703836115f2e8a32a4bae516071433902",
      coreParentCommit: "8b3b67c9f9d1e796f6a1bbd8639ab25d80ed0470", handoffSha256: "e178c96e3041877d2c436ae33f12b2671d4366cad711eb9b3e1f18381aecc4d3",
      handoffIndependentAuditSha256: "e7afdedbd19c687afc8a32d4ab51d2765e92407ebb2d1a97112e081201253869", frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true, htmlAndPdfCryptographicallyBound: true, pdfBindingCertifiesMathematicalCorrectness: false,
      theoremStatus: "PROVED_LOCAL_REAL_DYADIC_EXACT_HEAT_SHEAR_SINGLE_SLICE",
      literature: "ZHANG_PROP_7_1_ARCHITECTURE_CHEN_PRICE_MOTIVATION_DLMF_STANDARD_FACTS",
      pointwiseLowerConstant: "ONE_OVER_2_SQRT2", exteriorLowerConstant: "D_OVER_128",
      endpointL2Lower: "Q_OVER_SQRT2", endpointL3Lower: "TWO_TO_MINUS_ONE_THIRD_Q_TO_TWO_THIRDS",
      modeCount: "Q_POSITIVE_COSINE_MODES_EQUALS_2Q_COMPLEX_BRANCHES_NOT_COMPLEX_TQ_INCLUSION",
      packetScope: "EXACT_REAL_ONE_DYADIC_BAND_FIXED_SINGLE_SLICE_ONLY",
      prescribedSliceQuantifier: "FOR_EVERY_PRESCRIBED_S_STAR_AND_B_THERE_EXISTS_A_PACKET",
      sufficientModeWindow: "Q_LITTLE_O_L_SQUARED",
      fullUpperWindowLowerBound: "Q_LITTLE_O_L_TO_5_OVER_2_OPEN",
      signedCapPairing: "PROVED_AT_SELECTED_SLICE_ONLY",
      semigroupBackwardWarning: "EXP_C_T_M2_OVER_A2",
      completeClockSignedFluxFullPlateauQuotient: "OPEN_NOT_PROVED",
      l3EndpointOptimality: "OPEN_NOT_PROVED", multipleDyadicBands: "OPEN_NOT_PROVED",
      nonconstantShear: "OPEN_NOT_PROVED", arbitraryNonlinearPackets: "OPEN_NOT_PROVED",
      e24: "OPEN_NOT_PROVED", versionMExtraction: "OPEN_NOT_PROVED", fixedDeletion: "OPEN_NOT_PROVED",
      suitableWeakTransfer: "OPEN_NOT_PROVED", regularityOrSingularityClaim: false,
      noveltyPriorityCorrectnessOrPublishabilityClaim: false, formalScientificFigure: false, pdeData: false,
      dns: false, simulation: false, dgxUsed: false, clayClaim: false,
    },
    formalFigure: { required: false, status: "NOT APPLICABLE", exemptionManifest: "research/r076k_freeze_manifest.json" },
    cumulativeRecap: {
      required: false, updatedThrough: "R0.76I", terminalStep: 60, nodeCount: 203, preservedByteExact: true,
      excludesLaterReleases: ["R0.76J", "R0.76K"],
      htmlPath: "public/recap-r0-61-r0-76i.html", htmlSha256: protectedRecaps["public/recap-r0-61-r0-76i.html"],
      pdfPath: "public/recap-r0-61-r0-76i.pdf", pdfSha256: protectedRecaps["public/recap-r0-61-r0-76i.pdf"],
    },
  };
  await writeFile(resolve(root, bindingRelative), `${JSON.stringify(binding, null, 2)}\n`);
  await verifyRecaps("after PDF binding");
  process.stdout.write(`${JSON.stringify({ status: "bound", release: "R0.76K", step: 62,
    output: { pageCount: structure.pageCount, pdfBytes: pdf.length, pdfSha256: binding.publicPdf.sha256, sourceHtmlSha256: binding.publicChineseHtml.sha256 },
    formalScientificFigure: false, theoremStatus: binding.claimBoundary.theoremStatus, recapUpdated: false, iRecapPreserved: true }, null, 2)}\n`);
} finally {
  await new Promise((ok) => server.close(ok));
}
