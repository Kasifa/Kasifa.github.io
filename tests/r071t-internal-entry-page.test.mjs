import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificateRoot = new URL("research/certificates/r071t/", root);
const figureRoot = new URL(
  "figures/r071t-internal-entry/fig-r071t-internal-entry/",
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
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71t.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71t.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("retains the corrected R0.71T release after the R0.72G site update", async () => {
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
  assert.equal(count(route[1], 'href="/notes/r0-71t.html"'), 1);
  assert.equal(count(home, 'data-release="r071t"'), 1);
  assert.equal(count(home, 'href="/notes/r0-71t.html"'), 2);

  assert.ok(count(recap, '<article class="phase">') >= 12);
  assert.match(recap, /收录节点：84/);
  assert.match(recap, /回顾截止时公开笔记：144/);
  assert.match(recap, /R0\.70A–R0\.71T 完成版本/);
  assert.match(recap, /R0\.00–R0\.60 的内容保留在上一份阶段回顾中/);
  assert.match(literature, /R0\.69P–R0\.72G/);
  assert.match(literature, /开放接口 · R0\.72H/);

  for (const [page, minimum] of [
    [home, 10],
    [note, 12],
    [recap, 8],
    [literature, 50],
  ]) {
    assertAnchorsResolve(page, minimum);
    assert.doesNotMatch(page, /我们|攻关|主攻|三重审计/);
    assert.doesNotMatch(page, /千禧年问题已经解决|解决了千禧年问题/);
  }
  assert.ok(home.includes('src="/i18n-en.js?v=1.20"'));
  assert.ok(literature.includes('src="/i18n-en.js?v=1.20"'));
  assert.ok(note.includes('src="/i18n-en.js?v=1.05"'));
  assert.ok(recap.includes('src="/i18n-en.js?v=1.05"'));
});

test("states the internal-entry theorem, scoped scaling no-go, and open boundary", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "D_z\\Phi(0,0)=e^{-2\\nu\\tau}I",
    "z(a)=-a^2\\tau F_*+O(a^3)",
    "\\kappa^{-2}A_+(a)=\\frac{a^2e^{-2\\nu\\tau}}4+O(a^3)",
    "a_\\lambda=\\lambda^{-2}",
    "\\frac{2\\nu}{\\sinh(2\\nu\\tau)}\\lambda^2+o(\\lambda^2)",
    "\\rho_\\delta(r)",
    "q_\\beta^{\\rm jet}=\\kappa_j^{-6}",
    "finite-time singularity 或 global regularity",
    "Galerkin 图是截断 ODE 复核",
    "精确的四模目标投影",
    "不能把四模消去误写成任意宽环带消去",
    "D_z\\Phi=e^{\\nu\\tau\\Delta}",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /正时间.*精确归零.*正方向横穿/is);
  assert.match(note, /能量趋零.*临界范数趋零.*enstrophy 有界/is);
  assert.match(note, /representation，不是 a priori occupation theorem/is);
  assert.match(note, /只排除所有 smooth 解上.*bare normalized/is);
  assert.match(home, /genuine smooth positive-time internal entry/is);
  assert.match(recap, /initial-boundary caveat/is);
  assert.match(literature, /<b>R0\.71T<\/b>.*genuine internal entry.*两阶错配/is);
});

test("verifies exact and independent R0.71T certificates", async () => {
  const [exact, independent, report, gap, literatureAudit, independentAudit] =
    await Promise.all([
      readFile(new URL("result.json", certificateRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-result.json", certificateRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("research/r071t_report-source.md", root), "utf8"),
      readFile(new URL("research/r071t_gap_matrix.md", root), "utf8"),
      readFile(new URL("research/r071t_literature_audit.md", root), "utf8"),
      readFile(new URL("research/r071t_independent_audit.md", root), "utf8"),
    ]);

  assert.equal(exact.release, "R0.71T");
  assert.equal(exact.status, "passed");
  assert.equal(Object.keys(exact.checks).length, 8);
  assert.ok(Object.values(exact.checks).every((entry) => entry.passed));
  assert.equal(exact.checks.fourierSeed.F2, "1/4");
  assert.equal(exact.checks.fourierSeed.curlF2, "1/2");
  assert.equal(
    exact.checks.doubleScalingLedger.ratio,
    "2*lambda**2*nu/sinh(2*nu*tau)",
  );

  assert.equal(independent.release, "R0.71T");
  assert.equal(independent.status, "passed");
  assert.equal(Object.keys(independent.checks).length, 6);
  assert.ok(Object.values(independent.checks).every((entry) => entry.passed));
  assert.ok(independent.checks.resonantNormalForm.maximumResidual < 1.2e-13);
  assert.ok(independent.checks.outgoingCoarea.maximumResidual < 7e-16);
  assert.ok(independent.checks.traceVariation.maximumResidual < 2e-16);
  assert.ok(independent.checks.doubleScaling.maximumResidual < 4e-16);

  assert.match(report, /finite-dimensional implicit-function (?:argument|theorem)/i);
  assert.match(report, /positive-time internal entry/i);
  assert.match(report, /exactly the real four-mode projection/i);
  assert.match(report, /full-support extension/i);
  assert.ok(report.includes("+\\frac{\\kappa_j^{-2}}2\\int"));
  assert.match(gap, /not proved|open/i);
  assert.match(literatureAudit, /bounded (?:primary-source audit|answer)/i);
  assert.match(independentAudit, /independent/i);
  assert.doesNotMatch(report, /we prove global regularity/i);
  assert.doesNotMatch(report, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
});

test("ships journal figure mirrors, monitored computation, and reproducibility inventory", async () => {
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
    "galerkin_shoot.py",
    "independent-results.json",
    "independent-validation.json",
    "independent_galerkin.py",
    "independent_validate.py",
    "manifest.json",
    "plot.py",
    "progress.ndjson",
    "qa-grayscale.png",
    "qa-original.png",
    "qa-pdf.png",
    "qa-report.md",
    "qa_images.py",
    "requirements.txt",
    "resource-log.ndjson",
    "solver-results.json",
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
      readFile(new URL("figures/r0-71t-internal-entry.svg", publicRoot)),
      readFile(new URL("figures/r0-71t-internal-entry.pdf", publicRoot)),
      readFile(new URL("figures/r0-71t-internal-entry.png", publicRoot)),
      readFile(new URL("figure.svg", figureRoot)),
      readFile(new URL("figure.pdf", figureRoot)),
      readFile(new URL("figure.png", figureRoot)),
    ]);
  const [svg, pdf, png, sourceSvg, sourcePdf, sourcePng] = files;

  assert.equal(manifest.figureId, "fig-r071t-internal-entry");
  assert.equal(manifest.status, "formal");
  assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
  assert.equal(manifest.git.certificateCommit, manifest.git.sourceCommit);
  assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 124);
  assert.equal(manifest.computation.finiteGalerkin, true);
  assert.equal(manifest.computation.pdeTimeStepping, true);
  assert.equal(manifest.computation.dns, false);
  assert.equal(manifest.computation.monitoring.enabled, true);
  assert.equal(validation.status, "passed");
  assert.equal(independentValidation.status, "passed");
  assert.ok(progress.trim().split("\n").length >= 10);
  assert.ok(resource.trim().split("\n").length >= 2);

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
    "notes/r0-71t.pdf",
    "recap-r0-61-r0-71t.pdf",
    "figures/r0-71t-internal-entry.pdf",
  ]) {
    const value = await readFile(new URL(path, publicRoot));
    assert.equal(value.subarray(0, 4).toString(), "%PDF", path);
    assert.ok(value.length > 10_000, path);
  }
});
