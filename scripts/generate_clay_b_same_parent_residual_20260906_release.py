#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB SameParentResidual CB.22 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.66"
SLUG = "clay-b-same-parent-residual-20260906"
DISPLAY_ID = "ClayB-SameParentResidual-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_SECTIONS = [
    ("01 / 结果地图", "同一原解给出真实残差结构，但尚未关闭幅度端点", """<div class="grid"><div class="card"><strong class="proved">CONDITIONAL RESULT</strong>在 BP 的正终端能量原子条件下，z=b+√m w 的终端残差测度为 μ_*−mδ_a，并且在目标点 a 没有原子。</div><div class="card"><strong class="proved">PAID EQUATION</strong>z 满足保留 −2νΔb 源的正向抛物方程；全局能量与固定截止恒等式合法。</div><div class="card"><strong class="open">OPEN AMPLITUDE WORK</strong>混合压力虽有负范数消失和普通时间 little-o，仍没有随幅度 R 一致的压力功控制。</div></div><p>全部 BU 结论都以同一光滑周期 NS 原解、正原子、共同饱和伴随、常配对和终端定位为条件；没有插入任意新漂移或强初迹。</p>"""),
    ("02 / BU.1–BU.4", "目标点没有残差能量原子", """<p>令 b(ρ)=−u(T−ρ)、w(ρ)=A(T−ρ)、c=√m、z=b+cw。常配对 ⟨b,w⟩=−c 与伴随能量向 δ_a 定位，使交叉测度可对全部连续测试取极限；这不是把两个弱极限直接相乘。</p><div class="equation">|z(ρ)|²dx ⇀* μ_res := μ_*−mδ_a ≥ 0,   μ_res({a})=0.   (BU.4)</div><p>结论只删除目标点 a 的残差原子。背景能量和其他点的原子可以保留，不能据此声称 z 全局强 L² 收敛到零。</p>"""),
    ("03 / BU.5–BU.6", "正向残差方程保留已付源", """<p>反向原解 b 与共同伴随 w 的黏性符号相反。线性组合后，z 可写成正扩散方程，但必须保留由原解梯度能量支付的源 −2νΔb∈L²H⁻¹。</p><div class="equation">zρ+(b·∇)z+∇q = νΔz−2νΔb,   q=p_b+cπ=Π(z,z)−cΠ(z,w).   (BU.5–BU.6)</div><p><strong>DIRECT DERIVATION</strong>压力采用整个周期胞的统一零均值规范。π=r−cp_w、r=Π(z,w) 的精确分解不会让自压力或混合压力自动消失。</p>"""),
    ("04 / BU.7–BU.13", "全局能量与固定截止端点已付清", """<p>相反扩散在交叉能量中抵消，带源正向形式给出合法的全局估计。初始的 ||z(0)||² 只表示 μ_res 的总质量，不定义达到该范数的强 L² 初始场。</p><div class="equation">½||z(t)||²+ν∫ₛᵗ||∇z||² = ½||z(s)||²+2ν∫ₛᵗ∇b:∇z.   (BU.8)</div><p>完整周期压力、输运、截止边界与源项全部保留。先固定空间半径、再缩短时间、最后令半径趋零，可得到目标球内未缩放的残差能量与梯度对角小量；没有临界 r⁻¹ 归一化、抛物速率或联合缩球结论。</p>"""),
    ("05 / BU.14–BU.15", "混合张量在完整时间变量上消失", """<p>残差测度在 a 无原子，而 w 的能量集中于 a。近远区域的 Cauchy–Schwarz 分解因此给出全时间极限，而不是子列或有符号平均：</p><div class="equation">||z(ρ)⊗w(ρ)||₁ → 0,   ||r(ρ)||_{H^{-s}}+||∇r(ρ)||_{H^{-s-1}} ≤ C_s||z⊗w||₁,   s&gt;3/2.   (BU.14–BU.15)</div><p>Fourier 系数估计支付固定光滑测试和负 Sobolev 小量；没有使用错误的 Riesz 强 L¹ 有界性。</p>"""),
    ("06 / BU.16–BU.17", "完整周期混合压力获得普通时间 little-o", """<p>只在压力算子的输入张量中用光滑辅助截止作代数分割，然后仍对整个周期胞应用同一 CZ 算子。算子常数与半径无关，也没有截止导数。</p><div class="equation">||r||_{L²(0,δ;L³ᐟ²)} ≤ C[ε_r(δ)h_w(δ)+ω_r(δ)h_z(δ)] = o(h_w(δ)+h_z(δ)).   (BU.16–BU.17)</div><p>被估比值本身不含辅助半径，所以固定半径取 δ→0 上极限，再令半径趋零，得到普通时间 little-o。这里没有临界衰减率、联合缩放或对 q 的纯残差压力控制。</p>"""),
    ("07 / BU.18–BU.20", "固定幅度合法，不等于幅度一致可积", """<p>BT 的压力功精确分成自压力与混合压力。对每个固定 R，混合项由 CR h_w h_z 控制；这个显式 R 因子不能在 R→∞ 时忽略。</p><div class="equation">Q_R = c∫Dβ_R(w)·∇p_w − ∫Dβ_R(w)·∇r,   lim_{R→∞}∫₀^δQ_R dρ=1/2.   (BU.18–BU.20)</div><p><strong>OPEN</strong>现有 L³ᐟ² 压力不能直接与仅有 L² 控制的凸测试导数配对，负范数也没有支付随 R,w 变化的测试。半单位边界仍不能分别归给自压力或混合压力。</p>"""),
    ("08 / 来源、证据与下一步", "有符号幅度压力功审计尚未开始", """<p>科学源提交 9708a86053d507a51b0c3843211774ede954efea；冻结提交 6da74e5e62930a5b4b44d09962915f7e4e551541。六份本轮文件、143 份依赖和一份冻结 manifest 由 SHA-256 绑定；三份文本源、20 个 BU 标签、20 项独立有理复算及 4 项有限负对照通过。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_same_parent_residual_20260906.md">BU 残差正文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_same_parent_residual_reading_20260906.md">来源与去重边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_same_parent_residual_report_20260906.md">阶段报告</a></p><p>下一研发动作只检查精确分解下有符号、时间积分后的混合压力幅度功，能否得到不随 R 增长的控制；即使混合项被控制，自压力仍须单独分析。该审计尚未开始。</p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap；不分发第三方 PDF。原子存在或排除、强 L² 初迹、G、R.216–R.217、一般正则性与新颖性仍 OPEN。NOT CLAY。</strong></p>"""),
]

