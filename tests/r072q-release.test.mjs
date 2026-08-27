import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function absent(relative) {
  await assert.rejects(access(resolve(root, relative)), (error) => error?.code === "ENOENT");
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
    assert.equal(createHash("sha256").update(payload).digest("hex"), expected, name);
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries
      .filter((entry) => entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name))
      .map((entry) => entry.name)
      .sort(),
  );
}

test("declares R0.72Q as source-frozen without advancing the live R0.72P endpoint", async () => {
  const [manifest, site, home, literature, noteFiles] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    text("public/research-review.html"),
    text("public/literature-review.html"),
    readdir(resolve(publicRoot, "notes")),
  ]);
  assert.ok(["r072p", "r072q"].includes(manifest.latestCompletedRelease));
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
    assert.equal(manifest.nextReleaseSourceStage, undefined);
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
    assert.match(home, /R0\.60 recap 之后的累计回顾收录 107 个节点；全站现有 167 篇公开研究笔记/);
    assert.match(literature, /id="r072q-boundary"/);
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
      latest: "r072p",
      version: "1.29",
      notes: 166,
      recap: 106,
      next: "r072q",
      gate: "tests/r072p-superposition-gate.test.mjs",
      publicationTest: "tests/r072p-release.test.mjs",
      published: 68,
      sealed: 44,
      backlog: 24,
    },
  );
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.29",
    latestRelease: "R0.72P",
    publicHtmlNoteCount: 166,
    publishedDate: "2026-08-27",
  });
  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 166);
  assert.match(home, /<strong>R0\.72P<\/strong>最新研究节点/);
  assert.match(home, /NEXT · R0\.72Q/);
  assert.match(literature, /开放接口 · R0\.72Q/);

  const stage = manifest.nextReleaseSourceStage;
  assert.deepEqual(stage, {
    release: "r072q",
    stage: "source-freeze",
    publicationStatus: "pending-formal-certificate-figure-and-publication",
    publicCountersAdvanced: false,
    report: "research/r072q_report-source.md",
    independentAudit: "research/r072q_independent_audit.md",
    producer: "research/r072q_exact_audit.py",
    independentProducer: "research/r072q_independent_audit.mjs",
    comparator: "research/r072q_compare_audits.py",
    certificateDirectory: "research/certificates/r072q",
    figureDirectory:
      "figures/r072q-phase-robust-shape/fig-r072q-phase-robust-shape",
    generator: "scripts/generate_r072q_release.py",
    translationScript: "scripts/add-r072q-translations.mjs",
    releaseGate: "tests/r072q-phase-robust-shape-gate.test.mjs",
    publicationTest: "tests/r072q-release.test.mjs",
  });
});

