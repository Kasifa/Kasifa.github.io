#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reader-facing fragments for the fail-closed R0.73K release."""

FIGURE_ID = "fig-r073k-uniform-viscous-branch"
FIGURE_RELATIVE = f"figures/r073k/{FIGURE_ID}"

R073J_BASELINE = {
    "latestCompletedRelease": "r073j", "siteVersion": "1.50",
    "publicHtmlNoteCount": 186, "postR060RecapNodeCount": 126,
    "nextRelease": "r073k", "postR070APublishedReleaseCount": 88,
    "postR070AFormalSealedReleaseCount": 64,
    "legacyFormalFigureBacklogCount": 24,
}

R073K_TARGET = {
    "latestCompletedRelease": "r073k", "siteVersion": "1.51",
    "publicHtmlNoteCount": 187, "postR060RecapNodeCount": 127,
    "nextRelease": "r073l", "postR070APublishedReleaseCount": 89,
    "postR070AFormalSealedReleaseCount": 65,
    "legacyFormalFigureBacklogCount": 24,
}

CLOSED = (
    "uniformRankOneViscousBranch=CLOSED；"
    "uniformProjectionNormConvergence=CLOSED；"
    "uniformEigenvalueOepsilon=CLOSED；"
    "uniformProjectionConditioning=CLOSED；"
    "fixedHalfPlaneNoPollution=CLOSED；"
    "uniformReducedResolvent=CLOSED；"
    "uniformComplementSemigroup=CLOSED"
)

FINITE = (
    "finiteDiagnosticPackage=CLOSED；"
    "primarySpectralStates=1190；crossCutoffComparisons=952；"
    "independentFiniteReconstruction=PASS；"
    "finiteDimensionDoesNotCertifyContinuum=TRUE"
)

