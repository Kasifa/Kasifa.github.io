import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const readBytes = (path) => readFileSync(resolve(root, path));
const read = (path) => readBytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(readBytes(path)).digest("hex");
const node = process.env.CODEX_NODE || process.execPath;

test("R0.75E Step 30 publishes the exact proved/diagnostic/open boundary", () => {
  const note = read("public/notes/r0-75e.html");
  for (const marker of [
    "DIFFERENCE-FREQUENCY IDENTITY PROVED",
    "DIAGONAL FLUX ZERO",
    "REAL ZERO MODE ALL-PAYMENT PAID",
    "COMPLEX SINGLETON DIAGNOSTIC ONLY",
    "REAL ±N PAIR MAY COUPLE",
    "GENERAL CROSS-MODE GATE OPEN",
    "\\partial_2F=0",
    "\\mathcal T_\\xi(F,b)",
    "\\mathfrak X_{\\xi,R}(F,b)",
    "\\boxed{\\mathcal T_\\xi/\\pi=-\\frac12\\ne0.}",
    "\\boxed{\\mathfrak X_{\\xi,R}(F,b)\\le C(P_R^M)^{2/3}.}",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 250_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75e.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("R0.75F/G/H 与其他后续工作未读取、未公开"));
  for (const later of ["r0-75f", "r0-75g", "r0-75h"]) {
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".html")), false, later);
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".pdf")), false, later);
  }
});

test("R0.75E reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075e_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075e-step30-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75e.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75e.pdf"));
  assert.equal(binding.publicPdf.pageCount, 121);
  assert.equal(binding.frozenAuthority.sourceCommit, "aeaf5e588f2e606ee7deb960dd1f05fa4198e442");
  assert.equal(binding.frozenAuthority.handoffSha256, "c84b40e4833ebf9ce300ebd405c14605584aee84d0f890b48e17e9228f35d049");
  assert.equal(binding.frozenAuthority.independentHandoffAuditSha256, "5e16fceaa8f2127c817185cfc6c9e881c1068807f12cbea454d36aae2fb86795");
  assert.equal(binding.frozenAuthority.frozenFileCount, 10);
  assert.equal(binding.claimBoundary.diagonalFlux, "ZERO");
  assert.equal(binding.claimBoundary.realHorizontalZeroModeStatus, "PROVED");
  assert.equal(binding.claimBoundary.realHorizontalZeroModePaymentRegime, "ALL");
  assert.equal(binding.claimBoundary.realHorizontalZeroModeVerticalFrequency, "ARBITRARY");
  assert.equal(binding.claimBoundary.requiresSmallPayment, false);
  assert.equal(binding.claimBoundary.requiresD23Interaction, false);
  assert.equal(binding.claimBoundary.complexSingleton, "ALGEBRAIC DIAGNOSTIC ONLY");
  assert.equal(binding.claimBoundary.complexSingletonPhysicalRealNSEVelocity, false);
  assert.equal(binding.claimBoundary.realHarmonicPairMayCouple, true);
  assert.equal(binding.claimBoundary.arbitraryRealCrossModeGateStatus, "OPEN");
  assert.equal(binding.claimBoundary.completeClock, "OPEN");
  assert.equal(binding.claimBoundary.noveltyPriorityCorrectnessOrPublishabilityClaim, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.formalFigure.required, false);
  assert.equal(binding.formalFigure.status, "NOT APPLICABLE");
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75e.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75e.pdf")), false);
});

test("R0.75E routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075e"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075e-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75E Step 30", "HORIZONTAL CROSS-MODE FLUX", "NEXT · R0.75F", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75E Step 30 的 bounded primary-source screen", "difference-frequency", "complex singleton", "complete clock", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);

  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.09", html: 233, pdf: 190, published: 173, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75E" });

  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 135);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 7);
  assert.equal(inventory.latestPublishedRelease, "r075e");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075e").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075e"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075e").length, 1);

  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075e");
  assert.equal(manifest.latestCompletedStep, 30);
  assert.equal(manifest.nextRelease, "r075f");
  assert.equal(manifest.latestReleaseGate, "tests/r075e-step30-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075e-step30-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075e-step30-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "aeaf5e588f2e606ee7deb960dd1f05fa4198e442");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");

  const freeze = JSON.parse(read("research/r075e_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75E");
  assert.equal(freeze.frozen_file_count, 10);
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.horizontal_difference_frequency_identity, "PROVED");
  assert.equal(freeze.claim_status.diagonal_transport_flux, "ZERO_PROVED");
  assert.equal(freeze.claim_status.real_horizontal_zero_mode, "ALL_PAYMENT_PAID");
  assert.equal(freeze.claim_status.complex_singleton, "ALGEBRAIC_DIAGNOSTIC_ONLY_NOT_PHYSICAL");
  assert.equal(freeze.claim_status.real_nonzero_harmonic, "PAIR_MAY_COUPLE");
  assert.equal(freeze.claim_status.general_signed_cross_mode_gate, "OPEN");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_10_OF_10");

  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075e-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 82/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
