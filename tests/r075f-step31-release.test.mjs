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

test("R0.75F Step 31 publishes the exact phase-identity and route-pruning boundary", () => {
  const note = read("public/notes/r0-75f.html");
  for (const marker of [
    "MODAL PRODUCT IDENTITY PROVED",
    "OFF-DIAGONAL LEDGER RECONSTRUCTED",
    "PHASE SUBSTITUTION TAUTOLOGICAL",
    "POSITIVITY-ONLY CONTROL FALSE",
    "NOT AN E.24 COUNTEREXAMPLE",
    "DYNAMIC ROUTES REMAIN VIABLE",
    "E.24 OPEN",
    "\\mathcal T_\\xi\n=\\mathcal E_{\\rm off}",
    "\\mathcal E_{\\rm off}",
    "\\mathcal A_{\\rm off}",
    "\\mathcal D_{\\rm off}",
    "\\mathcal E_{\\rm diag}+\\mathcal D_{\\rm diag}",
    "=\\mathcal A_{\\rm diag}.}",
    "\\frac{2N+N^{-1}}3\\longrightarrow\\infty",
    "19/9",
    "17/5",
    "33/7",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 300_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75f.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未读取、未公开"));
  for (const later of ["r0-75g", "r0-75h", "r0-75i", "r0-75j", "r0-75k"]) {
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".html")), false, later);
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".pdf")), false, later);
  }
});

test("R0.75F reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075f_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075f-step31-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75f.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75f.pdf"));
  assert.equal(binding.publicPdf.pageCount, 124);
  assert.equal(binding.frozenAuthority.sourceCommit, "be9a79a1d2b1fd2b7ee0e33f1f6e18f23b63958c");
  assert.equal(binding.frozenAuthority.handoffCommit, "97706831d95f82664c9693773c79e111a12fce35");
  assert.equal(binding.frozenAuthority.handoffSha256, "1c150c22663850a3b21f47e1df3e1606796aa1a8edabad362d619fa81acf4afc");
  assert.equal(binding.frozenAuthority.independentHandoffAuditSha256, "92c45d8fe449a846ec3f02d1d5bcbe2dfe9b9a27f3cb981c8cafb3761560751b");
  assert.equal(binding.frozenAuthority.frozenFileCount, 12);
  assert.equal(binding.claimBoundary.modalProductEquationStatus, "PROVED");
  assert.equal(binding.claimBoundary.offDiagonalPhaseIdentityStatus, "PROVED_EXACT_ZERO_RESIDUAL");
  assert.equal(binding.claimBoundary.directPhaseSubstitutionResult, "TAUTOLOGICAL_NO_NEW_BOUND");
  assert.equal(binding.claimBoundary.independentSignSmallFactorOrObservability, false);
  assert.equal(binding.claimBoundary.positivityOnlyDiagonalComparison, "REFUTED");
  assert.equal(binding.claimBoundary.frozenCollarCounterexample, false);
  assert.equal(binding.claimBoundary.arbitraryRealE24, "OPEN");
  assert.equal(binding.claimBoundary.enhancedDissipationResolventPathwiseUncertaintyPaymentSensitiveRoutes, "VIABLE_UNPROVED");
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
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75f.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75f.pdf")), false);
});

test("R0.75F routes, accounting, manifests, repaired dependency ledger, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075f"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075f-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75F Step 31", "MODAL PHASE-INTEGRATION NO-GO", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75F Step 31 的 bounded primary-source screen", "phase integration", "positivity-only", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);

  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.10", html: 234, pdf: 191, published: 174, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75F" });

  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 136);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 8);
  assert.equal(inventory.latestPublishedRelease, "r075f");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075f").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075f"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075f").length, 1);

  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075f");
  assert.equal(manifest.latestCompletedStep, 31);
  assert.equal(manifest.nextRelease, "r075g");
  assert.equal(manifest.latestReleaseGate, "tests/r075f-step31-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075f-step31-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075f-step31-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "be9a79a1d2b1fd2b7ee0e33f1f6e18f23b63958c");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "97706831d95f82664c9693773c79e111a12fce35");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");

  const freeze = JSON.parse(read("research/r075f_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75F");
  assert.equal(freeze.source_commit, "be9a79a1d2b1fd2b7ee0e33f1f6e18f23b63958c");
  assert.equal(freeze.handoff_commit, "97706831d95f82664c9693773c79e111a12fce35");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.modal_product_identity, "PROVED");
  assert.equal(freeze.claim_status.off_diagonal_phase_reconstruction, "PROVED_EXACT_ZERO_RESIDUAL");
  assert.equal(freeze.claim_status.direct_phase_substitution, "TAUTOLOGICAL_NO_NEW_BOUND");
  assert.equal(freeze.claim_status.positivity_only_diagonal_comparison, "REFUTED_BY_EXACT_REAL_FEJER_FAMILY");
  assert.equal(freeze.claim_status.frozen_collar_counterexample, "NOT_CONSTRUCTED");
  assert.equal(freeze.claim_status.arbitrary_real_E24, "OPEN");
  assert.equal(freeze.claim_status.dynamic_payment_sensitive_routes, "VIABLE_UNPROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");

  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075f-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 79/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
