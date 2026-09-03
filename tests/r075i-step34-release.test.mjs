import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const readBytes = (path) => readFileSync(resolve(root, path));
const read = (path) => readBytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(readBytes(path)).digest("hex");
const node = process.env.CODEX_NODE || process.execPath;

test("R0.75I Step 34 publishes the diffusion-safe block-participation boundary", () => {
  const note = read("public/notes/r0-75i.html");
  for (const marker of [
    "DIFFUSION-SAFE ONE BLOCK",
    "NO PDE USED",
    "N_EFF EXACT",
    "SUFFICIENT ONLY",
    "THETA &lt; 8558/35721",
    "BETA &gt; 27163/35721",
    "ONE-BLOCK RATE -4279/238140000",
    "UNIFORM RATE +27163/476280000",
    "HIGH PARTICIPATION NOT NECESSARY",
    "E.24 OPEN",
    "\\mathfrak X_j",
    "N_{\\rm eff}",
    "L^{2/3}\\omega^{1/3}R^{-2/3}",
    "\\frac{8558}{35721}",
    "\\frac{27163}{35721}",
    "-\\frac{4279}{238140000}",
    "\\frac{27163}{476280000}",
    "\\tag{I.27}",
    "83/83",
    "12/12",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 300_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75i.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  for (const later of ["r0-75j", "r0-75k"]) {
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".html")), false, later);
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".pdf")), false, later);
  }
});

test("R0.75I reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075i_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075i-step34-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75i.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75i.pdf"));
  assert.equal(binding.publicPdf.pageCount, 138);
  assert.equal(binding.frozenAuthority.sourceCommit, "066ebe8007518eae2d542a7a3729541677cedcd8");
  assert.equal(binding.frozenAuthority.handoffCommit, "25b06bb84190d2c29748881ac1af2bb56e929565");
  assert.equal(binding.frozenAuthority.handoffSha256, "0ce777ed11fc98e3aa87c6c8ae7decb8802312c354da934271474f6a4d0f8795");
  assert.equal(binding.frozenAuthority.independentHandoffAuditSha256, "fb018ed2684dc4b7ccc96565c36a0b34fa0da15aeb3724ff8942fd1d83188441");
  assert.equal(binding.frozenAuthority.frozenFileCount, 12);
  assert.equal(binding.claimBoundary.oneBlockEstimate, "PROVED_I10_I14_ARBITRARY_FIELD_NO_PDE_USED");
  assert.equal(binding.claimBoundary.diffusionSafeMeaning, "PDE_INDEPENDENT_ONE_BLOCK_ALGEBRA_ONLY");
  assert.equal(binding.claimBoundary.effectiveParticipationIdentity, "PROVED_I15_I17");
  assert.equal(binding.claimBoundary.effectiveParticipationBounds, "1_LE_N_EFF_LE_CARDINALITY");
  assert.equal(binding.claimBoundary.unequalFixture, "[1,8]_MAPS_TO_125_OVER_81");
  assert.equal(binding.claimBoundary.sufficientParticipationThreshold, "theta < 8558/35721");
  assert.equal(binding.claimBoundary.equivalentActiveFractionThreshold, "beta > 27163/35721");
  assert.equal(binding.claimBoundary.thresholdEndpointIncluded, false);
  assert.equal(binding.claimBoundary.favorableOneBlockRate, "-4279/238140000");
  assert.equal(binding.claimBoundary.adverseUniformBlockRate, "+27163/476280000");
  assert.equal(binding.claimBoundary.highParticipationZeroFluxDiagnostic, "PROVED_I27");
  assert.equal(binding.claimBoundary.participationConditionNecessary, false);
  assert.equal(binding.claimBoundary.participationCounterexampleToE24, false);
  assert.equal(binding.claimBoundary.actualDiffusingFieldParticipationBound, "OPEN");
  assert.equal(binding.claimBoundary.signedInterBlockCancellation, "OPEN");
  assert.equal(binding.claimBoundary.arbitraryRealE24, "OPEN");
  assert.equal(binding.claimBoundary.completeClock, "OPEN");
  assert.equal(binding.claimBoundary.fixedDeletion, "OPEN");
  assert.equal(binding.claimBoundary.suitableWeakTransfer, "OPEN");
  assert.equal(binding.claimBoundary.noveltyPriorityCorrectnessOrPublishabilityClaim, false);
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.formalFigure.required, false);
  assert.equal(binding.formalFigure.status, "NOT APPLICABLE");
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75i.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75i.pdf")), false);
});

test("R0.75I routes, accounting, manifests, repaired dependency ledger, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075i"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075i-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75I Step 34", "DIFFUSION-SAFE BLOCK PARTICIPATION", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75I Step 34 的 bounded primary-source screen", "I.10--I.14", "I.19--I.23", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);

  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.13", html: 237, pdf: 194, published: 177, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75I" });

  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 139);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 11);
  assert.equal(inventory.latestPublishedRelease, "r075i");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075i").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075i"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075i").length, 1);

  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075i");
  assert.equal(manifest.latestCompletedStep, 34);
  assert.equal(manifest.nextRelease, "r075j");
  assert.equal(manifest.latestReleaseGate, "tests/r075i-step34-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075i-step34-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075i-step34-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "066ebe8007518eae2d542a7a3729541677cedcd8");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "25b06bb84190d2c29748881ac1af2bb56e929565");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");

  const freeze = JSON.parse(read("research/r075i_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75I");
  assert.equal(freeze.source_commit, "066ebe8007518eae2d542a7a3729541677cedcd8");
  assert.equal(freeze.handoff_commit, "25b06bb84190d2c29748881ac1af2bb56e929565");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.one_block_diffusion_safe_estimate, "PROVED_I10_I14_NO_PDE_USED");
  assert.equal(freeze.claim_status.effective_participation_identity, "PROVED_I15_I17");
  assert.equal(freeze.claim_status.conditional_threshold, "THETA_STRICTLY_BELOW_8558_OVER_35721");
  assert.equal(freeze.claim_status.high_participation_zero_flux, "PROVED_I27_SUFFICIENT_NOT_NECESSARY");
  assert.equal(freeze.claim_status.actual_diffusing_field_participation_bound, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.arbitrary_real_E24, "OPEN");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");

  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075i-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 47/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
