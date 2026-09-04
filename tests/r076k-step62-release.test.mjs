import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("R0.76K note PDF is cryptographically bound and the I recap plus J note are preserved", () => {
  const binding = JSON.parse(read("research/r076k_pdf_bindings.json"));
  assert.equal(binding.release, "R0.76K");
  assert.equal(binding.step, 62);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.equal(binding.provenance.sha256, sha(binding.provenance.path));
  assert.equal(binding.publicPdf.pageCount, 298);
  assert.equal(binding.frozenAuthority.sourceCommit, "8a89aee4fe0839de44e21a90ba827a9cc77b3062");
  assert.equal(binding.frozenAuthority.handoffCommit, "17bec49703836115f2e8a32a4bae516071433902");
  assert.equal(binding.claimBoundary.theoremStatus, "PROVED_LOCAL_REAL_DYADIC_EXACT_HEAT_SHEAR_SINGLE_SLICE");
  assert.equal(binding.claimBoundary.sufficientModeWindow, "Q_LITTLE_O_L_SQUARED");
  assert.equal(binding.claimBoundary.fullUpperWindowLowerBound, "Q_LITTLE_O_L_TO_5_OVER_2_OPEN");
  assert.equal(binding.claimBoundary.completeClockSignedFluxFullPlateauQuotient, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.l3EndpointOptimality, "OPEN_NOT_PROVED");
  assert.equal(binding.cumulativeRecap.required, false);
  assert.equal(binding.cumulativeRecap.updatedThrough, "R0.76I");
  assert.deepEqual(binding.cumulativeRecap.excludesLaterReleases, ["R0.76J", "R0.76K"]);
  assert.equal(sha("public/recap-r0-61-r0-76i.html"), "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9");
  assert.equal(sha("public/recap-r0-61-r0-76i.pdf"), "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98");
  assert.equal(sha("public/notes/r0-76j.html"), "501371270954bb64dae9db784c6981a945730f346d5db971550f3b9d85505de2");
  assert.equal(sha("public/notes/r0-76j.pdf"), "d264c951c9e3e43ab02181ebc4827513a1f6abe0ff37b07bb89ca9d2c6351d87");
});

test("R0.76K routes, counts, and manifests are current without publishing later material", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r076k"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r076k-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.76K Step 62", "REAL DYADIC EDGE SHARPNESS", "167 节已公开", "STOP · NO LATER RELEASE AUTHORIZED", "不覆盖 J/K", "/recap-r0-61-r0-76i.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.76K Step 62 的实单频带下界", "LITERATURE", "PROVED LOCALLY", "FINITE COMPUTATION", "MODE COUNT", "NO COMPLETE-CLOCK LOWER THEOREM", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  assert.equal(home.includes("R0.76L"), false);
  assert.equal(literature.includes("R0.76L"), false);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({ version: version.version, html: version.publicHtmlNoteCount, pdf: version.publicPdfNoteCount, published: version.postR060PublishedNodeCount, recap: version.postR060RecapNodeCount, latestRecap: version.latestRecapRelease, latestRelease: version.latestRelease },
    { version: "2.41", html: 265, pdf: 222, published: 205, recap: 203, latestRecap: "R0.76I", latestRelease: "R0.76K" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 167);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 39);
  assert.equal(inventory.latestPublishedRelease, "r076k");
  assert.equal(inventory.sameReleaseCompletedSteps.r076k, 62);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r076k");
  assert.equal(manifest.latestCompletedStep, 62);
  assert.equal(manifest.nextRelease, "r076l");
  assert.equal(manifest.latestRecapRelease, "r076i");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r076k_freeze_manifest.json"));
  assert.equal(freeze.claim_status.packet_scope, "EXACT_REAL_ONE_DYADIC_BAND_FIXED_SINGLE_SLICE_ONLY");
  assert.equal(freeze.claim_status.varying_degree_range, "Q_LITTLE_O_L_SQUARED_PROVED");
  assert.equal(freeze.claim_status.complete_clock_signed_flux_full_plateau_quotient, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
});
