#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.75F Step 31 note.
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
  const htmlRelative = "public/notes/r0-75f.html";
  const pdfRelative = "public/notes/r0-75f.pdf";
  const provenanceRelative = "research/r075f_note_pdf_render.json";
  const bindingRelative = "research/r075f_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-75f.html?lang=zh`;

  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.75F｜模态相位积分恒等式：离对角账本精确回收，正性比较失效";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r075f-step31-note-synchronized-pdf-binding-v1",
    release: "R0.75F",
    step: 31,
    kind: "modal-phase-integration-diagonal-control-no-go-note",
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
      sourceCommit: "be9a79a1d2b1fd2b7ee0e33f1f6e18f23b63958c",
      handoffCommit: "97706831d95f82664c9693773c79e111a12fce35",
      handoffSha256: "1c150c22663850a3b21f47e1df3e1606796aa1a8edabad362d619fa81acf4afc",
      independentHandoffAuditSha256: "92c45d8fe449a846ec3f02d1d5bcbe2dfe9b9a27f3cb981c8cafb3761560751b",
      frozenFileCount: 12,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      modalProductEquation: "i ell b g_nm = partial_t g_nm - g_nm'' + 2 f_n' conjugate(f_m') + (n^2+m^2)g_nm",
      modalProductEquationStatus: "PROVED",
      offDiagonalPhaseIdentity: "T_xi = E_off - A_off + D_off",
      offDiagonalPhaseIdentityStatus: "PROVED_EXACT_ZERO_RESIDUAL",
      postSubstitutionIdentity: "E_diag + D_diag = A_diag",
      directPhaseSubstitutionResult: "TAUTOLOGICAL_NO_NEW_BOUND",
      independentSignSmallFactorOrObservability: false,
      fejerFamily: "D_N=sum_(k=-M)^M exp(ikx), a_N=D_N/sqrt(N), X_N=|D_N|^2/N^2",
      fejerRatio: "(2N+N^-1)/3 -> infinity",
      fejerFiniteRatios: { "3": "19/9", "5": "17/5", "7": "33/7" },
      positivityOnlyDiagonalComparison: "REFUTED",
      frozenCollarCounterexample: false,
      arbitraryRealE24: "OPEN",
      enhancedDissipationResolventPathwiseUncertaintyPaymentSensitiveRoutes: "VIABLE_UNPROVED",
      completeClock: "OPEN",
      fixedDeletion: "OPEN",
      suitableWeakTransfer: "OPEN",
      regularityOrSingularityClaim: false,
      literatureScreen: "bounded finite non-hit only",
      noveltyPriorityCorrectnessOrPublishabilityClaim: false,
      formalScientificFigure: false,
      formalFigureApplicability: "NOT APPLICABLE",
      pdeData: false,
      dns: false,
      simulation: false,
      dgxUsed: false,
      clayClaim: false,
    },
    formalFigure: {
      required: false,
      status: "NOT APPLICABLE",
      exemptionManifest: "research/r075f_freeze_manifest.json",
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
