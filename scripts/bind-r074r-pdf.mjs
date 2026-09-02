#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.74R reader PDF.

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
    const child = spawn(executable, arguments_, { cwd: root, env: { ...process.env, ...options.env }, stdio: ["ignore", "pipe", "pipe"] });
    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8");
    child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", reject);
    child.on("close", (status) => status === 0 ? resolvePromise({ stdout, stderr }) : reject(new Error(`${executable} ${arguments_.join(" ")} failed (${status}): ${stderr || stdout}`)));
  });
}

function contentType(path) {
  return new Map([[".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"], [".css", "text/css; charset=utf-8"], [".svg", "image/svg+xml"], [".png", "image/png"], [".pdf", "application/pdf"], [".json", "application/json"]]).get(extname(path).toLowerCase()) ?? "application/octet-stream";
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

await new Promise((resolvePromise, reject) => { server.once("error", reject); server.listen(0, "127.0.0.1", resolvePromise); });
const address = server.address();

try {
  const htmlRelative = "public/notes/r0-74r.html";
  const pdfRelative = "public/notes/r0-74r.pdf";
  const provenanceRelative = "research/r074r_note_pdf_render.json";
  const bindingRelative = "research/r074r_pdf_bindings.json";
  const url = `http://127.0.0.1:${address.port}/notes/r0-74r.html?lang=zh`;
  await run(process.execPath, ["scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });
  const [html, pdf, provenanceBytes] = await Promise.all([readFile(resolve(root, htmlRelative)), readFile(resolve(root, pdfRelative)), readFile(resolve(root, provenanceRelative))]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.74R｜窗口质量为何收缩到第一壳层，任意时钟还缺什么？";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);
  const provenance = JSON.parse(provenanceBytes);
  if (provenance.loadedDocument?.equalsSourceHtml !== true || provenance.loadedDocument?.sha256 !== sha256(html) || provenance.source?.publicOrigin !== "https://kasifa.github.io") throw new Error("note render provenance mismatch");
  const binding = {
    schemaVersion: "r074r-note-synchronized-pdf-binding-v1",
    release: "R0.74R",
    kind: "note",
    publicChineseHtml: { path: htmlRelative, bytes: html.length, sha256: sha256(html) },
    publicPdf: { path: pdfRelative, bytes: pdf.length, sha256: sha256(pdf), pageCount: structure.pageCount, title: structure.title, structure },
    provenance: { path: provenanceRelative, bytes: provenanceBytes.length, sha256: sha256(provenanceBytes), sourceUrl: provenance.source.url, loadedMainDocumentEqualsSourceHtml: true },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      evidenceClassesSeparated: ["PROVED", "INHERITED", "FINITE", "CONDITIONAL", "LITERATURE BOUNDARY", "OPEN", "NO-GO", "NOT CLAY"],
      terminalWindowLobePacking: "PROVED",
      firstShellConcentration: "PROVED_IN_FROZEN_TARGET_FAMILY",
      arbitraryCompletedClockTrichotomy: "PROVED",
      persistenceToCubicPayment: "PROVED",
      arbitraryClockToFixedScaleImplication: "PROVED_CONDITIONAL_INPUT",
      universalExtractionInputs: "OPEN",
      noGoWitnesses: "PROVED_ABSTRACT_OR_FUNCTIONAL_NOT_NSE_SOLUTIONS",
      fixedScaleInequality: "OPEN",
      formalFigure: "PUBLISHED_DERIVED_FROM_FROZEN_ANALYTIC_SOURCE",
      navierStokesSimulation: false,
      directNumericalSimulation: false,
      translationPath: "LOCAL_DIRECT_NO_DGX",
      dgxUsed: false,
      regularityOrSingularityResolved: false,
      clayProblemSolved: false,
    },
  };
  await writeFile(resolve(root, bindingRelative), `${JSON.stringify(binding, null, 2)}\n`);
  process.stdout.write(`${JSON.stringify({ applied: true, release: "R0.74R", pageCount: structure.pageCount, sha256: sha256(pdf), bytes: pdf.length }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}

await run(process.env.RELEASE_PYTHON ?? "python3", ["scripts/generate_note_index.py"]);
