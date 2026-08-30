#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reader-facing source fragments for the fail-closed R0.73H release."""

FIGURE_ID = "fig-r073h-harmonic-feedback"
FIGURE_RELATIVE = f"figures/r073h/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r073h"

R073G_RELEASE_BASELINE = {
    "latestCompletedRelease": "r073g",
    "siteVersion": "1.47",
    "publicHtmlNoteCount": 183,
    "postR060RecapNodeCount": 123,
    "nextRelease": "r073h",
    "latestReleaseGate": "tests/r073g-nonlinear-bootstrap-gate.test.mjs",
    "latestReleasePublicationTest": "tests/r073g-release.test.mjs",
    "postR070APublishedReleaseCount": 85,
    "postR070AFormalSealedReleaseCount": 61,
    "legacyFormalFigureBacklogCount": 24,
}

R073H_RELEASE_TARGET = {
    "latestCompletedRelease": "r073h",
    "siteVersion": "1.48",
    "publicHtmlNoteCount": 184,
    "postR060RecapNodeCount": 124,
    "nextRelease": "r073i",
    "postR070APublishedReleaseCount": 86,
    "postR070AFormalSealedReleaseCount": 62,
    "legacyFormalFigureBacklogCount": 24,
}

CLOSED = (
    "exactHarmonicTaylorHierarchy=CLOSED；"
    "targetHasNoQuadraticOrQuarticTerm=CLOSED；"
    "continuumDoubledRowNumericalAbscissa=CLOSED；"
    "localizedLinearCumulativeEnergy=CLOSED；"
    "localizedQuadraticCubicEnergy=CLOSED；"
    "fourthOrderExactRemainder=CLOSED；"
    "gainNormalizedFixedDistanceDeparture=CLOSED；"
    "selectedOrbitGlobalSmoothness=CLOSED"
)

FALSE = (
    "gainLowerBoundDeterminesActualGain=FALSE_AS_INFERENCE；"
    "gainNormalizedDepartureImpliesPrescribedSeedDeparture=FALSE_AS_INFERENCE；"
    "finiteCubicCoefficientProvesContinuumSaturation=FALSE_AS_INFERENCE；"
    "familyDepartureIsSingleBackgroundLyapunovInstability=FALSE_AS_INFERENCE；"
    "planarDepartureCreatesThreeDimensionalVortexStretching=FALSE；"
    "planarDepartureImpliesFiniteTimeSingularity=FALSE；"
    "planarDepartureResolvesClay=FALSE"
)

