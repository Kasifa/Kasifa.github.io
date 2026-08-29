import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import {
  collectSiteStrings,
  containsChinese,
  extractProtectedTokens,
} from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");
const figure = "figures/r073f/fig-r073f-fixed-window-roughness";
const figureId = "fig-r073f-fixed-window-roughness";
const sourceCommit = "5edb1702314feca3e9d47a186b30fc53079cd67a";
const run = promisify(execFile);
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const sha = async (relative) =>
  createHash("sha256").update(await readFile(resolve(root, relative))).digest("hex");

function assertPublicVoice(value, label) {
  for (const phrase of [
    "我们",
    "攻关",
    "主攻",
    "突破",
    "研究纪律",
    "三重审计",
    "杀死错误想法",
  ]) {
    assert.equal(value.includes(phrase), false, `${label}: ${phrase}`);
  }
}

function nodeIndex(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  return recap.slice(start, end);
}

function accountingTokens(value) {
  return [...value.matchAll(
    /R0\.\d+[A-Z]?|v\d+(?:\.\d+)+|(?<![\p{L}\p{N}_])\d+(?:\.\d+)?(?![\p{L}\p{N}_])/gu,
  )].map((match) => match[0]);
}

async function inspectPdf(relative) {
  const bytes = await readFile(resolve(root, relative));
  const latin = bytes.toString("latin1");
  return {
    bytes: bytes.length,
    pages: [...latin.matchAll(/\/Type\s*\/Page\b/g)].length,
    header: bytes.subarray(0, 4).toString("latin1"),
  };
}

async function assertSourceBindings(rows, label) {
  assert.ok(Array.isArray(rows) && rows.length >= 6, label);
  for (const row of rows) {
    const commit = row.sourceCommit ?? row.commit;
    assert.equal(commit, sourceCommit, `${label}: ${row.path}`);
    assert.equal(row.sha256, await sha(row.path), `${label}: ${row.path}`);
  }
}

