import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

test("R0.74I accounting advances the note endpoint without changing the recap", async () => {
  const [manifest, site, inventory, version] = await Promise.all([
    text("research/release-manifest.json").then(JSON.parse),
    text("public/site-version.json").then(JSON.parse),
    text("research/formal-archive-inventory.json").then(JSON.parse),
    text("VERSION"),
  ]);
  assert.ok(Number.parseFloat(version) >= 1.75);
  assert.ok(manifest.publicHtmlNoteCount >= 211);
  assert.ok(manifest.publicPdfNoteCount >= 168);
  assert.ok(manifest.postR060PublishedNodeCount >= 151);
  assert.equal(manifest.postR060RecapNodeCount, 140);
  assert.equal(manifest.latestRecapRelease, "r073x");
  assert.equal(site.latestRecapRelease, "R0.73X");
  assert.ok(inventory.publishedReleases.includes("r074i"));
  assert.ok(inventory.formalSealedReleases.includes("r074i"));
  assert.ok(inventory.publishedReleaseCount >= 113);
  assert.ok(inventory.formalSealedReleaseCount >= 89);
});

test("complete Chinese note preserves formulas, qualifiers, and evidence links", async () => {
  const note = await text("public/notes/r0-74i.html");
  for (const marker of [
    "完整中文版本", "PROVED", "FINITE", "OPEN", "LITERATURE BOUNDARY", "NOT CLAY",
    "X_R^M\\le C\\bigl[(P_R^M)^{2/3}+P_R^M\\bigr]",
    "P_R^M\\le1", "\\mathcal E^{M,R}(z_0,8R)", "\\varepsilon_{\\rm tube}",
    "P_R^M\\le\\varepsilon_P", "\\liminf_{j\\to\\infty}", "\\sqrt{1+\\log_+P_j}",
    "\\gamma&lt;1/2", "P_j\\gtrsim B_j^3R_j^3",
    "给定尺度", "没有证明可能奇点", "不是已证明上界", "36/36", "269 个", "82/82", "24 文件",
  ]) assert.ok(note.includes(marker), marker);
  for (const path of [
    "r074i_suitable_weak_tube_and_log_obstruction.md", "r074i_weak_extension_independent_audit.md",
    "r074i_epsilon_log_independent_audit.md", "r074i_final_source_rebind_audit.md",
    "r074i_report-source.md", "r074i_tube_log_certificate_report.md",
    "r074i_tube_log_certificate.json", "r074i_tube_log_certificate.py",
    "r074i_tube_log_certificate_independent.rb", "r074i_certificate_independent_audit.md",
    "r074i_primary_literature_boundary.md", "r074i_primary_literature_independent_audit.md",
    "r074i_gap_matrix.md", "r074i_bilingual_dictionary.md", "r074i_freeze_manifest.json",
    "source-data.csv", "caption.md", "qa-report.md", "manifest.json", "validation.json",
  ]) assert.ok(note.includes(path), path);
  assert.ok(note.includes('srcset="/assets/r074i/fig-r074i-moving-tube-log-screen.svg"'));
  assert.ok(note.includes('src="/assets/r074i/fig-r074i-moving-tube-log-screen.png"'));
  for (const forbidden of ["世界首个", "首次证明", "解决千禧年问题", "接近解决"])
    assert.ok(!note.includes(forbidden), forbidden);
});

test("public figure mirrors and masters are exact frozen copies", async () => {
  const source = "research/figures/r074i/fig-r074i-moving-tube-log-screen";
  const mirror = "public/figures/r074i/fig-r074i-moving-tube-log-screen";
  const names = await readdir(resolve(root, source));
  assert.equal(names.length, 24);
  for (const name of names)
    assert.deepEqual(await read(`${mirror}/${name}`), await read(`${source}/${name}`), name);
  for (const extension of ["svg", "pdf", "png"])
    assert.deepEqual(
      await read(`public/assets/r074i/fig-r074i-moving-tube-log-screen.${extension}`),
      await read(`${source}/figure.${extension}`),
      extension,
    );
});

test("homepage, literature route, and index expose R0.74I once and compactly", async () => {
  const [home, literature, index] = await Promise.all([
    text("public/research-review.html"), text("public/literature-review.html"), text("public/notes/index.html"),
  ]);
  assert.equal((home.match(/data-release="r074i"/g) ?? []).length, 1);
  const card = home.match(/<div class="task-one" id="r074i"[\s\S]*?<div class="task-one" id="r074h"/)?.[0] ?? "";
  assert.ok(card.length > 0);
  assert.ok(card.length < 1600, "homepage R0.74I card must remain concise");
  assert.ok(literature.includes('id="r074i-boundary"'));
  assert.ok((index.match(/class="note-entry"/g) ?? []).length >= 211);
  assert.ok(index.includes('href="/notes/r0-74i.pdf"'));
});

test("R0.74I PDF is present and cryptographically bound to the Chinese HTML", async () => {
  await access(resolve(root, "public/notes/r0-74i.pdf"));
  const binding = JSON.parse(await text("research/r074i_pdf_bindings.json"));
  const html = await read("public/notes/r0-74i.html");
  const pdf = await read("public/notes/r0-74i.pdf");
  assert.equal(binding.release, "R0.74I");
  assert.equal(binding.publicChineseNote.sha256, sha256(html));
  assert.equal(binding.publicPdf.sha256, sha256(pdf));
  assert.ok(binding.publicPdf.pageCount >= 4);
  assert.equal(binding.publicPdf.title, "R0.74I｜适合弱解的移动管门与平方根对数支付边界");
  assert.equal(binding.claimBoundary.completeChinesePublicNote, true);
  assert.equal(binding.claimBoundary.pdfBindingCertifiesMathematicalCorrectness, false);
  assert.deepEqual(binding.claimBoundary.evidenceClassesSeparated, ["PROVED", "FINITE", "OPEN", "LITERATURE BOUNDARY", "NOT CLAY"]);
});

test("R0.73X recap remains byte-preserved and no R0.74I recap exists", async () => {
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.html")), "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776");
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.pdf")), "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa");
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74i.html")));
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74i.pdf")));
});
