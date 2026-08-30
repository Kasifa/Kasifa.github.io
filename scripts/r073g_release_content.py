#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reader-facing source fragments for the fail-closed R0.73G release."""

FIGURE_ID = "fig-r073g-nonlinear-row-leakage"
FIGURE_RELATIVE = f"figures/r073g/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r073g"
EXPERIMENT_RELATIVE = "experiments/r073g"

R073F_RELEASE_BASELINE = {
    "latestCompletedRelease": "r073f",
    "siteVersion": "1.46",
    "publicHtmlNoteCount": 182,
    "postR060RecapNodeCount": 122,
    "nextRelease": "r073g",
    "latestReleaseGate": "tests/r073f-moving-dichotomy-gate.test.mjs",
    "latestReleasePublicationTest": "tests/r073f-release.test.mjs",
    "postR070APublishedReleaseCount": 84,
    "postR070AFormalSealedReleaseCount": 60,
    "legacyFormalFigureBacklogCount": 24,
}

R073G_RELEASE_TARGET = {
    "latestCompletedRelease": "r073g",
    "siteVersion": "1.47",
    "publicHtmlNoteCount": 183,
    "postR060RecapNodeCount": 123,
    "nextRelease": "r073h",
    "postR070APublishedReleaseCount": 85,
    "postR070AFormalSealedReleaseCount": 61,
    "legacyFormalFigureBacklogCount": 24,
}

CLOSED = (
    "exactDecayingShearPerturbationEquation=CLOSED；"
    "selectedSeedPlanarInvariantClass=CLOSED；"
    "selectedNonlinearOrbitGlobalSmoothness=CLOSED；"
    "topEigenvectorPolynomialH3Cost=CLOSED；"
    "fixedWindowH3Bootstrap=CLOSED；"
    "allModeQuadraticRemainderBound=CLOSED；"
    "nonlinearRelativeAmplification=CLOSED；"
    "topEigenvectorDoubleRowLeakage=CLOSED"
)

FALSE = (
    "singleLinearRowNonlinearInvariant=FALSE；"
    "kineticL2QuadraticRemainderBound=FALSE；"
    "selectedRowCanCreateThreeDimensionalVortexStretching=FALSE；"
    "oneRowGainAloneImpliesOrderOneDeparture=FALSE_AS_INFERENCE；"
    "oneRowGainAloneImpliesFiniteTimeSingularity=FALSE"
)

