#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reader-facing fragments for the fail-closed R0.73J release."""

FIGURE_ID = "fig-r073j-continuum-branch-certificate"
FIGURE_RELATIVE = f"figures/r073j/{FIGURE_ID}"

R073I_BASELINE = {
    "latestCompletedRelease": "r073i", "siteVersion": "1.49",
    "publicHtmlNoteCount": 185, "postR060RecapNodeCount": 125,
    "nextRelease": "r073j", "postR070APublishedReleaseCount": 87,
    "postR070AFormalSealedReleaseCount": 63,
    "legacyFormalFigureBacklogCount": 24,
}

R073J_TARGET = {
    "latestCompletedRelease": "r073j", "siteVersion": "1.50",
    "publicHtmlNoteCount": 186, "postR060RecapNodeCount": 126,
    "nextRelease": "r073k", "postR070APublishedReleaseCount": 88,
    "postR070AFormalSealedReleaseCount": 64,
    "legacyFormalFigureBacklogCount": 24,
}

CLOSED = ("periodicRayleighContinuumBridge=CLOSED；"
          "uniqueAlgebraicallySimpleRightmostBranch=CLOSED；"
          "uniformSpectralGapAtLeastOneOverTwenty=CLOSED；"
          "kineticOverlapAndFixedPhaseAnchor=CLOSED")

FAILURE_HISTORY = ("contourFullBallChebyshevPowerBernstein=FAILED_WITH_LEDGER；"
                   "overlapDirectIntervalClenshaw=FAILED_WITH_LEDGER；"
                   "naturalBoxFirstRound=76_PASS_7_WRAPPING_INCONCLUSIVE；"
                   "naturalBoxDepthTwo=1_RESOLVED_6_WRAPPING_INCONCLUSIVE")

AUDIT_STATUS = ("naturalBoxAdaptiveDepthFive=PASS_7_OF_7_PARENTS_2896_OF_2896_LEAVES；"
                "independentOverlapRawOdeRecomputation=NOT_RUN")

