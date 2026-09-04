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

test("R0.75R reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075r_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075r-step43-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75r.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75r.pdf"));
  assert.equal(binding.publicPdf.pageCount, 180);
  assert.equal(binding.frozenAuthority.sourceCommit, "0b7a57c826823d14bfad66913556e8ed88584325");
  assert.equal(binding.frozenAuthority.handoffCommit, "9f99f88cdf8fb2d209401d8a6bc213df53bb2130");
  assert.equal(binding.frozenAuthority.coreParentCommit, "0b7a57c826823d14bfad66913556e8ed88584325");
  assert.equal(binding.frozenAuthority.handoffSha256, "7276d853ea41be03a638ff91faad79fe05da16cf15ab822a79acbbd76c965105");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "8ce8bbc86a92bd43ce84d0db0c8bfb4630a094fd06a1a71481f695e7fc2e06b8");
  assert.equal(binding.claimBoundary.radialCrossSectionIdentity, "PROVED_R12_TO_R14");
  assert.equal(binding.claimBoundary.realHighBandPacket, "PROVED_R19_TO_R23");
  assert.equal(binding.claimBoundary.signedFluxLowerBound, "PROVED_R35");
  assert.equal(binding.claimBoundary.plateauCubicUpperBound, "PROVED_R38");
  assert.equal(binding.claimBoundary.normalizedDivergence, "PROVED_R40_R41");
  assert.equal(binding.claimBoundary.plateauOnlyMultimodePayment, "RULED_OUT_UNIFORMLY");
  assert.equal(binding.claimBoundary.fullCutoffSupportPayment, "OPEN_NOT_COUNTEREXAMPLE");
  assert.equal(binding.claimBoundary.versionMAdmissibilityAndAggregation, "OPEN_NOT_COUNTEREXAMPLE");
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

test("R0.75R routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075r"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075r-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75R Step 43", "OUTER-CAP SPECTRAL CONCENTRATION OBSTRUCTION", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75R Step 43 的 bounded primary-source screen", "R.12--R.14", "R.40--R.41", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.22", html: 246, pdf: 203, published: 186, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75R" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 148);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 20);
  assert.equal(inventory.latestPublishedRelease, "r075r");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075r").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075r"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075r").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075r");
  assert.equal(manifest.latestCompletedStep, 43);
  assert.equal(manifest.nextRelease, "r075s");
  assert.equal(manifest.latestReleaseGate, "tests/r075r-step43-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075r-step43-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075r-step43-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "0b7a57c826823d14bfad66913556e8ed88584325");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "9f99f88cdf8fb2d209401d8a6bc213df53bb2130");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");
  const freeze = JSON.parse(read("research/r075r_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75R");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.radial_cross_section_identity, "PROVED_R12_TO_R14");
  assert.equal(freeze.claim_status.real_high_band_packet, "PROVED_R19_TO_R23");
  assert.equal(freeze.claim_status.plateau_only_multimode_payment, "RULED_OUT_UNIFORMLY");
  assert.equal(freeze.claim_status.full_cutoff_support_payment, "OPEN_NOT_COUNTEREXAMPLE");
  assert.equal(freeze.claim_status.version_m_admissibility_and_aggregation, "OPEN_NOT_COUNTEREXAMPLE");
  assert.equal(freeze.claim_status.E24, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075r-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 46/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75R keeps exclusions explicit and does not publish future or figure output", () => {
  const note = read("public/notes/r0-75r.html");
  for (const marker of ["NEGATIVE RESULT", "EXACT SMOOTH SHEAR", "REAL HIGH-BAND PACKET", "OUTER-CAP CONCENTRATION", "DIRICHLET KERNEL", "SIGNED FLUX LOWER", "PLATEAU CUBIC UPPER", "AMPLITUDE CANCELS", "PLATEAU-ONLY NO-GO", "FULL SUPPORT OPEN", "VERSION-M OPEN", "E.24 OPEN", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075r")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75s.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75s.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075s")), false);
});
