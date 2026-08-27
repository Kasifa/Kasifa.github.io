import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import {
  collectSiteStrings,
  extractProtectedTokens,
} from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function absent(relative) {
  await assert.rejects(
    access(resolve(root, relative)),
    (error) => error?.code === "ENOENT",
  );
}

async function inspectPdf(relative) {
  const pdf = await readFile(resolve(root, relative));
  const source = pdf.toString("latin1");
  const pages = [...source.matchAll(/\/Type\s*\/Page\b/g)].length;
  const titleHex = source.match(/\/Title\s*<([0-9a-f]+)>/i)?.[1];
  assert.ok(titleHex, `${relative}: hexadecimal PDF title metadata`);
  const titleBytes = Buffer.from(titleHex, "hex");
  let title;
  if (titleBytes[0] === 0xfe && titleBytes[1] === 0xff) {
    const codeUnits = [];
    for (let index = 2; index + 1 < titleBytes.length; index += 2) {
      codeUnits.push(titleBytes.readUInt16BE(index));
    }
    title = String.fromCharCode(...codeUnits);
  } else {
    title = titleBytes.toString("latin1");
  }
  return { pages, title };
}

async function verifyFlatHashLedger(directory) {
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trimEnd()
    .split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
    const [, expected, name] = match;
    assert.equal(
      createHash("sha256").update(await readFile(resolve(directory, name))).digest("hex"),
      expected,
      name,
    );
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries
      .filter(
        (entry) =>
          entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name),
      )
      .map((entry) => entry.name)
      .sort(),
  );
  return names;
}

function nodeIndex(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start, "current recap node index");
  return recap.slice(start, end);
}

function routeNoteLinks(home, lastRelease) {
  const pattern = new RegExp(
    `<nav class="route-note-links" aria-label="R0\\.69P–${lastRelease}">([\\s\\S]*?)</nav>`,
  );
  const route = home.match(pattern);
  assert.ok(route, "current public route index");
  return [...route[1].matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map(
    (match) => match[1],
  );
}

test("keeps the R0.72S source freeze non-public and advances v1.32 atomically", async () => {
  const [manifest, site, home, literature, noteFiles] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    text("public/research-review.html"),
    text("public/literature-review.html"),
    readdir(resolve(publicRoot, "notes")),
  ]);
  assert.ok(["r072r", "r072s"].includes(manifest.latestCompletedRelease));
  if (manifest.latestCompletedRelease === "r072r") {
    assert.deepEqual(
      {
        version: manifest.siteVersion,
        notes: manifest.publicHtmlNoteCount,
        recap: manifest.postR060RecapNodeCount,
        next: manifest.nextRelease,
        published: manifest.postR070APublishedReleaseCount,
        sealed: manifest.postR070AFormalSealedReleaseCount,
        backlog: manifest.legacyFormalFigureBacklogCount,
      },
      {
        version: "1.31", notes: 168, recap: 108, next: "r072s",
        published: 70, sealed: 46, backlog: 24,
      },
    );
    assert.equal(manifest.nextReleaseSourceStage?.release, "r072s");
    assert.equal(
      manifest.nextReleaseSourceStage?.releaseGate,
      "tests/r072s-singular-strata-gate.test.mjs",
    );
    assert.equal(
      manifest.nextReleaseSourceStage?.publicationTest,
      "tests/r072s-release.test.mjs",
    );
    assert.deepEqual(site, {
      schemaVersion: "research-site-version-v1",
      version: "1.31",
      latestRelease: "R0.72R",
      publicHtmlNoteCount: 168,
      publishedDate: "2026-08-28",
    });
    assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 168);
    assert.match(home, /<strong>R0\.72R<\/strong>最新研究节点/);
    assert.match(home, /NEXT · R0\.72S/);
    assert.match(literature, /开放接口 · R0\.72S/);
    return;
  }

  assert.deepEqual(
    {
      latest: manifest.latestCompletedRelease,
      version: manifest.siteVersion,
      notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount,
      next: manifest.nextRelease,
      gate: manifest.latestReleaseGate,
      publicationTest: manifest.latestReleasePublicationTest,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    },
    {
      latest: "r072s",
      version: "1.32",
      notes: 169,
      recap: 109,
      next: "r072t",
      gate: "tests/r072s-singular-strata-gate.test.mjs",
      publicationTest: "tests/r072s-release.test.mjs",
      published: 71,
      sealed: 47,
      backlog: 24,
    },
  );
  assert.equal(manifest.nextReleaseSourceStage, undefined);
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.32",
    latestRelease: "R0.72S",
    publicHtmlNoteCount: 169,
    publishedDate: "2026-08-28",
  });
  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 169);
  assert.match(home, /<strong>R0\.72S<\/strong>最新研究节点/);
  assert.match(home, /NEXT · R0\.72T/);
  assert.match(home, /累计回顾收录 109 个节点；全站现有 169 篇公开研究笔记/);
  const route = routeNoteLinks(home, "R0.72S");
  assert.equal(route.length, 79);
  assert.equal(new Set(route).size, 79);
  assert.equal(route.filter((slug) => slug === "r0-72s").length, 1);
  assert.match(literature, /id="r072s-boundary"/);
  assert.match(literature, /开放接口 · R0\.72T/);
});

