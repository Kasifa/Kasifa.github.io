#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB FrequencyActivation CB.25 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.69"
SLUG = "clay-b-frequency-activation-20260907"
DISPLAY_ID = "ClayB-FrequencyActivation-20260907"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]

ZH_SECTIONS = [
    ("01 / 结果地图", "能量级首次激活的尖锐时钟", """<div class="grid"><div class="card"><strong class="proved">UNIVERSAL LOWER BOUND</strong>固定能量下，空频带达到指定正振幅至少需要常数倍 N⁻⁵ᐟ² 时间。</div><div class="card"><strong class="proved">MATCHING FULL-NS FAMILY</strong>一族完整、无外力、周期光滑 NS 解在同阶时间激活严格空的目标带。</div><div class="card"><strong class="open">NO RESIDENCE OR CASCADE CLAIM</strong>这是首次到达，不是到达后驻留，也不是同一初值的无限级联。</div></div><p>因此，仅凭固定总能量、黏性、滤波器与阈值，普遍 N⁻² 抛物等待时间为假；这不否定依赖高阶初值、成熟历史或额外动态结构的估计。</p>"""),
    ("02 / FA.1–FA.4", "固定对象、阈值与严格量词", """<p>在固定三维周期环面上研究完整无外力 NS，固定 ν&gt;0、E₀&gt;0，并以径向光滑乘子 Q_N 观察 2.05N&lt;|k|&lt;2.2N。若带振幅从 b₀ 上升到 b₁，则</p><div class="equation">t−s ≥ (b₁−b₀)/(Cχ E₀ N⁵ᐟ²).   (FA.3)</div><p>另存在固定但仅为<strong>存在性</strong>的 η∈(0,E₀) 与随 N 改变的光滑初值族，使目标带初始严格为空，而首次达到带能量 η 的时刻 T_N 满足</p><div class="equation">cN⁻⁵ᐟ² ≤ T_N ≤ CN⁻⁵ᐟ².   (FA.4)</div><p>η 不依赖 N，但不是数值认证的能量比例；T_N 只在已证明光滑的局部时间窗内取首次到达。</p>"""),
    ("03 / FA.5–FA.6", "能量给出的普遍上升约束", """<p>目标带上的 Q_NPdiv 卷积核 L² 范数是 O(N⁵ᐟ²)：一个导数贡献 N，O(N³) 个格点在 Parseval 后贡献 N³ᐟ²。能量律于是给出</p><div class="equation">F_N(t) ≤ Cχ N⁵ᐟ²||u(t)||₂² ≤ 2CχE₀N⁵ᐟ².   (FA.5)</div><p>把它代入精确 mild 方程并丢掉热衰减，得到 FA.3。压力没有删去，完整源项允许任意 high–high 回落、所有频率相互作用及同一输出频率内的相位抵消；也没有假设频带振幅单调。</p>"""),
    ("04 / FA.7–FA.11", "严格空带与非退化输出种子", """<p>两个位于 p=(3/2,0,0)、q=(0,3/2,0) 附近的实偶无散 Fourier 波包，以横向极化 A=(0,1,0)、B=(0,0,1) 产生输出 ζ₀=p+q。该输出位于目标带，且</p><div class="equation">Γ̂_F(ζ₀)=(i/(2π)³)[(3/2)B+O(δ)]∫ψ_δ² ≠0.   (FA.9)</div><p>充分小的固定 δ 保证输入支撑在 1&lt;|ξ|&lt;2、目标带严格为空而二次输出非零。Schwartz 周期化、精确能量归一化及周期影像乘积误差控制把这一非退化性带到扩大环面：||G_N||₂→γ&gt;0。</p>"""),
    ("05 / FA.12–FA.15", "完整非线性轨道上的统一局部控制", """<p>扩大环面的非归一化 Sobolev 范数保留正确体积因子，因此 H⁵→W³,∞ 的常数与环面边长一致。直接 Leibniz 能量估计给出统一光滑窗和</p><div class="equation">sup ||U_N||H⁵≤M,   ||U_N(τ)−W_N||H³≤C_Mτ.   (FA.12–FA.13)</div><p>对完整 NS mild 方程，而不是只保留第一 Picard 项，有一致余项</p><div class="equation">||Q_NU_N(τ)+τG_N||₂ ≤ C₀τ².   (FA.14)</div><p>固定足够小的 τ₀ 后，真实非线性解的目标带振幅有与 N 无关的正下界。Galerkin 构造与高阶延拓保证整个使用窗口内光滑。</p>"""),
    ("06 / FA.16–FA.17", "回到固定环面：同阶上界与小耗散", """<p>精确缩放 u⁽ᴺ⁾(t,x)=N³ᐟ²U_N(N⁵ᐟ²t,Nx) 把扩大环面解变成固定环面、黏性恰为 ν 的完整无外力解，并保持初始总能量 E₀。</p><div class="equation">ν∫₀^{CN⁻⁵ᐟ²}||∇u⁽ᴺ⁾||₂²dt ≤ C′νN⁻¹ᐟ² →0.   (FA.17)</div><p>目标带在初时严格为零，在 τ₀N⁻⁵ᐟ² 时已有固定正振幅；连续性给出首次达到 η 的时刻。于是 νN²T_N→0，否定指定的普遍 N⁻² 等待下界，并说明能量级幂次不能普遍改善到任何 α&lt;5/2。</p>"""),
    ("07 / 文献与历史边界", "继承 AJ 的缩放工具，不主张机制新颖性", """<p><strong>LITERATURE</strong>本轮只做有界本地去重，并核对 Cheskidov–Peng arXiv:2407.06474v2 与 Luo arXiv:1803.05569v4 的官方元数据和摘要；没有导入新的外部 PDE 定理，也没有进行完整论文证明审计、PDF 核验、Deep Research 或穷尽性新颖性搜索。</p><p>AJ 已给出固定能量、扩大环面与 N⁻⁵ᐟ² 短时方法；本章的增量是严格空的原速度目标带、正能量首次激活及匹配的普遍下界组合。局部检索未命中不构成领域新颖性证明或优先权声明。</p>"""),
    ("08 / 证据与停止边界", "关闭能量级抛物激活时钟路线", """<p>科学源提交 1674af0dc98825d0d0299fa69e3ae12398c3d8a0；冻结提交 c688fca88da5a434aac5ca46971a7d800f146b39。三份本轮源、一个数学依赖、四份 provenance 记录和一份冻结 manifest 逐字节绑定；17 个 FA 标签、16 项独立 Ruby 有理复算与 4 项有限负对照通过。唯一完整非作者审查者 C 全文重推 FA.1–17 及必需 AJ 局部理论并接受。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_frequency_activation_20260907.md">FA 正文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_frequency_activation_audit_20260907.md">审核记录</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_frequency_activation_checks_20260907.json">有限检查</a></p><p>下一研究候选必须使用真正额外的实际 NS 动态结构，并明确减少哪一项未付输入；本冻结包没有接受下一条无条件候选。</p><p><strong>FINITE CHECKS ONLY：有限复算不认证 PDE、极限、统一存在性或新颖性。这里没有到达后驻留、低频起始、同一初值的无限级联、奇点或全局正则性结论；G、R.216–R.217 与一般终端缺口仍 OPEN。无新读者 PDF、仿真、科学图、DGX 或 recap。NOT CLAY。</strong></p>"""),
]

