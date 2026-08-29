#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reader-facing source fragments for the fail-closed R0.73E release."""

FIGURE_ID = "fig-r073e-complement-transfer"
FIGURE_RELATIVE = f"figures/r073e/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r073e"
EXPERIMENT_RELATIVE = "experiments/r073e"

R073D_RELEASE_BASELINE = {
    "latestCompletedRelease": "r073d",
    "siteVersion": "1.44",
    "publicHtmlNoteCount": 180,
    "postR060RecapNodeCount": 120,
    "nextRelease": "r073e",
    "latestReleaseGate": "tests/r073d-viscous-persistence-gate.test.mjs",
    "latestReleasePublicationTest": "tests/r073d-release.test.mjs",
    "postR070APublishedReleaseCount": 82,
    "postR070AFormalSealedReleaseCount": 58,
    "legacyFormalFigureBacklogCount": 24,
}

CLOSED = (
    "fixedPositiveHalfPlaneNoPollution=CLOSED；"
    "allModesRightOfBProjectionNormPersistence=CLOSED；"
    "topInviscidClusterExists=CLOSED；topViscousClusterPersistence=CLOSED；"
    "topReducedHalfPlaneResolventUniform=CLOSED；"
    "frozenTopClusterRelativeDichotomy=CLOSED；"
    "fixedFrozenGeneratorVolterraTransfer=CLOSED；logFastTimeTransfer=CLOSED；"
    "superPolynomialCompleteRowNoGo=CLOSED"
)

