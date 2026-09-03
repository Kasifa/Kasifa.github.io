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

test("R0.75D Step 29 publishes the exact proved/conditional/open boundary", () => {
  const note = read("public/notes/r0-75d.html");
  for (const marker of [
    "PASSIVE FALLBACK PROVED",
    "SMALL-PAYMENT PAID",
    "LOW FREQUENCY CONDITIONAL",
    "LARGE-PAYMENT OPEN",
    "INTERACTION GATE OPEN",
    "NO COUNTEREXAMPLE",
    "\\frac{147163}{476280000}",
    "\\frac{27163}{158760000}",
    "D_{k,R}^{{\\rm out},F}",
    "C L^{2/3}\\omega^{1/3}(P_R^M)^{2/3}+C P_R^M",
    "p_b p_F^2\\le C(P_R^M)^2",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 250_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75d.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("R0.75E/F/G/H 与其他后续工作未读取、未公开"));
  for (const later of ["r0-75e", "r0-75f", "r0-75g", "r0-75h"]) {
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".html")), false, later);
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".pdf")), false, later);
  }
});

test("R0.75D reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075d_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075d-step29-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75d.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75d.pdf"));
  assert.equal(binding.publicPdf.pageCount, 118);
  assert.equal(binding.frozenAuthority.sourceCommit, "1e010e638569f14f74fea6c1db89e08c1f63d622");
  assert.equal(binding.frozenAuthority.frozenFileCount, 10);
  assert.equal(binding.claimBoundary.unconditionalPassiveFallbackStatus, "PROVED");
  assert.equal(binding.claimBoundary.smallPaymentStatus, "PROVED");
  assert.equal(binding.claimBoundary.lowFrequencyPayment, "CONDITIONAL");
  assert.equal(binding.claimBoundary.lowFrequencyLogarithmicRate, "147163/476280000");
  assert.equal(binding.claimBoundary.horizontalFrequencyAloneSufficient, false);
  assert.equal(binding.claimBoundary.frozenCommonShearPaymentRegime, "LARGE");
  assert.equal(binding.claimBoundary.frozenBackgroundLogarithmicRate, "27163/158760000");
  assert.equal(binding.claimBoundary.interactionGate, "p_b p_F^2 <= C(P_R^M)^2");
  assert.equal(binding.claimBoundary.interactionGateStatus, "OPEN");
  assert.equal(binding.claimBoundary.directOuterDissipationB45, "OPEN");
  assert.equal(binding.claimBoundary.completeClock, "OPEN");
  assert.equal(binding.claimBoundary.exactCounterexample, false);
  assert.equal(binding.claimBoundary.noveltyPriorityCorrectnessOrPublishabilityClaim, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.formalFigure.required, false);
  assert.equal(binding.formalFigure.status, "NOT APPLICABLE");
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75d.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75d.pdf")), false);
});

test("R0.75D routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075d"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075d-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75D Step 29", "PASSIVE GRADIENT ROUTE", "NEXT · R0.75E", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75D Step 29 的 bounded primary-source screen", "small-payment closure", "interaction", "complete clock", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);

  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.08", html: 232, pdf: 189, published: 172, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75D" });

  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 134);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 6);
  assert.equal(inventory.latestPublishedRelease, "r075d");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075d").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075d"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075d").length, 1);

  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075d");
  assert.equal(manifest.latestCompletedStep, 29);
  assert.equal(manifest.nextRelease, "r075e");
  assert.equal(manifest.latestReleaseGate, "tests/r075d-step29-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075d-step29-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075d-step29-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "1e010e638569f14f74fea6c1db89e08c1f63d622");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");

  const freeze = JSON.parse(read("research/r075d_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75D");
  assert.equal(freeze.frozen_file_count, 10);
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.passive_caccioppoli_fallback, "PROVED_P_TWO_THIRDS_PLUS_P");
  assert.equal(freeze.claim_status.small_payment_passive_outer_dissipation, "PAID");
  assert.equal(freeze.claim_status.low_full_spatial_frequency, "PAID_CONDITIONALLY");
  assert.equal(freeze.claim_status.frozen_common_shear_branch, "LARGE_PAYMENT_NOT_CLOSED");
  assert.equal(freeze.claim_status.interaction_gate, "OPEN");
  assert.equal(freeze.claim_status.exact_counterexample, "NOT_CONSTRUCTED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_10_OF_10");

  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075d-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 74/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
