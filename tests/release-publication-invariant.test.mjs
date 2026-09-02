import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { access, readdir, readFile } from "node:fs/promises";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";

import {
  extractTranslatableStrings,
  listSiteHtmlFiles,
} from "../scripts/i18n-lib.mjs";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("../public/", import.meta.url);
const notesRoot = new URL("notes/", publicRoot);
const execFileAsync = promisify(execFile);

function isOneDriveConflictCopyName(name) {
  return / \d+(?=\.[^.]+$|$)/.test(name);
}

function isPublicNoteHtml(file) {
  return /^r0-[0-9a-z]+\.html$/.test(file);
}

function naturalNoteParts(file) {
  return file
    .replace(/^r0-/, "")
    .replace(/\.(?:html|pdf)$/, "")
    .match(/\d+|[a-z]+/g)
    .map((part) => (/^\d+$/.test(part) ? Number(part) : part));
}

function compareNaturalNotes(left, right) {
  const leftParts = naturalNoteParts(left);
  const rightParts = naturalNoteParts(right);
  const length = Math.max(leftParts.length, rightParts.length);
  for (let index = 0; index < length; index += 1) {
    if (leftParts[index] === undefined) return -1;
    if (rightParts[index] === undefined) return 1;
    if (leftParts[index] === rightParts[index]) continue;
    if (typeof leftParts[index] === "number") {
      return leftParts[index] - rightParts[index];
    }
    return leftParts[index].localeCompare(rightParts[index], "en");
  }
  return 0;
}

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

test("keeps a declared next-release source stage non-public and path-safe", async () => {
  const manifest = await releaseManifest();
  const stage = manifest.nextReleaseSourceStage;
  if (stage === undefined) {
    assert.equal(
      manifest.nextRelease,
      nextReleaseId(manifest.latestCompletedRelease),
      "a completed endpoint without a source-stage block must point to its successor",
    );
    assert.ok(
      manifest.latestReleaseGate.startsWith(
        `tests/${manifest.latestCompletedRelease}`,
      ),
    );
    assert.ok(
      manifest.latestReleasePublicationTest.startsWith(
        `tests/${manifest.latestCompletedRelease}`,
      ),
    );
    return;
  }
  assert.equal(typeof stage, "object", "next-release source stage");
  assert.equal(stage.release, manifest.nextRelease);
  assert.equal(stage.stage, "source-freeze");
  assert.equal(
    stage.publicationStatus,
    "pending-formal-certificate-figure-and-publication",
  );
  assert.equal(stage.publicCountersAdvanced, false);
  assert.notEqual(stage.release, manifest.latestCompletedRelease);

  const pathFields = [
    "report",
    "independentAudit",
    "producer",
    "independentProducer",
    "comparator",
    "certificateDirectory",
    "figureDirectory",
    "generator",
    "translationScript",
    "releaseGate",
    "publicationTest",
  ];
  for (const field of pathFields) {
    const relative = stage[field];
    assert.equal(typeof relative, "string", `source-stage ${field}`);
    assert.match(relative, /^(?:research|figures|scripts|tests)\/[A-Za-z0-9._/-]+$/);
    assert.doesNotMatch(relative, /(?:^|\/)\.\.(?:\/|$)|\\|\0/);
    const target = new URL(relative + (field.endsWith("Directory") ? "/" : ""), root);
    assert.ok(target.href.startsWith(root.href), `source-stage path escape: ${field}`);
    await access(target);
  }
  assert.equal(stage.report, `research/${stage.release}_report-source.md`);
  assert.equal(stage.generator, `scripts/generate_${stage.release}_release.py`);
  assert.equal(stage.translationScript, `scripts/add-${stage.release}-translations.mjs`);
  assert.ok(stage.releaseGate.startsWith(`tests/${stage.release}-`));
  assert.equal(stage.publicationTest, `tests/${stage.release}-release.test.mjs`);

  // A source-stage declaration must not move any live publication pointer.
  assert.ok(manifest.latestReleaseGate.startsWith(`tests/${manifest.latestCompletedRelease}`));
  assert.ok(
    manifest.latestReleasePublicationTest.startsWith(
      `tests/${manifest.latestCompletedRelease}`,
    ),
  );
});

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

