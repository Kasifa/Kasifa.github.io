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

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function absent(relative) {
  await assert.rejects(access(resolve(root, relative)), (error) => error?.code === "ENOENT", relative);
}

const expectedSourceStage = {
  release: "r072u",
  stage: "source-freeze",
  publicationStatus: "pending-formal-certificate-figure-and-publication",
  publicCountersAdvanced: false,
  report: "research/r072u_report-source.md",
  literatureAudit: "research/r072u_literature_audit.md",
  gapMatrix: "research/r072u_gap_matrix.md",
  independentAudit: "research/r072u_independent_audit.md",
  producer: "research/certificates/r072u/generate_certificate.py",
  independentProducer: "research/certificates/r072u/independent_recompute.py",
  comparator: "research/certificates/r072u/validate_certificate.py",
  certificateDirectory: "research/certificates/r072u",
  figureDirectory: "figures/r072u-local-observability/fig-r072u-two-moment-coercivity",
  generator: "scripts/generate_r072u_release.py",
  translationScript: "scripts/add-r072u-translations.mjs",
  releaseGate: "tests/r072u-local-observability-gate.test.mjs",
  publicationTest: "tests/r072u-release.test.mjs",
};

function nodeIndex(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  return recap.slice(start, end);
}

async function assertSourceStage() {
  const [manifest, site, noteFiles, home, recap] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    readdir(resolve(publicRoot, "notes")),
    text("public/research-review.html"),
    text("public/recap-r0-61-r0-72t.html"),
  ]);
  assert.deepEqual({
    latest: manifest.latestCompletedRelease,
    version: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount,
    recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease,
    published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  }, {
    latest: "r072t",
    version: "1.33",
    notes: 170,
    recap: 110,
    next: "r072u",
    published: 72,
    sealed: 48,
    backlog: 24,
  });
  assert.deepEqual(manifest.nextReleaseSourceStage, expectedSourceStage);
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.33",
    latestRelease: "R0.72T",
    publicHtmlNoteCount: 170,
    publishedDate: "2026-08-28",
  });
  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 170);
  assert.match(home, /<strong>170<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72T<\/strong>最新研究节点/);
  assert.doesNotMatch(home, /data-release="r072u"/);
  const links = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(links.length, 110);
  assert.equal(new Set(links).size, 110);
  for (const relative of [
    "public/notes/r0-72u.html",
    "public/notes/r0-72u.pdf",
    "public/recap-r0-61-r0-72u.html",
    "public/recap-r0-61-r0-72u.pdf",
  ]) await absent(relative);
}

async function inspectPdf(relative) {
  const pdf = await readFile(resolve(root, relative));
  const source = pdf.toString("latin1");
  const pages = [...source.matchAll(/\/Type\s*\/Page\b/g)].length;
  const titleHex = source.match(/\/Title\s*<([0-9a-f]+)>/i)?.[1];
  assert.ok(titleHex, relative + ": hexadecimal PDF title metadata");
  const bytes = Buffer.from(titleHex, "hex");
  const units = [];
  if (bytes[0] === 0xfe && bytes[1] === 0xff) {
    for (let index = 2; index + 1 < bytes.length; index += 2) {
      units.push(bytes.readUInt16BE(index));
    }
  }
  return {
    pages,
    title: units.length ? String.fromCharCode(...units) : bytes.toString("latin1"),
    bytes: pdf.length,
    source,
  };
}

async function verifyFlatHashLedger(relative) {
  const directory = resolve(root, relative);
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, "malformed SHA256SUMS row: " + row);
    const [, expected, name] = match;
    const actual = createHash("sha256")
      .update(await readFile(resolve(directory, name))).digest("hex");
    assert.equal(actual, expected, name);
    names.push(name);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries
      .filter((entry) => entry.isFile() && !["SHA256SUMS", ".DS_Store"].includes(entry.name))
      .map((entry) => entry.name).sort(),
  );
}

test("R0.72U advances the public counters atomically to v1.34", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072t") {
    await assertSourceStage();
    return;
  }
  const [site, archive, noteFiles, home, recap] = await Promise.all([
    json("public/site-version.json"),
    json("research/formal-archive-inventory.json"),
    readdir(resolve(publicRoot, "notes")),
    text("public/research-review.html"),
    text("public/recap-r0-61-r0-72u.html"),
  ]);
  assert.deepEqual({
    latest: manifest.latestCompletedRelease,
    version: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount,
    recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease,
    published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  }, {
    latest: "r072u",
    version: "1.34",
    notes: 171,
    recap: 111,
    next: "r072v",
    published: 73,
    sealed: 49,
    backlog: 24,
  });
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.34",
    latestRelease: "R0.72U",
    publicHtmlNoteCount: 171,
    publishedDate: "2026-08-28",
  });
  assert.equal(noteFiles.filter((name) => name.endsWith(".html")).length, 171);
  assert.match(home, /<strong>R0\.72U<\/strong>最新研究节点/);
  assert.match(home, /NEXT · R0\.72V/);
  assert.match(home, /累计回顾收录 111 个节点；全站现有 171 篇公开研究笔记/);
  const links = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(links.length, 111);
  assert.equal(new Set(links).size, 111);
  assert.equal(links.filter((slug) => slug === "r0-72u").length, 1);
  assert.equal([...recap.matchAll(/<article class="phase">/g)].length, 30);
  assert.deepEqual({
    latest: archive.latestPublishedRelease,
    published: archive.publishedReleaseCount,
    sealed: archive.formalSealedReleaseCount,
    backlog: archive.legacyFormalFigureBacklogCount,
  }, {
    latest: "r072u",
    published: 73,
    sealed: 49,
    backlog: 24,
  });
  assert.equal(archive.publishedReleases.at(-1), "r072u");
  assert.equal(archive.formalSealedReleases.at(-1), "r072u");
});

