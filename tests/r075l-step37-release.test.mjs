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

test("R0.75L Step 37 publishes the one-harmonic diffusive signed-flux gain boundary", () => {
  const note = read("public/notes/r0-75l.html");
  for (const marker of [
    "EXACT PASSIVE HARMONIC",
    "PHYSICAL SIGNED FLUX",
    "ZERO MODE CANCELED",
    "ONLY +/-2k",
    "FLUX k^-2",
    "CUBIC MASS k^-2",
    "GAIN k^-2/3",
    "FULL-TORUS ATOM",
    "SINGLE HARMONIC ONLY",
    "|B|V_XI UNPAID",
    "E.24 OPEN",
    "\\boxed{\\mathcal L_BF_k=0.}",
    "\\tag{L.9}",
    "\\tag{L.15}",
    "\\tag{L.17}",
    "120/120",
    "12/12",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 300_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75l.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  assert.equal(existsSync(resolve(root, "public/notes/r0-75m.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75m.pdf")), false);
  assert.equal(existsSync(resolve(root, "public/assets/r075l")), false);
});

test("R0.75L reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075l_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075l-step37-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75l.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75l.pdf"));
  assert.equal(binding.publicPdf.pageCount, 150);
  assert.equal(binding.frozenAuthority.sourceCommit, "8eef1888735a7e08bd0e9c988e01677a197f437a");
  assert.equal(binding.frozenAuthority.handoffCommit, "cd65721cf2b8d33d4cd97edab92c87daa1daf068");
  assert.equal(binding.frozenAuthority.handoffSha256, "caafa97240fcdf52cf8fd58d120d291a13933c89d8adcb79dde655c8f76b273e");
  assert.equal(binding.frozenAuthority.independentHandoffAuditSha256, "e08bc86dc42014057520fb5ce97e6bd81a16a93d739fd887ec71308e27aaf4c9");
  assert.equal(binding.frozenAuthority.frozenFileCount, 12);
  assert.equal(binding.claimBoundary.exactPassiveFamily, "PROVED_L2_L5");
  assert.equal(binding.claimBoundary.physicalSignedFlux, "DIAGONAL_ZERO_MODE_CANCELED_L6_L8");
  assert.equal(binding.claimBoundary.survivingFrequencies, "PLUS_MINUS_2K");
  assert.equal(binding.claimBoundary.exactFluxBound, "K_MINUS_2_L9");
  assert.equal(binding.claimBoundary.fullTorusCubicMass, "EXACT_L10");
  assert.equal(binding.claimBoundary.diffusivePaymentGain, "K_MINUS_2_OVER_3_L1_L10_L13");
  assert.equal(binding.claimBoundary.targetNormalization, "PROVED_L14_L15");
  assert.equal(binding.claimBoundary.frequencyThreshold, "CONDITIONAL_KAPPA_GT_27163_OVER_71442_L16_L17");
  assert.equal(binding.claimBoundary.backgroundCoefficientPayment, "B_TIMES_VARIATION_UNPAID");
  assert.equal(binding.claimBoundary.multimodeConvolution, "OPEN");
  assert.equal(binding.claimBoundary.frozenCollarLocalization, "OPEN");
  assert.equal(binding.claimBoundary.nonconstantShear, "OPEN");
  assert.equal(binding.claimBoundary.lowDifferenceFrequencySector, "OPEN");
  assert.equal(binding.claimBoundary.e24, "OPEN");
  assert.equal(binding.claimBoundary.noveltyPriorityCorrectnessOrPublishabilityClaim, false);
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.formalFigure.required, false);
  assert.equal(binding.formalFigure.status, "NOT APPLICABLE");
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75l.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75l.pdf")), false);
});

test("R0.75L routes, accounting, manifests, dependency ledger, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075l"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075l-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75L Step 37", "DIFFUSIVE SIGNED-FLUX GAIN", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75L Step 37 的 bounded primary-source screen", "L.10--L.13", "L.16--L.17", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);

  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.16", html: 240, pdf: 197, published: 180, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75L" });

  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 142);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 14);
  assert.equal(inventory.latestPublishedRelease, "r075l");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075l").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075l"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075l").length, 1);

  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075l");
  assert.equal(manifest.latestCompletedStep, 37);
  assert.equal(manifest.nextRelease, "r075m");
  assert.equal(manifest.latestReleaseGate, "tests/r075l-step37-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075l-step37-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075l-step37-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "8eef1888735a7e08bd0e9c988e01677a197f437a");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "cd65721cf2b8d33d4cd97edab92c87daa1daf068");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");

  const freeze = JSON.parse(read("research/r075l_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75L");
  assert.equal(freeze.source_commit, "8eef1888735a7e08bd0e9c988e01677a197f437a");
  assert.equal(freeze.handoff_commit, "cd65721cf2b8d33d4cd97edab92c87daa1daf068");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.exact_passive_family, "PROVED_L2_L5");
  assert.equal(freeze.claim_status.diffusive_payment_gain, "K_MINUS_2_OVER_3_L1_L10_L13");
  assert.equal(freeze.claim_status.frequency_threshold, "CONDITIONAL_KAPPA_GT_27163_OVER_71442_L16_L17");
  assert.equal(freeze.claim_status.multimode_convolution, "OPEN_NOT_PROVED");
  assert.equal(freeze.claim_status.E24, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");

  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075l-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 47/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