EN_SECTIONS = [
    ("01 / Result map", "The same parent supplies genuine residual structure but does not close the amplitude endpoint", """<div class="grid"><div class="card"><strong class="proved">CONDITIONAL RESULT</strong>Under BP's positive-terminal-energy-atom condition, the terminal residual measure of z=b+√m w is μ_*−mδ_a and has no atom at the target point a.</div><div class="card"><strong class="proved">PAID EQUATION</strong>z obeys a forward parabolic equation retaining the source −2νΔb. Global energy and fixed-cutoff identities are legitimate.</div><div class="card"><strong class="open">OPEN AMPLITUDE WORK</strong>Although mixed pressure vanishes in negative norms and has ordinary-time little-o, no pressure-work control uniform in amplitude R is proved.</div></div><p>Every BU conclusion is conditional on the same smooth periodic NS parent, positive atom, common saturated adjoint, constant pairing, and terminal localization. No arbitrary new drift or strong initial trace is inserted.</p>"""),
    ("02 / BU.1–BU.4", "The residual energy has no atom at the target point", """<p>Set b(ρ)=−u(T−ρ), w(ρ)=A(T−ρ), c=√m, and z=b+cw. The constant pairing ⟨b,w⟩=−c and concentration of the adjoint energy at δ_a let the cross measure converge against every continuous test. This is not multiplication of two weak limits.</p><div class="equation">|z(ρ)|²dx ⇀* μ_res := μ_*−mδ_a ≥ 0,   μ_res({a})=0.   (BU.4)</div><p>The conclusion removes only the residual atom at the target a. Background energy and atoms elsewhere may remain, so it does not imply global strong L² convergence of z to zero.</p>"""),
    ("03 / BU.5–BU.6", "The forward residual equation retains its paid source", """<p>The reversed parent b and common adjoint w have opposite viscosity signs. Their linear combination can be written as a positive-diffusion equation, but it must retain the source −2νΔb∈L²H⁻¹ paid by the parent gradient energy.</p><div class="equation">zρ+(b·∇)z+∇q = νΔz−2νΔb,   q=p_b+cπ=Π(z,z)−cΠ(z,w).   (BU.5–BU.6)</div><p><strong>DIRECT DERIVATION</strong>Pressure uses one zero-mean normalization on the full periodic cell. The exact split π=r−cp_w with r=Π(z,w) makes neither self-pressure nor mixed pressure disappear automatically.</p>"""),
    ("04 / BU.7–BU.13", "Global energy and fixed-cutoff endpoints are paid", """<p>Opposite diffusion cancels in the cross energy, while the forced forward formulation gives a legitimate global estimate. The initial symbol ||z(0)||² denotes only the total mass of μ_res; it does not define a strongly attained L² initial field.</p><div class="equation">½||z(t)||²+ν∫ₛᵗ||∇z||² = ½||z(s)||²+2ν∫ₛᵗ∇b:∇z.   (BU.8)</div><p>Full-periodic pressure, transport, cutoff-boundary, and source terms are all retained. Fixing the spatial radius, shortening time, and then sending the radius to zero gives unscaled diagonal residual-energy and gradient smallness in the target ball. It gives no critical r⁻¹ normalization, parabolic rate, or jointly shrinking scale.</p>"""),
    ("05 / BU.14–BU.15", "The mixed tensor vanishes along the full time variable", """<p>The residual measure has no atom at a while the w energy concentrates there. A near/far Cauchy–Schwarz decomposition therefore gives a full-time limit, not merely a subsequence or signed average:</p><div class="equation">||z(ρ)⊗w(ρ)||₁ → 0,   ||r(ρ)||_{H^{-s}}+||∇r(ρ)||_{H^{-s-1}} ≤ C_s||z⊗w||₁,   s&gt;3/2.   (BU.14–BU.15)</div><p>Fourier coefficient bounds pay for fixed smooth tests and negative-Sobolev smallness. No false strong L¹ boundedness of Riesz transforms is used.</p>"""),
    ("06 / BU.16–BU.17", "Full-periodic mixed pressure has ordinary-time little-o", """<p>A smooth auxiliary cutoff is used only to split the input tensor algebraically; the same CZ operator is then applied on the entire periodic cell. Its constant is radius independent, and no cutoff derivative appears.</p><div class="equation">||r||_{L²(0,δ;L³ᐟ²)} ≤ C[ε_r(δ)h_w(δ)+ω_r(δ)h_z(δ)] = o(h_w(δ)+h_z(δ)).   (BU.16–BU.17)</div><p>The estimated ratio itself contains no auxiliary radius. Fixing a radius for the δ→0 limsup and then sending the radius to zero gives ordinary-time little-o. No critical decay rate, joint shrinking scale, or control of q's pure residual pressure follows.</p>"""),
    ("07 / BU.18–BU.20", "Fixed amplitude is legitimate but not amplitude-uniform integrability", """<p>BT's pressure work splits exactly into self-pressure and mixed pressure. For each fixed R, the mixed term is bounded by CR h_w h_z. The explicit R factor cannot be discarded when R→∞.</p><div class="equation">Q_R = c∫Dβ_R(w)·∇p_w − ∫Dβ_R(w)·∇r,   lim_{R→∞}∫₀^δQ_R dρ=1/2.   (BU.18–BU.20)</div><p><strong>OPEN</strong>The existing L³ᐟ² pressure cannot be paired directly with a convex-test derivative controlled only in L², and the negative norm does not pay for a test varying with R,w. The half-unit boundary contribution still cannot be assigned separately to self-pressure or mixed pressure.</p>"""),
    ("08 / Sources, evidence, and next step", "The signed amplitude-pressure-work audit has not started", """<p>Scientific source commit: 9708a86053d507a51b0c3843211774ede954efea; freeze commit: 6da74e5e62930a5b4b44d09962915f7e4e551541. Six current files, 143 dependencies, and one frozen manifest are SHA-256-bound. Three text sources, 20 BU labels, 20 independent rational recomputations, and four limited negative controls pass.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_same_parent_residual_20260906.md">BU residual source</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_same_parent_residual_reading_20260906.md">source and deduplication boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_same_parent_residual_report_20260906.md">stage report</a></p><p>The next research action asks only whether signed time-integrated mixed-pressure amplitude work in the exact decomposition admits control independent of R. Even if the mixed term closes, self-pressure still requires separate analysis. That audit has not started.</p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap and redistributes no third-party PDF. Atom existence or exclusion, strong L² trace, G, R.216–R.217, general regularity, and novelty remain OPEN. NOT CLAY.</strong></p>"""),
]


