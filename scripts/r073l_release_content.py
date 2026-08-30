#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reader-facing fragments for the fail-closed R0.73L release."""

FIGURE_ID = "fig-r073l-adiabatic-tracking"
FIGURE_RELATIVE = f"figures/r073l/{FIGURE_ID}"

R073K_BASELINE = {
    "latestCompletedRelease": "r073k", "siteVersion": "1.51",
    "publicHtmlNoteCount": 187, "postR060RecapNodeCount": 127,
    "nextRelease": "r073l", "postR070APublishedReleaseCount": 89,
    "postR070AFormalSealedReleaseCount": 65,
    "legacyFormalFigureBacklogCount": 24,
}

R073L_TARGET = {
    "latestCompletedRelease": "r073l", "siteVersion": "1.52",
    "publicHtmlNoteCount": 188, "postR060RecapNodeCount": 128,
    "nextRelease": "r073m", "postR070APublishedReleaseCount": 90,
    "postR070AFormalSealedReleaseCount": 66,
    "legacyFormalFigureBacklogCount": 24,
}

CLOSED = (
    "commonDomainEvolution=CLOSED；"
    "katoIntertwining=CLOSED；"
    "movingComplementRelativeStability=CLOSED；"
    "nonselfadjointAdiabaticTracking=CLOSED；"
    "matchingSelectedGainAction=CLOSED；"
    "actionResolvedBackwardLocalization=CLOSED"
)

FINITE = (
    "finiteDiagnosticPackage=CLOSED；primaryAdiabaticCases=15；"
    "independentFiniteReconstruction=PASS；formalFigurePackage=PASS；"
    "finiteDimensionDoesNotCertifyContinuum=TRUE"
)

