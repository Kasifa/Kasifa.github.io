#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB ConvexPressureTrace CB.21 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.65"
SLUG = "clay-b-convex-pressure-trace-20260906"
DISPLAY_ID = "ClayB-ConvexPressureTrace-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_SECTIONS = [
    ("01 / 结果地图", "固定凸测试已经付清，二次端点仍未闭合", """<div class="grid"><div class="card"><strong class="proved">PROVED IN STATED SCOPE</strong>对每个固定的光滑凸函数 β，若其梯度和 Hessian 有界，则压力耦合线性方程具有精确凸能量恒等式，并覆盖弱初始端点。</div><div class="card"><strong class="proved">STRONG TRACE BELOW L²</strong>特定 β_R 给出 ||w(t)||₁≤κ(t)，从而所有 1≤q&lt;2 都有强零初迹。</div><div class="card"><strong class="open">OPEN ENDPOINT</strong>当附加正能量原子并撤去幅度截断时，压力通量仍承担 δ₀/2；强 L² 初迹与原子排除没有闭合。</div></div><p>BT.1–BT.12 不假设原子、初始能量不等式或 b 本身满足 NS。BT.13 以后才进入 BP 的条件性原子分支。</p>"""),
    ("02 / BT.1–BT.3", "压力梯度具有足够的时间可积性", """<p>在固定三维环面上，设 b,w∈L∞_tL²_x∩L²_tH¹_x、二者无散，w 满足投影后的线性方程并且 w∈C_wL²、具有弱零初迹。有限指数的周期 Leray 投影给出压力梯度，而不是更强的 L²H⁻¹ 时间迹接口。</p><div class="equation">∇π = −(I−P)(b·∇w) ∈ L¹_tL³ᐟ²_x,   κ(t)=∫₀ᵗ||∇π||₁ ds → 0.   (BT.2–BT.3)</div><p>这里 κ(t)≤C||b||_{L²(0,t;L⁶)}||∇w||_{L²((0,t)×Ω)}。这正好支付后续有界梯度测试的压力项，但不支付二次测试所需的强初迹。</p>"""),
    ("03 / BT.4–BT.9", "固定有界凸函数满足精确恒等式", """<p>先做空间卷积。输运项产生一个 L¹ 交换子，压力采用梯度形式；有界梯度与 Hessian 控制测试函数，强 L² 梯度收敛处理耗散。逐项极限后，对所有端点得到精确凸恒等式。</p><div class="equation">∫β(w(t)) + ν∫₀ᵗ∫D²β(w)[∇w,∇w] = ∫β(w(0)) + ∫₀ᵗ∫∇β(w)·∇π.   (BT.9)</div><p><strong>DIRECT DERIVATION</strong>这是本章针对向量压力方程的局部推导，不是把标量重整化定理直接改名导入。</p>"""),
    ("04 / BT.10–BT.12", "所有 1≤q<2 的强零初迹", """<p>取 β_R(z)=R²(√(1+|z|²/R²)−1)，除以 R 后令 R↓0；丢弃非负耗散，得到 ||w(t)||₁≤κ(t)。再与一致 L² 界插值：</p><div class="equation">||w(t)||_q → 0   for every 1≤q&lt;2,   but not q=2.   (BT.12)</div><p>因此弱零初迹被提升为全部次二次空间指数的强零初迹。这里没有把 q&lt;2 的结果外推到 q=2，也没有从固定 R 的估计假设 R 一致性。</p>"""),
    ("05 / BT.13–BT.17", "附加原子下，幅度压力通量重现端点成本", """<p>只有从这里开始恢复 BP 的同一共同伴随，并附加正终端能量原子。固定正时间先令 R→∞，幅度压力通量的积分趋于 1/2；它在正时间几乎处处趋零，却在任何初端窗口都不一致可积。</p><div class="equation">lim_{R→∞}∫₀ᵗQ_R(s)ds = 1/2,   Q_R ⇀ δ₀/2 against C¹ time tests.   (BT.15–BT.17)</div><p><strong>CONDITIONAL ENDPOINT</strong>这只是 BS 半单位端点成本的另一种精确表示。没有证明通量测度总变差一致有界、测度弱星收敛或 suitable 缺陷识别。</p>"""),
    ("06 / BT.18–BT.20", "幅度逃逸是必要约束，不是矛盾", """<p>低幅度能量至多为 (√2+1)Rκ(t)。若 R(t)→∞ 且 R(t)κ(t)→0，则渐近单位能量必须逃到该幅度以上；同时在扩展值意义下 κ(t)||w(t)||∞≥||w(t)||²₂。</p><p>这些是原子条件下的必要约束，不是互相矛盾的上下界。BT.20 的有符号空间压力配对只对几乎每个固定时间成立；只有有界梯度表示已证明属于时空 L¹。</p>"""),
    ("07 / BT.21–BT.22", "普遍消压的局部测试分类", """<p>若一个 C² 状态局部测试对每个光滑周期无散场 v 和每个独立光滑压力 p 都消去压力，则它只能是各向同性二次函数加仿射函数。凸性迫使二次系数非负；若再要求全局有界梯度，二次系数只能为零。</p><div class="equation">β(z)=a|z|²/2 + ℓ·z + c,   a≥0;   bounded ∇β ⇒ a=0.   (BT.22)</div><p>任意无迹 jet 由局部旋度势实现。这里的“每个独立压力”前提严格强于实际 NS 压力，因此这不是对同一 NS 压力、时空依赖、耦合或非局部测试的无路可走定理。</p>"""),
    ("08 / 来源、证据与下一步", "对齐残差审计尚未开始", """<p>科学源提交 1cd4679f91661ece2b3d55ae16d45ba980094344；冻结提交 148dc22795632524c303231ec000b1a239da192a。六份本轮文件、136 份依赖和一份冻结 manifest 由 SHA-256 绑定；三份文本源、22 个 BT 标签、16 项有理算术加一项 5×6 秩检查，以及 4 项有限负对照通过。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_convex_pressure_trace_20260906.md">BT 凸压力正文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_convex_pressure_primary_reading_20260906.md">BCC 核读边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_convex_pressure_report_20260906.md">阶段报告</a></p><p>下一研发动作只检查同一原解的 b+√m w 对齐残差梯度，是否提供当前未付的压力抵消或临界控制。该审计尚未开始。</p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap；不分发第三方 PDF。非零弱零迹解、原子存在或排除、强 L² 初迹、G、一般正则性与新颖性仍 OPEN。NOT CLAY。</strong></p>"""),
]

