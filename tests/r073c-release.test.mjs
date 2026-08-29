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
const certificate = "research/certificates/r073c";
const figure = "figures/r073c/fig-r073c-certified-rayleigh-instability";
const figureId = "fig-r073c-certified-rayleigh-instability";
const run = promisify(execFile);

const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const sha = async (relative) => createHash("sha256").update(await readFile(resolve(root, relative))).digest("hex");

async function absent(relative) {
  await assert.rejects(access(resolve(root, relative)),
    (error) => error && error.code === "ENOENT", relative);
}

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

async function verifyFlatHashLedger(relative) {
  const directory = resolve(root, relative);
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8")).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, "malformed SHA256SUMS row: " + row);
    assert.equal(await sha(relative + "/" + match[2]), match[1], match[2]);
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries.filter((entry) => entry.isFile() && entry.name !== "SHA256SUMS")
      .map((entry) => entry.name).sort(),
  );
}

async function inspectPdf(relative) {
  const bytes = await readFile(resolve(root, relative));
  const latin = bytes.toString("latin1");
  return { bytes: bytes.length, pages: [...latin.matchAll(/\/Type\s*\/Page\b/g)].length };
}

test("R0.73C release source pins v1.43 counters, boundaries, visible latest state, and write order", async () => {
  const [generator, translationScript] = await Promise.all([
    text("scripts/generate_r073c_release.py"),
    text("scripts/add-r073c-translations.mjs"),
  ]);
  for (const token of [
    "R073B_RELEASE_BASELINE", "SOURCE_STAGE_CONTRACT",
    '"independentAudit": "research/r073c_independent_analytic_audit.md"',
    '"independentProducer": "research/certificates/r073c/independent_recompute.py"',
    "exactCubicNeutralSpectrum=CLOSED",
    "infiniteDimensionalFrozenRayleighInstability=CLOSED",
    "frozenInstabilityFastTimeTransfer=OPEN",
    "superPolynomialCompleteRowNoGo=CONDITIONAL",
    "sharpLargeLambdaGrowthLaw=OPEN",
    "completeOSSquireA2DirectSum=OPEN",
    "nonlinearNavierStokes=OPEN", "Clay=OPEN",
    "周期单值矩阵", "Pöschl--Teller", "Decimal", "finite diagnostic",
    '"siteVersion": "1.43"', '"notes": 179', '"recapNodes": 119',
    '"published": 81', '"formalSealed": 57', '"legacyBacklog": 24',
    '"phases": 38', '"routeNotes": 89', '"next": "R0.73D"',
    '(ROOT / "VERSION").write_text("1.43\\n"',
    "HOME_LATEST_SPOTLIGHT", "179 篇研究笔记总索引", "119 节累计回顾",
    'data-history="true"', "历史研究笔记 R0.69V", "历史研究笔记 R0.69W",
  ]) assert.ok(generator.includes(token), token);
  const article = generator.match(/NOTE_ARTICLE = r'''([\s\S]*?)'''/)?.[1] ?? "";
  assert.ok(article.length > 5000);
  assertPublicVoice(article, "R0.73C article source");
  const main = generator.slice(generator.indexOf("def main() -> None:"));
  const calls = [
    "preflight_release_state()", "validate_inputs()", "publish_figure_assets()",
    "build_note()", "build_recap()", "update_home()", "update_literature()",
    "update_manifests()", "update_note_index()",
  ].map((call) => main.indexOf(call));
  assert.ok(calls.every((index) => index >= 0));
  assert.deepEqual(calls, [...calls].sort((left, right) => left - right));
  assert.ok(generator.indexOf("validate_inputs()") < generator.indexOf("publish_figure_assets()"));
  assert.match(generator, /validate_certificate\.py"\), "--require-formal"/);
  assert.match(generator, /subprocess\.run\(\[sys\.executable, str\(figure \/ "validate\.py"\)\]/);
  assert.match(translationScript, /R073C_RELEASE_ROOT/);
  assert.match(translationScript, /i18n-en\.js\?v=1\.43/);
  assert.match(translationScript, /i18n-snapshots\/r073c-missing\.json/);
  assert.match(translationScript, /"r073c"\s*\+\s*String\(index \+ 1\)/);
  assert.match(translationScript, /CLOSED\|OPEN\|FALSE\|CONDITIONAL/);
});

test("R0.73C frozen translation snapshot is complete and claim-safe before publication", async () => {
  const snapshot = await json("scripts/i18n-snapshots/r073c-missing.json");
  assert.equal(snapshot.length, 132);
  assert.equal(snapshot[0].zh, "打开 119 节完整索引");
  assert.equal(snapshot.at(-1).zh, "R0.73C：无穷维冻结 Rayleigh 不稳定已闭合");
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

test("R0.73C source and publication stages do not advance public counters early", async () => {
  const [manifest, site, archive, version] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    json("research/formal-archive-inventory.json"),
    text("VERSION"),
  ]);
  if (manifest.latestCompletedRelease === "r073b") {
    assert.deepEqual({
      version: manifest.siteVersion, notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount, next: manifest.nextRelease,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, {
      version: "1.42", notes: 178, recap: 118, next: "r073c",
      published: 80, sealed: 56, backlog: 24,
    });
    assert.deepEqual(site, {
      schemaVersion: "research-site-version-v1", version: "1.42",
      latestRelease: "R0.73B", publicHtmlNoteCount: 178,
      publishedDate: "2026-08-30",
    });
    assert.deepEqual({
      latest: archive.latestPublishedRelease, published: archive.publishedReleaseCount,
      sealed: archive.formalSealedReleaseCount, backlog: archive.legacyFormalFigureBacklogCount,
    }, { latest: "r073b", published: 80, sealed: 56, backlog: 24 });
    assert.ok(["1.41\n", "1.42\n"].includes(version), "known pre-R0.73C root VERSION drift only");
    for (const relative of [
      "public/notes/r0-73c.html", "public/notes/r0-73c.pdf",
      "public/recap-r0-61-r0-73c.html", "public/recap-r0-61-r0-73c.pdf",
    ]) await absent(relative);
  } else {
    assert.deepEqual({
      latest: manifest.latestCompletedRelease, version: manifest.siteVersion,
      notes: manifest.publicHtmlNoteCount, recap: manifest.postR060RecapNodeCount,
      next: manifest.nextRelease, published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, {
      latest: "r073c", version: "1.43", notes: 179, recap: 119,
      next: "r073d", published: 81, sealed: 57, backlog: 24,
    });
    assert.equal(manifest.nextReleaseSourceStage, undefined);
    assert.deepEqual(site, {
      schemaVersion: "research-site-version-v1", version: "1.43",
      latestRelease: "R0.73C", publicHtmlNoteCount: 179,
      publishedDate: "2026-08-30",
    });
    assert.equal(version, "1.43\n");
    assert.equal(version.trim(), manifest.siteVersion);
    assert.equal(version.trim(), site.version);
    assert.deepEqual({
      latest: archive.latestPublishedRelease, published: archive.publishedReleaseCount,
      sealed: archive.formalSealedReleaseCount, backlog: archive.legacyFormalFigureBacklogCount,
    }, { latest: "r073c", published: 81, sealed: 57, backlog: 24 });
    assert.equal(archive.publishedReleases.at(-1), "r073c");
    assert.equal(archive.formalSealedReleases.at(-1), "r073c");
  }
});

test("R0.73C final pages synchronize the homepage first screen, route, recap, index, and literature", async (context) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073c") {
    context.skip("source stage: R0.73C public mutation is correctly absent");
    return;
  }
  const [note, recap, home, literature, noteIndex, site] = await Promise.all([
    text("public/notes/r0-73c.html"),
    text("public/recap-r0-61-r0-73c.html"),
    text("public/research-review.html"),
    text("public/literature-review.html"),
    text("public/notes/index.html"),
    json("public/site-version.json"),
  ]);
  assert.equal((await readdir(resolve(publicRoot, "notes")))
    .filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 179);
  assert.equal(site.latestRelease, "R0.73C");
  for (const token of [
    "exactCubicNeutralSpectrum=CLOSED",
    "infiniteDimensionalFrozenRayleighInstability=CLOSED",
    "frozenInstabilityFastTimeTransfer=OPEN",
    "superPolynomialCompleteRowNoGo=CONDITIONAL",
    "sharpLargeLambdaGrowthLaw=OPEN", "completeOSSquireA2DirectSum=OPEN",
    "nonlinearNavierStokes=OPEN", "Clay=OPEN",
    "/assets/r073c/" + figureId + ".svg",
    "/notes/r0-73c.pdf", "/recap-r0-61-r0-73c.html",
  ]) assert.ok(note.includes(token), token);
  const index = nodeIndex(recap);
  const nodeLinks = [...index.matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)].map((match) => match[1]);
  assert.equal(nodeLinks.length, 119);
  assert.equal(new Set(nodeLinks).size, 119);
  assert.equal(nodeLinks.at(-1), "r0-73c");
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 38);
  assert.ok(recap.includes("R0.70A–R0.73C 的 81 节已公开"));
  assert.ok(recap.includes("57 节完整封存"));
  assert.ok(recap.includes("superPolynomialCompleteRowNoGo 为 CONDITIONAL"));

  const aboveRoute = home.slice(0, home.indexOf('<section class="route-overview" id="route-map"'));
  for (const token of [
    "LATEST RELEASE · R0.73C", "当前端点 R0.73C", "179 篇研究笔记总索引",
    "119 节累计回顾", "R0.70A–R0.73C · 81 节已公开", "57 节完整封存",
  ]) assert.ok(aboveRoute.includes(token), "first-screen latest token: " + token);
  assert.ok(home.includes("<strong>179</strong>公开研究笔记"));
  assert.ok(home.includes("<strong>R0.73C</strong>最新研究节点"));
  assert.equal((home.match(/data-release="r073c"/g) ?? []).length, 1);
  assert.ok(home.includes('<div class="task-one" id="r069v" data-history="true"'));
  assert.ok(home.includes('<div class="task-one" id="r069w" data-history="true"'));
  assert.ok(home.includes("历史研究笔记 R0.69V"));
  assert.ok(home.includes("历史研究笔记 R0.69W"));
  const route = home.match(/<nav class="route-note-links" aria-label="R0\.69P–R0\.73C">([\s\S]*?)<\/nav>/)?.[1] ?? "";
  assert.equal((route.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length, 89);
  assert.equal((home.match(/<strong style="color:var\(--gold\)">下一步 R0\.73D：/g) ?? []).length, 1);
  assert.equal(home.includes('<strong style="color:var(--gold)">下一步 R0.73C：'), false);
  assert.ok(literature.includes('id="r073c-boundary"'));
  assert.ok(literature.includes("开放接口 · R0.73D"));
  assert.ok(noteIndex.includes('data-note="r0-73c"'));
  assert.ok(noteIndex.includes("179 篇公开研究笔记"));
  assert.ok(noteIndex.includes("研究笔记总索引 · v1.43 · 2026-08-30"));
  for (const [value, label] of [[note, "note"], [recap, "recap"], [home, "home"], [literature, "literature"], [noteIndex, "note index"]]) {
    assert.ok(value.includes('/i18n-en.js?v=1.43'), label);
    assertPublicVoice(value, label);
  }
});

test("R0.73C formal archives, public figure assets, and synchronized PDFs are complete", async (context) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073c") {
    context.skip("source stage: formal publication artifacts are not yet complete");
    return;
  }
  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  for (const suffix of ["pdf", "png", "svg"]) {
    assert.equal(await sha(figure + "/figure." + suffix), await sha("public/assets/r073c/" + figureId + "." + suffix), suffix);
  }
  const notePdf = await inspectPdf("public/notes/r0-73c.pdf");
  const recapPdf = await inspectPdf("public/recap-r0-61-r0-73c.pdf");
  assert.ok(notePdf.bytes > 25000 && notePdf.pages >= 2, JSON.stringify(notePdf));
  assert.ok(recapPdf.bytes > 50000 && recapPdf.pages >= 4, JSON.stringify(recapPdf));
});

test("R0.73C English dictionary covers live strings and preserves claim-state tokens", async (context) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073c") {
    context.skip("source stage: R0.73C public strings do not exist yet");
    return;
  }
  const source = await collectSiteStrings(publicRoot);
  const translations = await json("translations/en.json");
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry.en]));
  assert.equal(byChinese.size, translations.length);
  assert.deepEqual(source.filter((entry) => !byChinese.has(entry.zh)), []);
  for (const entry of translations.filter((row) => /^r073c\d+$/.test(row.id))) {
    assert.equal(containsChinese(entry.en), false, entry.zh);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh), entry.zh);
    assert.deepEqual(
      entry.en.match(/\b(?:CLOSED|OPEN|FALSE|CONDITIONAL)\b/g) ?? [],
      entry.zh.match(/\b(?:CLOSED|OPEN|FALSE|CONDITIONAL)\b/g) ?? [],
      entry.zh,
    );
  }
  const result = await run(process.execPath, ["scripts/add-r073c-translations.mjs", "--check-only"], {
    cwd: root, maxBuffer: 8 * 1024 * 1024,
  });
  assert.match(result.stdout, /"missingAfter":0/);
});
