#!/usr/bin/env python3
"""Generate the fail-closed R0.72X all-center exact-path release.

R0.72X propagates the exact scalar collision family from every physical-time
center in a fixed compact interval, tiles arbitrary starts, and concatenates
fixed-margin A1 propagation with the exact A2 family.  It does not claim a
forced H^-1 transfer estimate, the complete linearized shear subsystem,
nonlinear closure, or a Clay result.
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


ROOT = Path(os.environ.get("R072X_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_ID = "fig-r072x-all-center-transfer"
FIGURE_RELATIVE = f"figures/r072x-all-center/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r072x"

R072W_RELEASE_BASELINE = {
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
}

SOURCE_STAGE_CONTRACT = {
    "release": "r072x",
    "stage": "source-freeze",
    "publicationStatus": "pending-formal-certificate-figure-and-publication",
    "publicCountersAdvanced": False,
    "report": "research/r072x_report-source.md",
    "literatureAudit": "research/r072x_literature_audit.md",
    "gapMatrix": "research/r072x_gap_matrix.md",
    "independentAudit": "research/r072x_independent_audit.md",
    "producer": "research/certificates/r072x/generate_certificate.py",
    "independentProducer": "research/certificates/r072x/independent_recompute.py",
    "comparator": "research/certificates/r072x/validate_certificate.py",
    "certificateDirectory": CERTIFICATE_RELATIVE,
    "figureDirectory": FIGURE_RELATIVE,
    "generator": "scripts/generate_r072x_release.py",
    "translationScript": "scripts/add-r072x-translations.mjs",
    "releaseGate": "tests/r072x-exact-path-gate.test.mjs",
    "publicationTest": "tests/r072x-release.test.mjs",
}

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

LITERATURE_X_OVERVIEW = (
    "这里没有完成 global caustic image，也没有证明一般三维 Navier--Stokes 正则性。"
    "R0.72T 固定 exact A2 spacetime germ 与唯一 scaling；R0.72U 闭合 center-uniform "
    "fixed-chart graph coercivity；R0.72V 闭合 exact cubic scalar whole-line graph "
    "coercivity 与 fixed-block contraction；R0.72W 保留 full analytic sine tail，"
    "闭合 exact periodic scalar collision block。R0.72X 把 graph constant 推到固定"
    "物理紧集内的 every block center，得到 all-start exact-path semigroup、integrated "
    "A2 scale、uniform Bloch twists 与 strong-row direct sum；这些 Bloch-uniform 结论"
    "只属于 exact A2 path。fixed-margin Coble--He 输入再与 exact A2 cocycle 拼成 "
    "periodic representative beta=0 的 A1--A2--A1 propagation；没有推断 Bloch-uniform "
    "A1 extension。shrinking-interface "
    "fixed-shape A1 hypotheses、prefactor-one all-gap exponential 和 every physical "
    "row strict contraction 均为 FALSE。forced H^-1 transfer、complete linearized "
    "shear subsystem、nonlinear Navier--Stokes 与 Clay 保持 OPEN。"
)


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.72X · ALL-CENTER EXACT PATH · A1--A2--A1</div>
        <h1>从任意起点传播精确碰撞族：<br>外区 A1 与中心 A2 的无损拼接</h1>
        <p class="lead">我把 R0.72W 的单个精确周期块推进到固定物理时间紧集内的任意块中心。uniform Bloch twists 只在 exact A2 path 上闭合；fixed-margin A1 与 A1--A2--A1 cocycle 只声明 periodic representative \(\beta=0\)。cell gauge 不充当界面状态，Fourier 归一化与 scalar damping 分别记账。结论仍限于声明的线性标量行。</p></div>
      <div class="stamp"><span class="state">状态 · R0.72X all-center exact path 完成</span><strong>arbitrary-start A2 and scoped A1--A2--A1 concatenation</strong><p>版本 v0.72X · 2026-08-28</p><p>A2 Bloch twists: CLOSED</p><p>A1--A2--A1 beta=0: CLOSED</p><p>shrinkingInterfaceFixedShapeA1Hypotheses: FALSE</p><p>allPhysicalRowsUniformContraction: FALSE</p><p>forcedHMinusOneTransfer: OPEN</p><p>nonlinearNavierStokes / Clay: OPEN</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>任意中心与精确时间拼接已闭合；三项外推被明确排除</h2>
          <div class="verdict-grid"><div class="verdict-card true"><strong>CLOSED · ALL-CENTER A2</strong><p>allCenterExactFamilyGraphCoercivity=CLOSED，allStartExactPathSemigroup=CLOSED，allStartIntegratedA2Scale=CLOSED。</p></div><div class="verdict-card true"><strong>CLOSED · SCOPED CONCATENATION</strong><p>uniformTwistedPeriodicGraph=CLOSED 只属于 A2 exact path；fixedMarginA1EnhancedDissipation=CLOSED 与 exactA1A2A1TimeConcatenation=CLOSED 只声明 periodic representative \(\beta=0\)。strongRowDirectSumNoCountLoss=CLOSED。</p></div><div class="verdict-card false"><strong>FALSE · UNSAFE EXTRAPOLATIONS</strong><p>shrinkingInterfaceFixedShapeA1Hypotheses=FALSE，prefactorOneAllGapExponential=FALSE，allPhysicalRowsUniformContraction=FALSE。</p></div><div class="verdict-card false"><strong>OPEN · MISSING SYSTEM</strong><p>forcedHMinusOneTransfer=OPEN，completeLinearizedShearSubsystem=OPEN，nonlinearNavierStokes=OPEN，Clay=OPEN。</p></div></div>
        </section>
        <section id="model"><div class="section-no">01 / Physical row</div><h2>所有拼接都在同一个无 gauge 物理传播子上完成</h2><div class="equation result">\[\partial_dv=\partial_x^2v-i\sigma\varepsilon_cW(d,x)v,\quad W=\frac12e^{-d}\left[-\sin x+\frac12e^{-3d}\sin2x\right].\]</div><p>我取 \(\kappa=\varepsilon_c/4\)、\(\alpha=\kappa^{-1/5}\)、\(S=\alpha^{-2}d\)、\(X=\alpha^{-1}x\)。cell gauge 只服务于局部证明，不出现在物理接口。</p></section>
        <section id="shift"><div class="section-no">02 / Shifted exact family</div><h2>块中心移动到固定物理紧集</h2><div class="equation result">\[D_0=\alpha^2S_0,\quad V_{\alpha,S_0}=\alpha^{-3}\left[2e^{-D_0-\alpha^2\tau}\sin(\alpha X)-e^{-4D_0-4\alpha^2\tau}\sin(2\alpha X)\right].\]</div><p>对 \(D_0\in K\Subset\mathbb R\) 与 \(|\tau|\le T\)，常数只依赖 \(K_T=K+[-T,T]\)；这里不声称 \(D_0\to+\infty\) 时仍一致。</p></section>
        <section id="compactness"><div class="section-no">03 / Compact--escaping audit</div><h2>有界分支回到碰撞图，逃逸分支保留端点控制</h2><div class="equation result">\[\theta=\alpha X_0\pmod{2\pi},\qquad (D_0,\theta)=(0,0)\pmod{2\pi},\qquad |V_{XXX}|\le M_{3,K,T},\quad |V_{XXXX}|\le\alpha M_{4,K,T}.\]</div><p>共同零点全局唯一；有界低阶系数迫使 \(\theta=O(\alpha)\)、\(D_0=O(\alpha^2)\)，极限是 translated \(H_3\)。其余序列沿用 R0.72W 的 escaping endpoint ledger。</p></section>
        <section id="graph"><div class="section-no">04 / All-center graph</div><h2>一个常数覆盖中心、cell、符号与尺度</h2><div class="equation result">\[\|u\|_{L^2}\le C_{K,T}\left(\|u_X\|_2+\|(\partial_\tau-i\sigma V_{\alpha,S_0})u\|_{L_\tau^2H_D^{-1}}\right).\]</div><p>结论对 \(0&lt;\alpha\le1\)、\(D_0\in K\)、两个符号和所有 cell 一致。常数 nonconstructive；有限证书不 machine-check compactness 或 trace passage。</p></section>
        <section id="twist"><div class="section-no">05 / Bloch twist</div><h2>covariant diffusion 化为 twist，不产生 residue 常数</h2><div class="equation result">\[w=e^{i\alpha\beta X}u,\qquad w(X+2\pi/\alpha)=e^{2\pi i\beta}w(X).\]</div><p>零延拓 cell tests 属于每个 twisted global test space；端点模长相同，边界项相消。uniformTwistedPeriodicGraph=CLOSED，但该结论只用于 A2 exact path。</p></section>
        <section id="semigroup"><div class="section-no">06 / Arbitrary starts</div><h2>exact cocycle 铺满任意物理子区间</h2><div class="equation result">\[\|U_\alpha(d_2,d_1)\|_{2\to2}\le q_{K,T}^{\lfloor(d_2-d_1)/(2T\alpha^2)\rfloor}\le q_{K,T}^{-1}e^{-c_{K,T}(d_2-d_1)/\alpha^2}.\]</div><p>首尾 remainder 只用能量收缩。强连续性说明 prefactorOneAllGapExponential=FALSE；第二个不等式必须保留 \(q^{-1}\)。</p></section>
        <section id="integrated"><div class="section-no">07 / Integrated A2 scale</div><h2>几何级数给出 collision-scale 能量</h2><div class="equation result">\[\int_{d_1}^{d_2}\|v(d)\|_2^2\,dd\le\frac{2T\alpha^2}{1-q_{K,T}^2}\|v(d_1)\|_2^2.\]</div><p>同一 envelope 对 \(L_d^2L_x^2\) forcing 给 \(O(\alpha^2)\) Duhamel operator norm；scale-sharp \(L_d^2H_x^{-1}\) transfer 仍为 OPEN。</p></section>
        <section id="outer"><div class="section-no">08 / Fixed-margin A1</div><h2>外区使用固定几何包，不把 A1 黑箱推进 fold</h2><p>在 \(K_*=[-\log2,1-\log2]\) 上取 \(\delta=1/8\)。两段 \([-\log2,-\delta]\) 与 \([\delta,1-\log2]\) 具有固定 critical count、separation、Hessian floor、away-gradient floor 与 derivative bounds。</p><div class="equation result">\[\|U_{A_1}(d_2,d_1)\|_{2\to2}\le C_\delta e^{-c_\delta\sqrt{\varepsilon_c}(d_2-d_1)},\qquad \int\|v\|_2^2\,dd\lesssim_\delta\varepsilon_c^{-1/2}\|v(d_1)\|_2^2.\]</div><p>这是 Coble--He theorem 经 slow-time rescaling后的限定使用，只对 periodic representative \(\beta=0\) 建立；没有推断 Bloch-uniform A1 estimate。</p></section>
        <section id="interface"><div class="section-no">09 / Shrinking interface</div><h2>固定形状 A1 假设不能随界面缩小</h2><p>pre-collision separation 与 Hessian 只有 \(O(\alpha)\)，post-collision away-gradient floor 只有 \(O(\alpha^2)\)。shrinkingInterfaceFixedShapeA1Hypotheses=FALSE 只否定这套 hypotheses，不表示 enhanced dissipation 本身失败。</p></section>
        <section id="concatenation"><div class="section-no">10 / Exact cocycle</div><h2>A1--A2--A1 使用真实传播子逐段相乘</h2><div class="equation result">\[U(d_R,d_L)=U(d_R,\delta)U(\delta,-\delta)U(-\delta,d_L).\]</div><p>这条 fast-history cocycle 只声明 periodic representative \(\beta=0\)。中心 A2 因子由 all-start exact family 控制；outer factors 与 shoulders 保留真实端点。cell gauge 与 endpoint norm factor 在各段内部精确抵消，没有 Bloch-uniform A1 外推。</p></section>
        <section id="rows"><div class="section-no">11 / Fourier ledger</div><h2>unitary transform、scalar damping 与 direct sum 分账</h2><p>每个 row 采用 unitary Fourier normalization；Bloch residue 进入 covariant diffusion。若另有 damping \(\mu\)，振幅因子是 \(e^{-\mu(d_2-d_1)}\)，energy 因子是其平方。</p><div class="equation result">\[\varepsilon_j=\frac{2|\delta K_{z,j}|a}{R^2}.\]</div><p>有共同 coupling floor 的 orthogonal strong rows 由 Parseval 常数一求和，不出现 row-count loss。</p></section>
        <section id="counterexample"><div class="section-no">12 / Physical-row boundary</div><h2>所有物理行的统一严格收缩为 false</h2><p>当 \(K_z=0\)、\(\beta=0\)、\(\mu=0\) 时，空间常数是精确不衰减模态。因此 allPhysicalRowsUniformContraction=FALSE；后续必须分别处理 strong、weak、damped 与 zero-coupling rows。</p></section>
        <section id="evidence"><div class="section-no">13 / Evidence boundary</div><h2>解析证明、有限证书、数值图与文献黑箱分开</h2><p>双路证书核对 center algebra、local jet、interface powers、block arithmetic、Bloch phase、damping 与 geometric series。compactness、twisted direct sum、parabolic evolution、Coble--He theorem 及其应用由解析文本承担。数值扫描只作 diagnostic；限定一手检索不构成新颖性、优先权或不存在性证明。</p></section>
        <section id="figure"><div class="section-no">14 / Journal figure</div><h2>正式附图记录 all-center transfer 与边界</h2><p><img src="/assets/r072x/fig-r072x-all-center-transfer.svg" alt="R0.72X all-center A2 propagation and beta-zero A1-A2-A1 concatenation"></p><p><a href="/assets/r072x/fig-r072x-all-center-transfer.pdf">下载 PDF</a> · <a href="/assets/r072x/fig-r072x-all-center-transfer.png">下载 PNG</a> · <a href="/assets/r072x/fig-r072x-all-center-transfer.svg">打开 SVG</a></p></section>
        <section id="value"><div class="section-no">15 / Research value</div><h2>单块结果成为任意起点的线性标量传播账本</h2><p>严格增量分成两层：A2 exact path 有 all-center、all-start、integrated scale 与 Bloch-uniform graph；periodic representative \(\beta=0\) 另有 exact A1--A2--A1 cocycle。这里没有 Bloch-uniform fast-history theorem。</p><p>直接 Clay 价值仍低：forced \(H^{-1}\) transfer、真实 row weights、pressure coupling、vortex stretching、nonlinear convolution、bootstrap 与 continuation criterion 都未完成。</p></section>
        <section id="next"><div class="section-no">16 / Next gate</div><h2>R0.72Y：恢复完整线性化 row ledger</h2><p>下一节恢复每行 \(\varepsilon_j\)、Bloch residue、scalar damping 与 coupling class，检验 complete triangular subsystem 是否有 scale-sharp forced terms 与 \(\ell^2\) direct-sum estimate。</p></section>
        <section id="reproduce"><div class="section-no">17 / Reproduction</div><h2>完整报告、边界矩阵、独立审计、证书与附图</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072x_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072x_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072x_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072x_independent_audit.md">独立数学审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072x">精确双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072x-all-center/fig-r072x-all-center-transfer">正式附图包</a> · <a href="/notes/r0-72x.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72x.html">累计回顾</a> · <a href="/recap-r0-61-r0-72x.pdf">累计回顾 PDF</a></p></section>
      </article>'''

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72Y</span><span class="tree-state current">下一检查点</span></div>
              <h3>complete linearized row ledger with forced transfer</h3><p>恢复每行 coupling、Bloch residue 与 scalar damping，分开 strong、weak、damped 和 zero-coupling rows，再检验 triangular subsystem 的 scale-sharp forced terms 与 \(\ell^2\) direct sum。</p>
            </article>'''

HOME_X_CARD = r'''          <div class="task-one" id="r072x" data-release="r072x" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72X · 2026-08-28</p><h3>从任意起点传播精确碰撞族：outer A1 与 central A2 的无损拼接</h3>
            <p>固定物理紧集内的 all-center graph constant 给 all-start exact-path semigroup 与 integrated A2 energy；Bloch twist 与 strong-row direct sum 只在 A2 rate 上闭合。</p><p>fixed-margin Coble--He propagation 与 exact A2 cocycle 的 fast-history 拼接只声明 periodic representative \(\beta=0\)。三项不安全外推保持 FALSE。</p>
            <p><strong>结论边界：</strong>&nbsp;allStartExactPathSemigroup=CLOSED 对 A2 Bloch twists；exactA1A2A1TimeConcatenation=CLOSED 只对 beta=0。forcedHMinusOneTransfer、completeLinearizedShearSubsystem、nonlinearNavierStokes 与 Clay 保持 OPEN。</p>
            <p><a href="/notes/r0-72x.html"><strong>阅读 R0.72X 研究笔记 →</strong></a><br><a href="/notes/r0-72x.pdf">下载同步研究笔记 PDF</a> · <a href="/assets/r072x/fig-r072x-all-center-transfer.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072x">查看精确证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072x_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-72x.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72Y：</strong>&nbsp;complete linearized row ledger with scale-sharp forced transfer。</p>
          </div>'''

def _validate_source_stage_manifest(release: dict) -> None:
    for key, value in R072W_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72W: {key}")
    if release.get("nextReleaseSourceStage") != SOURCE_STAGE_CONTRACT:
        raise RuntimeError(
            "R0.72X source-stage manifest contract is missing, stale, or has extra fields"
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
        "version": "1.36",
        "latestRelease": "R0.72W",
        "publicHtmlNoteCount": 173,
        "publishedDate": "2026-08-28",
    }
    if site != expected_site:
        raise RuntimeError("public site-version is not exactly at R0.72W")

    notes = sorted((PUBLIC / "notes").glob("*.html"))
    if len(notes) != 173:
        raise RuntimeError(f"R0.72W preflight expected 173 public HTML notes, got {len(notes)}")
    for relative in (
        "notes/r0-72x.html",
        "notes/r0-72x.pdf",
        "recap-r0-61-r0-72x.html",
        "recap-r0-61-r0-72x.pdf",
    ):
        if (PUBLIC / relative).exists():
            raise RuntimeError(f"R0.72W preflight found premature public output: {relative}")
    if (ROOT / "VERSION").exists():
        raise RuntimeError("R0.72W preflight found premature VERSION")

    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in (
        'data-site-version="1.36"',
        "<strong>173</strong>公开研究笔记",
        "<strong>R0.72W</strong>最新研究节点",
        'aria-label="R0.69P–R0.72W"',
    ):
        if token not in home:
            raise RuntimeError(f"R0.72W home baseline missing token: {token}")
    if 'data-release="r072x"' in home:
        raise RuntimeError("R0.72W home already contains an R0.72X card")
    route = re.search(
        r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72W">(.*?)</nav>',
        home,
        flags=re.S,
    )
    route_count = 0 if route is None else len(
        re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))
    )
    if route_count != 83:
        raise RuntimeError(f"R0.72W home route expected 83 notes, got {route_count}")

    recap = (PUBLIC / "recap-r0-61-r0-72w.html").read_text(encoding="utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    recap_links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    phases = len(re.findall(r'<article class="phase">', recap))
    if len(recap_links) != 113 or len(set(recap_links)) != 113 or phases != 32:
        raise RuntimeError(
            "R0.72W recap baseline expected 113 unique nodes and 32 phases"
        )

    literature = (PUBLIC / "literature-review.html").read_text(encoding="utf-8")
    if literature.count(LITERATURE_W_OVERVIEW) != 1:
        raise RuntimeError("R0.72W literature route overview is missing or duplicated")
    if literature.count("开放接口 · R0.72X") != 1:
        raise RuntimeError("R0.72W literature must contain exactly one R0.72X open interface")

    inventory = json.loads(
        (ROOT / "research/formal-archive-inventory.json").read_text(encoding="utf-8")
    )
    expected_inventory = {
        "latestPublishedRelease": "r072w",
        "publishedReleaseCount": 75,
        "formalSealedReleaseCount": 51,
        "legacyFormalFigureBacklogCount": 24,
    }
    for key, value in expected_inventory.items():
        if inventory.get(key) != value:
            raise RuntimeError(f"formal archive is not at R0.72W: {key}")
    if (
        len(inventory.get("publishedReleases", [])) != 75
        or len(inventory.get("formalSealedReleases", [])) != 51
        or inventory["publishedReleases"][-1] != "r072w"
        or inventory["formalSealedReleases"][-1] != "r072w"
        or "r072x" in inventory["publishedReleases"]
        or "r072x" in inventory["formalSealedReleases"]
    ):
        raise RuntimeError("formal archive lists are not append-only from R0.72W")


def validate_inputs() -> None:
    for relative in (
        "research/r072x_report-source.md",
        "research/r072x_literature_audit.md",
        "research/r072x_gap_matrix.md",
        "research/r072x_independent_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md",
        f"{CERTIFICATE_RELATIVE}/crosscheck.json",
        f"{FIGURE_RELATIVE}/manifest.json",
        "public/notes/r0-72w.html",
        "public/recap-r0-61-r0-72w.html",
    ):
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72X release input: {relative}")

    report = (ROOT / "research/r072x_report-source.md").read_text(encoding="utf-8")
    for token in (
        "allCenterExactFamilyGraphCoercivity",
        "allStartExactPathSemigroup",
        "allStartIntegratedA2Scale",
        "uniformTwistedPeriodicGraph",
        "strongRowDirectSumNoCountLoss",
        "fixedMarginA1EnhancedDissipation",
        "exactA1A2A1TimeConcatenation",
        "shrinkingInterfaceFixedShapeA1Hypotheses",
        "prefactorOneAllGapExponential",
        "allPhysicalRowsUniformContraction",
        "forcedHMinusOneTransfer",
        "completeLinearizedShearSubsystem",
        "q_{K,T}^{-1}",
        "2T\\alpha^2",
        "\\delta=\\frac18",
        "R0.72X",
        "Clay",
    ):
        if token not in report:
            raise RuntimeError(f"R0.72X report missing stable token: {token}")

    independent = (ROOT / "research/r072x_independent_audit.md").read_text(encoding="utf-8")
    for token in (
        "allCenterExactFamilyGraphCoercivity",
        "Bloch-twist audit",
        "Strict block contraction and arbitrary starts",
        "allStartIntegratedA2Scale",
        "fixed-margin A1 estimate",
        "exact A1--A2--A1",
        "prefactor-one exponential",
        "strict contraction of every",
        "Clay problem",
    ):
        if token not in independent:
            raise RuntimeError(f"R0.72X independent audit missing token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.72X certificate")
    verify_flat_hash_ledger(figure, "R0.72X figure")

    certificate_manifest = json.loads((certificate / "manifest.json").read_text(encoding="utf-8"))
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if certificate_manifest.get("status") != "formal":
        raise RuntimeError("R0.72X certificate is not formal")
    if not re.fullmatch(r"[0-9a-f]{40}", str(certificate_manifest.get("sourceCommit", ""))):
        raise RuntimeError("R0.72X certificate source commit is not frozen")
    if crosscheck.get("status") != "passed" or crosscheck.get("formalSourceReady") is not True:
        raise RuntimeError("R0.72X certificate crosscheck is not formal")
    if (
        crosscheck.get("sourceCommit") != certificate_manifest.get("sourceCommit")
        or crosscheck.get("sourceBindings") != certificate_manifest.get("sourceBindings")
        or crosscheck.get("temporaryUnsealedSourceAllowed") is not False
        or not all(crosscheck.get("checks", {}).values())
    ):
        raise RuntimeError("R0.72X certificate lineage or exhaustive checks failed")
    subprocess.run(
        [sys.executable, str(certificate / "validate_certificate.py"), "--require-formal"],
        cwd=ROOT,
        check=True,
    )

    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("release") != "R0.72X" or manifest.get("figureId") != FIGURE_ID:
        raise RuntimeError("R0.72X figure identity mismatch")
    if (
        manifest.get("status") != "formal"
        or manifest.get("qa", {}).get("status") != "passed"
        or manifest.get("qa", {}).get("visualInspectionExplicit") is not True
    ):
        raise RuntimeError("R0.72X figure is not formally validated")
    git = manifest.get("git", {})
    if (
        git.get("sourceCommit") != certificate_manifest.get("sourceCommit")
        or not re.fullmatch(r"[0-9a-f]{40}", str(git.get("certificateCommit", "")))
        or git.get("certificateCommit") == git.get("sourceCommit")
    ):
        raise RuntimeError("R0.72X figure does not preserve two-commit lineage")
    claims = manifest.get("claimBoundary", {})
    expected_claims = {
        "allCenterExactFamilyGraphCoercivityProvedInBoundReport": True,
        "allStartExactPathSemigroupProvedInBoundReport": True,
        "fixedMarginA1EnhancedDissipationImportedInBoundReport": True,
        "exactA2PathBlochUniformProvedInBoundReport": True,
        "periodicRepresentativeBetaZeroExactA1A2A1ConcatenationProvedInBoundReport": True,
        "shrinkingInterfaceFixedShapeA1HypothesesFalseInBoundReport": True,
        "numericalDiagnosticIsProof": False,
        "numericalDiagnosticEvaluatesAnalyticQ": False,
        "numericalDiagnosticIsInfiniteDimensionalOperatorNorm": False,
        "forcedHMinusOneTransferProved": False,
        "completeLinearizedShearSubsystemProved": False,
        "a1A2A1ConcatenationBlochUniform": False,
        "allPhysicalRowsUniformContraction": False,
        "nonlinearNavierStokesClosureProved": False,
        "clayMillenniumProblemSolved": False,
    }
    if set(claims) != set(expected_claims):
        raise RuntimeError("R0.72X figure claim boundary key set is not exact")
    for key, expected in expected_claims.items():
        if claims.get(key) is not expected:
            raise RuntimeError(f"R0.72X figure claim boundary mismatch: {key}")
    subprocess.run(
        [sys.executable, str(figure / "validate.py"), "--require-formal"],
        cwd=ROOT,
        check=True,
    )
    publication = manifest.get("publication", {})
    if publication.get("directory") != "public/assets/r072x":
        raise RuntimeError("R0.72X figure publication directory mismatch")
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = PUBLIC / "assets/r072x" / f"{FIGURE_ID}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72X public {suffix} is absent or not byte-identical")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72w.html").read_text(encoding="utf-8")
    for index, (pattern, value) in enumerate((
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72X：exact A2 path 对任意起点与 Bloch twist 一致；A1--A2--A1 拼接只声明 periodic representative beta=0。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72X｜All-center exact-path propagation and A1--A2--A1 concatenation">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="all-start A2 semigroup 对 Bloch twists 一致；exact A1--A2--A1 cocycle 只对 beta=0 闭合。forced H^-1 transfer、完整线性化系统、nonlinear 与 Clay 保持 OPEN。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072x/fig-r072x-all-center-transfer.png">'),
        (r'<title>.*?</title>', '<title>R0.72X｜All-center exact-path propagation and A1--A2--A1 concatenation</title>'),
    )):
        html = section(html, pattern, value, f"X note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.36", "/i18n-en.js?v=1.37", "X note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#model">物理行</a><a href="#shift">任意中心</a><a href="#compactness">二分审计</a><a href="#graph">graph</a><a href="#twist">Bloch</a><a href="#semigroup">任意起点</a><a href="#integrated">积分能量</a><a href="#outer">outer A1</a><a href="#interface">界面边界</a><a href="#concatenation">精确拼接</a><a href="#rows">row ledger</a><a href="#counterexample">反例边界</a><a href="#evidence">证据边界</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "X note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "X note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · direct decision</a></li><li><a href="#model">01 · physical row</a></li><li><a href="#shift">02 · shifted exact family</a></li><li><a href="#compactness">03 · compact--escaping audit</a></li><li><a href="#graph">04 · all-center graph</a></li><li><a href="#twist">05 · Bloch twist</a></li><li><a href="#semigroup">06 · arbitrary starts</a></li><li><a href="#integrated">07 · integrated A2 scale</a></li><li><a href="#outer">08 · fixed-margin A1</a></li><li><a href="#interface">09 · shrinking interface</a></li><li><a href="#concatenation">10 · exact cocycle</a></li><li><a href="#rows">11 · Fourier ledger</a></li><li><a href="#counterexample">12 · physical-row boundary</a></li><li><a href="#evidence">13 · evidence boundary</a></li><li><a href="#figure">14 · journal figure</a></li><li><a href="#value">15 · value</a></li><li><a href="#next">16 · R0.72Y</a></li><li><a href="#reproduce">17 · reproduction</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "X note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "X note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72X · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "X note footer")
    assert_clean(html, "R0.72X note")
    assert_mathjax_clean(html, "R0.72X note")
    (PUBLIC / "notes/r0-72x.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72w.html").read_text(encoding="utf-8")
    html = required(html, "/i18n-en.js?v=1.36", "/i18n-en.js?v=1.37", "X recap i18n")
    for label, pattern, value in (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72X 的 114 个节点；最新一节闭合 all-center exact path 与 A1--A2--A1 时间拼接。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.72X｜R0.60 之后的研究回顾">'),
        ("og desc", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="三十三个阶段、114 个节点：从约化递推到 all-start exact path 与 A1--A2--A1 cocycle。">'),
        ("title", r'<title>.*?</title>', '<title>R0.61–R0.72X｜R0.60 之后的研究回顾</title>'),
    ):
        html = section(html, pattern, value, "X recap " + label)
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.72X · 2026-08-28</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，完整保留 R0.61 到 R0.72X 的 114 个研究节点。R0.69P 以后，路线从局部证书、exact A2 germ、whole-line 与 periodic scalar block，推进到固定物理紧集内的 all-center A2 path；Bloch-uniformity 只在 A2 rate 上闭合，A1--A2--A1 fast history 只声明 periodic representative beta=0。forced transfer、完整线性化系统、nonlinear Navier--Stokes 与 Clay 都没有被外推。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72X</strong><p>收录节点：114</p><p>回顾截止时公开笔记：174</p><p>回顾截止节点：R0.72X</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "X recap hero")
    html = required(html, "02 · 113 节完整索引", "02 · 114 节完整索引", "X recap toc")
    html = required(html, "01 · 三十二个研究阶段", "01 · 三十三个研究阶段", "X recap phase toc")
    html = required(html, "R0.60 之后的路线分成三十二个阶段", "R0.60 之后的路线分成三十三个阶段", "X recap phase heading")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2>
          <div class="metrics"><div class="metric"><strong>114</strong><span>R0.61–R0.72X 研究节点</span></div><div class="metric"><strong>76</strong><span>R0.70A–R0.72X 已公开版本</span></div><div class="metric"><strong>52</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div>
          <p>R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.70A–R0.72X 的 76 个版本已公开，其中 52 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。</p>
        </section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "X recap result")
    new_phase = r'''            <article class="phase"><h3>R0.72X · all-center exact path and A1--A2--A1 cocycle</h3>
              <p>allCenterExactFamilyGraphCoercivity、allStartExactPathSemigroup、allStartIntegratedA2Scale、uniformTwistedPeriodicGraph 与 strongRowDirectSumNoCountLoss 均为 CLOSED。</p>
              <p>uniformTwistedPeriodicGraph=CLOSED 只属于 exact A2 path。fixedMarginA1EnhancedDissipation 与 exactA1A2A1TimeConcatenation 为 CLOSED 只对 periodic representative beta=0；拼接保留 unitary Fourier normalization、scalar damping 和真实端点。</p>
              <p>三项外推为 FALSE。forcedHMinusOneTransfer、completeLinearizedShearSubsystem、nonlinearNavierStokes 与 Clay 保持 OPEN。</p>
              <div class="links"><a href="/notes/r0-72x.html">R0.72X</a><a href="/assets/r072x/fig-r072x-all-center-transfer.pdf">R0.72X 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072x">R0.72X 证书</a></div></article>
'''
    html = once(html, "          </div>\n        </section>\n\n        <section id=\"node-index\">", new_phase + "          </div>\n        </section>\n\n        <section id=\"node-index\">", "X recap phase")
    html = required(html, "R0.61–R0.72W 的 113 节公开笔记", "R0.61–R0.72X 的 114 节公开笔记", "X recap node title")
    node_w = '            <span class="node-ref"><a href="/notes/r0-72w.html">R0.72W</a><span class="node-state kind-closed">闭</span></span>\n'
    node_x = '            <span class="node-ref"><a href="/notes/r0-72x.html">R0.72X</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_w, node_w + node_x, "X recap node")
    retained = r'''            <li>R0.72X 把 R0.72W 的 exact A2 block 推到 arbitrary starts 与 all Bloch twists；fixed-margin A1 fast-history cocycle 只对 beta=0 拼接，完整线性化系统仍开放。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "X recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>A2 任意起点与 beta=0 fast history 分层闭合；完整三维系统没有外推</h2><p>不能把 114 个节点或 76 个公开版本解释成 Clay 问题完成比例。R0.69P–R0.72X 的严格增量包括 Bloch-uniform all-start A2 path，以及另行限定在 periodic representative beta=0 的 A1--A2--A1 cocycle；直接 Clay 价值仍低。</p></section>''', "X recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72Y 恢复完整线性化 row ledger</h2><p>恢复 row-dependent coupling、Bloch residue、scalar damping、weak/zero modes 与 scale-sharp forced terms，再检验 triangular subsystem 的 \(\ell^2\) direct sum。</p></section>''', "X recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.72X 的 76 节已公开；52 节完整封存；24 节旧档待回补。</p><p>shrinkingInterfaceFixedShapeA1Hypotheses、prefactorOneAllGapExponential、allPhysicalRowsUniformContraction 为 FALSE；forcedHMinusOneTransfer、completeLinearizedShearSubsystem、nonlinearNavierStokes 与 Clay 为 OPEN。</p></section>''', "X recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72w.html">保留 R0.72W 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72x.html">打开最新节点 R0.72X</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072x">查看 R0.72X 精确证书</a> · <a href="/assets/r072x/fig-r072x-all-center-transfer.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72x.pdf">下载同步 PDF</a></p><p>完整节点索引保留 R0.61 起的全部历史编号；状态标签只描述证据类型。</p></section>''', "X recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72X 回顾 · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "W recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 114 or len(set(links)) != 114:
        raise RuntimeError(f"recap node index expected 114 unique links, got {len(links)}/{len(set(links))}")
    phases = re.findall(r'<article class="phase">', html)
    if len(phases) != 33:
        raise RuntimeError(f"recap expected 33 phases, got {len(phases)}")
    assert_clean(html, "R0.72X recap")
    assert_mathjax_clean(html, "R0.72X recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-72x.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.36"', 'data-site-version="1.37"'),
        ("/i18n-en.js?v=1.36", "/i18n-en.js?v=1.37"),
        ("/site-refresh.js?v=1.36", "/site-refresh.js?v=1.37"),
        ("<strong>v1.36</strong>网页版本", "<strong>v1.37</strong>网页版本"),
        ("<strong>173</strong>公开研究笔记", "<strong>174</strong>公开研究笔记"),
        ("<strong>R0.72W</strong>最新研究节点", "<strong>R0.72X</strong>最新研究节点"),
        ("Research topology · R0.1–R0.72W", "Research topology · R0.1–R0.72X"),
        ("R0.70A–R0.72W：75 节已公开，51 节完整封存", "R0.70A–R0.72X：76 节已公开，52 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72W</span>', '<span class="route-range">R0.69P–R0.72X</span>'),
        ('aria-label="R0.69P–R0.72W"', 'aria-label="R0.69P–R0.72X"'),
        ("展开 83 篇公开笔记", "展开 84 篇公开笔记"),
        ("本站 R0.69P–R0.72W 路线", "本站 R0.69P–R0.72X 路线"),
        ("综述 v1.36 · 2026-08-28", "综述 v1.37 · 2026-08-28"),
        ("上次综述 v1.35 · 2026-08-28", "上次综述 v1.36 · 2026-08-28"),
        ("/recap-r0-61-r0-72w.html", "/recap-r0-61-r0-72x.html"),
        ("/recap-r0-61-r0-72w.pdf", "/recap-r0-61-r0-72x.pdf"),
    ):
        html = required(html, old, new, "W home " + old)
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.72X 已闭合 Bloch-uniform all-start A2 path；fixed-margin A1--A2--A1 cocycle 只对 beta=0 闭合。下一关是完整线性化 row ledger 和 forced transfer。</span></div>', "X home focus")
    link_w = '<a class="milestone" href="/notes/r0-72w.html">R0.72W</a>'
    html = once(html, link_w, link_w + '\n                  <a class="milestone" href="/notes/r0-72x.html">R0.72X</a>', "X home route link")
    route_x = r'''              <p>R0.72X 把 R0.72W 的 exact periodic scalar block 推到 fixed physical compact 内的 every center；all-start、integrated scale 与 Bloch twists 只属于 A2 exact path。fixed-margin Coble--He 与 central A2 的 fast-history cocycle 只声明 periodic representative beta=0。三项外推为 FALSE；forced transfer、完整线性化系统与 nonlinear/Clay 仍为 OPEN。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_x + '              <details class="tree-notes" open>', "X home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "X home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem">
            <p class="eyebrow">累计回顾 R0.61–R0.72X · 2026-08-28</p>
            <h3>R0.60 recap 之后的累计回顾收录 114 个节点；全站现有 174 篇公开研究笔记</h3>
            <p>累计回顾现分三十三个问题阶段，并给出 R0.61–R0.72X 的完整索引；R0.72X 分开记录 Bloch-uniform all-start A2 path 与 beta=0 A1--A2--A1 cocycle。</p>
            <p>R0.70A–R0.72X 共 76 个版本已公开；52 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p>
            <p><strong>阶段判断：</strong>&nbsp;A2 exact path 对 Bloch twists 闭合，fast-history A1 cocycle 只对 beta=0 闭合；forced transfer、complete linearized subsystem 与 nonlinear/Clay 保持 OPEN。</p>
            <p><a href="/recap-r0-61-r0-72x.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72x.pdf">下载同步 PDF</a></p>
          </div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "X home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_X_CARD + '\n        </section>\n\n      </article>', "X home card")
    if html.count('data-release="r072x"') != 1:
        raise RuntimeError("home must contain exactly one R0.72X card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72X">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 84:
        raise RuntimeError("home current-route index must contain 84 note links")
    assert_clean(html, "R0.72X home")
    assert_mathjax_clean(html, "R0.72X home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.36", "/i18n-en.js?v=1.37"),
        ("本站 R0.69P–R0.72W 只列为研究笔记", "本站 R0.69P–R0.72X 只列为研究笔记"),
        ("/recap-r0-61-r0-72w.html", "/recap-r0-61-r0-72x.html"),
        ("文献综述 v1.36 · 2026-08-28", "文献综述 v1.37 · 2026-08-28"),
        ("累计回顾与 113 节索引", "累计回顾与 114 节索引"),
        ("打开 113 节完整索引", "打开 114 节完整索引"),
    ):
        html = required(html, old, new, "W literature " + old)
    html = once(
        html,
        LITERATURE_W_OVERVIEW,
        LITERATURE_X_OVERVIEW,
        "W literature overview",
    )
    old_open = '<div class="route-step pause"><header><b>开放接口 · R0.72X</b><strong>outer A1 plus A2 exact time concatenation</strong></header><p>连接 pre/post-collision nondegenerate intervals 与 exact collision block，保留 Fourier normalization、scalar gauges、energy factors 和 row-summation constants。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.72X</b><strong>all-center A2 path and scoped A1--A2--A1 cocycle</strong></header><p>fixed physical compact 上的 all-start、integrated scale 与 Bloch twists 只属于 A2 exact path；fixed-margin Coble--He 与 exact A2 的 fast-history cocycle 只声明 periodic representative beta=0。三项不安全外推为 FALSE；forced transfer 与完整线性化系统仍 OPEN。<a href="/notes/r0-72x.html">研究笔记</a> <a href="/recap-r0-61-r0-72x.html">当前累计回顾</a> <a href="#r072x-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72Y</b><strong>complete linearized row ledger with forced transfer</strong></header><p>恢复每行 coupling、Bloch residue、scalar damping、weak/zero modes 与 scale-sharp forced terms，再检验 triangular subsystem 的 \(\ell^2\) direct sum。</p></div>'''
    html = once(html, old_open, new_steps, "X literature route")
    boundary = r'''

          <h3 id="r072x-boundary">R0.72X 的 all-center theorem、A1 输入与文献边界</h3>
          <p>Coble--He Theorem 1.2 支持 periodic representative beta=0 的 fixed-margin A1 propagation；它不提供 shrinking fold interface 的 uniform constants，也没有在本节中扩展到 arbitrary Bloch twist。all-center、all-start 与 Bloch-uniformity 只属于 exact A2 path。我只报告 bounded primary-source search；它不构成新颖性、优先权或不存在性证明。</p>
          <div class="boundary"><strong>R0.72X 的主张边界</strong><p>allCenterExactFamilyGraphCoercivity=CLOSED、allStartExactPathSemigroup=CLOSED 与 uniformTwistedPeriodicGraph=CLOSED 属于 A2 exact path。fixedMarginA1EnhancedDissipation=CLOSED 与 exactA1A2A1TimeConcatenation=CLOSED 只对 beta=0。shrinkingInterfaceFixedShapeA1Hypotheses=FALSE，prefactorOneAllGapExponential=FALSE，allPhysicalRowsUniformContraction=FALSE。forcedHMinusOneTransfer=OPEN，completeLinearizedShearSubsystem=OPEN，nonlinearNavierStokes=OPEN，Clay=OPEN。</p></div>'''
    match = re.search(r'(<h3 id="r072w-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("X literature expected R0.72W boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "X literature boundary")
    assert_clean(html, "R0.72X literature")
    assert_mathjax_clean(html, "R0.72X literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    notes = len(list((PUBLIC / "notes").glob("*.html")))
    if notes != 174:
        raise RuntimeError(f"expected 174 public HTML notes after R0.72X, got {notes}")

    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    release.update({
        "latestCompletedRelease": "r072x",
        "siteVersion": "1.37",
        "publicHtmlNoteCount": 174,
        "postR060RecapNodeCount": 114,
        "nextRelease": "r072y",
        "latestReleaseGate": "tests/r072x-exact-path-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072x-release.test.mjs",
        "postR070APublishedReleaseCount": 76,
        "postR070AFormalSealedReleaseCount": 52,
        "legacyFormalFigureBacklogCount": 24,
    })
    release.pop("nextReleaseSourceStage", None)
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.36", "R0.72W", 173):
        raise RuntimeError("site-version is not at R0.72W")
    site.update({"version": "1.37", "latestRelease": "R0.72X", "publicHtmlNoteCount": 174, "publishedDate": "2026-08-28"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    current = (
        inventory.get("latestPublishedRelease"),
        inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"),
        inventory.get("legacyFormalFigureBacklogCount"),
    )
    if current != ("r072w", 75, 51, 24):
        raise RuntimeError("formal archive inventory is not at R0.72W")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072w" or "r072x" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72W")
        inventory[key].append("r072x")
    inventory.update({
        "latestPublishedRelease": "r072x",
        "publishedReleaseCount": 76,
        "formalSealedReleaseCount": 52,
        "legacyFormalFigureBacklogCount": 24,
    })
    if len(inventory["publishedReleases"]) != 76 or len(inventory["formalSealedReleases"]) != 52:
        raise RuntimeError("formal archive count mismatch after R0.72X")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "VERSION").write_text("1.37\n", encoding="utf-8")


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
        "notes/r0-72x.html",
        "recap-r0-61-r0-72x.html",
    ):
        content = (PUBLIC / relative).read_text(encoding="utf-8")
        assert_clean(content, relative)
        assert_mathjax_clean(content, relative, check_naked=False)
    print(json.dumps({
        "release": "R0.72X",
        "siteVersion": "1.37",
        "notes": 174,
        "recapNodes": 114,
        "published": 76,
        "formalSealed": 52,
        "legacyBacklog": 24,
        "phases": 33,
        "routeNotes": 84,
        "next": "R0.72Y",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