OPEN = (
    "explicitViscosityThreshold=OPEN；"
    "nonselfadjointAdiabaticTracking=OPEN；matchingSelectedGainAction=OPEN；"
    "nonlinearNavierStokes=OPEN；transverseThreeDimensionalClosure=OPEN；"
    "finiteTimeSingularity=OPEN；Clay=OPEN"
)

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73K · VANISHING VISCOSITY · UNIFORM RANK-ONE BRANCH</div>
        <h1>参数一致黏性 rank-one 谱支与补空间控制</h1>
        <p class="lead">R0.73K 证明：对已认证的两谐波周期剪切流族，存在一个共同但未显式数值化的黏度阈值。当 \(0<\varepsilon\le\varepsilon_K\) 时，对每个 \(d\in[0,1/450]\)，共同圆 \(|z-0.17|<0.003\) 内恰有一个实的代数简单黏性特征值；固定半平面 \(\operatorname{Re}z\ge0.12\) 内无其他谱点。Riesz 投影在算子范数下一致收敛，特征值偏移满足 \(O(\varepsilon)\) 上界；补空间 reduced resolvent 一致有界，半群满足 \(Ce^{0.12t}\) 增长上界。证明不假设完整 norm-resolvent 收敛。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73K 完成</span><strong>Continuum theorem + finite-dimensional diagnostic</strong><p>版本 v0.73K · 2026-08-31</p><p>共同黏度阈值：存在，未显式数值化</p><p>有限状态：1,190</p><p>跨 cutoff 比较：952</p><p>3D / CLAY：OPEN</p><p>NOT CLAY</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct result</div><h2>共同圆内的 rank-one 黏性谱块已经闭合</h2><div class="equation result">\[\sup_d\|P_\varepsilon(d)-P_0(d)\|\to0,\qquad \sup_d|\lambda_\varepsilon(d)-\lambda_0(d)|\le C_\lambda\varepsilon.\]</div><p>存在 \(\varepsilon_K>0\)，使结论对 \(0<\varepsilon\le\varepsilon_K\) 与 \(0\le d\le1/450\) 同时成立。共同圆 \(|z-0.17|<0.003\) 内恰有一个实的代数简单黏性特征值，它关于 \(d\) 实解析；固定半平面 \(\operatorname{Re}z\ge0.12\) 内无其他谱点。这个阈值是定性存在结论；本节没有给出可计算数值。</p></section>
        <section id="singular"><div class="section-no">01 / Singular limit</div><h2>全预解式的算子范数收敛在这里不成立</h2><p>正黏性算子有紧 resolvent，无黏算子保留乘法本质谱，其 resolvent 非紧。完整 resolvent 若按算子范数收敛，会把非紧算子写成紧算子的范数极限。因此 <code>fullNormResolventConvergence=FALSE</code>，证明只在紧项两侧建立参数一致收敛。</p></section>
        <section id="projection"><div class="section-no">02 / Riesz projection</div><h2>两侧紧夹逼把强收敛升级为算子范数下一致收敛</h2><p>耗散基 resolvent 及其伴随在共同右半平面紧集上联合强收敛。\(K_d\) 与 \(K_d^*\) 构成 collectively compact 族，所以左右紧夹逼按算子范数收敛。Fredholm 因子在共同圆周 \(|z-0.17|=0.003\) 上保持可逆；基 resolvent 的围道积分为零，留下的紧修正给出 \(P_\varepsilon\to P_0\) 和 rank-one 保持。</p></section>
        <section id="rate"><div class="section-no">03 / First-order rate</div><h2>把无界椭圆算子移到平滑左特征向量上</h2><div class="equation result">\[(\lambda_\varepsilon-\lambda_0)\langle\ell_0,h_\varepsilon\rangle=-\varepsilon\langle L\ell_0,h_\varepsilon\rangle.\]</div><p>显式无黏左特征向量属于 \(D(L)\)，且 \(\sup_d\|L\ell_0(d)\|<\infty\)。Riesz 投影在算子范数下的一致收敛和既有 overlap 下界使分母一致远离零，因此得到特征值偏移的 \(O(\varepsilon)\) 上界；这里没有估计 \(L(h_\varepsilon-h_0)\)。</p></section>
        <section id="conditioning"><div class="section-no">04 / Conditioning</div><h2>投影、overlap、相位锚和参数导数同时受控</h2><div class="equation result">\[\sup_{\varepsilon,d}\|P_\varepsilon(d)\|<\frac95,\qquad \inf_{\varepsilon,d}\operatorname{overlap}>\frac59,\qquad \sup_{\varepsilon,d}\|\partial_dP_\varepsilon(d)\|<\infty.\]</div><p>antiunitary 对称与圆内总重数一保证特征值为实数。固定正黏性时，type-A 解析族和 Riesz 公式给出参数解析性与导数界；固定相位锚也持续非零。</p></section>
        <section id="halfplane"><div class="section-no">05 / Fixed half-plane</div><h2>局部圆之外还处理完整固定半平面</h2><div class="equation result">\[\sigma(B_\varepsilon(d))\cap\{\operatorname{Re}z\ge0.12\}=\{\lambda_\varepsilon(d)\}.\]</div><p>高虚部、高实部和剩余紧矩形分别估计。移除 rank-one 极点后，缩减 resolvent 在整个固定半平面一致有界。平方 resolvent 的 Bromwich 移线给出 \(\|e^{tB_\varepsilon(d)}Q_\varepsilon(d)\|\le Ce^{0.12t}\)；rank-one 块逆向满足 \(\|e^{-tB_\varepsilon(d)}P_\varepsilon(d)\|\le Ce^{-0.16t}\)。保守安全间隔取 \(1/25=0.04\)。</p></section>
        <section id="audit"><div class="section-no">06 / Independent audits</div><h2>两份解析审计分别检查证明链和可能失效的环节</h2><p>逐节审计要求补齐左右紧夹逼的分解、左右特征向量的定义域、Riesz 投影诱导的定义域分解，以及平方预解式的 Bromwich 反演步骤；修订后结论为 ANALYTIC PASS。反例式审计尝试破坏全参数一致性、实性、条件数、无界配对和非正规半群估计，结论为 PASS。两者均未用有限 Fourier 数据替代连续证明。</p></section>
        <section id="diagnostic"><div class="section-no">07 / Finite diagnostic</div><h2>1,190 个有限谱状态由第二实现独立重建</h2><p>正式网格使用五个 cutoff、十七个 \(d\) 节点、十二个核心黏度和两个延拓压力测试黏度点，共保存 1,190 个谱状态与 952 个跨 cutoff 比较。第二实现从 \(W_d,W_d''\) 的显式 Fourier 系数重建矩阵，不复用主实现的递推代码。最大实现间特征值实部差为 \(1.008\times10^{-14}\)，全部九项整包检查通过。</p><p>在 \(N=160\)、\(\varepsilon\le10^{-3}\) 的核心网格上，\(\operatorname{Re}\lambda\in[0.168207092942025,0.170407976920434]\)，最小 overlap 为 \(0.5939991104\)，最大投影范数为 \(1.683504205\)，最大 \(\|P_\varepsilon-P_0\|\) 为 \(0.1806379812\)。这些数值只用于诊断有限维 Fourier 压缩。</p></section>
        <section id="figure"><div class="section-no">08 / Journal figure</div><h2>分支、投影条件数与 cutoff 收敛按期刊格式归档</h2><p><img src="/assets/r073k/__FIGURE_ID__.svg" alt="R0.73K finite-dimensional diagnostic for the parameter-uniform viscous branch"></p><p><a href="/assets/r073k/__FIGURE_ID__.pdf">下载矢量 PDF</a> · <a href="/assets/r073k/__FIGURE_ID__.png">下载 600 dpi PNG</a> · <a href="/assets/r073k/__FIGURE_ID__.svg">打开 SVG</a></p></section>
        <section id="literature"><div class="section-no">09 / Literature boundary</div><h2>一般黏性消失谱持续已知；本节给出该剖面族上的参数一致细化</h2><p>Shvydkoy--Friedlander 已证明 Euler 本质谱阈值右侧的孤立不稳定谱在黏性消失时持续。因此这里不声称首个一般谱持续定理。已核验来源中没有发现一条结果同时给出本节所需的整个 \(d\) 区间、Riesz 投影在算子范数下的一致收敛、特征值偏移的 \(O(\varepsilon)\) 上界、rank-one 条件数，以及固定半平面内补空间 reduced-resolvent 与半群增长上界；这只表示本次限定检索所核验的来源中未发现完全重合的定理，不是穷尽性、原创性或优先权声明。</p></section>
        <section id="boundary"><div class="section-no">10 / Exact boundary</div><h2>连续定理、有限诊断和开放问题分开列示</h2><p>__CLOSED__。</p><p>__FINITE__。</p><p>__OPEN__。</p><p>有限计算不认证连续 Riesz 秩、共同黏度阈值或补空间半群上界。连续定理也没有给出显式 \(\varepsilon_K\)，没有证明非自伴绝热跟踪、非线性增长、横向三维闭合、有限时间奇性或 Clay 问题。NOT CLAY。</p></section>
        <section id="value"><div class="section-no">11 / Research value</div><h2>移动生成元分析所需的静态谱输入已经具备</h2><p>结果提供一个可用固定相位锚规范化、条件数受控、以 \(O(\varepsilon)\) 靠近无黏支的 rank-one 谱块，并给出补空间 reduced-resolvent 的统一界与 \(Ce^{0.12t}\) 半群增长上界。这是当前绝热余项路线所需的一组静态输入，但不是绝热定理本身，更不能换算成 Clay 问题的完成比例。</p></section>
        <section id="next"><div class="section-no">12 / Next gate</div><h2>R0.73L：非自伴绝热跟踪</h2><p>下一节在共同定义域和上述非正规谱分解下估计移动投影耦合，检查时间尺度 \(D_*/\varepsilon\) 上的有界前因子和匹配作用量。</p></section>
        <section id="reproduce"><div class="section-no">13 / Reproduction</div><h2>证明、审计、文献、实验和附图均有直接入口</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073k_uniform_viscous_branch_proof.md">解析证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073k_independent_analytic_audit.md">独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073k_adversarial_audit.md">反例式审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073k_literature_audit.md">文献审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073k">有限诊断包</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073k/__FIGURE_ID__">正式附图包</a> · <a href="/notes/r0-73k.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73k.html">127 节累计回顾</a> · <a href="/recap-r0-61-r0-73k.pdf">累计回顾 PDF</a></p></section>
      </article>'''
NOTE_ARTICLE = (NOTE_ARTICLE.replace("__FIGURE_ID__", FIGURE_ID)
                .replace("__CLOSED__", CLOSED)
                .replace("__FINITE__", FINITE)
                .replace("__OPEN__", OPEN))

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73L</span><span class="tree-state current">下一检查点</span></div>
              <h3>非自伴绝热跟踪</h3><p>在共同定义域和上述非正规谱分解下控制移动投影耦合，检查 \(D_*/\varepsilon\) 时间尺度上的有界前因子和匹配作用量。</p>
            </article>'''