EN_SECTIONS = [
    ("01 / Result map", "Fixed convex tests are paid; the quadratic endpoint remains open", """<div class="grid"><div class="card"><strong class="proved">PROVED IN STATED SCOPE</strong>For every fixed smooth convex β with bounded gradient and Hessian, the pressure-coupled linear equation has an exact convex energy identity including the weak initial endpoint.</div><div class="card"><strong class="proved">STRONG TRACE BELOW L²</strong>A specific β_R gives ||w(t)||₁≤κ(t), hence strong-zero initial trace for every 1≤q&lt;2.</div><div class="card"><strong class="open">OPEN ENDPOINT</strong>After adding a positive energy atom and removing the amplitude cutoff, the pressure flux still carries δ₀/2; strong L² trace and atom exclusion do not close.</div></div><p>BT.1–BT.12 assumes no atom, initial energy inequality, or NS equation for b. The conditional atom branch begins only at BT.13.</p>"""),
    ("02 / BT.1–BT.3", "The pressure gradient has sufficient time integrability", """<p>On a fixed three-dimensional torus, let b,w∈L∞_tL²_x∩L²_tH¹_x be divergence free, with w solving the projected linear equation, w∈C_wL², and weak-zero initial trace. Finite-exponent periodic Leray projection gives the pressure gradient, not the stronger L²H⁻¹ time-trace interface.</p><div class="equation">∇π = −(I−P)(b·∇w) ∈ L¹_tL³ᐟ²_x,   κ(t)=∫₀ᵗ||∇π||₁ ds → 0.   (BT.2–BT.3)</div><p>Here κ(t)≤C||b||_{L²(0,t;L⁶)}||∇w||_{L²((0,t)×Ω)}. This pays exactly for the pressure term in bounded-gradient tests, but not for the strong trace needed by the quadratic test.</p>"""),
    ("03 / BT.4–BT.9", "Every fixed bounded convex test satisfies an exact identity", """<p>First mollify in space. Transport produces one L¹ commutator and pressure is kept in gradient form. Bounded gradient and Hessian control the test, while strong L² convergence of gradients handles dissipation. Passing each limit gives the exact convex identity at every endpoint.</p><div class="equation">∫β(w(t)) + ν∫₀ᵗ∫D²β(w)[∇w,∇w] = ∫β(w(0)) + ∫₀ᵗ∫∇β(w)·∇π.   (BT.9)</div><p><strong>DIRECT DERIVATION</strong>This is the chapter's local vector-pressure derivation, not a scalar renormalization theorem relabeled as a vector result.</p>"""),
    ("04 / BT.10–BT.12", "Strong-zero initial trace holds for every 1≤q<2", """<p>Choose β_R(z)=R²(√(1+|z|²/R²)−1), divide by R, send R↓0, and discard nonnegative dissipation. This yields ||w(t)||₁≤κ(t). Interpolation with the uniform L² bound gives:</p><div class="equation">||w(t)||_q → 0   for every 1≤q&lt;2,   but not q=2.   (BT.12)</div><p>The weak-zero trace is therefore upgraded to a strong-zero trace at every subquadratic spatial exponent. Nothing here extrapolates q&lt;2 to q=2 or assumes estimates for fixed R are uniform in R.</p>"""),
    ("05 / BT.13–BT.17", "With the additional atom, amplitude pressure flux reproduces the endpoint cost", """<p>Only here do we restore BP's same common adjoint and add the positive terminal-energy atom. Sending R→∞ at fixed positive time makes the integrated amplitude pressure flux tend to 1/2. It tends to zero almost everywhere at positive times but is not uniformly integrable on any initial interval.</p><div class="equation">lim_{R→∞}∫₀ᵗQ_R(s)ds = 1/2,   Q_R ⇀ δ₀/2 against C¹ time tests.   (BT.15–BT.17)</div><p><strong>CONDITIONAL ENDPOINT</strong>This is another exact representation of BS's unpaid half-unit endpoint cost. No uniform total variation, flux-measure weak-star convergence, or suitable-defect identification is proved.</p>"""),
    ("06 / BT.18–BT.20", "Amplitude escape is a necessary constraint, not a contradiction", """<p>Low-amplitude energy is at most (√2+1)Rκ(t). If R(t)→∞ and R(t)κ(t)→0, asymptotically unit energy must escape above that amplitude. Also κ(t)||w(t)||∞≥||w(t)||²₂ in the extended-value sense.</p><p>These are necessary constraints under the atom condition, not contradictory upper and lower bounds. The signed spatial pressure pairings in BT.20 hold only for almost every fixed time. Only the bounded-gradient representation is proved spacetime L¹.</p>"""),
    ("07 / BT.21–BT.22", "Classifying local tests that universally cancel pressure", """<p>If a C² state-local test cancels pressure for every smooth periodic divergence-free field v and every independent smooth pressure p, it must be an isotropic quadratic plus an affine function. Convexity makes the quadratic coefficient nonnegative, and a globally bounded gradient forces that coefficient to vanish.</p><div class="equation">β(z)=a|z|²/2 + ℓ·z + c,   a≥0;   bounded ∇β ⇒ a=0.   (BT.22)</div><p>Local curl potentials realize arbitrary trace-free jets. The “every independent pressure” premise is strictly stronger than actual NS pressure, so this is not a no-go theorem for same-NS pressure, time- or space-dependent, coupled, or nonlocal tests.</p>"""),
    ("08 / Sources, evidence, and next step", "The alignment-residual audit has not started", """<p>Scientific source commit: 1cd4679f91661ece2b3d55ae16d45ba980094344; freeze commit: 148dc22795632524c303231ec000b1a239da192a. Six current files, 136 dependencies, and one frozen manifest are SHA-256-bound. Three text sources, 22 BT labels, 16 rational checks plus one 5×6 rank check, and four limited negative controls pass.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_convex_pressure_trace_20260906.md">BT convex-pressure source</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_convex_pressure_primary_reading_20260906.md">BCC reading boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_convex_pressure_report_20260906.md">stage report</a></p><p>The next research action asks only whether the same-parent b+√m w alignment-residual gradient provides an unpaid pressure cancellation or critical control. That audit has not started.</p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap and redistributes no third-party PDF. A nonzero weak-zero-trace solution, atom existence or exclusion, strong L² trace, G, general regularity, and novelty remain OPEN. NOT CLAY.</strong></p>"""),
]


