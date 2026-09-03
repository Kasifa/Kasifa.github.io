#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.75C Step 28 note.
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
  const htmlRelative = "public/notes/r0-75c.html";
  const pdfRelative = "public/notes/r0-75c.pdf";
  const provenanceRelative = "research/r075c_note_pdf_render.json";
  const bindingRelative = "research/r075c_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-75c.html?lang=zh`;

  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.75C｜背景剪切的 packing 假阳性：B.44 普适性淘汰，passive dissipation 待解";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r075c-step28-note-synchronized-pdf-binding-v1",
    release: "R0.75C",
    step: 28,
    kind: "background-shear-packing-false-positive-note",
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
      sourceCommit: "08d2e6e2e8abfead79d8ee47ee63156b5984672a",
      handoffSha256: "6fd6741aed5d992da53dee6f3d1cb02b67bad1c912c9843dcc371cb299cc0910",
      independentHandoffAuditSha256: "30bf74a2041b4e5ddcc28feef8e8e747c6443a0593395639e5f31ae205be83cb",
      frozenFileCount: 9,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      exactSmoothSaturationShearFamilyOnly: true,
      shearOnlyField: "u^sh=(0,b,0)",
      effectiveShearCountAsymptotic: "R^-1",
      logarithmicRate: "9/40000",
      b44SufficientThreshold: "4279/79380000",
      thresholdExcess: "27163/158760000",
      b44UniversalNecessity: "DISPROVED",
      b44SufficientConditionValidity: "RETAINED",
      shearDissipation: "PAID",
      shearDissipationRatio: "omega^(1/3)L^(-1/3) -> 0",
      passiveAdditionPreservesShearPayment: true,
      directOuterDissipationB45: "NEITHER PROVED NOR DISPROVED",
      passiveDissipation: "OPEN",
      completeKControlled: false,
      fixedDeletionClosed: false,
      arbitrarySuitableWeakExtension: false,
      regularityOrSingularityClaim: false,
      literatureScreen: "bounded finite non-hit only",
      noveltyPriorityCorrectnessOrPublishabilityClaim: false,
      formalScientificFigure: false,
      formalFigureApplicability: "NOT APPLICABLE",
      pdeData: false,
      dns: false,
      simulation: false,
      dgxUsed: false,
      generalNavierStokesCounterexample: false,
      clayClaim: false,
    },
    formalFigure: {
      required: false,
      status: "NOT APPLICABLE",
      exemptionManifest: "research/r075c_freeze_manifest.json",
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
