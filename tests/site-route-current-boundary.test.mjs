import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const repositoryRoot = new URL("../", import.meta.url);
const publicRoot = new URL("public/", repositoryRoot);

async function page(name) {
  return readFile(new URL(name, publicRoot), "utf8");
}

async function repositoryJson(name) {
  return JSON.parse(await readFile(new URL(name, repositoryRoot), "utf8"));
}

function claimBoundary(html, id) {
  const heading = html.indexOf(`<h3 id="${id}">`);
  const start = html.indexOf('<div class="boundary">', heading);
  const end = html.indexOf("</div>", start);
  assert.ok(heading >= 0 && start > heading && end > start, `claim boundary #${id}`);
  return html.slice(start, end);
}

test("homepage current route reaches the materialized G, H, I, or J boundary without duplication", async () => {
  const [home, manifest] = await Promise.all([
    page("research-review.html"),
    repositoryJson("research/release-manifest.json"),
  ]);
  const isG = manifest.latestCompletedRelease === "r073g";
  const isH = manifest.latestCompletedRelease === "r073h";
  const isI = manifest.latestCompletedRelease === "r073i";
  const isJ = manifest.latestCompletedRelease === "r073j";
  assert.equal(
    [isG, isH, isI, isJ].filter(Boolean).length,
    1,
    `unsupported current release ${manifest.latestCompletedRelease}`,
  );
  const expectedVersion = isJ ? "1.50" : isI ? "1.49" : isH ? "1.48" : "1.47";
  assert.ok(home.includes(`data-site-version="${expectedVersion}"`), "homepage version matches manifest");
  const match = home.match(
    /<article class="tree-node current">([\s\S]*?)<details class="tree-notes" open>/,
  );
  assert.ok(match, "current route node");
  const current = match[1];

  assert.ok(current.includes(isJ
    ? "<h3>R0.73J：周期 Rayleigh 连续算子上的唯一简单最右谱支已认证</h3>"
    : isI
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
    isJ ? "R0.72R–R0.73J：" : isI ? "R0.72R–R0.73I：" : isH ? "R0.72R–R0.73H：" : "R0.72R–R0.73G：",
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
  if (isH || isI || isJ) {
    assert.ok(current.includes("actual-gain-normalized planar fixed-distance departure"));
  }
  if (isI || isJ) {
    assert.ok(current.includes("endpoint audit / continuum upper action / zero-window tangent"));
  }
  if (isJ) {
    assert.ok(current.includes("unique simple rightmost spectral branch of the continuum operator"));
  }

  assert.ok(
    home.includes(isJ
      ? '<a class="route-map-latest" href="/notes/r0-73j.pdf">阅读最新 R0.73J 研究笔记 →</a>'
      : isI
        ? '<a class="route-map-latest" href="/notes/r0-73i.pdf">阅读最新 R0.73I 研究笔记 →</a>'
        : isH
          ? '<a class="route-map-latest" href="/notes/r0-73h.pdf">阅读最新 R0.73H 研究笔记 →</a>'
          : '<a class="route-map-latest" href="/notes/r0-73g.pdf">阅读最新 R0.73G 研究笔记 →</a>'),
  );
  assert.ok(
    home.includes(isJ
      ? '<a class="route-map-latest" href="#r073j">跳到首页 R0.73J 卡片 →</a>'
      : isI
        ? '<a class="route-map-latest" href="#r073i">跳到首页 R0.73I 卡片 →</a>'
        : isH
          ? '<a class="route-map-latest" href="#r073h">跳到首页 R0.73H 卡片 →</a>'
          : '<a class="route-map-latest" href="#r073g">跳到首页 R0.73G 卡片 →</a>'),
  );
  assert.ok(home.includes('<a href="/notes/">查看完整笔记</a>'));

  const routeStart = home.indexOf('<section class="route-overview"');
  const routeEnd = home.indexOf('<div class="page-shell">', routeStart);
  const route = home.slice(routeStart, routeEnd);
  const latestSlug = isJ ? "r0-73j" : isI ? "r0-73i" : isH ? "r0-73h" : "r0-73g";
  assert.equal(
    (route.match(new RegExp(`href="/notes/${latestSlug}\\.html"`, "g")) ?? []).length,
    1,
    `${latestSlug} keeps one canonical note link in the route tree`,
  );
});

test("literature route records the materialized G, H, I, or J boundary", async () => {
  const [literature, manifest] = await Promise.all([
    page("literature-review.html"),
    repositoryJson("research/release-manifest.json"),
  ]);
  const isG = manifest.latestCompletedRelease === "r073g";
  const isH = manifest.latestCompletedRelease === "r073h";
  const isI = manifest.latestCompletedRelease === "r073i";
  const isJ = manifest.latestCompletedRelease === "r073j";
  assert.equal(
    [isG, isH, isI, isJ].filter(Boolean).length,
    1,
    `unsupported current release ${manifest.latestCompletedRelease}`,
  );
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
  if (isJ) {
    const boundary = claimBoundary(literature, "r073j-boundary");
    assert.ok(literature.includes("开放接口 · R0.73K"));
    for (const token of [
      "periodicRayleighContinuumBridge=CLOSED",
      "uniqueAlgebraicallySimpleRightmostBranch=CLOSED",
      "uniformSpectralGapAtLeastOneOverTwenty=CLOSED",
      "kineticOverlapAndFixedPhaseAnchor=CLOSED",
      "independentOverlapRawOdeRecomputation=NOT_RUN",
      "fullyIndependentRawGridAudit=OPEN",
      "uniformRankOneViscousBranch=OPEN",
      "Clay=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73J boundary ${token}`);
  } else if (isI) {
    const boundary = claimBoundary(literature, "r073i-boundary");
    assert.ok(literature.includes("开放接口 · R0.73J"));
    assert.ok(boundary.includes("inheritedEndpointStrictlyBelowOneOver450=CLOSED"));
    assert.ok(boundary.includes("zeroWindowTangentAction=CLOSED"));
    assert.ok(boundary.includes("matchingSelectedGainAction=OPEN"));
  } else if (isH) {
    const boundary = claimBoundary(literature, "r073h-boundary");
    assert.ok(literature.includes("开放接口 · R0.73I"));
    assert.ok(boundary.includes("gainNormalizedFixedDistanceDeparture=CLOSED"));
    assert.ok(boundary.includes("uniformTaylorRadiusAtNaturalEndpoint=OPEN"));
    assert.ok(boundary.includes("d=0.01"));
  } else {
    assert.ok(literature.includes("开放接口 · R0.73H"));
  }
  assert.equal(literature.includes("开放接口 · R0.73G"), false);
});
