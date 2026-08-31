import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { spawnSync } from "node:child_process";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const manifest = JSON.parse(read("research/release-manifest.json"));

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
  const result = runPython("-c", source);
  assert.equal(result.status, 0, result.stderr || result.stdout);
  return JSON.parse(result.stdout);
}

function runNode(...argumentsList) {
  return spawnSync(process.execPath, argumentsList, {
    cwd: root,
    encoding: "utf8",
  });
}

test("release content reads the fixed R0.73S title without writing", () => {
  const result = pythonJson("scripts/r073s_release_content.py", "--check-only");
  assert.equal(result.release, "R0.73S");
  assert.equal(result.title,
    "R0.73S | From triple convolution to autocorrelation: one computable certificate and two hard limits");
  assert.equal(result.publicTitleZh,
    "R0.73S｜把三重卷积降到自相关：一个可算证书，两条不能越过的边界");
  assert.equal(result.canonicalSources, 9);
  assert.equal(result.canonicalSourcesPlanned, 9);
  assert.equal(result.sections, 10);
  assert.equal(result.quadraticAutocorrelationBound, "VERIFIED_CLASSICAL");
  assert.equal(result.universalRuntimeLowerBound, "NOT_PROVED");
  assert.equal(result.zeroNonlinearityWitnesses, "CLOSED");
  assert.equal(result.arbitraryThreeDimensionalGlobalRegularity, "OPEN");
  assert.equal(result.clayConclusion, "OPEN");
  assert.equal(result.translationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(result.writes, 0);
  if (manifest.latestCompletedRelease === "r073s") {
    assert.equal(result.publicationReady, true);
    assert.deepEqual(result.readinessFailures, []);
  } else {
    assert.equal(manifest.latestCompletedRelease, "r073r");
    assert.equal(result.publicationReady, true);
    assert.deepEqual(result.readinessFailures, []);
  }
});

test("source-dry-run exposes exact accounting and the complete non-writing plan", () => {
  const result = pythonJson("scripts/generate_r073s_release.py", "--source-dry-run");
  assert.equal(result.release, "R0.73S");
  assert.equal(result.siteVersion, "1.59");
  assert.deepEqual(result.targetAccounting, {
    latestCompletedRelease: "r073s",
    siteVersion: "1.59",
    publicHtmlNoteCount: 195,
    postR060RecapNodeCount: 135,
    nextRelease: "r073t",
    postR070APublishedReleaseCount: 97,
    postR070AFormalSealedReleaseCount: 73,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.equal(result.baselineAccounting.latestCompletedRelease, "r073r");
  assert.equal(result.baselineAccounting.siteVersion, "1.58");
  assert.equal(result.canonicalSources, 9);
  assert.equal(result.certificate.present, true);
  assert.equal(result.figure.present, true);
  assert.equal(result.figure.formal, true);
  assert.equal(result.figure.figureId, "fig-r073s-quadratic-certificate");
  assert.equal(result.translationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(result.clayConclusion, "OPEN");
  assert.ok(result.coreOutputsPlanned.includes("public/notes/r0-73s.html"));
  assert.ok(result.coreOutputsPlanned.includes("public/recap-r0-61-r0-73s.html"));
  assert.ok(result.laterStageOutputsPlanned.includes("research/r073s_pdf_bindings.json"));
  assert.ok(result.figureOutputsPlanned.includes(
    "public/assets/r073s/fig-r073s-quadratic-certificate.pdf"));
  assert.equal(result.writes, 0);
  assert.equal(result.commitPinsReady, true);
  assert.equal(result.publicTransactionImplemented, true);
  assert.equal(result.publicationReady, true);
});

test("the layered generator pins every reviewed input through the normalized release-source slot", () => {
  const generator = read("scripts/generate_r073s_release.py");
  assert.match(generator,
    /RELEASE_BASELINE_COMMIT = "71b562d45529ac45d2423d598fcc0f7f0845ea4b"/);
  assert.match(generator,
    /ANALYTIC_SOURCE_COMMIT = "72e4c12760dc3b837dec328ee96a29736fe93c99"/);
  assert.match(generator,
    /FINITE_PACKAGE_COMMIT = "4bb49ecc380e4b41d33e3102af4f47de016b5653"/);
  assert.match(generator,
    /FIGURE_PACKAGE_COMMIT = "4bb49ecc380e4b41d33e3102af4f47de016b5653"/);
  assert.match(generator,
    /FINAL_CONTENT_COMMIT = "ee6b4f15733f68ead337eb04d29620fd8b98e60d"/);
  assert.match(generator, /RELEASE_SOURCE_COMMIT = "[0-9a-f]{40}"/);
  assert.ok(generator.includes("__NORMALIZED_RELEASE_SOURCE_COMMIT__"));
  assert.match(generator, /PUBLIC_TRANSACTION_IMPLEMENTED = True/);
  assert.ok(generator.includes("verify_commit_trees(FINITE_PACKAGE_COMMIT"));
  assert.ok(generator.includes("verify_commit_trees(FIGURE_PACKAGE_COMMIT"));
  assert.ok(generator.includes('"research/r073s_claim_source_ledger.md"'));
  assert.ok(generator.includes('"research/r073s_evidence_gap_matrix.md"'));
  assert.ok(generator.includes('"research/r073s_finite_diagnostic_audit.md"'));
  assert.ok(true, "the test suite never invokes --apply");
});

test("the public transaction assembles every target in memory without applying it", () => {
  const result = pythonCodeJson([
    "import json,sys",
    "sys.path.insert(0,'scripts')",
    "import generate_r073s_release as g",
    "s=g.build_staged(g.load_release_content(g.ROOT))",
    "rel=lambda p:p.relative_to(g.ROOT).as_posix()",
    "figure=json.loads(s[g.ROOT/g.FIGURE_ARCHIVE_RELATIVE/'manifest.json'])",
    "print(json.dumps({'count':len(s),'core':all(g.ROOT/p in s for p in g.CORE_TARGET_OUTPUTS),'html':sum(p.suffix=='.html' for p in s),'note':'R0.73S｜把三重卷积降到自相关' in s[g.PUBLIC/'notes/r0-73s.html'].decode(),'recap':'135 个节点' in s[g.PUBLIC/'recap-r0-61-r0-73s.html'].decode(),'home':'R0.73T 下一接口' in s[g.PUBLIC/'research-review.html'].decode(),'literature':'dynamic autocorrelation budget' in s[g.PUBLIC/'literature-review.html'].decode(),'figureStatus':figure['status'],'publicCopies':figure['publication']['publicCopiesComplete'],'paths':sorted(rel(p) for p in s)}))",
  ].join(";"));
  assert.equal(result.count, 62);
  assert.equal(result.core, true);
  assert.equal(result.html, 5);
  assert.equal(result.note, true);
  assert.equal(result.recap, true);
  assert.equal(result.home, true);
  assert.equal(result.literature, true);
  assert.equal(result.figureStatus, "formal");
  assert.equal(result.publicCopies, true);
  assert.ok(result.paths.includes("public/assets/r073s/fig-r073s-quadratic-certificate.pdf"));
  assert.ok(result.paths.includes("figures/r073s/fig-r073s-quadratic-certificate/manifest.json"));
});

test("the declared R0.73S release source owns its later local-only stages", () => {
  const generator = read("scripts/generate_r073s_release.py");
  for (const relative of [
    "scripts/r073s_release_content.py",
    "scripts/generate_r073s_release.py",
    "scripts/add-r073s-translations.mjs",
    "scripts/bind-r073s-pdfs.mjs",
    "tests/r073s-autocorrelation-gate.test.mjs",
    "tests/r073s-release.test.mjs",
    "tests/site-route-current-boundary.test.mjs",
  ]) {
    assert.ok(generator.includes(`"${relative}"`), relative);
  }
  assert.ok(generator.includes("capture-review-and-apply-local-translations"));
  assert.ok(generator.includes("render-synchronized-note-and-recap-pdfs"));
});

test("the deferred translation and PDF stages are syntax-safe and local-only", () => {
  const translation = read("scripts/add-r073s-translations.mjs");
  const binder = read("scripts/bind-r073s-pdfs.mjs");
  for (const [script, usage] of [
    ["scripts/add-r073s-translations.mjs", "add-r073s-translations.mjs"],
    ["scripts/bind-r073s-pdfs.mjs", "bind-r073s-pdfs.mjs"],
  ]) {
    const checked = runNode("--check", script);
    assert.equal(checked.status, 0, checked.stderr || checked.stdout);
    const help = runNode(script, "--help");
    assert.equal(help.status, 0, help.stderr || help.stdout);
    assert.match(help.stdout, new RegExp(usage.replaceAll(".", "\\.")));
  }
  assert.ok(translation.includes("reviewed-local-direct-no-dgx-no-network"));
  assert.ok(translation.includes("local-human-reviewed"));
  assert.ok(translation.includes("provenance !== localHumanProvenance"));
  assert.ok(translation.includes("/i18n-en.js?v=1.59"));
  assert.ok(translation.includes("R0.73T"));
  assert.doesNotMatch(translation, /from ["']node:(?:child_process|http|https|net|tls|dns)["']/);
  assert.doesNotMatch(translation, /\bfetch\s*\(/);
  assert.ok(binder.includes("fig-r073s-quadratic-certificate"));
  assert.ok(binder.includes(
    "R0.73S｜From triple convolution to autocorrelation: one computable certificate and two hard limits"));
  assert.ok(binder.includes("R0.61–R0.73S｜R0.60 之后的研究回顾"));
  assert.ok(binder.includes("quadraticAutocorrelationBound: \"VERIFIED_CLASSICAL\""));
  assert.ok(binder.includes("universalRuntimeLowerBound: \"NOT_PROVED\""));
  assert.ok(binder.includes("arbitraryThreeDimensionalGlobalRegularity: \"OPEN\""));
  assert.ok(binder.includes("clayConclusion: \"OPEN\""));
});
