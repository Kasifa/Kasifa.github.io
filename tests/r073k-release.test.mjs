import assert from "node:assert/strict";
import { spawnSync } from "node:child_process";
import { createHash } from "node:crypto";
import { copyFile, mkdir, mkdtemp, readFile, rm, writeFile } from "node:fs/promises";
import { tmpdir } from "node:os";
import { dirname, resolve } from "node:path";
import test from "node:test";
import { fileURLToPath } from "node:url";
import { containsChinese, extractProtectedTokens } from "../scripts/i18n-lib.mjs";

const root = resolve(dirname(fileURLToPath(import.meta.url)), "..");
const text = (relative) => readFile(resolve(root, relative), "utf8");
const json = async (relative) => JSON.parse(await text(relative));
const bytes = (relative) => readFile(resolve(root, relative));

const figureId = "fig-r073k-uniform-viscous-branch";
const figureRoot = "figures/r073k/" + figureId;
const mirrorRoot = "public/" + figureRoot;
const publicFigureRoot = "public/assets/r073k/" + figureId;
const publicPages = {
  note: "public/notes/r0-73k.html",
  recap: "public/recap-r0-61-r0-73k.html",
  home: "public/research-review.html",
  literature: "public/literature-review.html",
  index: "public/notes/index.html",
};
const target = {
  version: "1.51", latest: "r073k", notes: 187, recap: 127,
  published: 89, sealed: 65, backlog: 24, next: "r073l",
};
const forbidden = [
  "我们", "攻关", "主攻", "突破", "研究纪律", "三重审计", "杀死错误想法",
  "颠覆性", "世界首个", "接近解决", "解决了千禧年", "证明了全局正则性",
  "原创性定理", "首次证明",
];

function assertPublicVoice(value, label) {
  for (const phrase of forbidden) assert.equal(value.includes(phrase), false, label + ": " + phrase);
  assert.doesNotMatch(value, /\b(?:we|our|ours|ourselves|us)\b/i, label + ": collective English voice");
}

function machineLedgerAssignments(value) {
  return [...value.matchAll(/\b([A-Za-z][A-Za-z0-9]*)=([A-Z0-9][A-Z0-9_]*)\b/g)]
    .map((match) => match[0]);
}

