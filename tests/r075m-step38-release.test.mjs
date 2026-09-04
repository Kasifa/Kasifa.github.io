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

test("R0.75M reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075m_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075m-step38-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75m.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75m.pdf"));
  assert.equal(binding.publicPdf.pageCount, 154);
  assert.equal(binding.frozenAuthority.sourceCommit, "decc558786108fd1ce4a7f86d906d12c4eb61a25");
  assert.equal(binding.frozenAuthority.handoffCommit, "138b2081c18bdd4409b354bfe2aeea86db6ce185");
  assert.equal(binding.frozenAuthority.handoffSha256, "89f814a6c52ce6c4d2a52eedff9042eaaff00fb9fbe44028d398679da6f12d85");
  assert.equal(binding.frozenAuthority.independentHandoffAuditSha256, "fd8ba9ebb88a478d091c7a8535386c920a0f8964b7c91b4f4317488770633589");
  assert.equal(binding.claimBoundary.schurWienerEnergyBound, "K_MINUS_2_M8_M11_NO_MODE_COUNT");
  assert.equal(binding.claimBoundary.diffusivePaymentGain, "K_MINUS_2_OVER_3_M2_M16");
  assert.equal(binding.claimBoundary.packetCardinalityLoss, "NONE_EXPLICIT");
  assert.equal(binding.claimBoundary.interPacketSummation, "OPEN");
  assert.equal(binding.claimBoundary.frozenCollarWienerCalibration, "OPEN");
  assert.equal(binding.claimBoundary.e24, "OPEN");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75m.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75m.pdf")), false);
});

test("R0.75M routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075m"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075m-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75M Step 38", "DYADIC-PACKET DIFFUSIVE GAIN", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75M Step 38 的 bounded primary-source screen", "M.8--M.11", "M.18--M.20", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.17", html: 241, pdf: 198, published: 181, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75M" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 143);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 15);
  assert.equal(inventory.latestPublishedRelease, "r075m");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075m").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075m"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075m").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075m");
  assert.equal(manifest.latestCompletedStep, 38);
  assert.equal(manifest.nextRelease, "r075n");
  assert.equal(manifest.latestReleaseGate, "tests/r075m-step38-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075m-step38-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075m-step38-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "decc558786108fd1ce4a7f86d906d12c4eb61a25");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "138b2081c18bdd4409b354bfe2aeea86db6ce185");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");
  const freeze = JSON.parse(read("research/r075m_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75M");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.packet_cardinality_loss, "NONE_EXPLICIT");
  assert.equal(freeze.claim_status.inter_packet_summation, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.E24, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r075m-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 47/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.75M keeps exclusions explicit and does not publish future or figure output", () => {
  const note = read("public/notes/r0-75m.html");
  for (const marker of ["ONE PACKET ONLY", "COLLAR CALIBRATION OPEN", "E.24 OPEN", "NO FIGURE / NO DNS", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r075m")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75n.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75n.pdf")), false);
});
