import assert from "node:assert/strict";
import { access, readdir, readFile } from "node:fs/promises";
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

async function releaseManifest() {
  return JSON.parse(
    await readFile(new URL("research/release-manifest.json", root), "utf8"),
  );
}

async function formalArchiveInventory() {
  return JSON.parse(
    await readFile(
      new URL("research/formal-archive-inventory.json", root),
      "utf8",
    ),
  );
}

async function publishedReleaseIds() {
  const manifest = await releaseManifest();
  const first = manifest.firstPdfRequiredRelease;
  const latest = manifest.latestCompletedRelease;
  assert.match(first, /^r0\d{2}[a-z]$/, "manifest first release");
  assert.match(latest, /^r0\d{2}[a-z]$/, "manifest latest release");
  assert.ok(
    first.localeCompare(latest) <= 0,
    "manifest release range must be nonempty",
  );

  const releases = [];
  let current = first;
  while (current.localeCompare(latest) <= 0) {
    releases.push(current);
    if (current === latest) break;
    current = nextReleaseId(current);
  }
  assert.equal(releases.at(-1), latest, "manifest release range must close");
  return releases;
}

async function archivedFigureManifests(directory = new URL("figures/", root)) {
  const manifests = [];
  const entries = await readdir(directory, { withFileTypes: true });
  for (const entry of entries) {
    const target = new URL(entry.name + (entry.isDirectory() ? "/" : ""), directory);
    if (entry.isDirectory()) {
      manifests.push(...(await archivedFigureManifests(target)));
    } else if (entry.name === "manifest.json") {
      manifests.push({
        path: decodeURIComponent(target.pathname).replace(
          decodeURIComponent(root.pathname),
          "",
        ),
        value: JSON.parse(await readFile(target, "utf8")),
      });
    }
  }
  return manifests;
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

test("publishes every research release from R0.70A onward", async () => {
  const [releases, home, literature, noteFiles] = await Promise.all([
    publishedReleaseIds(),
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
    "every R0.70A+ public note must correspond to a published release",
  );
  assert.deepEqual(
    progressReleases,
    releases,
    "every R0.70A+ published release must have exactly one progress card",
  );

  assert.equal(releases[0], "r070a");
  for (let index = 1; index < releases.length; index += 1) {
    const expected = nextReleaseId(releases[index - 1]);
    assert.equal(
      releases[index],
      expected,
      "a published release is missing before " + expected,
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
  const [releases, manifest, home, literature, noteFiles] = await Promise.all([
    publishedReleaseIds(),
    releaseManifest(),
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
  assert.ok(releases.length >= 1, "published release list is empty");
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
  assert.equal(version, manifest.siteVersion, "manifest site version");
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
  assert.equal(
    htmlNotes.length,
    manifest.publicHtmlNoteCount,
    "manifest public-note count",
  );
  assert.equal(
    recapNodes,
    manifest.postR060RecapNodeCount,
    "manifest post-R0.60 recap count",
  );
  assert.equal(
    releases.length,
    manifest.postR070APublishedReleaseCount,
    "manifest published-release count",
  );
  assert.equal(
    nextReleaseId(latestRelease),
    manifest.nextRelease,
    "manifest next release",
  );
  assert.match(
    manifest.latestReleaseGate,
    /^tests\/r0\d{2}[a-z][a-z0-9-]*-gate\.test\.mjs$/,
    "manifest latest-release gate path",
  );
  await access(new URL(manifest.latestReleaseGate, root));
  assert.ok(
    manifest.latestReleaseGate.startsWith("tests/" + latestRelease),
    "latest-release gate must advance with the published endpoint",
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

test("separates the published inventory from the formal-sealed archive", async () => {
  const [releases, releaseIndex, archive, figureManifests, figureDirectories] =
    await Promise.all([
      publishedReleaseIds(),
      releaseManifest(),
      formalArchiveInventory(),
      archivedFigureManifests(),
      readdir(new URL("figures/", root), { withFileTypes: true }),
    ]);

  assert.equal(archive.schemaVersion, "formal-archive-inventory-v1");
  assert.equal(archive.contractStart, "r070a");
  assert.equal(archive.latestPublishedRelease, releases.at(-1));
  assert.deepEqual(archive.publishedReleases, releases);
  assert.equal(archive.latestPublishedRelease, "r072l");
  assert.equal(archive.publishedReleaseCount, releases.length);
  assert.equal(archive.publishedReleaseCount, 64);
  assert.equal(
    archive.formalSealedReleaseCount,
    archive.formalSealedReleases.length,
  );
  assert.equal(archive.formalSealedReleaseCount, 40);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);

  const formal = archive.formalSealedReleases;
  const backlog = archive.legacyFormalFigureBacklog.map((row) => row.release);
  assert.equal(new Set(formal).size, formal.length, "unique formal releases");
  assert.equal(new Set(backlog).size, backlog.length, "unique backlog releases");
  assert.deepEqual(
    [...formal, ...backlog].sort(),
    releases,
    "formal-sealed plus backlog must partition every published release",
  );
  assert.deepEqual(
    formal.filter((release) => backlog.includes(release)),
    [],
    "formal and backlog inventories must be disjoint",
  );

  assert.equal(
    releaseIndex.postR070APublishedReleaseCount,
    archive.publishedReleaseCount,
  );
  assert.equal(
    releaseIndex.postR070AFormalSealedReleaseCount,
    archive.formalSealedReleaseCount,
  );
  assert.equal(
    releaseIndex.legacyFormalFigureBacklogCount,
    archive.legacyFormalFigureBacklogCount,
  );

  const currentFormal = figureManifests
    .filter(
      ({ value }) =>
        value.status === "formal" &&
        /^R0\.(?:70|71|72)[A-Z]$/.test(value.release ?? ""),
    )
    .map(({ value }) => value.release.toLowerCase().replace(".", ""))
    .sort();
  assert.deepEqual(
    currentFormal,
    formal,
    "formal-sealed releases must be backed by formal figure manifests",
  );
  assert.ok(formal.includes("r072f"), "R0.72F must remain formal-sealed");
  assert.ok(formal.includes("r072g"), "R0.72G must be formal-sealed");
  assert.ok(formal.includes("r072h"), "R0.72H must be formal-sealed");
  assert.ok(formal.includes("r072i"), "R0.72I must remain formal-sealed");
  assert.ok(formal.includes("r072j"), "R0.72J must be formal-sealed");
  assert.ok(formal.includes("r072k"), "R0.72K must be formal-sealed");
  assert.ok(formal.includes("r072l"), "R0.72L must be formal-sealed");

  const explanatory = archive.legacyFormalFigureBacklog.filter(
    (row) => row.archiveState === "explanatory-package",
  );
  const missing = archive.legacyFormalFigureBacklog.filter(
    (row) => row.archiveState === "missing-figure-directory",
  );
  assert.equal(explanatory.length, 10);
  assert.equal(missing.length, 14);
  assert.deepEqual(
    explanatory.map((row) => row.release),
    [
      "r070c",
      "r070d",
      "r070e",
      "r070f",
      "r070g",
      "r070h",
      "r070i",
      "r070j",
      "r070k",
      "r070l",
    ],
  );
  assert.deepEqual(
    missing.map((row) => row.release),
    [
      "r070a",
      "r070b",
      "r070p",
      "r070q",
      "r070r",
      "r070s",
      "r070t",
      "r070u",
      "r070v",
      "r070w",
      "r070x",
      "r070y",
      "r070z",
      "r071a",
    ],
  );

  for (const row of explanatory) {
    const archived = figureManifests.find(({ path }) => path === row.manifest);
    assert.ok(archived, row.release + ": explanatory manifest exists");
    assert.equal(archived.value.status, "explanatory", row.release);
    assert.equal(
      archived.value.release.toLowerCase().replace(".", ""),
      row.release,
    );
  }

  const topLevelFigureDirectories = figureDirectories
    .filter((entry) => entry.isDirectory())
    .map((entry) => entry.name);
  for (const row of missing) {
    assert.equal(
      topLevelFigureDirectories.some((name) => name.startsWith(row.release + "-")),
      false,
      row.release + ": inventory says the figure directory is absent",
    );
  }
});