OPEN = (
    "sharpSelectedGainAction=OPEN；"
    "prescribedLowerLawSeedDeparture=OPEN；"
    "uniformTaylorRadiusAtNaturalEndpoint=OPEN；"
    "fullContinuumHarmonicResolvedSemigroupEstimate=OPEN；"
    "singleBackgroundLyapunovSequence=OPEN；"
    "transverseOSSquireEvolution=OPEN；"
    "transverseTriadClosure=OPEN；"
    "finiteTimeSingularity=OPEN；Clay=OPEN"
)

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73H · GAIN-NORMALIZED DEPARTURE · HARMONIC ENERGY</div>
        <h1>按实际增益归一化的<br>平面固定距离偏离</h1>
        <p class="lead">R0.73H 在精确平面 Navier--Stokes 子系统内解析控制线性、二次、三次系数与四阶余项。以实际选定增益 \(G_\Lambda\) 归一化的初态 \(\delta\phi_\Lambda/G_\Lambda\) 在固定端点留下至少 \(\delta/2\) 的目标行幅度，而初始 \(H^3\) 范数趋于零。结论属于随 \(\Lambda\) 变化的背景族；预设下界指数种子、固定背景 Lyapunov 不稳定、横向三维、奇性与 Clay 均未由此得到。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73H 完成</span><strong>Gain-normalized</strong><p>版本 v0.73H · 2026-08-30</p><p>CONTINUUM THEOREM</p><p>8 项结论：CLOSED</p><p>7 个推断：FALSE</p><p>3D / CLAY：OPEN</p><p>NOT CLAY</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>固定距离偏离已对实际增益归一化种子闭合</h2><div class="verdict-grid"><div class="verdict-card true"><strong>CLOSED · FIXED DISTANCE</strong><p>对固定足够小的 \(\delta>0\)，目标行在 \(d=D\) 的范数至少为 \(\delta/2\)。</p></div><div class="verdict-card true"><strong>CLOSED · HARMONIC ENERGY</strong><p>二次、三次系数与四阶精确余项具有对大 \(\Lambda\) 一致的局部化估计。</p></div><div class="verdict-card true"><strong>CLOSED · PLANAR SMOOTHNESS</strong><p>所选轨道处在二维不变子空间内，因而全局光滑。</p></div><div class="verdict-card false"><strong>OPEN · MATCHING ACTION / 3D</strong><p>实际增益的匹配作用量、横向三维耦合与 Clay 仍未闭合。</p></div></div></section>
        <section id="theorem"><div class="section-no">01 / Main theorem</div><h2>初态趋零，目标行在固定端点保持固定距离</h2><div class="equation result">\[G_\Lambda=\|S_{1,\Lambda}(D,0)\phi_\Lambda\|_2,\qquad u_\Lambda^\delta(0)=\frac{\delta}{G_\Lambda}\phi_\Lambda.\]</div><div class="equation result">\[\|\Pi_{\{K_z=\pm1\}}u_\Lambda^\delta(D)\|_2\ge\frac\delta2,\qquad \|u_\Lambda^\delta(0)\|_{H^3}\le C\delta\Lambda^2e^{-r\Lambda D}\to0.\]</div><p>这里 \(r>0.17035\)，\(D=\min\{d_0,1/450\}\)，物理时间为 \(T=D/4\)。背景和初态都依赖 \(\Lambda\)。</p></section>
        <section id="normalization"><div class="section-no">02 / Exact normalization</div><h2>实际增益与下界指数不能互换</h2><div class="equation result">\[a(s)=G_\Lambda^{-1}S_{1,\Lambda}(s,0)\phi_\Lambda,\qquad \|a(s)\|_2\le K_{\rm F}e^{-r\Lambda(D-s)},\quad\|a(D)\|_2=1.\]</div><p>这是端点归一化轨道的反向局部化，不是把算子范数下界倒过来使用。现有证明不提供 \(G_\Lambda\) 的匹配上界，因此不能把种子改写成预设的 \(\delta e^{-r\Lambda D}\phi_\Lambda\)。</p></section>
        <section id="hierarchy"><div class="section-no">03 / Harmonic hierarchy</div><h2>偶次离开目标行，奇次可以返回</h2><div class="equation result">\[a:\ \pm1,\qquad b:\ 0,\pm2,\qquad c:\ \pm1,\pm3.\]</div><p>正目标行的三次回馈包含 \((1,0),(0,1),(-1,2),(2,-1)\) 4 条有序路径及其共轭。选择律说明目标行没有二次项和四次项；三次之后的下一项至少是五次。</p></section>
        <section id="leray"><div class="section-no">04 / Exact Leray algebra</div><h2>一维公式由物理 Fourier--Leray 投影直接推出</h2><div class="equation result">\[\mathbf u_q[f]=\left(0,f,\frac{2i}{q}Df\right)e^{iqz},\qquad \mathbb PF_q=\mathbf u_q\!\left[(q^2-4D^2)^{-1}(q^2A+2iqDC)\right].\]</div><p>倍频、零频、目标回馈与三倍频公式逐路复算。generic convolution kernel 和独立 alias-free FFT 只核对有限代数与代码路径，不承担连续谱尾部证明。</p></section>
        <section id="abscissa"><div class="section-no">05 / Continuum doubled-row bound</div><h2>倍频行的数值横坐标严格低于局部化速率门</h2><div class="equation result">\[\omega_1(d)\le\frac13,\qquad0\le d\le D.\]</div><p>2 符号规范变换把问题化为 \(H_d=-\partial_x^2+1-\tfrac94W_x(d)^2\) 的正性。\(d=0\) 的精确 9 维有理数块、解析尾与交叉块给出 \(H_0\ge1/20\)；显式时间扰动再给 \(H_d\ge1/40\)。有限有理数块只是连续证明中的精确子证书。</p></section>
        <section id="localization"><div class="section-no">06 / Localized energies</div><h2>Stieltjes 局部化把累计耗散传到二次和三次层</h2><div class="equation result">\[Y_a+M_a\lesssim e^{-2r\Lambda(D-s)},\quad Y_b+M_b\lesssim e^{-4r\Lambda(D-s)},\quad Y_c+M_c\lesssim e^{-6r\Lambda(D-s)}.\]</div><p>严格速率门是 \(1/3<2r\)、\(1/2<3r\)、\(1/2<4r\)。证明使用二维 Ladyzhenskaya 不等式和累计耗散测度，不假设对 \(\Lambda\) 一致的高阶 Sobolev 传播。</p></section>
        <section id="remainder"><div class="section-no">07 / Fourth-order remainder</div><h2>精确方程与三阶近似之间的误差为四阶</h2><div class="equation result">\[u_{\rm app}=\delta a+\delta^2b+\delta^3c,\qquad \|u_\Lambda^\delta(D)-u_{\rm app}(D)\|_2\le C\delta^4.\]</div><p>余项从四次阶开始。输运抵消、4 至 6 次乘积测度和额外的梯度积分因子共同闭合能量估计。</p></section>
        <section id="endpoint"><div class="section-no">08 / Endpoint</div><h2>三次修正与四阶误差不能抹去线性端点</h2><div class="equation result">\[\|\Pi_{\pm1}u_\Lambda^\delta(D)\|_2\ge\delta-C_3\delta^3-C_R\delta^4\ge\frac\delta2.\]</div><p>先固定与 \(\Lambda\) 无关的足够小 \(\delta\)，再取足够大的 \(\Lambda\)。这给出背景族层面的固定距离偏离，不是单一背景上的 Lyapunov 不稳定。</p></section>
        <section id="finite"><div class="section-no">09 / Finite diagnostic boundary</div><h2>有限计算复核谐波代码，不证明连续定理</h2><p>正式包含 319 个主记录、21 个 cutoff 比较、6 个步长比较、4 个预注册独立哨兵和 1 个独立 holdout。独立系数最大相对误差为 \(2.0164\times10^{-9}\)；holdout 的二次与目标三次补偿比分别为 \(0.9250135\) 和 \(0.8849248\)，有符号总三次回馈为 \(-0.6597415\)。这些响应均取 \(d=0.01>1/450\)，严格位于定理区间之外，只能作为冻结网格诊断。</p></section>
        <section id="certificate"><div class="section-no">10 / Exact certificate</div><h2>精确算术与浮点诊断分开封存</h2><p>9 个有理数 \(LDL^*\) pivot、Bareiss 主子式、解析尾常数、Schur 行列式和速率余量由 2 套独立精确脚本复算。浮点部分另行保存原始复系数、进度日志、配置、环境、校验和与独立验证。6 个步长端点没有进入 NPZ，因此独立审计只验证锁定 producer、CSV 内部最大值、阈值和包哈希；该限制保留在证书中。</p></section>
        <section id="literature"><div class="section-no">11 / Literature boundary</div><h2>既有不稳定与阈值工作提供方法坐标，不替代本节证明</h2><p><a href="https://arxiv.org/abs/math/0508173">Friedlander--Pavlović--Shvydkoy</a>给出谱增长到非线性不稳定的经典框架；<a href="https://arxiv.org/abs/2206.01318">Bian--Grenier</a>讨论边界层中的三次相互作用；<a href="https://arxiv.org/abs/1707.00278">Lin--Xu</a>、<a href="https://arxiv.org/abs/2306.03555">Li--Zhao</a>和<a href="https://arxiv.org/abs/2410.23798">Li--Zhao</a>研究无外力或黏性驱动的剪切流机制。几何、谱假设与结论均不同；这里只作有界文献碰撞检查，不作首创或优先权声明。</p></section>
        <section id="audit"><div class="section-no">12 / Independent audit</div><h2>归一化、规范正性、谐波代数与四阶余项通过独立复核</h2><p>独立解析审计结论为 MATHEMATICAL FINAL PASS。敌对审计逐项检查错误的下界反演、缩放因子、漏失路径、有限维外推与三维外推，未留下数学修正义务。</p></section>
        <section id="figure"><div class="section-no">13 / Journal figure</div><h2>谐波缩放、回馈分解与数值核验归档</h2><p><img src="/assets/r073h/__FIGURE_ID__.svg" alt="R0.73H finite harmonic-response diagnostic"></p><p><a href="/assets/r073h/__FIGURE_ID__.pdf">下载 PDF</a> · <a href="/assets/r073h/__FIGURE_ID__.png">下载 600 dpi PNG</a> · <a href="/assets/r073h/__FIGURE_ID__.svg">打开 SVG</a></p></section>
        <section id="boundary"><div class="section-no">14 / Exact boundary</div><h2>CLOSED、FALSE 与 OPEN 继续分列</h2><p>__CLOSED__。</p><p>__FALSE__。</p><p>__OPEN__。</p><p>其中 <code>uniformTaylorRadiusAtNaturalEndpoint</code> 专指按下界指数预设种子的全阶 Taylor 半径，不指本节已经闭合的 gain-normalized 三阶近似与四阶直接余项。</p></section>
        <section id="value"><div class="section-no">15 / Research value</div><h2>过小种子的相对增益被推进为趋零初态的固定距离偏离</h2><p>R0.73G 只保留相对放大；R0.73H 借助实际增益归一化和谐波能量局部化，使初始 \(H^3\) 范数趋零而端点目标行保持固定距离。代价是种子由未知的实际增益定义，背景也随参数变化。它是严格的非线性进展，但离固定背景三维正则性问题仍有结构性距离。</p></section>
        <section id="next"><div class="section-no">16 / Next gate</div><h2>R0.73I：选定增益的匹配作用量</h2><p>下一节优先给 \(G_\Lambda\) 建立匹配上、下作用量，判断 \(\delta/G_\Lambda\) 能否改写为可预设的显式指数尺度。完成该门之前，不把 gain-normalized theorem 称为自然尺度阈值。</p></section>
        <section id="reproduce"><div class="section-no">17 / Reproduction</div><h2>证明、审计、证书、词典与附图均提供直接入口</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073h_report-source.md">完整报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073h_harmonic_energy_proof.md">主证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073h_harmonic_derivation.md">谐波推导</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073h_independent_analytic_audit.md">独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073h_adversarial_audit.md">敌对审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073h_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073h_bilingual_dictionary.md">双语词典</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073h">正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073h/__FIGURE_ID__">正式附图包</a> · <a href="/notes/r0-73h.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73h.html">124 节累计回顾</a> · <a href="/recap-r0-61-r0-73h.pdf">累计回顾 PDF</a></p></section>
      </article>'''
NOTE_ARTICLE = (
    NOTE_ARTICLE.replace("__FIGURE_ID__", FIGURE_ID)
    .replace("__CLOSED__", CLOSED)
    .replace("__FALSE__", FALSE)
    .replace("__OPEN__", OPEN)
)

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73I</span><span class="tree-state current">下一检查点</span></div>
              <h3>选定增益的匹配作用量</h3><p>为 \(G_\Lambda\) 建立匹配上、下界，判断按实际增益归一化的种子能否换成可预设的显式指数尺度。</p>
            </article>'''

