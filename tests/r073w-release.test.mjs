import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, lstatSync, readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const python = process.env.R073W_PYTHON ?? "python3";
const node = process.execPath;
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const bytes = (relative) => readFileSync(resolve(root, relative));
const json = (relative) => JSON.parse(read(relative));
const sha256 = (payload) => createHash("sha256").update(payload).digest("hex");
const runPython = (args) => execFileSync(python, ["-B", ...args], {
  cwd: root,
  encoding: "utf8",
  env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
});
const pythonJson = (source) => JSON.parse(runPython(["-c", source]));

const title =
  "R0.73W | Signed subfilter production: heat-plane characteristics, " +
  "the energy-class boundary, and exact counterexamples";
const publicTitle =
  "R0.73W｜带符号亚滤波 production：heat-plane 特征线、能量类边界与精确反例";
const pins = Object.freeze({
  baseline: "4970477d0c08992cd6881d4f3fe40362f41a7738",
  finiteSource: "b9f3b3943df1e2abf6abc2f51c1fb25d1f1e8440",
  finitePackage: "68893eccd7f5b6047bf2b00c5262913e23fadbc3",
  finalContent: "855e341e371302f315c5535006193f8ce0703740",
  figureSource: "ac6293ac4d0c46c696d2ec8e29d3fb1350e341f1",
  figurePackage: "60b0e869bbaa3a0ace185bf450e067d79fcd79b3",
});

const generator = read("scripts/generate_r073w_release.py");
const sourcePinMatch = generator.match(
  /^RELEASE_SOURCE_COMMIT = (ZERO_COMMIT|"([0-9a-f]{40})")$/m,
);
assert.ok(sourcePinMatch, "release-source pin slot");
const sourcePinReady = sourcePinMatch[1] !== "ZERO_COMMIT";
const currentReleaseManifest = json("research/release-manifest.json");
const publicReleaseApplied = currentReleaseManifest.latestCompletedRelease === "r073w";

function regular(relative) {
  const path = resolve(root, relative);
  return existsSync(path) && lstatSync(path).isFile() && !lstatSync(path).isSymbolicLink();
}

