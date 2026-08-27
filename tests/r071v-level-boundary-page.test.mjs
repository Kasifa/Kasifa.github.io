import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readFile, readdir } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificateRoot = new URL("research/certificates/r071v/", root);
const figureRoot = new URL(
  "figures/r071v-level-boundary/fig-r071v-zero-level-boundary/",
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
    readFile(new URL("notes/r0-71v.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71v.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("retains R0.71V artifacts while v1.28 publishes R0.72O as current", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 165);
  assert.match(home, /<strong>v1\.28<\/strong>网页版本/);
  assert.match(home, /<strong>165<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72O<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72O<\/span>/);
  assert.match(home, /展开 75 篇公开笔记/);
  assert.match(
    home,
    /<details class="tree-notes" open>[\s\S]*?aria-label="R0\.69P–R0\.72O"/,
  );
  assert.match(home, /href="#r070a">R0\.70A–R0\.72O：67 节已公开，43 节完整封存<\/a>/);
  assert.match(home, /累计回顾收录 105 个节点；全站现有 165 篇公开研究笔记/);
  assert.match(home, /R0\.70A–R0\.72O 共 67 个版本已公开；43 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单/);
  assert.match(home, /NEXT · R0\.72P/);

  const route = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72O">([\s\S]*?)<\/nav>/,
  );
  assert.ok(route);
  assert.equal(count(route[1], 'href="/notes/'), 75);
  assert.equal(count(route[1], 'href="/notes/r0-71v.html"'), 1);
  assert.equal(count(home, 'data-release="r071v"'), 1);
  assert.equal(count(home, 'href="/notes/r0-71v.html"'), 2);
  assert.equal(count(recap, '<article class="phase">'), 17);
  assert.match(recap, /R0\.60 之后的路线分成十七段/);
  assert.match(recap, /相对所选 singleton target shell 的 first-time-jet row/);
  assert.ok(recap.includes("完整 global \\(\\nu^2\\) baseline"));

  const nodeIndex =
    recap.match(/<div class="node-index-grid">([\s\S]*?)<\/div>/)?.[1] ?? "";
  assert.equal(count(nodeIndex, 'href="/notes/'), 86);
  assert.match(recap, /收录节点：86/);
  assert.match(recap, /回顾截止时公开笔记：146/);
  assert.match(recap, /R0\.70A–R0\.71V 完成版本/);
  assert.match(literature, /R0\.69P–R0\.72O/);
  assert.match(literature, /开放接口 · R0\.72P/);

  for (const [page, minimum, version] of [
    [home, 10, "1.28"],
    [note, 14, "1.08"],
    [recap, 8, "1.08"],
    [literature, 50, "1.28"],
  ]) {
    assertAnchorsResolve(page, minimum);
    assert.ok(page.includes('src="/i18n-en.js?v=' + version + '"'));
    assert.doesNotMatch(page, /我们|攻关|主攻|三重审计/);
    assert.doesNotMatch(page, /千禧年问题已经解决|解决了千禧年问题/);
  }
});

test("states the excursion theorem and the selected-row obstruction precisely", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "向右从零点出发",
    "左端 \\(a\\) 已经为正",
    "H_E^2=\\frac{\\kappa_j^{-6}h_E^2}{\\ell Y_E}",
    "Y_E&gt;0",
    "\\sum_{j,E}H_E^2",
    "D_E=\\frac{h_E^2Y(t_E)}{\\ell Y_Es_E^2}",
    "\\mathcal Q(0+)",
    "\\int\\mathcal Q_N=4/3",
    "K_y=K_z=1",
    "B_{1,q}^{(*)}",
    "B_{2,q}^{(*)}",
    "second prescribed root atom",
    "singleton target-shell selection",
    "这不是对 complete fixed-frame ledger 的 no-go",
    "完整 global \\(\\nu^2\\) baseline 尚未被排除",
    "这不是千禧年问题的解答",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /finite shell\/component.*Tonelli.*monotone convergence/is);
  assert.ok(note.includes("\\frac{J_{2,q}}{(2/\\ell)B_{1,q}^{(*)}}\\asymp q^2"));
  assert.ok(note.includes("\\frac{J_{2,q}}{(7\\ell/3)B_{2,q}^{(*)}}\\asymp q^{-2}"));
  assert.match(note, /excursion inequality 本身由解析证明承担/is);
  assert.match(home, /fixed zero-level atom.*first-time row/is);
  assert.match(home, /向右从零点出发的正 excursion/is);
  assert.match(home, /selected singleton target-shell/is);
  assert.match(home, /不是 complete fixed-frame ledger 的 no-go/is);
  assert.match(recap, /fixed zero-level trace/is);
  assert.match(literature, /right-rooted scale-zero excursion packing/is);
  assert.match(literature, /fixed-target genuine 2\.5D sequence/is);
  assert.match(literature, /排除 selected first-row fixed-zero sampling/is);
});