test("R0.73F release source pins the v1.46 transaction and GitHub-only contract", async () => {
  const [generator, content, translation, runner, agents] = await Promise.all([
    text("scripts/generate_r073f_release.py"),
    text("scripts/r073f_release_content.py"),
    text("scripts/add-r073f-translations.mjs"),
    text("scripts/run-release-publication-gate.mjs"),
    text("AGENTS.md"),
  ]);
  const source = generator + "\n" + content;
  for (const token of [
    "R073E_RELEASE_BASELINE",
    '"siteVersion": "1.45"',
    '"publicHtmlNoteCount": 181',
    '"siteVersion": "1.46"',
    '"publicHtmlNoteCount": 182',
    '"postR060RecapNodeCount": 122',
    '"postR070APublishedReleaseCount": 84',
    '"postR070AFormalSealedReleaseCount": 60',
    '"legacyFormalFigureBacklogCount": 24',
    '"nextRelease": "r073g"',
    "122 unique nodes",
    "41 phases",
    "92 note links",
    "verify_complete_flat_ledger",
    "verify_source_bindings",
    "CERTIFIED_REPORT_COMMIT",
    "FIGURE_PACKAGE_COMMIT",
    "CERTIFICATE_PACKAGE_COMMIT",
    "FIGURE_METADATA_SEAL_COMMIT",
  ]) assert.ok(source.includes(token), token);
  for (const token of [
    "boundedPerturbationRoughnessWithNoninvertibleStableSemigroup=CLOSED",
    "movingProfileUniformContour=CLOSED",
    "movingInstantaneousProjectionNormC1=CLOSED",
    "movingProfileEvolutionDichotomy=CLOSED",
    "fixedWindowExponentialLowerLaw=CLOSED",
    "fixedWindowLogGainThetaLambda=CLOSED",
    "spectralGapPlusBoundedC1PlusCommonDomainImpliesMovingDichotomy=FALSE",
    "instantaneousPositiveSpectralAbscissaImpliesFixedWindowGrowth=FALSE",
    "graphDomainKatoTransport=OPEN_NOT_USED",
    "completeOSSquireA2DirectSum=OPEN",
    "nonlinearNavierStokes=OPEN",
    "Clay=OPEN",
    "R0.73G",
    "seed size",
    "mode-convolution remainder",
    '<a class="route-map-latest" href="/notes/r0-73f.pdf">阅读最新 R0.73F 研究笔记 →</a>',
  ]) assert.ok(content.includes(token), token);
  assertPublicVoice(content, "R0.73F content source");
  const main = generator.slice(generator.indexOf("def main() -> None:"));
  const calls = [
    "preflight_release_state()",
    "validate_inputs()",
    "stage_figure_assets(staged, figure_manifest)",
    "build_note()",
    "build_recap()",
    "update_home()",
    "update_literature()",
    "build_manifest_outputs()",
    "build_note_index(",
    "validate_staged(staged)",
    "commit_transaction(staged)",
  ].map((call) => main.indexOf(call));
  assert.ok(calls.every((index) => index >= 0));
  assert.deepEqual(calls, [...calls].sort((a, b) => a - b));
  assert.match(translation, /R073F_RELEASE_ROOT/);
  assert.match(translation, /i18n-en\.js\?v=1\.46/);
  assert.match(translation, /i18n-snapshots\/r073f-missing\.json/);
  assert.match(translation, /"r073f"\s*\+\s*String\(index \+ 1\)/);
  assert.match(translation, /Version\/count-token mismatch/);
  assert.match(runner, /latest release publication test/);
  assert.match(runner, /resolvedGate\.publication/);
  assert.match(agents, /Publish this project only through the GitHub repository/);
  assert.match(agents, /https:\/\/kasifa\.github\.io\//);
  assert.match(agents, /Do not mirror or deploy the project to another hosting service/);
  assert.doesNotMatch(source, /netlify\.app|vercel\.app|pages\.dev/i);
});

test("R0.73F manifests advance v1.46 and the 84/60/24 archive counters once", async () => {
  const [manifest, site, archive, version] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    json("research/formal-archive-inventory.json"),
    text("VERSION"),
  ]);
  assert.deepEqual({
    latest: manifest.latestCompletedRelease,
    version: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount,
    recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease,
    gate: manifest.latestReleaseGate,
    publication: manifest.latestReleasePublicationTest,
    published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  }, {
    latest: "r073f",
    version: "1.46",
    notes: 182,
    recap: 122,
    next: "r073g",
    gate: "tests/r073f-moving-dichotomy-gate.test.mjs",
    publication: "tests/r073f-release.test.mjs",
    published: 84,
    sealed: 60,
    backlog: 24,
  });
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.46",
    latestRelease: "R0.73F",
    publicHtmlNoteCount: 182,
    publishedDate: "2026-08-30",
  });
  assert.equal(version, "1.46\n");
  assert.equal(archive.latestPublishedRelease, "r073f");
  assert.equal(archive.publishedReleaseCount, 84);
  assert.equal(archive.formalSealedReleaseCount, 60);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.equal(archive.publishedReleases.at(-1), "r073f");
  assert.equal(archive.formalSealedReleases.at(-1), "r073f");
  assert.equal(archive.publishedReleases.filter((value) => value === "r073f").length, 1);
  assert.equal(archive.formalSealedReleases.filter((value) => value === "r073f").length, 1);
  assert.deepEqual(manifest.formalArchiveInventory, {
    path: "research/formal-archive-inventory.json",
    sha256: await sha("research/formal-archive-inventory.json"),
  });
});

