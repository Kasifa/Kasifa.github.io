#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed R0.73D static viscous-persistence release."""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import replace
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


ROOT = Path(os.environ.get("R073D_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_ID = "fig-r073d-viscous-cluster-persistence"
FIGURE_RELATIVE = f"figures/r073d/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r073d"
EXPERIMENT_RELATIVE = "experiments/r073d"

R073C_RELEASE_BASELINE = {
    "latestCompletedRelease": "r073c",
    "siteVersion": "1.43",
    "publicHtmlNoteCount": 179,
    "postR060RecapNodeCount": 119,
    "nextRelease": "r073d",
    "latestReleaseGate": "tests/r073c-rayleigh-instability-gate.test.mjs",
    "latestReleasePublicationTest": "tests/r073c-release.test.mjs",
    "postR070APublishedReleaseCount": 81,
    "postR070AFormalSealedReleaseCount": 57,
    "legacyFormalFigureBacklogCount": 24,
}

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73D · STATIC VANISHING VISCOSITY · RIESZ CLUSTER</div>
        <h1>我证明了认证 Rayleigh 谱簇的<br>静态小黏性持续性</h1>
        <p class="lead">对 R0.73C 给出的任意 \(\sigma_*\in(0.17035,0.17050)\)，存在正半平面内的固定圆周和 \(\varepsilon_*>0\)。当 \(0&lt;\varepsilon&lt;\varepsilon_*\) 时，黏性谱簇存在，Riesz 投影在物理 kinetic norm 中按算子范数收敛，总代数重数保持。圆周和阈值只作存在性陈述；单性与收敛速率尚未证明。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73D static cluster theorem 完成</span><strong>Viscous spectral persistence</strong><p>版本 v0.73D · 2026-08-30</p><p>fixed viscous cluster: CLOSED</p><p>Riesz norm convergence: CLOSED</p><p>multiplicity preservation: CLOSED</p><p>complement / fast time: OPEN</p><p>nonlinear / Clay: OPEN</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>静态小黏性谱簇已经闭合；非自治传递与 Clay 仍未闭合</h2><div class="verdict-grid"><div class="verdict-card true"><strong>CLOSED · STATIC PERSISTENCE</strong><p>staticVanishingViscosityPersistence=CLOSED；fixedContourResolventUniform=CLOSED；R0.73C 的正无黏特征值在所有充分小的正黏性下持续为非空谱簇。</p></div><div class="verdict-card true"><strong>CLOSED · RIESZ CLUSTER</strong><p>fixedClusterRieszProjectionNormConvergence=CLOSED；fixedClusterAlgebraicMultiplicityPreserved=CLOSED；fixedClusterEigenvaluesConverge=CLOSED。</p></div><div class="verdict-card false"><strong>OPEN · QUANTITATIVE / COMPLEMENT</strong><p>explicitContourRadius=OPEN；explicitViscosityThreshold=OPEN；inviscidEigenvalueSimple=OPEN；uniformComplementaryDichotomy=OPEN。</p></div><div class="verdict-card false"><strong>OPEN / CONDITIONAL · DYNAMICS</strong><p>graphDomainKatoTransport=OPEN；logFastTimeTransfer=OPEN；superPolynomialCompleteRowNoGo=CONDITIONAL；completeOSSquireA2DirectSum=OPEN；nonlinearNavierStokes=OPEN；Clay=OPEN。</p></div></div></section>
        <section id="operator"><div class="section-no">01 / Operator and space</div><h2>定理只覆盖 \(d=0\)、\(\gamma=1/2\)、\(s=+1\) 的冻结二维 Fourier 行</h2><div class="equation result">\[W_0=-\tfrac12\sin x+\tfrac14\sin2x,\quad L=-\partial_x^2+\tfrac14,\quad A=-\tfrac i2(M_{W_0}+M_{W_0''}L^{-1}).\]</div><div class="equation result">\[\|q\|_X^2=4\langle L^{-1}q,q\rangle_{L^2},\qquad B_\varepsilon=A-\varepsilon L,\qquad D_X(B_\varepsilon)=H^1_{\rm per}.\]</div><p>对每个 \(\varepsilon>0\)，\(-\varepsilon L\) 在 \(X\) 上仍是无界项，所以不能把它当作有界小扰动。</p></section>
        <section id="theorem"><div class="section-no">02 / Fixed-cluster theorem</div><h2>固定圆周上的 resolvent、投影和代数重数同时持续</h2><div class="equation result">\[\Gamma_*=\{z:|z-\sigma_*|=r_*\}\subset\{\operatorname{Re}z>0\},\qquad \sup_{0&lt;\varepsilon&lt;\varepsilon_*}\sup_{z\in\Gamma_*}\|(z-B_\varepsilon)^{-1}\|_{\mathcal B(X)}&lt;\infty.\]</div><div class="equation result">\[P_\varepsilon=\frac1{2\pi i}\int_{\Gamma_*}(z-B_\varepsilon)^{-1}\,dz,\qquad \|P_\varepsilon-P_0\|_{\mathcal B(X)}\to0,\quad \operatorname{rank}P_\varepsilon=m_*.\]</div><p>圆盘按隔离谱点选取，不包含其他无黏谱点。这里 \(m_*\ge1\) 是未知的无黏代数重数。\(r_*\) 与 \(\varepsilon_*\) 均非显式；定理不把谱簇写成唯一或 rank-one 分支。</p></section>
        <section id="isometry"><div class="section-no">03 / Exact isometry</div><h2>酉变换保留奇异定义域跳变</h2><div class="equation result">\[U=2L^{-1/2}:X\to L^2,\qquad UAU^{-1}=M+K,\qquad M=-\tfrac i2M_{W_0}.\]</div><div class="equation result">\[D(M)=L^2\quad(\varepsilon=0),\qquad D(M-\varepsilon L)=H^2_{\rm per}\quad(\varepsilon>0).\]</div><p>定义域没有被人为固定。这个核对是处理 singular perturbation 的第一道门。</p></section>
        <section id="compact"><div class="section-no">04 / Compact correction</div><h2>Fourier commutator 把 Rayleigh 修正写成紧算子</h2><div class="equation result">\[K=-\frac i2\left(L^{-1/2}[M_{W_0},L^{1/2}]+L^{-1/2}M_{W_0''}L^{-1/2}\right).\]</div><p>Fourier 矩阵满足 \(|\omega_m-\omega_n|\le|m-n|\)，且 \(\sum_k|k||W_k|=1\)。commutator 有界，随后乘以紧的 \(L^{-1/2}\)，所以 \(K\) 紧。正半平面点谱因此是有限代数重数的孤立谱。</p></section>
        <section id="base"><div class="section-no">05 / Dissipative base</div><h2>基础 resolvent 强收敛，伴随 resolvent 也强收敛</h2><div class="equation result">\[H_\varepsilon=M-\varepsilon L,\qquad \|(z-H_\varepsilon)^{-1}\|\le(\operatorname{Re}z)^{-1}.\]</div><p>在稠密核 \(H^2\) 上的 resolvent identity 先给点态收敛，再由一致有界性扩张到全空间。对伴随重复同一论证。强收敛加伴随强收敛可以在紧算子两侧升级为算子范数收敛。</p></section>
        <section id="fredholm"><div class="section-no">06 / Fredholm contour</div><h2>紧 Fredholm 因子在固定围道上一致可逆</h2><div class="equation result">\[z-(H_\varepsilon+K)=(z-H_\varepsilon)\bigl(I-(z-H_\varepsilon)^{-1}K\bigr).\]</div><p>后一因子在 \(\Gamma_*\) 上按算子范数趋于无黏因子。无黏围道可逆后，充分小黏性下的全 resolvent 存在并一致有界。</p></section>
        <section id="projection"><div class="section-no">07 / Projection norm</div><h2>减去解析基础 resolvent，只积分范数收敛的紧 sandwich</h2><div class="equation result">\[G_\varepsilon-R_\varepsilon=G_\varepsilon K R_\varepsilon,\qquad \int_{\Gamma_*}R_\varepsilon(z)\,dz=0.\]</div><p>基础算子的谱位于闭左半平面，故其围道积分为零。积分后只剩 \(G_\varepsilon K R_\varepsilon\)；这部分在围道上一致按算子范数收敛，直接得到 \(\|P_\varepsilon-P_0\|\to0\)。</p></section>
        <section id="multiplicity"><div class="section-no">08 / Multiplicity</div><h2>投影距离小于一后，谱簇秩与总代数重数保持</h2><p>当 \(\|P_\varepsilon-P_0\|&lt;1\) 时，两个有限秩投影具有相同秩。对 \(\sigma_*\) 周围的嵌套小圆重复论证，便排除固定簇内特征值停留在远离 \(\sigma_*\) 的位置。因此簇内全部黏性特征值都趋于 \(\sigma_*\)，但本节没有给收敛速率。</p></section>
        <section id="finite"><div class="section-no">09 / Finite diagnostic</div><h2>四组 Fourier cutoff 只做复算和附图，不承担 continuum theorem</h2><table class="compact-table"><thead><tr><th>\(\varepsilon\)</th><th>\(\operatorname{Re}\lambda_{\varepsilon,128}\)</th><th>finite \(\|P_{\varepsilon,128}\|\)</th><th>finite \(\|P_{\varepsilon,128}-P_{0,128}\|\)</th></tr></thead><tbody><tr><td>0</td><td>0.17040797692043275</td><td>1.6835042049174966</td><td>0</td></tr><tr><td>\(10^{-2}\)</td><td>0.1563164070149083</td><td>1.486606332561653</td><td>0.5623486117028229</td></tr><tr><td>\(10^{-4}\)</td><td>0.17026100524770876</td><td>1.6756794461662503</td><td>0.028188658273282464</td></tr><tr><td>\(10^{-6}\)</td><td>0.17040650660020246</td><td>1.6834210770438685</td><td>0.0003090500927697423</td></tr><tr><td>\(10^{-8}\)</td><td>0.17040796221717075</td><td>1.6835033730864915</td><td>0.000003093771501094026</td></tr></tbody></table><p>在 \(N=96,128\) 间，特征值最大差为 \(2.83\times10^{-15}\)；\(N=128\) 最大嵌入残差为 \(6.46\times10^{-15}\)，全 cutoff 最大残差为 \(1.0294\times10^{-6}\)。独立程序逐项重算后误差为零，但两条路径仍使用同一 NumPy/SciPy binary64 体系，不是 interval 或 infinite-tail certificate。独立解析审计另外纠正了 \(X\) 必须按 completion 定义、\(D(H_0)=L^2\) 不能写成 \(H^2\)，并确认 strong resolvent 本身不足以推出投影范数收敛。所有有限数据继续标为 finite diagnostic only。</p></section>
        <section id="literature"><div class="section-no">10 / Literature boundary</div><h2>一般的无黏到黏性不稳定谱持续性已有先例</h2><p><a href="https://doi.org/10.1016/j.anihpc.2007.05.004">Shvydkoy--Friedlander（2008）</a>已证明一般周期情形的谱持续、代数重数和 Riesz 谱子空间结论；<a href="https://www.numdam.org/articles/10.1016/j.anihpc.2007.05.004/">NUMDAM 全文</a>和<a href="https://arxiv.org/abs/math/0509538">arXiv 版本</a>均可核查。<a href="https://doi.org/10.4310/DPDE.2005.v2.n2.a4">Li（2005）</a>给出周期 Kolmogorov-flow 例子；<a href="https://doi.org/10.1137/100794912">Li--Lin（2011）</a>处理 no-slip channel 的 Orr--Sommerfeld 延拓。本节的贡献是一条 explicit double-harmonic Fourier 行在精确 kinetic space 中的自包含证明，并把投影算子范数论证完整写出；不作一般首创、优先权或严格强化声明。</p></section>
        <section id="figure"><div class="section-no">11 / Journal figure</div><h2>算子分解、有限诊断和开放边界分面保存</h2><p><img src="/assets/r073d/fig-r073d-viscous-cluster-persistence.svg" alt="R0.73D static viscous persistence of the certified periodic Rayleigh cluster"></p><p><a href="/assets/r073d/fig-r073d-viscous-cluster-persistence.pdf">下载 PDF</a> · <a href="/assets/r073d/fig-r073d-viscous-cluster-persistence.png">下载 600 dpi PNG</a> · <a href="/assets/r073d/fig-r073d-viscous-cluster-persistence.svg">打开 SVG</a></p></section>
        <section id="value"><div class="section-no">12 / Research value</div><h2>R0.73C 的正无黏点谱现在有了严格的静态黏性承接</h2><p>这一步关闭了先前最直接的 singular-domain 缺口，也把有限矩阵观察提升为独立于截断的算子定理。它对后续快时间路线有必要价值，但还不充分：没有控制围道外的右半平面谱，没有补空间 semigroup dichotomy，也没有处理随时间变化的剖面。对 Clay 问题的直接价值仍有限。</p></section>
        <section id="boundary"><div class="section-no">13 / Exact boundary</div><h2>固定谱簇不是完整稳定性理论</h2><p>inviscidRootUnique=OPEN；inviscidEigenvalueSimple=OPEN；explicitContourRadius=OPEN；explicitViscosityThreshold=OPEN；quantitativeEigenvalueRate=OPEN；globalRightHalfPlaneNoPollution=OPEN；uniformComplementaryDichotomy=OPEN；movingProfileUniformContour=OPEN；graphDomainKatoTransport=OPEN；logFastTimeTransfer=OPEN；superPolynomialCompleteRowNoGo=CONDITIONAL；completeOSSquireA2DirectSum=OPEN；nonlinearNavierStokes=OPEN；Clay=OPEN。</p></section>
        <section id="next"><div class="section-no">14 / Next gate</div><h2>R0.73E：补空间 resolvent、semigroup dichotomy 与固定投影 Volterra 传递</h2><p>下一步先检查固定右半平面带中的全谱排除和 complement resolvent，再决定是否能用固定投影的 Volterra 论证处理缓慢 profile drift。只有这些门闭合后，才可能进入 \(M\log(1/\varepsilon)\) 的非自治增长窗口。</p></section>
        <section id="reproduce"><div class="section-no">15 / Reproduction</div><h2>完整证明、独立审计、有限诊断、证书和正式附图均已归档</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073d_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073d_viscous_persistence_proof.md">解析证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073d_independent_analytic_audit.md">独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073d_literature_audit.md">文献边界审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073d">正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073d">有限实验与监控记录</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073d/fig-r073d-viscous-cluster-persistence">正式附图包</a> · <a href="/notes/r0-73d.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73d.html">累计回顾</a> · <a href="/recap-r0-61-r0-73d.pdf">累计回顾 PDF</a></p></section>
      </article>'''

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73E</span><span class="tree-state current">下一检查点</span></div>
              <h3>complement resolvent、semigroup dichotomy 与 fixed-projection transfer</h3><p>先控制固定右半平面带中围道外的谱和补空间 semigroup，再检查缓慢 profile drift 的 Volterra 传递。</p>
            </article>'''

HOME_D_CARD = r'''          <div class="task-one" id="r073d" data-release="r073d" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73D · 2026-08-30</p><h3>认证 Rayleigh 谱簇的静态小黏性持续性</h3>
            <p>R0.73C 的 \(\sigma_*\in(0.17035,0.17050)\) 现在对所有充分小正黏性持续为非空谱簇。固定围道 resolvent 一致有界，Riesz 投影在物理 kinetic norm 中按算子范数收敛，总代数重数保持。</p><p>四组 cutoff 的特征值与投影曲线只作 finite diagnostic；continuum theorem 来自 compact-Fredholm 证明和独立解析审计。</p>
            <p><strong>结论边界：</strong>&nbsp;staticVanishingViscosityPersistence、fixedContourResolventUniform、fixedClusterRieszProjectionNormConvergence、fixedClusterAlgebraicMultiplicityPreserved 与 fixedClusterEigenvaluesConverge 为 CLOSED；inviscidRootUnique、inviscidEigenvalueSimple、explicitContourRadius、explicitViscosityThreshold、quantitativeEigenvalueRate、globalRightHalfPlaneNoPollution、uniformComplementaryDichotomy、movingProfileUniformContour、graphDomainKatoTransport、logFastTimeTransfer、completeOSSquireA2DirectSum、nonlinearNavierStokes 与 Clay 为 OPEN；superPolynomialCompleteRowNoGo 为 CONDITIONAL。</p>
            <p><a href="/notes/r0-73d.html"><strong>阅读 R0.73D 研究笔记 →</strong></a><br><a href="/notes/r0-73d.pdf">下载同步研究笔记 PDF</a> · <a href="/assets/r073d/fig-r073d-viscous-cluster-persistence.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073d">查看正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073d_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73d.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73E：</strong>&nbsp;complement resolvent、semigroup dichotomy 与 fixed-projection transfer。</p>
          </div>'''

HOME_LATEST_SPOTLIGHT = r'''    <section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">
      <div class="route-overview-inner">
        <header class="route-map-header">
          <div><p class="eyebrow">LATEST RELEASE · R0.73D · 2026-08-30</p><h2 class="route-map-title" id="latest-release-title">认证 Rayleigh 谱簇的静态小黏性持续性</h2><p class="route-map-intro">固定谱簇、围道 resolvent、Riesz 投影算子范数收敛和总代数重数保持已闭合。单性、显式速率、补空间 dichotomy、非自治快时间传递、nonlinear 与 Clay 仍为 OPEN。</p></div>
          <nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-73d.pdf">阅读最新 R0.73D 研究笔记 →</a><a href="/recap-r0-61-r0-73d.html">120 节累计回顾</a><a href="/notes/">180 篇研究笔记总索引</a><a href="#r073d">查看首页完整 R0.73D 卡片</a></nav>
        </header>
        <div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73D · 82 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>58 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73D</span></div>
      </div>
    </section>'''
