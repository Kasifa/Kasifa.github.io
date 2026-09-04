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

test("R0.75V note and milestone recap PDFs are cryptographically bound", () => {
  const note = JSON.parse(read("research/r075v_pdf_bindings.json"));
  const recap = JSON.parse(read("research/r075v_recap_pdf_bindings.json"));
  for (const binding of [note, recap]) {
    assert.equal(binding.release, "R0.75V");
    assert.equal(binding.step, 47);
    assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
    assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
    assert.ok(binding.publicPdf.pageCount >= (binding === note ? 190 : 4));
    assert.equal(binding.frozenAuthority.sourceCommit, "fc676ef2c0bf501e14c6a0e1f84558e470de6eb8");
    assert.equal(binding.frozenAuthority.handoffCommit, "038abd31f55795198ed8bebd9ba96823337c1621");
    assert.equal(binding.frozenAuthority.coreParentCommit, "73bcc4cd928370a7355b88f953e96082c58ebf69");
    assert.equal(binding.claimBoundary.combinedSelfAndSumFrequencyBlock, "PROVED_V3");
    assert.equal(binding.claimBoundary.completeTwoHarmonicSignedFluxPayment, "PROVED_V4_EXACT_PAIR_ONLY");
    assert.equal(binding.claimBoundary.versionMSameVelocityInclusion, "CONDITIONAL_V43_SAME_AS_R075S_U");
    assert.equal(binding.claimBoundary.lowCarrierPair, "OPEN_NOT_PROVED");
    assert.equal(binding.claimBoundary.formalScientificFigure, false);
    assert.equal(binding.claimBoundary.clayClaim, false);
    assert.equal(binding.cumulativeRecap.updatedThrough, "R0.75V");
    assert.equal(binding.cumulativeRecap.nodeCount, 190);
  }
  assert.equal(note.schemaVersion, "r075v-step47-note-synchronized-pdf-binding-v1");
  assert.equal(recap.schemaVersion, "r075v-step47-cumulative-recap-synchronized-pdf-binding-v1");
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
});

test("R0.75V routes, accounting, manifests, recap, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  const recap = read("public/recap-r0-61-r0-75v.html");
  assert.equal((home.match(/id="r075v"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075v-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75V Step 47", "COUPLED SELF/SUM PAYMENT", "190 个节点", "/recap-r0-61-r0-75v.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75V Step 47 的 bounded primary-source screen", "EXACT HIGH-CARRIER PAIR ONLY", "V.13--V.17", "V.43", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  for (const marker of ["T · spatial coercivity", "U · difference-frequency payment", "V · coupled self/sum payment", "R0.61–R0.75V 全部节点"]) assert.ok(recap.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.26", html: 250, pdf: 207, published: 190, recap: 190, latestRecap: "R0.75V", latestRelease: "R0.75V" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 152);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 24);
  assert.equal(inventory.latestPublishedRelease, "r075v");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075v").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075v"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075v").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075v");
  assert.equal(manifest.latestCompletedStep, 47);
  assert.equal(manifest.nextRelease, "r075w");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075v-step47-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75v.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75v.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "fc676ef2c0bf501e14c6a0e1f84558e470de6eb8");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, true);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");
  const freeze = JSON.parse(read("research/r075v_freeze_manifest.json"));
  assert.equal(freeze.scope, "COMPLETE_EXACT_HIGH_CARRIER_TWO_HARMONIC_SIGNED_FLUX_PAYMENT");
  assert.equal(freeze.claim_status.combined_self_and_sum_frequency_block, "PROVED_V3");
  assert.equal(freeze.claim_status.complete_two_harmonic_signed_flux_payment, "PROVED_V4_EXACT_PAIR_ONLY");
  assert.equal(freeze.publication_handoff.recap_update_required, true);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075v-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 115/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75V keeps the exact-pair boundary and publishes no later or figure output", () => {
  const note = read("public/notes/r0-75v.html");
  for (const marker of ["SELF + SUM BLOCK PAID", "FULL EXACT-PAIR FLUX", "MULTIMODE OPEN", "VERSION-M CONDITIONAL", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075v")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75w.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75w.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075w")), false);
});
