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
  "public/notes/clay-b-two-scale-20260905.html": "5c4a52ddc000a5f329c2adb238d66dc34db532dddd3d8e6e97e791c954749e09",
  "public/notes/clay-b-two-scale-20260905.pdf": "3f6fbe49c369190c8fac999a3f67bd91918d2a73f514c9ec5b3a8e8d2316423b",
};

test("the HTML-only signed-scale note is complete, bilingual, bounded, and figure-free", async () => {
  const note = await text("public/notes/clay-b-signed-scale-20260905.html");
  for (const marker of [
    "ClayB-SignedScale-20260905", "PROVED LOCALLY", "LITERATURE",
    "NO NUMERICAL CERTIFICATE", "NO FIGURE", "NO SIMULATION", "OPEN", "NOT CLAY",
    "S.8--S.15", "T.7--T.12", "T<sub>R</sub>=128R²", "初始 H¹：不统一",
    "Contract G", "first singular time",
  ]) assert.ok(note.includes(marker), marker);
  assert.equal((note.match(/<main data-language="zh">/g) ?? []).length, 1);
  assert.equal((note.match(/<main data-language="en">/g) ?? []).length, 1);
  assert.equal((note.match(/<section>/g) ?? []).length, 18);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(note.includes("/notes/clay-b-signed-scale-20260905.pdf"), false);
  assert.equal(note.includes("R0.76M"), false);
  for (const path of [
    "clay_b_signed_scale_telescope_preflight_20260905.md",
    "clay_b_signed_scale_local_budget_20260905.md",
    "clay_b_heat_dual_test_obstruction_20260905.md",
    "clay_b_signed_scale_independent_audit_20260905.md",
    "clay_b_signed_scale_release_20260905.json",
    "clay_b_signed_scale_frozen_ledger_20260905.json",
  ]) assert.ok(note.includes(path), path);
});

test("navigation integrates the strategy branch into the homepage route map", async () => {
  const [home, literature, index, site, manifest, noteFiles] = await Promise.all([
    text("public/research-review.html"),
    text("public/literature-review.html"),
    text("public/notes/index.html"),
    text("public/site-version.json").then(JSON.parse),
    text("research/release-manifest.json").then(JSON.parse),
    readdir(resolve(root, "public/notes")),
  ]);
  for (const page of [home, literature, index]) {
    assert.ok(page.includes("clay-b-signed-scale-20260905"));
    assert.equal(page.includes("R0.76M"), false);
  }
  const routeStart = home.indexOf('<div class="route-tree"');
  const signedRow = home.indexOf('class="tree-row clay-b-signed-scale-row"');
  const lastCanonicalLink = home.lastIndexOf('href="/notes/r0-76l.html"', home.indexOf('<div class="page-shell">'));
  const nextBoundary = home.indexOf("NEXT · NOT AUTHORIZED", routeStart);
  assert.ok(routeStart >= 0 && lastCanonicalLink < signedRow && signedRow < nextBoundary);
  assert.ok(home.slice(signedRow, nextBoundary).includes("R0.76L 边界 → Clay-B 两尺度完整支付"));
  assert.equal((home.match(/id="clay-b-signed-scale"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="clay-b-signed-scale-boundary"/g) ?? []).length, 1);
  assert.equal((index.match(/data-note="clay-b-signed-scale-20260905"/g) ?? []).length, 1);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 266);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.pdf$/.test(name)).length, 223);
  assert.equal(noteFiles.includes("clay-b-signed-scale-20260905.pdf"), false);
  assert.equal(site.version, "2.44");
  assert.equal(site.latestRelease, "R0.76L");
  assert.equal(site.publicIndependentNoteCount, 2);
  assert.equal(site.latestIndependentNote, "ClayB-SignedScale-20260905");
  assert.equal(site.latestIndependentResearchPdf, null);
  assert.equal(manifest.siteVersion, "2.44");
  assert.equal(manifest.latestCompletedRelease, "r076l");
  assert.equal(manifest.latestCompletedStep, 63);
  assert.equal(manifest.latestPublication.releaseId, "clay-b-signed-scale-20260905");
  assert.equal(manifest.latestPublication.pdfGenerated, false);
  assert.equal(manifest.latestPublication.pdfPolicy, "OMITTED_BY_USER_PUBLISHING_POLICY");
  assert.equal(manifest.latestPublication.advancesCanonicalR0Series, false);
});

test("the new release preserves previous milestone and note artifacts byte-exactly", async () => {
  for (const [path, expected] of Object.entries(protectedArtifacts)) {
    assert.equal(sha256(await read(path)), expected, path);
  }
  await assert.rejects(access(resolve(root, "public/notes/clay-b-signed-scale-20260905.pdf")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-signed-scale-20260905.html")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-signed-scale-20260905.pdf")));
});
