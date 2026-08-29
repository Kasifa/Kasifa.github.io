#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed R0.73A hidden-mean transient release.

R0.73A proves a viscous-rate all-start estimate in the singular hybrid
``X_mu`` norm for the physical ``beta=xi=0, mu=gamma^2>0`` row.  It does not
prove an A2 rate, a physical kinetic propagator, Squire/Bloch closure, a
nonlinear estimate, or the Clay problem.
"""

from __future__ import annotations

import csv
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


ROOT = Path(os.environ.get("R073A_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_ID = "fig-r073a-hidden-mean-transient-spectral"
FIGURE_RELATIVE = f"figures/r073a/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r073a"
EXPERIMENT_RELATIVE = "experiments/r073a"

R072Z_RELEASE_BASELINE = {
    "latestCompletedRelease": "r072z",
    "siteVersion": "1.39",
    "publicHtmlNoteCount": 176,
    "postR060RecapNodeCount": 116,
    "nextRelease": "r073a",
    "latestReleaseGate": "tests/r072z-os-squire-gate.test.mjs",
    "latestReleasePublicationTest": "tests/r072z-release.test.mjs",
    "postR070APublishedReleaseCount": 78,
    "postR070AFormalSealedReleaseCount": 54,
    "legacyFormalFigureBacklogCount": 24,
}

SOURCE_STAGE_CONTRACT = {
    "release": "r073a",
    "stage": "source-freeze",
    "publicationStatus": "pending-formal-certificate-figure-and-publication",
    "publicCountersAdvanced": False,
    "report": "research/r073a_report-source.md",
    "problemFreeze": "research/r073a_problem_freeze.md",
    "literatureAudit": "research/r073a_literature_audit.md",
    "gapMatrix": "research/r073a_gap_matrix.md",
    "analyticProof": "research/r073a_transient_proof.md",
    "projectionDerivation": "research/r073a_projection_derivation_agent.md",
    "projectionIndependentAudit": "research/r073a_projection_independent_audit.md",
    "independentAnalyticAudit": "research/r073a_independent_analytic_audit.md",
    "spectralAudit": "research/r073a_spectral_audit_agent.md",
    "producer": "research/certificates/r073a/generate_certificate.py",
    "independentProducer": "research/certificates/r073a/independent_recompute.py",
    "comparator": "research/certificates/r073a/validate_certificate.py",
    "certificateDirectory": CERTIFICATE_RELATIVE,
    "experimentDirectory": EXPERIMENT_RELATIVE,
    "figureDirectory": FIGURE_RELATIVE,
    "generator": "scripts/generate_r073a_release.py",
    "translationScript": "scripts/add-r073a-translations.mjs",
    "translationSnapshot": "scripts/i18n-snapshots/r073a-missing.json",
    "releaseGate": "tests/r073a-hidden-mean-gate.test.mjs",
    "publicationTest": "tests/r073a-release.test.mjs",
    "certificateSourceTest": "tests/r073a-deterministic-certificate-source.test.mjs",
    "figureSourceTest": "tests/r073a-hidden-mean-transient-spectral-figure-source.test.mjs",
}

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73A · PHYSICAL LONG WAVE · HIDDEN MEAN</div>
        <h1>我把长波零模改写成壁法向平均速度，<br>得到有限瞬态的黏性速率界</h1>
        <p class="lead">我在 \(\beta=\xi=0\)、\(\mu=\gamma^2\in(0,1]\) 的物理行上使用 \(h=\mu^{-1}\Pi_0q\)、\(r=Q_0q\)。精确均值抵消把齐次生成元中的 \(\mu^{-1}\) 消去，并在 \(X_\mu\) 范数中给出 all-start finite-transient bound。它只有 viscous rate；physical kinetic、Squire、Bloch、nonlinear 与 Clay 仍为 OPEN。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73A scoped physical row 完成</span><strong>hidden mean and finite transient</strong><p>版本 v0.73A · 2026-08-29</p><p>physical mean cancellation: CLOSED</p><p>X_mu viscous-rate bound: CLOSED</p><p>lifted tangent line: NOT INVARIANT</p><p>fixed-Lambda raw-q limit: OPEN</p><p>kinetic / Squire / Bloch: OPEN</p><p>nonlinear / Clay: OPEN</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>正间隙物理行在 \(X_\mu\) 中闭合；更强范数与更快速率没有被外推</h2><div class="verdict-grid"><div class="verdict-card true"><strong>CLOSED · PHYSICAL COORDINATE</strong><p>exactPhysicalMeanOSCancellation=CLOSED；exactMeanVelocityZeroMeanVorticitySystem=CLOSED；renormalizedPhysicalLongWaveOSTransientPropagator=CLOSED；renormalizedPhysicalLongWaveOSForcedDuhamel=CLOSED。</p></div><div class="verdict-card true"><strong>CLOSED · EXACT PROJECTION ALGEBRA</strong><p>exactPhysicalTangentLiftedLineNoninvariance=CLOSED；exactMovingTangentQuotientAlgebra=CLOSED；orthogonalTangentProjectionSpeed=CLOSED；explicitOrthogonalTangentBlocks=CLOSED。</p></div><div class="verdict-card false"><strong>FALSE · PRECISE ONE-DIMENSIONAL CLAIMS</strong><p>rankOneAbstractTangentClosesPhysicalLongWaveLimit=FALSE 只按 lifted one-dimensional invariant-state meaning 表示 lifted line \(h=0\)、\(r\in\operatorname{span}\{W_{xx}\}\) 不是充分的不变物理状态；fixedTwoHarmonicOSInvariance=FALSE 只在 \(c\ne0\) 的完整 \(\mathscr A_0\) 演化中使用；twoSidedInvariantOrthogonalTangentSplit=FALSE。positive-gap dual 的负结论只针对 normalized dual 与 raw \(Q^*\mathscr B^*\psi\) 的 unweighted bound；实际 OS off-block 另乘 \(|c|\)。</p></div><div class="verdict-card false"><strong>OPEN · STRONGER PHYSICAL THEOREMS</strong><p>lowGapOSTransientA2Propagator=OPEN；lowGapPhysicalKineticPropagator=OPEN；generalBlochLowGapOSPropagator=OPEN；lowGapOSSquirePropagator=OPEN；BlochUniformPhysicalVelocityDirectSum=OPEN；nonlinearNavierStokes=OPEN；Clay=OPEN。</p></div></div></section>
        <section id="coordinate"><div class="section-no">01 / Physical coordinate</div><h2>raw mean 不是低间隙的正则坐标</h2><div class="equation result">\[h=\mu^{-1}\Pi_0q=\Pi_0(\mathcal L_\mu^{-1}q),\qquad r=Q_0q,\qquad q=\mu h+r.\]</div><p>我把 mean wall-normal velocity 与 mean-zero OS vorticity 分开，并定义 \(\|(h,r)\|_{X_\mu}^2=|h|^2+\|r\|_2^2\)。</p></section>
        <section id="cancellation"><div class="section-no">02 / Exact cancellation</div><h2>两次周期分部积分精确消去零模奇性</h2><div class="equation result">\[\Pi_0\!\left(Wr+W_{xx}\mathcal L_\mu^{-1}r\right)=\mu\Pi_0\!\left(W\mathcal L_\mu^{-1}r\right).\]</div><p>这是对每个 mean-zero \(r\) 的恒等式，不是有限 Fourier 近似，也不是 \(\mu\) 的渐近展开。</p></section>
        <section id="system"><div class="section-no">03 / Regular system</div><h2>齐次 \((h,r)\) 生成元不再含负次 \(\mu\)</h2><div class="equation result">\[\begin{aligned}h_d&=-\mu h-ic\Pi_0(W\mathcal L_\mu^{-1}r),\\r_d&=-\mathcal L_\mu r-icQ_0(Wr+W_{xx}\mathcal L_\mu^{-1}r)-ic\,h(W_{xx}+\mu W).\end{aligned}\]</div><p>这项 regularity 属于 singular coordinate \(X_\mu\)，不表示 raw \(L^2_q\) 或 kinetic norm 已经统一。</p></section>
        <section id="transient"><div class="section-no">04 / All-start transient</div><h2>显式积分 majorant 给出有限 transient prefactor</h2><div class="equation result">\[J(s,d)=\frac74(e^{-s}-e^{-d})+\frac12(e^{-4s}-e^{-4d})\le\frac94e^{-s}.\]</div><div class="equation result">\[\boxed{\|U_\mu(d,s)\|_{X_\mu\to X_\mu}\le e^{-\mu(d-s)+|c|J(s,d)}}.\]</div><p>当 \(|c|\le4\) 时，我得到 \(e^9e^{-\mu(d-s)}\)。\(e^9\) 是透明但未优化的上界；速率是 \(\mu\)，不是 enhanced-dissipation 或 scalar \(A_2\) rate。</p></section>
        <section id="forcing"><div class="section-no">05 / Forced Duhamel</div><h2>受迫结论保留 mean forcing 的 \(\mu^{-1}\) payment</h2><div class="equation result">\[\mathfrak F_\mu=(\mu^{-1}\Pi_0F_q,Q_0F_q)\in L^1_{\rm loc}(X_\mu).\]</div><p>variation of constants 使用同一 transient kernel；删除 \(\mu^{-1}\Pi_0F_q\) 会改变物理变量或范数。</p></section>
        <section id="path"><div class="section-no">06 / Parameter-path boundary</div><h2>正间隙 noninvariance 与 \(\mu\to0\) 路径必须分开</h2><div class="equation result">\[h_d(s)=ic_\mu\left[\frac{e^{-2s}}{8(1+\mu)}+\frac{e^{-8s}}{8(4+\mu)}\right],\qquad c_\mu=\gamma\Lambda_\mu.\]</div><p>对每个 \(\mu>0\)、\(c_\mu\ne0\)，lifted tangent line 都不 invariant。只有沿 \(c_\mu\to c_0\ne0\) 的路径，上式才有非零极限；这要求 \(|\Lambda_\mu|\asymp|\gamma|^{-1}\)。固定 \(\Lambda\) 时 \(c_\mu\to0\)，raw-\(q\) singular limit 仍为 OPEN。</p></section>
        <section id="quotient"><div class="section-no">07 / Moving quotient</div><h2>不变一维物理状态失败，不等于 moving quotient 代数失败</h2><div class="equation result">\[Q\mathscr AP=P_dP,\qquad z_d=(Q\mathscr AQ-P_dQ)z.\]</div><p>tangent amplitude 不强迫 complement；complement 仍可强迫 amplitude。两侧都 invariant 当且仅当 \(\psi_d=-\mathscr A^*\psi\)，其 gapless OS 版本是 forward anti-parabolic。</p><p>以上恒等式只在完整报告列明的 common dense domain \(D\)、strong \(C^1\) solution 与 adjoint-domain compatibility 下逐点成立；它们不单独断言 standalone quotient 的 well-posedness。</p></section>
        <section id="orthogonal"><div class="section-no">08 / Orthogonal blocks</div><h2>投影转速有界，但 pressure block 不消失</h2><div class="equation result">\[\|(P_\perp)_d\|\le\frac32,\qquad \psi_{\perp,d}+\mathscr A_0^*\psi_\perp=\frac{2\zeta+icG}{N}.\]</div><p>因此 bounded kinematic rotation 不推出 small projected generator；\(|c|G\) 是显式非零的 complement-to-tangent coupling。</p></section>
        <section id="two-mode"><div class="section-no">09 / Two-mode carrier</div><h2>\(\operatorname{span}\{\sin x,\sin2x\}\) 运动学自然；当 \(c\ne0\) 时不是完整 OS 不变子空间</h2><div class="equation result">\[\mathscr B_0q=-\frac3{16}(a x_2+2b x_1)(\cos x-\cos3x).\]</div><p>无条件的代数事实是 \(\mathscr B_0\) 的泄漏公式及其 kernel 恰为 tangent line；乘上 \(-ic\) 后，\(c\ne0\) 才得到完整 \(\mathscr A_0\) 的 noninvariance、return coupling 与更高 harmonic。有限维删除不是该非零耦合演化的不变 quotient。</p></section>
        <section id="dual"><div class="section-no">10 / Positive-gap dual cost</div><h2>固定 \(d\)，归一化 dual 强制 raw pressure vector 的常数模 \(g^{-1}\)</h2><div class="equation result">\[\frac1g\le\|\mathscr B_{\beta,\mu}^*\psi_{\beta,\mu}\|_2+\|W\|_\infty\|\psi_{\beta,\mu}\|_2,\qquad g=\beta^2+\mu.\]</div><div class="equation result">\[\|Q^*\mathscr B_{\beta,\mu}^*\psi\|_2\ge\frac1g-\|W\|_\infty M-C_d(|\beta|+g)M^2\quad(\|\psi\|_2\le M).\]</div><p>uniform dichotomy 只在固定 \(d\)，或满足 \(\inf_d\|\phi(d)\|_2>0\) 的 compact \(d\)-interval 上表述。实际 OS off-block 还乘 \(|c|\)，因此其发散结论只沿 \(|c|/g\to\infty\) 的路径成立。这不声称无共同空间识别时 \(g=0\) 与 \(g>0\) 的算子范数不连续，也不排除像 \(X_\mu\) 那样明确支付权重的 theorem。</p></section>
        <section id="spectral"><div class="section-no">11 / Finite diagnostic</div><h2>冻结谱 screen 只负责筛错，不承担无限维证明</h2><p>有限 Fourier--Galerkin 审计记录 448 个 broad cases 与 150 个 target rows。删除 \(W_{xx}\) 或两谐波空间并不统一改善 finite spectral edge；stable compression 也可有正 numerical abscissa 与 sampled gain。没有 Galerkin tail bound、continuous-time maximum 或 nonautonomous concatenation theorem。</p></section>
        <section id="norms"><div class="section-no">12 / Three norms</div><h2>raw、hybrid 与 kinetic 三种账本不能互换</h2><div class="equation result">\[\|q\|_2^2=\mu^2|h|^2+\|r\|_2^2,\qquad \|(h,r)\|_{X_\mu}^2=|h|^2+\|r\|_2^2.\]</div><div class="equation result">\[Q_{\rm kin}^2=|h|^2+\mu^{-1}\|\mathcal L_\mu^{-1/2}r\|_2^2.\]</div><p>raw 到 \(X_\mu\) 在一个方向损失 \(\mu^{-1}\)；kinetic multiplier 也不与 \(X_\mu\) 统一等价。</p></section>
        <section id="literature"><div class="section-no">13 / Literature boundary</div><h2>已有 long-wave、投影与 transient 工具；组合接口仍未由引用文献覆盖</h2><p>Colombo--Dolce--Montalto--Ventura 提供 stationary physical long-wave mode；Chen--Dai--Wang--Wang 处理 parameter-uniform Riesz projection；Li--Zhao、Li--Wei--Zhang 与 Beekie--Chen--Jia 给出不同几何中的 nonautonomous、pseudospectral 或 periodic OS 工具。我只报告有界 primary-source search，不把未覆盖的组合写成新颖性证明。</p></section>
        <section id="evidence"><div class="section-no">14 / Evidence boundary</div><h2>无限维证明、有限证书与附图各自承担不同任务</h2><p>解析报告证明 cancellation、energy estimate、Duhamel 与 projection identities。双路证书核对有限 Fourier algebra 和 deterministic \(X_\mu\) grid；冻结谱实验仍是 finite diagnostic。附图只展示已绑定的公式、envelope 和 finite screen，不构成证明。</p></section>
        <section id="figure"><div class="section-no">15 / Journal figure</div><h2>隐藏均值、analytic envelope 与 finite spectral screen 分面展示</h2><p><img src="/assets/r073a/fig-r073a-hidden-mean-transient-spectral.svg" alt="R0.73A hidden mean, X_mu transient envelope, and finite frozen spectral audit"></p><p><a href="/assets/r073a/fig-r073a-hidden-mean-transient-spectral.pdf">下载 PDF</a> · <a href="/assets/r073a/fig-r073a-hidden-mean-transient-spectral.png">下载 PNG</a> · <a href="/assets/r073a/fig-r073a-hidden-mean-transient-spectral.svg">打开 SVG</a></p></section>
        <section id="value"><div class="section-no">16 / Research value</div><h2>这是一条真实但严格受限的 linear low-gap coordinate theorem</h2><p>我把 raw constant-mode singularity 改写成 physical hidden coordinate，并证明 time-dependent heat path 在 \(X_\mu\) 中只有有限 transient payment。它距离 Millennium 问题仍远：kinetic direct sum、Squire、Bloch summation、nonlinear convolution、vortex stretching 与 continuation 均未闭合。</p></section>
        <section id="next"><div class="section-no">17 / Next gate</div><h2>R0.73B：把 physical mean、tangent carrier 与 adjoint pressure cost 放进同一 weighted modulation</h2><p>下一步先寻求明确支付 \(g\)、\(|c|\)、\(|\Lambda|\) 与 orientation 的 physical kinetic estimate，再讨论任何 \(A_2\)-scale improvement。</p></section>
        <section id="reproduce"><div class="section-no">18 / Reproduction</div><h2>完整报告、审计、证书、实验和附图</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073a_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073a_literature_audit.md">文献边界审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073a_gap_matrix.md">主张—证据矩阵</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073a_independent_analytic_audit.md">独立解析审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073a">确定性证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073a">有限诊断与 propagator grid</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073a/fig-r073a-hidden-mean-transient-spectral">正式附图包</a> · <a href="/notes/r0-73a.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73a.html">累计回顾</a> · <a href="/recap-r0-61-r0-73a.pdf">累计回顾 PDF</a></p></section>
      </article>'''

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73B</span><span class="tree-state current">下一检查点</span></div>
              <h3>weighted physical modulation and kinetic control</h3><p>同时跟踪 physical mean、tangent carrier、near-constant mode 与 adjoint pressure cost，并显式支付 \(g\)、\(|c|\)、\(|\Lambda|\) 和 orientation。</p>
            </article>'''

HOME_A_CARD = r'''          <div class="task-one" id="r073a" data-release="r073a" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73A · 2026-08-29</p><h3>hidden physical mean 与 \(X_\mu\) finite-transient bound</h3>
            <p>我用 \(h=\Pi_0q/\mu\)、\(r=Q_0q\) 重写 physical \(\beta=\xi=0\) long-wave row；exact mean cancellation 给出 \(X_\mu\) 中的 all-start viscous-rate estimate。</p><p>对每个正 gap、\(c_\mu\ne0\)，lifted tangent line 不 invariant；只有 \(c_\mu\to c_0\ne0\) 才给 nonzero hidden-mean limit，fixed \(\Lambda\) raw-\(q\) limit 保持 OPEN。</p>
            <p><strong>结论边界：</strong>&nbsp;physical kinetic、Squire、general Bloch、direct sum、nonlinearNavierStokes 与 Clay 保持 OPEN。</p>
            <p><a href="/notes/r0-73a.html"><strong>阅读 R0.73A 研究笔记 →</strong></a><br><a href="/notes/r0-73a.pdf">下载同步研究笔记 PDF</a> · <a href="/assets/r073a/fig-r073a-hidden-mean-transient-spectral.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073a">查看确定性证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073a_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73a.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73B：</strong>&nbsp;weighted physical modulation and kinetic control。</p>
          </div>'''


def _validate_source_stage_manifest(release: dict) -> None:
    for key, value in R072Z_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.72Z: {key}")
    if release.get("nextReleaseSourceStage") != SOURCE_STAGE_CONTRACT:
        raise RuntimeError("R0.73A source-stage manifest contract is missing, stale, or has extra fields")


def preflight_release_state() -> None:
    release = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    expected_site = {"schemaVersion": "research-site-version-v1", "version": "1.39", "latestRelease": "R0.72Z", "publicHtmlNoteCount": 176, "publishedDate": "2026-08-28"}
    if json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8")) != expected_site:
        raise RuntimeError("public site-version is not exactly at R0.72Z")
    if len(list((PUBLIC / "notes").glob("*.html"))) != 176:
        raise RuntimeError("R0.72Z preflight expected 176 public HTML notes")
    for relative in ("notes/r0-73a.html", "notes/r0-73a.pdf", "recap-r0-61-r0-73a.html", "recap-r0-61-r0-73a.pdf"):
        if (PUBLIC / relative).exists():
            raise RuntimeError(f"R0.72Z preflight found premature public output: {relative}")
    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in ('data-site-version="1.39"', "<strong>176</strong>公开研究笔记", "<strong>R0.72Z</strong>最新研究节点", 'aria-label="R0.69P–R0.72Z"'):
        if token not in home:
            raise RuntimeError(f"R0.72Z home baseline missing token: {token}")
    if 'data-release="r073a"' in home:
        raise RuntimeError("R0.72Z home already contains an R0.73A card")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.72Z">(.*?)</nav>', home, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 86:
        raise RuntimeError("R0.72Z home route expected 86 notes")
    recap = (PUBLIC / "recap-r0-61-r0-72z.html").read_text(encoding="utf-8")
    start, end = recap.index('<section id="node-index">'), recap.index("</section>", recap.index('<section id="node-index">'))
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 116 or len(set(links)) != 116 or recap.count('<article class="phase">') != 35:
        raise RuntimeError("R0.72Z recap baseline expected 116 unique nodes and 35 phases")
    inventory = json.loads((ROOT / "research/formal-archive-inventory.json").read_text(encoding="utf-8"))
    if (inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"), inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount")) != ("r072z", 78, 54, 24):
        raise RuntimeError("formal archive inventory is not at R0.72Z")


def _binding_paths(manifest: dict) -> set[str]:
    bindings = manifest.get("sourceBindings")
    if not isinstance(bindings, list):
        raise RuntimeError("formal certificate sourceBindings are missing")
    paths = {row.get("path") for row in bindings if isinstance(row, dict)}
    if None in paths or len(paths) != len(bindings):
        raise RuntimeError("formal certificate sourceBindings are malformed or duplicated")
    return paths


def _verify_experiment_manifest() -> None:
    directory = ROOT / EXPERIMENT_RELATIVE
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if manifest.get("status") != "completed" or manifest.get("finiteDimensionalOnly") is not True:
        raise RuntimeError("R0.73A finite experiment scope or status mismatch")
    source = directory / str(manifest.get("source", ""))
    if not source.is_file() or digest(source) != manifest.get("sourceSha256"):
        raise RuntimeError("R0.73A finite experiment source hash mismatch")
    for row in manifest.get("outputs", []):
        path = directory / str(row.get("path", ""))
        if not path.is_file() or path.stat().st_size != row.get("bytes") or digest(path) != row.get("sha256"):
            raise RuntimeError(f"R0.73A finite experiment output hash mismatch: {row.get('path')}")
    validation = json.loads((directory / "validation.json").read_text(encoding="utf-8"))
    if validation.get("status") != "passed" or not all(validation.get("checks", {}).values()):
        raise RuntimeError("R0.73A finite experiment validation failed")


def validate_inputs() -> None:
    required_inputs = (
        "research/r073a_report-source.md", "research/r073a_problem_freeze.md", "research/r073a_literature_audit.md", "research/r073a_gap_matrix.md",
        "research/r073a_transient_proof.md", "research/r073a_projection_derivation_agent.md", "research/r073a_projection_independent_audit.md", "research/r073a_independent_analytic_audit.md", "research/r073a_spectral_audit_agent.md",
        f"{CERTIFICATE_RELATIVE}/README.md", f"{CERTIFICATE_RELATIVE}/crosscheck.json", f"{CERTIFICATE_RELATIVE}/manifest.json",
        f"{EXPERIMENT_RELATIVE}/manifest.json", f"{EXPERIMENT_RELATIVE}/summary.json", f"{EXPERIMENT_RELATIVE}/validation.json", f"{EXPERIMENT_RELATIVE}/xmu_propagator_certificate.csv",
        f"{FIGURE_RELATIVE}/manifest.json", "scripts/i18n-snapshots/r073a-missing.json",
        "public/notes/r0-72z.html", "public/recap-r0-61-r0-72z.html",
    )
    for relative in required_inputs:
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.73A release input: {relative}")
    report = (ROOT / "research/r073a_report-source.md").read_text(encoding="utf-8")
    for token in (
        "exactPhysicalMeanOSCancellation", "renormalizedPhysicalLongWaveOSTransientPropagator", "exactPhysicalTangentLiftedLineNoninvariance",
        "exactMovingTangentQuotientAlgebra", "rankOneAbstractTangentClosesPhysicalLongWaveLimit", "c_\\mu\\to c_0", "fixed",
        "X_\\mu", "viscous rate", "lowGapPhysicalKineticPropagator", "lowGapOSSquirePropagator", "BlochUniformPhysicalVelocityDirectSum", "nonlinearNavierStokes", "Clay",
    ):
        if token not in report:
            raise RuntimeError(f"R0.73A report missing stable token: {token}")
    audit = (ROOT / "research/r073a_independent_analytic_audit.md").read_text(encoding="utf-8")
    for token in ("ANALYTIC PASS", "PARAMETER-PATH", "fixed-\\(\\Lambda\\)", "moving quotient", "viscous-rate"):
        if token not in audit:
            raise RuntimeError(f"R0.73A independent audit missing token: {token}")
    projection_audit = (ROOT / "research/r073a_projection_independent_audit.md").read_text(encoding="utf-8")
    for token in (
        "ANALYTIC PASS WITH SCOPE EDITS APPLIED", "FALSE for c != 0",
        "Q^*\\mathscr B^*\\psi", "|c|/g\\to\\infty", "compact \\(d\\)-interval",
        "common-space identification",
    ):
        if token not in projection_audit:
            raise RuntimeError(f"R0.73A projection audit missing scoped token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.73A certificate")
    verify_flat_hash_ledger(figure, "R0.73A figure")
    certificate_manifest = json.loads((certificate / "manifest.json").read_text(encoding="utf-8"))
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    source_commit = str(certificate_manifest.get("sourceCommit", ""))
    if certificate_manifest.get("status") != "formal" or not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("R0.73A certificate is not formal or source-frozen")
    if crosscheck.get("status") != "passed" or crosscheck.get("formalSourceReady") is not True or crosscheck.get("temporaryUnsealedSourceAllowed") is not False:
        raise RuntimeError("R0.73A certificate crosscheck is not formal")
    if crosscheck.get("sourceCommit") != source_commit or crosscheck.get("sourceBindings") != certificate_manifest.get("sourceBindings") or not all(crosscheck.get("checks", {}).values()):
        raise RuntimeError("R0.73A certificate lineage or exhaustive checks failed")
    expected_bound_sources = {
        "research/r073a_report-source.md", "research/r073a_problem_freeze.md", "research/r073a_literature_audit.md", "research/r073a_gap_matrix.md",
        "research/r073a_transient_proof.md", "research/r073a_projection_derivation_agent.md", "research/r073a_projection_independent_audit.md", "research/r073a_independent_analytic_audit.md", "research/r073a_spectral_audit_agent.md",
        "research/release-manifest.json", "research/certificates/r073a/generate_certificate.py", "research/certificates/r073a/independent_recompute.py", "research/certificates/r073a/validate_certificate.py",
        "experiments/r073a/frozen_os_spectral_audit.py", "experiments/r073a/validate_frozen_os_spectral_audit.py", "experiments/r073a/manifest.json", "experiments/r073a/validation.json",
        "scripts/generate_r073a_release.py", "scripts/add-r073a-translations.mjs", "scripts/i18n-snapshots/r073a-missing.json",
        "tests/r073a-hidden-mean-gate.test.mjs", "tests/r073a-release.test.mjs", "tests/r073a-deterministic-certificate-source.test.mjs", "tests/r073a-hidden-mean-transient-spectral-figure-source.test.mjs",
        f"{FIGURE_RELATIVE}/contract.json", f"{FIGURE_RELATIVE}/config.json", f"{FIGURE_RELATIVE}/caption.md", f"{FIGURE_RELATIVE}/README.md",
    }
    missing_bindings = expected_bound_sources - _binding_paths(certificate_manifest)
    if missing_bindings:
        raise RuntimeError(f"R0.73A formal source binding is incomplete: {sorted(missing_bindings)}")
    external_csv = ROOT / EXPERIMENT_RELATIVE / "xmu_propagator_certificate.csv"
    expected_external = [{
        "path": f"{EXPERIMENT_RELATIVE}/xmu_propagator_certificate.csv",
        "bytes": external_csv.stat().st_size,
        "sha256": digest(external_csv),
    }]
    if certificate_manifest.get("externalOutputs") != expected_external:
        raise RuntimeError("R0.73A external propagator CSV binding is missing or stale")
    if crosscheck.get("independentCsv") != expected_external[0]:
        raise RuntimeError("R0.73A crosscheck external CSV binding is missing or stale")
    subprocess.run([sys.executable, str(certificate / "validate_certificate.py"), "--require-formal"], cwd=ROOT, check=True)
    _verify_experiment_manifest()

    figure_manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    figure_contract = json.loads((figure / "contract.json").read_text(encoding="utf-8"))
    if figure_manifest.get("release") != "R0.73A" or figure_manifest.get("figureId") != FIGURE_ID or figure_manifest.get("status") != "formal":
        raise RuntimeError("R0.73A figure identity or formal status mismatch")
    if figure_contract.get("chartContract", {}).get("certificateBoundCrosscheckTolerance") != 2e-8:
        raise RuntimeError("R0.73A figure certificate-bound tolerance is not the fixed 2e-8")
    if figure_manifest.get("qa", {}).get("status") != "passed" or figure_manifest.get("qa", {}).get("visualInspectionExplicit") is not True:
        raise RuntimeError("R0.73A figure visual QA is not formal")
    dependency = figure_manifest.get("dependency", {})
    if dependency.get("available") is not True or dependency.get("formalBlocked") is not False or dependency.get("syntheticSubstitutionAllowed") is not False:
        raise RuntimeError("R0.73A figure certificate overlay is absent or synthetic")
    git = figure_manifest.get("git", {})
    certificate_commit = str(git.get("certificateCommit", ""))
    if git.get("sourceCommit") != source_commit or not re.fullmatch(r"[0-9a-f]{40}", certificate_commit) or certificate_commit == source_commit:
        raise RuntimeError("R0.73A figure does not preserve two-commit lineage")
    if subprocess.run(["git", "merge-base", "--is-ancestor", source_commit, certificate_commit], cwd=ROOT).returncode:
        raise RuntimeError("R0.73A certificate commit is not a descendant of the source commit")
    with (ROOT / EXPERIMENT_RELATIVE / "xmu_propagator_certificate.csv").open(encoding="utf-8", newline="") as stream:
        reader = csv.DictReader(stream)
        expected_header = ["certificateId", "s", "d", "mu", "c", "gain", "bound", "sourceCommit", "certificateCommit"]
        if reader.fieldnames != expected_header:
            raise RuntimeError("R0.73A X_mu certificate CSV schema mismatch")
        rows = list(reader)
    if not rows:
        raise RuntimeError("R0.73A X_mu certificate CSV is empty")
    for row in rows:
        if row["sourceCommit"] != source_commit or row["certificateCommit"] not in {"pending", "bound-by-figure-manifest", certificate_commit} or not (0 < float(row["gain"]) <= float(row["bound"]) + 2e-8):
            raise RuntimeError("R0.73A X_mu certificate row or lineage mismatch")
    claims = figure_manifest.get("claimBoundary", {})
    for key in ("lowGapPhysicalKineticPropagatorProved", "BlochUniformPhysicalVelocityDirectSumProved", "nonlinearNavierStokesClosureProved", "clayMillenniumProblemSolved", "figureIsAnalyticProof"):
        if claims.get(key) is not False:
            raise RuntimeError(f"R0.73A figure escaped OPEN boundary: {key}")
    subprocess.run([sys.executable, str(figure / "validate.py"), "--require-formal"], cwd=ROOT, check=True)
    if figure_manifest.get("publication", {}).get("directory") != "public/assets/r073a":
        raise RuntimeError("R0.73A figure publication directory mismatch")
    for suffix in ("pdf", "svg", "png"):
        master = figure / f"figure.{suffix}"
        public = PUBLIC / "assets/r073a" / f"{FIGURE_ID}.{suffix}"
        if not public.is_file() or digest(public) != digest(master):
            raise RuntimeError(f"R0.73A public {suffix} is absent or not byte-identical")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-72z.html").read_text(encoding="utf-8")
    replacements = (
        (r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.73A：physical hidden mean、X_mu finite-transient viscous-rate bound 与精确 projection boundary。">'),
        (r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.73A｜Hidden physical mean and finite-transient X_mu bound">'),
        (r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="physical beta=xi=0 row 在 X_mu 中闭合；kinetic、Squire、Bloch、nonlinear 与 Clay 保持 OPEN。">'),
        (r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r073a/fig-r073a-hidden-mean-transient-spectral.png">'),
        (r'<title>.*?</title>', '<title>R0.73A｜Hidden physical mean and finite-transient X_mu bound</title>'),
    )
    for index, (pattern, value) in enumerate(replacements):
        html = section(html, pattern, value, f"A note metadata {index}")
    html = required(html, "/i18n-en.js?v=1.39", "/i18n-en.js?v=1.40", "A note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#coordinate">坐标</a><a href="#cancellation">抵消</a><a href="#system">系统</a><a href="#transient">transient</a><a href="#forcing">forcing</a><a href="#path">路径</a><a href="#quotient">quotient</a><a href="#orthogonal">投影</a><a href="#two-mode">two-mode</a><a href="#dual">dual</a><a href="#spectral">finite screen</a><a href="#norms">范数</a><a href="#literature">文献</a><a href="#evidence">证据</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "A note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "A note hero")
    toc_items = [("result", "00 · direct decision"), ("coordinate", "01 · physical coordinate"), ("cancellation", "02 · exact cancellation"), ("system", "03 · regular system"), ("transient", "04 · all-start transient"), ("forcing", "05 · forced Duhamel"), ("path", "06 · parameter path"), ("quotient", "07 · moving quotient"), ("orthogonal", "08 · orthogonal blocks"), ("two-mode", "09 · two-mode carrier"), ("dual", "10 · dual cost"), ("spectral", "11 · finite diagnostic"), ("norms", "12 · three norms"), ("literature", "13 · literature"), ("evidence", "14 · evidence"), ("figure", "15 · journal figure"), ("value", "16 · value"), ("next", "17 · R0.73B"), ("reproduce", "18 · reproduction")]
    toc = '      <aside class="toc"><strong>CONTENTS</strong><ol>\n' + "".join(f'        <li><a href="#{anchor}">{label}</a></li>' for anchor, label in toc_items) + '\n      </ol></aside>'
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "A note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "A note article")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.73A · 2026-08-29<br><a href="/">返回研究主页</a></div></footer>', "A note footer")
    for stale in ("fig-r072z-os-squire-threshold", "压力反馈的高间隙阈值", "必须支付的 Squire 方向代价"):
        if stale in html:
            raise RuntimeError(f"R0.73A note contains stale R0.72Z figure copy: {stale}")
    assert_clean(html, "R0.73A note")
    assert_mathjax_clean(html, "R0.73A note")
    (PUBLIC / "notes/r0-73a.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-72z.html").read_text(encoding="utf-8")
    html = required(html, "/i18n-en.js?v=1.39", "/i18n-en.js?v=1.40", "A recap i18n")
    html = required(html, 'data-current-route="R0.69P–R0.72Z"', 'data-current-route="R0.69P–R0.73A"', "A recap route")
    for label, pattern, value in (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.73A 的 117 个节点；最新一节闭合 physical hidden-mean coordinate 与 X_mu finite-transient bound。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.73A｜R0.60 之后的研究回顾">'),
        ("og desc", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="三十六个阶段、117 个节点：从约化递推到 physical hidden mean 与 viscous-rate X_mu transient theorem。">'),
        ("title", r'<title>.*?</title>', '<title>R0.61–R0.73A｜R0.60 之后的研究回顾</title>'),
    ):
        html = section(html, pattern, value, "A recap " + label)
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.73A · 2026-08-29</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页完整保留 R0.61 到 R0.73A 的 117 个研究节点。R0.69P 以后从局部证书推进到 scalar A2 collision、完整 Fourier row 与 high-gap OS；R0.73A 再把 physical long-wave zero mode 改写成 hidden mean coordinate，并在 \(X_\mu\) 中闭合 finite-transient viscous-rate estimate。physical kinetic、Squire、Bloch、nonlinear 与 Clay 没有被外推。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73A</strong><p>收录节点：117</p><p>回顾截止时公开笔记：177</p><p>回顾截止节点：R0.73A</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "A recap hero")
    for old, new in (("02 · 116 节完整索引", "02 · 117 节完整索引"), ("01 · 三十五个研究阶段", "01 · 三十六个研究阶段"), ("R0.60 之后的路线分成三十五个阶段", "R0.60 之后的路线分成三十六个阶段")):
        html = required(html, old, new, "A recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>117</strong><span>R0.61–R0.73A 研究节点</span></div><div class="metric"><strong>79</strong><span>R0.70A–R0.73A 已公开版本</span></div><div class="metric"><strong>55</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.70A–R0.73A 的 79 个版本已公开，其中 55 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "A recap result")
    phase = r'''            <article class="phase"><h3>R0.73A · hidden physical mean and finite-transient X_mu theorem</h3><p>exact physical mean cancellation、regular \((h,r)\) system、all-start viscous-rate transient bound 与 forced Duhamel 为 CLOSED。</p><p>对每个 \(c_\mu\ne0\) 的正间隙行，lifted tangent line 不 invariant；nonzero limit 只沿 \(c_\mu\to c_0\ne0\)，fixed \(\Lambda\) raw-\(q\) limit 仍 OPEN。moving quotient 代数本身保持 exact。</p><p>physical kinetic、Squire、general Bloch、direct sum、nonlinearNavierStokes 与 Clay 保持 OPEN。</p><div class="links"><a href="/notes/r0-73a.html">R0.73A</a><a href="/assets/r073a/fig-r073a-hidden-mean-transient-spectral.pdf">R0.73A 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073a">R0.73A 证书</a></div></article>
'''
    html = once(html, "          </div>\n        </section>\n\n        <section id=\"node-index\">", phase + "          </div>\n        </section>\n\n        <section id=\"node-index\">", "A recap phase")
    html = required(html, "R0.61–R0.72Z 的 116 节公开笔记", "R0.61–R0.73A 的 117 节公开笔记", "A recap node title")
    node_z = '            <span class="node-ref"><a href="/notes/r0-72z.html">R0.72Z</a><span class="node-state kind-closed">闭</span></span>\n'
    node_a = '            <span class="node-ref"><a href="/notes/r0-73a.html">R0.73A</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_z, node_z + node_a, "A recap node")
    retained = r'''            <li>R0.73A 闭合 physical hidden-mean coordinate 与 \(X_\mu\) finite-transient viscous-rate theorem，同时把 fixed-\(\Lambda\) limit、kinetic/Squire/Bloch 与 nonlinear/Clay 保留为 OPEN。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "A recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>physical long-wave coordinate 已正则化，但还不是 kinetic 或 nonlinear theorem</h2><p>不能把 117 个节点或 79 个公开版本解释成 Clay 问题完成比例。R0.73A 的严格增量是 exact zero-mode cancellation、\(X_\mu\) finite-transient bound、path-qualified lifted-line noninvariance 与 projection algebra boundary；直接 Clay 价值仍有限。</p></section>''', "A recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73B 研究 weighted physical modulation 与 kinetic control</h2><p>把 physical mean、tangent carrier、near-constant mode 与 adjoint pressure cost 放进同一带权演化框架。</p></section>''', "A recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.73A 的 79 节已公开；55 节完整封存；24 节旧档待回补。</p><p>rankOneAbstractTangentClosesPhysicalLongWaveLimit 仅按 lifted one-dimensional invariant-state meaning 为 FALSE；lowGapPhysicalKineticPropagator、lowGapOSSquirePropagator、BlochUniformPhysicalVelocityDirectSum、nonlinearNavierStokes 与 Clay 为 OPEN。</p></section>''', "A recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、证书、实验、正式附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-72z.html">保留 R0.72Z 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73a.html">打开最新节点 R0.73A</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073a">查看 R0.73A 确定性证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073a">查看有限诊断</a> · <a href="/assets/r073a/fig-r073a-hidden-mean-transient-spectral.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73a.pdf">下载同步 PDF</a></p><p>完整节点索引保留 R0.61 起的全部历史编号；状态标签只描述证据类型。</p></section>''', "A recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.73A 回顾 · 2026-08-29<br><a href="/">返回研究主页</a></div></footer>', "A recap footer")
    start, end = html.index('<section id="node-index">'), html.index("</section>", html.index('<section id="node-index">'))
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 117 or len(set(links)) != 117 or html.count('<article class="phase">') != 36:
        raise RuntimeError("R0.73A recap expected 117 unique nodes and 36 phases")
    assert_clean(html, "R0.73A recap")
    assert_mathjax_clean(html, "R0.73A recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-73a.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.39"', 'data-site-version="1.40"'), ("/i18n-en.js?v=1.39", "/i18n-en.js?v=1.40"), ("/site-refresh.js?v=1.39", "/site-refresh.js?v=1.40"),
        ("<strong>v1.39</strong>网页版本", "<strong>v1.40</strong>网页版本"), ("<strong>176</strong>公开研究笔记", "<strong>177</strong>公开研究笔记"), ("<strong>R0.72Z</strong>最新研究节点", "<strong>R0.73A</strong>最新研究节点"),
        ("Research topology · R0.1–R0.72Z", "Research topology · R0.1–R0.73A"), ("R0.70A–R0.72Z：78 节已公开，54 节完整封存", "R0.70A–R0.73A：79 节已公开，55 节完整封存"),
        ('<span class="route-range">R0.69P–R0.72Z</span>', '<span class="route-range">R0.69P–R0.73A</span>'), ('aria-label="R0.69P–R0.72Z"', 'aria-label="R0.69P–R0.73A"'),
        ("展开 86 篇公开笔记", "展开 87 篇公开笔记"), ("本站 R0.69P–R0.72Z 路线", "本站 R0.69P–R0.73A 路线"),
        ("综述 v1.39 · 2026-08-28", "综述 v1.40 · 2026-08-29"), ("上次综述 v1.38 · 2026-08-28", "上次综述 v1.39 · 2026-08-28"),
        ("/recap-r0-61-r0-72z.html", "/recap-r0-61-r0-73a.html"), ("/recap-r0-61-r0-72z.pdf", "/recap-r0-61-r0-73a.pdf"),
        ("<strong style=\"color:var(--gold)\">下一步 R0.73A：</strong>&nbsp;projected low-gap OS propagator with an explicit transient prefactor。", "<strong style=\"color:var(--gold)\">当时的下一步 R0.73A：</strong>&nbsp;projected low-gap OS propagator with an explicit transient prefactor。"),
    ):
        html = required(html, old, new, "A home " + old)
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73A 已在 physical \(\beta=\xi=0\) row 上闭合 hidden-mean coordinate 与 \(X_\mu\) finite-transient viscous-rate bound。下一关是 weighted physical modulation 与 kinetic control。</span></div>', "A home focus")
    link_z = '<a class="milestone" href="/notes/r0-72z.html">R0.72Z</a>'
    html = once(html, link_z, link_z + '\n                  <a class="milestone" href="/notes/r0-73a.html">R0.73A</a>', "A home route link")
    route_a = r'''              <p>R0.73A 用 \(h=\Pi_0q/\mu\) 记录 hidden physical mean，在 \(X_\mu\) 中闭合 all-start finite-transient viscous-rate bound。lifted tangent line 对每个 \(c_\mu\ne0\) 的正 gap 不 invariant；nonzero limit 只沿 \(c_\mu\to c_0\ne0\)，fixed \(\Lambda\) raw-\(q\) limit 与 kinetic/Squire/Bloch/nonlinear/Clay 保持 OPEN。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_a + '              <details class="tree-notes" open>', "A home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "A home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73A · 2026-08-29</p><h3>R0.60 recap 之后的累计回顾收录 117 个节点；全站现有 177 篇公开研究笔记</h3><p>累计回顾现分三十六个问题阶段，并给出 R0.61–R0.73A 的完整索引；R0.73A 分开记录 physical coordinate theorem、path-qualified tangent boundary 与 finite spectral diagnostic。</p><p>R0.70A–R0.73A 共 79 个版本已公开；55 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;\(X_\mu\) viscous-rate transient 已闭合；physical kinetic、Squire、Bloch 与 nonlinear/Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73a.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73a.pdf">下载同步 PDF</a></p></div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "A home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_A_CARD + '\n        </section>\n\n      </article>', "A home card")
    if html.count('data-release="r073a"') != 1:
        raise RuntimeError("home must contain exactly one R0.73A card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73B：') != 1 or '<strong style="color:var(--gold)">下一步 R0.73A：' in html:
        raise RuntimeError("home must distinguish the unique current R0.73B next gate from historical R0.73A")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73A">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 87:
        raise RuntimeError("home current-route index must contain 87 note links")
    assert_clean(html, "R0.73A home")
    assert_mathjax_clean(html, "R0.73A home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.39", "/i18n-en.js?v=1.40"), ("本站 R0.69P–R0.72Z 只列为研究笔记", "本站 R0.69P–R0.73A 只列为研究笔记"),
        ("/recap-r0-61-r0-72z.html", "/recap-r0-61-r0-73a.html"), ("文献综述 v1.39 · 2026-08-28", "文献综述 v1.40 · 2026-08-29"),
        ("累计回顾与 116 节索引", "累计回顾与 117 节索引"), ("打开 116 节完整索引", "打开 117 节完整索引"),
    ):
        html = required(html, old, new, "A literature " + old)
    old_open = r'<div class="route-step pause"><header><b>开放接口 · R0.73A</b><strong>projected low-gap OS propagator</strong></header><p>分离 tangent/lift-up 慢子空间，寻求带 explicit transient prefactor 的 low-gap limiting absorption 或 evolution estimate。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.73A</b><strong>hidden physical mean and finite-transient X_mu theorem</strong></header><p>exact zero-mode cancellation、regular \((h,r)\) system 与 all-start viscous-rate bound 已闭合。nonzero hidden-mean limit 只沿 \(c_\mu\to c_0\ne0\)；fixed \(\Lambda\)、kinetic/Squire/Bloch 与 nonlinear/Clay 仍 OPEN。<a href="/notes/r0-73a.html">研究笔记</a> <a href="/recap-r0-61-r0-73a.html">当前累计回顾</a> <a href="#r073a-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73B</b><strong>weighted physical modulation and kinetic control</strong></header><p>把 physical mean、tangent carrier、near-constant mode 与 adjoint pressure cost 统一到显式带权演化估计。</p></div>'''
    html = once(html, old_open, new_steps, "A literature route")
    boundary = r'''

          <h3 id="r073a-boundary">R0.73A 的 long-wave、projection 与 transient 文献边界</h3>
          <p>Colombo--Dolce--Montalto--Ventura 固定 stationary physical long-wave mode；Chen--Dai--Wang--Wang 给 parameter-uniform Riesz projection；Li--Zhao、Li--Wei--Zhang、Reddy--Schmid--Henningson、Beekie--Chen--Jia 与 Wei--Zhang--Zhao 分别固定 nonautonomous、pseudospectral、transient 或 periodic OS 工具。已核验来源没有同时给出本项目的 heat collision、physical hidden mean、path-qualified transient、Squire transfer 与 Bloch-uniform kinetic direct sum。我只报告 bounded primary-source search；它不是 novelty 或 priority proof。</p>
          <div class="boundary"><strong>R0.73A 的主张边界</strong><p>exactPhysicalMeanOSCancellation、renormalizedPhysicalLongWaveOSTransientPropagator、exactPhysicalTangentLiftedLineNoninvariance 与 exactMovingTangentQuotientAlgebra 为 CLOSED。rankOneAbstractTangentClosesPhysicalLongWaveLimit 只按 lifted one-dimensional invariant-state meaning 为 FALSE。fixed \(\Lambda\) raw-\(q\) limit、lowGapPhysicalKineticPropagator、lowGapOSSquirePropagator、BlochUniformPhysicalVelocityDirectSum、nonlinearNavierStokes 与 Clay 为 OPEN。</p></div>'''
    match = re.search(r'(<h3 id="r072z-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("A literature expected R0.72Z boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "A literature boundary")
    assert_clean(html, "R0.73A literature")
    assert_mathjax_clean(html, "R0.73A literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    if len(list((PUBLIC / "notes").glob("*.html"))) != 177:
        raise RuntimeError("expected 177 public HTML notes after R0.73A")
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    release.update({
        "latestCompletedRelease": "r073a", "siteVersion": "1.40", "publicHtmlNoteCount": 177, "postR060RecapNodeCount": 117,
        "nextRelease": "r073b", "latestReleaseGate": "tests/r073a-hidden-mean-gate.test.mjs", "latestReleasePublicationTest": "tests/r073a-release.test.mjs",
        "postR070APublishedReleaseCount": 79, "postR070AFormalSealedReleaseCount": 55, "legacyFormalFigureBacklogCount": 24,
    })
    release.pop("nextReleaseSourceStage", None)
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.39", "R0.72Z", 176):
        raise RuntimeError("site-version is not at R0.72Z")
    site.update({"version": "1.40", "latestRelease": "R0.73A", "publicHtmlNoteCount": 177, "publishedDate": "2026-08-29"})
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    if (inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"), inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount")) != ("r072z", 78, 54, 24):
        raise RuntimeError("formal archive inventory is not at R0.72Z")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r072z" or "r073a" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.72Z")
        inventory[key].append("r073a")
    inventory.update({"latestPublishedRelease": "r073a", "publishedReleaseCount": 79, "formalSealedReleaseCount": 55, "legacyFormalFigureBacklogCount": 24})
    if len(inventory["publishedReleases"]) != 79 or len(inventory["formalSealedReleases"]) != 55:
        raise RuntimeError("formal archive count mismatch after R0.73A")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "VERSION").write_text("1.40\n", encoding="utf-8")


def main() -> None:
    preflight_release_state()
    validate_inputs()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    for relative in ("research-review.html", "literature-review.html", "notes/r0-73a.html", "recap-r0-61-r0-73a.html"):
        content = (PUBLIC / relative).read_text(encoding="utf-8")
        assert_clean(content, relative)
        assert_mathjax_clean(content, relative, check_naked=False)
    print(json.dumps({
        "release": "R0.73A", "siteVersion": "1.40", "notes": 177, "recapNodes": 117,
        "published": 79, "formalSealed": 55, "legacyBacklog": 24, "phases": 36, "routeNotes": 87, "next": "R0.73B",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
