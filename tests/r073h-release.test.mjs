import assert from "node:assert/strict";
import { execFile } from "node:child_process";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { promisify } from "node:util";
import { containsChinese, extractProtectedTokens } from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const run = promisify(execFile);
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const bytes = (relative) => readFile(resolve(root, relative));
const sha = async (relative) =>
  createHash("sha256").update(await bytes(relative)).digest("hex");
const node = process.execPath;

const commits = {
  analytic: "5104cca02adf8b0bf967b352b6652c7c7006a7ac",
  certificate: "a2414fbf40908381acff0aa6f6ebf088e392a9b8",
  report: "b54d1c830a05e6366b9e95cbb4f730663435bef8",
  renderer: "0e326be588b7318adc8bc4b8651a066fd8876038",
  figure: "60a25759b0e153a6160dd48b246fb48b132c776f",
};
const figure = "figures/r073h/fig-r073h-harmonic-feedback";
const figureId = "fig-r073h-harmonic-feedback";

function assertPublicVoice(value, label) {
  for (const phrase of [
    "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  ]) assert.equal(value.includes(phrase), false, label + ": " + phrase);
}

function recapNodes(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  return [...recap.slice(start, end).matchAll(
    /href="\/notes\/(r0-[^"]+)\.html"/g,
  )].map((match) => match[1]);
}

async function absent(relative) {
  await assert.rejects(
    access(resolve(root, relative)),
    (error) => error?.code === "ENOENT",
    relative,
  );
}

async function verifyFlatLedger(relative) {
  const rows = (await text(relative + "/SHA256SUMS")).trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, row);
    assert.equal(await sha(relative + "/" + match[2]), match[1], match[2]);
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(resolve(root, relative), { withFileTypes: true });
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries.filter((entry) => entry.name !== "SHA256SUMS")
      .map((entry) => entry.name).sort(),
  );
}

