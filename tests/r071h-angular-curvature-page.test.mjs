import assert from "node:assert/strict";
import { access, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const notesRoot = new URL("notes/", publicRoot);
const figureSourceRoot = new URL(
  "figures/r071h-angular/fig-r071h-angular-curvature/",
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

function releaseToSlug(release) {
  return release.replace(/^r0(\d{2})([a-z])$/, "r0-$1$2");
}

function releaseRange() {
  const releases = [];
  for (let code = "a".charCodeAt(0); code <= "z".charCodeAt(0); code += 1) {
    releases.push("r070" + String.fromCharCode(code));
  }
  for (let code = "a".charCodeAt(0); code <= "h".charCodeAt(0); code += 1) {
    releases.push("r071" + String.fromCharCode(code));
  }
  return releases;
}

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71h.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71h.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("keeps the historical R0.71H release reachable after later releases", async () => {
  const { home, note, recap, literature } = await publishedPages();
  const opening = '<div class="task-one" id="r071h" data-release="r071h"';
  const start = home.indexOf(opening);
  const next = home.indexOf('<div class="task-one"', start + opening.length);
  const sectionEnd = home.indexOf("</section>", start);
  const end = next >= 0 && next < sectionEnd ? next : sectionEnd;
  const historicalCard = home.slice(start, end);

  assert.equal((home.match(new RegExp(opening, "g")) ?? []).length, 1);
  assert.ok(start >= 0);
  assert.match(historicalCard, /href="\/notes\/r0-71h\.html"/);
  assert.match(historicalCard, /href="\/notes\/r0-71h\.pdf"/);
  assert.match(historicalCard, /research\/r071h_report-source\.md/);
  assert.match(note, /研究笔记 R0\.71H/);
  assert.match(recap, /R0\.61–R0\.71H/);
  assert.match(recap, /收录节点：72/);
  assert.match(literature, /<b>R0\.71H<\/b>/);
  assert.match(literature, /href="\/notes\/r0-71h\.html"/);

  for (const [page, minimum] of [
    [home, 10],
    [note, 15],
    [recap, 8],
    [literature, 48],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71H/);
    assert.match(page, /src="\/i18n-en\.js\?v=\d+\.\d+"/);
  }
});

test("gives every R0.70A through R0.71H one independent progress card", async () => {
  const { home } = await publishedPages();

  for (const release of releaseRange()) {
    const slug = releaseToSlug(release);
    const opening =
      '<div class="task-one" id="' +
      release +
      '" data-release="' +
      release +
      '"';
    assert.equal(
      (home.match(new RegExp(opening, "g")) ?? []).length,
      1,
      release + ": independent progress card",
    );
    const start = home.indexOf(opening);
    const next = home.indexOf('<div class="task-one"', start + opening.length);
    const sectionEnd = home.indexOf("</section>", start);
    const end = next >= 0 && next < sectionEnd ? next : sectionEnd;
    const card = home.slice(start, end);

    assert.ok(
      card.includes('href="/notes/' + slug + '.html"'),
      release + ": HTML",
    );
    assert.ok(
      card.includes('href="/notes/' + slug + '.pdf"'),
      release + ": PDF",
    );
    assert.match(card, /<strong>结论边界：<\/strong>/, release + ": boundary");
    assert.match(
      card,
      /github\.com\/Kasifa\/Kasifa\.github\.io\/(?:blob|tree)\/main\/research\//,
      release + ": source",
    );
    assert.equal(
      (home.match(new RegExp('href="/notes/' + slug + '\\.html"', "g")) ?? [])
        .length,
      2,
      release + ": exactly one route and one progress entry",
    );

    await Promise.all([
      access(new URL(slug + ".html", notesRoot)),
      access(new URL(slug + ".pdf", notesRoot)),
    ]);
  }

  assert.doesNotMatch(home, /id="r070a-i"|id="r070p-z"/);
});

test("the historical R0.71H recap retains its 72-node index", async () => {
  const { recap } = await publishedPages();
  const indexStart = recap.indexOf('<section id="node-index"');
  const indexEnd = recap.indexOf("</section>", indexStart);
  const index = recap.slice(indexStart, indexEnd);
  const actual = [
    ...index.matchAll(/href="(\/notes\/r0-[^"]+\.html)"/g),
  ].map((match) => match[1]);
  assert.equal(new Set(actual).size, 72);
  assert.equal(actual.length, 72);
  assert.equal(actual[0], "/notes/r0-61.html");
  assert.equal(actual.at(-1), "/notes/r0-71h.html");

  assert.doesNotMatch(
    recap,
    /CONTENTS|路线怎样一步步收缩|当前门槛|价值确认|no-go|common-response|精确账本|交换子桥/,
  );
});

test("states the unit theorem, soft defects, crossing, and two-power gap exactly", async () => {
  const { note, recap } = await publishedPages();

  for (const token of [
    "E_t=d^{-1/2}P_{E^\\perp}C_t",
    "\\|E_t\\|_2^2+\\nu^2\\|P_{E^\\perp}A_0E\\|_2^2",
    "r_t=-2\\nu\\|X\\|_2^2\\le0",
    "+\\nu r_\\varepsilon m_t",
    "m_t^2/(4m)",
    "\\frac{3\\pi}{8\\sqrt\\varepsilon}",
    "D_\\delta=\\frac{3\\delta^2+4}{4}",
    "R_\\delta=\\frac{2(3\\delta^2+2)}{3\\delta^2+4}",
    "J_\\delta=\\frac{12\\delta^2}{(3\\delta^2+4)^2}",
    "K^{-2}|a_t|",
    "two-frequency-power gap",
    "\\mathfrak M_{j,Q,K}=\\nu(\\Delta+K^2)C_{j,Q}+G_{j,Q}",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.ok(note.includes("声明的低频球面 multiplier 与 \\(\\chi\\equiv1\\)"));
  assert.match(note, /这个 family 不是 integrated BV 反例/);
  assert.match(note, /没有把该结论外推到任意 fixed smooth matched frame/);
  assert.match(note, /这里不预设它能够关闭/);
  assert.match(note, /没有 DNS、拟合、ODE 积分或三维时间推进/);
  assert.match(recap, /没有证明三维 Navier–Stokes 的全局光滑性或有限时破裂/);
});

test("links the final R0.71H sources and primary literature", async () => {
  const { note, literature } = await publishedPages();

  for (const source of [
    "research/r071h_report-source.md",
    "research/r071h_literature_audit.md",
    "research/r071h_independent_audit.md",
    "research/r071h_gap_matrix.md",
    "research/r071h_exact_audit.py",
    "research/r071h_independent_audit.py",
    "research/certificates/r071h",
    "figures/r071h-angular/fig-r071h-angular-curvature",
  ]) {
    assert.ok(note.includes(source), source);
  }

  for (const source of [
    "https://arxiv.org/abs/nlin/0512034v4",
    "https://arxiv.org/abs/0705.2446v1",
    "https://arxiv.org/abs/1107.0058v4",
    "https://arxiv.org/abs/0708.3067v2",
    "https://arxiv.org/abs/1503.01746v4",
  ]) {
    assert.ok(literature.includes(source), source);
  }
});

test("ships synchronized PDFs and the three journal figure formats", async () => {
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
    readFile(new URL("notes/r0-71h.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71h.pdf", publicRoot)),
    readFile(new URL("figures/r0-71h-angular-curvature.svg", publicRoot)),
    readFile(new URL("figures/r0-71h-angular-curvature.pdf", publicRoot)),
    readFile(new URL("figures/r0-71h-angular-curvature.png", publicRoot)),
    readFile(new URL("figure.svg", figureSourceRoot)),
    readFile(new URL("figure.pdf", figureSourceRoot)),
    readFile(new URL("figure.png", figureSourceRoot)),
  ]);

  assert.match(note, /src="\/figures\/r0-71h-angular-curvature\.svg"/);
  assert.match(note, /href="\/notes\/r0-71h\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-71h\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-71h\.pdf"/);
  assert.match(home, /href="\/notes\/r0-71h\.pdf"/);
  assert.match(home, /href="\/figures\/r0-71h-angular-curvature\.pdf"/);

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

test("keeps the public writing and claim boundary clean", async () => {
  const { home, note, recap, literature } = await publishedPages();
  for (const page of [home, note, recap, literature]) {
    assert.doesNotMatch(page, /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/);
    assert.doesNotMatch(page, /解决了千禧年|证明了全局正则性|原创性定理|首次证明/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /\t/);
  }
});
