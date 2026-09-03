import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import { resolve, sep } from "node:path";
import test from "node:test";
import { pathToFileURL } from "node:url";

const routeTestRoot = process.env.R074A_ROUTE_TEST_ROOT ?? process.env.R073Z_ROUTE_TEST_ROOT ?? process.env.R073Y_ROUTE_TEST_ROOT ?? process.env.R073U_ROUTE_TEST_ROOT;
const repositoryRoot = routeTestRoot
  ? pathToFileURL(resolve(routeTestRoot) + sep)
  : new URL("../", import.meta.url);
const publicRoot = new URL("public/", repositoryRoot);
const ENDPOINTS = Object.freeze({
  r073g: { version: "1.47", code: "R0.73G", slug: "r0-73g", next: "R0.73H" },
  r073h: { version: "1.48", code: "R0.73H", slug: "r0-73h", next: "R0.73I" },
  r073i: { version: "1.49", code: "R0.73I", slug: "r0-73i", next: "R0.73J" },
  r073j: { version: "1.50", code: "R0.73J", slug: "r0-73j", next: "R0.73K" },
  r073k: { version: "1.51", code: "R0.73K", slug: "r0-73k", next: "R0.73L" },
  r073l: { version: "1.52", code: "R0.73L", slug: "r0-73l", next: "R0.73M" },
  r073m: { version: "1.53", code: "R0.73M", slug: "r0-73m", next: "R0.73N" },
  r073n: { version: "1.54", code: "R0.73N", slug: "r0-73n", next: "R0.73O" },
  r073o: { version: "1.55", code: "R0.73O", slug: "r0-73o", next: "R0.73P" },
  r073p: { version: "1.56", code: "R0.73P", slug: "r0-73p", next: "R0.73Q" },
  r073q: { version: "1.57", code: "R0.73Q", slug: "r0-73q", next: "R0.73R" },
  r073r: { version: "1.58", code: "R0.73R", slug: "r0-73r", next: "R0.73S" },
  r073s: { version: "1.59", code: "R0.73S", slug: "r0-73s", next: "R0.73T" },
  r073t: { version: "1.60", code: "R0.73T", slug: "r0-73t", next: "R0.73U" },
  r073u: { version: "1.61", code: "R0.73U", slug: "r0-73u", next: "R0.73V" },
  r073v: { version: "1.62", code: "R0.73V", slug: "r0-73v", next: "R0.73W" },
  r073w: { version: "1.63", code: "R0.73W", slug: "r0-73w", next: "R0.73X" },
  r073x: { version: "1.64", code: "R0.73X", slug: "r0-73x", next: "R0.73Y" },
  r073y: { version: "1.65", code: "R0.73Y", slug: "r0-73y", next: "R0.73Z" },
  r073z: { version: "1.66", code: "R0.73Z", slug: "r0-73z", next: "R0.74A" },
  r074a: { version: "1.67", code: "R0.74A", slug: "r0-74a", next: "R0.74B" },
  r074b: { version: "1.68", code: "R0.74B", slug: "r0-74b", next: "R0.74C" },
  r074c: { version: "1.69", code: "R0.74C", slug: "r0-74c", next: "R0.74D" },
  r074d: { version: "1.70", code: "R0.74D", slug: "r0-74d", next: "R0.74E" },
  r074e: { version: "1.71", code: "R0.74E", slug: "r0-74e", next: "R0.74F" },
  r074f: { version: "1.72", code: "R0.74F", slug: "r0-74f", next: "R0.74G" },
  r074g: { version: "1.73", code: "R0.74G", slug: "r0-74g", next: "R0.74H" },
  r074h: { version: "1.74", code: "R0.74H", slug: "r0-74h", next: "R0.74I" },
  r074i: { version: "1.75", code: "R0.74I", slug: "r0-74i", next: "R0.74J" },
  r074j: { version: "1.76", code: "R0.74J", slug: "r0-74j", next: "R0.74K" },
  r074k: { version: "1.77", code: "R0.74K", slug: "r0-74k", next: "R0.74L" },
  r074l: { version: "1.78", code: "R0.74L", slug: "r0-74l", next: "R0.74M" },
  r074m: { version: "1.79", code: "R0.74M", slug: "r0-74m", next: "R0.74N" },
  r074n: { version: "1.80", code: "R0.74N", slug: "r0-74n", next: "R0.74O" },
  r074o: { version: "1.81", code: "R0.74O", slug: "r0-74o", next: "R0.74P" },
  r074p: { version: "1.82", code: "R0.74P", slug: "r0-74p", next: "R0.74Q" },
  r074q: { version: "1.83", code: "R0.74Q", slug: "r0-74q", next: "R0.74R" },
  r074r: { version: "1.84", code: "R0.74R", slug: "r0-74r", next: "R0.74S" },
  r074s: { version: "1.97", code: "R0.74S", slug: "r0-74s", next: "R0.74T" },
  r074t: { version: "1.98", code: "R0.74T", slug: "r0-74t", next: "R0.74U" },
  r074u: { version: "1.99", code: "R0.74U", slug: "r0-74u", next: "R0.74V" },
  r074v: { version: "2.00", code: "R0.74V", slug: "r0-74v", next: "R0.74W" },
  r074w: { version: "2.01", code: "R0.74W", slug: "r0-74w", next: "R0.74X" },
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

test("homepage current route reaches the materialized G through R0.74A boundary without duplication", async () => {
  const [home, endpoint] = await Promise.all([
    page("research-review.html"),
    currentEndpoint(),
  ]);
  const isH = endpoint.release === "r073h";
  const isI = endpoint.release === "r073i";
  const isJ = endpoint.release === "r073j";
  const isK = endpoint.release === "r073k";
  const isL = endpoint.release === "r073l";
  const isM = endpoint.release === "r073m";
  const isN = endpoint.release === "r073n";
  const isO = endpoint.release === "r073o";
  const isP = endpoint.release === "r073p";
  const isQ = endpoint.release === "r073q";
  const isR = endpoint.release === "r073r";
  const isS = endpoint.release === "r073s";
  const isT = endpoint.release === "r073t";
  const isU = endpoint.release === "r073u";
  const isV = endpoint.release === "r073v";
  const isW = endpoint.release === "r073w";
  const isX = endpoint.release === "r073x";
  const isY = endpoint.release === "r073y";
  const isA = endpoint.release === "r074a";
  const isZ = endpoint.release === "r073z" || isA;
  assert.deepEqual(
    [...home.matchAll(/\bdata-site-version="([^"]+)"/g)].map((match) => match[1]),
    [endpoint.version],
    "homepage has exactly the manifest version",
  );
  const match = home.match(
    /<article class="tree-node current">([\s\S]*?)<details class="tree-notes">/,
  );
  assert.ok(match, "current route node");
  const current = match[1];
  assert.ok(
    current.includes('<details class="tree-route-details" hidden>'),
    "full historical route stays out of the compact homepage card",
  );

  if (endpoint.release.localeCompare("r074b") >= 0) {
    assert.ok(current.includes(`<h3>${endpoint.code}：`), "current compact route title");
    assert.ok(current.includes(`R0.72R–${endpoint.code}：`), "current detailed route range");
    assert.ok(home.includes(
      `<a class="route-map-latest" href="/notes/${endpoint.slug}.pdf">阅读最新 ${endpoint.code} 研究笔记 →</a>`,
    ));
    assert.ok(home.includes(["r074t", "r074u", "r074w"].includes(endpoint.release) ? "NEXT · FROZEN PACKAGE" : `NEXT · ${endpoint.next}`));
    const routeStart = home.indexOf('<section class="route-overview"');
    const routeEnd = home.indexOf('<div class="page-shell">', routeStart);
    const route = home.slice(routeStart, routeEnd);
    assert.equal(
      (route.match(new RegExp(`href="/notes/${endpoint.slug}\\.html"`, "g")) ?? []).length,
      1,
      `${endpoint.slug} keeps one canonical note link in the route tree`,
    );
    return;
  }

  assert.ok(current.includes(isA
    ? "<h3>R0.74A：局部 K_D 付款已闭合</h3>"
    : isZ
    ? "<h3>R0.73Z：初始端点有限性障碍、能量兼容正三次修复与 pressure-active 分离已分列</h3>"
    : isY
    ? "<h3>R0.73Y：exact shear kernel、全振幅零 production、A != 0 时严格正 heat covariance 与 production-only no-go 已分列</h3>"
    : isX
    ? "<h3>R0.73X：Gaussian 速度尾、代数 pressure 尾、positive-scale size 与 open coercivity bridge 已分列</h3>"
    : isW
    ? "<h3>R0.73W：带符号亚滤波 production、heat-plane 特征线、能量类边界与精确反例已分列</h3>"
    : isV
    ? "<h3>R0.73V：有符号三阶尺度生成、完整压力账本与精确 3→4 边界已分列</h3>"
    : isU
    ? "<h3>R0.73U：完整张量 heat hierarchy、同尺度压力重建与二次状态 no-go 已分列</h3>"
    : isT
    ? "<h3>R0.73T：动态 AQ 估计、精确非自治见证与压力张量障碍已分列</h3>"
    : isS
    ? "<h3>R0.73S：二次自相关证书、尖锐差集障碍与低摘要 no-go 已分列</h3>"
    : isR
    ? "<h3>R0.73R：经典热--Besov、逐壳相位证书与零非线性边界已分列</h3>"
    : isQ
    ? "<h3>R0.73Q：临界热流稳定管、严格扩域与端点边界已分列</h3>"
    : isP
    ? "<h3>R0.73P：临界稳定、频率门槛与早期弱区间已分列</h3>"
    : isO
    ? "<h3>R0.73O：全局轨道稳定管与强迫 Kolmogorov 对照已分列</h3>"
    : isN
    ? "<h3>R0.73N：固定成员有限应变稳定性与族转移障碍已闭合</h3>"
    : isM
      ? "<h3>R0.73M：prescribed-action 平面非线性固定距离偏离已闭合</h3>"
      : isL
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
  if (isH || isI || isJ || isK || isL || isM || isN || isO || isP || isQ || isR || isS || isT || isU || isV || isW || isX || isY || isZ) {
    assert.ok(current.includes("actual-gain-normalized planar fixed-distance departure"));
  }
  if (isI || isJ || isK || isL || isM || isN || isO || isP || isQ || isR || isS || isT || isU || isV || isW || isX || isY || isZ) {
    assert.ok(current.includes("endpoint audit / continuum upper action / zero-window tangent"));
  }
  if (isJ || isK || isL || isM || isN || isO || isP || isQ || isR || isS || isT || isU || isV || isW || isX || isY || isZ) {
    assert.ok(current.includes("unique simple rightmost spectral branch of the continuum operator"));
  }
  if (isK || isL || isM || isN || isO || isP || isQ || isR || isS || isT || isU || isV || isW || isX || isY || isZ) {
    assert.ok(current.includes("parameter-uniform viscous rank-one branch"));
    assert.ok(current.includes("finite diagnostic: 1190 states / 952 cross-cutoff comparisons"));
  }
  if (isL || isM || isN || isO || isP || isQ || isR || isS || isT || isU || isV || isW || isX || isY || isZ) {
    assert.ok(current.includes("non-selfadjoint adiabatic tracking / matching selected action"));
    assert.ok(current.includes("parameter-uniform nonselfadjoint adiabatic tracking"));
    assert.ok(current.includes("finite diagnostic: 15 primary / 5 independent / 346 figure rows"));
  }
  if (isM || isN || isO || isP || isQ || isR || isS || isT || isU || isV || isW || isX || isY || isZ) {
    assert.ok(current.includes("prescribed-action planar nonlinear fixed-distance departure"));
    assert.ok(current.includes("prescribed-action planar nonlinear departure"));
    assert.ok(current.includes(
      "finite diagnostic: 15 primary / 5 linear / 3 hierarchy / 27 figure rows / 28 checks",
    ));
  }
  if (isN || isO || isP || isQ || isR || isS || isT || isU || isV || isW || isX || isY || isZ) {
    assert.ok(current.includes("fixed-member finite-strain stability / family-transfer obstruction"));
  }
  if (isO || isP || isQ || isR || isS || isT || isU || isV || isW || isX || isY || isZ) {
    for (const token of [
      "global-orbit stability / forced Kolmogorov contrast",
      "global-orbit H3 stability",
      "forced planar H3-to-L2 escape",
    ]) assert.ok(current.includes(token), token);
    assert.equal(current.includes(
      "<h3>R0.73N：固定成员有限应变稳定性与族转移障碍已闭合</h3>"), false);
  }
  if (isP || isQ || isR || isS || isT || isU || isV || isW || isX || isY || isZ) {
    for (const token of [
      "critical H1/2 stability / N^-1/2 frequency gate",
      "band-limited N^-1/2 gate",
      "earlyWeakIntervalRegularity=OPEN",
    ]) assert.ok(home.includes(token), token);
  }
  if (isQ || isR || isS || isT || isU || isV || isW || isX || isY || isZ) {
    for (const token of [
      "critical heat-flow tube / endpoint boundary",
      "critical heat-flow tube",
      "endpoint no-go",
    ]) assert.ok(home.includes(token), token);
    if (isQ) assert.ok(home.includes("<h3>R0.73R 下一接口</h3>"));
  }
  if (isR || isS || isT || isU || isV || isW || isX || isY || isZ) {
    for (const token of [
      "shellwise phase certificate",
      "classical heat--Besov mechanism",
      "matched phase separation",
      "两族对流非线性严格为零",
      "/assets/r073r/fig-r073r-phase-coherence.pdf",
    ]) assert.ok(home.includes(token), token);
    if (isR) assert.ok(home.includes("<h3>R0.73S 下一接口</h3>"));
    assert.equal(home.includes("<h3>R0.73R 下一接口</h3>"), false);
  }
  if (isS || isT || isU || isV || isW || isX || isY || isZ) {
    for (const token of [
      "quadratic autocorrelation certificate",
      "difference-support obstruction",
      "low-summary non-identifiability",
      "基础不等式直接落在经典",
      "/assets/r073s/fig-r073s-quadratic-certificate.pdf",
    ]) assert.ok(home.includes(token), token);
    if (isS) assert.ok(home.includes("<h3>R0.73T 下一接口</h3>"));
    assert.equal(home.includes("<h3>R0.73S 下一接口</h3>"), false);
  }
  if (isT || isU || isV || isW || isX || isY || isZ) {
    for (const token of [
      "dynamic AQ upper inequality",
      "carrier-scale non-autonomy",
      "pressure-tensor barrier",
      "缺失的 A 积分已有经典 LPS 强度",
      "/assets/r073t/fig-r073t-dynamic-autocorrelation.pdf",
    ]) assert.ok(home.includes(token), token);
    if (isT) assert.ok(home.includes("<h3>R0.73U 下一接口</h3>"));
    assert.equal(home.includes("<h3>R0.73T 下一接口</h3>"), false);
  }
  if (isU) {
    for (const token of [
      "R0.73U｜完整张量进入热层级：压力可以恢复，但偶二次状态的动力学并不闭合",
      "heat covariance scale PDE",
      "same-scale pressure reconstruction",
      "quadratic-state non-autonomy",
      "零尺度能量控制仍开放",
      "R0.70A–R0.73U · 99 节已公开",
      "75 节完整封存",
      "137 节累计回顾",
      "197 篇研究笔记总索引",
      "/assets/r073u/fig-r073u-tensor-heat-hierarchy.pdf",
      "<h3>R0.73V 下一接口</h3>",
    ]) assert.ok(home.includes(token), `R0.73U homepage ${token}`);
    assert.equal(home.includes("<h3>R0.73U 下一接口</h3>"), false);
  }
  if (isV) {
    for (const token of [
      "R0.73V｜压力感知的有符号三阶热提升：精确尺度生成律与 3→4 物理时间边界",
      "signed cross-covariance scale PDE",
      "pressure-aware Germano interface",
      "selected quartic next-level remainder",
      "带符号的 production \\(-\\tau_s:\\nabla v_s\\)",
      "R0.70A–R0.73V · 100 节已公开",
      "76 节完整封存",
      "138 节累计回顾",
      "198 篇研究笔记总索引",
      "/assets/r073v/fig-r073v-signed-third-order-interface.pdf",
      "<h3>R0.73W 下一接口</h3>",
    ]) assert.ok(home.includes(token), `R0.73V homepage ${token}`);
    assert.equal(home.includes("<h3>R0.73V 下一接口</h3>"), false);
  }
  if (isA) {
    for (const token of [
      "R0.74A｜混合 heat covariance 的局部 size lemma",
      "positiveFourBlockMajorization=PROVED_ANALYTICALLY",
      "clockMatchedLocalEnergyTailBound=PROVED_ANALYTICALLY",
      "oldExteriorPackageOnlyControl=FALSE_BY_EXACT_ENERGY_CLASS_PACKETS",
      "velocityEndpointTail=FINITE_FOR_EVERY_STATED_PERIODIC_ENERGY_CLASS_FIELD",
      "R0.70A–R0.74A · 105 节已公开",
      "81 节完整封存",
      "上一大里程碑 recap（R0.61–R0.73X，140 节）",
      "203 篇研究笔记总索引",
      "/assets/r074a/fig-r074a-localized-kd-payments.pdf",
      "<h3>R0.74B 下一接口</h3>",
    ]) assert.ok(home.includes(token), `R0.74A homepage ${token}`);
    assert.equal(home.includes("/recap-r0-61-r0-74a"), false);
    assert.equal(home.includes("<h3>R0.74A 下一接口</h3>"), false);
  } else if (isZ) {
    for (const token of [
      "R0.73Z｜正三次 heat covariance 的有限性障碍与能量兼容修复",
      "initialEndpointEnergyClassFiniteness=FALSE_BY_EXACT_LERAY_HOPF_SHEAR",
      "energyCompatibleKDUpperBound=PROVED_ANALYTICALLY",
      "pressureActiveCrossedFamily=PROVED_ANALYTICALLY",
      "R0.70A–R0.73Z · 104 节已公开",
      "80 节完整封存",
      "上一大里程碑 recap（R0.61–R0.73X，140 节）",
      "202 篇研究笔记总索引",
      "/assets/r073z/fig-r073z-covariance-separation.pdf",
      "<h3>R0.74A 下一接口</h3>",
    ]) assert.ok(home.includes(token), `R0.73Z homepage ${token}`);
    assert.equal(home.includes("/recap-r0-61-r0-73z"), false);
    assert.equal(home.includes("<h3>R0.73Z 下一接口</h3>"), false);
  } else if (isY) {
    for (const token of [
      "R0.73Y｜Exact shear 类否定 production-only coercivity",
      "exact shear NSE",
      "zero production at every positive scale",
      "A != 0 时严格正 heat covariance",
      "Vreman（2004）",
      "R0.70A–R0.73Y · 103 节已公开",
      "79 节完整封存",
      "上一大里程碑 recap（R0.61–R0.73X，140 节）",
      "201 篇研究笔记总索引",
      "/assets/r073y/fig-r073y-exact-shear-obstruction.pdf",
      "<h3>R0.73Z 下一接口</h3>",
    ]) assert.ok(home.includes(token), `R0.73Y homepage ${token}`);
    assert.equal(home.includes("/recap-r0-61-r0-73y"), false);
    assert.equal(home.includes("<h3>R0.73Y 下一接口</h3>"), false);
  } else if (isX) {
    for (const token of [
      "R0.73X｜带显式外部尾项的局部热账本：Gaussian 速度控制、代数压力尾与未闭合 coercivity 桥",
      "direct Gaussian heat tails",
      "algebraic harmonic-pressure tails",
      "positive-scale absolute size",
      "R0.70A–R0.73X · 102 节已公开",
      "78 节完整封存",
      "140 节累计回顾",
      "200 篇研究笔记总索引",
      "/assets/r073x/fig-r073x-exterior-tail-ledger.pdf",
      "<h3>R0.73Y 下一接口</h3>",
    ]) assert.ok(home.includes(token), `R0.73X homepage ${token}`);
    assert.equal(home.includes("**"), false, "R0.73X homepage renders audit emphasis");
    assert.equal(home.includes("<h3>R0.73X 下一接口</h3>"), false);
  } else if (isW) {
    for (const token of [
      "R0.73W｜带符号亚滤波 production：heat-plane 特征线、能量类边界与精确反例",
      "signed subfilter production",
      "heat-plane characteristics",
      "exact rank-three counterexample",
      "R0.70A–R0.73W · 101 节已公开",
      "77 节完整封存",
      "139 节累计回顾",
      "199 篇研究笔记总索引",
      "/assets/r073w/fig-r073w-signed-production.pdf",
      "<h3>R0.73X 下一接口</h3>",
    ]) assert.ok(home.includes(token), `R0.73W homepage ${token}`);
    assert.equal(home.includes("**"), false, "R0.73W homepage renders audit emphasis");
    assert.equal(home.includes("<h3>R0.73W 下一接口</h3>"), false);
  }
  assert.equal(home.includes(`<h3>${endpoint.code} 下一接口</h3>`), false);

  assert.ok(
    home.includes(`<a class="route-map-latest" href="/notes/${endpoint.slug}.pdf">阅读最新 ${endpoint.code} 研究笔记 →</a>`),
  );
  assert.ok(isZ
    ? home.includes(`<a href="#${endpoint.release}">查看首页完整 ${endpoint.code} 卡片</a>`)
    : home.includes(`<a class="route-map-latest" href="#${endpoint.release}">跳到首页 ${endpoint.code} 卡片 →</a>`));
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

test("literature route records the materialized G through R0.74A boundary", async () => {
  const [literature, endpoint] = await Promise.all([
    page("literature-review.html"),
    currentEndpoint(),
  ]);
  const isH = endpoint.release === "r073h";
  const isI = endpoint.release === "r073i";
  const isJ = endpoint.release === "r073j";
  const isK = endpoint.release === "r073k";
  const isL = endpoint.release === "r073l";
  const isM = endpoint.release === "r073m";
  const isN = endpoint.release === "r073n";
  const isO = endpoint.release === "r073o";
  const isP = endpoint.release === "r073p";
  const isQ = endpoint.release === "r073q";
  const isR = endpoint.release === "r073r";
  const isS = endpoint.release === "r073s";
  const isT = endpoint.release === "r073t";
  const isU = endpoint.release === "r073u";
  const isV = endpoint.release === "r073v";
  const isW = endpoint.release === "r073w";
  const isX = endpoint.release === "r073x";
  const isY = endpoint.release === "r073y";
  const isA = endpoint.release === "r074a";
  const isZ = endpoint.release === "r073z" || isA;
  const match = literature.match(
    /<section id="route">([\s\S]*?)<figure class="topology"[^>]*>([\s\S]*?)<\/figure>/,
  );
  assert.ok(match, "literature route section");
  const intro = match[1];
  const topology = match[2];
  const boundary = claimBoundary(literature, endpoint.release);
  assert.ok(topology.includes(["r074t", "r074u", "r074w"].includes(endpoint.release) ? "开放接口 · 等待冻结包" : `开放接口 · ${endpoint.next}`));

  if (endpoint.release.localeCompare("r074b") >= 0) {
    assert.ok(literature.includes(`id="${endpoint.release}-boundary"`));
    assert.ok(literature.includes(`R0.69P–${endpoint.code}`));
    assert.ok(topology.includes(`<b>${endpoint.code}</b>`));
    for (const marker of ["PROVED", "FINITE", "OPEN", "NOT CLAY"]) {
      assert.ok(boundary.includes(marker), `${endpoint.code} boundary ${marker}`);
    }
    return;
  }

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
  if (isA) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o", "r073p", "r073q", "r073r", "r073s", "r073t", "r073u", "r073v", "r073w", "r073x", "r073y", "r073z"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes("R0.74A：mixed heat covariance 的 core/exterior 四块 size lemma"));
    assert.ok(literature.includes("R0.70A–R0.74A：105 节已公开，81 节完整封存"));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.74A</b><strong>localized mixed-covariance four-block size lemma</strong>',
    ));
    for (const token of [
      "positiveFourBlockMajorization=PROVED_ANALYTICALLY",
      "clockMatchedLocalEnergyTailBound=PROVED_ANALYTICALLY",
      "pressureCutoffInterface=PROVED_BY_INHERITANCE_AND_ANALYTIC_COMBINATION",
      "oldExteriorPackageOnlyControl=FALSE_BY_EXACT_ENERGY_CLASS_PACKETS",
      "velocityEndpointTail=FINITE_FOR_EVERY_STATED_PERIODIC_ENERGY_CLASS_FIELD",
      "gradientTail=FINITE_AND_IDENTICAL_TO_R073X_D_EXT",
      "localizedKDCertificate=FINITE_ARITHMETIC_CROSS_CHECK_ONLY",
      "formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES",
      "smallerCylinderTailControl=OPEN",
      "tailSmallnessOrAbsorption=OPEN",
      "weakStabilityAndLowerSemicontinuity=OPEN",
      "scaleUniformQuotientCoercivity=OPEN",
      "epsilonRegularity=OPEN",
      "arbitraryThreeDimensionalGlobalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.74A boundary ${token}`);
    for (const token of [
      "开放接口 · R0.74B",
      "tail absorption, weak stability, and blow-up-sequence compatibility",
      "time-supremum obstruction",
    ]) assert.ok(topology.includes(token), `R0.74B interface ${token}`);
    assert.equal(topology.includes("开放接口 · R0.74A"), false);
  } else if (isZ) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o", "r073p", "r073q", "r073r", "r073s", "r073t", "r073u", "r073v", "r073w", "r073x", "r073y"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes("R0.73Z：positive covariance 的初始端点障碍、能量修复与 pressure-active 分离"));
    assert.ok(literature.includes("R0.70A–R0.73Z：104 节已公开，80 节完整封存"));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73Z</b><strong>positive-covariance endpoint obstruction and energy-compatible repair</strong>',
    ));
    for (const token of [
      "initialEndpointEnergyClassFiniteness=FALSE_BY_EXACT_LERAY_HOPF_SHEAR",
      "energyCompatibleKDUpperBound=PROVED_ANALYTICALLY",
      "exactKernelKD=PROVED_ANALYTICALLY",
      "localCenteredOscillationProductLowerBound=PROVED_ANALYTICALLY",
      "pressureActiveCrossedFamily=PROVED_ANALYTICALLY",
      "covarianceFourierCertificate=FINITE_CROSS_CHECK_ONLY",
      "formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES",
      "interiorSuitableWeakFiniteness=OPEN",
      "localKDUpperPayment=OPEN",
      "scaleUniformQuotientCoercivity=OPEN",
      "epsilonRegularity=OPEN",
      "arbitraryThreeDimensionalGlobalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73Z boundary ${token}`);
    for (const token of [
      "开放接口 · R0.74A",
      "local K_D payment and pressure-cutoff debt",
      "core/exterior split",
    ]) assert.ok(topology.includes(token), `R0.74A interface ${token}`);
    assert.equal(topology.includes("开放接口 · R0.73Z"), false);
  } else if (isY) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o", "r073p", "r073q", "r073r", "r073s", "r073t", "r073u", "r073v", "r073w", "r073x"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes('class="route-r073y-deck-update"'));
    assert.ok(literature.includes(
      "R0.73Y：exact shear kernel 与 production-only no-go",
    ));
    assert.ok(literature.includes("R0.70A–R0.73Y：103 节已公开，79 节完整封存"));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73Y</b><strong>exact shear kernel and production-only no-go</strong>',
    ));
    for (const token of [
      "exactShearNSE=PROVED_ANALYTICALLY",
      "allPositiveHeatScalesZeroProduction=PROVED_ANALYTICALLY",
      "gradientCovarianceStrictlyPositiveForAneq0AndSgt0=PROVED_ANALYTICALLY",
      "zeroAmplitudeMemberCovariance=ZERO",
      "positiveSizeCubicHomogeneity=PROVED_ANALYTICALLY",
      "productionOnlyCoercivity=REFUTED_FOR_ZERO_PRESERVING_FUNCTIONALS",
      "singleFourierCertificate=FINITE_CROSS_CHECK_ONLY",
      "strictPositivityFromSampling=FALSE",
      "basicShearNoveltyOrPriority=NOT_CLAIMED",
      "formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED",
      "formalFigurePackage=SEALED_COMMIT_BOUND_25_FILES",
      "navierStokesSimulation=NOT_RUN",
      "directNumericalSimulation=NOT_RUN",
      "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
      "dgxUsed=false",
      "quotientCoercivity=OPEN",
      "pressureActiveInvisibleFamily=OPEN",
      "suitableWeakZeroScaleEndpoint=OPEN",
      "epsilonRegularity=OPEN",
      "arbitraryThreeDimensionalGlobalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73Y boundary ${token}`);
    for (const token of [
      "Vreman（2004）",
      "basicShearNoveltyOrPriority=NOT_CLAIMED",
      "quotientCoercivity=OPEN",
    ]) assert.ok(literature.includes(token), `R0.73Y literature update ${token}`);
    for (const token of [
      "开放接口 · R0.73Z",
      "scale-critical covariance",
      "quotient coercivity",
    ]) assert.ok(topology.includes(token), `R0.73Z interface ${token}`);
    assert.equal(topology.includes("开放接口 · R0.73Y"), false);
  } else if (isX) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o", "r073p", "r073q", "r073r", "r073s", "r073t", "r073u", "r073v", "r073w"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes('class="route-r073x-deck-update"'));
    assert.ok(literature.includes(
      "R0.73X 的 explicit exterior tails 与 positive-scale size 边界",
    ));
    assert.ok(literature.includes("R0.70A–R0.73X：102 节已公开，78 节完整封存"));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73X</b><strong>explicit exterior tails and positive-scale absolute size</strong>',
    ));
    for (const token of [
      "localizedHeatCharacteristicLedger=PROVED_WITH_STATED_SOLUTION_CLASS",
      "gaussianVelocityTailLemma=INDEPENDENT_AUDIT_PASS",
      "pressureExteriorTailSizeLemma=PASS_AT_POSITIVE_SCALE",
      "positiveScaleAbsoluteSize=PROVED",
      "gaussianTailCertificate=INDEPENDENT_SECOND_PRODUCER_PASS",
      "finiteHarmonicProbe=REFUTED_EXACTLY",
      "formalEvidenceCertificate=SOURCE_COMMIT_BOUND_PACKAGE_HASH_SEALED",
      "formalFigurePackage=SEALED_COMMIT_BOUND",
      "navierStokesSimulation=NOT_RUN",
      "directNumericalSimulation=NOT_RUN",
      "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
      "dgxUsed=false",
      "compactCutoffQuadraticAbsorption=OPEN",
      "signedToAbsoluteCoercivity=OPEN",
      "weightedTentCarlesonControl=OPEN",
      "suitableWeakZeroScaleEndpoint=OPEN",
      "epsilonRegularity=OPEN",
      "arbitraryThreeDimensionalGlobalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73X boundary ${token}`);
    for (const token of [
      "Gaussian velocity tail=INTERNAL AUDITED",
      "pressure tail=ALGEBRAIC",
      "positive-scale size=PROVED",
      "signed-to-absolute coercivity=OPEN",
      "不承担新颖性或优先权声明",
    ]) assert.ok(literature.includes(token), `R0.73X literature update ${token}`);
    for (const token of [
      "开放接口 · R0.73Y",
      "signed-to-absolute coercivity bridge",
      "compact cutoff",
    ]) assert.ok(topology.includes(token), `R0.73Y interface ${token}`);
    assert.equal(topology.includes("开放接口 · R0.73X"), false);
  } else if (isW) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o", "r073p", "r073q", "r073r", "r073s", "r073t", "r073u", "r073v"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes('class="route-r073w-deck-update"'));
    assert.ok(literature.includes(
      "R0.73W｜带符号亚滤波 production：heat-plane 特征线、能量类边界与精确反例",
    ));
    assert.ok(literature.includes("R0.70A–R0.73W：101 节已公开，77 节完整封存"));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73W</b><strong>signed subfilter production and heat-plane characteristics</strong>',
    ));
    for (const token of [
      "gaussianStressDuhamel=VERIFIED_CLASSICAL_REDERIVED",
      "deviatoricProductionIdentity=VERIFIED_CLASSICAL_REDERIVED",
      "heatPlaneCharacteristicIdentity=INTERNAL_EXACT_AUDITED",
      "energyClassFixedScaleEstimate=INTERNAL_UNCONDITIONAL_AUDITED",
      "centeredIncrementSplit=INTERNAL_EXACT_AUDITED",
      "criticalHalfScaleAverage=INTERNAL_CRITICAL_AUDITED",
      "formalFiniteCertificate=SEALED_COMMIT_BOUND",
      "formalFiniteCertificateChecks=56+56",
      "primaryWitnessFrequencyRank=3",
      "formalFigurePackage=SEALED_COMMIT_BOUND",
      "navierStokesSimulation=NOT_RUN",
      "directNumericalSimulation=NOT_RUN",
      "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
      "dgxUsed=false",
      "fixedScaleUniformEnergyClassControl=OPEN",
      "localizedScaleCriticalControl=OPEN",
      "arbitraryThreeDimensionalGlobalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73W boundary ${token}`);
    for (const token of [
      "Gaussian stress formula=CLASSICAL",
      "heat-coordinate identity=INTERNAL",
      "rank-three witness=FINITE",
      "localized scale-critical control=OPEN",
      "不承担新颖性或优先权声明",
    ]) assert.ok(literature.includes(token), `R0.73W literature update ${token}`);
    for (const token of [
      "开放接口 · R0.73X",
      "localized heat-characteristic and defect ledger",
      "pressure covariance",
      "energy-defect measure",
    ]) assert.ok(topology.includes(token), `R0.73X interface ${token}`);
    assert.equal(topology.includes("开放接口 · R0.73W"), false);
  } else if (isV) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o", "r073p", "r073q", "r073r", "r073s", "r073t", "r073u"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes('class="route-r073v-deck-update"'));
    assert.ok(literature.includes(
      "R0.73V｜压力感知的有符号三阶热提升：精确尺度生成律与 3→4 物理时间边界",
    ));
    assert.ok(literature.includes("R0.70A–R0.73V：100 节已公开，76 节完整封存"));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73V</b><strong>pressure-aware signed third-order heat lift</strong>',
    ));
    for (const token of [
      "pressureAwareSignedHeatLift=INTERNAL_EXACT_AUDITED",
      "signedCrossCovarianceScalePDE=INTERNAL_EXACT_AUDITED",
      "quadraticTensorOddSlotRecovered=INTERNAL_EXACT_AUDITED",
      "germanoStressEquation=VERIFIED_CLASSICAL_INDEX_AUDITED",
      "selectedQuarticNextLevelRemainder=INTERNAL_EXACT_FINITE_SEALED",
      "finiteWitnessIsSimulation=FALSE",
      "navierStokesSimulation=NOT_RUN",
      "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
      "dgxUsed=FALSE",
      "formalFiniteCertificate=PASS",
      "formalFiniteCertificateChecks=66",
      "coefficientwisePressureNonRecovery=INTERNAL_EXACT_FINITE_SEALED",
      "formalFigurePackage=PASS",
      "formalFigureChecks=147",
      "formalFigureRows=158",
      "pressureStrainCriticalRow=OPEN",
      "signedLiftInformationTheoreticMinimality=NOT_ESTABLISHED",
      "fourthOrderNonClosure=NOT_ESTABLISHED",
      "finiteMomentHierarchyNoGo=NOT_ESTABLISHED",
      "arbitraryThreeDimensionalGlobalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73V boundary ${token}`);
    for (const token of [
      "signed heat lift=INTERNAL_EXACT_AUDITED",
      "pressure-aware third-order interface=EXACT_OR_CLASSICAL",
      "minimality / hierarchy no-go=NOT_ESTABLISHED",
      "不承担新颖性或优先权声明",
    ]) assert.ok(literature.includes(token), `R0.73V literature update ${token}`);
    for (const token of [
      "开放接口 · R0.73W",
      "quantitative control at the exact next-level boundary",
      "\\(-\\tau_s:\\nabla v_s\\)",
    ]) assert.ok(topology.includes(token), `R0.73W interface ${token}`);
    assert.equal(topology.includes("开放接口 · R0.73V"), false);
  } else if (isU) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o", "r073p", "r073q", "r073r", "r073s", "r073t"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes('class="route-r073u-deck-update"'));
    assert.ok(literature.includes(
      "R0.73U｜完整张量进入热层级：压力可以恢复，但偶二次状态的动力学并不闭合",
    ));
    assert.ok(literature.includes("R0.70A–R0.73U：99 节已公开，75 节完整封存"));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73U</b><strong>tensor heat hierarchy and the signed-flux boundary</strong>',
    ));
    for (const token of [
      "heatCovariancePSD=INTERNAL_EXACT",
      "heatCovarianceScalePDE=INTERNAL_EXACT",
      "sameScalePressureReconstruction=VERIFIED_CLASSICAL",
      "filteredNSEAndSGSFlux=VERIFIED_CLASSICAL_RECONSTRUCTION",
      "conditionalCriticalStressRow=INTERNAL_COROLLARY",
      "fixedPositiveScaleEnergyStressBound=INTERNAL_COROLLARY",
      "fourSiteQuadraticStateNonAutonomy=CLOSED_EXACT",
      "parabolicCoefficientLoss=CLOSED_EXACT",
      "finiteWitnessIsSimulation=FALSE",
      "navierStokesSimulation=NOT_RUN",
      "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
      "dgxUsed=FALSE",
      "formalFiniteCertificate=PASS",
      "formalFiniteCertificateChecks=75",
      "formalFigurePackage=PASS",
      "formalFigureChecks=325",
      "finiteGeneralTensorClosure=OPEN",
      "zeroScaleEnergyCriticalStressControl=OPEN",
      "arbitraryThreeDimensionalGlobalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73U boundary ${token}`);
    for (const token of [
      "heat covariance / pressure reconstruction=EXACT OR CLASSICAL",
      "quadratic-state non-autonomy=CLOSED_EXACT",
      "general tensor closure=OPEN",
      "不承担新颖性或优先权声明",
    ]) assert.ok(literature.includes(token), `R0.73U literature update ${token}`);
    for (const token of [
      "开放接口 · R0.73V",
      "minimal signed third-order lift",
      "物理时间方程",
    ]) assert.ok(topology.includes(token), `R0.73V interface ${token}`);
    assert.equal(topology.includes("开放接口 · R0.73U"), false);
  } else if (isT) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o", "r073p", "r073q", "r073r", "r073s"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes('class="route-r073t-deck-update"'));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73T</b><strong>dynamic autocorrelation and the pressure-tensor barrier</strong>',
    ));
    for (const token of [
      "exactAutocorrelationEvolution=VERIFIED_CLASSICAL_RECONSTRUCTION",
      "dynamicAQUpperInequality=INTERNAL_COROLLARY",
      "criticalAIntegral=INTERNAL_EXACT_SCALING",
      "criticalAIntegralControl=OPEN",
      "carrierScaleNonAutonomy=CLOSED_EXACT",
      "signedVelocityPhaseInPressurePairing=CLOSED_EXACT",
      "pressureTensorNeededForGeneralReconstruction=VERIFIED_CLASSICAL",
      "finiteFormulaDiagnosticChecks=55",
      "formalFigureChecks=106",
      "navierStokesSimulation=NOT_RUN",
      "ordinaryTranslationPath=LOCAL_DIRECT_NO_DGX",
      "tensorHeatClosure=OPEN",
      "arbitraryThreeDimensionalGlobalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73T boundary ${token}`);
    for (const token of [
      "dynamic AQ inequality=INTERNAL_COROLLARY",
      "critical A integral / tensor heat closure=OPEN",
      "不承担新颖性或优先权声明",
    ]) assert.ok(literature.includes(token), `R0.73T literature update ${token}`);
    for (const token of [
      "开放接口 · R0.73U",
      "tensor heat hierarchy",
      "critical signed flux",
    ]) assert.ok(topology.includes(token), `R0.73U interface ${token}`);
  } else if (isS) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o", "r073p", "r073q", "r073r"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes('class="route-r073s-deck-update"'));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73S</b><strong>quadratic autocorrelation certificate and exact no-go boundary</strong>',
    ));
    for (const token of [
      "quadraticAutocorrelationBound=VERIFIED_CLASSICAL",
      "differenceSupportNikolskii=VERIFIED_CLASSICAL",
      "selectedShiftMagnitudeTailCertificate=CLOSED_EXACT",
      "fixedAnnulusDifferenceSupportObstruction=CLOSED_EXACT",
      "lowSummaryNonIdentifiability=CLOSED_EXACT",
      "completeAutocorrelationDeterminesL6=VERIFIED_CLASSICAL",
      "zeroNonlinearityWitnesses=CLOSED",
      "finiteFormulaCertificateOnly=TRUE",
      "heatFlowIntegralComputed=FALSE",
      "navierStokesSimulation=NOT_RUN",
      "runtimeBenchmark=FALSE",
      "translationPath=LOCAL_DIRECT_NO_DGX",
      "universalRuntimeLowerBound=NOT_PROVED",
      "failureOfEntranceImpliesUnsafeDynamics=FALSE",
      "uniformL2OnlyStrongRadius=OPEN",
      "arbitraryThreeDimensionalGlobalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73S boundary ${token}`);
    for (const token of [
      "quadratic autocorrelation inequality=VERIFIED_CLASSICAL",
      "universal runtime lower bound=NOT_PROVED",
      "不承担新颖性或优先权声明",
    ]) assert.ok(literature.includes(token), `R0.73S literature update ${token}`);
    for (const token of [
      "dynamic autocorrelation budget",
      "逐壳",
      "通量",
    ]) assert.ok(topology.includes(token), `R0.73T interface ${token}`);
  } else if (isR) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o", "r073p", "r073q"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes('class="route-r073r-deck-update"'));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73R</b><strong>shellwise phase certificate and classical Besov boundary</strong>',
    ));
    for (const token of [
      "periodicHeatBesovEquivalence=VERIFIED_CLASSICAL",
      "ell4ShellExponent=CLOSED_AFTER_AUDIT",
      "exactVectorTripleConvolution=CLOSED_EXACT_EVALUATION",
      "additiveMultiplicityCertificate=CLOSED",
      "supportCardinalityCertificate=CLOSED_SHARP_FROM_SUPPORT_ONLY",
      "matchedPhaseHeatTraceSeparation=CLOSED_AFTER_AUDIT",
      "zeroNonlinearityBoundary=CLOSED",
      "matchedSupportMagnitudeQuadraticData=CLOSED_EXACT",
      "finiteFormulaDiagnosticOnly=TRUE",
      "heatFlowIntegralComputed=FALSE",
      "navierStokesSimulation=NOT_RUN",
      "translationPath=LOCAL_DIRECT_NO_DGX",
      "failureOfEntranceImpliesUnsafeDynamics=FALSE",
      "uniformL2OnlyStrongRadius=OPEN",
      "arbitraryThreeDimensionalGlobalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73R boundary ${token}`);
    for (const token of [
      "periodic heat--Besov equivalence=VERIFIED_CLASSICAL",
      "uniform L2-only strong radius=OPEN",
      "不承担新颖性或优先权声明",
    ]) assert.ok(literature.includes(token), `R0.73R literature update ${token}`);
    for (const token of [
      "lower-cost deterministic phase proxy or no-go",
      "部分自相关、低阶加法能量",
      "确定性代理量",
    ]) assert.ok(topology.includes(token), `R0.73S interface ${token}`);
  } else if (isQ) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o", "r073p"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes('class="route-r073q-deck-update"'));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73Q</b><strong>critical heat-flow tube and endpoint boundary</strong>',
    ));
    for (const token of [
      "periodicOseenHLS=CLOSED_AFTER_AUDIT",
      "linearizedVolterraInverse=CLOSED_AFTER_AUDIT",
      "uniformAllRestartRadius=CLOSED_AFTER_AUDIT",
      "H3SerrinBridge=CLOSED_AFTER_AUDIT",
      "periodicHeatFlowTube=CLOSED_AFTER_AUDIT",
      "strictExtensionByUnion=CLOSED",
      "singleModeNormFormula=CLOSED_EXACT",
      "endpointTimeMapNoGo=CLOSED_EXACT",
      "navierStokesSimulation=NOT_RUN",
      "heatFlowBallContainsEntirePublishedH12Ball=NOT_PROVED",
      "fullKochTataruTheory=NOT_REFUTED",
      "uniformL2Only=OPEN",
      "nonperturbativeBMOInverseUniqueness=FALSE_IN_GENERAL",
      "arbitraryThreeDimensionalGlobalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73Q boundary ${token}`);
  } else if (isP) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n", "r073o"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes('class="route-r073p-deck-update"'));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73P</b><strong>critical stability and the N^-1/2 frequency gate</strong>',
    ));
    for (const token of [
      "globalCriticalH12OrbitStability=CLOSED_AS_CLASSICAL_COROLLARY",
      "bandLimitedL2ThresholdNMinusHalf=CLOSED_AS_COROLLARY",
      "oneSidedDelayedL2ToH3Synchronization=CLOSED_AFTER_AUDIT",
      "formulaDiagnostic=ANALYTIC_ONLY",
      "finiteAnalyticFigureProvesPDEThresholdNecessity=FALSE",
      "uniformL2OnlyStrongThreshold=OPEN_COLLISION_SENSITIVE",
      "earlyWeakIntervalRegularity=OPEN",
      "clayConclusion=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73P boundary ${token}`);
  } else if (isO) {
    for (const previous of ["r073j", "r073k", "r073l", "r073m", "r073n"]) {
      assert.ok(literature.includes(`id="${previous}-boundary"`));
    }
    assert.ok(literature.includes('class="route-r073o-deck-update"'));
    assert.ok(topology.includes(
      '<div class="route-step kept"><header><b>R0.73O</b><strong>global-orbit stability and a forced Kolmogorov contrast</strong>',
    ));
    for (const token of [
      "unforcedGlobalOrbitH3Stability=CLOSED_CONDITIONALLY_ON_GLOBAL_REFERENCE",
      "globalDataSetH3Open=CLOSED_AS_CLASSICAL_COROLLARY",
      "forcedKolmogorovPlanarH3InputL2Escape=CLOSED_BY_PRIMARY_SOURCE_COMBINATION",
      "finiteKolmogorovSpectrum=DIAGNOSTIC_ONLY",
      "finiteComputationProvesPositiveInfiniteDimensionalSpectrum=FALSE",
      "uniformL2OnlyInputThreshold=OPEN",
      "arbitraryDataGlobalRegularity=OPEN",
      "essentiallyThreeDimensionalInstability=OPEN_NOT_NEEDED",
      "Clay=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73O boundary ${token}`);
  } else if (isN) {
    assert.ok(literature.includes('id="r073j-boundary"'));
    assert.ok(literature.includes('id="r073k-boundary"'));
    assert.ok(literature.includes('id="r073l-boundary"'));
    assert.ok(literature.includes('id="r073m-boundary"'));
    assert.ok(literature.includes('class="route-r073n-deck-update"'));
    for (const token of [
      "fixedTimeRelativeL2LipschitzBound=CLOSED",
      "finiteAllTimeStrainEnvelope=CLOSED",
      "fixedMemberPlanarL2SynchronizedStability=CLOSED",
      "fixedMemberThreeDimensionalH3SynchronizedStability=CLOSED",
      "fullThreeDimensionalH3InputL2Output=CLOSED_AS_COROLLARY",
      "familyFlowMapNonuniformMarkedBasepointSensitivity=CLOSED",
      "finiteDiagnosticValidation=PASS",
      "formalFigurePackage=PASS",
      "familyDepartureImpliesFixedMemberInstability=FALSE_AS_INFERENCE",
      "singleR073mMemberH3SmallL2FixedDistanceEscape=FALSE",
      "fullThreeDimensionalFPSH3L2Stability=OPEN",
      "amplitudeOnlyIdentificationIsNSSymmetry=FALSE",
      "timeTranslationIdentifiesLambdaFamily=FALSE",
      "parabolicScalingIdentifiesLambdaFamilyOnFixedTorus=FALSE",
      "optimalFixedMemberStabilityRadius=OPEN",
      "sharpFamilyLipschitzExponent=OPEN",
      "arbitraryFixedBackgroundInstability=OPEN",
      "transverseCriticalNormGrowth=OPEN",
      "finiteTimeSingularity=OPEN",
      "Clay=OPEN",
      "originalTimeCompactness=FALSE",
      "boundedTimeShiftRetainsTwoHarmonics=FALSE",
      "infiniteSmoothHeatShearEvadesFiniteStrainTube=FALSE",
      "differentForcedOrNondecayingBackgroundRoute=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73N boundary ${token}`);
  } else if (isM) {
    assert.ok(literature.includes('id="r073j-boundary"'));
    assert.ok(literature.includes('id="r073k-boundary"'));
    assert.ok(literature.includes('id="r073l-boundary"'));
    assert.ok(literature.includes('class="route-r073m-deck-update"'));
    for (let number = 167; number <= 174; number += 1) {
      assert.equal(
        [...literature.matchAll(new RegExp('id="ref-' + number + '"', "g"))].length,
        1,
        `R0.73M reference ref-${number}`,
      );
    }
    for (const token of [
      "physicalKineticSelectedGainConjugacy=CLOSED",
      "fixedEndpointBackwardLocalization=CLOSED",
      "prescribedActionSeedWindow=CLOSED",
      "twoDimensionalNonlinearDeparture=CLOSED",
      "fixedDistanceEndpoint=CLOSED",
      "selectedPlanarOrbitGlobalSmoothness=CLOSED",
      "finiteDiagnosticPackage=CLOSED",
      "primaryPrescribedActionCases=15",
      "independentLinearSentinels=5",
      "independentHierarchySentinels=3",
      "formalFigurePackage=PASS",
      "finiteDimensionDoesNotCertifyContinuum=TRUE",
      "prefactorLimit=OPEN",
      "twoTermWKB=OPEN",
      "singleFixedBackgroundLyapunovInstability=OPEN",
      "transverseThreeDimensionalClosure=OPEN",
      "finiteTimeSingularity=OPEN",
      "Clay=OPEN",
      "NOT CLAY",
    ]) assert.ok(boundary.includes(token), `R0.73M boundary ${token}`);
  } else if (isL) {
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