HOME_K_CARD = r'''          <div class="task-one" id="r073k" data-release="r073k" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73K · 2026-08-31</p><h3>参数一致黏性 rank-one 谱支与补空间控制</h3>
            <p>存在共同但未数值化的黏度阈值；无黏特征值在整个 \(d\in[0,1/450]\) 上延拓为共同圆内唯一的实代数简单黏性谱支。Riesz 投影在算子范数下一致收敛，特征值偏移满足 \(O(\varepsilon)\) 上界。</p>
            <p>固定半平面 \(\operatorname{Re}z\ge0.12\) 内无其他谱点。补空间 reduced resolvent 一致有界，半群满足 \(Ce^{0.12t}\) 增长上界；选定 rank-one 谱块的逆向群满足 \(Ce^{-0.16t}\)，保守实部安全间隔为 \(1/25\)。</p>
            <p><strong>有限诊断：</strong>1,190 个谱状态、952 个跨 cutoff 比较和第二实现全部通过；它们不承担连续定理证明权重。</p>
            <p><strong>开放边界：</strong>&nbsp;__OPEN__。NOT CLAY。</p>
            <p><a href="/notes/r0-73k.html"><strong>阅读 R0.73K 研究笔记 →</strong></a><br><a href="/notes/r0-73k.pdf">下载同步 PDF</a> · <a href="/assets/r073k/__FIGURE_ID__.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073k">查看有限诊断包</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073k_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73k.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73L：</strong>&nbsp;证明或否定非自伴绝热跟踪及其有界前因子。</p>
          </div>'''