OPEN = (
    "naturalSeedOrderOneDeparture=OPEN；"
    "targetedCubicModeConvolutionEstimate=OPEN；"
    "harmonicResolvedEvenOddPropagation=OPEN；"
    "transverseThreeDimensionalTriadClosure=OPEN；"
    "singleBackgroundSingleOrbitInstability=OPEN；"
    "completeOSSquireA2DirectSum=OPEN；Clay=OPEN"
)

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73G · NONLINEAR RELATIVE AMPLIFICATION · PLANAR BARRIER</div>
        <h1>过小种子的非线性相对放大<br>与精确二维屏障</h1>
        <p class="lead">R0.73G 把 R0.73F 的一行线性固定窗口下界嵌入完整 Navier--Stokes 扰动方程。对一个显式的指数级过小种子，\(H^3\) bootstrap 与全模态 \(L^2\) 余项估计保留至少一半线性相对增益；同一 launch 又严格留在全局正则的二维不变子空间。natural seed、order-one departure、transverse 3D 与 Clay 均保持 OPEN。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73G 完成</span><strong>Relative gain</strong><p>版本 v0.73G · 2026-08-30</p><p>EXACT NONLINEAR THEOREM</p><p>8 项结论：CLOSED</p><p>5 个无效推断：FALSE</p><p>NATURAL / 3D：OPEN</p><p>NOT CLAY</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>非线性相对放大已闭合；直接路线同时被二维正则性封住</h2><div class="verdict-grid"><div class="verdict-card true"><strong>CLOSED · NONLINEAR GAIN</strong><p>对显式指数级过小种子，完整非线性解在固定物理窗口保留至少一半的 R0.73F 相对增益。</p></div><div class="verdict-card true"><strong>CLOSED · ALL-MODE ERROR</strong><p>\(H^3\) 强范数控制与 \(L^2\) 余项能量估计覆盖卷积生成的零行、倍频行及后续模态。</p></div><div class="verdict-card true"><strong>CLOSED · GLOBAL PLANAR ORBIT</strong><p>所选真实共轭 launch 的完整非线性轨道等价于周期二维 Navier--Stokes，因而全局光滑。</p></div><div class="verdict-card false"><strong>OPEN · NATURAL / TRANSVERSE 3D</strong><p>自然种子、order-one departure、横向三维耦合和 Clay 没有被当前估计证明。</p></div></div></section>
        <section id="background"><div class="section-no">01 / Exact background</div><h2>背景是标准三维环面上的精确无外力解</h2><div class="equation result">\[\overline U_\Lambda(t,y)=\bigl(0,0,2\Lambda W(4t,2y)\bigr),\qquad W(d,x)=-\tfrac12e^{-d}\sin x+\tfrac14e^{-4d}\sin2x.\]</div><p>由 \(W_d=W_{xx}\)，黏性取一时该背景精确满足 Navier--Stokes。扰动方程保留完整三维 Leray 投影与全部二次卷积。</p></section>
        <section id="equation"><div class="section-no">02 / Full perturbation</div><h2>非线性项没有投影回原始 Fourier 行</h2><div class="equation result">\[\partial_tw=L_\Lambda(t)w-\mathbb P\nabla\!\cdot(w\otimes w),\quad L_\Lambda(t)w=\Delta w-\mathbb P(\overline U_\Lambda\!\cdot\nabla w+w\!\cdot\nabla\overline U_\Lambda).\]</div><p>标度为 \(x=2y\)、\(d=4t\)、\(\theta=4\Lambda t\)、\(\varepsilon=\Lambda^{-1}\)。R0.73F 的 fast endpoint 正好对应 \(T_D=\min(D,d_0)/4\)。</p></section>
        <section id="planar"><div class="section-no">03 / Exact planar barrier</div><h2>较大的二维子空间不变；单一 Fourier 行并非不变</h2><div class="equation result">\[\mathcal S_{2D}=\{(0,u_2(y,z),u_3(y,z)):\partial_yu_2+\partial_zu_3=0\}.\]</div><p>背景与所选 top launch 均属于 \(\mathcal S_{2D}\)。完整非线性演化在该空间内就是周期二维 Navier--Stokes；标量涡量没有三维 vortex stretching，光滑轨道全局存在。</p></section>
        <section id="launch"><div class="section-no">04 / Smooth launch</div><h2>一个冻结 top 向量具有多项式 Sobolev 成本</h2><div class="equation result">\[\|\phi_\Lambda\|_2=1,\qquad \|\phi_\Lambda\|_{H^3}\le C_{\rm top}\Lambda^2.\]</div><p>固定围道控制 top eigenvalue；两次椭圆迭代给出 kinetic eigenvector 的 \(H^4=O(\Lambda^2)\)。精确 kinetic-to-velocity 等距与真实共轭配对把它变成标准环面上的平面真实向量。</p></section>
        <section id="bootstrap"><div class="section-no">05 / Strong-norm bootstrap</div><h2>固定窗口上的保守 \(H^3\) 包络闭合</h2><div class="equation result">\[Y'(t)\le a\Lambda Y(t)+bY(t)^2,\qquad Y(0)\le\frac{a\Lambda}{4b}e^{-a\Lambda T_D}.\]</div><div class="equation result">\[\sup_{0\le t\le T_D}Y(t)\le2e^{a\Lambda T_D}Y(0).\]</div><p>这里 \(Y=\|w\|_{H^3}\)。该估计是足够条件，不是自然转捩阈值；全局存在另外由精确二维不变性保证。</p></section>
        <section id="remainder"><div class="section-no">06 / All-mode remainder</div><h2>二次误差以完整 \(L^2\) 能量估计控制</h2><div class="equation result">\[\|r(T_D)\|_2\le C_De^{M_D\Lambda}\|w(0)\|_{H^3}^2,\qquad M_D=(c/2+2a)T_D.\]</div><p>令 \(r=w-z\)，其中 \(z\) 是精确全空间线性化解。估计不选择 Fourier 行，因此不会漏掉 mode convolution。</p></section>
        <section id="seed"><div class="section-no">07 / Explicit seed ceiling</div><h2>过小种子足以保留一半线性比率</h2><div class="equation result">\[\delta_\Lambda^{\max}=\min\!\left\{\frac{a}{4bC_{\rm top}}\Lambda^{-1}e^{-a\Lambda T_D},\frac{\Lambda^{-4}}{2K_{\rm F}C_DC_{\rm top}^2}e^{-(M_D-\kappa_D)_+\Lambda}\right\}.\]</div><div class="equation result">\[\|w(T_D)\|_2\ge(2K_{\rm F})^{-1}e^{\kappa_D\Lambda}\|w(0)\|_2.\]</div><p>该结论是相对放大。允许的 \(\delta\) 可能比 \(e^{-\kappa_D\Lambda}\) 更小，因此端点绝对幅度仍可能趋零。</p></section>
        <section id="leakage"><div class="section-no">08 / Exact row leakage</div><h2>top launch 在第一轮卷积产生零频与倍频行</h2><div class="equation result">\[u_v=(0,v(2y),2iv'(2y))e^{iz},\qquad (u_v\!\cdot\nabla)u_v=(0,0,4i[vv''-(v')^2](2y))e^{2iz}.\]</div><p>冻结 eigen-equation 的极端 \(n+2\) 列排除全部可能被 Leray 投影消去的两频 exceptional profile。真实共轭对产生 \(K_z=0,\pm2\)，反馈到 \(K_z=\pm1\) 最早出现在下一轮，即种子的三次阶。</p></section>
        <section id="false"><div class="section-no">09 / Exact no-go results</div><h2>线性增长、单行封闭和奇性推断分别失效</h2><p>显式 Fourier--Leray triad 否定单行非线性不变性，也给出不存在 \(\|\mathbb P(u\cdot\nabla u)\|_2\le C\|u\|_2^2\) 的精确高频反例。另一个全局有界二次 ODE 说明 \(e^{t/\varepsilon}\) 线性增长本身不蕴含非线性 blow-up。</p></section>
        <section id="finite"><div class="section-no">10 / Finite diagnostic boundary</div><h2>有限 Fourier 计算只诊断 Sobolev 成本与行泄漏</h2><p>一维约化恒等式、generic convolution kernel 与独立 FFT/Leray 实现在全部归档参数上相符，跨实现最大 scale-one 差为 \(6.01\times10^{-16}\)。cutoff 比较、有限 top eigenvector、\(H^3/L^2\) 成本和 \(K_z=0,\pm2\) 泄漏都不证明 continuum top cluster、非线性定理、自然阈值或三维正则性。</p></section>
        <section id="literature"><div class="section-no">11 / Literature boundary</div><h2>已有不稳定 bootstrap 提供方法参照，不是本问题的黑箱</h2><p><a href="https://doi.org/10.1007/s00220-006-1526-7">Friedlander--Pavlović--Shvydkoy</a>处理 steady autonomous Navier--Stokes；<a href="https://doi.org/10.1002/1097-0312%28200009%2953%3A9%3C1067%3A%3AAID-CPA1%3E3.0.CO%3B2-Q">Grenier</a>与<a href="https://numdam.org/item/AIHPC_2003__20_1_87_0/">Desjardins--Grenier</a>展示高阶 corrector、interaction algebra 与 residual control 的额外义务；<a href="https://doi.org/10.1007/s40818-019-0074-3">Grenier--Nguyen</a>的 heat-evolving 结果属于有边界层、解析性和小外力的不同几何。本节只作有界 non-collision 检查，不作原创性或优先权声明。</p></section>
        <section id="audit"><div class="section-no">12 / Independent analytic audit</div><h2>主定理的标度、等距、能量、余项与倍频证明逐项通过</h2><p>独立审计重新计算 \(d=4t\)、真实共轭归一化、\(H^3\) Riccati 界、\(M_D=(c/2+2a)T_D\) 及 extreme-column noncancellation。最终结论为 FINAL PASS；该复核不把有限诊断当作解析证明。</p></section>
        <section id="figure"><div class="section-no">13 / Journal figure</div><h2>top-vector 成本、倍频泄漏、零频泄漏与 cutoff 诊断归档</h2><p><img src="/assets/r073g/__FIGURE_ID__.svg" alt="R0.73G finite nonlinear row-leakage diagnostic"></p><p><a href="/assets/r073g/__FIGURE_ID__.pdf">下载 PDF</a> · <a href="/assets/r073g/__FIGURE_ID__.png">下载 600 dpi PNG</a> · <a href="/assets/r073g/__FIGURE_ID__.svg">打开 SVG</a></p></section>
        <section id="boundary"><div class="section-no">14 / Exact boundary</div><h2>CLOSED、FALSE 与 OPEN 保持分离</h2><p>__CLOSED__。</p><p>__FALSE__。</p><p>__OPEN__。</p></section>
        <section id="value"><div class="section-no">15 / Research value</div><h2>线性固定窗口下界已升级为一个精确但过小种子的非线性定理</h2><p>严格增量是 exact nonlinear relative amplification 与 exact planar global-regularity barrier 同时成立。它说明显著相对增长可以与全局光滑并存，也定位了直接一行路线对 Clay 的结构性限制；没有自然尺度的 order-one instability 或三维奇性结论。</p></section>
        <section id="next"><div class="section-no">16 / Next gate</div><h2>R0.73H：自然种子上的 harmonic-resolved 余项与横向三维接口</h2><p>下一门优先估计 even second-order response 与 odd cubic feedback，检验 \(e^{-\kappa_D\Lambda}\) 自然种子能否达到 order one；并冻结 \(K_x\ne0\) 或第一速度分量的 transverse coupling。任何 Clay 外推仍须经过新的三维定理。</p></section>
        <section id="reproduce"><div class="section-no">17 / Reproduction</div><h2>报告、证明、两份解析审计、文献与有限诊断均提供直接入口</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073g_report-source.md">完整报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073g_nonlinear_shadowing_proof.md">主证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073g_operator_derivation.md">独立算子推导</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073g_adversarial_audit.md">敌对审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073g_independent_analytic_audit.md">独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073g_gap_matrix.md">缺口矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073g_literature_audit.md">文献审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073g">正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073g">有限诊断与监控</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073g/__FIGURE_ID__">正式附图包</a> · <a href="/notes/r0-73g.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73g.html">123 节累计回顾</a> · <a href="/recap-r0-61-r0-73g.pdf">累计回顾 PDF</a></p></section>
      </article>'''
NOTE_ARTICLE = (
    NOTE_ARTICLE
    .replace("__FIGURE_ID__", FIGURE_ID)
    .replace("__CLOSED__", CLOSED)
    .replace("__FALSE__", FALSE)
    .replace("__OPEN__", OPEN)
)

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73H</span><span class="tree-state current">下一检查点</span></div>
              <h3>自然种子的 harmonic-resolved 余项与横向三维接口</h3><p>先控制 even 二阶响应和 odd 三阶反馈，再加入 \(K_x\ne0\) 或非零第一速度分量；分别检验 order-one departure 与 transverse 3D coupling。</p>
            </article>'''