EN_SECTIONS = [
    ("01 / Result map", "A sharp clock for energy-only first activation", """<div class="grid"><div class="card"><strong class="proved">UNIVERSAL LOWER BOUND</strong>At fixed energy, an empty band needs at least a constant multiple of N⁻⁵ᐟ² time to reach a prescribed positive amplitude.</div><div class="card"><strong class="proved">MATCHING FULL-NS FAMILY</strong>A family of full, unforced, periodic smooth NS solutions activates the strictly empty target band on the same scale.</div><div class="card"><strong class="open">NO RESIDENCE OR CASCADE CLAIM</strong>This is first arrival, not residence after arrival and not an infinite cascade from one fixed datum.</div></div><p>Therefore a universal N⁻² parabolic waiting time from fixed total energy, viscosity, filter, and threshold alone is false. Estimates depending on higher initial norms, mature history, or additional dynamics are not excluded.</p>"""),
    ("02 / FA.1–FA.4", "Fixed objects, threshold, and exact quantifiers", """<p>On the fixed three-dimensional torus, consider full unforced NS with fixed ν&gt;0 and E₀&gt;0, and use a smooth radial multiplier Q_N to observe 2.05N&lt;|k|&lt;2.2N. If the band amplitude rises from b₀ to b₁, then</p><div class="equation">t−s ≥ (b₁−b₀)/(Cχ E₀ N⁵ᐟ²).   (FA.3)</div><p>There also exists a fixed but purely <strong>existential</strong> η∈(0,E₀) and a smooth family whose data vary with N, with a strictly empty target band initially, such that the first time T_N at which its band energy reaches η satisfies</p><div class="equation">cN⁻⁵ᐟ² ≤ T_N ≤ CN⁻⁵ᐟ².   (FA.4)</div><p>The threshold is independent of N but is not a numerically certified energy fraction. The first hit is taken only inside the proved smooth local window.</p>"""),
    ("03 / FA.5–FA.6", "The universal growth constraint from energy", """<p>The L² norm of the Q_NPdiv convolution kernel is O(N⁵ᐟ²): one derivative gives N and O(N³) lattice points give N³ᐟ² after Parseval. The energy law therefore yields</p><div class="equation">F_N(t) ≤ Cχ N⁵ᐟ²||u(t)||₂² ≤ 2CχE₀N⁵ᐟ².   (FA.5)</div><p>Substitution into the exact mild equation, followed by discarding heat decay, gives FA.3. Pressure is not removed. The full source allows arbitrary high–high return, every frequency interaction, and phase cancellation at the same output frequency; no monotonicity of band amplitude is assumed.</p>"""),
    ("04 / FA.7–FA.11", "A strictly empty-band seed with nondegenerate output", """<p>Real even divergence-free Fourier packets near p=(3/2,0,0) and q=(0,3/2,0), with transverse polarizations A=(0,1,0) and B=(0,0,1), produce output ζ₀=p+q in the target band:</p><div class="equation">Γ̂_F(ζ₀)=(i/(2π)³)[(3/2)B+O(δ)]∫ψ_δ² ≠0.   (FA.9)</div><p>A sufficiently small fixed δ keeps the input in 1&lt;|ξ|&lt;2, makes the target band exactly empty, and preserves a nonzero quadratic output. Schwartz periodization, exact energy normalization, and control of periodic-image products carry this nondegeneracy to the expanding torus: ||G_N||₂→γ&gt;0.</p>"""),
    ("05 / FA.12–FA.15", "Uniform control on the full nonlinear trajectory", """<p>The unnormalized expanding-torus Sobolev norm keeps the correct volume factor, so H⁵→W³,∞ constants are uniform in the torus size. A direct Leibniz energy estimate gives a common smooth window and</p><div class="equation">sup ||U_N||H⁵≤M,   ||U_N(τ)−W_N||H³≤C_Mτ.   (FA.12–FA.13)</div><p>For the full NS mild equation, not merely its first Picard term, the uniform remainder is</p><div class="equation">||Q_NU_N(τ)+τG_N||₂ ≤ C₀τ².   (FA.14)</div><p>After fixing a sufficiently small τ₀, the actual nonlinear solution has an N-independent positive target-band amplitude. Galerkin construction and higher-order continuation keep the whole used window smooth.</p>"""),
    ("06 / FA.16–FA.17", "Return to the fixed torus: matching upper bound and small dissipation", """<p>The exact scaling u⁽ᴺ⁾(t,x)=N³ᐟ²U_N(N⁵ᐟ²t,Nx) produces a full unforced solution on the fixed torus with viscosity exactly ν and initial total energy E₀.</p><div class="equation">ν∫₀^{CN⁻⁵ᐟ²}||∇u⁽ᴺ⁾||₂²dt ≤ C′νN⁻¹ᐟ² →0.   (FA.17)</div><p>The target band is strictly zero initially and has a fixed positive amplitude at τ₀N⁻⁵ᐟ². Continuity gives the first hitting time of η. Hence νN²T_N→0, disproving the specified universal N⁻² waiting bound and showing that the energy-only exponent cannot be uniformly improved to any α&lt;5/2.</p>"""),
    ("07 / Literature and historical boundary", "AJ's scaling tools are inherited; no mechanism novelty is claimed", """<p><strong>LITERATURE</strong>This round performed bounded local deduplication and checked only the official metadata and abstracts for Cheskidov–Peng arXiv:2407.06474v2 and Luo arXiv:1803.05569v4. No new external PDE theorem, complete-paper proof audit, PDF review, Deep Research, or exhaustive novelty search was imported.</p><p>AJ already supplied the fixed-energy expanding-torus N⁻⁵ᐟ² short-time method. The increment here is the combination of a strictly empty velocity output band, positive-energy first activation, and the matching universal lower bound. A bounded local search miss does not certify field novelty or priority.</p>"""),
    ("08 / Evidence and stopping boundary", "Close the energy-only parabolic activation-clock route", """<p>Scientific source commit: 1674af0dc98825d0d0299fa69e3ae12398c3d8a0; freeze commit: c688fca88da5a434aac5ca46971a7d800f146b39. Three current sources, one mathematical dependency, four provenance records, and one frozen manifest are byte-bound. Seventeen FA labels, 16 independent Ruby rational recomputations, and four limited negative controls pass. The sole complete nonauthor reviewer C rederived FA.1–17 and the necessary AJ local theory and accepted them.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_frequency_activation_20260907.md">FA source</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_frequency_activation_audit_20260907.md">audit record</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_frequency_activation_checks_20260907.json">finite checks</a></p><p>Any next candidate must use genuinely additional actual-NS dynamics and identify the named unpaid input it reduces. This freeze accepts no next unconditional candidate.</p><p><strong>FINITE CHECKS ONLY: finite recomputation does not certify PDE, limits, uniform existence, or novelty. There is no result on post-arrival residence, low-frequency origin, an infinite cascade from one fixed datum, singularity, or global regularity. G, R.216–R.217, and the general terminal gap remain OPEN. There is no new reader PDF, simulation, scientific figure, DGX, or recap. NOT CLAY.</strong></p>"""),
]


