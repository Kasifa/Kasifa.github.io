#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.74X Step 23 note.
// The R0.74S milestone recap and frozen four-panel figure remain byte-exact.

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { createReadStream } from "node:fs";
import { createServer } from "node:http";
import { readFile, writeFile } from "node:fs/promises";
import { extname, resolve } from "node:path";
import { inspectPdf } from "./render-note-pdf.mjs";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const figureId = "fig-r074x-three-packet-payment-gate";

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
    [".html", "text/html; charset=utf-8"],
    [".js", "text/javascript; charset=utf-8"],
    [".css", "text/css; charset=utf-8"],
    [".svg", "image/svg+xml"],
    [".png", "image/png"],
    [".pdf", "application/pdf"],
    [".json", "application/json"],
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
  const htmlRelative = "public/notes/r0-74x.html";
  const pdfRelative = "public/notes/r0-74x.pdf";
  const provenanceRelative = "research/r074x_note_pdf_render.json";
  const bindingRelative = "research/r074x_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-74x.html?lang=zh`;

  await run(process.execPath, [
    "scripts/render-note-pdf.mjs",
    url,
    pdfRelative,
    "-",
    htmlRelative,
    provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.74X｜三 packet fixed-deletion endpoint obstruction 与 cubic-payment gate";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true ||
    provenance.loadedDocument?.sha256 !== sha256(html) ||
    provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const figureFiles = await Promise.all(["pdf", "png", "svg"].map(async (extension) => {
    const path = `public/assets/r074x/${figureId}.${extension}`;
    const bytes = await readFile(resolve(root, path));
    return { path, bytes: bytes.length, sha256: sha256(bytes) };
  }));

  const binding = {
    schemaVersion: "r074x-step23-note-synchronized-pdf-binding-v1",
    release: "R0.74X",
    step: 23,
    kind: "frozen-three-packet-fixed-deletion-payment-gate-note",
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
      handoffCommit: "9bddf4a591a159ac99f43602700a80f736dcc61b",
      handoffSha256: "c5bf4fc67476a489f3f473635d4b2106590457f0308208046d937989967a2122",
      sourceCommit: "802e5572b3490b326a03706c512f35ef6f5afa31",
      coreCommit: "802e5572b3490b326a03706c512f35ef6f5afa31",
      figureArchiveCommit: "a5670383091098331b557869a57c6ed9b6fa72e9",
      mainTextSha256: "4fdc9558605afd9557c557c4292ca1af50d52ff54f9aa11603f15c97a97b3ee3",
      primaryAuditSha256: "834ec846c3f8629f9e7462caf4503bfa99ba6b88288da2dd525793206de9357e",
      literatureAuditSha256: "f58f7a1d095ba6bd8b27c41872301fd367fe784597160fe060f9cd332c64c422",
      frozenResearchFileCount: 10,
      frozenFigureFileCount: 25,
      frozenFigureArchiveBytes: 3096940,
    },
    figure: {
      id: figureId,
      analyticSchematic: true,
      derivedAnalyticValues: true,
      pdeData: false,
      dns: false,
      sampledTrajectories: false,
      assets: figureFiles,
      visibleScopeLabel: "ANALYTIC SCHEMATIC | DERIVED ANALYTIC VALUES | NOT PDE DATA | NOT DNS | NOT CLAY",
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      family: "one frozen exact smooth three-packet periodic common-shear family",
      packet2RelativeSurvival: true,
      packet3RelativeSurvival: true,
      twoDistinctTStarNormalizedEndpointDivergences: true,
      fixedDeletionSetChosenBeforeTimeSupremum: true,
      witnessTimesMayDiffer: true,
      budgetOneEndpointFunctionalDivergesRelativeToTStar: true,
      actualGateNormalization: "(P_R^M)^(2/3)",
      actualPaymentNormalizedCounterexampleProved: false,
      equalTargetWStripRoute: "NO-GO BY CUBIC PAYMENT",
      auditedTwoStripComparisonOnly: true,
      open: [
        "payment-compatible two-coordinate construction X.52",
        "actual payment-normalized fixed-deletion counterexample",
        "whole-shell clock upper or lower bound",
        "positive-variation upper",
        "accumulated viscosity",
        "arbitrary-clock extraction",
        "scale contraction",
        "general suitable weak solutions",
        "regularity",
        "singularity",
      ],
      literatureScreen: "bounded primary-source non-hit only",
      noveltyPriorityCorrectnessOrPublishabilityClaim: false,
      pdeData: false,
      dns: false,
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
    pageCount: structure.pageCount,
    pdfSha256: binding.publicPdf.sha256,
    sourceHtmlSha256: binding.publicChineseHtml.sha256,
    figureAssets: figureFiles.length,
    recapPreserved: true,
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
