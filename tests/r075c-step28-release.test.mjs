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

test("R0.75C Step 28 publishes the exact disproved/paid/open boundary", () => {
  const note = read("public/notes/r0-75c.html");
  for (const marker of [
    "B.44 UNIVERSALITY DISPROVED",
    "SHEAR DISSIPATION PAID",
    "TOTAL-CUBIC FALSE POSITIVE",
    "B.45 UNDECIDED",
    "PASSIVE ROW OPEN",
    "NOT NSE COUNTEREXAMPLE",
    "\\frac9{40000}",
    "\\frac{4279}{79380000}",
    "\\frac{27163}{158760000}",
    "C\\omega^{1/3}L^{-1/3}(P_R^M)^{2/3}",
    "D_{k,R}^{{\\rm out},F}\\stackrel{?}{\\le}C(P_R^M)^{2/3}",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 250_000);
  assert.ok(note.includes('<link rel="canonical" href="https://kasifa.github.io/notes/r0-75c.html">'));
  assert.equal(note.includes("\r"), false);
  assert.equal(/[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]/.test(note), false);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 0);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.ok(note.includes("R0.75D/E/F/G 与其他后续工作未读取、未公开"));
  for (const later of ["r0-75d", "r0-75e", "r0-75f", "r0-75g"]) {
    assert.equal(existsSync(resolve(root, `public/notes/${later}.html`)), false, later);
    assert.equal(existsSync(resolve(root, `public/notes/${later}.pdf`)), false, later);
  }
});

test("R0.75C reader PDF is cryptographically bound while the A recap is preserved", () => {
  const binding = JSON.parse(read("research/r075c_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r075c-step28-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-75c.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-75c.pdf"));
  assert.equal(binding.publicPdf.pageCount, 116);
  assert.equal(binding.frozenAuthority.frozenFileCount, 9);
  assert.equal(binding.claimBoundary.b44UniversalNecessity, "DISPROVED");
  assert.equal(binding.claimBoundary.b44SufficientConditionValidity, "RETAINED");
  assert.equal(binding.claimBoundary.thresholdExcess, "27163/158760000");
  assert.equal(binding.claimBoundary.shearDissipation, "PAID");
  assert.equal(binding.claimBoundary.directOuterDissipationB45, "NEITHER PROVED NOR DISPROVED");
  assert.equal(binding.claimBoundary.passiveDissipation, "OPEN");
  assert.equal(binding.claimBoundary.completeKControlled, false);
  assert.equal(binding.claimBoundary.fixedDeletionClosed, false);
  assert.equal(binding.claimBoundary.arbitrarySuitableWeakExtension, false);
  assert.equal(binding.claimBoundary.generalNavierStokesCounterexample, false);
  assert.equal(binding.claimBoundary.noveltyPriorityCorrectnessOrPublishabilityClaim, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.formalFigure.required, false);
  assert.equal(binding.formalFigure.status, "NOT APPLICABLE");
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.cumulativeRecap.nodeCount, 169);
  assert.equal(sha("public/recap-r0-61-r0-75a.html"), "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0");
  assert.equal(sha("public/recap-r0-61-r0-75a.pdf"), "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62");
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75c.html")), false);
  assert.equal(existsSync(resolve(root, "public/recap-r0-61-r0-75c.pdf")), false);
});

test("R0.75C routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r075c"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r075c-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.75C Step 28", "PACKING FALSE POSITIVE", "NEXT · R0.75D NOT AUTHORIZED", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75C Step 28 的 bounded evidence", "universal B.44 proposal 被否定", "B.45", "passive dissipation", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);

  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.07", html: 231, pdf: 188, published: 171, recap: 169, latestRecap: "R0.75A", latestRelease: "R0.75C" });

  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 133);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 5);
  assert.equal(inventory.latestPublishedRelease, "r075c");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075c").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r075c"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r075c").length, 1);

  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r075c");
  assert.equal(manifest.latestCompletedStep, 28);
  assert.equal(manifest.nextRelease, "r075d");
  assert.equal(manifest.latestReleaseGate, "tests/r075c-step28-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075c-step28-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075c-step28-pdf.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  assert.equal(manifest.latestFormalFigurePublication.release, "R0.75A");

  const freeze = JSON.parse(read("research/r075c_freeze_manifest.json"));
  assert.equal(freeze.research_version, "R0.75C");
  assert.equal(freeze.frozen_file_count, 9);
  assert.equal(freeze.claim_status.formal_figure, "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION");
  assert.equal(freeze.claim_status.universal_b44, "DISPROVED");
  assert.equal(freeze.claim_status.background_shear_dissipation, "PAID");
  assert.equal(freeze.claim_status.direct_b45, "NEITHER_PROVED_NOR_DISPROVED");
  assert.equal(freeze.claim_status.passive_dissipation, "OPEN");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_9_OF_9");

  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075c-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 66/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});
