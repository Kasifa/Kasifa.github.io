#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB SourceEnstrophy CB.24 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.68"
SLUG = "clay-b-source-enstrophy-20260907"
DISPLAY_ID = "ClayB-SourceEnstrophy-20260907"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]

ZH_SECTIONS = [
    ("01 / 结果地图", "本节关闭一种方法误判，不关闭 G", """<div class="grid"><div class="card"><strong class="proved">EXACT IDENTITIES</strong>严格正时间上的全周期无散梯度测试消掉压力，但保留反号黏性、二阶源项与应变。</div><div class="card"><strong class="proved">FINITE-CLASS OBSTRUCTION</strong>固定正定二次梯度组合不能对所有 Hessian 方向产生共同正耗散。</div><div class="card"><strong class="open">CONDITIONAL DIVERGENCE</strong>正原子分支迫使 Δw 的 L⁴ᐟ³_tL²_x 成本在每个终端区间发散，但不能反推 W_z 发散。</div></div><p>全部 BW 结论仍假设 BP/BU 的同一周期无外力光滑 NS 原解、额外正终端能量原子及共同伴随。这是条件性方法审查，不构造或排除原子，也没有减少 G 的未证输入。</p>"""),
    ("02 / BW.1–BW.5", "严格正时间的梯度恒等式", """<p>先固定 0&lt;s&lt;t≤L，不把梯度端点移到 ρ=0。对 b、w、z 作全周期线性无散二阶测试，压力确实正交消失；带空间截止或幅值非线性测试没有这一特权。</p><div class="equation">½Γ_b′−νK_b=−B_b(b,b),   ½Γ_w′+νK_w=−B_b(w,w).   (BW.3)</div><div class="equation">½Γ_z′+νK_z=2νJ(b,z)−B_b(z,z),   H(z,w)′=−2νcK_w−2B_b(z,w).   (BW.3–BW.4)</div><p><strong>DIRECT DERIVATION</strong>相反黏性的交叉项抵消，但 2νcΔw 源产生的二阶项不能删去；这些式子还受 Γ_z 与 H(z,w) 的代数关系约束，不是独立的新预算。</p>"""),
    ("03 / BW.6–BW.8", "常系数二次组合的有限类障碍", """<p>对 Y=(z,w) 取任意固定实对称正定 2×2 矩阵 K，并在每个分量使用同一个二次梯度能量。其最高阶扩散对称部分满足</p><div class="equation">det sym(KA)=−ν²a(e+2cd+c²a)&lt;0.   (BW.7)</div><p>括号是 (c,1)ᵀK(c,1)&gt;0，因此固定二次型必有一正一负两个扩散方向。</p><p><strong>FINITE CLASS ONLY</strong>这只排除“对任意 Hessian 方向共同强制耗散”的常系数二次型；不排除变系数、非局部形式、真实轨道几何或其他有符号机制，也不是全部 NS 能量方法的不可能定理。</p>"""),
    ("04 / BW.9–BW.13", "二阶源项和应变仍留下未付成本", """<p>正向残差梯度估计需要原解的二阶成本 K_b；零阶能量已付的 −2νΔb∈L²H⁻¹ 并不支付 ∫K_b。</p><div class="equation">½Γ_z′+(ν/2)K_z ≤ 2νK_b+|B_b(z,z)|.   (BW.9)</div><p>普通应变插值与 Young 留下 Γ_b²Γ_v，能量只有 Γ_b∈L¹，不能直接作终端 Gronwall。代入 b=z−cw 后，残差应变需要以 K_w 为密度的控制，自应变还留下 c⁴Γ_w³。它们都不是 BV 的 W_z，也没有由一阶能量支付。</p>"""),
    ("05 / BW.14–BW.15", "耗散权重需要端点和时间变化", """<p>对合法的 C¹ 权重 f，精确恒等式为</p><div class="equation">2ν∫ₛᵗ fΓ_w = f(s)||w(s)||₂²−f(t)||w(t)||₂²+∫ₛᵗ f′||w||₂².   (BW.14)</div><p>把 f 换成 ||z||₃ 之前必须支付它的端点与时间变化，现有结果没有给出全时间有界变差。直接以 |z|z 测试残差方程时，压力和源项都会重新出现；严格正时间的局部可微性不能替代终端可积性。</p>"""),
    ("06 / BW.16–BW.18", "条件性 4/3 二阶成本发散", """<p>在当前正原子共同伴随分支，对每个 0&lt;δ≤L，</p><div class="equation">∫₀^δ ||Δw(ρ)||₂⁴ᐟ³ dρ=+∞,   ∫₀^δ K_w(ρ)dρ=+∞.   (BW.16)</div><p>若第一项有限，已付 b∈L⁴_tL³_x 与 Sobolev 给 P[(b·∇)w]∈L¹_tL²_x，投影方程于是使 w_ρ∈L¹_tL²_x 并产生强 L² 初迹；这与弱迹零、范数平方趋一矛盾。</p><div class="equation">W_z ≤ ||w||L∞L² ||z||L⁴L³ ||Δw||L⁴ᐟ³L².   (BW.18)</div><p><strong>ONE-WAY ONLY</strong>右端无穷不能反推 W_z 无穷；没有范数等价，也没有证明混合功不可控。自压力和端点同样不会因此消失。</p>"""),
    ("07 / 文献和历史去重边界", "有界第一手来源核查，没有导入新定理", """<p><strong>LITERATURE</strong>本轮读取 Leslie–Shvydkoy arXiv:1705.04420v4 的全空间设定、Theorem 1.2、Proposition 3.1 与完整 §4；这些结果仍保留额外可积性或 Type I 条件，不能自动移植为本节周期能量类的无原子结论。Shvydkoy arXiv:1205.1544v2 本轮只核对元数据与摘要。</p><p>没有重审前者 §3/§5 全部证明、外部依赖或周期迁移，也不声称穷尽性、外部同行评审或文献新颖性。后续 R/S 五项时钟来源只是已定位，完整去重尚未开始，不作为本章结果。</p>"""),
    ("08 / 证据与下一步", "停止重复二次组合，回到一般指定中心", """<p>科学源提交 53f167438c058c77aa218216a014c3e504300300；冻结提交 6c6186d86d22c925eb2f7e7d03ad39f291f4dfac。七份本轮文件、157 份依赖和一份冻结 manifest 由 SHA-256 绑定；三份文本源、18 个 BW 标签、25 项独立有理复算及 5 项有限负对照通过。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_source_enstrophy_20260907.md">BW 正文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_source_enstrophy_reading_20260907.md">阅读边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_source_enstrophy_report-source_20260907.md">研究报告</a></p><p>下一研发动作先完整核查 R 的 arbitrary-clock 与 S 的 signed-collar、boundary-mismatch、weighted-Abel、one-sided-clock 五项真实账本，再判断一般指定中心是否存在尚未测试的 NS 有符号项；该去重与后续推导尚未开始。</p><p><strong>FINITE CHECKS ONLY：有限复算不证明 PDE、矩阵正定性或极限。无新读者 PDF、仿真、科学图、DGX 数据或累计 recap。一般奇点到原子分支的连接、原子排除、G、R.216–R.217、一般三维正则性与 Clay 均 OPEN。NOT CLAY。</strong></p>"""),
]

