import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const archiveRoot = new URL(
  "figures/r070o-rank-bridge/fig-r070o-rank-bridge/",
  root,
);

function assertLocalAnchorsResolve(html, minimum) {
  const ids = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const targets = [...html.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(
    targets.length >= minimum,
    "only " + targets.length + " local targets",
  );
  for (const target of targets) {
    assert.ok(ids.has(target), "missing local target #" + target);
  }
}

function assertBilingualAssetsPrecedeMathJax(html) {
  const css = html.indexOf('href="/bilingual.css"');
  const dictionary = html.search(/src="\/i18n-en\.js(?:\?[^\"]*)?"/);
  const runtime = html.indexOf('src="/bilingual.js"');
  const mathJax = html.indexOf("mathjax@3/es5/tex-mml-chtml.js");
  assert.ok(css >= 0 && dictionary > css && runtime > dictionary);
  assert.ok(mathJax > runtime, "MathJax must load after bilingual assets");
}

test("publishes the exact R0.70O rank strata and reconstruction boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-70o.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r070o"/);
  assert.equal((home.match(/href="\/notes\/r0-70o\.html"/g) ?? []).length, 2);
  for (const token of [
    "\\lambda_3=\\min_{|n|=1}",
    "\\lambda_2+\\lambda_3",
    "\\mathsf C_\\delta",
    "\\mathsf L_{\\delta,\\eta}",
    "\\mathsf P_{\\delta,\\eta}",
    "(1-2\\eta)E",
    "(\\eta-2\\delta)E",
    "\\dot Q=\\Sigma Q+Q\\Sigma+F",
    "\\dot\\lambda_a=2\\lambda_a\\sigma_{aa}+f_{aa}",
    "\\|\\partial_iP_1\\|_F",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /互斥、完备/);
  assert.ok(note.includes("归一化三分法只在 \\(E&gt;0\\) 上使用"));
  assert.match(note, /谱隙只是分母/);
});

test("states the smooth obstruction, endpoint caveats, and positive theorem", async () => {
  const note = await readFile(new URL("notes/r0-70o.html", publicRoot), "utf8");

  for (const token of [
    "A(N_qe_2)\\to0",
    "N_q\\geq2",
    "(u_N\\cdot\\nabla)u_N=0",
    "{A(Ne_2)\\over4\\sqrt\\nu}",
    "{1\\over2\\nu^{1/4}}",
    "\\Phi(0)=0",
    "\\theta_{N,T}=1-e^{-4\\nu N^2T}",
    "{1\\over A(Ne_2)}",
    "[\\tau,\\infty)",
    "L^2\\setminus H^1",
    "A(k)\\geq a_0",
    "A(k)\\geq a_0|k|^{-1}",
    "[T_j,P]\\omega",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /“有限滤波器”本身不够/);
  assert.match(note, /固定正延迟/);
  assert.match(note, /初始端点的定性重建失败/);
  assert.match(note, /固定投影的正确条件是全频下框架/);
  assert.ok(note.includes("有限指标集 \\(J\\)"));
  assert.ok(note.includes("固定非负权重 \\(w_j\\geq0\\)"));
  assert.ok(note.includes("当 \\(A(Ne_2)&gt;0\\) 时"));
  assert.ok(note.includes("\\operatorname{Ran}P"));
  assert.match(note, /mean-zero/);
  assert.match(note, /compact-band 定性失败出现在粗糙初始端点/);
  assert.match(note, /高频盲有限标量滤波不能替代全频覆盖/);
  assert.match(note, /\\mathbb T\^3[\s\S]{0,180}\\mathbb R\^3/);
  assert.match(note, /没有得到新的继续性判据/);
  assert.match(note, /没有解决千禧年问题/);
  assert.match(note, /完整回归：609 \/ 609/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /__[A-Z0-9_]+__/);
  assertLocalAnchorsResolve(note, 12);
  assertBilingualAssetsPrecedeMathJax(note);
});

test("keeps every R0.70O public figure byte-exact and links the archive", async () => {
  const note = await readFile(new URL("notes/r0-70o.html", publicRoot), "utf8");
  for (const source of [
    "research/r070o_report-source.md",
    "research/r070o_literature_audit.md",
    "research/r070o_independent_audit.md",
    "research/certificates/r070o",
    "figures/r070o-rank-bridge/fig-r070o-rank-bridge",
    "https://www.claymath.org/millennium/navier-stokes-equation/",
  ]) {
    assert.ok(note.includes(source), source);
  }

  for (const extension of ["pdf", "png", "svg"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL("figure." + extension, archiveRoot)),
      readFile(
        new URL("figures/r0-70o-rank-bridge." + extension, publicRoot),
      ),
    ]);
    assert.deepEqual(published, archived, extension);
  }
});

test("advances the route tree through R0.70O and exposes the next bridge", async () => {
  const home = await readFile(new URL("research-review.html", publicRoot), "utf8");
  const start = home.indexOf('<section class="route-overview"');
  const end = home.indexOf('<div class="page-shell">', start);
  const route = home.slice(start, end);

  assert.match(route, /Research topology · R0\.1–R0\.70O/);
  assert.match(route, /R0\.69P–R0\.70O/);
  assert.match(route, /展开 14 篇公开笔记/);
  assert.equal((route.match(/href="\/notes\/r0-70o\.html"/g) ?? []).length, 1);
  assert.doesNotMatch(route, /NEXT · R0\.70O/);
  assert.match(route, /NEXT · R0\.70P/);
  assert.match(route, /全频下框架与变方向交换子/);
  assert.match(home, /综述 v0\.84 · 2026-08-25/);
  assert.match(home, /上次综述 v0\.83 · 2026-08-25/);
  assert.match(home, /src="\/i18n-en\.js\?v=0\.84"/);
});
