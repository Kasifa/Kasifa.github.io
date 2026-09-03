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

test("R0.74S Step 17 reader exposes the exact false/open boundary", () => {
  const note = read("public/notes/r0-74s.html");
  for (const marker of [
    "S.445–S.475：PROVED / FALSE / OPEN",
    "regular closed streamline",
    "absolute temporal variation",
    "A^3",
    "signed positive excursion",
    "A^2",
    "所有 \\(p\\ge1\\)、所有 \\(\\beta&lt;1\\)",
    "S.444：FALSE",
    "S.472 / direct hybrid / S.407：OPEN",
    "Q.12 / Q.1：OPEN",
    "NOT CLAY",
    "非 simulation / DNS",
  ]) assert.ok(note.includes(marker), marker);
  assert.ok(Buffer.byteLength(note, "utf8") > 22000);
  assert.ok(!/解决了.{0,20}(千禧年|Clay)/.test(note));
});

test("R0.74S Step 17 one-off route correction recap preserves the prior milestone", () => {
  assert.equal(sha("public/recap-r0-61-r0-74o.html"), "d06c9edb093664c9835feb814a11ecd180305780b3efcdcd560908f754fba4b2");
  assert.equal(sha("public/recap-r0-61-r0-74o.pdf"), "80264dab72ca12569252a360d9b70388ba0c4b107132012b98d73b76d634d076");
  const recap = read("public/recap-r0-61-r0-74s.html");
  for (const marker of [
    "MAJOR ROUTE-CORRECTION RECAP · 161 NODES",
    "Step 16 的 A² 没有错",
    "特殊 separatrix",
    "Step 17 在同一光滑 Taylor 精确解",
    "A^2",
    "A^3",
    "fixed-deletion hybrid / simultaneous height",
  ]) assert.ok(recap.includes(marker), marker);
});

test("R0.74S Step 17 complete four-panel figure archive and public mirrors are byte exact", () => {
  const canonicalRoot = "research/figures/r074s/fig-r074s-recurrent-tail-obstruction";
  const validation = JSON.parse(read(`${canonicalRoot}/validation.json`));
  assert.equal(validation.checkCount, 42);
  assert.equal(validation.checks.length, 42);
  assert.ok(validation.checks.every((row) => row.pass), JSON.stringify(validation.checks.filter((row) => !row.pass)));
  assert.equal(JSON.parse(read(`${canonicalRoot}/manifest.json`)).inventory.count, 25);
  for (const extension of ["svg", "pdf", "png"]) {
    const canonical = `${canonicalRoot}/figure.${extension}`;
    assert.ok(existsSync(resolve(root, canonical)), canonical);
    assert.equal(sha(`figures/r074s/fig-r074s-recurrent-tail-obstruction/figure.${extension}`), sha(canonical));
    assert.equal(sha(`public/figures/r074s/fig-r074s-recurrent-tail-obstruction/figure.${extension}`), sha(canonical));
    assert.equal(sha(`public/assets/r074s/fig-r074s-recurrent-tail-obstruction.${extension}`), sha(canonical));
  }
});

test("R0.74S Step 17 note and recap PDFs are cryptographically bound", () => {
  const note = JSON.parse(read("research/r074s_pdf_bindings.json"));
  assert.equal(note.publicChineseHtml.sha256, sha("public/notes/r0-74s.html"));
  assert.equal(note.publicPdf.sha256, sha("public/notes/r0-74s.pdf"));
  assert.ok(note.publicPdf.pageCount >= 70);
  assert.equal(note.claimBoundary.criticalEndpoint, "FALSE_S444_BY_RECURRENT_CLOSED_STREAMLINE");
  assert.equal(note.claimBoundary.s472FixedDeletionPositiveExcursion, "OPEN");
  assert.equal(note.claimBoundary.directHybridTerminalFluxGate, "OPEN_NOT_REFUTED");
  assert.equal(note.claimBoundary.clayProblemSolved, false);

  const recap = JSON.parse(read("research/r074s_recap_pdf_bindings.json"));
  assert.equal(recap.publicChineseHtml.sha256, sha("public/recap-r0-61-r0-74s.html"));
  assert.equal(recap.publicPdf.sha256, sha("public/recap-r0-61-r0-74s.pdf"));
  assert.ok(recap.publicPdf.pageCount >= 3);
  assert.equal(recap.claimBoundary.step16SpecialSeparatrixAbsoluteVariation, "ASYMPTOTIC_A_SQUARED");
  assert.equal(recap.claimBoundary.step17RecurrentClosedStreamlineAbsoluteVariation, "ASYMPTOTIC_A_CUBED");
});

test("R0.74S Step 17 bilingual coverage is complete and local", () => {
  const output = execFileSync(node, ["scripts/add-r074s-step17-translations.mjs", "--check-only"], { cwd: root, encoding: "utf8" });
  assert.match(output, /"translationPath": "LOCAL_DIRECT_NO_DGX"/);
  assert.match(output, /"dgxUsed": false/);
  assert.match(output, /"checked": 148/);
  assert.match(output, /"applied": false/);
});