EN_SECTIONS = [
    ("01 / Result map", "This chapter closes a methodological misreading, not G", """<div class="grid"><div class="card"><strong class="proved">EXACT IDENTITIES</strong>Full-periodic divergence-free gradient tests on strict positive-time intervals remove pressure but retain opposite viscosity, second-order sources, and strain.</div><div class="card"><strong class="proved">FINITE-CLASS OBSTRUCTION</strong>A fixed positive-definite quadratic gradient combination cannot give common positive dissipation in every Hessian direction.</div><div class="card"><strong class="open">CONDITIONAL DIVERGENCE</strong>The positive-atom branch forces divergence of the L⁴ᐟ³_tL²_x cost of Δw on every terminal interval, but does not imply divergence of W_z.</div></div><p>Every BW conclusion still assumes the BP/BU same periodic unforced smooth NS parent, extra positive terminal-energy atom, and common adjoint. This conditional method screen neither constructs nor excludes an atom and reduces no unproved input of G.</p>"""),
    ("02 / BW.1–BW.5", "Gradient identities on strict positive-time intervals", """<p>First fix 0&lt;s&lt;t≤L; no gradient endpoint is moved to ρ=0. Full-periodic linear divergence-free second-order tests of b,w,z make pressure genuinely orthogonal. Spatial cutoffs and nonlinear amplitude tests do not inherit this cancellation.</p><div class="equation">½Γ_b′−νK_b=−B_b(b,b),   ½Γ_w′+νK_w=−B_b(w,w).   (BW.3)</div><div class="equation">½Γ_z′+νK_z=2νJ(b,z)−B_b(z,z),   H(z,w)′=−2νcK_w−2B_b(z,w).   (BW.3–BW.4)</div><p><strong>DIRECT DERIVATION</strong>Opposite-viscosity cross terms cancel, but the second-order term created by the 2νcΔw source cannot be removed. Algebraic relations among Γ_z and H(z,w) mean these identities are not independent new budgets.</p>"""),
    ("03 / BW.6–BW.8", "Finite-class obstruction for constant quadratic combinations", """<p>For Y=(z,w), take any fixed real symmetric positive-definite 2×2 matrix K and the same quadratic gradient energy in every component. The symmetric highest-order diffusion part satisfies</p><div class="equation">det sym(KA)=−ν²a(e+2cd+c²a)&lt;0.   (BW.7)</div><p>The bracket is (c,1)ᵀK(c,1)&gt;0, so the fixed quadratic form has one positive and one negative diffusion direction.</p><p><strong>FINITE CLASS ONLY</strong>This excludes only common coercive dissipation for arbitrary Hessian directions in this constant quadratic class. It does not exclude variable or nonlocal forms, geometry of the actual trajectory, or other signed mechanisms, and is not a no-go theorem for all NS energy methods.</p>"""),
    ("04 / BW.9–BW.13", "Second-order sources and strain retain unpaid costs", """<p>The forward residual gradient estimate requires the parent's second-order cost K_b. The zero-order payment −2νΔb∈L²H⁻¹ does not pay ∫K_b.</p><div class="equation">½Γ_z′+(ν/2)K_z ≤ 2νK_b+|B_b(z,z)|.   (BW.9)</div><p>Standard strain interpolation and Young leave Γ_b²Γ_v, while energy gives only Γ_b∈L¹, so terminal Gronwall is unavailable. Substituting b=z−cw makes residual strain require control with density K_w, while self-strain leaves c⁴Γ_w³. Neither is BV's W_z or paid by first-order energy.</p>"""),
    ("05 / BW.14–BW.15", "Dissipation weights require endpoints and time variation", """<p>For a legitimate C¹ weight f, the exact identity is</p><div class="equation">2ν∫ₛᵗ fΓ_w = f(s)||w(s)||₂²−f(t)||w(t)||₂²+∫ₛᵗ f′||w||₂².   (BW.14)</div><p>Before setting f=||z||₃, its endpoints and time variation must be paid; no global bounded-variation result is available. Testing the residual equation by |z|z makes pressure and source terms reappear. Local differentiability on strict positive times does not replace terminal integrability.</p>"""),
    ("06 / BW.16–BW.18", "Conditional divergence of the 4/3 second-order cost", """<p>On the present positive-atom common-adjoint branch, for every 0&lt;δ≤L,</p><div class="equation">∫₀^δ ||Δw(ρ)||₂⁴ᐟ³ dρ=+∞,   ∫₀^δ K_w(ρ)dρ=+∞.   (BW.16)</div><p>If the first integral were finite, the paid b∈L⁴_tL³_x and Sobolev would give P[(b·∇)w]∈L¹_tL²_x. The projected equation would then imply w_ρ∈L¹_tL²_x and a strong L² initial trace, contradicting weak trace zero and squared norm tending to one.</p><div class="equation">W_z ≤ ||w||L∞L² ||z||L⁴L³ ||Δw||L⁴ᐟ³L².   (BW.18)</div><p><strong>ONE-WAY ONLY</strong>An infinite right-hand side does not imply W_z=∞. No norm equivalence or impossibility of mixed-work control is proved. Self-pressure and endpoints also remain.</p>"""),
    ("07 / Literature and historical-deduplication boundary", "Bounded primary-source review with no imported theorem", """<p><strong>LITERATURE</strong>This round read the full-space setup, Theorem 1.2, Proposition 3.1, and complete §4 of Leslie–Shvydkoy arXiv:1705.04420v4. Those results retain extra integrability or Type I assumptions and do not transfer automatically into an energy-class no-atom theorem on the present periodic domain. Only metadata and abstract were revisited for Shvydkoy arXiv:1205.1544v2.</p><p>The full proofs in §3/§5, external dependencies, and periodic transfer were not reaudited. No exhaustiveness, external peer review, or literature novelty is claimed. Five future R/S clock sources are only located; their full deduplication has not started and is not a result of this chapter.</p>"""),
    ("08 / Evidence and next step", "Stop repeating quadratic combinations and return to the general prescribed centre", """<p>Scientific source commit: 53f167438c058c77aa218216a014c3e504300300; freeze commit: 6c6186d86d22c925eb2f7e7d03ad39f291f4dfac. Seven current files, 157 dependencies, and one frozen manifest are SHA-256-bound. Three text sources, 18 BW labels, 25 independent rational recomputations, and five limited negative controls pass.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_source_enstrophy_20260907.md">BW source</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_source_enstrophy_reading_20260907.md">reading boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_source_enstrophy_report-source_20260907.md">research report</a></p><p>The next research action fully checks the real R arbitrary-clock and S signed-collar, boundary-mismatch, weighted-Abel, and one-sided-clock ledgers before asking whether a genuinely untested signed NS term exists at a general prescribed centre. That deduplication and any later derivation have not started.</p><p><strong>FINITE CHECKS ONLY: finite recomputation does not prove PDE, matrix positivity, or limits. No new reader PDF, simulation, scientific figure, DGX data, or cumulative recap. The link from a general singularity to the atom branch, atom exclusion, G, R.216–R.217, general 3D regularity, and Clay remain OPEN. NOT CLAY.</strong></p>"""),
]


