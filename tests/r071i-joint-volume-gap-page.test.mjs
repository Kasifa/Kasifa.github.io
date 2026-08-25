import assert from "node:assert/strict";
import { access, readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificatesRoot = new URL("research/certificates/r071i/", root);
const figureSourceRoot = new URL(
  "figures/r071i-joint/fig-r071i-joint-volume-gap/",
  root,
);

function assertLocalAnchorsResolve(html, minimumUniqueTargets) {
  const ids = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
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
    readFile(new URL("notes/r0-71i.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71i.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("keeps the R0.71I note and 73-node recap as frozen v0.94 artifacts", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.ok(noteNames.filter((name) => name.endsWith(".html")).length >= 133);
  assert.equal((home.match(/href="\/notes\/r0-71i\.html"/g) ?? []).length, 2);

  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 12);
  assert.match(recap, /收录节点：73/);
  assert.match(recap, /回顾截止时公开笔记：133/);
  assert.match(recap, /回顾截止节点：R0\.71I/);
  for (const [page, minimum] of [
    [note, 15],
    [recap, 8],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71I/);
    assert.match(page, /src="\/i18n-en\.js\?v=0\.94"/);
  }
  for (const [page, minimum] of [
    [home, 10],
    [literature, 48],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71I/);
  }
});

test("gives R0.71I independent release surfaces on home, recap, and literature", async () => {
  const { home, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071i" data-release="r071i"';
  const homeCard = sliceReleaseCard(home, opening);

  assert.equal((home.match(new RegExp(opening, "g")) ?? []).length, 1);
  assert.match(homeCard, /href="\/notes\/r0-71i\.html"/);
  assert.match(homeCard, /href="\/notes\/r0-71i\.pdf"/);
  assert.match(homeCard, /href="\/figures\/r0-71i-joint-volume-gap\.pdf"/);
  assert.match(homeCard, /research\/certificates\/r071i/);
  assert.match(homeCard, /research\/r071i_report-source\.md/);
  assert.match(homeCard, /figures\/r071i-joint\/fig-r071i-joint-volume-gap/);
  assert.match(homeCard, /<strong>结论边界：<\/strong>/);
  assert.match(homeCard, /R0\.71J/);

  const recapNeedle = 'href="/notes/r0-71i.html"';
  const recapNeedleIndex = recap.indexOf(recapNeedle);
  const recapCardStart = recap.lastIndexOf(
    '<article class="phase">',
    recapNeedleIndex,
  );
  const recapCardEnd = recap.indexOf("</article>", recapNeedleIndex);
  const recapCard = recap.slice(recapCardStart, recapCardEnd);
  assert.ok(recapNeedleIndex >= 0);
  assert.ok(recapCardStart >= 0);
  assert.match(recapCard, /R0\.71I/);
  assert.match(recapCard, /href="\/figures\/r0-71i-joint-volume-gap\.pdf"/);
  assert.match(recapCard, /research\/certificates\/r071i/);

  const literatureMarker = "<header><b>R0.71I</b>";
  const literatureMarkerIndex = literature.indexOf(literatureMarker);
  const literatureCardStart = literature.lastIndexOf(
    '<div class="route-step',
    literatureMarkerIndex,
  );
  const literatureCardEnd = literature.indexOf("</div>", literatureMarkerIndex);
  const literatureCard = literature.slice(literatureCardStart, literatureCardEnd);
  assert.ok(literatureMarkerIndex >= 0);
  assert.ok(literatureCardStart >= 0);
  assert.match(literatureCard, /href="\/notes\/r0-71i\.html"/);
  assert.match(literatureCard, /joint|联合/i);
  assert.ok(literatureCard.includes("\\(K^{-2}\\)"));
  assert.ok(literatureCard.includes("\\(O(K^{-4})\\)"));
});

test("the historical recap exposes the first 73 post-R0.60 nodes from home", async () => {
  const { home, recap } = await publishedPages();
  const routeStart = home.indexOf('<section class="route-overview"');
  const routeEnd = home.indexOf('<div class="page-shell">', routeStart);
  const route = home.slice(routeStart, routeEnd);
  const routeLinks = [
    ...route.matchAll(/href="(\/notes\/r0-[^"]+\.html)"/g),
  ].map((match) => match[1]);
  const first = routeLinks.indexOf("/notes/r0-61.html");
  const expected = routeLinks.slice(first, first + 73);
  assert.equal(expected.length, 73);
  assert.equal(expected.at(-1), "/notes/r0-71i.html");

  const indexStart = recap.indexOf('<section id="node-index"');
  const indexEnd = recap.indexOf("</section>", indexStart);
  const index = recap.slice(indexStart, indexEnd);
  const actual = [
    ...index.matchAll(/href="(\/notes\/r0-[^"]+\.html)"/g),
  ].map((match) => match[1]);
  assert.deepEqual(actual, expected);
  assert.equal(new Set(actual).size, 73);
});