def main_block(lang: str, sections: list[tuple[str, str, str]]) -> str:
    if lang == "zh":
        kicker = "CB.22 · 独立 Clay-B 方法笔记 · 2026-09-06"
        title = "CB.22｜同一原解的对齐残差：能量、混合压力与终端边界"
        dek = "正终端能量原子的条件分支中，对齐残差在目标点没有能量原子，并满足保留已付源的正向方程；完整周期混合压力具有普通时间 little-o，但幅度一致压力功仍未支付。"
        footer = "独立 HTML 研究笔记"
    else:
        kicker = "CB.22 · Independent Clay-B methods note · 2026-09-06"
        title = "CB.22 | Same-parent alignment residual: energy, mixed pressure, and terminal boundary"
        dek = "On the conditional positive-terminal-energy-atom branch, the alignment residual has no energy atom at the target point and obeys a forward equation retaining its paid source. Full-periodic mixed pressure has ordinary-time little-o, but amplitude-uniform pressure work remains unpaid."
        footer = "Independent HTML research note"
    body = "".join(f'<section><div class="section-no">{n}</div><h2>{h}</h2>{c}</section>' for n, h, c in sections)
    return f'''  <main data-language="{lang}">
    <article><header class="hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="dek">{dek}</p><div class="meta"><span>PROVED</span><span>CONDITIONAL</span><span>DIRECT DERIVATION</span><span>PAID SOURCE</span><span>LITERATURE</span><span>FINITE CHECKS ONLY</span><span>OPEN · NOT CLAY</span></div></header>{body}</article>
    <footer class="footer">CB.22 · {footer} · {DISPLAY_ID} · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-same-parent-residual" aria-labelledby="clay-b-same-parent-residual-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.22 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · SAME-PARENT RESIDUAL</p><h2 class="route-map-title" id="clay-b-same-parent-residual-title">CB.22｜同一原解的对齐残差：能量、混合压力与终端边界</h2><p class="route-map-intro">正原子条件下，对齐残差测度在目标点无原子，正向残差方程保留 −2νΔb 源；混合张量全时间消失，完整周期混合压力得到普通时间 little-o。幅度一致压力功、自压力、强 L² 初迹与原子排除仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 同一原解残差笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-same-parent-residual-20260906.html">阅读最新 CB.22 残差笔记 →</a><a href="/literature-review.html#clay-b-same-parent-residual-boundary">查看来源与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 同一原解残差结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>目标点无残差原子与已付源方程</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>混合压力普通时间 little-o</span><span><i class="route-legend-mark current" aria-hidden="true"></i>幅度一致压力功与自压力 OPEN · NOT CLAY</span></div></div></section>'''