test("does not publish Q HTML, PDFs, or public figure masters at source stage", async () => {
  const manifest = await json("research/release-manifest.json");
  const publicArtifacts = [
    "public/notes/r0-72q.html",
    "public/notes/r0-72q.pdf",
    "public/recap-r0-61-r0-72q.html",
    "public/recap-r0-61-r0-72q.pdf",
    "public/assets/r072q/fig-r072q-phase-robust-shape.pdf",
    "public/assets/r072q/fig-r072q-phase-robust-shape.png",
    "public/assets/r072q/fig-r072q-phase-robust-shape.svg",
  ];
  if (manifest.latestCompletedRelease === "r072p") {
    for (const relative of publicArtifacts) await absent(relative);
    return;
  }
  assert.equal(manifest.latestCompletedRelease, "r072q");
  const [note, notePdf, recap, recapPdf, home, literature] = await Promise.all([
    text("public/notes/r0-72q.html"),
    readFile(resolve(root, "public/notes/r0-72q.pdf")),
    text("public/recap-r0-61-r0-72q.html"),
    readFile(resolve(root, "public/recap-r0-61-r0-72q.pdf")),
    text("public/research-review.html"),
    text("public/literature-review.html"),
  ]);
  for (const page of [note, recap, home, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.30"/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  }
  assert.match(note, /Q_2\\le1\/2/);
  assert.match(note, /\\mathfrak C_1\)=36|C_1=36/);
  assert.match(note, /z\(\\phi\)=\\frac18e\^{-3i\\phi\}-\\frac38e\^{-i\\phi\}/);
  assert.match(note, /R0\.72R/);
  assert.match(recap, /R0\.61–R0\.72Q 的 107 节公开笔记/);
  assert.match(recap, /R0\.70A–R0\.72Q 的 69 节已公开；45 节/);
  for (const [label, pdf] of [["note", notePdf], ["recap", recapPdf]]) {
    assert.equal(pdf.subarray(0, 4).toString(), "%PDF", label);
    assert.ok(pdf.length > 10_000, `${label} PDF is unexpectedly small`);
  }

  const figure = resolve(
    root,
    "figures/r072q-phase-robust-shape/fig-r072q-phase-robust-shape",
  );
  const certificate = resolve(root, "research/certificates/r072q");
  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  const figureManifest = JSON.parse(
    await readFile(resolve(figure, "manifest.json"), "utf8"),
  );
  assert.equal(figureManifest.release, "R0.72Q");
  assert.equal(figureManifest.figureId, "fig-r072q-phase-robust-shape");
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  for (const suffix of ["pdf", "png", "svg"]) {
    const master = await readFile(resolve(figure, `figure.${suffix}`));
    const published = await readFile(
      resolve(root, `public/assets/r072q/fig-r072q-phase-robust-shape.${suffix}`),
    );
    assert.equal(Buffer.compare(master, published), 0, `${suffix} byte identity`);
    assert.ok(note.includes(`/assets/r072q/fig-r072q-phase-robust-shape.${suffix}`));
  }
});

test("deterministic Q generator advances only after formal certificate and figure preflight", async () => {
  const generator = await text("scripts/generate_r072q_release.py");
  for (const token of [
    "public/notes/r0-72p.html",
    "public/recap-r0-61-r0-72p.html",
    "notes/r0-72q.html",
    "recap-r0-61-r0-72q.html",
    "research/r072q_report-source.md",
    "research/r072q_literature_audit.md",
    "research/r072q_gap_matrix.md",
    "research/r072q_independent_audit.md",
    "research/certificates/r072q",
    "figures/r072q-phase-robust-shape/fig-r072q-phase-robust-shape",
    "tests/r072q-phase-robust-shape-gate.test.mjs",
    "tests/r072q-release.test.mjs",
    "expected 167 public HTML notes",
    '"recapNodes": 107',
    '"published": 69',
    '"formalSealed": 45',
    '"legacyBacklog": 24',
    '"routeNotes": 77',
    '"next": "R0.72R"',
    "Q_2\\le1/2",
    "(\\pi/12,81,36)",
    "(C_1)_{F}=12",
    "z(\\phi)=\\frac18e^{-3i\\phi}-\\frac38e^{-i\\phi}",
    "temporaryUnsealedSourceAllowed",
    "verify_flat_hash_ledger",
    "strict figure validation failed",
    "publicCopiesComplete",
    "assert_mathjax_clean",
  ]) assert.ok(generator.includes(token), token);
  assert.ok(
    generator.indexOf('"latestCompletedRelease": "r072p"') <
      generator.indexOf('"latestCompletedRelease": "r072q"'),
  );
  assert.ok(
    generator.indexOf("validate_inputs()") < generator.indexOf("build_note()"),
    "formal preflight must precede the first public mutation",
  );
  assert.doesNotMatch(generator, /allow-unsealed-source|source-preview|skip-(?:seal|validation)/);
});

test("Q translation scaffold is check-only capable and bound to the four future pages", async () => {
  const [script, snapshot, manifest] = await Promise.all([
    text("scripts/add-r072q-translations.mjs"),
    json("scripts/i18n-snapshots/r072q-missing.json"),
    json("research/release-manifest.json"),
  ]);
  for (const token of [
    "R072Q_RELEASE_ROOT",
    "--check-only",
    "r072q-missing.json",
    "literature-review.html",
    "notes/r0-72q.html",
    "recap-r0-61-r0-72q.html",
    "research-review.html",
    "/i18n-en.js?v=1.30",
    "extractProtectedTokens",
    "containsChinese",
  ]) assert.ok(script.includes(token), token);
  assert.ok(Array.isArray(snapshot));
  assert.ok(snapshot.length > 0, "R0.72Q source-stage translation snapshot is empty");
  assert.ok(
    snapshot.some((entry) => entry.zh.includes("R0.72R")),
    "snapshot must include the next-release copy",
  );
  assert.ok(
    snapshot.some((entry) => entry.zh.includes("Coble shear") || entry.zh.includes("物理")),
    "snapshot must preserve the normalized/physical shape distinction",
  );
  if (manifest.latestCompletedRelease === "r072q") {
    const [translations, built] = await Promise.all([
      json("translations/en.json"),
      text("public/i18n-en.js"),
    ]);
    const batch = translations.filter((entry) => /^r072q\d+$/.test(entry.id));
    assert.equal(batch.length, snapshot.length);
    assert.deepEqual(
      [...new Set(batch.flatMap((entry) => entry.files))].sort(),
      [
        "literature-review.html",
        "notes/r0-72q.html",
        "recap-r0-61-r0-72q.html",
        "research-review.html",
      ],
    );
    for (const entry of batch) {
      assert.ok(entry.en.trim(), entry.zh);
      assert.doesNotMatch(entry.en, /[\u3400-\u9fff\uf900-\ufaff]/u);
      assert.ok(built.includes(JSON.stringify(entry.zh)), entry.zh);
    }
  }
});
