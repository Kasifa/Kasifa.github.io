#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reader-facing fragments for the fail-closed R0.73M release."""

FIGURE_ID = "fig-r073m-prescribed-action-departure"
FIGURE_RELATIVE = f"figures/r073m/{FIGURE_ID}"

R073L_BASELINE = {
    "latestCompletedRelease": "r073l", "siteVersion": "1.52",
    "publicHtmlNoteCount": 188, "postR060RecapNodeCount": 128,
    "nextRelease": "r073m", "postR070APublishedReleaseCount": 90,
    "postR070AFormalSealedReleaseCount": 66,
    "legacyFormalFigureBacklogCount": 24,
}

R073M_TARGET = {
    "latestCompletedRelease": "r073m", "siteVersion": "1.53",
    "publicHtmlNoteCount": 189, "postR060RecapNodeCount": 129,
    "nextRelease": "r073n", "postR070APublishedReleaseCount": 91,
    "postR070AFormalSealedReleaseCount": 67,
    "legacyFormalFigureBacklogCount": 24,
}

CLOSED = (
    "physicalKineticSelectedGainConjugacy=CLOSED；"
    "fixedEndpointBackwardLocalization=CLOSED；"
    "prescribedActionSeedWindow=CLOSED；"
    "twoDimensionalNonlinearDeparture=CLOSED；"
    "fixedDistanceEndpoint=CLOSED；"
    "selectedPlanarOrbitGlobalSmoothness=CLOSED"
)

FINITE = (
    "finiteDiagnosticPackage=CLOSED；primaryPrescribedActionCases=15；"
    "independentLinearSentinels=5；independentHierarchySentinels=3；"
    "formalFigurePackage=PASS；finiteDimensionDoesNotCertifyContinuum=TRUE"
)

