#!/usr/bin/env node

// Render and cryptographically bind the synchronized R0.73Z note PDF. This
// certifies publication bytes and PDF structure, not mathematical correctness.

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { createReadStream } from "node:fs";
import { createServer } from "node:http";
import { mkdir, readFile, rename, writeFile } from "node:fs/promises";
import { extname, resolve } from "node:path";
import { inspectPdf } from "./render-note-pdf.mjs";

const root = resolve(process.env.R073Z_RELEASE_ROOT ?? resolve(import.meta.dirname, ".."));
const mode = process.argv.length === 2 ? "--apply" : process.argv[2];
if (!["--apply", "--check-only"].includes(mode)) {
  throw new Error("usage: bind-r073z-pdfs.mjs [--apply|--check-only]");
}
const apply = mode === "--apply";
const htmlPath = resolve(root, "public/notes/r0-73z.html");
const pdfPath = resolve(root, "public/notes/r0-73z.pdf");
const provenancePath = resolve(root, "research/r073z_note_pdf_render.json");
const bindingPath = resolve(root, "research/r073z_pdf_bindings.json");
const rendererPath = resolve(root, "scripts/render-note-pdf.mjs");
const reportPath = resolve(root, "research/r073z_report-source.md");
const dictionaryPath = resolve(root, "research/r073z_bilingual_dictionary.md");
const indexGenerator = resolve(root, "scripts/generate_note_index.py");
const title = "R0.73Z｜正三次 heat covariance 的有限性障碍与能量兼容修复";
const recap = new Map([
  ["public/recap-r0-61-r0-73x.html", "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776"],
  ["public/recap-r0-61-r0-73x.pdf", "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa"],
]);

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
}

async function atomicJson(path, value) {
  const temporary = `${path}.tmp-${process.pid}`;
  await writeFile(temporary, JSON.stringify(value, null, 2) + "\n");
  await rename(temporary, path);
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
    child.on("close", (status) => {
      if (status === 0) resolvePromise({ stdout, stderr });
      else reject(new Error(`${executable} ${arguments_.join(" ")} failed (${status}): ${stderr || stdout}`));
    });
  });
}

function contentType(path) {
  return new Map([
    [".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"],
    [".css", "text/css; charset=utf-8"], [".svg", "image/svg+xml"],
    [".png", "image/png"], [".pdf", "application/pdf"], [".json", "application/json"],
  ]).get(extname(path).toLowerCase()) ?? "application/octet-stream";
}

async function renderPdf() {
  const publicRoot = resolve(root, "public");
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
    const address = server.address();
    const url = `http://127.0.0.1:${address.port}/notes/r0-73z.html?lang=zh`;
    await run(process.execPath, [
      "scripts/render-note-pdf.mjs", url, "public/notes/r0-73z.pdf", "-",
      "public/notes/r0-73z.html", "research/r073z_note_pdf_render.json",
    ], {
      env: {
        PDF_RENDER_ROOT: root,
        PDF_PUBLIC_ORIGIN: "https://kasifa.github.io",
      },
    });
  } finally {
    await new Promise((resolvePromise) => server.close(resolvePromise));
  }
}

