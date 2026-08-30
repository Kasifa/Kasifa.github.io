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
const figure = "figures/r073g/fig-r073g-nonlinear-row-leakage";
const figureId = "fig-r073g-nonlinear-row-leakage";
const sourceCommit = "21c11ba3eef7f2b5dc3f107957e0744a0471745d";
const experimentCommit = "0679192b65a294bb211c96decc47bb046ab60b93";
const figureCommit = "0d311d22a62cfbc9253e95580de10d33898ecddc";
const certificateCommit = "589e366ccec6a316b25594542a7eb8cb879156fd";
const sealCommit = "339c9c27207571cfbade35c3288aae6a70c4193d";
const sourcePaths = [
  "research/r073g_problem_freeze.md",
  "research/r073g_nonlinear_shadowing_proof.md",
  "research/r073g_operator_derivation.md",
  "research/r073g_adversarial_audit.md",
  "research/r073g_independent_analytic_audit.md",
  "research/r073g_report-source.md",
  "research/r073g_gap_matrix.md",
  "research/r073g_literature_audit.md",
];
const run = promisify(execFile);
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const bytes = (relative) => readFile(resolve(root, relative));
const sha = async (relative) =>
  createHash("sha256").update(await bytes(relative)).digest("hex");

function assertPublicVoice(value, label) {
  for (const phrase of [
    "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  ]) assert.equal(value.includes(phrase), false, `${label}: ${phrase}`);
}

function nodeIndex(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start);
  return recap.slice(start, end);
}

function expectedPostR070A() {
  const result = [];
  for (const major of [70, 71, 72]) {
    for (let code = 97; code <= 122; code += 1) {
      result.push(`r0-${major}${String.fromCharCode(code)}`);
    }
  }
  for (let code = 97; code <= 103; code += 1) {
    result.push(`r0-73${String.fromCharCode(code)}`);
  }
  return result;
}

function expectedPostR060() {
  return [
    "r0-61", "r0-62", "r0-63", "r0-64", "r0-65", "r0-66", "r0-67",
    "r0-67b", "r0-67c1", "r0-67c2", "r0-68a", "r0-68b1", "r0-68b2",
    "r0-68b2de", "r0-68b2fgh",
    ...Array.from({ length: 23 }, (_, index) =>
      `r0-69${String.fromCharCode(97 + index)}`),
    ...expectedPostR070A(),
  ];
}

function assertUniqueIds(value, label) {
  const ids = [...value.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]);
  assert.equal(new Set(ids).size, ids.length, `${label}: duplicate id`);
}

function accountingTokens(value) {
  return [...value.matchAll(
    /R0\.\d+[A-Z]?|v\d+(?:\.\d+)+|(?<![\p{L}\p{N}_])\d+(?:\.\d+)?(?![\p{L}\p{N}_])/gu,
  )].map((match) => match[0]);
}

async function inspectPdf(relative) {
  const payload = await bytes(relative);
  const latin = payload.toString("latin1");
  return {
    bytes: payload.length,
    pages: [...latin.matchAll(/\/Type\s*\/Page\b/g)].length,
    header: payload.subarray(0, 4).toString("latin1"),
  };
}

async function absent(relative) {
  await assert.rejects(
    access(resolve(root, relative)),
    (error) => error?.code === "ENOENT",
    relative,
  );
}

async function assertSourceBindings(rows, label) {
  assert.ok(Array.isArray(rows), label);
  assert.deepEqual(
    rows.map((row) => row.path).sort(),
    [...sourcePaths].sort(),
    `${label}: exact eight-source inventory`,
  );
  for (const row of rows) {
    const commit = row.sourceCommit ?? row.commit;
    assert.equal(commit, sourceCommit, `${label}: ${row.path}`);
    const frozen = await run("git", ["show", `${sourceCommit}:${row.path}`], {
      cwd: root,
      encoding: "buffer",
      maxBuffer: 16 * 1024 * 1024,
    });
    assert.deepEqual(await bytes(row.path), frozen.stdout, `${label}: ${row.path}`);
    assert.equal(row.sha256, await sha(row.path), `${label}: ${row.path}`);
  }
}