def main_block(lang: str, sections: list[tuple[str, str, str]]) -> str:
    if lang == "zh":
        kicker, title = "CB.24 · 独立 Clay-B 方法笔记 · 2026-09-07", "CB.24｜残差的梯度能量：源项、应变与二次组合的边界"
        dek, footer = "严格正时间的梯度测试保留二阶源项与应变；常系数二次组合存在有限类障碍，正原子分支还迫使特定二阶时间成本发散，但这些都不关闭加权混合功或 G。", "独立 HTML 研究笔记"
    else:
        kicker, title = "CB.24 · Independent Clay-B methods note · 2026-09-07", "CB.24 | Residual gradient energy: sources, strain, and the boundary of quadratic combinations"
        dek, footer = "Strict-positive-time gradient tests retain second-order sources and strain. Constant quadratic combinations face a finite-class obstruction, and the positive-atom branch forces divergence of a specific second-order time cost, without closing weighted mixed work or G.", "Independent HTML research note"
    body = "".join(f'<section><div class="section-no">{n}</div><h2>{h}</h2>{c}</section>' for n, h, c in sections)
    return f'''  <main data-language="{lang}">
    <article><header class="hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="dek">{dek}</p><div class="meta"><span>PROVED</span><span>CONDITIONAL</span><span>DIRECT DERIVATION</span><span>NO CLOSURE</span><span>LITERATURE</span><span>FINITE</span><span>FINITE CHECKS ONLY</span><span>OPEN · NOT CLAY</span></div></header>{body}</article>
    <footer class="footer">CB.24 · {footer} · {DISPLAY_ID} · 2026-09-07</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-source-enstrophy" aria-labelledby="clay-b-source-enstrophy-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.24 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-07 · SOURCE / ENSTROPHY</p><h2 class="route-map-title" id="clay-b-source-enstrophy-title">CB.24｜残差的梯度能量：源项、应变与二次组合的边界</h2><p class="route-map-intro">全周期梯度测试消掉压力，却留下二阶源项和应变；固定正定二次组合不能共同正耗散。正原子分支迫使 Δw 的 L⁴ᐟ³_tL²_x 成本发散，但不能反推 W_z 发散、范数等价或混合功不可控。G 仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 源项与梯度能量笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-source-enstrophy-20260907.html">阅读最新 CB.24 笔记 →</a><a href="/literature-review.html#clay-b-source-enstrophy-boundary">查看来源与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 源项与梯度能量结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>严格正时间梯度恒等式</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>常二次组合有限类障碍</span><span><i class="route-legend-mark current" aria-hidden="true"></i>不能反推 W_z · G OPEN · NOT CLAY</span></div></div></section>'''


