#!/usr/bin/env node

// Render and cryptographically bind the Chinese R0.76J note. The I recap stays byte-exact.

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
const protectedRecaps = {
  "public/recap-r0-61-r0-76i.html": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9",
  "public/recap-r0-61-r0-76i.pdf": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98",
  "public/recap-r0-61-r0-75w.html": "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc",
  "public/recap-r0-61-r0-75w.pdf": "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce",
};

function run(executable, arguments_, options = {}) {
  return new Promise((resolvePromise, reject) => {
    const child = spawn(executable, arguments_, { cwd: root, env: { ...process.env, ...options.env }, stdio: ["ignore", "pipe", "pipe"] });
    let stdout = "";
    let stderr = "";
    child.stdout.setEncoding("utf8"); child.stderr.setEncoding("utf8");
    child.stdout.on("data", (chunk) => { stdout += chunk; });
    child.stderr.on("data", (chunk) => { stderr += chunk; });
    child.on("error", reject);
    child.on("close", (status) => status === 0 ? resolvePromise({ stdout, stderr })
      : reject(new Error(`${executable} ${arguments_.join(" ")} failed (${status}): ${stderr || stdout}`)));
  });
}

function contentType(filePath) {
  return new Map([[".html", "text/html; charset=utf-8"], [".js", "text/javascript; charset=utf-8"],
    [".css", "text/css; charset=utf-8"], [".svg", "image/svg+xml"], [".png", "image/png"],
    [".pdf", "application/pdf"], [".json", "application/json"]]).get(extname(filePath).toLowerCase()) ?? "application/octet-stream";
}

async function verifyRecaps(stage) {
  for (const [relative, expected] of Object.entries(protectedRecaps)) {
    if (sha256(await readFile(resolve(root, relative))) !== expected) throw new Error(`protected recap drift ${stage}: ${relative}`);
  }
}

await verifyRecaps("before PDF binding");
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
await new Promise((ok, reject) => { server.once("error", reject); server.listen(0, "127.0.0.1", ok); });

try {
  const address = server.address();
  const htmlRelative = "public/notes/r0-76j.html";
  const pdfRelative = "public/notes/r0-76j.pdf";
  const provenanceRelative = "research/r076j_note_pdf_render.json";
  const bindingRelative = "research/r076j_pdf_bindings.json";
  const title = "R0.76J｜本地重构端点外推并解除 exact-shear 窗口的文献条件";
  const url = `http://127.0.0.1:${address.port}/notes/r0-76j.html?lang=zh`;
  await run(process.execPath, ["scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative],
    { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });
  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)), readFile(resolve(root, pdfRelative)), readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);
  const provenance = JSON.parse(provenanceBytes);
  if (provenance.loadedDocument?.equalsSourceHtml !== true || provenance.loadedDocument?.sha256 !== sha256(html)
      || provenance.source?.publicOrigin !== "https://kasifa.github.io") throw new Error("note render provenance mismatch");
  const binding = {
    schemaVersion: "r076j-step61-note-synchronized-pdf-binding-v1", release: "R0.76J", step: 61,
    kind: "local-edge-extrapolation-reconstruction-exact-shear-note",
    publicChineseHtml: { path: htmlRelative, bytes: html.length, sha256: sha256(html) },
    publicPdf: { path: pdfRelative, bytes: pdf.length, sha256: sha256(pdf), pageCount: structure.pageCount, title: structure.title, structure },
    provenance: { path: provenanceRelative, bytes: provenanceBytes.length, sha256: sha256(provenanceBytes), sourceUrl: provenance.source.url, loadedMainDocumentEqualsSourceHtml: true },
    frozenAuthority: {
      sourceRepository: "/Users/kasifa/Documents/Math/navier-stokes-r074m",
      sourceCommit: "25d44e986d5283107816f910f89b94bceb1d5726", handoffCommit: "8b3b67c9f9d1e796f6a1bbd8639ab25d80ed0470",
      coreParentCommit: "72a5322f3ccb5cb53ad7cf489176c04e25148691", handoffSha256: "fedab351568d286247b90eb4fc314c41892de2deabf283ea82c69209fb9478fc",
      handoffIndependentAuditSha256: "9108064a741c595c52701be57a4e592dd62b453f54b89abbcf2742e47d32f0bf", frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true, htmlAndPdfCryptographicallyBound: true, pdfBindingCertifiesMathematicalCorrectness: false,
      theoremStatus: "PROVED_LOCALLY_FROM_ESTABLISHED_LITERATURE", zhangProposition42Imported: false,
      zhangRole: "ARCHITECTURE_AND_SHARPER_CONSTANT_COMPARISON_ONLY", historicalIConditionalLiteraturePreserved: true,
      packetScope: "EXACT_REAL_ONE_BAND_CONSTANT_SHEARS_ONLY", edgeSquaredPrefactor: "250_OVER_19",
      tailRecovery: "20_OVER_19", alphaCoefficient: "25_OVER_2", cutoff: "2",
      spatialCost: "Q2_EXP_20_SQRT2_Q_SQRT_DELTA_A", completeCost: "Q7_EXP_20_SQRT2_Q_SQRT_DELTA_A",
      sufficientModeWindow: "Q_LITTLE_O_L_TO_5_OVER_2", exactNormalizedRate: "MINUS_TWO_OVER_11907",
      multipleDyadicBands: "OPEN_NOT_PROVED", nonconstantShear: "OPEN_NOT_PROVED", arbitraryNonlinearPackets: "OPEN_NOT_PROVED",
      e24: "OPEN_NOT_PROVED", completeVersionMExtraction: "OPEN_NOT_PROVED", fixedDeletion: "OPEN_NOT_PROVED",
      suitableWeakTransfer: "OPEN_NOT_PROVED", regularityOrSingularityClaim: false,
      noveltyPriorityCorrectnessOrPublishabilityClaim: false, formalScientificFigure: false, pdeData: false, dns: false, simulation: false, dgxUsed: false, clayClaim: false,
    },
    formalFigure: { required: false, status: "NOT APPLICABLE", exemptionManifest: "research/r076j_freeze_manifest.json" },
    cumulativeRecap: {
      required: false, updatedThrough: "R0.76I", terminalStep: 60, nodeCount: 203, preservedByteExact: true,
      htmlPath: "public/recap-r0-61-r0-76i.html", htmlSha256: protectedRecaps["public/recap-r0-61-r0-76i.html"],
      pdfPath: "public/recap-r0-61-r0-76i.pdf", pdfSha256: protectedRecaps["public/recap-r0-61-r0-76i.pdf"],
    },
  };
  await writeFile(resolve(root, bindingRelative), `${JSON.stringify(binding, null, 2)}\n`);
  await verifyRecaps("after PDF binding");
  process.stdout.write(`${JSON.stringify({ status: "bound", release: "R0.76J", step: 61,
    output: { pageCount: structure.pageCount, pdfBytes: pdf.length, pdfSha256: binding.publicPdf.sha256, sourceHtmlSha256: binding.publicChineseHtml.sha256 },
    formalScientificFigure: false, theoremStatus: binding.claimBoundary.theoremStatus, recapUpdated: false, iRecapPreserved: true }, null, 2)}\n`);
} finally {
  await new Promise((ok) => server.close(ok));
}
