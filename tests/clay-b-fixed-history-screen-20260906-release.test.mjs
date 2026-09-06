import test from "node:test";
import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { resolve } from "node:path";

const root = resolve(import.meta.dirname, "..");
const read = (path) => readFile(resolve(root, path));
const text = async (path) => (await read(path)).toString("utf8");
const sha256 = (value) => createHash("sha256").update(value).digest("hex");
const protectedArtifacts = {
  "public/notes/clay-b-ancient-constant-screen-20260906.html": "9a025810a239657e4722a001cbeb71adcd4c3959801c582b51662a789afdf35c",
  "public/recap-r0-61-r0-76i.html": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9",
  "public/recap-r0-61-r0-76i.pdf": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98",
  "public/notes/r0-76l.html": "78085c5f2772e4b719004a1e9698147f84d84db73485ddcba2cf155c812e48b2",
  "public/notes/r0-76l.pdf": "3facbf01db259bf6ce2c247f0979b41ea64fe11be88c6c9b7a15a2d0d81d7ad8",
  "public/notes/clay-b-two-scale-20260905.pdf": "3f6fbe49c369190c8fac999a3f67bd91918d2a73f514c9ec5b3a8e8d2316423b",
};
const independentChapters = [
  ["CB.1", "clay-b-two-scale-20260905"], ["CB.2", "clay-b-signed-scale-20260905"],
  ["CB.3", "clay-b-physical-adjoint-20260906"], ["CB.4", "clay-b-window-localisation-20260906"],
  ["CB.5", "clay-b-plateau-history-20260906"], ["CB.6", "clay-b-concentration-limits-20260906"],
  ["CB.7", "clay-b-pressure-geometry-20260906"], ["CB.8", "clay-b-pressure-quotient-20260906"],
  ["CB.9", "clay-b-pressure-work-window-20260906"], ["CB.10", "clay-b-bad-time-net-work-20260906"],
  ["CB.11", "clay-b-pressure-test-coupling-20260906"], ["CB.12", "clay-b-lagged-pressure-reduction-20260906"],
  ["CB.13", "clay-b-recent-source-screen-20260906"], ["CB.14", "clay-b-pressure-mechanism-screen-20260906"],
  ["CB.15", "clay-b-ancient-constant-screen-20260906"], ["CB.16", "clay-b-fixed-history-screen-20260906"],
];

test("the HTML-only FixedHistoryScreen note is bilingual, bounded, and figure-free", async () => {
  const note = await text("public/notes/clay-b-fixed-history-screen-20260906.html");
  for (const marker of [
    "ClayB-FixedHistoryScreen-20260906", "CB.16", "完整历史支付增长窗口外", "complete history pays the tail outside a growing window",
    "固定窗口的完整 mild 分解", "fixed-window complete mild decomposition", "record 倍增的局部寿命", "Local lifetime bounds record doubling",
    "标量反检查只否定时间账本", "scalar countercheck targets only the time-ledger inference", "不同缩放的初始胞 L³", "Initial cell L³ identities for different rescalings",
    "PROVED IN STATED SCOPE", "CONDITIONAL ANCIENT BRANCH", "FINITE CHECKS ONLY", "QUANTIFIER BOUNDARY", "OPEN", "NOT CLAY",
  ]) assert.ok(note.includes(marker), marker);
  assert.equal((note.match(/<main data-language="zh">/g) ?? []).length, 1);
  assert.equal((note.match(/<main data-language="en">/g) ?? []).length, 1);
  assert.equal((note.match(/<section>/g) ?? []).length, 16);
  assert.equal((note.match(/<img\b/g) ?? []).length, 0);
  assert.equal(note.includes("/notes/clay-b-fixed-history-screen-20260906.pdf"), false);
  assert.equal(note.includes("R0.76M"), false);
});

