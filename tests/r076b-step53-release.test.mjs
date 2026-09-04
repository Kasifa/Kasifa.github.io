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

test("R0.76B note PDF is cryptographically bound while W recap is retained", () => {
  const binding = JSON.parse(read("research/r076b_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r076b-step53-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.76B");
  assert.equal(binding.step, 53);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.ok(binding.publicPdf.pageCount >= 234);
  assert.equal(binding.publicPdf.title, "R0.76B｜固定有限倍频带剪切的逆半径通量支付");
  assert.equal(binding.frozenAuthority.sourceCommit, "b31c53a5e48e2de56088ac2715a95000a64e2c9a");
  assert.equal(binding.frozenAuthority.handoffCommit, null);
  assert.equal(binding.frozenAuthority.coreParentCommit, "9d3e65316204f67f6122b5fdf47c38014d723e10");
  assert.equal(binding.frozenAuthority.handoffSha256, "cf35f0cbf8ffaddf392ae1635bdf022c08cf7801e5a7fac307db83d4ba365196");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "db93f10d26c0bb894ed1b06a999835d7eb4706b286bdfc763d9db97e32703bf3");
  assert.equal(binding.claimBoundary.harmonicScope, "EACH_FIXED_INTEGER_Q_EXACT_REAL_DYADIC_BAND");
  assert.equal(binding.claimBoundary.integerModes, "REQUIRED_POSITIVE_INTEGERS");
  assert.equal(binding.claimBoundary.realPhases, "REQUIRED_REAL_NUMBERS");
  assert.equal(binding.claimBoundary.sufficientlyLargeFrozenL, true);
  assert.equal(binding.claimBoundary.inverseRadiusCarrier, "PROVED_N1_R_LE_ONE");
  assert.equal(binding.claimBoundary.branchesExhaustiveWithinClaim, true);
  assert.equal(binding.claimBoundary.qUniformGrowingEstimate, false);
  assert.equal(binding.claimBoundary.completeRealSquare, "RETAINED_BEFORE_ABSOLUTE_VALUES");
  assert.equal(binding.claimBoundary.selfAndCrossTerms, "ALL_REASSEMBLED_BEFORE_ABSOLUTE_VALUES");
  assert.equal(binding.claimBoundary.spectralSeparationUsed, false);
  assert.equal(binding.claimBoundary.localizedCurrentSignUsed, false);
  assert.equal(binding.claimBoundary.ultraHighCarrier, "OPEN_N1_R_GT_ONE");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.required, false);
  assert.equal(binding.cumulativeRecap.updatedThrough, "R0.75W");
  assert.equal(binding.cumulativeRecap.nodeCount, 191);
  assert.equal(binding.cumulativeRecap.retainedHtmlSha256, "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(binding.cumulativeRecap.retainedPdfSha256, "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76B routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r076b"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r076b-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.76B Step 53", "FIXED-Q INVERSE-RADIUS FLUX PAYMENT", "158 节已公开", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.76B Step 53 的 bounded primary-source screen", "FIXED-Q INVERSE-RADIUS EXACT-SHEAR PAYMENT", "B.29--B.35", "FIXED Q ONLY", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.32", html: 256, pdf: 213, published: 196, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.76B" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 158);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 30);
  assert.equal(inventory.latestPublishedRelease, "r076b");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r076b").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r076b"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r076b").length, 1);
  assert.equal(inventory.sameReleaseCompletedSteps.r076b, 53);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r076b");
  assert.equal(manifest.latestCompletedStep, 53);
  assert.equal(manifest.nextRelease, "r076c");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r076b-step53-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "b31c53a5e48e2de56088ac2715a95000a64e2c9a");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, null);
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r076b_freeze_manifest.json"));
  assert.equal(freeze.scope, "FIXED_Q_INVERSE_RADIUS_EXACT_REAL_DYADIC_SHEAR_FLUX_PAYMENT");
  assert.equal(freeze.claim_status.fixed_q, "PROVED_FOR_EACH_FIXED_INTEGER_Q_GE_1_NOT_UNIFORM_IN_GROWING_Q");
  assert.equal(freeze.claim_status.integer_modes, "REQUIRED_NJ_IN_POSITIVE_INTEGERS");
  assert.equal(freeze.claim_status.real_phases, "REQUIRED_PHIJ_IN_REAL_NUMBERS");
  assert.equal(freeze.claim_status.inverse_radius_carrier, "PROVED_N1_R_LE_ONE");
  assert.equal(freeze.claim_status.complete_real_square, "RETAINED_BEFORE_ABSOLUTE_VALUES");
  assert.equal(freeze.claim_status.ultra_high_carrier, "OPEN_N1_R_GT_ONE");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.publication_handoff.retained_recap_terminal_release, "R0.75W_STEP48");
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r076b-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 47/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.76B publishes no figure, growing-q, ultra-high, arbitrary-field, unconditional Version-M, or recap rewrite", () => {
  const note = read("public/notes/r0-76b.html");
  for (const marker of ["FIXED INTEGER Q", "INTEGER MODES", "REAL PHASES", "COMPLETE REAL SQUARE", "Q-GROWTH OPEN", "N_1 R &gt; 1 OPEN", "NO FIGURE / NO DNS", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r076b")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
