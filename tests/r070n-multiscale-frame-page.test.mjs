import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const archiveRoot = new URL(
  "figures/r070n-multiscale-frame/fig-r070n-multiscale-frame/",
  root,
);

function assertLocalAnchorsResolve(html, minimum) {
  const ids = new Set(
    [...html.matchAll(/\sid="([^"]+)"/g)].map((match) => match[1]),
  );
  const targets = [...html.matchAll(/href="#([^"]+)"/g)].map(
    (match) => match[1],
  );
  assert.ok(targets.length >= minimum, `only ${targets.length} local targets`);
  for (const target of targets) {
    assert.ok(ids.has(target), `missing local target #${target}`);
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

test("publishes the R0.70N exact multiscale-frame no-go with its boundary", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-70n.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r070n"/);
  assert.equal((home.match(/href="\/notes\/r0-70n\.html"/g) ?? []).length, 2);
  assert.ok(note.includes("\\mathcal Q_k\\succeq c\\,\\operatorname{tr}(\\mathcal Q_k)I"));
  assert.ok(note.includes("\\ker\\mathcal Q_k=\\bigcap_{j:w_j>0}\\ker Q_j"));
  assert.ok(note.includes("u_s=Ae^{-\\nu N^2t}\\sin(Ny)e_1"));
  assert.ok(note.includes("\\nabla\\times u_b=Nu_b"));
  assert.ok(note.includes("\\det\\mathcal Q_{2h}=\\alpha\\beta(\\alpha+\\beta)"));
  assert.ok(note.includes("c_*(Q_L)=\\frac1{8L^2+2}\\longrightarrow0"));
  assert.match(note, /非局部滤波器实际读取的整个空间域/);
  assert.match(note, /这一步本身不声称任意滤波框架都满秩/);
  assert.match(note, /只取全环面 identity filter/);
  assert.match(note, /不存在.*统一正.*frame 常数/s);
  assert.match(note, /附加方向激励|条件性 frame/);
  assert.match(note, /没有得到新的继续性判据/);
  assert.match(note, /没有解决千禧年问题/);
  assert.doesNotMatch(
    note,
    /我们|攻关|主攻|研究纪律|三重审计|杀死错误想法|突破/,
  );
  assert.doesNotMatch(note, /__[A-Z0-9_]+__/);
  assertLocalAnchorsResolve(note, 12);
  assertBilingualAssetsPrecedeMathJax(note);
});

test("keeps every R0.70N public figure byte-exact and links the archive", async () => {
  const note = await readFile(new URL("notes/r0-70n.html", publicRoot), "utf8");
  for (const source of [
    "research/r070n_report-source.md",
    "research/r070n_literature_audit.md",
    "research/r070n_independent_audit.md",
    "research/certificates/r070n",
    "figures/r070n-multiscale-frame/fig-r070n-multiscale-frame",
    "https://www.claymath.org/millennium/navier-stokes-equation/",
  ]) {
    assert.ok(note.includes(source), source);
  }

  for (const extension of ["pdf", "png", "svg"]) {
    const [archived, published] = await Promise.all([
      readFile(new URL(`figure.${extension}`, archiveRoot)),
      readFile(
        new URL(`figures/r0-70n-multiscale-frame.${extension}`, publicRoot),
      ),
    ]);
    assert.deepEqual(published, archived, extension);
  }
});

test("retains R0.70N while the route tree advances through R0.71A", async () => {
  const home = await readFile(new URL("research-review.html", publicRoot), "utf8");
  const start = home.indexOf('<section class="route-overview"');
  const end = home.indexOf('<div class="page-shell">', start);
  const route = home.slice(start, end);

  assert.match(route, /Research topology · R0\.1–R0\.71A/);
  assert.match(route, /R0\.69P–R0\.71A/);
  assert.match(route, /展开 35 篇公开笔记/);
  assert.equal((route.match(/href="\/notes\/r0-70n\.html"/g) ?? []).length, 1);
  assert.equal((route.match(/href="\/notes\/r0-70o\.html"/g) ?? []).length, 1);
  assert.doesNotMatch(route, /NEXT · R0\.70O/);
  assert.match(route, /NEXT · R0\.71B/);
  assert.match(route, /common-response 的有符号尺度补偿/);
  assert.match(home, /综述 v0\.86 · 2026-08-25/);
  assert.match(home, /上次综述 v0\.85 · 2026-08-25/);
  assert.match(home, /src="\/i18n-en\.js\?v=0\.86"/);
});
