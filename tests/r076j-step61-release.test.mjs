import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (relative) => readFileSync(resolve(root, relative));
const read = (relative) => bytes(relative).toString("utf8");
const sha = (relative) => createHash("sha256").update(bytes(relative)).digest("hex");

test("R0.76J note PDF is cryptographically bound and I recap is preserved", () => {
  const binding = JSON.parse(read("research/r076j_pdf_bindings.json"));
  assert.equal(binding.release, "R0.76J");
  assert.equal(binding.step, 61);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.equal(binding.provenance.sha256, sha(binding.provenance.path));
  assert.equal(binding.publicPdf.pageCount, 290);
  assert.equal(binding.frozenAuthority.sourceCommit, "25d44e986d5283107816f910f89b94bceb1d5726");
  assert.equal(binding.frozenAuthority.handoffCommit, "8b3b67c9f9d1e796f6a1bbd8639ab25d80ed0470");
  assert.equal(binding.claimBoundary.theoremStatus, "PROVED_LOCALLY_FROM_ESTABLISHED_LITERATURE");
  assert.equal(binding.claimBoundary.zhangProposition42Imported, false);
  assert.equal(binding.claimBoundary.historicalIConditionalLiteraturePreserved, true);
  assert.equal(binding.cumulativeRecap.required, false);
  assert.equal(binding.cumulativeRecap.updatedThrough, "R0.76I");
  assert.equal(sha("public/recap-r0-61-r0-76i.html"), "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9");
  assert.equal(sha("public/recap-r0-61-r0-76i.pdf"), "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98");
});

test("R0.76J routes, counts, and manifests are current without publishing later material", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r076j"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r076j-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.76J Step 61", "LOCAL EDGE EXTRAPOLATION RECONSTRUCTION", "166 节已公开", "STOP · NO LATER RELEASE AUTHORIZED", "上一大里程碑", "/recap-r0-61-r0-76i.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.76J Step 61 的本地端点重构", "LITERATURE", "PROVED LOCALLY FROM ESTABLISHED LITERATURE", "FINITE COMPUTATION", "HISTORICAL BOUNDARY", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  assert.equal(home.includes("R0.76K"), false);
  assert.equal(literature.includes("R0.76K"), false);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({ version: version.version, html: version.publicHtmlNoteCount, pdf: version.publicPdfNoteCount, published: version.postR060PublishedNodeCount, recap: version.postR060RecapNodeCount, latestRecap: version.latestRecapRelease, latestRelease: version.latestRelease },
    { version: "2.40", html: 264, pdf: 221, published: 204, recap: 203, latestRecap: "R0.76I", latestRelease: "R0.76J" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 166);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 38);
  assert.equal(inventory.latestPublishedRelease, "r076j");
  assert.equal(inventory.sameReleaseCompletedSteps.r076j, 61);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r076j");
  assert.equal(manifest.latestCompletedStep, 61);
  assert.equal(manifest.nextRelease, "r076k");
  assert.equal(manifest.latestRecapRelease, "r076i");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r076j_freeze_manifest.json"));
  assert.equal(freeze.claim_status.composite_theorem, "PROVED_LOCALLY_FROM_ESTABLISHED_LITERATURE");
  assert.equal(freeze.claim_status.historical_i_status, "CONDITIONAL_LITERATURE_PRESERVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
});
