#!/usr/bin/env python3
"""Generate the fail-closed R0.72U bounded-chart observability release.

R0.72U closes an uncut graph-coercivity theorem on each fixed spatial chart,
uniformly in the time-interval center.  It does not claim a whole-line block
contraction, a periodic transfer, or a Navier--Stokes regularity theorem.
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


ROOT = Path(os.environ.get("R072U_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_ID = "fig-r072u-two-moment-coercivity"
FIGURE_RELATIVE = f"figures/r072u-local-observability/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r072u"

R072T_RELEASE_BASELINE = {
    "latestCompletedRelease": "r072t",
    "siteVersion": "1.33",
    "publicHtmlNoteCount": 170,
    "postR060RecapNodeCount": 110,
    "nextRelease": "r072u",
    "latestReleaseGate": "tests/r072t-a2-spacetime-gate.test.mjs",
    "latestReleasePublicationTest": "tests/r072t-release.test.mjs",
    "postR070APublishedReleaseCount": 72,
    "postR070AFormalSealedReleaseCount": 48,
    "legacyFormalFigureBacklogCount": 24,
}

SOURCE_STAGE_CONTRACT = {
    "release": "r072u",
    "stage": "source-freeze",
    "publicationStatus": "pending-formal-certificate-figure-and-publication",
    "publicCountersAdvanced": False,
    "report": "research/r072u_report-source.md",
    "literatureAudit": "research/r072u_literature_audit.md",
    "gapMatrix": "research/r072u_gap_matrix.md",
    "independentAudit": "research/r072u_independent_audit.md",
    "producer": "research/certificates/r072u/generate_certificate.py",
    "independentProducer": "research/certificates/r072u/independent_recompute.py",
    "comparator": "research/certificates/r072u/validate_certificate.py",
    "certificateDirectory": CERTIFICATE_RELATIVE,
    "figureDirectory": FIGURE_RELATIVE,
    "generator": "scripts/generate_r072u_release.py",
    "translationScript": "scripts/add-r072u-translations.mjs",
    "releaseGate": "tests/r072u-local-observability-gate.test.mjs",
    "publicationTest": "tests/r072u-release.test.mjs",
}

LITERATURE_T_OVERVIEW = (
    "这里没有完成 global caustic image，也没有证明 ED through collision。"
    "R0.72T 进一步固定 exact A2 spacetime germ 与唯一 scaling，核对 quadratic "
    "wrong-model calibration、physical 3/5 回填、combined fixed-f identity、"
    "inviscid mixing 和 CDZE 6/7 barrier；block contraction 与 periodic transfer "
    "仍开放。一般 Navier–Stokes 正则性仍开放。"
)

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


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72U · LOCAL GRAPH COERCIVITY · TWO-MOMENT PROOF</div>
        <h1>固定空间图上的未截断估计已闭合；<br>全直线传递仍待证明</h1>
        <p class="lead">我先排除了原先的字面 cutoff 目标：若 \(\chi u\) 在 \(X\) 方向紧支撑，普通 Poincare inequality 已经控制 \(\|\chi u\|_2\)，不含 A2 信息。改正后的命题不设时间 cutoff，也不设空间零迹。对 \(P_{c,\sigma}=\partial_S-i\sigma[X^3+6(c+S)X]\)，固定有界空间图上的 graph estimate 对中心 \(c\) 一致成立，并直接给出局部真实解 observability。wholeLineBlockContraction、periodicTransfer 与 Clay 问题仍开放。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72U bounded-chart theorem 完成</span><strong>uncut local coercivity closed</strong><p>版本 v0.72U · 2026-08-28</p><p>literal spatial cutoff: Poincare-trivial</p><p>centerUniformLocalGraphCoercivity: CLOSED</p><p>localSolutionObservability: CLOSED</p><p>wholeLineBlockContraction: OPEN</p><p>periodicTransfer / Clay: OPEN</p></div>
    </div></header>'''


NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>非平凡局部命题闭合；全局耗散命题没有被偷换</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>CLOSED · UNCUT GRAPH ESTIMATE</strong><p>在固定 \(I\times J\) 上，不设时间零迹或空间 Dirichlet 迹，graph norm 以对中心 \(c\) 一致的常数控制 \(L^2\) norm。</p></div>
            <div class="verdict-card true"><strong>CLOSED · LOCAL SOLUTIONS</strong><p>对 \(P_{c,\sigma}u=u_{XX}\)，负范数残差由 \(\|u_X\|_2\) 支付，得到 uncut local solution observability。</p></div>
            <div class="verdict-card true"><strong>NO-GO · LITERAL CUTOFF</strong><p>若 \(\chi u\in H^1_0(J)\)，普通空间 Poincare 已证明原式；这个版本不能作为 A2 mixing certificate。</p></div>
            <div class="verdict-card false"><strong>OPEN · WHOLE LINE</strong><p>局部定理没有控制 chart tails、边界 flux 或 cutoff commutators，不能直接写成 whole-line block contraction。</p></div>
          </div>
        </section>

        <section id="cutoff"><div class="section-no">01 / Literal cutoff audit</div><h2>空间紧支撑版本被普通 Poincare 完全覆盖</h2>
          <p>如果 \(v=\chi u\) 在 \(X\) 方向紧支撑于 \(J\)，那么 \(v\in H^1_0(J)\)，逐时已有</p>
          <div class="equation result">\[\|v\|_{L^2(J)}\le\frac{|J|}{\pi}\|v_X\|_{L^2(J)}.\]</div>
          <p>因此把 \(\|P_{c,\sigma}v\|_{H^{-1}}\) 加到右端不会增加数学内容。R0.72U 不把这条真但平凡的式子计为 observability 结果。</p>
        </section>

        <section id="theorem"><div class="section-no">02 / Corrected theorem</div><h2>未截断 fixed-chart graph estimate 对 interval center 一致</h2>
          <p>令 \(I=(-T,T)\)、\(J=(-R,R)\)，并取 \(H_D^{-1}(J)=(H^1_0(J))^*\)。对任意 \(c\in\mathbb R\)、\(\sigma=\pm1\) 及</p>
          <div class="equation">\[v\in L^2(I;H^1(J)),\qquad P_{c,\sigma}v\in L^2(I;H_D^{-1}(J)),\]</div>
          <p>存在只依赖 \(R,T\) 的有限常数 \(C_{R,T}\)，使</p>
          <div class="equation result">\[\boxed{\|v\|_{L^2(I\times J)}\le C_{R,T}\left[\|v_X\|_{L^2(I\times J)}+\|P_{c,\sigma}v\|_{L^2(I;H_D^{-1}(J))}\right].}\]</div>
          <p>这里没有时间 cutoff，没有空间零迹，常数也不随 \(c\) 改变。定理只断言有限性与一致性，不给数值最优常数。</p>
        </section>

        <section id="trace"><div class="section-no">03 / Graph-space trace</div><h2>不能使用 \(L^2_X\) endpoint shortcut；两个 scalar traces 足够</h2>
          <p>graph space 只直接给 \(v\in C(\overline I;H_D^{-1})\)，并不保证 \(v\in C(\overline I;L^2)\)。因此用 \(\|v(\pm T)\|_{L^2}\) 的证明是不合法的。</p>
          <p>选取 even \(\rho\in C_c^\infty(J)\)，则 \(A(S)=\langle v,\rho\rangle\) 与 \(B(S)=\langle v,X\rho\rangle\) 都属于 \(H^1(I)\)。证明只对这两个标量做端点分部积分。</p>
        </section>

        <section id="poincare"><div class="section-no">04 / Poincare modulo constants</div><h2>空间导数把函数压到一个时间标量</h2>
          <p>令 \(m(S)\) 是 \(v(S,\cdot)\) 的空间均值。固定图上的 mean-zero Poincare 给出</p>
          <div class="equation result">\[\|v-m\|_{L^2(I\times J)}\le C_R\|v_X\|_{L^2(I\times J)}.\]</div>
          <p>由于 \(\rho\) even 且归一化，\(A=m+O(\|v_X\|)\)，而 odd moment \(B=O(\|v_X\|)\)。所以只须排除非零的近常数模。</p>
        </section>

        <section id="moments"><div class="section-no">05 / Two scalar moments</div><h2>大中心项在两个 moment equations 中形成闭合交换</h2>
          <p>记 \(L=6\sigma c\)、\(\mu_2=\int_JX^2\rho\,dX>0\)。配对方程后得到</p>
          <div class="equation result">\[A'=iLB+E_0,\qquad B'=iL\mu_2A+iLF_2+E_1,\]</div>
          <p>其中 \(B,F_2,E_0\) 都由 graph defect 控制，\(E_1\) 在 unit normalization 下有界。第一式阻止 \(A\) 以任意快的频率振荡；第二式把 escaping-center 强度送回 \(A\)。</p>
        </section>

        <section id="bounded"><div class="section-no">06 / Bounded centers</div><h2>紧性极限不允许非零空间常数模</h2>
          <p>若 \(c_n\) 有界且 graph defect 趋零，Poincare reduction 与 \(A_n\) 的 \(H^1(I)\) 紧性给出强极限 \(m(S)\)。极限方程是</p>
          <div class="equation">\[m'-i\sigma[X^3+6(c_*+S)X]m=0.\]</div>
          <p>对 \(X\) 微分后，\([3X^2+6(c_*+S)]m=0\)。该多项式不可能在非退化区间 \(J\) 上恒为零，因此 \(m=0\)，与 unit normalization 矛盾。</p>
        </section>

        <section id="escaping"><div class="section-no">07 / Escaping centers</div><h2>大 \(|c|\) 不破坏常数，反而进入 coercive moment identity</h2>
          <p>对 \(|c|\to\infty\)，积分 \(B'\overline A\) 并使用两条 moment equations，得到主项 \(|L|\mu_2\|A\|_2^2\) 与 \(|L|\|B\|_2^2\)。除端点项外，其余误差除以 \(|L|\) 后都趋零。</p>
          <div class="equation result">\[\frac{|B(S)A(S)|}{|L|}\le C\left(\delta+\sqrt{\frac{\delta}{|L|}}\right),\qquad S=\pm T.\]</div>
          <p>这里 \(\delta\) 是归一化 graph defect。该界不要求 \(|c|\delta\to0\)，所以 escaping-center 情形真正闭合。</p>
        </section>

        <section id="endpoint"><div class="section-no">08 / Endpoint correction</div><h2>端点不消失；标量 \(H^1\) trace 精确支付</h2>
          <p>分部积分保留 \([B\overline A]_{-T}^{T}\)。证明使用 scalar inequality</p>
          <div class="equation">\[|h(-T)|^2+|h(T)|^2\le C_T\left(\|h\|_2^2+\|h\|_2\|h'\|_2\right),\qquad h\in H^1(I).\]</div>
          <p>这一步既不设 \(A(\pm T)=B(\pm T)=0\)，也不调用不存在的 \(L^2_X\)-valued trace。</p>
        </section>

        <section id="discriminator"><div class="section-no">09 / Nontriviality check</div><h2>未截断定理能区分 A2 模型与零 transport</h2>
          <p>如果把整个乘法势删除，使算子退化为 \(\partial_S\)，未截断函数 \(v\equiv1\) 满足 \(v_X=0\)、\(\partial_Sv=0\)，graph coercivity 立即失败。相反，时间 compact cutoff 会产生 cutoff derivative，仍可能满足普通 parabolic Poincare。这个对照说明真正有内容的是 uncut theorem。</p>
        </section>

        <section id="solutions"><div class="section-no">10 / Actual solutions</div><h2>局部 evolving-solution observability 不再需要 endpoint patch</h2>
          <p>对 \(P_{c,\sigma}u=u_{XX}\)，有 \(\|u_{XX}\|_{H_D^{-1}}\le\|u_X\|_2\)。因此定理直接给</p>
          <div class="equation result">\[\boxed{\|u\|_{L^2(I\times J)}\le2C_{R,T}\|u_X\|_{L^2(I\times J)}.}\]</div>
          <p>这是对 interval center 一致的 fixed-chart、all-start、actual-solution estimate；它不是 frozen-profile identity。</p>
        </section>

        <section id="global"><div class="section-no">11 / Local-to-global boundary</div><h2>局部 mass control 还没有支付 tails 与 boundary flux</h2>
          <p><strong>wholeLineBlockContraction=OPEN</strong>：定理只控制 \(I\times(-R,R)\)。全直线质量可以留在 chart 外，局部能量还含 \(2\operatorname{Re}[u_X\overline u]_{\partial J}\)。</p>
          <p><strong>periodicTransfer=OPEN</strong>：尚未吸收 spatial cutoff commutators、\(H_5,H_7,R_9\) remainders，也没有把非周期 polynomial chart 转回 exact periodic heat path。</p>
        </section>

        <section id="certificate"><div class="section-no">12 / Certificate</div><h2>机器证书只核对有限精确 ledger</h2>
          <p>双路证书在 rational probe 假设 \(J\supset[-1,1]\) 下核对 moments \(\mu_2,\mu_4\)。large-center threshold \(27/13\) 与 fixed-gauge floor \(4/5\) 都是 \(T=1\) 的校准值；它们不是任意时间窗常数，也不是 functional theorem 的机器证明。</p>
          <p>weighted Poincare reduction、compactness、bounded/escaping-center contradiction、endpoint trace 与 local-solution corollary 由完整数学报告和独立审计支持。证书不枚举未知最优常数，也不声称 whole-line contraction。</p>
        </section>

        <section id="literature"><div class="section-no">13 / Literature boundary</div><h2>Hörmander、kinetic Poincare 与 stationary ED 只作为邻近基线</h2>
          <p>Hörmander 与 Bedrossian–Liss 支持局部 graph regularity；Albritton–Armstrong–Mourrat–Novack 给 kinetic strong/weak norm 先例；Albritton–Beekie–Novack 给 stationary cubic \(1/5\) benchmark。它们都不直接给本节 uncut、center-uniform、collision-crossing estimate。</p>
          <p>限定一手检索没有找到可直接替代本节证明的定理。这个 bounded-search absence 不是不存在性、新颖性或优先权证明。</p>
        </section>

        <section id="figure"><div class="section-no">14 / Journal figure</div><h2>正式附图记录两条 moments 与局部—全局边界</h2>
          <p><img src="/assets/r072u/fig-r072u-two-moment-coercivity.svg" alt="R0.72U two-moment coercivity and local-to-global boundary"></p>
          <p><a href="/assets/r072u/fig-r072u-two-moment-coercivity.pdf">下载 PDF</a> · <a href="/assets/r072u/fig-r072u-two-moment-coercivity.png">下载 PNG</a> · <a href="/assets/r072u/fig-r072u-two-moment-coercivity.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">15 / Research value</div><h2>本节把 local model 的 all-start solution observability 闭合</h2>
          <p>R0.72U 的严格增量是：排除 cutoff 平凡化，证明 arbitrary-trace fixed-chart graph coercivity，对 escaping centers 保持统一，并把它转成真实解的 local observability。</p>
          <p>对 Clay 问题的直接价值仍低。结果是线性局部模型定理，不是一般三维 continuation estimate，也不控制全空间 vortex stretching。</p>
        </section>

        <section id="next"><div class="section-no">16 / Next gate</div><h2>R0.72V：whole-line tail 与 commutator transfer</h2>
          <p>下一节要证明对中心一致的 tail tightness，并控制空间 partition 产生的 flux 与 commutators。只有把局部 observability 拼成全直线 block estimate 后，才可检查 periodic exact-heat-path transfer。</p>
        </section>

        <section id="reproduce"><div class="section-no">17 / Reproduction</div><h2>完整证明、文献审计、独立审计、证书与正式附图</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072u_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072u_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072u_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072u_independent_audit.md">独立数学审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072u">精确双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072u-local-observability/fig-r072u-two-moment-coercivity">正式附图包</a> · <a href="/notes/r0-72u.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72u.html">累计回顾</a> · <a href="/recap-r0-61-r0-72u.pdf">累计回顾 PDF</a></p>
        </section>
      </article>'''


HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72V</span><span class="tree-state current">下一检查点</span></div>
              <h3>whole-line tail and cutoff-commutator transfer</h3>
              <p>从 fixed-chart observability 出发，控制全直线 tails、chart boundary flux 与 spatial cutoff commutators；全直线 block estimate 闭合前不进入 periodic transfer。</p>
            </article>'''


HOME_U_CARD = r'''          <div class="task-one" id="r072u" data-release="r072u" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72U · 2026-08-28</p>
            <h3>未截断 fixed-chart graph coercivity 已对所有 interval centers 闭合</h3>
            <p>字面 spatial-cutoff target 被普通 Poincare inequality 完全覆盖，因此不计为 A2 observability。改正后的命题不设时间 cutoff，也不设空间零迹。</p>
            <p>even test function 产生两个 scalar moments。bounded centers 用 compactness，escaping centers 用 \(B'\overline A\) identity 与 scalar endpoint traces；证明不假设 \(L^2_X\)-valued endpoint trace。</p>
            <p><strong>结论边界：</strong>&nbsp;localSolutionObservability=CLOSED；wholeLineBlockContraction、periodicTransfer 与 Clay 保持 OPEN。</p>
            <p><a href="/notes/r0-72u.html"><strong>阅读 R0.72U 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72u.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072u/fig-r072u-two-moment-coercivity.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072u">查看精确证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072u_report-source.md">查看完整数学报告</a> ·
              <a href="/recap-r0-61-r0-72u.html">阅读累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72V：</strong>&nbsp;处理 whole-line tail 与 cutoff-commutator transfer。</p>
          </div>'''


def _validate_source_stage_manifest(release: dict) -> None:
    for key, value in R072T_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72T: {key}")
    if release.get("nextReleaseSourceStage") != SOURCE_STAGE_CONTRACT:
        raise RuntimeError(
            "R0.72U source-stage manifest contract is missing, stale, or has extra fields"
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
        "version": "1.33",
        "latestRelease": "R0.72T",
        "publicHtmlNoteCount": 170,
        "publishedDate": "2026-08-28",
    }
    if site != expected_site:
        raise RuntimeError("public site-version is not exactly at R0.72T")

    notes = sorted((PUBLIC / "notes").glob("*.html"))
    if len(notes) != 170:
        raise RuntimeError(f"R0.72T preflight expected 170 public HTML notes, got {len(notes)}")
    for relative in (
        "notes/r0-72u.html",
        "notes/r0-72u.pdf",
        "recap-r0-61-r0-72u.html",
        "recap-r0-61-r0-72u.pdf",
    ):
        if (PUBLIC / relative).exists():
            raise RuntimeError(f"R0.72T preflight found premature public output: {relative}")

    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in (
        'data-site-version="1.33"',
        "<strong>170</strong>公开研究笔记",
        "<strong>R0.72T</strong>最新研究节点",
        'aria-label="R0.69P–R0.72T"',
    ):
        if token not in home:
            raise RuntimeError(f"R0.72T home baseline missing token: {token}")
    if 'data-release="r072u"' in home:
        raise RuntimeError("R0.72T home already contains an R0.72U card")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72T">(.*?)</nav>',
        home,
        flags=re.S,
    )
    route_count = 0 if route is None else len(
        re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))
    )
    if route_count != 80:
        raise RuntimeError(f"R0.72T home route expected 80 notes, got {route_count}")

    recap = (PUBLIC / "recap-r0-61-r0-72t.html").read_text(encoding="utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    recap_links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    phases = len(re.findall(r'<article class="phase">', recap))
    if len(recap_links) != 110 or len(set(recap_links)) != 110 or phases != 29:
        raise RuntimeError(
            "R0.72T recap baseline expected 110 unique nodes and 29 phases"
        )

    literature = (PUBLIC / "literature-review.html").read_text(encoding="utf-8")
    if literature.count(LITERATURE_T_OVERVIEW) != 1:
        raise RuntimeError("R0.72T literature route overview is missing or duplicated")
    if literature.count("开放接口 · R0.72U") != 1:
        raise RuntimeError("R0.72T literature must contain exactly one R0.72U open interface")

    inventory = json.loads(
        (ROOT / "research/formal-archive-inventory.json").read_text(encoding="utf-8")
    )
    expected_inventory = {
        "latestPublishedRelease": "r072t",
        "publishedReleaseCount": 72,
        "formalSealedReleaseCount": 48,
        "legacyFormalFigureBacklogCount": 24,
    }
    for key, value in expected_inventory.items():
        if inventory.get(key) != value:
            raise RuntimeError(f"formal archive is not at R0.72T: {key}")
    if (
        len(inventory.get("publishedReleases", [])) != 72
        or len(inventory.get("formalSealedReleases", [])) != 48
        or inventory["publishedReleases"][-1] != "r072t"
        or inventory["formalSealedReleases"][-1] != "r072t"
        or "r072u" in inventory["publishedReleases"]
        or "r072u" in inventory["formalSealedReleases"]
    ):
        raise RuntimeError("formal archive lists are not append-only from R0.72T")


def validate_inputs() -> None:
    for relative in (
        "research/r072u_report-source.md",
        "research/r072u_literature_audit.md",
        "research/r072u_gap_matrix.md",
        "research/r072u_independent_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md",
        f"{CERTIFICATE_RELATIVE}/crosscheck.json",
        f"{FIGURE_RELATIVE}/manifest.json",
        "public/notes/r0-72t.html",
        "public/recap-r0-61-r0-72t.html",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72U release input: {relative}")

    report = (ROOT / "research/r072u_report-source.md").read_text(encoding="utf-8")
    for token in (
        "centerUniformLocalGraphCoercivity",
        "localSolutionObservability",
        "wholeLineBlockContraction",
        "P_c",
        "H_D^{-1}",
        "A'",
        "B'",
        "Poincare",
        "endpoint",
        "periodicTransfer",
        "Clay",
    ):
        if token not in report:
            raise RuntimeError(f"R0.72U report missing stable token: {token}")

    independent = (ROOT / "research/r072u_independent_audit.md").read_text(encoding="utf-8")
    for token in (
        "Literal spatial-cutoff inequality",
        "Large-\\(|c|\\) endpoint bound",
        "boundedChartGraph=PASS",
        "wholeLineBlock=OPEN",
        "periodicTransfer=OPEN",
        "Clay=OPEN",
    ):
        if token not in independent:
            raise RuntimeError(f"R0.72U independent audit missing token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.72U certificate")
    verify_flat_hash_ledger(figure, "R0.72U figure")

    certificate_manifest = json.loads((certificate / "manifest.json").read_text(encoding="utf-8"))
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if certificate_manifest.get("status") != "formal":
        raise RuntimeError("R0.72U certificate is not formal")
    if not re.fullmatch(r"[0-9a-f]{40}", str(certificate_manifest.get("sourceCommit", ""))):
        raise RuntimeError("R0.72U certificate source commit is not frozen")
    if crosscheck.get("status") != "passed" or crosscheck.get("formalSourceReady") is not True:
        raise RuntimeError("R0.72U certificate crosscheck is not formal")
    subprocess.run(
        [sys.executable, str(certificate / "validate_certificate.py"), "--require-formal"],
        cwd=ROOT,
        check=True,
    )

    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("release") != "R0.72U" or manifest.get("figureId") != FIGURE_ID:
        raise RuntimeError("R0.72U figure identity mismatch")
    if manifest.get("status") != "formal" or manifest.get("qa", {}).get("status") != "passed":
        raise RuntimeError("R0.72U figure is not formally validated")
    subprocess.run(
        [sys.executable, str(figure / "validate.py"), "--require-formal"],
        cwd=ROOT,
        check=True,
    )
    publication = manifest.get("publication", {})
    if publication.get("directory") != "public/assets/r072u":
        raise RuntimeError("R0.72U figure publication directory mismatch")
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = PUBLIC / "assets/r072u" / f"{FIGURE_ID}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72U public {suffix} is absent or not byte-identical")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72t.html").read_text(encoding="utf-8")
    for index, (pattern, value) in enumerate((
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72U：未截断 fixed-chart graph coercivity 对 interval center 一致闭合，并给出 local actual-solution observability。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72U｜center-uniform local graph coercivity">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="local observability 已闭合；whole-line block contraction、periodic transfer 与 Clay 仍开放。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072u/fig-r072u-two-moment-coercivity.png">'),
        (r'<title>.*?</title>', '<title>R0.72U｜center-uniform local graph coercivity</title>'),
    )):
        html = section(html, pattern, value, f"U note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.33", "/i18n-en.js?v=1.34", "U note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#cutoff">cutoff audit</a><a href="#theorem">定理</a><a href="#trace">trace</a><a href="#poincare">Poincare</a><a href="#moments">moments</a><a href="#bounded">bounded centers</a><a href="#escaping">escaping centers</a><a href="#endpoint">endpoint</a><a href="#discriminator">nontriviality</a><a href="#solutions">solutions</a><a href="#global">global boundary</a><a href="#certificate">证书</a><a href="#literature">文献</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "U note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "U note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · direct decision</a></li><li><a href="#cutoff">01 · cutoff audit</a></li><li><a href="#theorem">02 · corrected theorem</a></li><li><a href="#trace">03 · graph-space trace</a></li><li><a href="#poincare">04 · Poincare reduction</a></li><li><a href="#moments">05 · two moments</a></li><li><a href="#bounded">06 · bounded centers</a></li><li><a href="#escaping">07 · escaping centers</a></li><li><a href="#endpoint">08 · endpoint correction</a></li><li><a href="#discriminator">09 · nontriviality</a></li><li><a href="#solutions">10 · actual solutions</a></li><li><a href="#global">11 · local-to-global</a></li><li><a href="#certificate">12 · certificate</a></li><li><a href="#literature">13 · literature</a></li><li><a href="#figure">14 · journal figure</a></li><li><a href="#value">15 · value</a></li><li><a href="#next">16 · R0.72V</a></li><li><a href="#reproduce">17 · reproduction</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "U note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "U note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72U · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "U note footer")
    assert_clean(html, "R0.72U note")
    assert_mathjax_clean(html, "R0.72U note")
    (PUBLIC / "notes/r0-72u.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72t.html").read_text(encoding="utf-8")
    html = required(html, "/i18n-en.js?v=1.33", "/i18n-en.js?v=1.34", "U recap i18n")
    for label, pattern, value in (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72U 的 111 个节点；最新一节闭合 fixed-chart observability。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.72U｜R0.60 之后的研究回顾">'),
        ("og desc", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="三十个阶段、111 个节点：从约化递推到 center-uniform local observability。">'),
        ("title", r'<title>.*?</title>', '<title>R0.61–R0.72U｜R0.60 之后的研究回顾</title>'),
    ):
        html = section(html, pattern, value, "U recap " + label)
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.72U · 2026-08-28</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，保留 R0.61 到 R0.72U 的 111 个研究节点。R0.72U 排除 spatial-cutoff 平凡化，并闭合未截断、center-uniform、fixed-chart graph coercivity 与 local actual-solution observability。节点状态描述证据类型，不把局部模型结果写成全局问题已经解决。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72U</strong><p>收录节点：111</p><p>回顾截止时公开笔记：171</p><p>回顾截止节点：R0.72U</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "U recap hero")
    html = required(html, "02 · 110 节完整索引", "02 · 111 节完整索引", "U recap toc")
    html = required(html, "01 · 二十九个研究阶段", "01 · 三十个研究阶段", "U recap phase toc")
    html = required(html, "R0.60 之后的路线分成二十九个阶段", "R0.60 之后的路线分成三十个阶段", "U recap phase heading")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2>
          <div class="metrics"><div class="metric"><strong>111</strong><span>R0.61–R0.72U 研究节点</span></div><div class="metric"><strong>73</strong><span>R0.70A–R0.72U 已公开版本</span></div><div class="metric"><strong>49</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div>
          <p>R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.70A–R0.72U 的 73 个版本已经公开，其中 49 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。</p>
        </section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "U recap result")
    new_phase = r'''            <article class="phase"><h3>R0.72U · center-uniform fixed-chart graph coercivity</h3>
              <p>R0.72U 先证明原字面 spatial-cutoff target 只是普通 Poincare inequality，随后改成不设 temporal cutoff、也不设 spatial zero trace 的 fixed-chart graph estimate。</p>
              <p>bounded centers 用 compactness；escaping centers 用两个 scalar moments、保留端点的 \(B'\overline A\) identity 与 scalar \(H^1\) trace inequality。常数对 interval center 一致，并直接给 actual solutions 的 local observability。</p>
              <p>wholeLineBlockContraction、periodicTransfer 与 Clay 仍开放。下一阶段处理 whole-line tails、boundary flux 与 cutoff commutators。</p>
              <div class="links"><a href="/notes/r0-72u.html">R0.72U</a><a href="/assets/r072u/fig-r072u-two-moment-coercivity.pdf">R0.72U 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072u">R0.72U 证书</a></div></article>
'''
    html = once(html, "          </div>\n        </section>\n\n        <section id=\"node-index\">", new_phase + "          </div>\n        </section>\n\n        <section id=\"node-index\">", "U recap phase")
    html = required(html, "R0.61–R0.72T 的 110 节公开笔记", "R0.61–R0.72U 的 111 节公开笔记", "U recap node title")
    node_t = '            <span class="node-ref"><a href="/notes/r0-72t.html">R0.72T</a><span class="node-state kind-nogo">阻</span></span>\n'
    node_u = '            <span class="node-ref"><a href="/notes/r0-72u.html">R0.72U</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_t, node_t + node_u, "U recap node")
    retained = r'''            <li>R0.72U 的 local observability：literal spatial cutoff 是 Poincare-trivial；uncut fixed-chart graph estimate 与 local actual-solution observability 已对 interval center 一致闭合。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "U recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>局部模型 observability 已闭合；全直线 transfer 是新的明确缺口</h2><p>截至 R0.72U，没有一般三维 continuation criterion，也没有证明有限时破裂或全局光滑性；不能把 111 个节点或 73 个公开版本解释成 Clay 问题完成比例。</p><p>新的严格增量是 uncut fixed-chart graph coercivity、center uniformity 与 local actual-solution observability。whole-line tails、boundary flux、periodic transfer 仍开放。</p></section>''', "U recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72V 处理 whole-line tail 与 commutator transfer</h2><p>目标是把 fixed-chart observability 延伸到全直线：控制 chart 外 tails、local energy boundary flux 与 spatial cutoff commutators。whole-line block estimate 闭合后，才进入 periodic exact-heat-path transfer。</p></section>''', "U recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.72U 的 73 节已公开；49 节按当前 formal-figure 合同完整封存；24 节旧档仍待回补。</p><p>R0.72U 完成的是线性 bounded-chart theorem。wholeLineBlockContraction、periodicTransfer、一般三维 continuation 与 Clay 正式问题仍开放。</p></section>''', "U recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72t.html">保留 R0.72T 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72u.html">打开最新节点 R0.72U</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072u">查看 R0.72U 精确证书</a> · <a href="/assets/r072u/fig-r072u-two-moment-coercivity.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72u.pdf">下载同步 PDF</a></p><p>完整节点索引保留历史编号；状态标签只描述证据类型。</p></section>''', "U recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72U 回顾 · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "U recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 111 or len(set(links)) != 111:
        raise RuntimeError(f"recap node index expected 111 unique links, got {len(links)}/{len(set(links))}")
    phases = re.findall(r'<article class="phase">', html)
    if len(phases) != 30:
        raise RuntimeError(f"recap expected 30 phases, got {len(phases)}")
    assert_clean(html, "R0.72U recap")
    assert_mathjax_clean(html, "R0.72U recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-72u.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.33"', 'data-site-version="1.34"'),
        ("/i18n-en.js?v=1.33", "/i18n-en.js?v=1.34"),
        ("/site-refresh.js?v=1.33", "/site-refresh.js?v=1.34"),
        ("<strong>v1.33</strong>网页版本", "<strong>v1.34</strong>网页版本"),
        ("<strong>170</strong>公开研究笔记", "<strong>171</strong>公开研究笔记"),
        ("<strong>R0.72T</strong>最新研究节点", "<strong>R0.72U</strong>最新研究节点"),
        ("Research topology · R0.1–R0.72T", "Research topology · R0.1–R0.72U"),
        ("R0.70A–R0.72T：72 节已公开，48 节完整封存", "R0.70A–R0.72U：73 节已公开，49 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72T</span>', '<span class="route-range">R0.69P–R0.72U</span>'),
        ('aria-label="R0.69P–R0.72T"', 'aria-label="R0.69P–R0.72U"'),
        ("展开 80 篇公开笔记", "展开 81 篇公开笔记"),
        ("本站 R0.69P–R0.72T 路线", "本站 R0.69P–R0.72U 路线"),
        ("综述 v1.33 · 2026-08-28", "综述 v1.34 · 2026-08-28"),
        ("上次综述 v1.32 · 2026-08-28", "上次综述 v1.33 · 2026-08-28"),
        ("/recap-r0-61-r0-72t.html", "/recap-r0-61-r0-72u.html"),
        ("/recap-r0-61-r0-72t.pdf", "/recap-r0-61-r0-72u.pdf"),
    ):
        html = required(html, old, new, "U home " + old)
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.72U 已闭合 center-uniform fixed-chart graph coercivity 与 local actual-solution observability；下一关是 whole-line tails 与 cutoff commutators。</span></div>', "U home focus")
    link_t = '<a class="milestone" href="/notes/r0-72t.html">R0.72T</a>'
    html = once(html, link_t, link_t + '\n                  <a class="milestone" href="/notes/r0-72u.html">R0.72U</a>', "U home route link")
    route_u = r'''              <p>R0.72U 排除 literal spatial-cutoff 的 Poincare 平凡化，改证无 temporal cutoff、无 spatial zero trace 的 fixed-chart graph estimate。bounded centers 用 compactness，escaping centers 用 two-moment endpoint identity；local actual-solution observability 已闭合。whole-line tails、boundary flux 与 periodic transfer 仍开放。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_u + '              <details class="tree-notes" open>', "U home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "U home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72U · 2026-08-28</p>
            <h3>R0.60 recap 之后的累计回顾收录 111 个节点；全站现有 171 篇公开研究笔记</h3>
            <p>累计回顾现分三十个问题阶段，并给出 R0.61–R0.72U 的完整逐节点索引。R0.72U 增加 uncut fixed-chart graph coercivity、center uniformity 与 local actual-solution observability。</p>
            <p>R0.70A–R0.72U 共 73 个版本已公开；49 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;局部 observability 已闭合；whole-line block、periodic transfer 与一般三维问题仍开放。</p>
            <p><a href="/recap-r0-61-r0-72u.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72u.pdf">下载同步 PDF</a></p>
          </div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "U home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_U_CARD + '\n        </section>\n\n      </article>', "U home card")
    if html.count('data-release="r072u"') != 1:
        raise RuntimeError("home must contain exactly one R0.72U card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72U">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 81:
        raise RuntimeError("home current-route index must contain 81 note links")
    assert_clean(html, "R0.72U home")
    assert_mathjax_clean(html, "R0.72U home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.33", "/i18n-en.js?v=1.34"),
        ("本站 R0.69P–R0.72T 只列为研究笔记", "本站 R0.69P–R0.72U 只列为研究笔记"),
        ("/recap-r0-61-r0-72t.html", "/recap-r0-61-r0-72u.html"),
        ("文献综述 v1.33 · 2026-08-28", "文献综述 v1.34 · 2026-08-28"),
        ("累计回顾与 110 节索引", "累计回顾与 111 节索引"),
        ("打开 110 节完整索引", "打开 111 节完整索引"),
    ):
        html = required(html, old, new, "U literature " + old)
    html = once(
        html,
        LITERATURE_T_OVERVIEW,
        LITERATURE_U_OVERVIEW,
        "U literature overview",
    )
    old_open = '<div class="route-step pause"><header><b>开放接口 · R0.72U</b><strong>direct observability for the parameter-free model</strong></header><p>用 \\(\\partial_X(\\chi u)\\) 的 \\(L^2_SL^2_X\\) norm 与 equation residual 的 \\(L^2_SH^{-1}_X\\) norm 控制 \\(\\chi u\\) 的 spacetime \\(L^2\\) norm，再补 all-start endpoint control。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.72U</b><strong>uncut center-uniform graph coercivity on a fixed chart</strong></header><p>literal spatial cutoff 被确认为 Poincare-trivial；改正后的 arbitrary-trace graph estimate 与 local actual-solution observability 已闭合。<a href="/notes/r0-72u.html">研究笔记</a> <a href="/recap-r0-61-r0-72u.html">当前累计回顾</a> <a href="#r072u-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72V</b><strong>whole-line tail and commutator transfer</strong></header><p>控制 chart tails、boundary flux 与 spatial cutoff commutators，再检查 periodic exact-heat-path transfer。</p></div>'''
    html = once(html, old_open, new_steps, "U literature route")
    boundary = r'''

          <h3 id="r072u-boundary">R0.72U 的 fixed-chart theorem 与文献边界</h3>
          <p>Hörmander 与 Bedrossian–Liss 给局部 graph regularity；Albritton–Armstrong–Mourrat–Novack 给 kinetic strong/weak Poincare 先例；Albritton–Beekie–Novack 给 stationary cubic \(1/5\) benchmark。它们都不直接推出本节 uncut、arbitrary-trace、center-uniform collision estimate。</p>
          <p>R0.72U 的证明使用 model-specific two-moment identity。限定一手检索没有定位到可直接替代该证明的定理；这个检索结论不构成不存在性、新颖性或优先权主张。</p>
          <div class="boundary"><strong>R0.72U 的主张边界</strong><p>centerUniformLocalGraphCoercivity=CLOSED，localSolutionObservability=CLOSED。wholeLineBlockContraction=OPEN，periodicTransfer=OPEN，Clay=OPEN。fixed-chart mass control 不能省略 tails、boundary flux 与 cutoff commutators。</p></div>'''
    match = re.search(r'(<h3 id="r072t-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("U literature expected R0.72T boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "U literature boundary")
    assert_clean(html, "R0.72U literature")
    assert_mathjax_clean(html, "R0.72U literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    notes = len(list((PUBLIC / "notes").glob("*.html")))
    if notes != 171:
        raise RuntimeError(f"expected 171 public HTML notes after R0.72U, got {notes}")

    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    release.update({
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
    })
    del release["nextReleaseSourceStage"]
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.33", "R0.72T", 170):
        raise RuntimeError("site-version is not at R0.72T")
    site.update({"version": "1.34", "latestRelease": "R0.72U", "publicHtmlNoteCount": 171, "publishedDate": "2026-08-28"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    current = (
        inventory.get("latestPublishedRelease"),
        inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"),
        inventory.get("legacyFormalFigureBacklogCount"),
    )
    if current != ("r072t", 72, 48, 24):
        raise RuntimeError("formal archive inventory is not at R0.72T")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072t" or "r072u" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72T")
        inventory[key].append("r072u")
    inventory.update({
        "latestPublishedRelease": "r072u",
        "publishedReleaseCount": 73,
        "formalSealedReleaseCount": 49,
        "legacyFormalFigureBacklogCount": 24,
    })
    if len(inventory["publishedReleases"]) != 73 or len(inventory["formalSealedReleases"]) != 49:
        raise RuntimeError("formal archive count mismatch after R0.72U")
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
        "notes/r0-72u.html",
        "recap-r0-61-r0-72u.html",
    ):
        content = (PUBLIC / relative).read_text(encoding="utf-8")
        assert_clean(content, relative)
        assert_mathjax_clean(content, relative, check_naked=False)
    print(json.dumps({
        "release": "R0.72U",
        "siteVersion": "1.34",
        "notes": 171,
        "recapNodes": 111,
        "published": 73,
        "formalSealed": 49,
        "legacyBacklog": 24,
        "phases": 30,
        "routeNotes": 81,
        "next": "R0.72V",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
