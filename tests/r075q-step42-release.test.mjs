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

test("R0.75Q reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075q_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075q-step42-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75q.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75q.pdf"));
  assert.equal(binding.publicPdf.pageCount, 173);
  assert.equal(binding.frozenAuthority.sourceCommit, "1b1d092e96aaca9afe723c40994accbe1aee5031");
  assert.equal(binding.frozenAuthority.handoffCommit, "780596a1b431a695cbed0978714f721b8577af81");
  assert.equal(binding.frozenAuthority.coreParentCommit, "1b1d092e96aaca9afe723c40994accbe1aee5031");
  assert.equal(binding.frozenAuthority.handoffSha256, "998fa28d8d0f6d3c2cb205a51309014c00f566d74190fe3335f1818bd365da7b");
  assert.equal(binding.claimBoundary.entranceConcentration, "NOT_ASSUMED_LOW_ENTRANCE_DIAGNOSTIC_Q27_Q28");
  assert.equal(binding.claimBoundary.signedFluxCancellation, "EXACT_CONSTANT_ROW_ZERO_Q11_TO_Q14");
  assert.equal(binding.claimBoundary.harmonicFluxGain, "K_MINUS_2_OVER_3_M_COL_2_OVER_3_Q4_Q22");
  assert.equal(binding.claimBoundary.paymentScope, "CONDITIONAL_SAME_VELOCITY_ACTUAL_COMPONENT_Q26");
  assert.equal(binding.claimBoundary.physicalCollarLocalization, "PROVED_FOR_ONE_SPATIALLY_SPREAD_HARMONIC");
  assert.equal(binding.claimBoundary.generalLowEntrancePackets, "OPEN_NOT_COUNTEREXAMPLE");
  assert.equal(binding.claimBoundary.multimodeInterference, "OPEN");
  assert.equal(binding.claimBoundary.arbitraryVerticalStructure, "OPEN");
  assert.equal(binding.claimBoundary.interPacketSummation, "OPEN");
  assert.equal(binding.claimBoundary.nonconstantShear, "OPEN");
  assert.equal(binding.claimBoundary.e24, "OPEN");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75q.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75q.pdf")), false);
});

test("R0.75Q routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075q"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075q-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75Q Step 42", "SPATIALLY SPREAD HARMONIC COLLAR PAYMENT", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75Q Step 42 的 bounded primary-source screen", "Q.8--Q.10", "Q.27--Q.28", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.21", html: 245, pdf: 202, published: 185, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75Q" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 147);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 19);
  assert.equal(inventory.latestPublishedRelease, "r075q");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075q").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075q"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075q").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075q");
  assert.equal(manifest.latestCompletedStep, 42);
  assert.equal(manifest.nextRelease, "r075r");
  assert.equal(manifest.latestReleaseGate, "tests/r075q-step42-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075q-step42-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075q-step42-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "1b1d092e96aaca9afe723c40994accbe1aee5031");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "780596a1b431a695cbed0978714f721b8577af81");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");
  const freeze = JSON.parse(read("research/r075q_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75Q");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.entrance_concentration, "NOT_ASSUMED_LOW_ENTRANCE_DIAGNOSTIC_Q27_Q28");
  assert.equal(freeze.claim_status.harmonic_flux_gain, "K_MINUS_2_OVER_3_M_COL_2_OVER_3_Q4_Q22");
  assert.equal(freeze.claim_status.payment_scope, "CONDITIONAL_SAME_VELOCITY_ACTUAL_COMPONENT_Q26");
  assert.equal(freeze.claim_status.multimode_interference, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.inter_packet_summation, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.E24, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075q-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 46/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75Q keeps exclusions explicit and does not publish future or figure output", () => {
  const note = read("public/notes/r0-75q.html");
  for (const marker of ["CONSTANT SHEAR", "ONE REAL HARMONIC", "SPATIALLY SPREAD", "EXACT ZERO ROW", "PHASE-UNIFORM PERIODS", "3D COLLAR CUBIC", "K^-2/3 GAIN", "ACTUAL COMPONENT ONLY", "MULTIMODE OPEN", "E.24 OPEN", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075q")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75r.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75r.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075r")), false);
});
