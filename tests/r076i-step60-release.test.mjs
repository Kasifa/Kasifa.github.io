import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("R0.76I note and cumulative recap PDFs are cryptographically bound", () => {
  for (const file of ["research/r076i_pdf_bindings.json", "research/r076i_recap_pdf_bindings.json"]) {
    const binding = JSON.parse(read(file));
    assert.equal(binding.release, "R0.76I");
    assert.equal(binding.step, 60);
    assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
    assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
    assert.equal(binding.provenance.sha256, sha(binding.provenance.path));
    assert.equal(binding.frozenAuthority.sourceCommit, "0b73f68e072e573d9aaaa824e137e29a49d3cd67");
    assert.equal(binding.frozenAuthority.handoffCommit, "72a5322f3ccb5cb53ad7cf489176c04e25148691");
    assert.equal(binding.frozenAuthority.coreParentCommit, "8626f085f3220a79d19816ec220eacc8909971cc");
    assert.equal(binding.claimBoundary.compositeTheoremStatus, "CONDITIONAL_LITERATURE");
    assert.equal(binding.claimBoundary.independentProofOfImportedPreprint, false);
    assert.equal(binding.claimBoundary.packetScope, "EXACT_REAL_ONE_BAND_CONSTANT_SHEARS_ONLY");
    assert.equal(binding.claimBoundary.sufficientModeWindow, "Q_LITTLE_O_L_TO_5_OVER_2");
    assert.equal(binding.claimBoundary.exactNormalizedRate, "MINUS_TWO_OVER_11907");
    assert.equal(binding.claimBoundary.fullSparseFourierSharpnessTransferredToExactShears, false);
    assert.equal(binding.claimBoundary.regularityOrSingularityClaim, false);
    assert.equal(binding.claimBoundary.formalScientificFigure, false);
    assert.equal(binding.claimBoundary.clayClaim, false);
    assert.equal(binding.cumulativeRecap.required, true);
    assert.equal(binding.cumulativeRecap.updatedThrough, "R0.76I");
    assert.equal(binding.cumulativeRecap.nodeCount, 203);
    assert.equal(binding.cumulativeRecap.previousHtmlSha256, "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
    assert.equal(binding.cumulativeRecap.previousPdfSha256, "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
  }
  assert.equal(JSON.parse(read("research/r076i_pdf_bindings.json")).publicPdf.pageCount, 282);
  assert.equal(JSON.parse(read("research/r076i_recap_pdf_bindings.json")).publicPdf.pageCount, 3);
});

test("R0.76I routes, accounting, manifests, and claim hierarchy are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r076i"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r076i-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.76I Step 60", "CHEBYSHEV-SCALE FULL-PLATEAU WINDOW", "165 节已公开", "STOP · NO LATER RELEASE AUTHORIZED", "/recap-r0-61-r0-76i.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.76I Step 60 的 conditional-literature", "LITERATURE", "PROVED LOCALLY", "CONDITIONAL-LITERATURE", "FINITE COMPUTATION", "q=o(L^(5/2))", "NO FULL-CLASS SHARPNESS CLAIM", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  assert.equal(home.includes('id="r076j"'), false);
  assert.equal(home.includes('href="/notes/r0-76j.html"'), false);
  assert.equal(literature.includes('href="/notes/r0-76j.html"'), false);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({ version: version.version, html: version.publicHtmlNoteCount, pdf: version.publicPdfNoteCount, published: version.postR060PublishedNodeCount, recap: version.postR060RecapNodeCount, latestRecap: version.latestRecapRelease, latestRelease: version.latestRelease }, { version: "2.39", html: 263, pdf: 220, published: 203, recap: 203, latestRecap: "R0.76I", latestRelease: "R0.76I" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 165);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 37);
  assert.equal(inventory.latestPublishedRelease, "r076i");
  assert.equal(inventory.sameReleaseCompletedSteps.r076i, 60);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r076i");
  assert.equal(manifest.latestCompletedStep, 60);
  assert.equal(manifest.nextRelease, "r076j");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r076i-step60-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-76i.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-76i.pdf");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, true);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r076i_freeze_manifest.json"));
  assert.equal(freeze.scope, "CHEBYSHEV_SCALE_FULL_PLATEAU_WINDOW_FOR_EXACT_ONE_BAND_CONSTANT_SHEARS");
  assert.equal(freeze.claim_status.composite_theorem, "CONDITIONAL_LITERATURE");
  assert.equal(freeze.claim_status.mode_window, "Q_LITTLE_O_L_TO_5_OVER_2");
  assert.equal(freeze.claim_status.normalized_rate, "EXACT_MINUS_TWO_OVER_11907");
  assert.equal(freeze.claim_status.full_class_sharpness, "NOT_CLAIMED_OPEN_IN_EXACT_SHEAR_CLASS");
  assert.equal(freeze.publication_handoff.recap_update_required, true);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
});

test("R0.76I publishes no figure, unconditional theorem, full-class sharpness, or later release", () => {
  const note = read("public/notes/r0-76i.html");
  const recap = read("public/recap-r0-61-r0-76i.html");
  for (const marker of ["CONDITIONAL-LITERATURE", "EXACT SHEAR ONLY", "NO FIGURE / NO DNS", "does not prove sharpness", "complete Version-M extraction", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.ok(recap.includes("NO FULL-CLASS SHARPNESS CLAIM"));
  assert.equal(existsSync(resolve(root, "public/assets/r076i")), false);
  assert.equal(note.includes("R0.76J"), false);
  assert.equal(recap.includes("R0.76J"), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