HOME_K_CARD = HOME_K_CARD.replace("__FIGURE_ID__", FIGURE_ID).replace("__OPEN__", OPEN)

HOME_LATEST_SPOTLIGHT = r'''    <section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">
      <div class="route-overview-inner"><header class="route-map-header">
        <div><p class="eyebrow">LATEST RELEASE · R0.73K · 2026-08-31</p><h2 class="route-map-title" id="latest-release-title">参数一致黏性 rank-one 谱支与补空间控制</h2><p class="route-map-intro">共同圆内唯一的实代数简单黏性谱支、Riesz 投影在算子范数下的一致收敛、特征值偏移的 \(O(\varepsilon)\) 上界、条件数、固定半平面内无其他谱点，以及补空间 reduced-resolvent 与半群增长上界已经闭合。共同黏度阈值尚未显式量化；有限诊断、非自伴绝热、横向三维、奇性与 Clay 的边界分别保留。</p></div>
        <nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-73k.pdf">阅读最新 R0.73K 研究笔记 →</a><a href="/recap-r0-61-r0-73k.html">127 节累计回顾</a><a href="/notes/">187 篇研究笔记总索引</a><a href="#r073k">查看首页完整 R0.73K 卡片</a></nav>
      </header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73K · 89 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>65 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73K</span></div></div>
    </section>'''

RECAP_PHASE = r'''            <article class="phase"><h3>R0.73K · Parameter-uniform viscous rank-one branch</h3><p>存在共同阈值 \(\varepsilon_K>0\)，使完整 \(d\in[0,1/450]\) 上的无黏特征值延拓为共同圆内唯一的实代数简单黏性谱支。Riesz 投影在算子范数下一致收敛，\(|\lambda_\varepsilon-\lambda_0|\le C_\lambda\varepsilon\)，投影范数小于 \(9/5\)，固定相位锚持续非零。</p><p>固定半平面 \(\operatorname{Re}z\ge0.12\) 只有选定谱支；补空间 reduced resolvent 一致有界，半群满足 \(Ce^{0.12t}\) 增长上界，选定 rank-one 谱块的逆向界为 \(Ce^{-0.16t}\)。1,190 个有限状态和 952 个跨 cutoff 比较全部通过独立重建，但不认证连续定理。</p><p>__CLOSED__。__FINITE__。__OPEN__。NOT CLAY。</p><div class="links"><a href="/notes/r0-73k.html">R0.73K</a><a href="/assets/r073k/__FIGURE_ID__.pdf">R0.73K 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073k">R0.73K 有限诊断包</a></div></article>'''
RECAP_PHASE = (RECAP_PHASE.replace("__CLOSED__", CLOSED)
               .replace("__FINITE__", FINITE)
               .replace("__OPEN__", OPEN)
               .replace("__FIGURE_ID__", FIGURE_ID))