test("states the joint identity, volume gap, claim boundary, and R0.71J gate", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "z_t+\\nu K^2z=\\mathcal J",
    "a_t+2\\nu K^2a=2z^+\\mathcal J",
    "\\Xi_t+\\nu K^2\\Xi",
    "4\\int z^+\\mathcal J^+dt",
    "1+\\theta_\\varepsilon",
    "\\frac{71-17\\sqrt{17}}{16}",
    "\\frac{\\nu(71-17\\sqrt{17})}{3}K^2",
    "\\frac{263}{90}",
    "\\frac{36}{5}K^2",
    "d_K(0)=8K^4",
    "O(K^{-4})",
    "\\frac{3U^2}{28}",
    "3U^2/(28K^2)",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.ok(note.includes("固定 \\(\\theta\\) 的 \\(K\\to\\infty\\) 极限"));
  assert.ok(note.includes("不是有限 \\(K\\) 的精确曲线"));
  assert.match(note, /预设宽单环 frame、完整 Parseval frame 和全框架右端都没有在这里处理/);
  assert.match(note, /R0\.71J 检查全壳求和后是否出现新的 NSE 抵消/);
  assert.match(recap, /R0\.71J 检查完整 frame 求和后的正生成/);
});

test("links the formal report, two audits, certificate, and figure package", async () => {
  const { note } = await publishedPages();
  const linkedSources = [
    "research/r071i_report-source.md",
    "research/r071i_literature_audit.md",
    "research/r071i_independent_audit.md",
    "research/r071i_gap_matrix.md",
    "research/r071i_exact_audit.py",
    "research/r071i_independent_audit.py",
    "research/certificates/r071i",
    "figures/r071i-joint/fig-r071i-joint-volume-gap",
  ];
  for (const source of linkedSources) assert.ok(note.includes(source), source);

  await Promise.all([
    access(new URL("research/r071i_report-source.md", root)),
    access(new URL("research/r071i_exact_audit.py", root)),
    access(new URL("research/r071i_independent_audit.md", root)),
    access(new URL("research/r071i_independent_audit.py", root)),
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
    "joint-identity-closed-heat-volume-alone-rejected",
  );
  assert.equal(independentCertificate.status, "passed");
  assert.equal(independentCertificate.claims.hardAndSoftIdentitiesChecked, true);
  assert.equal(
    independentCertificate.claims.symmetricEightTargetModesChecked,
    true,
  );
  assert.equal(independentCertificate.claims.fullWeightedBVRejected, false);
});

test("ships synchronized note and recap PDFs plus three journal figure formats", async () => {
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
    readFile(new URL("notes/r0-71i.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71i.pdf", publicRoot)),
    readFile(new URL("figures/r0-71i-joint-volume-gap.svg", publicRoot)),
    readFile(new URL("figures/r0-71i-joint-volume-gap.pdf", publicRoot)),
    readFile(new URL("figures/r0-71i-joint-volume-gap.png", publicRoot)),
    readFile(new URL("figure.svg", figureSourceRoot)),
    readFile(new URL("figure.pdf", figureSourceRoot)),
    readFile(new URL("figure.png", figureSourceRoot)),
  ]);

  assert.match(note, /src="\/figures\/r0-71i-joint-volume-gap\.svg"/);
  assert.match(note, /href="\/notes\/r0-71i\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-71i\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-71i\.pdf"/);
  assert.match(home, /href="\/notes\/r0-71i\.pdf"/);
  assert.match(home, /href="\/figures\/r0-71i-joint-volume-gap\.pdf"/);

  assert.equal(notePdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.equal(recapPdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.ok(notePdf.length > 100_000);
  assert.ok(recapPdf.length > 100_000);
  assert.match(svg.toString("utf8"), /<svg/);
  assert.equal(figurePdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.deepEqual(svg, sourceSvg);
  assert.deepEqual(figurePdf, sourceFigurePdf);
  assert.deepEqual(png, sourcePng);
});

test("keeps the R0.71I public writing factual and free of inflated claims", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const forbiddenInflation =
    /攻关|主攻|研究纪律|三重审计|杀死错误想法|重大突破|颠覆性|世界首个|接近解决|解决了千禧年|证明了全局正则性|原创性定理|首次证明/;

  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, forbiddenInflation);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /\t/);
  }

  assert.match(note, /不是千禧年问题/);
  assert.match(note, /不作新颖性或优先权声明/);
  assert.match(note, /没有证明三维 Navier–Stokes 的全局光滑性或有限时破裂/);
  assert.match(recap, /Clay 正式问题仍然开放/);
});
