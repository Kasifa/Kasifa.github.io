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
  "public/notes/r0-76l.html": "78085c5f2772e4b719004a1e9698147f84d84db73485ddcba2cf155c812e48b2",
  "public/notes/r0-76l.pdf": "3facbf01db259bf6ce2c247f0979b41ea64fe11be88c6c9b7a15a2d0d81d7ad8",
  "public/notes/clay-b-plateau-history-20260906.html": "abaac5473dc9043cb209a1ad5bee8bd788fa8eb3ee715df4f1b74f8990066e66",
  "public/notes/clay-b-window-localisation-20260906.html": "83ed7410121996d0d121b54d4af1e6b481b1c51d158ddda8ffa6181261a414f6",
  "public/notes/clay-b-two-scale-20260905.pdf": "3f6fbe49c369190c8fac999a3f67bd91918d2a73f514c9ec5b3a8e8d2316423b",
};

test("the HTML-only ConcentrationLimits note is bilingual, bounded, and figure-free", async () => {
  const note = await text("public/notes/clay-b-concentration-limits-20260906.html");
  for (const marker of [
    "ClayB-ConcentrationLimits-20260906",
    "固定球集中之后，还缺少什么",
    "What remains after fixed-ball concentration",
    "LITERATURE CONDITIONAL",
    "typographical interpretation",
    "solution-dependent",
    "not an NS",
    "growing initial energy",
    "t_B/r²→0",
    "bare far-source pressure impulse",
    "not velocity-weighted pressure work",
    "AA.18",
    "FINITE: NONE",
    "OPEN",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.equal((note.match(/<main data-language="zh">/g) ?? []).length, 1);
  assert.equal((note.match(/<main data-language="en">/g) ?? []).length, 1);
  assert.equal((note.match(/<section>/g) ?? []).length, 16);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(note.includes("/notes/clay-b-concentration-limits-20260906.pdf"), false);
  assert.equal(note.includes("R0.76M"), false);
});

test("the concentration-limits node continues the existing homepage roadmap and remains its sole independent spotlight", async () => {
  const [home, literature, index, site, manifest, noteFiles] = await Promise.all([
    text("public/research-review.html"),
    text("public/literature-review.html"),
    text("public/notes/index.html"),
    text("public/site-version.json").then(JSON.parse),
    text("research/release-manifest.json").then(JSON.parse),
    readdir(resolve(root, "public/notes")),
  ]);
  for (const page of [home, literature, index]) assert.ok(page.includes("clay-b-concentration-limits-20260906"));
  const routeStart = home.indexOf('<div class="route-tree"');
  const windowRow = home.indexOf('class="tree-row clay-b-window-localisation-row"', routeStart);
  const plateauRow = home.indexOf('class="tree-row clay-b-plateau-history-row"', routeStart);
  const concentrationRow = home.indexOf('class="tree-row clay-b-concentration-limits-row"', routeStart);
  const nextBoundary = home.indexOf("NEXT · NOT AUTHORIZED", routeStart);
  assert.ok(routeStart >= 0 && windowRow < plateauRow && plateauRow < concentrationRow && concentrationRow < nextBoundary);
  const route = home.slice(concentrationRow, nextBoundary);
  for (const marker of ["固定球文献输入 L", "固定 R 原路径 P", "解依赖慢对角半径 D", "精确能量非 NS 模型 M/N", "AA.1–AA.15", "裸远源压力冲量 AA.16–AA.18", "近源压力与黏性 OPEN"]) assert.ok(route.includes(marker), marker);
  assert.equal((home.match(/class="route-overview independent-release-spotlight"/g) ?? []).length, 1);
  assert.equal((home.match(/id="clay-b-concentration-limits"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="clay-b-concentration-limits-boundary"/g) ?? []).length, 1);
  assert.equal((index.match(/data-note="clay-b-concentration-limits-20260906"/g) ?? []).length, 1);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 266);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.pdf$/.test(name)).length, 223);
  assert.equal(noteFiles.includes("clay-b-concentration-limits-20260906.pdf"), false);
  assert.equal(site.version, "2.49");
  assert.equal(site.latestRelease, "R0.76L");
  assert.equal(site.publicIndependentNoteCount, 6);
  assert.equal(site.latestIndependentNote, "ClayB-ConcentrationLimits-20260906");
  assert.equal(site.latestIndependentResearchHtml, "/notes/clay-b-concentration-limits-20260906.html");
  assert.equal(site.latestIndependentResearchPdf, null);
  assert.equal(manifest.siteVersion, "2.49");
  assert.equal(manifest.latestCompletedRelease, "r076l");
  assert.equal(manifest.latestCompletedStep, 63);
  assert.equal(manifest.latestPublication.releaseId, "clay-b-concentration-limits-20260906");
  assert.equal(manifest.latestPublication.logicalPredecessor, "ClayB-PlateauHistory-20260906");
  assert.equal(manifest.latestPublication.pdfGenerated, false);
  assert.equal(manifest.latestPublication.advancesCanonicalR0Series, false);
});

test("historical milestone, earlier independent notes, and PDF assets remain byte-exact", async () => {
  for (const [path, expected] of Object.entries(protectedArtifacts)) assert.equal(sha256(await read(path)), expected, path);
  await assert.rejects(access(resolve(root, "public/notes/clay-b-concentration-limits-20260906.pdf")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-concentration-limits-20260906.html")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-concentration-limits-20260906.pdf")));
});
