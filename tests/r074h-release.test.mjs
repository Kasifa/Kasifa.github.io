import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

test("R0.74H accounting advances the note endpoint without changing the recap", async () => {
  const [manifest, site, inventory, version] = await Promise.all([
    text("research/release-manifest.json").then(JSON.parse),
    text("public/site-version.json").then(JSON.parse),
    text("research/formal-archive-inventory.json").then(JSON.parse),
    text("VERSION"),
  ]);
  assert.equal(version, "1.74\n");
  assert.equal(manifest.latestCompletedRelease, "r074h");
  assert.equal(manifest.nextRelease, "r074i");
  assert.equal(manifest.siteVersion, "1.74");
  assert.equal(manifest.publicHtmlNoteCount, 210);
  assert.equal(manifest.publicPdfNoteCount, 167);
  assert.equal(manifest.postR060PublishedNodeCount, 150);
  assert.equal(manifest.postR060RecapNodeCount, 140);
  assert.equal(manifest.latestRecapRelease, "r073x");
  assert.equal(site.latestRelease, "R0.74H");
  assert.equal(site.latestRecapRelease, "R0.73X");
  assert.equal(inventory.publishedReleases.at(-1), "r074h");
  assert.equal(inventory.formalSealedReleases.at(-1), "r074h");
  assert.equal(inventory.publishedReleaseCount, 112);
  assert.equal(inventory.formalSealedReleaseCount, 88);
});

test("complete Chinese note preserves theorem formulas, qualifiers, and evidence links", async () => {
  const note = await text("public/notes/r0-74h.html");
  for (const marker of [
    "完整中文版本", "PROVED", "FINITE", "OPEN", "LITERATURE BOUNDARY", "NOT CLAY",
    "X_R^M\\le C\\bigl[(P_R^M)^{2/3}+P_R^M\\bigr]",
    "X_R^F\\le C\\bigl[(P_R^F)^{2/3}+P_{0,R}^F\\bigr]",
    "P_R^\\alpha\\le1", "\\widehat P_R^\\alpha", "\\mathfrak C_{R_j}^M=\\mathfrak C_{R_j}^F",
    "没有证明反向比较", "25/25", "150 个字段", "69/69", "24 个文件",
  ]) assert.ok(note.includes(marker), marker);
  for (const path of [
    "r074h_collar_flux_two_regime_closure.md", "r074h_energy_identity_independent_audit.md",
    "r074h_packet_flux_independent_audit.md", "r074h_scaling_and_claim_audit.md",
    "r074h_full_note_adversarial_audit.md", "r074h_final_source_rebind_audit.md",
    "r074h_report-source.md", "r074h_collar_flux_certificate_report.md",
    "r074h_collar_flux_certificate.json", "r074h_collar_flux_certificate.py",
    "r074h_collar_flux_certificate_independent.rb", "r074h_certificate_independent_audit.md",
    "r074h_primary_literature_boundary.md", "r074h_primary_literature_independent_audit.md",
    "r074h_gap_matrix.md", "r074h_freeze_manifest.json", "source-data.csv", "caption.md",
    "qa-report.md", "validation.json",
  ]) assert.ok(note.includes(path), path);
  assert.ok(note.includes('srcset="/assets/r074h/fig-r074h-collar-flux-repair.svg"'));
  assert.ok(note.includes('src="/assets/r074h/fig-r074h-collar-flux-repair.png"'));
  assert.ok(!note.includes("世界首个"));
  assert.ok(!note.includes("解决千禧年问题"));
});

test("public figure mirrors and masters are exact frozen copies", async () => {
  const source = "research/figures/r074h/fig-r074h-collar-flux-repair";
  const mirror = "public/figures/r074h/fig-r074h-collar-flux-repair";
  const names = await readdir(resolve(root, source));
  assert.equal(names.length, 24);
  for (const name of names)
    assert.deepEqual(await read(`${mirror}/${name}`), await read(`${source}/${name}`), name);
  for (const extension of ["svg", "pdf", "png"])
    assert.deepEqual(
      await read(`public/assets/r074h/fig-r074h-collar-flux-repair.${extension}`),
      await read(`${source}/figure.${extension}`),
      extension,
    );
});

test("homepage, literature route, and index expose R0.74H once and compactly", async () => {
  const [home, literature, index] = await Promise.all([
    text("public/research-review.html"), text("public/literature-review.html"), text("public/notes/index.html"),
  ]);
  assert.equal((home.match(/data-release="r074h"/g) ?? []).length, 1);
  for (const marker of ["LATEST RELEASE · R0.74H", "NEXT · R0.74I", "210 篇研究笔记总索引", "112 节已公开", "88 节完整封存"])
    assert.ok(home.includes(marker), marker);
  const card = home.match(/<div class="task-one" id="r074h"[\s\S]*?<div class="task-one" id="r074g"/)?.[0] ?? "";
  assert.ok(card.length > 0);
  assert.ok(card.length < 1600, "homepage R0.74H card must remain concise");
  assert.ok(literature.includes('id="r074h-boundary"'));
  assert.ok(literature.includes("开放接口 · R0.74I"));
  assert.equal((index.match(/class="note-entry"/g) ?? []).length, 210);
  assert.ok(index.includes('href="/notes/r0-74h.pdf"'));
});

test("R0.74H PDF is present and cryptographically bound to the Chinese HTML", async () => {
  await access(resolve(root, "public/notes/r0-74h.pdf"));
  const binding = JSON.parse(await text("research/r074h_pdf_bindings.json"));
  const html = await read("public/notes/r0-74h.html");
  const pdf = await read("public/notes/r0-74h.pdf");
  assert.equal(binding.release, "R0.74H");
  assert.equal(binding.publicChineseNote.sha256, sha256(html));
  assert.equal(binding.publicPdf.sha256, sha256(pdf));
  assert.equal(binding.publicPdf.pageCount, 4);
  assert.equal(binding.claimBoundary.completeChinesePublicNote, true);
  assert.equal(binding.claimBoundary.pdfBindingCertifiesMathematicalCorrectness, false);
  assert.deepEqual(binding.claimBoundary.evidenceClassesSeparated, ["PROVED", "FINITE", "OPEN", "LITERATURE BOUNDARY", "NOT CLAY"]);
});

test("R0.73X recap remains byte-preserved and no R0.74H recap exists", async () => {
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.html")), "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776");
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.pdf")), "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa");
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74h.html")));
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74h.pdf")));
});
