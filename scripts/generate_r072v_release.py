#!/usr/bin/env python3
"""Generate the fail-closed R0.72V whole-line graph-coercivity release.

For the exact cubic linear scalar model, R0.72V closes a coefficient-uniform
unit-chart theorem, nonhomogeneous H^{-1} whole-line globalization, a separate
all-L2 energy evolution, and fixed-block contraction.  It does not claim
short-time uniformity, periodic transfer, nonlinear closure, or a Clay result.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from pathlib import Path

from generate_r072o_release import (
    assert_clean,
    digest,
    once,
    required,
    section,
    verify_flat_hash_ledger,
)
from generate_r072p_release import assert_mathjax_clean


ROOT = Path(os.environ.get("R072V_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_ID = "fig-r072v-unit-chart-globalization"
FIGURE_RELATIVE = f"figures/r072v-whole-line-transfer/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r072v"

R072U_RELEASE_BASELINE = {
    "latestCompletedRelease": "r072u",
    "siteVersion": "1.34",
    "publicHtmlNoteCount": 171,
    "postR060RecapNodeCount": 111,
    "nextRelease": "r072v",
    "latestReleaseGate": "tests/r072u-local-observability-gate.test.mjs",
    "latestReleasePublicationTest": "tests/r072u-release.test.mjs",
    "postR070APublishedReleaseCount": 73,
    "postR070AFormalSealedReleaseCount": 49,
    "legacyFormalFigureBacklogCount": 24,
}

SOURCE_STAGE_CONTRACT = {
    "release": "r072v",
    "stage": "source-freeze",
    "publicationStatus": "pending-formal-certificate-figure-and-publication",
    "publicCountersAdvanced": False,
    "report": "research/r072v_report-source.md",
    "literatureAudit": "research/r072v_literature_audit.md",
    "gapMatrix": "research/r072v_gap_matrix.md",
    "independentAudit": "research/r072v_independent_audit.md",
    "producer": "research/certificates/r072v/generate_certificate.py",
    "independentProducer": "research/certificates/r072v/independent_recompute.py",
    "comparator": "research/certificates/r072v/validate_certificate.py",
    "certificateDirectory": CERTIFICATE_RELATIVE,
    "figureDirectory": FIGURE_RELATIVE,
    "generator": "scripts/generate_r072v_release.py",
    "translationScript": "scripts/add-r072v-translations.mjs",
    "releaseGate": "tests/r072v-whole-line-graph-gate.test.mjs",
    "publicationTest": "tests/r072v-release.test.mjs",
}

LITERATURE_U_OVERVIEW = (
    "这里没有完成 global caustic image，也没有证明 ED through collision。"
    "R0.72T 进一步固定 exact A2 spacetime germ 与唯一 scaling，核对 quadratic "
    "wrong-model calibration、physical 3/5 回填、combined fixed-f identity、"
    "inviscid mixing 和 CDZE 6/7 barrier；block contraction 与 periodic transfer "
    "仍开放。R0.72U 随后排除 literal spatial-cutoff 的 Poincare 平凡化，闭合无 "
    "temporal cutoff、无 spatial zero trace 的 center-uniform fixed-chart graph "
    "coercivity 与 local actual-solution observability；whole-line tails、boundary "
    "flux、cutoff commutators 与 periodic transfer 仍开放。一般 Navier–Stokes "
    "正则性仍开放。"
)

LITERATURE_V_OVERVIEW = (
    "这里没有完成 global caustic image，也没有证明 ED through collision。"
    "R0.72T 进一步固定 exact A2 spacetime germ 与唯一 scaling，核对 quadratic "
    "wrong-model calibration、physical 3/5 回填、combined fixed-f identity、"
    "inviscid mixing 和 CDZE 6/7 barrier；block contraction 与 periodic transfer "
    "仍开放。R0.72U 随后排除 literal spatial-cutoff 的 Poincare 平凡化，闭合无 "
    "temporal cutoff、无 spatial zero trace 的 center-uniform fixed-chart graph "
    "coercivity 与 local actual-solution observability。R0.72V 再以 coefficient-uniform "
    "unit charts 和 nonhomogeneous H^-1 direct sum 闭合 exact cubic linear scalar "
    "model 的 whole-line graph coercivity；另行构造的 all-L2 energy evolution 给出 "
    "whole-line actual-solution observability 与 fixed-block contraction。常数不对 "
    "T downarrow 0 一致；H5/H7/R9 remainder、periodic transfer、nonlinear/Clay "
    "仍开放。一般 Navier–Stokes 正则性仍开放。"
)


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72V · WHOLE-LINE GRAPH NORM · BLOCK CONTRACTION</div>
        <h1>二参数单位图估计已全球化；<br>精确三次标量模型获得固定块收缩</h1>
        <p class="lead">对 \(P_{c,\sigma}=\partial_t-i\sigma[x^3+6(c+t)x]\)，先证明单位区间上的 graph estimate 对两个低阶多项式系数同时一致，再用互不相交的单位区间和 nonhomogeneous \(H^{-1}(\mathbb R)\) direct sum 得到 whole-line graph coercivity。另行构造的 all-\(L^2\) energy evolution 使 observability 可转成严格 fixed-block contraction。结论只覆盖 exact cubic linear scalar model；短时 \(T\)-一致性为 false，\(H_5,H_7,R_9\)、periodic、nonlinear/Clay 仍开放。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72V exact cubic scalar theorem 完成</span><strong>whole-line graph and fixed-block contraction closed</strong><p>版本 v0.72V · 2026-08-28</p><p>wholeLineGraphCoercivity: CLOSED</p><p>allL2EnergyEvolution: CLOSED</p><p>whole-line block contraction: CLOSED (exact cubic energy model)</p><p>timeLengthUniformity: FALSE</p><p>periodic / Clay: OPEN</p><p>nonlinearNavierStokes: OPEN</p></div>
    </div></header>'''


NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>全直线图范数与固定块收缩闭合；外推边界保持明确</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>CLOSED · WHOLE-LINE GRAPH</strong><p>对每个固定 \(T>0\)，wholeLineGraphCoercivity=CLOSED，常数与碰撞中心 \(c\) 和符号 \(\sigma\) 无关。</p></div>
            <div class="verdict-card true"><strong>CLOSED · ENERGY BLOCK</strong><p>另行构造的 all-\(L^2\) energy evolution 给 wholeLineSolutionObservability=CLOSED 与 wholeLineBlockContraction=CLOSED。</p></div>
            <div class="verdict-card false"><strong>FALSE · SHORT-TIME UNIFORMITY</strong><p>timeLengthUniformity=FALSE；精确测试族给每个可行 graph constant 的下界 \(C_T\gtrsim T^{-1/3}\)。</p></div>
            <div class="verdict-card false"><strong>OPEN · TRANSFER AND NONLINEAR</strong><p>higherOrderRemainderStability=OPEN、periodicTransfer=OPEN、Clay=OPEN；没有 nonlinear Navier--Stokes closure。</p></div>
          </div>
        </section>

        <section id="model"><div class="section-no">01 / Exact model</div><h2>命题只针对 exact cubic linear scalar model</h2>
          <p>固定 \(I=(-T,T)\)、\(T>0\)，考虑</p>
          <div class="equation result">\[P_{c,\sigma}=\partial_t-i\sigma\bigl[x^3+6(c+t)x\bigr],\qquad c\in\mathbb R,\quad\sigma\in\{-1,1\}.\]</div>
          <p>全直线负空间采用 nonhomogeneous \(H^{-1}(\mathbb R)=(H^1(\mathbb R))^*\)。势项与时间导数只要求作为整体 \(P_{c,\sigma}v\) 落入该负空间；不分别施加额外可积性。</p>
        </section>

        <section id="unit-chart"><div class="section-no">02 / Unit-chart theorem</div><h2>单位图常数对两个低阶系数同时一致</h2>
          <p>在 \(J=(-1/2,1/2)\) 上令</p>
          <div class="equation">\[Q_{a,b,\sigma}=\partial_t-i\sigma\bigl[y^3+ay^2+(b+6t)y\bigr].\]</div>
          <p>存在只依赖固定 \(T\) 的 \(C_T^{\rm loc}\)，对全部 \((a,b,\sigma)\) 有</p>
          <div class="equation result">\[\|v\|_{L^2(I\times J)}\le C_T^{\rm loc}\left(\|v_y\|_{L^2(I\times J)}+\|Q_{a,b,\sigma}v\|_{L^2(I;H_D^{-1}(J))}\right).\]</div>
          <p>这条 twoParameterUnitChartCoercivity=CLOSED，不设空间或时间零迹；相对 R0.72U 的关键加强是对 \(a,b\) 同时一致。</p>
        </section>

        <section id="gauge"><div class="section-no">03 / Scalar gauge</div><h2>时间标量规范精确消去二次项的均值</h2>
          <p>对 even normalized probe \(q_0\)，记 \(\mu_2=\int_Jy^2q_0\)。变换 \(w=e^{-i\sigma a\mu_2t}v\) 保持所用各范数，并把势改成</p>
          <div class="equation result">\[\widetilde W_{a,b}=y^3+a(y^2-\mu_2)+(b+6t)y,\qquad\int_J\widetilde W_{a,b}q_0=0.\]</div>
          <p>这是 time-only unitary gauge，不改变空间微分算子。</p>
        </section>

        <section id="coefficients"><div class="section-no">04 / Coefficient compactness</div><h2>有界与逃逸系数两种情形都闭合</h2>
          <p>有界 \((a,b)\) 用 weighted Poincare 与 scalar compactness 排除非零空间常数极限。对 \(\lambda=(a^2+b^2)^{1/2}\to\infty\)，adaptive moment 给</p>
          <div class="equation result">\[B'=i\sigma\bigl[\lambda\kappa_{\alpha,\beta}+\ell_{\alpha,\beta}(t)\bigr]A+E,\qquad \kappa_{\alpha,\beta}\ge\kappa_0>0.\]</div>
          <p>端点只使用 scalar \(A,B\in H^1(I)\) traces。除以 \(\lambda\) 后 endpoint ledger 趋零，不假设 \(\lambda\delta\to0\)，也不使用 full-function \(L^2(J)\)-valued endpoint trace。</p>
        </section>

        <section id="translation"><div class="section-no">05 / Spatial translation</div><h2>每个全直线单位格都落入同一个二参数定理</h2>
          <p>在 \(J_k=(k-1/2,k+1/2)\) 写 \(x=k+y\)。展开给出</p>
          <div class="equation result">\[a_k=3k,\qquad b_{k,c}=3k^2+6c,\qquad k^3+6(c+t)k\ \text{为可消去的时间标量项}.\]</div>
          <p>因此大 \(|k|\)、大 \(|c|\) 以及 \(3k^2\) 与 \(6c\) 的抵消都由同一 coefficient-uniform constant 覆盖。</p>
        </section>

        <section id="direct-sum"><div class="section-no">06 / Negative-Sobolev direct sum</div><h2>互不相交的单位格避免 tail 与 cutoff 损失</h2>
          <p>零延拓把 \(\bigoplus_kH_0^1(J_k)\) 等距嵌入 \(H^1(\mathbb R)\)。对偶化后得到精确不等式</p>
          <div class="equation result">\[\sum_{k\in\mathbb Z}\|g|_{J_k}\|_{H_D^{-1}(J_k)}^2\le\|g\|_{H^{-1}(\mathbb R)}^2.\]</div>
          <p>这是 countable functional-analytic direct sum，不是有限代数证书的机器检查项。</p>
        </section>

        <section id="whole-line"><div class="section-no">07 / Whole-line theorem</div><h2>逐格平方求和直接给全直线 graph coercivity</h2>
          <p>对 maximal distributional graph class 中每个 \(v\)，有</p>
          <div class="equation result">\[\boxed{\|v\|_{L^2(I\times\mathbb R)}\le C_T\left(\|v_x\|_{L^2(I\times\mathbb R)}+\|P_{c,\sigma}v\|_{L^2(I;H^{-1}(\mathbb R))}\right).}\]</div>
          <p>常数与 \(c,\sigma\) 无关，但依赖固定 \(T>0\)。证明不使用 spatial cutoff，因此没有 fixed-origin tail fraction 或 artificial boundary flux。</p>
        </section>

        <section id="solutions"><div class="section-no">08 / Actual solutions</div><h2>graph-class 解获得 whole-line spacetime observability</h2>
          <p>若 \(P_{c,\sigma}u=u_{xx}\)，则 \(\|u_{xx}\|_{H^{-1}}\le\|u_x\|_2\)，所以</p>
          <div class="equation result">\[\boxed{\|u\|_{L^2(I\times\mathbb R)}\le2C_T\|u_x\|_{L^2(I\times\mathbb R)}.}\]</div>
          <p>这是 graph-class actual-solution a priori estimate；单靠 maximal graph membership 不提供时间迹、能量律或 arbitrary-data existence。</p>
        </section>

        <section id="evolution"><div class="section-no">09 / All-L2 evolution</div><h2>时间迹与能量律来自一条独立构造</h2>
          <p>先截断实多项式势，再以 uniform energy bounds、local Aubin--Lions compactness 和 spatial-cutoff energy limit 构造每个 \(L^2\) 初值的唯一</p>
          <div class="equation">\[u\in C(\overline I;L^2(\mathbb R))\cap L^2(I;H^1(\mathbb R)).\]</div>
          <p class="mini-kpi">scope: every (L^2) initial datum</p>
          <p>该构造给 exact energy identity。它是解析证明的一部分，不是 finite certificate 对 compactness、trace、direct sum 或 nonautonomous existence 的 machine check。</p>
        </section>

        <section id="contraction"><div class="section-no">10 / Energy contraction</div><h2>observability 与能量单调性给固定块严格收缩</h2>
          <p>记 \(E(t)=\|u(t)\|_2^2\)。对上述已构造的 energy solution，重排两行 energy ledger 得到</p>
          <div class="equation result">\[\boxed{E(T)\le\frac{C_T^2}{T+C_T^2}E(-T),\qquad\frac{C_T^2}{T+C_T^2}<1.}\]</div>
          <p>这是 wholeLineBlockContraction=CLOSED 的全部范围：固定正时间块、exact cubic linear scalar model、all-\(L^2\) energy data。</p>
        </section>

        <section id="commutator"><div class="section-no">11 / Cutoff commutator</div><h2>全局定理之后，普通 cutoff commutator 可被吸收</h2>
          <div class="equation result">\[2\eta'u_x+\eta''u=\partial_x(2\eta'u)-\eta''u.\]</div>
          <p>该恒等式给直接 \(H^{-1}\) 支付；尺度 \(L\) 足够大时，square partition 的 \(L^{-1}\) 与 \(L^{-2}\) errors 可吸收。它不处理在空间无界增长的 \(H_5,H_7,R_9\) heat-polynomial remainders。</p>
        </section>

        <section id="short-time"><div class="section-no">12 / Short-time boundary</div><h2>固定 \(T\) 的定理不能升级成 \(T\downarrow0\) 一致结论</h2>
          <p>空间尺度 \(L=T^{-1/3}\) 的 exact kernel family 给 \(\|v_x\|_2/\|v\|_2\lesssim T^{1/3}\)，因此</p>
          <div class="equation result">\[C_T\gtrsim T^{-1/3},\qquad0&lt;T\le1.\]</div>
          <p>这里只证明 lower bound；没有 matching upper bound、sharp asymptotic，也没有短块上远离一的 uniform contraction factor。</p>
        </section>

        <section id="certificate"><div class="section-no">13 / Certificate boundary</div><h2>机器证书只封存有限精确代数</h2>
          <p>双路 rational ledger 核对 \(\mu_2=1/44\)、\(\mu_4=3/2288\)、\(\kappa_0=5/6292\)、\(T=1\) 的 sufficient threshold \(693/2\)、translation map 与 contraction ratio。</p>
          <p>weighted Poincare、compactness、scalar endpoint traces、countable \(H^{-1}\) direct sum、all-\(L^2\) evolution existence 与 cutoff-energy limit 仍由数学报告和独立审计证明，不能写成 machine checked。</p>
        </section>

        <section id="literature"><div class="section-no">14 / Literature boundary</div><h2>邻近文献不直接替代非自治 whole-line graph theorem</h2>
          <p>自治 enhanced-dissipation、纯虚半经典势、kinetic Poincare 与局部 subelliptic estimates 提供尺度和方法基线，但没有直接给出本节同时需要的 nonautonomous、whole-line、center-uniform、\(L_t^2H_x^{-1}\)-forced theorem。</p>
          <p>限定的一手检索不构成不存在性、新颖性或优先权证明。</p>
        </section>

        <section id="figure"><div class="section-no">15 / Journal figure</div><h2>正式附图记录 moment floor、translation map 与收缩链</h2>
          <p><img src="/assets/r072v/fig-r072v-unit-chart-globalization.svg" alt="R0.72V unit-chart globalization and exact cubic energy contraction"></p>
          <p><a href="/assets/r072v/fig-r072v-unit-chart-globalization.pdf">下载 PDF</a> · <a href="/assets/r072v/fig-r072v-unit-chart-globalization.png">下载 PNG</a> · <a href="/assets/r072v/fig-r072v-unit-chart-globalization.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">16 / Research value</div><h2>线性模型链闭合，但离一般三维问题仍有多层缺口</h2>
          <p>本节把 local chart theorem 升级为全直线 graph theorem，并为 exact cubic scalar energy evolution 给出严格块收缩。这比 local observability 更接近 collision-block transfer 的可用输入。</p>
          <p>直接 Clay 价值仍低：没有 \(H_5,H_7,R_9\) perturbation stability、periodic transfer、pressure estimate、vortex-stretching control、nonlinear bootstrap 或 continuation criterion。</p>
        </section>

        <section id="next"><div class="section-no">17 / Next gate</div><h2>R0.72W：weighted remainder-stable whole-line theorem</h2>
          <p>下一节先控制 full heat-path expansion 中的 \(H_5,H_7,R_9\) corrections，使吸收常数与 collision rescaling 兼容；该门通过后才检查 periodic exact-heat-path transfer。</p>
        </section>

        <section id="reproduce"><div class="section-no">18 / Reproduction</div><h2>完整证明、边界矩阵、独立审计、证书与正式附图</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072v_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072v_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072v_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072v_independent_audit.md">独立数学审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072v">精确双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072v-whole-line-transfer/fig-r072v-unit-chart-globalization">正式附图包</a> · <a href="/notes/r0-72v.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72v.html">累计回顾</a> · <a href="/recap-r0-61-r0-72v.pdf">累计回顾 PDF</a></p>
        </section>
      </article>'''


HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72W</span><span class="tree-state current">下一检查点</span></div>
              <h3>weighted remainder-stable whole-line transfer</h3>
              <p>为 \(H_5,H_7,R_9\) corrections 建立与 collision rescaling 兼容的 weighted absorption；remainder-stable theorem 闭合后再检查 periodic exact-heat-path transfer。</p>
            </article>'''


HOME_V_CARD = r'''          <div class="task-one" id="r072v" data-release="r072v" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72V · 2026-08-28</p>
            <h3>exact cubic scalar model 的 whole-line graph theorem 与 fixed-block contraction 已闭合</h3>
            <p>coefficient-uniform unit charts 经 spatial translation 与 nonhomogeneous \(H^{-1}\) direct sum 全球化；该证明不需要 spatial cutoff 或 fixed-origin tail fraction。</p>
            <p>另行构造的 all-\(L^2\) energy evolution 提供时间迹和能量律，再由 observability 得到 \(E(T)\le C_T^2(T+C_T^2)^{-1}E(-T)\)。</p>
            <p><strong>结论边界：</strong>&nbsp;wholeLineGraphCoercivity=CLOSED，wholeLineBlockContraction=CLOSED，timeLengthUniformity=FALSE；higherOrderRemainderStability、periodicTransfer 与 Clay 保持 OPEN。</p>
            <p><a href="/notes/r0-72v.html"><strong>阅读 R0.72V 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72v.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072v/fig-r072v-unit-chart-globalization.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072v">查看精确证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072v_report-source.md">查看完整数学报告</a> ·
              <a href="/recap-r0-61-r0-72v.html">阅读累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72W：</strong>&nbsp;证明 weighted remainder-stable whole-line theorem。</p>
          </div>'''


def _validate_source_stage_manifest(release: dict) -> None:
    for key, value in R072U_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72U: {key}")
    if release.get("nextReleaseSourceStage") != SOURCE_STAGE_CONTRACT:
        raise RuntimeError(
            "R0.72V source-stage manifest contract is missing, stale, or has extra fields"
        )


def preflight_release_state() -> None:
    """Reject any stale source/public baseline before a public file is written."""
    release = json.loads(
        (ROOT / "research/release-manifest.json").read_text(encoding="utf-8")
    )
    _validate_source_stage_manifest(release)

    site = json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8"))
    expected_site = {
        "schemaVersion": "research-site-version-v1",
        "version": "1.34",
        "latestRelease": "R0.72U",
        "publicHtmlNoteCount": 171,
        "publishedDate": "2026-08-28",
    }
    if site != expected_site:
        raise RuntimeError("public site-version is not exactly at R0.72U")

    notes = sorted((PUBLIC / "notes").glob("*.html"))
    if len(notes) != 171:
        raise RuntimeError(f"R0.72U preflight expected 171 public HTML notes, got {len(notes)}")
    for relative in (
        "notes/r0-72v.html",
        "notes/r0-72v.pdf",
        "recap-r0-61-r0-72v.html",
        "recap-r0-61-r0-72v.pdf",
    ):
        if (PUBLIC / relative).exists():
            raise RuntimeError(f"R0.72U preflight found premature public output: {relative}")

    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in (
        'data-site-version="1.34"',
        "<strong>171</strong>公开研究笔记",
        "<strong>R0.72U</strong>最新研究节点",
        'aria-label="R0.69P–R0.72U"',
    ):
        if token not in home:
            raise RuntimeError(f"R0.72U home baseline missing token: {token}")
    if 'data-release="r072v"' in home:
        raise RuntimeError("R0.72U home already contains an R0.72V card")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72U">(.*?)</nav>',
        home,
        flags=re.S,
    )
    route_count = 0 if route is None else len(
        re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))
    )
    if route_count != 81:
        raise RuntimeError(f"R0.72U home route expected 81 notes, got {route_count}")

    recap = (PUBLIC / "recap-r0-61-r0-72u.html").read_text(encoding="utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    recap_links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    phases = len(re.findall(r'<article class="phase">', recap))
    if len(recap_links) != 111 or len(set(recap_links)) != 111 or phases != 30:
        raise RuntimeError(
            "R0.72U recap baseline expected 111 unique nodes and 30 phases"
        )

    literature = (PUBLIC / "literature-review.html").read_text(encoding="utf-8")
    if literature.count(LITERATURE_U_OVERVIEW) != 1:
        raise RuntimeError("R0.72U literature route overview is missing or duplicated")
    if literature.count("开放接口 · R0.72V") != 1:
        raise RuntimeError("R0.72U literature must contain exactly one R0.72V open interface")

    inventory = json.loads(
        (ROOT / "research/formal-archive-inventory.json").read_text(encoding="utf-8")
    )
    expected_inventory = {
        "latestPublishedRelease": "r072u",
        "publishedReleaseCount": 73,
        "formalSealedReleaseCount": 49,
        "legacyFormalFigureBacklogCount": 24,
    }
    for key, value in expected_inventory.items():
        if inventory.get(key) != value:
            raise RuntimeError(f"formal archive is not at R0.72U: {key}")
    if (
        len(inventory.get("publishedReleases", [])) != 73
        or len(inventory.get("formalSealedReleases", [])) != 49
        or inventory["publishedReleases"][-1] != "r072u"
        or inventory["formalSealedReleases"][-1] != "r072u"
        or "r072v" in inventory["publishedReleases"]
        or "r072v" in inventory["formalSealedReleases"]
    ):
        raise RuntimeError("formal archive lists are not append-only from R0.72U")


def validate_inputs() -> None:
    for relative in (
        "research/r072v_report-source.md",
        "research/r072v_literature_audit.md",
        "research/r072v_gap_matrix.md",
        "research/r072v_independent_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md",
        f"{CERTIFICATE_RELATIVE}/crosscheck.json",
        f"{FIGURE_RELATIVE}/manifest.json",
        "public/notes/r0-72u.html",
        "public/recap-r0-61-r0-72u.html",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72V release input: {relative}")

    report = (ROOT / "research/r072v_report-source.md").read_text(encoding="utf-8")
    for token in (
        "twoParameterUnitChartCoercivity",
        "wholeLineGraphCoercivity",
        "wholeLineSolutionObservability",
        "wholeLineBlockContraction",
        "cutoffCommutatorAbsorption",
        "timeLengthUniformity",
        "higherOrderRemainderStability",
        "P_{c,\\sigma}",
        "H_D^{-1}",
        "periodicTransfer",
        "Clay",
    ):
        if token not in report:
            raise RuntimeError(f"R0.72V report missing stable token: {token}")

    independent = (ROOT / "research/r072v_independent_audit.md").read_text(encoding="utf-8")
    for token in (
        "coefficient-uniform unit-chart theorem",
        "whole-line direct-sum globalization",
        "all-}L^2\\text{-data energy evolution",
        "energy-solution block contraction",
        "block contraction from graph membership alone",
        "uniformity as }T\\downarrow0",
    ):
        if token not in independent:
            raise RuntimeError(f"R0.72V independent audit missing token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.72V certificate")
    verify_flat_hash_ledger(figure, "R0.72V figure")

    certificate_manifest = json.loads((certificate / "manifest.json").read_text(encoding="utf-8"))
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if certificate_manifest.get("status") != "formal":
        raise RuntimeError("R0.72V certificate is not formal")
    if not re.fullmatch(r"[0-9a-f]{40}", str(certificate_manifest.get("sourceCommit", ""))):
        raise RuntimeError("R0.72V certificate source commit is not frozen")
    if crosscheck.get("status") != "passed" or crosscheck.get("formalSourceReady") is not True:
        raise RuntimeError("R0.72V certificate crosscheck is not formal")
    subprocess.run(
        [sys.executable, str(certificate / "validate_certificate.py"), "--require-formal"],
        cwd=ROOT,
        check=True,
    )

    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("release") != "R0.72V" or manifest.get("figureId") != FIGURE_ID:
        raise RuntimeError("R0.72V figure identity mismatch")
    if (
        manifest.get("status") != "formal"
        or manifest.get("qa", {}).get("status") != "passed"
        or manifest.get("qa", {}).get("visualInspectionExplicit") is not True
    ):
        raise RuntimeError("R0.72V figure is not formally validated")
    subprocess.run(
        [sys.executable, str(figure / "validate.py"), "--require-formal"],
        cwd=ROOT,
        check=True,
    )
    publication = manifest.get("publication", {})
    if publication.get("directory") != "public/assets/r072v":
        raise RuntimeError("R0.72V figure publication directory mismatch")
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = PUBLIC / "assets/r072v" / f"{FIGURE_ID}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72V public {suffix} is absent or not byte-identical")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72u.html").read_text(encoding="utf-8")
    for index, (pattern, value) in enumerate((
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72V：exact cubic linear scalar model 的 whole-line graph coercivity、all-L2 energy evolution 与 fixed-block contraction。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72V｜whole-line graph coercivity and block contraction">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="whole-line graph 与 fixed-block contraction 已闭合；T-uniform、higher-order remainder、periodic 与 nonlinear/Clay 仍开放。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072v/fig-r072v-unit-chart-globalization.png">'),
        (r'<title>.*?</title>', '<title>R0.72V｜whole-line graph coercivity and block contraction</title>'),
    )):
        html = section(html, pattern, value, f"U note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.34", "/i18n-en.js?v=1.35", "V note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#model">模型</a><a href="#unit-chart">单位图</a><a href="#gauge">gauge</a><a href="#coefficients">系数</a><a href="#translation">平移</a><a href="#direct-sum">direct sum</a><a href="#whole-line">全直线</a><a href="#solutions">真实解</a><a href="#evolution">energy evolution</a><a href="#contraction">收缩</a><a href="#commutator">commutator</a><a href="#short-time">短时边界</a><a href="#certificate">证书</a><a href="#literature">文献</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "U note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "U note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · direct decision</a></li><li><a href="#model">01 · exact model</a></li><li><a href="#unit-chart">02 · unit-chart theorem</a></li><li><a href="#gauge">03 · scalar gauge</a></li><li><a href="#coefficients">04 · coefficient compactness</a></li><li><a href="#translation">05 · spatial translation</a></li><li><a href="#direct-sum">06 · H^-1 direct sum</a></li><li><a href="#whole-line">07 · whole-line theorem</a></li><li><a href="#solutions">08 · actual solutions</a></li><li><a href="#evolution">09 · all-L2 evolution</a></li><li><a href="#contraction">10 · energy contraction</a></li><li><a href="#commutator">11 · cutoff commutator</a></li><li><a href="#short-time">12 · short-time boundary</a></li><li><a href="#certificate">13 · certificate</a></li><li><a href="#literature">14 · literature</a></li><li><a href="#figure">15 · journal figure</a></li><li><a href="#value">16 · value</a></li><li><a href="#next">17 · R0.72W</a></li><li><a href="#reproduce">18 · reproduction</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "U note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "U note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72V · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "U note footer")
    assert_clean(html, "R0.72V note")
    assert_mathjax_clean(html, "R0.72V note")
    (PUBLIC / "notes/r0-72v.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72u.html").read_text(encoding="utf-8")
    html = required(html, "/i18n-en.js?v=1.34", "/i18n-en.js?v=1.35", "V recap i18n")
    for label, pattern, value in (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72V 的 112 个节点；最新一节闭合 exact cubic scalar whole-line graph theorem 与 fixed-block contraction。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.72V｜R0.60 之后的研究回顾">'),
        ("og desc", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="三十一个阶段、112 个节点：从约化递推到 exact cubic whole-line contraction。">'),
        ("title", r'<title>.*?</title>', '<title>R0.61–R0.72V｜R0.60 之后的研究回顾</title>'),
    ):
        html = section(html, pattern, value, "V recap " + label)
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.72V · 2026-08-28</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，保留 R0.61 到 R0.72V 的 112 个研究节点。R0.72V 以 coefficient-uniform unit charts 和 nonhomogeneous H^-1 direct sum 闭合 exact cubic linear scalar model 的 whole-line graph theorem；另行构造的 all-L2 energy evolution 给出 fixed-block contraction。节点状态只描述声明范围内的证据，不把线性标量结果写成 periodic、nonlinear 或 Clay 结论。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72V</strong><p>收录节点：112</p><p>回顾截止时公开笔记：172</p><p>回顾截止节点：R0.72V</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "V recap hero")
    html = required(html, "02 · 111 节完整索引", "02 · 112 节完整索引", "V recap toc")
    html = required(html, "01 · 三十个研究阶段", "01 · 三十一个研究阶段", "V recap phase toc")
    html = required(html, "R0.60 之后的路线分成三十个阶段", "R0.60 之后的路线分成三十一个阶段", "V recap phase heading")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2>
          <div class="metrics"><div class="metric"><strong>112</strong><span>R0.61–R0.72V 研究节点</span></div><div class="metric"><strong>74</strong><span>R0.70A–R0.72V 已公开版本</span></div><div class="metric"><strong>50</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div>
          <p>R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.70A–R0.72V 的 74 个版本已经公开，其中 50 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。</p>
        </section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "V recap result")
    new_phase = r'''            <article class="phase"><h3>R0.72V · unit-chart globalization 与 exact cubic block contraction</h3>
              <p>对 \((a,b)\) 一致的 unit-chart theorem、spatial translation 与 nonhomogeneous \(H^{-1}\) direct sum 给 wholeLineGraphCoercivity=CLOSED。</p>
              <p>另行构造的 all-L2 energy evolution 给 wholeLineBlockContraction=CLOSED；graph membership alone 不提供时间迹或能量律。</p>
              <p>timeLengthUniformity=FALSE。\(H_5,H_7,R_9\)、periodicTransfer、nonlinear Navier--Stokes 与 Clay 保持 OPEN；R0.72W 处理 weighted higher-order remainders。</p>
              <div class="links"><a href="/notes/r0-72v.html">R0.72V</a><a href="/assets/r072v/fig-r072v-unit-chart-globalization.pdf">R0.72V 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072v">R0.72V 证书</a></div></article>
'''
    html = once(html, "          </div>\n        </section>\n\n        <section id=\"node-index\">", new_phase + "          </div>\n        </section>\n\n        <section id=\"node-index\">", "U recap phase")
    html = required(html, "R0.61–R0.72U 的 111 节公开笔记", "R0.61–R0.72V 的 112 节公开笔记", "V recap node title")
    node_u = '            <span class="node-ref"><a href="/notes/r0-72u.html">R0.72U</a><span class="node-state kind-closed">闭</span></span>\n'
    node_v = '            <span class="node-ref"><a href="/notes/r0-72v.html">R0.72V</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_u, node_u + node_v, "V recap node")
    retained = r'''            <li>R0.72V 的 exact cubic scalar theorem：whole-line graph coercivity、all-L2 energy evolution 与 fixed-block contraction 已闭合；短时 T-uniformity 为 false。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "U recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>exact cubic scalar collision block 已闭合；一般三维问题没有被外推</h2><p>不能把 112 个节点或 74 个公开版本解释成 Clay 问题完成比例。严格增量是 whole-line graph theorem、另行构造的 all-L2 energy evolution 与 fixed-block contraction。</p></section>''', "V recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72W 处理 weighted H5/H7/R9 remainder stability</h2><p>先证明与 collision rescaling 兼容的 weighted whole-line absorption，再检查 periodic exact-heat-path transfer。</p></section>''', "V recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.72V 的 74 节已公开；50 节完整封存；24 节旧档待回补。</p><p>timeLengthUniformity=FALSE；higherOrderRemainderStability、periodicTransfer、nonlinear Navier--Stokes 与 Clay 保持 OPEN。</p></section>''', "V recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72u.html">保留 R0.72U 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72v.html">打开最新节点 R0.72V</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072v">查看 R0.72V 精确证书</a> · <a href="/assets/r072v/fig-r072v-unit-chart-globalization.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72v.pdf">下载同步 PDF</a></p><p>完整节点索引保留历史编号；状态标签只描述证据类型。</p></section>''', "U recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72V 回顾 · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "U recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 112 or len(set(links)) != 112:
        raise RuntimeError(f"recap node index expected 112 unique links, got {len(links)}/{len(set(links))}")
    phases = re.findall(r'<article class="phase">', html)
    if len(phases) != 31:
        raise RuntimeError(f"recap expected 31 phases, got {len(phases)}")
    assert_clean(html, "R0.72V recap")
    assert_mathjax_clean(html, "R0.72V recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-72v.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.34"', 'data-site-version="1.35"'),
        ("/i18n-en.js?v=1.34", "/i18n-en.js?v=1.35"),
        ("/site-refresh.js?v=1.34", "/site-refresh.js?v=1.35"),
        ("<strong>v1.34</strong>网页版本", "<strong>v1.35</strong>网页版本"),
        ("<strong>171</strong>公开研究笔记", "<strong>172</strong>公开研究笔记"),
        ("<strong>R0.72U</strong>最新研究节点", "<strong>R0.72V</strong>最新研究节点"),
        ("Research topology · R0.1–R0.72U", "Research topology · R0.1–R0.72V"),
        ("R0.70A–R0.72U：73 节已公开，49 节完整封存", "R0.70A–R0.72V：74 节已公开，50 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72U</span>', '<span class="route-range">R0.69P–R0.72V</span>'),
        ('aria-label="R0.69P–R0.72U"', 'aria-label="R0.69P–R0.72V"'),
        ("展开 81 篇公开笔记", "展开 82 篇公开笔记"),
        ("本站 R0.69P–R0.72U 路线", "本站 R0.69P–R0.72V 路线"),
        ("综述 v1.34 · 2026-08-28", "综述 v1.35 · 2026-08-28"),
        ("上次综述 v1.33 · 2026-08-28", "上次综述 v1.34 · 2026-08-28"),
        ("/recap-r0-61-r0-72u.html", "/recap-r0-61-r0-72v.html"),
        ("/recap-r0-61-r0-72u.pdf", "/recap-r0-61-r0-72v.pdf"),
    ):
        html = required(html, old, new, "U home " + old)
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.72V 已闭合 exact cubic scalar model 的 whole-line graph theorem 与 fixed-block contraction；下一关是 weighted H5/H7/R9 remainder stability。</span></div>', "V home focus")
    link_t = '<a class="milestone" href="/notes/r0-72u.html">R0.72U</a>'
    html = once(html, link_t, link_t + '\n                  <a class="milestone" href="/notes/r0-72v.html">R0.72V</a>', "U home route link")
    route_u = r'''              <p>R0.72V 以 coefficient-uniform unit charts、spatial translation 与 nonhomogeneous H^-1 direct sum 闭合 exact cubic scalar whole-line graph theorem；另行构造的 all-L2 energy evolution 给 fixed-block contraction。T-uniformity 为 false，H5/H7/R9、periodic 与 nonlinear/Clay 仍开放。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_u + '              <details class="tree-notes" open>', "U home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "U home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72V · 2026-08-28</p>
            <h3>R0.60 recap 之后的累计回顾收录 112 个节点；全站现有 172 篇公开研究笔记</h3>
            <p>累计回顾现分三十一个问题阶段，并给出 R0.61–R0.72V 的完整逐节点索引。R0.72V 增加 whole-line graph coercivity、all-L2 energy evolution 与 fixed-block contraction。</p>
            <p>R0.70A–R0.72V 共 74 个版本已公开；50 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;exact cubic scalar block 已闭合；T-uniform、higher-order remainder、periodic 与 nonlinear/Clay 保持开放。</p>
            <p><a href="/recap-r0-61-r0-72v.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72v.pdf">下载同步 PDF</a></p>
          </div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "U home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_V_CARD + '\n        </section>\n\n      </article>', "V home card")
    if html.count('data-release="r072v"') != 1:
        raise RuntimeError("home must contain exactly one R0.72V card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72V">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 82:
        raise RuntimeError("home current-route index must contain 82 note links")
    assert_clean(html, "R0.72V home")
    assert_mathjax_clean(html, "R0.72V home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.34", "/i18n-en.js?v=1.35"),
        ("本站 R0.69P–R0.72U 只列为研究笔记", "本站 R0.69P–R0.72V 只列为研究笔记"),
        ("/recap-r0-61-r0-72u.html", "/recap-r0-61-r0-72v.html"),
        ("文献综述 v1.34 · 2026-08-28", "文献综述 v1.35 · 2026-08-28"),
        ("累计回顾与 111 节索引", "累计回顾与 112 节索引"),
        ("打开 111 节完整索引", "打开 112 节完整索引"),
    ):
        html = required(html, old, new, "U literature " + old)
    html = once(
        html,
        LITERATURE_U_OVERVIEW,
        LITERATURE_V_OVERVIEW,
        "V literature overview",
    )
    old_open = '<div class="route-step pause"><header><b>开放接口 · R0.72V</b><strong>whole-line tail and commutator transfer</strong></header><p>控制 chart tails、boundary flux 与 spatial cutoff commutators，再检查 periodic exact-heat-path transfer。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.72V</b><strong>coefficient-uniform unit charts and whole-line graph coercivity</strong></header><p>nonhomogeneous H^-1 direct sum 给 exact cubic scalar whole-line graph theorem；另行构造的 all-L2 energy evolution 给 fixed-block contraction。<a href="/notes/r0-72v.html">研究笔记</a> <a href="/recap-r0-61-r0-72v.html">当前累计回顾</a> <a href="#r072v-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72W</b><strong>weighted H_5/H_7/R_9 remainder stability</strong></header><p>证明与 collision rescaling 兼容的 weighted whole-line absorption，再检查 periodic exact-heat-path transfer。</p></div>'''
    html = once(html, old_open, new_steps, "U literature route")
    boundary = r'''

          <h3 id="r072v-boundary">R0.72V 的 whole-line theorem 与文献边界</h3>
          <p>邻近自治 ED、纯虚半经典势、kinetic Poincare 与局部 subelliptic estimates 都不直接给 nonautonomous、whole-line、center-uniform、L2_t H^-1_x-forced theorem。限定检索不构成新颖性或优先权证明。</p>
          <div class="boundary"><strong>R0.72V 的主张边界</strong><p>wholeLineGraphCoercivity=CLOSED，allL2EnergyEvolution=CLOSED，wholeLineBlockContraction=CLOSED，timeLengthUniformity=FALSE。higherOrderRemainderStability=OPEN，periodicTransfer=OPEN，nonlinearNavierStokes=OPEN，Clay=OPEN。</p></div>'''
    match = re.search(r'(<h3 id="r072u-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("U literature expected R0.72U boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "U literature boundary")
    assert_clean(html, "R0.72V literature")
    assert_mathjax_clean(html, "R0.72V literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    notes = len(list((PUBLIC / "notes").glob("*.html")))
    if notes != 172:
        raise RuntimeError(f"expected 172 public HTML notes after R0.72V, got {notes}")

    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    release.update({
        "latestCompletedRelease": "r072v",
        "siteVersion": "1.35",
        "publicHtmlNoteCount": 172,
        "postR060RecapNodeCount": 112,
        "nextRelease": "r072w",
        "latestReleaseGate": "tests/r072v-whole-line-graph-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072v-release.test.mjs",
        "postR070APublishedReleaseCount": 74,
        "postR070AFormalSealedReleaseCount": 50,
        "legacyFormalFigureBacklogCount": 24,
    })
    del release["nextReleaseSourceStage"]
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.34", "R0.72U", 171):
        raise RuntimeError("site-version is not at R0.72U")
    site.update({"version": "1.35", "latestRelease": "R0.72V", "publicHtmlNoteCount": 172, "publishedDate": "2026-08-28"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    current = (
        inventory.get("latestPublishedRelease"),
        inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"),
        inventory.get("legacyFormalFigureBacklogCount"),
    )
    if current != ("r072u", 73, 49, 24):
        raise RuntimeError("formal archive inventory is not at R0.72U")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072u" or "r072v" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72U")
        inventory[key].append("r072v")
    inventory.update({
        "latestPublishedRelease": "r072v",
        "publishedReleaseCount": 74,
        "formalSealedReleaseCount": 50,
        "legacyFormalFigureBacklogCount": 24,
    })
    if len(inventory["publishedReleases"]) != 74 or len(inventory["formalSealedReleases"]) != 50:
        raise RuntimeError("formal archive count mismatch after R0.72V")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def main() -> None:
    preflight_release_state()
    validate_inputs()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in (
        "research-review.html",
        "literature-review.html",
        "notes/r0-72v.html",
        "recap-r0-61-r0-72v.html",
    ):
        content = (PUBLIC / relative).read_text(encoding="utf-8")
        assert_clean(content, relative)
        assert_mathjax_clean(content, relative, check_naked=False)
    print(json.dumps({
        "release": "R0.72V",
        "siteVersion": "1.35",
        "notes": 172,
        "recapNodes": 112,
        "published": 74,
        "formalSealed": 50,
        "legacyBacklog": 24,
        "phases": 31,
        "routeNotes": 82,
        "next": "R0.72W",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
