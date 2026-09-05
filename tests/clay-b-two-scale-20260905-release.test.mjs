import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (bytes) => createHash("sha256").update(bytes).digest("hex");
const protectedArtifacts = {
  "public/recap-r0-61-r0-76i.html": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9",
  "public/recap-r0-61-r0-76i.pdf": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98",
  "public/notes/r0-76j.html": "501371270954bb64dae9db784c6981a945730f346d5db971550f3b9d85505de2",
  "public/notes/r0-76j.pdf": "d264c951c9e3e43ab02181ebc4827513a1f6abe0ff37b07bb89ca9d2c6351d87",
  "public/notes/r0-76k.html": "d4960ea6616b718a4a9edf217f53cbfc276df9fe0662b107f10bca8bf779042d",
  "public/notes/r0-76k.pdf": "b3dce39a5d020a3c2d74133bdfd5c0324e46aefe8b34471b0acb349f90ddc7e1",
  "public/notes/r0-76l.html": "78085c5f2772e4b719004a1e9698147f84d84db73485ddcba2cf155c812e48b2",
  "public/notes/r0-76l.pdf": "3facbf01db259bf6ce2c247f0979b41ea64fe11be88c6c9b7a15a2d0d81d7ad8",
};

test("independent note is complete, bounded, figure-free, and outside the R0 numbering", async () => {
  const note = await text("public/notes/clay-b-two-scale-20260905.html");
  for (const marker of [
    "ClayB-TwoScale-20260905", "PROVED LOCALLY", "FINITE COMPUTATION", "LITERATURE",
    "FIXED POSITIVE SCALE", "NO FIGURE", "NO SIMULATION", "OPEN", "NOT CLAY",
    "D.24-false", "E.5", "E.10", "3A}{20", "3A}{32", "R⁻²", "初值依赖常数",
    "完整时间抵消", "合同 G", "不声称新颖性或优先权",
  ]) assert.ok(note.includes(marker), marker);
  assert.equal(note.includes("R0.76M"), false);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal((note.match(/<section id=/g) ?? []).length, 9);
  for (const path of [
    "clay_b_two_scale_energy_working_20260905.md", "clay_b_two_scale_paid_budget_20260905.md",
    "clay_b_two_scale_report-source_20260905.md", "clay_b_two_scale_independent_audit_20260905.md",
    "clay_b_two_scale_fourier_check.py", "clay_b_two_scale_fourier_certificate_20260905.json",
    "clay_b_two_scale_release_20260905.json", "clay_b_two_scale_frozen_ledger_20260905.json",
  ]) assert.ok(note.includes(path), path);
});

test("navigation exposes the independent note while preserving the R0.76L endpoint", async () => {
  const [home, literature, index, site, manifest, noteFiles] = await Promise.all([
    text("public/research-review.html"),
    text("public/literature-review.html"),
    text("public/notes/index.html"),
    text("public/site-version.json").then(JSON.parse),
    text("research/release-manifest.json").then(JSON.parse),
    readdir(resolve(root, "public/notes")),
  ]);
  for (const page of [home, literature, index]) {
    assert.ok(page.includes("clay-b-two-scale-20260905"));
    assert.equal(page.includes("R0.76M"), false);
  }
  assert.equal((home.match(/id="clay-b-two-scale"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="clay-b-two-scale-boundary"/g) ?? []).length, 1);
  assert.equal((index.match(/data-note="clay-b-two-scale-20260905"/g) ?? []).length, 1);
  assert.equal((index.match(/class="note-entry"/g) ?? []).length, 266);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 266);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.pdf$/.test(name)).length, 223);
  assert.equal(site.version, "2.43");
  assert.equal(site.latestRelease, "R0.76L");
  assert.equal(site.publicIndependentNoteCount, 1);
  assert.equal(site.latestIndependentNote, "ClayB-TwoScale-20260905");
  assert.equal(manifest.siteVersion, "2.43");
  assert.equal(manifest.latestCompletedRelease, "r076l");
  assert.equal(manifest.latestCompletedStep, 63);
  assert.equal(manifest.latestPublication.releaseId, "clay-b-two-scale-20260905");
  assert.equal(manifest.latestPublication.advancesCanonicalR0Series, false);
  assert.equal(manifest.latestPublication.formalFigureRequired, false);
  assert.equal(manifest.latestPublication.simulationRequired, false);
  assert.equal(manifest.latestPublication.recapRequired, false);
  assert.equal(manifest.latestPublication.canonicalR0EndpointPreserved, "r076l");
});

test("Clay-B reader PDF is bound to the Chinese HTML", async () => {
  await access(resolve(root, "public/notes/clay-b-two-scale-20260905.pdf"));
  const binding = JSON.parse(await text("research/clay_b_two_scale_pdf_bindings_20260905.json"));
  const [html, pdf, provenance, ledger] = await Promise.all([
    read(binding.publicChineseHtml.path),
    read(binding.publicPdf.path),
    read(binding.provenance.path),
    read(binding.frozenAuthority.ledgerPath),
  ]);
  assert.equal(binding.releaseId, "ClayB-TwoScale-20260905");
  assert.equal(binding.publicChineseHtml.sha256, sha256(html));
  assert.equal(binding.publicPdf.sha256, sha256(pdf));
  assert.equal(binding.provenance.sha256, sha256(provenance));
  assert.equal(binding.frozenAuthority.ledgerSha256, sha256(ledger));
  assert.ok(binding.publicPdf.pageCount >= 5 && binding.publicPdf.pageCount <= 30);
  assert.equal(binding.publicPdf.title, "两尺度差能量：瞬时吸收的限制与完整支付");
  assert.equal(binding.scientificFigure.required, false);
  assert.equal(binding.scientificFigure.generated, false);
  assert.equal(binding.simulation.run, false);
  assert.equal(binding.cumulativeRecap.updated, false);
  assert.equal(binding.canonicalSeries.advanced, false);
});

test("the I recap and J/K/L note pairs remain byte-exact", async () => {
  for (const [path, expected] of Object.entries(protectedArtifacts)) {
    assert.equal(sha256(await read(path)), expected, path);
  }
  await assert.rejects(access(resolve(root, "public/recap-clay-b-two-scale-20260905.html")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-two-scale-20260905.pdf")));
});
