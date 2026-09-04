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

test("R0.75Z note PDF is cryptographically bound while W recap is retained", () => {
  const binding = JSON.parse(read("research/r075z_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075z-step51-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.75Z");
  assert.equal(binding.step, 51);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.ok(binding.publicPdf.pageCount >= 223);
  assert.equal(binding.publicPdf.title, "R0.75Z｜未解簇正规形与载频电流门");
  assert.equal(binding.frozenAuthority.sourceCommit, "85e633132cbcde89ec78bfef465f3c0393c27994");
  assert.equal(binding.frozenAuthority.handoffCommit, null);
  assert.equal(binding.frozenAuthority.coreParentCommit, "d1d9f261425804ecb53aa99ddb56705c87267c24");
  assert.equal(binding.frozenAuthority.handoffSha256, "295af460aa6f15624a1d41adeeb6c0974acb3ee4f2c194f47777755d41c7b639");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "8aa60590a884f4be7ac85167f693420a934bc3e57d3ce4a8a7571088ab53d6ab");
  assert.equal(binding.claimBoundary.xyzPartition, "EXHAUSTIVE_X_LOW_Y_STRONGLY_SEPARATED_Z_CLUSTERED_HIGH");
  assert.equal(binding.claimBoundary.equalityConvention, "GAP_TIMES_ELL_EQ_8Q_IS_Y_SEPARATOR");
  assert.equal(binding.claimBoundary.localCurrentIdentity, "PROVED_WITH_MINUS_4_N_J");
  assert.equal(binding.claimBoundary.pointwiseAbsorption, "NO_CARRIER_UNIFORM_2N_ABS_J_BY_Q_PLUS_ABS_ZY_SQUARED");
  assert.equal(binding.claimBoundary.naiveRecursiveXStrategy, "CLOSED_ONLY_AFTER_POINTWISE_ABSOLUTE_CURRENT");
  assert.equal(binding.claimBoundary.fullClusteredSectorPayment, "OPEN_NOT_PROVED_OR_DISPROVED");
  assert.equal(binding.claimBoundary.clusterAdditivity, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.crossClusterProductsAndPayment, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.counterexampleToFinalClusterFlux, false);
  assert.equal(binding.claimBoundary.versionMSameVelocityInclusion, "CONDITIONAL_MEASUREMENT_WEIGHT_REALIZED_SUBCLASS_ACTUAL_COMPONENT_LEDGER_ALIGNMENT");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.required, false);
  assert.equal(binding.cumulativeRecap.updatedThrough, "R0.75W");
  assert.equal(binding.cumulativeRecap.nodeCount, 191);
  assert.equal(binding.cumulativeRecap.retainedHtmlSha256, "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(binding.cumulativeRecap.retainedPdfSha256, "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.75Z routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075z"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075z-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75Z Step 51", "CLUSTER CARRIER-CURRENT GATE", "156 节已公开", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75Z Step 51 的 bounded primary-source screen", "EXACT PARTITION · NARROW METHOD NO-GO", "Z.18--Z.21", "NO COUNTEREXAMPLE CLAIM", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.30", html: 254, pdf: 211, published: 194, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.75Z" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 156);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 28);
  assert.equal(inventory.latestPublishedRelease, "r075z");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075z").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075z"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075z").length, 1);
  assert.equal(inventory.sameReleaseCompletedSteps.r075z, 51);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075z");
  assert.equal(manifest.latestCompletedStep, 51);
  assert.equal(manifest.nextRelease, "r076a");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075z-step51-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "85e633132cbcde89ec78bfef465f3c0393c27994");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, null);
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r075z_freeze_manifest.json"));
  assert.equal(freeze.scope, "UNRESOLVED_CLUSTER_CARRIER_CURRENT_GATE");
  assert.equal(freeze.claim_status.fixed_q_xyz_partition, "PROVED_Z1_Z3_EXHAUSTIVE_WITH_Y_EQUALITY");
  assert.equal(freeze.claim_status.naive_recursive_x_strategy, "CLOSED_ONLY_AFTER_POINTWISE_ABSOLUTE_CURRENT");
  assert.equal(freeze.claim_status.full_clustered_sector_payment, "OPEN_NOT_PROVED_OR_DISPROVED");
  assert.equal(freeze.claim_status.counterexample_to_final_cluster_flux, "NOT_CLAIMED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.publication_handoff.retained_recap_terminal_release, "R0.75W_STEP48");
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075z-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 48/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75Z publishes no figure, later release, full-payment claim, or recap rewrite", () => {
  const note = read("public/notes/r0-75z.html");
  for (const marker of ["EXHAUSTIVE X/Y/Z PARTITION", "POINTWISE ABSORPTION NO-GO", "NAIVE X RECURSION CLOSED", "FULL CLUSTER PAYMENT OPEN", "NO COUNTEREXAMPLE CLAIM", "VERSION-M CONDITIONAL", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075z")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-76a.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-76a.pdf")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
