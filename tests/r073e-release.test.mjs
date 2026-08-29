import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import { collectSiteStrings, containsChinese, extractProtectedTokens } from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const publicRoot = resolve(root, "public");
const figure = "figures/r073e/fig-r073e-complement-transfer";
const figureId = "fig-r073e-complement-transfer";
const run = promisify(execFile);
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const sha = async (relative) => createHash("sha256").update(await readFile(resolve(root, relative))).digest("hex");

function assertPublicVoice(value, label) {
  for (const phrase of ["我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法"]) {
    assert.equal(value.includes(phrase), false, `${label}: ${phrase}`);
  }
}

function nodeIndex(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  return recap.slice(start, end);
}

async function inspectPdf(relative) {
  const bytes = await readFile(resolve(root, relative));
  const latin = bytes.toString("latin1");
  return { bytes: bytes.length, pages: [...latin.matchAll(/\/Type\s*\/Page\b/g)].length, header: bytes.subarray(0, 4).toString("latin1") };
}

test("R0.73E release source pins the v1.45 transaction and exact route counts", async () => {
  const [generator, content, translation] = await Promise.all([
    text("scripts/generate_r073e_release.py"),
    text("scripts/r073e_release_content.py"),
    text("scripts/add-r073e-translations.mjs"),
  ]);
  const source = generator + "\n" + content;
  for (const token of [
    "R073D_RELEASE_BASELINE", '"siteVersion": "1.44"', '"publicHtmlNoteCount": 180',
    '"siteVersion": "1.45"', '"publicHtmlNoteCount": 181',
    '"postR060RecapNodeCount": 121', '"postR070APublishedReleaseCount": 83',
    '"postR070AFormalSealedReleaseCount": 59', '"legacyFormalFigureBacklogCount": 24',
    '"nextRelease": "r073f"', "121 unique nodes", "40 phases", "91 note links",
    "verify_manifest_hashes", "public figure copy ledger is incomplete",
    "CERTIFIED_REPORT_COMMIT", "FIGURE_DIRECTORY_COMMIT", "formalArchiveInventory",
  ]) assert.ok(source.includes(token), token);
  for (const token of [
    "fixedPositiveHalfPlaneNoPollution=CLOSED",
    "allModesRightOfBProjectionNormPersistence=CLOSED",
    "topInviscidClusterExists=CLOSED", "topViscousClusterPersistence=CLOSED",
    "topReducedHalfPlaneResolventUniform=CLOSED",
    "frozenTopClusterRelativeDichotomy=CLOSED",
    "fixedFrozenGeneratorVolterraTransfer=CLOSED", "logFastTimeTransfer=CLOSED",
    "superPolynomialCompleteRowNoGo=CLOSED",
    "certifiedSigmaStarIsRightmost=OPEN", "uniformHalfPlaneBoundAtBEqualsZero=OPEN",
    "movingProfileEvolutionDichotomy=OPEN", "fixedWindowExponentialLowerLaw=OPEN",
    "completeOSSquireA2DirectSum=OPEN", "nonlinearNavierStokes=OPEN", "Clay=OPEN",
    "R0.73F", "fixed-window", "graph-domain/Kato transport",
    '<a class="route-map-latest" href="/notes/r0-73e.pdf">阅读最新 R0.73E 研究笔记 →</a>',
  ]) assert.ok(content.includes(token), token);
  assertPublicVoice(content, "R0.73E content source");
  const main = generator.slice(generator.indexOf("def main() -> None:"));
  const calls = ["preflight_release_state()", "validate_inputs()", "publish_figure_assets()", "build_note()", "build_recap()", "update_home()", "update_literature()", "update_manifests()", "update_note_index()"].map((call) => main.indexOf(call));
  assert.ok(calls.every((index) => index >= 0));
  assert.deepEqual(calls, [...calls].sort((a, b) => a - b));
  assert.match(translation, /R073E_RELEASE_ROOT/);
  assert.match(translation, /i18n-en\.js\?v=1\.45/);
  assert.match(translation, /i18n-snapshots\/r073e-missing\.json/);
  assert.match(translation, /"r073e"\s*\+\s*String\(index \+ 1\)/);
});

test("R0.73E manifests advance counters once and bind the archive inventory", async () => {
  const [manifest, site, archive, version] = await Promise.all([
    json("research/release-manifest.json"), json("public/site-version.json"),
    json("research/formal-archive-inventory.json"), text("VERSION"),
  ]);
  assert.deepEqual({
    latest: manifest.latestCompletedRelease, version: manifest.siteVersion,
    notes: manifest.publicHtmlNoteCount, recap: manifest.postR060RecapNodeCount,
    next: manifest.nextRelease, published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  }, { latest: "r073e", version: "1.45", notes: 181, recap: 121, next: "r073f", published: 83, sealed: 59, backlog: 24 });
  assert.deepEqual(site, { schemaVersion: "research-site-version-v1", version: "1.45", latestRelease: "R0.73E", publicHtmlNoteCount: 181, publishedDate: "2026-08-30" });
  assert.equal(version, "1.45\n");
  assert.equal(archive.latestPublishedRelease, "r073e");
  assert.equal(archive.publishedReleaseCount, 83);
  assert.equal(archive.formalSealedReleaseCount, 59);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.equal(archive.publishedReleases.at(-1), "r073e");
  assert.equal(archive.formalSealedReleases.at(-1), "r073e");
  assert.deepEqual(manifest.formalArchiveInventory, {
    path: "research/formal-archive-inventory.json",
    sha256: await sha("research/formal-archive-inventory.json"),
  });
});

