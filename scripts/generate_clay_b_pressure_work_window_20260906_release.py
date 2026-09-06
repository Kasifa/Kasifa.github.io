#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB PressureWorkWindow CB.9 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.53"
SLUG = "clay-b-pressure-work-window-20260906"
DISPLAY_ID = "ClayB-PressureWorkWindow-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in __import__("sys").argv[1:]


ZH_MAIN = '''  <main data-language="zh">
    <article>
      <header class="hero">
        <div class="kicker">CB.9 · 独立 Clay-B 解析笔记 · 2026-09-06</div>
        <h1>CB.9｜固定总能量不能给出这条 L³ 增长预算</h1>
        <p class="dek">对每个固定初始 L² 能量，构造一族真实、光滑、黏性为 1 的周期 Navier–Stokes 解：真实正压力功在统一早时窗内造成固定比例的 L³ 三次方增长，而同期累计梯度平方趋于零。这只排除一条前置系数为 1、无加性预算、常数仅依赖总能量的精确估计。</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>LITERATURE BOUNDED</span><span>FINITE: NONE</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / 结论地图</div><h2>真实压力做功，而不是 CB.8 的零做功残差平台</h2><div class="grid"><div class="card"><strong class="proved">紧支撑正压力功</strong>周期正压力功种子经过 curl cutoff 和高频压力调制，得到光滑紧支撑的全空间无散场。</div><div class="card"><strong class="proved">统一真实增长</strong>固定能量单泡在 tε=τ₀ε^(5/2) 内保持正压力功，并获得与 ε 无关的相对 H 增量。</div><div class="card"><strong class="open">严格边界</strong>这是变化初值族的早时窗口；成熟时间、固定单解历史、首次奇点与合同 G 仍 OPEN。</div></div><p>与 CB.8 的 F=0 常速平台不同，CB.9 控制的是真实有符号压力功和净 L³ 增长。</p></section>
      <section><div class="section-no">02 / AI.1–AI.18</div><h2>从周期正压力功到紧支撑 Euclidean 无散场</h2><p>从固定有限 Fourier、周期、无散且正压力功的种子出发，先取周期向量势，再对其作 curl cutoff。这样保持精确无散；零速处使用全局 Lipschitz 张量 B(z)=z⊗z/|z|，不除以速度或 cutoff。</p><div class="equation">W_R³(V_N)=N f̄ ∫a⁴+O(1)&gt;0.                                  (AI.18)</div><p>全空间压力乘子的高频主项保留正号；总频率零点由 Schwartz 尾部控制，低频平均压力与 cutoff 修正也被压入误差。辅助调制场不冒充 NS 速度。</p></section>
      <section><div class="section-no">03 / AI.19–AI.30</div><h2>固定 L² 能量的单泡具有真实初始净增长</h2><p>把一个正压力功紧支撑场 V 归一化到 E₀，再缩成单泡嵌入单位环面。对应量的主尺度为</p><div class="equation">H≈ε^(−3/2),  ||∇u||₂²≈ε^(−2),
D≈ε^(−7/2),  W≈ε^(−4),
H′(0)=ε^(−4)W_V−ε^(−7/2)D_V+O(ε^(−1))&gt;0.             (AI.24–AI.28)</div><p>因此 ((H′(0))₊/H)/(1+||∇u||₂²)≈ε^(−1/2) 发散。这里已经是真实 NS 初始压力功，不是大残差替代物；但瞬时结论本身还不是正时间窗口。</p></section>
      <section><div class="section-no">04 / AJ.1–AJ.9</div><h2>扩张环面把物理短窗变成固定重标时间</h2><p>令 L=ε⁻¹，并作 y=(x−x₀)/ε、τ=ε^(−5/2)t、uε=ε^(−3/2)Uε。单位环面上黏性 1 的方程精确变为扩张环面上的低黏性方程</p><div class="equation">∂τUε+Uε·∇Uε+∇Pε=√ε ΔUε,
div Uε=0,  Uε(0)=V_L.                                      (AJ.3–AJ.4)</div><p>非归一化 Sobolev 范数、格点分壳、Leray 投影和压力零频约定都显式固定；嵌入常数不随 L 增长。</p></section>
      <section><div class="section-no">05 / AJ.10–AJ.22</div><h2>统一 H⁵ 生命周期与正压力功连续性</h2><p>直接 Leibniz 交换子估计、Galerkin 构造和高阶延拓给出只依赖 V 的统一 τ₁ 与 H⁵ 上界。时间导数的 H³ 控制使 Uε(τ) 在 H³ 中以 O(τ) 靠近初值。</p><div class="equation">sup_(0≤τ≤τ₁)||Uε(τ)||_(H⁵)≤M,
W_L(Uε(τ))≥w₀/2  for 0≤τ≤τ₀.                         (AJ.13, AJ.22)</div><p>初始 Euclidean 比较保留 Newtonian Hessian 的 delta 项；正时间则使用全环面乘子与压力功的 H²-Lipschitz 连续性，不假设黏性解继续紧支撑。</p></section>
      <section><div class="section-no">06 / AJ.23–AJ.29</div><h2>固定相对 H 增长与消失的累计梯度预算</h2><div class="equation">tε=τ₀ε^(5/2),
Hε(tε)/Hε(0)≥1+δ₀,
∫₀^(tε)||∇uε(t)||₂²dt≤C√ε→0.                         (AJ.27–AJ.28)</div><p>在整个窗口中还有 W(uε(t))≥(w₀/2)ε⁻⁴ 和 H′ε(t)≥(w₀/4)ε⁻⁴。这是光滑周期真实 NS 解族的解析结论，不是有限采样、仿真或数值拟合。</p></section>
      <section><div class="section-no">07 / AJ.30</div><h2>只排除一个量词完全固定的指数估计</h2><div class="equation">H(t)≤H(0) exp[C(E₀)∫₀ᵗ(1+||∇u(s)||₂²)ds].                 (AJ.30)</div><p>若该式对所有相应光滑解从初始时刻成立，且前置系数严格为 1、没有加性预算、C 只依赖 E₀，那么右侧相对增量趋于零，与固定的 δ₀ 矛盾。允许 K&gt;1、加性预算或依赖 H(0) 等其他初值范数的估计并未被排除。</p></section>
      <section><div class="section-no">08 / 文献、证据与下一问题</div><h2>早时窗口不能冒充成熟时间</h2><p>tε/ε²=τ₀√ε→0，且 Hε(0)≈ε⁻³ᐟ²、||∇uε(0)||₂²≈ε⁻² 都发散。这是一族变化初值，不是一条固定解的首次奇点历史。下一研发问题回到同一解、固定半径和 t≥Cε² 的成熟时间恒等式，保留近源压力、外壳输运与黏性支付。</p><table><thead><tr><th>类别</th><th>本章范围</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>AI 的紧支撑正压力功与固定能量初始净增长；AJ 的统一早时真实压力功、固定相对 H 增长和 O(√ε) 累计梯度平方。</td></tr><tr><td>LITERATURE</td><td>Tran–Yu 已有 Lq 压力功与 speed moderator；Bourgain–Pavlović 和 Kang–Yun–Protas 研究的是不同空间、不同固定量或数值对象。</td></tr><tr><td>FINITE COMPUTATION</td><td>无；没有仿真、数值证书或科学图。</td></tr><tr><td>OPEN</td><td>成熟时间上的同一解压力功，近源、外壳、首次奇点、缩球、原路径和 G/G-P/G-C。</td></tr></tbody></table><p class="note">科学源提交：fd6fa4b2bcebb702ddc2e8c03884496dca139101；冻结提交：4c52c02026ce0191a121e03241d88fa6573d5536。七份科学源、四份依赖和两份冻结信封按 SHA-256 绑定；AI 与 AJ 共 60 个公式标签。内部实际文件审查不是外部同行评审。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_compact_pressure_work_preflight_20260906.md">AI 紧支撑正压力功</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_short_time_pressure_work_preflight_20260906.md">AJ 统一短窗</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_work_literature-boundary_20260906.md">有限文献边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_work_freeze_audit_20260906.md">最终实际源审查</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_work_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap。独立论文 v2 私有包不在本次发布范围。G OPEN / NOT CLAY。</strong></p></section>
    </article>
    <footer class="footer">CB.9 · Independent HTML research note · ClayB-PressureWorkWindow-20260906 · 2026-09-06</footer>
  </main>'''


