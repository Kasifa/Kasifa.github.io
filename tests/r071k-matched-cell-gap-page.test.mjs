import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const certificatesRoot = new URL("research/certificates/r071k/", root);
const figureSourceRoot = new URL(
  "figures/r071k-matched-cells/fig-r071k-matched-cell-gap/",
  root,
);

function assertLocalAnchorsResolve(html, minimumUniqueTargets) {
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

function sliceReleaseCard(html, opening) {
  const start = html.indexOf(opening);
  assert.ok(start >= 0, opening);
  const next = html.indexOf('<div class="task-one"', start + opening.length);
  const sectionEnd = html.indexOf("</section>", start);
  const end = next >= 0 && next < sectionEnd ? next : sectionEnd;
  return html.slice(start, end);
}

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71k.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71k.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("keeps the R0.71K v0.96 release archived after later site updates", async () => {
  const { home, note, recap, literature } = await publishedPages();

  assert.equal((home.match(/href="\/notes\/r0-71k\.html"/g) ?? []).length, 2);

  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 12);
  assert.match(recap, /收录节点：75/);
  assert.match(recap, /回顾截止时公开笔记：135/);
  assert.match(recap, /回顾截止节点：R0\.71K/);
  for (const [page, minimum] of [
    [home, 10],
    [note, 15],
    [recap, 8],
    [literature, 48],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71K/);
  }
  for (const page of [note, recap]) {
    assert.match(page, /src="\/i18n-en\.js\?v=0\.96"/);
  }
});

test("gives R0.71K independent release surfaces on home, recap, and literature", async () => {
  const { home, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071k" data-release="r071k"';
  const homeCard = sliceReleaseCard(home, opening);

  assert.equal((home.match(new RegExp(opening, "g")) ?? []).length, 1);
  assert.match(homeCard, /href="\/notes\/r0-71k\.html"/);
  assert.match(homeCard, /href="\/notes\/r0-71k\.pdf"/);
  assert.match(homeCard, /href="\/figures\/r0-71k-matched-cell-gap\.pdf"/);
  assert.match(homeCard, /research\/certificates\/r071k/);
  assert.match(homeCard, /research\/r071k_report-source\.md/);
  assert.match(homeCard, /figures\/r071k-matched-cells\/fig-r071k-matched-cell-gap/);
  assert.match(homeCard, /<strong>结论边界：<\/strong>/);
  assert.match(homeCard, /R0\.71L/);

  const recapNeedle = 'href="/notes/r0-71k.html"';
  const recapNeedleIndex = recap.indexOf(recapNeedle);
  const recapCardStart = recap.lastIndexOf(
    '<article class="phase">',
    recapNeedleIndex,
  );
  const recapCardEnd = recap.indexOf("</article>", recapNeedleIndex);
  const recapCard = recap.slice(recapCardStart, recapCardEnd);
  assert.ok(recapNeedleIndex >= 0);
  assert.ok(recapCardStart >= 0);
  assert.match(recapCard, /matched cells|匹配小区/i);
  assert.match(recapCard, /href="\/figures\/r0-71k-matched-cell-gap\.pdf"/);
  assert.match(recapCard, /research\/certificates\/r071k/);

  const literatureMarker = "<header><b>R0.71K</b>";
  const literatureMarkerIndex = literature.indexOf(literatureMarker);
  const literatureCardStart = literature.lastIndexOf(
    '<div class="route-step',
    literatureMarkerIndex,
  );
  const literatureCardEnd = literature.indexOf("</div>", literatureMarkerIndex);
  const literatureCard = literature.slice(
    literatureCardStart,
    literatureCardEnd,
  );
  assert.ok(literatureMarkerIndex >= 0);
  assert.ok(literatureCardStart >= 0);
  assert.match(literatureCard, /href="\/notes\/r0-71k\.html"/);
  assert.ok(literatureCard.includes("\\(K^{-2}\\)"));
  assert.ok(literatureCard.includes("\\((\\nu K^4)^{-1}\\)"));
});

test("states the translated-cell theorem and the leading-collar boundary", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "B_{\\kappa,Q}=\\frac{B_\\kappa}{K^3}",
    "d_{\\kappa,Q}=\\frac{D_{\\rm loc}}{K^3}",
    "\\sum_Qq_{\\kappa,Q}=\\frac{(B_\\kappa^+)^2}{D_{\\rm loc}}",
    "C_{\\rm part}=2C_0+\\frac{4C_1}{\\rho^2}",
    "\\frac{A_*}{64C_{\\rm part}K^2}",
    "\\frac{N(1-2^{-1/9})}{2\\nu K^4}",
    "\\text{viscous collar budget}\\sim K^{-2}",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(note, /每个小区都有/);
  assert.match(note, /选中有限小区没有 denominator face/);
  assert.match(note, /固定 cutoff 只消去 motion row，tangent row 仍在/);
  assert.match(note, /这里没有暗中使用无限 frame–cell evolution identity/);
  assert.match(note, /collar 足够大，尺度上可能支付正生成；但目前没有从 Leray energy 推出它的绝对预算/);
  assert.match(recap, /R0\.71L 检查 fixed-cell collar 与 tangent budget/);
  assert.match(literature, /Dascaliuc|Leitmeyer/);
});

