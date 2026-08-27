import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import { collectSiteStrings, extractProtectedTokens } from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");
const run = promisify(execFile);

async function text(relative) { return readFile(resolve(root, relative), "utf8"); }
async function json(relative) { return JSON.parse(await text(relative)); }
async function absent(relative) {
  await assert.rejects(access(resolve(root, relative)), (error) => error?.code === "ENOENT", relative);
}

const expectedSourceStage = {
  release: "r072t", stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072t_report-source.md",
  literatureAudit: "research/r072t_literature_audit.md",
  gapMatrix: "research/r072t_gap_matrix.md",
  independentAudit: "research/r072t_independent_audit.md",
  producer: "research/certificates/r072t/generate_certificate.py",
  independentProducer: "research/certificates/r072t/independent_recompute.py",
  comparator: "research/certificates/r072t/validate_certificate.py",
  certificateDirectory: "research/certificates/r072t",
  figureDirectory: "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model",
  generator: "scripts/generate_r072t_release.py",
  translationScript: "scripts/add-r072t-translations.mjs",
  releaseGate: "tests/r072t-a2-spacetime-gate.test.mjs",
  publicationTest: "tests/r072t-release.test.mjs",
};

async function assertSourceStage() {
  const [manifest, site, noteFiles, home, recap] = await Promise.all([
    json("research/release-manifest.json"), json("public/site-version.json"),
    readdir(resolve(publicRoot, "notes")), text("public/research-review.html"),
    text("public/recap-r0-61-r0-72s.html"),
  ]);
  assert.deepEqual({
    latest: manifest.latestCompletedRelease, version: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount, recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease, published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  }, { latest: "r072s", version: "1.32", notes: 169, recap: 109,
    next: "r072t", published: 71, sealed: 47, backlog: 24 });
  assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
  assert.deepEqual(site, { schemaVersion: "research-site-version-v1", version: "1.32",
    latestRelease: "R0.72S", publicHtmlNoteCount: 169, publishedDate: "2026-08-28" });
  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 169);
  assert.match(home, /<strong>169<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72S<\/strong>最新研究节点/);
  assert.doesNotMatch(home, /data-release="r072t"/);
  const links = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map((match) => match[1]);
  assert.equal(links.length, 109);
  assert.equal(new Set(links).size, 109);
  for (const relative of ["public/notes/r0-72t.html", "public/notes/r0-72t.pdf",
    "public/recap-r0-61-r0-72t.html", "public/recap-r0-61-r0-72t.pdf"]) await absent(relative);
}

function nodeIndex(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  return recap.slice(start, end);
}

async function inspectPdf(relative) {
  const pdf = await readFile(resolve(root, relative));
  const source = pdf.toString("latin1");
  const pages = [...source.matchAll(/\/Type\s*\/Page\b/g)].length;
  const titleHex = source.match(/\/Title\s*<([0-9a-f]+)>/i)?.[1];
  assert.ok(titleHex, `${relative}: hexadecimal PDF title metadata`);
  const bytes = Buffer.from(titleHex, "hex");
  const units = [];
  if (bytes[0] === 0xfe && bytes[1] === 0xff) {
    for (let index = 2; index + 1 < bytes.length; index += 2) units.push(bytes.readUInt16BE(index));
  }
  return { pages, title: units.length ? String.fromCharCode(...units) : bytes.toString("latin1"), bytes: pdf.length };
}

async function verifyFlatHashLedger(relative) {
  const directory = resolve(root, relative);
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8")).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, `malformed SHA256SUMS row: ${row}`);
    const [, expected, name] = match;
    const actual = createHash("sha256").update(await readFile(resolve(directory, name))).digest("hex");
    assert.equal(actual, expected, name);
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(names, entries.filter((entry) => entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name)).map((entry) => entry.name).sort());
}

test("R0.72T advances the public counters atomically to v1.33", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072s") { await assertSourceStage(); return; }
  const [site, archive, noteFiles, home, recap] = await Promise.all([
    json("public/site-version.json"), json("research/formal-archive-inventory.json"),
    readdir(resolve(publicRoot, "notes")), text("public/research-review.html"),
    text("public/recap-r0-61-r0-72t.html"),
  ]);
  assert.deepEqual(
    {
      latest: manifest.latestCompletedRelease, version: manifest.siteVersion,
      notes: manifest.publicHtmlNoteCount, recap: manifest.postR060RecapNodeCount,
      next: manifest.nextRelease, published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    },
    { latest: "r072t", version: "1.33", notes: 170, recap: 110,
      next: "r072u", published: 72, sealed: 48, backlog: 24 },
  );
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1", version: "1.33",
    latestRelease: "R0.72T", publicHtmlNoteCount: 170,
    publishedDate: "2026-08-28",
  });
  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 170);
  assert.match(home, /<strong>R0\.72T<\/strong>最新研究节点/);
  assert.match(home, /NEXT · R0\.72U/);
  assert.match(home, /累计回顾收录 110 个节点；全站现有 170 篇公开研究笔记/);
  const links = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map((match) => match[1]);
  assert.equal(links.length, 110);
  assert.equal(new Set(links).size, 110);
  assert.equal(links.filter((slug) => slug === "r0-72t").length, 1);
  assert.equal([...recap.matchAll(/<article class="phase">/g)].length, 29);
  assert.deepEqual(
    { latest: archive.latestPublishedRelease, published: archive.publishedReleaseCount,
      sealed: archive.formalSealedReleaseCount, backlog: archive.legacyFormalFigureBacklogCount },
    { latest: "r072t", published: 72, sealed: 48, backlog: 24 },
  );
  assert.equal(archive.publishedReleases.at(-1), "r072t");
  assert.equal(archive.formalSealedReleases.at(-1), "r072t");
});

