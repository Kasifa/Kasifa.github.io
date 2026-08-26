import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("../public/", import.meta.url);
const notesRoot = new URL("notes/", publicRoot);

function releaseToSlug(release) {
  const match = release.match(/^r0(\d{2})([a-z])$/);
  assert.ok(match, "unexpected release id: " + release);
  return "r0-" + match[1] + match[2];
}

function releaseToPublicCode(release) {
  return release
    .replace(/^r0(\d{2})([a-z])$/, "R0.$1$2")
    .toUpperCase();
}

function nextReleaseId(release) {
  const match = release.match(/^r0(\d{2})([a-z])$/);
  assert.ok(match, "unexpected release id: " + release);
  if (match[2] === "z") {
    return "r0" + String(Number(match[1]) + 1).padStart(2, "0") + "a";
  }
  const nextLetter = String.fromCharCode(match[2].charCodeAt(0) + 1);
  return "r0" + match[1] + nextLetter;
}

function nextPublicCode(release) {
  return releaseToPublicCode(nextReleaseId(release));
}

test("rolls the publication code across an alphabet boundary", () => {
  assert.equal(nextReleaseId("r071z"), "r072a");
  assert.equal(nextPublicCode("r071z"), "R0.72A");
});

async function completedReleaseIds() {
  const files = await readdir(new URL("research/", root));
  const reports = files
    .map((file) => file.match(/^(r0\d{2}[a-z])_report-source\.md$/)?.[1])
    .filter(Boolean)
    .filter((release) => release.localeCompare("r070a") >= 0);
  return [...new Set(["r070a", ...reports])].sort();
}

function publicReleaseId(file) {
  const match = file.match(/^r0-(\d{2})([a-z])\.html$/);
  if (!match) return null;
  const release = "r0" + match[1] + match[2];
  return release.localeCompare("r070a") >= 0 ? release : null;
}

test("keeps every synchronized public note PDF discoverable from its note", async () => {
  const noteFiles = await readdir(notesRoot);
  const notePdfs = noteFiles.filter((file) => /^r0-.+\.pdf$/.test(file)).sort();

  assert.ok(notePdfs.length > 0, "public note PDF inventory is empty");
  for (const pdf of notePdfs) {
    const htmlFile = pdf.replace(/\.pdf$/, ".html");
    assert.ok(
      noteFiles.includes(htmlFile),
      pdf + ": matching public HTML note is missing",
    );
    const html = await readFile(new URL(htmlFile, notesRoot), "utf8");
    assert.ok(
      html.includes('href="/notes/' + pdf + '"'),
      pdf + ": synchronized PDF download link is missing from its note",
    );
  }
});

