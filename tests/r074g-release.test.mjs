import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";
import test from "node:test";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");

const frozen = new Map([
  ["research/r074g_complete_payment_counterexample.md", "95548d6225389b9cfd1822a8abaf89e495e7f15ca5ff30c6b92aaa8ac5f2d6be"],
  ["research/r074g_energy_pressure_independent_audit.md", "305d73a8d45b7292baa7f3535b9347d3822f366087a6600e936915ad20cd1d0e"],
  ["research/r074g_occupation_independent_audit.md", "aa958b3ab703e0078b4e3e1e9d028b7304889d6038be58dd3c4333f2ae6843ab"],
  ["research/r074g_complete_ledger_adversarial_audit.md", "60fff91179a49f2f71a4a68aa5d0e77304b58c6310791e2293ad50d9a95f2cb6"],
  ["scripts/r074g_complete_payment_certificate.py", "315f4cc7f0a397287cc2eb14ec1ad65bcacb797692e2a6ce5a1459985a4853ca"],
  ["research/r074g_complete_payment_certificate.json", "2a411007989e63e51ab7f1644724f654f26794b80507681aaf62e00adbeefd53"],
  ["research/r074g_complete_payment_certificate_report.md", "aee995c26795c460fa76cd004f227f56a102ca2daf1040b428c313d48f3ab3bc"],
  ["research/r074g_certificate_independent_audit.md", "598a92ef5c3cb061142ede1bb1c5dff0680848c386c0847f45d97f246b93fade"],
  ["research/r074g_gap_matrix.md", "e9001e32b993ac565eaf9d3efc70cbec55e4045cc03d3e9c1e736653bea97bf3"],
  ["research/r074g_freeze_manifest.json", "9e6df815df139212ddaa6c54e473bb7fd6e516264287784e20ee96010afe2abe"],
]);

test("R0.74G accounting advances the note endpoint without a recap", async () => {
  const [manifest, site, inventory, version] = await Promise.all([
    text("research/release-manifest.json").then(JSON.parse),
    text("public/site-version.json").then(JSON.parse),
    text("research/formal-archive-inventory.json").then(JSON.parse),
    text("VERSION"),
  ]);
  assert.ok(Number.parseFloat(version) >= 1.73);
  assert.ok(manifest.publicHtmlNoteCount >= 209);
  assert.ok(manifest.publicPdfNoteCount >= 166);
  assert.ok(manifest.postR060PublishedNodeCount >= 149);
  assert.equal(manifest.postR060RecapNodeCount, 140);
  assert.equal(manifest.latestRecapRelease, "r073x");
  assert.equal(site.latestRecapRelease, "R0.73X");
  assert.ok(inventory.publishedReleases.includes("r074g"));
  assert.ok(inventory.formalSealedReleases.includes("r074g"));
  assert.ok(inventory.publishedReleaseCount >= 111);
  assert.ok(inventory.formalSealedReleaseCount >= 87);
});

test("frozen R0.74G research assets remain byte-exact", async () => {
  for (const [path, expected] of frozen)
    assert.equal(sha256(await read(path)), expected, path);
  const base = "research/figures/r074g/fig-r074g-complete-payment-ledger";
  const expectedMasters = new Map([
    ["figure.svg", "254aa5c7482d3665ab0873690bd2a3a14dfa0a0555beb3182b001636b8518785"],
    ["figure.pdf", "62fdeeca29227ce508631386d8406815440fd8d06ee9110cb3fb2b707f0f8134"],
    ["figure.png", "57e83342f003217eaa915a7a68122c6015aef3da5d8a8d7f3e6322667306ba7d"],
  ]);
  for (const [name, expected] of expectedMasters)
    assert.equal(sha256(await read(`${base}/${name}`)), expected, name);
});