async function verifyFlatHashLedger(relative) {
  const directory = resolve(root, relative);
  const rows = (await readFile(resolve(directory, "SHA256SUMS"), "utf8"))
    .trimEnd().split("\n");
  const names = [];
  for (const row of rows) {
    const match = row.match(/^([0-9a-f]{64})  ([^/\\\r\n]+)$/);
    assert.ok(match, "malformed SHA256SUMS row: " + row);
    assert.equal(await sha(`${relative}/${match[2]}`), match[1], match[2]);
    names.push(match[2]);
  }
  assert.deepEqual(names, [...new Set(names)].sort());
  const entries = await readdir(directory, { withFileTypes: true });
  assert.ok(entries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  assert.deepEqual(
    names,
    entries.filter((entry) => entry.name !== "SHA256SUMS")
      .map((entry) => entry.name).sort(),
  );
}

test("R0.73G release source pins the v1.46-to-v1.47 transaction and source/E/F/C/S/P chain", async () => {
  const [generator, content, translation, agents] = await Promise.all([
    text("scripts/generate_r073g_release.py"),
    text("scripts/r073g_release_content.py"),
    text("scripts/add-r073g-translations.mjs"),
    text("AGENTS.md"),
  ]);
  const source = generator + "\n" + content;
  for (const token of [
    "R073F_RELEASE_BASELINE",
    '"latestCompletedRelease": "r073f"',
    '"siteVersion": "1.46"',
    '"publicHtmlNoteCount": 182',
    '"postR060RecapNodeCount": 122',
    '"postR070APublishedReleaseCount": 84',
    '"postR070AFormalSealedReleaseCount": 60',
    '"latestCompletedRelease": "r073g"',
    '"siteVersion": "1.47"',
    '"publicHtmlNoteCount": 183',
    '"postR060RecapNodeCount": 123',
    '"postR070APublishedReleaseCount": 85',
    '"postR070AFormalSealedReleaseCount": 61',
    '"legacyFormalFigureBacklogCount": 24',
    '"nextRelease": "r073h"',
    "123 unique nodes", "42 phases", "93 note links",
    "verify_complete_flat_ledger", "verify_source_bindings",
    `CERTIFIED_REPORT_COMMIT = "${sourceCommit}"`,
    `EXPERIMENT_PACKAGE_COMMIT = "${experimentCommit}"`,
    `FIGURE_PACKAGE_COMMIT = "${figureCommit}"`,
    `CERTIFICATE_PACKAGE_COMMIT = "${certificateCommit}"`,
    `FIGURE_METADATA_SEAL_COMMIT = "${sealCommit}"`,
    "source < E", "E < F", "F < C", "C < S", "S < P",
  ]) assert.ok(source.includes(token), token);
  const publicationCommit = generator.match(
    /FIGURE_PUBLICATION_COMMIT = "([0-9a-f]{40}|TO_BE_FILLED_AFTER_FIGURE_PUBLICATION_COMMIT)"/,
  )?.[1];
  assert.ok(publicationCommit, "P binding is placeholder-sealed or a full commit");
  const preflight = generator.slice(
    generator.indexOf("def preflight_release_state()"),
    generator.indexOf("def validate_analytic_sources()"),
  );
  assert.doesNotMatch(preflight, /assets\/r073g/,
    "P-first lifecycle must allow sealed public assets before HTML generation");
  for (const token of [
    "exactDecayingShearPerturbationEquation=CLOSED",
    "selectedSeedPlanarInvariantClass=CLOSED",
    "selectedNonlinearOrbitGlobalSmoothness=CLOSED",
    "topEigenvectorPolynomialH3Cost=CLOSED",
    "fixedWindowH3Bootstrap=CLOSED",
    "allModeQuadraticRemainderBound=CLOSED",
    "nonlinearRelativeAmplification=CLOSED",
    "topEigenvectorDoubleRowLeakage=CLOSED",
    "singleLinearRowNonlinearInvariant=FALSE",
    "kineticL2QuadraticRemainderBound=FALSE",
    "selectedRowCanCreateThreeDimensionalVortexStretching=FALSE",
    "oneRowGainAloneImpliesOrderOneDeparture=FALSE_AS_INFERENCE",
    "oneRowGainAloneImpliesFiniteTimeSingularity=FALSE",
    "naturalSeedOrderOneDeparture=OPEN",
    "harmonicResolvedEvenOddPropagation=OPEN",
    "transverseThreeDimensionalTriadClosure=OPEN",
    "singleBackgroundSingleOrbitInstability=OPEN",
    "completeOSSquireA2DirectSum=OPEN",
    "Clay=OPEN",
    "过小种子的非线性相对放大", "精确二维屏障", "R0.73H",
  ]) assert.ok(content.includes(token), token);
  assertPublicVoice(content, "R0.73G content source");

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
  assert.match(translation, /R073G_RELEASE_ROOT/);
  assert.match(translation, /i18n-en\.js\?v=1\.47/);
  assert.match(translation, /i18n-snapshots\/r073g-missing\.json/);
  assert.match(translation, /"r073g"\s*\+\s*String\(index \+ 1\)/);
  assert.match(translation, /FALSE_AS_INFERENCE/);
  assert.match(agents, /Publish this project only through the GitHub repository/);
  assert.match(agents, /https:\/\/kasifa\.github\.io\//);
  assert.doesNotMatch(source, /netlify\.app|vercel\.app|pages\.dev/i);
});

test("R0.73G analytic sources are byte-locked at the exact source commit", async () => {
  await assert.doesNotReject(
    run("git", ["cat-file", "-e", `${sourceCommit}^{commit}`], { cwd: root }),
  );
  for (const relative of sourcePaths) {
    const frozen = await run("git", ["show", `${sourceCommit}:${relative}`], {
      cwd: root,
      encoding: "buffer",
      maxBuffer: 16 * 1024 * 1024,
    });
    assert.deepEqual(await bytes(relative), frozen.stdout, relative);
  }
  const [report, gap, adversarial, independent] = await Promise.all([
    text("research/r073g_report-source.md"),
    text("research/r073g_gap_matrix.md"),
    text("research/r073g_adversarial_audit.md"),
    text("research/r073g_independent_analytic_audit.md"),
  ]);
  for (const key of [
    "exactDecayingShearPerturbationEquation", "selectedSeedPlanarInvariantClass",
    "selectedNonlinearOrbitGlobalSmoothness", "topEigenvectorPolynomialH3Cost",
    "fixedWindowH3Bootstrap", "allModeQuadraticRemainderBound",
    "nonlinearRelativeAmplification", "topEigenvectorDoubleRowLeakage",
  ]) {
    assert.ok(report.includes(`${key}=CLOSED`), key);
    assert.ok(gap.includes(`${key}=CLOSED`), key);
  }
  assert.match(adversarial, /POST-REPAIR SUBSTANTIVE VERDICT: FINAL PASS/);
  assert.match(independent, /\*\*Correction obligations:\*\* none/);
});

test("R0.73G source-stage builders have unique note anchors, post-R0.60 recap semantics, and route 93", async (context) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073f") {
    context.skip("final stage: builder transaction was already materialized");
    return;
  }
  const probe = String.raw`
import json, re, sys
sys.path.insert(0, "scripts")
import generate_r073g_release as release
note = release.build_note()
recap = release.build_recap()
home = release.update_home()
nav = re.search(r"<nav>(.*?)</nav>", note, flags=re.S)
anchors = re.findall(r'href="#([^"]+)"', nav.group(1)) if nav else []
start = recap.index('<section id="node-index">')
end = recap.index('</section>', start)
nodes = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73G">(.*?)</nav>', home, flags=re.S)
route_links = re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1)) if route else []
print(json.dumps({
    "anchors": anchors,
    "nodes": len(nodes),
    "uniqueNodes": len(set(nodes)),
    "phases": recap.count('<article class="phase">'),
    "postR060": "R0.60 之后的研究回顾" in recap,
    "startsAtR061": ">R0.61<" in recap,
    "routeLinks": len(route_links),
}))
`;
  const result = await run("python3", ["-c", probe], {
    cwd: root, maxBuffer: 16 * 1024 * 1024,
  });
  const payload = JSON.parse(result.stdout);
  assert.equal(payload.anchors.length, 18);
  assert.equal(new Set(payload.anchors).size, payload.anchors.length);
  assert.deepEqual(payload.anchors, [
    "result", "background", "equation", "planar", "launch", "bootstrap",
    "remainder", "seed", "leakage", "false", "finite", "literature",
    "audit", "figure", "boundary", "value", "next", "reproduce",
  ]);
  assert.deepEqual({
    nodes: payload.nodes, uniqueNodes: payload.uniqueNodes,
    phases: payload.phases, postR060: payload.postR060,
    startsAtR061: payload.startsAtR061, routeLinks: payload.routeLinks,
  }, {
    nodes: 123, uniqueNodes: 123, phases: 42,
    postR060: true, startsAtR061: true, routeLinks: 93,
  });
});

