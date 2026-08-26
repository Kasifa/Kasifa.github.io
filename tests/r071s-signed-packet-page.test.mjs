import assert from "node:assert/strict";
import { createHash } from "node:crypto";
import { access, readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const certificatesRoot = new URL("research/certificates/r071s/", root);
const figureSourceRoot = new URL(
  "figures/r071s-signed-packet/fig-r071s-signed-packet/",
  root,
);

function occurrenceCount(value, fragment) {
  return value.split(fragment).length - 1;
}

function sha256(value) {
  return createHash("sha256").update(value).digest("hex");
}

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
  assert.ok(end > start, "release card closing boundary");
  return html.slice(start, end);
}

function releaseSequence() {
  const values = [];
  for (let code = "a".charCodeAt(0); code <= "z".charCodeAt(0); code += 1) {
    values.push("r0-70" + String.fromCharCode(code));
  }
  for (let code = "a".charCodeAt(0); code <= "s".charCodeAt(0); code += 1) {
    values.push("r0-71" + String.fromCharCode(code));
  }
  return values;
}

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71s.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71s.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("keeps R0.71S complete while v1.15 publishes R0.72B as current", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(notesRoot),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 152);
  assert.match(home, /<strong>v1\.15<\/strong>网页版本/);
  assert.match(home, /<strong>152<\/strong>公开研究笔记/);
  assert.match(home, /<strong>R0\.72B<\/strong>最新研究节点/);
  assert.match(home, /<span class="route-range">R0\.69P–R0\.72B<\/span>/);
  assert.match(home, /展开 62 篇公开笔记/);
  assert.match(home, /累计回顾收录 92 个节点；全站现有 152 篇公开研究笔记/);
  assert.match(home, /R0\.70A–R0\.72B 共 54 个完成版本/);
  assert.match(home, /NEXT · R0\.72C/);

  const currentRoute = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72B">([\s\S]*?)<\/nav>/,
  );
  assert.ok(currentRoute);
  assert.equal(occurrenceCount(currentRoute[1], 'href="/notes/'), 62);

  assert.ok(occurrenceCount(recap, '<article class="phase">') >= 12);
  assert.match(recap, /收录节点：83/);
  assert.match(recap, /回顾截止时公开笔记：143/);
  assert.match(recap, /<strong>45<\/strong><span>R0\.70A–R0\.71S 完成版本/);
  assert.match(literature, /R0\.69P–R0\.72B/);
  assert.match(literature, /开放接口 · R0\.72C/);

  for (const [page, minimum, i18nVersion] of [
    [home, 10, "1.15"],
    [note, 14, "1.04"],
    [recap, 8, "1.04"],
    [literature, 50, "1.15"],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71S/);
    assert.ok(page.includes('src="/i18n-en.js?v=' + i18nVersion + '"'));
  }
});