test("homepage keeps the solid R0 sequence separate from the dashed CB.1–CB.16 lane", async () => {
  const [home, literature, index, site, manifest, noteFiles] = await Promise.all([
    text("public/research-review.html"), text("public/literature-review.html"), text("public/notes/index.html"),
    text("public/site-version.json").then(JSON.parse), text("research/release-manifest.json").then(JSON.parse), readdir(resolve(root, "public/notes")),
  ]);
  for (const page of [home, literature, index]) assert.ok(page.includes("clay-b-fixed-history-screen-20260906"));
  const r0Start = home.indexOf('class="route-tree r0-route-tree"');
  const r0Boundary = home.indexOf('class="tree-row r0-public-boundary-row"', r0Start);
  const laneDivider = home.indexOf('class="route-lane-divider"', r0Boundary);
  const clayStart = home.indexOf('class="route-tree clay-b-route-tree"', laneDivider);
  const clayBoundary = home.indexOf('class="tree-row clay-b-public-boundary-row"', clayStart);
  assert.ok(r0Start >= 0 && r0Start < r0Boundary && r0Boundary < laneDivider && laneDivider < clayStart && clayStart < clayBoundary);
  assert.equal(home.slice(r0Start, laneDivider).includes("clay-b-two-scale-row"), false);
  assert.match(home, /\.clay-b-route-tree \.tree-row::before[\s\S]*?border-left-style: dashed/);
  assert.match(home, /不把策略转向画成从 R0\.76L 推出 Clay-B 的定理依赖/);
  const positions = independentChapters.map(([chapter, slug]) => {
    const rowClass = slug.replace(/-2026090[56]$/, "") + "-row";
    const row = home.indexOf(`class="tree-row ${rowClass}"`, clayStart);
    assert.ok(row >= clayStart && row < clayBoundary, `${chapter} row position`);
    assert.ok(home.slice(row, row + 2200).includes(chapter), `${chapter} route label`);
    return row;
  });
  assert.deepEqual(positions, [...positions].sort((a, b) => a - b));
  assert.equal((home.match(/class="route-overview independent-release-spotlight"/g) ?? []).length, 1);
  assert.equal((home.match(/id="clay-b-fixed-history-screen"/g) ?? []).length, 1);
  assert.equal((home.match(/id="clay-b-ancient-constant-screen"/g) ?? []).length, 0);
  assert.equal((literature.match(/id="clay-b-fixed-history-screen-boundary"/g) ?? []).length, 1);
  assert.equal((index.match(/data-note="clay-b-fixed-history-screen-20260906"/g) ?? []).length, 1);
  for (const [chapter, slug] of independentChapters) {
    const note = await text(`public/notes/${slug}.html`);
    assert.ok(note.includes(chapter), `${chapter} note`);
    assert.match(index, new RegExp(`data-note="${slug}"[\\s\\S]*?class="note-code">${chapter.replace(".", "\\.")} ·`));
    assert.ok(literature.includes(`${chapter} · ClayB-`), `${chapter} literature boundary`);
  }
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 266);
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.pdf$/.test(name)).length, 223);
  assert.equal(noteFiles.includes("clay-b-fixed-history-screen-20260906.pdf"), false);
  assert.equal(site.version, "2.60");
  assert.equal(site.latestRelease, "R0.76L");
  assert.equal(site.publicIndependentNoteCount, 16);
  assert.equal(site.latestIndependentNote, "ClayB-FixedHistoryScreen-20260906");
  assert.equal(site.latestIndependentResearchHtml, "/notes/clay-b-fixed-history-screen-20260906.html");
  assert.equal(site.latestIndependentResearchPdf, null);
  assert.equal(site.latestIndependentChapter, "CB.16");
  assert.equal(site.nextIndependentChapter, "CB.17");
  assert.equal(manifest.siteVersion, "2.60");
  assert.equal(manifest.latestCompletedRelease, "r076l");
  assert.equal(manifest.latestPublication.releaseId, "clay-b-fixed-history-screen-20260906");
  assert.equal(manifest.latestPublication.logicalPredecessor, "ClayB-AncientConstantScreen-20260906");
  assert.equal(manifest.latestPublication.pdfGenerated, false);
  assert.equal(manifest.latestPublication.advancesCanonicalR0Series, false);
  assert.equal(manifest.latestPublication.chapter, "CB.16");
});

test("historical milestones, endpoint, prior note, and retained PDFs remain byte-exact", async () => {
  for (const [path, expected] of Object.entries(protectedArtifacts)) assert.equal(sha256(await read(path)), expected, path);
  await assert.rejects(access(resolve(root, "public/notes/clay-b-fixed-history-screen-20260906.pdf")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-fixed-history-screen-20260906.html")));
  await assert.rejects(access(resolve(root, "public/recap-clay-b-fixed-history-screen-20260906.pdf")));
});