CB_ROWS = '''          <div class="tree-row clay-b-same-parent-residual-row">
            <article class="tree-node"><div class="tree-node-head"><span class="route-range">CB.22 · 2026-09-06 · BU SAME-PARENT RESIDUAL</span><span class="tree-state">独立路线章节</span></div><h3>CB.22｜同一原解的对齐残差：能量、混合压力与终端边界</h3><p>正原子条件下，终端残差测度在目标点无原子，正向方程保留 −2νΔb 源；混合张量全时间消失且完整周期混合压力有普通时间 little-o。</p><p class="tree-path"><a href="/notes/clay-b-same-parent-residual-20260906.html">阅读 CB.22 HTML</a> · <a href="/literature-review.html#clay-b-same-parent-residual-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
          </div>

          <div class="tree-row clay-b-signed-mixed-pressure-row">
            <article class="tree-node"><div class="tree-node-head"><span class="route-range">CB.23 · 2026-09-07 · BV SIGNED MIXED PRESSURE</span><span class="tree-state">独立路线章节</span></div><h3>CB.23｜有符号混合压力功：投影测试和联合截断</h3><p>投影给出逐时幅度一致上界；联合截断只控制有符号累计压力。W_z 与混合压力平方是两条不同且未付的充分接口，三个余项和自压力均保留。</p><p class="tree-path"><a href="/notes/clay-b-signed-mixed-pressure-20260907.html">阅读 CB.23 HTML</a> · <a href="/literature-review.html#clay-b-signed-mixed-pressure-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right kept"><span class="tree-state">SOURCE / ENSTROPHY AUDIT COMPLETED</span><h3>源项与梯度能量核查已进入 CB.24</h3><p>BW 已写清严格正时间恒等式、常二次组合的有限类障碍与条件性 4/3 二阶成本发散；结果见下一个路线节点。</p></aside>
          </div>

          <div class="tree-row clay-b-source-enstrophy-row">
            <article class="tree-node current"><div class="tree-node-head"><span class="route-range">CB.24 · 2026-09-07 · BW SOURCE / ENSTROPHY</span><span class="tree-state current">当前路线边界</span></div><h3>CB.24｜残差的梯度能量：源项、应变与二次组合的边界</h3><p>全周期线性无散梯度测试消掉压力，但二阶源项、应变与梯度端点仍未支付；常系数正定二次型的扩散对称部分行列式恒负，只排除任意 Hessian 方向的固定二次组合。</p><p>正原子分支迫使 Δw∉L⁴ᐟ³_tL²_x，否则投影方程给出矛盾的强 L² 初迹。这不反推 W_z 发散、范数等价或混合功不可控，也未减少 G 的未证输入。</p><p class="tree-path"><a href="/notes/clay-b-source-enstrophy-20260907.html">阅读 CB.24 HTML</a> · <a href="/literature-review.html#clay-b-source-enstrophy-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发动作：一般中心的 R/S 历史去重</h3><p>先完整读取五项已定位的时钟与边界账本，再判断是否存在尚未测试的 NS 有符号项。去重与推导均尚未开始。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.25 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.24</h3><p>CB.25 只是下一章占位，不是已完成研究。R/S 去重、W_z、混合压力平方、自压力、原子存在或排除、G、R.216–R.217、一般正则性与 Clay 均未关闭。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-source-enstrophy-boundary">CB.24 · Clay-B 源项与梯度能量的来源和主张边界</h3><p>本轮有界第一手来源核查读取 <a href="https://arxiv.org/html/1705.04420v4">Leslie–Shvydkoy arXiv:1705.04420v4</a> 的全空间设定、Theorem 1.2、Proposition 3.1 与完整 §4；这些结论保留额外可积性或 Type I 条件，没有自动支付 BW 的周期能量类输入。<a href="https://arxiv.org/abs/1205.1544v2">Shvydkoy arXiv:1205.1544v2</a> 本轮只核对元数据与摘要。没有重审前者 §3/§5 全部证明、外部依赖或周期迁移，也不主张穷尽性、外部同行评审或文献新颖性。</p><div class="boundary"><strong>CB.24 · ClayB-SourceEnstrophy-20260907 公开边界</strong><p>CONDITIONAL：全部 BW 结论假设 BP/BU 的同一周期无外力光滑 NS 原解、额外正终端能量原子与共同伴随。STRICT POSITIVE TIME：全周期线性无散梯度测试消掉压力，但保留反号黏性、二阶源、应变及未受控梯度端点；非线性或截止测试仍有压力。FINITE CLASS：任意固定正定 2×2 二次梯度组合的 sym(KA) 行列式为 −ν²a(e+2cd+c²a)&lt;0，只排除对任意 Hessian 方向共同正耗散的常系数类，不是实际 NS 轨道或全部能量方法的 no-go。CONDITIONAL DIVERGENCE：正原子分支上，每个 0&lt;δ≤L 都有 ∫₀^δ||Δw||₂⁴ᐟ³=∞；若有限，则 b∈L⁴L³ 使 w_ρ∈L¹L² 并产生与弱零迹、范数趋一矛盾的强 L² 迹。ONE-WAY ONLY：BW.18 的充分上界右端无穷不能反推 W_z 无穷；没有范数等价、混合功不可能性或 G 输入减少。BV 的两条充分接口、自压力和端点仍未付。FINITE CHECKS ONLY：三份文本源、18 个 BW 标签、164/164 文件绑定、25 项有理复算和 5 项有限负对照不替代 PDE 证明。未来 R/S 五项去重尚未开始；原子生成/排除、G、R.216–R.217、一般正则性和新颖性 OPEN；无图、仿真、新 PDF 或 recap。NOT CLAY。<a href="/notes/clay-b-source-enstrophy-20260907.html">阅读完整 CB.24 笔记</a>。</p></div>
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
    value = (ROOT / "public/notes/clay-b-signed-mixed-pressure-20260907.html").read_text(encoding="utf-8")
    value = set_version(value)
    value = re.sub(r'<title>.*?</title>', '<title>残差的梯度能量：源项、应变与二次组合的边界</title>', value, count=1)
    value = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 残差梯度能量、源项、应变、二次组合边界与条件性二阶成本发散的双语方法笔记。">', value, count=1)
    value = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', value, count=1)
    value = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.24 · {DISPLAY_ID}</strong></header>', value, count=1)
    both = main_block("zh", ZH_SECTIONS) + "\n\n" + main_block("en", EN_SECTIONS)
    value, count = re.subn(r'  <main data-language="zh">[\s\S]*?  </main>\n\n  <main data-language="en">[\s\S]*?  </main>', both, value, count=1)
    if count != 1: raise RuntimeError("note bilingual template drift")
    return value


def update_home(value: str) -> str:
    value = set_version(value, "综述", refresh=True)
    value = re.sub(r'<strong>v\d+\.\d+</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', value, count=1)
    value, count = re.subn(r'<section class="route-overview independent-release-spotlight"[\s\S]*?</section>', SPOTLIGHT, value, count=1)
    if count != 1: raise RuntimeError("independent spotlight drift")
    value = value.replace("CB.1–CB.23", "CB.1–CB.24")
    value = value.replace("signed mixed-pressure / joint truncation", "source / enstrophy / quadratic boundary", 1)
    old = "Clay-B 已用全周期投影得到不显含截断幅度的逐时混合压力功上界，并以同幅联合截断证明联合压力的有符号原函数一致趋零；但加权时间成本与混合压力平方只是两条不同且未付的充分接口，三个余项、自压力与原子排除仍未闭合。下一步直接检查源项和梯度能量演化。"
    new = "Clay-B 已核清同父残差的梯度能量边界：全周期线性无散测试消掉压力，却留下二阶源项、应变和梯度端点；固定正定二次组合不能共同正耗散，正原子分支还迫使 Δw 的 L⁴ᐟ³_tL²_x 成本发散。但这不反推 W_z 发散、混合功不可控或 G 输入减少。下一步先做一般中心 R/S 历史去重。"
    if old in value: value = value.replace(old, new, 1)
    elif new not in value: raise RuntimeError("homepage focus copy drift")
    value, count = re.subn(r'          <div class="tree-row clay-b-same-parent-residual-row">[\s\S]*?<div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB_ROWS + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if count != 1: raise RuntimeError("Clay-B tail drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-source-enstrophy-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value: raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload.update({"publicIndependentNoteCount": 24, "latestIndependentNote": DISPLAY_ID, "latestIndependentResearchHtml": f"/notes/{SLUG}.html", "latestIndependentResearchPdf": None, "independentChapterScheme": "CB.n", "latestIndependentChapter": "CB.24", "nextIndependentChapter": "CB.25"})
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note", "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.24",
            "sourceCommit": "53f167438c058c77aa218216a014c3e504300300", "baseCommit": "363bb4b83b2b3c3db605e42e05491072cb073bf5", "handoffCommit": "6c6186d86d22c925eb2f7e7d03ad39f291f4dfac", "logicalPredecessor": "ClayB-SignedMixedPressure-20260907",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False, "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-source-enstrophy-20260907-gate.test.mjs", "publicationTest": "tests/clay-b-source-enstrophy-20260907-release.test.mjs", "translationScript": "scripts/add-clay-b-source-enstrophy-20260907-translations.mjs",
            "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs", "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE", "simulationRequired": False, "recapRequired": False, "advancesCanonicalR0Series": False, "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "CONDITIONAL_ON_BP_BU_SAME_PARENT_POSITIVE_ATOM_STRICT_POSITIVE_TIME_GRADIENT_IDENTITIES_RETAIN_SOURCE_AND_STRAIN_CONSTANT_SPD_QUADRATIC_SCREEN_ONLY_ARBITRARY_HESSIAN_DIRECTIONS_CONDITIONAL_DELTA_W_L4_OVER_3_TIME_L2_SPACE_DIVERGENCE_DOES_NOT_IMPLY_WEIGHTED_WORK_DIVERGENCE_NORM_EQUIVALENCE_OR_MIXED_WORK_IMPOSSIBILITY_NO_G_INPUT_REDUCED_SELF_PRESSURE_ENDPOINTS_ATOM_EXCLUSION_GENERAL_REGULARITY_AND_NOVELTY_OPEN_NOT_CLAY",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def handoff_bytes() -> bytes:
    ledger = json.loads((ROOT / "research/clay_b_source_enstrophy_frozen_ledger_20260907.json").read_text(encoding="utf-8"))
    qa = json.loads((ROOT / "release/qa/clay-b-source-enstrophy-20260907.json").read_text(encoding="utf-8"))
    artifacts = [{"path": r["path"], "sha256": r["sha256"], "role": "frozen-scientific-source" if r["role"] == "scientific-source" else "frozen-dependency", "commit": r["commit"]} for r in ledger["files"]]
    artifacts += [{"path": r["path"], "sha256": r["sha256"], "role": "frozen-release-manifest", "commit": r["commit"]} for r in ledger["handoffEnvelope"]]
    outputs = [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html", "public/notes/index.html", "public/site-version.json", "research/release-manifest.json", "VERSION"]
    support = ["research/clay_b_source_enstrophy_frozen_ledger_20260907.json", "release/handoffs/clay-b-source-enstrophy-20260907.json", "release/qa/clay-b-source-enstrophy-20260907.json", "scripts/import_clay_b_source_enstrophy_20260907_frozen.py", "scripts/generate_clay_b_source_enstrophy_20260907_release.py", "scripts/generate_note_index.py", "scripts/add-clay-b-source-enstrophy-20260907-translations.mjs", "tests/clay-b-source-enstrophy-20260907-gate.test.mjs", "tests/clay-b-source-enstrophy-20260907-release.test.mjs", "tests/release-publication-invariant.test.mjs", "translations/en.json", "public/i18n-en.js"]
    managed = list(dict.fromkeys(outputs + [r["path"] for r in artifacts] + support))
    payload = {
        "schemaVersion": "research-publication-handoff-v1", "releaseId": DISPLAY_ID, "frozenCommit": "6c6186d86d22c925eb2f7e7d03ad39f291f4dfac", "sourceRepository": "navier-stokes-r074m", "translationRoute": "LOCAL_DIRECT_NO_DGX", "artifacts": artifacts,
        "artifactPolicy": {"readerPdf": "OMIT_NEW", "scientificFigure": "NOT_REQUIRED"},
        "claimBoundary": {"requiredLabels": ["PROVED", "CONDITIONAL", "DIRECT DERIVATION", "NO CLOSURE", "LITERATURE", "FINITE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"], "publicFiles": [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html"]},
        "recap": {"mode": "PRESERVE", "latestRecapRelease": "r076i", "preservedArtifacts": [{"path": "public/recap-r0-61-r0-76i.html", "sha256": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9"}, {"path": "public/recap-r0-61-r0-76i.pdf", "sha256": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98"}]},
        "stages": {"generate": {"runner": "python-local", "script": "scripts/generate_clay_b_source_enstrophy_20260907_release.py", "inputs": [r["path"] for r in artifacts] + ["research/clay_b_source_enstrophy_frozen_ledger_20260907.json"], "outputs": outputs}, "translate": {"runner": "node-local", "script": "scripts/add-clay-b-source-enstrophy-20260907-translations.mjs", "inputs": ["public/research-review.html", "public/literature-review.html", "public/notes/index.html", "translations/en.json"], "outputs": ["translations/en.json", "public/i18n-en.js"]}},
        "publication": {"expectedCommit": None, "siteBaseUrl": "https://kasifa.github.io", "repository": "Kasifa/Kasifa.github.io", "workflow": "pages.yml", "remote": "origin", "targetBranch": "main", "commitMessage": "Publish ClayB SourceEnstrophy CB.24 HTML note", "managedPaths": managed, "expectedLive": qa["online"]["expectedLive"], "expectedAbsent": qa["online"]["expectedAbsent"], "siteVersionExpectations": qa["online"]["siteVersionExpectations"]},
        "visualQa": {"evidencePath": qa["browser"]["evidencePath"], "configPath": "release/qa/clay-b-source-enstrophy-20260907.json", "requiredChecks": [f"{t['id']}-{s['id']}" for t in qa["browser"]["targets"] for s in qa["browser"]["scenarios"]]},
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.24", DISPLAY_ID, "残差的梯度能量：源项、应变与二次组合的边界", "Residual gradient energy: sources, strain, and the boundary of quadratic combinations", "PROVED", "CONDITIONAL", "DIRECT DERIVATION", "NO CLOSURE", "LITERATURE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"]:
        if marker not in note: raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16: raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists(): raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.24", "Clay-B 独立路线停在 CB.24", "CB.25 · NEXT", 'class="tree-row clay-b-source-enstrophy-row"', f"/notes/{SLUG}.html", "单独的虚线泳道"]:
        if marker not in home: raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1: raise RuntimeError("homepage independent spotlight count drift")
    r0 = home.index('class="route-tree r0-route-tree"'); rb = home.index('class="tree-row r0-public-boundary-row"', r0); div = home.index('class="route-lane-divider"', rb); clay = home.index('class="route-tree clay-b-route-tree"', div); cb = home.index('class="tree-row clay-b-source-enstrophy-row"', clay); bound = home.index('class="tree-row clay-b-public-boundary-row"', cb)
    if not (r0 < rb < div < clay < cb < bound): raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-source-enstrophy-boundary"' not in literature or "CB.24 · ClayB-SourceEnstrophy-20260907 公开边界" not in literature: raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.24 · {DISPLAY_ID}" not in index or "24 NOTES" not in index: raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8")); manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.24" or site.get("nextIndependentChapter") != "CB.25": raise RuntimeError("version or chapter metadata drift")
    if manifest.get("latestCompletedRelease") != "r076l" or site.get("latestRelease") != "R0.76L": raise RuntimeError("canonical R0 endpoint drift")
    path = ROOT / "release/handoffs/clay-b-source-enstrophy-20260907.json"
    if not path.is_file() or path.read_bytes() != handoff_bytes(): raise RuntimeError("publication handoff drift")


if not CHECK_ONLY:
    NOTE_PATH.write_text(build_note(), encoding="utf-8")
    home = ROOT / "public/research-review.html"; home.write_text(update_home(home.read_text(encoding="utf-8")), encoding="utf-8")
    literature = ROOT / "public/literature-review.html"; literature.write_text(update_literature(literature.read_text(encoding="utf-8")), encoding="utf-8")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    update_metadata(ROOT / "public/site-version.json"); update_metadata(ROOT / "research/release-manifest.json")
    subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    (ROOT / "release/handoffs/clay-b-source-enstrophy-20260907.json").write_bytes(handoff_bytes())

validate()
print(json.dumps({"schemaVersion": "clay-b-source-enstrophy-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.24", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
