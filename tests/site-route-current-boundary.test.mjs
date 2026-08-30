import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const publicRoot = new URL("../public/", import.meta.url);

async function page(name) {
  return readFile(new URL(name, publicRoot), "utf8");
}

test("homepage current route reaches the materialized G, H, or I boundary without duplication", async () => {
  const home = await page("research-review.html");
  const isI = home.includes('data-site-version="1.49"');
  const isH = home.includes('data-site-version="1.48"');
  const match = home.match(
    /<article class="tree-node current">([\s\S]*?)<details class="tree-notes" open>/,
  );
  assert.ok(match, "current route node");
  const current = match[1];

  assert.ok(current.includes(isI
    ? "<h3>R0.73I：端点校正、连续体上作用量与零窗口切向速率已闭合</h3>"
    : isH
      ? "<h3>R0.73H：按实际增益归一化的平面固定距离偏离已闭合</h3>"
      : "<h3>R0.73G：过小种子的非线性相对放大与精确二维屏障已闭合</h3>"));
  assert.equal(
    current.includes(
      "<h3>R0.73F：移动剖面二分与固定窗口指数增益已闭合</h3>",
    ),
    false,
  );
  for (const token of [
    isI ? "R0.72R–R0.73I：" : isH ? "R0.72R–R0.73H：" : "R0.72R–R0.73G：",
    "caustic-free core",
    "marked \\(A_2\\)–\\(A_5\\) collisions",
    "exact scalar \\(A_2\\) block",
    "full Fourier–Leray row",
    "signed OS–Squire ledger",
    "hidden-mean transient",
    "Bloch physical-kinetic direct sum",
    "certified frozen Rayleigh instability",
    "static viscous cluster persistence",
    "fixed-half-plane logarithmic transfer",
    "exact kinetic space",
    "Riesz 投影按算子范数收敛",
    "Shvydkoy--Friedlander",
    "完整 top cluster 相对二分",
    "moving-profile fixed-window dichotomy",
    "over-small-seed nonlinear relative amplification / exact planar barrier",
  ]) {
    assert.ok(current.includes(token), token);
  }
  if (isH) {
    assert.ok(current.includes("actual-gain-normalized planar fixed-distance departure"));
  }
  if (isI) {
    assert.ok(current.includes("actual-gain-normalized planar fixed-distance departure"));
    assert.ok(current.includes("endpoint audit / continuum upper action / zero-window tangent"));
  }

  assert.ok(
    home.includes(isI
      ? '<a class="route-map-latest" href="/notes/r0-73i.pdf">阅读最新 R0.73I 研究笔记 →</a>'
      : isH
        ? '<a class="route-map-latest" href="/notes/r0-73h.pdf">阅读最新 R0.73H 研究笔记 →</a>'
        : '<a class="route-map-latest" href="/notes/r0-73g.pdf">阅读最新 R0.73G 研究笔记 →</a>'),
  );
  assert.ok(
    home.includes(isI
      ? '<a class="route-map-latest" href="#r073i">跳到首页 R0.73I 卡片 →</a>'
      : isH
        ? '<a class="route-map-latest" href="#r073h">跳到首页 R0.73H 卡片 →</a>'
        : '<a class="route-map-latest" href="#r073g">跳到首页 R0.73G 卡片 →</a>'),
  );
  assert.ok(home.includes('<a href="/notes/">查看完整笔记</a>'));

  const routeStart = home.indexOf('<section class="route-overview"');
  const routeEnd = home.indexOf('<div class="page-shell">', routeStart);
  const route = home.slice(routeStart, routeEnd);
  const latestSlug = isI ? "r0-73i" : isH ? "r0-73h" : "r0-73g";
  assert.equal(
    (route.match(new RegExp(`href="/notes/${latestSlug}\\.html"`, "g")) ?? []).length,
    1,
    `${latestSlug} keeps one canonical note link in the route tree`,
  );
});

test("literature route records the materialized G, H, or I boundary", async () => {
  const literature = await page("literature-review.html");
  const isI = literature.includes('id="r073i-boundary"');
  const isH = literature.includes('id="r073h-boundary"');
  const match = literature.match(
    /<section id="route">([\s\S]*?)<figure class="topology"/,
  );
  assert.ok(match, "literature route section");
  const intro = match[1];

  for (const token of [
    "R0.72Z 在 high-gap \\(q\\)-graph 上闭合 signed OS pressure",
    "R0.73A 用 hidden physical mean 闭合 low-gap \\(X_\\mu\\) finite transient",
    "R0.73B 再由 exact Bloch carrier cancellation",
    "low-gap vector direct sum at viscous rates 已为 CLOSED",
    "R0.73C 随后用 exact cubic neutral spectrum",
    "infinite-dimensional frozen Rayleigh instability",
    "R0.73D 再在精确 kinetic space 中证明",
    "static vanishing-viscosity persistence",
    "Riesz 投影算子范数收敛",
    "Shvydkoy--Friedlander",
    "R0.73E 用固定正半平面完备性",
    "完整 top cluster 相对二分",
    "logarithmic fast-time transfer",
    "moving-profile fixed-window、完整 OS--Squire、nonlinear 与 Clay 仍为 OPEN",
    "R0.73F 再用有界扰动 roughness",
    "一条精确线性行的 fixed-window exponential lower law",
    "complete OS--Squire A2 direct sum",
    "nonlinear Navier--Stokes 与 Clay 保持 OPEN",
    "R0.73G 再用显式强范数 bootstrap 与全模态余项能量估计",
    "过小种子的 nonlinear relative amplification",
    "所选真实轨道严格留在全局光滑二维子空间",
    "自然种子、order-one departure、横向三维与 Clay 保持 OPEN",
  ]) {
    assert.ok(intro.includes(token), token);
  }
  assert.ok(literature.includes('id="r073d-boundary"'));
  assert.ok(literature.includes('id="r073e-boundary"'));
  assert.ok(literature.includes('id="r073f-boundary"'));
  assert.ok(literature.includes('id="r073g-boundary"'));
  if (isI) {
    assert.ok(literature.includes("开放接口 · R0.73J"));
    assert.ok(literature.includes("inheritedEndpointStrictlyBelowOneOver450=CLOSED"));
    assert.ok(literature.includes("zeroWindowTangentAction=CLOSED"));
    assert.ok(literature.includes("matchingSelectedGainAction=OPEN"));
  } else if (isH) {
    assert.ok(literature.includes("开放接口 · R0.73I"));
    assert.ok(literature.includes("gainNormalizedFixedDistanceDeparture=CLOSED"));
    assert.ok(literature.includes("uniformTaylorRadiusAtNaturalEndpoint=OPEN"));
    assert.ok(literature.includes("d=0.01"));
  } else {
    assert.ok(literature.includes("开放接口 · R0.73H"));
  }
  assert.equal(literature.includes("开放接口 · R0.73G"), false);
});
