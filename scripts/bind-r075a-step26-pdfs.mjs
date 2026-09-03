#!/usr/bin/env node

// Render and cryptographically bind the Chinese R0.75A note and cumulative P-A recap.

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { createReadStream } from "node:fs";
import { createServer } from "node:http";
import { readFile, writeFile } from "node:fs/promises";
import { extname, resolve } from "node:path";
import { inspectPdf } from "./render-note-pdf.mjs";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const figureId = "fig-r075a-local-persistence-payment";

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
    [".md", "text/markdown; charset=utf-8"], [".csv", "text/csv; charset=utf-8"],
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
  const address = server.address();
  const jobs = [
    {
      kind: "note",
      htmlRelative: "public/notes/r0-75a.html",
      pdfRelative: "public/notes/r0-75a.pdf",
      provenanceRelative: "research/r075a_note_pdf_render.json",
      bindingRelative: "research/r075a_pdf_bindings.json",
      publicPath: "/notes/r0-75a.html",
      title: "R0.75A｜局部持续/付款二分：moving-cutoff 关闭任意短 endpoint focusing",
      schemaVersion: "r075a-step26-note-synchronized-pdf-binding-v1",
    },
    {
      kind: "recap",
      htmlRelative: "public/recap-r0-61-r0-75a.html",
      pdfRelative: "public/recap-r0-61-r0-75a.pdf",
      provenanceRelative: "research/r075a_recap_pdf_render.json",
      bindingRelative: "research/r075a_recap_pdf_bindings.json",
      publicPath: "/recap-r0-61-r0-75a.html",
      title: "R0.61–R0.75A 累计里程碑回顾｜从 clock compression 到 local dichotomy",
      schemaVersion: "r075a-step26-cumulative-recap-synchronized-pdf-binding-v1",
    },
  ];

  const outputs = [];
  for (const job of jobs) {
    const url = `http://127.0.0.1:${address.port}${job.publicPath}?lang=zh`;
    await run(process.execPath, [
      "scripts/render-note-pdf.mjs", url, job.pdfRelative, "-", job.htmlRelative, job.provenanceRelative,
    ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

    const [html, pdf, provenanceBytes] = await Promise.all([
      readFile(resolve(root, job.htmlRelative)),
      readFile(resolve(root, job.pdfRelative)),
      readFile(resolve(root, job.provenanceRelative)),
    ]);
    const structure = inspectPdf(pdf, job.pdfRelative);
    if (structure.title !== job.title) throw new Error(`${job.kind} PDF title drift: ${structure.title}`);
    const provenance = JSON.parse(provenanceBytes);
    if (
      provenance.loadedDocument?.equalsSourceHtml !== true
      || provenance.loadedDocument?.sha256 !== sha256(html)
      || provenance.source?.publicOrigin !== "https://kasifa.github.io"
    ) throw new Error(`${job.kind} render provenance mismatch`);

    const figureFiles = await Promise.all(["pdf", "png", "svg"].map(async (extension) => {
      const path = `public/assets/r075a/${figureId}.${extension}`;
      const bytes = await readFile(resolve(root, path));
      return { path, bytes: bytes.length, sha256: sha256(bytes) };
    }));
    const binding = {
      schemaVersion: job.schemaVersion,
      release: "R0.75A",
      step: 26,
      kind: job.kind === "note" ? "local-persistence-payment-dichotomy-note" : "cumulative-r061-r075a-pa-recap",
      publicChineseHtml: { path: job.htmlRelative, bytes: html.length, sha256: sha256(html) },
      publicPdf: {
        path: job.pdfRelative,
        bytes: pdf.length,
        sha256: sha256(pdf),
        pageCount: structure.pageCount,
        title: structure.title,
        structure,
      },
      provenance: {
        path: job.provenanceRelative,
        bytes: provenanceBytes.length,
        sha256: sha256(provenanceBytes),
        sourceUrl: provenance.source.url,
        loadedMainDocumentEqualsSourceHtml: true,
      },
      frozenAuthority: {
        sourceRepository: "/Users/kasifa/Documents/Math/navier-stokes-r074m",
        handoffCommit: "8c3c7e617d486abb31ae7207f38a97282d06b047",
        handoffSha256: "489b2f4b67d88974c555ea22e543906b9cd5cd469f135562fdca6c2aad0ad581",
        sourceCommit: "d15b7d8f9a3b16b63b4f324c75c9e156e9d03ff8",
        figureArchiveCommit: "243969b9d75d71224070bbdb3da64ce0103c1441",
        recapDeltaCommit: "9f01a3a8df2f60633a16e41eb2a1cb606c750198",
        mainTextSha256: "f8117a7ff6380676d2ed05e749119579cc3f6972463834dcc6ad2a0b03026388",
        primaryAuditSha256: "c599a1dcee8a82ec1c91512d5b664b1394707fd6d69ac2ca7ba022ebf715d3f6",
        literatureAuditSha256: "169eff2e607338ae990fb9994db3f75e11830246a36ee5cce8a7376e64302cea",
        frozenResearchFileCount: 11,
        frozenRecapFileCount: 2,
        frozenFigureFileCount: 25,
        frozenFigureArchiveBytes: 2588462,
      },
      figure: {
        id: figureId,
        analyticSchematic: true,
        derivedAnalyticValues: true,
        pdeSimulation: false,
        dns: false,
        assets: figureFiles,
      },
      claimBoundary: {
        completeChinesePublication: true,
        htmlAndPdfCryptographicallyBound: true,
        pdfBindingCertifiesMathematicalCorrectness: false,
        exactSmoothFiniteCommonShearFamily: true,
        movingCutoffIdentityProved: true,
        persistenceRapidRiseExhaustive: true,
        criticalAndArbitrarilyShortSmoothFocusingCovered: true,
        wRemoteEndpointPaymentDichotomyProved: true,
        exactGapA34: "64279/238140000",
        completeClockControlled: false,
        fixedDeletionClosed: false,
        arbitrarySuitableWeakSolutionsCovered: false,
        wholeShellUpperProved: false,
        noveltyOrPriorityClaim: false,
        clayClaim: false,
      },
      cumulativeRecap: {
        required: true,
        updatedThrough: "R0.75A",
        nodeCount: 169,
        previousR074SRecapPreserved: true,
      },
    };
    await writeFile(resolve(root, job.bindingRelative), `${JSON.stringify(binding, null, 2)}\n`);
    outputs.push({
      kind: job.kind,
      pageCount: structure.pageCount,
      pdfBytes: pdf.length,
      pdfSha256: binding.publicPdf.sha256,
      sourceHtmlSha256: binding.publicChineseHtml.sha256,
    });
  }

  process.stdout.write(`${JSON.stringify({
    status: "bound",
    release: "R0.75A",
    step: 26,
    outputs,
    figureAssets: 3,
    recapUpdated: true,
    previousRecapPreserved: true,
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