function recapNodes(recap) {
  const start = recap.indexOf('<section id="node-index">');
  const end = recap.indexOf("</section>", start);
  assert.ok(start >= 0 && end > start, "recap node-index section");
  return [...recap.slice(start, end).matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
}

function decodeUtf16Be(payload) {
  const start = payload[0] === 0xfe && payload[1] === 0xff ? 2 : 0;
  const littleEndian = Buffer.alloc(payload.length - start);
  for (let index = start; index < payload.length; index += 2) {
    littleEndian[index - start] = payload[index + 1];
    littleEndian[index - start + 1] = payload[index];
  }
  return littleEndian.toString("utf16le");
}

async function assertPdf(relative, expectedTitle) {
  const value = await bytes(relative);
  assert.ok(value.length > 10_000, relative + ": substantive PDF");
  assert.equal(value.subarray(0, 4).toString(), "%PDF", relative);
  const match = value.toString("latin1").match(/\/Title\s*<([0-9A-Fa-f]+)>/);
  assert.ok(match, relative + ": PDF title metadata");
  assert.equal(decodeUtf16Be(Buffer.from(match[1], "hex")), expectedTitle, relative);
}

test("R0.73K pins the v1.51 accounting endpoint", async () => {
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
  assert.equal(release.latestReleaseGate, "tests/r073k-uniform-viscous-branch-gate.test.mjs");
  assert.equal(release.latestReleasePublicationTest, "tests/r073k-release.test.mjs");
  assert.deepEqual(
    { version: site.version, latest: site.latestRelease, notes: site.publicHtmlNoteCount },
    { version: "1.51", latest: "R0.73K", notes: 187 },
  );
  assert.equal(site.publishedDate, "2026-08-31");
  assert.equal(inventory.latestPublishedRelease, "r073k");
  assert.equal(inventory.publishedReleaseCount, 89);
  assert.equal(inventory.formalSealedReleaseCount, 65);
  assert.equal(inventory.legacyFormalFigureBacklogCount, 24);
  assert.equal(version, "1.51\n");
});

test("R0.73K release source pins every executable and global-gate dependency", async () => {
  const generator = await text("scripts/generate_r073k_release.py");
  const block = generator.match(/RELEASE_SOURCE_EXACT_PATHS = \(\n([\s\S]*?)\n\)/);
  assert.ok(block, "RELEASE_SOURCE_EXACT_PATHS block");
  const pinnedPaths = [...block[1].matchAll(/^\s+"([^"]+)",$/gm)]
    .map((match) => match[1]);
  assert.deepEqual(pinnedPaths, [
    ".github/workflows/pages.yml",
    ".github/workflows/release-publication-gate.yml",
    "research/validate_figure_package.py",
    "scripts/r073k_release_content.py",
    "scripts/add-r073k-translations.mjs",
    "scripts/generate_r073k_release.py",
    "scripts/generate_r072o_release.py",
    "scripts/generate_r072p_release.py",
    "scripts/generate_note_index.py",
    "scripts/i18n-lib.mjs",
    "scripts/render-note-pdf.mjs",
    "scripts/bind-r073k-pdfs.mjs",
    "scripts/run-release-publication-gate.mjs",
    "tests/bilingual-content.test.mjs",
    "tests/internal-public-links.test.mjs",
    "tests/release-publication-gate-runner.test.mjs",
    "tests/release-publication-invariant.test.mjs",
    "tests/r073k-uniform-viscous-branch-gate.test.mjs",
    "tests/r073k-release.test.mjs",
    "tests/site-route-current-boundary.test.mjs",
  ]);
  for (const name of [
    "ANALYTIC_SOURCE_COMMIT", "EXPERIMENT_PACKAGE_COMMIT", "FIGURE_PACKAGE_COMMIT",
    "RELEASE_BASELINE_COMMIT", "RELEASE_SOURCE_COMMIT",
  ]) assert.match(generator, new RegExp(name + ' = "[0-9a-f]{40}"'));
  assert.match(generator, /normalized_release_generator\(git_bytes\(RELEASE_SOURCE_COMMIT, generator_relative\)\)/);
});

test("R0.73K public route, recap, and claim boundary are complete", async () => {
  const [note, recap, home, literature, index] =
    await Promise.all(Object.values(publicPages).map(text));
  for (const [label, value] of Object.entries({ note, recap, home, literature, index })) {
    assert.ok(value.includes("R0.73K"), label + ": release label");
    assert.ok(value.includes("/i18n-en.js?v=1.51"), label + ": i18n v1.51");
    assertPublicVoice(value, label + " HTML");
  }
  for (const token of [
    "fullNormResolventConvergence=FALSE", "0.12", "0.16", "1/25", "9/5", "5/9",
    "1190", "952", "1.008", "0.5939991104", "uniformRankOneViscousBranch=CLOSED",
    "finiteDiagnosticPackage=CLOSED", "explicitViscosityThreshold=OPEN",
    "nonselfadjointAdiabaticTracking=OPEN", "Clay=OPEN", "NOT CLAY",
  ]) assert.ok(note.includes(token), "note token " + token);

  const nodes = recapNodes(recap);
  assert.equal(nodes.length, 127);
  assert.equal(new Set(nodes).size, 127);
  assert.equal(nodes[0], "r0-61");
  assert.equal(nodes.at(-1), "r0-73k");
  assert.equal(recap.match(/<article class="phase">/g)?.length, 46);
  assert.ok(recap.includes("回顾截止节点：R0.73K"));

  assert.ok(home.includes("LATEST RELEASE · R0.73K"));
  assert.ok(home.includes("当前端点 R0.73K"));
  assert.ok(home.includes("NEXT · R0.73L"));
  assert.ok(home.includes("parameter-uniform viscous rank-one branch"));
  assert.ok(home.includes("finite diagnostic: 1190 states / 952 cross-cutoff comparisons"));
  const route = home.match(/<nav class="route-note-links" aria-label="R0\.69P–R0\.73K">([\s\S]*?)<\/nav>/);
  assert.ok(route);
  const routeLinks = [...route[1].matchAll(/href="\/notes\/(r0-[^"]+)\.html"/g)]
    .map((match) => match[1]);
  assert.equal(routeLinks.length, 97);
  assert.equal(new Set(routeLinks).size, 97);
  assert.ok(literature.includes('id="r073k-boundary"'));
  assert.ok(literature.includes('class="route-r073k-deck-update"'));
  for (let number = 156; number <= 166; number += 1) {
    assert.equal(
      [...literature.matchAll(new RegExp('id="ref-' + number + '"', "g"))].length,
      1, "ref-" + number,
    );
  }
  const literatureIds = [...literature.matchAll(/\bid="([^"]+)"/g)].map((match) => match[1]);
  assert.equal(new Set(literatureIds).size, literatureIds.length, "literature ids unique");
  assert.ok(index.includes('data-note="r0-73k"'));
  assert.ok(index.includes("187 篇公开研究笔记"));
});

test("R0.73K figure mirrors are byte-identical and synchronized PDFs exist", async () => {
  for (const name of [
    "README.md", "SHA256SUMS", "caption.md", "command.txt", "config.json", "contract.json",
    "environment.json", "figure.pdf", "figure.png", "figure.svg", "manifest.json", "plot.py",
    "progress.ndjson", "qa-final-size.png", "qa-grayscale.png", "qa-pdf.png", "qa-protocol.md",
    "qa-report.md", "requirements.txt", "resource-log.ndjson", "results.json", "source-data.csv",
    "validate.py", "validation.json",
  ]) {
    assert.deepEqual(await bytes(mirrorRoot + "/" + name), await bytes(figureRoot + "/" + name), "mirror " + name);
  }
  for (const suffix of ["pdf", "svg", "png"]) {
    assert.deepEqual(
      await bytes(publicFigureRoot + "." + suffix),
      await bytes(figureRoot + "/figure." + suffix),
      suffix + " web master",
    );
  }
  await assertPdf(
    "public/notes/r0-73k.pdf",
    "R0.73K｜Parameter-uniform viscous rank-one branch",
  );
  await assertPdf(
    "public/recap-r0-61-r0-73k.pdf",
    "R0.61–R0.73K｜R0.60 之后的研究回顾",
  );
  const binding = await json("research/r073k_pdf_bindings.json");
  assert.equal(binding.schemaVersion, "r073k-synchronized-pdf-bindings-v1");
  assert.equal(binding.release, "R0.73K");
  assert.equal(binding.documents.length, 2);
  for (const row of binding.documents) {
    for (const record of [row.html, row.pdf]) {
      const payload = await bytes(record.path);
      assert.equal(payload.length, record.bytes, record.path + ": bytes");
      assert.equal(createHash("sha256").update(payload).digest("hex"), record.sha256, record.path);
    }
  }
  const bindingCheck = spawnSync(
    process.execPath, ["scripts/bind-r073k-pdfs.mjs", "--check-only"],
    { cwd: root, encoding: "utf8" },
  );
  assert.equal(bindingCheck.status, 0, bindingCheck.stderr);
});

test("R0.73K finite evidence remains separate from the continuum theorem", async () => {
  const [experiment, primary, independent, figure, results, validation] = await Promise.all([
    json("experiments/r073k/manifest.json"),
    json("experiments/r073k/viscous_branch_diagnostic.json"),
    json("experiments/r073k/independent_validation.json"),
    json(figureRoot + "/manifest.json"),
    json(figureRoot + "/results.json"),
    json(figureRoot + "/validation.json"),
  ]);
  assert.equal(experiment.status, "sealed");
  assert.equal(experiment.claimBoundary.continuumTheoremCertifiedByThisManifest, false);
  assert.equal(primary.rows.length, 1190);
  assert.equal(primary.crossCutoffComparisons.length, 952);
  assert.equal(primary.claimBoundary.fixedCircleCountIsContinuumRieszRankProof, false);
  assert.equal(independent.validator.importsPrimaryProducer, false);
  assert.equal(independent.allChecksPass, true);
  assert.equal(figure.status, "formal");
  assert.equal(figure.publication.publicCopiesComplete, true);
  assert.equal(figure.claimBoundary.finiteDimensionalDiagnostic, true);
  assert.equal(figure.claimBoundary.continuumViscousBranchCertifiedByFigure, false);
  assert.equal(results.rowCounts.sourceData, 213);
  assert.equal(results.allChecksPass, true);
  assert.equal(validation.allChecksPass, true);
  assert.equal(Object.keys(validation.checks).length, 22);
});

test("R0.73K translations and browser bundle are synchronized and public-safe", async () => {
  const [translations, bundle, ...htmlPages] = await Promise.all([
    json("translations/en.json"), text("public/i18n-en.js"),
    ...Object.values(publicPages).map(text),
  ]);
  const rows = translations.filter((entry) => /^r073k\d+$/.test(entry.id));
  assert.ok(rows.length > 0, "R0.73K translation rows");
  assert.equal(new Set(rows.map((entry) => entry.id)).size, rows.length);
  assert.equal(new Set(rows.map((entry) => entry.zh)).size, rows.length);
  for (const [index, entry] of rows.entries()) {
    const label = "R0.73K translation row " + String(index + 1);
    assert.ok(typeof entry.en === "string" && entry.en.trim(), label + ": en");
    assert.equal(containsChinese(entry.en), false, label + ": Chinese in English");
    assert.doesNotMatch(entry.en, /\b(?:we|our|ours|ourselves|us)\b/i, label);
    assert.deepEqual(extractProtectedTokens(entry.en), extractProtectedTokens(entry.zh), label + ": protected tokens");
    assert.deepEqual(machineLedgerAssignments(entry.en), machineLedgerAssignments(entry.zh), label + ": machine ledgers");
    assert.ok(
      bundle.includes(JSON.stringify(entry.zh) + ": " + JSON.stringify(entry.en)),
      label + ": browser bundle",
    );
  }
  assertPublicVoice(JSON.stringify(rows), "R0.73K translations");
  for (const [index, value] of htmlPages.entries()) {
    assertPublicVoice(value, "public HTML " + String(index + 1));
  }
});

test("R0.73K note-index generation reads the frozen baseline, not poisoned live notes", async () => {
  const scratch = await mkdtemp(resolve(tmpdir(), "r073k-release-root-"));
  try {
    const notes = resolve(scratch, "public/notes");
    await mkdir(notes, { recursive: true });
    await writeFile(
      resolve(notes, "r0-73j.html"),
      "<title>R0.73J｜POISONED LIVE NOTE</title>",
    );
    await copyFile(resolve(root, "public/site-version.json"), resolve(scratch, "public/site-version.json"));
    const code = [
      "import json",
      "from pathlib import Path",
      "import generate_r073k_release as g",
      "g.PUBLIC=Path(" + JSON.stringify(resolve(scratch, "public")) + ")",
      "payload=json.dumps({'schemaVersion':'research-site-version-v1','version':'1.51','latestRelease':'R0.73K','publicHtmlNoteCount':187,'publishedDate':'2026-08-31'}).encode()",
      "value=g.build_note_index(payload)",
      "assert 'data-note=\"r0-73k\"' in value",
      "assert 'POISONED LIVE NOTE' not in value",
      "assert 'data-note=\"r0-73j\"' in value",
      "print('frozen-baseline-ok')",
    ].join("\n");
    const run = spawnSync("python3", ["-c", code], {
      cwd: root,
      encoding: "utf8",
      env: { ...process.env, PYTHONPATH: resolve(root, "scripts") },
    });
    assert.equal(run.status, 0, run.stderr);
    assert.match(run.stdout, /frozen-baseline-ok/);
  } finally {
    await rm(scratch, { recursive: true, force: true });
  }
});

test("R0.73K HTML transaction rolls back an injected replace failure", () => {
  const code = [
    "import tempfile",
    "from pathlib import Path",
    "import generate_r073k_release as g",
    "with tempfile.TemporaryDirectory() as raw:",
    "    g.ROOT=Path(raw).resolve()",
    "    first=g.ROOT/'first.txt'",
    "    second=g.ROOT/'nested'/'second.txt'",
    "    second.parent.mkdir()",
    "    first.write_bytes(b'old-first')",
    "    second.write_bytes(b'old-second')",
    "    original=g.os.replace",
    "    calls={'count': 0}",
    "    def flaky(source, target):",
    "        calls['count'] += 1",
    "        if calls['count'] == 2:",
    "            raise OSError('injected replace failure')",
    "        return original(source, target)",
    "    g.os.replace=flaky",
    "    try:",
    "        g.commit_transaction({first:b'new-first', second:b'new-second'})",
    "    except OSError as error:",
    "        assert 'injected' in str(error)",
    "    else:",
    "        raise AssertionError('injected failure did not fire')",
    "    finally:",
    "        g.os.replace=original",
    "    assert first.read_bytes() == b'old-first'",
    "    assert second.read_bytes() == b'old-second'",
    "    assert not list(g.ROOT.rglob('*.tmp'))",
    "print('rollback-ok')",
  ].join("\n");
  const run = spawnSync("python3", ["-c", code], {
    cwd: root,
    encoding: "utf8",
    env: { ...process.env, PYTHONPATH: resolve(root, "scripts") },
  });
  assert.equal(run.status, 0, run.stderr);
  assert.match(run.stdout, /rollback-ok/);
});
