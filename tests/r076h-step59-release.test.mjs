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

test("R0.76H note PDF is cryptographically bound while W recap is retained", () => {
  const binding = JSON.parse(read("research/r076h_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r076h-step59-note-synchronized-pdf-binding-v1");
  assert.equal(binding.release, "R0.76H");
  assert.equal(binding.step, 59);
  assert.equal(binding.publicChineseHtml.sha256, sha(binding.publicChineseHtml.path));
  assert.equal(binding.publicPdf.sha256, sha(binding.publicPdf.path));
  assert.ok(binding.publicPdf.pageCount >= 270);
  assert.equal(binding.publicPdf.title, "R0.76H｜完整平台吸收平移二项式障碍");
  assert.equal(binding.frozenAuthority.sourceCommit, "6f3ea9599de24902d6ddbfdcc45d1df7614fe31e");
  assert.equal(binding.frozenAuthority.handoffCommit, "8626f085f3220a79d19816ec220eacc8909971cc");
  assert.equal(binding.frozenAuthority.coreParentCommit, "6f203611dc13b7343005bcab3a429b6c68b10add");
  assert.equal(binding.frozenAuthority.handoffSha256, "cb89fc65dcfdddcc816c958fca207e8cc75e45f0963aaef79837ca7d6870c2ca");
  assert.equal(binding.frozenAuthority.handoffIndependentAuditSha256, "930404041d4b32b5eeac858ed92016ecc4f4b8f7287ec5ffa695bb877cd6b7b6");
  assert.equal(binding.claimBoundary.packetScope, "EXACT_R076G_SHIFTED_BINOMIAL_PACKET_ONLY");
  assert.equal(binding.claimBoundary.fullPhysicalPlateauMass, true);
  assert.equal(binding.claimBoundary.absorptionCost, "EXP_O_M_OVER_A");
  assert.equal(binding.claimBoundary.completeSignedFlux, "STRICTLY_POSITIVE_FOR_ALL_LARGE_L");
  assert.equal(binding.claimBoundary.rawRate, "EXACT_THREE_OVER_40000");
  assert.equal(binding.claimBoundary.normalizedRate, "EXACT_MINUS_TWO_OVER_11907");
  assert.equal(binding.claimBoundary.candidateKilled, "R076G_FULL_PLATEAU_COUNTEREXAMPLE_CANDIDATE");
  assert.equal(binding.claimBoundary.arbitraryPacketTheorem, false);
  assert.equal(binding.claimBoundary.completeVersionMExtraction, "OPEN_NOT_PROVED");
  assert.equal(binding.claimBoundary.formalScientificFigure, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
  assert.equal(binding.cumulativeRecap.required, false);
  assert.equal(binding.cumulativeRecap.updatedThrough, "R0.75W");
  assert.equal(binding.cumulativeRecap.nodeCount, 191);
  assert.equal(binding.cumulativeRecap.retainedHtmlSha256, "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(binding.cumulativeRecap.retainedPdfSha256, "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});

test("R0.76H routes, accounting, manifests, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  assert.equal((home.match(/id="r076h"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="r076h-boundary"/g) ?? []).length, 1);
  for (const marker of ["R0.76H Step 59", "FULL-PLATEAU ABSORPTION FOR THE SHIFTED PACKET", "164 节已公开", "NO LATER RELEASE AUTHORIZED", "/recap-r0-61-r0-75w.html"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.76H Step 59 的 bounded source boundary", "FULL-PLATEAU ABSORPTION FOR THE SHIFTED PACKET", "exp(O(m/a))", "-2/11907", "开放接口 · 后续版本", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  assert.equal(home.includes('id="r076i"'), false);
  assert.equal(home.includes('href="/notes/r0-76i.html"'), false);
  assert.equal(literature.includes('href="/notes/r0-76i.html"'), false);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latestRecap: version.latestRecapRelease,
    latestRelease: version.latestRelease,
  }, { version: "2.38", html: 262, pdf: 219, published: 202, recap: 191, latestRecap: "R0.75W", latestRelease: "R0.76H" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 164);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 36);
  assert.equal(inventory.latestPublishedRelease, "r076h");
  assert.equal(inventory.publishedReleases.filter((row) => row === "r076h").length, 1);
  assert.equal(inventory.formalSealedReleases.includes("r076h"), false);
  assert.equal(inventory.formalFigureExemptReleases.filter((row) => row === "r076h").length, 1);
  assert.equal(inventory.sameReleaseCompletedSteps.r076h, 59);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedRelease, "r076h");
  assert.equal(manifest.latestCompletedStep, 59);
  assert.equal(manifest.nextRelease, "r076i");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r076h-step59-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75w.html");
  assert.equal(manifest.latestRecapPdf, "/recap-r0-61-r0-75w.pdf");
  assert.equal(manifest.latestPublicationIdentity.sourceCommit, "6f3ea9599de24902d6ddbfdcc45d1df7614fe31e");
  assert.equal(manifest.latestPublicationIdentity.handoffCommit, "8626f085f3220a79d19816ec220eacc8909971cc");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, false);
  assert.equal(manifest.latestPublicationIdentity.formalFigureRequired, false);
  const freeze = JSON.parse(read("research/r076h_freeze_manifest.json"));
  assert.equal(freeze.scope, "FULL_PLATEAU_ABSORPTION_FOR_EXPLICIT_SHIFTED_BINOMIAL_PACKET");
  assert.equal(freeze.claim_status.full_plateau_absorption, "PROVED_AT_EXP_O_M_OVER_A_COST");
  assert.equal(freeze.claim_status.raw_rate, "EXACT_THREE_OVER_40000");
  assert.equal(freeze.claim_status.normalized_rate, "EXACT_MINUS_TWO_OVER_11907");
  assert.equal(freeze.claim_status.arbitrary_packets, "OPEN_NOT_PROVED");
  assert.equal(freeze.publication_handoff.recap_update_required, false);
  assert.equal(freeze.publication_handoff.retained_recap_terminal_release, "R0.75W_STEP48");
  assert.equal(freeze.verification.frozen_hash_ledger, "PASS_12_OF_12");
  const output = execFileSync(node, ["scripts/add-r076h-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 54/);
  assert.match(output, /"dgxUsed": false/);
});

test("R0.76H publishes no figure, arbitrary-packet theorem, later release, or recap rewrite", () => {
  const note = read("public/notes/r0-76h.html");
  for (const marker of ["CANDIDATE KILLED", "FULL PLATEAU ABSORPTION", "EXPLICIT PACKET ONLY", "RAW RATE 3/40000", "NORMALIZED RATE -2/11907", "NO ARBITRARY-PACKET THEOREM", "NO VERSION-M CLAIM", "NO FIGURE / NO DNS", "NOT CLAY"]) assert.ok(note.includes(marker), marker);
  assert.equal(existsSync(resolve(root, "public/assets/r076h")), false);
  assert.equal(note.includes("R0.76I"), false);
  assert.equal(sha("public/recap-r0-61-r0-75w.html"), "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc");
  assert.equal(sha("public/recap-r0-61-r0-75w.pdf"), "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce");
});