test("verifies the exact and independent R0.71V ledgers", async () => {
  const [exact, independent, report, gap, literatureAudit, independentAudit] =
    await Promise.all([
      readFile(new URL("result.json", certificateRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-result.json", certificateRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("research/r071v_report-source.md", root), "utf8"),
      readFile(new URL("research/r071v_gap_matrix.md", root), "utf8"),
      readFile(new URL("research/r071v_literature_audit.md", root), "utf8"),
      readFile(new URL("research/r071v_independent_audit.md", root), "utf8"),
    ]);

  assert.equal(exact.release, "R0.71V");
  assert.equal(exact.status, "passed");
  assert.ok(Object.keys(exact.checks).length >= 7);
  assert.ok(Object.values(exact.checks).every((entry) => entry.passed));
  assert.equal(independent.release, "R0.71V");
  assert.equal(independent.status, "passed");
  assert.ok(Object.keys(independent.checks).length >= 7);
  assert.ok(Object.values(independent.checks).every((entry) => entry.passed));

  assert.match(report, /right-rooted connected component/i);
  assert.match(report, /selected singleton target shell/i);
  assert.match(report, /complete fixed-frame\s+ledger/i);
  assert.match(gap, /initial trace/i);
  assert.match(gap, /not proved|open|rejected/i);
  assert.match(literatureAudit, /bounded primary-source audit/i);
  assert.match(independentAudit, /standalone/i);
  assert.doesNotMatch(report, /we prove global regularity/i);
});

test("ships the monitored figure package and exact public mirrors", async () => {
  const requiredFigureFiles = [
    "README.md",
    "SHA256SUMS",
    "build_manifest.py",
    "caption.md",
    "command.txt",
    "config.json",
    "contract.json",
    "data.csv",
    "data.json",
    "environment.txt",
    "figure-contract.md",
    "figure-data-metadata.json",
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "manifest.json",
    "plot.py",
    "produce_data.py",
    "progress.ndjson",
    "qa_images.py",
    "qa-grayscale.png",
    "qa-original.png",
    "qa-pdf.png",
    "qa-report.md",
    "requirements.txt",
    "resource-log.ndjson",
    "results.json",
    "validate.py",
    "validation.json",
  ];
  await Promise.all(requiredFigureFiles.map((path) => access(new URL(path, figureRoot))));

  const [config, results, validation, progress, resource, ...files] = await Promise.all([
    readFile(new URL("config.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("results.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("validation.json", figureRoot), "utf8").then(JSON.parse),
    readFile(new URL("progress.ndjson", figureRoot), "utf8"),
    readFile(new URL("resource-log.ndjson", figureRoot), "utf8"),
    readFile(new URL("figures/r0-71v-zero-level-boundary.svg", publicRoot)),
    readFile(new URL("figures/r0-71v-zero-level-boundary.pdf", publicRoot)),
    readFile(new URL("figures/r0-71v-zero-level-boundary.png", publicRoot)),
    readFile(new URL("figure.svg", figureRoot)),
    readFile(new URL("figure.pdf", figureRoot)),
    readFile(new URL("figure.png", figureRoot)),
  ]);
  const [svg, pdf, png, sourceSvg, sourcePdf, sourcePng] = files;

  assert.equal(config.release, "R0.71V");
  assert.equal(config.target.Ky, 1);
  assert.equal(config.target.Kz, 1);
  assert.equal(results.release, "R0.71V");
  assert.equal(results.figureId, "fig-r071v-zero-level-boundary");
  assert.equal(results.status, "passed");
  assert.equal(validation.release, "R0.71V");
  assert.equal(validation.status, "passed");
  assert.equal(validation.checks.length, 21);
  assert.ok(validation.checks.every((entry) => entry.passed));
  assert.ok(results.producerChecks["allTargetResidualsBelow1e-12"]);
  assert.ok(results.producerChecks.allTargetShellPrefactorsMatchDeclared);
  assert.ok(results.fittedExponentsTailFour.secondRootAtomOverFirstRow > 1.8);
  assert.ok(results.fittedExponentsTailFour.secondRootAtomOverSecondRow < -1.8);
  assert.ok(results.fittedExponentsTailFour.terminalD < -3.7);
  assert.ok(progress.trim().split("\n").length >= 6);
  assert.ok(resource.trim().split("\n").length >= 3);

  assert.match(svg.toString("utf8"), /<svg/);
  assert.equal(pdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.equal(sha256(svg), sha256(sourceSvg));
  assert.equal(sha256(pdf), sha256(sourcePdf));
  assert.equal(sha256(png), sha256(sourcePng));

  for (const path of [
    "notes/r0-71v.pdf",
    "recap-r0-61-r0-71v.pdf",
    "figures/r0-71v-zero-level-boundary.pdf",
  ]) {
    const value = await readFile(new URL(path, publicRoot));
    assert.equal(value.subarray(0, 4).toString(), "%PDF", path);
    assert.ok(value.length > 10_000, path);
  }
});
