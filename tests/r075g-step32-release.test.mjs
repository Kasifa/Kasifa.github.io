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

test("R0.75G Step 32 publishes the exact signed-flux gain threshold boundary", () => {
  const note = read("public/notes/r0-75g.html");
  for (const marker of [
    "EXACT THRESHOLD PROVED",
    "ALPHA STAR 27163/107163",
    "STRICT INEQUALITY REQUIRED",
    "ONE THIRD CONDITIONALLY SUFFICIENT",
    "ONE QUARTER INSUFFICIENT BY THIS ROUTE",
    "AMPLITUDE GAIN IMPOSSIBLE",
    "RESIDENCE BETA STAR 27163/35721",
    "POSITIVE GAIN OPEN",
    "E.24 OPEN",
    "\\frac{27163}{107163}",
    "\\frac{27163}{35721}",
    "-\\frac{4279}{238140000}",
    "\\frac{1489}{1905120000}",
    "\\tag{G.24}",
    "57/57",
    "12/12",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 300_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75g.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("后续工作未授权、未读取、未公开"));
  for (const later of ["r0-75h", "r0-75i", "r0-75j", "r0-75k"]) {
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".html")), false, later);
    assert.equal(existsSync(resolve(root, "public/notes/" + later + ".pdf")), false, later);
  }
});

test("R0.75G reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075g_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075g-step32-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75g.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75g.pdf"));
  assert.equal(binding.publicPdf.pageCount, 128);
  assert.equal(binding.frozenAuthority.sourceCommit, "b4ec164eeae4ec79be3c517da98321b62294d991");
  assert.equal(binding.frozenAuthority.handoffCommit, "8ddccdefa292d0768f8594995553af4853923833");
  assert.equal(binding.frozenAuthority.handoffSha256, "628dbe1a1e0d53d87bcf782edba1425b130269722ecded882207549c232c9d1c");
  assert.equal(binding.frozenAuthority.independentHandoffAuditSha256, "4bf12a10837ea83b6e37f8f0413bdd31bedbd498cbd02da4e6008a7de4b066f7");
  assert.equal(binding.frozenAuthority.frozenFileCount, 12);
  assert.equal(binding.claimBoundary.conditionalGainEstimateStatus, "ASSUMED_NOT_PROVED");
  assert.equal(binding.claimBoundary.alphaStar, "27163/107163");
  assert.equal(binding.claimBoundary.alphaStrictThreshold, "alpha > alphaStar");
  assert.equal(binding.claimBoundary.alphaOneThirdRate, "-4279/238140000");
  assert.equal(binding.claimBoundary.alphaOneThirdStatus, "CONDITIONALLY_SUFFICIENT");
  assert.equal(binding.claimBoundary.alphaOneQuarterRate, "1489/1905120000");
  assert.equal(binding.claimBoundary.alphaOneQuarterStatus, "INSUFFICIENT_FOR_THIS_REDUCTION_NOT_COUNTEREXAMPLE");
  assert.equal(binding.claimBoundary.interactionBetaStar, "27163/35721");
  assert.equal(binding.claimBoundary.amplitudeScalingCreatesGain, false);
  assert.equal(binding.claimBoundary.monotoneCrossingStatus, "KINEMATIC_BENCHMARK_ONLY");
  assert.equal(binding.claimBoundary.pureTransportFluxAndEndpointHalfEnergy, "1/32");
  assert.equal(binding.claimBoundary.positiveGainG1, "OPEN");
  assert.equal(binding.claimBoundary.interactionAtomG18, "OPEN");
  assert.equal(binding.claimBoundary.minimumTargetG24, "OPEN");
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
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75g.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75g.pdf")), false);
});

test("R0.75G routes, accounting, manifests, repaired dependency ledger, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075g"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075g-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75G Step 32", "EXACT SIGNED-FLUX GAIN THRESHOLD", "NEXT · NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75G Step 32 的 bounded primary-source screen", "27163/107163", "27163/35721", "E.24", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);

  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.11", html: 235, pdf: 192, published: 175, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75G" });

  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 137);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 9);
  assert.equal(inventory.latestPublishedRelease, "r075g");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075g").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075g"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075g").length, 1);

  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075g");
  assert.equal(manifest.latestCompletedStep, 32);
  assert.equal(manifest.nextRelease, "r075h");
  assert.equal(manifest.latestReleaseGate, "tests/r075g-step32-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075g-step32-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075g-step32-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "b4ec164eeae4ec79be3c517da98321b62294d991");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "8ddccdefa292d0768f8594995553af4853923833");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");

  const freeze = JSON.parse(read("research/r075g_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75G");
  assert.equal(freeze.source_commit, "b4ec164eeae4ec79be3c517da98321b62294d991");
  assert.equal(freeze.handoff_commit, "8ddccdefa292d0768f8594995553af4853923833");
  assert.equal(freeze.frozen_file_count, 12);
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.conditional_alpha_threshold, "PROVED_STRICT_ALPHA_GT_27163_OVER_107163");
  assert.equal(freeze.claim_status.alpha_one_third, "CONDITIONALLY_SUFFICIENT_STRICT_NEGATIVE_MARGIN");
  assert.equal(freeze.claim_status.alpha_one_quarter, "INSUFFICIENT_FOR_THIS_REDUCTION_NOT_COUNTEREXAMPLE");
  assert.equal(freeze.claim_status.amplitude_scaling_gain, "IMPOSSIBLE_BY_HOMOGENEITY");
  assert.equal(freeze.claim_status.interaction_beta_threshold, "PROVED_STRICT_BETA_GT_27163_OVER_35721");
  assert.equal(freeze.claim_status.minimum_target_G24, "OPEN_UNPROVED");
  assert.equal(freeze.claim_status.arbitrary_real_E24, "OPEN");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");

  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075g-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 96/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
