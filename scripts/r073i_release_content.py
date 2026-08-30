#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reader-facing fragments for the fail-closed R0.73I release."""

FIGURE_ID = "fig-r073i-action-boundary"
FIGURE_RELATIVE = f"figures/r073i/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r073i"

R073H_BASELINE = {
    "latestCompletedRelease": "r073h",
    "siteVersion": "1.48",
    "publicHtmlNoteCount": 184,
    "postR060RecapNodeCount": 124,
    "nextRelease": "r073i",
    "postR070APublishedReleaseCount": 86,
    "postR070AFormalSealedReleaseCount": 62,
    "legacyFormalFigureBacklogCount": 24,
}

R073I_TARGET = {
    "latestCompletedRelease": "r073i",
    "siteVersion": "1.49",
    "publicHtmlNoteCount": 185,
    "postR060RecapNodeCount": 125,
    "nextRelease": "r073j",
    "postR070APublishedReleaseCount": 87,
    "postR070AFormalSealedReleaseCount": 63,
    "legacyFormalFigureBacklogCount": 24,
}

CLOSED = (
    "inheritedEndpointStrictlyBelowOneOver450=CLOSED；"
    "improvedContinuumUpperAction=CLOSED；"
    "zeroWindowTangentAction=CLOSED"
)

FALSE = (
    "fixedWindowActionFromInheritedInputs=FALSE_AS_INFERENCE；"
    "theoremEndpointEqualsOneOver450=FALSE_AS_INFERENCE；"
    "actionLimitAloneGivesBoundedPrefactor=FALSE_AS_INFERENCE；"
    "finitePilotProvesContinuumAction=FALSE_AS_INFERENCE；"
    "finiteWkbProvesContinuumTwoTermLaw=FALSE_AS_INFERENCE"
)

