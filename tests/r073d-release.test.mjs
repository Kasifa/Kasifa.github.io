import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { readFile, readdir } from "node:fs/promises";
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
const figure = "figures/r073d/fig-r073d-viscous-cluster-persistence";
const figureId = "fig-r073d-viscous-cluster-persistence";
const run = promisify(execFile);

const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const sha = async (relative) => createHash("sha256")
  .update(await readFile(resolve(root, relative))).digest("hex");

function nodeIndex(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  return recap.slice(start, end);
}

function assertPublicVoice(value, label) {
  for (const phrase of ["我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法"]) {
    assert.equal(value.includes(phrase), false, label + ": " + phrase);
  }
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

test("R0.73D release source pins the v1.44 transaction and exact claim boundary", async () => {
  const [generator, content, translationScript] = await Promise.all([
    text("scripts/generate_r073d_release.py"),
    text("scripts/r073d_release_content.py"),
    text("scripts/add-r073d-translations.mjs"),
  ]);
  const releaseSource = generator + "\n" + content;
  for (const token of [
    "R073C_RELEASE_BASELINE",
    '"siteVersion": "1.43"',
    '"publicHtmlNoteCount": 179',
    '"postR060RecapNodeCount": 119',
    '"postR070APublishedReleaseCount": 81',
    '"postR070AFormalSealedReleaseCount": 57',
    '"legacyFormalFigureBacklogCount": 24',
    '"siteVersion": "1.44"',
    '"publicHtmlNoteCount": 180',
    '"postR060RecapNodeCount": 120',
    '"postR070APublishedReleaseCount": 82',
    '"postR070AFormalSealedReleaseCount": 58',
    '"nextRelease": "r073e"',
    "public figure copy ledger is incomplete",
    "git_commit_for",
    "HOME_LATEST_SPOTLIGHT",
    "HOME_D_CARD",
    "120 unique nodes",
    "39 phases",
    "90 note links",
    "D home mobile claim wrapping",
    "D literature mobile claim wrapping",
    "overflow-wrap: anywhere",
    '<a class="route-map-latest" href="#r073d">跳到首页 R0.73D 卡片 →</a>',
  ]) assert.ok(releaseSource.includes(token), token);
  for (const token of [
    "staticVanishingViscosityPersistence=CLOSED",
    "fixedContourResolventUniform=CLOSED",
    "fixedClusterRieszProjectionNormConvergence=CLOSED",
    "fixedClusterAlgebraicMultiplicityPreserved=CLOSED",
    "fixedClusterEigenvaluesConverge=CLOSED",
    "inviscidRootUnique=OPEN",
    "inviscidEigenvalueSimple=OPEN",
    "explicitContourRadius=OPEN",
    "explicitViscosityThreshold=OPEN",
    "quantitativeEigenvalueRate=OPEN",
    "globalRightHalfPlaneNoPollution=OPEN",
    "uniformComplementaryDichotomy=OPEN",
    "movingProfileUniformContour=OPEN",
    "graphDomainKatoTransport=OPEN",
    "logFastTimeTransfer=OPEN",
    "superPolynomialCompleteRowNoGo=CONDITIONAL",
    "completeOSSquireA2DirectSum=OPEN",
    "nonlinearNavierStokes=OPEN",
    "Clay=OPEN",
    "Shvydkoy",
    "finite diagnostic only",
    "R0.73E",
  ]) assert.ok(content.includes(token), token);
  assertPublicVoice(content, "R0.73D public content source");

  const main = generator.slice(generator.indexOf("def main() -> None:"));
  const calls = [
    "preflight_release_state()", "validate_inputs()", "publish_figure_assets()",
    "build_note()", "build_recap()", "update_home()", "update_literature()",
    "update_manifests()", "update_note_index()",
  ].map((call) => main.indexOf(call));
  assert.ok(calls.every((index) => index >= 0));
  assert.deepEqual(calls, [...calls].sort((left, right) => left - right));
  assert.match(translationScript, /R073D_RELEASE_ROOT/);
  assert.match(translationScript, /i18n-en\.js\?v=1\.44/);
  assert.match(translationScript, /i18n-snapshots\/r073d-missing\.json/);
  assert.match(translationScript, /"r073d"\s*\+\s*String\(index \+ 1\)/);
  assert.match(translationScript, /CLOSED\|OPEN\|FALSE\|CONDITIONAL/);
});

test("R0.73D frozen translation snapshot is complete and claim-safe", async () => {
  const snapshot = await json("scripts/i18n-snapshots/r073d-missing.json");
  assert.equal(snapshot.length, 131);
  assert.equal(snapshot[0].zh, "打开 120 节完整索引");
  assert.equal(snapshot.at(-1).zh,
    "staticVanishingViscosityPersistence、fixedContourResolventUniform、fixedClusterRieszProjectionNormConvergence、fixedClusterAlgebraicMultiplicityPreserved 与 fixedClusterEigenvaluesConverge 为 CLOSED；inviscidRootUnique、inviscidEigenvalueSimple、explicitContourRadius、explicitViscosityThreshold、quantitativeEigenvalueRate、globalRightHalfPlaneNoPollution、uniformComplementaryDichotomy、movingProfileUniformContour、graphDomainKatoTransport、logFastTimeTransfer、completeOSSquireA2DirectSum、nonlinearNavierStokes 与 Clay 为 OPEN；superPolynomialCompleteRowNoGo 为 CONDITIONAL。");
  assert.equal(new Set(snapshot.map((entry) => entry.zh)).size, snapshot.length);
  for (const entry of snapshot) {
    assert.deepEqual(Object.keys(entry), ["zh", "en"]);
    assert.equal(containsChinese(entry.en), false, entry.zh);
    assert.equal(/\b(?:we|our|ours|ourselves|us)\b/i.test(entry.en), false, entry.zh);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh), entry.zh);
    assert.deepEqual(
      entry.en.match(/\b(?:CLOSED|OPEN|FALSE|CONDITIONAL)\b/g) ?? [],
      entry.zh.match(/\b(?:CLOSED|OPEN|FALSE|CONDITIONAL)\b/g) ?? [],
      entry.zh,
    );
  }
});