HOME_G_CARD = r'''          <div class="task-one" id="r073g" data-release="r073g" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73G · 2026-08-30</p><h3>过小种子的非线性相对放大与精确二维屏障</h3>
            <p>显式 \(H^3\) bootstrap 和全模态 \(L^2\) 余项估计，把 R0.73F 的一行线性下界升级为固定窗口上的精确非线性相对放大。</p>
            <p>同一 launch 严格留在全局正则的二维不变子空间。单行会泄漏到 \(K_z=0,\pm2\)，但不会产生三维 vortex stretching；natural seed、order-one departure、transverse 3D 与 Clay 保持 OPEN。</p>
            <p><strong>闭合结论：</strong>&nbsp;__CLOSED__。</p><p><strong>否定推断：</strong>&nbsp;__FALSE__。</p><p><strong>开放边界：</strong>&nbsp;__OPEN__。</p>
            <p><a href="/notes/r0-73g.html"><strong>阅读 R0.73G 研究笔记 →</strong></a><br><a href="/notes/r0-73g.pdf">下载同步 PDF</a> · <a href="/assets/r073g/__FIGURE_ID__.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073g">查看正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073g_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73g.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73H：</strong>&nbsp;冻结自然种子的 harmonic-resolved 余项，并建立 transverse 3D coupling 的精确接口。</p>
          </div>'''
HOME_G_CARD = (
    HOME_G_CARD
    .replace("__FIGURE_ID__", FIGURE_ID)
    .replace("__CLOSED__", CLOSED)
    .replace("__FALSE__", FALSE)
    .replace("__OPEN__", OPEN)
)

HOME_LATEST_SPOTLIGHT = r'''    <section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">
      <div class="route-overview-inner"><header class="route-map-header">
        <div><p class="eyebrow">LATEST RELEASE · R0.73G · 2026-08-30</p><h2 class="route-map-title" id="latest-release-title">过小种子的非线性相对放大与精确二维屏障</h2><p class="route-map-intro">八项精确非线性结论闭合，五个过强推断被拒绝。自然种子、order-one departure、transverse 3D 与 Clay 保持 OPEN。</p></div>
        <nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-73g.pdf">阅读最新 R0.73G 研究笔记 →</a><a href="/recap-r0-61-r0-73g.html">123 节累计回顾</a><a href="/notes/">183 篇研究笔记总索引</a><a href="#r073g">查看首页完整 R0.73G 卡片</a></nav>
      </header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73G · 85 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>61 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73G</span></div></div>
    </section>'''
