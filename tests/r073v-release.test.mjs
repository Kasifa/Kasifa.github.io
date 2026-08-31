import assert from "node:assert/strict";
import { execFileSync, spawnSync } from "node:child_process";
import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const python = process.env.R073V_PYTHON ?? "python3";
const node = process.execPath;
const read = (relative) => readFileSync(resolve(root, relative), "utf8");
const runPython = (args) => execFileSync(python, ["-B", ...args], {
  cwd: root,
  encoding: "utf8",
  env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
});
const pythonJson = (source) => JSON.parse(runPython(["-c", source]));

const title =
  "R0.73V | A pressure-aware signed third-order heat lift: exact scale " +
  "generation and the 3→4 physical-time boundary";
const publicTitle =
  "R0.73V｜压力感知的有符号三阶热提升：精确尺度生成律与 3→4 物理时间边界";
const pins = Object.freeze({
  baseline: "ebc75b1614994d09eafd60ac926469dcebb54b94",
  analytic: "25636c886f1ee2449418b5548b42f9f0fa269b47",
  finiteSource: "7c445c522a241bdc8b867b6fce0f0fed9b82e97d",
  finitePackage: "b34d91ea96c257b943f11d134e8024138e5f3cb0",
  figureSource: "f94915332ff405ae723711e8041acc2af07e896b",
  figurePackage: "ae679d5afa5f3cfacfe79c4d7b8a462baca2c195",
  finalContent: "482905ed7a9dcc3cc337d5ba17f73af5ac61c60f",
});

const generator = read("scripts/generate_r073v_release.py");
const sourcePinMatch = generator.match(
  /^RELEASE_SOURCE_COMMIT = (ZERO_COMMIT|"([0-9a-f]{40})")$/m,
);
assert.ok(sourcePinMatch, "release-source pin slot");
const sourcePinReady = sourcePinMatch[1] !== "ZERO_COMMIT";

