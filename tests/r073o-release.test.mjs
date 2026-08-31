import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { access, readFile } from "node:fs/promises";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const text = (relative) => readFile(resolve(root, relative), "utf8");
const bytes = (relative) => readFile(resolve(root, relative));
const json = async (relative) => JSON.parse(await text(relative));
const sha256 = (payload) => createHash("sha256").update(payload).digest("hex");
const exists = async (relative) => {
  try {
    await access(resolve(root, relative));
    return true;
  } catch (error) {
    if (error?.code === "ENOENT") return false;
    throw error;
  }
};
const run = (command, argumentsList) => spawnSync(command, argumentsList, {
  cwd: root,
  encoding: "utf8",
  env: { ...process.env, R073O_RELEASE_ROOT: root },
});

const scaffoldFiles = [
  "scripts/r073o_release_content.py",
  "scripts/generate_r073o_release.py",
  "scripts/add-r073o-translations.mjs",
  "scripts/bind-r073o-pdfs.mjs",
  "tests/r073o-release.test.mjs",
];
const coreSources = [
  "research/r073o_problem_freeze.md",
  "research/r073o_global_orbit_stability_proof.md",
  "research/r073o_forced_kolmogorov_contrast.md",
  "research/r073o_independent_analytic_audit.md",
  "research/r073o_literature_audit.md",
  "research/r073o_claim_source_ledger.md",
  "research/r073o_gap_matrix.md",
];
const finalSources = [
  "research/r073o_finite_diagnostic_audit.md",
  "research/r073o_report-source.md",
  "research/r073o_bilingual_dictionary.md",
];
const targetPages = {
  note: "public/notes/r0-73o.html",
  recap: "public/recap-r0-61-r0-73o.html",
  home: "public/research-review.html",
  literature: "public/literature-review.html",
  index: "public/notes/index.html",
};
const forbidden = [
  "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  "颠覆性", "世界首个", "接近解决", "解决了千禧年", "证明了全局正则性",
  "原创性定理", "首次证明",
];
const pinNames = [
  "RELEASE_BASELINE_COMMIT", "ANALYTIC_SOURCE_COMMIT", "FINITE_PACKAGE_COMMIT",
  "FIGURE_PACKAGE_COMMIT", "FINAL_CONTENT_COMMIT", "RELEASE_SOURCE_COMMIT",
];

function releasePins(generator) {
  return Object.fromEntries(pinNames.map((name) => {
    const match = generator.match(new RegExp(
      `^${name} = (ZERO_COMMIT|"([0-9a-f]{40})")$`, "m",
    ));
    assert.ok(match, `${name}: missing or malformed pin slot`);
    return [name, { zero: match[1] === "ZERO_COMMIT", commit: match[2] ?? null }];
  }));
}

