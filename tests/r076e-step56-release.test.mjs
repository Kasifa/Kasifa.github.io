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

test("R0.76E note PDF is cryptographically bound while W recap is retained", () => {
  const binding = JSON.parse(read("research/r076e_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r076e-step56-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.76E");
  assert.equal(binding.step, 56);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.ok(binding.publicPdf.pageCount >= 254);
  assert.equal(binding.publicPdf.title, "R0.76E｜精确剪切的线性模态熵窗口");
  assert.equal(binding.frozenAuthority.sourceCommit, "0e929c4066f2111545afa4683b363edac8440825");
  assert.equal(binding.frozenAuthority.handoffCommit, null);
  assert.equal(binding.frozenAuthority.coreParentCommit, "1bb929241ebd5a889babce8e86b4641a665eb64a");
  assert.equal(binding.frozenAuthority.handoffSha256, "a6c640a20ab75981b6f21506f69917b4fa60ed1ce7c4b47c8dd62cfaec79ead8");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "fb0498be663ff220ab99c04d861534cf8669ea8fed01e97ffedfa19301229519");
  assert.equal(binding.claimBoundary.modalEntropyLoss, "EXP_CSTAR_Q_REQUIRED_NOT_SUPPRESSED");
  assert.equal(binding.claimBoundary.growingModeWindow, "Q_OF_L_IS_O_OF_L_SQUARED");
  assert.equal(binding.claimBoundary.frozenCoefficientRate, "MINUS_TWO_OVER_11907_RETAINED_IN_WINDOW");
  assert.equal(binding.claimBoundary.delayedStableClock, "S_N_EQUALS_C0_N_LOG_N_PLUS_1_UNIFORM_IN_N");
  assert.equal(binding.claimBoundary.earlyInterval, "HOLDER_WITH_FULL_K_T_GIVES_S_N_TO_FOUR_THIRDS");
  assert.equal(binding.claimBoundary.lateInterval, "CENTERED_ESTIMATE_USED_ONLY_AFTER_MONOTONICITY");
  assert.equal(binding.claimBoundary.endpointComparison, "LAST_UNIT_TURAN_NAZAROV_EXP_CN_T_MINUS_TWO_THIRDS_K_T_TWO_THIRDS");
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
test("R0.76E routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r076e"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r076e-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.76E Step 56", "LINEAR MODAL-ENTROPY WINDOW", "161 节已公开", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.76E Step 56 的 bounded primary-source screen", "LINEAR MODAL-ENTROPY WINDOW", "E.22", "EXP(CQ) LOSS RETAINED", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.35", html: 259, pdf: 216, published: 199, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.76E" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 161);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 33);
  assert.equal(inventory.latestPublishedRelease, "r076e");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r076e").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r076e"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r076e").length, 1);
  assert.equal(inventory.sameReleaseCompletedSteps.r076e, 56);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r076e");
  assert.equal(manifest.latestCompletedStep, 56);
  assert.equal(manifest.nextRelease, "r076f");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r076e-step56-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "0e929c4066f2111545afa4683b363edac8440825");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r076e_freeze_manifest.json"));
  assert.equal(freeze.scope, "LINEAR_MODAL_ENTROPY_WINDOW_FOR_EXACT_REAL_CONSTANT_SHEARS");
  assert.equal(freeze.claim_status.modal_entropy_loss, "EXP_CSTAR_Q_REQUIRED_NOT_SUPPRESSED");
  assert.equal(freeze.claim_status.growing_mode_window, "Q_OF_L_IS_O_OF_L_SQUARED");
  assert.equal(freeze.claim_status.delayed_stable_clock, "S_N_EQUALS_C0_N_LOG_N_PLUS_1_UNIFORM_IN_N");
  assert.equal(freeze.claim_status.endpoint_comparison, "LAST_UNIT_TURAN_NAZAROV_EXP_CN_T_MINUS_TWO_THIRDS_K_T_TWO_THIRDS");
  assert.equal(freeze.claim_status.external_inputs, "TURAN_NAZAROV_AND_ERDELYI");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.publication_handoff.retained_recap_terminal_release, "R0.75W_STEP48");
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r076e-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 56/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.76E publishes no figure, arbitrary-packet theorem, unconditional Version-M, or recap rewrite", () => {
  const note = read("public/notes/r0-76e.html");
  for (const marker of ["EXP(C Q) LOSS", "Q(L) = o(L^2)", "DELAYED STABLE HEAT CLOCK", "LAST-UNIT ENDPOINT", "B!=0 VERSION-M CONDITIONAL", "NO FIGURE / NO DNS", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r076e")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
