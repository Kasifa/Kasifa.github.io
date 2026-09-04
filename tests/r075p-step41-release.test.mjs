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

test("R0.75P reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075p_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075p-step41-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75p.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75p.pdf"));
  assert.equal(binding.publicPdf.pageCount, 168);
  assert.equal(binding.frozenAuthority.sourceCommit, "272b4d29a419becd5188721dfdfc88d2a4194082");
  assert.equal(binding.frozenAuthority.handoffCommit, "2e6c8de0278ebb74aea3dac5c12093a61b13c5ac");
  assert.equal(binding.frozenAuthority.coreParentCommit, "272b4d29a419becd5188721dfdfc88d2a4194082");
  assert.equal(binding.frozenAuthority.handoffSha256, "5b35e9981b53402602fc5261b3546a1ead2762b7ad1f348e361c6512e037ef1c");
  assert.equal(binding.claimBoundary.entranceConcentration, "ASSUMED_E_IN_GE_MU_E0_P1");
  assert.equal(binding.claimBoundary.localEnergyPersistence, "E_PHI_GE_MU_E0_OVER_2_TO_TAU_P20");
  assert.equal(binding.claimBoundary.packetFluxGain, "MU_MINUS_5_OVER_3_K_MINUS_2_OVER_3_P4_P26_TO_P28");
  assert.equal(binding.claimBoundary.strictConcentrationThreshold, "SIGMA_LT_8558_OVER_178605_P5_P29_P30");
  assert.equal(binding.claimBoundary.paymentScope, "CONDITIONAL_SAME_VELOCITY_ACTUAL_COMPONENT_P31");
  assert.equal(binding.claimBoundary.physicalCollarLocalization, "PROVED_FOR_ENTRANCE_CONCENTRATED_PACKET");
  assert.equal(binding.claimBoundary.lowEntranceConcentration, "OPEN_NOT_COUNTEREXAMPLE");
  assert.equal(binding.claimBoundary.interPacketSummation, "OPEN");
  assert.equal(binding.claimBoundary.nonconstantShear, "OPEN");
  assert.equal(binding.claimBoundary.e24, "OPEN");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75p.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75p.pdf")), false);
});

test("R0.75P routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075p"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075p-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75P Step 41", "BUFFERED-COLLAR ENTRANCE CONCENTRATION", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75P Step 41 的 bounded primary-source screen", "P.7--P.10", "P.29--P.30", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.20", html: 244, pdf: 201, published: 184, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75P" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 146);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 18);
  assert.equal(inventory.latestPublishedRelease, "r075p");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075p").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075p"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075p").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075p");
  assert.equal(manifest.latestCompletedStep, 41);
  assert.equal(manifest.nextRelease, "r075q");
  assert.equal(manifest.latestReleaseGate, "tests/r075p-step41-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075p-step41-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075p-step41-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "272b4d29a419becd5188721dfdfc88d2a4194082");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "2e6c8de0278ebb74aea3dac5c12093a61b13c5ac");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");
  const freeze = JSON.parse(read("research/r075p_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75P");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.entrance_concentration, "ASSUMED_E_IN_GE_MU_E0_P1");
  assert.equal(freeze.claim_status.packet_flux_gain, "MU_MINUS_5_OVER_3_K_MINUS_2_OVER_3_P4_P26_TO_P28");
  assert.equal(freeze.claim_status.strict_concentration_threshold, "SIGMA_LT_8558_OVER_178605_P5_P29_P30");
  assert.equal(freeze.claim_status.payment_scope, "CONDITIONAL_SAME_VELOCITY_ACTUAL_COMPONENT_P31");
  assert.equal(freeze.claim_status.inter_packet_summation, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.E24, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075p-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": \d+/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75P keeps exclusions explicit and does not publish future or figure output", () => {
  const note = read("public/notes/r0-75p.html");
  for (const marker of ["CONSTANT SHEAR", "ENTRANCE CONCENTRATION", "MOVING CUTOFF", "3D COLLAR CUBIC", "K^-2/3 GAIN", "ACTUAL COMPONENT ONLY", "E.24 OPEN", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075p")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75q.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75q.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075q")), false);
});
