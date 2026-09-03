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

test("R0.75J Step 35 publishes the mean-zero adjoint obstruction boundary", () => {
  const note = read("public/notes/r0-75j.html");
  for (const marker of [
    "MEAN-ZERO SOURCE",
    "EXACT ADJOINT SIGN-CHANGING",
    "DUALITY EXACT",
    "NEGATIVE WEIGHTED DISSIPATION",
    "CONSTANT SHIFT CANCELED",
    "SURCHARGE CD",
    "POSITIVE MAJORANT VIABLE",
    "INITIAL ROW UNPAID",
    "NOT BLANKET NO-GO",
    "E.24 OPEN",
    "\\mathcal L^*\\psi=a",
    "\\psi\\text{ changes sign.}",
    "\\int\\psi_-|\\nabla_{23}F|^2",
    "\\frac C2\\bigl(E(s)-E(t_2)\\bigr)-CD=0",
    "a\\le\\mathcal L^*\\Phi",
    "\\tag{J.20}",
    "84/84",
    "12/12",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 300_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75j.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  for (const later of ["r0-75k"]) {
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".html")), false, later);
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".pdf")), false, later);
  }
});

test("R0.75J reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075j_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075j-step35-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75j.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75j.pdf"));
  assert.equal(binding.publicPdf.pageCount, 143);
  assert.equal(binding.frozenAuthority.sourceCommit, "6c81786ea2977234de1ebb3286334d418fa0090b");
  assert.equal(binding.frozenAuthority.handoffCommit, "af29a609b21714ad9360d511351e8388f7038ec4");
  assert.equal(binding.frozenAuthority.handoffSha256, "29a8bb1ea736e7e0d1d18d6b775aed08276da5563a2b1143dab56624723caae2");
  assert.equal(binding.frozenAuthority.independentHandoffAuditSha256, "1056af95444eab42b416f7dd1a64c94476e6a92b9ed7054c49f9917f20da270b");
  assert.equal(binding.frozenAuthority.frozenFileCount, 12);
  assert.equal(binding.claimBoundary.sourceMeanZero, "PROVED_J7_EVERY_FIXED_T_X1");
  assert.equal(binding.claimBoundary.exactZeroTerminalAdjointMeanZero, "PROVED_J8_J9");
  assert.equal(binding.claimBoundary.exactAdjointSignChange, "FORCED_UNLESS_SOURCE_IDENTICALLY_ZERO_J4");
  assert.equal(binding.claimBoundary.exactDuality, "PROVED_J5_J12");
  assert.equal(binding.claimBoundary.negativeAdjointDissipation, "UNFAVORABLE_POSITIVE_ROW_J13_UNPAID");
  assert.equal(binding.claimBoundary.constantPositiveShift, "EXACTLY_CANCELED_J16_J17");
  assert.equal(binding.claimBoundary.droppedDissipationSurcharge, "CD_GLOBAL_ENERGY_DROP_J18");
  assert.equal(binding.claimBoundary.positiveMajorantDirection, "a<=LstarPhi_J19");
  assert.equal(binding.claimBoundary.positiveMajorantInitialRow, "OPEN_UNPAID_BY_VERSION_M");
  assert.equal(binding.claimBoundary.positivePartReplacementPreservesSignedSource, false);
  assert.equal(binding.claimBoundary.blanketNoGoForAdjointResolventOrFeynmanKac, false);
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
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75j.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75j.pdf")), false);
});

test("R0.75J routes, accounting, manifests, repaired dependency ledger, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075j"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075j-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75J Step 35", "MEAN-ZERO ADJOINT OBSTRUCTION", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75J Step 35 的 bounded primary-source screen", "J.8--J.9", "J.19--J.20", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);

  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.14", html: 238, pdf: 195, published: 178, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75J" });

  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 140);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 12);
  assert.equal(inventory.latestPublishedRelease, "r075j");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075j").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075j"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075j").length, 1);

  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075j");
  assert.equal(manifest.latestCompletedStep, 35);
  assert.equal(manifest.nextRelease, "r075k");
  assert.equal(manifest.latestReleaseGate, "tests/r075j-step35-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075j-step35-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075j-step35-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "6c81786ea2977234de1ebb3286334d418fa0090b");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "af29a609b21714ad9360d511351e8388f7038ec4");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");

  const freeze = JSON.parse(read("research/r075j_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75J");
  assert.equal(freeze.source_commit, "6c81786ea2977234de1ebb3286334d418fa0090b");
  assert.equal(freeze.handoff_commit, "af29a609b21714ad9360d511351e8388f7038ec4");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.physical_signed_source_mean_zero, "PROVED_J7_EVERY_FIXED_PARAMETER_SLICE");
  assert.equal(freeze.claim_status.exact_zero_terminal_adjoint, "FORCED_SIGN_CHANGE_UNLESS_SOURCE_ZERO_J8_J9");
  assert.equal(freeze.claim_status.constant_shift, "EXACTLY_CANCELED_J14_J17");
  assert.equal(freeze.claim_status.dropped_dissipation_surcharge, "EXACTLY_CD_J18_GLOBAL_ENERGY_DROP");
  assert.equal(freeze.claim_status.positive_majorant_initial_row, "OPEN_NOT_PAID");
  assert.equal(freeze.claim_status.arbitrary_real_E24, "OPEN");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");

  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075j-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 45/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