test("R0.72T public prose preserves the exact negative boundary and individual voice", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072s") { await assertSourceStage(); return; }
  const pages = await Promise.all([
    "public/notes/r0-72t.html", "public/recap-r0-61-r0-72t.html",
    "public/research-review.html", "public/literature-review.html",
  ].map(text));
  for (const page of pages) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.33"/);
    assert.doesNotMatch(page, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /[A-Za-z0-9_}]\\\(/);
  }
  const note = pages[0];
  for (const token of ["W_d=W_{xx}", "H_3=X^3+6SX", "\\nu a^2T^5", "1/720", "6/7",
    "blockContraction=OPEN", "periodicTransfer=OPEN", "R0.72U", "Clay"]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /derivative-versus-primitive/);
  assert.match(note, /CDZE/);
  assert.match(note, /Poincaré gap/);
  assert.match(note, /compact \\(H\^1\\to L\^2\\)/);
  assert.match(note, /step five/);
  assert.match(pages[3], /id="r072t-boundary"/);
  assert.match(pages[3], /开放接口 · R0\.72U/);
});

test("R0.72T synchronizes PDFs and the formal figure bytes", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072s") { await assertSourceStage(); return; }
  for (const [relative, tokens] of [
    ["public/notes/r0-72t.pdf", ["R0.72T"]],
    ["public/recap-r0-61-r0-72t.pdf", ["R0.61", "R0.72T"]],
  ]) {
    const inspected = await inspectPdf(relative);
    assert.ok(inspected.bytes > 10_000);
    assert.ok(inspected.pages >= 2 && inspected.pages <= 40);
    for (const token of tokens) assert.ok(inspected.title.includes(token), `${relative}: ${token}`);
  }
  const figure = "figures/r072t-a2-spacetime-model/fig-r072t-a2-spacetime-model";
  const certificate = "research/certificates/r072t";
  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  const [certificateManifest, crosscheck, figureManifest] = await Promise.all([
    json(`${certificate}/manifest.json`), json(`${certificate}/crosscheck.json`),
    json(`${figure}/manifest.json`),
  ]);
  assert.equal(certificateManifest.status, "formal");
  assert.match(certificateManifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.ok(Array.isArray(certificateManifest.sourceBindings) && certificateManifest.sourceBindings.length > 0);
  assert.equal(crosscheck.formalSourceReady, true);
  assert.equal(crosscheck.sourceCommit, certificateManifest.sourceCommit);
  assert.deepEqual(crosscheck.sourceBindings, certificateManifest.sourceBindings);
  await run(process.env.CODEX_PYTHON || "python3", [
    "research/certificates/r072t/validate_certificate.py", "--require-formal",
  ], { cwd: root });
  assert.equal(figureManifest.release, "R0.72T");
  assert.equal(figureManifest.figureId, "fig-r072t-a2-spacetime-model");
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  const note = await text("public/notes/r0-72t.html");
  for (const suffix of ["pdf", "png", "svg"]) {
    const master = await readFile(resolve(root, figure, `figure.${suffix}`));
    const route = `/assets/r072t/fig-r072t-a2-spacetime-model.${suffix}`;
    const published = await readFile(resolve(publicRoot, route.slice(1)));
    assert.equal(Buffer.compare(master, published), 0, suffix);
    assert.ok(note.includes(route), route);
  }
});

test("R0.72T bilingual dictionary covers every live Chinese string exactly", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072s") { await assertSourceStage(); return; }
  const translations = await json("translations/en.json");
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry.en]));
  assert.equal(byChinese.size, translations.length);
  const source = await collectSiteStrings(publicRoot);
  const missing = source.filter((entry) => !byChinese.has(entry.zh));
  assert.deepEqual(missing, []);
  for (const entry of source) {
    const english = byChinese.get(entry.zh);
    assert.ok(english?.trim(), entry.zh);
    assert.doesNotMatch(english, /[\u3400-\u9fff]/);
    assert.doesNotMatch(english, /\b(?:we|our|ours|ourselves|us)\b/i);
    assert.deepEqual(extractProtectedTokens(english), extractProtectedTokens(entry.zh), entry.zh);
  }
  const bundle = await text("public/i18n-en.js");
  assert.match(bundle, /R0\.72T/);
});
