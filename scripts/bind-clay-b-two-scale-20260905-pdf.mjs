#!/usr/bin/env node

// Render and cryptographically bind the independent Clay-B Chinese reader PDF.

import { createHash } from "node:crypto";
import { spawn } from "node:child_process";
import { createReadStream } from "node:fs";
import { createServer } from "node:http";
import { readFile, writeFile } from "node:fs/promises";
import { extname, resolve } from "node:path";
import { inspectPdf } from "./render-note-pdf.mjs";

const root = resolve(import.meta.dirname, "..");
const publicRoot = resolve(root, "public");
const slug = "clay-b-two-scale-20260905";
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const protectedArtifacts = {
  "public/recap-r0-61-r0-76i.html": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9",
  "public/recap-r0-61-r0-76i.pdf": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98",
  "public/notes/r0-76j.html": "501371270954bb64dae9db784c6981a945730f346d5db971550f3b9d85505de2",
  "public/notes/r0-76j.pdf": "d264c951c9e3e43ab02181ebc4827513a1f6abe0ff37b07bb89ca9d2c6351d87",
  "public/notes/r0-76k.html": "d4960ea6616b718a4a9edf217f53cbfc276df9fe0662b107f10bca8bf779042d",
  "public/notes/r0-76k.pdf": "b3dce39a5d020a3c2d74133bdfd5c0324e46aefe8b34471b0acb349f90ddc7e1",
  "public/notes/r0-76l.html": "78085c5f2772e4b719004a1e9698147f84d84db73485ddcba2cf155c812e48b2",
  "public/notes/r0-76l.pdf": "3facbf01db259bf6ce2c247f0979b41ea64fe11be88c6c9b7a15a2d0d81d7ad8",
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
    [".css", "text/css; charset=utf-8"], [".pdf", "application/pdf"],
    [".json", "application/json"],
  ]).get(extname(filePath).toLowerCase()) ?? "application/octet-stream";
}

async function verifyProtected(stage) {
  for (const [relative, expected] of Object.entries(protectedArtifacts)) {
    const actual = sha256(await readFile(resolve(root, relative)));
    if (actual !== expected) throw new Error(`protected artifact drift ${stage}: ${relative}`);
  }
}

await verifyProtected("before PDF binding");
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
await new Promise((ok, reject) => {
  server.once("error", reject);
  server.listen(0, "127.0.0.1", ok);
});

try {
  const address = server.address();
  const htmlRelative = `public/notes/${slug}.html`;
  const pdfRelative = `public/notes/${slug}.pdf`;
  const provenanceRelative = "research/clay_b_two_scale_note_pdf_render_20260905.json";
  const bindingRelative = "research/clay_b_two_scale_pdf_bindings_20260905.json";
  const title = "两尺度差能量：瞬时吸收的限制与完整支付";
  const url = `http://127.0.0.1:${address.port}/notes/${slug}.html?lang=zh`;
  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });
  const [html, pdf, provenanceBytes, ledgerBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
    readFile(resolve(root, "research/clay_b_two_scale_frozen_ledger_20260905.json")),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);
  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true ||
    provenance.loadedDocument?.sha256 !== sha256(html) ||
    provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");
  const binding = {
    schemaVersion: "clay-b-two-scale-synchronized-pdf-binding-v1",
    releaseId: "ClayB-TwoScale-20260905",
    kind: "independent-two-scale-difference-energy-note",
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
      sourceCommit: "59e628a44e71b5bc54317db16758d9e6efd91334",
      baseContractCommit: "bbe05cfc584b550d52b5f2c899dfc5e32491114d",
      handoffCommit: "a09229a714247c6f6e959661ba428e91c1cb3ab1",
      ledgerPath: "research/clay_b_two_scale_frozen_ledger_20260905.json",
      ledgerSha256: sha256(ledgerBytes),
      scientificFileCount: 7,
      dependencyFileCount: 2,
    },
    claimBoundary: {
      trueNavierStokesDifferenceIdentity: "PROVED_LOCALLY",
      solutionIndependentInstantaneousAbsorption: "RULED_OUT_WITHOUT_EXTRA_PAYMENT",
      fixedPositiveScaleWeakEndpoint: "PROVED_LOCALLY",
      completePaidEstimateE5: "PROVED_LOCALLY",
      inverseSquareScalePayment: "NOT_RULED_OUT",
      initialDataDependence: "NOT_RULED_OUT",
      completeTimeCancellation: "NOT_RULED_OUT",
      contractG: "OPEN",
      regularityOrSingularityClaim: false,
      noveltyOrPriorityClaim: false,
      clayClaim: false,
    },
    scientificFigure: {
      required: false,
      status: "NOT_APPLICABLE_ANALYTIC_RELEASE",
      generated: false,
    },
    simulation: { required: false, run: false, dns: false, dgxUsed: false },
    cumulativeRecap: {
      required: false,
      updated: false,
      terminalRelease: "R0.76I",
      preservedByteExact: true,
    },
    canonicalSeries: { advanced: false, endpointPreserved: "R0.76L" },
  };
  await writeFile(resolve(root, bindingRelative), `${JSON.stringify(binding, null, 2)}\n`);
  await verifyProtected("after PDF binding");
  process.stdout.write(`${JSON.stringify({
    status: "bound",
    releaseId: binding.releaseId,
    output: {
      pageCount: structure.pageCount,
      pdfBytes: pdf.length,
      pdfSha256: binding.publicPdf.sha256,
      sourceHtmlSha256: binding.publicChineseHtml.sha256,
    },
    formalScientificFigure: false,
    simulation: false,
    recapUpdated: false,
    canonicalR0Endpoint: "R0.76L",
  }, null, 2)}\n`);
} finally {
  await new Promise((ok) => server.close(ok));
}