def main_block(lang: str, sections: list[tuple[str, str, str]]) -> str:
    if lang == "zh":
        kicker = "CB.25 · 独立 Clay-B 研究笔记 · 2026-09-07"
        title = "CB.25｜固定能量下的频带激活：尖锐的 N⁻⁵ᐟ² 时间尺度"
        dek = "完整无外力周期 NS 的能量预算给出 N⁻⁵ᐟ² 首次激活下界；严格空带的光滑解族达到同阶上界，从而排除仅靠总能量的普遍 N⁻² 等待时间。"
        footer = "独立 HTML 研究笔记"
    else:
        kicker = "CB.25 · Independent Clay-B research note · 2026-09-07"
        title = "CB.25 | Band activation at fixed energy: the sharp N⁻⁵ᐟ² timescale"
        dek = "The energy budget of full unforced periodic NS gives an N⁻⁵ᐟ² lower bound for first activation, and a smooth family with a strictly empty band attains the same scale, excluding a universal energy-only N⁻² waiting time."
        footer = "Independent HTML research note"
    body = "".join(f'<section><div class="section-no">{n}</div><h2>{h}</h2>{c}</section>' for n, h, c in sections)
    return f'''  <main data-language="{lang}">
    <article><header class="hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="dek">{dek}</p><div class="meta"><span>PROVED</span><span>SHARP SCALE</span><span>FULL NS</span><span>EXISTENTIAL THRESHOLD</span><span>NO RESIDENCE CLAIM</span><span>LITERATURE</span><span>FINITE CHECKS ONLY</span><span>OPEN · NOT CLAY</span></div></header>{body}</article>
    <footer class="footer">CB.25 · {footer} · {DISPLAY_ID} · 2026-09-07</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-frequency-activation" aria-labelledby="clay-b-frequency-activation-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.25 · INDEPENDENT CLAY-B RESEARCH NOTE · 2026-09-07 · FREQUENCY ACTIVATION</p><h2 class="route-map-title" id="clay-b-frequency-activation-title">CB.25｜固定能量下的频带激活：尖锐的 N⁻⁵ᐟ² 时间尺度</h2><p class="route-map-intro">能量预算给出空频带达到固定正阈值的普遍 N⁻⁵ᐟ² 下界，一族完整无外力周期光滑 NS 解达到同阶上界。因此仅靠总能量的普遍 N⁻² 抛物等待时间被排除；首次激活不等于到达后驻留，也不是同一初值的无限级联。OPEN · NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 频带激活笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-frequency-activation-20260907.html">阅读最新 CB.25 笔记 →</a><a href="/literature-review.html#clay-b-frequency-activation-boundary">查看来源与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 频带激活结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>N⁻⁵ᐟ² 普遍下界</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>完整 NS 家族达到同阶</span><span><i class="route-legend-mark current" aria-hidden="true"></i>无驻留或固定数据级联结论 · NOT CLAY</span></div></div></section>'''