test("R0.73G generator remains read-only while publication commit P is a placeholder", async (context) => {
  const generator = await text("scripts/generate_r073g_release.py");
  if (!generator.includes(
    'FIGURE_PUBLICATION_COMMIT = "TO_BE_FILLED_AFTER_FIGURE_PUBLICATION_COMMIT"',
  )) {
    context.skip("P is pinned: placeholder-only safety test no longer applies");
    return;
  }
  const watched = [
    "research/release-manifest.json", "research/formal-archive-inventory.json",
    "public/site-version.json", "public/research-review.html",
    "public/literature-review.html", "public/notes/index.html", "VERSION",
  ];
  const before = new Map(await Promise.all(
    watched.map(async (relative) => [relative, await sha(relative)]),
  ));
  await assert.rejects(
    run("python3", ["scripts/generate_r073g_release.py"], {
      cwd: root,
      maxBuffer: 16 * 1024 * 1024,
    }),
    (error) => {
      assert.match(error.stderr, /TO_BE_FILLED_AFTER_FIGURE_PUBLICATION_COMMIT/);
      assert.match(error.stderr, /intentionally sealed shut/);
      return true;
    },
  );
  for (const relative of watched) assert.equal(await sha(relative), before.get(relative));
  for (const relative of [
    "public/notes/r0-73g.html", "public/notes/r0-73g.pdf",
    "public/recap-r0-61-r0-73g.html", "public/recap-r0-61-r0-73g.pdf",
    `public/assets/r073g/${figureId}.pdf`,
    `public/assets/r073g/${figureId}.svg`,
    `public/assets/r073g/${figureId}.png`,
  ]) await absent(relative);
});

