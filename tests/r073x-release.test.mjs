import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { execFileSync, spawnSync } from "node:child_process";
import { existsSync, lstatSync, readFileSync, statSync } from "node:fs";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const python = process.env.R073X_PYTHON ?? "python3";
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
const regular = (relative) => {
  const path = resolve(root, relative);
  return existsSync(path) && lstatSync(path).isFile() && !lstatSync(path).isSymbolicLink();
};
const conflictCopy = (name) => / \d+(?=\.[^.]+$|$)/.test(name);

const title =
  "R0.73X | Localized heat ledgers with explicit exterior tails: Gaussian " +
  "velocity control, algebraic pressure tails, and the open coercivity bridge";
const publicTitle =
  "R0.73X｜带显式外部尾项的局部热账本：Gaussian 速度控制、代数压力尾与未闭合 coercivity 桥";
const sourceCommit = "958b6b4216f6914a5d42f7712b6bc9b218caf801";
const figureId = "fig-r073x-exterior-tail-ledger";
const generator = read("scripts/generate_r073x_release.py");
const currentReleaseManifest = json("research/release-manifest.json");
const publicReleaseApplied = currentReleaseManifest.latestCompletedRelease === "r073x";

const watchedDryRunPaths = [
  "VERSION",
  "research/release-manifest.json",
  "research/formal-archive-inventory.json",
  "public/site-version.json",
  "public/research-review.html",
  "public/literature-review.html",
  "public/notes/index.html",
  "public/notes/r0-73x.html",
  "public/recap-r0-61-r0-73x.html",
];

function snapshot(paths) {
  return Object.fromEntries(paths.map((relative) => {
    if (!regular(relative)) return [relative, null];
    const payload = bytes(relative);
    const status = statSync(resolve(root, relative));
    return [relative, {
      bytes: payload.length,
      sha256: sha256(payload),
      mtimeMs: status.mtimeMs,
    }];
  }));
}

function sourceDryRun() {
  return JSON.parse(runPython([
    "scripts/generate_r073x_release.py", "--source-dry-run",
  ]));
}

function pinValue(name) {
  const match = generator.match(new RegExp(
    `^${name} = (ZERO_COMMIT|"([0-9a-f]{40})")$`, "m",
  ));
  assert.ok(match, `${name} pin slot`);
  return match[1] === "ZERO_COMMIT" ? null : match[2];
}

