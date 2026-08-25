import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);

function assertLocalAnchorsResolve(html) {
  const ids = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const targets = [...html.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(targets.length >= 14);
  for (const target of targets) assert.ok(ids.has(target), target);
}

test("publishes the exact R0.71E projected-Lamb decision", async () => {
  const [home, note, recap, literature] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71e.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71e.html", publicRoot), "utf8"),
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r071e"/);
  assert.equal((home.match(/href="\/notes\/r0-71e\.html"/g) ?? []).length, 2);
  assert.match(recap, /R0\.71E · Projected-Lamb 热体积与底边迹/);
  assert.match(
    literature,
    /Projected-Lamb 热体积由 Leray 能量无条件控制/,
  );
  for (const token of [
    "u\\times\\omega=L+\\nabla B",
    "(\\partial_t-\\nu\\partial_s)W_{j,s}",
    "b_{j,s}=\\langle\\nabla\\times W_{j,s},A_{j,s}L\\rangle",
    "\\Theta_s^2\\le\\|e^{s\\Delta}L\\|_2^2",
    "\\mathcal V(t)=\\frac1{Y(t)}",
    "A_{\\rm sb,+}=\\Lambda_L^2\\mathcal V",
    "q_{\\rm lo}(0)=2K^2\\int_0^\\infty",
    "A_{\\rm sb,+}(0)=2K^2\\mathcal V(0)",
    "R0.71F",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assertLocalAnchorsResolve(note);
});

test("keeps the positive theorem and unresolved trace boundary explicit", async () => {
  const note = await readFile(new URL("notes/r0-71e.html", publicRoot), "utf8");

  assert.match(note, /归一化(?:竖直)?热体积由 Leray 能量无条件控制/);
  assert.match(note, /不能从热体积免费恢复底边值/);
  assert.match(note, /不是新的无条件正则性判据/);
  assert.match(note, /零均值周期 Leray–Hopf 解/);
  assert.match(note, /Galilean 归一化/);
  assert.ok(note.includes("\\sum_j|m_j(k)|^2=1"));
  assert.match(note, /零 Fourier 模上置零/);
  assert.ok(note.includes("\\(Y=0\\) 时令 \\(\\mathcal V=0\\)"));
  assert.ok(note.includes("\\(Y=0\\) 时令 \\(A_{\\rm sb,+}=0\\)"));
  assert.ok(note.includes("分母为零时令 \\(\\Lambda_L=0\\)"));
  assert.ok(note.includes("在光滑或强解区间、且 \\(Y&gt;0\\) 时"));
  assert.ok(note.includes("A_{\\rm sb,+}(0)=2K^2\\mathcal V(0)"));
  assert.ok(!note.includes("A_{\\rm sb,+}=2K^2\\mathcal V"));
  assert.ok(
    note.includes(
      "(\\partial_t+V_j\\cdot\\nabla-\\nu\\partial_s)\\phi=R_{\\rm shape}",
    ),
  );
  assert.match(note, /不是不存在证明，也不是原创性或优先权声明/);
  assert.match(note, /没有证明全局正则性/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|杀死错误想法|突破/);
  assert.doesNotMatch(note, /[\u0000-\u0008\u000b\u000c\u000e-\u001f\u007f]/);
  assert.doesNotMatch(note, /\t/);
});

test("links the complete R0.71E sources and closest literature overlap", async () => {
  const note = await readFile(new URL("notes/r0-71e.html", publicRoot), "utf8");
  for (const source of [
    "research/r071e_report-source.md",
    "research/r071e_literature_audit.md",
    "research/r071e_independent_audit.md",
    "research/r071e_exact_audit.py",
    "research/r071e_independent_audit.py",
    "research/certificates/r071e",
    "figures/r071e-projected-lamb-trace/fig-r071e-projected-lamb-trace",
    "19880002646",
    "10.1063/1.858488",
    "10.1017/jfm.2021.914",
    "2203.07950",
    "2606.27560",
    "2008.05588",
    "2009.14291",
  ]) {
    assert.ok(note.includes(source), source);
  }
});

test("ships synchronized R0.71E PDFs and journal figure copies", async () => {
  const [note, notePdf, recapPdf, svg, figurePdf, png] = await Promise.all([
    readFile(new URL("notes/r0-71e.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71e.pdf", publicRoot)),
    readFile(new URL("recap-r0-61-r0-71e.pdf", publicRoot)),
    readFile(
      new URL("figures/r0-71e-projected-lamb-trace.svg", publicRoot),
      "utf8",
    ),
    readFile(new URL("figures/r0-71e-projected-lamb-trace.pdf", publicRoot)),
    readFile(new URL("figures/r0-71e-projected-lamb-trace.png", publicRoot)),
  ]);

  assert.match(note, /src="\/figures\/r0-71e-projected-lamb-trace\.svg"/);
  assert.match(note, /href="\/figures\/r0-71e-projected-lamb-trace\.pdf"/);
  assert.match(note, /href="\/figures\/r0-71e-projected-lamb-trace\.png"/);
  assert.match(note, /href="\/notes\/r0-71e\.pdf"/);
  assert.equal(notePdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.equal(recapPdf.subarray(0, 5).toString("ascii"), "%PDF-");
  assert.ok(notePdf.length > 100_000);
  assert.ok(recapPdf.length > 100_000);
  assert.match(svg, /<svg/);
  assert.equal(figurePdf.subarray(0, 4).toString("ascii"), "%PDF");
  assert.equal(png.subarray(1, 4).toString("ascii"), "PNG");
});

test("retains the R0.71E cumulative recap and corrected bibliography", async () => {
  const [literature, recap] = await Promise.all([
    readFile(new URL("literature-review.html", publicRoot), "utf8"),
    readFile(new URL("recap-r0-61-r0-71e.html", publicRoot), "utf8"),
  ]);

  assert.ok((literature.match(/<li id="ref-/g) ?? []).length >= 37);
  for (const bibliography of [
    "Filtered Vortex Stretching and Subgrid Defects for the Three-Dimensional Navier–Stokes Equations",
    "Logarithmic Depletion of Vortex Stretching and Singularity Evasion in the 3D Navier–Stokes Equations",
    "On helicity fluctuations and the energy cascade in turbulence",
    "ICASE-87-69 / NASA-CR-178403",
    "Nonlinear amplification in hydrodynamic turbulence",
    "J. Fluid Mech. 930, R2 (2022)",
    "Construction of Maximal Functions associated with Skewed Cylinders Generated by Incompressible Flows and Applications",
  ]) {
    assert.ok(literature.includes(bibliography), bibliography);
  }
  assert.match(recap, /收录节点：69/);
  assert.match(recap, /回顾截止时公开笔记：129/);
  assert.match(recap, /href="\/recap-r0-61-r0-71e\.pdf"/);
  assert.match(recap, /src="\/i18n-en\.js\?v=0\.90"/);
});
