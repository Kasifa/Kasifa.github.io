#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.74U Step 20 note.
// The Step 17 milestone recap is intentionally preserved byte-for-byte.

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
  const htmlRelative = "public/notes/r0-74u.html";
  const pdfRelative = "public/notes/r0-74u.pdf";
  const provenanceRelative = "research/r074u_note_pdf_render.json";
  const bindingRelative = "research/r074u_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-74u.html?lang=zh`;

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
  const title = "R0.74U｜内禀运动认证驻留尺度，并关闭指数短驻留逃逸";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true ||
    provenance.loadedDocument?.sha256 !== sha256(html) ||
    provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r074u-step20-note-synchronized-pdf-binding-v1",
    release: "R0.74U",
    step: 20,
    kind: "note",
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
      handoffCommit: "f3031095b7dfa51837df511f5b015bacb34c473b",
      handoffSha256: "115620fe742b3321c7d1422743b202ab83886beb4016fd8da45c81142d66a22b",
      sourceCommit: "735030d9e51068518796a79571ada291c5414a06",
      coreCommit: "d74e7b297928147334136f4c3cb29c5226d66381",
      figureSourceCommit: "8b75193df63a962392f89fcf1dbc20a8411334ba",
      mainTextSha256: "e149243c81e6919c318ddcd4bc94c4830c74cfc586b776e29284f79a35336d99",
      literatureAuditSha256: "0cf6e19a42e524aaf79aca10d72c5380029dce37032215974d99976a0b2a327c",
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      proved: ["U.21-U.25", "U.33", "U.34-U.35 lower only", "U.36-U.41", "U.45"],
      inherited: ["full-slab packet survival and total-field dominance inputs"],
      open: [
        "full K-superlevel upper measure",
        "full completed-clock upper ledger including off-target rows and accumulation",
        "arbitrary-clock lobe extraction",
        "high-Rayleigh and anomalous-defect branches",
        "fixed deletion",
        "direct hybrid",
        "Q.12",
        "Q.1",
        "scale contraction",
        "regularity",
        "singularity",
      ],
      certifiedGeometricCorridorUpperTransfersToFullKSuperlevel: false,
      fullKSuperlevelLowerOnly: true,
      literatureNearCollision: "Inage 2026 terminology-level only",
      figure: "ANALYTIC_SCHEMATIC_DERIVED_ANALYTIC_VALUES",
      pdeData: false,
      dns: false,
      navierStokesCounterexample: false,
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
    recapPreserved: true,
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