OPEN = (
    "canonicalSelectedBranch=OPEN；explicitPositiveActionWindow=OPEN；"
    "uniformRankOneViscousBranch=OPEN；matchingSelectedGainAction=OPEN；"
    "twoTermSelectedGainAsymptotic=OPEN；"
    "actionResolvedBackwardLocalization=OPEN；"
    "prescribedActionSeedDeparture=OPEN；"
    "fixedBackgroundLyapunovInstability=OPEN；"
    "transverseThreeDimensionalClosure=OPEN；"
    "finiteTimeSingularity=OPEN；Clay=OPEN"
)

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73I · ENDPOINT AUDIT · UPPER ACTION · ZERO-WINDOW TANGENT</div>
        <h1>选定增益作用量的<br>端点校正与固定窗口边界</h1>
        <p class="lead">R0.73I 证明 R0.73H 的继承端点必为可继续缩小的 \(d_0<\sqrt{19/180}/392<1/450\)，并得到完整移动传播子的连续体上作用量与严格黏性因子。完整顶谱块的最小、最大增益在“先 \(\varepsilon\downarrow0\)，再 \(D\downarrow0\)”的顺序下具有共同切向速率 \(a\)。两个精确反例同时证明：现有 R0.73F–H 输入不能推出固定正窗口的规范作用量或有界前因子。真实算子的匹配作用量、预设种子、固定背景、横向三维、奇性与 Clay 仍为 OPEN。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73I 完成</span><strong>Fail-closed action audit</strong><p>版本 v0.73I · 2026-08-30</p><p>3 项：CLOSED</p><p>5 个推断：FALSE</p><p>FIXED WINDOW：OPEN</p><p>3D / CLAY：OPEN</p><p>NOT CLAY</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>端点、上作用量和零窗口切向速率已经闭合</h2><div class="verdict-grid"><div class="verdict-card true"><strong>CLOSED · ENDPOINT</strong><p>继承端点严格小于 \(\sqrt{19/180}/392\)，所以不等于 \(1/450\)。</p></div><div class="verdict-card true"><strong>CLOSED · UPPER ACTION</strong><p>完整传播子满足 \(e^{\Omega_H(D)/\varepsilon-D/4}\) 上界。</p></div><div class="verdict-card true"><strong>CLOSED · TANGENT RATE</strong><p>顶谱块最小、最大增益的零窗口切向速率都等于 \(a\)。</p></div><div class="verdict-card false"><strong>OPEN · FIXED WINDOW</strong><p>规范谱支、匹配作用量与有界前因子尚未得到。</p></div></div></section>
        <section id="endpoint"><div class="section-no">01 / Inherited endpoint</div><h2>R0.73H 的实际端点是可缩小的 \(d_0\)</h2><div class="equation result">\[D=d_0<\frac{\sqrt{19/180}}{392}\approx8.2880904293\times10^{-4}<\frac1{450}.\]</div><p>R0.73F 的粗糙性条件给 \(d_0<\nu/(16K^2C_A)\)，其中 \(C_A=49/4\)、\(K\ge1\)、\(\nu&lt;a/2\)。R0.73H 的精确 \(H_0\ge I/20\) 证书再给 \(a\le\sqrt{19/180}\)。这个数只是严格上界，不是 \(d_0\) 的取值；原证明允许继续缩小端点。</p></section>
        <section id="upper"><div class="section-no">02 / Continuum upper action</div><h2>\(\gamma=1/2\) 行的完整传播子有显式一侧作用量</h2><div class="equation result">\[c_H(d)=\frac13\sqrt{\frac{19}{20}+\frac{45d}{4}},\qquad \Omega_H(D)=\int_0^D c_H(s)\,\mathrm ds.\]</div><div class="equation result">\[\|U_\varepsilon(D/\varepsilon,0)\|\le\exp\!\left(\frac{\Omega_H(D)}{\varepsilon}-\frac D4\right),\quad0\le D\le1/450.\]</div><p>完成平方把 \(\gamma=1/2\) 数值横坐标转回 R0.73H 的 \(H_d\) 正性。因 \(L\ge I/4\)，黏性还保留严格因子 \(e^{-D/4}\)。这是完整传播子的一侧上界，不是匹配作用量。</p></section>
        <section id="tangent"><div class="section-no">03 / Zero-window tangent</div><h2>完整顶谱块在零窗口具有共同切向速率</h2><div class="equation result">\[m_\varepsilon(D)=\inf_{\substack{v\in P_\varepsilon H\\\|v\|=1}}\|U_\varepsilon(D/\varepsilon,0)v\|,\qquad M_\varepsilon(D)=\sup_{\substack{v\in P_\varepsilon H\\\|v\|=1}}\|U_\varepsilon(D/\varepsilon,0)v\|.\]</div><div class="equation result">\[\lim_{D\downarrow0}\liminf_{\varepsilon\downarrow0}\frac{\varepsilon}{D}\log m_\varepsilon(D)=\lim_{D\downarrow0}\limsup_{\varepsilon\downarrow0}\frac{\varepsilon}{D}\log M_\varepsilon(D)=a,\]</div><p>其余两种 limsup/liminf 组合也等于 \(a\)。R0.73F 的 every-vector 下界控制最小增益，R0.73E 的冻结半群与 \(49d/4\) 漂移控制最大增益。</p></section>
        <section id="quantifiers"><div class="section-no">04 / Quantifier order</div><h2>先固定窗口取 \(\varepsilon\downarrow0\)，再让窗口趋零</h2><p>给定下精度 \(\zeta>0\)，先选择谱切分，再得到依赖于 \(\zeta\) 的 \(d_\zeta>0\)。固定 \(0&lt;D\le d_\zeta\) 后才取 \(\varepsilon\downarrow0\)，最后取 \(D\downarrow0\) 与 \(\zeta\downarrow0\)。证明不允许任意联合路径 \(D=D(\varepsilon)\)，也不证明任何固定正 \(D\) 的内层极限存在。</p></section>
        <section id="selection"><div class="section-no">05 / Selection no-go</div><h2>二维顶谱块可以让不同合法 launch 产生不同作用量</h2><div class="equation result">\[A(d)=\operatorname{diag}(a+\kappa d,a-\kappa d),\qquad \varepsilon\log G_{\varepsilon,\pm}(D)\to aD\pm\frac{\kappa D^2}{2}.\]</div><p>在 \(d=0\) 两个向量都属于同一顶谱块，并满足现有“选择一个归一化顶特征向量”的规则。交替选择会产生两个子列极限。这个反例只否定从现有抽象输入推出唯一作用量，不否定真实 PDE 算子可能有唯一简单右端谱支。</p></section>
        <section id="prefactor"><div class="section-no">06 / Prefactor no-go</div><h2>作用量存在也不保证去指数后的前因子有界</h2><div class="equation result">\[A(d)=\begin{pmatrix}a&0\\d&a\end{pmatrix},\qquad G_\varepsilon(D)=e^{aD/\varepsilon-D}\sqrt{1+\frac{D^4}{4\varepsilon^2}}.\]</div><p>这里 \(\varepsilon\log G_\varepsilon(D)\to aD\)，但补偿后的增益按 \(\varepsilon^{-1}=\Lambda\) 增长。粗二分指数可以吸收这个多项式，因此 R0.73F 的固定窗口下界不会排除它。</p></section>
        <section id="seed"><div class="section-no">07 / Prescribed seed</div><h2>纯指数种子需要额外的两侧前因子定理</h2><div class="equation result">\[0&lt;c_D\le G_\Lambda(D)e^{-\Lambda\mathcal A(D)}\le C_D<\infty.\]</div><p>只有 \(\Lambda^{-1}\log G_\Lambda\to\mathcal A\) 时，剩余的 \(e^{o(\Lambda)}\) 仍可能趋零、发散或振荡。若真实前因子是 \(\Lambda^p\)，预设种子必须包含 \(\Lambda^{-p}\)。所以 R0.73H 的 \(\delta/G_\Lambda\) 目前不能换成纯指数。</p></section>
        <section id="finite"><div class="section-no">08 / Finite action diagnostic</div><h2>三个窗口分开标记，均不冒充定理端点</h2><table class="compact-table"><thead><tr><th>有限窗口</th><th>\(\mathcal A_N(D)\)</th><th>\(\mathcal A_N(D)/D\)</th></tr></thead><tbody><tr><td>\(10^{-4}\)，显式 pilot</td><td>\(1.7039125194755544\times10^{-5}\)</td><td>\(0.17039125194755542\)</td></tr><tr><td>\(D_{\rm ub}\)，仅为 \(d_0\) 上界</td><td>\(1.4112087459740226\times10^{-4}\)</td><td>\(0.17026946774036794\)</td></tr><tr><td>\(1/450\)，旧比较点</td><td>\(3.778603553777033\times10^{-4}\)</td><td>\(0.17003715991996649\)</td></tr></tbody></table><p>这些数来自 \(N=48\) binary64 Fourier--Galerkin 压缩。cutoff、积分阶数和快时间步长比较通过，但没有无穷维尾部包络。</p></section>
        <section id="wkb"><div class="section-no">09 / Finite WKB diagnostic</div><h2>有限 residual 与 Berry–黏性修正吻合</h2><div class="equation result">\[\mathcal C_N(D)=-\int_0^D\operatorname{Re}\left(\langle\ell_{0,N},\partial_dh_{0,N}\rangle+\langle\ell_{0,N},L_Nh_{0,N}\rangle\right)\,\mathrm dd.\]</div><p>三个窗口在 \(\Lambda=10^6\) 时，\(\log G_{\Lambda,N}-\Lambda\mathcal A_N-\mathcal C_N\) 都约为 \(8.64\times10^{-7}\)。独立 kinetic-coordinate RK4 与 CF4 的最大 log 差为 \(1.636\times10^{-9}\)。这支持下一条谱支—绝热路线，但不证明连续体两项式。</p></section>
        <section id="certificate"><div class="section-no">10 / Certificate</div><h2>精确常数链、逻辑反例和有限诊断分层封存</h2><p>主证书用 Fraction 与 Decimal 独立核对 \(5/19\)、\(19/180\)、392、\(8/405\)、严格端点比较和两个反例。第二套脚本采用不同代数链复算。有限包另存 98 条进度事件、三类 CSV、环境、配置、manifest 与 SHA256；其 claim boundary 明确把 continuum action、WKB 定理和 Clay 全部设为 false。</p></section>
        <section id="literature"><div class="section-no">11 / Literature boundary</div><h2>有限维非自伴绝热先例不能替代本题的连续谱门槛</h2><p>Nenciu–Rasche 的二能级 least-dissipative 绝热展开给出 Berry 修正的正面先例；Kato、Nenciu 与开放系统绝热工作提供一般框架。它们不自动覆盖本题的未界抛物生成元、\(\varepsilon\)-依赖黏性修正、连续体唯一右端谱支与 complement 余项。Li–Masmoudi–Zhao 的近 Couette 增长机制和 Li–Zhao 的热演化剪切研究与本题相邻，但几何与结论不同。</p></section>
        <section id="audit"><div class="section-no">12 / Independent audit</div><h2>常数、量词、定义域和反例范围逐项复核</h2><p>独立解析审计检查完成平方中的 2 与 4、严格黏性因子、\(d_0\) 的严格不等式、四个迭代极限和反例的粗二分兼容性。敌对审计专门攻击把上界说成匹配、把零窗口说成固定窗口、把有限 WKB 说成连续定理，以及把逻辑不可推出说成 PDE 反例。</p></section>
        <section id="figure"><div class="section-no">13 / Journal figure</div><h2>有限作用量与 WKB residual 以期刊格式归档</h2><p><img src="/assets/r073i/__FIGURE_ID__.svg" alt="R0.73I finite action and WKB residual diagnostic"></p><p><a href="/assets/r073i/__FIGURE_ID__.pdf">下载 PDF</a> · <a href="/assets/r073i/__FIGURE_ID__.png">下载 600 dpi PNG</a> · <a href="/assets/r073i/__FIGURE_ID__.svg">打开 SVG</a></p></section>
        <section id="boundary"><div class="section-no">14 / Exact boundary</div><h2>CLOSED、FALSE AS INFERENCE 与 OPEN 分列</h2><p>__CLOSED__。</p><p>__FALSE__。</p><p>__OPEN__。</p><p><code>FALSE_AS_INFERENCE</code> 只否定从现有输入到目标结论的推断，不否定真实算子可能满足该结论。</p></section>
        <section id="value"><div class="section-no">15 / Research value</div><h2>这一节把“未知增益”拆成可证明部分与真正谱门槛</h2><p>端点歧义已经清除；连续体上作用量和零窗口切向匹配成为可复用定理；纯指数种子所需的前因子条件也被准确识别。固定正窗口仍需唯一简单右端谱支和非自伴绝热控制。该进展改善的是证明结构，不是三维奇性结论。</p></section>
        <section id="next"><div class="section-no">16 / Next gate</div><h2>R0.73J：唯一简单右端谱支的连续体证书</h2><p>下一节在一个显式正窗口上计数 Rayleigh/Evans 零点、证明简单性并排除更右谱点；随后才进入黏性支与绝热余项。有限矩阵的一维顶支和约 \(0.1296\) 实部间隙只作为围道设计信息。</p></section>
        <section id="reproduce"><div class="section-no">17 / Reproduction</div><h2>证明、反例、审计、证书、有限包和附图均提供直接入口</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_report-source.md">完整报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_continuum_upper_action_proof.md">上作用量证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_zero_window_tangent_proof.md">零窗口证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_fixed_window_no_go.md">固定窗口反例</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_independent_analytic_audit.md">独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_adversarial_audit.md">敌对审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_literature_audit.md">文献审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_bilingual_dictionary.md">双语词典</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073i">正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073i">有限诊断包</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073i/__FIGURE_ID__">正式附图包</a> · <a href="/notes/r0-73i.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73i.html">125 节累计回顾</a> · <a href="/recap-r0-61-r0-73i.pdf">累计回顾 PDF</a></p></section>
      </article>'''
NOTE_ARTICLE = (NOTE_ARTICLE.replace("__FIGURE_ID__", FIGURE_ID)
                .replace("__CLOSED__", CLOSED)
                .replace("__FALSE__", FALSE)
                .replace("__OPEN__", OPEN))

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73J</span><span class="tree-state current">下一检查点</span></div>
              <h3>唯一简单右端谱支的连续体证书</h3><p>在显式正窗口上计数 Rayleigh/Evans 零点、证明简单性并排除更右谱点；随后进入黏性谱支与非自伴绝热余项。</p>
            </article>'''

