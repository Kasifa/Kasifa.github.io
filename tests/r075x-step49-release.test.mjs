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

test("R0.75X note PDF is cryptographically bound while W recap is retained", () => {
  const binding = JSON.parse(read("research/r075x_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075x-step49-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.75X");
  assert.equal(binding.step, 49);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.ok(binding.publicPdf.pageCount >= 210);
  assert.equal(binding.publicPdf.title, "R0.75X｜固定有限谐波族的低载频 signed-flux 付款");
  assert.equal(binding.frozenAuthority.sourceCommit, "a97e197521b4efc0e3450f34cda5e646a2560d57");
  assert.equal(binding.frozenAuthority.handoffCommit, null);
  assert.equal(binding.frozenAuthority.coreParentCommit, "3f2461b7ae0fd4a19c6d83dea859ead9fb5ff64d");
  assert.equal(binding.frozenAuthority.handoffSha256, "bf49a24643fda42abc7cc863349dd4da29dafe76e1ff8cc18641c6c7ca09f4cd");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "7c013cdc97247ddb54ef588a44a7df4f0d689fbaf2a95fd10f70b3512e1122c5");
  assert.equal(binding.claimBoundary.harmonicScope, "EVERY_FIXED_FINITE_REAL_FAMILY_ONE_DYADIC_BAND");
  assert.equal(binding.claimBoundary.lowCarrierCondition, "PROVED_X5_N1_A_R_LT_C0");
  assert.equal(binding.claimBoundary.fixedQConstant, "FINITE_CQ_INDEPENDENT_OF_R_FREQUENCIES_GAPS_AMPLITUDES_PHASES_B");
  assert.equal(binding.claimBoundary.uniformQGrowth, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.highCarrierThreeOrMoreModes, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.localEnergyIdentity, "PROVED_X26_X33_NO_DIVISION_BY_V_AMPLITUDE_FREQUENCY_OR_GAP");
  assert.equal(binding.claimBoundary.exactL2Rate, "MINUS_2_OVER_11907");
  assert.equal(binding.claimBoundary.versionMSameVelocityInclusion, "CONDITIONAL_MEASUREMENT_WEIGHT_REALIZED_SUBCLASS_ACTUAL_COMPONENT_LEDGER_ALIGNMENT");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.required, false);
  assert.equal(binding.cumulativeRecap.updatedThrough, "R0.75W");
  assert.equal(binding.cumulativeRecap.nodeCount, 191);
  assert.equal(binding.cumulativeRecap.retainedHtmlSha256, "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(binding.cumulativeRecap.retainedPdfSha256, "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.75X routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075x"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075x-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75X Step 49", "FIXED FINITE LOW CARRIER", "154 节已公开", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75X Step 49 的 bounded primary-source screen", "FIXED FINITE q · LOW CARRIER ONLY", "X.15--X.20", "X.36", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.28", html: 252, pdf: 209, published: 192, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.75X" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 154);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 26);
  assert.equal(inventory.latestPublishedRelease, "r075x");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075x").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075x"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075x").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075x");
  assert.equal(manifest.latestCompletedStep, 49);
  assert.equal(manifest.nextRelease, "r075y");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075x-step49-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "a97e197521b4efc0e3450f34cda5e646a2560d57");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, null);
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r075x_freeze_manifest.json"));
  assert.equal(freeze.scope, "FIXED_FINITE_MODE_LOW_CARRIER_SIGNED_FLUX_PAYMENT");
  assert.equal(freeze.claim_status.low_carrier_sector, "PROVED_X5_N1_A_R_LT_C0");
  assert.equal(freeze.claim_status.uniform_q_growth, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.high_carrier_three_or_more_modes, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.publication_handoff.retained_recap_terminal_release, "R0.75W_STEP48");
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075x-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 54/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75X publishes no figure or later-release output and does not rewrite W recap", () => {
  const note = read("public/notes/r0-75x.html");
  for (const marker of ["FIXED FINITE q", "LOW CARRIER ONLY", "NO UNIFORM q GROWTH", "HIGH CARRIER 3+ OPEN", "VERSION-M CONDITIONAL", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075x")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75y.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75y.pdf")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