test("release tooling binds the immutable W chain and CI stays manifest-driven", () => {
  const content = read("scripts/r073w_release_content.py");
  const translation = read("scripts/add-r073w-translations.mjs");
  const binder = read("scripts/bind-r073w-pdfs.mjs");
  const renderer = read("scripts/render-note-pdf.mjs");
  const runner = read("scripts/run-release-publication-gate.mjs");
  const scientificGate = read("tests/r073w-signed-production-gate.test.mjs");
  const tooling = [content, generator, translation, binder, scientificGate].join("\n");

  for (const token of [
    title,
    publicTitle,
    ...Object.values(pins),
    "R073V_BASELINE",
    "formalFiniteCertificateChecks=56+56",
    "fig-r073w-signed-production",
    "LOCAL_DIRECT_NO_DGX",
    "dgxUsed: false",
    "tests/r073w-signed-production-gate.test.mjs",
    "tests/r073w-release.test.mjs",
    ".github/workflows/pages.yml",
    ".github/workflows/release-publication-gate.yml",
  ]) assert.ok(tooling.includes(token), token);

  assert.equal(translation.includes("node:child_process"), false);
  assert.doesNotMatch(translation, /\bfetch\s*\(|https?\.request|\bspawn\s*\(|\bexec\s*\(/);
  assert.ok(translation.includes("translationPath: translationRoute"));
  assert.ok(translation.includes("dgxUsed: false"));
  assert.ok(binder.includes("ordinaryTranslationPath: \"LOCAL_DIRECT_NO_DGX\""));
  assert.ok(binder.includes("dgxUsed: false"));
  assert.ok(renderer.includes("expectsMathJax"));
  assert.ok(renderer.includes("page.waitForFunction"));
  assert.ok(renderer.includes("globalThis.MathJax?.startup?.promise"));
  assert.ok(runner.includes("manifest.latestReleaseGate"));
  assert.ok(runner.includes("manifest.latestReleasePublicationTest"));
  for (const workflow of [
    ".github/workflows/pages.yml",
    ".github/workflows/release-publication-gate.yml",
  ]) assert.ok(read(workflow).includes("node scripts/run-release-publication-gate.mjs"));
});

test("source dry-run freezes 1.63 and the 199/139/101/77/24 transition without writes", () => {
  const result = JSON.parse(runPython([
    "scripts/generate_r073w_release.py", "--source-dry-run",
  ]));
  assert.equal(result.release, "R0.73W");
  assert.equal(result.siteVersion, "1.63");
  assert.equal(result.title, title);
  assert.equal(result.publicTitleZh, publicTitle);
  assert.deepEqual(result.baselineAccounting, {
    latestCompletedRelease: "r073v",
    siteVersion: "1.62",
    publicHtmlNoteCount: 198,
    postR060RecapNodeCount: 138,
    nextRelease: "r073w",
    postR070APublishedReleaseCount: 100,
    postR070AFormalSealedReleaseCount: 76,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.deepEqual(result.targetAccounting, {
    latestCompletedRelease: "r073w",
    siteVersion: "1.63",
    publicHtmlNoteCount: 199,
    postR060RecapNodeCount: 139,
    nextRelease: "r073x",
    postR070APublishedReleaseCount: 101,
    postR070AFormalSealedReleaseCount: 77,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.equal(result.publicationReady, true);
  assert.deepEqual(result.readinessFailures, []);
  assert.equal(result.canonicalSources.length, 9);
  assert.equal(result.plannedAuditPaths.length, 2);
  assert.equal(result.certificate.finalSeal, true);
  assert.equal(result.certificate.status, "SEALED_COMMIT_BOUND");
  assert.equal(result.certificate.sourceCommit, pins.finiteSource);
  assert.deepEqual(result.certificate.inventory, {
    boundFileCount: 11,
    generatedFileCount: 4,
    packageFileCount: 13,
    sha256SumsLineCount: 12,
    sourceFileCount: 9,
  });
  assert.deepEqual(result.certificate.checks,
    { exactPerPath: 56, requiredPerPath: 56, twoPathComparisons: 2 });
  assert.equal(result.figure.formal, true);
  assert.equal(result.figure.expectedPackageFileCount, 25);
  assert.equal(result.figure.validation.passed, 49);
  assert.equal(result.figure.validation.required, 49);
  assert.equal(result.figure.validation.checksObserved, 49);
  assert.equal(result.releaseSourceReady, true);
  assert.equal(result.commitPinsReady, sourcePinReady);
  assert.deepEqual(result.zeroCommitLayers,
    sourcePinReady ? [] : ["R0.73W release source"]);
  assert.equal(result.coreOutputsPlanned.length, 11);
  assert.equal(result.figureResearchArchiveOutputsPlanned.length, 25);
  assert.equal(result.figurePublicArchiveOutputsPlanned.length, 25);
  assert.equal(result.figurePublicAssetOutputsPlanned.length, 3);
  assert.equal(result.laterStageOutputsPlanned.length, 8);
  assert.equal(result.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(result.dgxUsed, false);
  assert.equal(result.clayConclusion, "OPEN");
  assert.equal(result.writes, 0);
});

test("canonical reader extraction is ready and hands the open interface to R0.73X", () => {
  const result = pythonJson(String.raw`
import json,sys
sys.path.insert(0,"scripts")
import generate_r073w_release as g
from r073w_release_content import load_release_content
c=load_release_content(g.ROOT)
print(json.dumps({
  "title":c.release_title_en,
  "publicTitle":c.public_title_zh,
  "sections":len(c.sections),
  "ready":c.publication_ready,
  "failures":list(c.readiness_failures),
  "next":c.next_release,
  "nextGate":c.next_gate_zh,
  "home":c.home_zh,
  "recap":c.recap_zh,
  "literature":c.literature_zh,
  "sourceCount":len(c.source_sha256),
},ensure_ascii=False))
`);
  assert.equal(result.title, title);
  assert.equal(result.publicTitle, publicTitle);
  assert.equal(result.sections, 11);
  assert.equal(result.ready, true);
  assert.deepEqual(result.failures, []);
  assert.equal(result.next, "R0.73X");
  assert.match(result.nextGate, /localized|cutoff|defect|局部|尺度/iu);
  assert.match(result.home, /production|heat|能量/iu);
  assert.match(result.recap, /符号|尺度|反例/u);
  assert.match(result.literature, /新颖性|优先权/u);
  assert.equal(result.sourceCount, 9);
});

test("the in-memory transaction builds 64 current targets with W kept and X open", () => {
  const result = pythonJson(String.raw`
import json,sys
sys.path.insert(0,"scripts")
import generate_r073w_release as g
from r073w_release_content import load_release_content
s=g.build_staged(load_release_content(g.ROOT))
def text(relative): return s[g.ROOT/relative].decode("utf-8")
note=text("public/notes/r0-73w.html")
recap=text("public/recap-r0-61-r0-73w.html")
home=text("public/research-review.html")
literature=text("public/literature-review.html")
index=text("public/notes/index.html")
figure=json.loads(text("public/figures/r073w/fig-r073w-signed-production/manifest.json"))
names=sorted(p.name for p in (g.ROOT/g.FIGURE_SOURCE_RELATIVE).iterdir() if p.is_file())
print(json.dumps({
  "count":len(s),
  "html":sum(path.suffix==".html" for path in s),
  "core":sum(g.ROOT/path in s for path in g.CORE_OUTPUTS),
  "researchFigure":sum(g.ROOT/path in s for path in g.FIGURE_RESEARCH_ARCHIVE_OUTPUTS),
  "publicFigure":sum(g.ROOT/path in s for path in g.FIGURE_PUBLIC_ARCHIVE_OUTPUTS),
  "assets":sum(g.ROOT/path in s for path in g.FIGURE_PUBLIC_ASSET_OUTPUTS),
  "copiesEqual":all(s[g.ROOT/"research"/g.FIGURE_ARCHIVE_RELATIVE/name]==s[g.PUBLIC/g.FIGURE_ARCHIVE_RELATIVE/name] for name in names),
  "auditsEqual":all(s[g.PUBLIC/"research"/"r073w"/name]==(g.ROOT/"research"/name).read_bytes() for name in ("r073w_figure_source_audit.md","r073w_figure_source_reaudit.md")),
  "recapNodes":recap.count('class="node-ref"'),
  "indexNotes":index.count('<li class="note-entry"'),
  "homeCounts":all(value in home for value in ("199</strong>公开研究笔记","139 节累计回顾","101 节已公开","77 节完整封存")),
  "currentRoute":literature.count('<header><b>R0.73W</b>')==1 and literature.count('开放接口 · R0.73X')==1 and '开放接口 · R0.73W' not in literature,
  "literatureCounts":all(value in literature for value in ("本站 R0.69P–R0.73W 只列为研究笔记","累计回顾与 139 节索引","打开 139 节完整索引")) and all(value not in literature for value in ("本站 R0.69P–R0.73V 只列为研究笔记","累计回顾与 138 节索引","打开 138 节完整索引")),
  "currentVersion":all("v1.62" not in value and "v=1.62" not in value for value in (home,literature,index)),
  "indexLatest":"最新节点 R0.73V" not in index and "199 篇公开研究笔记" in index,
  "recapMeta":"最新一节分开带符号亚滤波 production、heat-plane 特征线" in recap,
  "recapSources":all(value in recap for value in ("打开最新节点 R0.73W","research/r073w_report-source.md","research/r073w_signed_production_heat_characteristic.md","research/r073w_primary_literature_audit.md","research/certificates/r073w","/assets/r073w/fig-r073w-signed-production.pdf")) and "打开最新节点 R0.73V" not in recap,
  "homeRecap":all(value in home[home.index('id="post-r060-recap"'):home.index('id="r070a"')] for value in ("R0.61–R0.73W","139 个节点","199 篇公开研究笔记","58 个阶段","101 个版本已公开","77 个按当前 formal-figure 合同完整封存")) and all(value not in home[home.index('id="post-r060-recap"'):home.index('id="r070a"')] for value in ("累计回顾 R0.61–R0.73V","完整保留 R0.61–R0.73V","R0.70A–R0.73V 共","138 个节点","198 篇公开研究笔记","57 个阶段")),
  "homeRoute":all(value in home for value in ("Research topology · R0.1–R0.73W",'href="#r073w">跳到首页 R0.73W 卡片',"R0.69P–R0.73W","展开 109 篇公开笔记",'href="/notes/r0-73w.html">R0.73W</a>',"localized heat-characteristic and defect ledger")) and all(value not in home for value in ("Research topology · R0.1–R0.73V",'href="#r073v">跳到首页 R0.73V 卡片','<span class="route-range">R0.69P–R0.73V</span>',"展开 108 篇公开笔记")),
  "noteMath":"mathjax@3/es5/tex-mml-chtml.js" in note and "window.MathJax=" in note and "**" not in note and "<strong>[开放]</strong>" in note,
  "noteMathDelimiters":"inlineMath:[['\\\\(','\\\\)']]" in note and "displayMath:[['\\\\[','\\\\]']]" in note,
  "sealedBoundary":"formalFigurePackage=SEALED_COMMIT_BOUND" in note,
  "rawFence":any(chr(96)*3 in value for value in (note,recap,home,literature)),
  "figureStatus":[figure.get("publicationStatus"),figure.get("sourcePublicationStatus")],
  "figureSource":figure.get("publication",{}).get("figureSourceCommit"),
  "figurePackage":figure.get("publication",{}).get("figurePackageCommit"),
},ensure_ascii=False))
`);
  assert.deepEqual(result, {
    count: 64,
    html: 5,
    core: 11,
    researchFigure: 25,
    publicFigure: 25,
    assets: 3,
    copiesEqual: true,
    auditsEqual: true,
    recapNodes: 139,
    indexNotes: 199,
    homeCounts: true,
    currentRoute: true,
    literatureCounts: true,
    currentVersion: true,
    indexLatest: true,
    recapMeta: true,
    recapSources: true,
    homeRecap: true,
    homeRoute: true,
    noteMath: true,
    noteMathDelimiters: true,
    sealedBoundary: true,
    rawFence: false,
    figureStatus: ["published", "staged"],
    figureSource: pins.figureSource,
    figurePackage: pins.figurePackage,
  });
});

test("the in-memory generator is fail-closed until its normalized release-source pin exists", () => {
  const completed = spawnSync(
    python,
    ["-B", "scripts/generate_r073w_release.py", "--check-only"],
    {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  if (!sourcePinReady) {
    assert.notEqual(completed.status, 0);
    assert.match(completed.stderr, /ZERO_COMMIT|unsealed 40-zero commit pin|release source/i);
  } else {
    assert.equal(completed.status, 0, completed.stderr);
    const result = JSON.parse(completed.stdout);
    assert.equal(result.release, "R0.73W");
    assert.equal(result.siteVersion, "1.63");
    assert.equal(result.checkOnly, true);
    assert.equal(result.transaction, "IN_MEMORY_ONLY");
    assert.equal(result.stagedOutputs, 64);
    assert.equal(Object.keys(result.stagedSha256).length, 64);
    assert.equal(result.writes, 0);
  }
});

test("local translation and PDF binding either reproduce W or fail closed before public apply", () => {
  for (const script of [
    "scripts/add-r073w-translations.mjs",
    "scripts/bind-r073w-pdfs.mjs",
  ]) {
    execFileSync(node, ["--check", script], { cwd: root, stdio: "pipe" });
    const help = spawnSync(node, [script, "--help"], { cwd: root, encoding: "utf8" });
    assert.equal(help.status, 0, `${script}: ${help.stderr}`);
    assert.match(help.stdout, /usage|R0\.73W/i);

    const checked = spawnSync(node, [script, "--check-only"], {
      cwd: root, encoding: "utf8",
    });
    if (publicReleaseApplied) {
      assert.equal(checked.status, 0, `${script}: ${checked.stderr}`);
      const result = JSON.parse(checked.stdout);
      assert.equal(result.dgxUsed, false);
    } else {
      assert.notEqual(checked.status, 0, `${script} must fail before the W public apply`);
      assert.match(checked.stderr, /snapshot.*absent|HTML\/accounting|must precede|missing|stale/i);
    }
  }
});

test("published W binds the exact HTML/PDF bytes, counts, and canonical output names", (t) => {
  if (!publicReleaseApplied) {
    t.skip("R0.73W public transaction is not applied; source-dry-run and fail-closed gates apply");
    return;
  }

  const release = json("research/release-manifest.json");
  const site = json("public/site-version.json");
  const expected = {
    latestCompletedRelease: "r073w",
    siteVersion: "1.63",
    publicHtmlNoteCount: 199,
    postR060RecapNodeCount: 139,
    nextRelease: "r073x",
    postR070APublishedReleaseCount: 101,
    postR070AFormalSealedReleaseCount: 77,
    legacyFormalFigureBacklogCount: 24,
  };
  for (const [key, value] of Object.entries(expected)) assert.equal(release[key], value, key);
  assert.equal(release.latestReleaseGate, "tests/r073w-signed-production-gate.test.mjs");
  assert.equal(release.latestReleasePublicationTest, "tests/r073w-release.test.mjs");
  assert.equal(site.version, "1.63");
  assert.equal(site.latestRelease, "R0.73W");
  assert.equal(site.publicHtmlNoteCount, 199);
  assert.equal(read("VERSION"), "1.63\n");

  const note = read("public/notes/r0-73w.html");
  const recap = read("public/recap-r0-61-r0-73w.html");
  const home = read("public/research-review.html");
  assert.ok(note.includes(publicTitle));
  assert.ok(note.includes("/assets/r073w/fig-r073w-signed-production.pdf"));
  assert.ok(note.includes("/notes/r0-73w.pdf"));
  assert.equal(recap.match(/class="node-ref"/g)?.length, 139);
  assert.equal(home.match(/data-release="r073w"/g)?.length, 1);
  assert.ok(home.includes("R0.73X"));

  const bindings = json("research/r073w_pdf_bindings.json");
  assert.equal(bindings.schemaVersion, "r073w-synchronized-pdf-bindings-v1");
  assert.equal(bindings.release, "R0.73W");
  assert.equal(bindings.documents.length, 2);
  assert.equal(bindings.claimBoundary.htmlAndPdfBytesCryptographicallyBound, true);
  assert.equal(bindings.claimBoundary.formalFigureChecks, 49);
  assert.equal(bindings.claimBoundary.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(bindings.claimBoundary.dgxUsed, false);
  for (const document of bindings.documents) {
    assert.equal(regular(document.html.path), true, document.html.path);
    assert.equal(regular(document.pdf.path), true, document.pdf.path);
    assert.equal(sha256(bytes(document.html.path)), document.html.sha256, document.html.path);
    assert.equal(sha256(bytes(document.pdf.path)), document.pdf.sha256, document.pdf.path);
    assert.ok(document.pdf.pageCount > 0, document.pdf.path);
    assert.ok(document.pdf.bytes > 10_000, document.pdf.path);
  }

  const conflictCopy = (name) => / [234](?=\.[^.]+$|$)/.test(name);
  for (const directory of [
    "public/assets/r073w",
    "public/figures/r073w/fig-r073w-signed-production",
    "public/research/r073w",
    "research/figures/r073w/fig-r073w-signed-production",
  ]) {
    const tracked = execFileSync("git", ["ls-files", "-z", "--", directory], {
      cwd: root, encoding: "utf8",
    }).split("\0").filter(Boolean);
    assert.equal(tracked.some(conflictCopy), false, directory);
  }
  for (const directory of ["public", "public/notes", "research", "scripts/i18n-snapshots"]) {
    const bad = execFileSync("git", ["ls-files", "-z", "--", directory], {
      cwd: root, encoding: "utf8",
    }).split("\0").filter(Boolean)
      .filter((name) => /r073w|r0-73w/i.test(name) && conflictCopy(name));
    assert.deepEqual(bad, [], directory);
  }
});