EN_MAIN = '''  <main data-language="en">
    <article>
      <header class="hero">
        <div class="kicker">CB.9 · Independent Clay-B analytic note · 2026-09-06</div>
        <h1>CB.9 | Fixed total energy cannot provide this L³ growth budget</h1>
        <p class="dek">For every fixed initial L² energy, construct a family of genuine smooth periodic Navier–Stokes solutions with viscosity one: genuine positive pressure work causes a fixed relative increase of the cubic L³ quantity on a uniform early-time window, while the accumulated squared-gradient action tends to zero. This excludes only one exact estimate with leading factor one, no additive budget, and a constant depending solely on total energy.</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>LITERATURE BOUNDED</span><span>FINITE: NONE</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / Result map</div><h2>Genuine pressure work, not the zero-work residual plateau of CB.8</h2><div class="grid"><div class="card"><strong class="proved">Compact positive pressure work</strong>A periodic positive-pressure-work seed becomes a smooth compactly supported whole-space divergence-free field through curl cutoff and high-frequency pressure modulation.</div><div class="card"><strong class="proved">Uniform genuine growth</strong>At fixed energy, a single bubble retains positive pressure work until tε=τ₀ε^(5/2) and gains a relative amount of H independent of ε.</div><div class="card"><strong class="open">Strict boundary</strong>This is an early-time window for a changing-data family; mature time, one fixed solution's history, first singularities, and contract G remain OPEN.</div></div><p>Unlike the F=0 constant-speed plateau in CB.8, CB.9 controls genuine signed pressure work and net L³ growth.</p></section>
      <section><div class="section-no">02 / AI.1–AI.18</div><h2>From periodic positive pressure work to a compact Euclidean solenoidal field</h2><p>Start with a fixed finite-Fourier periodic divergence-free seed having positive pressure work, take a periodic vector potential, and apply a curl cutoff. Exact solenoidality is preserved. At zero velocity the globally Lipschitz tensor B(z)=z⊗z/|z| is used, with no division by the velocity or cutoff.</p><div class="equation">W_R³(V_N)=N f̄ ∫a⁴+O(1)&gt;0.                                  (AI.18)</div><p>The high-frequency main term of the whole-space pressure multiplier keeps its positive sign. A Schwartz tail controls total frequency zero, while the low-frequency mean pressure and cutoff correction enter the error. The auxiliary modulation field is not presented as an NS velocity.</p></section>
      <section><div class="section-no">03 / AI.19–AI.30</div><h2>A fixed-L²-energy single bubble has genuine initial net growth</h2><p>Normalize one compact positive-pressure-work field V to E₀, then shrink it to one bubble and embed it in the unit torus. The leading scales are</p><div class="equation">H≈ε^(−3/2),  ||∇u||₂²≈ε^(−2),
D≈ε^(−7/2),  W≈ε^(−4),
H′(0)=ε^(−4)W_V−ε^(−7/2)D_V+O(ε^(−1))&gt;0.             (AI.24–AI.28)</div><p>Thus ((H′(0))₊/H)/(1+||∇u||₂²) diverges like ε^(−1/2). This is genuine initial NS pressure work, not a large-residual surrogate, but an instantaneous statement alone is not yet a positive-time window.</p></section>
      <section><div class="section-no">04 / AJ.1–AJ.9</div><h2>An expanding torus turns the physical short window into fixed rescaled time</h2><p>Set L=ε⁻¹ and use y=(x−x₀)/ε, τ=ε^(−5/2)t, and uε=ε^(−3/2)Uε. The viscosity-one equation on the unit torus becomes exactly the low-viscosity equation on the expanding torus</p><div class="equation">∂τUε+Uε·∇Uε+∇Pε=√ε ΔUε,
div Uε=0,  Uε(0)=V_L.                                      (AJ.3–AJ.4)</div><p>The nonnormalized Sobolev norms, lattice-shell count, Leray projection, and pressure zero-mode convention are all explicit. The embedding constants do not grow with L.</p></section>
      <section><div class="section-no">05 / AJ.10–AJ.22</div><h2>A uniform H⁵ lifespan and continuity of positive pressure work</h2><p>Direct Leibniz commutator estimates, a Galerkin construction, and high-order continuation give a uniform τ₁ and H⁵ bound depending only on V. The H³ bound on the time derivative keeps Uε(τ) within O(τ) of its initial datum in H³.</p><div class="equation">sup_(0≤τ≤τ₁)||Uε(τ)||_(H⁵)≤M,
W_L(Uε(τ))≥w₀/2  for 0≤τ≤τ₀.                         (AJ.13, AJ.22)</div><p>The initial Euclidean comparison retains the delta term in the Newtonian Hessian. Positive time uses global torus multipliers and H²-Lipschitz continuity of pressure work, without assuming that the viscous solution remains compactly supported.</p></section>
      <section><div class="section-no">06 / AJ.23–AJ.29</div><h2>Fixed relative H growth with vanishing accumulated gradient action</h2><div class="equation">tε=τ₀ε^(5/2),
Hε(tε)/Hε(0)≥1+δ₀,
∫₀^(tε)||∇uε(t)||₂²dt≤C√ε→0.                         (AJ.27–AJ.28)</div><p>Throughout the window, W(uε(t))≥(w₀/2)ε⁻⁴ and H′ε(t)≥(w₀/4)ε⁻⁴. This is an analytic result for a family of genuine smooth periodic NS solutions, not finite sampling, simulation, or numerical fitting.</p></section>
      <section><div class="section-no">07 / AJ.30</div><h2>Only one estimate with completely fixed quantifiers is excluded</h2><div class="equation">H(t)≤H(0) exp[C(E₀)∫₀ᵗ(1+||∇u(s)||₂²)ds].                 (AJ.30)</div><p>If this held for every corresponding smooth solution from its initial time, with leading factor exactly one, no additive budget, and C depending only on E₀, then its relative increment would tend to zero, contradicting the fixed δ₀. Bounds allowing K&gt;1, an additive budget, or dependence on H(0) or other initial norms are not excluded.</p></section>
      <section><div class="section-no">08 / Literature, evidence, and next question</div><h2>The early-time window must not be presented as mature time</h2><p>Here tε/ε²=τ₀√ε→0, while Hε(0)≈ε⁻³ᐟ² and ||∇uε(0)||₂²≈ε⁻² both diverge. This is a changing-initial-data family, not the first-singularity history of one fixed solution. The next research problem returns to one solution at fixed radius and the mature-time identity for t≥Cε², retaining near-source pressure, outer-shell transport, and viscous payment.</p><table><thead><tr><th>Class</th><th>Scope here</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>AI's compact positive pressure work and fixed-energy initial net growth; AJ's uniform early-time genuine pressure work, fixed relative H growth, and O(√ε) accumulated squared gradient.</td></tr><tr><td>LITERATURE</td><td>Tran–Yu precedes the Lq pressure-work identity and speed moderator. Bourgain–Pavlović and Kang–Yun–Protas concern different spaces, fixed quantities, or numerical objects.</td></tr><tr><td>FINITE COMPUTATION</td><td>None; there is no simulation, numerical certificate, or scientific figure.</td></tr><tr><td>OPEN</td><td>Same-solution pressure work at mature time, near field, outer shell, first singularity, shrinking balls, original paths, and G/G-P/G-C.</td></tr></tbody></table><p class="note">Scientific source commit: fd6fa4b2bcebb702ddc2e8c03884496dca139101; freeze commit: 4c52c02026ce0191a121e03241d88fa6573d5536. Seven scientific sources, four dependencies, and two frozen envelopes are SHA-256-bound; AI and AJ contain 60 formula tags. Internal actual-file review is not external peer review.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_compact_pressure_work_preflight_20260906.md">AI compact positive pressure work</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_short_time_pressure_work_preflight_20260906.md">AJ uniform short window</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_work_literature-boundary_20260906.md">bounded literature boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_work_freeze_audit_20260906.md">final actual-source audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_work_frozen_ledger_20260906.json">portable ledger</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap. The private independent-paper v2 package is outside this release. G OPEN / NOT CLAY.</strong></p></section>
    </article>
    <footer class="footer">CB.9 · Independent HTML research note · ClayB-PressureWorkWindow-20260906 · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-pressure-work-window" aria-labelledby="clay-b-pressure-work-window-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.9 · INDEPENDENT CLAY-B ANALYTIC NOTE · 2026-09-06 · PRESSURE-WORK WINDOW</p><h2 class="route-map-title" id="clay-b-pressure-work-window-title">CB.9｜固定总能量不能给出这条 L³ 增长预算</h2><p class="route-map-intro">紧支撑化保留严格正压力功；固定能量单泡在 tε=τ₀ε^(5/2) 内产生固定比例的真实 L³ 三次方增长，而累计梯度平方为 O(√ε)。这只排除前置系数为 1、无加性预算、常数仅依赖 E₀ 的准确估计；窗口严格早于成熟时间，固定单解、首次奇点和合同 G 仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 压力功窗口笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-pressure-work-window-20260906.html">阅读最新 CB.9 压力功窗口笔记 →</a><a href="/literature-review.html#clay-b-pressure-work-window-boundary">查看文献与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 压力功窗口结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>真实正压力功与净增长：已证</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>固定比例 H 增长；作用量趋零</span><span><i class="route-legend-mark current" aria-hidden="true"></i>早于成熟时间；G OPEN · NOT CLAY</span></div></div></section>'''


