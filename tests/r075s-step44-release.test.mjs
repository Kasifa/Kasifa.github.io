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

test("R0.75S reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075s_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075s-step44-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75s.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75s.pdf"));
  assert.equal(binding.publicPdf.pageCount, 186);
  assert.equal(binding.frozenAuthority.sourceCommit, "0afac1ea57d26466883d89b39b19965dcaaa1e58");
  assert.equal(binding.frozenAuthority.handoffCommit, "1c7432ac79521f26aab3b32a0dd4a272484f2776");
  assert.equal(binding.frozenAuthority.coreParentCommit, "9f99f88cdf8fb2d209401d8a6bc213df53bb2130");
  assert.equal(binding.frozenAuthority.handoffSha256, "dbbbc1474751fa6a7ddaa4ff6eed21756688809bfdd8b2d7a69303acd52377a0");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "e24548e99ed1ccb4c98aac541e86f2381c78af1b60216cdfc927c7d2ef32641b");
  assert.equal(binding.claimBoundary.completeFrozenClock, "PROVED_S1");
  assert.equal(binding.claimBoundary.radialCrossSectionIdentity, "PROVED_S11");
  assert.equal(binding.claimBoundary.exactScalarFluxReduction, "PROVED_S12_S13");
  assert.equal(binding.claimBoundary.radialSineCoefficientBounds, "PROVED_S15_S17");
  assert.equal(binding.claimBoundary.spatialNodeAndMovingPhaseLemmas, "PROVED_S18_S25");
  assert.equal(binding.claimBoundary.lowFrequencyPayment, "PROVED_S26_S30");
  assert.equal(binding.claimBoundary.highFrequencyPayment, "PROVED_S31_S38");
  assert.equal(binding.claimBoundary.allIntegerFrequencyPayment, "PROVED_S4_S6");
  assert.equal(binding.claimBoundary.normalizedLogarithmicL2Rate, "MINUS_2_OVER_11907");
  assert.equal(binding.claimBoundary.versionMRealizedSubclass, "CONDITIONAL_S39");
  assert.equal(binding.claimBoundary.multimodeInterferenceAndPacketAggregation, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.fourierProjectionOfLargerVelocity, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.nonconstantShear, "OPEN");
  assert.equal(binding.claimBoundary.e24, "OPEN");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75r.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75r.pdf")), false);
});

test("R0.75S routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075s"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075s-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75S Step 44", "FULL-FREQUENCY SINGLE-HARMONIC CLOCK PAYMENT", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75S Step 44 的 bounded primary-source screen", "ONE-HARMONIC SCOPE", "S.6--S.7", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.23", html: 247, pdf: 204, published: 187, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75S" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 149);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 21);
  assert.equal(inventory.latestPublishedRelease, "r075s");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075s").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075s"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075s").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075s");
  assert.equal(manifest.latestCompletedStep, 44);
  assert.equal(manifest.nextRelease, "r075t");
  assert.equal(manifest.latestReleaseGate, "tests/r075s-step44-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075s-step44-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075s-step44-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "0afac1ea57d26466883d89b39b19965dcaaa1e58");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "1c7432ac79521f26aab3b32a0dd4a272484f2776");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");
  const freeze = JSON.parse(read("research/r075s_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75S");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.complete_frozen_clock, "PROVED_S1");
  assert.equal(freeze.claim_status.radial_cross_section_identity, "PROVED_S11");
  assert.equal(freeze.claim_status.exact_scalar_flux_reduction, "PROVED_S12_S13");
  assert.equal(freeze.claim_status.low_frequency_payment, "PROVED_S26_S30");
  assert.equal(freeze.claim_status.high_frequency_payment, "PROVED_S31_S38");
  assert.equal(freeze.claim_status.all_integer_frequency_payment, "PROVED_S4_S6");
  assert.equal(freeze.claim_status.version_m_realized_subclass, "CONDITIONAL_S39");
  assert.equal(freeze.claim_status.multimode_interference_and_packet_aggregation, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.E24, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075s-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 46/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75S keeps exclusions explicit and does not publish future or figure output", () => {
  const note = read("public/notes/r0-75s.html");
  for (const marker of ["POSITIVE THEOREM", "COMPLETE CLOCK", "ALL INTEGER FREQUENCIES", "ONE REAL HARMONIC", "EXACT SMOOTH SHEAR", "RADIAL REDUCTION", "MOVING-PHASE LEMMA", "LOW/HIGH COVERAGE", "AMPLITUDE CANCELS", "VERSION-M CONDITIONAL", "MULTIMODE OPEN", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075s")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75t.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75t.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075t")), false);
});
