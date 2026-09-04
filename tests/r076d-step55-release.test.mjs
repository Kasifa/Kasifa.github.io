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

test("R0.76D note PDF is cryptographically bound while W recap is retained", () => {
  const binding = JSON.parse(read("research/r076d_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r076d-step55-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.76D");
  assert.equal(binding.step, 55);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.ok(binding.publicPdf.pageCount >= 248);
  assert.equal(binding.publicPdf.title, "R0.76D｜精确剪切的定量增长模态熵窗口");
  assert.equal(binding.frozenAuthority.sourceCommit, "c0cfe20b1970d9abbc32c191a5fad71dfdad1465");
  assert.equal(binding.frozenAuthority.handoffCommit, null);
  assert.equal(binding.frozenAuthority.coreParentCommit, "675638c96b204b7d853407fc2b0ace64ba5e061d");
  assert.equal(binding.frozenAuthority.handoffSha256, "8fb0b43aea6958a5fa40c36e118aa5dc7a9d275597f6ecb07ca9b719d97d9452");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "1231b3bf4de7e097f9e3cec947fa16716a5f4e3772365bfcecd2a3b6905f279e");
  assert.equal(binding.claimBoundary.modalEntropyLoss, "EXP_CSTAR_Q_LOG_Q_PLUS_1_REQUIRED_NOT_SUPPRESSED");
  assert.equal(binding.claimBoundary.growingModeWindow, "Q_OF_L_LOG_Q_OF_L_PLUS_1_IS_O_OF_L_SQUARED");
  assert.equal(binding.claimBoundary.frozenCoefficientRate, "MINUS_TWO_OVER_11907_RETAINED_IN_WINDOW");
  assert.equal(binding.claimBoundary.spatialDerivative, "ALPHA_PLUS_Q_FACTOR_RETAINED");
  assert.equal(binding.claimBoundary.maximumSpatialFrequencyDependence, "EXPLICIT_ALPHA_DEPENDENCE_RETAINED_NO_GAP_DENOMINATOR");
  assert.equal(binding.claimBoundary.factorialTail, "M_PLUS_ONE_FACTORIAL_OVER_FOUR");
  assert.equal(binding.claimBoundary.endpointComparison, "FIVE_OVER_FOUR_TO_THE_M_FACTOR_RETAINED");
  assert.equal(binding.claimBoundary.externalInputs, "TURAN_NAZAROV_AND_ERDELYI");
  assert.equal(binding.claimBoundary.finiteCertificateIsContinuumProof, false);
  assert.equal(binding.claimBoundary.arbitraryPacketTheorem, false);
  assert.match(binding.claimBoundary.versionMWhenBNonzero, /B_NONZERO|B_NE_ZERO/);
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.required, false);
  assert.equal(binding.cumulativeRecap.updatedThrough, "R0.75W");
  assert.equal(binding.cumulativeRecap.nodeCount, 191);
  assert.equal(binding.cumulativeRecap.retainedHtmlSha256, "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(binding.cumulativeRecap.retainedPdfSha256, "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76D routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r076d"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r076d-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.76D Step 55", "QUANTITATIVE GROWING-MODE ENTROPY WINDOW", "160 节已公开", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.76D Step 55 的 bounded primary-source screen", "QUANTITATIVE GROWING-MODE ENTROPY WINDOW", "D.25", "(5/4)^M RETAINED", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.34", html: 258, pdf: 215, published: 198, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.76D" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 160);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 32);
  assert.equal(inventory.latestPublishedRelease, "r076d");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r076d").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r076d"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r076d").length, 1);
  assert.equal(inventory.sameReleaseCompletedSteps.r076d, 55);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r076d");
  assert.equal(manifest.latestCompletedStep, 55);
  assert.equal(manifest.nextRelease, "r076e");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r076d-step55-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "c0cfe20b1970d9abbc32c191a5fad71dfdad1465");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r076d_freeze_manifest.json"));
  assert.equal(freeze.scope, "QUANTITATIVE_GROWING_MODE_ENTROPY_WINDOW_FOR_EXACT_REAL_CONSTANT_SHEARS");
  assert.equal(freeze.claim_status.modal_entropy_loss, "EXP_CSTAR_Q_LOG_Q_PLUS_1_REQUIRED_NOT_SUPPRESSED");
  assert.equal(freeze.claim_status.growing_mode_window, "Q_OF_L_LOG_Q_OF_L_PLUS_1_IS_O_OF_L_SQUARED");
  assert.equal(freeze.claim_status.spatial_observation, "TURAN_NAZAROV_VALUE_ROW_AND_ERDELYI_ALPHA_PLUS_Q_DERIVATIVE_ROW");
  assert.equal(freeze.claim_status.endpoint_comparison, "FIVE_OVER_FOUR_TO_THE_M_FACTOR_RETAINED");
  assert.equal(freeze.claim_status.external_inputs, "TURAN_NAZAROV_AND_ERDELYI");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.publication_handoff.retained_recap_terminal_release, "R0.75W_STEP48");
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r076d-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 56/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.76D publishes no figure, arbitrary-packet theorem, unconditional Version-M, or recap rewrite", () => {
  const note = read("public/notes/r0-76d.html");
  for (const marker of ["EXP(C Q LOG(Q+1))", "GROWING-MODE WINDOW", "ALPHA+Q DERIVATIVE", "(5/4)^M ENDPOINT", "B!=0 VERSION-M CONDITIONAL", "NO FIGURE / NO DNS", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r076d")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