CB_ROWS = '''          <div class="tree-row clay-b-same-parent-residual-row">
            <article class="tree-node"><div class="tree-node-head"><span class="route-range">CB.22 · 2026-09-06 · BU SAME-PARENT RESIDUAL</span><span class="tree-state">独立路线章节</span></div><h3>CB.22｜同一原解的对齐残差：能量、混合压力与终端边界</h3><p>正原子条件下，终端残差测度在目标点无原子，正向方程保留 −2νΔb 源；混合张量全时间消失且完整周期混合压力有普通时间 little-o。</p><p class="tree-path"><a href="/notes/clay-b-same-parent-residual-20260906.html">阅读 CB.22 HTML</a> · <a href="/literature-review.html#clay-b-same-parent-residual-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
          </div>

          <div class="tree-row clay-b-signed-mixed-pressure-row">
            <article class="tree-node"><div class="tree-node-head"><span class="route-range">CB.23 · 2026-09-07 · BV SIGNED MIXED PRESSURE</span><span class="tree-state">独立路线章节</span></div><h3>CB.23｜有符号混合压力功：投影测试和联合截断</h3><p>投影给出逐时幅度一致上界；联合截断只控制有符号累计压力。W_z 与混合压力平方是两条不同且未付的充分接口。</p><p class="tree-path"><a href="/notes/clay-b-signed-mixed-pressure-20260907.html">阅读 CB.23 HTML</a> · <a href="/literature-review.html#clay-b-signed-mixed-pressure-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
          </div>

          <div class="tree-row clay-b-source-enstrophy-row">
            <article class="tree-node"><div class="tree-node-head"><span class="route-range">CB.24 · 2026-09-07 · BW SOURCE / ENSTROPHY</span><span class="tree-state">独立路线章节</span></div><h3>CB.24｜残差的梯度能量：源项、应变与二次组合的边界</h3><p>全周期梯度测试保留二阶源项、应变与端点；固定正定二次组合存在有限类障碍，正原子分支迫使特定二阶成本发散，但不能反推 W_z 发散。</p><p class="tree-path"><a href="/notes/clay-b-source-enstrophy-20260907.html">阅读 CB.24 HTML</a> · <a href="/literature-review.html#clay-b-source-enstrophy-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right kept"><span class="tree-state">FREQUENCY ACTIVATION COMPLETED</span><h3>能量级激活时钟已进入 CB.25</h3><p>FA 给出空频带首次达到固定正阈值的 N⁻⁵ᐟ² 普遍下界，并由完整 NS 光滑解族达到同阶。</p></aside>
          </div>

          <div class="tree-row clay-b-frequency-activation-row">
            <article class="tree-node current"><div class="tree-node-head"><span class="route-range">CB.25 · 2026-09-07 · FA FREQUENCY ACTIVATION</span><span class="tree-state current">当前路线边界</span></div><h3>CB.25｜固定能量下的频带激活：尖锐的 N⁻⁵ᐟ² 时间尺度</h3><p>能量级源项估计给出首次激活的 N⁻⁵ᐟ² 下界；严格空带、固定能量、完整无外力周期 NS 的光滑解族在同阶时间达到固定正阈值。</p><p>这排除指定的普遍 N⁻² 抛物等待时间，但不证明到达后驻留、低频起始、同一初值的无限级联、奇点或全局正则性。</p><p class="tree-path"><a href="/notes/clay-b-frequency-activation-20260907.html">阅读 CB.25 HTML</a> · <a href="/literature-review.html#clay-b-frequency-activation-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研究候选必须支付额外动态输入</h3><p>本冻结包没有接受下一条无条件候选；不能把首次激活重命名为驻留、固定数据级联或新缩放机制。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.26 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.25</h3><p>CB.26 只是下一章占位，不是已完成研究。到达后驻留、成熟历史、固定数据无限级联、G、R.216–R.217、一般终端缺口、一般正则性与 Clay 均未关闭。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-frequency-activation-boundary">CB.25 · Clay-B 频带激活的来源和主张边界</h3><p>本轮进行有界本地去重，并核对 <a href="https://arxiv.org/abs/2407.06474v2">Cheskidov–Peng arXiv:2407.06474v2</a> 与 <a href="https://arxiv.org/abs/1803.05569v4">Luo arXiv:1803.05569v4</a> 的官方元数据和摘要。没有导入新的外部 PDE 定理，也没有完整论文证明审计、PDF 核验、Deep Research 或穷尽性新颖性搜索。AJ 已包含固定能量、扩大环面与 N⁻⁵ᐟ² 短时工具；本章增加严格空的原速度目标带、固定正能量首次激活及匹配普遍下界的组合，不主张缩放机制新颖性、优先权或外部同行评审结论。</p><div class="boundary"><strong>CB.25 · ClayB-FrequencyActivation-20260907 公开边界</strong><p>PROVED：固定周期、ν&gt;0、E₀&gt;0 和固定光滑带乘子下，任意光滑完整无外力 NS 解的指定正振幅上升至少耗时常数倍 N⁻⁵ᐟ²；另有初值随 N 改变、目标带初始严格为空且总能量精确为 E₀ 的完整光滑解族，在同阶时间首次达到某个固定存在性阈值 η∈(0,E₀)。THRESHOLD：η 与 N 无关，但不是数值认证的能量比例。SPECIFIED COUNTEREXAMPLE：这排除仅依赖固定能量、黏性、滤波器和阈值的普遍 N⁻² 抛物激活等待下界，也排除能量级幂次 α&lt;5/2 的普遍替换。BOUNDARY：首次激活不等于到达后驻留；初始能量已在 N 附近，初值与高阶范数随 N 变化，不是低频起始、同一初值的无限级联、奇点或长期行为。FINITE CHECKS ONLY：8/8 源与来源记录、17 个 FA 标签、16 项独立有理复算及 4 项有限负对照不代替解析证明；唯一完整非作者审查者 C 接受 FA.1–17 与必需 AJ 局部理论。G、R.216–R.217、一般终端缺口、一般正则性与新颖性 OPEN；无图、仿真、新 PDF 或 recap。NOT CLAY。<a href="/notes/clay-b-frequency-activation-20260907.html">阅读完整 CB.25 笔记</a>。</p></div>
'''