test("R0.73D manifests advance every public counter exactly once", async (context) => {
  const activeManifest = await json("research/release-manifest.json");
  if (activeManifest.latestCompletedRelease !== "r073d") {
    context.skip("R0.73D current-site transaction is preserved by the R0.73D source and archive tests");
    return;
  }
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
    published: manifest.postR070APublishedReleaseCount,
    sealed: manifest.postR070AFormalSealedReleaseCount,
    backlog: manifest.legacyFormalFigureBacklogCount,
  }, {
    latest: "r073d", version: "1.44", notes: 180, recap: 120,
    next: "r073e", published: 82, sealed: 58, backlog: 24,
  });
  assert.equal(manifest.nextReleaseSourceStage, undefined);
  assert.deepEqual(site, {
    schemaVersion: "research-site-version-v1",
    version: "1.44",
    latestRelease: "R0.73D",
    publicHtmlNoteCount: 180,
    publishedDate: "2026-08-30",
  });
  assert.equal(version, "1.44\n");
  assert.equal(archive.latestPublishedRelease, "r073d");
  assert.equal(archive.publishedReleaseCount, 82);
  assert.equal(archive.formalSealedReleaseCount, 58);
  assert.equal(archive.legacyFormalFigureBacklogCount, 24);
  assert.equal(archive.publishedReleases.at(-1), "r073d");
  assert.equal(archive.formalSealedReleases.at(-1), "r073d");
  assert.equal(archive.publishedReleases.filter((value) => value === "r073d").length, 1);
  assert.equal(archive.formalSealedReleases.filter((value) => value === "r073d").length, 1);
});