test("R0.73G source and publication lifecycles keep the exact F or G counters", async () => {
  const [manifest, site, archive, version] = await Promise.all([
    json("research/release-manifest.json"), json("public/site-version.json"),
    json("research/formal-archive-inventory.json"), text("VERSION"),
  ]);
  if (manifest.latestCompletedRelease === "r073f") {
    assert.deepEqual({
      version: manifest.siteVersion, notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount, next: manifest.nextRelease,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, {
      version: "1.46", notes: 182, recap: 122, next: "r073g",
      published: 84, sealed: 60, backlog: 24,
    });
    assert.deepEqual(site, {
      schemaVersion: "research-site-version-v1", version: "1.46",
      latestRelease: "R0.73F", publicHtmlNoteCount: 182,
      publishedDate: "2026-08-30",
    });
    assert.equal(version, "1.46\n");
    assert.deepEqual({
      latest: archive.latestPublishedRelease, published: archive.publishedReleaseCount,
      sealed: archive.formalSealedReleaseCount, backlog: archive.legacyFormalFigureBacklogCount,
    }, { latest: "r073f", published: 84, sealed: 60, backlog: 24 });
  } else {
    assert.equal(manifest.latestCompletedRelease, "r073g");
    assert.deepEqual({
      version: manifest.siteVersion, notes: manifest.publicHtmlNoteCount,
      recap: manifest.postR060RecapNodeCount, next: manifest.nextRelease,
      gate: manifest.latestReleaseGate,
      publication: manifest.latestReleasePublicationTest,
      published: manifest.postR070APublishedReleaseCount,
      sealed: manifest.postR070AFormalSealedReleaseCount,
      backlog: manifest.legacyFormalFigureBacklogCount,
    }, {
      version: "1.47", notes: 183, recap: 123, next: "r073h",
      gate: "tests/r073g-nonlinear-bootstrap-gate.test.mjs",
      publication: "tests/r073g-release.test.mjs",
      published: 85, sealed: 61, backlog: 24,
    });
    assert.deepEqual(site, {
      schemaVersion: "research-site-version-v1", version: "1.47",
      latestRelease: "R0.73G", publicHtmlNoteCount: 183,
      publishedDate: "2026-08-30",
    });
    assert.equal(version, "1.47\n");
    assert.deepEqual({
      latest: archive.latestPublishedRelease, published: archive.publishedReleaseCount,
      sealed: archive.formalSealedReleaseCount, backlog: archive.legacyFormalFigureBacklogCount,
    }, { latest: "r073g", published: 85, sealed: 61, backlog: 24 });
    assert.equal(archive.publishedReleases.at(-1), "r073g");
    assert.equal(archive.formalSealedReleases.at(-1), "r073g");
  }
});

test("R0.73G final pages synchronize note 183, recap 123/42, route 93, and next H", async (context) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073g") {
    context.skip("source stage: public mutation is correctly absent");
    return;
  }
  const [note, recap, home, literature, noteIndex] = await Promise.all([
    text("public/notes/r0-73g.html"), text("public/recap-r0-61-r0-73g.html"),
    text("public/research-review.html"), text("public/literature-review.html"),
    text("public/notes/index.html"),
  ]);
  const noteFiles = await readdir(resolve(publicRoot, "notes"));
  assert.equal(noteFiles.filter((name) => /^r0-[0-9a-z]+\.html$/.test(name)).length, 183);
  for (const token of [
    "nonlinearRelativeAmplification=CLOSED",
    "selectedNonlinearOrbitGlobalSmoothness=CLOSED",
    "singleLinearRowNonlinearInvariant=FALSE",
    "oneRowGainAloneImpliesOrderOneDeparture=FALSE_AS_INFERENCE",
    "naturalSeedOrderOneDeparture=OPEN",
    "transverseThreeDimensionalTriadClosure=OPEN", "Clay=OPEN",
    `/assets/r073g/${figureId}.svg`, "/notes/r0-73g.pdf",
    "/recap-r0-61-r0-73g.html", "R0.73H",
  ]) assert.ok(note.includes(token), token);
  const nodes = [...nodeIndex(recap).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.deepEqual(nodes, expectedPostR060());
  await Promise.all(nodes.map((slug) => access(resolve(publicRoot, `notes/${slug}.html`))));
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 42);
  assert.ok(recap.includes("85 个版本已经公开"));
  assert.ok(recap.includes("61 个满足当前完整封存合同"));
  assert.equal((home.match(/data-release="r073g"/g) ?? []).length, 1);
  const route = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.73G">([\s\S]*?)<\/nav>/,
  )?.[1] ?? "";
  const routeSlugs = [...route.matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  const expectedRoute = [
    ...Array.from({ length: 8 }, (_, index) =>
      `r0-69${String.fromCharCode(112 + index)}`),
    ...expectedPostR070A(),
  ];
  assert.deepEqual(routeSlugs, expectedRoute);
  await Promise.all(routeSlugs.map((slug) =>
    access(resolve(publicRoot, `notes/${slug}.html`))));
  const cards = [...home.matchAll(
    /<div class="task-one" id="(r0\d+[a-z])" data-release="\1"[\s\S]*?<\/div>/g,
  )];
  const expectedCardIds = expectedPostR070A().map((slug) => slug.replace("r0-", "r0"));
  assert.deepEqual(cards.map((match) => match[1]), expectedCardIds);
  for (const match of cards) {
    const noteSlug = match[1].replace(/^r0(\d+)/, "r0-$1");
    assert.ok(match[0].includes(`href="/notes/${noteSlug}.html"`), noteSlug);
  }
  assert.equal((home.match(/<strong style="color:var\(--gold\)">下一步 R0\.73H：/g) ?? []).length, 1);
  assert.ok(literature.includes('id="r073g-boundary"'));
  assert.ok(literature.includes("开放接口 · R0.73H"));
  assert.ok(noteIndex.includes('data-note="r0-73g"'));
  assert.ok(noteIndex.includes('href="/notes/r0-73g.pdf"'));
  assert.ok(noteIndex.includes("183 篇公开研究笔记"));
  assert.ok(note.includes("28 个正式网格点"));
  assert.ok(note.includes("5 个预注册哨兵点"));
  assert.ok(note.includes("5.21\\times10^{-16}"));
  assert.ok(note.includes("6.01\\times10^{-16}"));
  for (const [value, label] of [
    [note, "note"], [recap, "recap"], [home, "home"],
    [literature, "literature"], [noteIndex, "index"],
  ]) {
    assertUniqueIds(value, label);
    assert.ok(value.includes('/i18n-en.js?v=1.47'), label);
    assertPublicVoice(value, label);
  }
});

