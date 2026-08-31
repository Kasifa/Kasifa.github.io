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
  r073m: { version: "1.53", code: "R0.73M", slug: "r0-73m", next: "R0.73N" },
  r073n: { version: "1.54", code: "R0.73N", slug: "r0-73n", next: "R0.73O" },
  r073o: { version: "1.55", code: "R0.73O", slug: "r0-73o", next: "R0.73P" },
  r073p: { version: "1.56", code: "R0.73P", slug: "r0-73p", next: "R0.73Q" },
  r073q: { version: "1.57", code: "R0.73Q", slug: "r0-73q", next: "R0.73R" },
  r073r: { version: "1.58", code: "R0.73R", slug: "r0-73r", next: "R0.73S" },
  r073s: { version: "1.59", code: "R0.73S", slug: "r0-73s", next: "R0.73T" },
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

test("homepage current route reaches the materialized G through S boundary without duplication", async () => {
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

  assert.ok(current.includes(isS
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
  if (isH || isI || isJ || isK || isL || isM || isN || isO || isP || isQ || isR || isS) {
    assert.ok(current.includes("actual-gain-normalized planar fixed-distance departure"));
  }
  if (isI || isJ || isK || isL || isM || isN || isO || isP || isQ || isR || isS) {
    assert.ok(current.includes("endpoint audit / continuum upper action / zero-window tangent"));
  }
  if (isJ || isK || isL || isM || isN || isO || isP || isQ || isR || isS) {
    assert.ok(current.includes("unique simple rightmost spectral branch of the continuum operator"));
  }
  if (isK || isL || isM || isN || isO || isP || isQ || isR || isS) {
    assert.ok(current.includes("parameter-uniform viscous rank-one branch"));
    assert.ok(current.includes("finite diagnostic: 1190 states / 952 cross-cutoff comparisons"));
  }
  if (isL || isM || isN || isO || isP || isQ || isR || isS) {
    assert.ok(current.includes("non-selfadjoint adiabatic tracking / matching selected action"));
    assert.ok(current.includes("parameter-uniform nonselfadjoint adiabatic tracking"));
    assert.ok(current.includes("finite diagnostic: 15 primary / 5 independent / 346 figure rows"));
  }
  if (isM || isN || isO || isP || isQ || isR || isS) {
    assert.ok(current.includes("prescribed-action planar nonlinear fixed-distance departure"));
    assert.ok(current.includes("prescribed-action planar nonlinear departure"));
    assert.ok(current.includes(
      "finite diagnostic: 15 primary / 5 linear / 3 hierarchy / 27 figure rows / 28 checks",
    ));
  }
  if (isN || isO || isP || isQ || isR || isS) {
    assert.ok(current.includes("fixed-member finite-strain stability / family-transfer obstruction"));
  }
  if (isO || isP || isQ || isR || isS) {
    for (const token of [
      "global-orbit stability / forced Kolmogorov contrast",
      "global-orbit H3 stability",
      "forced planar H3-to-L2 escape",
    ]) assert.ok(current.includes(token), token);
    assert.equal(current.includes(
      "<h3>R0.73N：固定成员有限应变稳定性与族转移障碍已闭合</h3>"), false);
  }
  if (isP || isQ || isR || isS) {
    for (const token of [
      "critical H1/2 stability / N^-1/2 frequency gate",
      "band-limited N^-1/2 gate",
      "earlyWeakIntervalRegularity=OPEN",
    ]) assert.ok(home.includes(token), token);
  }
  if (isQ || isR || isS) {
    for (const token of [
      "critical heat-flow tube / endpoint boundary",
      "critical heat-flow tube",
      "endpoint no-go",
    ]) assert.ok(home.includes(token), token);
    if (isQ) assert.ok(home.includes("<h3>R0.73R 下一接口</h3>"));
  }
  if (isR || isS) {
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
  if (isS) {
    for (const token of [
      "quadratic autocorrelation certificate",
      "difference-support obstruction",
      "low-summary non-identifiability",
      "基础不等式直接落在经典",
      "/assets/r073s/fig-r073s-quadratic-certificate.pdf",
    ]) assert.ok(home.includes(token), token);
    assert.ok(home.includes("<h3>R0.73T 下一接口</h3>"));
    assert.equal(home.includes("<h3>R0.73S 下一接口</h3>"), false);
  }
  assert.equal(home.includes(`<h3>${endpoint.code} 下一接口</h3>`), false);

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

test("literature route records the materialized G through S boundary", async () => {
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
  if (isS) {
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