test("publishes every completed research release from R0.70A onward", async () => {
  const [releases, home, literature, noteFiles] = await Promise.all([
    completedReleaseIds(),
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
    readdir(notesRoot),
  ]);

  const publicReleases = noteFiles.map(publicReleaseId).filter(Boolean).sort();
  const progressReleases = [
    ...home.matchAll(/data-release="(r0\d{2}[a-z])"/g),
  ]
    .map((match) => match[1])
    .filter((release) => release.localeCompare("r070a") >= 0)
    .sort();

  assert.deepEqual(
    publicReleases,
    releases,
    "every R0.70A+ public note must correspond to a completed release",
  );
  assert.deepEqual(
    progressReleases,
    releases,
    "every R0.70A+ completed release must have exactly one progress card",
  );

  assert.equal(releases[0], "r070a");
  for (let index = 1; index < releases.length; index += 1) {
    const expected = nextReleaseId(releases[index - 1]);
    assert.equal(
      releases[index],
      expected,
      "a completed release is missing before " + expected,
    );
  }

  for (const release of releases) {
    const slug = releaseToSlug(release);
    const [html, pdf] = await Promise.all([
      readFile(new URL(slug + ".html", notesRoot), "utf8"),
      readFile(new URL(slug + ".pdf", notesRoot)),
    ]);

    const publicCode = releaseToPublicCode(release);
    assert.ok(html.includes(publicCode), release + ": public code");
    assert.ok(
      html.includes('href="/notes/' + slug + '.pdf"'),
      release + ": PDF link",
    );
    assert.ok(
      home.includes('href="/notes/' + slug + '.html"'),
      release + ": homepage link",
    );
    assert.ok(
      literature.includes('href="/notes/' + slug + '.html"'),
      release + ": literature-review direct link",
    );
    const cardMarker = 'data-release="' + release + '"';
    const markerMatches = home.match(new RegExp(cardMarker, "g")) ?? [];
    assert.equal(markerMatches.length, 1, release + ": one progress card");
    const cardStart = home.indexOf(cardMarker);
    const nextCard = home.indexOf('data-release="', cardStart + cardMarker.length);
    const card = home.slice(cardStart, nextCard < 0 ? home.length : nextCard);
    assert.ok(
      home.includes(
        '<div class="task-one" id="' + release + '" ' + cardMarker,
      ),
      release + ": progress card structure",
    );
    assert.ok(card.includes(publicCode), release + ": visible progress-card code");
    assert.ok(
      card.includes('href="/notes/' + slug + '.html"'),
      release + ": progress card note link",
    );
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", release + ": PDF header");
    assert.ok(pdf.length > 10_000, release + ": PDF is unexpectedly small");
    assert.doesNotMatch(html, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
    assert.doesNotMatch(html, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(html, /\t/);
  }
});

test("derives homepage counts, latest release, route size, and recap endpoint", async () => {
  const [releases, home, literature, noteFiles] = await Promise.all([
    completedReleaseIds(),
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
    readdir(notesRoot),
  ]);

  const htmlNotes = noteFiles.filter((file) => file.endsWith(".html"));
  const latestRelease = releases.at(-1);
  const latestSlug = releaseToSlug(latestRelease);
  const latestCode = releaseToPublicCode(latestRelease);
  const nextCode = nextPublicCode(latestRelease);
  const recapStem = "recap-r0-61-" + latestSlug;
  const routeStart = home.indexOf('<section class="route-overview"');
  const routeEnd = home.indexOf('<div class="page-shell">', routeStart);
  assert.ok(routeStart >= 0 && routeEnd > routeStart, "homepage route map");
  const route = home.slice(routeStart, routeEnd);
  const routeLinks = [
    ...route.matchAll(/href="(\/notes\/r0-[^"]+\.html)"/g),
  ].map((match) => match[1]);
  const publicNoteLinks = htmlNotes.map((file) => "/notes/" + file).sort();
  assert.equal(new Set(routeLinks).size, routeLinks.length, "unique route links");
  assert.deepEqual([...routeLinks].sort(), publicNoteLinks);

  const recapStart = routeLinks.indexOf("/notes/r0-61.html");
  assert.ok(recapStart >= 0, "R0.61 recap start is missing from route");
  const recapNodes = routeLinks.length - recapStart;
  const detailsBlocks = [
    ...route.matchAll(
      /<details class="tree-notes"[^>]*>([\s\S]*?)<\/details>/g,
    ),
  ];
  const currentDetails = detailsBlocks.at(-1)?.[1] ?? "";
  const currentRouteNotes = (
    currentDetails.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []
  ).length;
  assert.ok(currentRouteNotes > 0, "current route note list is empty");
  assert.ok(releases.length >= 1, "completed release list is empty");
  assert.equal(
    htmlNotes.length,
    routeLinks.length,
    "homepage route must enumerate every public HTML note exactly once",
  );
  const [latestNote, recap, recapPdf] = await Promise.all([
    readFile(new URL(latestSlug + ".html", notesRoot), "utf8"),
    readFile(new URL(recapStem + ".html", publicRoot), "utf8"),
    readFile(new URL(recapStem + ".pdf", publicRoot)),
  ]);

  const nodeIndexStart = recap.indexOf('<section id="node-index">');
  const nodeIndexEnd = recap.indexOf("</section>", nodeIndexStart);
  assert.ok(
    nodeIndexStart >= 0 && nodeIndexEnd > nodeIndexStart,
    "current recap node index",
  );
  const recapIndex = recap.slice(nodeIndexStart, nodeIndexEnd);
  const recapIndexLinks = [
    ...recapIndex.matchAll(/href="(\/notes\/r0-[^"]+\.html)"/g),
  ].map((match) => match[1]);
  assert.deepEqual(
    recapIndexLinks,
    routeLinks.slice(recapStart),
    "current recap must index every post-R0.60 route node exactly once",
  );

  const versionMatch = home.match(/<strong>v(\d+\.\d+)<\/strong>\u7f51\u9875\u7248\u672c/);
  assert.ok(versionMatch, "homepage version marker is missing");
  const version = versionMatch[1];
  assert.match(version, /^\d+\.\d+$/, "current publication version format");
  for (const [label, html] of [
    ["homepage", home],
    ["literature", literature],
    ["latest note", latestNote],
    ["current recap", recap],
  ]) {
    assert.ok(
      html.includes('src="/i18n-en.js?v=' + version + '"'),
      label + ": i18n cache version must match homepage v" + version,
    );
  }
  assert.ok(
    home.includes("\u7efc\u8ff0 v" + version + " \u00b7"),
    "homepage footer version must match metadata",
  );
  assert.ok(
    literature.includes("\u6587\u732e\u7efc\u8ff0 v" + version + " \u00b7"),
    "literature footer version must match homepage metadata",
  );

  assert.ok(htmlNotes.length > 60);
  const homepageCountMatches = [
    ...home.matchAll(/<strong>(\d+)<\/strong>公开研究笔记/g),
  ];
  assert.equal(
    homepageCountMatches.length,
    1,
    "homepage must expose one canonical public-note count",
  );
  assert.equal(
    Number(homepageCountMatches[0][1]),
    htmlNotes.length,
    "homepage public-note count must equal public HTML notes",
  );
  assert.ok(
    home.includes("<strong>" + latestCode + "</strong>最新研究节点"),
  );
  assert.ok(home.includes("展开 " + currentRouteNotes + " 篇公开笔记"));
  assert.ok(
    home.includes(
      "累计回顾收录 " +
        recapNodes +
        " 个节点；全站现有 " +
        htmlNotes.length +
        " 篇公开研究笔记",
    ),
  );
  assert.ok(home.includes('href="/' + recapStem + '.html"'));
  assert.ok(home.includes('href="/' + recapStem + '.pdf"'));
  assert.ok(recap.includes('href="/' + recapStem + '.pdf"'));
  assert.ok(home.includes("NEXT · " + nextCode));
  assert.ok(literature.includes("R0.69P–" + latestCode));
  assert.ok(literature.includes("开放接口 · " + nextCode));
  assert.ok(latestNote.includes('href="/' + recapStem + '.html"'));
  assert.ok(latestNote.includes('href="/' + recapStem + '.pdf"'));

  for (const release of releases) {
    const slug = releaseToSlug(release);
    const pattern = new RegExp('href="/notes/' + slug + '\\.html"', "g");
    const matches = home.match(pattern) ?? [];
    assert.equal(
      matches.length,
      2,
      slug + ": expected exactly one route and one progress link",
    );
  }

  for (const phrase of [
    "R0.61–" + latestCode,
    "收录节点：" + recapNodes,
    "回顾截止时公开笔记：" + htmlNotes.length,
    nextCode,
    latestCode,
  ]) {
    assert.ok(recap.includes(phrase), phrase);
  }
  assert.match(recap, /id="retained"/);
  for (const token of ["projected-Lamb", "\\mathcal V\\in L_t^1", "2K^2"]) {
    assert.ok(recap.includes(token), token);
  }
  assert.doesNotMatch(
    recap,
    /CONTENTS|路线怎样一步步收缩|当前门槛|价值确认|common-response|精确账本|交换子桥/,
  );
  assert.equal(recapPdf.subarray(0, 4).toString(), "%PDF");
  assert.ok(recapPdf.length > 10_000);
});
