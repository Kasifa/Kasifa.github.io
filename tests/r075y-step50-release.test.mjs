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

test("R0.75Y note PDF is cryptographically bound while W recap is retained", () => {
  const binding = JSON.parse(read("research/r075y_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075y-step50-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.75Y");
  assert.equal(binding.step, 50);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.ok(binding.publicPdf.pageCount >= 216);
  assert.equal(binding.publicPdf.title, "R0.75Y｜强分离多谐波族的完整 signed-flux 付款");
  assert.equal(binding.frozenAuthority.sourceCommit, "cb150f97a6c2595066360c0d4c6aca3c4062bdbe");
  assert.equal(binding.frozenAuthority.handoffCommit, null);
  assert.equal(binding.frozenAuthority.coreParentCommit, "4d12592f991e2cbb7db65f5470579783c2791fab");
  assert.equal(binding.frozenAuthority.handoffSha256, "945d918d54b0309c340b8aa3048e0ddd2f624c302eb687331b8a9312807a1c17");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "327cefd9cefe0c1878c5f5b2b4ba96105e2a1b0376a23a29cb8d3acb65ee0763");
  assert.equal(binding.claimBoundary.harmonicScope, "STRONGLY_SEPARATED_FINITE_REAL_FAMILY_ONE_DYADIC_BAND");
  assert.equal(binding.claimBoundary.strongSeparationCondition, "A_R_DELTA_N_GE_8Q");
  assert.equal(binding.claimBoundary.explicitModeCountCost, "Q_SQUARED_NO_HIDDEN_Q_CONSTANT");
  assert.equal(binding.claimBoundary.modalRowCount, "EXACTLY_Q_SQUARED_SELF_DIFFERENCE_SUM_ROWS");
  assert.equal(binding.claimBoundary.exactL2Rate, "MINUS_2_OVER_11907_FIXED_Q");
  assert.equal(binding.claimBoundary.growingQRate, "MINUS_2_OVER_11907_IF_LOG_Q_O_L_SQUARED_AND_STRONG_SEPARATION_CONTINUES");
  assert.equal(binding.claimBoundary.unresolvedHighCarrierClusters, "OPEN_A_R_DELTA_N_LT_8Q");
  assert.equal(binding.claimBoundary.versionMSameVelocityInclusion, "CONDITIONAL_MEASUREMENT_WEIGHT_REALIZED_SUBCLASS_ACTUAL_COMPONENT_LEDGER_ALIGNMENT");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.required, false);
  assert.equal(binding.cumulativeRecap.updatedThrough, "R0.75W");
  assert.equal(binding.cumulativeRecap.nodeCount, 191);
  assert.equal(binding.cumulativeRecap.retainedHtmlSha256, "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(binding.cumulativeRecap.retainedPdfSha256, "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.75Y routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075y"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075y-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75Y Step 50", "STRONGLY SEPARATED MULTIMODE", "155 节已公开", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75Y Step 50 的 bounded primary-source screen", "STRONGLY SEPARATED · EXPLICIT q^2 COST", "Y.15--Y.19", "Y.38", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.29", html: 253, pdf: 210, published: 193, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.75Y" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 155);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 27);
  assert.equal(inventory.latestPublishedRelease, "r075y");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075y").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075y"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075y").length, 1);
  assert.equal(inventory.sameReleaseCompletedSteps.r075y, 50);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075y");
  assert.equal(manifest.latestCompletedStep, 50);
  assert.equal(manifest.nextRelease, "r075z");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075y-step50-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "cb150f97a6c2595066360c0d4c6aca3c4062bdbe");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, null);
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r075y_freeze_manifest.json"));
  assert.equal(freeze.scope, "STRONGLY_SEPARATED_MULTIMODE_SIGNED_FLUX_PAYMENT");
  assert.equal(freeze.claim_status.strong_separation, "PROVED_ASSUMPTION_Y3_A_R_DELTA_N_GE_8Q");
  assert.equal(freeze.claim_status.explicit_mode_count_cost, "Q_SQUARED_NO_HIDDEN_Q_CONSTANT");
  assert.equal(freeze.claim_status.unresolved_high_carrier_clusters, "OPEN_A_R_DELTA_N_LT_8Q");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.publication_handoff.retained_recap_terminal_release, "R0.75W_STEP48");
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075y-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 49/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75Y publishes no figure or later-release output and does not rewrite W recap", () => {
  const note = read("public/notes/r0-75y.html");
  for (const marker of ["STRONGLY SEPARATED", "EXPLICIT q^2 COST", "CLUSTERS OPEN", "VERSION-M CONDITIONAL", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075y")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75z.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75z.pdf")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