OPEN = (
    "explicitAdiabaticThreshold=OPEN；prefactorLimit=OPEN；twoTermWKB=OPEN；"
    "nonlinearNavierStokes=OPEN；transverseThreeDimensionalClosure=OPEN；"
    "finiteTimeSingularity=OPEN；Clay=OPEN"
)

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73L · NONSELFADJOINT ADIABATIC TRACKING</div>
        <h1>非自伴绝热跟踪与匹配增长作用量</h1>
        <p class="lead">R0.73L 在 R0.73K 的一致 rank-one 黏性谱支上证明真实非自治演化的长时间跟踪。对 \(0<\varepsilon\le\varepsilon_L\) 与完整慢窗 \(0\le D\le1/450\)，从 selected line 出发的精确增益与 \(\exp(\varepsilon^{-1}\int_0^D\lambda_0)\) 只差一个与 \(\varepsilon\) 无关的两侧乘法常数；精确轨道相对 Kato selected orbit 的误差为 \(O(\varepsilon)\)。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73L 完成</span><strong>Continuum theorem + independent audits</strong><p>版本 v0.73L · 2026-08-31</p><p>解析门：L1–L8 CLOSED</p><p>有限主案例：15</p><p>独立有限重算：PASS</p><p>正式附图：PASS</p><p>NONLINEAR / 3D / CLAY：OPEN</p><p>NOT CLAY</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct result</div><h2>真实非自治增益与 selected action 匹配</h2><div class="equation result">\[c_Le^{\Phi_\varepsilon(D,0)}\le\|U_\varepsilon(D,0)h_\varepsilon(0)\|\le C_Le^{\Phi_\varepsilon(D,0)},\qquad \Phi_\varepsilon(D,0)=\varepsilon^{-1}\int_0^D\lambda_\varepsilon(r)\,dr.\]</div><p>存在 \(0<\varepsilon_L\le\varepsilon_K\) 和与 \(\varepsilon,D\) 无关的 \(0<c_L\le C_L<\infty\)，使结论对完整 \(D\in[0,1/450]\) 同时成立。R0.73K 的 \(|\lambda_\varepsilon-\lambda_0|\le C_\lambda\varepsilon\) 允许把黏性 action 换成无黏 action，只改变固定乘法常数。</p></section>
        <section id="obstruction"><div class="section-no">01 / Nonnormal obstruction</div><h2>瞬时不稳定谱并不自动给出动态增长</h2><p>Jordan nilpotent、移动投影条件数和补空间 switching growth 都可能制造无界 prefactor。证明没有把瞬时特征值直接积分后忽略余项，而是使用 rank-one 半单性、一致投影条件数、冻结补空间余隙和慢漂移。</p></section>
        <section id="kato"><div class="section-no">02 / Kato transport</div><h2>正确的 commutator 精确移动谱纤维</h2><div class="equation result">\[\mathcal K_\varepsilon=[P_\varepsilon',P_\varepsilon],\qquad P(d)U^{\rm a}(d,s)=U^{\rm a}(d,s)P(s).\]</div><p>由 \([P,\mathcal K]=-P'\) 得到 exact intertwining。修正演化使用正的 \(+\mathcal K\)；精确演化相对修正演化的 Duhamel 项带负号。固定 \(\varepsilon\) 时投影关于 \(d\) 实解析，因此 \(\mathcal K\) 范数连续；统一估计只使用其范数界，不要求统一 \(P''\)。</p></section>
        <section id="block"><div class="section-no">03 / Fixed fast block</div><h2>一个固定快时间块把冻结余隙变成移动补空间收缩</h2><p>选 \(T\) 使 \(C_Ke^{-(0.16-0.12)T}\le1/4\)。在 \(d=s+\varepsilon\tau\)、\(0\le\tau\le T\) 上，生成元漂移与 Kato 修正合计为 \(O(\varepsilon)\) 的有界扰动。Duhamel 误差趋于零后，每个完整块相对 selected action 至多乘 \(1/2\)。</p><div class="equation result">\[\|U_Q^{\rm a}(d,s)\|\le M_Qe^{\Phi_\varepsilon(d,s)}e^{-\gamma_Q(d-s)/\varepsilon}.\]</div></section>
        <section id="volterra"><div class="section-no">04 / Forward Volterra</div><h2>相对衰减核只有 \(O(\varepsilon)\) 的有效积分长度</h2><p>在 \(p=P(d)u(d)\)、\(q=Q(d)u(d)\) 分解下，Kato commutator 只产生 off-diagonal 耦合。纯前向 Volterra 估计先给出 \(q=O(\varepsilon)p\)，再吸收到 selected coordinate，得到统一上界和正下界。非正交下界使用 \(\|Pu\|\le\|P\|\|u\|\)，不使用虚假的 Pythagorean identity。</p></section>
        <section id="tracking"><div class="section-no">05 / Vector tracking</div><h2>精确终点只要求相对靠近，不要求恰在瞬时谱线上</h2><div class="equation result">\[\|U_\varepsilon(D,0)h-U_{\varepsilon,P}^{\rm a}(D,0)h\|\le C_L\varepsilon e^{\Phi_\varepsilon(D,0)}.\]</div><p>真实终点相对移动 selected line 为 \(O(\varepsilon)\)。本节不声称精确轨道在每一时刻都属于 \(P_\varepsilon(d)H\)。</p></section>
        <section id="localization"><div class="section-no">06 / Forward-orbit localization</div><h2>后向定位由同一条前向轨道的两个时刻相除得到</h2><div class="equation result">\[\frac{\|U_\varepsilon(s,0)h\|}{\|U_\varepsilon(D,0)h\|}\le C_L\exp\!\left[-\varepsilon^{-1}\int_s^D\lambda_0(r)\,dr\right].\]</div><p>这里没有反向求解 parabolic complement，也没有从任意 terminal eigenvector 反推初值。</p></section>
        <section id="audits"><div class="section-no">07 / Independent audits</div><h2>逐行解析审计与反例导向审计均为 PASS</h2><p>解析审计修正了一个块估计中的 \(\|Q\|\) 因子和 lower absorption 中的 \(M_W^3\) 次数，并核对 common-domain evolution、commutator 符号、Duhamel 符号、fiber chaining 和 action transfer。对抗审计尝试引入 Jordan 块、竞争谱支、switching growth、投影退化、非法 backward evolution、图范数爆炸与非正交抵消；没有反例能同时保留全部封存假设。</p></section>
        <section id="diagnostic"><div class="section-no">08 / Finite diagnostic</div><h2>15 条主轨迹由第二种积分器独立重算</h2><p>有限诊断使用 \(N=32,48,64\)、五个 \(\varepsilon\) 水平、65 个慢时间节点和完整慢窗。\(N=64\) 的 terminal action-normalized gain 位于 \([0.9993290525,0.9998284900]\)，三小参数的 terminal leakage slope 为 \(1.0281276\)，最大 forward-orbit localization residual 为 \(6.711726\times10^{-4}\)。</p><p>\(N=48\) 与 \(N=64\) 的 terminal 差在 \(10^{-15}\) 量级；独立 midpoint matrix-exponential 重算与主 DOP853 输出的最大差在 \(10^{-9}\) 量级。所有冻结容差通过，但这些数值不承担连续证明权重。</p></section>
        <section id="figure"><div class="section-no">09 / Journal figure</div><h2>增益、泄漏、定位余差与验证裕度按期刊格式归档</h2><p><img src="/assets/r073l/__FIGURE_ID__.svg" alt="R0.73L finite adiabatic tracking diagnostic"></p><p><a href="/assets/r073l/__FIGURE_ID__.pdf">下载矢量 PDF</a> · <a href="/assets/r073l/__FIGURE_ID__.png">下载 600 dpi PNG</a> · <a href="/assets/r073l/__FIGURE_ID__.svg">打开 SVG</a></p></section>
        <section id="literature"><div class="section-no">10 / Deep Research boundary</div><h2>现成绝热定理提供结构先例，但不能直接给出这里的双参数统一常数</h2><p>Schmid 的共同定义域结果要求 Kato stability 和更高阶投影正则性；Abou Salem–Fröhlich 的 quasi-bounded 版本会产生不适合当前长时间增长支的指数因子；Joye 的理论说明非平凡 nilpotent block 可产生次指数 prefactor。R0.73L 因而保留模型限定的固定块证明，不声称首个一般非自伴绝热定理，也不作穷尽性、原创性或优先权声明。</p></section>
        <section id="boundary"><div class="section-no">11 / Exact boundary</div><h2>连续定理、有限诊断和开放问题分开列示</h2><p>__CLOSED__。</p><p>__FINITE__。</p><p>__OPEN__。</p><p>本节没有显式 \(\varepsilon_L\)，没有 prefactor 极限或两项 WKB 展开，也没有二维非线性、横向三维、有限时间奇性或 Clay 闭合。NOT CLAY。</p></section>
        <section id="value"><div class="section-no">12 / Research value</div><h2>冻结谱信息已经升级为真实长时间非自治增长</h2><p>这一结果排除了“瞬时不稳定不等于可实现动态增长”的关键逻辑缺口，具备进一步整理为谱动力学或非自伴绝热演化稿件的潜力。它仍只是二维线性中间定理，不能换算成 Clay 问题完成比例。</p></section>
        <section id="next"><div class="section-no">13 / Next gate</div><h2>R0.73M：绝热尺度上的二维非线性离轨 bootstrap</h2><p>下一节冻结扰动方程、linear seed 幅度、退出时间和非线性余项范数，目标是在 selected gain 达到预定阈值前证明二次 Duhamel 项严格小于线性主项。若显式不等式无法闭合，就保留在线性定理，不能以数值离轨代替证明。</p></section>
        <section id="reproduce"><div class="section-no">14 / Reproduction</div><h2>证明、审计、文献、实验和附图均有直接入口</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073l_adiabatic_tracking_proof.md">解析证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073l_independent_analytic_audit.md">独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073l_adversarial_audit.md">对抗审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073l_literature_audit.md">Deep Research 文献审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073l">有限诊断包</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073l/__FIGURE_ID__">正式附图包</a> · <a href="/notes/r0-73l.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73l.html">128 节累计回顾</a> · <a href="/recap-r0-61-r0-73l.pdf">累计回顾 PDF</a></p></section>
      </article>'''
NOTE_ARTICLE = (NOTE_ARTICLE.replace("__FIGURE_ID__", FIGURE_ID)
                .replace("__CLOSED__", CLOSED)
                .replace("__FINITE__", FINITE)
                .replace("__OPEN__", OPEN))

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73M</span><span class="tree-state current">下一检查点</span></div>
              <h3>绝热尺度上的二维非线性离轨 bootstrap</h3><p>冻结 linear seed、退出时间与二次 Duhamel 余项，检查非线性误差能否在 selected action 达到阈值前被严格吸收。</p>
            </article>'''

HOME_L_CARD = r'''          <div class="task-one" id="r073l" data-release="r073l" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73L · 2026-08-31</p><h3>非自伴绝热跟踪与匹配增长作用量</h3>
            <p>共同定义域上的 Kato transport、固定快时间块和移动补空间相对衰减已经闭合。真实 selected orbit 在完整 \(D\in[0,1/450]\) 上取得与 \(\exp(\varepsilon^{-1}\int_0^D\lambda_0)\) 匹配的两侧增益，乘法常数不随 \(\varepsilon\downarrow0\) 发散。</p>
            <p>精确轨道相对 Kato selected orbit 的误差为 \(O(\varepsilon)\)。action-resolved localization 由同一条前向轨道相除得到，不使用 backward parabolic evolution。</p>
            <p><strong>有限诊断：</strong>15 条主轨迹、5 条独立重算、346 行附图源数据和正式四联图全部通过；它们不承担连续定理证明权重。</p>
            <p><strong>开放边界：</strong>&nbsp;__OPEN__。NOT CLAY。</p>
            <p><a href="/notes/r0-73l.html"><strong>阅读 R0.73L 研究笔记 →</strong></a><br><a href="/notes/r0-73l.pdf">下载同步 PDF</a> · <a href="/assets/r073l/__FIGURE_ID__.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073l">查看有限诊断包</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073l_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73l.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73M：</strong>&nbsp;建立二维非线性离轨 bootstrap；若二次余项不能被吸收，就停在线性定理。</p>
          </div>'''
HOME_L_CARD = HOME_L_CARD.replace("__FIGURE_ID__", FIGURE_ID).replace("__OPEN__", OPEN)

HOME_LATEST_SPOTLIGHT = r'''    <section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">
      <div class="route-overview-inner"><header class="route-map-header">
        <div><p class="eyebrow">LATEST RELEASE · R0.73L · 2026-08-31</p><h2 class="route-map-title" id="latest-release-title">非自伴绝热跟踪与匹配增长作用量</h2><p class="route-map-intro">R0.73K 的冻结 rank-one 黏性谱支已经升级为真实长时间非自治增长：Kato intertwining、固定快时间块、移动补空间相对衰减、前向 Volterra 吸收、两侧 bounded prefactor、无黏 action 转移和 forward-orbit localization 均已闭合。独立解析审计、对抗审计、有限重算和正式图件分别通过；非线性、三维、奇性与 Clay 继续 OPEN。</p></div>
        <nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-73l.pdf">阅读最新 R0.73L 研究笔记 →</a><a href="/recap-r0-61-r0-73l.html">128 节累计回顾</a><a href="/notes/">188 篇研究笔记总索引</a><a href="#r073l">查看首页完整 R0.73L 卡片</a></nav>
      </header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73L · 90 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>66 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73L</span></div></div>
    </section>'''

RECAP_PHASE = r'''            <article class="phase"><h3>R0.73L · Parameter-uniform nonselfadjoint adiabatic tracking</h3><p>在共同定义域上加入 \([P_\varepsilon',P_\varepsilon]\) 后，Kato 演化精确移动 rank-one selected line 与补空间。固定快时间块把 R0.73K 的冻结余隙升级为移动补空间相对指数衰减；前向 Volterra 吸收进一步给出 \(q=O(\varepsilon)p\) 和 selected gain 的两侧 bounded prefactor。</p><p>真实增益与黏性 action、继而与无黏 action 匹配；同一条前向轨道满足 action-resolved localization。独立解析审计与对抗审计均通过。15 条有限主轨迹、第二积分器重算和期刊级四联图用于复现与错误探测，不认证连续结论。</p><p>__CLOSED__。__FINITE__。__OPEN__。NOT CLAY。</p><div class="links"><a href="/notes/r0-73l.html">R0.73L</a><a href="/assets/r073l/__FIGURE_ID__.pdf">R0.73L 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073l">R0.73L 有限诊断包</a></div></article>'''
RECAP_PHASE = (RECAP_PHASE.replace("__CLOSED__", CLOSED)
               .replace("__FINITE__", FINITE)
               .replace("__OPEN__", OPEN)
               .replace("__FIGURE_ID__", FIGURE_ID))
