import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);

function assertLocalAnchorsResolve(html, minimum) {
  const ids = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const targets = [...html.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(targets.length >= minimum, "only " + targets.length + " anchors");
  for (const target of targets) {
    assert.ok(ids.has(target), "missing local target #" + target);
  }
}

function assertBilingualAssetsPrecedeMathJax(html) {
  const css = html.indexOf('href="/bilingual.css"');
  const dictionary = html.search(/src="\/i18n-en\.js(?:\?[^"]*)?"/);
  const runtime = html.indexOf('src="/bilingual.js"');
  const mathJax = html.indexOf("mathjax@3/es5/tex-mml-chtml.js");
  assert.ok(css >= 0 && dictionary > css && runtime > dictionary);
  assert.ok(mathJax > runtime, "MathJax must load after bilingual assets");
}

test("publishes the exact R0.71A constant-projector sign pair", async () => {
  const [home, note, pdf] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71a.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-71a.pdf", publicRoot)),
  ]);

  assert.match(home, /id="r071a"/);
  assert.equal((home.match(/href="\/notes\/r0-71a\.html"/g) ?? []).length, 2);
  assert.equal(pdf.subarray(0, 5).toString("ascii"), "%PDF-");
  for (const token of [
    "Q(\\omega_{\\Lambda,+})=Q(\\omega_{\\Lambda,-})",
    "\\pm{3\\sqrt2\\over40}\\Lambda^3",
    "P_1=e_3\\otimes e_3",
    "\\nabla P_1=0",
    "[T_\\alpha,I-P_1]=0",
    "\\lambda_1-\\lambda_2\\geq10\\Lambda^2",
    "{\\lambda_1-\\lambda_2\\over\\lambda_1}\\geq{2\\over3}",
    "{\\lambda_1-\\lambda_2\\over\\operatorname{tr}Q}\\geq{1\\over2}",
    "={3\\over2}\\Lambda^2",
    "\\{0:12,1:0,2:0,3:0\\}",
  ]) {
    assert.ok(note.includes(token), token);
  }
});

test("states the critical L1 method boundary and conditional theorem", async () => {
  const note = await readFile(new URL("notes/r0-71a.html", publicRoot), "utf8");

  for (const token of [
    "2/q+3/p=1",
    "\\|I_L\\|_{L_t^1}",
    "\\widehat u_\\lambda",
    "\\lambda^{2-2/s}",
    "(I_L)_+",
    "\\mathfrak W_{L,p}",
    "P\\omega\\in L_t^4L_x^2",
    "common-response",
    "705 / 705",
  ]) {
    assert.ok(note.includes(token), token);
  }
  assert.match(note, /运动学测试场，不是 Navier–Stokes 解/);
  assert.match(note, /不是对所有 Navier–Stokes 证明方法的否定/);
  assert.match(note, /不是所寻求的纯投影相干准则/);
  assert.match(note, /没有证明临界投影继续性准则为假/);
  assert.match(note, /没有构造有限时奇性/);
  assert.match(note, /没有证明全局光滑性/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /__[A-Z0-9_]+__/);
  assertLocalAnchorsResolve(note, 12);
  assertBilingualAssetsPrecedeMathJax(note);
});

test("links the R0.71A archive and its primary-source boundary", async () => {
  const note = await readFile(new URL("notes/r0-71a.html", publicRoot), "utf8");
  for (const source of [
    "research/r071a_report-source.md",
    "research/r071a_literature_audit.md",
    "research/r071a_independent_audit.md",
    "research/certificates/r071a",
    "research/r070p_report-source.md",
    "research/r070y_report-source.md",
    "research/r070z_report-source.md",
    "chae.pdf",
    "2002.02152",
    "hbv-79.pdf",
    "https://www.claymath.org/millennium/navier-stokes-equation/",
  ]) {
    assert.ok(note.includes(source), source);
  }
});

test("advances the route tree and review version through R0.71A", async () => {
  const home = await readFile(new URL("research-review.html", publicRoot), "utf8");
  const start = home.indexOf('<section class="route-overview"');
  const end = home.indexOf('<div class="page-shell">', start);
  const route = home.slice(start, end);

  assert.match(route, /Research topology · R0\.1–R0\.71A/);
  assert.match(route, /R0\.69P–R0\.71A/);
  assert.match(route, /展开 35 篇公开笔记/);
  assert.equal((route.match(/href="\/notes\/r0-71a\.html"/g) ?? []).length, 1);
  assert.match(route, /NEXT · R0\.71B/);
  assert.match(route, /common-response 的有符号尺度补偿/);
  assert.match(home, /综述 v0\.86 · 2026-08-25/);
  assert.match(home, /上次综述 v0\.85 · 2026-08-25/);
  assert.match(home, /src="\/i18n-en\.js\?v=0\.86"/);
});