test("Chinese note exposes formulas, evidence classes, and every required link", async () => {
  const note = await text("public/notes/r0-74g.html");
  for (const marker of [
    "完整中文版本", "PROVED", "FINITE", "OPEN", "ROUTE REJECTED", "NOT CLAY",
    "完整支付账本已经闭合", "同一精确解族与反例尺度", "完整分母", "路线结论",
    "P_{R_j}^M=P_{R_j}^F", "cL_j\\longrightarrow\\infty", "31/31", "70/70",
    "只表示指定的两条内部候选估计被反例排除", "不声明“首次”",
  ]) assert.ok(note.includes(marker), marker);
  for (const path of [
    "r074g_complete_payment_counterexample.md", "r074g_energy_pressure_independent_audit.md",
    "r074g_occupation_independent_audit.md", "r074g_complete_ledger_adversarial_audit.md",
    "r074g_complete_payment_certificate_report.md", "r074g_complete_payment_certificate.json",
    "r074g_complete_payment_certificate.py", "r074g_certificate_independent_audit.md",
    "r074g_gap_matrix.md", "r074g_freeze_manifest.json", "source-data.csv", "caption.md",
    "qa-report.md", "validation.json",
  ]) assert.ok(note.includes(path), path);
  assert.ok(note.includes('srcset="/assets/r074g/fig-r074g-complete-payment-ledger.svg"'));
  assert.ok(note.includes('src="/assets/r074g/fig-r074g-complete-payment-ledger.png"'));
  assert.ok(!note.includes("世界首个"));
  assert.ok(!note.includes("证明千禧年问题"));
});

test("public figure mirrors and masters are exact copies", async () => {
  const source = "research/figures/r074g/fig-r074g-complete-payment-ledger";
  const mirror = "public/figures/r074g/fig-r074g-complete-payment-ledger";
  const names = await readdir(resolve(root, source));
  assert.equal(names.length, 24);
  for (const name of names)
    assert.deepEqual(await read(`${mirror}/${name}`), await read(`${source}/${name}`), name);
  for (const extension of ["svg", "pdf", "png"])
    assert.deepEqual(
      await read(`public/assets/r074g/fig-r074g-complete-payment-ledger.${extension}`),
      await read(`${source}/figure.${extension}`),
      extension,
    );
});

test("homepage, literature route, and index expose R0.74G once", async () => {
  const [home, literature, index] = await Promise.all([
    text("public/research-review.html"), text("public/literature-review.html"), text("public/notes/index.html"),
  ]);
  assert.equal((home.match(/data-release="r074g"/g) ?? []).length, 1);
  assert.ok(literature.includes('id="r074g-boundary"'));
  assert.ok((index.match(/class="note-entry"/g) ?? []).length >= 209);
  assert.ok(index.includes('href="/notes/r0-74g.pdf"'));
});

test("six queued PDFs are present and R0.74G is cryptographically bound", async () => {
  for (const code of ["b", "c", "d", "e", "f", "g"])
    await access(resolve(root, `public/notes/r0-74${code}.pdf`));
  const binding = JSON.parse(await text("research/r074g_pdf_bindings.json"));
  const html = await read("public/notes/r0-74g.html");
  const pdf = await read("public/notes/r0-74g.pdf");
  assert.equal(binding.release, "R0.74G");
  assert.equal(binding.publicChineseNote.sha256, sha256(html));
  assert.equal(binding.publicPdf.sha256, sha256(pdf));
  assert.equal(binding.publicPdf.pageCount, 4);
  assert.equal(binding.claimBoundary.completeChinesePublicNote, true);
  assert.equal(binding.claimBoundary.pdfBindingCertifiesMathematicalCorrectness, false);
  assert.deepEqual(binding.claimBoundary.evidenceClassesSeparated, ["PROVED", "FINITE", "OPEN", "ROUTE REJECTED", "NOT CLAY"]);
});

test("R0.73X recap is byte-preserved and no R0.74G recap exists", async () => {
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.html")), "44e38b7a6855edfd92842d2c5eb75792e03f5fb1ca6de6902a1402dcbe0a3776");
  assert.equal(sha256(await read("public/recap-r0-61-r0-73x.pdf")), "e95324099393b5be917cb32b29d4986c4c8699fa3ba21904d7a7b5304e6501fa");
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74g.html")));
  await assert.rejects(access(resolve(root, "public/recap-r0-61-r0-74g.pdf")));
});
