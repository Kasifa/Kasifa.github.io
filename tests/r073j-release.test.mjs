import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { copyFile, mkdir, mkdtemp, readFile, readdir, rm } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { containsChinese, extractProtectedTokens } from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const bytes = (relative) => readFile(resolve(root, relative));

const figureId = "fig-r073j-continuum-branch-certificate";
const figureRoot = `figures/r073j/${figureId}`;
const mirrorRoot = `public/${figureRoot}`;
const publicFigureRoot = `public/assets/r073j/${figureId}`;
const publicPages = {
  note: "public/notes/r0-73j.html",
  recap: "public/recap-r0-61-r0-73j.html",
  home: "public/research-review.html",
  literature: "public/literature-review.html",
  index: "public/notes/index.html",
};

const target = {
  version: "1.50", latest: "r073j", notes: 186, recap: 126,
  published: 88, sealed: 64, backlog: 24, next: "r073k",
};
const forbidden = [
  "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  "颠覆性", "世界首个", "接近解决", "解决了千禧年", "证明了全局正则性",
  "原创性定理", "首次证明",
];

function assertPublicVoice(value, label) {
  for (const phrase of forbidden) assert.equal(value.includes(phrase), false, `${label}: ${phrase}`);
  assert.doesNotMatch(value, /\b(?:we|our|ours|ourselves|us)\b/i, `${label}: collective English voice`);
}

function machineLedgerAssignments(value) {
  return [...value.matchAll(/\b([A-Za-z][A-Za-z0-9]*)=([A-Z][A-Z0-9_]*)\b/g)]
    .map((match) => match[0]);
}

function recapNodes(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start, "recap node-index section");
  return [...recap.slice(start, end).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
}

function section(html, id) {
  const start = html.indexOf(`<section id="${id}">`);
  const end = html.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start, `section #${id}`);
  return html.slice(start, end);
}

async function assertPdf(relative) {
  const value = await bytes(relative);
  assert.ok(value.length > 4, `${relative}: nonempty PDF`);
  assert.equal(value.subarray(0, 4).toString(), "%PDF", relative);
}

test("R0.73J pins the v1.50 accounting endpoint", async () => {
  const [release, site, inventory, version] = await Promise.all([
    json("research/release-manifest.json"), json("public/site-version.json"),
    json("research/formal-archive-inventory.json"), text("VERSION"),
  ]);
  assert.deepEqual({
    version: release.siteVersion, latest: release.latestCompletedRelease,
    notes: release.publicHtmlNoteCount, recap: release.postR060RecapNodeCount,
    published: release.postR070APublishedReleaseCount,
    sealed: release.postR070AFormalSealedReleaseCount,
    backlog: release.legacyFormalFigureBacklogCount, next: release.nextRelease,
  }, target);
  assert.equal(release.latestReleaseGate, "tests/r073j-continuum-branch-gate.test.mjs");
  assert.equal(release.latestReleasePublicationTest, "tests/r073j-release.test.mjs");
  assert.deepEqual({ version: site.version, latest: site.latestRelease, notes: site.publicHtmlNoteCount },
    { version: "1.50", latest: "R0.73J", notes: 186 });
  assert.equal(inventory.latestPublishedRelease, "r073j");
  assert.equal(inventory.publishedReleaseCount, 88);
  assert.equal(inventory.formalSealedReleaseCount, 64);
  assert.equal(inventory.legacyFormalFigureBacklogCount, 24);
  assert.equal(version, "1.50\n");
});

test("R0.73J release source pins every executable generation helper", async () => {
  const generator = await text("scripts/generate_r073j_release.py");
  for (const relative of [
    "scripts/r073j_release_content.py",
    "scripts/add-r073j-translations.mjs",
    "scripts/generate_r072o_release.py",
    "scripts/generate_r072p_release.py",
    "scripts/generate_note_index.py",
    "scripts/i18n-lib.mjs",
    "tests/r073j-continuum-branch-gate.test.mjs",
    "tests/r073j-release.test.mjs",
  ]) assert.ok(generator.includes(JSON.stringify(relative)), `release-source pin ${relative}`);
  assert.match(generator, /normalized_release_generator\(git_bytes\(RELEASE_SOURCE_COMMIT, generator_relative\)\)/);
});