test("R0.73F note, homepage card, route 92, recap 122/41, index, and literature agree", async () => {
  const [note, recap, home, literature, noteIndex] = await Promise.all([
    text("public/notes/r0-73f.html"),
    text("public/recap-r0-61-r0-73f.html"),
    text("public/research-review.html"),
    text("public/literature-review.html"),
    text("public/notes/index.html"),
  ]);
  const noteFiles = await readdir(resolve(publicRoot, "notes"));
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 182);
  for (const token of [
    "boundedPerturbationRoughnessWithNoninvertibleStableSemigroup=CLOSED",
    "movingProfileUniformContour=CLOSED",
    "movingProfileEvolutionDichotomy=CLOSED",
    "fixedWindowExponentialLowerLaw=CLOSED",
    "fixedWindowLogGainThetaLambda=CLOSED",
    "spectralGapPlusBoundedC1PlusCommonDomainImpliesMovingDichotomy=FALSE",
    "graphDomainKatoTransport=OPEN_NOT_USED",
    "completeOSSquireA2DirectSum=OPEN",
    "nonlinearNavierStokes=OPEN",
    "Clay=OPEN",
    `/assets/r073f/${figureId}.svg`,
    "/notes/r0-73f.pdf",
    "/recap-r0-61-r0-73f.html",
    "R0.73G",
    "doi.org/10.1006/jdeq.1999.3668",
    "doi.org/10.1007/BFb0067780",
    "doi.org/10.1142/S0129055X19500144",
    "doi.org/10.1007/s00220-007-0299-y",
  ]) assert.ok(note.includes(token), token);
  const nodes = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(nodes.length, 122);
  assert.equal(new Set(nodes).size, 122);
  assert.equal(nodes.at(-1), "r0-73f");
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 41);
  for (const token of [
    "R0.61–R0.69W",
    "R0.70A–R0.71Z",
    "R0.72A–R0.73B",
    "R0.73C–F",
    "84 个版本已经公开",
    "60 个满足当前完整封存合同",
    "24 个历史版本",
    "R0.73G",
  ]) assert.ok(recap.includes(token), token);
  const firstScreen = home.slice(0, home.indexOf('<section class="route-overview" id="route-map"'));
  for (const token of [
    "LATEST RELEASE · R0.73F",
    "当前端点 R0.73F",
    "182 篇研究笔记总索引",
    "122 节累计回顾",
    "R0.70A–R0.73F · 84 节已公开",
    "60 节完整封存",
  ]) assert.ok(firstScreen.includes(token), token);
  assert.equal((home.match(/data-release="r073f"/g) ?? []).length, 1);
  const route = home.match(/<nav class="route-note-links" aria-label="R0\.69P–R0\.73F">([\s\S]*?)<\/nav>/)?.[1] ?? "";
  assert.equal((route.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length, 92);
  assert.equal((home.match(/<strong style="color:var\(--gold\)">下一步 R0\.73G：/g) ?? []).length, 1);
  assert.ok(literature.includes('id="r073f-boundary"'));
  assert.ok(literature.includes("开放接口 · R0.73G"));
  assert.ok(noteIndex.includes('data-note="r0-73f"'));
  assert.ok(noteIndex.includes("182 篇公开研究笔记"));
  for (const [value, label] of [
    [note, "note"],
    [recap, "recap"],
    [home, "home"],
    [literature, "literature"],
    [noteIndex, "index"],
  ]) {
    assert.ok(value.includes('/i18n-en.js?v=1.46'), label);
    assertPublicVoice(value, label);
  }
});

