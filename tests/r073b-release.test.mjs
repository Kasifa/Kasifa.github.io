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
const certificate = "research/certificates/r073b";
const figure = "figures/r073b/fig-r073b-bloch-kinetic-transient";
const figureId = "fig-r073b-bloch-kinetic-transient";
const run = promisify(execFile);

async function text(relative) {
  return readFile(resolve(root, relative), "utf8");
}

async function json(relative) {
  return JSON.parse(await text(relative));
}

async function absent(relative) {
  await assert.rejects(access(resolve(root, relative)),
    (error) => error && error.code === "ENOENT", relative);
}

async function sha(relative) {
  return createHash("sha256").update(await readFile(resolve(root, relative))).digest("hex");
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
  return {
    bytes: bytes.length,
    pages: [...latin.matchAll(/\/Type\s*\/Page\b/g)].length,
  };
}

test("R0.73B release source pins counters, final boundaries, and fail-closed write order", async () => {
  const [generator, translationScript] = await Promise.all([
    text("scripts/generate_r073b_release.py"),
    text("scripts/add-r073b-translations.mjs"),
  ]);
  for (const token of [
    "R073A_RELEASE_BASELINE", "SOURCE_STAGE_CONTRACT",
    '"independentAudit": "research/r073b_independent_analytic_audit.md"',
    '"independentAnalyticAudit": "research/r073b_independent_analytic_audit.md"',
    '"independentProducer": "research/certificates/r073b/independent_recompute.py"',
    "exactBlochNearCarrierCancellation=CLOSED",
    "completePhysicalKineticFiniteTransient=CLOSED",
    "completeOSSquireKineticFiniteTransient=CLOSED",
    "blochUniformPhysicalVelocityDirectSumAtViscousRates=CLOSED",
    "lambdaIndependentKineticPrefactor=FALSE",
    "fixedCUniformLowGapKineticPropagator=FALSE",
    "allRowPrefactorOneKineticContraction=FALSE",
    "polynomiallySharpLambdaKineticPrefactor=OPEN",
    "completeOSSquireA2DirectSum=OPEN",
    "transportedAdjointPressureA2Modulation=OPEN",
    "nonlinearNavierStokes=OPEN", "Clay=OPEN",
    "半开 Bloch cell", "selected carrier", "orthogonal direct integral",
    "\\(F_q=0\\)", "\\(\\mu>0\\)", "\\(0<g\\le1\\)",
    "0.188106027072", "280 propagators", "1960 primary norm rows", "245 targeted rows",
    '"siteVersion": "1.41"', '"notes": 178', '"recapNodes": 118',
    '"published": 80', '"formalSealed": 56', '"legacyBacklog": 24',
    '"phases": 37', '"routeNotes": 88', '"next": "R0.73C"',
    '(ROOT / "VERSION").write_text("1.41\\n"',
  ]) assert.ok(generator.includes(token), token);
  for (const boundary of [
    'R0.72T</a><span class="node-state kind-conditional">条件</span>',
    "R0.72S 在 fixed-first-harmonic \\\\(1{:}2{:}3\\\\) family 内证明 incidence preimages",
    "这不是四维 caustic image 的全局分类",
    "fixed \\\\(\\\\Lambda\\\\) raw-\\\\(q\\\\) limit 与 kinetic/Squire/Bloch/nonlinear/Clay 保持 OPEN",
    "该双谐波 heat path 上 complete linearized row 的 viscous-rate finite transient 已闭合；A2 与 nonlinear 门仍未闭合",
    "没有 Galerkin tail enclosure，也不证明无限维收敛或 nonlinear convolution",
    "completeOSSquireA2DirectSum、transportedAdjointPressureA2Modulation、nonlinearNavierStokes 与 Clay 为 OPEN",
  ]) assert.ok(generator.includes(boundary), boundary);
  const article = generator.match(/NOTE_ARTICLE = r'''([\s\S]*?)'''/)?.[1] ?? "";
  assert.ok(article.length > 5000);
  for (const stale of [
    "fig-r073a-hidden-mean-transient-spectral",
    "R0.73A scoped physical row",
  ]) assert.equal(article.includes(stale), false, stale);
  const main = generator.slice(generator.indexOf("def main() -> None:"));
  const calls = [
    "preflight_release_state()", "validate_inputs()", "build_note()", "build_recap()",
    "update_home()", "update_literature()", "update_manifests()",
  ].map((call) => main.indexOf(call));
  assert.ok(calls.every((index) => index >= 0));
  assert.deepEqual(calls, [...calls].sort((left, right) => left - right));
  assert.ok(generator.indexOf("validate_inputs()") < generator.indexOf("build_note()"));
  assert.match(generator, /validate_certificate\.py"\), "--require-formal"/);
  assert.match(generator, /subprocess\.run\(\[sys\.executable, str\(figure \/ "validate\.py"\)\]/);
  assert.doesNotMatch(generator, /(?:weasyprint|wkhtmltopdf|playwright|chromium).*pdf/i);
  assert.match(translationScript, /R073B_RELEASE_ROOT/);
  assert.match(translationScript, /i18n-en\.js\?v=1\.42/);
  assert.match(translationScript, /i18n-snapshots\/r073b-missing\.json/);
  assert.match(translationScript, /"r073b"\s*\+\s*String\(index \+ 1\)/);
  assert.match(translationScript, /\bwe\|our\|ours\|ourselves\|us\b/);
  assertPublicVoice(article, "R0.73B article source");
});

test("R0.73B source and publication lifecycles never mix public counters", async () => {
  const [manifest, site, archive] = await Promise.all([
    json("research/release-manifest.json"),
    json("public/site-version.json"),
    json("research/formal-archive-inventory.json"),
  ]);
  if (manifest.latestCompletedRelease === "r073a") {
    assert.deepEqual({
      version: manifest.siteVersion, notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount, next: manifest.nextRelease,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, {
      version: "1.40", notes: 177, recap: 117, next: "r073b",
      published: 79, sealed: 55, backlog: 24,
    });
    assert.deepEqual(site, {
      schemaVersion: "research-site-version-v1", version: "1.40",
      latestRelease: "R0.73A", publicHtmlNoteCount: 177,
      publishedDate: "2026-08-29",
    });
    assert.deepEqual({
      latest: archive.latestPublishedRelease, published: archive.publishedReleaseCount,
      sealed: archive.formalSealedReleaseCount, backlog: archive.legacyFormalFigureBacklogCount,
    }, { latest: "r073a", published: 79, sealed: 55, backlog: 24 });
    for (const relative of [
      "public/notes/r0-73b.html", "public/notes/r0-73b.pdf",
      "public/recap-r0-61-r0-73b.html", "public/recap-r0-61-r0-73b.pdf",
    ]) await absent(relative);
  } else {
    assert.deepEqual({
      latest: manifest.latestCompletedRelease, version: manifest.siteVersion,
      notes: manifest.publicHtmlNoteCount, recap: manifest.postR060RecapNodeCount,
      next: manifest.nextRelease, published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, {
      latest: "r073b", version: "1.42", notes: 178, recap: 118,
      next: "r073c", published: 80, sealed: 56, backlog: 24,
    });
    assert.equal(manifest.nextReleaseSourceStage, undefined);
    assert.deepEqual(site, {
      schemaVersion: "research-site-version-v1", version: "1.42",
      latestRelease: "R0.73B", publicHtmlNoteCount: 178,
      publishedDate: "2026-08-30",
    });
    assert.deepEqual({
      latest: archive.latestPublishedRelease, published: archive.publishedReleaseCount,
      sealed: archive.formalSealedReleaseCount, backlog: archive.legacyFormalFigureBacklogCount,
    }, { latest: "r073b", published: 80, sealed: 56, backlog: 24 });
    assert.equal(archive.publishedReleases.at(-1), "r073b");
    assert.equal(archive.formalSealedReleases.at(-1), "r073b");
  }
});

test("R0.73B final public pages are synchronized, complete, and preserve a unique next gate", async (context) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073b") {
    context.skip("source stage: public mutation is correctly absent");
    return;
  }
  const [note, recap, home, literature, version] = await Promise.all([
    text("public/notes/r0-73b.html"),
    text("public/recap-r0-61-r0-73b.html"),
    text("public/research-review.html"),
    text("public/literature-review.html"),
    json("public/site-version.json"),
  ]);
  assert.equal((await readdir(resolve(publicRoot, "notes")))
    .filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 178);
  assert.deepEqual(version, {
    schemaVersion: "research-site-version-v1", version: "1.42",
    latestRelease: "R0.73B", publicHtmlNoteCount: 178,
    publishedDate: "2026-08-30",
  });
  for (const token of [
    "exactBlochNearCarrierCancellation=CLOSED",
    "completePhysicalKineticFiniteTransient=CLOSED",
    "completeOSSquireKineticFiniteTransient=CLOSED",
    "fixedCUniformLowGapKineticPropagator=FALSE",
    "polynomiallySharpLambdaKineticPrefactor=OPEN",
    "transportedAdjointPressureA2Modulation=OPEN",
    "nonlinearNavierStokes=OPEN", "Clay=OPEN",
    "/assets/r073b/" + figureId + ".svg",
    "/notes/r0-73b.pdf", "/recap-r0-61-r0-73b.html",
  ]) assert.ok(note.includes(token), token);
  const index = nodeIndex(recap);
  const nodeLinks = [...index.matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(nodeLinks.length, 118);
  assert.equal(new Set(nodeLinks).size, 118);
  assert.equal(nodeLinks.at(-1), "r0-73b");
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 37);
  assert.equal(recap.includes("kind-nogo"), false);
  assert.ok(index.includes('<a href="/notes/r0-72t.html">R0.72T</a><span class="node-state kind-conditional">条件</span>'));
  assert.ok(recap.includes("R0.72S 在 fixed-first-harmonic \\(1{:}2{:}3\\) family 内证明 incidence preimages"));
  assert.ok(recap.includes("这不是四维 caustic image 的全局分类"));
  assert.ok(recap.includes("fixed \\(\\Lambda\\) raw-\\(q\\) limit"));
  assert.ok(recap.includes("该双谐波 heat path 上 complete linearized row 的 viscous-rate finite transient 已闭合"));
  assert.ok(recap.includes("没有 Galerkin tail enclosure，也不证明无限维收敛或 nonlinear convolution"));
  assert.ok(recap.includes("completeOSSquireA2DirectSum、transportedAdjointPressureA2Modulation、nonlinearNavierStokes 与 Clay 为 OPEN"));
  assert.equal((recap.match(/transportedAdjointPressureA2Modulation/g) ?? []).length, 2);
  assert.ok(recap.includes("R0.70A–R0.73B 的 80 节已公开"));
  assert.ok(recap.includes("56 节完整封存"));
  assert.equal((home.match(/data-release="r073b"/g) ?? []).length, 1);
  assert.ok(home.includes("<strong>2026-08-30</strong>最近修订"));
  assert.equal(home.includes("<strong>2026-08-29</strong>最近修订"), false);
  const route = home.match(/<nav class="route-note-links" aria-label="R0\.69P–R0\.73B">([\s\S]*?)<\/nav>/)?.[1] ?? "";
  assert.equal((route.match(/href="\/notes\/r0-[^"]+\.html"/g) ?? []).length, 88);
  assert.equal((home.match(/<strong style="color:var\(--gold\)">下一步 R0\.73C：/g) ?? []).length, 1);
  assert.equal(home.includes('<strong style="color:var(--gold)">下一步 R0.73B：'), false);
  assert.ok(literature.includes('id="r073b-boundary"'));
  assert.ok(literature.includes("开放接口 · R0.73C"));
  for (const [value, label] of [[note, "note"], [recap, "recap"], [home, "home"], [literature, "literature"]]) {
    assert.ok(value.includes('/i18n-en.js?v=1.42'), label);
    assertPublicVoice(value, label);
  }
});

test("R0.73B formal archives and public figure assets are byte-identical", async (context) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073b") {
    context.skip("source stage: formal publication artifacts are not yet complete");
    return;
  }
  await verifyFlatHashLedger(certificate);
  await verifyFlatHashLedger(figure);
  for (const suffix of ["pdf", "png", "svg"]) {
    assert.equal(
      await sha(figure + "/figure." + suffix),
      await sha("public/assets/r073b/" + figureId + "." + suffix),
      suffix,
    );
  }
  const notePdf = await inspectPdf("public/notes/r0-73b.pdf");
  const recapPdf = await inspectPdf("public/recap-r0-61-r0-73b.pdf");
  assert.ok(notePdf.bytes > 25000 && notePdf.pages >= 2, JSON.stringify(notePdf));
  assert.ok(recapPdf.bytes > 50000 && recapPdf.pages >= 4, JSON.stringify(recapPdf));
});

test("R0.73B final English dictionary exactly covers live strings without boundary drift", async (context) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073b") {
    context.skip("source stage: R0.73B public strings do not exist yet");
    return;
  }
  const source = await collectSiteStrings(publicRoot);
  const translations = await json("translations/en.json");
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry.en]));
  assert.equal(byChinese.size, translations.length);
  const missing = source.filter((entry) => !byChinese.has(entry.zh));
  assert.deepEqual(missing, []);
  for (const entry of translations.filter((row) => /^r073b\d+$/.test(row.id))) {
    assert.equal(containsChinese(entry.en), false, entry.zh);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh), entry.zh);
    assert.deepEqual(
      entry.en.match(/\b(?:CLOSED|OPEN|FALSE)\b/g) ?? [],
      entry.zh.match(/\b(?:CLOSED|OPEN|FALSE)\b/g) ?? [],
      entry.zh,
    );
  }
  const result = await run(process.execPath, ["scripts/add-r073b-translations.mjs", "--check-only"], {
    cwd: root, maxBuffer: 8 * 1024 * 1024,
  });
  assert.match(result.stdout, /"missingAfter":0/);
});
