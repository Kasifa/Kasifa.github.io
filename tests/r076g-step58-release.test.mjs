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

test("R0.76G note PDF is cryptographically bound while W recap is retained", () => {
  const binding = JSON.parse(read("research/r076g_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r076g-step58-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.76G");
  assert.equal(binding.step, 58);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.ok(binding.publicPdf.pageCount >= 265);
  assert.equal(binding.publicPdf.title, "R0.76G｜完整时钟中心纤维通量的指数下界");
  assert.equal(binding.frozenAuthority.sourceCommit, "17b366e477c46d11b4caa5e2026381bbf08e7d62");
  assert.equal(binding.frozenAuthority.handoffCommit, "6f203611dc13b7343005bcab3a429b6c68b10add");
  assert.equal(binding.frozenAuthority.coreParentCommit, "52ee189e3dfaa2ea0924ed44cd2e1196b2ec3a5b");
  assert.equal(binding.frozenAuthority.handoffSha256, "2f1811e02b4fc6685dd543ae9844382f3bac077df58d9bae9395f49864a2c1ea");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "7b1230ec13b4ea894e19eef372a8816a947eda2af73262328aa7d62362f54a22");
  assert.equal(binding.claimBoundary.completeClock, true);
  assert.equal(binding.claimBoundary.signedFluxLowerBound, "C_STAR_BETA_TIMES_NINE_SEVENTHS_TO_FOUR_M");
  assert.equal(binding.claimBoundary.centralFibreProxy, true);
  assert.equal(binding.claimBoundary.modeDensity, "Q_OVER_L_SQUARED_TO_TWO_OVER_3969");
  assert.equal(binding.claimBoundary.normalizedRate, "LIMINF_GT_TWO_OVER_35721");
  assert.equal(binding.claimBoundary.exactShearEmbedding, "SMOOTH_UNFORCED_CONSTANT_PRESSURE_WITH_NONZERO_DRIFT");
  assert.equal(binding.claimBoundary.completeCollarFluxLowerBound, true);
  assert.equal(binding.claimBoundary.fullPhysicalPlateauLowerBound, false);
  assert.equal(binding.claimBoundary.r076eE24OrVersionMCounterexample, false);
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

test("R0.76G routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r076g"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r076g-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.76G Step 58", "COMPLETE-CLOCK CENTRAL-FIBRE FLUX LOWER BOUND", "163 节已公开", "NEXT · R0.76H", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.76G Step 58 的 bounded primary-source screen", "COMPLETE-CLOCK CENTRAL-FIBRE FLUX LOWER BOUND", "β(9/7)^(4m)", "NO FULL-PLATEAU LOWER BOUND", "开放接口 · R0.76H", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  assert.equal(home.includes('id="r076h"'), false);
  assert.equal(home.includes('href="/notes/r0-76h.html"'), false);
  assert.equal(literature.includes('href="/notes/r0-76h.html"'), false);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.37", html: 261, pdf: 218, published: 201, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.76G" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 163);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 35);
  assert.equal(inventory.latestPublishedRelease, "r076g");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r076g").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r076g"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r076g").length, 1);
  assert.equal(inventory.sameReleaseCompletedSteps.r076g, 58);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r076g");
  assert.equal(manifest.latestCompletedStep, 58);
  assert.equal(manifest.nextRelease, "r076h");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r076g-step58-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "17b366e477c46d11b4caa5e2026381bbf08e7d62");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "6f203611dc13b7343005bcab3a429b6c68b10add");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r076g_freeze_manifest.json"));
  assert.equal(freeze.scope, "COMPLETE_CLOCK_CENTRAL_FIBRE_SIGNED_FLUX_LOWER_BOUND");
  assert.equal(freeze.claim_status.complete_signed_flux, "LOWER_BOUND_PROVED_AGAINST_CENTRAL_FIBRE_PROXY");
  assert.equal(freeze.claim_status.flux_ratio_lower_bound, "C_STAR_BETA_TIMES_NINE_SEVENTHS_TO_FOUR_M");
  assert.equal(freeze.claim_status.full_plateau_lower_bound, "NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.publication_handoff.retained_recap_terminal_release, "R0.75W_STEP48");
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r076g-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 55/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.76G publishes no figure, full-plateau lower bound, arbitrary-packet theorem, or recap rewrite", () => {
  const note = read("public/notes/r0-76g.html");
  for (const marker of ["COMPLETE CLOCK", "SIGNED FLUX LOWER BOUND", "NONZERO DRIFT", "CENTRAL-FIBRE PROXY", "NO FULL-PLATEAU LOWER BOUND", "NO VERSION-M COUNTEREXAMPLE", "NO FIGURE / NO DNS", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r076g")), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