OPEN = (
    "certifiedSigmaStarIsRightmost=OPEN；selectedSigmaStarComplementDichotomy=OPEN；"
    "uniformHalfPlaneBoundAtBEqualsZero=OPEN；globalRightHalfPlaneNoPollution=OPEN；"
    "absoluteUniformComplementDecay=OPEN；explicitHalfPlaneGap=OPEN；"
    "explicitViscosityThreshold=OPEN；quantitativeEigenvalueRate=OPEN；"
    "movingProfileUniformContour=OPEN；graphDomainKatoTransport=OPEN；"
    "movingProfileEvolutionDichotomy=OPEN；inviscidRootUnique=OPEN；"
    "inviscidEigenvalueSimple=OPEN；completeOSSquireA2DirectSum=OPEN；"
    "fixedWindowExponentialLowerLaw=OPEN；nonlinearNavierStokes=OPEN；Clay=OPEN"
)

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73E · HALF-PLANE SPLITTING · LOGARITHMIC TRANSFER</div>
        <h1>固定正半平面分裂与<br>对数快时间传递</h1>
        <p class="lead">对一条精确的周期二维 Fourier 行，我把 R0.73D 的局部谱簇持续推进到每个固定正半平面的谱完备性、完整 top cluster 的相对二分，以及 \(M\log(1/\varepsilon)\) 快时间上的 Volterra 传递。由此排除必须覆盖该行的任意固定次数多项式上界。固定物理窗口指数律、移动谱束、完整 OS--Squire、非线性与 Clay 仍未解决。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73E 完成</span><strong>Half-plane transfer</strong><p>版本 v0.73E · 2026-08-30</p><p>9 项线性结论：CLOSED</p><p>fixed-window exponential：OPEN</p><p>complete OS--Squire：OPEN</p><p>nonlinear / Clay：OPEN</p></div>
    </div></header>'''

NOTE_ARTICLE = rf'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>固定正半平面与对数传递已闭合；移动谱束和非线性仍开放</h2><div class="verdict-grid"><div class="verdict-card true"><strong>CLOSED · FIXED HALF-PLANE</strong><p>任意固定 \(b&gt;0\) 且边界线避开无黏谱时，右侧谱由有限个持续谱簇完全捕获；总 Riesz 投影和有限谱块按算子范数收敛。</p></div><div class="verdict-card true"><strong>CLOSED · RELATIVE DICHOTOMY</strong><p>选取全部最右 top cluster 后，补空间有统一的相对增长上界，top block 有统一的反向增长控制。</p></div><div class="verdict-card true"><strong>CLOSED · LOG TRANSFER</strong><p>精确 profile drift 是 \(O(\varepsilon\theta)\) 的有界扰动；任意固定 \(M&gt;0\) 的 \(M\log(1/\varepsilon)\) 快时间增长可传递。</p></div><div class="verdict-card false"><strong>OPEN · MOVING / NONLINEAR</strong><p>固定小物理窗口上的 moving-profile top bundle、\(e^{{c|\Lambda|}}\) 律、完整 OS--Squire、非线性与 Clay 保持 OPEN。</p></div></div></section>
        <section id="row"><div class="section-no">01 / Exact row</div><h2>结论只覆盖一个精确周期 Fourier 行</h2><div class="equation result">\[\beta=\xi=0,\quad\gamma=\tfrac12,\quad \varepsilon=|\Lambda|^{{-1}},\quad B_\varepsilon=M+K-\varepsilon L.\]</div><div class="equation result">\[M^*=-M,\qquad K\text{{ compact}},\qquad L=-\partial_x^2+\tfrac14.\]</div><p>物理 kinetic vorticity norm 通过 \(U=2L^{{-1/2}}\) 与 \(L^2\) 精确等距。定义域从 \(\varepsilon&gt;0\) 的 \(H^2\) 跳到 \(\varepsilon=0\) 的全空间，因此这不是有界小扰动问题。</p></section>
        <section id="halfplane"><div class="section-no">02 / Fixed positive half-plane</div><h2>每条固定正竖线右侧没有额外黏性谱污染</h2><div class="equation result">\[\sigma(B_0)\cap\{{\operatorname{{Re}}z=b\}}=\varnothing\Longrightarrow \sup_{{0&lt;\varepsilon&lt;\varepsilon_b}}\sup_{{\operatorname{{Re}}z\ge b}}\|(z-B_\varepsilon)^{{-1}}Q_{{\varepsilon,b}}\|&lt;\infty.\]</div><p>证明把紧矩形上的 compact--Fredholm 收敛与高虚部 \(O(|\operatorname{{Im}}z|^{{-1}})\) resolvent 尾部拼接。结论对每个固定 \(b&gt;0\) 成立，不对 \(b\downarrow0\) 一致。</p></section>
        <section id="projection"><div class="section-no">03 / Total projection</div><h2>右侧全部谱簇必须一起投影</h2><div class="equation result">\[\|P_{{\varepsilon,b}}-P_{{0,b}}\|\to0,\qquad \|B_\varepsilon P_{{\varepsilon,b}}-B_0P_{{0,b}}\|\to0.\]</div><p>这比只追踪 R0.73C 的一个 \(\sigma_*\) 更强，也更必要。有限诊断显示，移除领先有限谱簇后仍有正实部共轭对；这项有限观察不被解释为 continuum 点谱证明。</p></section>
        <section id="top"><div class="section-no">04 / Complete top cluster</div><h2>最右谱集由全部实部等于 \(a\) 的特征值组成</h2><div class="equation result">\[a=\max_{{z\in\sigma(B_0)}}\operatorname{{Re}}z\ge\sigma_*&gt;0.17035,\qquad \Sigma_{{\rm top}}=\{{z:\operatorname{{Re}}z=a\}}.\]</div><p>没有证明已认证的 \(\sigma_*\) 本身最右，也没有证明它唯一或单。top cluster 是有限集合，并与其余无黏谱保持正的但未显式计算的实部间隔。</p></section>
        <section id="dichotomy"><div class="section-no">05 / Relative dichotomy</div><h2>统一控制是相对增长，不是补空间绝对衰减</h2><div class="equation result">\[\|e^{{tB_\varepsilon}}Q_{{\varepsilon,\rm top}}\|\le C_b e^{{bt}},\qquad \|e^{{-tB_\varepsilon}}P_{{\varepsilon,\rm top}}\|\le C_c e^{{-ct}},\quad b&lt;c&lt;a.\]</div><p>完整竖线 resolvent、平方 resolvent 的可积性、Bromwich 移线和共同短时间界共同给出统一 prefactor。局部围道或逐个 \(\varepsilon\) 的解析半群不足以推出这个结论。</p></section>
        <section id="drift"><div class="section-no">06 / Exact drift</div><h2>热剖面的快时间漂移有显式有界上界</h2><div class="equation result">\[\|U(A(d)-A(0))U^{{-1}}\|\le\frac{{49}}{{4}}d,\qquad d=\varepsilon\theta.\]</div><p>该估计允许直接在固定冻结生成元上写 Duhamel 方程，不需要假设 moving Riesz projection、graph-domain Kato transport 或移动谱隙已经存在。</p></section>
        <section id="transfer"><div class="section-no">07 / Logarithmic transfer</div><h2>任意固定 \(M\) 的对数快时间都能保留 top-mode 增长</h2><div class="equation result">\[T_\varepsilon=M\log(1/\varepsilon),\qquad \|\mathcal U_\varepsilon(T_\varepsilon,0)v_\varepsilon\|\ge\tfrac12e^{{\operatorname{{Re}}\lambda_\varepsilon T_\varepsilon}}.\]</div><p>误差相对量为 \(O(\varepsilon^{{1/2}}\log^2(1/\varepsilon))\)。对应物理时间 \(d_\varepsilon=M\log|\Lambda|/|\Lambda|\to0\)，因此最终落入任意固定 \(d_*&gt;0\) 观察窗口。</p></section>
        <section id="consequence"><div class="section-no">08 / Complete-row consequence</div><h2>必须覆盖该行的固定次数多项式上界全部失效</h2><div class="equation result">\[\forall d_*,p&gt;0,\qquad \lim_{{|\Lambda|\to\infty}}\frac{{G_{{1/2}}(\Lambda;d_*)}}{{|\Lambda|^p}}=\infty.\]</div><p>三角 OS--Squire 行中取零初始 Squire 分量，完整行范数至少覆盖这一 q-block 下界。这里没有闭合完整 \(A_2\) 直和，也没有得到固定窗口 \(e^{{c|\Lambda|}}\) 下界。</p></section>
        <section id="finite"><div class="section-no">09 / Finite diagnostic</div><h2>有限矩阵解释为什么不能只删一个领先谱簇</h2><table class="compact-table"><thead><tr><th>对象</th><th>\(N=96,\varepsilon=10^{{-6}}\)</th></tr></thead><tbody><tr><td>leading eigenvalue</td><td>0.170406506600201</td></tr><tr><td>finite complementary pair</td><td>\(0.040536174080661\pm0.176136754131770i\)</td></tr><tr><td>moving complement semigroup at \(t=200\)</td><td>\(1.68367\times10^4\)</td></tr><tr><td>fixed \(Q_0\) leakage at \(t=200\)</td><td>\(1.94966\times10^{{11}}\)</td></tr></tbody></table><p>15 组 binary64 数据和独立程序重算全部通过；最大代数残差为 \(6.2430\times10^{{-14}}\)。它们只承担 finite diagnostic 与附图，不证明 continuum 谱、连续时间界或非自治传递。</p></section>
        <section id="literature"><div class="section-no">10 / Literature boundary</div><h2>一般谱持续、半群判据和非自治理论只作为边界</h2><p><a href="https://doi.org/10.1016/j.anihpc.2007.05.004">Shvydkoy--Friedlander</a>是无黏到黏性不稳定谱持续的一般先例；本节不把其投影拓扑写成未明确陈述的 operator norm。<a href="https://doi.org/10.1007/978-3-642-66282-9">Kato 的分离谱框架</a>与<a href="https://doi.org/10.1143/JPSJ.5.435">Kato 1950 adiabatic theorem</a>分开使用；<a href="https://doi.org/10.1142/S0129055X19500144">Schmid 的 time-independent-domain 定理</a>及其<a href="https://arxiv.org/abs/1804.11255">time-dependent-domain 预印本</a>也单独核对。<a href="https://doi.org/10.1090/S0002-9947-1978-0461206-1">Gearhart</a>与<a href="https://doi.org/10.1090/S0002-9947-1984-0743749-9">Prüss</a>说明需要完整竖线 resolvent。<a href="https://doi.org/10.1016/j.jde.2020.06.046">Grenier--Nguyen</a>在不同几何和范数中给出统一半群先例。<a href="https://doi.org/10.1006/jdeq.1999.3668">Latushkin--Schnaubelt</a>与<a href="https://doi.org/10.1016/j.na.2008.11.009">Popescu</a>的 evolution-family 条件没有被自动移植到移动剖面。这里不作原创性或优先权声明。</p></section>
        <section id="figure"><div class="section-no">11 / Journal figure</div><h2>谱、resolvent、semigroup 与固定投影泄漏分面归档</h2><p><img src="/assets/r073e/{FIGURE_ID}.svg" alt="R0.73E finite complement and transfer diagnostic"></p><p><a href="/assets/r073e/{FIGURE_ID}.pdf">下载 PDF</a> · <a href="/assets/r073e/{FIGURE_ID}.png">下载 600 dpi PNG</a> · <a href="/assets/r073e/{FIGURE_ID}.svg">打开 SVG</a></p></section>
        <section id="boundary"><div class="section-no">12 / Exact boundary</div><h2>九项 CLOSED 与所有 OPEN 接口保持分离</h2><p>{CLOSED}。</p><p>{OPEN}。</p></section>
        <section id="value"><div class="section-no">13 / Research value</div><h2>一条线性 Fourier 行上的多项式上界障碍已从条件命题升级为定理</h2><p>R0.73E 把局部谱簇持续、完整正半平面控制、相对二分和缓慢漂移连接成闭合证明链。它对识别高频线性增长机制有实质价值，但对 Clay 问题的直接价值仍有限：没有非线性频率耦合、能量闭合、延拓准则或奇性构造。</p></section>
        <section id="next"><div class="section-no">14 / Next gate</div><h2>R0.73F：固定小物理窗口上的 moving-profile top bundle</h2><p>下一节将证明或否证 moving-profile top bundle 的统一谱隙与演化二分，目标是把 logarithmic fast-time lower bound 升级为 fixed-window \(e^{{c|\Lambda|}}\)。graph-domain/Kato transport 只是候选方法，当前仍为 OPEN。</p></section>
        <section id="reproduce"><div class="section-no">15 / Reproduction</div><h2>报告、证明、审计、文献、证书、实验和正式附图都给出直接入口</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073e_report-source.md">完整报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073e_halfplane_transfer_proof.md">解析证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073e_independent_analytic_audit.md">独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073e_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073e_gap_matrix.md">缺口矩阵</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073e">正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073e">有限实验与监控</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073e/{FIGURE_ID}">正式附图包</a> · <a href="/notes/r0-73e.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73e.html">121 节累计回顾</a> · <a href="/recap-r0-61-r0-73e.pdf">累计回顾 PDF</a></p></section>
      </article>'''

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73F</span><span class="tree-state current">下一检查点</span></div>
              <h3>固定小物理窗口上的 moving-profile top bundle</h3><p>证明或否证统一谱隙与演化二分，目标是把 logarithmic fast-time lower bound 升级为 fixed-window \(e^{c|\Lambda|}\)。graph-domain/Kato transport 仍只是候选方法。</p>
            </article>'''

HOME_E_CARD = rf'''          <div class="task-one" id="r073e" data-release="r073e" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73E · 2026-08-30</p><h3>固定正半平面分裂与对数快时间传递</h3>
            <p>每个固定正半平面中的黏性谱都由持续的无黏谱簇捕获。选取完整 top cluster 后，相对 semigroup dichotomy 与固定生成元 Volterra 传递闭合。</p>
            <p>因此，必须覆盖这条精确 Fourier 行的任意固定次数多项式上界都失效。结论仍不是 fixed-window \(e^{{c|\Lambda|}}\) 律、完整 OS--Squire 结论、非线性估计或 Clay 解答。</p>
            <p><strong>结论边界：</strong>&nbsp;{CLOSED}；{OPEN}。</p>
            <p><a href="/notes/r0-73e.html"><strong>阅读 R0.73E 研究笔记 →</strong></a><br><a href="/notes/r0-73e.pdf">下载同步 PDF</a> · <a href="/assets/r073e/{FIGURE_ID}.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073e">查看正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073e_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73e.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73F：</strong>&nbsp;证明或否证固定小物理窗口上的 moving-profile top bundle 统一谱隙与演化二分。</p>
          </div>'''

HOME_LATEST_SPOTLIGHT = r'''    <section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">
      <div class="route-overview-inner"><header class="route-map-header">
        <div><p class="eyebrow">LATEST RELEASE · R0.73E · 2026-08-30</p><h2 class="route-map-title" id="latest-release-title">固定正半平面分裂与对数快时间传递</h2><p class="route-map-intro">九项一条精确线性行的结论已闭合。固定小物理窗口指数律、移动谱束、完整 OS--Squire、非线性与 Clay 仍为 OPEN。</p></div>
        <nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-73e.pdf">阅读最新 R0.73E 研究笔记 →</a><a href="/recap-r0-61-r0-73e.html">121 节累计回顾</a><a href="/notes/">181 篇研究笔记总索引</a><a href="#r073e">查看首页完整 R0.73E 卡片</a></nav>
      </header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73E · 83 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>59 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73E</span></div></div>
    </section>'''
