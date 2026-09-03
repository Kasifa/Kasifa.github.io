#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.74T Step 19 note.
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
  const htmlRelative = "public/notes/r0-74t.html";
  const pdfRelative = "public/notes/r0-74t.pdf";
  const provenanceRelative = "research/r074t_note_pdf_render.json";
  const bindingRelative = "research/r074t_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-74t.html?lang=zh`;

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
  const title = "R0.74T｜错峰外叶的 Hölder 强制付款与指数驻留屏障";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true ||
    provenance.loadedDocument?.sha256 !== sha256(html) ||
    provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r074t-step19-note-synchronized-pdf-binding-v1",
    release: "R0.74T",
    step: 19,
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
      handoffCommit: "cbe52bd5df2dfdb948b0ac8bb761ccd8774004f1",
      handoffSha256: "13ff4edeeebf1da9c9356246c3308e67109857bf36fbceb67fcba5188c1fa71f",
      sourceCommit: "2a3a59d4626face7b883159ee9b18500005e41d7",
      coreCommit: "b120598d36140385676bb4a9922d46abcdff0ba4",
      figureSourceCommit: "0433c129868ddf349c7b64d427747f590fa06898",
      mainTextSha256: "8d56a66ff918fe1c25056617468022379b71ab37bacff2650599194501ea4fbd",
      literatureAuditSha256: "60b49f6279c696a370af5f8050a6162753372eba81f8215e02e15259f084e88b",
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      proved: ["T.9-T.10", "T.17", "T.24-T.29", "T.34-T.43"],
      abstractOnly: ["measure-theoretic constant-rectangle sharpness tests"],
      open: [
        "full completed-clock payment-scale upper bound",
        "off-target clocks and accumulated dissipation",
        "K-to-Hfix bridge without Step 18 payment terms",
        "fixed deletion",
        "direct hybrid",
        "Q.12",
        "Q.1",
        "scale contraction",
        "regularity",
        "singularity",
      ],
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
