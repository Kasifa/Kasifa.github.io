#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB SignedMixedPressure CB.23 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.67"
SLUG = "clay-b-signed-mixed-pressure-20260907"
DISPLAY_ID = "ClayB-SignedMixedPressure-20260907"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_SECTIONS = [
    ("01 / 结果地图", "同父正原子分支上的条件性方法结果", """<div class="grid"><div class="card"><strong class="proved">PROVED IN STATED SCOPE</strong>全周期投影把混合压力功改写为实际输运配对，并给出不显含截断幅度 R 的逐时上界。</div><div class="card"><strong class="open">TWO UNPAID INTERFACES</strong>加权时间成本 W_z 与混合压力平方 r∈L² 两条充分接口彼此不同，当前都未支付。</div><div class="card"><strong class="open">SIGNED PRIMITIVE ONLY</strong>联合截断只证明联合压力原函数一致趋零，不是 L¹、总变差或一致可积性结论。</div></div><p>全部 BV 结论都保留 BP/BU 的同一光滑无外力周期 NS 原解、额外正终端原子、共同饱和伴随及定位条件；不构造或排除原子。</p>"""),
    ("02 / BV.1–BV.5", "不显含幅度的投影上界", """<p>令 b=−u(T−ρ)、w=A(T−ρ)、c=√m、z=b+cw，r=Π(z,w)，P 为全周期 Leray 投影、Q=I−P。Q 消掉常数模态；径向测试的输运项在整个周期胞上消去。</p><div class="equation">M_R = ∫Qg_R(w)·(z·∇)w = −∫Pg_R(w)·(z·∇)w.   (BV.2–BV.3)</div><p>由 J_R²≤J_R、零均值 Sobolev 与空间 Hölder 的 6,3,2 配对，得到</p><div class="equation">|M_R(ρ)| ≤ C||z(ρ)||₃||∇w(ρ)||₂ D_R(ρ)¹ᐟ² ≤ C||z(ρ)||₃||∇w(ρ)||₂².   (BV.5)</div><p><strong>DIRECT DERIVATION</strong>常数 C 与 R 无关。这是逐时估计，不等于右端已经具有可积时间主函数。</p>"""),
    ("03 / BV.6–BV.9", "加权时间成本是充分条件，但尚未支付", """<p>若额外取得</p><div class="equation">W_z(δ)=∫₀^δ ||z(ρ)||₃||∇w(ρ)||₂² dρ &lt; ∞,   (BV.6)</div><p>则空间 H¹ 收敛与支配收敛给 M_R→0 于 L¹(0,δ)。现有能量只给 ||z||₃∈L⁴ 与 ||∇w||₂²∈L¹，不能自动推出加权乘积可积。BV.8 的标量时间函数只展示 Hölder 缺口，不是 NS 或同父反例。</p><p>Young 吸收留下 ||z||₃²||∇w||₂² 的未付成本。即使 W_z 后来闭合，自压力仍承受 BT 的条件性半单位端点，不能宣布原子矛盾。</p>"""),
    ("04 / BV.10–BV.17", "联合截断给出合法但非强制性的累计恒等式", """<p>以同一幅度同时截断 z,w，联合 Hessian 的对角与混合块分别有 6、6、1 的统一界。相反黏性的两个交叉项精确抵消，但源 2νcΔw 产生的两项都必须保留。</p><div class="equation">V_R → −2νc||∇w||₂² in L¹,   F_R → ⟨z,w⟩=−2νcD_w in C([0,L]).   (BV.16–BV.17)</div><div class="equation">sup₀≤t≤L |∫₀ᵗ P_R dρ| → 0.   (BV.17)</div><p><strong>CONDITIONAL / SIGNED</strong>联合压力原函数只按有符号累计消失；不能升级为 ||P_R||L¹→0、总变差有界、一致可积或新的强制估计。</p>"""),
    ("05 / BV.18–BV.20", "三个余项和自压力都不能省略", """<p>联合压力完整展开为</p><div class="equation">P_R = T_R − cM_R + E_R^q + E_R^π.   (BV.18)</div><p>T_R、E_R^q、E_R^π 在几乎每个正时间分别趋零，却没有统一的可积时间主函数。因此联合原函数的极限不能单独抽出 M_R。交换 z,w 也不能靠重命名消去差异，因为两者的压力、黏性和源不同。</p><p>即使未来控制混合功 M_R，原来的自压力 S_R 及其条件性端点仍然保留。</p>"""),
    ("06 / BV.21–BV.23", "两个不同且未付的充分接口", """<p>同一配对还给出压力平方接口：</p><div class="equation">M_R=∫r div(g_R(w)−w),   ∇(g_R(w)−w)→0 in L².   (BV.21)</div><p>若额外有 r∈L²((0,δ)×Ω)，则时空 Cauchy–Schwarz 足以推出 ||M_R||L¹→0。当前插值只到 r∈L⁴ᐟ³_tL²_x，其对偶时间指数是 4，而现有导数只有 L²。</p><div class="equation">2νcD_w(ρ)=|⟨z(ρ),w(ρ)⟩|≤||z(ρ)⊗w(ρ)||₁→0.   (BV.23)</div><p>这个累计耗散约束不是残差权重相对耗散密度 dD_w 的可积性。W_z 有限与 r∈L² 是两条不同的充分条件：未证明必要、等价或由当前能量类推出。</p>"""),
    ("07 / 来源与审阅范围", "直接推导、有限原著核对与非作者审阅", """<p><strong>LITERATURE</strong>本轮完整读取冻结的 BU、BT；外部来源只核对 Berselli–Chiodaroli arXiv:1807.02667v3 的官方元数据与摘要，没有读取其 PDF 定理或证明，也没有导入外部能量等式。旧 Hardy/BMO 比较仅是团队范围核算，不构成穷尽检索、外部同行评审或新颖性结论。</p><p>非作者审阅完整覆盖 BV.1–BV.23 的投影、零模、联合 Hessian、黏性与源符号、端点、余项、时间插值及累计耗散边界。</p>"""),
    ("08 / 证据与下一步", "有限证书完成，源项与梯度能量审计尚未开始", """<p>科学源提交 cb5acbb4416ca2d6502e9b7d48d19f91a150f2a0；冻结提交 cf4f8a27bc1ddab92f857945b229a24fb05d5517。六份本轮文件、150 份依赖和一份冻结 manifest 由 SHA-256 绑定；三份文本源、23 个 BV 标签、25 项独立有理复算及 4 项有限负对照通过。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_signed_mixed_pressure_20260907.md">BV 正文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_signed_mixed_pressure_reading_20260907.md">来源与方法边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_signed_mixed_pressure_report_20260907.md">阶段报告</a></p><p>下一研发动作直接核对同一原解与残差方程的源项、梯度能量和交叉梯度演化，判断能否支付 W_z、压力平方接口或更弱的有符号混合功控制；该审计尚未开始。</p><p><strong>FINITE CHECKS ONLY：有限复算不证明 PDE 极限。无新读者 PDF、仿真、科学图、DGX 数据或累计 recap。原子存在或排除、G、R.216–R.217、一般三维正则性、文献新颖性与 Clay 均 OPEN。NOT CLAY。</strong></p>"""),
]


