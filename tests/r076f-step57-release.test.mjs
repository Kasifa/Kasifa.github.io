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

test("R0.76F note PDF is cryptographically bound while W recap is retained", () => {
  const binding = JSON.parse(read("research/r076f_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r076f-step57-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.76F");
  assert.equal(binding.step, 57);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.ok(binding.publicPdf.pageCount >= 260);
  assert.equal(binding.publicPdf.title, "R0.76F｜继承空间观测的指数下界");
  assert.equal(binding.frozenAuthority.sourceCommit, "ff0254315b2fc4f2aaab1ee6f3f2ddcaaeac7366");
  assert.equal(binding.frozenAuthority.handoffCommit, "52ee189e3dfaa2ea0924ed44cd2e1196b2ec3a5b");
  assert.equal(binding.frozenAuthority.coreParentCommit, "01473589257b882c5b35e0d04fb58a71b36c9093");
  assert.equal(binding.frozenAuthority.handoffSha256, "5bf493b8703bb33233d846d4db8d1c621320d565a80e02a339b17431325bf06c");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "8a2ee0b0d69aa5002119da6db10f685230d2af48e2ed09f099fcd5c5153ca45b");
  assert.equal(binding.claimBoundary.spatialObservationLowerBound, "AT_LEAST_TWO_TO_Q_MINUS_ONE");
  assert.equal(binding.claimBoundary.observationConstant, "LOG_C_Q_AT_LEAST_Q_MINUS_ONE_TIMES_LOG_TWO");
  assert.equal(binding.claimBoundary.upperLowerOrderMatch, "EXP_THETA_Q_ONLY_NO_OPTIMAL_BASE_CLAIM");
  assert.equal(binding.claimBoundary.exactShearEmbedding, "SMOOTH_UNFORCED_CONSTANT_PRESSURE_WITH_B_ZERO");
  assert.equal(binding.claimBoundary.completeTransportFlux, "ZERO_FOR_REALIZING_EXAMPLE");
  assert.equal(binding.claimBoundary.completeCollarFluxLowerBound, false);
  assert.equal(binding.claimBoundary.finiteCertificateIsContinuumProof, false);
  assert.equal(binding.claimBoundary.arbitraryPacketTheorem, false);
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.required, false);
  assert.equal(binding.cumulativeRecap.updatedThrough, "R0.75W");
  assert.equal(binding.cumulativeRecap.nodeCount, 191);
  assert.equal(binding.cumulativeRecap.retainedHtmlSha256, "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(binding.cumulativeRecap.retainedPdfSha256, "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
test("R0.76F routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r076f"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r076f-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.76F Step 57", "EXPONENTIAL SPATIAL-OBSERVATION LOWER BOUND", "162 节已公开", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.76F Step 57 的 bounded primary-source screen", "EXPONENTIAL SPATIAL-OBSERVATION LOWER BOUND", "2^(q-1)", "NO COMPLETE-FLUX LOWER BOUND", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.36", html: 260, pdf: 217, published: 200, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.76F" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 162);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 34);
  assert.equal(inventory.latestPublishedRelease, "r076f");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r076f").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r076f"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r076f").length, 1);
  assert.equal(inventory.sameReleaseCompletedSteps.r076f, 57);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r076f");
  assert.equal(manifest.latestCompletedStep, 57);
  assert.equal(manifest.nextRelease, "r076g");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r076f-step57-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "ff0254315b2fc4f2aaab1ee6f3f2ddcaaeac7366");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "52ee189e3dfaa2ea0924ed44cd2e1196b2ec3a5b");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r076f_freeze_manifest.json"));
  assert.equal(freeze.scope, "EXPONENTIAL_LOWER_BOUND_FOR_INHERITED_SPATIAL_OBSERVATION");
  assert.equal(freeze.claim_status.spatial_observation_lower_bound, "AT_LEAST_TWO_TO_Q_MINUS_ONE");
  assert.equal(freeze.claim_status.observation_constant, "LOG_C_Q_AT_LEAST_Q_MINUS_ONE_TIMES_LOG_TWO");
  assert.equal(freeze.claim_status.complete_collar_flux_lower_bound, "NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.publication_handoff.retained_recap_terminal_release, "R0.75W_STEP48");
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r076f-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 59/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.76F publishes no figure, complete-flux lower bound, arbitrary-packet theorem, or recap rewrite", () => {
  const note = read("public/notes/r0-76f.html");
  for (const marker of ["2^(Q-1) LOWER BOUND", "EXP(THETA(Q)) SHARPNESS", "B = 0", "SPATIAL ROW ONLY", "NO FULL-FLUX LOWER BOUND", "NO FIGURE / NO DNS", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r076f")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
