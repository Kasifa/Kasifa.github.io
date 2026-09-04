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

test("R0.75T reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075t_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075t-step45-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.75T");
  assert.equal(binding.step, 45);
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75t.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75t.pdf"));
  assert.ok(binding.publicPdf.pageCount >= 180);
  assert.equal(binding.frozenAuthority.sourceCommit, "985b09647f726c420593d4d7fd61b7e9d045a80d");
  assert.equal(binding.frozenAuthority.handoffCommit, "a7d599bf9068f346e4d02c4bfce8324e2f4a823a");
  assert.equal(binding.frozenAuthority.coreParentCommit, "1c7432ac79521f26aab3b32a0dd4a272484f2776");
  assert.equal(binding.frozenAuthority.handoffSha256, "3432f8214ccd529fd50cf902d5a1cbddc5bd63b7bca8235ec779b27c2e423c0b");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "1f461acd199a6a698035d600af0254e23a7b8de5036bb04f1c6aa471b3de19bc");
  assert.equal(binding.claimBoundary.spatialTwoHarmonicCollarCoercivity, "PROVED_T3");
  assert.equal(binding.claimBoundary.exactPlateauFibre, "PROVED_T10");
  assert.equal(binding.claimBoundary.slowEnvelopeSampling, "PROVED_T13");
  assert.equal(binding.claimBoundary.unresolvedBeatDefect, "PROVED_T21_T24");
  assert.equal(binding.claimBoundary.resolvedBeatGap, "PROVED_T25_T27");
  assert.equal(binding.claimBoundary.diffusiveTimeSliceCorollary, "PROVED_T6_UNEQUAL_HEAT_RATES_RETAINED");
  assert.equal(binding.claimBoundary.fourFrequencyFluxIdentity, "PROVED_T30");
  assert.equal(binding.claimBoundary.weightedTemporalDifferenceFrequencyEstimate, "OPEN_T31_NOT_PROVED");
  assert.equal(binding.claimBoundary.completeTwoHarmonicTemporalPayment, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.completeTwoHarmonicSignedFluxPayment, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75t.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75t.pdf")), false);
});

test("R0.75T routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075t"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075t-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75T Step 45", "TWO-HARMONIC SPATIAL COLLAR COERCIVITY", "NEXT · NOT AUTHORIZED", "169 个节点"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75T Step 45 的 bounded primary-source screen", "SPATIAL TWO-HARMONIC SCOPE", "T.31", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.24", html: 248, pdf: 205, published: 188, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75T" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 150);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 22);
  assert.equal(inventory.latestPublishedRelease, "r075t");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075t").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075t"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075t").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075t");
  assert.equal(manifest.latestCompletedStep, 45);
  assert.equal(manifest.nextRelease, "r075u");
  assert.equal(manifest.latestReleaseGate, "tests/r075t-step45-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075t-step45-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075t-step45-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "985b09647f726c420593d4d7fd61b7e9d045a80d");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "a7d599bf9068f346e4d02c4bfce8324e2f4a823a");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");
  const freeze = JSON.parse(read("research/r075t_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75T");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.two_harmonic_spatial_collar_coercivity, "PROVED_T3");
  assert.equal(freeze.claim_status.exact_plateau_fibre, "PROVED_T10");
  assert.equal(freeze.claim_status.diffusive_time_slice_corollary, "PROVED_T6_UNEQUAL_HEAT_RATES_RETAINED");
  assert.equal(freeze.claim_status.four_frequency_flux_identity, "PROVED_T30");
  assert.equal(freeze.claim_status.weighted_temporal_difference_frequency_estimate, "OPEN_T31_NOT_PROVED");
  assert.equal(freeze.claim_status.complete_two_harmonic_signed_flux_payment, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075t-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 46/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75T keeps exclusions explicit and publishes no future or figure output", () => {
  const note = read("public/notes/r0-75t.html");
  for (const marker of ["SPATIAL THEOREM", "EXACTLY TWO HARMONICS", "ONE DYADIC PAIR", "HIGH CARRIER", "EXACT PLATEAU FIBRE", "SLOW-ENVELOPE COERCIVITY", "BEAT DEFECT", "SHARP DEGENERACY", "UNEQUAL HEAT RATES", "FOUR-FREQUENCY FLUX", "TEMPORAL PAYMENT OPEN", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075t")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75u.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75u.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075u")), false);
});