EN_SECTIONS = [
    ("01 / Result map", "A conditional method result on the same-parent positive-atom branch", """<div class="grid"><div class="card"><strong class="proved">PROVED IN STATED SCOPE</strong>Full-periodic projection rewrites mixed-pressure work as the actual transport pairing and gives a pointwise bound with no explicit truncation amplitude R.</div><div class="card"><strong class="open">TWO UNPAID INTERFACES</strong>The weighted-time cost W_z and mixed-pressure square r∈L² are distinct sufficient interfaces; neither is paid.</div><div class="card"><strong class="open">SIGNED PRIMITIVE ONLY</strong>Joint truncation proves uniform decay only of the joint-pressure primitive, not L¹, total variation, or uniform integrability.</div></div><p>Every BV statement retains BP/BU's same smooth unforced periodic NS parent, extra positive terminal atom, common saturated adjoint, and localization. No atom is constructed or excluded.</p>"""),
    ("02 / BV.1–BV.5", "An amplitude-independent projected bound", """<p>Set b=−u(T−ρ), w=A(T−ρ), c=√m, z=b+cw, and r=Π(z,w). Let P be the full-periodic Leray projection and Q=I−P. Q removes the constant mode, while radial testing cancels transport over the full periodic cell.</p><div class="equation">M_R = ∫Qg_R(w)·(z·∇)w = −∫Pg_R(w)·(z·∇)w.   (BV.2–BV.3)</div><div class="equation">|M_R(ρ)| ≤ C||z(ρ)||₃||∇w(ρ)||₂ D_R(ρ)¹ᐟ² ≤ C||z(ρ)||₃||∇w(ρ)||₂².   (BV.5)</div><p><strong>DIRECT DERIVATION</strong>The constant is independent of R. This is a pointwise-in-time estimate, not a paid integrable time majorant.</p>"""),
    ("03 / BV.6–BV.9", "The weighted-time cost is sufficient but unpaid", """<p>If one additionally proves</p><div class="equation">W_z(δ)=∫₀^δ ||z(ρ)||₃||∇w(ρ)||₂² dρ &lt; ∞,   (BV.6)</div><p>then spatial H¹ convergence and dominated convergence imply M_R→0 in L¹(0,δ). Current energy control gives only ||z||₃∈L⁴ and ||∇w||₂²∈L¹, which does not automatically make their weighted product integrable. The scalar functions in BV.8 exhibit only this Hölder gap; they are not NS or same-parent counterexamples.</p><p>Young absorption leaves another unpaid squared weighted cost. Even if W_z later closes, self-pressure still carries BT's conditional half-unit endpoint.</p>"""),
    ("04 / BV.10–BV.17", "Joint truncation yields a legitimate but non-coercive cumulative identity", """<p>Truncating z and w at the same amplitude gives uniform diagonal and mixed Hessian bounds 6,6,1. The opposite-viscosity cross terms cancel exactly, but both terms created by the source 2νcΔw remain.</p><div class="equation">V_R → −2νc||∇w||₂² in L¹,   F_R → ⟨z,w⟩=−2νcD_w in C([0,L]).   (BV.16–BV.17)</div><div class="equation">sup₀≤t≤L |∫₀ᵗ P_R dρ| → 0.   (BV.17)</div><p><strong>CONDITIONAL / SIGNED</strong>Only the signed primitive of joint pressure vanishes uniformly. This does not give ||P_R||L¹→0, bounded variation, uniform integrability, or a new coercive estimate.</p>"""),
    ("05 / BV.18–BV.20", "All three remainders and self-pressure must remain", """<p>The complete expansion is</p><div class="equation">P_R = T_R − cM_R + E_R^q + E_R^π.   (BV.18)</div><p>T_R, E_R^q, and E_R^π vanish at almost every positive time but lack a common integrable time majorant. The joint primitive limit therefore cannot isolate M_R. Swapping z and w does not erase their different pressure, viscosity, and source terms.</p><p>Even if mixed work M_R is later controlled, the original self-pressure S_R and its conditional endpoint remain.</p>"""),
    ("06 / BV.21–BV.23", "Two distinct and unpaid sufficient interfaces", """<p>The same pairing supplies a pressure-square interface:</p><div class="equation">M_R=∫r div(g_R(w)−w),   ∇(g_R(w)−w)→0 in L².   (BV.21)</div><p>An additional r∈L²((0,δ)×Ω) would make ||M_R||L¹→0 by spacetime Cauchy–Schwarz. Current interpolation reaches only r∈L⁴ᐟ³_tL²_x, whose dual time exponent is 4 rather than the available 2.</p><div class="equation">2νcD_w(ρ)=|⟨z(ρ),w(ρ)⟩|≤||z(ρ)⊗w(ρ)||₁→0.   (BV.23)</div><p>The cumulative dissipation constraint does not control residual weight against the dissipation density dD_w. Finiteness of W_z and r∈L² are distinct sufficient conditions, not proved necessary, equivalent, or consequences of the current energy class.</p>"""),
    ("07 / Sources and review scope", "Direct derivation, bounded primary-source check, and non-author review", """<p><strong>LITERATURE</strong>This round fully read the frozen BU and BT. External reading was limited to official metadata and abstract for Berselli–Chiodaroli arXiv:1807.02667v3; its PDF theorems and proofs were not read or imported. The prior Hardy/BMO comparison is team-bounded context, not exhaustive search, external peer review, or novelty certification.</p><p>Non-author review covered BV.1–BV.23: projection, zero mode, joint Hessian, viscosity and source signs, endpoints, remainders, time interpolation, and the cumulative-dissipation boundary.</p>"""),
    ("08 / Evidence and next step", "Finite certification is complete; the source/enstrophy audit has not started", """<p>Scientific source commit: cb5acbb4416ca2d6502e9b7d48d19f91a150f2a0; freeze commit: cf4f8a27bc1ddab92f857945b229a24fb05d5517. Six current files, 150 dependencies, and one frozen manifest are SHA-256-bound. Three text sources, 23 BV labels, 25 independent rational recomputations, and four limited negative controls pass.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_signed_mixed_pressure_20260907.md">BV source</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_signed_mixed_pressure_reading_20260907.md">source and method boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_signed_mixed_pressure_report_20260907.md">stage report</a></p><p>The next research action uses the same-parent and residual equations to audit source, gradient-energy, and cross-gradient evolution for W_z, the pressure-square interface, or a weaker signed-work control. That audit has not started.</p><p><strong>FINITE CHECKS ONLY: finite recomputation does not prove PDE limits. No new reader PDF, simulation, scientific figure, DGX data, or cumulative recap. Atom existence or exclusion, G, R.216–R.217, general 3D regularity, literature novelty, and Clay remain OPEN. NOT CLAY.</strong></p>"""),
]