test("R0.73D note, cumulative recap, homepage, index, and literature are synchronized", async (context) => {
  const activeManifest = await json("research/release-manifest.json");
  if (activeManifest.latestCompletedRelease !== "r073d") {
    context.skip("R0.73D is no longer the current-site endpoint");
    return;
  }
  const [note, recap, home, literature, noteIndex] = await Promise.all([
    text("public/notes/r0-73d.html"),
    text("public/recap-r0-61-r0-73d.html"),
    text("public/research-review.html"),
    text("public/literature-review.html"),
    text("public/notes/index.html"),
  ]);
  const noteFiles = await readdir(resolve(publicRoot, "notes"));
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 180);
  for (const token of [
    "staticVanishingViscosityPersistence=CLOSED",
    "fixedContourResolventUniform=CLOSED",
    "fixedClusterRieszProjectionNormConvergence=CLOSED",
    "fixedClusterAlgebraicMultiplicityPreserved=CLOSED",
    "fixedClusterEigenvaluesConverge=CLOSED",
    "inviscidRootUnique=OPEN", "inviscidEigenvalueSimple=OPEN",
    "explicitContourRadius=OPEN", "explicitViscosityThreshold=OPEN",
    "quantitativeEigenvalueRate=OPEN", "globalRightHalfPlaneNoPollution=OPEN",
    "uniformComplementaryDichotomy=OPEN", "movingProfileUniformContour=OPEN",
    "graphDomainKatoTransport=OPEN", "logFastTimeTransfer=OPEN",
    "superPolynomialCompleteRowNoGo=CONDITIONAL",
    "completeOSSquireA2DirectSum=OPEN", "nonlinearNavierStokes=OPEN", "Clay=OPEN",
    "d=0", "\\gamma=1/2", "s=+1", "finite diagnostic only",
    "/assets/r073d/" + figureId + ".svg",
    "/notes/r0-73d.pdf", "/recap-r0-61-r0-73d.html",
    "doi.org/10.1016/j.anihpc.2007.05.004",
    "numdam.org/articles/10.1016/j.anihpc.2007.05.004",
    "arxiv.org/abs/math/0509538",
  ]) assert.ok(note.includes(token), token);
  assert.doesNotMatch(note, /root uniqueness (?:is )?proved|rank-one continuum|Clay=(?:CLOSED|TRUE)/i);

  const index = nodeIndex(recap);
  const nodeLinks = [...index.matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(nodeLinks.length, 120);
  assert.equal(new Set(nodeLinks).size, 120);
  assert.equal(nodeLinks.at(-1), "r0-73d");
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 39);
  for (const token of [
    "R0.61–R0.69W", "R0.70A–R0.71Z", "R0.72A–R0.73B", "R0.73C", "R0.73D",
    "R0.70A–R0.73D 的 82 节已公开", "58 节完整封存", "24 节旧档待回补",
    "fixedContourResolventUniform", "graphDomainKatoTransport",
    "superPolynomialCompleteRowNoGo 为 CONDITIONAL", "R0.73E",
  ]) assert.ok(recap.includes(token), token);

  const aboveRoute = home.slice(0, home.indexOf('<section class="route-overview" id="route-map"'));
  for (const token of [
    "LATEST RELEASE · R0.73D", "当前端点 R0.73D", "180 篇研究笔记总索引",
    "120 节累计回顾", "R0.70A–R0.73D · 82 节已公开", "58 节完整封存",
  ]) assert.ok(aboveRoute.includes(token), "first-screen latest token: " + token);
  assert.ok(home.includes("<strong>180</strong>公开研究笔记"));
  assert.ok(home.includes("<strong>R0.73D</strong>最新研究节点"));
  assert.equal((home.match(/data-release="r073d"/g) ?? []).length, 1);
  assert.ok(home.includes('<div class="task-one" id="r069v" data-history="true"'));
  assert.ok(home.includes('<div class="task-one" id="r069w" data-history="true"'));
  assert.ok(home.includes("历史研究笔记 R0.69V"));
  assert.ok(home.includes("历史研究笔记 R0.69W"));
  const route = home.match(/<nav class="route-note-links" aria-label="R0\.69P–R0\.73D">([\s\S]*?)<\/nav>/)?.[1] ?? "";
  assert.equal((route.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length, 90);
  assert.equal((home.match(/<strong style="color:var\(--gold\)">下一步 R0\.73E：/g) ?? []).length, 1);
  assert.ok(home.includes('<a class="route-map-latest" href="#r073d">跳到首页 R0.73D 卡片 →</a>'));
  assert.ok(home.includes(".task-one p, .task-one li { overflow-wrap: anywhere; word-break: break-word; }"));
  assert.ok(literature.includes('id="r073d-boundary"'));
  assert.ok(literature.includes("Shvydkoy--Friedlander 2008"));
  assert.ok(literature.includes("开放接口 · R0.73E"));
  assert.ok(literature.includes(".boundary p { overflow-wrap: anywhere; word-break: break-word; }"));
  assert.ok(noteIndex.includes('data-note="r0-73d"'));
  assert.ok(noteIndex.includes("180 篇公开研究笔记"));
  assert.ok(noteIndex.includes("研究笔记总索引 · v1.44 · 2026-08-30"));
  for (const [value, label] of [[note, "note"], [recap, "recap"], [home, "home"], [literature, "literature"], [noteIndex, "note index"]]) {
    assert.ok(value.includes('/i18n-en.js?v=1.44'), label);
    assertPublicVoice(value, label);
  }
});

