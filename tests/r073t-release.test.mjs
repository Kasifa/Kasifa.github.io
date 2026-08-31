import assert from "node:assert/strict";
import {
  mkdirSync,
  mkdtempSync,
  readFileSync,
  realpathSync,
  renameSync,
  rmSync,
  symlinkSync,
  unlinkSync,
  writeFileSync,
} from "node:fs";
import { tmpdir } from "node:os";
import { dirname, join, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");

function runPython(...argumentsList) {
  return spawnSync("python3", ["-B", ...argumentsList], {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
  });
}
function pythonJson(...argumentsList) {
  const result = runPython(...argumentsList);
  assert.equal(result.status, 0, result.stderr || result.stdout);
  return JSON.parse(result.stdout);
}
function pythonCodeJson(source) {
  return pythonJson("-c", source);
}
function runNode(...argumentsList) {
  return spawnSync(process.execPath, argumentsList, { cwd: root, encoding: "utf8" });
}

const activeTranslationPages = [
  "literature-review.html",
  "notes/index.html",
  "notes/r0-73t.html",
  "recap-r0-61-r0-73t.html",
  "research-review.html",
];

function createTranslationFixture() {
  const fixture = mkdtempSync(join(tmpdir(), "r073t-translation-test-"));
  for (const directory of [
    "public/notes", "research", "translations", "scripts/i18n-snapshots",
  ]) mkdirSync(resolve(fixture, directory), { recursive: true });
  const html = '<script src="/i18n-en.js?v=1.60"></script>' +
    "<p>R0.73T</p><p>新条目</p><p>保留条目</p>";
  for (const relative of activeTranslationPages) {
    writeFileSync(resolve(fixture, "public", relative), html);
  }
  writeFileSync(resolve(fixture, "public/notes/r0-1.html"), [
    "<p>R0.1 历史缺失英文</p>",
    "<p>顺序等价：alphaState=OPEN；betaState=CLOSED；R0.1；R0.2</p>",
    "<p>机器账本 legacyMachineState=OPEN</p>",
    "<p>样本总数 1,792</p>",
    "<p>八十度方向</p>",
    "<p>数量 1</p>",
    "<p>第 21 项</p>",
    "<p>阈值 74.95</p>",
    "<p>温度 0°C</p>",
    "<p>每个分子都是次数 8 的有理多项式；区间不包含零，所以导数符号是严格结论。</p>",
    "<p>所以 \\(D_0\\) 严格凸，并在 \\(\\alpha\\) 取得唯一零点。 对横向多项式 \\(J\\)，把局部长方体映到单位立方体。 它的次数为 \\((5,5,3)\\)，在 \\(\\lambda_*\\) 的两个有理隔离端点共检查 288 个 Bernstein 系数，得到</p>",
    "<p>02 · 二阶上界</p>",
    "<p>20 万对精确实现回归</p>",
    "<p>数量 64、22、39</p>",
    "<p>误差 −167.102</p>",
    "<p>四个次数 8 的导数分子</p>",
    "<p>前 10 个二进制层级</p>",
    "<p>5 阶与 4 阶</p>",
  ].join(""));
  writeFileSync(resolve(fixture, "public/i18n-en.js"), "");
  writeFileSync(resolve(fixture, "public/site-version.json"), JSON.stringify({
    latestRelease: "R0.73T", version: "1.60", publicHtmlNoteCount: 196,
  }));
  writeFileSync(resolve(fixture, "research/release-manifest.json"), JSON.stringify({
    latestCompletedRelease: "r073t", siteVersion: "1.60", publicHtmlNoteCount: 196,
    postR060RecapNodeCount: 136, nextRelease: "r073u",
    postR070APublishedReleaseCount: 98, postR070AFormalSealedReleaseCount: 74,
    legacyFormalFigureBacklogCount: 24,
  }));
  const dictionaryTokens = [
    "sourceCommitAssigned=TRUE", "generatedArtifactCommitAssigned=TRUE",
    "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX", "translationPath=LOCAL_DIRECT_NO_DGX",
    "dgxUsed=FALSE", "externalTranslationServiceUsed=FALSE",
    "dynamicAQUpperInequality=INTERNAL_COROLLARY", "carrierScaleNonAutonomy=CLOSED_EXACT",
    "signPairTensorAndPressureIdentical=CLOSED_EXACT",
    "signedVelocityPhaseInPressurePairingNonIdentifiability=CLOSED_EXACT",
    "pressureReconstructionRequiresTensor=VERIFIED_CLASSICAL",
    "finiteFormulaCertificateOnly=TRUE", "finiteFormulaDiagnosticValidation=PASS",
    "finiteFormulaDiagnosticChecks=55", "formalFigurePackage=PASS", "formalFigureChecks=106",
    "formalFigureRows=28", "finalSeal=TRUE", "navierStokesSimulation=NOT_RUN",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN", "clayConclusion=OPEN",
    "noveltyOrPriorityClaim=FORBIDDEN",
  ];
  writeFileSync(resolve(fixture, "research/r073t_bilingual_dictionary.md"), [
    "# fixture", "", "**Release title:** R0.73T | Dynamic autocorrelation and the pressure-tensor barrier",
    "", "**Public title (zh):** R0.73T｜自相关进入动力学：一个临界一侧估计与压力张量障碍",
    "", "**Next release:** R0.73U", "", ...dictionaryTokens,
  ].join("\n"));
  writeFileSync(resolve(fixture, "research/r073t_report-source.md"), [
    "exactAutocorrelationEvolution=VERIFIED_CLASSICAL_RECONSTRUCTION",
    "dynamicAQUpperInequality=INTERNAL_COROLLARY", "criticalAIntegralControl=OPEN",
    "carrierScaleNonAutonomy=CLOSED_EXACT",
    "signedVelocityPhaseInPressurePairing=CLOSED_EXACT",
    "pressureTensorNeededForGeneralReconstruction=VERIFIED_CLASSICAL",
    "finiteFormulaDiagnosticChecks=55", "formalFigureChecks=106",
    "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX", "dgxUsed=FALSE",
    "arbitraryThreeDimensionalGlobalRegularity=OPEN", "clayConclusion=OPEN",
  ].join("\n"));
  writeFileSync(resolve(fixture, "translations/en.json"), JSON.stringify([
    { id: "old001", zh: "保留条目", count: 99, files: ["stale.html"], en: "Retained entry" },
    { id: "stale001", zh: "失活条目", count: 1, files: ["stale.html"], en: "Stale entry" },
    { id: "legacyMissing", zh: "R0.1 历史缺失英文", count: 1,
      files: ["notes/r0-1.html"], en: "" },
    { id: "legacyOrder", zh: "顺序等价：alphaState=OPEN；betaState=CLOSED；R0.1；R0.2",
      count: 1, files: ["notes/r0-1.html"],
      en: "Order-equivalent: betaState=CLOSED; alphaState=OPEN; R0.2; R0.1" },
    { id: "legacyMachine", zh: "机器账本 legacyMachineState=OPEN", count: 1,
      files: ["notes/r0-1.html"], en: "Machine ledger legacyMachineState=CLOSED" },
    { id: "legacyThousands", zh: "样本总数 1,792", count: 1,
      files: ["notes/r0-1.html"], en: "Sample total: 1792" },
    { id: "legacyDegree", zh: "八十度方向", count: 1,
      files: ["notes/r0-1.html"], en: "degree-80 direction" },
    { id: "legacyOne", zh: "数量 1", count: 1,
      files: ["notes/r0-1.html"], en: "Quantity one" },
    { id: "legacyOrdinal", zh: "第 21 项", count: 1,
      files: ["notes/r0-1.html"], en: "21st item" },
    { id: "legacyDecimal", zh: "阈值 74.95", count: 1,
      files: ["notes/r0-1.html"], en: "Threshold 7.495" },
    { id: "legacyTemperature", zh: "温度 0°C", count: 1,
      files: ["notes/r0-1.html"], en: "Temperature 32°F" },
    { id: "s1812", zh: "每个分子都是次数 8 的有理多项式；区间不包含零，所以导数符号是严格结论。",
      count: 1, files: ["notes/r0-1.html"],
      en: "Each molecule is an eighth-degree rational polynomial; the interval does not contain zero, so the sign of the derivative is a strict conclusion." },
    { id: "s1824", zh: "所以 \\(D_0\\) 严格凸，并在 \\(\\alpha\\) 取得唯一零点。 对横向多项式 \\(J\\)，把局部长方体映到单位立方体。 它的次数为 \\((5,5,3)\\)，在 \\(\\lambda_*\\) 的两个有理隔离端点共检查 288 个 Bernstein 系数，得到",
      count: 1, files: ["notes/r0-1.html"],
      en: "So \\(D_0\\) is strictly convex and attains a unique zero at \\(\\alpha\\). For the transverse polynomial \\(J\\), map the local rectangular box to the unit cube. Its degree is \\((5,5,3)\\), and it checks 288 rational isolated endpoints of 288 Bernstein coefficients at \\(\\lambda_*\\), obtaining" },
    { id: "s2429", zh: "02 · 二阶上界", count: 1,
      files: ["notes/r0-1.html"], en: "· second-order upper bound" },
    { id: "s5412", zh: "20 万对精确实现回归", count: 1,
      files: ["notes/r0-1.html"], en: "Exact Implementation Regression on 200,000 Pairs" },
    { id: "legacyCompound", zh: "数量 64、22、39", count: 1,
      files: ["notes/r0-1.html"],
      en: "Quantity sixty-four, twenty-two, and thirty-nine" },
    { id: "legacyUnicodeMinus", zh: "误差 −167.102", count: 1,
      files: ["notes/r0-1.html"], en: "Error -167.102" },
    { id: "legacyAdjacentOrdinals", zh: "四个次数 8 的导数分子", count: 1,
      files: ["notes/r0-1.html"], en: "four eighth-degree derivative numerators" },
    { id: "legacyFirstTen", zh: "前 10 个二进制层级", count: 1,
      files: ["notes/r0-1.html"], en: "through the first ten dyadic levels" },
    { id: "legacyNumberList", zh: "5 阶与 4 阶", count: 1,
      files: ["notes/r0-1.html"], en: "orders five and four" },
  ], null, 2) + "\n");
  return fixture;
}

function runTranslation(fixture, action) {
  return spawnSync(process.execPath, ["scripts/add-r073t-translations.mjs", action], {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, R073T_RELEASE_ROOT: fixture },
  });
}

