import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import test from "node:test";

const repositoryRoot = new URL("../", import.meta.url);
const publicRoot = new URL("public/", repositoryRoot);
const ENDPOINTS = Object.freeze({
  r073g: { version: "1.47", code: "R0.73G", slug: "r0-73g", next: "R0.73H" },
  r073h: { version: "1.48", code: "R0.73H", slug: "r0-73h", next: "R0.73I" },
  r073i: { version: "1.49", code: "R0.73I", slug: "r0-73i", next: "R0.73J" },
  r073j: { version: "1.50", code: "R0.73J", slug: "r0-73j", next: "R0.73K" },
  r073k: { version: "1.51", code: "R0.73K", slug: "r0-73k", next: "R0.73L" },
  r073l: { version: "1.52", code: "R0.73L", slug: "r0-73l", next: "R0.73M" },
});

async function page(name) {
  return readFile(new URL(name, publicRoot), "utf8");
}

async function repositoryJson(name) {
  return JSON.parse(await readFile(new URL(name, repositoryRoot), "utf8"));
}

async function currentEndpoint() {
  const manifest = await repositoryJson("research/release-manifest.json");
  const endpoint = ENDPOINTS[manifest.latestCompletedRelease];
  assert.ok(endpoint, `unsupported current endpoint: ${manifest.latestCompletedRelease}`);
  return { release: manifest.latestCompletedRelease, ...endpoint };
}

function claimBoundary(html, release) {
  const heading = `<h3 id="${release}-boundary">`;
  const start = html.indexOf(heading);
  assert.ok(start >= 0, `${release} boundary heading`);
  const tail = html.slice(start + heading.length);
  const next = tail.search(/<h3 id="r0\d{2}[a-z]-boundary">/);
  const section = next < 0 ? tail : tail.slice(0, next);
  const blocks = [...section.matchAll(/<div class="boundary">([\s\S]*?)<\/div>/g)];
  assert.equal(blocks.length, 1, `${release} must have one claim boundary`);
  return blocks[0][1];
}

