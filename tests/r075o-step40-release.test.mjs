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

test("R0.75O reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075o_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075o-step40-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75o.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75o.pdf"));
  assert.equal(binding.publicPdf.pageCount, 162);
  assert.equal(binding.frozenAuthority.sourceCommit, "9ad6873ca91c756309d009ffba142e4545f6c4c3");
  assert.equal(binding.frozenAuthority.handoffCommit, "9bf705522928d390472e062f8d244d6b8b5220a0");
  assert.equal(binding.frozenAuthority.coreParentCommit, "43a9b617df0b2478dbdfa649335d6b4040e926b7");
  assert.equal(binding.frozenAuthority.handoffSha256, "f0f5e667dca7be397782a750d8dff80b3e9c4c6fe13294846cfdf1a4d60d7cb5");
  assert.equal(binding.frozenAuthority.independentHandoffAuditSha256, "b68ad69da2d06796faf577a9bb9ea7297c9caf2c19c3e28dc4d72e4f664567a8");
  assert.equal(binding.claimBoundary.arbitraryVerticalFrequencyEnergyRow, "PROVED_WITHOUT_UPPER_VERTICAL_CAP_O4_TO_O12");
  assert.equal(binding.claimBoundary.energyFluxConstant, "ABS_T_LE_ABS_B_W_INFINITY_E0_OVER_4K2_O12");
  assert.equal(binding.claimBoundary.packetFluxGain, "K_MINUS_2_OVER_3_O2_O20");
  assert.equal(binding.claimBoundary.strictKappaThreshold, "KAPPA_GT_98605_OVER_71442_O22");
  assert.equal(binding.claimBoundary.paymentScope, "PACKET_OWN_FULL_T2_ATOM_ONLY_NOT_VERSION_M");
  assert.equal(binding.claimBoundary.physicalCollarLocalization, "OPEN");
  assert.equal(binding.claimBoundary.interPacketSummation, "OPEN");
  assert.equal(binding.claimBoundary.nonconstantShear, "OPEN");
  assert.equal(binding.claimBoundary.e24, "OPEN");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75o.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75o.pdf")), false);
});

test("R0.75O routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075o"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075o-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75O Step 40", "VERTICAL-DIFFUSION PACKET GAIN", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75O Step 40 的 bounded primary-source screen", "O.4--O.12", "O.23--O.24", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.19", html: 243, pdf: 200, published: 183, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75O" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 145);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 17);
  assert.equal(inventory.latestPublishedRelease, "r075o");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075o").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075o"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075o").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075o");
  assert.equal(manifest.latestCompletedStep, 40);
  assert.equal(manifest.nextRelease, "r075p");
  assert.equal(manifest.latestReleaseGate, "tests/r075o-step40-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075o-step40-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075o-step40-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "9ad6873ca91c756309d009ffba142e4545f6c4c3");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "9bf705522928d390472e062f8d244d6b8b5220a0");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");
  const freeze = JSON.parse(read("research/r075o_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75O");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.arbitrary_vertical_frequency_energy_row, "PROVED_WITHOUT_UPPER_VERTICAL_CAP_O4_TO_O12");
  assert.equal(freeze.claim_status.packet_flux_gain, "K_MINUS_2_OVER_3_O2_O20");
  assert.equal(freeze.claim_status.strict_kappa_threshold, "KAPPA_GT_98605_OVER_71442_O22");
  assert.equal(freeze.claim_status.payment_scope, "PACKET_OWN_FULL_T2_ATOM_ONLY_NOT_VERSION_M");
  assert.equal(freeze.claim_status.inter_packet_summation, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.E24, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075o-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 47/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75O keeps exclusions explicit and does not publish future or figure output", () => {
  const note = read("public/notes/r0-75o.html");
  for (const marker of ["CONSTANT SHEAR", "VERTICAL DIFFUSION", "SCHUR 1/4", "K^-2/3 GAIN", "FULL-T2 ATOM ONLY", "E.24 OPEN", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075o")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75p.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75p.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075p")), false);
});
