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

async function verifyFlatHashLedger(directory) {
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trimEnd()
    .split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
    const [, expected, name] = match;
    const payload = await readFile(resolve(directory, name));
    assert.equal(
      createHash("sha256").update(payload).digest("hex"),
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

test("keeps R0.72R source work non-public and advances the formal endpoint atomically", async () => {
  const [manifest, site, home, literature, noteFiles] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    text("public/research-review.html"),
    text("public/literature-review.html"),
    readdir(resolve(publicRoot, "notes")),
  ]);
  assert.ok(["r072q", "r072r"].includes(manifest.latestCompletedRelease));
  if (manifest.latestCompletedRelease === "r072q") {
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
        latest: "r072q",
        version: "1.30",
        notes: 167,
        recap: 107,
        next: "r072r",
        gate: "tests/r072q-phase-robust-shape-gate.test.mjs",
        publicationTest: "tests/r072q-release.test.mjs",
        published: 69,
        sealed: 45,
        backlog: 24,
      },
    );
    assert.deepEqual(site, {
      schemaVersion: "research-site-version-v1",
      version: "1.30",
      latestRelease: "R0.72Q",
      publicHtmlNoteCount: 167,
      publishedDate: "2026-08-28",
    });
    assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 167);
    assert.match(home, /<strong>R0\.72Q<\/strong>最新研究节点/);
    assert.match(home, /NEXT · R0\.72R/);
    assert.match(literature, /开放接口 · R0\.72R/);
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
      latest: "r072r",
      version: "1.31",
      notes: 168,
      recap: 108,
      next: "r072s",
      gate: "tests/r072r-caustic-free-core-gate.test.mjs",
      publicationTest: "tests/r072r-release.test.mjs",
      published: 70,
      sealed: 46,
      backlog: 24,
    },
  );
  assert.equal(manifest.nextReleaseSourceStage, undefined);
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
  assert.match(home, /阶段后续 R0\.72Q（已完成）：/);
  assert.match(home, /阶段后续 R0\.72R（已完成）：/);
  assert.doesNotMatch(home, />下一步 R0\.72[QR]：/);
  assert.match(home, /累计回顾收录 108 个节点；全站现有 168 篇公开研究笔记/);
  assert.match(literature, /id="r072r-boundary"/);
  assert.match(literature, /开放接口 · R0\.72S/);
});

test("keeps R artifacts absent at source stage and synchronized after formal release", async () => {
  const manifest = await json("research/release-manifest.json");
  const publicArtifacts = [
    "public/notes/r0-72r.html",
    "public/notes/r0-72r.pdf",
    "public/recap-r0-61-r0-72r.html",
    "public/recap-r0-61-r0-72r.pdf",
    "public/assets/r072r/fig-r072r-caustic-free-core.pdf",
    "public/assets/r072r/fig-r072r-caustic-free-core.png",
    "public/assets/r072r/fig-r072r-caustic-free-core.svg",
  ];
  if (manifest.latestCompletedRelease === "r072q") {
    for (const relative of publicArtifacts) await absent(relative);
    return;
  }
  assert.equal(manifest.latestCompletedRelease, "r072r");
  const [note, notePdf, recap, recapPdf, home, literature] = await Promise.all([
    text("public/notes/r0-72r.html"),
    readFile(resolve(root, "public/notes/r0-72r.pdf")),
    text("public/recap-r0-61-r0-72r.html"),
    readFile(resolve(root, "public/recap-r0-61-r0-72r.pdf")),
    text("public/research-review.html"),
    text("public/literature-review.html"),
  ]);
  for (const page of [note, recap, home, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.31"/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(
      page,
      /[A-Za-z0-9_}]\\\(/,
      "function arguments must not become fresh MathJax delimiters",
    );
  }
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  for (const token of [
    "|z_2-3/20|",
    "|z_3|",
    "14/25",
    "20489/256000",
    "(\\pi/48,144,240)",
    "161/25",
    "\\eta_{\\rm CH}",
    "four-real-dimensional",
    "完整四维 caustic",
    "third-carrier amplitude floor",
    "R0.72S",
  ]) assert.ok(note.includes(token), token);
  assert.match(note, /href="\/notes\/r0-72r\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-72r\.html"/);
  assert.match(note, /href="\/recap-r0-61-r0-72r\.pdf"/);
  assert.match(recap, /R0\.61–R0\.72R 的 108 节公开笔记/);
  assert.match(recap, /R0\.70A–R0\.72R 的 70 节已公开；46 节/);
  const index = nodeIndex(recap);
  const links = [...index.matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map(
    (match) => match[1],
  );
  assert.equal(links.length, 108);
  assert.equal(new Set(links).size, 108);
  assert.equal(links.filter((slug) => slug === "r0-72r").length, 1);
  assert.match(literature, /Arnol.d/);
  assert.match(literature, /Voorhaar/);
  assert.match(literature, /Coble/);
  assert.match(literature, /完整四维|four-dimensional/);
  for (const [label, pdf] of [["note", notePdf], ["recap", recapPdf]]) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label);
    assert.ok(pdf.length > 10_000, `${label} PDF is unexpectedly small`);
  }

  const figure = resolve(
    root,
    "figures/r072r-caustic-free-core/fig-r072r-caustic-free-core",
  );
  const certificate = resolve(root, "research/certificates/r072r");
  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  const figureManifest = JSON.parse(
    await readFile(resolve(figure, "manifest.json"), "utf8"),
  );
  assert.equal(figureManifest.release, "R0.72R");
  assert.equal(figureManifest.figureId, "fig-r072r-caustic-free-core");
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  for (const suffix of ["pdf", "png", "svg"]) {
    const relative = `/assets/r072r/fig-r072r-caustic-free-core.${suffix}`;
    const master = await readFile(resolve(figure, `figure.${suffix}`));
    const published = await readFile(resolve(publicRoot, relative.slice(1)));
    assert.equal(Buffer.compare(master, published), 0, `${suffix} byte identity`);
    assert.ok(note.includes(relative), relative);
  }
});

