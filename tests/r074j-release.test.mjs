import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

test("R0.74J accounting advances note endpoint without changing recap", async () => {
  const [manifest, site, inventory, version] = await Promise.all([
    text("research/release-manifest.json").then(JSON.parse),
    text("public/site-version.json").then(JSON.parse),
    text("research/formal-archive-inventory.json").then(JSON.parse),
    text("VERSION"),
  ]);
  assert.equal(version, "1.76\n");
  assert.equal(manifest.latestCompletedRelease, "r074j");
  assert.equal(manifest.nextRelease, "r074k");
  assert.equal(manifest.siteVersion, "1.76");
  assert.equal(manifest.publicHtmlNoteCount, 212);
  assert.equal(manifest.publicPdfNoteCount, 169);
  assert.equal(manifest.postR060PublishedNodeCount, 152);
  assert.equal(manifest.postR060RecapNodeCount, 140);
  assert.equal(manifest.latestRecapRelease, "r073x");
  assert.equal(site.latestRelease, "R0.74J");
  assert.equal(site.latestRecapRelease, "R0.73X");
  assert.equal(inventory.publishedReleases.at(-1), "r074j");
  assert.equal(inventory.formalSealedReleases.at(-1), "r074j");
  assert.equal(inventory.publishedReleaseCount, 114);
  assert.equal(inventory.formalSealedReleaseCount, 90);
});

test("complete Chinese note preserves formulas, qualifiers, and evidence links", async () => {
  const note = await text("public/notes/r0-74j.html");
  for (const marker of [
    "完整中文版本", "PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY",
    "A_5(2R_j)", "\\Gamma_5=e^{-8}", "8e^{-8}B_j^3R_j^3",
    "P_j:=P_{R_j}^M=P_{R_j}^F", "\\frac{\\log P_j}{L_j^2}", "\\frac3{320}", "\\frac9{320}",
    "P_j^{2/3}\\sqrt{1+\\log_+P_j}", "精确解族", "不是普适", "38/38", "287 个", "79/79", "24 文件",
  ]) assert.ok(note.includes(marker), marker);
  for (const path of [
    "r074j_matching_payment_law.md", "r074j_heat_platform_independent_audit.md",
    "r074j_complete_payment_ledger_independent_audit.md", "r074j_final_source_rebind_audit.md",
    "r074j_report-source.md", "r074j_matching_payment_certificate_report.md",
    "r074j_matching_payment_certificate.json", "r074j_matching_payment_certificate.py",
    "r074j_matching_payment_certificate_independent.rb", "r074j_certificate_independent_audit.md",
    "r074j_primary_literature_boundary.md", "r074j_primary_literature_independent_audit.md",
    "r074j_gap_matrix.md", "r074j_bilingual_dictionary.md", "r074j_freeze_manifest.json",
    "source-data.csv", "caption.md", "qa-report.md", "plot.py", "validate.py", "manifest.json", "validation.json",
  ]) assert.ok(note.includes(path), path);
  assert.ok(note.includes('srcset="/assets/r074j/fig-r074j-fifth-shell-payment.svg"'));
  assert.ok(note.includes('src="/assets/r074j/fig-r074j-fifth-shell-payment.png"'));
  for (const forbidden of ["世界首个", "首次证明", "解决千禧年问题", "接近解决"])
    assert.ok(!note.includes(forbidden), forbidden);
});

test("public figure mirrors and masters are exact frozen copies", async () => {
  const source = "research/figures/r074j/fig-r074j-fifth-shell-payment";
  const mirror = "public/figures/r074j/fig-r074j-fifth-shell-payment";
  const names = await readdir(resolve(root, source));
  assert.equal(names.length, 24);
  for (const name of names)
    assert.deepEqual(await read(`${mirror}/${name}`), await read(`${source}/${name}`), name);
  for (const extension of ["svg", "pdf", "png"])
    assert.deepEqual(
      await read(`public/assets/r074j/fig-r074j-fifth-shell-payment.${extension}`),
      await read(`${source}/figure.${extension}`), extension,
    );
});

test("homepage, literature route, and index expose R0.74J once and compactly", async () => {
  const [home, literature, index] = await Promise.all([
    text("public/research-review.html"), text("public/literature-review.html"), text("public/notes/index.html"),
  ]);
  assert.equal((home.match(/data-release="r074j"/g) ?? []).length, 1);
  for (const marker of ["LATEST RELEASE · R0.74J", "NEXT · R0.74K", "212 篇研究笔记总索引", "114 节已公开", "90 节完整封存"])
    assert.ok(home.includes(marker), marker);
  const card = home.match(/<div class="task-one" id="r074j"[\s\S]*?<div class="task-one" id="r074i"/)?.[0] ?? "";
  assert.ok(card.length > 0);
  assert.ok(card.length < 1600, "homepage R0.74J card must remain concise");
  assert.ok(literature.includes('id="r074j-boundary"'));
  assert.ok(literature.includes("开放接口 · R0.74K"));
  assert.equal((index.match(/class="note-entry"/g) ?? []).length, 212);
  assert.ok(index.includes('href="/notes/r0-74j.pdf"'));
});

test("R0.74J PDF is cryptographically bound to Chinese HTML", async () => {
  await access(resolve(root, "public/notes/r0-74j.pdf"));
  const binding = JSON.parse(await text("research/r074j_pdf_bindings.json"));
  const html = await read("public/notes/r0-74j.html");
  const pdf = await read("public/notes/r0-74j.pdf");
  assert.equal(binding.release, "R0.74J");
  assert.equal(binding.publicChineseNote.sha256, sha256(html));
  assert.equal(binding.publicPdf.sha256, sha256(pdf));
  assert.equal(binding.publicPdf.pageCount, 3);
  assert.equal(binding.publicPdf.title, "R0.74J｜第五支付壳给出的匹配完整支付律");
  assert.deepEqual(binding.claimBoundary.evidenceClassesSeparated, ["PROVED", "INHERITED", "FINITE", "LITERATURE BOUNDARY", "OPEN", "NOT CLAY"]);
});

test("R0.73X recap remains byte-preserved and no R0.74J recap exists", async () => {
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.html")), "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776");
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.pdf")), "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa");
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74j.html")));
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74j.pdf")));
});