test("homepage current route reaches the materialized G through L boundary without duplication", async () => {
  const [home, endpoint] = await Promise.all([
    page("research-review.html"),
    currentEndpoint(),
  ]);
  const isH = endpoint.release === "r073h";
  const isI = endpoint.release === "r073i";
  const isJ = endpoint.release === "r073j";
  const isK = endpoint.release === "r073k";
  const isL = endpoint.release === "r073l";
  assert.deepEqual(
    [...home.matchAll(/\bdata-site-version="([^"]+)"/g)].map((match) => match[1]),
    [endpoint.version],
    "homepage has exactly the manifest version",
  );
  const match = home.match(
    /<article class="tree-node current">([\s\S]*?)<details class="tree-notes" open>/,
  );
  assert.ok(match, "current route node");
  const current = match[1];

  assert.ok(current.includes(isL
    ? "<h3>R0.73L：非自伴绝热跟踪与匹配作用量已闭合</h3>"
    : isK
      ? "<h3>R0.73K：参数一致黏性 rank-one 谱支与补空间控制已闭合</h3>"
    : isJ
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
    `R0.72R–${endpoint.code}：`,
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
  if (isH || isI || isJ || isK || isL) {
    assert.ok(current.includes("actual-gain-normalized planar fixed-distance departure"));
  }
  if (isI || isJ || isK || isL) {
    assert.ok(current.includes("endpoint audit / continuum upper action / zero-window tangent"));
  }
  if (isJ || isK || isL) {
    assert.ok(current.includes("unique simple rightmost spectral branch of the continuum operator"));
  }
  if (isK || isL) {
    assert.ok(current.includes("parameter-uniform viscous rank-one branch"));
    assert.ok(current.includes("finite diagnostic: 1190 states / 952 cross-cutoff comparisons"));
  }
  if (isL) {
    assert.ok(current.includes("non-selfadjoint adiabatic tracking / matching selected action"));
    assert.ok(current.includes("parameter-uniform nonselfadjoint adiabatic tracking"));
    assert.ok(current.includes("finite diagnostic: 15 primary / 5 independent / 346 figure rows"));
  }

  assert.ok(
    home.includes(`<a class="route-map-latest" href="/notes/${endpoint.slug}.pdf">阅读最新 ${endpoint.code} 研究笔记 →</a>`),
  );
  assert.ok(
    home.includes(`<a class="route-map-latest" href="#${endpoint.release}">跳到首页 ${endpoint.code} 卡片 →</a>`),
  );
  assert.ok(home.includes('<a href="/notes/">查看完整笔记</a>'));

  const routeStart = home.indexOf('<section class="route-overview"');
  const routeEnd = home.indexOf('<div class="page-shell">', routeStart);
  const route = home.slice(routeStart, routeEnd);
  const latestSlug = endpoint.slug;
  assert.equal(
    (route.match(new RegExp(`href="/notes/${latestSlug}\\.html"`, "g")) ?? []).length,
    1,
    `${latestSlug} keeps one canonical note link in the route tree`,
  );
});

test("literature route records the materialized G through L boundary", async () => {
  const [literature, endpoint] = await Promise.all([
    page("literature-review.html"),
    currentEndpoint(),
  ]);
  const isH = endpoint.release === "r073h";
  const isI = endpoint.release === "r073i";
  const isJ = endpoint.release === "r073j";
  const isK = endpoint.release === "r073k";
  const isL = endpoint.release === "r073l";
  const match = literature.match(
    /<section id="route">([\s\S]*?)<figure class="topology"[^>]*>([\s\S]*?)<\/figure>/,
  );
  assert.ok(match, "literature route section");
  const intro = match[1];
  const topology = match[2];
  const boundary = claimBoundary(literature, endpoint.release);
  assert.ok(topology.includes(`开放接口 · ${endpoint.next}`));

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
  if (isL) {
    assert.ok(literature.includes('id="r073j-boundary"'));
    assert.ok(literature.includes('id="r073k-boundary"'));
    assert.ok(literature.includes('class="route-r073l-deck-update"'));
    for (let number = 167; number <= 172; number += 1) {
      assert.equal(
        [...literature.matchAll(new RegExp('id="ref-' + number + '"', "g"))].length,
        1,
        `R0.73L reference ref-${number}`,
      );
    }
    for (const token of [
      "commonDomainEvolution=CLOSED",
      "katoIntertwining=CLOSED",
      "movingComplementRelativeStability=CLOSED",
      "nonselfadjointAdiabaticTracking=CLOSED",
      "matchingSelectedGainAction=CLOSED",
      "actionResolvedBackwardLocalization=CLOSED",
      "finiteDiagnosticPackage=CLOSED",
      "primaryAdiabaticCases=15",
      "independentFiniteReconstruction=PASS",
      "formalFigurePackage=PASS",
      "finiteDimensionDoesNotCertifyContinuum=TRUE",
      "explicitAdiabaticThreshold=OPEN",
      "prefactorLimit=OPEN",
      "twoTermWKB=OPEN",
      "nonlinearNavierStokes=OPEN",
      "transverseThreeDimensionalClosure=OPEN",
      "finiteTimeSingularity=OPEN",
      "Clay=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73L boundary ${token}`);
  } else if (isK) {
    assert.ok(literature.includes('id="r073j-boundary"'));
    for (const token of [
      "uniformRankOneViscousBranch=CLOSED",
      "uniformProjectionNormConvergence=CLOSED",
      "uniformEigenvalueOepsilon=CLOSED",
      "uniformProjectionConditioning=CLOSED",
      "fixedHalfPlaneNoPollution=CLOSED",
      "uniformReducedResolvent=CLOSED",
      "uniformComplementSemigroup=CLOSED",
      "finiteDiagnosticPackage=CLOSED",
      "primarySpectralStates=1190",
      "crossCutoffComparisons=952",
      "independentFiniteReconstruction=PASS",
      "finiteDimensionDoesNotCertifyContinuum=TRUE",
      "explicitViscosityThreshold=OPEN",
      "nonselfadjointAdiabaticTracking=OPEN",
      "matchingSelectedGainAction=OPEN",
      "nonlinearNavierStokes=OPEN",
      "transverseThreeDimensionalClosure=OPEN",
      "finiteTimeSingularity=OPEN",
      "Clay=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73K boundary ${token}`);
  } else if (isJ) {
    for (const token of [
      "periodicRayleighContinuumBridge=CLOSED",
      "uniqueAlgebraicallySimpleRightmostBranch=CLOSED",
      "uniformSpectralGapAtLeastOneOverTwenty=CLOSED",
      "kineticOverlapAndFixedPhaseAnchor=CLOSED",
      "contourFullBallChebyshevPowerBernstein=FAILED_WITH_LEDGER",
      "overlapDirectIntervalClenshaw=FAILED_WITH_LEDGER",
      "naturalBoxFirstRound=76_PASS_7_WRAPPING_INCONCLUSIVE",
      "naturalBoxDepthTwo=1_RESOLVED_6_WRAPPING_INCONCLUSIVE",
      "naturalBoxAdaptiveDepthFive=PASS_7_OF_7_PARENTS_2896_OF_2896_LEAVES",
      "independentOverlapRawOdeRecomputation=NOT_RUN",
      "fullyIndependentRawGridAudit=OPEN",
      "uniformRankOneViscousBranch=OPEN",
      "nonselfadjointAdiabaticRemainder=OPEN",
      "Clay=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73J boundary ${token}`);
  } else if (isI) {
    assert.ok(boundary.includes("inheritedEndpointStrictlyBelowOneOver450=CLOSED"));
    assert.ok(boundary.includes("zeroWindowTangentAction=CLOSED"));
    assert.ok(boundary.includes("matchingSelectedGainAction=OPEN"));
  } else if (isH) {
    assert.ok(boundary.includes("gainNormalizedFixedDistanceDeparture=CLOSED"));
    assert.ok(boundary.includes("uniformTaylorRadiusAtNaturalEndpoint=OPEN"));
    assert.ok(boundary.includes("d=0.01"));
  } else {
    assert.ok(literature.includes("开放接口 · R0.73H"));
  }
  assert.equal(literature.includes("开放接口 · R0.73G"), false);
});
