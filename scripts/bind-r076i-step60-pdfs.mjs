#!/usr/bin/env node

// Render and cryptographically bind the Chinese R0.76I note and cumulative recap.
// The prior R0.75W recap remains byte-exact; this analytic release has no formal figure.

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { createReadStream } from "node:fs";
import { createServer } from "node:http";
import { readFile, writeFile } from "node:fs/promises";
import { extname, resolve } from "node:path";
import { inspectPdf } from "./render-note-pdf.mjs";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const previousRecapExpected = {
  "public/recap-r0-61-r0-75w.html": "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc",
  "public/recap-r0-61-r0-75w.pdf": "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce",
};

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

function contentType(filePath) {
  return new Map([
    [".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"],
    [".css", "text/css; charset=utf-8"], [".svg", "image/svg+xml"],
    [".png", "image/png"], [".pdf", "application/pdf"], [".json", "application/json"],
  ]).get(extname(filePath).toLowerCase()) ?? "application/octet-stream";
}

for (const [relative, expected] of Object.entries(previousRecapExpected)) {
  if (sha256(await readFile(resolve(root, relative))) !== expected) throw new Error(`W recap drift before PDF binding: ${relative}`);
}

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
  const jobs = [
    {
      kind: "note",
      htmlRelative: "public/notes/r0-76i.html",
      pdfRelative: "public/notes/r0-76i.pdf",
      provenanceRelative: "research/r076i_note_pdf_render.json",
      bindingRelative: "research/r076i_pdf_bindings.json",
      publicPath: "/notes/r0-76i.html",
      title: "R0.76I｜切比雪夫尺度的完整平台增长模态窗口",
      schemaVersion: "r076i-step60-note-synchronized-pdf-binding-v1",
      bindingKind: "chebyshev-scale-full-plateau-exact-shear-window-note",
    },
    {
      kind: "recap",
      htmlRelative: "public/recap-r0-61-r0-76i.html",
      pdfRelative: "public/recap-r0-61-r0-76i.pdf",
      provenanceRelative: "research/r076i_recap_pdf_render.json",
      bindingRelative: "research/r076i_recap_pdf_bindings.json",
      publicPath: "/recap-r0-61-r0-76i.html",
      title: "R0.61–R0.76I 累计里程碑回顾｜从 exp(Cq) 障碍到条件性切比雪夫尺度窗口",
      schemaVersion: "r076i-step60-cumulative-recap-synchronized-pdf-binding-v1",
      bindingKind: "cumulative-r061-r076i-conditional-chebyshev-window-recap",
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

    const binding = {
      schemaVersion: job.schemaVersion,
      release: "R0.76I",
      step: 60,
      kind: job.bindingKind,
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
        sourceCommit: "0b73f68e072e573d9aaaa824e137e29a49d3cd67",
        handoffCommit: "72a5322f3ccb5cb53ad7cf489176c04e25148691",
        coreParentCommit: "8626f085f3220a79d19816ec220eacc8909971cc",
        handoffSha256: "b69e0f736de1253c277852aeb40f81733dbe32e34e2c2df19f8e2fd2581c9d29",
        handoffIndependentAuditSha256: "271a3adc20ce41ce9c63e31cfbc1a79a95a109b57cc6ed03036b13c265f9adaf",
        frozenFileCount: 12,
      },
      claimBoundary: {
        completeChinesePublication: true,
        htmlAndPdfCryptographicallyBound: true,
        pdfBindingCertifiesMathematicalCorrectness: false,
        compositeTheoremStatus: "CONDITIONAL_LITERATURE",
        importedInput: "ZHANG_2026_ARXIV_V1_PROPOSITION_4_2_UNREFEREED",
        independentProofOfImportedPreprint: false,
        packetScope: "EXACT_REAL_ONE_BAND_CONSTANT_SHEARS_ONLY",
        fullPlateauGap: "DELTA_A_EQUALS_O_ONE_OVER_A",
        spatialCost: "Q2_EXP_12_SQRT2_Q_SQRT_DELTA_A",
        completeCost: "Q7_EXP_12_SQRT2_Q_SQRT_DELTA_A",
        sufficientModeWindow: "Q_LITTLE_O_L_TO_5_OVER_2",
        exactNormalizedRate: "MINUS_TWO_OVER_11907",
        modeCountsComparableWithL2Included: true,
        fullSparseFourierSharpnessTransferredToExactShears: false,
        multipleDyadicBands: "OPEN_NOT_PROVED",
        nonconstantShear: "OPEN_NOT_PROVED",
        arbitraryNonlinearPackets: "OPEN_NOT_PROVED",
        e24: "OPEN_NOT_PROVED",
        completeVersionMExtraction: "OPEN_NOT_PROVED",
        fixedDeletion: "OPEN_NOT_PROVED",
        suitableWeakTransfer: "OPEN_NOT_PROVED",
        regularityOrSingularityClaim: false,
        finiteCertificateValidatesImportedPreprint: false,
        noveltyPriorityCorrectnessOrPublishabilityClaim: false,
        formalScientificFigure: false,
        pdeData: false,
        dns: false,
        simulation: false,
        dgxUsed: false,
        clayClaim: false,
      },
      formalFigure: {
        required: false,
        status: "NOT APPLICABLE",
        exemptionManifest: "research/r076i_freeze_manifest.json",
      },
      cumulativeRecap: {
        required: true,
        updatedThrough: "R0.76I",
        terminalStep: 60,
        nodeCount: 203,
        previousR075WRecapPreserved: true,
        previousHtmlPath: "public/recap-r0-61-r0-75w.html",
        previousHtmlSha256: previousRecapExpected["public/recap-r0-61-r0-75w.html"],
        previousPdfPath: "public/recap-r0-61-r0-75w.pdf",
        previousPdfSha256: previousRecapExpected["public/recap-r0-61-r0-75w.pdf"],
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
  for (const [relative, expected] of Object.entries(previousRecapExpected)) {
    if (sha256(await readFile(resolve(root, relative))) !== expected) throw new Error(`W recap drift after PDF binding: ${relative}`);
  }
  process.stdout.write(`${JSON.stringify({
    status: "bound",
    release: "R0.76I",
    step: 60,
    outputs,
    formalScientificFigure: false,
    theoremStatus: "CONDITIONAL_LITERATURE",
    recapUpdated: true,
    previousRecapPreserved: true,
  }, null, 2)}\n`);
} finally {
  await new Promise((resolvePromise) => server.close(resolvePromise));
}