test("R0.73E note, cumulative recap, homepage, index, and literature are synchronized", async () => {
  const [note, recap, home, literature, noteIndex] = await Promise.all([
    text("public/notes/r0-73e.html"), text("public/recap-r0-61-r0-73e.html"),
    text("public/research-review.html"), text("public/literature-review.html"),
    text("public/notes/index.html"),
  ]);
  const noteFiles = await readdir(resolve(publicRoot, "notes"));
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 181);
  for (const token of [
    "fixedPositiveHalfPlaneNoPollution=CLOSED", "topReducedHalfPlaneResolventUniform=CLOSED",
    "frozenTopClusterRelativeDichotomy=CLOSED", "logFastTimeTransfer=CLOSED",
    "superPolynomialCompleteRowNoGo=CLOSED", "movingProfileEvolutionDichotomy=OPEN",
    "fixedWindowExponentialLowerLaw=OPEN", "nonlinearNavierStokes=OPEN", "Clay=OPEN",
    "/assets/r073e/" + figureId + ".svg", "/notes/r0-73e.pdf",
    "/recap-r0-61-r0-73e.html", "doi.org/10.1016/j.anihpc.2007.05.004",
    "doi.org/10.1090/S0002-9947-1978-0461206-1",
    "doi.org/10.1143/JPSJ.5.435", "doi.org/10.1142/S0129055X19500144",
    "doi.org/10.1006/jdeq.1999.3668", "doi.org/10.1016/j.na.2008.11.009",
  ]) assert.ok(note.includes(token), token);
  assert.doesNotMatch(note, /moving-profile (?:spectral )?(?:theorem|dichotomy).*CLOSED/i);
  const nodes = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map((match) => match[1]);
  assert.equal(nodes.length, 121);
  assert.equal(new Set(nodes).size, 121);
  assert.equal(nodes.at(-1), "r0-73e");
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 40);
  for (const token of ["R0.61–R0.69W", "R0.70A–R0.71Z", "R0.72A–R0.73B", "R0.73C", "R0.73D", "R0.73E", "83 个版本已经公开", "59 个满足当前完整封存合同", "24 个历史版本", "R0.73F"]) assert.ok(recap.includes(token), token);
  const firstScreen = home.slice(0, home.indexOf('<section class="route-overview" id="route-map"'));
  for (const token of ["LATEST RELEASE · R0.73E", "当前端点 R0.73E", "181 篇研究笔记总索引", "121 节累计回顾", "R0.70A–R0.73E · 83 节已公开", "59 节完整封存"]) assert.ok(firstScreen.includes(token), token);
  assert.ok(firstScreen.includes('<a class="route-map-latest" href="/notes/r0-73e.pdf">阅读最新 R0.73E 研究笔记 →</a>'));
  assert.equal((home.match(/data-release="r073e"/g) ?? []).length, 1);
  const route = home.match(/<nav class="route-note-links" aria-label="R0\.69P–R0\.73E">([\s\S]*?)<\/nav>/)?.[1] ?? "";
  assert.equal((route.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length, 91);
  assert.equal((home.match(/<strong style="color:var\(--gold\)">下一步 R0\.73F：/g) ?? []).length, 1);
  assert.ok(literature.includes('id="r073e-boundary"'));
  assert.ok(literature.includes("开放接口 · R0.73F"));
  assert.ok(literature.includes("Shvydkoy--Friedlander 2008"));
  assert.ok(noteIndex.includes('data-note="r0-73e"'));
  assert.ok(noteIndex.includes("181 篇公开研究笔记"));
  for (const [value, label] of [[note, "note"], [recap, "recap"], [home, "home"], [literature, "literature"], [noteIndex, "index"]]) {
    assert.ok(value.includes('/i18n-en.js?v=1.45'), label);
    assertPublicVoice(value, label);
  }
});

test("R0.73E public figure assets and synchronized PDFs are complete", async () => {
  for (const suffix of ["pdf", "png", "svg"]) assert.equal(await sha(`${figure}/figure.${suffix}`), await sha(`public/assets/r073e/${figureId}.${suffix}`), suffix);
  const note = await inspectPdf("public/notes/r0-73e.pdf");
  const recap = await inspectPdf("public/recap-r0-61-r0-73e.pdf");
  assert.equal(note.header, "%PDF");
  assert.equal(recap.header, "%PDF");
  assert.ok(note.bytes > 25_000 && note.pages >= 2, JSON.stringify(note));
  assert.ok(recap.bytes > 50_000 && recap.pages >= 4, JSON.stringify(recap));
});

test("R0.73E English dictionary covers every live string and remains reproducible", async () => {
  const source = await collectSiteStrings(publicRoot);
  const translations = await json("translations/en.json");
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry.en]));
  assert.equal(byChinese.size, translations.length);
  assert.deepEqual(source.filter((entry) => !byChinese.has(entry.zh)), []);
  for (const entry of translations.filter((row) => /^r073e\d+$/.test(row.id))) {
    assert.equal(containsChinese(entry.en), false, entry.zh);
    assert.equal(/\b(?:we|our|ours|ourselves|us)\b/i.test(entry.en), false, entry.zh);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh), entry.zh);
    assert.deepEqual(entry.en.match(/\b(?:CLOSED|OPEN|FALSE|CONDITIONAL)\b/g) ?? [], entry.zh.match(/\b(?:CLOSED|OPEN|FALSE|CONDITIONAL)\b/g) ?? [], entry.zh);
  }
  const result = await run(process.execPath, ["scripts/add-r073e-translations.mjs", "--check-only"], { cwd: root, maxBuffer: 16 * 1024 * 1024 });
  assert.match(result.stdout, /"missingAfter":0/);
});