def main_block(lang: str, sections: list[tuple[str, str, str]]) -> str:
    if lang == "zh":
        kicker = "CB.23 · 独立 Clay-B 方法笔记 · 2026-09-07"
        title = "CB.23｜有符号混合压力功：投影测试和联合截断"
        dek = "全周期投影给出不显含截断幅度的逐时混合压力功上界；联合截断控制有符号累计压力，却仍未支付时间积分、自压力或原子排除。"
        footer = "独立 HTML 研究笔记"
    else:
        kicker = "CB.23 · Independent Clay-B methods note · 2026-09-07"
        title = "CB.23 | Signed mixed-pressure work: projected tests and joint truncation"
        dek = "Full-periodic projection gives a pointwise mixed-pressure-work bound without explicit truncation amplitude. Joint truncation controls signed cumulative pressure, while time integration, self-pressure, and atom exclusion remain unpaid."
        footer = "Independent HTML research note"
    body = "".join(f'<section><div class="section-no">{n}</div><h2>{h}</h2>{c}</section>' for n, h, c in sections)
    return f'''  <main data-language="{lang}">
    <article><header class="hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="dek">{dek}</p><div class="meta"><span>PROVED</span><span>CONDITIONAL</span><span>DIRECT DERIVATION</span><span>LITERATURE</span><span>FINITE</span><span>FINITE CHECKS ONLY</span><span>OPEN · NOT CLAY</span></div></header>{body}</article>
    <footer class="footer">CB.23 · {footer} · {DISPLAY_ID} · 2026-09-07</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-signed-mixed-pressure" aria-labelledby="clay-b-signed-mixed-pressure-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.23 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-07 · SIGNED MIXED PRESSURE</p><h2 class="route-map-title" id="clay-b-signed-mixed-pressure-title">CB.23｜有符号混合压力功：投影测试和联合截断</h2><p class="route-map-intro">投影恒等式去掉逐时估计中显式的幅度成本；联合截断只控制有符号累计压力。加权时间成本与混合压力平方是两条不同且未付的充分接口，自压力与原子排除仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 有符号混合压力笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-signed-mixed-pressure-20260907.html">阅读最新 CB.23 笔记 →</a><a href="/literature-review.html#clay-b-signed-mixed-pressure-boundary">查看来源与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 有符号混合压力结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>逐时幅度一致投影上界</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>联合压力仅有符号累计消失</span><span><i class="route-legend-mark current" aria-hidden="true"></i>两条充分接口与自压力 OPEN · NOT CLAY</span></div></div></section>'''