test("R0.73O scaffold is fail-closed and names the R0.73N baseline", async () => {
  for (const relative of scaffoldFiles) assert.equal(await exists(relative), true, relative);
  for (const relative of coreSources) assert.equal(await exists(relative), true, relative);
  const generator = await text("scripts/generate_r073o_release.py");
  const pins = releasePins(generator);
  assert.equal(pins.RELEASE_BASELINE_COMMIT.zero, false);
  assert.equal(pins.RELEASE_BASELINE_COMMIT.commit,
    "d6d12469c266d16f08834320e2cae869af0aa479");
  const later = [pins.ANALYTIC_SOURCE_COMMIT, pins.FINITE_PACKAGE_COMMIT,
    pins.FIGURE_PACKAGE_COMMIT, pins.FINAL_CONTENT_COMMIT, pins.RELEASE_SOURCE_COMMIT];
  const firstZero = later.findIndex(({ zero }) => zero);
  if (firstZero >= 0) assert.ok(later.slice(firstZero).every(({ zero }) => zero));
  assert.match(generator, /R0\.73N release baseline/);
  assert.match(await text("scripts/r073o_release_content.py"), /fig-r073o-kolmogorov-spectrum/);
  assert.match(generator, /R073O_CERTIFICATE_DEPS/);
  assert.match(generator, /--verify-only/);
  assert.match(generator, /verify_pinned_paths_exist\(RELEASE_BASELINE_COMMIT/);
  assert.doesNotMatch(generator, /verify_exact_paths\(RELEASE_BASELINE_COMMIT/);
});

test("R0.73O command help is side-effect-free", () => {
  for (const [command, relative] of [
    ["python3", "scripts/r073o_release_content.py"],
    ["python3", "scripts/generate_r073o_release.py"],
    [process.execPath, "scripts/add-r073o-translations.mjs"],
    [process.execPath, "scripts/bind-r073o-pdfs.mjs"],
  ]) {
    const result = run(command, [relative, "--help"]);
    assert.equal(result.status, 0, `${relative}: ${result.stderr}`);
    assert.match(result.stdout, /usage:/i, relative);
  }
});

test("R0.73O source dry-run is local, read-only, and reports canonical gates", async () => {
  const watched = ["VERSION", "research/release-manifest.json", "public/site-version.json",
    "public/research-review.html", "public/literature-review.html", "public/notes/index.html"];
  const before = await Promise.all(watched.map(bytes));
  const contentCheck = run("python3", ["scripts/r073o_release_content.py", "--check-only"]);
  assert.equal(contentCheck.status, 0, contentCheck.stderr);
  const result = run("python3", ["scripts/generate_r073o_release.py", "--source-dry-run"]);
  assert.equal(result.status, 0, result.stderr);
  const summary = JSON.parse(result.stdout);
  assert.equal(summary.release, "R0.73O");
  assert.equal(summary.fullThreeDimensionalFPS_H3_L2, "OPEN");
  assert.equal(summary.canonicalSourcesPlanned, coreSources.length + finalSources.length);
  const missing = (await Promise.all(finalSources.map(async (relative) => [relative, await exists(relative)])))
    .filter(([, present]) => !present).map(([relative]) => relative).sort();
  assert.deepEqual(summary.missingCanonicalSources.sort(), missing);
  assert.equal(summary.writes, 0);
  const finalText = (await Promise.all(finalSources.map(async (relative) => (
    await exists(relative) ? await text(relative) : ""
  )))).join("\n");
  const hasPresealState = [
    "finiteDiagnosticPackage=PRESEAL_PASS",
    "sourceCommitAssigned=FALSE",
    "finalSeal=FALSE",
    "formalFigurePackage=PRESEAL_PASS",
    "publicReleaseContent=PENDING",
  ].some((token) => finalText.includes(token));
  if (missing.length > 0 || hasPresealState) {
    assert.equal(summary.finalContentReady, false);
    assert.ok(summary.finalContentPending.length > 0);
  }
  assert.deepEqual(summary.bindingOrder, ["R0.73N release baseline", "analytic source",
    "finite package", "figure package", "final content", "R0.73O release source"]);
  assert.deepEqual(summary.publicationStageOrder, ["freeze-r073n-baseline",
    "freeze-analytic-source", "seal-finite-package-to-analytic-source",
    "seal-figure-package-to-analytic-source", "freeze-final-report-dictionary-and-finite-audit",
    "freeze-release-source-and-fill-normalized-pin-slot", "apply-html-manifest-and-figure-transaction",
    "capture-review-and-apply-translations", "render-synchronized-note-and-recap-pdfs",
    "bind-html-pdf-hashes-and-titles", "run-publication-tests-then-deploy"]);
  const after = await Promise.all(watched.map(bytes));
  assert.deepEqual(after.map(sha256), before.map(sha256));
});

test("R0.73O check-only remains sealed while a required pin is zero", async (t) => {
  const pins = Object.values(releasePins(await text("scripts/generate_r073o_release.py")));
  if (pins.every(({ zero }) => !zero)) {
    t.skip("all pins are bound");
    return;
  }
  const before = await Promise.all([bytes("VERSION"), bytes("research/release-manifest.json"),
    bytes("public/site-version.json"), bytes("public/research-review.html")]);
  const result = run("python3", ["scripts/generate_r073o_release.py", "--check-only"]);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr + result.stdout, /unsealed 40-zero commit pin|fail-closed/i);
  const after = await Promise.all([bytes("VERSION"), bytes("research/release-manifest.json"),
    bytes("public/site-version.json"), bytes("public/research-review.html")]);
  assert.deepEqual(after.map(sha256), before.map(sha256));
});

test("prepublication state is still exactly R0.73N", async (t) => {
  const release = await json("research/release-manifest.json");
  if (release.latestCompletedRelease === "r073o") {
    t.skip("R0.73O is already materialized");
    return;
  }
  assert.equal(release.latestCompletedRelease, "r073n");
  for (const relative of ["public/notes/r0-73o.html", "public/notes/r0-73o.pdf",
    "public/recap-r0-61-r0-73o.html", "public/recap-r0-61-r0-73o.pdf",
    "research/r073o_pdf_bindings.json", "scripts/i18n-snapshots/r073o-missing.json",
    "public/assets/r073o/fig-r073o-kolmogorov-spectrum.pdf"])
    assert.equal(await exists(relative), false, relative);
});

test("materialized R0.73O publication has exact accounting and boundaries", async (t) => {
  const release = await json("research/release-manifest.json");
  if (release.latestCompletedRelease !== "r073o") {
    t.skip("R0.73O publication has not been applied");
    return;
  }
  assert.deepEqual({version: release.siteVersion, latest: release.latestCompletedRelease,
    notes: release.publicHtmlNoteCount, recap: release.postR060RecapNodeCount,
    published: release.postR070APublishedReleaseCount,
    sealed: release.postR070AFormalSealedReleaseCount,
    backlog: release.legacyFormalFigureBacklogCount, next: release.nextRelease},
  {version: "1.55", latest: "r073o", notes: 191, recap: 131,
    published: 93, sealed: 69, backlog: 24, next: "r073p"});
  assert.equal(release.latestReleasePublicationTest, "tests/r073o-release.test.mjs");

  const pages = Object.fromEntries(await Promise.all(Object.entries(targetPages)
    .map(async ([key, relative]) => [key, await text(relative)])));
  for (const [label, value] of Object.entries(pages)) {
    assert.ok(value.includes("R0.73O"), label);
    assert.ok(value.includes("/i18n-en.js?v=1.55"), label);
    for (const phrase of forbidden) assert.equal(value.includes(phrase), false, `${label}: ${phrase}`);
  }
  for (const token of ["unforcedGlobalOrbitH3Stability=CLOSED_CONDITIONALLY_ON_GLOBAL_REFERENCE",
    "forcedKolmogorovPlanarH3InputL2Escape=CLOSED_BY_PRIMARY_SOURCE_COMBINATION",
    "finiteComputationProvesPositiveInfiniteDimensionalSpectrum=FALSE",
    "uniformL2OnlyInputThreshold=OPEN", "Clay=OPEN", "NOT CLAY"])
    assert.ok(pages.note.includes(token), `note: ${token}`);
  assert.ok(pages.note.includes("经典路线闭合"));
  assert.ok(pages.note.includes("有限谱计算不证明无限维正实谱"));
  assert.ok(pages.note.includes("/note-retro.css"));
  for (const suffix of ["pdf", "svg", "png"])
    assert.ok(pages.note.includes(`/assets/r073o/fig-r073o-kolmogorov-spectrum.${suffix}`));

  for (const token of ["<strong>131</strong><span>R0.61–R0.73O 研究节点</span>",
    "<strong>93</strong><span>R0.70A–R0.73O 已公开版本</span>",
    "<strong>69</strong><span>当前 formal-figure 合同下完整封存</span>",
    "检查 L2-only / 高频输入接口"])
    assert.ok(pages.recap.includes(token), `recap: ${token}`);
  for (const token of ["Research topology · R0.1–R0.73O", "<strong>v1.55</strong>网页版本",
    "<strong>R0.73O</strong>最新研究节点", "<summary>展开 101 篇公开笔记</summary>",
    "累计回顾收录 131 个节点；全站现有 191 篇公开研究笔记"])
    assert.ok(pages.home.includes(token), `home: ${token}`);
  for (const token of ['<div class="route-step kept"><header><b>R0.73O</b>',
    "开放接口 · R0.73P", 'id="r073o-boundary"',
    "R0.73O 的全局轨道稳定与强迫对照文献边界"])
    assert.ok(pages.literature.includes(token), `literature: ${token}`);
  assert.equal(pages.literature.includes("开放接口 · R0.73O"), false);

  for (const relative of ["public/notes/r0-73o.pdf", "public/recap-r0-61-r0-73o.pdf",
    "research/r073o_pdf_bindings.json", "scripts/i18n-snapshots/r073o-missing.json",
    "figures/r073o/fig-r073o-kolmogorov-spectrum/manifest.json",
    "public/figures/r073o/fig-r073o-kolmogorov-spectrum/manifest.json",
    "public/assets/r073o/fig-r073o-kolmogorov-spectrum.pdf",
    "public/assets/r073o/fig-r073o-kolmogorov-spectrum.svg",
    "public/assets/r073o/fig-r073o-kolmogorov-spectrum.png"])
    assert.equal(await exists(relative), true, relative);
  for (const suffix of ["pdf", "svg", "png"]) {
    const sealed = await bytes(`research/figures/r073o/fig-r073o-kolmogorov-spectrum/figure.${suffix}`);
    const published = await bytes(`public/assets/r073o/fig-r073o-kolmogorov-spectrum.${suffix}`);
    assert.equal(sha256(published), sha256(sealed), `published ${suffix} master`);
  }
  for (const [script, mode] of [["scripts/add-r073o-translations.mjs", "--check-only"],
    ["scripts/bind-r073o-pdfs.mjs", "--check-only"]]) {
    const result = run(process.execPath, [script, mode]);
    assert.equal(result.status, 0, `${script}: ${result.stderr}`);
  }
});