CB9_ROW = '''          <div class="tree-row clay-b-pressure-work-window-row">
            <article class="tree-node current">
              <div class="tree-node-head"><span class="route-range">CB.9 · 2026-09-06 · AI/AJ PRESSURE-WORK WINDOW</span><span class="tree-state current">当前路线边界</span></div>
              <h3>CB.9｜紧支撑正压力功与统一早时真实 L³ 增长</h3>
              <p>AI 从固定有限 Fourier 周期种子出发，用 curl cutoff 和受控高频压力调制得到光滑紧支撑的全空间无散场，并在固定 L² 能量的单泡上得到真实初始净增长。其 W、D、H 和 enstrophy 尺度分别为 ε⁻⁴、ε⁻⁷ᐟ²、ε⁻³ᐟ² 和 ε⁻²。</p>
              <p>AJ 在扩张环面上建立与 L 和有效黏性无关的 H⁵ 短时控制，使正压力功维持到 tε=τ₀ε^(5/2)：H(tε)/H(0)≥1+δ₀，而累计梯度平方为 O(√ε)。因此一条量词准确的固定能量指数预算失败；允许额外前置因子、加性预算或初值范数依赖的估计并未被排除。</p>
              <p class="tree-path">CB.8 残差候选失败但不做功 → AI 紧支撑真实正压力功 → 固定能量初始净增长 → AJ 统一早时窗口与固定相对 H 增长 → 成熟时间同一解完整配对 OPEN</p>
              <p><a href="/notes/clay-b-pressure-quotient-20260906.html">CB.8：压力投影与瞬时反检查</a> · <a href="/notes/clay-b-pressure-work-window-20260906.html">CB.9：正压力功与统一早时窗口</a></p>
            </article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发问题：同一解的成熟时间压力功预算</h3><p>固定半径并进入 t≥Cε²，保留近源压力、外壳输运和黏性项，逐项说明时间、空间尺度、初值依赖与可积性来源；不能把变化初值族的早时窗口平移成成熟历史。该问题尚未冻结。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.10 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.9</h3><p>CB.10 只是下一章占位，不是已完成研究。同一固定解在成熟时间的真实压力功、近源、外壳、首次奇点、缩球、原移动路径及 G/G-P/G-C 尚未冻结；不把后续研发写成已证结论。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-pressure-work-window-boundary">CB.9 · Clay-B 正压力功短窗的文献和主张边界</h3><p><a href="https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/12230/Tran_2016_Regularity_AML_AAM.pdf?isAllowed=y&amp;sequence=1">Tran–Yu, accepted manuscript, equations (5)–(8) and Lemma 1</a>已经给出 Lq 压力功恒等式和不贡献该积分的 speed-dependent pressure moderator；这些不是本站的新发现。<a href="https://arxiv.org/pdf/0807.0882">Bourgain–Pavlović, Theorem 1.1</a>处理全空间负阶 Besov 空间的小数据 norm inflation；<a href="https://arxiv.org/pdf/1909.00041">Kang–Yun–Protas, Problem 3.1 and §6</a>固定初始 enstrophy 并数值优化终端 enstrophy。两者都不等同于本章固定初始速度 L² 能量、初始 H 与 enstrophy 发散的早时解族。</p><div class="boundary"><strong>CB.9 · ClayB-PressureWorkWindow-20260906 公开边界</strong><p>PROVED LOCALLY：AI 通过 curl cutoff 和受控压力调制把固定周期正压力功种子转成光滑紧支撑 Euclidean 无散场；固定 E₀ 单泡满足 W≈ε⁻⁴、D≈ε⁻⁷ᐟ²、H≈ε⁻³ᐟ²、||∇u||₂²≈ε⁻²，并有真实初始净增长。AJ 给出扩张环面上一致的 H⁵ 生命周期、压力功连续性和 tε=τ₀ε^(5/2) 窗口，其中 H(tε)/H(0)≥1+δ₀，累计梯度平方为 O(√ε)。因此只排除从初始时刻起、前置系数为 1、无加性预算、C 仅依赖 E₀ 的精确指数估计。STRICT LIMITS：tε/ε²→0，严格早于成熟扩散时间；初始 H 与 enstrophy 发散，且解族随 ε 更换初值；不排除 K&gt;1、加性预算或常数依赖更多初值范数的估计，也不构成一般 L³ norm inflation、固定单解首次奇点或正则性反例。FINITE COMPUTATION：无。OPEN：成熟时间同一解的有符号压力功、近源、外壳、首次奇点、缩球、原路径和 G/G-P/G-C。文献核查有界，不作新颖性、优先权、发表等级或 Clay 声明；无图件、仿真、数值证书或累计 recap。NOT CLAY。<a href="/notes/clay-b-pressure-work-window-20260906.html">阅读完整 CB.9 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-pressure-quotient-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>固定总能量不能给出这条 L³ 增长预算</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 紧支撑正压力功、固定能量单泡与统一早时真实 L³ 增长的双语解析笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    if "h1 { max-width:16ch; overflow-wrap:anywhere;" not in template:
        template = template.replace("h1 { max-width:16ch;", "h1 { max-width:16ch; overflow-wrap:anywhere;", 1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.9 · {DISPLAY_ID}</strong></header>', template, count=1)
    template, count = re.subn(r'  <main data-language="zh">[\s\S]*?  </main>\n\n  <main data-language="en">[\s\S]*?  </main>', ZH_MAIN + "\n\n" + EN_MAIN, template, count=1)
    if count != 1:
        raise RuntimeError("note bilingual template drift")
    return template


def update_home(value: str) -> str:
    value = set_version(value, "综述", refresh=True)
    value = re.sub(r'<strong>v\d+\.\d+</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', value, count=1)
    value, count = re.subn(r'<section class="route-overview independent-release-spotlight"[\s\S]*?</section>', SPOTLIGHT, value, count=1)
    if count != 1:
        raise RuntimeError("independent spotlight drift")
    value = value.replace("CB.1–CB.8", "CB.1–CB.9")
    value = value.replace("speed projection / conditional residual / fixed-energy obstruction / signed pairing", "compact pressure work / uniform early window / mature-time boundary", 1)
    old_focus = "Clay-B 的速率函数压力对全域压力功精确不可见；最佳加权残差的时间积分给出条件延拓接口，但未由能量支付。固定能量单泡排除一条特定瞬时残差候选界，同时揭示 F=0 平台可产生大残差而不做压力功；近源、外壳与合同 G 仍开放。"
    new_focus = "Clay-B 已把真实正压力功保持到统一早时窗口：固定能量单泡取得固定比例的 L³ 三次方增长，而累计梯度平方趋于零。这只排除一条量词精确的候选预算；窗口仍早于成熟扩散时间，同一固定解、近源、外壳与合同 G 继续开放。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")

    if 'class="tree-row clay-b-pressure-work-window-row"' in value:
        if "Clay-B 独立路线停在 CB.9" not in value or "CB.10 · NEXT" not in value:
            raise RuntimeError("existing CB.9 route boundary drift")
        return value

    cb8_start = value.index('<div class="tree-row clay-b-pressure-quotient-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb8_start)
    cb8 = value[cb8_start:boundary_start]
    cb8 = cb8.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb8 = cb8.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb8, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">NEXT TEST COMPLETED</span><h3>真实压力功短窗已进入 CB.9</h3><p>AI/AJ 已把正压力功和净 L³ 增长保持到统一早时窗口；结果见下一个正式路线节点。</p></aside>', cb8, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.8 branch drift")
    value = value[:cb8_start] + cb8 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB9_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-pressure-work-window-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 9
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.9"
    payload["nextIndependentChapter"] = "CB.10"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1",
            "kind": "independent-analytic-note",
            "releaseId": SLUG,
            "displayReleaseId": DISPLAY_ID,
            "chapter": "CB.9",
            "sourceCommit": "fd6fa4b2bcebb702ddc2e8c03884496dca139101",
            "baseCommit": "9771fa5b79b25824ce015c2e9174ae9bc9de6ae7",
            "handoffCommit": "4c52c02026ce0191a121e03241d88fa6573d5536",
            "logicalPredecessor": "ClayB-PressureQuotient-20260906",
            "html": f"public/notes/{SLUG}.html",
            "pdfGenerated": False,
            "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-pressure-work-window-20260906-gate.test.mjs",
            "publicationTest": "tests/clay-b-pressure-work-window-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-pressure-work-window-20260906-translations.mjs",
            "browserQaScript": "scripts/qa-publication-browser.mjs",
            "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False,
            "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE",
            "simulationRequired": False,
            "recapRequired": False,
            "advancesCanonicalR0Series": False,
            "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "GENUINE_POSITIVE_PRESSURE_WORK_AND_NET_L3_GROWTH_PROVED_ON_UNIFORM_EARLY_WINDOW_AT_FIXED_L2_ENERGY_ONLY_PREFACTOR_ONE_NO_ADDITIVE_BUDGET_E0_ONLY_EXPONENTIAL_BOUND_EXCLUDED_WINDOW_PRE_MATURE_CHANGING_DATA_FAMILY_MATURE_TIME_FIRST_SINGULARITY_G_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.9", DISPLAY_ID, "固定总能量不能给出这条 L³ 增长预算", "Fixed total energy cannot provide this L³ growth budget", "tε=τ₀ε^(5/2)", "O(√ε)", "FINITE: NONE", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.9", "Clay-B 独立路线停在 CB.9", "CB.10 · NEXT", 'class="tree-row clay-b-pressure-work-window-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb9 = home.index('class="tree-row clay-b-pressure-work-window-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb9)
    if not (r0_start < r0_boundary < divider < clay_start < cb9 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-pressure-work-window-boundary"' not in literature or "CB.9 · ClayB-PressureWorkWindow-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.9 · {DISPLAY_ID}" not in index or "9 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION:
        raise RuntimeError("version metadata drift")
    if site.get("latestIndependentChapter") != "CB.9" or site.get("nextIndependentChapter") != "CB.10":
        raise RuntimeError("independent chapter metadata drift")
    if manifest.get("latestCompletedRelease") != "r076l" or site.get("latestRelease") != "R0.76L":
        raise RuntimeError("canonical R0 endpoint drift")


if not CHECK_ONLY:
    NOTE_PATH.write_text(build_note(), encoding="utf-8")
    home_path = ROOT / "public/research-review.html"
    home_path.write_text(update_home(home_path.read_text(encoding="utf-8")), encoding="utf-8")
    literature_path = ROOT / "public/literature-review.html"
    literature_path.write_text(update_literature(literature_path.read_text(encoding="utf-8")), encoding="utf-8")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    update_metadata(ROOT / "public/site-version.json")
    update_metadata(ROOT / "research/release-manifest.json")
    subprocess.run([__import__("sys").executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)

validate()
print(json.dumps({"schemaVersion": "clay-b-pressure-work-window-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.9", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