test("R0.73G formal lifecycle preserves A/E/F/C/S/P and public byte identity", async (context) => {
  const release = await json("research/release-manifest.json");
  if (release.latestCompletedRelease !== "r073g") {
    context.skip("source stage: formal publication artifacts are not yet complete");
    return;
  }
  const [generator, figureManifest, certificateManifest] = await Promise.all([
    text("scripts/generate_r073g_release.py"), json(`${figure}/manifest.json`),
    json("research/certificates/r073g/manifest.json"),
  ]);
  const commits = Object.fromEntries([
    ["E", "EXPERIMENT_PACKAGE_COMMIT"], ["F", "FIGURE_PACKAGE_COMMIT"],
    ["C", "CERTIFICATE_PACKAGE_COMMIT"],
    ["S", "FIGURE_METADATA_SEAL_COMMIT"], ["P", "FIGURE_PUBLICATION_COMMIT"],
  ].map(([label, name]) => [
    label, generator.match(new RegExp(`${name}\\s*=\\s*"([0-9a-f]{40})"`))?.[1],
  ]));
  for (const [label, commit] of Object.entries(commits)) assert.ok(commit, label);
  assert.equal(commits.E, experimentCommit);
  assert.equal(new Set([sourceCommit, ...Object.values(commits)]).size, 6);
  for (const [ancestor, descendant, label] of [
    [sourceCommit, commits.E, "A < E"], [commits.E, commits.F, "E < F"],
    [commits.F, commits.C, "F < C"],
    [commits.C, commits.S, "C < S"], [commits.S, commits.P, "S < P"],
    [commits.P, "HEAD", "P <= HEAD"],
  ]) await assert.doesNotReject(
    run("git", ["merge-base", "--is-ancestor", ancestor, descendant], { cwd: root }),
    label,
  );

  const immutableAtF = [
    "README.md", "caption.md", "config.json", "figure.pdf", "figure.png",
    "figure.svg", "plot.py", "qa-final-size.png", "qa-grayscale.png",
    "qa-pdf.png", "qa-protocol.md", "qa-report.md", "requirements.txt", "results.json",
  ];
  assert.equal(immutableAtF.length, 14);
  for (const name of immutableAtF) {
    const relative = `${figure}/${name}`;
    const [frozen, current] = await Promise.all([
      run("git", ["rev-parse", `${commits.F}:${relative}`], { cwd: root }),
      run("git", ["hash-object", relative], { cwd: root }),
    ]);
    assert.equal(current.stdout.trim(), frozen.stdout.trim(), `${name}: differs from F`);
  }
  for (const name of ["contract.json", "command.txt", "validate.py", "validation.json"]) {
    const relative = `${figure}/${name}`;
    const [sealed, current] = await Promise.all([
      run("git", ["rev-parse", `${commits.S}:${relative}`], { cwd: root }),
      run("git", ["hash-object", relative], { cwd: root }),
    ]);
    assert.equal(current.stdout.trim(), sealed.stdout.trim(), `${name}: differs from S`);
  }
  const publicationFree = { ...figureManifest };
  assert.ok(Object.hasOwn(publicationFree, "publication"));
  delete publicationFree.publication;
  const sealedManifest = await run("git", ["show", `${commits.S}:${figure}/manifest.json`], {
    cwd: root, maxBuffer: 16 * 1024 * 1024,
  });
  assert.equal(`${JSON.stringify(publicationFree, null, 2)}\n`, sealedManifest.stdout);
  const stripManifestRow = (value) => {
    const rows = value.match(/^[0-9a-f]{64}  manifest\.json\r?\n?/gm) ?? [];
    assert.equal(rows.length, 1);
    return value.replace(/^[0-9a-f]{64}  manifest\.json\r?\n?/gm, "");
  };
  const [currentLedger, sealedLedger] = await Promise.all([
    text(`${figure}/SHA256SUMS`),
    run("git", ["show", `${commits.S}:${figure}/SHA256SUMS`], { cwd: root })
      .then((result) => result.stdout),
  ]);
  assert.equal(stripManifestRow(currentLedger), stripManifestRow(sealedLedger));

  const publicationTree = (await run(
    "git", ["ls-tree", "-r", "--name-only", commits.P, "--", figure], { cwd: root },
  )).stdout.trim().split("\n").filter(Boolean).sort();
  const currentEntries = await readdir(resolve(root, figure), { withFileTypes: true });
  assert.ok(currentEntries.every((entry) => entry.isFile() && !entry.isSymbolicLink()));
  assert.deepEqual(
    currentEntries.map((entry) => `${figure}/${entry.name}`).sort(), publicationTree,
  );
  for (const relative of publicationTree) {
    const [published, current] = await Promise.all([
      run("git", ["rev-parse", `${commits.P}:${relative}`], { cwd: root }),
      run("git", ["hash-object", relative], { cwd: root }),
    ]);
    assert.equal(current.stdout.trim(), published.stdout.trim(), relative);
  }
  await verifyFlatHashLedger(figure);
  await verifyFlatHashLedger("research/certificates/r073g");
  assert.equal(figureManifest.git.sourceCommit, sourceCommit);
  assert.equal(figureManifest.git.figurePackageCommit, commits.F);
  assert.equal(figureManifest.git.certificateCommit, commits.C);
  assert.equal(certificateManifest.sourceCommit, sourceCommit);
  await assertSourceBindings(figureManifest.sourceBindings, "figure source bindings");
  await assertSourceBindings(certificateManifest.sourceBindings, "certificate source bindings");
  assert.equal(figureManifest.publication.byteIdentityRequired, true);
  assert.equal(figureManifest.publication.publicCopiesComplete, true);
  assert.equal(figureManifest.publication.directory, "public/assets/r073g");
  assert.equal(figureManifest.publication.fileStem, figureId);
  assert.equal(figureManifest.publication.assets.length, 3);
  for (const suffix of ["pdf", "svg", "png"]) {
    const sourcePath = `${figure}/figure.${suffix}`;
    const publicPath = `public/assets/r073g/${figureId}.${suffix}`;
    assert.deepEqual(await bytes(publicPath), await bytes(sourcePath), suffix);
    const row = figureManifest.publication.assets.find((asset) => asset.path === publicPath);
    assert.ok(row, suffix);
    assert.equal(row.bytes, (await bytes(publicPath)).length);
    assert.equal(row.sha256, await sha(publicPath));
  }
  for (const relative of ["public/notes/r0-73g.pdf", "public/recap-r0-61-r0-73g.pdf"]) {
    const pdf = await inspectPdf(relative);
    assert.equal(pdf.header, "%PDF");
    assert.ok(pdf.bytes > 25_000 && pdf.pages >= 2, JSON.stringify(pdf));
  }
});