def set_version(value: str, footer_label: str | None = None, *, refresh: bool = False) -> str:
    value = re.sub(r'data-site-version="\d+\.\d+"', f'data-site-version="{VERSION}"', value, count=1)
    value = re.sub(r'/i18n-en\.js\?v=\d+\.\d+', f'/i18n-en.js?v={VERSION}', value, count=1)
    if refresh:
        value = re.sub(r'/site-refresh\.js\?v=\d+\.\d+', f'/site-refresh.js?v={VERSION}', value, count=1)
    if footer_label:
        value = re.sub(rf'(?<!上次){re.escape(footer_label)} v\d+\.\d+ ·', f'{footer_label} v{VERSION} ·', value, count=1)
    return value


def build_note() -> str:
    value = (ROOT / "public/notes/clay-b-source-enstrophy-20260907.html").read_text(encoding="utf-8")
    value = set_version(value)
    value = re.sub(r'<title>.*?</title>', '<title>固定能量下的频带激活：尖锐的 N⁻⁵ᐟ² 时间尺度</title>', value, count=1)
    value = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 固定能量频带首次激活的尖锐 N⁻⁵ᐟ² 时间尺度、完整 NS 匹配构造与严格边界。">', value, count=1)
    value = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', value, count=1)
    value = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.25 · {DISPLAY_ID}</strong></header>', value, count=1)
    both = main_block("zh", ZH_SECTIONS) + "\n\n" + main_block("en", EN_SECTIONS)
    value, count = re.subn(r'  <main data-language="zh">[\s\S]*?  </main>\n\n  <main data-language="en">[\s\S]*?  </main>', both, value, count=1)
    if count != 1:
        raise RuntimeError("note bilingual template drift")
    return value