async function verifyFlatHashLedger(directory) {
  const ledger = (await readFile(new URL("SHA256SUMS", directory), "utf8"))
    .trimEnd()
    .split("\n");
  const names = [];
  for (const row of ledger) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed formal-figure SHA256SUMS row: ${row}`);
    const [, expected, name] = match;
    const payload = await readFile(new URL(name, directory));
    assert.equal(createHash("sha256").update(payload).digest("hex"), expected, name);
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort(), "formal-figure hash rows");
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()), "formal-figure symlink");
  const expectedNames = entries
    .filter(
      (entry) =>
        entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name) &&
        !isOneDriveConflictCopyName(entry.name),
    )
    .map((entry) => entry.name)
    .sort();
  assert.deepEqual(names, expectedNames, "formal-figure hash coverage");
}

async function verifyLatestFormalFigure(record, latestCode) {
  assert.ok(record, `${latestCode}: formal figure manifest is missing`);
  const manifest = record.value;
  assert.equal(manifest.status, "formal");
  assert.equal(manifest.release, latestCode);
  const manifestUrl = new URL(record.path, root);
  const packageUrl = new URL("./", manifestUrl);
  const validator = new URL("research/validate_figure_package.py", root);
  const { stdout } = await execFileAsync(
    process.env.CODEX_PYTHON || "python3",
    [fileURLToPath(validator), fileURLToPath(packageUrl)],
    { cwd: fileURLToPath(root) },
  );
  assert.deepEqual(JSON.parse(stdout).errors, [], `${latestCode}: strict figure validator`);
  await verifyFlatHashLedger(packageUrl);

  let publicationManifest = manifest;
  if (manifest.publicationStatus === "staged") {
    const researchManifestUrl = new URL(`research/${record.path}`, root);
    const publicManifestUrl = new URL(`public/${record.path}`, root);
    const [researchManifestBytes, publicManifestBytes] = await Promise.all([
      readFile(researchManifestUrl),
      readFile(publicManifestUrl),
    ]);
    assert.equal(
      Buffer.compare(researchManifestBytes, publicManifestBytes),
      0,
      `${latestCode}: research/public publication manifests`,
    );
    publicationManifest = JSON.parse(researchManifestBytes.toString("utf8"));
    assert.equal(publicationManifest.publicationStatus, "published");
    assert.equal(
      publicationManifest.sourcePublicationStatus,
      manifest.publicationStatus,
    );
    assert.equal(publicationManifest.figureId, manifest.figureId);
    assert.equal(publicationManifest.release, latestCode);
    const normalizedSource = structuredClone(manifest);
    const normalizedPublication = structuredClone(publicationManifest);
    delete normalizedSource.publicationStatus;
    delete normalizedPublication.publicationStatus;
    delete normalizedPublication.sourcePublicationStatus;
    delete normalizedPublication.publication;
    assert.deepEqual(
      normalizedPublication,
      normalizedSource,
      `${latestCode}: published manifest scientific payload`,
    );
    const researchPackageUrl = new URL("./", researchManifestUrl);
    const publicPackageUrl = new URL("./", publicManifestUrl);
    await Promise.all([
      verifyFlatHashLedger(researchPackageUrl),
      verifyFlatHashLedger(publicPackageUrl),
    ]);
    const [sourceEntries, researchEntries, publicEntries] = await Promise.all([
      readdir(packageUrl, { withFileTypes: true }),
      readdir(researchPackageUrl, { withFileTypes: true }),
      readdir(publicPackageUrl, { withFileTypes: true }),
    ]);
    for (const [label, entries] of [
      ["source", sourceEntries],
      ["research", researchEntries],
      ["public", publicEntries],
    ]) {
      assert.ok(
        entries.every((entry) => entry.isFile()),
        `${latestCode}: ${label} package must be flat and regular`,
      );
    }
    const names = (entries) => entries
      .filter((entry) => !isOneDriveConflictCopyName(entry.name))
      .map((entry) => entry.name).sort();
    assert.deepEqual(names(researchEntries), names(sourceEntries));
    assert.deepEqual(names(publicEntries), names(sourceEntries));
    for (const entry of sourceEntries.filter(
      (entry) => !isOneDriveConflictCopyName(entry.name),
    )) {
      if (["manifest.json", "SHA256SUMS"].includes(entry.name)) continue;
      const [sourcePayload, researchPayload, publicPayload] = await Promise.all([
        readFile(new URL(entry.name, packageUrl)),
        readFile(new URL(entry.name, researchPackageUrl)),
        readFile(new URL(entry.name, publicPackageUrl)),
      ]);
      assert.equal(
        Buffer.compare(sourcePayload, researchPayload),
        0,
        `${latestCode}: research copy ${entry.name}`,
      );
      assert.equal(
        Buffer.compare(sourcePayload, publicPayload),
        0,
        `${latestCode}: public copy ${entry.name}`,
      );
    }
  }

  assert.equal(publicationManifest.publicationStatus, "published");
  const publication = publicationManifest.publication ?? {};
  const packageRelative = record.path.replace(/\/manifest\.json$/, "");
  const releaseId = latestCode.toLowerCase().replace(".", "");
  assert.equal(publication.archiveDirectory, `public/${packageRelative}`);
  if (publication.researchArchiveDirectory !== undefined) {
    assert.equal(publication.researchArchiveDirectory, `research/${packageRelative}`);
  }
  assert.equal(publication.directory, `public/assets/${releaseId}`);
  assert.equal(publication.fileStem, manifest.figureId);
  assert.equal(publication.byteIdentityRequired, true);
  assert.equal(publication.publicCopiesComplete, true);
  for (const key of ["releaseSourceCommit", "figureSourceCommit", "figurePackageCommit"]) {
    if (publication[key] !== undefined) {
      assert.match(publication[key], /^[0-9a-f]{40}$/, `${latestCode}: ${key}`);
    }
  }
  if (publication.figureSourceCommit !== undefined) {
    assert.equal(publication.figureSourceCommit, manifest.git?.figureSourceCommit);
    assert.equal(publication.figureSourceCommit, manifest.seal?.figureSourceCommit);
  }
  const publicAssets = publication.assets ?? [];
  assert.equal(publicAssets.length, 3, `${latestCode}: PDF/SVG/PNG public masters`);
  assert.deepEqual(
    publicAssets.map((row) => row.path.split(".").at(-1)).sort(),
    ["pdf", "png", "svg"],
    `${latestCode}: exact public asset suffixes`,
  );
  const archivalOutputs = new Map(
    (manifest.figure?.outputs ?? []).map((row) => [row.path.split(".").at(-1), row]),
  );
  for (const row of publicAssets) {
    const suffix = row.path.split(".").at(-1);
    assert.equal(
      row.path,
      `public/assets/${releaseId}/${manifest.figureId}.${suffix}`,
      `${latestCode}: public asset path`,
    );
    const archival = archivalOutputs.get(suffix);
    assert.ok(archival, `${latestCode}: missing archival ${suffix}`);
    const [master, published] = await Promise.all([
      readFile(new URL(archival.path, packageUrl)),
      readFile(new URL(row.path, root)),
    ]);
    const hash = createHash("sha256").update(master).digest("hex");
    assert.equal(hash, archival.sha256, `${latestCode}: archival ${suffix} hash`);
    assert.equal(hash, row.sha256, `${latestCode}: public ${suffix} hash`);
    assert.equal(master.length, archival.bytes, `${latestCode}: archival ${suffix} bytes`);
    assert.equal(master.length, row.bytes, `${latestCode}: public ${suffix} bytes`);
    assert.equal(Buffer.compare(master, published), 0, `${latestCode}: ${suffix} byte identity`);
  }
}

async function verifyLatestAnalyticFigureExemption(latestRelease, latestCode) {
  const freeze = JSON.parse(
    await readFile(new URL(`research/${latestRelease}_freeze_manifest.json`, root), "utf8"),
  );
  assert.equal(
    freeze.claim_status?.formal_figure,
    "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
    `${latestCode}: frozen formal-figure exemption`,
  );
  assert.equal(freeze.claim_status?.simulation_or_dns, "NOT_USED");
  assert.equal(freeze.claim_status?.dgx, "NOT_USED");
  assert.equal(freeze.verification?.formal_figure_or_simulation_package, "NOT_APPLICABLE");
  assert.equal(freeze.publication_handoff?.target_primary_figure, null);
  const note = await readFile(
    new URL(`public/notes/${releaseToSlug(latestRelease)}.html`, root),
    "utf8",
  );
  assert.ok(note.includes("正式图件：NOT APPLICABLE"));
  assert.ok(note.includes("本节纯解析，没有 Navier--Stokes 数值仿真、DNS、DGX 或正式图件"));
  assert.doesNotMatch(note, new RegExp(`(?:assets|figures)/${latestRelease}`, "i"));
  for (const directory of ["figures/", "research/figures/", "public/figures/", "public/assets/"]) {
    const entries = await readdir(new URL(directory, root), { withFileTypes: true });
    assert.equal(
      entries.some((entry) => entry.name.startsWith(latestRelease)),
      false,
      `${latestCode}: analytic exemption must not fabricate ${directory} package`,
    );
  }
}

function publicReleaseId(file) {
  const match = file.match(/^r0-(\d{2})([a-z])\.html$/);
  if (!match) return null;
  const release = "r0" + match[1] + match[2];
  return release.localeCompare("r070a") >= 0 ? release : null;
}

test("keeps every synchronized public note PDF discoverable from its note", async () => {
  const noteFiles = (await readdir(notesRoot)).filter(
    (file) => !isOneDriveConflictCopyName(file),
  );
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

test("keeps the complete research-note index deterministic, latest-first, and count-safe", async () => {
  const [manifest, noteFiles, index, generatorResult, i18nFiles] = await Promise.all([
    releaseManifest(),
    readdir(notesRoot),
    readFile(new URL("index.html", notesRoot), "utf8"),
    execFileAsync(
      process.env.CODEX_PYTHON || "python3",
      ["scripts/generate_note_index.py", "--check"],
      { cwd: fileURLToPath(root) },
    ),
    listSiteHtmlFiles(fileURLToPath(publicRoot)),
  ]);
  const htmlNotes = noteFiles
    .filter(isPublicNoteHtml)
    .sort(compareNaturalNotes)
    .reverse();
  const pdfNotes = noteFiles
    .filter((file) => /^r0-[0-9a-z]+\.pdf$/.test(file))
    .sort(compareNaturalNotes)
    .reverse();
  const latestCode = releaseToPublicCode(manifest.latestCompletedRelease);
  const latestHtml = releaseToSlug(manifest.latestCompletedRelease) + ".html";
  const htmlOnlyNotes = htmlNotes.length - pdfNotes.length;
  const summary = JSON.parse(generatorResult.stdout);
  assert.deepEqual(summary, {
    htmlNotes: htmlNotes.length,
    htmlOnlyNotes,
    latest: latestCode,
    oldest: "R0.1",
    output: "public/notes/index.html",
    pdfNotes: pdfNotes.length,
    schemaVersion: "research-note-index-v1",
    status: "current",
  });

  assert.ok(htmlNotes.length > 60);
  assert.ok(pdfNotes.length > 0);
  assert.ok(htmlOnlyNotes >= 0);
  assert.equal(htmlNotes.length, manifest.publicHtmlNoteCount);
  assert.equal(htmlNotes[0], latestHtml);
  assert.equal(htmlNotes.at(-1), "r0-1.html");

  const entries = [
    ...index.matchAll(
      /<li class="note-entry" data-note="([^"]+)">([\s\S]*?)<\/li>/g,
    ),
  ];
  const indexedSlugs = entries.map((match) => match[1]);
  const expectedSlugs = htmlNotes.map((file) => file.replace(/\.html$/, ""));
  assert.deepEqual(indexedSlugs, expectedSlugs);
  assert.equal(new Set(indexedSlugs).size, htmlNotes.length);

  const htmlLinks = [
    ...index.matchAll(/href="\/notes\/(r0-[0-9a-z]+)\.html"/g),
  ].map((match) => match[1]);
  const pdfLinks = [
    ...index.matchAll(/href="\/notes\/(r0-[0-9a-z]+)\.pdf"/g),
  ].map((match) => match[1]);
  const missingPdfMarkers = [
    ...index.matchAll(/data-pdf-missing="(r0-[0-9a-z]+)"/g),
  ].map((match) => match[1]);
  assert.deepEqual(htmlLinks, expectedSlugs, "one latest-first HTML link per note");
  assert.deepEqual(
    pdfLinks,
    pdfNotes.map((file) => file.replace(/\.pdf$/, "")),
    "only existing synchronized PDFs may be linked",
  );
  assert.equal(missingPdfMarkers.length, htmlOnlyNotes);
  assert.equal(new Set(missingPdfMarkers).size, htmlOnlyNotes);

  const availablePdfs = new Set(pdfLinks);
  for (const [, slug, body] of entries) {
    assert.ok(
      body.includes(`href="/notes/${slug}.html"`),
      `${slug}: HTML link`,
    );
    if (availablePdfs.has(slug)) {
      assert.ok(body.includes(`href="/notes/${slug}.pdf"`), `${slug}: PDF link`);
      assert.equal(body.includes(`data-pdf-missing="${slug}"`), false);
    } else {
      assert.ok(
        body.includes(`data-pdf-missing="${slug}"`),
        `${slug}: explicit historical HTML-only marker`,
      );
      assert.equal(body.includes(`href="/notes/${slug}.pdf"`), false);
    }
  }

  assert.ok(index.includes("索引页本身不计入研究笔记总数"));
  assert.ok(index.includes(`${htmlOnlyNotes} 篇早期笔记尚无同名 PDF`));
  assert.ok(index.includes("PDF 未生成 · 历史笔记"));
  assert.ok(index.includes("@media (prefers-color-scheme: dark)"));
  assert.ok(index.includes("color-scheme: light dark"));
  assert.ok(index.includes('href="/bilingual.css"'));
  assert.ok(index.includes('src="/i18n-en.js?v='));
  assert.ok(index.includes('src="/bilingual.js"'));
  assert.ok(
    i18nFiles.includes(fileURLToPath(new URL("index.html", notesRoot))),
    "the bilingual source collector must include the note index",
  );
  const indexTranslationKeys = new Set(extractTranslatableStrings(index));
  const versionSpecificUiKeys = [...indexTranslationKeys].filter((key) =>
    /^(?:R0\.\S+ 文件|阅读 R0\.|下载 R0\.|\d+ 篇$)/.test(key),
  );
  assert.deepEqual(
    versionSpecificUiKeys,
    [],
    "version-specific UI labels must not create hundreds of translation keys",
  );
  assert.doesNotMatch(index, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
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
  const [releases, manifest, site, home, literature, noteIndex, noteFiles, versionFile, archive] = await Promise.all([
    publishedReleaseIds(),
    releaseManifest(),
    readFile(new URL("site-version.json", publicRoot), "utf8").then(JSON.parse),
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/index.html", publicRoot), "utf8"),
    readdir(notesRoot),
    readFile(new URL("VERSION", root), "utf8").then((value) => value.trim()),
    formalArchiveInventory(),
  ]);

  const htmlNotes = noteFiles.filter(isPublicNoteHtml);
  const pdfNotes = noteFiles.filter((file) => /^r0-[0-9a-z]+\.pdf$/.test(file));
  const latestRelease = releases.at(-1);
  const latestSlug = releaseToSlug(latestRelease);
  const latestCode = releaseToPublicCode(latestRelease);
  const nextCode = nextPublicCode(latestRelease);
  const recapRelease = manifest.latestRecapRelease;
  assert.match(recapRelease, /^r0\d{2}[a-z]$/, "manifest latest recap release");
  const recapSlug = releaseToSlug(recapRelease);
  const recapCode = releaseToPublicCode(recapRelease);
  const recapNextCode = nextPublicCode(recapRelease);
  const recapStem = "recap-r0-61-" + recapSlug;
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
  const publishedNodes = routeLinks.length - recapStart;
  const recapTerminal = routeLinks.indexOf("/notes/" + recapSlug + ".html");
  assert.ok(recapTerminal >= recapStart, "declared recap endpoint is absent from route");
  const recapNodes = recapTerminal - recapStart + 1;
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
  const [latestNote, recapEndpointNote, recap, recapPdf] = await Promise.all([
    readFile(new URL(latestSlug + ".html", notesRoot), "utf8"),
    readFile(new URL(recapSlug + ".html", notesRoot), "utf8"),
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
    routeLinks.slice(recapStart, recapTerminal + 1),
    "milestone recap must index exactly its declared post-R0.60 coverage",
  );

  const versionMatch = home.match(/<strong>v(\d+\.\d+)<\/strong>\u7f51\u9875\u7248\u672c/);
  assert.ok(versionMatch, "homepage version marker is missing");
  const version = versionMatch[1];
  assert.match(version, /^\d+\.\d+$/, "current publication version format");
  assert.match(versionFile, /^\d+\.\d+$/, "VERSION format");
  assert.equal(versionFile, manifest.siteVersion, "VERSION must equal manifest siteVersion");
  assert.equal(version, manifest.siteVersion, "manifest site version");
  assert.equal(site.version, manifest.siteVersion, "site-version version");
  assert.equal(site.latestRelease, latestCode, "site-version latestRelease");
  for (const [label, html] of [
    ["homepage", home],
    ["literature", literature],
    ["latest note", latestNote],
  ]) {
    assert.ok(
      html.includes('src="/i18n-en.js?v=' + version + '"'),
      label + ": i18n cache version must match homepage v" + version,
    );
  }
  const recapEndpointVersion = recapEndpointNote.match(/data-site-version="(\d+\.\d+)"/);
  assert.ok(recapEndpointVersion, "recap endpoint note site version");
  const recapI18nVersions = [
    ...recap.matchAll(/src="\/i18n-en\.js\?v=(\d+\.\d+)"/g),
  ].map((match) => match[1]);
  assert.deepEqual(
    recapI18nVersions,
    [recapEndpointVersion[1]],
    "milestone recap keeps its own endpoint i18n version",
  );
  const recapDataVersions = [
    ...recap.matchAll(/data-site-version="(\d+\.\d+)"/g),
  ].map((match) => match[1]);
  assert.ok(recapDataVersions.length <= 1, "recap has at most one site-version attribute");
  if (recapDataVersions.length === 1) {
    assert.equal(recapDataVersions[0], recapEndpointVersion[1]);
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
  assert.equal(site.publicHtmlNoteCount, htmlNotes.length, "site-version public HTML count");
  assert.equal(manifest.publicPdfNoteCount, pdfNotes.length, "manifest public PDF count");
  assert.equal(site.publicPdfNoteCount, pdfNotes.length, "site-version public PDF count");
  assert.equal(
    publishedNodes,
    manifest.postR060PublishedNodeCount,
    "manifest post-R0.60 published-node count",
  );
  assert.equal(
    recapNodes,
    manifest.postR060RecapNodeCount,
    "manifest post-R0.60 recap count",
  );
  assert.equal(site.postR060PublishedNodeCount, manifest.postR060PublishedNodeCount);
  assert.equal(site.postR060RecapNodeCount, manifest.postR060RecapNodeCount);
  assert.equal(site.latestRecapRelease, recapCode);
  assert.equal(site.version, versionFile);
  assert.ok(
    recapRelease.localeCompare(latestRelease) <= 0,
    "recap endpoint cannot run ahead of the published endpoint",
  );
  assert.equal(
    recapNodes <= publishedNodes,
    true,
    "recap coverage cannot exceed published-node coverage",
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
  assert.match(
    manifest.latestReleasePublicationTest,
    /^tests\/r0\d{2}[a-z][a-z0-9-]*\.test\.mjs$/,
    "manifest latest-release publication test path",
  );
  await access(new URL(manifest.latestReleasePublicationTest, root));
  assert.ok(
    manifest.latestReleasePublicationTest.startsWith("tests/" + latestRelease),
    "latest-release publication test must advance with the published endpoint",
  );
  assert.ok(
    home.includes("<strong>" + latestCode + "</strong>最新研究节点"),
  );
  assert.ok(home.includes("LATEST RELEASE · " + latestCode + " ·"));
  assert.ok(home.includes(htmlNotes.length + " 篇研究笔记总索引"));
  assert.ok(
    home.includes(
      "R0.70A–" + latestCode + " · " + archive.publishedReleaseCount + " 节已公开",
    ),
    "latest spotlight published count",
  );
  assert.ok(
    home.includes(archive.formalSealedReleaseCount + " 节完整封存"),
    "latest spotlight formal-sealed count",
  );
  assert.ok(home.includes("当前端点 " + latestCode));
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
  assert.ok(noteIndex.includes('href="/' + recapStem + '.html"'));
  if (recapRelease !== latestRelease) {
    for (const [label, page] of [
      ["latest note", latestNote],
      ["homepage", home],
      ["note index", noteIndex],
    ]) {
      assert.ok(page.includes("上一大里程碑"), label + ": milestone recap wording");
    }
    const undeclaredRecapStem = "recap-r0-61-" + latestSlug;
    await assert.rejects(access(new URL(undeclaredRecapStem + ".html", publicRoot)));
    await assert.rejects(access(new URL(undeclaredRecapStem + ".pdf", publicRoot)));
  }

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
    "R0.61–" + recapCode,
    "收录节点：" + recapNodes,
    "回顾截止时公开笔记：" +
      (htmlNotes.length - (publishedNodes - recapNodes)),
    recapNextCode,
    recapCode,
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
  assert.equal(
    archive.latestPublishedRelease,
    releaseIndex.latestCompletedRelease,
  );
  assert.equal(archive.publishedReleaseCount, releases.length);
  assert.equal(
    archive.publishedReleaseCount,
    releaseIndex.postR070APublishedReleaseCount,
  );
  assert.equal(
    archive.formalSealedReleaseCount,
    archive.formalSealedReleases.length,
  );
  assert.equal(
    archive.formalSealedReleaseCount,
    releaseIndex.postR070AFormalSealedReleaseCount,
  );
  assert.equal(
    archive.legacyFormalFigureBacklogCount,
    releaseIndex.legacyFormalFigureBacklogCount,
  );
  assert.equal(
    archive.formalFigureExemptReleaseCount,
    releaseIndex.formalFigureExemptReleaseCount,
  );

  const formal = archive.formalSealedReleases;
  const backlog = archive.legacyFormalFigureBacklog.map((row) => row.release);
  const exempt = archive.formalFigureExemptReleases;
  assert.equal(new Set(formal).size, formal.length, "unique formal releases");
  assert.equal(new Set(backlog).size, backlog.length, "unique backlog releases");
  assert.equal(new Set(exempt).size, exempt.length, "unique formal-figure exemptions");
  assert.equal(archive.formalFigureExemptReleaseCount, exempt.length);
  assert.deepEqual(
    [...formal, ...backlog, ...exempt].sort(),
    releases,
    "formal-sealed, backlog, and declared analytic exemptions must partition every published release",
  );
  assert.deepEqual(
    formal.filter((release) => backlog.includes(release)),
    [],
    "formal and backlog inventories must be disjoint",
  );
  assert.deepEqual(formal.filter((release) => exempt.includes(release)), [], "formal and exempt inventories must be disjoint");
  assert.deepEqual(backlog.filter((release) => exempt.includes(release)), [], "backlog and exempt inventories must be disjoint");

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
  assert.equal(
    releaseIndex.formalFigureExemptReleaseCount,
    archive.formalFigureExemptReleaseCount,
  );

  const currentFormal = [...new Set(figureManifests
    .filter(
      ({ value }) =>
        value.status === "formal" && typeof value.release === "string",
    )
    .map(({ value }) => value.release.toLowerCase().replace(".", ""))
    .filter((release) => releases.includes(release)))]
    .sort();
  assert.deepEqual(
    currentFormal,
    formal,
    "formal-sealed releases must be backed by formal figure manifests",
  );
  const latestCode = releaseToPublicCode(releases.at(-1));
  if (formal.includes(releases.at(-1))) {
    await verifyLatestFormalFigure(
      figureManifests.find(
        ({ value }) => value.status === "formal" && value.release === latestCode,
      ),
      latestCode,
    );
  } else {
    assert.ok(exempt.includes(releases.at(-1)), `${latestCode}: latest release must be formal or explicitly exempt`);
    await verifyLatestAnalyticFigureExemption(releases.at(-1), latestCode);
  }
  assert.ok(formal.includes("r072f"), "R0.72F must remain formal-sealed");
  assert.ok(formal.includes("r072g"), "R0.72G must be formal-sealed");
  assert.ok(formal.includes("r072h"), "R0.72H must be formal-sealed");
  assert.ok(formal.includes("r072i"), "R0.72I must remain formal-sealed");
  assert.ok(formal.includes("r072j"), "R0.72J must be formal-sealed");
  assert.ok(formal.includes("r072k"), "R0.72K must be formal-sealed");
  assert.ok(formal.includes("r072l"), "R0.72L must be formal-sealed");
  assert.ok(formal.includes("r072m"), "R0.72M must be formal-sealed");
  assert.ok(formal.includes("r072n"), "R0.72N must be formal-sealed");
  assert.ok(formal.includes("r072o"), "R0.72O must be formal-sealed");

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