test("R0.73F formal figure/certificate manifests preserve source/F/C/S provenance", async () => {
  const [figureManifest, figureValidation, certificateManifest, certificate, certificateValidation, generator] = await Promise.all([
    json(`${figure}/manifest.json`),
    json(`${figure}/validation.json`),
    json("research/certificates/r073f/manifest.json"),
    json("research/certificates/r073f/certificate.json"),
    json("research/certificates/r073f/validation.json"),
    text("scripts/generate_r073f_release.py"),
  ]);
  const figureCommit = generator.match(/FIGURE_PACKAGE_COMMIT\s*=\s*"([0-9a-f]{40})"/)?.[1];
  const certificateCommit = generator.match(/CERTIFICATE_PACKAGE_COMMIT\s*=\s*"([0-9a-f]{40})"/)?.[1];
  const figureSealCommit = generator.match(/FIGURE_METADATA_SEAL_COMMIT\s*=\s*"([0-9a-f]{40})"/)?.[1];
  assert.ok(figureCommit);
  assert.ok(certificateCommit);
  assert.ok(figureSealCommit);
  assert.equal(new Set([sourceCommit, figureCommit, certificateCommit, figureSealCommit]).size, 4);
  for (const [ancestor, descendant, label] of [
    [sourceCommit, figureCommit, "source < F"],
    [figureCommit, certificateCommit, "F < C"],
    [certificateCommit, figureSealCommit, "C < S"],
    [figureSealCommit, "HEAD", "S < release HEAD"],
  ]) {
    await assert.doesNotReject(
      run("git", ["merge-base", "--is-ancestor", ancestor, descendant], { cwd: root }),
      label,
    );
  }
  const sealedTree = (await run(
    "git",
    ["ls-tree", "-r", "--name-only", figureSealCommit, "--", figure],
    { cwd: root },
  )).stdout.trim().split("\n").filter(Boolean).sort();
  const currentEntries = await readdir(resolve(root, figure), { withFileTypes: true });
  assert.ok(currentEntries.every((entry) => entry.isFile()), "the formal figure package must remain flat");
  const currentTree = currentEntries.map((entry) => `${figure}/${entry.name}`).sort();
  assert.deepEqual(currentTree, sealedTree, "the current formal figure ledger must equal seal S");
  for (const relative of sealedTree) {
    const [sealedBlob, currentBlob] = await Promise.all([
      run("git", ["rev-parse", `${figureSealCommit}:${relative}`], { cwd: root }),
      run("git", ["hash-object", relative], { cwd: root }),
    ]);
    assert.equal(currentBlob.stdout.trim(), sealedBlob.stdout.trim(), `${relative}: differs from seal S`);
  }
  assert.equal(figureManifest.figureId, figureId);
  assert.equal(figureManifest.status, "formal");
  assert.equal(figureManifest.git.sourceCommit, sourceCommit);
  assert.equal(figureManifest.git.figurePackageCommit, figureCommit);
  assert.equal(figureManifest.git.certificateCommit, certificateCommit);
  assert.equal(figureValidation.status, "passed");
  assert.equal(certificate.sourceCommit, sourceCommit);
  assert.equal(certificateManifest.sourceCommit, sourceCommit);
  assert.equal(certificateValidation.allChecksPass, true);
  await assertSourceBindings(figureManifest.sourceBindings, "figure source bindings");
  await assertSourceBindings(certificateManifest.sourceBindings, "certificate source bindings");
  for (const suffix of ["pdf", "png", "svg"]) {
    assert.equal(await sha(`${figure}/figure.${suffix}`), await sha(`public/assets/r073f/${figureId}.${suffix}`), suffix);
  }
  const note = await inspectPdf("public/notes/r0-73f.pdf");
  const recap = await inspectPdf("public/recap-r0-61-r0-73f.pdf");
  assert.equal(note.header, "%PDF");
  assert.equal(recap.header, "%PDF");
  assert.ok(note.bytes > 25_000 && note.pages >= 2, JSON.stringify(note));
  assert.ok(recap.bytes > 50_000 && recap.pages >= 4, JSON.stringify(recap));
});

test("R0.73F English dictionary is complete, neutral, and token-preserving", async () => {
  const source = await collectSiteStrings(publicRoot);
  const translations = await json("translations/en.json");
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry.en]));
  assert.equal(byChinese.size, translations.length);
  assert.deepEqual(source.filter((entry) => !byChinese.has(entry.zh)), []);
  const boundaryTokens = (value) =>
    value.match(/\b(?:CLOSED|OPEN|FALSE|CONDITIONAL)\b/g) ?? [];
  const batch = translations.filter((row) => /^r073f\d+$/.test(row.id));
  assert.ok(batch.length > 0);
  for (const entry of batch) {
    assert.equal(containsChinese(entry.en), false, entry.zh);
    assert.equal(/\b(?:we|our|ours|ourselves|us)\b/i.test(entry.en), false, entry.zh);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh), entry.zh);
    assert.deepEqual(accountingTokens(entry.en), accountingTokens(entry.zh), entry.zh);
    assert.deepEqual(boundaryTokens(entry.en), boundaryTokens(entry.zh), entry.zh);
  }
  const result = await run(process.execPath, [
    "scripts/add-r073f-translations.mjs",
    "--check-only",
  ], { cwd: root, maxBuffer: 16 * 1024 * 1024 });
  assert.match(result.stdout, /"missingAfter":0/);
});

test("R0.73F GitHub Pages publication has no alternate-host deployment contract", async () => {
  for (const relative of ["netlify.toml", "vercel.json", "wrangler.toml"]) {
    await assert.rejects(access(resolve(root, relative)));
  }
  const [pages, agents] = await Promise.all([
    text(".github/workflows/pages.yml"),
    text("AGENTS.md"),
  ]);
  assert.match(pages, /actions\/deploy-pages@/);
  assert.match(agents, /GitHub Pages site at `https:\/\/kasifa\.github\.io\/`/);
  assert.match(agents, /Do not mirror or deploy/);
});
