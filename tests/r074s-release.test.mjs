import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const bytes = (path) => readFileSync(resolve(root, path));
const sha = (path) => createHash("sha256").update(bytes(path)).digest("hex");

test("R0.74S cumulative release remains on one note while Step 18 advances", () => {
  const version = JSON.parse(bytes("public/site-version.json"));
  const manifest = JSON.parse(bytes("research/release-manifest.json"));
  assert.deepEqual(version, {
    schemaVersion: "research-site-version-v1",
    version: "1.97",
    latestRelease: "R0.74S",
    latestPublishedResearchHtml: "/notes/r0-74s.html",
    latestPublishedResearchPdf: "/notes/r0-74s.pdf",
    publicHtmlNoteCount: 221,
    postR060PublishedNodeCount: 161,
    postR060RecapNodeCount: 161,
    latestRecapRelease: "R0.74S",
    publicPdfNoteCount: 178,
    publishedDate: "2026-09-03",
  });
  assert.equal(manifest.latestCompletedRelease, "r074s");
  assert.equal(manifest.latestCompletedStep, 18);
  assert.equal(manifest.nextRelease, "r074t");
  assert.equal(manifest.postR070APublishedReleaseCount, 123);
  assert.equal(manifest.postR070AFormalSealedReleaseCount, 98);
  assert.equal(manifest.latestRecapRelease, "r074s");
  assert.equal(sha("public/recap-r0-61-r0-74s.html"), "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81");
  assert.equal(sha("public/recap-r0-61-r0-74s.pdf"), "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec");
});

test("R0.74S Step 18 synchronized binding retains the strict boundary", () => {
  const binding = JSON.parse(bytes("research/r074s_pdf_bindings.json"));
  assert.equal(binding.schemaVersion, "r074s-step18-note-synchronized-pdf-binding-v1");
  assert.equal(binding.publicChineseHtml.sha256, sha("public/notes/r0-74s.html"));
  assert.equal(binding.publicPdf.sha256, sha("public/notes/r0-74s.pdf"));
  assert.deepEqual(binding.claimBoundary.proved, ["S.476-S.485", "S.488-S.493"]);
  assert.deepEqual(binding.claimBoundary.abstractOnly, [
    "triangular-clock strictness",
    "linear-ledger two-thirds-power obstruction",
  ]);
  assert.ok(binding.claimBoundary.open.includes("S.486"));
  assert.ok(binding.claimBoundary.open.includes("S.487"));
  assert.equal(binding.claimBoundary.pdeData, false);
  assert.equal(binding.claimBoundary.dns, false);
  assert.equal(binding.claimBoundary.clayClaim, false);
});
