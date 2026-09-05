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
  "public/notes/clay-b-two-scale-20260905.html": "5c4a52ddc000a5f329c2adb238d66dc34db532dddd3d8e6e97e791c954749e09",
  "public/notes/clay-b-two-scale-20260905.pdf": "3f6fbe49c369190c8fac999a3f67bd91918d2a73f514c9ec5b3a8e8d2316423b",
};

test("the HTML-only PhysicalAdjoint note is bilingual, bounded, and figure-free", async () => {
  const note = await text("public/notes/clay-b-physical-adjoint-20260906.html");
  for (const marker of [
    "ClayB-PhysicalAdjoint-20260906",
    "伴随测试的定位代价",
    "The localization cost of an adjoint test",
    "PROVED LOCALLY",
    "LITERATURE",
    "FINITE: NONE",
    "OPEN",
    "NOT CLAY",
    "B.1–B.5",
    "B.6–B.13",
    "B.14–B.16",
    "C.1–C.6",
    "Initial L2 and H1 are both nonuniform",
  ]) assert.ok(note.includes(marker), marker);
  assert.equal((note.match(/<main data-language="zh">/g) ?? []).length, 1);
  assert.equal((note.match(/<main data-language="en">/g) ?? []).length, 1);
  assert.equal((note.match(/<section>/g) ?? []).length, 16);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(note.includes("/notes/clay-b-physical-adjoint-20260906.pdf"), false);
  assert.equal(note.includes("R0.76M"), true);
  assert.match(note, /does not occupy R0\.76M/);
});

test("the adjusted-strategy work is part of the homepage route tree", async () => {
  const [home, literature, index, site, manifest, noteFiles] = await Promise.all([
    text("public/research-review.html"),
    text("public/literature-review.html"),
    text("public/notes/index.html"),
    text("public/site-version.json").then(JSON.parse),
    text("research/release-manifest.json").then(JSON.parse),
    readdir(resolve(root, "public/notes")),
  ]);
  for (const page of [home, literature, index]) assert.ok(page.includes("clay-b-physical-adjoint-20260906"));
  const routeStart = home.indexOf('<div class="route-tree"');
  const signedRow = home.indexOf('class="tree-row clay-b-signed-scale-row"', routeStart);
  const adjointRow = home.indexOf('class="tree-row clay-b-physical-adjoint-row"', routeStart);
  const nextBoundary = home.indexOf("NEXT · NOT AUTHORIZED", routeStart);
  assert.ok(routeStart >= 0 && signedRow < adjointRow && adjointRow < nextBoundary);
  assert.ok(home.slice(adjointRow, nextBoundary).includes("原计时合同持留/上穿输入"));
  assert.equal((home.match(/id="clay-b-physical-adjoint"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="clay-b-physical-adjoint-boundary"/g) ?? []).length, 1);
  assert.equal((index.match(/data-note="clay-b-physical-adjoint-20260906"/g) ?? []).length, 1);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 266);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.pdf$/.test(name)).length, 223);
  assert.equal(noteFiles.includes("clay-b-physical-adjoint-20260906.pdf"), false);
  assert.equal(site.version, "2.45");
  assert.equal(site.latestRelease, "R0.76L");
  assert.equal(site.publicIndependentNoteCount, 3);
  assert.equal(site.latestIndependentNote, "ClayB-PhysicalAdjoint-20260906");
  assert.equal(site.latestIndependentResearchPdf, null);
  assert.equal(manifest.siteVersion, "2.45");
  assert.equal(manifest.latestCompletedRelease, "r076l");
  assert.equal(manifest.latestCompletedStep, 63);
  assert.equal(manifest.latestPublication.releaseId, "clay-b-physical-adjoint-20260906");
  assert.equal(manifest.latestPublication.pdfGenerated, false);
  assert.equal(manifest.latestPublication.advancesCanonicalR0Series, false);
});

test("historical milestone and PDF assets remain byte-exact", async () => {
  for (const [path, expected] of Object.entries(protectedArtifacts)) {
    assert.equal(sha256(await read(path)), expected, path);
  }
  await assert.rejects(access(resolve(root, "public/notes/clay-b-physical-adjoint-20260906.pdf")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-physical-adjoint-20260906.html")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-physical-adjoint-20260906.pdf")));
});
