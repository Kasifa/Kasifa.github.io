import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);

function assertLocalAnchorsResolve(html) {
  const ids = new Set([...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]));
  const targets = [...html.matchAll(/href="#([^"]+)"/g)].map((match) => match[1]);
  assert.ok(targets.length >= 16);
  for (const target of targets) assert.ok(ids.has(target), target);
}

test("publishes the exact R0.71D material heat-tent decision", async () => {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71d.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71d.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r071d"/);
  assert.equal((home.match(/href="\/notes\/r0-71d\.html"/g) ?? []).length, 2);
  assert.match(recap, /R0\.71B–R0\.71D · 正输出系数、有符号传播和物质热 tent/);
  assert.match(literature, /完整物质热 tent 仍保留临界黏性缺陷/);
  for (const token of [
    "(\\partial_t+u\\cdot\\nabla-\\nu\\partial_s)W_j",
    "[u\\cdot\\nabla,A_{j,s}]\\omega",
    "(u-U_j)\\cdot\\nabla\\phi+R_{\\rm shape}",
    "\\beta_++\\beta_-=0",
    "\\frac{\\delta_k}{Y}=\\frac{\\nu^2\\rho^2}{2+\\rho}k^2",
    "\\tau_k=\\theta/(\\nu k^2)",
    "-\\rho ma/4",
    "R0.71E",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assertLocalAnchorsResolve(note);
});

test("keeps the exact no-go and open nonlinear boundary explicit", async () => {
  const note = await readFile(new URL("notes/r0-71d.html", publicRoot), "utf8");

  assert.match(note, /几何型通用估计/);
  assert.match(note, /没有说明加入三维拉伸、交换子和压力相关后仍不可能出现额外小量/);
  assert.match(note, /不证明所有自适应 tent 缺陷发散/);
  assert.match(note, /不是不存在、新颖性或优先权证明/);
  assert.match(note, /没有改进已有无条件正则性理论/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  assert.doesNotMatch(note.slice(note.indexOf("<body")), /\\\\\(/);
});

test("links the complete R0.71D source and closest literature overlap", async () => {
  const note = await readFile(new URL("notes/r0-71d.html", publicRoot), "utf8");
  for (const source of [
    "research/r071d_report-source.md",
    "research/r071d_literature_audit.md",
    "research/r071d_independent_audit.md",
    "research/r071d_exact_audit.py",
    "research/r071d_independent_audit.py",
    "research/certificates/r071d",
    "figures/r071d-material-heat-tent/fig-r071d-critical-heat-defect",
    "2606.12756",
    "AIHPC/20",
    "s00205-021-01661-4",
    "10.2140/apde.2013.6.25",
  ]) {
    assert.ok(note.includes(source), source);
  }
});

test("ships synchronized R0.71D PDFs and journal figure copies", async () => {
  const [note, notePdf, recapPdf, svg, figurePdf, png] = await Promise.all([
    readFile(new URL("notes/r0-71d.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71d.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71d.pdf", publicRoot)),
    readFile(new URL("figures/r0-71d-critical-heat-defect.svg", publicRoot), "utf8"),
    readFile(new URL("figures/r0-71d-critical-heat-defect.pdf", publicRoot)),
    readFile(new URL("figures/r0-71d-critical-heat-defect.png", publicRoot)),
  ]);

  assert.match(note, /src="\/figures\/r0-71d-critical-heat-defect\.svg"/);
  assert.match(note, /href="\/figures\/r0-71d-critical-heat-defect\.pdf"/);
  assert.match(note, /href="\/figures\/r0-71d-critical-heat-defect\.png"/);
  assert.match(note, /href="\/notes\/r0-71d\.pdf"/);
  assert.equal(notePdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.equal(recapPdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.ok(notePdf.length > 100_000);
  assert.ok(recapPdf.length > 100_000);
  assert.match(svg, /<svg/);
  assert.equal(figurePdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
});

test("retains the R0.71D historical recap", async () => {
  const recap = await readFile(
    new URL("recap-r0-61-r0-71d.html", publicRoot),
    "utf8",
  );
  assert.match(recap, /收录节点：68/);
  assert.match(recap, /回顾截止时公开笔记：128/);
  assert.match(recap, /href="\/recap-r0-61-r0-71d\.pdf"/);
  assert.match(recap, /src="\/i18n-en\.js\?v=0\.89"/);
});