HOME_H_CARD = r'''          <div class="task-one" id="r073h" data-release="r073h" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73H · 2026-08-30</p><h3>按实际增益归一化的平面固定距离偏离</h3>
            <p>精确谐波选择律、倍频行连续数值横坐标界、Stieltjes 能量局部化与四阶余项控制，把 R0.73G 的相对放大推进为趋零初态的固定距离端点。</p>
            <p>种子是 \(\delta\phi_\Lambda/G_\Lambda\)，不是预设的 \(\delta e^{-r\Lambda D}\phi_\Lambda\)。背景随 \(\Lambda\) 变化，轨道仍处于全局光滑二维子空间；横向三维、奇性与 Clay 保持 OPEN。</p>
            <p><strong>闭合结论：</strong>&nbsp;__CLOSED__。</p><p><strong>否定推断：</strong>&nbsp;__FALSE__。</p><p><strong>开放边界：</strong>&nbsp;__OPEN__。</p><p><code>uniformTaylorRadiusAtNaturalEndpoint</code> 专指按下界指数预设种子的全阶 Taylor 半径，不指本节已经闭合的 gain-normalized 四阶直接余项。</p>
            <p><a href="/notes/r0-73h.html"><strong>阅读 R0.73H 研究笔记 →</strong></a><br><a href="/notes/r0-73h.pdf">下载同步 PDF</a> · <a href="/assets/r073h/__FIGURE_ID__.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073h">查看正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073h_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73h.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73I：</strong>&nbsp;建立选定增益 \(G_\Lambda\) 的匹配作用量。</p>
          </div>'''
HOME_H_CARD = (
    HOME_H_CARD.replace("__FIGURE_ID__", FIGURE_ID)
    .replace("__CLOSED__", CLOSED)
    .replace("__FALSE__", FALSE)
    .replace("__OPEN__", OPEN)
)

HOME_LATEST_SPOTLIGHT = r'''    <section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">
      <div class="route-overview-inner"><header class="route-map-header">
        <div><p class="eyebrow">LATEST RELEASE · R0.73H · 2026-08-30</p><h2 class="route-map-title" id="latest-release-title">按实际增益归一化的平面固定距离偏离</h2><p class="route-map-intro">8 项解析结论已经闭合。有限诊断与连续定理分开封存；预设指数种子、固定背景、横向三维、奇性与 Clay 保持 OPEN。</p></div>
        <nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-73h.pdf">阅读最新 R0.73H 研究笔记 →</a><a href="/recap-r0-61-r0-73h.html">124 节累计回顾</a><a href="/notes/">184 篇研究笔记总索引</a><a href="#r073h">查看首页完整 R0.73H 卡片</a></nav>
      </header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73H · 86 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>62 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73H</span></div></div>
    </section>'''