OPEN = (
    "prefactorLimit=OPEN；twoTermWKB=OPEN；"
    "singleFixedBackgroundLyapunovInstability=OPEN；"
    "transverseThreeDimensionalClosure=OPEN；"
    "finiteTimeSingularity=OPEN；Clay=OPEN"
)

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73M · PRESCRIBED-ACTION PLANAR DEPARTURE</div>
        <h1>由完整作用量指定种子的平面非线性固定距离偏离</h1>
        <p class="lead">R0.73M 把 R0.73L 的两侧 action 估计接到 R0.73H 的谐波能量层级：对一族精确、无外力、随热流演化的周期剪切背景，初始扰动可以直接写成 \(\rho e^{-\Lambda\mathcal A_*}\phi_\Lambda\)，并在固定物理时刻 \(T_*=1/1800\) 到达与 \(\rho\) 同阶的 \(L^2\) 距离。所有构造轨道都留在精确二维不变子空间；这不是单一固定背景的 Lyapunov 不稳定性，也不是三维奇性结论。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73M 完成</span><strong>Continuum theorem + independent audits</strong><p>版本 v0.73M · 2026-08-31</p><p>解析门：M1–M8 CLOSED</p><p>有限主案例：15</p><p>独立线性 / 层级：5 / 3</p><p>验证器：28 / 28 PASS</p><p>正式附图：PASS</p><p>FIXED BACKGROUND / 3D / CLAY：OPEN</p><p>NOT CLAY</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct result</div><h2>指数小的 prescribed-action 种子在固定时刻产生固定距离</h2><div class="equation result">\[\left\|\Pi_{\{K_z=\pm1\}}\bigl(U_\Lambda^\rho(T_*)-\bar U_\Lambda(T_*)\bigr)\right\|_2\ge c_*\rho,\qquad \|U_\Lambda^\rho(0)-\bar U_\Lambda(0)\|_{H^3}\le C\rho\Lambda^2e^{-\Lambda\mathcal A_*}\to0.\]</div><p>这里 \(D_*=1/450\)、\(T_*=D_*/4=1/1800\)，且 \(167/450000<\mathcal A_*<173/450000\)。常数 \(c_*\)、\(\rho_0\) 和 \(\Lambda_0\) 是连续证明中的存在性常数，没有从有限计算中拟合。</p></section>
        <section id="background"><div class="section-no">01 / Exact background</div><h2>背景是精确的无外力热流，但随 \(\Lambda\) 改变</h2><div class="equation result">\[\bar U_\Lambda(t,y)=(0,0,2\Lambda W(4t,2y)),\qquad W(d,x)=-\tfrac12e^{-d}\sin x+\tfrac14e^{-4d}\sin2x.\]</div><p>由于 \(W_d=W_{xx}\)，每个背景都是光滑的精确 Navier–Stokes 解。背景振幅随 \(\Lambda\) 增长，因此结论是 family-level departure，不是对一个固定基流的 Lyapunov 不稳定性。</p></section>
        <section id="action"><div class="section-no">02 / Action recoding</div><h2>两侧 bounded prefactor 把未知实际增益换成完整无黏作用量</h2><div class="equation result">\[c_Le^{\Lambda\mathcal A_*}\le G_\Lambda^*\le C_Le^{\Lambda\mathcal A_*},\qquad \delta_\Lambda=\rho G_\Lambda^*e^{-\Lambda\mathcal A_*}\in[c_L\rho,C_L\rho].\]</div><p>这一步只使用 R0.73L 的两侧界，不假设 prefactor 收敛。若只知道 \(\Lambda^{-1}\log G_\Lambda^*\to\mathcal A_*\)，就不能保证有效 Taylor 振幅留在统一半径内。</p></section>
        <section id="localization"><div class="section-no">03 / Forward localization</div><h2>固定端点上的局部化速率严格越过二次与三次门槛</h2><p>端点归一化轨道满足 \(\|a_\Lambda(s)\|_2\le C_Le^{-\mu_*\Lambda(D_*-s)}\)，其中 \(\mu_*=167/1000>1/6\)。这是同一条前向轨道的商，不是反向求解抛物方程。</p></section>
        <section id="hierarchy"><div class="section-no">04 / Nonlinear hierarchy</div><h2>二次、三次与四阶余项在完整固定窗口上闭合</h2><div class="equation result">\[2\mu_*-\tfrac13=\tfrac1{1500},\qquad3\mu_*-\tfrac12=\tfrac1{1000},\qquad4\mu_*-\tfrac12=\tfrac{21}{125}.\]</div><p>三个严格正裕度分别控制 doubled row、cubic rows 与四阶 remainder。证明沿精确 Fourier–Leray 行和 Stieltjes 能量账本工作，没有插入全空间高 Sobolev 半群界。</p></section>
        <section id="endpoint"><div class="section-no">05 / Fixed-distance endpoint</div><h2>选定谐波的线性主项压过立方修正与四阶余项</h2><p>对 \(0<\rho\le\rho_0\)，有效振幅 \(\delta_\Lambda\) 保持统一小，奇偶谐波结构排除二次项直接返回 \(K_z=\pm1\)。故终点 selected-pair 范数 \(\ge(c_L/2)\rho\)。</p></section>
        <section id="global"><div class="section-no">06 / Exact dimensional boundary</div><h2>全局光滑性来自精确二维不变子空间</h2><p>背景和实值 launch 都属于 \(\mathcal S_{2D}=\{(0,u_2(y,z),u_3(y,z)): \partial_yu_2+\partial_zu_3=0\}\)。二维涡量能量恒等式给出每条 selected orbit 的全局光滑性；这里没有控制横向三维扰动或 vortex stretching。</p></section>
        <section id="audits"><div class="section-no">07 / Independent audits</div><h2>独立解析、对抗与文献边界审计均为 PASS</h2><p>审计逐项核对物理/kinetic 范数、\(d=4t\) 因子、行支持、三个严格裕度、bounded-prefactor 而非 prefactor-limit 的用法，以及量词次序。对抗审计没有找到能保留全部封存假设的反例。</p></section>
        <section id="diagnostic"><div class="section-no">08 / Finite diagnostic</div><h2>15 个主案例、5 个线性哨兵与 3 个层级哨兵独立通过</h2><p>有限网格为 \(N=40,48,64\) 与五个 \(\varepsilon\) 水平，共 1,170 行 action 数据。有限 inviscid-action prefactor 位于 \([0.9960745297,0.9965850278]\)；独立线性重算的最大 gain 差为 \(2.083\times10^{-9}\)，独立 cubic hierarchy 的最大系数相对差为 \(8.320\times10^{-10}\)。验证器 28/28 PASS。</p><p>有限量 \(A_{N,0}\) 与连续量 \(\mathcal A_*\) 分开命名；有限 cutoff agreement 不认证连续 Fourier tail，也不认证 prefactor 极限。</p></section>
        <section id="figure"><div class="section-no">09 / Journal figure</div><h2>作用量归一化、谐波层级、带符号 cubic return 与门限裕度已归档</h2><p><img src="/assets/r073m/__FIGURE_ID__.svg" alt="R0.73M finite prescribed-action departure diagnostic"></p><p><a href="/assets/r073m/__FIGURE_ID__.pdf">下载矢量 PDF</a> · <a href="/assets/r073m/__FIGURE_ID__.png">下载 600 dpi PNG</a> · <a href="/assets/r073m/__FIGURE_ID__.svg">打开 SVG</a></p></section>
        <section id="literature"><div class="section-no">10 / Deep Research boundary</div><h2>邻近文献提供机制先例，但没有可直接代入的同构定理</h2><p>Friedlander–Pavlović–Shvydkoy 处理自治谱不稳定到非线性不稳定；Grenier 系方法处理高阶 corrector 和边界层；Li–Masmoudi–Zhao 证明精确无外力 near-Couette 热流的瞬态非线性放大；Li–Zhao 研究无边界热演化剪切的谱转变。限定检索没有发现一条现成定理同时包含这里的移动黏性谱线、完整慢窗 action、谐波返回、零外力和固定距离终点。这只是 bounded-search gap，不是绝对原创性或优先权声明。</p></section>
        <section id="boundary"><div class="section-no">11 / Exact boundary</div><h2>连续定理、有限诊断和开放问题分开列示</h2><p>__CLOSED__。</p><p>__FINITE__。</p><p>__OPEN__。</p><p>本节没有 prefactor 极限、两项 WKB、固定背景 Lyapunov 不稳定、横向三维闭合、有限时间奇性或 Clay 结论。NOT CLAY。</p></section>
        <section id="value"><div class="section-no">12 / Research value</div><h2>初始尺度不再依赖未知实际增益</h2><p>严格增量是把 gain-normalized departure 升级为 full-action-prescribed departure，并把终点固定在 \(T_*=1/1800\)。这使结果更接近可比较、可引用的非自治不稳定定理，但 family-level 与二维边界仍是决定性限制。</p></section>
        <section id="next"><div class="section-no">13 / Next gate</div><h2>R0.73N：固定背景 Lyapunov 不稳定性的可行性与障碍审计</h2><p>下一节只做 feasibility/obstruction gate：先辨认变背景幅度 \(O(\Lambda)\) 是否能通过重标度、时间平移或嵌入机制变成一个固定基流问题，并逐条检验量词与范数。它不预设可闭合；若结构性障碍成立，就以 no-go 定理封存。横向三维与 Clay 仍是更后的 OPEN 接口。</p></section>
        <section id="reproduce"><div class="section-no">14 / Reproduction</div><h2>证明、审计、文献、证书和附图均有直接入口</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073m_prescribed_action_departure_proof.md">解析证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073m_independent_analytic_audit.md">独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073m_adversarial_audit.md">对抗审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073m_literature_audit.md">Deep Research 文献审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073m">有限诊断包</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073m/__FIGURE_ID__">正式附图包</a> · <a href="/notes/r0-73m.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73m.html">129 节累计回顾</a> · <a href="/recap-r0-61-r0-73m.pdf">累计回顾 PDF</a></p></section>
      </article>'''
NOTE_ARTICLE = (NOTE_ARTICLE.replace("__FIGURE_ID__", FIGURE_ID)
                .replace("__CLOSED__", CLOSED)
                .replace("__FINITE__", FINITE)
                .replace("__OPEN__", OPEN))

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73N</span><span class="tree-state current">下一检查点</span></div>
              <h3>固定背景 Lyapunov 不稳定性的可行性与障碍审计</h3><p>辨认变背景 family-level theorem 能否转化成固定基流问题；不预设闭合，结构性失败就封存为 no-go。横向三维与 Clay 保持为更后的 OPEN 接口。</p>
            </article>'''