test("links and verifies the report, two audits, certificate, and figure package", async () => {
  const { note } = await publishedPages();
  const linkedSources = [
    "research/r071k_report-source.md",
    "research/r071k_literature_audit.md",
    "research/r071k_independent_audit.md",
    "research/r071k_gap_matrix.md",
    "research/r071k_exact_audit.py",
    "research/r071k_independent_audit.py",
    "research/certificates/r071k",
    "figures/r071k-matched-cells/fig-r071k-matched-cell-gap",
  ];
  for (const source of linkedSources) assert.ok(note.includes(source), source);

  await Promise.all([
    access(new URL("research/r071k_report-source.md", root)),
    access(new URL("research/r071k_exact_audit.py", root)),
    access(new URL("research/r071k_independent_audit.md", root)),
    access(new URL("research/r071k_independent_audit.py", root)),
    access(new URL("result.json", certificatesRoot)),
    access(new URL("independent-result.json", certificatesRoot)),
    access(new URL("SHA256SUMS", certificatesRoot)),
    access(new URL("manifest.json", figureSourceRoot)),
    access(new URL("validation.json", figureSourceRoot)),
    access(new URL("independent-validation.json", figureSourceRoot)),
  ]);

  const [exactCertificate, independentCertificate, manifest] =
    await Promise.all([
      readFile(new URL("result.json", certificatesRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-result.json", certificatesRoot), "utf8").then(
        JSON.parse,
      ),
      readFile(new URL("manifest.json", figureSourceRoot), "utf8").then(JSON.parse),
    ]);
  assert.equal(
    exactCertificate.status,
    "matched-aligned-cells-preserve-two-power-heat-gap",
  );
  assert.equal(exactCertificate.positiveDefect.identityResidual, "0");
  assert.equal(exactCertificate.finiteSelectedFamily.denominatorFaces, 0);
  assert.equal(exactCertificate.collarBoundary.lerayPaymentProved, false);
  assert.equal(independentCertificate.status, "passed");
  assert.equal(independentCertificate.claims.alignedMatchedPartitionChecked, true);
  assert.equal(independentCertificate.claims.sameLocalHeatPaymentRejected, true);
  assert.equal(independentCertificate.claims.separateCollarPaymentRejected, false);
  assert.equal(independentCertificate.claims.arbitraryPartitionsChecked, false);
  assert.equal(independentCertificate.claims.regularityTheoremClaimed, false);
  assert.ok(
    independentCertificate.partition.maximumPartitionResidual < 1e-14,
  );
  assert.equal(manifest.qa.status, "passed");
  assert.equal(manifest.computation.dns, false);
  assert.equal(manifest.computation.fittedData, false);
  if (manifest.status === "formal") {
    assert.match(manifest.git.sourceCommit, /^[0-9a-f]{40}$/);
    assert.equal(manifest.git.certificateCommit, manifest.git.sourceCommit);
    assert.equal(manifest.git.dirtyAtCertifiedRun, false);
  } else {
    assert.equal(manifest.status, "draft");
    assert.equal(manifest.git.sourceCommit, "pending");
  }
});

test("ships synchronized PDFs and three journal figure formats", async () => {
  const [
    { home, note, recap },
    notePdf,
    recapPdf,
    svg,
    figurePdf,
    png,
    sourceSvg,
    sourceFigurePdf,
    sourcePng,
  ] = await Promise.all([
    publishedPages(),
    readFile(new URL("notes/r0-71k.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71k.pdf", publicRoot)),
    readFile(new URL("figures/r0-71k-matched-cell-gap.svg", publicRoot)),
    readFile(new URL("figures/r0-71k-matched-cell-gap.pdf", publicRoot)),
    readFile(new URL("figures/r0-71k-matched-cell-gap.png", publicRoot)),
    readFile(new URL("figure.svg", figureSourceRoot)),
    readFile(new URL("figure.pdf", figureSourceRoot)),
    readFile(new URL("figure.png", figureSourceRoot)),
  ]);

  assert.match(note, /src="\/figures\/r0-71k-matched-cell-gap\.svg"/);
  assert.match(note, /href="\/notes\/r0-71k\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-71k\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-71k\.pdf"/);
  assert.match(home, /href="\/notes\/r0-71k\.pdf"/);
  assert.match(home, /href="\/figures\/r0-71k-matched-cell-gap\.pdf"/);

  assert.equal(notePdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.equal(recapPdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.ok(notePdf.length > 10_000);
  assert.ok(recapPdf.length > 10_000);
  assert.match(svg.toString("utf8"), /<svg/);
  assert.equal(figurePdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.deepEqual(svg, sourceSvg);
  assert.deepEqual(figurePdf, sourceFigurePdf);
  assert.deepEqual(png, sourcePng);
});

test("keeps R0.71K claims factual, scoped, and free of broken TeX escapes", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const forbiddenInflation =
    /攻关|主攻|研究纪律|三重审计|杀死错误想法|重大突破|颠覆性|世界首个|接近解决|解决了千禧年|证明了全局正则性|原创性定理|首次证明/;

  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, forbiddenInflation);
    assert.doesNotMatch(page, /我们/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /\t/);
    assert.doesNotMatch(page, /(^|\n)u K\^4/m);
  }

  assert.match(note, /不是千禧年问题的解答/);
  assert.match(note, /不作新颖性、优先权或发表级别声明/);
  assert.match(note, /未证明：collar 的 Leray-level payment/);
  assert.match(recap, /Clay 正式问题仍然开放/);
});
