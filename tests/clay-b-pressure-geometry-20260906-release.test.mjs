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
  "public/notes/clay-b-two-scale-20260905.pdf": "3f6fbe49c369190c8fac999a3f67bd91918d2a73f514c9ec5b3a8e8d2316423b",
  "public/notes/clay-b-concentration-limits-20260906.html": "774508240221c02cf400b8f064ebd8333ff2eff1f728b2a578774643bfb2ce3e",
};
const independentChapters = [
  ["CB.1", "clay-b-two-scale-20260905"],
  ["CB.2", "clay-b-signed-scale-20260905"],
  ["CB.3", "clay-b-physical-adjoint-20260906"],
  ["CB.4", "clay-b-window-localisation-20260906"],
  ["CB.5", "clay-b-plateau-history-20260906"],
  ["CB.6", "clay-b-concentration-limits-20260906"],
  ["CB.7", "clay-b-pressure-geometry-20260906"],
];

test("the HTML-only PressureGeometry note is bilingual, bounded, and figure-free", async () => {
  const note = await text("public/notes/clay-b-pressure-geometry-20260906.html");
  for (const marker of [
    "ClayB-PressureGeometry-20260906",
    "CB.7",
    "压力功的符号、速度方向与临界条件",
    "Pressure-work signs, velocity direction, and the critical condition",
    "C c₀ M⁴ r⁻² L⁻⁷",
    "both pressure-work signs",
    "F∈L²_tL³_x",
    "Energy gives only F∈L²_tL²_x",
    "fixed angular cone",
    "Initial energy grows",
    "FINITE: NONE",
    "OPEN",
    "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.equal((note.match(/<main data-language="zh">/g) ?? []).length, 1);
  assert.equal((note.match(/<main data-language="en">/g) ?? []).length, 1);
  assert.equal((note.match(/<section>/g) ?? []).length, 16);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(note.includes("/notes/clay-b-pressure-geometry-20260906.pdf"), false);
  assert.equal(note.includes("R0.76M"), false);
});

test("the homepage keeps the solid R0 sequence separate from the dashed CB.1–CB.7 lane", async () => {
  const [home, literature, index, site, manifest, noteFiles] = await Promise.all([
    text("public/research-review.html"),
    text("public/literature-review.html"),
    text("public/notes/index.html"),
    text("public/site-version.json").then(JSON.parse),
    text("research/release-manifest.json").then(JSON.parse),
    readdir(resolve(root, "public/notes")),
  ]);
  for (const page of [home, literature, index]) assert.ok(page.includes("clay-b-pressure-geometry-20260906"));
  const r0Start = home.indexOf('class="route-tree r0-route-tree"');
  const r0Boundary = home.indexOf('class="tree-row r0-public-boundary-row"', r0Start);
  const laneDivider = home.indexOf('class="route-lane-divider"', r0Boundary);
  const clayStart = home.indexOf('class="route-tree clay-b-route-tree"', laneDivider);
  const clayBoundary = home.indexOf('class="tree-row clay-b-public-boundary-row"', clayStart);
  assert.ok(r0Start >= 0 && r0Start < r0Boundary && r0Boundary < laneDivider && laneDivider < clayStart && clayStart < clayBoundary);
  assert.equal(home.slice(r0Start, laneDivider).includes("clay-b-two-scale-row"), false);
  assert.match(home, /\.clay-b-route-tree \.tree-row::before[\s\S]*?border-left-style: dashed/);
  assert.match(home, /不声明由 R0\.76L 直接推出/);
  const positions = independentChapters.map(([chapter, slug]) => {
    const row = home.indexOf(`class="tree-row ${slug.replace(/-2026090[56]$/, "")}-row"`, clayStart);
    assert.ok(row >= clayStart && row < clayBoundary, `${chapter} row position`);
    assert.ok(home.slice(row, row + 1100).includes(chapter), `${chapter} route label`);
    return row;
  });
  assert.deepEqual(positions, [...positions].sort((a, b) => a - b));
  assert.equal((home.match(/class="route-overview independent-release-spotlight"/g) ?? []).length, 1);
  assert.equal((home.match(/id="clay-b-pressure-geometry"/g) ?? []).length, 1);
  assert.equal((literature.match(/id="clay-b-pressure-geometry-boundary"/g) ?? []).length, 1);
  assert.equal((index.match(/data-note="clay-b-pressure-geometry-20260906"/g) ?? []).length, 1);
  for (const [chapter, slug] of independentChapters) {
    const note = await text(`public/notes/${slug}.html`);
    assert.ok(note.includes(chapter), `${chapter} note`);
    assert.match(index, new RegExp(`data-note="${slug}"[\\s\\S]*?class="note-code">${chapter.replace(".", "\\.")} ·`));
    assert.ok(literature.includes(`${chapter} · ClayB-`), `${chapter} literature boundary`);
  }
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 266);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.pdf$/.test(name)).length, 223);
  assert.equal(noteFiles.includes("clay-b-pressure-geometry-20260906.pdf"), false);
  assert.equal(site.version, "2.51");
  assert.equal(site.latestRelease, "R0.76L");
  assert.equal(site.publicIndependentNoteCount, 7);
  assert.equal(site.latestIndependentNote, "ClayB-PressureGeometry-20260906");
  assert.equal(site.latestIndependentResearchHtml, "/notes/clay-b-pressure-geometry-20260906.html");
  assert.equal(site.latestIndependentResearchPdf, null);
  assert.equal(site.independentChapterScheme, "CB.n");
  assert.equal(site.latestIndependentChapter, "CB.7");
  assert.equal(site.nextIndependentChapter, "CB.8");
  assert.equal(manifest.siteVersion, "2.51");
  assert.equal(manifest.latestCompletedRelease, "r076l");
  assert.equal(manifest.latestCompletedStep, 63);
  assert.equal(manifest.latestPublication.releaseId, "clay-b-pressure-geometry-20260906");
  assert.equal(manifest.latestPublication.logicalPredecessor, "ClayB-ConcentrationLimits-20260906");
  assert.equal(manifest.latestPublication.pdfGenerated, false);
  assert.equal(manifest.latestPublication.advancesCanonicalR0Series, false);
  assert.equal(manifest.latestPublication.chapter, "CB.7");
});

test("historical milestones, endpoint, prior note, and retained PDFs remain byte-exact", async () => {
  for (const [path, expected] of Object.entries(protectedArtifacts)) assert.equal(sha256(await read(path)), expected, path);
  await assert.rejects(access(resolve(root, "public/notes/clay-b-pressure-geometry-20260906.pdf")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-pressure-geometry-20260906.html")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-pressure-geometry-20260906.pdf")));
});