HOME_I_CARD = r'''          <div class="task-one" id="r073i" data-release="r073i" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73I · 2026-08-30</p><h3>选定增益作用量的端点校正与固定窗口边界</h3>
            <p>继承端点严格小于 \(1/450\)；完整传播子得到显式连续体上作用量；完整顶谱块的最小、最大增益在零窗口具有共同切向速率 \(a\)。</p>
            <p>两个精确反例说明，现有 R0.73F–H 输入不能推出固定正窗口的规范作用量或有界前因子。有限 WKB 吻合只用于设计下一条谱支—绝热路线。</p>
            <p><strong>闭合结论：</strong>&nbsp;__CLOSED__。</p><p><strong>作为推断为假：</strong>&nbsp;__FALSE__。</p><p><strong>开放边界：</strong>&nbsp;__OPEN__。</p>
            <p><a href="/notes/r0-73i.html"><strong>阅读 R0.73I 研究笔记 →</strong></a><br><a href="/notes/r0-73i.pdf">下载同步 PDF</a> · <a href="/assets/r073i/__FIGURE_ID__.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073i">查看正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073i_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73i.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73J：</strong>&nbsp;认证唯一简单右端谱支及其显式正窗口。</p>
          </div>'''
HOME_I_CARD = (HOME_I_CARD.replace("__FIGURE_ID__", FIGURE_ID)
               .replace("__CLOSED__", CLOSED)
               .replace("__FALSE__", FALSE)
               .replace("__OPEN__", OPEN))

HOME_LATEST_SPOTLIGHT = r'''    <section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">
      <div class="route-overview-inner"><header class="route-map-header">
        <div><p class="eyebrow">LATEST RELEASE · R0.73I · 2026-08-30</p><h2 class="route-map-title" id="latest-release-title">选定增益作用量的端点校正与固定窗口边界</h2><p class="route-map-intro">3 项连续体结论闭合，5 个越界推断被严格否定。固定正窗口的规范谱支、匹配作用量、预设种子、固定背景、横向三维、奇性与 Clay 保持 OPEN。</p></div>
        <nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-73i.pdf">阅读最新 R0.73I 研究笔记 →</a><a href="/recap-r0-61-r0-73i.html">125 节累计回顾</a><a href="/notes/">185 篇研究笔记总索引</a><a href="#r073i">查看首页完整 R0.73I 卡片</a></nav>
      </header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73I · 87 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>63 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73I</span></div></div>
    </section>'''
