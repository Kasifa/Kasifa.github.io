import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificateRoot = new URL("research/certificates/r071u/", root);
const figureRoot = new URL(
  "figures/r071u-second-jet/fig-r071u-recurrence-packing/",
  root,
);

function count(value, fragment) {
  return value.split(fragment).length - 1;
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

function assertAnchorsResolve(html, minimumUniqueTargets) {
  const idList = [...html.matchAll(/\sid="([^"]+)"/g)].map(
    (match) => match[1],
  );
  const ids = new Set(idList);
  assert.equal(ids.size, idList.length, "duplicate HTML id");
  const targets = [...html.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(new Set(targets).size >= minimumUniqueTargets);
  for (const target of targets) assert.ok(ids.has(target), target);
}

async function publishedPages() {
  const [home, note, recap, literature, previousNote] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71u.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71u.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71t.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature, previousNote };
}

test("retains R0.71U while v1.20 publishes R0.72G as current", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 157);
  assert.match(home, /<strong>v1\.20<\/strong>网页版本/);
  assert.match(home, /<strong>157<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72G<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72G<\/span>/);
  assert.match(home, /展开 67 篇公开笔记/);
  assert.match(home, /累计回顾收录 97 个节点；全站现有 157 篇公开研究笔记/);
  assert.match(home, /R0\.70A–R0\.72G 共 59 个版本已公开；按当前 formal-figure 合同有 35 个完整封存，24 个旧版附图档案列入回补清单/);
  assert.match(home, /NEXT · R0\.72H/);

  const route = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72G">([\s\S]*?)<\/nav>/,
  );
  assert.ok(route);
  assert.equal(count(route[1], 'href="/notes/'), 67);
  assert.equal(count(route[1], 'href="/notes/r0-71u.html"'), 1);
  assert.equal(count(home, 'data-release="r071u"'), 1);
  assert.equal(count(home, 'href="/notes/r0-71u.html"'), 2);

  assert.ok(count(recap, '<article class="phase">') >= 12);
  assert.match(recap, /收录节点：85/);
  assert.match(recap, /回顾截止时公开笔记：145/);
  assert.match(recap, /R0\.70A–R0\.71U 完成版本/);
  assert.match(recap, /R0\.00–R0\.60 的内容保留在上一份阶段回顾中/);
  assert.match(literature, /R0\.69P–R0\.72G/);
  assert.match(literature, /开放接口 · R0\.72H/);

  for (const [page, minimum, version] of [
    [home, 10, "1.20"],
    [note, 14, "1.06"],
    [recap, 8, "1.06"],
    [literature, 50, "1.20"],
  ]) {
    assertAnchorsResolve(page, minimum);
    assert.ok(page.includes('src="/i18n-en.js?v=' + version + '"'));
    assert.doesNotMatch(page, /我们|攻关|主攻|三重审计/);
    assert.doesNotMatch(page, /千禧年问题已经解决|解决了千禧年问题/);
  }
});

test("states the classical second-jet theorem and exact recurrence with correct quantifiers", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "\\frac2\\ell\\int_I\\|X'\\|_H^2",
    "\\frac{7\\ell}{3}",
    "0&lt;\\inf_KY\\le\\sup_KY&lt;\\infty",
    "\\kappa_j^{-6}\\|C_{j,tt}\\|_2^2",
    "ordinary Leray energy inequality 不控制",
    "integer \\(\\lambda\\)",
    "classical trace 允许零点落在闭区间端点",
    "每个 finite set 和每个 \\(N\\) 可以选择一个新解",
    "unit energy–enstrophy ball",
    "这不是 weighted-atom counterexample",
    "single-trajectory infinite recurrence",
    "这不是千禧年问题的解答",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /trajectory-wise classical estimate/is);
  assert.match(note, /不是弱解定理/is);
  assert.match(note, /第一行.*Leray.*第二行.*recurrence tax/is);
  assert.match(note, /每个(?:给定 )?finite time set.*选择一个新的真实无外力 NSE 解/is);
  assert.match(note, /atom.*随.*增加.*缩小/is);
  assert.match(home, /R0\.71U 已完成.*classical second-time-jet.*不排除 weighted packing/is);
  assert.match(recap, /每个 finite set 可选择新解/is);
  assert.match(
    literature,
    /<b>R0\.71U<\/b>.*classical second-time jet.*raw count 无统一界/is,
  );
});

test("retains the exact-thin and complete finite-support correction for R0.71T", async () => {
  const { home, note, literature, previousNote } = await publishedPages();
  const previousReport = await readFile(
    new URL("research/r071t_report-source.md", root),
    "utf8",
  );

  for (const page of [home, note, literature, previousNote, previousReport]) {
    assert.match(page, /four[- ]mode|四模/i);
    assert.match(page, /full[- ]support|完整有限|target-support/i);
  }
  assert.match(note, /D_z\\Phi\(0,0\)=e\^\{\\nu\\tau\\Delta\}\|_\{E_j\}/);
  assert.match(previousNote, /不能把四模消去误写成任意宽环带消去/);
  assert.doesNotMatch(home, /使整个目标壳在预定正时间/);
});

