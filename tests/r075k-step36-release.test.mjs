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

test("R0.75K Step 36 publishes the fixed-positive-majorant high-frequency trace-loss boundary", () => {
  const note = read("public/notes/r0-75k.html");
  for (const marker of [
    "SMOOTH PASSIVE FAMILY",
    "POSITIVE MAJORANT",
    "ENTRANCE MASS POSITIVE",
    "TRACE ROW FIXED",
    "CUBIC MASS k^-2",
    "RATIO k^4/3",
    "SIGNED FLUX ZERO",
    "PROOF LOSS",
    "FIXED WEIGHT ONLY",
    "E.24 OPEN",
    "\\mathcal L^*\\Phi=q",
    "\\boxed{\\mathcal L F_k=0.}",
    "B_k:=\\frac12",
    "\\boxed{\\mathcal T_k=0.}",
    "\\tag{K.18}",
    "100/100",
    "12/12",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 300_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75k.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  for (const later of ["r0-75l"]) {
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".html")), false, later);
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".pdf")), false, later);
  }
});

test("R0.75K reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075k_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075k-step36-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75k.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75k.pdf"));
  assert.equal(binding.publicPdf.pageCount, 147);
  assert.equal(binding.frozenAuthority.sourceCommit, "69f3989c46f0ff09c8a20cb0c387625beae42d45");
  assert.equal(binding.frozenAuthority.handoffCommit, "b6a41917fa2b30051f7c8550d313326da128d3b9");
  assert.equal(binding.frozenAuthority.handoffSha256, "07a0b2db03bfcf9f31f418af820f805d8a10abf2f70d06a91a5628c68618e71b");
  assert.equal(binding.frozenAuthority.independentHandoffAuditSha256, "58d998edf141ea38672643bc97b1fb171c7512acf7d835da5ef8ca03bd042b04");
  assert.equal(binding.frozenAuthority.frozenFileCount, 12);
  assert.equal(binding.claimBoundary.positiveMajorant, "SMOOTH_NONNEGATIVE_ADMISSIBLE_K4_K7");
  assert.equal(binding.claimBoundary.exactPassiveFamily, "PROVED_K8_K10");
  assert.equal(binding.claimBoundary.positiveEntranceRow, "FREQUENCY_INDEPENDENT_K11");
  assert.equal(binding.claimBoundary.localSpacetimeCubicMass, "EXACT_K12_DECAYS_K_MINUS_2");
  assert.equal(binding.claimBoundary.traceToCubicRatio, "DIVERGES_K_TO_THE_4_OVER_3_K13_K14");
  assert.equal(binding.claimBoundary.physicalSignedFlux, "EXACTLY_ZERO_K15_K16");
  assert.equal(binding.claimBoundary.generalFixedWeight, "RIEMANN_LEBESGUE_K17");
  assert.equal(binding.claimBoundary.limitedNoGo, "FIXED_POSITIVE_WEIGHT_PLUS_LOCAL_CUBIC_ALONE_K18");
  assert.equal(binding.claimBoundary.e24Counterexample, false);
  assert.equal(binding.claimBoundary.signedOrFrequencyAwareRepair, "OPEN_NOT_RULED_OUT");
  assert.equal(binding.claimBoundary.fullVersionMTraceFrequencyPayment, "OPEN_NOT_RULED_OUT");
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
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75k.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75k.pdf")), false);
});

test("R0.75K routes, accounting, manifests, repaired dependency ledger, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075k"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075k-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75K Step 36", "HIGH-FREQUENCY TRACE LOSS", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75K Step 36 的 bounded primary-source screen", "K.12--K.14", "K.15--K.16", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);

  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.15", html: 239, pdf: 196, published: 179, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75K" });

  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 141);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 13);
  assert.equal(inventory.latestPublishedRelease, "r075k");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075k").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075k"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075k").length, 1);

  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075k");
  assert.equal(manifest.latestCompletedStep, 36);
  assert.equal(manifest.nextRelease, "r075l");
  assert.equal(manifest.latestReleaseGate, "tests/r075k-step36-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075k-step36-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075k-step36-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "69f3989c46f0ff09c8a20cb0c387625beae42d45");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "b6a41917fa2b30051f7c8550d313326da128d3b9");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");

  const freeze = JSON.parse(read("research/r075k_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75K");
  assert.equal(freeze.source_commit, "69f3989c46f0ff09c8a20cb0c387625beae42d45");
  assert.equal(freeze.handoff_commit, "b6a41917fa2b30051f7c8550d313326da128d3b9");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.positive_majorant, "SMOOTH_NONNEGATIVE_ADMISSIBLE_K4_K7");
  assert.equal(freeze.claim_status.exact_passive_family, "PROVED_K8_K10");
  assert.equal(freeze.claim_status.trace_to_cubic_ratio, "DIVERGES_K_TO_THE_4_OVER_3_K13_K14");
  assert.equal(freeze.claim_status.physical_signed_flux, "EXACTLY_ZERO_K15_K16");
  assert.equal(freeze.claim_status.limited_no_go, "FIXED_POSITIVE_ENTRANCE_WEIGHT_PLUS_LOCAL_CUBIC_ATOM_ALONE_K18");
  assert.equal(freeze.claim_status.arbitrary_real_E24, "OPEN");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");

  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075k-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 47/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