test("keeps S artifacts absent at source stage and synchronizes HTML, PDF, and figure bytes after release", async () => {
  const manifest = await json("research/release-manifest.json");
  const publicArtifacts = [
    "public/notes/r0-72s.html",
    "public/notes/r0-72s.pdf",
    "public/recap-r0-61-r0-72s.html",
    "public/recap-r0-61-r0-72s.pdf",
    "public/assets/r072s/fig-r072s-heat-collisions.pdf",
    "public/assets/r072s/fig-r072s-heat-collisions.png",
    "public/assets/r072s/fig-r072s-heat-collisions.svg",
  ];
  if (manifest.latestCompletedRelease === "r072r") {
    for (const relative of publicArtifacts) await absent(relative);
    return;
  }
  assert.equal(manifest.latestCompletedRelease, "r072s");
  const [note, notePdf, recap, recapPdf, home, literature] = await Promise.all([
    text("public/notes/r0-72s.html"),
    readFile(resolve(root, "public/notes/r0-72s.pdf")),
    text("public/recap-r0-61-r0-72s.html"),
    readFile(resolve(root, "public/recap-r0-61-r0-72s.pdf")),
    text("public/research-review.html"),
    text("public/literature-review.html"),
  ]);
  for (const page of [note, recap, home, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.32"/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(
      page,
      /[A-Za-z0-9_}]\\\(/,
      "function arguments must not become fresh MathJax delimiters",
    );
  }
  for (const [label, page] of [["note", note], ["recap", recap],
    ["home", home], ["literature", literature]]) {
    assert.doesNotMatch(
      page,
      /我们|攻关|主攻|研究纪律|杀死错误想法|突破/,
      `${label} must preserve the individual-researcher voice`,
    );
  }
  for (const token of [
    "incidence preimage",
    "restricted miniversal",
    "5400",
    "4/3/2",
    "4/2/2",
    "A_2",
    "A_3",
    "R0.72T",
    "Clay",
  ]) assert.ok(note.includes(token), token);
  assert.match(note, /href="\/notes\/r0-72s\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-72s\.html"/);
  assert.match(note, /href="\/recap-r0-61-r0-72s\.pdf"/);
  assert.match(recap, /R0\.61–R0\.72S 的 109 节公开笔记/);
  assert.match(recap, /R0\.70A–R0\.72S 的 71 节已公开；47 节/);
  const links = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(links.length, 109);
  assert.equal(new Set(links).size, 109);
  assert.equal(links.filter((slug) => slug === "r0-72s").length, 1);

  const correctArnold = "https://link.springer.com/chapter/10.1007/978-1-4612-4122-5_4";
  assert.ok(literature.includes(correctArnold));
  assert.doesNotMatch(literature, /978-1-4612-4122-5_8/);
  assert.match(literature, /restricted miniversal|R\^\+-versal/);
  assert.match(literature, /Arnol.d/);
  assert.match(literature, /Voorhaar/);
  assert.match(literature, /collision|碰撞/);
  const pdfCases = [
    ["note", "public/notes/r0-72s.pdf", notePdf, ["R0.72S"]],
    ["recap", "public/recap-r0-61-r0-72s.pdf", recapPdf, ["R0.61", "R0.72S"]],
  ];
  for (const [label, relative, pdf, versionTokens] of pdfCases) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label);
    assert.ok(pdf.length > 10_000, `${label} PDF is unexpectedly small`);
    const inspected = await inspectPdf(relative);
    assert.ok(inspected.pages >= 2 && inspected.pages <= 40,
      `${label} PDF page count ${inspected.pages} is implausible`);
    for (const token of versionTokens) {
      assert.ok(
        inspected.title.includes(token),
        `${label} PDF title metadata must expose ${token}`,
      );
    }
  }

  const figure = resolve(
    root,
    "figures/r072s-heat-collisions/fig-r072s-heat-collisions",
  );
  const certificate = resolve(root, "research/certificates/r072s");
  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  const figureManifest = JSON.parse(
    await readFile(resolve(figure, "manifest.json"), "utf8"),
  );
  assert.equal(figureManifest.release, "R0.72S");
  assert.equal(figureManifest.figureId, "fig-r072s-heat-collisions");
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  for (const suffix of ["pdf", "png", "svg"]) {
    const relative = `/assets/r072s/fig-r072s-heat-collisions.${suffix}`;
    const master = await readFile(resolve(figure, `figure.${suffix}`));
    const published = await readFile(resolve(publicRoot, relative.slice(1)));
    assert.equal(Buffer.compare(master, published), 0, `${suffix} byte identity`);
    assert.ok(note.includes(relative), relative);
  }
});

