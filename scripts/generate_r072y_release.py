#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed R0.72Y full-row and forced-transfer release.

R0.72Y closes the exact Fourier--Leray and Orr--Sommerfeld--Squire row
identities, the scalar forced-transfer scales, and an exact lift-up negative
result.  It does not close the low-gap complete vector row, nonlinear
Navier--Stokes, or the Clay problem.
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


ROOT = Path(os.environ.get("R072Y_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_ID = "fig-r072y-full-row-forced-transfer"
FIGURE_RELATIVE = f"figures/r072y/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r072y"

R072X_RELEASE_BASELINE = {
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
}

SOURCE_STAGE_CONTRACT = {
    "release": "r072y",
    "stage": "source-freeze",
    "publicationStatus": "pending-formal-certificate-figure-and-publication",
    "publicCountersAdvanced": False,
    "report": "research/r072y_report-source.md",
    "literatureAudit": "research/r072y_literature_audit.md",
    "gapMatrix": "research/r072y_gap_matrix.md",
    "independentAudit": "research/r072y_independent_audit.md",
    "producer": "research/certificates/r072y/generate_certificate.py",
    "independentProducer": "research/certificates/r072y/independent_recompute.py",
    "comparator": "research/certificates/r072y/validate_certificate.py",
    "certificateDirectory": CERTIFICATE_RELATIVE,
    "figureDirectory": FIGURE_RELATIVE,
    "generator": "scripts/generate_r072y_release.py",
    "translationScript": "scripts/add-r072y-translations.mjs",
    "releaseGate": "tests/r072y-full-row-forced-gate.test.mjs",
    "publicationTest": "tests/r072y-release.test.mjs",
}

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
    "A1 extension。shrinking-interface fixed-shape A1 hypotheses、prefactor-one all-gap "
    "exponential 和 every physical row strict contraction 均为 FALSE。forced H^-1 "
    "transfer、complete linearized shear subsystem、nonlinear Navier--Stokes 与 Clay "
    "保持 OPEN。"
)

LITERATURE_Y_OVERVIEW = (
    "这里没有完成 global caustic image，也没有证明一般三维 Navier--Stokes 正则性。"
    "R0.72T--W 固定并闭合 exact scalar A2 collision block，R0.72X 再得到 fixed physical "
    "compact 上的 all-start A2 path；Bloch-uniformity 仍只属于该 scalar path。R0.72Y "
    "从 Navier--Stokes 重新推导完整 Fourier--Leray row、pressure factor two、"
    "Orr--Sommerfeld--Squire triangularization 和 velocity recovery，并把 scalar invariant "
    "row 的 forcing 结论按空间范数拆开：standard H^-1 spacetime transfer 是 alpha，"
    "semiclassical H^-1 spacetime transfer 是 alpha^2，standard endpoint 没有 vanishing "
    "alpha gain。exact zero-coupling lift-up 说明 epsilon-only full-row closure 与 every-row "
    "strict contraction 为 FALSE。strong complete-row A2 estimate、low-gap vector direct sum、"
    "complete linearized shear subsystem、nonlinear Navier--Stokes 与 Clay 保持 OPEN。"
)


NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.72Y · FOURIER--LERAY ROWS · FORCED TRANSFER</div>
        <h1>从标量碰撞行回到完整三维线性化：<br>受迫传递与 lift-up 边界</h1>
        <p class="lead">我从 Navier--Stokes 重新推导完整 Fourier--Leray row，固定 pressure factor two、Orr--Sommerfeld--Squire 符号、velocity recovery 和特殊零行。R0.72X 的 scalar invariant row 给出三种不同的 forcing scale；exact lift-up 解同时排除只依赖 \(\varepsilon_j\) 的 full-row strict contraction。完整 low-gap 向量行仍未闭合。</p></div>
      <div class="stamp"><span class="state">状态 · R0.72Y row ledger 完成</span><strong>exact row identities and scoped scalar forcing</strong><p>版本 v0.72Y · 2026-08-28</p><p>complete row algebra: CLOSED</p><p>standard H^-1 spacetime: alpha</p><p>semiclassical H^-1 spacetime: alpha^2</p><p>uniform full-row contraction: FALSE</p><p>strong full-row A2: OPEN</p><p>nonlinear / Clay: OPEN</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>完整 row 恒等式和标量受迫尺度已闭合；完整强耦合行仍开放</h2><div class="verdict-grid"><div class="verdict-card true"><strong>CLOSED · EXACT ROW LEDGER</strong><p>exactThreeDimensionalLinearization、exactPressurePoissonFactorTwo、exactOSSquireTriangularization、exactVelocityReconstruction 与 fullRowEnergyIdentity 均为 CLOSED。</p></div><div class="verdict-card true"><strong>CLOSED · SCALAR FORCING</strong><p>strongRowL2ForcingDuhamelAlpha2、strongRowStandardHMinusOneTransferAlpha、strongRowSemiclassicalHMinusOneTransferAlpha2 与 strongForcedDirectSumNoCountLoss 均为 CLOSED。</p></div><div class="verdict-card false"><strong>FALSE · UNSAFE EXTENSIONS</strong><p>scalarA2EqualsCompleteRow、epsilonOnlyFullRowClosure、allPhysicalRowsUniformStrictContraction、standardHMinusOneTransferAlpha2 与 HMinusOneEndpointAlphaGain 均为 FALSE。</p></div><div class="verdict-card false"><strong>OPEN · COMPLETE SYSTEM</strong><p>strongFullRowA2Estimate、scaleSharpOSPressureAbsorption、orientationUniformSquireTransfer、completeLinearizedShearSubsystem、nonlinearNavierStokes 与 Clay 均为 OPEN。</p></div></div></section>
        <section id="physical"><div class="section-no">01 / Physical linearization</div><h2>压力右端的 factor two 来自两个不同散度项</h2><div class="equation result">\[\partial_tu+V\partial_{x_3}u+u_2V_ye_3+\nabla p=\nu\Delta u,\qquad \nabla\cdot u=0,\]</div><div class="equation result">\[\Delta_Kp=-2iK_zV_yu_2.\]</div><p>一份 \(iK_zV_yu_2\) 来自 background transport，另一份来自 shear-gradient term；符号与 \(+\nabla p\) 在左侧的约定一起冻结。</p></section>
        <section id="row"><div class="section-no">02 / Bloch--Leray row</div><h2>完整 row label 同时保留水平方向与 residue class</h2><div class="equation result">\[j=(K_x,K_z,[r]_R),\quad A_\beta=\partial_x+i\beta,\quad \mathcal L=-A_\beta^2+\mu,\quad \mu=\xi^2+\gamma^2,\]</div><div class="equation result">\[\mathbb P_j=I+\nabla_j\mathcal L^{-1}\operatorname{div}_j,\qquad u_d=-\mathcal Lu-\mathbb P_j(icWu+\Lambda W_xu_2e_3).\]</div><p>orthogonal direct sum 是结构恒等式；它不会自动生成 row-uniform bound。</p></section>
        <section id="os"><div class="section-no">03 / Orr--Sommerfeld--Squire</div><h2>μ&gt;0 时得到精确三角系统</h2><div class="equation result">\[q=\mathcal Lu_2,\qquad \eta=i\gamma u_1-i\xi u_3,\]</div><div class="equation result">\[q_d=(-\mathcal L-icW)q-icW_{xx}\mathcal L^{-1}q,\]</div><div class="equation result">\[\eta_d=(-\mathcal L-icW)\eta+i\xi\Lambda W_x\mathcal L^{-1}q.\]</div><p>pressure feedback 与 Squire transfer 的尺度不同；μ=0 不能套用这组逆公式。</p></section>
        <section id="recovery"><div class="section-no">04 / Velocity recovery</div><h2>速度恢复与 kinetic energy identity 均保留方向权重</h2><div class="equation result">\[u_1=\frac{i}{\mu}(\xi A_\beta u_2-\gamma\eta),\qquad u_3=\frac{i}{\mu}(\gamma A_\beta u_2+\xi\eta),\]</div><div class="equation result">\[\|u\|_2^2=\|u_2\|_2^2+\mu^{-1}(\|A_\beta u_2\|_2^2+\|\eta\|_2^2).\]</div></section>
        <section id="embedding"><div class="section-no">05 / Scalar embedding</div><h2>R0.72X scalar operator 是完整 row 的严格不变子空间</h2><div class="equation result">\[u=g(\gamma,0,-\xi)/\sqrt\mu,\qquad g_d=(A_\beta^2-\mu)g-icWg.\]</div><p>scalarA2InvariantEmbedding=CLOSED；scalarA2EqualsCompleteRow=FALSE。一般数据仍会激活 pressure feedback 与 Squire transfer。</p></section>
        <section id="energy"><div class="section-no">06 / Full-row energy</div><h2>high-gap class 有显式衰减，low-gap class 没有被外推</h2><div class="equation result">\[\frac12\frac d{dd}\|u\|^2+\|A_\beta u\|^2+\mu\|u\|^2=-\Lambda\operatorname{Re}\langle W_xu_2,u_3\rangle.\]</div><p>若 \(g_j&gt;|\Lambda|M_K/2\)，则 norm exponent 是 \(g_j-|\Lambda|M_K/2\)。这是 damping-dominated full rows，不是完整 low-gap theorem。</p></section>
        <section id="lift"><div class="section-no">07 / Exact lift-up obstruction</div><h2>zero coupling 仍可产生严格 transient growth</h2><div class="equation result">\[u_2(d)=e^{-\xi^2d}v_0,\qquad u_3(d)=-\Lambda d e^{-\xi^2d}W_x(d,x)v_0,\]</div><div class="equation result">\[\frac{\|u(d)\|^2}{\|u(0)\|^2}=e^{-2\xi^2d}\left[1+\frac{\Lambda^2d^2}{8}(e^{-2d}+e^{-8d})\right].\]</div><p>ξ=0 时任意非零 Λ 都增长；ξ&gt;0 给 spatially mean-zero 扰动，取足够大的 |Λ| 仍可增长。因此 epsilonOnlyFullRowClosure=FALSE，allPhysicalRowsUniformStrictContraction=FALSE。</p></section>
        <section id="kernel"><div class="section-no">08 / Exact causal kernel</div><h2>几何 block envelope 直接给出 scalar L2 forcing 的 alpha-squared scale</h2><div class="equation result">\[\int_0^\infty\!\left(e^{-\mu r}q^{\lfloor r/h\rfloor}\right)^pdr=\frac{1-e^{-p\mu h}}{p\mu(1-q^pe^{-p\mu h})},\qquad h=2T\alpha^2.\]</div><p>\(\mu\to0\) 的极限是 \(h/(1-q^p)\)。Young convolution 给 \(L_d^2L_x^2\to L_d^2L_x^2\) 的 \(O(\alpha^2)\) bound。</p></section>
        <section id="negative"><div class="section-no">09 / Negative Sobolev forcing</div><h2>standard 与 semiclassical negative norm 必须分开</h2><div class="equation result">\[\|G\|_{L_d^2L_x^2}\le C_q\alpha\|F\|_{L_d^2H^{-1}_\beta},\]</div><div class="equation result">\[\|G\|_{L_d^2L_x^2}\le C_q\alpha^2\|F\|_{L_d^2\mathcal H^{-1}_{\alpha,\beta}}.\]</div><p>两条结论来自 backward-adjoint energy 与 transposition；standardHMinusOneTransferAlpha2=FALSE。</p></section>
        <section id="endpoint"><div class="section-no">10 / Endpoint boundary</div><h2>standard endpoint 只有 scale one；semiclassical endpoint 有 alpha</h2><div class="equation result">\[\max\{\|G\|_{L_d^\infty L_x^2},\|A_\beta G\|_{L_d^2L_x^2}\}\le C_q'\|F\|_{L_d^2H^{-1}_\beta}.\]</div><p>semiclassical 输入的右端另有一个 α。terminal high-frequency pulse 给 order-one endpoint response，所以 HMinusOneEndpointAlphaGain=FALSE。</p></section>
        <section id="sharpness"><div class="section-no">11 / Sharpness</div><h2>collision-chart witness 分别饱和 alpha 与 alpha-squared</h2><p>compactly supported mean-zero witness 的 scaling ratios 分别是 standard \(H^{-1}\) 的 \(\alpha\) 和 semiclassical negative norm 的 \(\alpha^2\)；证明使用解析缩放与极限，不由有限证书代替。</p></section>
        <section id="weak"><div class="section-no">12 / Weak and zero rows</div><h2>有限历史 energy ledger 闭合，但没有共同 strong scale</h2><p>weak/zero scalar rows 有 \(O_K(1)\) 的 finite-history bound；有 covariant gap 时还有 time-global estimate。gapless constant row 在持续 forcing 下线性增长。mean-zero 也不在 \(WG\) 下自动保持。</p></section>
        <section id="literature"><div class="section-no">13 / Literature boundary</div><h2>已有 forced 与 vector 先例，但现有方法没有覆盖本节组合</h2><p>Wei--Zhang 已在 monotone Couette 邻域给出 nonautonomous forced 和三维向量闭合；该坐标法在 \(V_y=0\) 的 collision 处失效。Coble--He 的 fixed-shape homogeneous theorem 不含 forcing 或完整向量行。我只报告有界原始文献核验，不把“未发现”写成首创性证明。</p></section>
        <section id="evidence"><div class="section-no">14 / Evidence boundary</div><h2>有限代数、函数分析和附图各有明确职责</h2><p>双路证书核对 heat identity、pressure factor、Leray signs、OS--Squire coefficients、velocity recovery、lift-up residual、kernel algebra 与 Fourier weights。Galerkin limit、duality、endpoint trace、sharpness limit 和 evolution-family existence 由解析报告承担。附图只可视化精确公式与已证明 power guides。</p></section>
        <section id="figure"><div class="section-no">15 / Journal figure</div><h2>正式附图分开显示 row structure、lift-up 与 forcing powers</h2><p><img src="/assets/r072y/fig-r072y-full-row-forced-transfer.svg" alt="R0.72Y full Fourier row, exact lift-up counterexample, and forced-transfer scales"></p><p><a href="/assets/r072y/fig-r072y-full-row-forced-transfer.pdf">下载 PDF</a> · <a href="/assets/r072y/fig-r072y-full-row-forced-transfer.png">下载 PNG</a> · <a href="/assets/r072y/fig-r072y-full-row-forced-transfer.svg">打开 SVG</a></p></section>
        <section id="value"><div class="section-no">16 / Research value</div><h2>本节把 scalar result 放回正确的完整线性边界</h2><p>严格价值在于不再把 scalar A2 estimate 与 complete vector row 混同，并固定了 forcing topology 对 α power 的影响。直接 Clay 价值仍低：low-gap vector estimate、nonlinear convolution、vortex stretching bootstrap 与 continuation criterion 都未完成。</p></section>
        <section id="next"><div class="section-no">17 / Next gate</div><h2>R0.72Z：吸收 Orr--Sommerfeld feedback，并支付 orientation-dependent Squire transfer</h2><p>下一节直接研究 \(q\to\eta\) 三角系统，按 \(|\xi/\gamma|\)、damping gap 与 \(\mu=0\) exceptional rows 分区；任何结论都必须保留 lift-up transient prefactor。</p></section>
        <section id="reproduce"><div class="section-no">18 / Reproduction</div><h2>完整报告、边界矩阵、独立审计、证书与附图</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072y_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072y_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072y_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072y_independent_audit.md">独立数学审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072y">确定性双路证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r072y/fig-r072y-full-row-forced-transfer">正式附图包</a> · <a href="/notes/r0-72y.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-72y.html">累计回顾</a> · <a href="/recap-r0-61-r0-72y.pdf">累计回顾 PDF</a></p></section>
      </article>'''

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.72Z</span><span class="tree-state current">下一检查点</span></div>
              <h3>collision-scale Orr--Sommerfeld absorption with orientation payment</h3><p>直接处理 pressure feedback 与 Squire transfer，按 orientation ratio、damping gap 和 exceptional rows 分区，并保留 exact lift-up transient prefactor。</p>
            </article>'''

HOME_Y_CARD = r'''          <div class="task-one" id="r072y" data-release="r072y" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.72Y · 2026-08-28</p><h3>从 scalar collision row 回到完整三维线性化：forced transfer 与 lift-up boundary</h3>
            <p>完整 Fourier--Leray row、pressure factor two、Orr--Sommerfeld--Squire signs、velocity recovery 和 exceptional rows 已逐项冻结。</p><p>scalar invariant rows 的 standard H^-1 spacetime scale 是 alpha，semiclassical scale 是 alpha-squared；standard endpoint 没有 vanishing alpha gain。exact zero-coupling lift-up 排除 epsilon-only full-row closure。</p>
            <p><strong>结论边界：</strong>&nbsp;strongFullRowA2Estimate、completeLinearizedShearSubsystem、nonlinearNavierStokes 与 Clay 保持 OPEN。</p>
            <p><a href="/notes/r0-72y.html"><strong>阅读 R0.72Y 研究笔记 →</strong></a><br><a href="/notes/r0-72y.pdf">下载同步研究笔记 PDF</a> · <a href="/assets/r072y/fig-r072y-full-row-forced-transfer.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072y">查看确定性证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r072y_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-72y.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.72Z：</strong>&nbsp;collision-scale OS pressure absorption and orientation-dependent Squire transfer。</p>
          </div>'''


def _validate_source_stage_manifest(release: dict) -> None:
    for key, value in R072X_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72X: {key}")
    if release.get("nextReleaseSourceStage") != SOURCE_STAGE_CONTRACT:
        raise RuntimeError("R0.72Y source-stage manifest contract is missing, stale, or has extra fields")


def preflight_release_state() -> None:
    release = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    expected_site = {
        "schemaVersion": "research-site-version-v1",
        "version": "1.37",
        "latestRelease": "R0.72X",
        "publicHtmlNoteCount": 174,
        "publishedDate": "2026-08-28",
    }
    if json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8")) != expected_site:
        raise RuntimeError("public site-version is not exactly at R0.72X")
    if len(list((PUBLIC / "notes").glob("*.html"))) != 174:
        raise RuntimeError("R0.72X preflight expected 174 public HTML notes")
    for relative in ("notes/r0-72y.html", "notes/r0-72y.pdf", "recap-r0-61-r0-72y.html", "recap-r0-61-r0-72y.pdf"):
        if (PUBLIC / relative).exists():
            raise RuntimeError(f"R0.72X preflight found premature public output: {relative}")
    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in ('data-site-version="1.37"', "<strong>174</strong>公开研究笔记", "<strong>R0.72X</strong>最新研究节点", 'aria-label="R0.69P–R0.72X"'):
        if token not in home:
            raise RuntimeError(f"R0.72X home baseline missing token: {token}")
    if 'data-release="r072y"' in home:
        raise RuntimeError("R0.72X home already contains an R0.72Y card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72X">(.*?)</nav>', home, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 84:
        raise RuntimeError("R0.72X home route expected 84 notes")
    recap = (PUBLIC / "recap-r0-61-r0-72x.html").read_text(encoding="utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 114 or len(set(links)) != 114 or recap.count('<article class="phase">') != 33:
        raise RuntimeError("R0.72X recap baseline expected 114 unique nodes and 33 phases")
    literature = (PUBLIC / "literature-review.html").read_text(encoding="utf-8")
    if literature.count(LITERATURE_X_OVERVIEW) != 1 or literature.count("开放接口 · R0.72Y") != 1:
        raise RuntimeError("R0.72X literature baseline is stale")
    inventory = json.loads((ROOT / "research/formal-archive-inventory.json").read_text(encoding="utf-8"))
    if (inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"), inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount")) != ("r072x", 76, 52, 24):
        raise RuntimeError("formal archive inventory is not at R0.72X")
    if inventory["publishedReleases"][-1] != "r072x" or inventory["formalSealedReleases"][-1] != "r072x" or "r072y" in inventory["publishedReleases"] or "r072y" in inventory["formalSealedReleases"]:
        raise RuntimeError("formal archive lists are not append-only from R0.72X")


def _binding_paths(manifest: dict) -> set[str]:
    bindings = manifest.get("sourceBindings")
    if not isinstance(bindings, list):
        raise RuntimeError("formal certificate sourceBindings are missing")
    paths = {row.get("path") for row in bindings if isinstance(row, dict)}
    if None in paths or len(paths) != len(bindings):
        raise RuntimeError("formal certificate sourceBindings are malformed or duplicated")
    return paths


def validate_inputs() -> None:
    required_inputs = (
        "research/r072y_report-source.md", "research/r072y_literature_audit.md",
        "research/r072y_gap_matrix.md", "research/r072y_independent_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md", f"{CERTIFICATE_RELATIVE}/crosscheck.json",
        f"{CERTIFICATE_RELATIVE}/manifest.json", f"{FIGURE_RELATIVE}/manifest.json",
        "public/notes/r0-72x.html", "public/recap-r0-61-r0-72x.html",
    )
    for relative in required_inputs:
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.72Y release input: {relative}")
    report = (ROOT / "research/r072y_report-source.md").read_text(encoding="utf-8")
    for token in (
        "exactThreeDimensionalLinearization", "exactPressurePoissonFactorTwo",
        "exactOSSquireTriangularization", "exactVelocityReconstruction",
        "exactZeroCouplingLiftUpFormula", "strongRowStandardHMinusOneTransferAlpha",
        "strongRowSemiclassicalHMinusOneTransferAlpha2", "standardHMinusOneTransferAlpha2",
        "HMinusOneEndpointAlphaGain", "strongFullRowA2Estimate",
        "completeLinearizedShearSubsystem", "nonlinearNavierStokes", "Clay",
    ):
        if token not in report:
            raise RuntimeError(f"R0.72Y report missing stable token: {token}")
    audit = (ROOT / "research/r072y_independent_audit.md").read_text(encoding="utf-8")
    for token in ("**Outcome:** **PASS**", "Pressure and Leray signs", "Orr--Sommerfeld--Squire audit", "Exact lift-up counterexample", "Negative-Sobolev duality audit", "Final publication decision"):
        if token not in audit:
            raise RuntimeError(f"R0.72Y independent audit missing token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.72Y certificate")
    verify_flat_hash_ledger(figure, "R0.72Y figure")
    certificate_manifest = json.loads((certificate / "manifest.json").read_text(encoding="utf-8"))
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    source_commit = str(certificate_manifest.get("sourceCommit", ""))
    if certificate_manifest.get("status") != "formal" or not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("R0.72Y certificate is not formal or source-frozen")
    if crosscheck.get("status") != "passed" or crosscheck.get("formalSourceReady") is not True or crosscheck.get("temporaryUnsealedSourceAllowed") is not False:
        raise RuntimeError("R0.72Y certificate crosscheck is not formal")
    if crosscheck.get("sourceCommit") != source_commit or crosscheck.get("sourceBindings") != certificate_manifest.get("sourceBindings") or not all(crosscheck.get("checks", {}).values()):
        raise RuntimeError("R0.72Y certificate lineage or exhaustive checks failed")
    expected_bound_sources = {
        "research/r072y_report-source.md", "research/r072y_gap_matrix.md",
        "research/r072y_literature_audit.md", "research/r072y_independent_audit.md",
        "research/certificates/r072y/generate_certificate.py",
        "research/certificates/r072y/independent_recompute.py",
        "research/certificates/r072y/validate_certificate.py",
        "scripts/generate_r072y_release.py", "scripts/add-r072y-translations.mjs",
        "tests/r072y-full-row-forced-gate.test.mjs", "tests/r072y-release.test.mjs",
        "tests/r072y-deterministic-certificate-source.test.mjs",
        "tests/r072y-full-row-forced-transfer-figure-source.test.mjs",
        f"{FIGURE_RELATIVE}/contract.json", f"{FIGURE_RELATIVE}/config.json",
        f"{FIGURE_RELATIVE}/caption.md", f"{FIGURE_RELATIVE}/README.md",
    }
    missing_bindings = expected_bound_sources - _binding_paths(certificate_manifest)
    if missing_bindings:
        raise RuntimeError(f"R0.72Y formal source binding is incomplete: {sorted(missing_bindings)}")
    subprocess.run([sys.executable, str(certificate / "validate_certificate.py"), "--require-formal"], cwd=ROOT, check=True)

    manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("release") != "R0.72Y" or manifest.get("figureId") != FIGURE_ID:
        raise RuntimeError("R0.72Y figure identity mismatch")
    if manifest.get("status") != "formal" or manifest.get("qa", {}).get("status") != "passed" or manifest.get("qa", {}).get("visualInspectionExplicit") is not True:
        raise RuntimeError("R0.72Y figure is not formally validated")
    git = manifest.get("git", {})
    certificate_commit = str(git.get("certificateCommit", ""))
    if git.get("sourceCommit") != source_commit or not re.fullmatch(r"[0-9a-f]{40}", certificate_commit) or certificate_commit == source_commit:
        raise RuntimeError("R0.72Y figure does not preserve two-commit lineage")
    expected_claims = {
        "exactThreeDimensionalLinearizationClosedInBoundReport": True,
        "exactPressurePoissonFactorTwoClosedInBoundReport": True,
        "exactOSSquireTriangularizationForMuPositiveClosedInBoundReport": True,
        "scalarA2InvariantEmbeddingClosedInBoundReport": True,
        "exactZeroCouplingLiftUpFormulaClosedInBoundReport": True,
        "strongRowStandardHMinusOneSpacetimeAlphaClosedInBoundReport": True,
        "strongRowSemiclassicalHMinusOneSpacetimeAlphaSquaredClosedInBoundReport": True,
        "standardHMinusOneEndpointAlphaGain": False,
        "allPhysicalRowsUniformStrictContraction": False,
        "strongFullRowA2Estimate": False,
        "completeLinearizedShearSubsystemProved": False,
        "nonlinearNavierStokesClosureProved": False,
        "clayMillenniumProblemSolved": False,
        "figureIsAnalyticProof": False,
        "ratesAreFitted": False,
    }
    if manifest.get("claimBoundary") != expected_claims:
        raise RuntimeError("R0.72Y figure claim boundary is not exact")
    subprocess.run([sys.executable, str(figure / "validate.py"), "--require-formal"], cwd=ROOT, check=True)
    if manifest.get("publication", {}).get("directory") != "public/assets/r072y":
        raise RuntimeError("R0.72Y figure publication directory mismatch")
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = PUBLIC / "assets/r072y" / f"{FIGURE_ID}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.72Y public {suffix} is absent or not byte-identical")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72x.html").read_text(encoding="utf-8")
    for index, (pattern, value) in enumerate((
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.72Y：完整 Fourier--Leray row、精确 lift-up 边界，以及按空间范数区分的 scalar forced-transfer scales。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.72Y｜Full Fourier--Leray rows, forced transfer, and lift-up boundary">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="完整 row 恒等式与 scalar forcing scales 已闭合；uniform full-row contraction 为 FALSE，strong full-row A2 与 nonlinear/Clay 保持 OPEN。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r072y/fig-r072y-full-row-forced-transfer.png">'),
        (r'<title>.*?</title>', '<title>R0.72Y｜Full Fourier--Leray rows, forced transfer, and lift-up boundary</title>'),
    )):
        html = section(html, pattern, value, f"Y note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.37", "/i18n-en.js?v=1.38", "Y note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#physical">线性化</a><a href="#row">row</a><a href="#os">OS--Squire</a><a href="#recovery">恢复</a><a href="#embedding">标量嵌入</a><a href="#energy">能量</a><a href="#lift">lift-up</a><a href="#kernel">kernel</a><a href="#negative">negative norm</a><a href="#endpoint">端点</a><a href="#sharpness">sharpness</a><a href="#weak">弱行</a><a href="#literature">文献</a><a href="#evidence">证据</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "Y note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "Y note hero")
    toc = '''      <aside class="toc"><strong>CONTENTS</strong><ol>
        <li><a href="#result">00 · direct decision</a></li><li><a href="#physical">01 · physical linearization</a></li><li><a href="#row">02 · Bloch--Leray row</a></li><li><a href="#os">03 · OS--Squire</a></li><li><a href="#recovery">04 · velocity recovery</a></li><li><a href="#embedding">05 · scalar embedding</a></li><li><a href="#energy">06 · full-row energy</a></li><li><a href="#lift">07 · lift-up obstruction</a></li><li><a href="#kernel">08 · causal kernel</a></li><li><a href="#negative">09 · negative Sobolev forcing</a></li><li><a href="#endpoint">10 · endpoint boundary</a></li><li><a href="#sharpness">11 · sharpness</a></li><li><a href="#weak">12 · weak and zero rows</a></li><li><a href="#literature">13 · literature boundary</a></li><li><a href="#evidence">14 · evidence boundary</a></li><li><a href="#figure">15 · journal figure</a></li><li><a href="#value">16 · value</a></li><li><a href="#next">17 · R0.72Z</a></li><li><a href="#reproduce">18 · reproduction</a></li>
      </ol></aside>'''
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "Y note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "Y note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.72Y · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "Y note footer")
    assert_clean(html, "R0.72Y note")
    assert_mathjax_clean(html, "R0.72Y note")
    (PUBLIC / "notes/r0-72y.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72x.html").read_text(encoding="utf-8")
    html = required(html, "/i18n-en.js?v=1.37", "/i18n-en.js?v=1.38", "Y recap i18n")
    for label, pattern, value in (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.72Y 的 115 个节点；最新一节固定完整 row 账本、scalar forcing scales 与 lift-up 边界。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.72Y｜R0.60 之后的研究回顾">'),
        ("og desc", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="三十四个阶段、115 个节点：从约化递推到完整 Fourier row、forced transfer 与 lift-up boundary。">'),
        ("title", r'<title>.*?</title>', '<title>R0.61–R0.72Y｜R0.60 之后的研究回顾</title>'),
    ):
        html = section(html, pattern, value, "Y recap " + label)
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.72Y · 2026-08-28</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页接在 R0.00–R0.60 的阶段回顾之后，完整保留 R0.61 到 R0.72Y 的 115 个研究节点。R0.69P 以后的路线从局部证书推进到 scalar A2 collision path，再在 R0.72Y 回到完整 Fourier--Leray linearized row。scalar forced transfer 按 standard 与 semiclassical negative norms 分开闭合；exact lift-up 排除 epsilon-only full-row strict contraction。完整 low-gap vector row、nonlinear Navier--Stokes 与 Clay 都没有被外推。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.72Y</strong><p>收录节点：115</p><p>回顾截止时公开笔记：175</p><p>回顾截止节点：R0.72Y</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "Y recap hero")
    html = required(html, "02 · 114 节完整索引", "02 · 115 节完整索引", "Y recap toc")
    html = required(html, "01 · 三十三个研究阶段", "01 · 三十四个研究阶段", "Y recap phase toc")
    html = required(html, "R0.60 之后的路线分成三十三个阶段", "R0.60 之后的路线分成三十四个阶段", "Y recap phase heading")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>115</strong><span>R0.61–R0.72Y 研究节点</span></div><div class="metric"><strong>77</strong><span>R0.70A–R0.72Y 已公开版本</span></div><div class="metric"><strong>53</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.70A–R0.72Y 的 77 个版本已公开，其中 53 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "Y recap result")
    new_phase = r'''            <article class="phase"><h3>R0.72Y · full Fourier row, forced scalar transfer, and lift-up boundary</h3><p>完整 physical linearization、pressure factor two、Bloch--Leray row、OS--Squire triangularization、velocity recovery、energy identity 与 exceptional-row split 均为 CLOSED。</p><p>scalar invariant rows 的 standard H^-1 spacetime transfer 是 alpha，semiclassical transfer 是 alpha-squared；standard endpoint alpha gain 为 FALSE。exact lift-up 同时排除 epsilon-only full-row closure。</p><p>strongFullRowA2Estimate、completeLinearizedShearSubsystem、nonlinearNavierStokes 与 Clay 保持 OPEN。</p><div class="links"><a href="/notes/r0-72y.html">R0.72Y</a><a href="/assets/r072y/fig-r072y-full-row-forced-transfer.pdf">R0.72Y 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072y">R0.72Y 证书</a></div></article>
'''
    html = once(html, "          </div>\n        </section>\n\n        <section id=\"node-index\">", new_phase + "          </div>\n        </section>\n\n        <section id=\"node-index\">", "Y recap phase")
    html = required(html, "R0.61–R0.72X 的 114 节公开笔记", "R0.61–R0.72Y 的 115 节公开笔记", "Y recap node title")
    node_x = '            <span class="node-ref"><a href="/notes/r0-72x.html">R0.72X</a><span class="node-state kind-closed">闭</span></span>\n'
    node_y = '            <span class="node-ref"><a href="/notes/r0-72y.html">R0.72Y</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_x, node_x + node_y, "Y recap node")
    retained = r'''            <li>R0.72Y 恢复完整 Fourier--Leray row，并分开 scalar forcing powers 与 full-row OPEN boundary；exact lift-up 排除 epsilon-only strict contraction。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "Y recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>scalar forcing 结论进入完整 row 账本，但没有成为 full-row theorem</h2><p>不能把 115 个节点或 77 个公开版本解释成 Clay 问题完成比例。R0.72Y 的严格增量是 exact row identities、按 norm 区分的 scalar forcing scales 与 lift-up negative result；直接 Clay 价值仍低。</p></section>''', "Y recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.72Z 处理 OS pressure absorption 与 orientation payment</h2><p>直接研究 \(q\to\eta\) 三角系统，按 orientation ratio、damping gap 和 exceptional rows 分区，并保留 lift-up transient prefactor。</p></section>''', "Y recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.72Y 的 77 节已公开；53 节完整封存；24 节旧档待回补。</p><p>epsilonOnlyFullRowClosure、allPhysicalRowsUniformStrictContraction、standardHMinusOneTransferAlpha2 与 HMinusOneEndpointAlphaGain 为 FALSE；strongFullRowA2Estimate、completeLinearizedShearSubsystem、nonlinearNavierStokes 与 Clay 为 OPEN。</p></section>''', "Y recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72x.html">保留 R0.72X 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-72y.html">打开最新节点 R0.72Y</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r072y">查看 R0.72Y 确定性证书</a> · <a href="/assets/r072y/fig-r072y-full-row-forced-transfer.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-72y.pdf">下载同步 PDF</a></p><p>完整节点索引保留 R0.61 起的全部历史编号；状态标签只描述证据类型。</p></section>''', "Y recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.72Y 回顾 · 2026-08-28<br><a href="/">返回研究主页</a></div></footer>', "Y recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 115 or len(set(links)) != 115 or html.count('<article class="phase">') != 34:
        raise RuntimeError("R0.72Y recap expected 115 unique nodes and 34 phases")
    assert_clean(html, "R0.72Y recap")
    assert_mathjax_clean(html, "R0.72Y recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-72y.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.37"', 'data-site-version="1.38"'),
        ("/i18n-en.js?v=1.37", "/i18n-en.js?v=1.38"),
        ("/site-refresh.js?v=1.37", "/site-refresh.js?v=1.38"),
        ("<strong>v1.37</strong>网页版本", "<strong>v1.38</strong>网页版本"),
        ("<strong>174</strong>公开研究笔记", "<strong>175</strong>公开研究笔记"),
        ("<strong>R0.72X</strong>最新研究节点", "<strong>R0.72Y</strong>最新研究节点"),
        ("Research topology · R0.1–R0.72X", "Research topology · R0.1–R0.72Y"),
        ("R0.70A–R0.72X：76 节已公开，52 节完整封存", "R0.70A–R0.72Y：77 节已公开，53 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72X</span>', '<span class="route-range">R0.69P–R0.72Y</span>'),
        ('aria-label="R0.69P–R0.72X"', 'aria-label="R0.69P–R0.72Y"'),
        ("展开 84 篇公开笔记", "展开 85 篇公开笔记"),
        ("本站 R0.69P–R0.72X 路线", "本站 R0.69P–R0.72Y 路线"),
        ("综述 v1.37 · 2026-08-28", "综述 v1.38 · 2026-08-28"),
        ("上次综述 v1.36 · 2026-08-28", "上次综述 v1.37 · 2026-08-28"),
        ("/recap-r0-61-r0-72x.html", "/recap-r0-61-r0-72y.html"),
        ("/recap-r0-61-r0-72x.pdf", "/recap-r0-61-r0-72y.pdf"),
    ):
        html = required(html, old, new, "Y home " + old)
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.72Y 已固定完整 Fourier--Leray row 与 scalar forced-transfer scales，并用 exact lift-up 排除 epsilon-only full-row closure。下一关是 OS pressure absorption 与 orientation-dependent Squire transfer。</span></div>', "Y home focus")
    link_x = '<a class="milestone" href="/notes/r0-72x.html">R0.72X</a>'
    html = once(html, link_x, link_x + '\n                  <a class="milestone" href="/notes/r0-72y.html">R0.72Y</a>', "Y home route link")
    route_y = r'''              <p>R0.72Y 从 Navier--Stokes 恢复 complete Fourier--Leray row，闭合 pressure factor two、OS--Squire signs、velocity recovery、scalar invariant embedding 与按 norm 分层的 forced-transfer powers。exact zero-coupling lift-up 排除 epsilon-only strict contraction；strong complete-row A2 estimate 与 nonlinear/Clay 仍为 OPEN。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_y + '              <details class="tree-notes" open>', "Y home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "Y home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.72Y · 2026-08-28</p><h3>R0.60 recap 之后的累计回顾收录 115 个节点；全站现有 175 篇公开研究笔记</h3><p>累计回顾现分三十四个问题阶段，并给出 R0.61–R0.72Y 的完整索引；R0.72Y 分开记录 complete row identities、scalar forcing scales 与 lift-up boundary。</p><p>R0.70A–R0.72Y 共 77 个版本已公开；53 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;scalar forced transfer 已按 norm 分层闭合；complete low-gap vector row 与 nonlinear/Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-72y.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-72y.pdf">下载同步 PDF</a></p></div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "Y home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_Y_CARD + '\n        </section>\n\n      </article>', "Y home card")
    if html.count('data-release="r072y"') != 1:
        raise RuntimeError("home must contain exactly one R0.72Y card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72Y">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 85:
        raise RuntimeError("home current-route index must contain 85 note links")
    assert_clean(html, "R0.72Y home")
    assert_mathjax_clean(html, "R0.72Y home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.37", "/i18n-en.js?v=1.38"),
        ("本站 R0.69P–R0.72X 只列为研究笔记", "本站 R0.69P–R0.72Y 只列为研究笔记"),
        ("/recap-r0-61-r0-72x.html", "/recap-r0-61-r0-72y.html"),
        ("文献综述 v1.37 · 2026-08-28", "文献综述 v1.38 · 2026-08-28"),
        ("累计回顾与 114 节索引", "累计回顾与 115 节索引"),
        ("打开 114 节完整索引", "打开 115 节完整索引"),
    ):
        html = required(html, old, new, "Y literature " + old)
    html = once(html, LITERATURE_X_OVERVIEW, LITERATURE_Y_OVERVIEW, "Y literature overview")
    old_open = r'<div class="route-step pause"><header><b>开放接口 · R0.72Y</b><strong>complete linearized row ledger with forced transfer</strong></header><p>恢复每行 coupling、Bloch residue、scalar damping、weak/zero modes 与 scale-sharp forced terms，再检验 triangular subsystem 的 \(\ell^2\) direct sum。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.72Y</b><strong>full Fourier row, scalar forced transfer, and lift-up boundary</strong></header><p>完整 row algebra、scalar invariant embedding、按 norm 分层的 spacetime forcing scales 与 exact lift-up negative result 已闭合。standard endpoint alpha gain 为 FALSE；complete low-gap vector row 仍 OPEN。<a href="/notes/r0-72y.html">研究笔记</a> <a href="/recap-r0-61-r0-72y.html">当前累计回顾</a> <a href="#r072y-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.72Z</b><strong>OS pressure absorption and orientation-dependent Squire transfer</strong></header><p>直接研究 \(q\to\eta\) 三角系统，按 orientation ratio、damping gap 与 exceptional rows 分区，并保留 lift-up transient prefactor。</p></div>'''
    html = once(html, old_open, new_steps, "Y literature route")
    boundary = r'''

          <h3 id="r072y-boundary">R0.72Y 的 forced/vector 先例与 collision 边界</h3>
          <p>Wei--Zhang 已在 monotone Couette 邻域给出 nonautonomous structured forcing 与三维 vector/pressure closure；其 \(Y=V\) 坐标要求 \(V_y\neq0\)，不能直接穿过本节 collision。Coble--He 的 fixed-shape homogeneous theorem 不含 forcing、Bloch 或完整向量 row。Poiseuille 的 ordinary Fourier sum 也不证明 continuous Bloch-uniform full-row transfer。我只报告 bounded primary-source search；它不构成新颖性、优先权或不存在性证明。</p>
          <div class="boundary"><strong>R0.72Y 的主张边界</strong><p>complete row identities 与 scalar forced-transfer powers 为 CLOSED。epsilonOnlyFullRowClosure、allPhysicalRowsUniformStrictContraction、standardHMinusOneTransferAlpha2 与 HMinusOneEndpointAlphaGain 为 FALSE。strongFullRowA2Estimate、scaleSharpOSPressureAbsorption、orientationUniformSquireTransfer、completeLinearizedShearSubsystem、nonlinearNavierStokes 与 Clay 为 OPEN。</p></div>'''
    match = re.search(r'(<h3 id="r072x-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("Y literature expected R0.72X boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "Y literature boundary")
    assert_clean(html, "R0.72Y literature")
    assert_mathjax_clean(html, "R0.72Y literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    if len(list((PUBLIC / "notes").glob("*.html"))) != 175:
        raise RuntimeError("expected 175 public HTML notes after R0.72Y")
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    release.update({
        "latestCompletedRelease": "r072y", "siteVersion": "1.38",
        "publicHtmlNoteCount": 175, "postR060RecapNodeCount": 115,
        "nextRelease": "r072z", "latestReleaseGate": "tests/r072y-full-row-forced-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r072y-release.test.mjs",
        "postR070APublishedReleaseCount": 77, "postR070AFormalSealedReleaseCount": 53,
        "legacyFormalFigureBacklogCount": 24,
    })
    release.pop("nextReleaseSourceStage", None)
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.37", "R0.72X", 174):
        raise RuntimeError("site-version is not at R0.72X")
    site.update({"version": "1.38", "latestRelease": "R0.72Y", "publicHtmlNoteCount": 175, "publishedDate": "2026-08-28"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if (inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"), inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount")) != ("r072x", 76, 52, 24):
        raise RuntimeError("formal archive inventory is not at R0.72X")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072x" or "r072y" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72X")
        inventory[key].append("r072y")
    inventory.update({"latestPublishedRelease": "r072y", "publishedReleaseCount": 77, "formalSealedReleaseCount": 53, "legacyFormalFigureBacklogCount": 24})
    if len(inventory["publishedReleases"]) != 77 or len(inventory["formalSealedReleases"]) != 53:
        raise RuntimeError("formal archive count mismatch after R0.72Y")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "VERSION").write_text("1.38\n", encoding="utf-8")


def main() -> None:
    preflight_release_state()
    validate_inputs()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in ("research-review.html", "literature-review.html", "notes/r0-72y.html", "recap-r0-61-r0-72y.html"):
        content = (PUBLIC / relative).read_text(encoding="utf-8")
        assert_clean(content, relative)
        assert_mathjax_clean(content, relative, check_naked=False)
    print(json.dumps({
        "release": "R0.72Y", "siteVersion": "1.38", "notes": 175,
        "recapNodes": 115, "published": 77, "formalSealed": 53,
        "legacyBacklog": 24, "phases": 34, "routeNotes": 85,
        "next": "R0.72Z",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