test("R0.73J public route, recap, and claim boundary are complete", async () => {
  const [note, recap, home, literature, index] = await Promise.all(Object.values(publicPages).map(text));
  for (const [label, value] of Object.entries({ note, recap, home, literature, index })) {
    assert.ok(value.includes("R0.73J"), `${label}: release label`);
    assert.ok(value.includes("/i18n-en.js?v=1.50"), `${label}: i18n v1.50`);
    assertPublicVoice(value, `${label} HTML`);
  }
  for (const token of [
    "0.167", "0.173", "0.11", "0.057", "1/20", "0.585343", "0.585009",
    "1.84154", "5.49948", "0.164355", "76", "83", "depth-two", "1/7",
    "2896/2896", "0.00714950", "0.04", "不承担连续算子上的存在性或重数证明权重",
    "NOT CLAY",
  ]) assert.ok(note.includes(token), `note token ${token}`);
  assert.ok(note.includes("共享原始网格"));
  assert.ok(note.includes("independentOverlapRawOdeRecomputation=NOT_RUN"));
  for (const key of [
    "fullyIndependentRawGridAudit=OPEN", "uniformRankOneViscousBranch=OPEN",
    "nonselfadjointAdiabaticRemainder=OPEN", "matchingSelectedGainAction=OPEN",
    "twoTermSelectedGainAsymptotic=OPEN", "actionResolvedBackwardLocalization=OPEN",
    "prescribedActionSeedDeparture=OPEN", "fixedBackgroundLyapunovInstability=OPEN",
    "transverseThreeDimensionalClosure=OPEN", "finiteTimeSingularity=OPEN", "Clay=OPEN",
  ]) assert.ok(note.includes(key), `OPEN ledger ${key}`);
  assert.ok(section(note, "next").includes("R0.73K"));
  assert.doesNotMatch(section(note, "boundary"), /线性连续谱认证/);

  const nodes = recapNodes(recap);
  assert.equal(nodes.length, 126);
  assert.equal(new Set(nodes).size, 126);
  assert.equal(nodes[0], "r0-61");
  assert.equal(nodes.at(-1), "r0-73j");
  assert.equal(recap.match(/<article class="phase">/g)?.length, 45);
  assert.ok(recap.includes("回顾截止节点：R0.73J"));

  assert.ok(home.includes("LATEST RELEASE · R0.73J"));
  assert.ok(home.includes("当前端点 R0.73J"));
  assert.ok(home.includes("NEXT · R0.73K"));
  assert.ok(home.includes('/notes/r0-73j.pdf'));
  assert.ok(home.includes('/recap-r0-61-r0-73j.html'));
  assert.ok(literature.includes('id="r073j-boundary"'));
  assert.ok(literature.includes("2896/2896"));
  assert.ok(literature.includes("独立 overlap raw-ODE 三盒仍未运行"));
  const literatureIds = [...literature.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]);
  assert.equal(new Set(literatureIds).size, literatureIds.length, "literature HTML ids are unique");
  for (let number = 146; number <= 155; number += 1) {
    assert.equal(literatureIds.filter((id) => id === `ref-${number}`).length, 1, `ref-${number}`);
  }
  assert.ok(index.includes('data-note="r0-73j"'));
  assert.ok(index.includes("186 篇公开研究笔记"));
});