test("verifies exact and independent R0.71U certificates", async () => {
  const [exact, independent, report, gap, literatureAudit, independentAudit] =
    await Promise.all([
      readFile(new URL("result.json", certificateRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-result.json", certificateRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("research/r071u_report-source.md", root), "utf8"),
      readFile(new URL("research/r071u_gap_matrix.md", root), "utf8"),
      readFile(new URL("research/r071u_literature_audit.md", root), "utf8"),
      readFile(new URL("research/r071u_independent_audit.md", root), "utf8"),
    ]);

  assert.equal(exact.release, "R0.71U");
  assert.equal(exact.status, "passed");
  assert.deepEqual(Object.keys(exact.checks).sort(), [
    "eigenshellAtomIdentity",
    "exact25DSubstitution",
    "forcedPathStressTest",
    "fullSupportIFTDerivative",
    "modularIsolation",
    "responseMatrixAudit",
    "scaleLedger",
    "zeroSamplingAlgebra",
  ]);
  assert.ok(Object.values(exact.checks).every((entry) => entry.passed));

  assert.equal(independent.release, "R0.71U");
  assert.equal(independent.status, "passed");
  assert.ok(Object.keys(independent.checks).length >= 7);
  assert.ok(Object.values(independent.checks).every((entry) => entry.passed));
  assert.ok(
    Math.max(
      ...independent.checks.directLatticeShooting.rows.map(
        (row) => row.maximumTargetResidual,
      ),
    ) < 1e-12,
  );
  assert.ok(
    Math.min(
      ...independent.checks.directLatticeShooting.rows.map(
        (row) => row.minimumSlopeMagnitude,
      ),
    ) > 1e-7,
  );

  assert.match(report, /zero-count-independent/i);
  assert.match(report, /arbitrary finite exact NSE recurrence/i);
  assert.match(report, /not a weighted-atom counterexample/i);
  assert.match(gap, /not proved|open/i);
  assert.match(literatureAudit, /bounded/i);
  assert.match(independentAudit, /independent/i);
  assert.doesNotMatch(report, /we prove global regularity/i);
});

test("ships reproducible journal figures, monitored computation, and exact mirrors", async () => {
  const requiredCertificateFiles = [
    "README.md",
    "SHA256SUMS",
    "build_hashes.py",
    "command.txt",
    "environment.txt",
    "result.json",
    "independent-result.json",
  ];
  const requiredFigureFiles = [
    "README.md",
    "SHA256SUMS",
    "assemble_data.py",
    "build_manifest.py",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "data.csv",
    "environment.txt",
    "figure-contract.md",
    "figure-data-metadata.json",
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "independent-results.json",
    "independent-validation.json",
    "independent_solver.py",
    "independent_validate.py",
    "manifest.json",
    "modular_solver.py",
    "plot.py",
    "primary-results.json",
    "progress.ndjson",
    "qa-grayscale.png",
    "qa-original.png",
    "qa-pdf.png",
    "qa-report.md",
    "qa_images.py",
    "requirements.txt",
    "resource-log.ndjson",
    "validate_data.py",
    "validation.json",
  ];
  await Promise.all([
    ...requiredCertificateFiles.map((path) =>
      access(new URL(path, certificateRoot)),
    ),
    ...requiredFigureFiles.map((path) => access(new URL(path, figureRoot))),
  ]);

  const [manifest, validation, independentValidation, progress, resource, ...files] =
    await Promise.all([
      readFile(new URL("manifest.json", figureRoot), "utf8").then(JSON.parse),
      readFile(new URL("validation.json", figureRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-validation.json", figureRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("progress.ndjson", figureRoot), "utf8"),
      readFile(new URL("resource-log.ndjson", figureRoot), "utf8"),
      readFile(new URL("figures/r0-71u-recurrence-packing.svg", publicRoot)),
      readFile(new URL("figures/r0-71u-recurrence-packing.pdf", publicRoot)),
      readFile(new URL("figures/r0-71u-recurrence-packing.png", publicRoot)),
      readFile(new URL("figure.svg", figureRoot)),
      readFile(new URL("figure.pdf", figureRoot)),
      readFile(new URL("figure.png", figureRoot)),
    ]);
  const [svg, pdf, png, sourceSvg, sourcePdf, sourcePng] = files;

  assert.equal(manifest.figureId, "fig-r071u-recurrence-packing");
  assert.equal(manifest.status, "formal");
  assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(manifest.git.certificateCommit, manifest.git.sourceCommit);
  assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  assert.ok(Math.abs(manifest.figure.widthMillimetres - 178) < 0.25);
  assert.equal(manifest.computation.finiteGalerkin, true);
  assert.equal(manifest.computation.pdeTimeStepping, true);
  assert.equal(manifest.computation.dns, false);
  assert.equal(manifest.computation.monitoring.enabled, true);
  assert.equal(validation.release, "R0.71U");
  assert.equal(validation.passed, true);
  assert.equal(independentValidation.release, "R0.71U");
  assert.equal(independentValidation.passed, true);
  assert.ok(progress.trim().split("\n").length >= 15);
  assert.ok(resource.trim().split("\n").length >= 8);

  assert.match(svg.toString("utf8"), /<svg/);
  assert.equal(pdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.deepEqual(svg, sourceSvg);
  assert.deepEqual(pdf, sourcePdf);
  assert.deepEqual(png, sourcePng);
  for (const [path, publicValue] of [
    ["figure.svg", svg],
    ["figure.pdf", pdf],
    ["figure.png", png],
  ]) {
    const expected = manifest.figure.outputs.find((output) => output.path === path);
    assert.ok(expected, path);
    assert.equal(sha256(publicValue), expected.sha256, path);
  }

  for (const path of [
    "notes/r0-71u.pdf",
    "recap-r0-61-r0-71u.pdf",
    "figures/r0-71u-recurrence-packing.pdf",
  ]) {
    const value = await readFile(new URL(path, publicRoot));
    assert.equal(value.subarray(0, 4).toString(), "%PDF", path);
    assert.ok(value.length > 10_000, path);
  }
});