async function validateAndBind(writeBinding) {
  for (const [path, expected] of recap) {
    if (sha256(await readFile(resolve(root, path))) !== expected) {
      throw new Error(`protected recap drift: ${path}`);
    }
  }
  const [html, pdf, provenanceBytes, renderer, report, dictionary] = await Promise.all([
    readFile(htmlPath), readFile(pdfPath), readFile(provenancePath), readFile(rendererPath),
    readFile(reportPath), readFile(dictionaryPath),
  ]);
  const structure = inspectPdf(pdf, "public/notes/r0-73z.pdf");
  if (structure.title !== title) {
    throw new Error(`PDF title drift: ${JSON.stringify(structure.title)}`);
  }
  const provenance = JSON.parse(provenanceBytes);
  const htmlRecord = { path: "public/notes/r0-73z.html", bytes: html.length, sha256: sha256(html) };
  const pdfRecord = {
    path: "public/notes/r0-73z.pdf", bytes: pdf.length, sha256: sha256(pdf),
    pageCount: structure.pageCount, title: structure.title,
  };
  const rendererRecord = {
    path: "scripts/render-note-pdf.mjs", bytes: renderer.length, sha256: sha256(renderer),
  };
  for (const [label, actual, expected] of [
    ["HTML", provenance.html, htmlRecord], ["PDF", provenance.pdf, pdfRecord],
    ["renderer", provenance.renderer, rendererRecord],
  ]) {
    if (JSON.stringify(actual) !== JSON.stringify(expected)) {
      throw new Error(`${label} provenance mismatch`);
    }
  }
  if (provenance.loadedDocument?.sha256 !== htmlRecord.sha256 ||
      provenance.loadedDocument?.equalsSourceHtml !== true ||
      provenance.source?.publicOrigin !== "https://kasifa.github.io" ||
      JSON.stringify(provenance.structure) !== JSON.stringify(structure)) {
    throw new Error("render provenance sidecar mismatch");
  }
  const binding = {
    schemaVersion: "r073z-synchronized-pdf-bindings-v1",
    release: "R0.73Z",
    canonicalTitleSource: {
      path: "research/r073z_report-source.md", sha256: sha256(report), publicChineseTitle: title,
    },
    canonicalBoundarySource: {
      path: "research/r073z_bilingual_dictionary.md", sha256: sha256(dictionary),
    },
    renderer: rendererRecord,
    documents: [{
      kind: "research-note", html: htmlRecord, pdf: { ...pdfRecord, structure },
      provenance: {
        path: "research/r073z_note_pdf_render.json", bytes: provenanceBytes.length,
        sha256: sha256(provenanceBytes), schemaVersion: provenance.schemaVersion,
        url: provenance.source.url, origin: provenance.source.origin,
        publicOrigin: provenance.source.publicOrigin,
      },
    }],
    recap: {
      mode: "PRESERVE", latestRecapRelease: "R0.73X",
      htmlSha256: recap.get("public/recap-r0-61-r0-73x.html"),
      pdfSha256: recap.get("public/recap-r0-61-r0-73x.pdf"), recapGenerated: false,
    },
    claimBoundary: {
      htmlAndPdfBytesCryptographicallyBound: true,
      loadedMainDocumentEqualsSourceHtml: true,
      pdfHeaderEofXrefPageCountAndTitleValidated: true,
      initialEndpointEnergyClassFiniteness: "FALSE_BY_EXACT_LERAY_HOPF_SHEAR",
      energyCompatibleKDUpperBound: "PROVED_ANALYTICALLY",
      pressureActiveCrossedFamily: "PROVED_ANALYTICALLY",
      covarianceFourierCertificate: "FINITE_CROSS_CHECK_ONLY",
      localKDUpperPayment: "OPEN",
      epsilonRegularity: "OPEN",
      arbitraryThreeDimensionalGlobalRegularity: "OPEN",
      ordinaryTranslationPath: "LOCAL_DIRECT_NO_DGX",
      dgxUsed: false,
      clayConclusion: "OPEN",
      pdfBindingCertifiesMathematicalCorrectness: false,
      clayProblemSolved: false,
    },
  };
  if (writeBinding) await atomicJson(bindingPath, binding);
  else {
    const current = JSON.parse(await readFile(bindingPath, "utf8"));
    if (JSON.stringify(current) !== JSON.stringify(binding)) {
      throw new Error("R0.73Z PDF binding manifest is stale");
    }
  }
  return { pageCount: structure.pageCount, pdfSha256: pdfRecord.sha256 };
}

await mkdir(resolve(root, "public/notes"), { recursive: true });
if (apply) {
  await renderPdf();
  // The PDF now exists, so rebuild the index to replace its historical
  // HTML-only label with a live PDF link.
  await run(process.env.RELEASE_PYTHON ?? "python3", [indexGenerator]);
  await validateAndBind(true);
}
const result = await validateAndBind(false);
console.log(JSON.stringify({
  applied: apply, checked: true, documents: 1,
  output: "research/r073z_pdf_bindings.json",
  translationPath: "LOCAL_DIRECT_NO_DGX", dgxUsed: false, ...result,
}));