test("R0.73H release pins the v1.47-to-v1.48 transaction and A/C/R/E/F chain", async () => {
  const [generator, content, translation, agents] = await Promise.all([
    text("scripts/generate_r073h_release.py"),
    text("scripts/r073h_release_content.py"),
    text("scripts/add-r073h-translations.mjs"),
    text("AGENTS.md"),
  ]);
  const source = generator + "\n" + content;
  for (const token of [
    "R073G_RELEASE_BASELINE",
    '"latestCompletedRelease": "r073g"',
    '"siteVersion": "1.47"',
    '"publicHtmlNoteCount": 183',
    '"postR060RecapNodeCount": 123',
    '"postR070APublishedReleaseCount": 85',
    '"postR070AFormalSealedReleaseCount": 61',
    '"latestCompletedRelease": "r073h"',
    '"siteVersion": "1.48"',
    '"publicHtmlNoteCount": 184',
    '"postR060RecapNodeCount": 124',
    '"postR070APublishedReleaseCount": 86',
    '"postR070AFormalSealedReleaseCount": 62',
    '"legacyFormalFigureBacklogCount": 24',
    '"nextRelease": "r073i"',
    "124 unique nodes", "43 phases", "94 note links",
    'ANALYTIC_SOURCE_COMMIT = "' + commits.analytic + '"',
    'CERTIFICATE_PACKAGE_COMMIT = "' + commits.certificate + '"',
    'CERTIFIED_REPORT_COMMIT = "' + commits.report + '"',
    'FIGURE_RENDERER_COMMIT = "' + commits.renderer + '"',
    'FIGURE_PACKAGE_COMMIT = "' + commits.figure + '"',
    "verify_exact_directory_at_commit", "verify_flat_ledger",
    "commit_transaction(staged)", '"publicationStageIncomplete": True',
    "pdfGenerated", "translationsGenerated",
  ]) assert.ok(source.includes(token), token);
  for (const token of [
    "gainNormalizedFixedDistanceDeparture=CLOSED",
    "gainNormalizedDepartureImpliesPrescribedSeedDeparture=FALSE_AS_INFERENCE",
    "familyDepartureIsSingleBackgroundLyapunovInstability=FALSE_AS_INFERENCE",
    "planarDepartureResolvesClay=FALSE",
    "sharpSelectedGainAction=OPEN",
    "uniformTaylorRadiusAtNaturalEndpoint=OPEN",
    "d=0.01>1/450", "4 个预注册独立哨兵", "1 个独立 holdout",
    "R0.73I", "匹配作用量",
  ]) assert.ok(content.includes(token), token);
  assert.match(content, /uniformTaylorRadiusAtNaturalEndpoint[\s\S]*预设/);
  assertPublicVoice(content, "R0.73H content");
  assert.match(translation, /R073H_RELEASE_ROOT/);
  assert.match(translation, /i18n-en\.js\?v=1\.48/);
  assert.match(translation, /i18n-snapshots\/r073h-missing\.json/);
  assert.match(translation, /--apply/);
  assert.match(translation, /"r073h"\s*\+\s*String\(index \+ 1\)/);
  assert.match(translation, /writeTranslationTransaction/);
  assert.match(translation, /handle\.sync\(\)/);
  assert.doesNotMatch(translation, /Promise\.all\(\[\s*writeFile\(translationPath/);
  assert.match(agents, /https:\/\/kasifa\.github\.io\//);
  assert.doesNotMatch(source, /netlify\.app|vercel\.app|pages\.dev/i);

  const main = generator.slice(generator.indexOf("def main() -> None:"));
  const calls = [
    "preflight_release_state()", "validate_inputs()",
    "stage_figure_assets(staged, figure_manifest)", "build_note()",
    "build_recap()", "update_home()", "update_literature()",
    "build_manifest_outputs()", "build_note_index(",
    "validate_staged(staged)", "commit_transaction(staged)",
  ].map((call) => main.indexOf(call));
  assert.ok(calls.every((index) => index >= 0));
  assert.deepEqual(calls, [...calls].sort((left, right) => left - right));
});

test("R0.73H help and default CLI paths are read-only", async () => {
  const watched = [
    "public/research-review.html", "public/literature-review.html",
    "public/notes/index.html", "public/site-version.json",
    "research/release-manifest.json", "research/formal-archive-inventory.json",
    "translations/en.json", "public/i18n-en.js", "VERSION",
  ];
  const before = new Map(await Promise.all(
    watched.map(async (relative) => [relative, await sha(relative)]),
  ));
  const generatorHelp = await run("python3", ["scripts/generate_r073h_release.py", "--help"], { cwd: root });
  const generatorDefault = await run("python3", ["scripts/generate_r073h_release.py"], { cwd: root });
  const translationHelp = await run(node, ["scripts/add-r073h-translations.mjs", "--help"], { cwd: root });
  const translationDefault = await run(node, ["scripts/add-r073h-translations.mjs"], { cwd: root });
  assert.match(generatorHelp.stdout, /--apply/);
  assert.match(generatorDefault.stdout, /--check-only/);
  assert.match(translationHelp.stdout, /--apply/);
  assert.match(translationDefault.stdout, /--check-only/);
  for (const relative of watched) assert.equal(await sha(relative), before.get(relative), relative);
});

test("R0.73H read-only evidence preflight validates every sealed input", async () => {
  const probe = [
    "import json, sys",
    "sys.path.insert(0, 'scripts')",
    "import generate_r073h_release as r",
    "r.preflight_release_state()",
    "c, f = r.validate_inputs()",
    "print(json.dumps({'certificate': c['allChecksPass'], 'figure': f['status']}))",
  ].join("\n");
  const result = await run("python3", ["-c", probe], {
    cwd: root, maxBuffer: 64 * 1024 * 1024,
  });
  assert.deepEqual(JSON.parse(result.stdout), {
    certificate: true, figure: "formal",
  });
  for (const [older, newer] of [
    [commits.analytic, commits.certificate],
    [commits.certificate, commits.report],
    [commits.report, commits.renderer],
    [commits.renderer, commits.figure],
    [commits.figure, "HEAD"],
  ]) {
    await assert.doesNotReject(
      run("git", ["merge-base", "--is-ancestor", older, newer], { cwd: root }),
      older + " < " + newer,
    );
  }
  await verifyFlatLedger("research/certificates/r073h");
  await verifyFlatLedger(figure);
});

test("R0.73H transaction rollback removes directories created by the failed write", async () => {
  const probe = [
    "import pathlib, sys, tempfile",
    "sys.path.insert(0, 'scripts')",
    "import generate_r073h_release as r",
    "with tempfile.TemporaryDirectory() as temporary:",
    "    root = pathlib.Path(temporary).resolve()",
    "    r.ROOT = root",
    "    existing = root / 'kept' / 'a.txt'",
    "    existing.parent.mkdir()",
    "    existing.write_bytes(b'old')",
    "    created = root / 'new' / 'deep' / 'b.txt'",
    "    real_replace = r.os.replace",
    "    failed = False",
    "    def injected(source, target):",
    "        global failed",
    "        if pathlib.Path(target) == created and not failed:",
    "            failed = True",
    "            raise OSError('injected install failure')",
    "        return real_replace(source, target)",
    "    r.os.replace = injected",
    "    try:",
    "        r.commit_transaction({existing: b'new', created: b'value'})",
    "    except OSError:",
    "        pass",
    "    else:",
    "        raise AssertionError('injection did not fail')",
    "    finally:",
    "        r.os.replace = real_replace",
    "    assert existing.read_bytes() == b'old'",
    "    assert not created.exists()",
    "    assert not (root / 'new').exists()",
    "    assert not list(root.rglob('*.r073h-*'))",
  ].join("\n");
  await assert.doesNotReject(run("python3", ["-c", probe], { cwd: root }));
});

test("R0.73H completion status rejects empty or untranslated English", async () => {
  const probe = [
    "import json, pathlib, sys, tempfile",
    "sys.path.insert(0, 'scripts')",
    "import generate_r073h_release as r",
    "with tempfile.TemporaryDirectory() as temporary:",
    "    root = pathlib.Path(temporary).resolve()",
    "    r.ROOT = root",
    "    r.PUBLIC = root / 'public'",
    "    (root / 'public' / 'notes').mkdir(parents=True)",
    "    (root / 'scripts' / 'i18n-snapshots').mkdir(parents=True)",
    "    (root / 'translations').mkdir()",
    "    (root / 'public' / 'notes' / 'r0-73h.pdf').write_bytes(b'%PDF-test')",
    "    (root / 'public' / 'recap-r0-61-r0-73h.pdf').write_bytes(b'%PDF-test')",
    "    snapshot = [{'zh': '甲', 'en': ''}]",
    "    translated = [{'id': 'r073h001', 'zh': '甲', 'en': ''}]",
    "    (root / 'scripts' / 'i18n-snapshots' / 'r073h-missing.json').write_text(json.dumps(snapshot), encoding='utf-8')",
    "    (root / 'translations' / 'en.json').write_text(json.dumps(translated), encoding='utf-8')",
    "    (root / 'public' / 'i18n-en.js').write_text(json.dumps('甲', ensure_ascii=False) + ': ' + json.dumps(''), encoding='utf-8')",
    "    assert r.publication_stage_incomplete() is True",
    "    snapshot[0]['en'] = translated[0]['en'] = 'Alpha'",
    "    (root / 'scripts' / 'i18n-snapshots' / 'r073h-missing.json').write_text(json.dumps(snapshot), encoding='utf-8')",
    "    (root / 'translations' / 'en.json').write_text(json.dumps(translated), encoding='utf-8')",
    "    (root / 'public' / 'i18n-en.js').write_text(json.dumps('甲', ensure_ascii=False) + ': ' + json.dumps('Alpha'), encoding='utf-8')",
    "    assert r.publication_stage_incomplete() is False",
  ].join("\n");
  await assert.doesNotReject(run("python3", ["-c", probe], { cwd: root }));
});

test("R0.73H source-stage builders produce exact counts without writing public", async (context) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073g") {
    context.skip("final stage: builder transaction already materialized");
    return;
  }
  const watched = [
    "public/research-review.html", "public/literature-review.html",
    "public/notes/index.html", "public/site-version.json",
    "research/release-manifest.json", "research/formal-archive-inventory.json", "VERSION",
  ];
  const before = new Map(await Promise.all(
    watched.map(async (relative) => [relative, await sha(relative)]),
  ));
  const probe = [
    "import json, re, sys",
    "sys.path.insert(0, 'scripts')",
    "import generate_r073h_release as r",
    "note, recap, home, literature = r.build_note(), r.build_recap(), r.update_home(), r.update_literature()",
    "start, end = recap.index('<section id=\"node-index\">'), recap.index('</section>', recap.index('<section id=\"node-index\">'))",
    "nodes = re.findall(r'href=\"/notes/(r0-[^\"]+)\\.html\"', recap[start:end])",
    "route = re.search(r'<nav class=\"route-note-links\" aria-label=\"R0\\.69P–R0\\.73H\">(.*?)</nav>', home, flags=re.S)",
    "routes = re.findall(r'href=\"/notes/r0-[^\"]+\\.html\"', route.group(1))",
    "nav = re.search(r'<nav>(.*?)</nav>', note, flags=re.S)",
    "anchors = re.findall(r'href=\"#([^\"]+)\"', nav.group(1))",
    "print(json.dumps({'anchors': anchors, 'nodes': len(nodes), 'unique': len(set(nodes)), 'phases': recap.count('<article class=\"phase\">'), 'routes': len(routes), 'literatureH': 'id=\"r073h-boundary\"' in literature}))",
  ].join("\n");
  const result = await run("python3", ["-c", probe], {
    cwd: root, maxBuffer: 64 * 1024 * 1024,
  });
  const payload = JSON.parse(result.stdout);
  assert.equal(payload.anchors.length, 18);
  assert.equal(new Set(payload.anchors).size, 18);
  assert.deepEqual({
    nodes: payload.nodes, unique: payload.unique, phases: payload.phases,
    routes: payload.routes, literatureH: payload.literatureH,
  }, { nodes: 124, unique: 124, phases: 43, routes: 94, literatureH: true });
  for (const relative of watched) assert.equal(await sha(relative), before.get(relative));
  for (const relative of [
    "public/notes/r0-73h.html", "public/notes/r0-73h.pdf",
    "public/recap-r0-61-r0-73h.html", "public/recap-r0-61-r0-73h.pdf",
    "public/assets/r073h",
  ]) await absent(relative);
});

test("R0.73H source and final lifecycles preserve exact G or H counters", async () => {
  const [release, site, inventory, version] = await Promise.all([
    json("research/release-manifest.json"), json("public/site-version.json"),
    json("research/formal-archive-inventory.json"), text("VERSION"),
  ]);
  if (release.latestCompletedRelease === "r073g") {
    assert.deepEqual({
      version: release.siteVersion, notes: release.publicHtmlNoteCount,
      recap: release.postR060RecapNodeCount, next: release.nextRelease,
      published: release.postR070APublishedReleaseCount,
      sealed: release.postR070AFormalSealedReleaseCount,
      backlog: release.legacyFormalFigureBacklogCount,
    }, {
      version: "1.47", notes: 183, recap: 123, next: "r073h",
      published: 85, sealed: 61, backlog: 24,
    });
    assert.equal(site.version, "1.47");
    assert.equal(inventory.latestPublishedRelease, "r073g");
    assert.equal(version, "1.47\n");
  } else {
    assert.equal(release.latestCompletedRelease, "r073h");
    assert.deepEqual({
      version: release.siteVersion, notes: release.publicHtmlNoteCount,
      recap: release.postR060RecapNodeCount, next: release.nextRelease,
      published: release.postR070APublishedReleaseCount,
      sealed: release.postR070AFormalSealedReleaseCount,
      backlog: release.legacyFormalFigureBacklogCount,
    }, {
      version: "1.48", notes: 184, recap: 124, next: "r073i",
      published: 86, sealed: 62, backlog: 24,
    });
    assert.equal(site.version, "1.48");
    assert.equal(inventory.latestPublishedRelease, "r073h");
    assert.equal(version, "1.48\n");
  }
});

test("R0.73H final site keeps figure byte identity and post-R0.60 coverage", async (context) => {
  const release = await json("research/release-manifest.json");
  if (release.latestCompletedRelease !== "r073h") {
    context.skip("source stage: public transaction not materialized");
    return;
  }
  const [note, recap, home, literature, index] = await Promise.all([
    text("public/notes/r0-73h.html"), text("public/recap-r0-61-r0-73h.html"),
    text("public/research-review.html"), text("public/literature-review.html"),
    text("public/notes/index.html"),
  ]);
  const nodes = recapNodes(recap);
  assert.equal(nodes.length, 124);
  assert.equal(new Set(nodes).size, 124);
  assert.equal(recap.match(/<article class="phase">/g)?.length, 43);
  assert.ok(home.includes("展开 94 篇公开笔记"));
  assert.ok(literature.includes('id="r073h-boundary"'));
  assert.ok(index.includes('data-note="r0-73h"'));
  for (const value of [note, recap, home, literature, index]) {
    assert.ok(value.includes("/i18n-en.js?v=1.48"));
    assertPublicVoice(value, "final HTML");
  }
  for (const suffix of ["pdf", "svg", "png"]) {
    assert.deepEqual(
      await bytes("public/assets/r073h/" + figureId + "." + suffix),
      await bytes(figure + "/figure." + suffix),
      suffix,
    );
  }
  for (const relative of [
    "public/notes/r0-73h.pdf",
    "public/recap-r0-61-r0-73h.pdf",
  ]) {
    assert.equal((await bytes(relative)).subarray(0, 4).toString(), "%PDF", relative);
  }
});

test("R0.73H translation source is deterministic before or after publication", async () => {
  const snapshot = await json("scripts/i18n-snapshots/r073h-missing.json");
  assert.ok(Array.isArray(snapshot) && snapshot.length > 0);
  assert.equal(new Set(snapshot.map((entry) => entry.zh)).size, snapshot.length);
  assert.equal(
    snapshot.find((entry) => entry.zh === "R0.73I 建立选定增益的匹配作用量")?.en,
    "R0.73I: Establish matching actions for the selected gain",
  );
  const nextGate = snapshot.find((entry) => entry.zh.startsWith(
    "R0.73H 已对实际增益归一化的趋零初态闭合平面固定距离偏离。",
  ))?.en ?? "";
  assert.match(nextGate, /The next gate is to establish matching actions/);
  assert.doesNotMatch(nextGate, /The next gate establishes/);
  const boundaryTokens = (value) =>
    value.match(/\b(?:FALSE_AS_INFERENCE|CONDITIONAL|CLOSED|OPEN|FALSE)\b/g) ?? [];
  const claimKeyTokens = (value) =>
    value.match(/\b[A-Za-z][A-Za-z0-9]*(?==(?:FALSE_AS_INFERENCE|CLOSED|OPEN|FALSE)\b)/g) ?? [];
  const accountingTokens = (value) =>
    [...value.matchAll(
      /R0\.\d+[A-Z]?|v\d+(?:\.\d+)+[A-Z]?|(?<![\p{L}\p{N}_])\d+(?:\.\d+)?(?![\p{L}\p{N}_])/gu,
    )].map((match) => match[0]);
  for (const [index, entry] of snapshot.entries()) {
    assert.equal(typeof entry.zh, "string", `snapshot zh row ${index + 1}`);
    assert.ok(typeof entry.en === "string" && entry.en.trim(), `snapshot en row ${index + 1}`);
    assert.equal(containsChinese(entry.en), false, `snapshot Chinese row ${index + 1}`);
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh));
    assert.deepEqual(accountingTokens(entry.en), accountingTokens(entry.zh));
    assert.deepEqual(boundaryTokens(entry.en), boundaryTokens(entry.zh));
    assert.deepEqual(claimKeyTokens(entry.en), claimKeyTokens(entry.zh));
  }
  const release = await json("research/release-manifest.json");
  if (release.latestCompletedRelease === "r073h") {
    const result = await run(node, ["scripts/add-r073h-translations.mjs", "--check-only"], {
      cwd: root, maxBuffer: 64 * 1024 * 1024,
    });
    assert.match(result.stdout, /"missingAfter":0/);
  }
});

test("R0.73H remains a GitHub Pages-only publication contract", async () => {
  for (const relative of ["netlify.toml", "vercel.json", "wrangler.toml"]) {
    await absent(relative);
  }
  const pages = await text(".github/workflows/pages.yml");
  assert.match(pages, /actions\/deploy-pages@/);
});
