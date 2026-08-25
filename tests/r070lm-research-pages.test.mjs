import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const root = new URL("../", import.meta.url);
const publicRoot = new URL("public/", root);
const releases = [
  {
    id: "r070l",
    note: "notes/r0-70l.html",
    archive: "figures/r070l-source-compensator/fig-r070l-source-compensator/",
    publicStem: "r0-70l-source-compensator",
  },
  {
    id: "r070m",
    note: "notes/r0-70m.html",
    archive: "figures/r070m-deformation-holonomy/fig-r070m-deformation-holonomy/",
    publicStem: "r0-70m-deformation-holonomy",
  },
];

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
  const dictionary = html.indexOf('src="/i18n-en.js?v=0.86"');
  const runtime = html.indexOf('src="/bilingual.js"');
  const mathJax = html.indexOf("mathjax@3/es5/tex-mml-chtml.js");
  assert.ok(css >= 0 && dictionary > css && runtime > dictionary);
  assert.ok(mathJax > runtime, "MathJax must load after bilingual assets");
}

test("publishes the R0.70L pressure obstruction without enlarging its scope", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-70l.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r070l"/);
  assert.match(home, /href="\/notes\/r0-70l\.html"/);
  assert.ok(note.includes("\\dot\\Phi\\big|_H=-D_\\Sigma\\Phi:H_*^\\circ"));
  assert.ok(note.includes("\\boxed{D_\\Sigma\\Phi=0.}"));
  assert.ok(note.includes("\\mathcal Q=-2"));
  assert.ok(note.includes("\\mathcal Q=1"));
  assert.ok(note.includes("\\dot q_-=\\frac{3901}{2040}&gt;0"));
  assert.ok(note.includes("\\dot q_+=-\\frac{1283}{2040}&lt;0"));
  assert.match(note, /两组初值能量相同/);
  assert.match(note, /见证发生在初始面/);
  assert.match(note, /不自动覆盖非紧 Gaussian 或严格 Littlewood–Paley 滤波/);
  assert.match(note, /不是千禧年问题的部分解答/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|三重审计|突破/);
  assert.doesNotMatch(note, /__[A-Z0-9_]+__/);
  assertLocalAnchorsResolve(note, 10);
  assertBilingualAssetsPrecedeMathJax(note);
});

test("publishes the R0.70M pullback losses and separates matrix from NSE witnesses", async () => {
  const [home, note] = await Promise.all([
    readFile(new URL("research-review.html", publicRoot), "utf8"),
    readFile(new URL("notes/r0-70m.html", publicRoot), "utf8"),
  ]);

  assert.match(home, /id="r070m"/);
  assert.match(home, /href="\/notes\/r0-70m\.html"/);
  assert.ok(note.includes("\\boxed{\\dot{\\widehat Q}=G^{-1}FG^{-\\mathsf T}.}"));
  assert.match(note, /应变传播子.*不是物理形变梯度/);
  assert.ok(note.includes("\\rho_G\\le\\kappa_2(G)^2\\rho_0"));
  assert.ok(note.includes("\\operatorname{tr}G_*=-\\frac{862}{81}&lt;-2"));
  assert.match(
    note,
    /\\operatorname\{tr\}B_\*\^2\s*=\\frac23-\\frac\{13122\}\{3296483\}/,
  );
  assert.ok(note.includes("Q^{-1}"));
  assert.match(note, /光滑无外力剪切严格产生秩一协方差/);
  assert.match(note, /四脉冲回路已经由一条无外力有限能周期 NSE 轨道实现/);
  assert.match(note, /没有得到新的继续性判据/);
  assert.match(note, /没有解决千禧年问题/);
  assert.doesNotMatch(note, /我们|攻关|主攻|研究纪律|三重审计|突破/);
  assert.doesNotMatch(note, /__[A-Z0-9_]+__/);
  assertLocalAnchorsResolve(note, 11);
  assertBilingualAssetsPrecedeMathJax(note);
});

test("keeps every R0.70L/M public figure byte-exact and links every archive", async () => {
  for (const release of releases) {
    const note = await readFile(new URL(release.note, publicRoot), "utf8");
    for (const source of [
      `research/${release.id}_report-source.md`,
      `research/${release.id}_literature_audit.md`,
      `research/${release.id}_independent_audit.md`,
      `research/certificates/${release.id}`,
      release.archive.slice(0, -1),
      "https://www.claymath.org/millennium/navier-stokes-equation/",
    ]) {
      assert.ok(note.includes(source), `${release.id}: ${source}`);
    }

    for (const extension of ["pdf", "png", "svg"]) {
      const [archived, published] = await Promise.all([
        readFile(new URL(`figure.${extension}`, new URL(release.archive, root))),
        readFile(
          new URL(`figures/${release.publicStem}.${extension}`, publicRoot),
        ),
      ]);
      assert.deepEqual(published, archived, `${release.id}.${extension}`);
    }
  }
});

test("retains R0.70L/M while the public route advances through R0.71C", async () => {
  const home = await readFile(new URL("research-review.html", publicRoot), "utf8");
  const start = home.indexOf('<section class="route-overview"');
  const end = home.indexOf('<div class="page-shell">', start);
  const route = home.slice(start, end);

  assert.match(route, /Research topology · R0\.1–R0\.71C/);
  assert.match(route, /R0\.69P–R0\.71C/);
  assert.match(route, /展开 37 篇公开笔记/);
  assert.equal((route.match(/href="\/notes\/r0-70l\.html"/g) ?? []).length, 1);
  assert.equal((route.match(/href="\/notes\/r0-70m\.html"/g) ?? []).length, 1);
  assert.match(route, /NEXT · R0\.71D/);
  assert.match(route, /通量平衡的物质抛物 tent/);
  assert.match(home, /综述 v0\.88 · 2026-08-25/);
  assert.match(home, /上次综述 v0\.87 · 2026-08-25/);
  assert.match(home, /src="\/i18n-en\.js\?v=0\.88"/);
});

test("ships complete R0.70L/M translations in the generated dictionary", async () => {
  const [translations, generated] = await Promise.all([
    readFile(new URL("translations/en.json", root), "utf8"),
    readFile(new URL("i18n-en.js", publicRoot), "utf8"),
  ]);
  for (const phrase of [
    "Pressure can still flip the sign independently",
    "yet cannot return to the physical metric for free",
    "multiscale covariance frame coercivity",
  ]) {
    assert.ok(translations.includes(phrase), phrase);
    assert.ok(generated.includes(phrase), phrase);
  }
});
