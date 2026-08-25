import assert from "node:assert/strict";
import { readdir, readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);

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
    readFile(new URL("notes/r0-71f.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71f.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);
  return { home, note, recap, literature };
}

test("publishes 130 notes, 70 recap nodes, 11 phases, and two home entries", async () => {
  const [{ home, note, recap, literature }, noteNames] = await Promise.all([
    publishedPages(),
    readdir(new URL("notes/", publicRoot)),
  ]);

  assert.equal(noteNames.filter((name) => name.endsWith(".html")).length, 130);
  assert.match(home, /<strong>130<\/strong>公开研究笔记/);
  assert.match(home, /id="r071f"/);
  assert.equal((home.match(/href="\/notes\/r0-71f\.html"/g) ?? []).length, 2);
  assert.equal((recap.match(/<article class="phase">/g) ?? []).length, 11);
  assert.match(recap, /收录节点：70/);
  assert.match(recap, /回顾截止时公开笔记：130/);
  assert.match(recap, /R0\.71F · 局部热打包与临界迹障碍/);
  assert.match(
    literature,
    /R0\.71F[\s\S]*局部化保留 heat packing，临界底边迹仍不免费/,
  );

  for (const [page, minimum] of [
    [home, 10],
    [note, 16],
    [recap, 7],
    [literature, 39],
  ]) {
    assertLocalAnchorsResolve(page, minimum);
    assert.match(page, /R0\.71G/);
  }
});

test("publishes the exact R0.71F positive results and trace boundaries", async () => {
  const { note } = await publishedPages();

  for (const token of [
    "B_Q^L=\\langle F_{j,s},\\nabla\\times(\\chi_QW_{j,s})\\rangle",
    "d_{j,Q}=\\|\\nabla\\times(\\chi_QW_{j,s})\\|_2^2",
    "A_{\\rm loc,+}(t)",
    "\\sum_{j,Q}q_{j,Q}(t,s)",
    "\\frac{N\\Gamma(\\alpha)}{2^\\alpha}",
    "q_\\phi(0)",
    "\\frac{2K^2}{1-e^{-2K^2h}}",
    "\\|u_{-,K^{-1},K}\\|_2^2=6",
    "\\frac{A_{Q_r}}{\\mathcal V_{Q_r,\\theta r^2}",
    "R0.71G",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /moving-cutoff 恒等式本身只在光滑或强解区间使用/);
  assert.ok(note.includes("标准能量自动闭合的是 \\(\\alpha=1\\)，不是全部"));
  assert.match(note, /每个非零非负 cutoff/);
  assert.match(note, /真实全局光滑 NSE 初始迹的固定动能分离/);
  assert.match(note, /不是 full-frame 两侧估计/);
  assert.ok(note.includes("临界 \\(Cr^{-2}\\) 没有被否定"));
  assert.match(note, /不是三维 Navier–Stokes 全局正则性的证明/);
  assert.match(note, /没有构造奇性/);
  assert.match(note, /没有建立外部同行评审或原创性结论/);
  assert.match(note, /不是原创性或优先权声明/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  assert.doesNotMatch(note, /解决了千禧年|证明了全局正则性|原创性定理|首次证明|严格弱于/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  assert.doesNotMatch(note, /\t/);
});

test("links every R0.71F source and all four version-locked primary sources", async () => {
  const { note, literature } = await publishedPages();

  for (const source of [
    "research/r071f_report-source.md",
    "research/r071f_literature_audit.md",
    "research/r071f_independent_audit.md",
    "research/r071f_gap_matrix.md",
    "research/r071f_exact_audit.py",
    "research/r071f_independent_audit.py",
    "research/certificates/r071f",
    "figures/r071f-local-trace/fig-r071f-local-trace",
  ]) {
    assert.ok(note.includes(source), source);
  }

  for (const source of [
    "https://arxiv.org/abs/2008.05588v2",
    "https://arxiv.org/html/2009.14291v1",
    "https://arxiv.org/html/2606.16438v1",
    "https://arxiv.org/html/2606.27560v1",
  ]) {
    assert.ok(note.includes(source), source);
  }
  for (const source of [
    "https://arxiv.org/abs/2008.05588v2",
    "https://arxiv.org/abs/2009.14291v1",
    "https://arxiv.org/abs/2606.16438v1",
    "https://arxiv.org/abs/2606.27560v1",
  ]) {
    assert.ok(literature.includes(source), source);
  }
  assert.match(note, /它不是从零阶热体积恢复这里的 signed bottom trace/);
  assert.match(note, /其余 shell budgets 的可和性仍是额外输入/);
});

test("links and ships the synchronized R0.71F PDFs and journal figure", async () => {
  const [{ home, note, recap }, notePdf, recapPdf, svg, figurePdf, png] =
    await Promise.all([
      publishedPages(),
      readFile(new URL("notes/r0-71f.pdf", publicRoot)),
      readFile(new URL("recap-r0-61-r0-71f.pdf", publicRoot)),
      readFile(new URL("figures/r0-71f-local-trace.svg", publicRoot), "utf8"),
      readFile(new URL("figures/r0-71f-local-trace.pdf", publicRoot)),
      readFile(new URL("figures/r0-71f-local-trace.png", publicRoot)),
    ]);

  assert.match(note, /src="\/figures\/r0-71f-local-trace\.svg"/);
  assert.match(note, /href="\/figures\/r0-71f-local-trace\.pdf"/);
  assert.match(note, /href="\/figures\/r0-71f-local-trace\.png"/);
  assert.match(note, /href="\/notes\/r0-71f\.pdf"/);
  assert.match(recap, /href="\/recap-r0-61-r0-71f\.pdf"/);
  assert.match(home, /href="\/notes\/r0-71f\.pdf"/);
  assert.match(home, /href="\/figures\/r0-71f-local-trace\.pdf"/);
  assert.equal(notePdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.equal(recapPdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.ok(notePdf.length > 100_000);
  assert.ok(recapPdf.length > 100_000);
  assert.match(svg, /<svg/);
  assert.equal(figurePdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
});
