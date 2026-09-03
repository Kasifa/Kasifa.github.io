import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync } from "node:child_process";
import { existsSync, readFileSync, readdirSync, statSync } from "node:fs";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const readBytes = (path) => readFileSync(resolve(root, path));
const read = (path) => readBytes(path).toString("utf8");
const sha = (path) => createHash("sha256").update(readBytes(path)).digest("hex");
const node = process.env.CODEX_NODE || process.execPath;
const figureId = "fig-r075a-local-persistence-payment";

test("R0.75A Step 26 reader publishes the exact local dichotomy and stop line", () => {
  const note = read("public/notes/r0-75a.html");
  for (const marker of [
    "MOVING-CUTOFF EXACT",
    "TWO CASES EXHAUSTIVE",
    "W-REMOTE PAYMENT PROVED",
    "CRITICAL COVERED",
    "COMPLETE K OPEN",
    "64279/238140000",
    "Wang--Wang--Zhang--Zhang",
    "bounded screen",
    "NO NOVELTY CLAIM",
    "NOT CLAY",
    "A.63 remote complete-clock extraction",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 250_000);
  assert.equal((note.match(/<section id="figure">/g) ?? []).length, 1);
  assert.ok(note.includes(`/assets/r075a/${figureId}.svg`));
  assert.ok(note.includes("R0.75B、R0.75C、R0.75D 与其他后续工作未读取、未公开"));
  assert.ok(!note.includes("/assets/r075b/"));
  assert.ok(!note.includes("/assets/r075c/"));
  assert.ok(!note.includes("/assets/r075d/"));
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
});

test("R0.75A cumulative recap contains 169 nodes and the exact P-A five-field ledger", () => {
  const recap = read("public/recap-r0-61-r0-75a.html");
  assert.ok(recap.includes("CUMULATIVE MILESTONE RECAP · 169 NODES"));
  assert.ok(recap.includes("Problem / Result / Rejected / Boundary / Next"));
  assert.equal((recap.match(/<article class="card node">/g) ?? []).length, 12);
  for (const code of ["P", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z", "A"]) {
    assert.equal((recap.match(new RegExp(`<p class="eyebrow">${code} /`, "g")) ?? []).length, 1, code);
  }
  assert.ok(recap.includes("V.46–V.50 只限定到六对 central-chart"));
  assert.ok(recap.includes("即使在六对有限表域，whole-annulus occupation estimates 仍 OPEN"));
  assert.ok(recap.includes("64279/238140000>0"));
  assert.ok(recap.includes("bounded non-hit 不证明 novelty 或 priority"));
  assert.ok(recap.includes("NOT CLAY"));
  const nodeIndex = recap.match(/<div class="node-links">([\s\S]*?)<\/div>/)?.[1] ?? "";
  assert.equal((nodeIndex.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length, 169);
  assert.equal(sha("public/recap-r0-61-r0-74s.html"), "47f8eddf89c018e9ea5c73cb7179e8c282d96d002baa16d52b7fae225f5dae81");
  assert.equal(sha("public/recap-r0-61-r0-74s.pdf"), "eea82eba8d6fe66ca8a45348d3d9e20a9450c039f749feafae007a362a2a49ec");
});

test("R0.75A note and cumulative recap PDFs are cryptographically bound", () => {
  const note = JSON.parse(read("research/r075a_pdf_bindings.json"));
  const recap = JSON.parse(read("research/r075a_recap_pdf_bindings.json"));
  assert.equal(note.schemaVersion, "r075a-step26-note-synchronized-pdf-binding-v1");
  assert.equal(recap.schemaVersion, "r075a-step26-cumulative-recap-synchronized-pdf-binding-v1");
  assert.equal(note.publicChineseHtml.sha256, sha("public/notes/r0-75a.html"));
  assert.equal(note.publicPdf.sha256, sha("public/notes/r0-75a.pdf"));
  assert.equal(note.publicPdf.pageCount, 113);
  assert.equal(recap.publicChineseHtml.sha256, sha("public/recap-r0-61-r0-75a.html"));
  assert.equal(recap.publicPdf.sha256, sha("public/recap-r0-61-r0-75a.pdf"));
  assert.equal(recap.publicPdf.pageCount, 4);
  for (const binding of [note, recap]) {
    assert.equal(binding.claimBoundary.persistenceRapidRiseExhaustive, true);
    assert.equal(binding.claimBoundary.criticalAndArbitrarilyShortSmoothFocusingCovered, true);
    assert.equal(binding.claimBoundary.completeClockControlled, false);
    assert.equal(binding.claimBoundary.fixedDeletionClosed, false);
    assert.equal(binding.claimBoundary.noveltyOrPriorityClaim, false);
    assert.equal(binding.claimBoundary.clayClaim, false);
    assert.equal(binding.cumulativeRecap.nodeCount, 169);
  }
});

test("R0.75A routes, accounting, manifest, and translations are current", () => {
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  for (const marker of ["R0.75A Step 26", "LOCAL DICHOTOMY", "NEXT · R0.75B NOT AUTHORIZED · A.63", "169 节"]) assert.ok(home.includes(marker), marker);
  for (const marker of ["R0.75A Step 26 的 bounded literature screen", "Wang--Wang--Zhang--Zhang", "complete K", "NO NOVELTY CLAIM", "NOT CLAY"]) assert.ok(literature.includes(marker), marker);
  const version = JSON.parse(read("public/site-version.json"));
  assert.deepEqual({
    version: version.version,
    html: version.publicHtmlNoteCount,
    pdf: version.publicPdfNoteCount,
    published: version.postR060PublishedNodeCount,
    recap: version.postR060RecapNodeCount,
    latest: version.latestRecapRelease,
  }, { version: "2.05", html: 229, pdf: 186, published: 169, recap: 169, latest: "R0.75A" });
  const inventory = JSON.parse(read("research/formal-archive-inventory.json"));
  assert.equal(inventory.publishedReleaseCount, 131);
  assert.equal(inventory.formalSealedReleaseCount, 104);
  assert.equal(inventory.formalFigureExemptReleaseCount, 3);
  assert.equal(inventory.publishedReleases.filter((row) => row === "r075a").length, 1);
  assert.equal(inventory.formalSealedReleases.filter((row) => row === "r075a").length, 1);
  const manifest = JSON.parse(read("research/release-manifest.json"));
  assert.equal(manifest.latestCompletedStep, 26);
  assert.equal(manifest.nextRelease, "r075b");
  assert.equal(manifest.latestReleaseGate, "tests/r075a-step26-gate.test.mjs");
  assert.equal(manifest.latestReleasePublicationTest, "tests/r075a-step26-release.test.mjs");
  assert.equal(manifest.latestReleasePdfBinder, "scripts/bind-r075a-step26-pdfs.mjs");
  assert.equal(manifest.latestRecapHtml, "/recap-r0-61-r0-75a.html");
  assert.equal(manifest.latestPublicationIdentity.recapRequired, true);
  assert.equal(manifest.latestFormalFigurePublication.inventory.files, 25);
  assert.equal(manifest.latestFormalFigurePublication.inventory.bytes, 2588462);
  assert.ok(existsSync(resolve(root, "public/i18n-en.js")));
  const output = execFileSync(node, ["scripts/add-r075a-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"checked": 152/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"applied": false/);
});

test("R0.75A frozen figure masters match all published copies", () => {
  const canonicalRoot = `research/figures/r075a/${figureId}`;
  const names = readdirSync(resolve(root, canonicalRoot)).filter((name) => !/ 2(?:\.|$)/.test(name)).sort();
  assert.equal(names.length, 25);
  assert.equal(names.reduce((sum, name) => sum + statSync(resolve(root, canonicalRoot, name)).size, 0), 2588462);
  for (const extension of ["svg", "pdf", "png"]) {
    assert.equal(sha(`public/assets/r075a/${figureId}.${extension}`), sha(`${canonicalRoot}/figure.${extension}`));
  }
  assert.equal(existsSync(resolve(root, "public/notes/r0-75b.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75c.html")), false);
  assert.equal(existsSync(resolve(root, "public/notes/r0-75d.html")), false);
});