def main_block(lang: str, sections: list[tuple[str, str, str]]) -> str:
    if lang == "zh":
        kicker = "CB.21 · 独立 Clay-B 方法笔记 · 2026-09-06"
        title = "CB.21｜有界凸压力测试：次二次强初迹与幅度端点"
        dek = "有限指数压力估计足以关闭每个固定有界凸测试，并把弱零初迹提升到所有 1≤q<2；但在额外正原子分支中，撤去幅度截断仍留下 δ₀/2 的端点成本，强 L² 初迹没有闭合。"
        footer = "独立 HTML 研究笔记"
    else:
        kicker = "CB.21 · Independent Clay-B methods note · 2026-09-06"
        title = "CB.21 | Bounded convex pressure tests: subquadratic strong trace and amplitude endpoint"
        dek = "Finite-exponent pressure control closes every fixed bounded convex test and upgrades the weak-zero trace to every 1≤q<2. On the additional positive-atom branch, however, removing the amplitude cutoff still leaves an endpoint cost δ₀/2, and strong L² trace does not close."
        footer = "Independent HTML research note"
    body = "".join(f'<section><div class="section-no">{n}</div><h2>{h}</h2>{c}</section>' for n, h, c in sections)
    return f'''  <main data-language="{lang}">
    <article><header class="hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="dek">{dek}</p><div class="meta"><span>PROVED IN STATED SCOPE</span><span>DIRECT DERIVATION</span><span>CONDITIONAL ENDPOINT</span><span>LITERATURE</span><span>FINITE CHECKS ONLY</span><span>OPEN · NOT CLAY</span></div></header>{body}</article>
    <footer class="footer">CB.21 · {footer} · {DISPLAY_ID} · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-convex-pressure-trace" aria-labelledby="clay-b-convex-pressure-trace-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.21 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · CONVEX PRESSURE TRACE</p><h2 class="route-map-title" id="clay-b-convex-pressure-trace-title">CB.21｜有界凸压力测试：次二次强初迹与幅度端点</h2><p class="route-map-intro">固定有界凸测试在压力梯度 L¹ 时间预算下得到精确恒等式，并推出所有 1≤q&lt;2 的强零初迹；额外正原子下，撤去幅度截断仍重现 δ₀/2 的端点压力成本。强 L² 初迹、原子排除与一般正则性 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 有界凸压力笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-convex-pressure-trace-20260906.html">阅读最新 CB.21 凸压力笔记 →</a><a href="/literature-review.html#clay-b-convex-pressure-trace-boundary">查看原始来源与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 有界凸压力结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>固定凸测试与次二次强初迹</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>幅度端点仍承担 δ₀/2</span><span><i class="route-legend-mark current" aria-hidden="true"></i>同一原解对齐残差与强 L² OPEN · NOT CLAY</span></div></div></section>'''

