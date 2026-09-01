#!/usr/bin/env node

// Render and bind the queued R0.74B--R0.74F Chinese notes.  This certifies
// publication bytes and PDF structure; it does not certify mathematics.

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { createReadStream } from "node:fs";
import { createServer } from "node:http";
import { readFile, writeFile } from "node:fs/promises";
import { extname, resolve } from "node:path";
import { inspectPdf } from "./render-note-pdf.mjs";

const root = resolve(import.meta.dirname, "..");
const releases = [
  ["r074b", "r0-74b", "R0.74B｜缓冲环带闭合：Gaussian 外部尾项由倍半径付款"],
  ["r074c", "r0-74c", "R0.74C｜平流剪切阻断固定中心的大付款端点"],
  ["r074d", "r0-74d", "R0.74D｜零总均值仍不能修复固定中心运输缺口"],
  ["r074e", "r0-74e", "R0.74E｜局部随流坐标：旧反例被支付，外环新门槛通过"],
  ["r074f", "r0-74f", "R0.74F｜奇对称局部坐标中的双包存活：周期桥估计闭合"],
];

function sha256(bytes) {
  return createHash("sha256").update(bytes).digest("hex");
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

const address = server.address();
const results = [];
try {
  for (const [release, noteSlug, title] of releases) {
    const htmlRelative = `public/notes/${noteSlug}.html`;
    const pdfRelative = `public/notes/${noteSlug}.pdf`;
    const provenanceRelative = `research/${release}_note_pdf_render.json`;
    const url = `http://127.0.0.1:${address.port}/notes/${noteSlug}.html?lang=zh`;
    await run(process.execPath, [
      "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
    ], {
      env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" },
    });
    const [html, pdf, provenanceBytes, dictionary] = await Promise.all([
      readFile(resolve(root, htmlRelative)), readFile(resolve(root, pdfRelative)),
      readFile(resolve(root, provenanceRelative)),
      readFile(resolve(root, `research/${release}_bilingual_dictionary.md`)),
    ]);
    const structure = inspectPdf(pdf, pdfRelative);
    if (structure.title !== title) throw new Error(`${release}: PDF title drift`);
    const provenance = JSON.parse(provenanceBytes);
    if (provenance.loadedDocument?.equalsSourceHtml !== true ||
        provenance.loadedDocument?.sha256 !== sha256(html) ||
        provenance.source?.publicOrigin !== "https://kasifa.github.io") {
      throw new Error(`${release}: render provenance mismatch`);
    }
    const binding = {
      schemaVersion: "r074b-f-synchronized-pdf-binding-v1",
      release: release.toUpperCase().replace("R074", "R0.74"),
      publicChineseNote: { path: htmlRelative, bytes: html.length, sha256: sha256(html) },
      publicPdf: {
        path: pdfRelative, bytes: pdf.length, sha256: sha256(pdf),
        pageCount: structure.pageCount, title: structure.title, structure,
      },
      bilingualDictionary: {
        path: `research/${release}_bilingual_dictionary.md`,
        bytes: dictionary.length, sha256: sha256(dictionary),
      },
      provenance: {
        path: provenanceRelative, bytes: provenanceBytes.length, sha256: sha256(provenanceBytes),
        sourceUrl: provenance.source.url, loadedMainDocumentEqualsSourceHtml: true,
      },
      claimBoundary: {
        completeChinesePublicNote: true,
        htmlAndPdfCryptographicallyBound: true,
        pdfBindingCertifiesMathematicalCorrectness: false,
        evidenceClassesSeparated: ["PROVED", "FINITE", "OPEN", "BOUNDED LITERATURE AUDIT", "NOT CLAY"],
        translationPath: "LOCAL_DIRECT_NO_DGX",
        dgxUsed: false,
        clayProblemSolved: false,
      },
    };
    await writeFile(resolve(root, `research/${release}_pdf_bindings.json`), JSON.stringify(binding, null, 2) + "\n");
    results.push({ release, pageCount: structure.pageCount, sha256: sha256(pdf) });
  }
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}

await run(process.env.RELEASE_PYTHON ?? "python3", ["scripts/generate_note_index.py"]);
console.log(JSON.stringify({ applied: true, documents: results.length, results }, null, 2));