test("R0.73D public figure assets and synchronized PDFs are complete", async () => {
  for (const suffix of ["pdf", "png", "svg"]) {
    assert.equal(
      await sha(figure + "/figure." + suffix),
      await sha("public/assets/r073d/" + figureId + "." + suffix),
      suffix,
    );
  }
  const notePdf = await inspectPdf("public/notes/r0-73d.pdf");
  const recapPdf = await inspectPdf("public/recap-r0-61-r0-73d.pdf");
  assert.equal(notePdf.header, "%PDF");
  assert.equal(recapPdf.header, "%PDF");
  assert.ok(notePdf.bytes > 25000 && notePdf.pages >= 2, JSON.stringify(notePdf));
  assert.ok(recapPdf.bytes > 50000 && recapPdf.pages >= 4, JSON.stringify(recapPdf));
});

test("R0.73D English dictionary covers every live string and remains reproducible", async (context) => {
  const activeManifest = await json("research/release-manifest.json");
  if (activeManifest.latestCompletedRelease !== "r073d") {
    context.skip("R0.73D frozen translation snapshot is covered by its dedicated historical test");
    return;
  }
  const source = await collectSiteStrings(publicRoot);
  const translations = await json("translations/en.json");
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry.en]));
  assert.equal(byChinese.size, translations.length);
  assert.deepEqual(source.filter((entry) => !byChinese.has(entry.zh)), []);
  for (const entry of translations.filter((row) => /^r073d\d+$/.test(row.id))) {
    assert.equal(containsChinese(entry.en), false, entry.zh);
    assert.equal(/\b(?:we|our|ours|ourselves|us)\b/i.test(entry.en), false, entry.zh);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh), entry.zh);
    assert.deepEqual(
      entry.en.match(/\b(?:CLOSED|OPEN|FALSE|CONDITIONAL)\b/g) ?? [],
      entry.zh.match(/\b(?:CLOSED|OPEN|FALSE|CONDITIONAL)\b/g) ?? [],
      entry.zh,
    );
  }
  const result = await run(process.execPath, ["scripts/add-r073d-translations.mjs", "--check-only"], {
    cwd: root, maxBuffer: 16 * 1024 * 1024,
  });
  assert.match(result.stdout, /"added":131/);
  assert.match(result.stdout, /"missingAfter":0/);
});
