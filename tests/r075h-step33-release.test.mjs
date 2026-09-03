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

test("R0.75H Step 33 publishes the pure-transport terminal-tube boundary", () => {
  const note = read("public/notes/r0-75h.html");
  for (const marker of [
    "PURE TRANSPORT PROVED",
    "SIGNED POSITIVE PART",
    "TERMINAL TUBE",
    "FIXED LIFT / NO SEAM",
    "R^(1/3) BENCHMARK GAIN",
    "RATE -4279/238140000",
    "DIFFUSIVE EXTENSION OPEN",
    "E.24 OPEN",
    "NOT AN NSE SOLUTION FUNCTIONAL",
    "\\mathfrak X_{\\xi,R}^{\\rm tr}",
    "[\\mathcal T_{\\xi,\\eta}^{\\rm tr}]_+",
    "L^{2/3}\\omega^{1/3}R^{-2/3}",
    "-\\frac{4279}{238140000}",
    "\\tag{H.28}",
    "66/66",
    "12/12",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 300_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75h.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  for (const later of ["r0-75i", "r0-75j", "r0-75k"]) {
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".html")), false, later);
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".pdf")), false, later);
  }
});

test("R0.75H reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075h_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075h-step33-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75h.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75h.pdf"));
  assert.equal(binding.publicPdf.pageCount, 133);
  assert.equal(binding.frozenAuthority.sourceCommit, "41e138f1770bbc3f06a69ba67fa7d1ec59c1c397");
  assert.equal(binding.frozenAuthority.handoffCommit, "07b03ea63d05e8de4d20d2ea489d3373cb6251a5");
  assert.equal(binding.frozenAuthority.handoffSha256, "008b1f64f566165dc0fcf5fc3f2978c6e6519ae1d2285392cd8fc3dd4b1eb1ec");
  assert.equal(binding.frozenAuthority.independentHandoffAuditSha256, "fb9785d8d282ba09bfa6a5de5f349ecd7a7c37b08060ad155f074eb3474376c9");
  assert.equal(binding.frozenAuthority.frozenFileCount, 12);
  assert.equal(binding.claimBoundary.signedFluxEndpointIdentity, "PROVED_H13");
  assert.equal(binding.claimBoundary.positiveSignedFluxBound, "PROVED_H14_BY_HALF_TERMINAL_ENERGY");
  assert.equal(binding.claimBoundary.terminalTubePersistence, "PROVED_H16_H19_FIXED_LIFT_NO_SEAM");
  assert.equal(binding.claimBoundary.terminalTubeCubicEstimate, "PROVED_H23");
  assert.equal(binding.claimBoundary.benchmarkGainRate, "-4279/238140000");
  assert.equal(binding.claimBoundary.benchmarkVersionMStatus, "FORMULA_EVALUATED_ON_PURE_TRANSPORT_NOT_NSE_SOLUTION");
  assert.equal(binding.claimBoundary.absoluteFluxClaim, false);
  assert.equal(binding.claimBoundary.multipleWindingsCovered, false);
  assert.equal(binding.claimBoundary.characteristicPersistenceWithDiffusion, false);
  assert.equal(binding.claimBoundary.diffusiveIdentityH28, "EXACT_BUT_CIRCULAR_FOR_TARGET_DISSIPATION");
  assert.equal(binding.claimBoundary.diffusiveTerminalTubeEstimate, "OPEN");
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
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75h.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75h.pdf")), false);
});

test("R0.75H routes, accounting, manifests, repaired dependency ledger, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075h"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075h-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75H Step 33", "PURE-TRANSPORT TERMINAL-TUBE CLOSURE", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75H Step 33 的 bounded primary-source screen", "H.13--H.14", "H.23", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);

  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.12", html: 236, pdf: 193, published: 176, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75H" });

  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 138);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 10);
  assert.equal(inventory.latestPublishedRelease, "r075h");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075h").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075h"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075h").length, 1);

  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075h");
  assert.equal(manifest.latestCompletedStep, 33);
  assert.equal(manifest.nextRelease, "r075i");
  assert.equal(manifest.latestReleaseGate, "tests/r075h-step33-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075h-step33-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075h-step33-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "41e138f1770bbc3f06a69ba67fa7d1ec59c1c397");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "07b03ea63d05e8de4d20d2ea489d3373cb6251a5");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");

  const freeze = JSON.parse(read("research/r075h_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75H");
  assert.equal(freeze.source_commit, "41e138f1770bbc3f06a69ba67fa7d1ec59c1c397");
  assert.equal(freeze.handoff_commit, "07b03ea63d05e8de4d20d2ea489d3373cb6251a5");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.pure_transport_signed_identity, "PROVED_H13_H14");
  assert.equal(freeze.claim_status.terminal_tube_persistence, "PROVED_H16_H19_FIXED_LIFT_NO_SEAM");
  assert.equal(freeze.claim_status.terminal_tube_cubic_payment, "PROVED_H23");
  assert.equal(freeze.claim_status.alpha_one_third_benchmark_gain, "PROVED_STRICT_NEGATIVE_RATE");
  assert.equal(freeze.claim_status.diffusive_identity_H28, "EXACT_BUT_CIRCULAR_FOR_TARGET_DISSIPATION");
  assert.equal(freeze.claim_status.arbitrary_real_E24, "OPEN");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");

  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075h-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 46/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