CB_ROWS = '''          <div class="tree-row clay-b-adjoint-weak-trace-screen-row">
            <article class="tree-node"><div class="tree-node-head"><span class="route-range">CB.20 · 2026-09-06 · BS ADJOINT WEAK-TRACE SCREEN</span><span class="tree-state">独立路线章节</span></div><h3>CB.20｜伴随的弱零初迹：边界通量与唯一性接口</h3><p>BS 把共同伴随反时为前向正黏性、压力耦合向量方程：初迹分布意义下为零，但能量右极限为一。有限 Fourier 通量对 C¹ 时间测试趋于边界泛函 δ₀/2，正时间几乎处处趋零，因而不一致可积。</p><p>额外 L²H⁻¹、张量 L² 或 Serrin 漂移条件会给强初迹并排除该跳跃，但基本能量没有支付。ESS、Lei–Yang–Yuan、Cheskidov–Luo 与 Bonicatto–Ciampa–Crippa 四个接口都不能在不增加假设时原样导入；这不是穷尽性文献结论。</p><p class="tree-path"><a href="/notes/clay-b-adjoint-weak-trace-screen-20260906.html">阅读 CB.20 HTML</a> · <a href="/literature-review.html#clay-b-adjoint-weak-trace-screen-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right kept"><span class="tree-state">CONVEX PRESSURE TRACE COMPLETED</span><h3>有界凸压力测试已进入 CB.21</h3><p>BT 已付清压力梯度可积性、固定凸测试和次二次强初迹，并校准幅度端点与普遍局部测试分类；结果见下一个正式路线节点。</p></aside>
          </div>

          <div class="tree-row clay-b-convex-pressure-trace-row">
            <article class="tree-node current"><div class="tree-node-head"><span class="route-range">CB.21 · 2026-09-06 · BT CONVEX PRESSURE TRACE</span><span class="tree-state current">当前路线边界</span></div><h3>CB.21｜有界凸压力测试：次二次强初迹与幅度端点</h3><p>BT 用有限指数 Leray 投影得到 ∇π∈L¹_tL³ᐟ²_x，并为每个固定有界凸测试建立含弱初端点的精确恒等式。特定 β_R 推出 ||w(t)||₁≤κ(t)，从而所有 1≤q&lt;2 都有强零初迹，但不包括 q=2。</p><p>在额外正能量原子条件下，幅度 R→∞ 的压力通量仍对 C¹ 时间测试趋于 δ₀/2；低幅度能量估计与普遍消压局部测试分类都是必要校准，不排除原子，也不是一般正则性结论。</p><p class="tree-path"><a href="/notes/clay-b-convex-pressure-trace-20260906.html">阅读 CB.21 HTML</a> · <a href="/literature-review.html#clay-b-convex-pressure-trace-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发动作：同一原解的对齐残差</h3><p>只检查 b+√m w 的残差梯度是否产生当前未付的压力抵消或临界控制。该审计尚未开始。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.22 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.21</h3><p>CB.22 只是下一章占位，不是已完成研究。同一原解对齐残差、非局部压力抵消、原子存在或排除、强 L² 初迹、G、任意奇点输入生成、一般正则性与 Clay 均未关闭。</p></article></div>'''

