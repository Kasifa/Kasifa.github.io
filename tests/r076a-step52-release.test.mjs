import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const node = process.execPath;
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("R0.76A note PDF is cryptographically bound while W recap is retained", () => {
  const binding = JSON.parse(read("research/r076a_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r076a-step52-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.76A");
  assert.equal(binding.step, 52);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.ok(binding.publicPdf.pageCount >= 228);
  assert.equal(binding.publicPdf.title, "R0.76A｜完整时钟局部载频电流负号障碍");
  assert.equal(binding.frozenAuthority.sourceCommit, "1f15e31b56c37a6a3941a1c4961321b7b1745e6c");
  assert.equal(binding.frozenAuthority.handoffCommit, null);
  assert.equal(binding.frozenAuthority.coreParentCommit, "69d65cd5cf897c90a9943d1b29090a11dc3c4f03");
  assert.equal(binding.frozenAuthority.handoffSha256, "ddf207b3785cab74bedebca695f48660a69b71412eb6427ebc4e9b174d00c46c");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "3ea9f69740496eb1d15a259cffe62d8961fd76296b1dd8b208796cb940643513");
  assert.equal(binding.claimBoundary.profileAssumption, "ZERO_LT_DELTA0_LT_DELTA");
  assert.equal(binding.claimBoundary.localizedCurrent, "STRICTLY_NEGATIVE_UNIFORMLY_ON_PRIMITIVE_SUPPORT");
  assert.equal(binding.claimBoundary.currentCorrectionRow, "STRICTLY_NEGATIVE_UNIFORMLY_ON_PRIMITIVE_SUPPORT");
  assert.equal(binding.claimBoundary.positiveCarrierDensityRow, "RETAINED_FULL_GRADIENT_NONNEGATIVE");
  assert.equal(binding.claimBoundary.localizedSignDropping, "CLOSED_ONE_SIDED_OFFSET_SPECTRUM_NOT_LOCAL_POSITIVITY");
  assert.equal(binding.claimBoundary.r075wTwoModeFluxPayment, "INTACT_NOT_COUNTEREXAMPLE");
  assert.equal(binding.claimBoundary.fullClusteredSectorPayment, "OPEN_NOT_PROVED_OR_DISPROVED");
  assert.equal(binding.claimBoundary.generalClusterCurrentEstimate, "OPEN_NOT_PROVED_OR_DISPROVED");
  assert.equal(binding.claimBoundary.jointDensityCarrierBlockPayment, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.crossClusterAggregation, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.counterexampleToTwoModeOrGeneralClusterFlux, false);
  assert.equal(binding.claimBoundary.versionMSameVelocityInclusion, "CONDITIONAL_MEASUREMENT_WEIGHT_REALIZED_SUBCLASS_ACTUAL_COMPONENT_LEDGER_ALIGNMENT");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.required, false);
  assert.equal(binding.cumulativeRecap.updatedThrough, "R0.75W");
  assert.equal(binding.cumulativeRecap.nodeCount, 191);
  assert.equal(binding.cumulativeRecap.retainedHtmlSha256, "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(binding.cumulativeRecap.retainedPdfSha256, "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76A routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r076a"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r076a-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.76A Step 52", "COMPLETE-CLOCK LOCALIZED CURRENT SIGN OBSTRUCTION", "157 节已公开", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.76A Step 52 的 bounded primary-source screen", "COMPLETE-CLOCK STRICT NEGATIVITY · SIGN-DROPPING ONLY", "A.23--A.31", "W TWO-MODE PAYMENT INTACT", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.31", html: 255, pdf: 212, published: 195, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.76A" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 157);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 29);
  assert.equal(inventory.latestPublishedRelease, "r076a");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r076a").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r076a"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r076a").length, 1);
  assert.equal(inventory.sameReleaseCompletedSteps.r076a, 52);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r076a");
  assert.equal(manifest.latestCompletedStep, 52);
  assert.equal(manifest.nextRelease, "r076b");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r076a-step52-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "1f15e31b56c37a6a3941a1c4961321b7b1745e6c");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, null);
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r076a_freeze_manifest.json"));
  assert.equal(freeze.scope, "COMPLETE_CLOCK_LOCALIZED_CURRENT_SIGN_OBSTRUCTION");
  assert.equal(freeze.claim_status.profile_assumption, "PROVED_WITH_0_LT_DELTA0_LT_DELTA");
  assert.equal(freeze.claim_status.localized_sign_dropping, "CLOSED_ONLY_ONE_SIDED_OFFSET_SPECTRUM_DOES_NOT_GIVE_LOCAL_POSITIVITY");
  assert.equal(freeze.claim_status.full_clustered_sector_payment, "OPEN_NOT_PROVED_OR_DISPROVED");
  assert.equal(freeze.claim_status.r075w_two_mode_flux_payment, "INTACT_NOT_COUNTEREXAMPLE");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.publication_handoff.retained_recap_terminal_release, "R0.75W_STEP48");
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r076a-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 45/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.76A publishes no figure, general-payment claim, or recap rewrite", () => {
  const note = read("public/notes/r0-76a.html");
  for (const marker of ["ACTUAL COLLAR PRIMITIVE", "COMPLETE CLOCK", "LOCAL CURRENT STRICTLY NEGATIVE", "CORRECTION ROW STRICTLY NEGATIVE", "SIGN-DROPPING CLOSED", "W TWO-MODE PAYMENT INTACT", "VERSION-M CONDITIONAL", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r076a")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