test("ships one R0.71S release card and the complete reader-facing package", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071s" data-release="r071s"';
  const card = sliceReleaseCard(home, opening);

  assert.equal(occurrenceCount(home, opening), 1);
  assert.equal(occurrenceCount(home, 'href="/notes/r0-71s.html"'), 2);
  for (const token of [
    'href="/notes/r0-71s.html"',
    'href="/notes/r0-71s.pdf"',
    'href="/figures/r0-71s-signed-packet.pdf"',
    "research/certificates/r071s",
    "research/r071s_report-source.md",
    "research/r071s_literature_audit.md",
    "research/r071s_gap_matrix.md",
    "research/r071s_independent_audit.md",
    "figures/r071s-signed-packet/fig-r071s-signed-packet",
    'href="/recap-r0-61-r0-72b.html"',
    'href="/recap-r0-61-r0-72b.pdf"',
  ]) {
    assert.ok(card.includes(token), token);
  }
  assert.match(card, /R0\.71T 已完成/);

  for (const token of [
    'href="/recap-r0-61-r0-71s.html"',
    'href="/notes/r0-71s.pdf"',
    'href="/recap-r0-61-r0-71s.pdf"',
    'src="/figures/r0-71s-signed-packet.svg"',
    "research/r071s_report-source.md",
    "research/r071s_literature_audit.md",
    "research/r071s_independent_audit.md",
    "research/r071s_gap_matrix.md",
    "research/r071s_exact_audit.py",
    "research/r071s_independent_audit.py",
    "research/certificates/r071s",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(recap, /href="\/notes\/r0-71s\.html"/);
  assert.match(recap, /href="\/figures\/r0-71s-signed-packet\.pdf"/);
  assert.match(literature, /<header><b>R0\.71S<\/b>/);

  for (const path of [
    "notes/r0-71s.pdf",
    "recap-r0-61-r0-71s.pdf",
    "figures/r0-71s-signed-packet.pdf",
    "figures/r0-71s-signed-packet.svg",
    "figures/r0-71s-signed-packet.png",
  ]) {
    await access(new URL(path, publicRoot));
  }
});

test("states the finite packet theorem, sharp taxes, and initial-versus-internal boundary", async () => {
  const { home, note, recap, literature } = await publishedPages();

  for (const token of [
    "f_\\beta(t)=\\frac{\\langle F_{j_\\beta}(t),e_\\beta\\rangle}{\\sqrt{Y(t)}}",
    "a_\\beta=\\kappa_{j_\\beta}^{-2}\\bigl(f_\\beta(t_\\beta)^+\\bigr)^2",
    "h_\\beta=\\theta_\\beta\\kappa_{j_\\beta}^{-2}",
    "p_\\beta\\ge(1-\\delta)\\mu\\sqrt{h_\\beta}",
    "\\frac{B_{\\rm crit}}",
    "{\\mu^2(1-\\delta)^2\\theta_-}",
    "\\|\\Phi_\\beta\\|^2=\\kappa_{j_\\beta}^2",
    "B_{\\rm crit}\\ge\\max_\\beta\\kappa_{j_\\beta}^2",
    "G_{k\\ell}=\\left(1-\\frac{|b_k-b_\\ell|}{h}\\right)_+",
    "\\kappa^2\\frac{1-e^{-2\\nu\\theta}}{2\\nu}",
    "k_0=\\langle1,K1\\rangle",
    "A_-=A_+&gt;0",
    String.raw`signed face \(A_+-A_-=0\)`,
    "不是 NSE trajectory",
    "observation-boundary entry",
    "不覆盖只计算 internal entries 的定理",
    String.raw`不能只是裸 \(dt\) 积分`,
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(
    note,
    /sampling coherence.*统一 (?:θ|\\theta).*B_\{\\rm crit\}.*hypotheses/is,
  );
  assert.match(note, /单包.*至少.*κ²/is);
  assert.match(note, /同向聚簇.*事件数/is);
  assert.match(note, /真实 NSE 初始 face.*协变缩放/is);
  assert.match(note, /initial observation face/is);
  assert.match(note, /没有得到新的无条件继续性判据/is);

  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, /我们/);
    assert.doesNotMatch(page, /千禧年问题已经解决|解决了千禧年问题/);
    assert.doesNotMatch(page, /证明(?:了)?三维 Navier.?Stokes 全局正则性/iu);
    assert.doesNotMatch(page, /所有 internal entries (?:均|都)?(?:被)?排除/iu);
    assert.doesNotMatch(page, /even touch (?:is|是) (?:a )?(?:genuine )?NSE trajectory/iu);
    assert.doesNotMatch(page, /bare Leray time integral (?:proves|gives) global regularity/iu);
    assert.doesNotMatch(page, /uniform internal-entry packing (?:is )?proved/iu);
  }

  assert.match(home, /observation-boundary|初始 observation face/i);
  assert.match(recap, /internal entr(?:y|ies)/i);
  assert.match(
    literature,
    /genuine NSE initial-face|initial observation-boundary|初始 observation face/i,
  );
});

test("verifies the R0.71S report, gap boundary, certificates, and package inventory", async () => {
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
    "build_manifest.py",
    "caption.md",
    "command.txt",
    "contract.json",
    "data.csv",
    "environment.txt",
    "exact-certificate.json",
    "figure-contract.md",
    "figure-data-metadata.json",
    "figure.pdf",
    "figure.png",
    "figure.svg",
    "generate_data.py",
    "independent-certificate.json",
    "independent-validation.json",
    "independent_validate.py",
    "manifest.json",
    "plot.py",
    "qa-grayscale.png",
    "qa-original.png",
    "qa-report.md",
    "qa_images.py",
    "validate_data.py",
    "validation.json",
  ];

  await Promise.all([
    ...requiredCertificateFiles.map((path) =>
      access(new URL(path, certificatesRoot)),
    ),
    ...requiredFigureFiles.map((path) => access(new URL(path, figureSourceRoot))),
  ]);

  const [exact, independent, report, literature, gap, independentAudit] =
    await Promise.all([
      readFile(new URL("result.json", certificatesRoot), "utf8").then(JSON.parse),
      readFile(new URL("independent-result.json", certificatesRoot), "utf8").then(JSON.parse),
      readFile(new URL("research/r071s_report-source.md", root), "utf8"),
      readFile(new URL("research/r071s_literature_audit.md", root), "utf8"),
      readFile(new URL("research/r071s_gap_matrix.md", root), "utf8"),
      readFile(new URL("research/r071s_independent_audit.md", root), "utf8"),
    ]);

  assert.equal(exact.release, "R0.71S");
  assert.equal(exact.status, "passed");
  assert.ok(Object.values(exact.checks).every((check) => check.passed));
  assert.match(exact.scope, /finite signed\/bilinear time-packet method audit/i);
  assert.match(exact.scope, /no NSE packet packing theorem/i);
  assert.equal(
    exact.checks.boxDiagonalScaling.rows.at(-1).constantReproductionDiagonal,
    "32768",
  );
  assert.equal(
    exact.checks.finiteBoxGram.finiteIntervalEnclosure,
    "p-(p^2-1)/(3N) <= lambda_max <= p",
  );
  assert.match(
    exact.checks.backwardHeatConstants.reproductionIdentity,
    /nu\*K\^2\/2.*coth/i,
  );
  assert.match(
    exact.checks.bilinearMeanDichotomy.zeroMeanCase,
    /annihilates constant leading data exactly/i,
  );
  assert.equal(exact.checks.evenTouchCancellation.rows.at(-1).totalSignedMass, "0");
  assert.match(
    exact.checks.genuineInitialFaceScaling.boundary,
    /one-sided genuine NSE initial face/i,
  );
  assert.match(
    exact.checks.genuineInitialFaceScaling.boundary,
    /not an internal even touch.*positive-time integration/i,
  );

  assert.equal(independent.release, "R0.71S");
  assert.equal(independent.status, "passed");
  assert.ok(Object.values(independent.checks).every((check) => check.passed));
  assert.equal(independent.checks.heatPacketChecks.gaussLegendreOrder, 512);
  assert.ok(independent.checks.gramChecks.maximumEigenResidual < 1e-12);
  assert.equal(independent.checks.initialFaceChecks.maximumEntryError, 0);
  assert.match(independent.scope, /no positive-time NSE integration/i);

  for (const token of [
    "Theorem 2.1 -- finite critical directional-packet payment",
    "B_{\\rm crit}\\ge\\max_{\\beta\\in\\mathcal E}\\kappa_{j(\\beta)}^2",
    "B_{\\rm crit}\\ge N\\kappa_j^2",
    "necessary directional Carleson condition",
    "Theorem 8.1 -- no scale-uniform bare Leray-time payment including the initial face",
    "It does not prove any of the following",
    "internal NSE entry",
  ]) {
    assert.ok(report.includes(token), token);
  }
  assert.match(gap, /S16.*rejected by genuine NSE scaling/i);
  assert.match(gap, /S17.*not proved/i);
  assert.match(literature, /bounded negative finding/i);
  assert.match(independentAudit, /initial.*boundary|observation-boundary/i);
  assert.doesNotMatch(report, /we prove global regularity/i);
});

