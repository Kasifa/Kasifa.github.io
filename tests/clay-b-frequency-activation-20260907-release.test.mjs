import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readdir, readFile } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const protectedArtifacts = {
  "public/notes/clay-b-source-enstrophy-20260907.html": "b1b9c0deb076222c00680389daaefa7198f85493c7e0b173c282e0662c8bcb6f",
  "public/recap-r0-61-r0-76i.html": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9",
  "public/recap-r0-61-r0-76i.pdf": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98",
  "public/notes/r0-76l.html": "78085c5f2772e4b719004a1e9698147f84d84db73485ddcba2cf155c812e48b2",
  "public/notes/r0-76l.pdf": "3facbf01db259bf6ce2c247f0979b41ea64fe11be88c6c9b7a15a2d0d81d7ad8",
  "public/notes/clay-b-two-scale-20260905.pdf": "3f6fbe49c369190c8fac999a3f67bd91918d2a73f514c9ec5b3a8e8d2316423b",
};

test("the HTML-only FrequencyActivation note is bilingual, bounded, and figure-free", async () => {
  const note = await text("public/notes/clay-b-frequency-activation-20260907.html");
  for (const marker of [
    "ClayB-FrequencyActivation-20260907", "CB.25", "固定能量下的频带激活",
    "Band activation at fixed energy", "N⁻⁵ᐟ²", "能量给出的普遍上升约束",
    "The universal growth constraint from energy", "严格空带与非退化输出种子",
    "A strictly empty-band seed with nondegenerate output", "PROVED", "SHARP SCALE",
    "FULL NS", "EXISTENTIAL THRESHOLD", "NO RESIDENCE CLAIM", "LITERATURE",
    "FINITE CHECKS ONLY", "OPEN", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.equal((note.match(/<main data-language="zh">/g) ?? []).length, 1);
  assert.equal((note.match(/<main data-language="en">/g) ?? []).length, 1);
  assert.equal((note.match(/<section>/g) ?? []).length, 16);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(note.includes("/notes/clay-b-frequency-activation-20260907.pdf"), false);
  assert.equal(note.includes("R0.76M"), false);
});

test("homepage keeps R0 solid, Clay-B dashed, sequential, and spotlight-latest", async () => {
  const [home, literature, index, site, manifest, noteFiles] = await Promise.all([
    text("public/research-review.html"), text("public/literature-review.html"), text("public/notes/index.html"),
    text("public/site-version.json").then(JSON.parse), text("research/release-manifest.json").then(JSON.parse), readdir(resolve(root, "public/notes")),
  ]);
  for (const page of [home, literature, index]) assert.ok(page.includes("clay-b-frequency-activation-20260907"));
  const r0 = home.indexOf('class="route-tree r0-route-tree"');
  const rb = home.indexOf('class="tree-row r0-public-boundary-row"', r0);
  const divider = home.indexOf('class="route-lane-divider"', rb);
  const clay = home.indexOf('class="route-tree clay-b-route-tree"', divider);
  const cb22 = home.indexOf('class="tree-row clay-b-same-parent-residual-row"', clay);
  const cb23 = home.indexOf('class="tree-row clay-b-signed-mixed-pressure-row"', cb22);
  const cb24 = home.indexOf('class="tree-row clay-b-source-enstrophy-row"', cb23);
  const cb25 = home.indexOf('class="tree-row clay-b-frequency-activation-row"', cb24);
  const boundary = home.indexOf('class="tree-row clay-b-public-boundary-row"', cb25);
  assert.ok(r0 < rb && rb < divider && divider < clay && clay < cb22 && cb22 < cb23 && cb23 < cb24 && cb24 < cb25 && cb25 < boundary);
  assert.equal(home.slice(r0, divider).includes("clay-b-two-scale-row"), false);
  assert.match(home, /\.clay-b-route-tree \.tree-row::before[\s\S]*?border-left-style: dashed/);
  assert.match(home, /不把策略转向画成从 R0\.76L 推出 Clay-B 的定理依赖/);
  assert.equal((home.match(/class="route-overview independent-release-spotlight"/g) ?? []).length, 1);
  assert.equal((home.match(/id="clay-b-frequency-activation"/g) ?? []).length, 1);
  assert.equal((home.match(/id="clay-b-source-enstrophy"/g) ?? []).length, 0);
  assert.equal((literature.match(/id="clay-b-frequency-activation-boundary"/g) ?? []).length, 1);
  assert.equal((index.match(/data-note="clay-b-frequency-activation-20260907"/g) ?? []).length, 1);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 266);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.pdf$/.test(name)).length, 223);
  assert.equal(noteFiles.includes("clay-b-frequency-activation-20260907.pdf"), false);
  assert.equal(site.version, "2.69");
  assert.equal(site.latestRelease, "R0.76L");
  assert.equal(site.publicIndependentNoteCount, 25);
  assert.equal(site.latestIndependentNote, "ClayB-FrequencyActivation-20260907");
  assert.equal(site.latestIndependentResearchHtml, "/notes/clay-b-frequency-activation-20260907.html");
  assert.equal(site.latestIndependentResearchPdf, null);
  assert.equal(site.latestIndependentChapter, "CB.25");
  assert.equal(site.nextIndependentChapter, "CB.26");
  assert.equal(manifest.siteVersion, "2.69");
  assert.equal(manifest.latestCompletedRelease, "r076l");
  assert.equal(manifest.latestPublication.releaseId, "clay-b-frequency-activation-20260907");
  assert.equal(manifest.latestPublication.logicalPredecessor, "ClayB-SourceEnstrophy-20260907");
  assert.equal(manifest.latestPublication.pdfGenerated, false);
  assert.equal(manifest.latestPublication.advancesCanonicalR0Series, false);
  assert.equal(manifest.latestPublication.chapter, "CB.25");
});

test("prior note, canonical endpoint, recap, and historical PDF remain byte-exact", async () => {
  for (const [path, expected] of Object.entries(protectedArtifacts)) assert.equal(sha256(await read(path)), expected, path);
  await assert.rejects(access(resolve(root, "public/notes/clay-b-frequency-activation-20260907.pdf")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-frequency-activation-20260907.html")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-frequency-activation-20260907.pdf")));
});