HOME_M_CARD = r'''          <div class="task-one" id="r073m" data-release="r073m" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73M · 2026-08-31</p><h3>由完整作用量指定种子的平面非线性固定距离偏离</h3>
            <p>对精确无外力两谐波剪切背景族，初始扰动 \(\rho e^{-\Lambda\mathcal A_*}\phi_\Lambda\) 在固定物理时刻 \(T_*=1/1800\) 产生至少 \(c_*\rho\) 的 selected-pair 距离，同时初始 \(H^3\) 范数趋于零。</p>
            <p>R0.73L 的 bounded two-sided prefactor 把未知实际增益换成完整 inviscid action；\(1/1500\)、\(1/1000\)、\(21/125\) 三个严格裕度闭合非线性谐波层级。</p>
            <p><strong>有限诊断：</strong>15 个主案例、1,170 行 action 数据、5 个独立线性哨兵、3 个独立层级哨兵和 28/28 验证均通过；这些有限数据不承担连续证明权重。</p>
            <p><strong>开放边界：</strong>&nbsp;__OPEN__。NOT CLAY。</p>
            <p><a href="/notes/r0-73m.html"><strong>阅读 R0.73M 研究笔记 →</strong></a><br><a href="/notes/r0-73m.pdf">下载同步 PDF</a> · <a href="/assets/r073m/__FIGURE_ID__.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073m">查看有限诊断包</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073m_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73m.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73N：</strong>&nbsp;固定背景 Lyapunov 不稳定性的可行性与障碍审计；不预设闭合。</p>
          </div>'''