test("R0.73J figure mirrors are byte-identical and synchronized PDFs exist", async () => {
  for (const name of [
    "README.md", "SHA256SUMS", "caption.md", "command.txt", "config.json", "contract.json",
    "environment.json", "figure.pdf", "figure.png", "figure.svg", "manifest.json", "plot.py",
    "progress.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "qa-protocol.md",
    "qa-report.md", "requirements.txt", "resource-log.ndjson", "results.json", "source-data.csv",
    "validate.py", "validation.json",
  ]) assert.deepEqual(await bytes(`${mirrorRoot}/${name}`), await bytes(`${figureRoot}/${name}`), `mirror ${name}`);
  for (const suffix of ["pdf", "svg", "png"]) {
    assert.deepEqual(await bytes(`${publicFigureRoot}.${suffix}`), await bytes(`${figureRoot}/figure.${suffix}`), `${suffix} web master`);
  }
  await assertPdf("public/notes/r0-73j.pdf");
  await assertPdf("public/recap-r0-61-r0-73j.pdf");
});

test("R0.73J experiment and figure preserve certificate and audit boundaries", async () => {
  const [manifest, summary, contour, overlap, independent, independentOverlap, natural, depth2, deep, failures, figure, result, validation] = await Promise.all([
    json("experiments/r073j/manifest.json"), json("experiments/r073j/summary.json"),
    json("experiments/r073j/contour_certificate.json"), json("experiments/r073j/overlap_certificate.json"),
    json("experiments/r073j/independent_validation.json"), json("experiments/r073j/independent_overlap_validation.json"),
    json("experiments/r073j/natural_box_validation.json"), json("experiments/r073j/natural_box_refinement.json"),
    json("experiments/r073j/natural_box_refinement_deep.json"), json("experiments/r073j/failure_ledger.json"),
    json(`${figureRoot}/manifest.json`), json(`${figureRoot}/results.json`), json(`${figureRoot}/validation.json`),
  ]);
  assert.equal(manifest.schemaVersion, "r073j-validated-computation-manifest-v1");
  assert.equal(manifest.allChecksPass, true);
  assert.equal(manifest.sharedRawGridLimitationDeclared, true);
  assert.equal(manifest.naturalBoxAuditIsPrerequisite, false);
  assert.equal(manifest.claimBoundary.clayProblemSolved, false);
  assert.equal(summary.theorem.rootInterval, "167/1000 < lambda_0(d) < 173/1000");
  assert.equal(summary.theorem.otherSpectrumUpperRealPart, "11/100");
  assert.equal(summary.theorem.strictRealPartGap, "57/1000");
  assert.equal(summary.theorem.conservativeGap, "1/20");

  assert.equal(contour.status, "passed");
  assert.equal(contour.panels.length, 64);
  assert.equal(contour.decisions.globalBasePositiveOrientationWinding, 1);
  assert.equal(contour.decisions.localBasePositiveOrientationWinding, 1);
  assert.match(contour.decisions.globalMinimumAbsoluteLower, /^\[5\.499484/);
  assert.match(contour.decisions.localMinimumAbsoluteLower, /^\[0\.164355/);
  assert.equal(overlap.status, "passed");
  assert.equal(overlap.cells.length, 128);
  assert.match(overlap.decisions.minimumKineticOverlapLower, /^\[0\.585343/);
  assert.match(overlap.decisions.minimumAnchorAbsoluteLower, /^\[1\.841548/);
  assert.equal(independent.classification, "independent-postprocessing-from-shared-raw-grid");
  assert.match(independent.independentDecisions.globalMinimumAbsoluteLower, /^\[5\.497398/);
  assert.match(independentOverlap.decisions.minimumKineticOverlapLower, /^\[0\.585009/);
  assert.equal(natural.status, "failed");
  assert.deepEqual([natural.decisions.passedBoxCount, natural.decisions.failedBoxCount], [76, 7]);
  assert.equal(depth2.status, "inconclusive");
  assert.deepEqual([depth2.decisions.originalFailedParentCount, depth2.decisions.secondLevelPassedBoxCount, depth2.decisions.secondLevelFailedBoxCount], [7, 16, 96]);
  assert.equal(deep.status, "passed");
  assert.equal(deep.decisions.resolvedOriginalParentCount, 7);
  assert.equal(deep.decisions.finalPassedLeafBoxCount, 2896);
  assert.equal(deep.decisions.finalInconclusiveLeafBoxCount, 0);
  assert.match(deep.decisions.minimumFinalPassedLeafEvansAbsoluteLower.value, /^\[0\.00714950/);
  assert.equal(failures.entries.length, 2);

  assert.equal(figure.schemaVersion, "r073j-continuum-branch-figure-manifest-v1");
  assert.equal(figure.status, "formal");
  assert.equal(figure.claimBoundary.clayProblemSolved, false);
  assert.equal(result.rowCounts.globalContourPanels + result.rowCounts.localContourPanels, 64);
  assert.equal(result.rowCounts.overlapCells, 128);
  assert.equal(result.rowCounts.sourceData, 192);
  assert.equal(result.decisions.globalBasePositiveOrientationWinding, 1);
  assert.equal(result.decisions.localBasePositiveOrientationWinding, 1);
  assert.ok(Object.values(validation.checks).every(Boolean));
});

test("R0.73J translations and browser bundle are synchronized and public-safe", async () => {
  const [translations, bundle, ...htmlPages] = await Promise.all([
    json("translations/en.json"), text("public/i18n-en.js"), ...Object.values(publicPages).map(text),
  ]);
  const rows = translations.filter((entry) => /^r073j\d+$/.test(entry.id));
  assert.ok(rows.length > 0, "R0.73J translation rows");
  assert.equal(new Set(rows.map((entry) => entry.id)).size, rows.length);
  assert.equal(new Set(rows.map((entry) => entry.zh)).size, rows.length);
  for (const [index, entry] of rows.entries()) {
    const label = `R0.73J translation row ${index + 1}`;
    assert.ok(typeof entry.en === "string" && entry.en.trim(), `${label}: en`);
    assert.equal(containsChinese(entry.en), false, `${label}: Chinese in English`);
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i, label);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh), `${label}: protected tokens`);
    assert.deepEqual(machineLedgerAssignments(entry.en), machineLedgerAssignments(entry.zh), `${label}: machine ledgers`);
    assert.ok(bundle.includes(`${JSON.stringify(entry.zh)}: ${JSON.stringify(entry.en)}`), `${label}: browser bundle`);
  }
  const machineLedgers = rows.flatMap((entry) => machineLedgerAssignments(entry.zh));
  for (const status of [
    "FAILED_WITH_LEDGER", "76_PASS_7_WRAPPING_INCONCLUSIVE",
    "PASS_7_OF_7_PARENTS_2896_OF_2896_LEAVES",
  ]) assert.ok(machineLedgers.some((assignment) => assignment.endsWith(`=${status}`)), `machine ledger ${status}`);
  assertPublicVoice(JSON.stringify(rows), "R0.73J translations");
  for (const [index, value] of htmlPages.entries()) assertPublicVoice(value, `public HTML ${index + 1}`);
});

test("R0.73J note-index generation is isolated by R073J_RELEASE_ROOT", async () => {
  const scratch = await mkdtemp(resolve(tmpdir(), "r073j-release-root-"));
  try {
    const notes = resolve(scratch, "public/notes");
    await mkdir(notes, { recursive: true });
    for (const name of await readdir(resolve(root, "public/notes"))) {
      if (/^r0-.*\.html$/.test(name) && name !== "r0-73j.html") {
        await copyFile(resolve(root, "public/notes", name), resolve(notes, name));
      }
    }
    await copyFile(resolve(root, "public/site-version.json"), resolve(scratch, "public/site-version.json"));
    const code = `
import json
import generate_r073j_release as g
payload=json.dumps({'schemaVersion':'research-site-version-v1','version':'1.50','latestRelease':'R0.73J','publicHtmlNoteCount':186,'publishedDate':'2026-08-30'}).encode()
value=g.build_note_index(payload)
assert 'data-note="r0-73j"' in value
assert ${JSON.stringify(root)} not in str(g.ROOT)
print('isolated-ok')
`;
    const run = spawnSync("python3", ["-c", code], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, PYTHONPATH: resolve(root, "scripts"), R073J_RELEASE_ROOT: scratch },
    });
    assert.equal(run.status, 0, run.stderr);
    assert.match(run.stdout, /isolated-ok/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});
