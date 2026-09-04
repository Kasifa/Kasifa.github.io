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

test("R0.75N reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075n_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075n-step39-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75n.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75n.pdf"));
  assert.equal(binding.publicPdf.pageCount, 158);
  assert.equal(binding.frozenAuthority.sourceCommit, "90a0d654447ba40865797669e5e5ad21ad9baa54");
  assert.equal(binding.frozenAuthority.handoffCommit, "43a9b617df0b2478dbdfa649335d6b4040e926b7");
  assert.equal(binding.frozenAuthority.handoffSha256, "07995870a834c9999f952443b71b46c13e9931187c7a04850f8db17c4b82a9d4");
  assert.equal(binding.frozenAuthority.independentHandoffAuditSha256, "f0690d04ad983a22669764dfd9066f2e584774854206362095a6c3d1149b4a8c");
  assert.equal(binding.claimBoundary.x1AveragedRow, "O_L_WITHOUT_R_NEGATIVE_POWER_N2");
  assert.equal(binding.claimBoundary.fullyAveragedRow, "O_L_SQUARED_R_N3_N16");
  assert.equal(binding.claimBoundary.coefficientwiseSupremumOrder, "SUM_ELL_SUP_X3_PROVED_N2_N13");
  assert.equal(binding.claimBoundary.universalCutoffTheorem, "OPEN");
  assert.equal(binding.claimBoundary.interPacketSummation, "OPEN");
  assert.equal(binding.claimBoundary.verticalDiffusion, "OPEN");
  assert.equal(binding.claimBoundary.e24, "OPEN");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75n.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75n.pdf")), false);
});

test("R0.75N routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075n"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075n-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75N Step 39", "RADIAL-COLLAR AVERAGED WIENER ROW", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75N Step 39 的 bounded primary-source screen", "N.6--N.9", "N.14--N.16", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.18", html: 242, pdf: 199, published: 182, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75N" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 144);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 16);
  assert.equal(inventory.latestPublishedRelease, "r075n");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075n").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075n"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075n").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075n");
  assert.equal(manifest.latestCompletedStep, 39);
  assert.equal(manifest.nextRelease, "r075o");
  assert.equal(manifest.latestReleaseGate, "tests/r075n-step39-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075n-step39-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075n-step39-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "90a0d654447ba40865797669e5e5ad21ad9baa54");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "43a9b617df0b2478dbdfa649335d6b4040e926b7");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");
  const freeze = JSON.parse(read("research/r075n_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75N");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.x1_averaged_row, "O_L_WITHOUT_R_NEGATIVE_POWER_N2");
  assert.equal(freeze.claim_status.fully_averaged_row, "O_L_SQUARED_R_N3_N16");
  assert.equal(freeze.claim_status.inter_packet_summation, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.E24, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075n-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 48/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75N keeps exclusions explicit and does not publish future or figure output", () => {
  const note = read("public/notes/r0-75n.html");
  for (const marker of ["CANONICAL RADIAL COLLAR", "SELECTABLE CUTOFF", "WIENER ROW O(L)", "FULL AVERAGE O(L^2 R)", "E.24 OPEN", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075n")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75o.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75o.pdf")), false);
});