def update_home(value: str) -> str:
    value = set_version(value, "综述", refresh=True)
    value = re.sub(r'<strong>v\d+\.\d+</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', value, count=1)
    value, count = re.subn(r'<section class="route-overview independent-release-spotlight"[\s\S]*?</section>', SPOTLIGHT, value, count=1)
    if count != 1:
        raise RuntimeError("independent spotlight drift")
    value = value.replace("CB.1–CB.24", "CB.1–CB.25")
    value = value.replace("source / enstrophy / quadratic boundary", "frequency activation / sharp N^-5/2 clock", 1)
    old = "Clay-B 已核清同父残差的梯度能量边界：全周期线性无散测试消掉压力，却留下二阶源项、应变和梯度端点；固定正定二次组合不能共同正耗散，正原子分支还迫使 Δw 的 L⁴ᐟ³_tL²_x 成本发散。但这不反推 W_z 发散、混合功不可控或 G 输入减少。下一步先做一般中心 R/S 历史去重。"
    new = "Clay-B 已得到固定能量下频带首次激活的尖锐 N⁻⁵ᐟ² 时钟：普遍能量估计给下界，严格空带的完整无外力周期 NS 光滑解族达到同阶。这排除仅靠总能量的普遍 N⁻² 等待时间，但不提供到达后驻留、低频起始或同一初值的无限级联。下一候选必须支付真正额外的动态输入。"
    if old in value:
        value = value.replace(old, new, 1)
    elif new not in value:
        raise RuntimeError("homepage focus copy drift")
    value, count = re.subn(r'          <div class="tree-row (?:clay-b-same-parent-residual-row|clay-b-signed-mixed-pressure-row)">[\s\S]*?<div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB_ROWS + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if count != 1:
        raise RuntimeError("Clay-B tail drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-frequency-activation-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload.update({
        "publicIndependentNoteCount": 25,
        "latestIndependentNote": DISPLAY_ID,
        "latestIndependentResearchHtml": f"/notes/{SLUG}.html",
        "latestIndependentResearchPdf": None,
        "independentChapterScheme": "CB.n",
        "latestIndependentChapter": "CB.25",
        "nextIndependentChapter": "CB.26",
    })
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1",
            "kind": "independent-analytic-note",
            "releaseId": SLUG,
            "displayReleaseId": DISPLAY_ID,
            "chapter": "CB.25",
            "sourceCommit": "1674af0dc98825d0d0299fa69e3ae12398c3d8a0",
            "baseCommit": "c9bb03ff544c81cedeb3a6d116514d204033eb63",
            "handoffCommit": "c688fca88da5a434aac5ca46971a7d800f146b39",
            "logicalPredecessor": "ClayB-SourceEnstrophy-20260907",
            "html": f"public/notes/{SLUG}.html",
            "pdfGenerated": False,
            "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-frequency-activation-20260907-gate.test.mjs",
            "publicationTest": "tests/clay-b-frequency-activation-20260907-release.test.mjs",
            "translationScript": "scripts/add-clay-b-frequency-activation-20260907-translations.mjs",
            "browserQaScript": "scripts/qa-publication-browser.mjs",
            "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False,
            "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE",
            "simulationRequired": False,
            "recapRequired": False,
            "advancesCanonicalR0Series": False,
            "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "PROVED_ENERGY_ONLY_N_MINUS_5_OVER_2_FIRST_ACTIVATION_LOWER_BOUND_AND_MATCHING_FULL_UNFORCED_PERIODIC_SMOOTH_NS_FAMILY_WITH_STRICTLY_EMPTY_TARGET_BAND_EXISTENTIAL_FIXED_POSITIVE_THRESHOLD_NOT_NUMERIC_FRACTION_FIRST_ACTIVATION_NOT_RESIDENCE_INITIAL_ENERGY_ALREADY_COMPARABLE_HIGH_FREQUENCY_DATA_DEPENDS_ON_N_NO_FIXED_DATA_INFINITE_CASCADE_SINGULARITY_GLOBAL_REGULARITY_NOVELTY_OR_CLAY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def handoff_bytes() -> bytes:
    ledger = json.loads((ROOT / "research/clay_b_frequency_activation_frozen_ledger_20260907.json").read_text(encoding="utf-8"))
    qa = json.loads((ROOT / "release/qa/clay-b-frequency-activation-20260907.json").read_text(encoding="utf-8"))
    roles = {"scientific-source": "frozen-scientific-source", "dependency": "frozen-dependency", "provenance": "frozen-provenance-record"}
    artifacts = [{"path": r["path"], "sha256": r["sha256"], "role": roles[r["role"]], "commit": r["commit"]} for r in ledger["files"]]
    artifacts += [{"path": r["path"], "sha256": r["sha256"], "role": "frozen-release-manifest", "commit": r["commit"]} for r in ledger["handoffEnvelope"]]
    outputs = [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html", "public/notes/index.html", "public/site-version.json", "research/release-manifest.json", "VERSION"]
    support = ["research/clay_b_frequency_activation_frozen_ledger_20260907.json", "release/handoffs/clay-b-frequency-activation-20260907.json", "release/qa/clay-b-frequency-activation-20260907.json", "scripts/import_clay_b_frequency_activation_20260907_frozen.py", "scripts/generate_clay_b_frequency_activation_20260907_release.py", "scripts/generate_note_index.py", "scripts/add-clay-b-frequency-activation-20260907-translations.mjs", "tests/clay-b-frequency-activation-20260907-gate.test.mjs", "tests/clay-b-frequency-activation-20260907-release.test.mjs", "tests/release-publication-invariant.test.mjs", "translations/en.json", "public/i18n-en.js"]
    managed = list(dict.fromkeys(outputs + [r["path"] for r in artifacts] + support))
    payload = {
        "schemaVersion": "research-publication-handoff-v1",
        "releaseId": DISPLAY_ID,
        "frozenCommit": "c688fca88da5a434aac5ca46971a7d800f146b39",
        "sourceRepository": "navier-stokes-r074m",
        "translationRoute": "LOCAL_DIRECT_NO_DGX",
        "artifacts": artifacts,
        "artifactPolicy": {"readerPdf": "OMIT_NEW", "scientificFigure": "NOT_REQUIRED"},
        "claimBoundary": {"requiredLabels": ["PROVED", "SHARP SCALE", "FULL NS", "EXISTENTIAL THRESHOLD", "NO RESIDENCE CLAIM", "LITERATURE", "FINITE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"], "publicFiles": [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html"]},
        "recap": {"mode": "PRESERVE", "latestRecapRelease": "r076i", "preservedArtifacts": [{"path": "public/recap-r0-61-r0-76i.html", "sha256": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9"}, {"path": "public/recap-r0-61-r0-76i.pdf", "sha256": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98"}]},
        "stages": {"generate": {"runner": "python-local", "script": "scripts/generate_clay_b_frequency_activation_20260907_release.py", "inputs": [r["path"] for r in artifacts] + ["research/clay_b_frequency_activation_frozen_ledger_20260907.json"], "outputs": outputs}, "translate": {"runner": "node-local", "script": "scripts/add-clay-b-frequency-activation-20260907-translations.mjs", "inputs": ["public/research-review.html", "public/literature-review.html", "public/notes/index.html", "translations/en.json"], "outputs": ["translations/en.json", "public/i18n-en.js"]}},
        "publication": {"expectedCommit": None, "siteBaseUrl": "https://kasifa.github.io", "repository": "Kasifa/Kasifa.github.io", "workflow": "pages.yml", "remote": "origin", "targetBranch": "main", "commitMessage": "Publish ClayB FrequencyActivation CB.25 HTML note", "managedPaths": managed, "expectedLive": qa["online"]["expectedLive"], "expectedAbsent": qa["online"]["expectedAbsent"], "siteVersionExpectations": qa["online"]["siteVersionExpectations"]},
        "visualQa": {"evidencePath": qa["browser"]["evidencePath"], "configPath": "release/qa/clay-b-frequency-activation-20260907.json", "requiredChecks": [f"{t['id']}-{s['id']}" for t in qa["browser"]["targets"] for s in qa["browser"]["scenarios"]]},
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.25", DISPLAY_ID, "固定能量下的频带激活", "Band activation at fixed energy", "N⁻⁵ᐟ²", "PROVED", "SHARP SCALE", "FULL NS", "EXISTENTIAL THRESHOLD", "NO RESIDENCE CLAIM", "LITERATURE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.25", "Clay-B 独立路线停在 CB.25", "CB.26 · NEXT", 'class="tree-row clay-b-frequency-activation-row"', f"/notes/{SLUG}.html", "单独的虚线泳道"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0 = home.index('class="route-tree r0-route-tree"'); rb = home.index('class="tree-row r0-public-boundary-row"', r0); div = home.index('class="route-lane-divider"', rb); clay = home.index('class="route-tree clay-b-route-tree"', div); cb = home.index('class="tree-row clay-b-frequency-activation-row"', clay); bound = home.index('class="tree-row clay-b-public-boundary-row"', cb)
    if not (r0 < rb < div < clay < cb < bound):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-frequency-activation-boundary"' not in literature or "CB.25 · ClayB-FrequencyActivation-20260907 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.25 · {DISPLAY_ID}" not in index or "25 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8")); manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.25" or site.get("nextIndependentChapter") != "CB.26":
        raise RuntimeError("version or chapter metadata drift")
    if manifest.get("latestCompletedRelease") != "r076l" or site.get("latestRelease") != "R0.76L":
        raise RuntimeError("canonical R0 endpoint drift")
    path = ROOT / "release/handoffs/clay-b-frequency-activation-20260907.json"
    if not path.is_file() or path.read_bytes() != handoff_bytes():
        raise RuntimeError("publication handoff drift")


if not CHECK_ONLY:
    NOTE_PATH.write_text(build_note(), encoding="utf-8")
    home = ROOT / "public/research-review.html"; home.write_text(update_home(home.read_text(encoding="utf-8")), encoding="utf-8")
    literature = ROOT / "public/literature-review.html"; literature.write_text(update_literature(literature.read_text(encoding="utf-8")), encoding="utf-8")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    update_metadata(ROOT / "public/site-version.json"); update_metadata(ROOT / "research/release-manifest.json")
    subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    (ROOT / "release/handoffs/clay-b-frequency-activation-20260907.json").write_bytes(handoff_bytes())

validate()
print(json.dumps({"schemaVersion": "clay-b-frequency-activation-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.25", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
