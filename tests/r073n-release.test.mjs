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
  env: { ...process.env, R073N_RELEASE_ROOT: root },
});

const skeletonFiles = [
  "scripts/r073n_release_content.py",
  "scripts/generate_r073n_release.py",
  "scripts/add-r073n-translations.mjs",
  "scripts/bind-r073n-pdfs.mjs",
  "tests/r073n-release.test.mjs",
];
const canonicalSources = [
  "research/r073n_problem_freeze.md",
  "research/r073n_fixed_background_no_go_proof.md",
  "research/r073n_scaling_obstruction.md",
  "research/r073n_independent_analytic_audit.md",
  "research/r073n_adversarial_audit.md",
  "research/r073n_literature_audit.md",
  "research/r073n_claim_source_ledger.md",
  "research/r073n_gap_matrix.md",
  "research/r073n_finite_diagnostic_audit.md",
  "research/r073n_report-source.md",
  "research/r073n_bilingual_dictionary.md",
];
const targetPages = {
  note: "public/notes/r0-73n.html",
  recap: "public/recap-r0-61-r0-73n.html",
  home: "public/research-review.html",
  literature: "public/literature-review.html",
  index: "public/notes/index.html",
};
const boundaryTokens = [
  "fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED",
  "fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY",
  "fixedMemberPlanarL2SynchronizedStability=CLOSED",
  "fullThreeDimensionalFPSH3L2Stability=OPEN",
  "NOT CLAY",
];
const forbidden = [
  "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  "颠覆性", "世界首个", "接近解决", "解决了千禧年", "证明了全局正则性",
  "原创性定理", "首次证明",
];
const pinNames = [
  "ANALYTIC_SOURCE_COMMIT", "FINITE_PACKAGE_COMMIT", "FIGURE_PACKAGE_COMMIT",
  "RELEASE_BASELINE_COMMIT", "FINAL_CONTENT_COMMIT", "RELEASE_SOURCE_COMMIT",
];

function releasePins(generator) {
  return pinNames.map((name) => {
    const match = generator.match(new RegExp(
      `^${name} = (ZERO_COMMIT|"([0-9a-f]{40})")$`, "m",
    ));
    assert.ok(match, `${name}: missing or malformed pin slot`);
    return { name, zero: match[1] === "ZERO_COMMIT", commit: match[2] ?? null };
  });
}

