import assert from "node:assert/strict";
import { access, readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificatesRoot = new URL("research/certificates/r071j/", root);
const figureSourceRoot = new URL(
  "figures/r071j-full-frame/fig-r071j-full-frame-gap/",
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
    readFile(new URL("notes/r0-71j.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71j.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("keeps the R0.71J v0.95 release archived after the R0.71L site update", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 136);
  assert.match(home, /<strong>v0\.97<\/strong>网页版本/);
  assert.match(home, /<strong>136<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.71L<\/strong>最新研究节点/);
  assert.match(home, /展开 46 篇公开笔记/);
  assert.match(home, /累计回顾收录 76 个节点；全站现有 136 篇公开研究笔记/);
  assert.equal((home.match(/href="\/notes\/r0-71j\.html"/g) ?? []).length, 2);

  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 12);
  assert.match(recap, /收录节点：74/);
  assert.match(recap, /回顾截止时公开笔记：134/);
  assert.match(recap, /回顾截止节点：R0\.71J/);
  assert.match(literature, /R0\.69P–R0\.71L/);
  assert.match(literature, /开放接口 · R0\.71M/);

  for (const [page, minimum] of [
    [home, 10],
    [note, 15],
    [recap, 8],
    [literature, 48],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71J/);
  }
  for (const page of [note, recap]) {
    assert.match(page, /src="\/i18n-en\.js\?v=0\.95"/);
  }
  for (const page of [home, literature]) {
    assert.match(page, /src="\/i18n-en\.js\?v=0\.97"/);
  }
});

test("gives R0.71J independent release surfaces on home, recap, and literature", async () => {
  const { home, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071j" data-release="r071j"';
  const homeCard = sliceReleaseCard(home, opening);

  assert.equal((home.match(new RegExp(opening, "g")) ?? []).length, 1);
  assert.match(homeCard, /href="\/notes\/r0-71j\.html"/);
  assert.match(homeCard, /href="\/notes\/r0-71j\.pdf"/);
  assert.match(homeCard, /href="\/figures\/r0-71j-full-frame-gap\.pdf"/);
  assert.match(homeCard, /research\/certificates\/r071j/);
  assert.match(homeCard, /research\/r071j_report-source\.md/);
  assert.match(homeCard, /figures\/r071j-full-frame\/fig-r071j-full-frame-gap/);
  assert.match(homeCard, /<strong>结论边界：<\/strong>/);
  assert.match(homeCard, /R0\.71K/);

  const recapNeedle = 'href="/notes/r0-71j.html"';
  const recapNeedleIndex = recap.indexOf(recapNeedle);
  const recapCardStart = recap.lastIndexOf(
    '<article class="phase">',
    recapNeedleIndex,
  );
  const recapCardEnd = recap.indexOf("</article>", recapNeedleIndex);
  const recapCard = recap.slice(recapCardStart, recapCardEnd);
  assert.ok(recapNeedleIndex >= 0);
  assert.ok(recapCardStart >= 0);
  assert.match(recapCard, /positive-defect|正缺陷/i);
  assert.match(recapCard, /href="\/figures\/r0-71j-full-frame-gap\.pdf"/);
  assert.match(recapCard, /research\/certificates\/r071j/);

  const literatureMarker = "<header><b>R0.71J</b>";
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
  assert.match(literatureCard, /href="\/notes\/r0-71j\.html"/);
  assert.ok(literatureCard.includes("\\(K^{-2}\\)"));
  assert.ok(literatureCard.includes("\\(K^{-4}\\)"));
});

test("states the exact defect, broad-parent witness, and quantified full-frame gap", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "2\\mathcal Z_+=\\partial_t\\mathcal A_w",
    "2\\nu\\sum_\\gamma a_\\gamma+2\\mathcal Z_-",
    "2\\nu\\sum_\\gamma\\theta_{\\varepsilon,\\gamma}",
    "\\sum_jB_j=\\langle L,-\\Delta u\\rangle",
    "\\frac{((\\sum_jB_j)^+)^2}{\\sum_jd_j}",
    "\\frac{2041}{200}",
    "Y=178K^2",
    "\\|F_\\kappa\\|_2^2=500K^2",
    "d_\\kappa=3942K^4",
    "\\theta_*=\\log2/18",
    "\\frac{A_*}{64K^2}",
    "\\frac{1-2^{-1/9}}{2\\nu K^4}",
    "\\frac{\\nu A_*}{32(1-2^{-1/9})}K^2",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(note, /R0\.71E §10\.1 parent-only frame/);
  assert.match(note, /以及它们的共轭模/);
  assert.ok(note.includes("\\(I_K=[0,\\theta_*/(\\nu K^2)]\\)"));
  assert.match(note, /所有充分大 dyadic/);
  assert.ok(note.includes("不是有限 \\(K\\) 的 DNS 曲线"));
  assert.match(note, /未证明：R0\.71E §10\.2 任意 child refinement/);
  assert.match(note, /R0\.71K 把 global cell 换成一个固定 matched spatial partition/);
  assert.match(home, /R0\.71J/);
  assert.match(recap, /R0\.71K 检查 matched spatial localization/);
  assert.match(literature, /完整 broad parent frame/);
});

test("links and verifies the report, two audits, certificate, and figure package", async () => {
  const { note } = await publishedPages();
  const linkedSources = [
    "research/r071j_report-source.md",
    "research/r071j_literature_audit.md",
    "research/r071j_independent_audit.md",
    "research/r071j_gap_matrix.md",
    "research/r071j_exact_audit.py",
    "research/r071j_independent_audit.py",
    "research/certificates/r071j",
    "figures/r071j-full-frame/fig-r071j-full-frame-gap",
  ];
  for (const source of linkedSources) assert.ok(note.includes(source), source);

  await Promise.all([
    access(new URL("research/r071j_report-source.md", root)),
    access(new URL("research/r071j_exact_audit.py", root)),
    access(new URL("research/r071j_independent_audit.md", root)),
    access(new URL("research/r071j_independent_audit.py", root)),
    access(new URL("result.json", certificatesRoot)),
    access(new URL("independent-result.json", certificatesRoot)),
    access(new URL("SHA256SUMS", certificatesRoot)),
    access(new URL("manifest.json", figureSourceRoot)),
    access(new URL("validation.json", figureSourceRoot)),
    access(new URL("independent-validation.json", figureSourceRoot)),
  ]);

  const [exactCertificate, independentCertificate] = await Promise.all([
    readFile(new URL("result.json", certificatesRoot), "utf8").then(JSON.parse),
    readFile(new URL("independent-result.json", certificatesRoot), "utf8").then(
      JSON.parse,
    ),
  ]);
  assert.equal(
    exactCertificate.status,
    "all-shell-positive-defect-closed-full-frame-heat-payment-rejected",
  );
  assert.equal(exactCertificate.positiveDefectIdentity.hardResidual, "0");
  assert.equal(exactCertificate.positiveDefectIdentity.softResidual, "0");
  assert.equal(independentCertificate.status, "passed");
  assert.equal(independentCertificate.claims.parentOnlyFrameChecked, true);
  assert.equal(
    independentCertificate.claims.totalHeatPaymentRejectedForThatFrame,
    true,
  );
  assert.equal(independentCertificate.claims.matchedSpatialCellsChecked, false);
  assert.equal(independentCertificate.claims.facePaidWeightedBVRejected, false);
  assert.equal(independentCertificate.claims.regularityTheoremClaimed, false);
  assert.ok(
    independentCertificate.directHeatFourierReconstruction.maximumResidual <
      1e-12,
  );
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
    readFile(new URL("notes/r0-71j.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71j.pdf", publicRoot)),
    readFile(new URL("figures/r0-71j-full-frame-gap.svg", publicRoot)),
    readFile(new URL("figures/r0-71j-full-frame-gap.pdf", publicRoot)),
    readFile(new URL("figures/r0-71j-full-frame-gap.png", publicRoot)),
    readFile(new URL("figure.svg", figureSourceRoot)),
    readFile(new URL("figure.pdf", figureSourceRoot)),
    readFile(new URL("figure.png", figureSourceRoot)),
  ]);

  assert.match(note, /src="\/figures\/r0-71j-full-frame-gap\.svg"/);
  assert.match(note, /href="\/notes\/r0-71j\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-71j\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-71j\.pdf"/);
  assert.match(home, /href="\/notes\/r0-71j\.pdf"/);
  assert.match(home, /href="\/recap-r0-61-r0-71l\.pdf"/);
  assert.match(home, /href="\/figures\/r0-71j-full-frame-gap\.pdf"/);

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

test("keeps R0.71J claims factual and scoped", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const forbiddenInflation =
    /攻关|主攻|研究纪律|三重审计|杀死错误想法|重大突破|颠覆性|世界首个|接近解决|解决了千禧年|证明了全局正则性|原创性定理|首次证明/;

  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, forbiddenInflation);
    assert.doesNotMatch(page, /我们/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /\t/);
  }

  assert.match(note, /不是千禧年问题的解答/);
  assert.match(note, /不作新颖性、优先权或发表级别声明/);
  assert.match(note, /未证明：无条件 weighted BV、继续性判据、全局光滑性或有限时破裂/);
  assert.match(recap, /Clay 正式问题仍然开放/);
});