test("formal R release advances archive inventory and deterministic generator together", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072q") return;
  assert.equal(manifest.latestCompletedRelease, "r072r");
  const [archive, generator] = await Promise.all([
    json("research/formal-archive-inventory.json"),
    text("scripts/generate_r072r_release.py"),
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
      latest: "r072r",
      published: 70,
      sealed: 46,
      backlog: 24,
      publishedLast: "r072r",
      sealedLast: "r072r",
    },
  );
  for (const token of [
    "public/notes/r0-72q.html",
    "public/recap-r0-61-r0-72q.html",
    "notes/r0-72r.html",
    "recap-r0-61-r0-72r.html",
    "research/r072r_report-source.md",
    "research/r072r_literature_audit.md",
    "research/r072r_gap_matrix.md",
    "research/r072r_independent_audit.md",
    "research/certificates/r072r",
    "figures/r072r-caustic-free-core/fig-r072r-caustic-free-core",
    "tests/r072r-caustic-free-core-gate.test.mjs",
    "tests/r072r-release.test.mjs",
    "expected 168 public HTML notes",
    '"recapNodes": 108',
    '"published": 70',
    '"formalSealed": 46',
    '"legacyBacklog": 24',
    '"routeNotes": 78',
    '"next": "R0.72S"',
    "temporaryUnsealedSourceAllowed",
    "verify_flat_hash_ledger",
    "strict figure validation failed",
    "publicCopiesComplete",
    "assert_mathjax_clean",
  ]) assert.ok(generator.includes(token), token);
  assert.ok(
    generator.indexOf('"latestCompletedRelease": "r072q"') <
      generator.indexOf('"latestCompletedRelease": "r072r"'),
  );
  assert.ok(
    generator.indexOf("validate_inputs()") < generator.indexOf("build_note()"),
    "formal preflight must precede the first public mutation",
  );
  assert.doesNotMatch(
    generator,
    /allow-unsealed-source|source-preview|skip-(?:seal|validation)/,
  );
});

test("formal R translation batch covers all live Chinese strings without changing protected mathematics", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072q") return;
  assert.equal(manifest.latestCompletedRelease, "r072r");
  const [script, snapshot, source, translations, built] = await Promise.all([
    text("scripts/add-r072r-translations.mjs"),
    json("scripts/i18n-snapshots/r072r-missing.json"),
    collectSiteStrings(publicRoot),
    json("translations/en.json"),
    text("public/i18n-en.js"),
  ]);
  for (const token of [
    "R072R_RELEASE_ROOT",
    "--check-only",
    "r072r-missing.json",
    "literature-review.html",
    "notes/r0-72r.html",
    "recap-r0-61-r0-72r.html",
    "research-review.html",
    "/i18n-en.js?v=1.31",
    "extractProtectedTokens",
    "containsChinese",
  ]) assert.ok(script.includes(token), token);
  assert.ok(Array.isArray(snapshot));
  assert.ok(snapshot.length > 0);
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry]));
  assert.equal(byChinese.size, translations.length);
  assert.deepEqual(source.filter((entry) => !byChinese.has(entry.zh)), []);
  const batch = translations.filter((entry) => /^r072r\d+$/.test(entry.id));
  assert.equal(batch.length, snapshot.length);
  assert.deepEqual([...new Set(batch.flatMap((entry) => entry.files))].sort(), [
    "literature-review.html",
    "notes/r0-72r.html",
    "recap-r0-61-r0-72r.html",
    "research-review.html",
  ]);
  for (const entry of batch) {
    assert.ok(entry.en.trim(), entry.zh);
    assert.doesNotMatch(entry.en, /[\u3400-\u9fff\uf900-\ufaff]/u);
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i);
    assert.deepEqual(
      extractProtectedTokens(entry.en),
      extractProtectedTokens(entry.zh),
    );
    assert.ok(built.includes(JSON.stringify(entry.zh)), entry.zh);
  }
});