HOME_M_CARD = HOME_M_CARD.replace("__FIGURE_ID__", FIGURE_ID).replace("__OPEN__", OPEN)

HOME_LATEST_SPOTLIGHT = r'''    <section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">
      <div class="route-overview-inner"><header class="route-map-header">
        <div><p class="eyebrow">LATEST RELEASE · R0.73M · 2026-08-31</p><h2 class="route-map-title" id="latest-release-title">由完整作用量指定种子的平面非线性固定距离偏离</h2><p class="route-map-intro">R0.73L 的真实非自治 selected action 已接到固定端点的非线性谐波层级：prescribed-action seed、物理/kinetic 精确共轭、forward-orbit localization、二次与三次能量账本、四阶余项、固定距离终点和二维全局光滑性均已闭合。独立解析、对抗、文献、有限证书和正式附图分别通过；固定背景、横向三维、奇性与 Clay 继续 OPEN。</p></div>
        <nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-73m.pdf">阅读最新 R0.73M 研究笔记 →</a><a href="/recap-r0-61-r0-73m.html">129 节累计回顾</a><a href="/notes/">189 篇研究笔记总索引</a><a href="#r073m">查看首页完整 R0.73M 卡片</a></nav>
      </header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73M · 91 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>67 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73M</span></div></div>
    </section>'''

RECAP_PHASE = r'''            <article class="phase"><h3>R0.73M · Prescribed-action planar nonlinear departure</h3><p>R0.73L 的两侧 selected-action 界把 R0.73H 中依赖未知实际增益的种子，重写为 \(\rho e^{-\Lambda\mathcal A_*}\phi_\Lambda\)。在完整 \(D_*=1/450\) 窗口上，endpoint-normalized forward orbit 的速率 \(\mu_*=0.167>1/6\) 使二次、三次与四阶能量账本分别留下 \(1/1500\)、\(1/1000\)、\(21/125\) 的严格裕度。</p><p>因此指数小的 \(H^3\) 扰动在固定物理时刻 \(T_*=1/1800\) 到达与 \(\rho\) 同阶的 selected-pair 距离。轨道全局光滑只因为它们留在精确二维不变子空间。15 个有限案例、两种独立重算、28/28 验证和期刊级四联图用于复现与错误探测，不认证连续结论。</p><p>__CLOSED__。__FINITE__。__OPEN__。NOT CLAY。</p><div class="links"><a href="/notes/r0-73m.html">R0.73M</a><a href="/assets/r073m/__FIGURE_ID__.pdf">R0.73M 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073m">R0.73M 有限诊断包</a></div></article>'''
RECAP_PHASE = (RECAP_PHASE.replace("__CLOSED__", CLOSED)
               .replace("__FINITE__", FINITE)
               .replace("__OPEN__", OPEN)
               .replace("__FIGURE_ID__", FIGURE_ID))