test("R0.73N release pins admit only skeleton, source-freeze, or fully bound state", async () => {
  for (const relative of skeletonFiles) assert.equal(await exists(relative), true, relative);
  const generator = await text("scripts/generate_r073n_release.py");
  assert.match(generator, /^ZERO_COMMIT = "0" \* 40$/m);
  const pins = releasePins(generator);
  const skeleton = pins.every(({ zero }) => zero);
  const sourceFreeze = pins.slice(0, -1).every(({ zero }) => !zero) && pins.at(-1).zero;
  const fullyBound = pins.every(({ zero }) => !zero);
  assert.ok(skeleton || sourceFreeze || fullyBound,
    "only all-zero, first-five-bound/release-source-zero, or all-bound pins are allowed");
  assert.match(generator, /Binding order \(oldest to newest\)/);
  assert.match(generator, /fullThreeDimensionalFPS_H3_L2/);
  assert.match(generator, /validate_certificate\.py/);
  assert.match(generator, /R073N_CERTIFICATE_DEPS/);
  assert.match(generator, /seal_package\.py/);
  assert.match(generator, /FIGURE_SOURCE_RELATIVE/);
  assert.match(generator, /--verify-only/);
  assert.match(generator, /verify_pinned_paths_exist\(RELEASE_BASELINE_COMMIT/);
  assert.doesNotMatch(generator, /verify_exact_paths\(RELEASE_BASELINE_COMMIT/);
});

test("R0.73N command help is side-effect-free", () => {
  for (const [command, relative] of [
    ["python3", "scripts/r073n_release_content.py"],
    ["python3", "scripts/generate_r073n_release.py"],
    [process.execPath, "scripts/add-r073n-translations.mjs"],
    [process.execPath, "scripts/bind-r073n-pdfs.mjs"],
  ]) {
    const result = run(command, [relative, "--help"]);
    assert.equal(result.status, 0, `${relative}: ${result.stderr}`);
    assert.match(result.stdout, /usage:/i, relative);
  }
});

test("R0.73N check-only is sealed shut before any public baseline read", async (t) => {
  const pins = releasePins(await text("scripts/generate_r073n_release.py"));
  if (pins.every(({ zero }) => !zero)) {
    t.skip("all pins are bound; this skeleton-phase assertion no longer applies");
    return;
  }
  const before = await Promise.all([
    bytes("VERSION"), bytes("research/release-manifest.json"),
    bytes("public/site-version.json"), bytes("public/research-review.html"),
  ]);
  const result = run("python3", ["scripts/generate_r073n_release.py", "--check-only"]);
  assert.notEqual(result.status, 0);
  assert.match(result.stderr + result.stdout, /unsealed 40-zero commit pin|fail-closed/i);
  const after = await Promise.all([
    bytes("VERSION"), bytes("research/release-manifest.json"),
    bytes("public/site-version.json"), bytes("public/research-review.html"),
  ]);
  assert.deepEqual(after.map(sha256), before.map(sha256));
});

test("R0.73N canonical source dry-run writes zero bytes", async (t) => {
  if (!(await Promise.all(canonicalSources.map(exists))).every(Boolean)) {
    t.skip("canonical source set is not complete yet");
    return;
  }
  const watched = [
    "VERSION", "research/release-manifest.json", "public/site-version.json",
    "public/research-review.html", "public/literature-review.html", "public/notes/index.html",
  ];
  const before = await Promise.all(watched.map(bytes));
  const contentCheck = run("python3", ["scripts/r073n_release_content.py", "--check-only"]);
  assert.equal(contentCheck.status, 0, contentCheck.stderr);
  const result = run("python3", ["scripts/generate_r073n_release.py", "--source-dry-run"]);
  assert.equal(result.status, 0, result.stderr);
  const summary = JSON.parse(result.stdout);
  assert.equal(summary.release, "R0.73N");
  assert.equal(summary.fullThreeDimensionalFPS_H3_L2, "OPEN");
  const pins = releasePins(await text("scripts/generate_r073n_release.py"));
  assert.equal(summary.commitPinsReady, pins.every(({ zero }) => !zero));
  assert.equal(summary.writes, 0);
  assert.deepEqual(summary.bindingOrder, [
    "R0.73M release baseline", "analytic source", "finite package",
    "figure package", "final content", "R0.73N release source",
  ]);
  assert.deepEqual(summary.publicationStageOrder, [
    "freeze-r073m-baseline",
    "freeze-analytic-source",
    "seal-finite-package-to-analytic-source",
    "seal-figure-package-to-analytic-source",
    "freeze-final-report-dictionary-and-finite-audit",
    "freeze-release-source-and-fill-normalized-pin-slot",
    "apply-html-manifest-and-figure-transaction",
    "capture-review-and-apply-translations",
    "render-synchronized-note-and-recap-pdfs",
    "bind-html-pdf-hashes-and-titles",
    "run-publication-tests-then-deploy",
  ]);
  const after = await Promise.all(watched.map(bytes));
  assert.deepEqual(after.map(sha256), before.map(sha256));
});

test("prepublication state contains no materialized R0.73N release artifacts", async (t) => {
  const release = await json("research/release-manifest.json");
  if (release.latestCompletedRelease === "r073n") {
    t.skip("R0.73N is already materialized; the conditional publication test applies");
    return;
  }
  assert.equal(release.latestCompletedRelease, "r073m");
  for (const relative of [
    "public/notes/r0-73n.html", "public/notes/r0-73n.pdf",
    "public/recap-r0-61-r0-73n.html", "public/recap-r0-61-r0-73n.pdf",
    "research/r073n_pdf_bindings.json", "scripts/i18n-snapshots/r073n-missing.json",
    "public/assets/r073n/fig-r073n-finite-strain-bracket.pdf",
  ]) assert.equal(await exists(relative), false, relative);
});

test("materialized R0.73N publication is exact when the manifest advances", async (t) => {
  const release = await json("research/release-manifest.json");
  if (release.latestCompletedRelease !== "r073n") {
    t.skip("R0.73N publication has not been applied");
    return;
  }
  assert.deepEqual({
    version: release.siteVersion,
    latest: release.latestCompletedRelease,
    notes: release.publicHtmlNoteCount,
    recap: release.postR060RecapNodeCount,
    published: release.postR070APublishedReleaseCount,
    sealed: release.postR070AFormalSealedReleaseCount,
    backlog: release.legacyFormalFigureBacklogCount,
    next: release.nextRelease,
  }, {
    version: "1.54", latest: "r073n", notes: 190, recap: 130,
    published: 92, sealed: 68, backlog: 24, next: "r073o",
  });
  assert.equal(release.latestReleaseGate, "tests/r073n-fixed-background-no-go-gate.test.mjs");
  assert.equal(release.latestReleasePublicationTest, "tests/r073n-release.test.mjs");

  const pages = Object.fromEntries(
    await Promise.all(Object.entries(targetPages).map(async ([key, relative]) => [key, await text(relative)])),
  );
  for (const [label, value] of Object.entries(pages)) {
    assert.ok(value.includes("R0.73N"), label);
    assert.ok(value.includes("/i18n-en.js?v=1.54"), label);
    for (const phrase of forbidden) assert.equal(value.includes(phrase), false, `${label}: ${phrase}`);
  }
  for (const token of boundaryTokens) assert.ok(pages.note.includes(token), token);
  assert.ok(pages.note.includes(
    "full-three-dimensional forward synchronized \\((H^3,H^3)\\)",
  ));
  assert.ok(pages.note.includes("full-three-dimensional FPS \\((H^3,L^2)\\)"));
  assert.ok(pages.note.includes("bounded"));
  assert.ok(pages.note.includes("priority"));
  assert.ok(pages.note.includes("/note-retro.css"));
  assert.equal((pages.note.match(/<table class="report-table">/g) ?? []).length, 3);
  assert.equal((pages.note.match(/<blockquote>/g) ?? []).length, 3);
  assert.ok(pages.note.includes('<ol class="report-list report-list-ordered">'));
  assert.ok(pages.note.includes("<h3>Lead</h3>"));
  assert.ok(pages.note.includes("<strong>OPEN</strong>"));
  assert.ok(pages.note.includes("<code>NOT CLAY</code>"));
  assert.ok(pages.note.includes('href="/recap-r0-61-r0-73n.pdf"'));
  assert.equal(pages.note.includes('class="source-table"'), false);
  assert.equal(pages.note.includes("&gt; The amplification"), false);
  for (const suffix of ["pdf", "svg", "png"]) {
    assert.ok(pages.note.includes(
      `/assets/r073n/fig-r073n-finite-strain-bracket.${suffix}`,
    ));
  }
  assert.match(await text("public/note-retro.css"), /prefers-color-scheme\s*:\s*dark/);

  for (const token of [
    "<strong>130</strong><span>R0.61–R0.73N 研究节点</span>",
    "<strong>92</strong><span>R0.70A–R0.73N 已公开版本</span>",
    "<strong>68</strong><span>当前 formal-figure 合同下完整封存</span>",
    "R0.73O：冻结结构不同的固定背景候选问题",
    "变背景族与固定成员的量词边界已经分开",
  ]) assert.ok(pages.recap.includes(token), `recap: ${token}`);
  for (const stale of ["<strong>129</strong>", "<strong>91</strong>", "<strong>67</strong>"]) {
    assert.equal(pages.recap.includes(stale), false, `recap stale metric: ${stale}`);
  }
  for (const token of [
    "Research topology · R0.1–R0.73N",
    "<strong>v1.54</strong>网页版本",
    "<strong>R0.73N</strong>最新研究节点",
    'href="#r073n">跳到首页 R0.73N 卡片 →',
    '<span class="route-range">R0.69P–R0.73N</span>',
    "<summary>展开 100 篇公开笔记</summary>",
    'href="/notes/r0-73n.html">R0.73N</a>',
    "累计回顾收录 130 个节点；全站现有 190 篇公开研究笔记",
  ]) assert.ok(pages.home.includes(token), `home: ${token}`);
  assert.equal(pages.home.includes("Research topology · R0.1–R0.73M"), false);
  assert.equal(pages.home.includes("累计回顾收录 129 个节点；全站现有 189 篇公开研究笔记"), false);
  assert.equal(pages.home.includes("<strong>v1.53</strong>网页版本"), false);
  assert.equal(pages.home.includes("<strong>R0.73M</strong>最新研究节点"), false);
  assert.equal(pages.home.includes("/recap-r0-61-r0-73m.html"), false);
  assert.equal(pages.home.includes("/recap-r0-61-r0-73m.pdf"), false);
  assert.ok(pages.home.includes("综述 v1.54 ·"));
  for (const token of [
    '<div class="route-step kept"><header><b>R0.73N</b>',
    "开放接口 · R0.73O",
    'id="r073n-boundary"',
    "R0.73N 的主张边界",
  ]) assert.ok(pages.literature.includes(token), `literature: ${token}`);
  assert.equal(pages.literature.includes("开放接口 · R0.73N"), false);
  assert.ok(pages.literature.includes("文献综述 v1.54 ·"));

  for (const relative of [
    "public/notes/r0-73n.pdf", "public/recap-r0-61-r0-73n.pdf",
    "research/r073n_pdf_bindings.json", "scripts/i18n-snapshots/r073n-missing.json",
    "figures/r073n/fig-r073n-finite-strain-bracket/manifest.json",
    "public/figures/r073n/fig-r073n-finite-strain-bracket/manifest.json",
    "public/assets/r073n/fig-r073n-finite-strain-bracket.pdf",
    "public/assets/r073n/fig-r073n-finite-strain-bracket.svg",
    "public/assets/r073n/fig-r073n-finite-strain-bracket.png",
  ]) assert.equal(await exists(relative), true, relative);

  const formalFigure = await json(
    "figures/r073n/fig-r073n-finite-strain-bracket/manifest.json",
  );
  assert.equal(formalFigure.status, "formal");
  assert.equal(formalFigure.publicationStatus, "published");
  assert.equal(formalFigure.publication.publicCopiesComplete, true);
  assert.equal(formalFigure.publication.assets.length, 3);
  for (const name of formalFigure.packageInventory.paths) {
    const archived = await bytes(`figures/r073n/fig-r073n-finite-strain-bracket/${name}`);
    const published = await bytes(`public/figures/r073n/fig-r073n-finite-strain-bracket/${name}`);
    assert.equal(sha256(archived), sha256(published), `formal figure archive ${name}`);
  }

  for (const suffix of ["pdf", "svg", "png"]) {
    const sealed = await bytes(
      `research/figures/r073n/fig-r073n-finite-strain-bracket/figure.${suffix}`,
    );
    const published = await bytes(
      `public/assets/r073n/fig-r073n-finite-strain-bracket.${suffix}`,
    );
    assert.equal(sha256(published), sha256(sealed), `published ${suffix} master`);
  }

  for (const [script, mode] of [
    ["scripts/add-r073n-translations.mjs", "--check-only"],
    ["scripts/bind-r073n-pdfs.mjs", "--check-only"],
  ]) {
    const result = run(process.execPath, [script, mode]);
    assert.equal(result.status, 0, `${script}: ${result.stderr}`);
  }
});