test("R0.72U public prose preserves the exact local-to-global boundary and individual voice", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072t") {
    await assertSourceStage();
    return;
  }
  const pages = await Promise.all([
    "public/notes/r0-72u.html",
    "public/recap-r0-61-r0-72u.html",
    "public/research-review.html",
    "public/literature-review.html",
  ].map(text));
  for (const page of pages) {
    assert.match(page, /src="\/i18n-en\.js\?v=1\.34"/);
    assert.doesNotMatch(page, /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /[A-Za-z0-9_}]\\\(/);
  }
  const note = pages[0];
  for (const token of [
    "Poincare-trivial",
    "centerUniformLocalGraphCoercivity",
    "localSolutionObservability",
    "wholeLineBlockContraction=OPEN",
    "periodicTransfer=OPEN",
    "R0.72V",
    "Clay",
  ]) assert.ok(note.includes(token), token);
  assert.match(note, /没有时间 cutoff，没有空间零迹/);
  assert.match(note, /A'=iLB\+E_0/);
  assert.match(note, /B'=iL\\mu_2A\+iLF_2\+E_1/);
  assert.ok(note.includes("v\\in C(\\overline I;H_D^{-1})"));
  assert.match(note, /不保证[^。]*v\\in C\(\\overline I;L\^2\)/);
  assert.match(note, /boundary flux/);
  assert.ok(note.includes("\\(J\\supset[-1,1]\\)"));
  assert.match(note, /27\/13[^。]*4\/5[^。]*\\\(T=1\\\)/);
  assert.match(pages[3], /id="r072u-boundary"/);
  assert.match(pages[3], /开放接口 · R0\.72V/);
  assert.match(
    pages[3],
    /<p class="deck">.*R0\.72T 进一步固定.*R0\.72U 随后排除 literal spatial-cutoff.*一般 Navier–Stokes 正则性仍开放。<\/p>/s,
  );
});

test("R0.72U synchronizes PDFs and the formal figure bytes", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072t") {
    await assertSourceStage();
    return;
  }
  for (const [relative, tokens, bodyUris] of [
    ["public/notes/r0-72u.pdf", ["R0.72U"], [
      "https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072u_report-source.md",
      "https://kasifa.github.io/assets/r072u/fig-r072u-two-moment-coercivity.pdf",
      "https://kasifa.github.io/recap-r0-61-r0-72u.html",
    ]],
    ["public/recap-r0-61-r0-72u.pdf", ["R0.61", "R0.72U"], [
      "https://kasifa.github.io/notes/r0-72u.html",
      "https://kasifa.github.io/assets/r072u/fig-r072u-two-moment-coercivity.pdf",
    ]],
  ]) {
    const inspected = await inspectPdf(relative);
    assert.ok(inspected.bytes > 10_000);
    assert.ok(inspected.pages >= 2 && inspected.pages <= 40);
    for (const token of tokens) {
      assert.ok(inspected.title.includes(token), relative + ": " + token);
    }
    for (const uri of bodyUris) {
      assert.ok(inspected.source.includes(`/URI (${uri})`), `${relative}: ${uri}`);
    }
  }
  const figure = "figures/r072u-local-observability/fig-r072u-two-moment-coercivity";
  const certificate = "research/certificates/r072u";
  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  const [certificateManifest, crosscheck, figureManifest] = await Promise.all([
    json(certificate + "/manifest.json"),
    json(certificate + "/crosscheck.json"),
    json(figure + "/manifest.json"),
  ]);
  assert.equal(certificateManifest.status, "formal");
  assert.match(certificateManifest.sourceCommit, /^[0-9a-f]{40}$/);
  assert.ok(Array.isArray(certificateManifest.sourceBindings));
  assert.ok(certificateManifest.sourceBindings.length > 0);
  assert.equal(crosscheck.formalSourceReady, true);
  assert.equal(crosscheck.sourceCommit, certificateManifest.sourceCommit);
  assert.deepEqual(crosscheck.sourceBindings, certificateManifest.sourceBindings);
  await run(process.env.CODEX_PYTHON || "python3", [
    "research/certificates/r072u/validate_certificate.py", "--require-formal",
  ], { cwd: root });
  await run(process.env.CODEX_PYTHON || "python3", [
    "figures/r072u-local-observability/fig-r072u-two-moment-coercivity/validate.py",
    "--require-formal",
  ], { cwd: root });
  assert.equal(figureManifest.release, "R0.72U");
  assert.equal(figureManifest.figureId, "fig-r072u-two-moment-coercivity");
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.qa.status, "passed");
  assert.equal(figureManifest.qa.visualInspectionExplicit, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  const note = await text("public/notes/r0-72u.html");
  for (const suffix of ["pdf", "png", "svg"]) {
    const master = await readFile(resolve(root, figure, "figure." + suffix));
    const route = "/assets/r072u/fig-r072u-two-moment-coercivity." + suffix;
    const published = await readFile(resolve(publicRoot, route.slice(1)));
    assert.equal(Buffer.compare(master, published), 0, suffix);
    assert.ok(note.includes(route), route);
  }
});

test("R0.72U bilingual dictionary covers every live Chinese string exactly", async () => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease === "r072t") {
    await assertSourceStage();
    return;
  }
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
  assert.match(bundle, /R0\.72U/);
});