test("formal S release advances the archive inventory and deterministic generator together", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072r") return;
  assert.equal(manifest.latestCompletedRelease, "r072s");
  const [archive, generator] = await Promise.all([
    json("research/formal-archive-inventory.json"),
    text("scripts/generate_r072s_release.py"),
  ]);
  assert.deepEqual(
    {
      latest: archive.latestPublishedRelease,
      published: archive.publishedReleaseCount,
      sealed: archive.formalSealedReleaseCount,
      backlog: archive.legacyFormalFigureBacklogCount,
      publishedLast: archive.publishedReleases.at(-1),
      sealedLast: archive.formalSealedReleases.at(-1),
    },
    {
      latest: "r072s",
      published: 71,
      sealed: 47,
      backlog: 24,
      publishedLast: "r072s",
      sealedLast: "r072s",
    },
  );
  for (const token of [
    "public/notes/r0-72r.html",
    "public/recap-r0-61-r0-72r.html",
    "notes/r0-72s.html",
    "recap-r0-61-r0-72s.html",
    "research/r072s_report-source.md",
    "research/r072s_literature_audit.md",
    "research/r072s_gap_matrix.md",
    "research/r072s_independent_audit.md",
    "research/certificates/r072s",
    "figures/r072s-heat-collisions/fig-r072s-heat-collisions",
    "tests/r072s-singular-strata-gate.test.mjs",
    "tests/r072s-release.test.mjs",
    "expected 169 public HTML notes",
    '"recapNodes": 109',
    '"published": 71',
    '"formalSealed": 47',
    '"legacyBacklog": 24',
    '"routeNotes": 79',
    '"next": "R0.72T"',
    "temporaryUnsealedSourceAllowed",
    "verify_flat_hash_ledger",
    "strict figure validation failed",
    "publicCopiesComplete",
    "assert_mathjax_clean",
    "978-1-4612-4122-5_4",
  ]) assert.ok(generator.includes(token), token);
  assert.doesNotMatch(generator, /978-1-4612-4122-5_8/);
  assert.ok(
    generator.indexOf('"latestCompletedRelease": "r072r"') <
      generator.indexOf('"latestCompletedRelease": "r072s"'),
  );
  assert.ok(
    generator.indexOf("validate_inputs()") < generator.indexOf("build_note()"),
    "formal preflight must precede the first public mutation",
  );
  assert.doesNotMatch(
    generator,
    /allow-unsealed(?:-source)?|source-preview|skip-(?:seal|validation)/,
  );
});

test("formal S translation batch covers every live Chinese string and preserves mathematics", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072r") return;
  assert.equal(manifest.latestCompletedRelease, "r072s");
  const [script, snapshot, source, translations, built] = await Promise.all([
    text("scripts/add-r072s-translations.mjs"),
    json("scripts/i18n-snapshots/r072s-missing.json"),
    collectSiteStrings(publicRoot),
    json("translations/en.json"),
    text("public/i18n-en.js"),
  ]);
  for (const token of [
    "R072S_RELEASE_ROOT",
    "--check-only",
    "r072s-missing.json",
    "literature-review.html",
    "notes/r0-72s.html",
    "recap-r0-61-r0-72s.html",
    "research-review.html",
    "/i18n-en.js?v=1.32",
    "extractProtectedTokens",
    "containsChinese",
  ]) assert.ok(script.includes(token), token);
  assert.ok(Array.isArray(snapshot));
  assert.ok(snapshot.length > 0);
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry]));
  assert.equal(byChinese.size, translations.length);
  assert.deepEqual(source.filter((entry) => !byChinese.has(entry.zh)), []);
  const batch = translations.filter((entry) => /^r072s\d+$/.test(entry.id));
  assert.equal(batch.length, snapshot.length);
  assert.deepEqual([...new Set(batch.flatMap((entry) => entry.files))].sort(), [
    "literature-review.html",
    "notes/r0-72s.html",
    "recap-r0-61-r0-72s.html",
    "research-review.html",
  ]);
  for (const entry of batch) {
    assert.ok(entry.en.trim(), entry.zh);
    assert.doesNotMatch(entry.en, /[\u3400-\u9fff\uf900-\ufaff]/u);
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh));
    assert.ok(built.includes(JSON.stringify(entry.zh)), entry.zh);
  }
});
