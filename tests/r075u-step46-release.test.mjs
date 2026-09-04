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

test("R0.75U reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075u_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075u-step46-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.75U");
  assert.equal(binding.step, 46);
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75u.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75u.pdf"));
  assert.ok(binding.publicPdf.pageCount >= 180);
  assert.equal(binding.frozenAuthority.sourceCommit, "4bc33028aa27e6f47fb3464022a500556f3e34e4");
  assert.equal(binding.frozenAuthority.handoffCommit, "73bcc4cd928370a7355b88f953e96082c58ebf69");
  assert.equal(binding.frozenAuthority.coreParentCommit, "a7d599bf9068f346e4d02c4bfce8324e2f4a823a");
  assert.equal(binding.frozenAuthority.handoffSha256, "33ae9d6d7d5b10aa5878e2b9e24c2f2f8bf1c5b1b668874dcac35d8e5cacf653");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "6991ed0b3d0d3ca4db923f9b816dd91a2adc196f61de88fb10461c5708889259");
  assert.equal(binding.claimBoundary.differenceFrequencyComponentOnly, "PROVED_U4");
  assert.equal(binding.claimBoundary.radialQuotient, "PROVED_U10_ALL_INTEGER_N_GE_1");
  assert.equal(binding.claimBoundary.weightedMovingPhaseLemma, "PROVED_U13_ALL_LAMBDA_GE_0_ALL_SIGMA_AND_PHASE");
  assert.equal(binding.claimBoundary.slowFastAndWeakStrongHeatRegimes, "PROVED_U14_U20");
  assert.equal(binding.claimBoundary.exactScalingAndAmplitudeCancellation, "PROVED_U21_U24");
  assert.equal(binding.claimBoundary.normalizedDifferenceFrequencyEstimate, "PROVED_U6_U7_R_POWERS_CANCEL");
  assert.equal(binding.claimBoundary.exactL2Rate, "MINUS_2_OVER_11907");
  assert.equal(binding.claimBoundary.exactSmoothUnforcedShearSolution, "PROVED_U27");
  assert.equal(binding.claimBoundary.versionMSameVelocityInclusion, "CONDITIONAL_U28_SAME_AS_R075S");
  assert.equal(binding.claimBoundary.weightedTemporalDifferenceFrequencyEstimate, "PROVED_U4_CLOSES_T31_DIFFERENCE_ROW_ONLY");
  assert.equal(binding.claimBoundary.combinedSelfAndSumFrequencyBlock, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.completeTwoHarmonicTemporalPayment, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.completeTwoHarmonicSignedFluxPayment, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75u.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75u.pdf")), false);
});

test("R0.75U routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075u"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075u-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75U Step 46", "DIFFERENCE-FREQUENCY COMPLETE-CLOCK PAYMENT", "NEXT · NOT AUTHORIZED", "169 个节点"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75U Step 46 的 bounded primary-source screen", "DIFFERENCE-FREQUENCY COMPLETE-CLOCK SCOPE", "U.13", "U.28", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.25", html: 249, pdf: 206, published: 189, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75U" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 151);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 23);
  assert.equal(inventory.latestPublishedRelease, "r075u");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075u").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075u"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075u").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075u");
  assert.equal(manifest.latestCompletedStep, 46);
  assert.equal(manifest.nextRelease, "r075v");
  assert.equal(manifest.latestReleaseGate, "tests/r075u-step46-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075u-step46-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075u-step46-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "4bc33028aa27e6f47fb3464022a500556f3e34e4");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "73bcc4cd928370a7355b88f953e96082c58ebf69");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");
  const freeze = JSON.parse(read("research/r075u_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75U");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.scope, "TWO_HARMONIC_DIFFERENCE_FREQUENCY_COMPLETE_CLOCK_PAYMENT");
  assert.equal(freeze.claim_status.difference_frequency_component_only, "PROVED_U4");
  assert.equal(freeze.claim_status.radial_quotient, "PROVED_U10_ALL_INTEGER_N_GE_1");
  assert.equal(freeze.claim_status.weighted_moving_phase_lemma, "PROVED_U13_ALL_LAMBDA_GE_0_ALL_SIGMA_AND_PHASE");
  assert.equal(freeze.claim_status.normalized_difference_frequency_estimate, "PROVED_U6_U7_R_POWERS_CANCEL");
  assert.equal(freeze.claim_status.exact_l2_rate, "MINUS_2_OVER_11907");
  assert.equal(freeze.claim_status.version_m_same_velocity_inclusion, "CONDITIONAL_U28_SAME_AS_R075S");
  assert.equal(freeze.claim_status.weighted_temporal_difference_frequency_estimate, "PROVED_U4_CLOSES_T31_DIFFERENCE_ROW_ONLY");
  assert.equal(freeze.claim_status.combined_self_and_sum_frequency_block, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.complete_two_harmonic_signed_flux_payment, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075u-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 45/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75U keeps exclusions explicit and publishes no future or figure output", () => {
  const note = read("public/notes/r0-75u.html");
  for (const marker of ["DIFFERENCE ROW PAID", "EXACTLY TWO HARMONICS", "ONE DYADIC PAIR", "HIGH CARRIER", "COMPLETE CLOCK", "WEIGHTED PHASE LEMMA", "PHASE-DISTANCE MOMENT", "SLOW / FAST REGIMES", "AMPLITUDE CANCELS", "R POWERS CANCEL", "EXACT RATE -2/11907", "VERSION-M CONDITIONAL", "SELF / SUM BLOCK OPEN", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075u")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75u.html")), true);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75u.pdf")), true);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75v.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75v.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075u")), false);
});