test("R0.73V release tooling freezes the exact source chain and local translation route", () => {
  const content = read("scripts/r073v_release_content.py");
  const translation = read("scripts/add-r073v-translations.mjs");
  const binder = read("scripts/bind-r073v-pdfs.mjs");
  const scientificGate = read("tests/r073v-signed-third-order-interface-gate.test.mjs");
  const tooling = [content, generator, translation, binder].join("\n");
  const corpus = [tooling, scientificGate].join("\n");

  for (const token of [
    title,
    publicTitle,
    ...Object.values(pins),
    "R073U_BASELINE",
    "LOCAL_DIRECT_NO_DGX",
    "dgxUsed: false",
    "formalFigureChecks=147",
    "formalFigureRows=158",
    "public/research/r073v/r073v_figure_source_audit.md",
    "public/research/r073v/r073v_figure_source_reaudit.md",
    ".github/workflows/pages.yml",
    ".github/workflows/release-publication-gate.yml",
  ]) assert.ok(corpus.includes(token), token);

  for (const stale of [
    "R073T_BASELINE",
    "research/r073v_tensor_heat_hierarchy.md",
    "fig-r073v-tensor-heat-hierarchy",
    "INITIAL_TIME_BOUNDARY_ZH",
  ]) assert.equal(tooling.includes(stale), false, stale);

  assert.equal(translation.includes("node:child_process"), false);
  assert.doesNotMatch(translation, /\bfetch\s*\(|https?\.request|\bspawn\s*\(|\bexec\s*\(/);
  assert.ok(translation.includes("translationPath: translationRoute"));
  assert.ok(translation.includes("dgxUsed: false"));
  assert.ok(binder.includes("ordinaryTranslationPath: \"LOCAL_DIRECT_NO_DGX\""));
  assert.ok(binder.includes("dgxUsed: false"));
});

test("source dry-run reports the U-to-V accounting transition without writes", () => {
  const result = JSON.parse(runPython([
    "scripts/generate_r073v_release.py", "--source-dry-run",
  ]));
  assert.equal(result.release, "R0.73V");
  assert.equal(result.siteVersion, "1.62");
  assert.equal(result.title, title);
  assert.equal(result.publicTitleZh, publicTitle);
  assert.deepEqual(result.baselineAccounting, {
    latestCompletedRelease: "r073u",
    siteVersion: "1.61",
    publicHtmlNoteCount: 197,
    postR060RecapNodeCount: 137,
    nextRelease: "r073v",
    postR070APublishedReleaseCount: 99,
    postR070AFormalSealedReleaseCount: 75,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.deepEqual(result.targetAccounting, {
    latestCompletedRelease: "r073v",
    siteVersion: "1.62",
    publicHtmlNoteCount: 198,
    postR060RecapNodeCount: 138,
    nextRelease: "r073w",
    postR070APublishedReleaseCount: 100,
    postR070AFormalSealedReleaseCount: 76,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.equal(result.publicationReady, true);
  assert.deepEqual(result.readinessFailures, []);
  assert.equal(result.certificate.finalSeal, true);
  assert.equal(result.certificate.checks.exact, 66);
  assert.equal(result.figure.formal, true);
  assert.equal(result.figure.validationChecks, 147);
  assert.equal(result.figure.sourceCommitAssigned, true);
  assert.equal(result.canonicalSources, 8);
  assert.equal(result.sections, 9);
  assert.equal(result.releaseSourceReady, true);
  assert.equal(result.commitPinsReady, sourcePinReady);
  assert.equal(result.publicTransactionImplemented, true);
  assert.equal(result.coreOutputsPlanned.length, 11);
  assert.equal(result.figureOutputsPlanned.length, 5);
  assert.equal(new Set(result.figureOutputsPlanned).size, 5);
  assert.equal(result.translationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(result.clayConclusion, "OPEN");
  assert.equal(result.writes, 0);
});

test("canonical reader extraction is publication-ready and keeps the claim boundary narrow", () => {
  const result = pythonJson(String.raw`
import json,sys
sys.path.insert(0,"scripts")
import generate_r073v_release as g
from r073v_release_content import load_release_content
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
  "literature":c.literature_update,
  "sourceCount":len(c.source_sha256),
},ensure_ascii=False))
`);
  assert.equal(result.title, title);
  assert.equal(result.publicTitle, publicTitle);
  assert.equal(result.sections, 9);
  assert.equal(result.ready, true);
  assert.deepEqual(result.failures, []);
  assert.equal(result.next, "R0.73W");
  assert.match(result.nextGate, /production|carr|尺度|能量/iu);
  assert.match(result.home, /压力|三阶|3→4/u);
  assert.match(result.recap, /非循环|能量|符号控制/u);
  assert.match(result.literature, /不承担新颖性或优先权声明/u);
  assert.equal(result.sourceCount, 8);
});

test("the in-memory transaction assembles 64 auditable targets and no stale U endpoint", () => {
  const result = pythonJson(String.raw`
import json,sys
sys.path.insert(0,"scripts")
import generate_r073v_release as g
from r073v_release_content import load_release_content
c=load_release_content(g.ROOT)
s=g.build_staged(c)
def text(path): return s[g.ROOT/path].decode("utf-8")
note=text("public/notes/r0-73v.html")
recap=text("public/recap-r0-61-r0-73v.html")
home=text("public/research-review.html")
lit=text("public/literature-review.html")
fig=json.loads(text("public/figures/r073v/fig-r073v-signed-third-order-interface/manifest.json"))
source_dir=g.ROOT/g.FIGURE_SOURCE_RELATIVE
names=sorted(p.name for p in source_dir.iterdir() if p.is_file())
copies_equal=all(
  s[g.ROOT/"research"/g.FIGURE_ARCHIVE_RELATIVE/name]
  ==s[g.PUBLIC/g.FIGURE_ARCHIVE_RELATIVE/name]
  for name in names
)
audit_equal=all(
  s[g.PUBLIC/"research"/"r073v"/name]
  ==(g.ROOT/"research"/name).read_bytes()
  for name in ("r073v_figure_source_audit.md","r073v_figure_source_reaudit.md")
)
print(json.dumps({
  "count":len(s),
  "html":sum(p.suffix==".html" for p in s),
  "core":all(g.ROOT/p in s for p in g.CORE_TARGET_OUTPUTS),
  "title":c.public_title_zh in note,
  "boundary":all(x in note for x in (
    "formalFiniteCertificateChecks=66","formalFigureChecks=147",
    "formalFigureRows=158","ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
    "clayConclusion=OPEN","NOT CLAY")),
  "rawFence":any(chr(96)*3 in v for v in (note,recap,home,lit)),
  "voiceBan":any(x in note+recap for x in g.PUBLIC_VOICE_BANS),
  "counts":all(x in home for x in (
    "R0.70A–R0.73V · 100 节已公开","76 节完整封存",
    "138 节累计回顾","198 篇研究笔记总索引")),
  "nextW":"<h3>R0.73W 下一接口</h3>" in home and "开放接口 · R0.73W" in lit,
  "staleNextV":"<h3>R0.73V 下一接口</h3>" in home or "开放接口 · R0.73V" in lit,
  "linkedDoi":"href=\"https://doi.org/10.1098/rspa.1938.0013\"" in lit,
  "copiesEqual":copies_equal,
  "auditEqual":audit_equal,
  "figureFiles":len(names),
  "figureId":fig.get("figureId"),
  "figureChecks":fig.get("qa",{}).get("validationChecks"),
  "figureRows":json.loads(text("public/figures/r073v/fig-r073v-signed-third-order-interface/results.json")).get("rowCount"),
  "figureSource":fig.get("git",{}).get("figureSourceCommit"),
  "publicationStatus":fig.get("publicationStatus"),
  "dgxUsed":fig.get("computePolicy",{}).get("dgxUsed"),
  "translationPath":fig.get("computePolicy",{}).get("ordinaryTranslationPath"),
},ensure_ascii=False))
`);
  assert.equal(result.count, 64);
  assert.equal(result.html, 5);
  assert.equal(result.core, true);
  assert.equal(result.title, true);
  assert.equal(result.boundary, true);
  assert.equal(result.rawFence, false);
  assert.equal(result.voiceBan, false);
  assert.equal(result.counts, true);
  assert.equal(result.nextW, true);
  assert.equal(result.staleNextV, false);
  assert.equal(result.linkedDoi, true);
  assert.equal(result.copiesEqual, true);
  assert.equal(result.auditEqual, true);
  assert.equal(result.figureFiles, 25);
  assert.equal(result.figureId, "fig-r073v-signed-third-order-interface");
  assert.equal(result.figureChecks, 147);
  assert.equal(result.figureRows, 158);
  assert.equal(result.figureSource, pins.figureSource);
  assert.equal(result.publicationStatus, "published");
  assert.equal(result.dgxUsed, false);
  assert.equal(result.translationPath, "LOCAL_DIRECT_NO_DGX");
});

test("the release transaction fails closed until its normalized source pin is frozen", () => {
  const completed = spawnSync(
    python,
    ["-B", "scripts/generate_r073v_release.py", "--check-only"],
    { cwd: root, encoding: "utf8", env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" } },
  );
  if (!sourcePinReady) {
    assert.notEqual(completed.status, 0);
    assert.match(completed.stderr, /unsealed 40-zero commit pin|release source/i);
  } else {
    assert.equal(completed.status, 0, completed.stderr);
    const result = JSON.parse(completed.stdout);
    assert.equal(result.release, "R0.73V");
    assert.equal(result.checkOnly, true);
    assert.equal(result.stagedOutputs, 64);
  }
});

test("translation and PDF binders are local, syntax-valid, and reproduce the sealed outputs", () => {
  for (const script of [
    "scripts/add-r073v-translations.mjs",
    "scripts/bind-r073v-pdfs.mjs",
  ]) {
    execFileSync(node, ["--check", script], { cwd: root, stdio: "pipe" });
    const help = spawnSync(node, [script, "--help"], { cwd: root, encoding: "utf8" });
    assert.equal(help.status, 0, `${script}: ${help.stderr}`);
    assert.match(help.stdout, /usage|help|R0\.73V/i);
  }
  assert.match(read("scripts/add-r073v-translations.mjs"), /LOCAL_DIRECT_NO_DGX/);
  assert.match(read("scripts/bind-r073v-pdfs.mjs"), /LOCAL_DIRECT_NO_DGX/);

  for (const script of [
    "scripts/add-r073v-translations.mjs",
    "scripts/bind-r073v-pdfs.mjs",
  ]) {
    const checked = spawnSync(node, [script, "--check-only"], {
      cwd: root,
      encoding: "utf8",
    });
    assert.equal(checked.status, 0, `${script}: ${checked.stderr}`);
    const result = JSON.parse(checked.stdout);
    assert.equal(result.dgxUsed, false);
  }
});