test("release tooling freezes the X transaction, local translation path, and manifest-driven CI", () => {
  const content = read("scripts/r073x_release_content.py");
  const translation = read("scripts/add-r073x-translations.mjs");
  const binder = read("scripts/bind-r073x-pdfs.mjs");
  const renderer = read("scripts/render-note-pdf.mjs");
  const runner = read("scripts/run-release-publication-gate.mjs");
  const scientificGate = read("tests/r073x-exterior-tail-gate.test.mjs");
  const invariant = read("tests/release-publication-invariant.test.mjs");
  const tooling = [content, generator, translation, binder, scientificGate].join("\n");

  for (const token of [
    title,
    publicTitle,
    sourceCommit,
    "R073W_BASELINE",
    figureId,
    "r073x-formal-evidence-manifest-v1",
    "r073x-exterior-tail-ledger-contract-v1",
    "r073x-exterior-tail-ledger-manifest-v1",
    "r073x-exterior-tail-ledger-validation-v1",
    "r073x-exterior-tail-ledger-results-v1",
    "LOCAL_DIRECT_NO_DGX",
    "tests/r073x-exterior-tail-gate.test.mjs",
    "tests/r073x-release.test.mjs",
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
  assert.match(invariant, /\\d\+/);
  for (const workflow of [
    ".github/workflows/pages.yml",
    ".github/workflows/release-publication-gate.yml",
  ]) assert.ok(read(workflow).includes("node scripts/run-release-publication-gate.mjs"));
});

test("source dry-run freezes 1.64 and 200/140/102/78/24 without touching public files", () => {
  const before = snapshot(watchedDryRunPaths);
  const result = sourceDryRun();
  const after = snapshot(watchedDryRunPaths);
  assert.deepEqual(after, before, "--source-dry-run must not rewrite any watched target");

  assert.equal(result.release, "R0.73X");
  assert.equal(result.siteVersion, "1.64");
  assert.equal(result.mode, "source-dry-run");
  assert.equal(result.title, title);
  assert.equal(result.publicTitleZh, publicTitle);
  assert.deepEqual(result.baselineAccounting, {
    latestCompletedRelease: "r073w",
    siteVersion: "1.63",
    publicHtmlNoteCount: 199,
    postR060RecapNodeCount: 139,
    nextRelease: "r073x",
    postR070APublishedReleaseCount: 101,
    postR070AFormalSealedReleaseCount: 77,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.deepEqual(result.targetAccounting, {
    latestCompletedRelease: "r073x",
    siteVersion: "1.64",
    publicHtmlNoteCount: 200,
    postR060RecapNodeCount: 140,
    nextRelease: "r073y",
    postR070APublishedReleaseCount: 102,
    postR070AFormalSealedReleaseCount: 78,
    legacyFormalFigureBacklogCount: 24,
  });
  assert.equal(result.canonicalSources.length, 18);
  assert.equal(result.plannedAuditPaths.length, 2);
  assert.equal(result.certificateArchivePaths.length, 16);
  assert.equal(result.figureSourcePaths.length, 10);
  assert.equal(result.figureRawResultPaths.length, 11);
  assert.equal(result.figurePackagePaths.length, 25);
  assert.equal(result.coreOutputsPlanned.length, 11);
  assert.equal(result.figureResearchArchiveOutputsPlanned.length, 25);
  assert.equal(result.figurePublicArchiveOutputsPlanned.length, 25);
  assert.equal(result.figurePublicAssetOutputsPlanned.length, 3);
  assert.equal(result.laterStageOutputsPlanned.length, 8);
  assert.equal(result.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(result.dgxUsed, false);
  assert.equal(result.clayConclusion, "OPEN");
  assert.equal(result.publicTransaction, "IN_MEMORY_GATE_THEN_ATOMIC_REPLACE_WITH_ROLLBACK");
  assert.match(result.releaseApplication, /FAIL_CLOSED/i);
  assert.equal(result.published, false);
  assert.equal(result.writes, 0);

  const blockers = [
    ...(result.readinessFailures ?? []),
    ...(result.commitPinBlockers ?? []),
    result.certificate?.pending,
    result.figure?.pending,
  ].filter(Boolean);
  if (!result.publicationReady || !result.commitPinsReady || !result.figure.formal) {
    assert.ok(blockers.length > 0, "every incomplete formal layer must name a blocker");
    assert.ok(blockers.every((row) => typeof row === "string" && row.trim().length > 0));
  }
  if (result.zeroCommitLayers.length > 0) {
    assert.equal(result.commitPinsReady, false);
    assert.ok(result.commitPinBlockers.length >= result.zeroCommitLayers.length);
  }
  if (!result.figure.formal) assert.match(result.figure.pending ?? "", /figure|seal|pin|immutable/i);
  if (!result.publicationReady) assert.ok(result.readinessFailures.length > 0);
});

test("canonical reader extraction keeps 18 sources, 11 sections, and hands off only to R0.73Y", () => {
  const result = pythonJson(String.raw`
import json,sys
sys.path.insert(0,"scripts")
import generate_r073x_release as g
from r073x_release_content import load_release_content
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
  assert.equal(result.next, "R0.73Y");
  assert.equal(result.sourceCount, 18);
  assert.match(result.nextGate, /coerciv|cutoff|weighted|endpoint|epsilon|闭合|压力|尺度/iu);
  assert.match(result.home, /Gaussian|pressure|positive-scale|正尺度/iu);
  assert.match(result.recap, /Gaussian|pressure|coerciv|OPEN|尾/iu);
  assert.match(result.literature, /新颖性|优先权|novelty|priority|literature/iu);
  assert.equal(result.ready, result.failures.length === 0);
});

test("full in-memory generation remains fail-closed until every immutable layer is sealed", () => {
  const dry = sourceDryRun();
  const completed = spawnSync(
    python,
    ["-B", "scripts/generate_r073x_release.py", "--check-only"],
    {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, PYTHONDONTWRITEBYTECODE: "1" },
    },
  );
  const fullyReady = dry.commitPinsReady && dry.publicationReady && dry.figure.formal &&
    dry.certificate?.sourceBoundHashSealed === true && dry.releaseSourceReady;

  if (!fullyReady) {
    assert.notEqual(completed.status, 0);
    assert.match(
      `${completed.stderr}\n${completed.stdout}`,
      /ZERO_COMMIT|unsealed|pending|provisional|missing|seal|pin|source|package|publication-ready/i,
    );
  } else {
    assert.equal(completed.status, 0, completed.stderr);
    const result = JSON.parse(completed.stdout);
    assert.equal(result.release, "R0.73X");
    assert.equal(result.siteVersion, "1.64");
    assert.equal(result.checkOnly, true);
    assert.equal(result.transaction, "IN_MEMORY_ONLY");
    assert.equal(result.stagedOutputs, 64);
    assert.equal(Object.keys(result.stagedSha256).length, 64);
    assert.equal(result.writes, 0);
  }
});

test("all mutable commit slots are explicit and never disguised zero hashes", () => {
  assert.equal(pinValue("FINITE_SOURCE_COMMIT"), sourceCommit);
  const figureSourcePin = pinValue("FIGURE_SOURCE_COMMIT");
  if (figureSourcePin !== null) assert.doesNotMatch(figureSourcePin, /^0{40}$/);
  for (const name of [
    "FINITE_PACKAGE_COMMIT", "FINAL_CONTENT_COMMIT", "FIGURE_PACKAGE_COMMIT",
    "RELEASE_SOURCE_COMMIT",
  ]) {
    const value = pinValue(name);
    if (value !== null) assert.doesNotMatch(value, /^0{40}$/);
  }
  assert.match(generator, /FINAL_CONTENT_COMMIT_STATUS\s*=\s*"(?:PENDING|IMMUTABLE)/);
});

test("local translation and PDF binding either reproduce X or stop before public apply", () => {
  for (const script of [
    "scripts/add-r073x-translations.mjs",
    "scripts/bind-r073x-pdfs.mjs",
  ]) {
    execFileSync(node, ["--check", script], { cwd: root, stdio: "pipe" });
    const help = spawnSync(node, [script, "--help"], { cwd: root, encoding: "utf8" });
    assert.equal(help.status, 0, `${script}: ${help.stderr}`);
    assert.match(help.stdout, /usage|R0\.73X/i);

    const checked = spawnSync(node, [script, "--check-only"], {
      cwd: root,
      encoding: "utf8",
    });
    if (publicReleaseApplied) {
      assert.equal(checked.status, 0, `${script}: ${checked.stderr}`);
      const result = JSON.parse(checked.stdout);
      assert.equal(result.dgxUsed, false);
    } else {
      assert.notEqual(checked.status, 0, `${script} must fail before the X public apply`);
      assert.match(
        `${checked.stderr}\n${checked.stdout}`,
        /snapshot.*absent|HTML\/accounting|must precede|missing|stale|sealed|figure|certificate/i,
      );
    }
  }
});

test("published X binds exact accounting, reader routes, formal figure, and synchronized PDFs", (t) => {
  if (!publicReleaseApplied) {
    t.skip("R0.73X is not publicly applied; source-dry-run and fail-closed gates are active");
    return;
  }

  const release = json("research/release-manifest.json");
  const site = json("public/site-version.json");
  const expected = {
    latestCompletedRelease: "r073x",
    siteVersion: "1.64",
    publicHtmlNoteCount: 200,
    postR060RecapNodeCount: 140,
    nextRelease: "r073y",
    postR070APublishedReleaseCount: 102,
    postR070AFormalSealedReleaseCount: 78,
    legacyFormalFigureBacklogCount: 24,
  };
  for (const [key, value] of Object.entries(expected)) assert.equal(release[key], value, key);
  assert.equal(release.latestReleaseGate, "tests/r073x-exterior-tail-gate.test.mjs");
  assert.equal(release.latestReleasePublicationTest, "tests/r073x-release.test.mjs");
  assert.equal(site.version, "1.64");
  assert.equal(site.latestRelease, "R0.73X");
  assert.equal(site.publicHtmlNoteCount, 200);
  assert.equal(read("VERSION"), "1.64\n");

  const note = read("public/notes/r0-73x.html");
  const recap = read("public/recap-r0-61-r0-73x.html");
  const home = read("public/research-review.html");
  const literature = read("public/literature-review.html");
  const index = read("public/notes/index.html");
  assert.ok(note.includes(publicTitle));
  assert.ok(note.includes(`\/assets\/r073x\/${figureId}.pdf`.replaceAll("\\/", "/")));
  assert.ok(note.includes("pressureExteriorTailSizeLemma=PASS_AT_POSITIVE_SCALE"));
  assert.ok(note.includes("signedToAbsoluteCoercivity=OPEN"));
  assert.ok(note.includes("/notes/r0-73x.pdf"));
  assert.equal(recap.match(/class="node-ref"/g)?.length, 140);
  assert.equal(index.match(/<li class="note-entry"/g)?.length, 200);
  for (const token of [
    "R0.61–R0.73X", "140 个节点", "200 篇公开研究笔记", "59 个阶段",
    "102 个版本已公开", "78 个按当前 formal-figure 合同完整封存",
  ]) assert.ok(home.includes(token), token);
  assert.ok(literature.includes("开放接口 · R0.73Y"));
  assert.equal(home.match(/data-release="r073x"/g)?.length, 1);

  for (const relative of [
    `public/assets/r073x/${figureId}.pdf`,
    `public/assets/r073x/${figureId}.png`,
    `public/assets/r073x/${figureId}.svg`,
    "public/notes/r0-73x.pdf",
    "public/recap-r0-61-r0-73x.pdf",
  ]) assert.equal(regular(relative), true, relative);

  const bindings = json("research/r073x_pdf_bindings.json");
  assert.equal(bindings.schemaVersion, "r073x-synchronized-pdf-bindings-v1");
  assert.equal(bindings.release, "R0.73X");
  assert.equal(bindings.documents.length, 2);
  const boundary = bindings.claimBoundary;
  assert.equal(boundary.htmlAndPdfBytesCryptographicallyBound, true);
  assert.equal(boundary.pressureExteriorTailSizeLemma, "PASS_AT_POSITIVE_SCALE");
  assert.equal(boundary.positiveScaleAbsoluteSize, "PROVED");
  assert.equal(boundary.compactCutoffQuadraticAbsorption, "OPEN");
  assert.equal(boundary.translatedPacketCounterexample, "FUNCTIONAL_ONLY_NOT_NSE");
  assert.equal(boundary.associatedPressureCounterexample, "NOT_CLAIMED");
  assert.equal(boundary.signedToAbsoluteCoercivity, "OPEN");
  assert.equal(boundary.weightedTentCarlesonControl, "OPEN");
  assert.equal(boundary.suitableWeakZeroScaleEndpoint, "OPEN");
  assert.equal(boundary.epsilonRegularity, "OPEN");
  assert.equal(
    boundary.formalEvidenceCertificate,
    "SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED",
  );
  assert.equal(boundary.navierStokesSimulation, false);
  assert.equal(boundary.directNumericalSimulation, false);
  assert.equal(boundary.clayConclusion, "OPEN");
  assert.equal(boundary.clayProblemSolved, false);
  assert.equal(boundary.ordinaryTranslationPath, "LOCAL_DIRECT_NO_DGX");
  assert.equal(boundary.dgxUsed, false);
  assert.ok(Number.isInteger(boundary.formalFigureChecks) && boundary.formalFigureChecks > 0);
  assert.ok(Number.isInteger(boundary.formalFigureRows) && boundary.formalFigureRows > 0);
  for (const document of bindings.documents) {
    assert.equal(regular(document.html.path), true, document.html.path);
    assert.equal(regular(document.pdf.path), true, document.pdf.path);
    assert.equal(sha256(bytes(document.html.path)), document.html.sha256, document.html.path);
    assert.equal(sha256(bytes(document.pdf.path)), document.pdf.sha256, document.pdf.path);
    assert.ok(document.pdf.pageCount > 0, document.pdf.path);
    assert.ok(document.pdf.bytes > 10_000, document.pdf.path);
  }

  for (const directory of [
    "public/assets/r073x",
    `public/figures/r073x/${figureId}`,
    "public/research/r073x",
    `research/figures/r073x/${figureId}`,
  ]) {
    const tracked = execFileSync("git", ["ls-files", "-z", "--", directory], {
      cwd: root,
      encoding: "utf8",
    }).split("\0").filter(Boolean);
    assert.equal(tracked.some(conflictCopy), false, directory);
  }
  for (const directory of ["public", "public/notes", "research", "scripts/i18n-snapshots"]) {
    const bad = execFileSync("git", ["ls-files", "-z", "--", directory], {
      cwd: root,
      encoding: "utf8",
    }).split("\0").filter(Boolean)
      .filter((name) => /r073x|r0-73x/i.test(name) && conflictCopy(name));
    assert.deepEqual(bad, [], directory);
  }
});
