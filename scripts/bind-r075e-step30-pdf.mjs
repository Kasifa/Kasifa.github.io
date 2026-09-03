#!/usr/bin/env node

// Render and cryptographically bind the complete Chinese R0.75E Step 30 note.
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
  const htmlRelative = "public/notes/r0-75e.html";
  const pdfRelative = "public/notes/r0-75e.pdf";
  const provenanceRelative = "research/r075e_note_pdf_render.json";
  const bindingRelative = "research/r075e_pdf_bindings.json";
  const address = server.address();
  const url = `http://127.0.0.1:${address.port}/notes/r0-75e.html?lang=zh`;

  await run(process.execPath, [
    "scripts/render-note-pdf.mjs", url, pdfRelative, "-", htmlRelative, provenanceRelative,
  ], { env: { PDF_RENDER_ROOT: root, PDF_PUBLIC_ORIGIN: "https://kasifa.github.io" } });

  const [html, pdf, provenanceBytes] = await Promise.all([
    readFile(resolve(root, htmlRelative)),
    readFile(resolve(root, pdfRelative)),
    readFile(resolve(root, provenanceRelative)),
  ]);
  const structure = inspectPdf(pdf, pdfRelative);
  const title = "R0.75E｜横向交叉模态通量：实零模全支付，任意实场聚合待解";
  if (structure.title !== title) throw new Error(`note PDF title drift: ${structure.title}`);

  const provenance = JSON.parse(provenanceBytes);
  if (
    provenance.loadedDocument?.equalsSourceHtml !== true
    || provenance.loadedDocument?.sha256 !== sha256(html)
    || provenance.source?.publicOrigin !== "https://kasifa.github.io"
  ) throw new Error("note render provenance mismatch");

  const binding = {
    schemaVersion: "r075e-step30-note-synchronized-pdf-binding-v1",
    release: "R0.75E",
    step: 30,
    kind: "horizontal-cross-mode-flux-reduction-note",
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
      sourceCommit: "aeaf5e588f2e606ee7deb960dd1f05fa4198e442",
      handoffSha256: "c84b40e4833ebf9ce300ebd405c14605584aee84d0f890b48e17e9228f35d049",
      independentHandoffAuditSha256: "5e16fceaa8f2127c817185cfc6c9e881c1068807f12cbea454d36aae2fb86795",
      frozenFileCount: 10,
    },
    claimBoundary: {
      completeChinesePublication: true,
      htmlAndPdfCryptographicallyBound: true,
      pdfBindingCertifiesMathematicalCorrectness: false,
      passiveEquation: "(partial_t+b(t,x3)partial_2-Delta_23)F=0",
      localizedFlux: "T_xi=pi Re sum_(n,m) i(m-n) integral eta_R b Xi_(m-n) f_n conjugate(f_m)",
      diagonalFlux: "ZERO",
      fluxStructure: "purely off-diagonal difference-frequency",
      spectralOrthogonalityClosure: "Xi_(m-n)=0 for distinct supported modes implies T_xi=0",
      realHorizontalZeroMode: "partial_2 F=0",
      realHorizontalZeroModeEstimate: "D_out,F <= C(P_R^M)^(2/3) for sufficiently large L",
      realHorizontalZeroModePaymentRegime: "ALL",
      realHorizontalZeroModeVerticalFrequency: "ARBITRARY",
      realHorizontalZeroModeStatus: "PROVED",
      requiresSmallPayment: false,
      requiresD23Interaction: false,
      complexSingleton: "ALGEBRAIC DIAGNOSTIC ONLY",
      complexSingletonPhysicalRealNSEVelocity: false,
      realHarmonicPairMayCouple: true,
      realHarmonicDifferenceFrequency: "2n",
      frozenWitness: "Xi=2+cos(2x)+sin(2x), F=2cos(x)+sin(x), T_xi/pi=-1/2",
      frozenWitnessScope: "algebraic normalization only; not a spacetime trajectory or geometric collar",
      arbitraryRealCrossModeGate: "X_(xi,R)(F,b) <= C(P_R^M)^(2/3)",
      arbitraryRealCrossModeGateStatus: "OPEN",
      cutoffFourierTailsOrLocalizedObservability: "OPEN",
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
      exemptionManifest: "research/r075e_freeze_manifest.json",
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