CB_ROWS = '''          <div class="tree-row clay-b-convex-pressure-trace-row">
            <article class="tree-node"><div class="tree-node-head"><span class="route-range">CB.21 · 2026-09-06 · BT CONVEX PRESSURE TRACE</span><span class="tree-state">独立路线章节</span></div><h3>CB.21｜有界凸压力测试：次二次强初迹与幅度端点</h3><p>BT 用有限指数 Leray 投影得到 ∇π∈L¹_tL³ᐟ²_x，并为每个固定有界凸测试建立含弱初端点的精确恒等式。特定 β_R 推出 ||w(t)||₁≤κ(t)，从而所有 1≤q&lt;2 都有强零初迹，但不包括 q=2。</p><p>在额外正能量原子条件下，幅度 R→∞ 的压力通量仍对 C¹ 时间测试趋于 δ₀/2；低幅度能量估计与普遍消压局部测试分类都是必要校准，不排除原子，也不是一般正则性结论。</p><p class="tree-path"><a href="/notes/clay-b-convex-pressure-trace-20260906.html">阅读 CB.21 HTML</a> · <a href="/literature-review.html#clay-b-convex-pressure-trace-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right kept"><span class="tree-state">SAME-PARENT RESIDUAL COMPLETED</span><h3>同一原解残差核算已进入 CB.22</h3><p>BU 已把目标点残差测度、保留源的正向方程和完整周期混合压力小量写成正式结论；结果见下一个路线节点。</p></aside>
          </div>

          <div class="tree-row clay-b-same-parent-residual-row">
            <article class="tree-node current"><div class="tree-node-head"><span class="route-range">CB.22 · 2026-09-06 · BU SAME-PARENT RESIDUAL</span><span class="tree-state current">当前路线边界</span></div><h3>CB.22｜同一原解的对齐残差：能量、混合压力与终端边界</h3><p>在 BP 正原子条件下，z=b+√m w 的终端能量测度 μ_res=μ_*−mδ_a 在目标点 a 无原子；z 满足保留 −2νΔb 源的正向抛物方程。固定截止端点合法，目标球内只得到未缩放对角小量。</p><p>混合张量 z⊗w 在全时间变量上趋零；完整周期混合压力 r=Π(z,w) 在负 Sobolev 范数消失，并有相对 h_w+h_z 的普通时间 little-o。没有临界速率、幅度一致压力功或对 BT 半单位端点的分量归属。</p><p class="tree-path"><a href="/notes/clay-b-same-parent-residual-20260906.html">阅读 CB.22 HTML</a> · <a href="/literature-review.html#clay-b-same-parent-residual-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发动作：有符号幅度压力功</h3><p>只检查混合压力的有符号时间积分能否得到不随 R 增长的控制；即使混合项关闭，自压力仍须单独分析。该审计尚未开始。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.23 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.22</h3><p>CB.23 只是下一章占位，不是已完成研究。幅度一致混合压力功、自压力端点、原子存在或排除、强 L² 初迹、G、R.216–R.217、一般正则性与 Clay 均未关闭。</p></article></div>'''

