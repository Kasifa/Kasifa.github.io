#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.74Y Step 24 route screen.
// The R0.74S milestone recap remains byte-exact; this release has no formal figure.

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { createReadStream } from "node:fs";
import { createServer } from "node:http";
import { readFile, writeFile } from "node:fs/promises";
import { extname, resolve } from "node:path";
import { inspectPdf } from "./render-note-pdf.mjs";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");

function sha256(bytes) { return createHash("sha256").update(bytes).digest("hex"); }

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

function contentType(path) {
  return new Map([
    [".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"],
    [".css", "text/css; charset=utf-8"], [".svg", "image/svg+xml"],
    [".png", "image/png"], [".pdf", "application/pdf"], [".json", "application/json"],
  ]).get(extname(path).toLowerCase()) ?? "application/octet-stream";
}

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

await new Promise((resolvePromise, reject) => {
  server.once("error", reject);
  server.listen(0, "127.0.0.1", resolvePromise);
});

try {
  const htmlRelative = "public/notes/r0-74y.html";
  const pdfRelative = "public/notes/r0-74y.pdf";
  const provenanceRelative = "research/r074y_note_pdf_render.json";
  const bindingRelative = "research/r074y_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-74y.html?lang=zh`;

  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.74Y｜付款兼容的双坐标路线筛选：冻结几何 no-go 与形式取消窗口";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r074y-step24-note-synchronized-pdf-binding-v1",
    release: "R0.74Y",
    step: 24,
    kind: "payment-compatible-route-screen-note",
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
      handoffCommit: "87e32a45c78ee7131a919ebb51768714cd561b62",
      handoffSha256: "d333ba1223bce44b4d5dd5d23fa123a185402560945899e4416e7a4ab27d53b4",
      sourceCommit: "e75ccf1197484d0e551e8073f409e6a39b248564",
      coreCommit: "e75ccf1197484d0e551e8073f409e6a39b248564",
      mainTextSha256: "6144fe796d6c59a286fc32b3b0aa2b794c50006fdc7879d4595b5958c9646954",
      primaryAuditSha256: "c9b8ef6f78d0d196c2f17c6c7b83fe54667a6c80135553695dd7c68325af6f49",
      literatureAuditSha256: "e93275e31b1f04b1878071123fa3471a90e88fee5bb2b0dfd26afa6abf8d43a6",
      frozenFileCount: 10,
    },
    claimBoundary: {
      completeChinesePublication: true,
      routeScreen: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      target: "min{K_r,R(t_r),K_s,R(t_s)}/(P_R^M)^(2/3) -> infinity for r != s",
      deletionSetChosenBeforeTimeSupremum: true,
      witnessTimesMayDiffer: true,
      frozenGeometrySamePacketSelfPaymentNoGoProved: true,
      unequalAmplitudesAlone: "STRICT NO-GO IN FROZEN GEOMETRY",
      nonAdjacentDyadicPlacement: "STRICT NO-GO",
      deficitAgeAndHeatAgeDistinct: true,
      frozenXiMaximum: "-875993/968647680",
      changedGeometryRationalWindow: "FORMAL NECESSARY EXPONENTS ONLY",
      cancellationCellConstructed: false,
      propositionY57Proved: false,
      accumulatedViscosity: "DIMENSIONALLY DISFAVORED; OPEN / NOT CERTIFIED",
      completePaymentUpperProved: false,
      wholeShellEstimateInferredFromStrip: false,
      literatureScreen: "bounded primary-source non-hit only",
      noveltyPriorityCorrectnessOrPublishabilityClaim: false,
      formalScientificFigure: false,
      pdeData: false,
      dns: false,
      simulation: false,
      dgxUsed: false,
      generalNavierStokesCounterexample: false,
      clayClaim: false,
    },
    milestoneRecap: {
      updated: false,
      preservedHtmlSha256: "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81",
      preservedPdfSha256: "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec",
    },
  };
  await writeFile(resolve(root, bindingRelative), `${JSON.stringify(binding, null, 2)}\n`);
  process.stdout.write(`${JSON.stringify({
    status: "bound",
    release: binding.release,
    step: binding.step,
    routeScreen: true,
    pageCount: structure.pageCount,
    pdfSha256: binding.publicPdf.sha256,
    sourceHtmlSha256: binding.publicChineseHtml.sha256,
    formalScientificFigure: false,
    recapPreserved: true,
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
