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

test("R0.75W note and milestone recap PDFs are cryptographically bound", () => {
  const note = JSON.parse(read("research/r075w_pdf_bindings.json"));
  const recap = JSON.parse(read("research/r075w_recap_pdf_bindings.json"));
  for (const binding of [note, recap]) {
    assert.equal(binding.release, "R0.75W");
    assert.equal(binding.step, 48);
    assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
    assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
    assert.ok(binding.publicPdf.pageCount >= (binding === note ? 200 : 4));
    assert.equal(binding.frozenAuthority.sourceCommit, "e8e48a510db0c0ed86626c238e4c81c281bcc998");
    assert.equal(binding.frozenAuthority.handoffCommit, null);
    assert.equal(binding.frozenAuthority.coreParentCommit, "038abd31f55795198ed8bebd9ba96823337c1621");
    assert.equal(binding.claimBoundary.carrierPartition, "EXHAUSTIVE_W7_AND_W31");
    assert.equal(binding.claimBoundary.localEnergyIdentity, "PROVED_W24_W29_NO_DIVISION_BY_V_OR_GAP");
    assert.equal(binding.claimBoundary.completeTwoHarmonicSignedFluxPayment, "PROVED_W2_ALL_CARRIERS_EXACT_PAIR_ONLY");
    assert.equal(binding.claimBoundary.versionMSameVelocityInclusion, "CONDITIONAL_W33_REALIZED_SUBCLASS_AND_LEDGER_ALIGNMENT");
    assert.equal(binding.claimBoundary.threeOrMoreHarmonics, "OPEN_NOT_PROVED");
    assert.equal(binding.claimBoundary.formalScientificFigure, false);
    assert.equal(binding.claimBoundary.clayClaim, false);
    assert.equal(binding.cumulativeRecap.updatedThrough, "R0.75W");
    assert.equal(binding.cumulativeRecap.nodeCount, 191);
    assert.equal(binding.cumulativeRecap.previousR075VRecapPreserved, true);
  }
  assert.equal(note.schemaVersion, "r075w-step48-note-synchronized-pdf-binding-v1");
  assert.equal(recap.schemaVersion, "r075w-step48-cumulative-recap-synchronized-pdf-binding-v1");
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(sha("public/recap-r0-61-r0-75v.html"), "297c95300a2e983cce2ab201142f24297a70cc5eb9552cc3f2daee009025bee5");
  assert.equal(sha("public/recap-r0-61-r0-75v.pdf"), "bc0de2db711729bf1e202cff1b2f2d5cd1568ba5cd4f28f1bfb68b6ebc85e7eb");
});

test("R0.75W routes, accounting, manifests, recap, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  const recap = read("public/recap-r0-61-r0-75w.html");
  assert.equal((home.match(/id="r075w"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075w-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75W Step 48", "FULL-FREQUENCY EXACT PAIR", "191 个节点", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75W Step 48 的 bounded primary-source screen", "FULL-FREQUENCY EXACT DYADIC PAIR ONLY", "W.12--W.14", "W.33", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  for (const marker of ["T · high-carrier spatial coercivity", "U · high-carrier difference row", "V · high-carrier self/sum block", "W · low-carrier local energy", "R0.61–R0.75W 全部节点"]) assert.ok(recap.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.27", html: 251, pdf: 208, published: 191, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.75W" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 153);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 25);
  assert.equal(inventory.latestPublishedRelease, "r075w");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075w").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075w"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075w").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075w");
  assert.equal(manifest.latestCompletedStep, 48);
  assert.equal(manifest.nextRelease, "r075x");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075w-step48-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "e8e48a510db0c0ed86626c238e4c81c281bcc998");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, null);
  assert.equal(manifest.latestPublicationIdentity.recapRequired, true);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");
  const freeze = JSON.parse(read("research/r075w_freeze_manifest.json"));
  assert.equal(freeze.scope, "FULL_FREQUENCY_EXACT_DYADIC_TWO_HARMONIC_SIGNED_FLUX_PAYMENT");
  assert.equal(freeze.claim_status.carrier_partition, "EXHAUSTIVE_W7_AND_W31");
  assert.equal(freeze.claim_status.complete_two_harmonic_signed_flux_payment, "PROVED_W2_ALL_CARRIERS_EXACT_PAIR_ONLY");
  assert.equal(freeze.publication_handoff.recap_update_required, true);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075w-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 81/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75W keeps the exact-pair boundary and publishes no X or figure output", () => {
  const note = read("public/notes/r0-75w.html");
  for (const marker of ["LOW CARRIER PAID", "HIGH / LOW UNION", "FULL FREQUENCY", "3+ MODES OPEN", "VERSION-M CONDITIONAL", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075w")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75x.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75x.pdf")), false);
});