test("release content exposes the frozen eight-section R0.73T boundary without writing", () => {
  const result = pythonJson("scripts/r073t_release_content.py", "--check-only");
  assert.equal(result.release, "R0.73T");
  assert.equal(result.title, "R0.73T | Dynamic autocorrelation and the pressure-tensor barrier");
  assert.equal(result.publicTitleZh,
    "R0.73T｜自相关进入动力学：一个临界一侧估计与压力张量障碍");
  assert.equal(result.canonicalSources, 12);
  assert.equal(result.canonicalSourcesPlanned, 12);
  assert.equal(result.sections, 8);
  assert.equal(result.exactAutocorrelationEvolution, "VERIFIED_CLASSICAL_RECONSTRUCTION");
  assert.equal(result.dynamicAQUpperInequality, "INTERNAL_COROLLARY");
  assert.equal(result.criticalAIntegralControl, "OPEN");
  assert.equal(result.carrierScaleNonAutonomy, "CLOSED_EXACT");
  assert.equal(result.signedVelocityPhaseInPressurePairing, "CLOSED_EXACT");
  assert.equal(result.pressureTensorNeededForGeneralReconstruction, "VERIFIED_CLASSICAL");
  assert.equal(result.arbitraryThreeDimensionalGlobalRegularity, "OPEN");
  assert.equal(result.clayConclusion, "OPEN");
  assert.equal(result.translationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(result.publicationReady, true);
  assert.deepEqual(result.readinessFailures, []);
  assert.equal(result.writes, 0);
});

test("canonical text rejects U+0008 instead of silently repairing frozen sources", () => {
  const result = pythonCodeJson(`
import json, sys, tempfile
from pathlib import Path
sys.path.insert(0, "scripts")
import r073t_release_content as c
with tempfile.TemporaryDirectory() as directory:
    root = Path(directory)
    (root / "bad.md").write_bytes(b"alpha\\x08beta")
    rejected = False
    try:
        c._regular_text(root, "bad.md")
    except c.CanonicalSourceError:
        rejected = True
    print(json.dumps({"rejected": rejected}))
`);
  assert.equal(result.rejected, true);
});

test("source-dry-run exposes the exact accounting and non-writing publication plan", () => {
  const result = pythonJson("scripts/generate_r073t_release.py", "--source-dry-run");
  assert.equal(result.release, "R0.73T");
  assert.equal(result.siteVersion, "1.60");
  assert.deepEqual(result.targetAccounting, {
    latestCompletedRelease: "r073t", siteVersion: "1.60", publicHtmlNoteCount: 196,
    postR060RecapNodeCount: 136, nextRelease: "r073u",
    postR070APublishedReleaseCount: 98, postR070AFormalSealedReleaseCount: 74,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.deepEqual(result.baselineAccounting, {
    latestCompletedRelease: "r073s", siteVersion: "1.59", publicHtmlNoteCount: 195,
    postR060RecapNodeCount: 135, nextRelease: "r073t",
    postR070APublishedReleaseCount: 97, postR070AFormalSealedReleaseCount: 73,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.equal(result.canonicalSources, 12);
  assert.equal(result.certificate.present, true);
  assert.equal(result.figure.present, true);
  assert.equal(result.figure.formal, true);
  assert.equal(result.figure.figureId, "fig-r073t-dynamic-autocorrelation");
  assert.equal(result.releaseSourceReady, true);
  assert.equal(typeof result.commitPinsReady, "boolean");
  assert.equal(result.publicTransactionImplemented, true);
  assert.equal(result.translationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(result.clayConclusion, "OPEN");
  assert.ok(result.coreOutputsPlanned.includes("public/notes/r0-73t.html"));
  assert.ok(result.coreOutputsPlanned.includes("public/recap-r0-61-r0-73t.html"));
  assert.ok(result.laterStageOutputsPlanned.includes("research/r073t_pdf_bindings.json"));
  assert.ok(result.figureOutputsPlanned.includes(
    "public/assets/r073t/fig-r073t-dynamic-autocorrelation.pdf"));
  assert.equal(result.writes, 0);
});

test("the generator pins reviewed layers and permits the normalized zero-to-full self-pin lifecycle", () => {
  const generator = read("scripts/generate_r073t_release.py");
  assert.match(generator, /RELEASE_BASELINE_COMMIT = "4323440923238d1ab04496f892ab9809b2d57532"/);
  assert.match(generator, /ANALYTIC_SOURCE_COMMIT = "05c55d21f060a17a0a4db04c12e89e7271b03d30"/);
  assert.match(generator, /FINITE_PACKAGE_COMMIT = "29d01625731d1c611f927c2852dbddf05967c6cb"/);
  assert.match(generator, /FIGURE_PACKAGE_COMMIT = "b17c45013cc9a3f6f09efa146bcbc2ef8ab043f9"/);
  assert.match(generator, /FINAL_CONTENT_COMMIT = "[0-9a-f]{40}"/);
  assert.match(generator, /RELEASE_SOURCE_COMMIT = (?:ZERO_COMMIT|"[0-9a-f]{40}")/);
  assert.ok(generator.includes("__NORMALIZED_RELEASE_SOURCE_COMMIT__"));
  assert.match(generator, /PUBLIC_TRANSACTION_IMPLEMENTED = True/);
  for (const relative of [
    "research/r073t_claim_source_ledger.md", "research/r073t_evidence_gap_matrix.md",
    "research/r073t_finite_diagnostic_audit.md", "scripts/add-r073t-translations.mjs",
    "scripts/bind-r073t-pdfs.mjs", "tests/r073t-dynamic-autocorrelation-gate.test.mjs",
    "tests/r073t-release.test.mjs",
  ]) assert.ok(generator.includes(`"${relative}"`), relative);
});

test("the public transaction assembles the required targets in memory without applying", () => {
  const result = pythonCodeJson([
    "import json,sys", "sys.path.insert(0,'scripts')", "import generate_r073t_release as g",
    "s=g.build_staged(g.load_release_content(g.ROOT))", "rel=lambda p:p.relative_to(g.ROOT).as_posix()",
    "f=json.loads(s[g.ROOT/g.FIGURE_ARCHIVE_RELATIVE/'manifest.json'])",
    "lit=s[g.PUBLIC/'literature-review.html'].decode()",
    "tblock=lit.split('<h3 id=\"r073t-boundary\"',1)[1].split('<ol class=\"criteria\">',1)[0]",
    "print(json.dumps({'core':all(g.ROOT/p in s for p in g.CORE_TARGET_OUTPUTS),'html':sum(p.suffix=='.html' for p in s),'note':'R0.73T｜自相关进入动力学' in s[g.PUBLIC/'notes/r0-73t.html'].decode(),'recap':'136' in s[g.PUBLIC/'recap-r0-61-r0-73t.html'].decode(),'home':'R0.73U' in s[g.PUBLIC/'research-review.html'].decode(),'literature':'dynamic AQ inequality' in lit,'literatureFiniteBoundary':'有限包只复算公式诊断，不认证连续 PDE' in tblock,'staleFiniteSufficiency':'有限充分证书' in tblock,'figureId':f.get('figureId'),'checks':f.get('sourceSeal',{}).get('validationCheckCount'),'paths':sorted(rel(p) for p in s)}))",
  ].join(";"));
  assert.equal(result.core, true);
  assert.equal(result.html, 5);
  assert.equal(result.note, true);
  assert.equal(result.recap, true);
  assert.equal(result.home, true);
  assert.equal(result.literature, true);
  assert.equal(result.literatureFiniteBoundary, true);
  assert.equal(result.staleFiniteSufficiency, false);
  assert.equal(result.figureId, "fig-r073t-dynamic-autocorrelation");
  assert.equal(result.checks, 106);
  assert.ok(result.paths.includes("public/assets/r073t/fig-r073t-dynamic-autocorrelation.pdf"));
  assert.ok(result.paths.includes(
    "public/figures/r073t/fig-r073t-dynamic-autocorrelation/manifest.json"));
});

test("the formal archive carries log-bound and transparently backfilled runtime metadata", () => {
  const result = pythonCodeJson([
    "import json,sys", "sys.path.insert(0,'scripts')", "import generate_r073t_release as g",
    "s=g.build_staged(g.load_release_content(g.ROOT))",
    "f=json.loads(s[g.ROOT/g.FIGURE_ARCHIVE_RELATIVE/'manifest.json'])",
    "print(json.dumps({'wallTime':f['computation'].get('scientificWallTimeSeconds'),'runtimeProvenance':f['computation'].get('runtimeMetadataProvenance'),'operatingSystem':f['compute'].get('operatingSystem'),'cpu':f['compute'].get('cpu'),'memoryGiB':f['compute'].get('memoryGiB'),'metadataProvenance':f['compute'].get('metadataProvenance'),'figureMetadataResealCommit':f['git'].get('figureMetadataResealCommit')}))",
  ].join(";"));
  assert.equal(result.wallTime, 0.7639225840102881);
  assert.equal(result.runtimeProvenance.captureMode, "same-host-bracketed-backfill");
  assert.equal(result.runtimeProvenance.notOriginalRunEmission, true);
  assert.deepEqual(result.runtimeProvenance.wallTimeCrossCheckedAgainst,
    ["progress.ndjson", "resource-log.ndjson"]);
  assert.equal(result.operatingSystem, "macOS-26.6.2-arm64-arm-64bit");
  assert.equal(result.cpu, "arm64 / 18 logical CPUs");
  assert.equal(result.memoryGiB, 36);
  assert.equal(result.metadataProvenance, "same-host-bracketed-backfill");
  assert.equal(result.figureMetadataResealCommit,
    "b17c45013cc9a3f6f09efa146bcbc2ef8ab043f9");
});

test("the HTML transaction rejects symlinked and dangling ancestor directories", () => {
  const result = pythonCodeJson(`
import json, sys, tempfile
from pathlib import Path
sys.path.insert(0, "scripts")
import generate_r073t_release as g
with tempfile.TemporaryDirectory() as directory:
    sandbox = Path(directory)
    root = sandbox / "root"
    outside = sandbox / "outside"
    root.mkdir()
    outside.mkdir()
    (root / "linked").symlink_to(outside, target_is_directory=True)
    (root / "dangling").symlink_to(sandbox / "missing", target_is_directory=True)
    g.ROOT = root
    outcomes = []
    for target in (root / "linked" / "escape.txt", root / "dangling" / "escape.txt"):
        try:
            g.commit_transaction({target: b"blocked"})
        except RuntimeError:
            outcomes.append(True)
        else:
            outcomes.append(False)
    print(json.dumps({"outcomes": outcomes, "outsideUntouched": not (outside / "escape.txt").exists()}))
`);
  assert.deepEqual(result.outcomes, [true, true]);
  assert.equal(result.outsideUntouched, true);
});

test("translation apply rebuilds the ledger from live source and revalidates retained English", () => {
  const fixture = createTranslationFixture();
  try {
    const captured = runTranslation(fixture, "--capture-missing");
    assert.equal(captured.status, 0, captured.stderr || captured.stdout);
    const captureResult = JSON.parse(captured.stdout);
    assert.equal(captureResult.newRowsRequiringEnglish, 1);
    assert.equal(captureResult.legacyRowsRequiringRepair, 8);
    assert.equal(captureResult.forcedSemanticReviewCount, 3);
    const snapshotPath = resolve(fixture, "scripts/i18n-snapshots/r073t-missing.json");
    const snapshot = JSON.parse(readFileSync(snapshotPath, "utf8"));
    assert.deepEqual(new Set(snapshot.map(({ zh }) => zh)), new Set([
      "新条目", "R0.1 历史缺失英文", "机器账本 legacyMachineState=OPEN",
      "阈值 74.95", "温度 0°C", "20 万对精确实现回归",
      "每个分子都是次数 8 的有理多项式；区间不包含零，所以导数符号是严格结论。",
      "所以 \\(D_0\\) 严格凸，并在 \\(\\alpha\\) 取得唯一零点。 对横向多项式 \\(J\\)，把局部长方体映到单位立方体。 它的次数为 \\((5,5,3)\\)，在 \\(\\lambda_*\\) 的两个有理隔离端点共检查 288 个 Bernstein 系数，得到",
      "02 · 二阶上界",
    ]));
    assert.equal(snapshot.some(({ zh }) => zh.startsWith("顺序等价")), false,
      "token-order-only differences must not enter the repair batch");
    assert.equal(snapshot.some(({ zh }) => zh === "样本总数 1,792"), false,
      "thousands separators must normalize before comparison");
    assert.equal(snapshot.some(({ zh }) => zh === "八十度方向"), false,
      "English extra digits from Chinese number words must be allowed");
    assert.equal(snapshot.some(({ zh }) => zh === "数量 1"), false,
      "small required Arabic integers may be represented by English number words");
    assert.equal(snapshot.some(({ zh }) => zh === "第 21 项"), false,
      "English ordinal suffixes must preserve the source integer");
    assert.equal(snapshot.some(({ zh }) => zh === "数量 64、22、39"), false,
      "compound English number words must normalize to single integers");
    assert.equal(snapshot.some(({ zh }) => zh === "误差 −167.102"), false,
      "Unicode minus and ASCII minus must normalize identically");
    for (const zh of ["四个次数 8 的导数分子", "前 10 个二进制层级", "5 阶与 4 阶"]) {
      assert.equal(snapshot.some((entry) => entry.zh === zh), false,
        "adjacent independent number words must remain separate: " + zh);
    }
    for (const id of ["s1812", "s1824", "s2429"]) {
      const row = snapshot.find(({ sourceIdAtCapture }) => sourceIdAtCapture === id);
      assert.ok(row, `${id} must be forced into the review batch`);
      assert.ok(row.reasonCodes.includes("HUMAN_SEMANTIC_REVIEW"));
      assert.equal(row.resolution, "translation-corrected");
      assert.match(row.capturedEnglishSha256, /^[0-9a-f]{64}$/);
    }
    snapshot.find(({ zh }) => zh === "新条目").en = "New entry";
    snapshot.find(({ zh }) => zh === "R0.1 历史缺失英文").en =
      "R0.1 historical missing English";
    const machineReview = snapshot.find(({ zh }) => zh === "机器账本 legacyMachineState=OPEN");
    machineReview.resolution = "semantic-equivalent-approved";
    machineReview.reviewNote = "This intentionally invalid note cannot waive a machine-token change.";
    snapshot.find(({ zh }) => zh === "阈值 74.95").en = "Threshold 74.95";
    const temperatureReview = snapshot.find(({ zh }) => zh === "温度 0°C");
    temperatureReview.resolution = "semantic-equivalent-approved";
    temperatureReview.reviewNote = "0 degrees Celsius is exactly 32 degrees Fahrenheit.";
    const whitelistedReview = snapshot.find(({ sourceIdAtCapture }) => sourceIdAtCapture === "s5412");
    whitelistedReview.resolution = "semantic-equivalent-approved";
    whitelistedReview.reviewNote = "Chinese 20 wan pairs equals 200,000 pairs.";
    const forcedMolecule = snapshot.find(({ sourceIdAtCapture }) => sourceIdAtCapture === "s1812");
    const capturedMoleculeEnglish = forcedMolecule.en;
    const correctedMoleculeEnglish =
      "Each numerator is a rational polynomial of degree 8; the interval excludes zero, so the derivative sign follows rigorously.";
    forcedMolecule.en = correctedMoleculeEnglish;
    snapshot.find(({ sourceIdAtCapture }) => sourceIdAtCapture === "s1824").en =
      "So \\(D_0\\) is strictly convex and attains its unique zero at \\(\\alpha\\). For the transverse polynomial \\(J\\), map the local rectangular box to the unit cube. Its degree is \\((5,5,3)\\); at each of the two rational isolating endpoints for \\(\\lambda_*\\), all 288 Bernstein coefficients are checked, yielding";
    snapshot.find(({ sourceIdAtCapture }) => sourceIdAtCapture === "s2429").en =
      "02 · second-order upper bound";
    writeFileSync(snapshotPath, JSON.stringify(snapshot, null, 2) + "\n");

    const machineWaiverRejected = runTranslation(fixture, "--apply");
    assert.notEqual(machineWaiverRejected.status, 0);
    assert.match(machineWaiverRejected.stderr, /semantic approval cannot waive/);
    machineReview.en = "Machine ledger legacyMachineState=OPEN";
    machineReview.resolution = "translation-corrected";
    machineReview.reviewNote = "";
    writeFileSync(snapshotPath, JSON.stringify(snapshot, null, 2) + "\n");

    const genericNumericWaiverRejected = runTranslation(fixture, "--apply");
    assert.notEqual(genericNumericWaiverRejected.status, 0);
    assert.match(genericNumericWaiverRejected.stderr, /absent from the frozen whitelist/);
    temperatureReview.en = "Temperature 0°C";
    temperatureReview.resolution = "translation-corrected";
    temperatureReview.reviewNote = "";

    forcedMolecule.resolution = "semantic-equivalent-approved";
    forcedMolecule.reviewNote = "The old wording is not acceptable as a semantic approval.";
    writeFileSync(snapshotPath, JSON.stringify(snapshot, null, 2) + "\n");
    const forcedWaiverRejected = runTranslation(fixture, "--apply");
    assert.notEqual(forcedWaiverRejected.status, 0);
    assert.match(forcedWaiverRejected.stderr, /requires translation-corrected and cannot be approved/);

    forcedMolecule.resolution = "translation-corrected";
    forcedMolecule.reviewNote = "";
    forcedMolecule.en = capturedMoleculeEnglish;
    writeFileSync(snapshotPath, JSON.stringify(snapshot, null, 2) + "\n");
    const forcedUnchangedRejected = runTranslation(fixture, "--apply");
    assert.notEqual(forcedUnchangedRejected.status, 0);
    assert.match(forcedUnchangedRejected.stderr, /requires English changed from capture/);

    forcedMolecule.en = correctedMoleculeEnglish;
    writeFileSync(snapshotPath, JSON.stringify(snapshot, null, 2) + "\n");

    const applied = runTranslation(fixture, "--apply");
    assert.equal(applied.status, 0, applied.stderr || applied.stdout);
    const result = JSON.parse(applied.stdout);
    assert.equal(result.added, 1);
    assert.equal(result.removedStale, 1);
    assert.equal(result.legacyRowsRequiringRepair, 8);
    assert.equal(result.forcedSemanticReviewCount, 3);
    assert.equal(result.semanticEquivalentApprovals, 1);
    assert.equal(result.total, 20);
    assert.equal(result.liveStrings, 20);

    const entries = JSON.parse(readFileSync(resolve(fixture, "translations/en.json"), "utf8"));
    assert.equal(entries.length, 20);
    const retained = entries.find(({ zh }) => zh === "保留条目");
    const added = entries.find(({ zh }) => zh === "新条目");
    const repairedMissing = entries.find(({ zh }) => zh === "R0.1 历史缺失英文");
    const repairedMachine = entries.find(({ zh }) => zh === "机器账本 legacyMachineState=OPEN");
    const repairedDecimal = entries.find(({ zh }) => zh === "阈值 74.95");
    const correctedTemperature = entries.find(({ zh }) => zh === "温度 0°C");
    const approvedWhitelisted = entries.find(({ id }) => id === "s5412");
    const correctedMolecule = entries.find(({ id }) => id === "s1812");
    const correctedBernstein = entries.find(({ id }) => id === "s1824");
    const correctedHeading = entries.find(({ id }) => id === "s2429");
    const orderOnly = entries.find(({ zh }) => zh.startsWith("顺序等价"));
    assert.equal(retained.id, "old001");
    assert.equal(retained.count, 5);
    assert.deepEqual(new Set(retained.files), new Set(activeTranslationPages));
    assert.match(added.id, /^r073t\d{3}$/);
    assert.equal(added.en, "New entry");
    assert.equal(repairedMissing.id, "legacyMissing");
    assert.equal(repairedMissing.en, "R0.1 historical missing English");
    assert.equal(repairedMachine.id, "legacyMachine");
    assert.equal(repairedMachine.en, "Machine ledger legacyMachineState=OPEN");
    assert.equal(repairedDecimal.id, "legacyDecimal");
    assert.equal(repairedDecimal.en, "Threshold 74.95");
    assert.equal(correctedTemperature.id, "legacyTemperature");
    assert.equal(correctedTemperature.en, "Temperature 0°C");
    assert.equal(approvedWhitelisted.en, "Exact Implementation Regression on 200,000 Pairs");
    assert.match(correctedMolecule.en, /numerator/);
    assert.match(correctedBernstein.en, /all 288 Bernstein coefficients/);
    assert.equal(correctedHeading.en, "02 · second-order upper bound");
    assert.equal(orderOnly.id, "legacyOrder");
    assert.equal(orderOnly.en,
      "Order-equivalent: betaState=CLOSED; alphaState=OPEN; R0.2; R0.1");
    assert.equal(entries.some(({ zh }) => zh === "失活条目"), false);
    const bundle = readFileSync(resolve(fixture, "public/i18n-en.js"), "utf8");
    assert.ok(bundle.includes("保留条目"));
    assert.ok(bundle.includes("新条目"));
    assert.ok(bundle.includes("R0.1 历史缺失英文"));
    assert.ok(bundle.includes("legacyMachineState=OPEN"));
    assert.ok(bundle.includes("温度 0°C"));
    assert.doesNotMatch(bundle, /失活条目/);

    const checked = runTranslation(fixture, "--check-only");
    assert.equal(checked.status, 0, checked.stderr || checked.stdout);

    const sealedSnapshot = JSON.parse(readFileSync(snapshotPath, "utf8"));
    const sealedWhitelisted = sealedSnapshot.find(({ sourceIdAtCapture }) =>
      sourceIdAtCapture === "s5412");
    const fixedWhitelistNote = sealedWhitelisted.reviewNote;
    sealedWhitelisted.reviewNote += " Tampered.";
    writeFileSync(snapshotPath, JSON.stringify(sealedSnapshot, null, 2) + "\n");
    const whitelistNoteTamperRejected = runTranslation(fixture, "--check-only");
    assert.notEqual(whitelistNoteTamperRejected.status, 0);
    assert.match(whitelistNoteTamperRejected.stderr, /fixed review note drift/);
    sealedWhitelisted.reviewNote = fixedWhitelistNote;

    const fixedWhitelistEnglish = sealedWhitelisted.en;
    sealedWhitelisted.en = "Exact Implementation Regression on 200,001 Pairs";
    writeFileSync(snapshotPath, JSON.stringify(sealedSnapshot, null, 2) + "\n");
    const whitelistEnglishTamperRejected = runTranslation(fixture, "--check-only");
    assert.notEqual(whitelistEnglishTamperRejected.status, 0);
    assert.match(whitelistEnglishTamperRejected.stderr, /cannot alter captured English/);
    sealedWhitelisted.en = fixedWhitelistEnglish;

    const reasonOrderRow = sealedSnapshot.find(({ zh }) => zh === "R0.1 历史缺失英文");
    reasonOrderRow.reasonCodes.reverse();
    writeFileSync(snapshotPath, JSON.stringify(sealedSnapshot, null, 2) + "\n");
    const reasonDriftRejected = runTranslation(fixture, "--check-only");
    assert.notEqual(reasonDriftRejected.status, 0);
    assert.match(reasonDriftRejected.stderr, /capture binding drift/);
    reasonOrderRow.reasonCodes.reverse();

    const driftedTemperature = sealedSnapshot.find(({ zh }) => zh === "温度 0°C");
    driftedTemperature.reviewedIssues = ["BOUNDARY_TOKEN_MULTISET"];
    driftedTemperature.reasonCodes = ["BOUNDARY_TOKEN_MULTISET"];
    writeFileSync(snapshotPath, JSON.stringify(sealedSnapshot, null, 2) + "\n");
    const approvalDriftRejected = runTranslation(fixture, "--check-only");
    assert.notEqual(approvalDriftRejected.status, 0);
    assert.match(approvalDriftRejected.stderr, /capture binding drift/);
    driftedTemperature.reviewedIssues = ["REQUIRED_ARABIC_NUMBER_MULTISET"];
    driftedTemperature.reasonCodes = ["REQUIRED_ARABIC_NUMBER_MULTISET"];
    writeFileSync(snapshotPath, JSON.stringify(sealedSnapshot, null, 2) + "\n");

    retained.en = "Our retained entry";
    writeFileSync(resolve(fixture, "translations/en.json"), JSON.stringify(entries, null, 2) + "\n");
    const rejected = runTranslation(fixture, "--check-only");
    assert.notEqual(rejected.status, 0);
    assert.match(rejected.stderr, /collective English voice/);
  } finally {
    rmSync(fixture, { recursive: true, force: true });
  }
});

test("translation path walk rejects real, dangling, and nondirectory ancestors", () => {
  const fixture = createTranslationFixture();
  try {
    const translations = resolve(fixture, "translations");
    const realTranslations = resolve(fixture, "real-translations");
    renameSync(translations, realTranslations);
    symlinkSync(realTranslations, translations, "dir");
    const linked = runTranslation(fixture, "--capture-missing");
    assert.notEqual(linked.status, 0);
    assert.match(linked.stderr, /symlink component rejected/);

    unlinkSync(translations);
    symlinkSync(resolve(fixture, "missing-translations"), translations, "dir");
    const dangling = runTranslation(fixture, "--capture-missing");
    assert.notEqual(dangling.status, 0);
    assert.match(dangling.stderr, /symlink component rejected/);

    unlinkSync(translations);
    writeFileSync(translations, "not a directory");
    const nondirectory = runTranslation(fixture, "--capture-missing");
    assert.notEqual(nondirectory.status, 0);
    assert.match(nondirectory.stderr, /nondirectory ancestor rejected/);
  } finally {
    rmSync(fixture, { recursive: true, force: true });
  }
});

test("the deferred translation and PDF stages are syntax-safe and local-only", () => {
  const translation = read("scripts/add-r073t-translations.mjs");
  const binder = read("scripts/bind-r073t-pdfs.mjs");
  for (const [script, usage] of [
    ["scripts/add-r073t-translations.mjs", "add-r073t-translations.mjs"],
    ["scripts/bind-r073t-pdfs.mjs", "bind-r073t-pdfs.mjs"],
  ]) {
    const checked = runNode("--check", script);
    assert.equal(checked.status, 0, checked.stderr || checked.stdout);
    const help = runNode(script, "--help");
    assert.equal(help.status, 0, help.stderr || help.stdout);
    assert.ok(help.stdout.includes(usage));
  }
  assert.ok(translation.includes("LOCAL_DIRECT_NO_DGX"));
  assert.ok(translation.includes("reviewed-local-direct-no-dgx-no-network"));
  assert.ok(translation.includes("local-direct-reviewed"));
  assert.ok(translation.includes("--capture-missing"));
  assert.ok(translation.includes("/i18n-en.js?v=1.60"));
  assert.ok(translation.includes("assertSafePath"));
  assert.ok(translation.includes("source.map((entry)"));
  assert.ok(translation.includes("removedStale"));
  assert.doesNotMatch(translation, /from ["']node:(?:child_process|http|https|net|tls|dns)["']/);
  assert.doesNotMatch(translation, /\bfetch\s*\(/);
  assert.ok(binder.includes("fig-r073t-dynamic-autocorrelation"));
  assert.ok(binder.includes("R0.73T｜Dynamic autocorrelation and the pressure-tensor barrier"));
  assert.ok(binder.includes("R0.61–R0.73T｜R0.60 之后的研究回顾"));
  for (const token of [
    'exactAutocorrelationEvolution: "VERIFIED_CLASSICAL_RECONSTRUCTION"',
    'dynamicAQUpperInequality: "INTERNAL_COROLLARY"',
    'criticalAIntegralControl: "OPEN"',
    'carrierScaleNonAutonomy: "CLOSED_EXACT"',
    'signedVelocityPhaseInPressurePairing: "CLOSED_EXACT"',
    'pressureTensorNeededForGeneralReconstruction: "VERIFIED_CLASSICAL"',
    "finiteFormulaDiagnosticChecks: 55", "formalFigureChecks: 106",
    'arbitraryThreeDimensionalGlobalRegularity: "OPEN"', 'clayConclusion: "OPEN"',
  ]) assert.ok(binder.includes(token), token);
});

test("PDF structure parser accepts bound hex/literal Info titles and rejects broken tails", async () => {
  const { inspectPdf } = await import(
    new URL("../scripts/render-note-pdf.mjs", import.meta.url)
  );
  const fixture = (titleToken) => {
    const chunks = [Buffer.from("%PDF-1.4\n", "latin1")];
    const offsets = [0];
    const object = (number, body) => {
      offsets[number] = Buffer.concat(chunks).length;
      chunks.push(Buffer.from(`${number} 0 obj\n${body}\nendobj\n`, "latin1"));
    };
    object(1, "<< /Type /Catalog /Pages 2 0 R /Title (Decoy title) >>");
    object(2, "<< /Type /Pages /Kids [3 0 R] /Count 1 >>");
    object(3, "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 100 100] >>");
    object(4, `<< /Title ${titleToken} >>`);
    const startxref = Buffer.concat(chunks).length;
    chunks.push(Buffer.from(
      "xref\n0 5\n0000000000 65535 f \n" +
      offsets.slice(1).map((offset) => `${String(offset).padStart(10, "0")} 00000 n \n`).join("") +
      "trailer\n<< /Size 5 /Root 1 0 R /Info 4 0 R >>\n" +
      `startxref\n${startxref}\n%%EOF\n`,
      "latin1",
    ));
    return Buffer.concat(chunks);
  };
  const utf16 = Buffer.concat([
    Buffer.from([0xfe, 0xff]),
    Buffer.from("R0.73T").reduce(
      (bytes, value) => Buffer.concat([bytes, Buffer.from([0, value])]), Buffer.alloc(0),
    ),
  ]).toString("hex").toUpperCase();
  const hex = inspectPdf(fixture(`<${utf16}>`), "hex fixture");
  assert.equal(hex.title, "R0.73T");
  assert.notEqual(hex.title, "Decoy title");
  assert.equal(hex.titleEncoding, "hex");
  assert.equal(hex.pageCount, 1);
  assert.equal(hex.infoObject, "4 0 R");
  assert.equal(hex.xrefKeyword, "xref");
  const literal = inspectPdf(fixture("(Literal\\(Title\\))"), "literal fixture");
  assert.equal(literal.title, "Literal(Title)");
  assert.equal(literal.titleEncoding, "literal");
  assert.throws(
    () => inspectPdf(Buffer.from(fixture("(Broken)").toString("latin1").replace("%%EOF", "%EOF"), "latin1")),
    /startxref\/%%EOF/,
  );
  assert.throws(
    () => inspectPdf(Buffer.from(fixture("(Broken)").toString("latin1").replace(/startxref\n\d+/, "startxref\n1"), "latin1")),
    /does not point to xref/,
  );

  const binderFixture = mkdtempSync(join(realpathSync(tmpdir()), "r073t-pdf-binder-test-"));
  try {
    writeFileSync(resolve(binderFixture, "fixture.pdf"), fixture(`<${utf16}>`));
    const checked = spawnSync(
      process.execPath,
      ["scripts/bind-r073t-pdfs.mjs", "--structure-check", "fixture.pdf", "R0.73T"],
      {
        cwd: root,
        encoding: "utf8",
        env: { ...process.env, R073T_RELEASE_ROOT: binderFixture },
      },
    );
    assert.equal(checked.status, 0, checked.stderr || checked.stdout);
    const structure = JSON.parse(checked.stdout);
    assert.equal(structure.title, "R0.73T");
    assert.equal(structure.infoObject, "4 0 R");
    assert.equal(structure.pageCount, 1);
    assert.equal(structure.eof, true);
    assert.equal(structure.xrefKeyword, "xref");
  } finally {
    rmSync(binderFixture, { recursive: true, force: true });
  }
});

test("renderer formal mode rejects a symlinked output ancestor before browser launch", () => {
  const fixture = mkdtempSync(join(realpathSync(tmpdir()), "r073t-render-safety-test-"));
  try {
    mkdirSync(resolve(fixture, "actual-output"));
    symlinkSync(resolve(fixture, "actual-output"), resolve(fixture, "linked-output"), "dir");
    writeFileSync(resolve(fixture, "source.html"), "<!doctype html><title>fixture</title>");
    const result = spawnSync(
      process.execPath,
      [
        "scripts/render-note-pdf.mjs", "http://127.0.0.1:9/fixture.html",
        resolve(fixture, "linked-output/result.pdf"), "-",
        resolve(fixture, "source.html"), resolve(fixture, "render.json"),
      ],
      {
        cwd: root,
        encoding: "utf8",
        env: { ...process.env, PDF_RENDER_ROOT: fixture },
      },
    );
    assert.notEqual(result.status, 0);
    assert.match(result.stderr, /symlink ancestor/);
    assert.equal(readFileSync(resolve(fixture, "source.html"), "utf8").includes("fixture"), true);
  } finally {
    rmSync(fixture, { recursive: true, force: true });
  }
});

test("R0.73T PDF evidence chain requires deterministic render sidecars and safe ancestry", () => {
  const renderer = read("scripts/render-note-pdf.mjs");
  const binder = read("scripts/bind-r073t-pdfs.mjs");
  for (const token of [
    "[SOURCE_HTML] [PROVENANCE_JSON]",
    "loaded main-document bytes differ from SOURCE_HTML",
    "loadedDocument",
    "synchronized-pdf-render-provenance-v1",
    "terminal startxref/%%EOF",
    "last startxref does not point to xref",
    "trailer /Info reference is absent",
    "PDF provenance output",
    "assertSafeDirectoryChain",
  ]) assert.ok(renderer.includes(token), token);
  for (const token of [
    "research/r073t_note_pdf_render.json",
    "research/r073t_recap_pdf_render.json",
    "loadedMainDocumentEqualsSourceHtml",
    "renderProvenanceSidecarsBound",
    "pdfStartxrefPointsToXref",
    "pdfTrailerInfoReferenceValidated",
    "assertSafeDirectoryChain",
    "O_NOFOLLOW",
  ]) assert.ok(binder.includes(token), token);
  assert.doesNotMatch(renderer, /createdAt|timestamp|Date\.now\(\)/);
});