LITERATURE_BLOCK = '''<h3 id="clay-b-same-parent-residual-boundary">CB.22 · Clay-B 同一原解残差的来源和主张边界</h3><p>本轮根任务完整重读已冻结 BP 正原子共同伴随章节与 BT §§1–5，并只重新打开 <a href="https://arxiv.org/abs/2608.04138v1">Huang 2608.04138v1</a> 的元数据和摘要；没有重新读取该 PDF 或导入新的外部定理。周期有限指数 Leray/CZ 与 Sobolev 工具沿用 BP/BL 已核查接口。团队成员的有界历史比较只作内部去重，不扩大为根任务亲读范围、文献穷尽或新颖性结论。</p><div class="boundary"><strong>CB.22 · ClayB-SameParentResidual-20260906 公开边界</strong><p>CONDITIONAL：全部 BU 结论假设 BP 的同一光滑无外力周期 NS 原解、目标点正终端原子 mδ_a、共同饱和伴随、常配对及终端定位。RESIDUAL MEASURE：z=b+√m w 的连续测试终端测度是 μ_res=μ_*−mδ_a≥0 且 μ_res({a})=0；交叉测度来自常配对和定位，不是弱极限乘法，背景能量及其他原子可以保留。PAID FORCED EQUATION：相反黏性给 zρ+b·∇z+∇q=νΔz−2νΔb；源属于 L²H⁻¹，全部压力、截止和源梯度项保留。固定截止端点合法，初始残差能量表示终端测度而非强 L² 迹；只得到未缩放对角局部小量。MIXED PRESSURE：||z⊗w||₁ 在完整时间变量上趋零，r=Π(z,w) 在 H^{-s}、s&gt;3/2 消失。光滑辅助截止只分割输入张量，完整周期 CZ 常数与半径无关且无截止导数，因比值不含半径，得到 ||r||_{L²L³ᐟ²}=o(h_w+h_z) 的普通 δ→0 little-o；没有时间速率或联合缩球尺度。AMPLITUDE GAP：π=r−√mΠ(w,w)；固定 R 的混合功上界仍含 R，L³ᐟ² 压力不能直接和仅有 L² 的凸测试导数配对，负范数也不支付随 R,w 变化的测试。BT 的 1/2 边界不能分别归给自压力或混合压力。FINITE CHECKS ONLY：三份文本源、20 个 BU 标签、149/149 文件绑定、20 项有理复算和 4 项有限负对照不替代 PDE 证明。原子存在或排除、强 L² 初迹、幅度一致压力功、G、R.216–R.217、一般正则性与新颖性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。<a href="/notes/clay-b-same-parent-residual-20260906.html">阅读完整 CB.22 笔记</a>。</p></div>
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
    value = (ROOT / "public/notes/clay-b-convex-pressure-trace-20260906.html").read_text(encoding="utf-8")
    value = set_version(value)
    value = re.sub(r'<title>.*?</title>', '<title>同一原解的对齐残差：能量、混合压力与终端边界</title>', value, count=1)
    value = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 同一原解对齐残差、带源能量和完整周期混合压力的双语方法笔记。">', value, count=1)
    value = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', value, count=1)
    value = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.22 · {DISPLAY_ID}</strong></header>', value, count=1)
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
    value = value.replace("CB.1–CB.21", "CB.1–CB.22")
    value = value.replace("bounded convex pressure / subquadratic trace", "same-parent residual / mixed-pressure smallness", 1)
    old_focus = "Clay-B 已完成固定有界凸压力测试：能量类给出压力梯度时间 L¹ 可积性和所有 1≤q<2 的强零初迹；但额外正原子下撤去幅度截断仍重现 δ₀/2 的端点成本，强 L² 与原子排除没有闭合。下一步只检查同一原解的对齐残差。"
    new_focus = "Clay-B 已把同一原解的终端对齐展开为残差测度、带源正向方程和完整周期混合压力：目标点无残差原子，混合张量全时间消失，且混合压力相对能量梯度预算有普通时间 little-o；但幅度一致压力功、自压力端点、强 L² 与原子排除仍未闭合。下一步只检查有符号幅度压力功。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    value, count = re.subn(r'          <div class="tree-row clay-b-convex-pressure-trace-row">[\s\S]*?<div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB_ROWS + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if count != 1:
        raise RuntimeError("Clay-B tail drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-same-parent-residual-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 22
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.22"
    payload["nextIndependentChapter"] = "CB.23"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note",
            "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.22",
            "sourceCommit": "9708a86053d507a51b0c3843211774ede954efea",
            "baseCommit": "281d36f1d55254dc13b0bc5c3b5b80ccf94467a0",
            "handoffCommit": "6da74e5e62930a5b4b44d09962915f7e4e551541",
            "logicalPredecessor": "ClayB-ConvexPressureTrace-20260906",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False,
            "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-same-parent-residual-20260906-gate.test.mjs",
            "publicationTest": "tests/clay-b-same-parent-residual-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-same-parent-residual-20260906-translations.mjs",
            "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE",
            "simulationRequired": False, "recapRequired": False, "advancesCanonicalR0Series": False,
            "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "CONDITIONAL_ON_BP_SAME_PARENT_POSITIVE_ATOM_RESIDUAL_MEASURE_HAS_NO_ATOM_AT_TARGET_ONLY_FORWARD_RESIDUAL_EQUATION_RETAINS_PAID_MINUS_TWO_NU_LAPLACIAN_B_SOURCE_FULL_PERIODIC_MIXED_TENSOR_AND_NEGATIVE_NORM_VANISHING_ORDINARY_TIME_L2L3_OVER_2_LITTLE_O_WITHOUT_RATE_OR_JOINT_SCALE_FIXED_AMPLITUDE_WORK_NOT_UNIFORM_IN_R_SELF_PRESSURE_AND_HALF_UNIT_ENDPOINT_UNASSIGNED_ATOM_EXCLUSION_STRONG_L2_GENERAL_REGULARITY_AND_NOVELTY_OPEN_NOT_CLAY",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def handoff_bytes() -> bytes:
    ledger = json.loads((ROOT / "research/clay_b_same_parent_residual_frozen_ledger_20260906.json").read_text(encoding="utf-8"))
    qa = json.loads((ROOT / "release/qa/clay-b-same-parent-residual-20260906.json").read_text(encoding="utf-8"))
    artifacts = [{"path": row["path"], "sha256": row["sha256"], "role": "frozen-scientific-source" if row["role"] == "scientific-source" else "frozen-dependency", "commit": row["commit"]} for row in ledger["files"]]
    artifacts += [{"path": row["path"], "sha256": row["sha256"], "role": "frozen-release-manifest", "commit": row["commit"]} for row in ledger["handoffEnvelope"]]
    outputs = [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html", "public/notes/index.html", "public/site-version.json", "research/release-manifest.json", "VERSION"]
    support = ["research/clay_b_same_parent_residual_frozen_ledger_20260906.json", "release/handoffs/clay-b-same-parent-residual-20260906.json", "release/qa/clay-b-same-parent-residual-20260906.json", "scripts/import_clay_b_same_parent_residual_20260906_frozen.py", "scripts/generate_clay_b_same_parent_residual_20260906_release.py", "scripts/generate_note_index.py", "scripts/add-clay-b-same-parent-residual-20260906-translations.mjs", "tests/clay-b-same-parent-residual-20260906-gate.test.mjs", "tests/clay-b-same-parent-residual-20260906-release.test.mjs", "tests/release-publication-invariant.test.mjs", "translations/en.json", "public/i18n-en.js"]
    managed = list(dict.fromkeys(outputs + [row["path"] for row in artifacts] + support))
    payload = {
        "schemaVersion": "research-publication-handoff-v1", "releaseId": DISPLAY_ID,
        "frozenCommit": "6da74e5e62930a5b4b44d09962915f7e4e551541", "sourceRepository": "navier-stokes-r074m",
        "translationRoute": "LOCAL_DIRECT_NO_DGX", "artifacts": artifacts,
        "artifactPolicy": {"readerPdf": "OMIT_NEW", "scientificFigure": "NOT_REQUIRED"},
        "claimBoundary": {"requiredLabels": ["PROVED", "CONDITIONAL", "DIRECT DERIVATION", "PAID SOURCE", "LITERATURE", "FINITE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"], "publicFiles": [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html"]},
        "recap": {"mode": "PRESERVE", "latestRecapRelease": "r076i", "preservedArtifacts": [{"path": "public/recap-r0-61-r0-76i.html", "sha256": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9"}, {"path": "public/recap-r0-61-r0-76i.pdf", "sha256": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98"}]},
        "stages": {
            "generate": {"runner": "python-local", "script": "scripts/generate_clay_b_same_parent_residual_20260906_release.py", "inputs": [row["path"] for row in artifacts] + ["research/clay_b_same_parent_residual_frozen_ledger_20260906.json"], "outputs": outputs},
            "translate": {"runner": "node-local", "script": "scripts/add-clay-b-same-parent-residual-20260906-translations.mjs", "inputs": ["public/research-review.html", "public/literature-review.html", "public/notes/index.html", "translations/en.json"], "outputs": ["translations/en.json", "public/i18n-en.js"]},
        },
        "publication": {"expectedCommit": None, "siteBaseUrl": "https://kasifa.github.io", "repository": "Kasifa/Kasifa.github.io", "workflow": "pages.yml", "remote": "origin", "targetBranch": "main", "commitMessage": "Publish ClayB SameParentResidual CB.22 HTML note", "managedPaths": managed, "expectedLive": qa["online"]["expectedLive"], "expectedAbsent": qa["online"]["expectedAbsent"], "siteVersionExpectations": qa["online"]["siteVersionExpectations"]},
        "visualQa": {"evidencePath": qa["browser"]["evidencePath"], "configPath": "release/qa/clay-b-same-parent-residual-20260906.json", "requiredChecks": [f"{target['id']}-{scenario['id']}" for target in qa["browser"]["targets"] for scenario in qa["browser"]["scenarios"]]},
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.22", DISPLAY_ID, "同一原解的对齐残差：能量、混合压力与终端边界", "Same-parent alignment residual: energy, mixed pressure, and terminal boundary", "PROVED", "CONDITIONAL", "DIRECT DERIVATION", "PAID SOURCE", "LITERATURE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.22", "Clay-B 独立路线停在 CB.22", "CB.23 · NEXT", 'class="tree-row clay-b-same-parent-residual-row"', f"/notes/{SLUG}.html", "单独的虚线泳道"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb22 = home.index('class="tree-row clay-b-same-parent-residual-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb22)
    if not (r0_start < r0_boundary < divider < clay_start < cb22 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-same-parent-residual-boundary"' not in literature or "CB.22 · ClayB-SameParentResidual-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.22 · {DISPLAY_ID}" not in index or "22 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.22" or site.get("nextIndependentChapter") != "CB.23":
        raise RuntimeError("version or chapter metadata drift")
    if manifest.get("latestCompletedRelease") != "r076l" or site.get("latestRelease") != "R0.76L":
        raise RuntimeError("canonical R0 endpoint drift")
    expected = handoff_bytes()
    path = ROOT / "release/handoffs/clay-b-same-parent-residual-20260906.json"
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
    (ROOT / "release/handoffs/clay-b-same-parent-residual-20260906.json").write_bytes(handoff_bytes())

validate()
print(json.dumps({"schemaVersion": "clay-b-same-parent-residual-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.22", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