LITERATURE_BLOCK = '''<h3 id="clay-b-convex-pressure-trace-boundary">CB.21 · Clay-B 有界凸压力测试的文献和主张边界</h3><p>本轮根任务复核 <a href="https://arxiv.org/abs/2306.15529v1">Bonicatto–Ciampa–Crippa 2306.15529v1</a> 元数据，并完整提取、视觉复读 PDF 6–8 页，包括 Definition 2.3、Lemma 2.6 和 Theorem 2.7 的完整证明。该文是标量连续性方程接口；本章的向量压力扩展是局部推导，不冒充原文结论。Vasseur、Frehse–Specovius-Neugebauer 等更宽读取只记作内部 B-only 范围，没有作为根任务完整核读或新增定理导入。</p><div class="boundary"><strong>CB.21 · ClayB-ConvexPressureTrace-20260906 公开边界</strong><p>PROVED IN STATED SCOPE：BT.1–BT.12 只假设固定三维环面、ν&gt;0、无散 b,w∈L∞L²∩L²H¹、投影线性方程、w∈C_wL² 与弱零初迹；不假设原子、初始能量不等式或 b 满足 NS。PRESSURE INTEGRABILITY：有限指数投影给 ∇π∈L¹_tL³ᐟ²_x 和 κ(t)→0，不是 L²H⁻¹ 接口。DIRECT DERIVATION：每个固定光滑凸 β 若梯度与 Hessian 有界，则空间卷积、一个 L¹ 交换子、压力梯度形式与强 L² 梯度收敛给出含弱初端点的精确凸恒等式。SUBQUADRATIC TRACE：β_R 在 R↓0 后给 ||w(t)||₁≤κ(t) 与所有 1≤q&lt;2 的强零初迹，不包括 q=2。CONDITIONAL ENDPOINT：只从 BT.13 起增加 BP 正原子；R→∞ 后幅度压力通量积分为 1/2，正时间几乎处处为零，对 C¹ 时间测试趋于 δ₀/2；无一致总变差、测度弱星收敛或 suitable 缺陷识别。AMPLITUDE ESCAPE：低幅度能量上界与 κ(t)||w(t)||∞≥||w(t)||²₂ 是必要约束，不是矛盾。BT.20 仅在几乎每个固定时间给等价有符号压力配对；只有有界梯度形式证明时空 L¹。LOCAL-TEST CLASSIFICATION：对每个独立光滑压力都普遍消压的 C² 状态局部测试只能是各向同性二次加仿射；该前提强于实际 NS，不排除同一 NS 压力、时空耦合或非局部测试。FINITE CHECKS ONLY：三份文本源、22 个 BT 标签、142/142 文件绑定、17 项算术或秩检查和 4 项有限负对照不替代 PDE 证明。非零弱零迹解、原子存在或排除、强 L² 初迹、对齐残差、G、一般正则性与新颖性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。<a href="/notes/clay-b-convex-pressure-trace-20260906.html">阅读完整 CB.21 笔记</a>。</p></div>
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
    value = (ROOT / "public/notes/clay-b-adjoint-weak-trace-screen-20260906.html").read_text(encoding="utf-8")
    value = set_version(value)
    value = re.sub(r'<title>.*?</title>', '<title>有界凸压力测试：次二次强初迹与幅度端点</title>', value, count=1)
    value = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 有界凸压力测试、次二次强零初迹和条件性幅度端点的双语方法笔记。">', value, count=1)
    value = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', value, count=1)
    value = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.21 · {DISPLAY_ID}</strong></header>', value, count=1)
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
    value = value.replace("CB.1–CB.20", "CB.1–CB.21")
    value = value.replace("adjoint weak-trace / endpoint-flux screen", "bounded convex pressure / subquadratic trace", 1)
    old_focus = "Clay-B 已把共同伴随的唯一性问题校准为弱初迹端点通量：反时后是前向压力耦合方程，有限 Fourier 通量对 C¹ 时间测试趋于 δ₀/2，但总变差、测度弱星收敛和 suitable 缺陷识别均未证明。四个已核读唯一性接口仍需未付输入。下一步只检查压力感知的有界凸测试。"
    new_focus = "Clay-B 已完成固定有界凸压力测试：能量类给出压力梯度时间 L¹ 可积性和所有 1≤q<2 的强零初迹；但额外正原子下撤去幅度截断仍重现 δ₀/2 的端点成本，强 L² 与原子排除没有闭合。下一步只检查同一原解的对齐残差。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    value, count = re.subn(r'          <div class="tree-row clay-b-adjoint-weak-trace-screen-row">[\s\S]*?<div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB_ROWS + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if count != 1:
        raise RuntimeError("Clay-B tail drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-convex-pressure-trace-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 21
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.21"
    payload["nextIndependentChapter"] = "CB.22"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1",
            "kind": "independent-analytic-note",
            "releaseId": SLUG,
            "displayReleaseId": DISPLAY_ID,
            "chapter": "CB.21",
            "sourceCommit": "1cd4679f91661ece2b3d55ae16d45ba980094344",
            "baseCommit": "a1dc8ad6a9a5b50f6a9fd63c482538d863583c77",
            "handoffCommit": "148dc22795632524c303231ec000b1a239da192a",
            "logicalPredecessor": "ClayB-AdjointWeakTraceScreen-20260906",
            "html": f"public/notes/{SLUG}.html",
            "pdfGenerated": False,
            "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-convex-pressure-trace-20260906-gate.test.mjs",
            "publicationTest": "tests/clay-b-convex-pressure-trace-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-convex-pressure-trace-20260906-translations.mjs",
            "browserQaScript": "scripts/qa-publication-browser.mjs",
            "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False,
            "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE",
            "simulationRequired": False,
            "recapRequired": False,
            "advancesCanonicalR0Series": False,
            "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "FIXED_SMOOTH_CONVEX_TESTS_WITH_BOUNDED_GRADIENT_AND_HESSIAN_HAVE_EXACT_IDENTITIES_AND_GIVE_STRONG_ZERO_TRACE_FOR_ALL_Q_BELOW_TWO_PRESSURE_GRADIENT_ONLY_L1_TIME_NOT_L2H_MINUS1_ADDITIONAL_POSITIVE_ATOM_AMPLITUDE_LIMIT_REPRODUCES_DELTA_ZERO_OVER_TWO_WITHOUT_TV_MEASURE_WEAK_STAR_OR_SUITABLE_DEFECT_IDENTIFICATION_UNIVERSAL_ARBITRARY_PRESSURE_LOCAL_TEST_CLASSIFICATION_STRONGER_THAN_ACTUAL_NS_PREMISE_ALIGNMENT_RESIDUAL_ATOM_EXCLUSION_STRONG_L2_GENERAL_REGULARITY_AND_NOVELTY_OPEN_NOT_CLAY",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def handoff_bytes() -> bytes:
    ledger = json.loads((ROOT / "research/clay_b_convex_pressure_trace_frozen_ledger_20260906.json").read_text(encoding="utf-8"))
    qa = json.loads((ROOT / "release/qa/clay-b-convex-pressure-trace-20260906.json").read_text(encoding="utf-8"))
    artifacts = [{"path": row["path"], "sha256": row["sha256"], "role": "frozen-scientific-source" if row["role"] == "scientific-source" else "frozen-dependency", "commit": row["commit"]} for row in ledger["files"]]
    artifacts += [{"path": row["path"], "sha256": row["sha256"], "role": "frozen-release-manifest", "commit": row["commit"]} for row in ledger["handoffEnvelope"]]
    outputs = [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html", "public/notes/index.html", "public/site-version.json", "research/release-manifest.json", "VERSION"]
    support = ["research/clay_b_convex_pressure_trace_frozen_ledger_20260906.json", "release/handoffs/clay-b-convex-pressure-trace-20260906.json", "release/qa/clay-b-convex-pressure-trace-20260906.json", "scripts/import_clay_b_convex_pressure_trace_20260906_frozen.py", "scripts/generate_clay_b_convex_pressure_trace_20260906_release.py", "scripts/generate_note_index.py", "scripts/add-clay-b-convex-pressure-trace-20260906-translations.mjs", "tests/clay-b-convex-pressure-trace-20260906-gate.test.mjs", "tests/clay-b-convex-pressure-trace-20260906-release.test.mjs", "tests/release-publication-invariant.test.mjs", "translations/en.json", "public/i18n-en.js"]
    managed = list(dict.fromkeys(outputs + [row["path"] for row in artifacts] + support))
    payload = {
        "schemaVersion": "research-publication-handoff-v1",
        "releaseId": DISPLAY_ID,
        "frozenCommit": "148dc22795632524c303231ec000b1a239da192a",
        "sourceRepository": "navier-stokes-r074m",
        "translationRoute": "LOCAL_DIRECT_NO_DGX",
        "artifacts": artifacts,
        "artifactPolicy": {"readerPdf": "OMIT_NEW", "scientificFigure": "NOT_REQUIRED"},
        "claimBoundary": {"requiredLabels": ["PROVED", "PROVED IN STATED SCOPE", "DIRECT DERIVATION", "CONDITIONAL ENDPOINT", "LITERATURE", "FINITE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"], "publicFiles": [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html"]},
        "recap": {"mode": "PRESERVE", "latestRecapRelease": "r076i", "preservedArtifacts": [{"path": "public/recap-r0-61-r0-76i.html", "sha256": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9"}, {"path": "public/recap-r0-61-r0-76i.pdf", "sha256": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98"}]},
        "stages": {
            "generate": {"runner": "python-local", "script": "scripts/generate_clay_b_convex_pressure_trace_20260906_release.py", "inputs": [row["path"] for row in artifacts] + ["research/clay_b_convex_pressure_trace_frozen_ledger_20260906.json"], "outputs": outputs},
            "translate": {"runner": "node-local", "script": "scripts/add-clay-b-convex-pressure-trace-20260906-translations.mjs", "inputs": ["public/research-review.html", "public/literature-review.html", "public/notes/index.html", "translations/en.json"], "outputs": ["translations/en.json", "public/i18n-en.js"]},
        },
        "publication": {"expectedCommit": None, "siteBaseUrl": "https://kasifa.github.io", "repository": "Kasifa/Kasifa.github.io", "workflow": "pages.yml", "remote": "origin", "targetBranch": "main", "commitMessage": "Publish ClayB ConvexPressureTrace CB.21 HTML note", "managedPaths": managed, "expectedLive": qa["online"]["expectedLive"], "expectedAbsent": qa["online"]["expectedAbsent"], "siteVersionExpectations": qa["online"]["siteVersionExpectations"]},
        "visualQa": {"evidencePath": qa["browser"]["evidencePath"], "configPath": "release/qa/clay-b-convex-pressure-trace-20260906.json", "requiredChecks": [f"{target['id']}-{scenario['id']}" for target in qa["browser"]["targets"] for scenario in qa["browser"]["scenarios"]]},
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.21", DISPLAY_ID, "有界凸压力测试：次二次强初迹与幅度端点", "Bounded convex pressure tests: subquadratic strong trace and amplitude endpoint", "PROVED IN STATED SCOPE", "DIRECT DERIVATION", "CONDITIONAL ENDPOINT", "LITERATURE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.21", "Clay-B 独立路线停在 CB.21", "CB.22 · NEXT", 'class="tree-row clay-b-convex-pressure-trace-row"', f"/notes/{SLUG}.html", "单独的虚线泳道"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb21 = home.index('class="tree-row clay-b-convex-pressure-trace-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb21)
    if not (r0_start < r0_boundary < divider < clay_start < cb21 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-convex-pressure-trace-boundary"' not in literature or "CB.21 · ClayB-ConvexPressureTrace-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.21 · {DISPLAY_ID}" not in index or "21 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.21" or site.get("nextIndependentChapter") != "CB.22":
        raise RuntimeError("version or chapter metadata drift")
    if manifest.get("latestCompletedRelease") != "r076l" or site.get("latestRelease") != "R0.76L":
        raise RuntimeError("canonical R0 endpoint drift")
    expected = handoff_bytes()
    path = ROOT / "release/handoffs/clay-b-convex-pressure-trace-20260906.json"
    if not path.is_file() or path.read_bytes() != expected:
        raise RuntimeError("publication handoff drift")


if not CHECK_ONLY:
    NOTE_PATH.write_text(build_note(), encoding="utf-8")
    home_path = ROOT / "public/research-review.html"
    home_path.write_text(update_home(home_path.read_text(encoding="utf-8")), encoding="utf-8")
    literature_path = ROOT / "public/literature-review.html"
    literature_path.write_text(update_literature(literature_path.read_text(encoding="utf-8")), encoding="utf-8")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    update_metadata(ROOT / "public/site-version.json")
    update_metadata(ROOT / "research/release-manifest.json")
    subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    (ROOT / "release/handoffs/clay-b-convex-pressure-trace-20260906.json").write_bytes(handoff_bytes())

validate()
print(json.dumps({"schemaVersion": "clay-b-convex-pressure-trace-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.21", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