test("ships hash-identical R0.71S figure mirrors and keeps 45 releases through R0.71S", async () => {
  const [
    { home },
    svg,
    pdf,
    png,
    sourceSvg,
    sourcePdf,
    sourcePng,
    manifest,
  ] = await Promise.all([
    publishedPages(),
    readFile(new URL("figures/r0-71s-signed-packet.svg", publicRoot)),
    readFile(new URL("figures/r0-71s-signed-packet.pdf", publicRoot)),
    readFile(new URL("figures/r0-71s-signed-packet.png", publicRoot)),
    readFile(new URL("figure.svg", figureSourceRoot)),
    readFile(new URL("figure.pdf", figureSourceRoot)),
    readFile(new URL("figure.png", figureSourceRoot)),
    readFile(new URL("manifest.json", figureSourceRoot), "utf8").then(JSON.parse),
  ]);

  assert.match(svg.toString("utf8"), /<svg/);
  assert.equal(pdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
  assert.deepEqual(svg, sourceSvg);
  assert.deepEqual(pdf, sourcePdf);
  assert.deepEqual(png, sourcePng);
  assert.equal(manifest.figureId, "fig-r071s-signed-packet");
  assert.equal(manifest.figure.widthMillimetres, 178);
  assert.equal(manifest.figure.heightMillimetres, 118);
  assert.equal(manifest.computation.pdeTimeStepping, false);
  assert.equal(manifest.computation.dns, false);
  assert.match(manifest.claimBoundary, /even touch.*not an NSE trajectory/i);
  assert.match(manifest.claimBoundary, /initial.*face|observation-boundary/i);

  for (const [path, publicValue, sourceValue] of [
    ["figure.svg", svg, sourceSvg],
    ["figure.pdf", pdf, sourcePdf],
    ["figure.png", png, sourcePng],
  ]) {
    const expected = manifest.figure.outputs.find((output) => output.path === path);
    assert.ok(expected, path);
    assert.equal(sha256(publicValue), expected.sha256, "public hash " + path);
    assert.equal(sha256(sourceValue), expected.sha256, "source hash " + path);
  }

  const routeMatch = home.match(
    /<nav class="route-note-links" aria-label="R0\.69P–R0\.72B">([\s\S]*?)<\/nav>/,
  );
  assert.ok(routeMatch);
  const releases = releaseSequence();
  assert.equal(releases.length, 45);
  for (const slug of releases) {
    const releaseId = slug.replaceAll("-", "");
    const link = 'href="/notes/' + slug + '.html"';
    const opening =
      '<div class="task-one" id="' +
      releaseId +
      '" data-release="' +
      releaseId +
      '"';
    await access(new URL("notes/" + slug + ".html", publicRoot));
    assert.equal(occurrenceCount(home, opening), 1, releaseId);
    assert.equal(occurrenceCount(home, link), 2, slug);
    assert.equal(occurrenceCount(routeMatch[1], link), 1, "route " + slug);
    assert.equal(
      occurrenceCount(sliceReleaseCard(home, opening), link),
      1,
      "card " + slug,
    );
  }
});
