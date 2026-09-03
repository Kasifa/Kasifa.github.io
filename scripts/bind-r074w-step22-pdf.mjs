#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.74W Step 22 note.
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
const figureId = "fig-r074w-remote-adjacent-inward-threshold";

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
  const htmlRelative = "public/notes/r0-74w.html";
  const pdfRelative = "public/notes/r0-74w.pdf";
  const provenanceRelative = "research/r074w_note_pdf_render.json";
  const bindingRelative = "research/r074w_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-74w.html?lang=zh`;

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
  const title = "R0.74W｜远端相邻内壳 common-shear 阈值与加权端点阻断";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true ||
    provenance.loadedDocument?.sha256 !== sha256(html) ||
    provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const figureFiles = await Promise.all(["pdf", "png", "svg"].map(async (extension) => {
    const path = `public/assets/r074w/${figureId}.${extension}`;
    const bytes = await readFile(resolve(root, path));
    return { path, bytes: bytes.length, sha256: sha256(bytes) };
  }));

  const binding = {
    schemaVersion: "r074w-step22-note-synchronized-pdf-binding-v1",
    release: "R0.74W",
    step: 22,
    kind: "frozen-family-threshold-note",
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
      handoffCommit: "eb72349afeb5f7b02ee133b7c4d10466e2ae8ff4",
      handoffSha256: "01a9d5cb2d9a5d2c7a8f57c8e8fca964f2c59b330eebc2975b0e968840e1ec5b",
      sourceCommit: "f581c46ee7759c190b6f407633549e7106ff60b5",
      coreCommit: "f581c46ee7759c190b6f407633549e7106ff60b5",
      figureArchiveCommit: "0143d65322a3c854fe220aa9d3e4f93a1f6ca09e",
      mainTextSha256: "d818db13acc16ad26a2d9628f2681e4a654698c9966815dd6cf1712813830d10",
      primaryAuditSha256: "66ec78f67bba64c555a92e9a616c477d702ebb200b48bbfc08a353bdfde5bb73",
      literatureAuditSha256: "ec6259d95990fd6a8357d9685cc3f17e300e672c1add911a5eb64c6291f3bb99",
      frozenResearchFileCount: 10,
      frozenFigureFileCount: 25,
      frozenFigureArchiveBytes: 3774363,
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
      family: "one frozen exact smooth two-packet common-shear family",
      relativeProbabilityStatement: true,
      uniformSlabSurvivalBelowQ65: true,
      uniformSlabSweepingAboveQ64: true,
      fixedLimitingEllStrictSidesClassified: true,
      criticalEqualityOpen: true,
      packet1OriginalScale: "swept",
      packet2OriginalScale: "survives",
      frozenPlacementMatchingAllShellUpper: false,
      fixedDeletionResolved: false,
      open: [
        "critical equality law",
        "fixed deletion",
        "whole-shell H1 occupation",
        "time occupation",
        "positive-variation upper",
        "accumulated viscosity",
        "payment normalization",
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