CB_ROWS = '''          <div class="tree-row clay-b-convex-pressure-trace-row">
            <article class="tree-node"><div class="tree-node-head"><span class="route-range">CB.21 · 2026-09-06 · BT CONVEX PRESSURE TRACE</span><span class="tree-state">独立路线章节</span></div><h3>CB.21｜有界凸压力测试：次二次强初迹与幅度端点</h3><p>固定有界凸压力测试给出精确恒等式与所有 1≤q&lt;2 的强零初迹；额外正原子下，撤去幅度截断仍重现条件性半单位端点。</p><p class="tree-path"><a href="/notes/clay-b-convex-pressure-trace-20260906.html">阅读 CB.21 HTML</a> · <a href="/literature-review.html#clay-b-convex-pressure-trace-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
          </div>

          <div class="tree-row clay-b-same-parent-residual-row">
            <article class="tree-node"><div class="tree-node-head"><span class="route-range">CB.22 · 2026-09-06 · BU SAME-PARENT RESIDUAL</span><span class="tree-state">独立路线章节</span></div><h3>CB.22｜同一原解的对齐残差：能量、混合压力与终端边界</h3><p>正原子条件下，终端残差测度在目标点无原子，正向方程保留 −2νΔb 源；混合张量全时间消失且完整周期混合压力有普通时间 little-o。</p><p class="tree-path"><a href="/notes/clay-b-same-parent-residual-20260906.html">阅读 CB.22 HTML</a> · <a href="/literature-review.html#clay-b-same-parent-residual-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right kept"><span class="tree-state">SIGNED-WORK AUDIT COMPLETED</span><h3>有符号混合压力功核算已进入 CB.23</h3><p>BV 已给出逐时幅度一致投影界、合法的联合截断恒等式与两条明确但未付的充分接口；结果见下一个路线节点。</p></aside>
          </div>

          <div class="tree-row clay-b-signed-mixed-pressure-row">
            <article class="tree-node current"><div class="tree-node-head"><span class="route-range">CB.23 · 2026-09-07 · BV SIGNED MIXED PRESSURE</span><span class="tree-state current">当前路线边界</span></div><h3>CB.23｜有符号混合压力功：投影测试和联合截断</h3><p>全周期投影把混合压力功改写为输运配对，并给出 |M_R|≤C||z||₃||∇w||₂² 的逐时幅度一致上界；但相应加权时间成本 W_z 尚未由能量类支付。</p><p>同幅联合截断证明联合压力的有符号原函数一致趋零，而非 L¹、总变差或 UI。W_z 有限与 r∈L² 是两条不同的充分接口，均未闭合；三个余项和自压力必须保留。</p><p class="tree-path"><a href="/notes/clay-b-signed-mixed-pressure-20260907.html">阅读 CB.23 HTML</a> · <a href="/literature-review.html#clay-b-signed-mixed-pressure-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发动作：源项与梯度能量审计</h3><p>直接核对同一原解和残差方程能否支付 W_z、混合压力平方或更弱的有符号控制；不把累计耗散误作加权密度控制。该审计尚未开始。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.24 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.23</h3><p>CB.24 只是下一章占位，不是已完成研究。两条充分接口、自压力、原子存在或排除、G、R.216–R.217、一般正则性与 Clay 均未关闭。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-signed-mixed-pressure-boundary">CB.23 · Clay-B 有符号混合压力功的来源和主张边界</h3><p>本轮完整读取冻结的 BU 与 BT。外部读取仅限 <a href="https://arxiv.org/abs/1807.02667v3">Berselli–Chiodaroli arXiv:1807.02667v3</a> 的官方元数据和摘要，没有读取该 PDF 的定理或证明，也没有导入外部能量等式。旧 Hardy/BMO 比较只作团队范围核算，不扩大为穷尽检索、外部同行评审或新颖性结论。</p><div class="boundary"><strong>CB.23 · ClayB-SignedMixedPressure-20260907 公开边界</strong><p>CONDITIONAL：全部 BV 结论假设 BP/BU 的同一光滑无外力周期 NS 原解、额外正终端原子、共同饱和伴随与定位。PROVED IN STATED SCOPE：全周期投影与径向输运消去给 |M_R|≤C||z||₃||∇w||₂²，常数不依赖 R，但这只是逐时估计。SUFFICIENT INPUTS：W_z=∫||z||₃||∇w||₂²&lt;∞ 或 r∈L²_{t,x} 各自足以推出 M_R→0 于 L¹；两者不同、均未支付，也未证明必要或等价。JOINT TRUNCATION：同幅联合 Hessian 有统一界，相反黏性交叉项抵消但两个 −2νc 源项保留；只有 sup_t|∫₀ᵗP_R|→0，不能升级为 L¹、总变差或 UI。REMAINDERS：T_R、E_R^q、E_R^π 与自压力均不能省略；累计 2νcD_w≤||z⊗w||₁→0 不支付残差加权耗散密度。FINITE CHECKS ONLY：三份文本源、23 个 BV 标签、156/156 文件绑定、25 项有理复算和 4 项有限负对照不替代 PDE 证明。原子存在或排除、G、R.216–R.217、一般正则性与新颖性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。<a href="/notes/clay-b-signed-mixed-pressure-20260907.html">阅读完整 CB.23 笔记</a>。</p></div>
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
    value = (ROOT / "public/notes/clay-b-same-parent-residual-20260906.html").read_text(encoding="utf-8")
    value = set_version(value)
    value = re.sub(r'<title>.*?</title>', '<title>有符号混合压力功：投影测试和联合截断</title>', value, count=1)
    value = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 有符号混合压力功、投影测试、联合截断与未付充分接口的双语方法笔记。">', value, count=1)
    value = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', value, count=1)
    value = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.23 · {DISPLAY_ID}</strong></header>', value, count=1)
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
    value = value.replace("CB.1–CB.22", "CB.1–CB.23")
    value = value.replace("same-parent residual / mixed-pressure smallness", "signed mixed-pressure / joint truncation", 1)
    old_focus = "Clay-B 已把同一原解的终端对齐展开为残差测度、带源正向方程和完整周期混合压力：目标点无残差原子，混合张量全时间消失，且混合压力相对能量梯度预算有普通时间 little-o；但幅度一致压力功、自压力端点、强 L² 与原子排除仍未闭合。下一步只检查有符号幅度压力功。"
    new_focus = "Clay-B 已用全周期投影得到不显含截断幅度的逐时混合压力功上界，并以同幅联合截断证明联合压力的有符号原函数一致趋零；但加权时间成本与混合压力平方只是两条不同且未付的充分接口，三个余项、自压力与原子排除仍未闭合。下一步直接检查源项和梯度能量演化。"
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
    if 'id="clay-b-signed-mixed-pressure-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 23
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.23"
    payload["nextIndependentChapter"] = "CB.24"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note",
            "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.23",
            "sourceCommit": "cb5acbb4416ca2d6502e9b7d48d19f91a150f2a0",
            "baseCommit": "ecc17ffc95f3399f0cca1289f4b1787c1bdba3a1",
            "handoffCommit": "cf4f8a27bc1ddab92f857945b229a24fb05d5517",
            "logicalPredecessor": "ClayB-SameParentResidual-20260906",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False,
            "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-signed-mixed-pressure-20260907-gate.test.mjs",
            "publicationTest": "tests/clay-b-signed-mixed-pressure-20260907-release.test.mjs",
            "translationScript": "scripts/add-clay-b-signed-mixed-pressure-20260907-translations.mjs",
            "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE",
            "simulationRequired": False, "recapRequired": False, "advancesCanonicalR0Series": False,
            "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "CONDITIONAL_ON_BP_BU_SAME_PARENT_POSITIVE_ATOM_PROJECTED_POINTWISE_MIXED_PRESSURE_WORK_BOUND_IS_AMPLITUDE_INDEPENDENT_BUT_TIME_COST_UNPAID_WEIGHTED_COST_AND_MIXED_PRESSURE_L2_ARE_DISTINCT_SUFFICIENT_INTERFACES_NOT_NECESSARY_OR_EQUIVALENT_JOINT_PRESSURE_PRIMITIVE_ONLY_SIGNED_CUMULATIVE_NOT_L1_TV_OR_UI_ALL_THREE_REMAINDERS_AND_SELF_PRESSURE_RETAINED_ATOM_EXCLUSION_GENERAL_REGULARITY_AND_NOVELTY_OPEN_NOT_CLAY",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def handoff_bytes() -> bytes:
    ledger = json.loads((ROOT / "research/clay_b_signed_mixed_pressure_frozen_ledger_20260907.json").read_text(encoding="utf-8"))
    qa = json.loads((ROOT / "release/qa/clay-b-signed-mixed-pressure-20260907.json").read_text(encoding="utf-8"))
    artifacts = [{"path": row["path"], "sha256": row["sha256"], "role": "frozen-scientific-source" if row["role"] == "scientific-source" else "frozen-dependency", "commit": row["commit"]} for row in ledger["files"]]
    artifacts += [{"path": row["path"], "sha256": row["sha256"], "role": "frozen-release-manifest", "commit": row["commit"]} for row in ledger["handoffEnvelope"]]
    outputs = [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html", "public/notes/index.html", "public/site-version.json", "research/release-manifest.json", "VERSION"]
    support = ["research/clay_b_signed_mixed_pressure_frozen_ledger_20260907.json", "release/handoffs/clay-b-signed-mixed-pressure-20260907.json", "release/qa/clay-b-signed-mixed-pressure-20260907.json", "scripts/import_clay_b_signed_mixed_pressure_20260907_frozen.py", "scripts/generate_clay_b_signed_mixed_pressure_20260907_release.py", "scripts/generate_note_index.py", "scripts/add-clay-b-signed-mixed-pressure-20260907-translations.mjs", "tests/clay-b-signed-mixed-pressure-20260907-gate.test.mjs", "tests/clay-b-signed-mixed-pressure-20260907-release.test.mjs", "tests/release-publication-invariant.test.mjs", "translations/en.json", "public/i18n-en.js"]
    managed = list(dict.fromkeys(outputs + [row["path"] for row in artifacts] + support))
    payload = {
        "schemaVersion": "research-publication-handoff-v1", "releaseId": DISPLAY_ID,
        "frozenCommit": "cf4f8a27bc1ddab92f857945b229a24fb05d5517", "sourceRepository": "navier-stokes-r074m",
        "translationRoute": "LOCAL_DIRECT_NO_DGX", "artifacts": artifacts,
        "artifactPolicy": {"readerPdf": "OMIT_NEW", "scientificFigure": "NOT_REQUIRED"},
        "claimBoundary": {"requiredLabels": ["PROVED", "CONDITIONAL", "DIRECT DERIVATION", "LITERATURE", "FINITE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"], "publicFiles": [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html"]},
        "recap": {"mode": "PRESERVE", "latestRecapRelease": "r076i", "preservedArtifacts": [{"path": "public/recap-r0-61-r0-76i.html", "sha256": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9"}, {"path": "public/recap-r0-61-r0-76i.pdf", "sha256": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98"}]},
        "stages": {
            "generate": {"runner": "python-local", "script": "scripts/generate_clay_b_signed_mixed_pressure_20260907_release.py", "inputs": [row["path"] for row in artifacts] + ["research/clay_b_signed_mixed_pressure_frozen_ledger_20260907.json"], "outputs": outputs},
            "translate": {"runner": "node-local", "script": "scripts/add-clay-b-signed-mixed-pressure-20260907-translations.mjs", "inputs": ["public/research-review.html", "public/literature-review.html", "public/notes/index.html", "translations/en.json"], "outputs": ["translations/en.json", "public/i18n-en.js"]},
        },
        "publication": {"expectedCommit": None, "siteBaseUrl": "https://kasifa.github.io", "repository": "Kasifa/Kasifa.github.io", "workflow": "pages.yml", "remote": "origin", "targetBranch": "main", "commitMessage": "Publish ClayB SignedMixedPressure CB.23 HTML note", "managedPaths": managed, "expectedLive": qa["online"]["expectedLive"], "expectedAbsent": qa["online"]["expectedAbsent"], "siteVersionExpectations": qa["online"]["siteVersionExpectations"]},
        "visualQa": {"evidencePath": qa["browser"]["evidencePath"], "configPath": "release/qa/clay-b-signed-mixed-pressure-20260907.json", "requiredChecks": [f"{target['id']}-{scenario['id']}" for target in qa["browser"]["targets"] for scenario in qa["browser"]["scenarios"]]},
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.23", DISPLAY_ID, "有符号混合压力功：投影测试和联合截断", "Signed mixed-pressure work: projected tests and joint truncation", "PROVED", "CONDITIONAL", "DIRECT DERIVATION", "LITERATURE", "FINITE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.23", "Clay-B 独立路线停在 CB.23", "CB.24 · NEXT", 'class="tree-row clay-b-signed-mixed-pressure-row"', f"/notes/{SLUG}.html", "单独的虚线泳道"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb23 = home.index('class="tree-row clay-b-signed-mixed-pressure-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb23)
    if not (r0_start < r0_boundary < divider < clay_start < cb23 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-signed-mixed-pressure-boundary"' not in literature or "CB.23 · ClayB-SignedMixedPressure-20260907 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.23 · {DISPLAY_ID}" not in index or "23 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.23" or site.get("nextIndependentChapter") != "CB.24":
        raise RuntimeError("version or chapter metadata drift")
    if manifest.get("latestCompletedRelease") != "r076l" or site.get("latestRelease") != "R0.76L":
        raise RuntimeError("canonical R0 endpoint drift")
    path = ROOT / "release/handoffs/clay-b-signed-mixed-pressure-20260907.json"
    if not path.is_file() or path.read_bytes() != handoff_bytes():
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
    (ROOT / "release/handoffs/clay-b-signed-mixed-pressure-20260907.json").write_bytes(handoff_bytes())

validate()
print(json.dumps({"schemaVersion": "clay-b-signed-mixed-pressure-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.23", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
