import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("../public/", import.meta.url);
const notesRoot = new URL("notes/", publicRoot);

function releaseToSlug(release) {
  const match = release.match(/^r0(\d{2})([a-z])$/);
  assert.ok(match, `unexpected release id: ${release}`);
  return `r0-${match[1]}${match[2]}`;
}

async function completedReleaseIds() {
  const files = await readdir(new URL("research/", root));
  const reports = files
    .map((file) => file.match(/^(r0\d{2}[a-z])_report-source\.md$/)?.[1])
    .filter(Boolean)
    .filter((release) => release.localeCompare("r070a") >= 0);
  return [...new Set(["r070a", ...reports])].sort();
}

test("publishes every completed research release from R0.70A onward", async () => {
  const [releases, home] = await Promise.all([
    completedReleaseIds(),
    readFile(new URL("research-review.html", publicRoot), "utf8"),
  ]);

  assert.deepEqual(releases, [
    ...Array.from({ length: 26 }, (_, index) =>
      `r070${String.fromCharCode(97 + index)}`,
    ),
    "r071a",
    "r071b",
    "r071c",
  ]);

  for (const release of releases) {
    const slug = releaseToSlug(release);
    const [html, pdf] = await Promise.all([
      readFile(new URL(`${slug}.html`, notesRoot), "utf8"),
      readFile(new URL(`${slug}.pdf`, notesRoot)),
    ]);

    const publicCode = release
      .replace(/^r0(\d{2})([a-z])$/, "R0.$1$2")
      .toUpperCase();
    assert.ok(html.includes(publicCode), `${release}: public code`);
    assert.ok(html.includes(`href="/notes/${slug}.pdf"`), `${release}: PDF link`);
    assert.ok(home.includes(`href="/notes/${slug}.html"`), `${release}: homepage link`);
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", `${release}: PDF header`);
    assert.ok(pdf.length > 10_000, `${release}: PDF is unexpectedly small`);
    assert.doesNotMatch(html, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
    assert.doesNotMatch(html, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  }
});

test("keeps homepage counts, route links, progress links, and cumulative recap synchronized", async () => {
  const [home, noteFiles, recap, recapPdf] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readdir(notesRoot),
    readFile(new URL("recap-r0-61-r0-71c.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71c.pdf", publicRoot)),
  ]);

  const htmlNotes = noteFiles.filter((file) => file.endsWith(".html"));
  assert.equal(htmlNotes.length, 127);
  assert.match(home, /<strong>127<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.71C<\/strong>最新研究节点/);
  assert.match(home, /展开 37 篇公开笔记/);
  assert.match(home, /累计回顾收录 67 个节点；全站现有 127 篇公开研究笔记/);
  assert.match(home, /href="\/recap-r0-61-r0-71c\.html"/);
  assert.match(home, /href="\/recap-r0-61-r0-71c\.pdf"/);

  const current = [
    ...Array.from({ length: 26 }, (_, index) =>
      `r0-70${String.fromCharCode(97 + index)}`,
    ),
    "r0-71a",
    "r0-71b",
    "r0-71c",
  ];
  for (const slug of current) {
    const matches = home.match(new RegExp(`href="/notes/${slug}\\.html"`, "g")) ?? [];
    assert.ok(matches.length >= 2, `${slug}: expected route and progress links`);
  }

  for (const phrase of [
    "R0.61–R0.71C",
    "收录节点：67",
    "回顾截止时公开笔记：127",
    "这些结果目前能说明什么",
    "R0.71D 只检查带完整通量的局部时间账本",
    "R0.71B–R0.71C · 正输出系数和有符号传播",
  ]) {
    assert.ok(recap.includes(phrase), phrase);
  }
  assert.doesNotMatch(
    recap,
    /CONTENTS|路线怎样一步步收缩|当前门槛|价值确认|no-go|common-response|精确账本|交换子桥/,
  );
  assert.equal(recapPdf.subarray(0, 4).toString(), "%PDF");
  assert.ok(recapPdf.length > 10_000);
});
