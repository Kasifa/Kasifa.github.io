import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const figureSourceRoot = new URL(
  "figures/r071g-residence/fig-r071g-residence-gate/",
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

async function publishedPages() {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71g.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71g.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("retains the R0.71G release checkpoint after later site releases", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(new URL("notes/", publicRoot)),
  ]);

  assert.ok(noteNames.filter((name) => name.endsWith(".html")).length >= 131);
  assert.match(home, /id="r071g"/);
  assert.equal((home.match(/href="\/notes\/r0-71g\.html"/g) ?? []).length, 2);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 12);
  assert.match(recap, /收录节点：71/);
  assert.match(recap, /回顾截止时公开笔记：131/);
  assert.match(recap, /R0\.71G · 正号驻留反例与加权 BV 门槛/);
  assert.match(literature, /R0\.71G[\s\S]*Sign-only 驻留失败/);

  for (const [page, minimum] of [
    [home, 10],
    [note, 15],
    [recap, 7],
    [literature, 39],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71G/);
    assert.match(page, /src="\/i18n-en\.js\?v=/);
  }

  assert.match(note, /href="\/recap-r0-61-r0-71g\.html"/);
  assert.match(recap, /href="\/notes\/r0-71g\.html"/);
});

test("publishes the exact R0.71G time ledger, witness, and claim boundaries", async () => {
  const { note, recap } = await publishedPages();

  for (const token of [
    "\\partial_tL=\\nu\\Delta L",
    "((\\partial_m u\\cdot\\nabla)\\partial_m u)",
    "d^{-1/2}\\langle P_{E^\\perp}F,C_t\\rangle",
    "c_m'=-(m^2+1)c_m+i\\mu e^{-\\theta}(c_{m-1}+c_{m+1})",
    "\\|u_0\\|_2^2=6",
    "q_\\varepsilon=(B^+)^2/(d+\\varepsilon)",
    "\\sum_nK_n^{-2}\\int A_n",
    "\\frac C2K^{-2}",
    "K_j^{-4}\\frac{\\|T_j\\partial_tL\\|_2^2}{Y}",
    "\\frac{\\partial_t(q/Y)}{q/Y}",
  ]) {
    assert.ok(note.includes(token), token);
  }

  assert.match(note, /不是 DNS，也不是奇性模拟/);
  assert.match(note, /这是一条条件定理，不是 residence 单独的推论/);
  assert.match(note, /未证明：一般 NSE 解的归一化高迹 occupation/);
  assert.match(note, /不是文献不存在证明，也不是原创性或优先权声明/);
  assert.match(note, /未得到：无条件继续性、有限时奇性、外部同行评审、原创性结论或千禧年问题解答/);
  assert.match(recap, /问题状态：仍未解决/);
  assert.match(recap, /没有证明三维 Navier–Stokes 的全局光滑性或有限时破裂/);

  for (const page of [note, recap]) {
    assert.doesNotMatch(page, /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/);
    assert.doesNotMatch(page, /解决了千禧年|证明了全局正则性|原创性定理|首次证明|严格弱于/);
    assert.doesNotMatch(page, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
    assert.doesNotMatch(page, /\t/);
  }
});

test("links every R0.71G source and all six version-locked primary sources", async () => {
  const { note, literature } = await publishedPages();

  for (const source of [
    "research/r071g_report-source.md",
    "research/r071g_literature_audit.md",
    "research/r071g_independent_audit.md",
    "research/r071g_gap_matrix.md",
    "research/r071g_exact_audit.py",
    "research/r071g_independent_audit.py",
    "research/certificates/r071g",
    "figures/r071g-residence/fig-r071g-residence-gate",
  ]) {
    assert.ok(note.includes(source), source);
  }

  for (const source of [
    "https://arxiv.org/abs/1102.1944v2",
    "https://arxiv.org/abs/1507.06611v6",
    "https://arxiv.org/abs/math/0406146",
    "https://arxiv.org/abs/1710.05569v4",
    "https://arxiv.org/abs/2203.07950v1",
    "https://arxiv.org/abs/2606.27560v1",
  ]) {
    assert.ok(note.includes(source), source + ": note");
    assert.ok(literature.includes(source), source + ": literature");
  }
});

test("links and ships both synchronized R0.71G PDFs and all three journal figure formats", async () => {
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
    readFile(new URL("notes/r0-71g.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71g.pdf", publicRoot)),
    readFile(new URL("figures/r0-71g-residence-gate.svg", publicRoot)),
    readFile(new URL("figures/r0-71g-residence-gate.pdf", publicRoot)),
    readFile(new URL("figures/r0-71g-residence-gate.png", publicRoot)),
    readFile(new URL("figure.svg", figureSourceRoot)),
    readFile(new URL("figure.pdf", figureSourceRoot)),
    readFile(new URL("figure.png", figureSourceRoot)),
  ]);

  assert.match(note, /src="\/figures\/r0-71g-residence-gate\.svg"/);
  assert.match(note, /href="\/figures\/r0-71g-residence-gate\.pdf"/);
  assert.match(note, /href="\/figures\/r0-71g-residence-gate\.png"/);
  assert.match(note, /href="\/notes\/r0-71g\.pdf"/);
  assert.match(note, /href="\/recap-r0-61-r0-71g\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-71g\.pdf"/);
  assert.match(home, /href="\/notes\/r0-71g\.pdf"/);
  assert.match(home, /href="\/figures\/r0-71g-residence-gate\.pdf"/);

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
