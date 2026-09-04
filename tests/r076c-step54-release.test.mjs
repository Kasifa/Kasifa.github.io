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

test("R0.76C note PDF is cryptographically bound while W recap is retained", () => {
  const binding = JSON.parse(read("research/r076c_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r076c-step54-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.76C");
  assert.equal(binding.step, 54);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.ok(binding.publicPdf.pageCount >= 241);
  assert.equal(binding.publicPdf.title, "R0.76C｜固定有限倍频带剪切的全频通量支付");
  assert.equal(binding.frozenAuthority.sourceCommit, "e2057338114e1d09355270196d23c37a13b25048");
  assert.equal(binding.frozenAuthority.handoffCommit, null);
  assert.equal(binding.frozenAuthority.coreParentCommit, "87fdf888a511c47a64816c281e117f2462358bb8");
  assert.equal(binding.frozenAuthority.handoffSha256, "58bea911e1556a56632fb924a023e8c72ffa7765d2e5e7d5f35693abc4f84884");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "d71ced54951327205076e3718695847baabfde41c6ee58807f99a8c70f0cdf44");
  assert.equal(binding.claimBoundary.harmonicScope, "EACH_FIXED_INTEGER_Q_EXACT_REAL_DYADIC_BAND");
  assert.equal(binding.claimBoundary.integerModes, "REQUIRED_POSITIVE_INTEGERS");
  assert.equal(binding.claimBoundary.realPhases, "REQUIRED_REAL_NUMBERS");
  assert.equal(binding.claimBoundary.sufficientlyLargeFrozenL, true);
  assert.equal(binding.claimBoundary.allCarriers, "PROVED_FOR_EACH_FIXED_Q_EXACT_REAL_DYADIC_SHEAR");
  assert.equal(binding.claimBoundary.inverseRadiusBranch, "R076B_N1_R_LE_ONE");
  assert.equal(binding.claimBoundary.ultraHighCarrierBranch, "R076C_N1_R_GT_ONE");
  assert.equal(binding.claimBoundary.temporalFamily, "POINTWISE_EXPONENTIAL_POLYNOMIAL_SATISFYING_C12_ONLY");
  assert.equal(binding.claimBoundary.weightedLambdaPower, "MINUS_ONE_THIRD");
  assert.equal(binding.claimBoundary.terminalLambdaPower, "ZERO");
  assert.equal(binding.claimBoundary.branchesExhaustiveWithinClaim, true);
  assert.equal(binding.claimBoundary.qUniformGrowingEstimate, false);
  assert.equal(binding.claimBoundary.completeRealSquare, "RETAINED_BEFORE_ABSOLUTE_VALUES");
  assert.equal(binding.claimBoundary.selfAndCrossTerms, "ALL_REASSEMBLED_BEFORE_ABSOLUTE_VALUES");
  assert.equal(binding.claimBoundary.spectralSeparationUsed, false);
  assert.equal(binding.claimBoundary.localizedCurrentSignUsed, false);
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.required, false);
  assert.equal(binding.cumulativeRecap.updatedThrough, "R0.75W");
  assert.equal(binding.cumulativeRecap.nodeCount, 191);
  assert.equal(binding.cumulativeRecap.retainedHtmlSha256, "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(binding.cumulativeRecap.retainedPdfSha256, "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76C routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r076c"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r076c-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.76C Step 54", "FIXED-Q FULL-FREQUENCY FLUX PAYMENT", "159 节已公开", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.76C Step 54 的 bounded primary-source screen", "FIXED-Q FULL-FREQUENCY EXACT-SHEAR PAYMENT", "C.28--C.34", "FIXED Q ONLY", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.33", html: 257, pdf: 214, published: 197, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.76C" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 159);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 31);
  assert.equal(inventory.latestPublishedRelease, "r076c");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r076c").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r076c"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r076c").length, 1);
  assert.equal(inventory.sameReleaseCompletedSteps.r076c, 54);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r076c");
  assert.equal(manifest.latestCompletedStep, 54);
  assert.equal(manifest.nextRelease, "r076d");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r076c-step54-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "e2057338114e1d09355270196d23c37a13b25048");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, null);
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r076c_freeze_manifest.json"));
  assert.equal(freeze.scope, "FIXED_Q_FULL_FREQUENCY_EXACT_REAL_DYADIC_SHEAR_FLUX_PAYMENT");
  assert.equal(freeze.claim_status.fixed_q, "PROVED_FOR_EACH_FIXED_INTEGER_Q_GE_1_NOT_UNIFORM_IN_GROWING_Q");
  assert.equal(freeze.claim_status.integer_modes, "REQUIRED_NJ_IN_POSITIVE_INTEGERS");
  assert.equal(freeze.claim_status.real_phases, "REQUIRED_PHIJ_IN_REAL_NUMBERS");
  assert.equal(freeze.claim_status.all_carriers, "PROVED_FOR_EACH_FIXED_Q_EXACT_REAL_DYADIC_SHEAR");
  assert.equal(freeze.claim_status.inverse_radius_branch, "PAID_BY_R076B_N1_R_LE_ONE");
  assert.equal(freeze.claim_status.ultra_high_branch, "PROVED_HERE_N1_R_GT_ONE");
  assert.equal(freeze.claim_status.temporal_trace, "POINTWISE_EXPONENTIAL_POLYNOMIAL_FAMILY_SATISFYING_C12_ONLY");
  assert.equal(freeze.claim_status.weighted_lambda_power, "MINUS_ONE_THIRD");
  assert.equal(freeze.claim_status.terminal_lambda_power, "ZERO");
  assert.equal(freeze.claim_status.complete_real_square, "RETAINED_BEFORE_ABSOLUTE_VALUES");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.publication_handoff.retained_recap_terminal_release, "R0.75W_STEP48");
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r076c-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 46/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.76C publishes no figure, growing-q, arbitrary-field, unconditional Version-M, or recap rewrite", () => {
  const note = read("public/notes/r0-76c.html");
  for (const marker of ["FIXED INTEGER Q", "INTEGER MODES", "REAL PHASES", "ALL CARRIERS", "N_1 R &gt; 1 · C", "C.14 POINTWISE FAMILY", "COMPLETE REAL SQUARE", "Q-GROWTH OPEN", "NO FIGURE / NO DNS", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r076c")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
