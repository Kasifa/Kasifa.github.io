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

test("R0.75B Step 27 publishes the exact paid/open boundary", () => {
  const note = read("public/notes/r0-75b.html");
  for (const marker of [
    "SAFE SUBCLOCK PAID",
    "FULL ENDPOINT PAID",
    "OUTER DISSIPATION OPEN",
    "METHOD FAILURE ≠ COUNTEREXAMPLE",
    "full K / fixed deletion：OPEN",
    "-92837/476280000",
    "4279/238140000",
    "\\frac{27163}{476280000}",
    "\\frac{4279}{79380000}",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 250_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75b.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  for (const later of ["r0-75c", "r0-75d", "r0-75e", "/assets/r075b/"]) {
    assert.equal(note.includes(`href="/${later}`), false, later);
  }
  assert.ok(note.includes("R0.75C/D/E 与其他后续工作未读取、未公开"));
  for (const later of ["r0-75c", "r0-75d", "r0-75e"]) {
    assert.equal(existsSync(resolve(root, `public/notes/${later}.html`)), false, later);
    assert.equal(existsSync(resolve(root, `public/notes/${later}.pdf`)), false, later);
  }
});

test("R0.75B reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075b_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075b-step27-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75b.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75b.pdf"));
  assert.equal(binding.publicPdf.pageCount, 114);
  assert.equal(binding.claimBoundary.safeCompleteSubclockPaid, true);
  assert.equal(binding.claimBoundary.innerPaddingPaid, true);
  assert.equal(binding.claimBoundary.fullEndpointRowPaid, true);
  assert.equal(binding.claimBoundary.outerCollarAccumulatedDissipation, "OPEN");
  assert.equal(binding.claimBoundary.effectiveTemporalPacking, "OPEN");
  assert.equal(binding.claimBoundary.adverseFullWindowCoefficient, "METHOD FAILURE, NOT A COUNTEREXAMPLE");
  assert.equal(binding.claimBoundary.completeKControlled, false);
  assert.equal(binding.claimBoundary.fixedDeletionClosed, false);
  assert.equal(binding.claimBoundary.arbitrarySuitableWeakExtension, false);
  assert.equal(binding.claimBoundary.noveltyPriorityCorrectnessOrPublishabilityClaim, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.formalFigure.required, false);
  assert.equal(binding.formalFigure.status, "NOT APPLICABLE");
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75b.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75b.pdf")), false);
});

test("R0.75B routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075b"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075b-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75B Step 27", "OUTER PADDING GATE", "NEXT · R0.75C NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75B Step 27 的 bounded literature screen", "Caccioppoli", "method failure", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.06", html: 230, pdf: 187, published: 170, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75B" });

  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 132);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 4);
  assert.equal(inventory.latestPublishedRelease, "r075b");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075b").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075b"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075b").length, 1);

  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075b");
  assert.equal(manifest.latestCompletedStep, 27);
  assert.equal(manifest.nextRelease, "r075c");
  assert.equal(manifest.latestReleaseGate, "tests/r075b-step27-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075b-step27-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075b-step27-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");

  const freeze = JSON.parse(read("research/r075b_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75B");
  assert.equal(freeze.frozen_file_count, 10);
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.outer_accumulated_dissipation, "OPEN");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_10_OF_10");

  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075b-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 87/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