test("R0.73G final English dictionary is complete, neutral, and token-preserving", async (context) => {
  const manifest = await json("research/release-manifest.json");
  if (manifest.latestCompletedRelease !== "r073g") {
    context.skip("source stage: R0.73G public strings do not exist yet");
    return;
  }
  const source = await collectSiteStrings(publicRoot);
  const translations = await json("translations/en.json");
  const byChinese = new Map(translations.map((entry) => [entry.zh, entry.en]));
  assert.equal(byChinese.size, translations.length);
  assert.deepEqual(source.filter((entry) => !byChinese.has(entry.zh)), []);
  const boundaryTokens = (value) =>
    value.match(/\b(?:CLOSED|OPEN|FALSE_AS_INFERENCE|FALSE|CONDITIONAL)\b/g) ?? [];
  const batch = translations.filter((entry) => /^r073g\d+$/.test(entry.id));
  assert.ok(batch.length > 0);
  for (const entry of batch) {
    assert.equal(containsChinese(entry.en), false, entry.zh);
    assert.equal(/\b(?:we|our|ours|ourselves|us)\b/i.test(entry.en), false, entry.zh);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh), entry.zh);
    assert.deepEqual(accountingTokens(entry.en), accountingTokens(entry.zh), entry.zh);
    assert.deepEqual(boundaryTokens(entry.en), boundaryTokens(entry.zh), entry.zh);
  }
  const result = await run(process.execPath, [
    "scripts/add-r073g-translations.mjs", "--check-only",
  ], { cwd: root, maxBuffer: 16 * 1024 * 1024 });
  assert.match(result.stdout, /"missingAfter":0/);
});

test("R0.73G remains a GitHub Pages-only publication contract", async () => {
  for (const relative of ["netlify.toml", "vercel.json", "wrangler.toml"]) {
    await absent(relative);
  }
  const [pages, agents] = await Promise.all([
    text(".github/workflows/pages.yml"), text("AGENTS.md"),
  ]);
  assert.match(pages, /actions\/deploy-pages@/);
  assert.match(agents, /GitHub Pages site at `https:\/\/kasifa\.github\.io\/`/);
  assert.match(agents, /Do not mirror or deploy/);
});
