#!/usr/bin/env python3
"""Generate the fail-closed R0.72W exact-periodic collision-block release.

R0.72W keeps the full analytic trigonometric tail, proves uniform graph
coercivity on the expanding physical torus, and obtains strict contraction for
one exact linear scalar Fourier row on one collision-scale block.  It does not
claim short-time uniformity, outer-time concatenation, nonlinear closure, or a
Clay result.
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


ROOT = Path(os.environ.get("R072W_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_ID = "fig-r072w-exact-tail-transfer"
FIGURE_RELATIVE = f"figures/r072w-exact-periodic/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r072w"

R072V_RELEASE_BASELINE = {
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
}

SOURCE_STAGE_CONTRACT = {
    "release": "r072w",
    "stage": "source-freeze",
    "publicationStatus": "pending-formal-certificate-figure-and-publication",
    "publicCountersAdvanced": False,
    "report": "research/r072w_report-source.md",
    "literatureAudit": "research/r072w_literature_audit.md",
    "gapMatrix": "research/r072w_gap_matrix.md",
    "independentAudit": "research/r072w_independent_audit.md",
    "producer": "research/certificates/r072w/generate_certificate.py",
    "independentProducer": "research/certificates/r072w/independent_recompute.py",
    "comparator": "research/certificates/r072w/validate_certificate.py",
    "certificateDirectory": CERTIFICATE_RELATIVE,
    "figureDirectory": FIGURE_RELATIVE,
    "generator": "scripts/generate_r072w_release.py",
    "translationScript": "scripts/add-r072w-translations.mjs",
    "releaseGate": "tests/r072w-exact-periodic-gate.test.mjs",
    "publicationTest": "tests/r072w-release.test.mjs",
}

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

LITERATURE_W_OVERVIEW = (
    "这里没有完成 global caustic image，也没有证明 ED through collision。"
    "R0.72T 进一步固定 exact A2 spacetime germ 与唯一 scaling，核对 quadratic "
    "wrong-model calibration、physical 3/5 回填、combined fixed-f identity、"
    "inviscid mixing 和 CDZE 6/7 barrier；block contraction 与 periodic transfer "
    "仍开放。R0.72U 随后排除 literal spatial-cutoff 的 Poincare 平凡化，闭合无 "
    "temporal cutoff、无 spatial zero trace 的 center-uniform fixed-chart graph "
    "coercivity 与 local actual-solution observability。R0.72V 再以 coefficient-uniform "
    "unit charts 和 nonhomogeneous H^-1 direct sum 闭合 exact cubic linear scalar "
    "model 的 whole-line graph coercivity，并由独立 all-L2 evolution 得到固定块收缩。"
    "R0.72W 证明 finite H5/H7/R9 termwise absorption 在整条扩张周期上为 FALSE，"
    "转而保留 full analytic sine tail；compact--escaping cell dichotomy、torus H^-1 "
    "direct sum 与 all-L2 energy evolution 闭合 exact periodic scalar collision-block "
    "contraction。T downarrow 0 一致性为 FALSE；outer A1/A2 time concatenation、"
    "complete linearized shear subsystem、nonlinear/Clay 仍开放。一般 Navier–Stokes "
    "正则性仍开放。"
)


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div>
        <div class="eyebrow">研究笔记 R0.72W · EXACT ANALYTIC TAIL · PERIODIC COLLISION BLOCK</div>
        <h1>保留解析尾项的精确周期块收缩：<br>有界—逃逸胞元二分</h1>
        <p class="lead">有限的 \(H_5,H_7,R_9\) 展开在整条扩张周期上不能作为小扰动吸收。R0.72W 因而保留 exact trigonometric heat path，以 compact--escaping cell dichotomy 直接证明对 \(0&lt;\alpha\le1\) 一致的 unit-cell graph theorem，并经 nonhomogeneous \(H^{-1}\) direct sum 全球化到 whole line 和 expanding torus。对 every torus \(L^2\) datum 的独立能量演化随后给出 exact periodic scalar collision-block contraction。结论仍只是一个 exact linear scalar Fourier row。</p>
      </div>
      <div class="stamp"><span class="state">状态 · R0.72W exact periodic scalar block 完成</span><strong>exact-tail periodic contraction through the compact–escaping cell dichotomy</strong><p>版本 v0.72W · 2026-08-28</p><p>exactPeriodicGraphCoercivity: CLOSED</p><p>exactPeriodicBlockContraction: CLOSED</p><p>globalTermwiseRemainderAbsorption: FALSE</p><p>timeLengthUniformity: FALSE</p><p>outerTimeConcatenation: OPEN</p><p>nonlinearNavierStokes / Clay: OPEN</p></div>
    </div></header>'''


NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>精确周期碰撞块已闭合；有限尾项的全局吸收路线被否定</h2>
          <div class="verdict-grid">
            <div class="verdict-card true"><strong>CLOSED · EXACT PERIODIC GRAPH</strong><p>weightedNonabsorbedRemainderEstimate=CLOSED，growingCoreAbsorption=CLOSED；exactFamilyUnitCellCoercivity、exactWholeLineGraphCoercivity 与 exactPeriodicGraphCoercivity 均为 CLOSED。</p></div>
            <div class="verdict-card true"><strong>CLOSED · COLLISION BLOCK</strong><p>exactPeriodicBlockContraction=CLOSED，且回到物理变量的 conjugacy 不使用任何 polynomial truncation。</p></div>
            <div class="verdict-card false"><strong>FALSE · GLOBAL TERMWISE ABSORPTION</strong><p>globalTermwiseRemainderAbsorption=FALSE；整条周期依赖 full analytic cancellation。</p></div>
            <div class="verdict-card false"><strong>OPEN · OUTER AND NONLINEAR</strong><p>outerTimeConcatenation=OPEN，complete linearized subsystem、nonlinear Navier--Stokes 与 Clay 均未闭合。</p></div>
          </div>
        </section>

        <section id="model"><div class="section-no">01 / Exact heat path</div><h2>碰撞缩放保留完整双谐波势</h2>
          <div class="equation result">\[V_\alpha(S,X)=\alpha^{-3}\left[2e^{-\alpha^2S}\sin(\alpha X)-e^{-4\alpha^2S}\sin(2\alpha X)\right],\qquad \partial_SV_\alpha=\partial_X^2V_\alpha.\]</div>
          <p>势定义在 \(\mathbb T_\alpha=\mathbb R/(2\pi/\alpha)\mathbb Z\)，并在 bounded chart 上展开为 \(H_3-\alpha^2H_5/4+\alpha^4H_7/40-17\alpha^6H_9/12096+\cdots\)。</p>
        </section>

        <section id="weighted"><div class="section-no">02 / Weighted envelope</div><h2>全局解析尾项只有 weighted、nonabsorbed 控制</h2>
          <div class="equation result">\[|\mathcal R_\alpha(S,X)|\le2(e^T+256e^{4T})\alpha^6\Omega_{9,T}(X).\]</div>
          <p>R0.72V 的 whole-line graph theorem 因此给出带 \(W_{5,T}v\)、\(W_{7,T}v\) 与 \(\Omega_{9,T}v\) costs 的精确估计；“nonabsorbed”表示这些 weighted norms 没有被无条件移到左边。</p>
        </section>

        <section id="core"><div class="section-no">03 / Growing core</div><h2>有界乘子吸收只达到严格小于周期尺度的 collision core</h2>
          <div class="equation result">\[R=o(\kappa^{2/25}),\qquad D_{\alpha,T}(r\kappa^{2/25})=\frac{r^5}{4}+o(1).\]</div>
          <p>这个 core 在原坐标中的宽度为 \(r\kappa^{-3/25}\)，远小于扩张周期对应的 \(\kappa^{1/5}\) 尺度。</p>
        </section>

        <section id="no-go"><div class="section-no">04 / Global no-go</div><h2>全直线与一周期尺度都排除有限 Neumann 吸收</h2>
          <p>translated bump 给 \(H_5\) correction 的相对成本 \(\asymp\alpha^2L^2\)。在 antipodal chart，exact slope difference 的相对极限是</p>
          <div class="equation result">\[-1-\frac{4}{3\pi^2}\ne0,\qquad \frac{5\pi^2}{12}>4.\]</div>
          <p>该 obstruction 使用 centered spatial variation，因而不被 time-only scalar gauge 消去。结论是 globalTermwiseRemainderAbsorption=FALSE，而不是证明 exact sine family 失去 coercivity。</p>
        </section>

        <section id="derivatives"><div class="section-no">05 / Exact derivative ledger</div><h2>第三、四阶导数控制逃逸方向的时间旋转</h2>
          <div class="equation result">\[|V_{XXX}|\le2e^T+8e^{4T},\qquad |V_{XXXX}|\le\alpha(2e^T+16e^{4T}).\]</div>
          <p>由 heat identity，\((V_X)_S=V_{XXX}\) 且 \((V_{XX}/2)_S=V_{XXXX}/2\)。可能很大的 slope 只以 \(O_T(1)\) 变化，curvature 只以 \(O_T(\alpha)\) 变化。</p>
        </section>

        <section id="probe"><div class="section-no">06 / Scaled probe</div><h2>变化胞元长度上的 adaptive variance 有统一正下界</h2>
          <div class="equation result">\[\mu_{2,\ell}=\frac{\ell^2}{44},\qquad \mu_{4,\ell}=\frac{3\ell^4}{2288},\qquad \mu_{4,\ell}-\mu_{2,\ell}^2=\frac{5\ell^4}{6292}\ge\frac5{6292}.\]</div>
          <p>这里 \(1\le\ell\le2\)。Poincare constants、multiplication norms 和 probe test norms 由这个紧长度区间统一控制。</p>
        </section>

        <section id="dichotomy"><div class="section-no">07 / Compact–escaping dichotomy</div><h2>有界系数收敛到 nonconstant chart；逃逸系数由端点账本排除</h2>
          <p>若 cell slope 与 curvature 有界，\(\alpha\to0\) 时共同零点代数迫使 chart 回到 translated \(H_3\)；若 \(\alpha\) 不趋零，则得到 nonconstant exact trigonometric limit。</p>
          <div class="equation result">\[U_n=\lambda_np_n+h_n,\qquad \|h_n\|_\infty\le R_T,\qquad \int p_n^2q_{\ell_n}\ge\frac5{6292}.\]</div>
          <p>逃逸分支保留两个 scalar endpoints；除以 \(\lambda_n\) 后所有项趋零，不假设 \(\lambda_n\delta_n\to0\)。</p>
        </section>

        <section id="cell"><div class="section-no">08 / Unit-cell theorem</div><h2>一个常数覆盖所有参数、中心、胞元长度和符号</h2>
          <div class="equation result">\[\|v\|_{L^2(I\times J_\ell)}\le C_T^{\rm cell}\left(\|v_y\|_2+\|(\partial_S-i\sigma\mathcal V_{\alpha,X_0})v\|_{L^2H_D^{-1}}\right).\]</div>
          <p>这里 \(H_D^{-1}(J_\ell)=\bigl(H_0^1(J_\ell),\text{ full inherited }H^1\text{ norm}\bigr)^*\)。定理在 maximal graph class \(v\in L^2(I;H^1(J_\ell))\)、\(Qv\in L^2(I;H_D^{-1}(J_\ell))\) 上成立；该定义使后续 constant-one direct-sum estimate 自包含。</p>
          <p>常数对 \(0&lt;\alpha\le1\)、\(X_0\in\mathbb R\)、\(1\le\ell\le2\) 和两个符号一致；不规定 spatial 或 temporal trace。</p>
        </section>

        <section id="global"><div class="section-no">09 / Whole-line and torus</div><h2>同一 nonhomogeneous negative-Sobolev direct sum 完成两次全球化</h2>
          <p>whole line 用单位格；torus 取 \(N_\alpha=\lfloor2\pi/\alpha\rfloor\)，使每格长度 \(1\le\ell_\alpha&lt;2\)。零延拓和 Hilbert-space duality 给</p>
          <div class="equation result">\[\sum_j\|g_j\|_{H_D^{-1}}^2\le\|g\|_{H^{-1}}^2.\]</div>
          <p>exact whole-line 与 exact periodic graph theorems 都针对 full trigonometric potential，不是 finite heat-polynomial truncation。</p>
        </section>

        <section id="evolution"><div class="section-no">10 / All-L2 energy evolution</div><h2>graph coercivity 与 arbitrary-data energy theory 保持分离</h2>
          <p>对 every \(u_-\in L^2(\mathbb T_\alpha)\)，smooth bounded real potential 给唯一</p>
          <div class="equation">\[u\in C(\overline I;L^2(\mathbb T_\alpha))\cap L^2(I;H^1(\mathbb T_\alpha))\]</div>
          <p>以及 exact energy identity。finite certificate 只核对能量代数，不 machine-check parabolic existence、compactness、trace 或 \(H^{-1}\) direct sum。</p>
        </section>

        <section id="contraction"><div class="section-no">11 / Periodic contraction</div><h2>observability 与能量单调性给统一严格收缩</h2>
          <div class="equation result">\[E(T)\le\frac{(C_T^{\rm per})^2}{T+(C_T^{\rm per})^2}E(-T),\qquad q_T=\frac{C_T^{\rm per}}{\sqrt{T+(C_T^{\rm per})^2}}&lt;1.\]</div>
          <p>\(C_T^{\rm per}\) 的存在是 nonconstructive；没有声称数值最优 \(q_T\)，也没有声称 \(T\downarrow0\) 时 uniformly away from one。</p>
        </section>

        <section id="physical"><div class="section-no">12 / Physical return</div><h2>物理碰撞行的端点比例由精确共轭保留</h2>
          <div class="equation result">\[\|v(T\kappa^{-2/5})\|_{L^2(\mathbb T_{2\pi})}\le q_T\|v(-T\kappa^{-2/5})\|_{L^2(\mathbb T_{2\pi})}.\]</div>
          <p>这里 \(V_\alpha=-4\alpha^{-3}W(\alpha^2S,\alpha X)\)，端点的 \(L^2\) scaling factor 相同并相消。只覆盖 R0.72T 声明的一个 scalar Fourier row。</p>
        </section>

        <section id="numerics"><div class="section-no">13 / Numerical diagnostic</div><h2>Strang splitting 只作为 stress test</h2>
          <p>exact potential 的 Fourier Strang splitting 与 forward--adjoint power iteration 在测试网格上给出小于 \(0.12\) 的 norms，并通过分辨率加密。</p>
          <p>numericalDiagnosticIsProof=FALSE，numericalDiagnosticDeterminesAnalyticConstant=FALSE；有限网格不是 infinite-dimensional propagator norm 的严格上界。</p>
        </section>

        <section id="certificate"><div class="section-no">14 / Certificate and literature</div><h2>有限精确代数、解析证明和限定检索各自保持边界</h2>
          <p>双路证书核对 Taylor coefficients、heat identities、probe moments、common-zero algebra、torus partition 与 energy ratio；compact--escaping contradiction 和 nonautonomous graph theorem 仍是解析论证。</p>
          <p>Coble--He 的主要 ED theorem 要求固定数量、保持分离的 nondegenerate critical points；该假设在 merger 处失效。限定的一手检索不构成不存在性、新颖性或优先权证明。</p>
        </section>

        <section id="figure"><div class="section-no">15 / Journal figure</div><h2>正式附图记录 exact-tail transfer 与证据边界</h2>
          <p><img src="/assets/r072w/fig-r072w-exact-tail-transfer.svg" alt="R0.72W exact-tail periodic contraction through the compact-escaping cell dichotomy"></p>
          <p><a href="/assets/r072w/fig-r072w-exact-tail-transfer.pdf">下载 PDF</a> · <a href="/assets/r072w/fig-r072w-exact-tail-transfer.png">下载 PNG</a> · <a href="/assets/r072w/fig-r072w-exact-tail-transfer.svg">打开 SVG</a></p>
        </section>

        <section id="value"><div class="section-no">16 / Research value</div><h2>碰撞块从 cubic germ 推进到 exact periodic row，但尚未形成完整时间历史</h2>
          <p>严格增量是 nonperturbative：它证明 finite tail absorption 路线为 false，同时用 full sine cancellation 完成 expanding-torus collision block。</p>
          <p>直接 Clay 价值仍低。缺少 outer \(A_1\) intervals 的一致拼接、所有 Fourier rows 的 normalization 和 summation、pressure、vortex stretching、nonlinear bootstrap 与 continuation criterion。</p>
        </section>

        <section id="next"><div class="section-no">17 / Next gate</div><h2>R0.72X：outer A1 与 A2 collision block 的精确时间拼接</h2>
          <p>下一节必须保留物理 Fourier normalization、scalar gauges、energy factors 和 later row summation 所需常数，把 pre/post-collision \(A_1\) regions 与已完成的 \(A_2\) block 连接起来。</p>
        </section>

        <section id="reproduce"><div class="section-no">18 / Reproduction</div><h2>完整证明、边界矩阵、独立审计、证书与正式附图</h2>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072w_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072w_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072w_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072w_independent_audit.md">独立数学审计</a></p>
          <p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072w">精确双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072w-exact-periodic/fig-r072w-exact-tail-transfer">正式附图包</a> · <a href="/notes/r0-72w.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72w.html">累计回顾</a> · <a href="/recap-r0-61-r0-72w.pdf">累计回顾 PDF</a></p>
        </section>
      </article>'''


HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72X</span><span class="tree-state current">下一检查点</span></div>
              <h3>outer A1 plus A2 exact time concatenation</h3>
              <p>把 pre/post-collision nondegenerate \(A_1\) intervals 与已完成的 exact \(A_2\) collision block 拼接，同时保留 Fourier normalization、scalar gauges、energy factors 和 row-summation constants。</p>
            </article>'''


HOME_W_CARD = r'''          <div class="task-one" id="r072w" data-release="r072w" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72W · 2026-08-28</p>
            <h3>保留解析尾项的精确周期块收缩：有界—逃逸胞元二分</h3>
            <p>有限 \(H_5,H_7,R_9\) corrections 在整条扩张周期上不能 termwise absorb；保留 full trigonometric tail 后，compact--escaping dichotomy 给 coefficient-uniform unit-cell theorem。</p>
            <p>whole-line 与 torus \(H^{-1}\) direct sums 完成全球化；every-torus-\(L^2\) energy evolution 给 collision-scale block contraction，并通过 exact conjugacy 回到物理 scalar row。</p>
            <p><strong>结论边界：</strong>&nbsp;exactPeriodicGraphCoercivity=CLOSED，exactPeriodicBlockContraction=CLOSED，globalTermwiseRemainderAbsorption=FALSE，timeLengthUniformity=FALSE；outerTimeConcatenation、nonlinear/Clay 保持 OPEN。</p>
            <p><a href="/notes/r0-72w.html"><strong>阅读 R0.72W 研究笔记 →</strong></a><br>
              <a href="/notes/r0-72w.pdf">下载同步研究笔记 PDF</a> ·
              <a href="/assets/r072w/fig-r072w-exact-tail-transfer.pdf">下载期刊附图 PDF</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072w">查看精确证书</a> ·
              <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072w_report-source.md">查看完整数学报告</a> ·
              <a href="/recap-r0-61-r0-72w.html">阅读累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72X：</strong>&nbsp;outer A1 plus A2 exact time concatenation。</p>
          </div>'''


def _validate_source_stage_manifest(release: dict) -> None:
    for key, value in R072V_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72V: {key}")
    if release.get("nextReleaseSourceStage") != SOURCE_STAGE_CONTRACT:
        raise RuntimeError(
            "R0.72W source-stage manifest contract is missing, stale, or has extra fields"
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
        "version": "1.35",
        "latestRelease": "R0.72V",
        "publicHtmlNoteCount": 172,
        "publishedDate": "2026-08-28",
    }
    if site != expected_site:
        raise RuntimeError("public site-version is not exactly at R0.72V")

    notes = sorted((PUBLIC / "notes").glob("*.html"))
    if len(notes) != 172:
        raise RuntimeError(f"R0.72V preflight expected 172 public HTML notes, got {len(notes)}")
    for relative in (
        "notes/r0-72w.html",
        "notes/r0-72w.pdf",
        "recap-r0-61-r0-72w.html",
        "recap-r0-61-r0-72w.pdf",
    ):
        if (PUBLIC / relative).exists():
            raise RuntimeError(f"R0.72V preflight found premature public output: {relative}")

    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in (
        'data-site-version="1.35"',
        "<strong>172</strong>公开研究笔记",
        "<strong>R0.72V</strong>最新研究节点",
        'aria-label="R0.69P–R0.72V"',
    ):
        if token not in home:
            raise RuntimeError(f"R0.72V home baseline missing token: {token}")
    if 'data-release="r072w"' in home:
        raise RuntimeError("R0.72V home already contains an R0.72W card")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72V">(.*?)</nav>',
        home,
        flags=re.S,
    )
    route_count = 0 if route is None else len(
        re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))
    )
    if route_count != 82:
        raise RuntimeError(f"R0.72V home route expected 82 notes, got {route_count}")

    recap = (PUBLIC / "recap-r0-61-r0-72v.html").read_text(encoding="utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    recap_links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    phases = len(re.findall(r'<article class="phase">', recap))
    if len(recap_links) != 112 or len(set(recap_links)) != 112 or phases != 31:
        raise RuntimeError(
            "R0.72V recap baseline expected 112 unique nodes and 31 phases"
        )

    literature = (PUBLIC / "literature-review.html").read_text(encoding="utf-8")
    if literature.count(LITERATURE_V_OVERVIEW) != 1:
        raise RuntimeError("R0.72V literature route overview is missing or duplicated")
    if literature.count("开放接口 · R0.72W") != 1:
        raise RuntimeError("R0.72V literature must contain exactly one R0.72W open interface")

    inventory = json.loads(
        (ROOT / "research/formal-archive-inventory.json").read_text(encoding="utf-8")
    )
    expected_inventory = {
        "latestPublishedRelease": "r072v",
        "publishedReleaseCount": 74,
        "formalSealedReleaseCount": 50,
        "legacyFormalFigureBacklogCount": 24,
    }
    for key, value in expected_inventory.items():
        if inventory.get(key) != value:
            raise RuntimeError(f"formal archive is not at R0.72V: {key}")
    if (
        len(inventory.get("publishedReleases", [])) != 74
        or len(inventory.get("formalSealedReleases", [])) != 50
        or inventory["publishedReleases"][-1] != "r072v"
        or inventory["formalSealedReleases"][-1] != "r072v"
        or "r072w" in inventory["publishedReleases"]
        or "r072w" in inventory["formalSealedReleases"]
    ):
        raise RuntimeError("formal archive lists are not append-only from R0.72V")


def validate_inputs() -> None:
    for relative in (
        "research/r072w_report-source.md",
        "research/r072w_literature_audit.md",
        "research/r072w_gap_matrix.md",
        "research/r072w_independent_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md",
        f"{CERTIFICATE_RELATIVE}/crosscheck.json",
        f"{FIGURE_RELATIVE}/manifest.json",
        "public/notes/r0-72v.html",
        "public/recap-r0-61-r0-72v.html",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72W release input: {relative}")

    report = (ROOT / "research/r072w_report-source.md").read_text(encoding="utf-8")
    for token in (
        "weightedNonabsorbedRemainderEstimate",
        "growingCoreAbsorption",
        "globalTermwiseRemainderAbsorption",
        "exactFamilyUnitCellCoercivity",
        "exactWholeLineGraphCoercivity",
        "exactPeriodicGraphCoercivity",
        "exactPeriodicBlockContraction",
        "outerTimeConcatenation",
        "P_{\\alpha,\\sigma}",
        "H_D^{-1}",
        "R0.72X",
        "Clay",
    ):
        if token not in report:
            raise RuntimeError(f"R0.72W report missing stable token: {token}")

    independent = (ROOT / "research/r072w_independent_audit.md").read_text(encoding="utf-8")
    for token in (
        "global analytic-tail envelope",
        "no-go to global termwise absorption",
        "uniform exact-family unit-cell theorem",
        "both negative-Sobolev",
        "exact periodic energy-block contraction",
        "NOT a machine-assisted proof",
        "Outer-time",
        "Clay problem remain open",
    ):
        if token not in independent:
            raise RuntimeError(f"R0.72W independent audit missing token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.72W certificate")
    verify_flat_hash_ledger(figure, "R0.72W figure")

    certificate_manifest = json.loads((certificate / "manifest.json").read_text(encoding="utf-8"))
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if certificate_manifest.get("status") != "formal":
        raise RuntimeError("R0.72W certificate is not formal")
    if not re.fullmatch(r"[0-9a-f]{40}", str(certificate_manifest.get("sourceCommit", ""))):
        raise RuntimeError("R0.72W certificate source commit is not frozen")
    if crosscheck.get("status") != "passed" or crosscheck.get("formalSourceReady") is not True:
        raise RuntimeError("R0.72W certificate crosscheck is not formal")
    if (
        crosscheck.get("sourceCommit") != certificate_manifest.get("sourceCommit")
        or crosscheck.get("sourceBindings") != certificate_manifest.get("sourceBindings")
        or crosscheck.get("temporaryUnsealedSourceAllowed") is not False
        or not all(crosscheck.get("checks", {}).values())
    ):
        raise RuntimeError("R0.72W certificate lineage or exhaustive checks failed")
    subprocess.run(
        [sys.executable, str(certificate / "validate_certificate.py"), "--require-formal"],
        cwd=ROOT,
        check=True,
    )

    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("release") != "R0.72W" or manifest.get("figureId") != FIGURE_ID:
        raise RuntimeError("R0.72W figure identity mismatch")
    if (
        manifest.get("status") != "formal"
        or manifest.get("qa", {}).get("status") != "passed"
        or manifest.get("qa", {}).get("visualInspectionExplicit") is not True
    ):
        raise RuntimeError("R0.72W figure is not formally validated")
    git = manifest.get("git", {})
    if (
        git.get("sourceCommit") != certificate_manifest.get("sourceCommit")
        or not re.fullmatch(r"[0-9a-f]{40}", str(git.get("certificateCommit", "")))
        or git.get("certificateCommit") == git.get("sourceCommit")
    ):
        raise RuntimeError("R0.72W figure does not preserve two-commit lineage")
    claims = manifest.get("claimBoundary", {})
    expected_claims = {
        "weightedNonabsorbedRemainderEstimateProved": True,
        "growingCoreAbsorptionProved": True,
        "globalTermwiseRemainderAbsorptionFalse": True,
        "exactFamilyUnitCellCoercivityProved": True,
        "exactWholeLineGraphCoercivityProved": True,
        "exactPeriodicGraphCoercivityProved": True,
        "exactPeriodicBlockContractionProved": True,
        "numericalDiagnosticIsProof": False,
        "numericalDiagnosticDeterminesAnalyticConstant": False,
        "outerTimeConcatenationProved": False,
        "timeLengthUniformity": False,
        "nonlinearNavierStokesClosureProved": False,
        "clayMillenniumProblemSolved": False,
    }
    for key, expected in expected_claims.items():
        if claims.get(key) is not expected:
            raise RuntimeError(f"R0.72W figure claim boundary mismatch: {key}")
    subprocess.run(
        [sys.executable, str(figure / "validate.py"), "--require-formal"],
        cwd=ROOT,
        check=True,
    )
    publication = manifest.get("publication", {})
    if publication.get("directory") != "public/assets/r072w":
        raise RuntimeError("R0.72W figure publication directory mismatch")
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = PUBLIC / "assets/r072w" / f"{FIGURE_ID}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72W public {suffix} is absent or not byte-identical")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72v.html").read_text(encoding="utf-8")
    for index, (pattern, value) in enumerate((
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72W：保留解析尾项，以有界—逃逸胞元二分闭合精确周期标量碰撞块收缩。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72W｜Exact-tail periodic contraction through the compact–escaping cell dichotomy">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="exact periodic graph 与 collision-block contraction 已闭合；global termwise absorption 和 short-time uniformity 为 FALSE，outer/nonlinear/Clay 仍开放。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072w/fig-r072w-exact-tail-transfer.png">'),
        (r'<title>.*?</title>', '<title>R0.72W｜Exact-tail periodic contraction through the compact–escaping cell dichotomy</title>'),
    )):
        html = section(html, pattern, value, f"W note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.35", "/i18n-en.js?v=1.36", "W note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#model">精确势</a><a href="#weighted">weighted tail</a><a href="#core">core</a><a href="#no-go">no-go</a><a href="#derivatives">导数账本</a><a href="#probe">probe</a><a href="#dichotomy">胞元二分</a><a href="#cell">单位胞元</a><a href="#global">全球化</a><a href="#evolution">energy evolution</a><a href="#contraction">收缩</a><a href="#physical">物理回填</a><a href="#numerics">数值边界</a><a href="#certificate">证书与文献</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "W note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "W note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · direct decision</a></li><li><a href="#model">01 · exact heat path</a></li><li><a href="#weighted">02 · weighted envelope</a></li><li><a href="#core">03 · growing core</a></li><li><a href="#no-go">04 · global no-go</a></li><li><a href="#derivatives">05 · derivative ledger</a></li><li><a href="#probe">06 · scaled probe</a></li><li><a href="#dichotomy">07 · compact–escaping dichotomy</a></li><li><a href="#cell">08 · unit-cell theorem</a></li><li><a href="#global">09 · whole-line and torus</a></li><li><a href="#evolution">10 · all-L2 evolution</a></li><li><a href="#contraction">11 · periodic contraction</a></li><li><a href="#physical">12 · physical return</a></li><li><a href="#numerics">13 · numerical boundary</a></li><li><a href="#certificate">14 · certificate and literature</a></li><li><a href="#figure">15 · journal figure</a></li><li><a href="#value">16 · value</a></li><li><a href="#next">17 · R0.72X</a></li><li><a href="#reproduce">18 · reproduction</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "W note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "W note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72W · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "W note footer")
    assert_clean(html, "R0.72W note")
    assert_mathjax_clean(html, "R0.72W note")
    (PUBLIC / "notes/r0-72w.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72v.html").read_text(encoding="utf-8")
    html = required(html, "/i18n-en.js?v=1.35", "/i18n-en.js?v=1.36", "W recap i18n")
    for label, pattern, value in (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72W 的 113 个节点；最新一节保留 full analytic tail，闭合 exact periodic scalar collision-block contraction。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.72W｜R0.60 之后的研究回顾">'),
        ("og desc", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="三十二个阶段、113 个节点：从约化递推到 exact-tail periodic collision-block contraction。">'),
        ("title", r'<title>.*?</title>', '<title>R0.61–R0.72W｜R0.60 之后的研究回顾</title>'),
    ):
        html = section(html, pattern, value, "W recap " + label)
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.72W · 2026-08-28</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，完整保留 R0.61 到 R0.72W 的 113 个研究节点。R0.72W 先证明 finite H5/H7/R9 termwise absorption 在整条扩张周期上为 false，再以 full analytic sine tail、compact--escaping cell dichotomy 和 torus H^-1 direct sum 闭合 exact periodic scalar collision-block contraction。节点状态只描述声明范围内的证据，不把一个 linear scalar block 写成 outer-time、complete linearized、nonlinear 或 Clay 结论。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72W</strong><p>收录节点：113</p><p>回顾截止时公开笔记：173</p><p>回顾截止节点：R0.72W</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "W recap hero")
    html = required(html, "02 · 112 节完整索引", "02 · 113 节完整索引", "W recap toc")
    html = required(html, "01 · 三十一个研究阶段", "01 · 三十二个研究阶段", "W recap phase toc")
    html = required(html, "R0.60 之后的路线分成三十一个阶段", "R0.60 之后的路线分成三十二个阶段", "W recap phase heading")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2>
          <div class="metrics"><div class="metric"><strong>113</strong><span>R0.61–R0.72W 研究节点</span></div><div class="metric"><strong>75</strong><span>R0.70A–R0.72W 已公开版本</span></div><div class="metric"><strong>51</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div>
          <p>R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.70A–R0.72W 的 75 个版本已经公开，其中 51 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。</p>
        </section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "W recap result")
    new_phase = r'''            <article class="phase"><h3>R0.72W · exact-tail periodic contraction through compact--escaping cells</h3>
              <p>globalTermwiseRemainderAbsorption=FALSE：finite H5/H7/R9 truncation 在 whole line 和 one-period scale 都不 relatively small；growingCoreAbsorption=CLOSED 只达到 \(R=o(\kappa^{2/25})\)。</p>
              <p>保留 full sine tail 后，exactFamilyUnitCellCoercivity、exactWholeLineGraphCoercivity、exactPeriodicGraphCoercivity 与 exactPeriodicBlockContraction 均为 CLOSED。</p>
              <p>all-torus-L2 energy evolution 与 graph theorem 分开论证；numerical diagnostic 不是 proof。timeLengthUniformity=FALSE，outerTimeConcatenation、complete linearized subsystem、nonlinear Navier--Stokes 与 Clay 保持 OPEN。</p>
              <div class="links"><a href="/notes/r0-72w.html">R0.72W</a><a href="/assets/r072w/fig-r072w-exact-tail-transfer.pdf">R0.72W 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072w">R0.72W 证书</a></div></article>
'''
    html = once(html, "          </div>\n        </section>\n\n        <section id=\"node-index\">", new_phase + "          </div>\n        </section>\n\n        <section id=\"node-index\">", "W recap phase")
    html = required(html, "R0.61–R0.72V 的 112 节公开笔记", "R0.61–R0.72W 的 113 节公开笔记", "W recap node title")
    node_v = '            <span class="node-ref"><a href="/notes/r0-72v.html">R0.72V</a><span class="node-state kind-closed">闭</span></span>\n'
    node_w = '            <span class="node-ref"><a href="/notes/r0-72w.html">R0.72W</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_v, node_v + node_w, "W recap node")
    retained = r'''            <li>R0.72W 保留 exact analytic tail，闭合 expanding-torus scalar collision-block contraction；outer-time concatenation 仍开放。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "W recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>exact periodic scalar collision block 已闭合；完整时间历史与一般三维问题均未外推</h2><p>不能把 113 个节点或 75 个公开版本解释成 Clay 问题完成比例。严格增量是对 global termwise absorption 的 no-go，以及 full analytic tail 下的 exact periodic graph theorem 与 one-block contraction。</p></section>''', "W recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72X 拼接 outer A1 与 exact A2 collision block</h2><p>必须保留 physical Fourier normalization、scalar gauges、energy factors 和 later row summation constants，完成 pre/post-collision intervals 的 exact time concatenation。</p></section>''', "W recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.72W 的 75 节已公开；51 节完整封存；24 节旧档待回补。</p><p>globalTermwiseRemainderAbsorption=FALSE，timeLengthUniformity=FALSE；outerTimeConcatenation、complete linearized shear subsystem、nonlinear Navier--Stokes 与 Clay 保持 OPEN。</p></section>''', "W recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72v.html">保留 R0.72V 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72w.html">打开最新节点 R0.72W</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072w">查看 R0.72W 精确证书</a> · <a href="/assets/r072w/fig-r072w-exact-tail-transfer.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72w.pdf">下载同步 PDF</a></p><p>完整节点索引保留 R0.61 起的全部历史编号；状态标签只描述证据类型。</p></section>''', "W recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72W 回顾 · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "W recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 113 or len(set(links)) != 113:
        raise RuntimeError(f"recap node index expected 113 unique links, got {len(links)}/{len(set(links))}")
    phases = re.findall(r'<article class="phase">', html)
    if len(phases) != 32:
        raise RuntimeError(f"recap expected 32 phases, got {len(phases)}")
    assert_clean(html, "R0.72W recap")
    assert_mathjax_clean(html, "R0.72W recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-72w.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.35"', 'data-site-version="1.36"'),
        ("/i18n-en.js?v=1.35", "/i18n-en.js?v=1.36"),
        ("/site-refresh.js?v=1.35", "/site-refresh.js?v=1.36"),
        ("<strong>v1.35</strong>网页版本", "<strong>v1.36</strong>网页版本"),
        ("<strong>172</strong>公开研究笔记", "<strong>173</strong>公开研究笔记"),
        ("<strong>R0.72V</strong>最新研究节点", "<strong>R0.72W</strong>最新研究节点"),
        ("Research topology · R0.1–R0.72V", "Research topology · R0.1–R0.72W"),
        ("R0.70A–R0.72V：74 节已公开，50 节完整封存", "R0.70A–R0.72W：75 节已公开，51 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72V</span>', '<span class="route-range">R0.69P–R0.72W</span>'),
        ('aria-label="R0.69P–R0.72V"', 'aria-label="R0.69P–R0.72W"'),
        ("展开 82 篇公开笔记", "展开 83 篇公开笔记"),
        ("本站 R0.69P–R0.72V 路线", "本站 R0.69P–R0.72W 路线"),
        ("综述 v1.35 · 2026-08-28", "综述 v1.36 · 2026-08-28"),
        ("上次综述 v1.34 · 2026-08-28", "上次综述 v1.35 · 2026-08-28"),
        ("/recap-r0-61-r0-72v.html", "/recap-r0-61-r0-72w.html"),
        ("/recap-r0-61-r0-72v.pdf", "/recap-r0-61-r0-72w.pdf"),
    ):
        html = required(html, old, new, "W home " + old)
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.72W 已保留 full analytic tail 并闭合 exact periodic scalar collision block；下一关是 outer A1 plus A2 exact time concatenation。</span></div>', "W home focus")
    link_v = '<a class="milestone" href="/notes/r0-72v.html">R0.72V</a>'
    html = once(html, link_v, link_v + '\n                  <a class="milestone" href="/notes/r0-72w.html">R0.72W</a>', "W home route link")
    route_w = r'''              <p>R0.72W 排除 finite H5/H7/R9 global termwise absorption，转而保留 full trigonometric heat path；compact--escaping cell dichotomy 与 whole-line/torus H^-1 direct sums 给 exact periodic graph theorem，all-L2 energy evolution 给 scalar collision-block contraction。T-uniformity 为 false，outer-time concatenation 与 nonlinear/Clay 仍开放。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_w + '              <details class="tree-notes" open>', "W home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "W home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72W · 2026-08-28</p>
            <h3>R0.60 recap 之后的累计回顾收录 113 个节点；全站现有 173 篇公开研究笔记</h3>
            <p>累计回顾现分三十二个问题阶段，并给出 R0.61–R0.72W 的完整逐节点索引。R0.72W 增加 global termwise no-go、exact periodic graph coercivity 与 scalar collision-block contraction。</p>
            <p>R0.70A–R0.72W 共 75 个版本已公开；51 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;exact periodic scalar collision block 已闭合；T-uniform、outer-time concatenation、complete linearized subsystem 与 nonlinear/Clay 保持开放。</p>
            <p><a href="/recap-r0-61-r0-72w.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72w.pdf">下载同步 PDF</a></p>
          </div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "W home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_W_CARD + '\n        </section>\n\n      </article>', "W home card")
    if html.count('data-release="r072w"') != 1:
        raise RuntimeError("home must contain exactly one R0.72W card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72W">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 83:
        raise RuntimeError("home current-route index must contain 83 note links")
    assert_clean(html, "R0.72W home")
    assert_mathjax_clean(html, "R0.72W home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.35", "/i18n-en.js?v=1.36"),
        ("本站 R0.69P–R0.72V 只列为研究笔记", "本站 R0.69P–R0.72W 只列为研究笔记"),
        ("/recap-r0-61-r0-72v.html", "/recap-r0-61-r0-72w.html"),
        ("文献综述 v1.35 · 2026-08-28", "文献综述 v1.36 · 2026-08-28"),
        ("累计回顾与 112 节索引", "累计回顾与 113 节索引"),
        ("打开 112 节完整索引", "打开 113 节完整索引"),
    ):
        html = required(html, old, new, "W literature " + old)
    html = once(
        html,
        LITERATURE_V_OVERVIEW,
        LITERATURE_W_OVERVIEW,
        "V literature overview",
    )
    old_open = '<div class="route-step pause"><header><b>开放接口 · R0.72W</b><strong>weighted H_5/H_7/R_9 remainder stability</strong></header><p>证明与 collision rescaling 兼容的 weighted whole-line absorption，再检查 periodic exact-heat-path transfer。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.72W</b><strong>exact-tail periodic contraction through compact--escaping cells</strong></header><p>finite H5/H7/R9 global termwise absorption 为 FALSE；保留 full sine tail 后，unit-cell dichotomy、whole-line/torus H^-1 direct sums 与 all-L2 energy evolution 给 exact periodic scalar collision-block contraction。<a href="/notes/r0-72w.html">研究笔记</a> <a href="/recap-r0-61-r0-72w.html">当前累计回顾</a> <a href="#r072w-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72X</b><strong>outer A1 plus A2 exact time concatenation</strong></header><p>连接 pre/post-collision nondegenerate intervals 与 exact collision block，保留 Fourier normalization、scalar gauges、energy factors 和 row-summation constants。</p></div>'''
    html = once(html, old_open, new_steps, "W literature route")
    boundary = r'''

          <h3 id="r072w-boundary">R0.72W 的 exact-periodic theorem 与文献边界</h3>
          <p>fixed finite-type shears、separated moving critical points 和 fixed imaginary polynomial potentials 提供尺度与 proof templates，但不直接给 merging critical points、expanding torus、nonautonomous L2_t H^-1_x forcing 与 degeneration-uniform constant 的组合。限定检索不构成新颖性、优先权或不存在性证明。</p>
          <div class="boundary"><strong>R0.72W 的主张边界</strong><p>exactPeriodicGraphCoercivity=CLOSED，exactPeriodicBlockContraction=CLOSED，globalTermwiseRemainderAbsorption=FALSE，timeLengthUniformity=FALSE。outerTimeConcatenation=OPEN，completeLinearizedShearSubsystem=OPEN，nonlinearNavierStokes=OPEN，Clay=OPEN。</p></div>'''
    match = re.search(r'(<h3 id="r072v-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("W literature expected R0.72V boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "W literature boundary")
    assert_clean(html, "R0.72W literature")
    assert_mathjax_clean(html, "R0.72W literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    notes = len(list((PUBLIC / "notes").glob("*.html")))
    if notes != 173:
        raise RuntimeError(f"expected 173 public HTML notes after R0.72W, got {notes}")

    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    release.update({
        "latestCompletedRelease": "r072w",
        "siteVersion": "1.36",
        "publicHtmlNoteCount": 173,
        "postR060RecapNodeCount": 113,
        "nextRelease": "r072x",
        "latestReleaseGate": "tests/r072w-exact-periodic-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072w-release.test.mjs",
        "postR070APublishedReleaseCount": 75,
        "postR070AFormalSealedReleaseCount": 51,
        "legacyFormalFigureBacklogCount": 24,
    })
    del release["nextReleaseSourceStage"]
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.35", "R0.72V", 172):
        raise RuntimeError("site-version is not at R0.72V")
    site.update({"version": "1.36", "latestRelease": "R0.72W", "publicHtmlNoteCount": 173, "publishedDate": "2026-08-28"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    current = (
        inventory.get("latestPublishedRelease"),
        inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"),
        inventory.get("legacyFormalFigureBacklogCount"),
    )
    if current != ("r072v", 74, 50, 24):
        raise RuntimeError("formal archive inventory is not at R0.72V")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072v" or "r072w" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72V")
        inventory[key].append("r072w")
    inventory.update({
        "latestPublishedRelease": "r072w",
        "publishedReleaseCount": 75,
        "formalSealedReleaseCount": 51,
        "legacyFormalFigureBacklogCount": 24,
    })
    if len(inventory["publishedReleases"]) != 75 or len(inventory["formalSealedReleases"]) != 51:
        raise RuntimeError("formal archive count mismatch after R0.72W")
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
        "notes/r0-72w.html",
        "recap-r0-61-r0-72w.html",
    ):
        content = (PUBLIC / relative).read_text(encoding="utf-8")
        assert_clean(content, relative)
        assert_mathjax_clean(content, relative, check_naked=False)
    print(json.dumps({
        "release": "R0.72W",
        "siteVersion": "1.36",
        "notes": 173,
        "recapNodes": 113,
        "published": 75,
        "formalSealed": 51,
        "legacyBacklog": 24,
        "phases": 32,
        "routeNotes": 83,
        "next": "R0.72X",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