OPEN = ("fullyIndependentRawGridAudit=OPEN；uniformRankOneViscousBranch=OPEN；"
        "nonselfadjointAdiabaticRemainder=OPEN；matchingSelectedGainAction=OPEN；"
        "twoTermSelectedGainAsymptotic=OPEN；actionResolvedBackwardLocalization=OPEN；"
        "prescribedActionSeedDeparture=OPEN；fixedBackgroundLyapunovInstability=OPEN；"
        "transverseThreeDimensionalClosure=OPEN；finiteTimeSingularity=OPEN；Clay=OPEN")

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73J · PERIODIC RAYLEIGH · CONTINUUM-OPERATOR SPECTRAL CERTIFICATE</div>
        <h1>周期 Rayleigh 唯一简单最右谱支的连续算子认证</h1>
        <p class="lead">R0.73J 在完整区间 \(0\le d\le1/450\) 上认证一个实、代数简单且唯一的最右谱支 \(\lambda_0(d)\in(0.167,0.173)\)。其余谱点满足 \(\operatorname{Re}\lambda\le0.11\)，所以谱隙严格大于 \(0.057\)，并可固定取 \(g_*=1/20\)。证书还给出左右本征向量的统一重叠与固定相位锚。自然参数盒首轮和 depth-two 的 wrapping 历史完整保留；继续自适应细分到 depth five 后，7/7 原失败父盒与 2896/2896 最终叶盒均通过。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73J 完成</span><strong>Fail-closed continuum-operator certificate</strong><p>版本 v0.73J · 2026-08-30</p><p>主围道绕数：1</p><p>局部围道绕数：1</p><p>各审计共享对应原始网格</p><p>3D / CLAY：OPEN</p><p>NOT CLAY</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct result</div><h2>唯一简单最右谱支在连续算子层面闭合</h2><div class="equation result">\[\lambda_0:[0,1/450]\to(0.167,0.173),\qquad \sup\operatorname{Re}\!\left(\sigma(A_X(d))\setminus\{\lambda_0(d)\}\right)\le0.11.\]</div><p>因此 \(\lambda_0(d)\) 是实、代数简单的特征值，也是唯一满足 \(\operatorname{Re}\lambda>0.11\) 的谱点。严格谱隙大于 \(0.057\)，后续可统一采用 \(g_*=1/20\)。</p></section>
        <section id="bridge"><div class="section-no">01 / Analytic bridge</div><h2>Rayleigh 铅笔、Evans 零点与动力生成元的代数重数一致</h2><p>解析证明把动能空间生成元、普通 \(L^2\) 实现和周期 Rayleigh 边值问题连接起来。右半平面的 Evans 零点阶数等于生成元特征值的代数重数；Howard 圆盘保证每个满足 \(\operatorname{Re}\lambda>0.11\) 的谱点都落在全局计数矩形内。</p></section>
        <section id="contours"><div class="section-no">02 / Contour certificate</div><h2>64 个围道面板全部非零，两个绕数都等于 1</h2><div class="equation result">\[\inf_{[0,1/450]\times\partial\Omega}|E|>5.49948,\qquad \inf_{[0,1/450]\times\partial B_{\rm loc}}|E|>0.164355.\]</div><p>全局外矩形由 56 个面板覆盖，局部根圆由 8 个面板覆盖。每个参数端点与每个围道单元均进入证书；基点全局、局部绕数均为 1。非零同伦把计数延拓到整个参数区间。</p></section>
        <section id="overlap"><div class="section-no">03 / Overlap and phase</div><h2>左右重叠和固定相位锚远离零</h2><div class="equation result">\[\frac{|\langle\ell_d,h_d\rangle_X|}{\|\ell_d\|_X\|h_d\|_X}>0.585343,\qquad |M_{12}(d,\lambda_0(d))|>1.84154.\]</div><p>主区间计算覆盖 128 个重叠单元。第二种中心—Lipschitz 后处理复核全部单元，给出独立下界 \(0.585009>1/2\)。这允许固定连续相位并排除左右配对退化。</p></section>
        <section id="independence"><div class="section-no">04 / Audit boundary</div><h2>两项第二实现各自共用对应的冻结原始 ODE 网格</h2><p>围道证书的第二套 range 与 winding 实现共用对应的冻结围道网格；重叠证书的第二套 center--Lipschitz 实现共用另一批对应的冻结重叠网格。两者都能发现后处理、索引和舍入错误，但都没有独立重算原始 ODE 数据。因此这里写作“共享对应原始网格的独立后处理”，不写成完全独立的数值复现。完整独立 raw-grid 审计仍为 OPEN。</p></section>
        <section id="natural"><div class="section-no">05 / Natural-box audit</div><h2>自然参数盒最终通过，但仍只是辅助复核</h2><p>首轮 83 个自然盒中 76 个通过，7 个因 Evans 区间 wrapping 无法判定。depth-two 仅解析 1/7 个父盒，留下 96 个未决叶盒。继续自适应细分后，depth three 为 64/384、depth four 为 768/1280、depth five 为 2048/2048；最终 7/7 个父盒、83/83 个选定自然盒与 2896/2896 个最终叶盒全部覆盖通过，最小 Evans 下界大于 \(0.00714950\)。这仍是抽样辅助复核，不替代主围道的完整参数一致证书。</p></section>
        <section id="failures"><div class="section-no">06 / Failed methods</div><h2>失败的区间路线保留在方法账本</h2><p>围道证书的 full-ball Chebyshev--power--Bernstein 转换发生过度 wrapping；重叠证书的直接区间 Clenshaw 在参数端点丢失共享变量依赖。失败输入、范围和原因保存在 <code>failure_ledger.json</code>。这些记录说明正式证书为何改用各自通过验证的替代范围方法，而不是把未决范围静默丢弃。</p></section>
        <section id="figure"><div class="section-no">07 / Journal figure</div><h2>围道与重叠证书以期刊格式归档</h2><p><img src="/assets/r073j/__FIGURE_ID__.svg" alt="R0.73J continuum-operator spectral-branch contour and overlap certificate"></p><p><a href="/assets/r073j/__FIGURE_ID__.pdf">下载矢量 PDF</a> · <a href="/assets/r073j/__FIGURE_ID__.png">下载 600 dpi PNG</a> · <a href="/assets/r073j/__FIGURE_ID__.svg">打开 SVG</a></p></section>
        <section id="boundary"><div class="section-no">08 / Exact boundary</div><h2>CLOSED、失败历史、审计状态与 OPEN 分列</h2><p>__CLOSED__。</p><p>__FAILURE_HISTORY__。</p><p>__AUDIT_STATUS__。</p><p>__OPEN__。</p><p>有限 Galerkin 诊断中实部约为 \(0.04\) 的较弱不稳定共轭对不承担连续算子上的存在性或重数证明权重；它不与“\(\operatorname{Re}\lambda>0.11\) 区域内唯一”的定理冲突。</p><p>本节是特定周期剪切剖面的连续算子谱支认证，不是三维 Navier--Stokes 正则性或奇性证明。NOT CLAY。</p></section>
        <section id="literature"><div class="section-no">09 / Literature boundary</div><h2>周期 Evans 计数与验证数值工作提供方法先例</h2><p>文献审计区分周期 Evans 零点理论、验证围道计算、Howard 包络以及退化临界层问题。相邻工作不自动给出本算子的统一参数证书；本节的重数桥接与全部数值边界均由随附材料单独核验。</p></section>
        <section id="value"><div class="section-no">10 / Research value</div><h2>下一阶段所需的谱支选择条件已经具备</h2><p>这一结果关闭了固定正窗口上的谱支唯一性、简单性、统一谱隙、左右重叠与相位选择门槛。它为黏性谱支延拓和非自伴绝热估计提供输入，但尚未证明这两步，也没有推出非线性增长或三维奇性。</p></section>
        <section id="next"><div class="section-no">11 / Next gate</div><h2>R0.73K：黏性谱支与统一投影控制</h2><p>下一节检查小黏性扰动下的唯一谱支、Riesz 投影与补空间半群界，并保持参数和大频率常数可追踪。</p></section>
        <section id="reproduce"><div class="section-no">12 / Reproduction</div><h2>定理、证明、审计、文献、实验和附图均有直接入口</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073j_continuum_branch_theorem.md">定理</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073j_analytic_proof.md">解析证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073j_overlap_analytic_proof.md">重叠证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073j_analytic_audit.md">独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073j_adversarial_audit.md">敌对证据审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073j_literature_audit.md">文献审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073j">正式实验包</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073j/__FIGURE_ID__">正式附图包</a> · <a href="/notes/r0-73j.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73j.html">126 节累计回顾</a> · <a href="/recap-r0-61-r0-73j.pdf">累计回顾 PDF</a></p></section>
      </article>'''
NOTE_ARTICLE = (NOTE_ARTICLE.replace("__FIGURE_ID__", FIGURE_ID)
                .replace("__CLOSED__", CLOSED)
                .replace("__FAILURE_HISTORY__", FAILURE_HISTORY)
                .replace("__AUDIT_STATUS__", AUDIT_STATUS)
                .replace("__OPEN__", OPEN))

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73K</span><span class="tree-state current">下一检查点</span></div>
              <h3>黏性谱支与统一投影控制</h3><p>检查小黏性扰动下的唯一谱支、Riesz 投影和补空间半群界；随后再进入非自伴绝热余项。</p>
            </article>'''

HOME_I_CARD = r'''          <div class="task-one" id="r073j" data-release="r073j" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73J · 2026-08-30</p><h3>周期 Rayleigh 唯一简单最右谱支的连续算子认证</h3>
            <p>在 \(0\le d\le1/450\) 上，唯一最右谱支满足 \(\lambda_0(d)\in(0.167,0.173)\)。其余谱点实部不超过 \(0.11\)，严格谱隙大于 \(0.057\)，可取 \(g_*=1/20\)。</p>
            <p>主证书给出重叠 \(>0.585343\)、相位锚 \(>1.84154\)、全局与局部围道下界 \(>5.49948\) 和 \(>0.164355\)，两个绕数均为 1。</p>
            <p><strong>审计边界：</strong>围道的 range/winding 与重叠的 center--Lipschitz 第二实现各自共用对应的冻结原始 ODE 网格，均未独立重算 raw ODE；自然盒首轮 76/83 通过，depth-two 仅 1/7 解析。自适应推进到 depth five 后，7/7 父盒和 2896/2896 最终叶盒全部通过；独立 overlap raw-ODE 三盒仍未运行。</p>
            <p><strong>开放边界：</strong>&nbsp;__OPEN__。NOT CLAY。</p>
            <p><a href="/notes/r0-73j.html"><strong>阅读 R0.73J 研究笔记 →</strong></a><br><a href="/notes/r0-73j.pdf">下载同步 PDF</a> · <a href="/assets/r073j/__FIGURE_ID__.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073j">查看实验包</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073j_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73j.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73K：</strong>&nbsp;认证黏性谱支和统一投影控制。</p>
          </div>'''
HOME_I_CARD = HOME_I_CARD.replace("__FIGURE_ID__", FIGURE_ID).replace("__OPEN__", OPEN)

HOME_LATEST_SPOTLIGHT = r'''    <section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">
      <div class="route-overview-inner"><header class="route-map-header">
        <div><p class="eyebrow">LATEST RELEASE · R0.73J · 2026-08-30</p><h2 class="route-map-title" id="latest-release-title">周期 Rayleigh 唯一简单最右谱支的连续算子认证</h2><p class="route-map-intro">连续算子上的唯一简单最右谱支、显式谱隙、左右重叠和固定相位锚已经闭合。自然盒自适应深审计已覆盖 83/83 个选定盒；各项第二实现共用对应冻结原始网格的限制、尚未运行的 overlap raw-ODE 三盒、黏性延拓、非自伴绝热、横向三维、奇性与 Clay 均明确保留。</p></div>
        <nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-73j.pdf">阅读最新 R0.73J 研究笔记 →</a><a href="/recap-r0-61-r0-73j.html">126 节累计回顾</a><a href="/notes/">186 篇研究笔记总索引</a><a href="#r073j">查看首页完整 R0.73J 卡片</a></nav>
      </header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73J · 88 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>64 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73J</span></div></div>
    </section>'''
