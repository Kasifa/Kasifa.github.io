#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB PressureMechanismScreen CB.14 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.58"
SLUG = "clay-b-pressure-mechanism-screen-20260906"
DISPLAY_ID = "ClayB-PressureMechanismScreen-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_MAIN = '''  <main data-language="zh">
    <article>
      <header class="hero">
        <div class="kicker">CB.14 · 独立 Clay-B 方法笔记 · 2026-09-06</div>
        <h1>CB.14｜单侧压力机制：周期恒等式与能量类边界</h1>
        <p class="dek">单侧压力判据中的径向空间恒等式可以在零均值周期压力规范下精确重算，固定外尺度的平滑修正由能量支付；但局部环带和时间一致的负压力势仍未得到。基本能量只给尺度一致的时间可积控制，不能自动推出端点控制。这关闭的是一条 energy-only 候选，不是 NS 动力学本身。</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>FINITE CHECKS ONLY</span><span>EXACT SPATIAL IDENTITY</span><span>ENERGY-CLASS OBSTRUCTION</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / 结论地图</div><h2>空间恒等式可以周期化，时间一致压力势不能由基本能量免费获得</h2><div class="grid"><div class="card"><strong class="proved">BF / 精确空间恒等式</strong>规范周期压力满足精确径向恒等式；固定外尺度修正与内尺度 R 无关，并由总能量控制。</div><div class="card"><strong class="open">BF / 未付局部输入</strong>局部环带只有随 R→0 恶化的粗界；单侧压力势的中心、时间一致控制仍是额外假设。</div><div class="card"><strong class="open">BG / 能量类筛查</strong>能量给 L¹_t 尺度一致界和固定 R 的 L_t^(4/3) 界，却不给 L∞_t 或终点有限左迹。</div></div><p>本章没有扩大正则性解类，没有闭合 Q_J 或 G，也没有构造或排除 NS 奇点。</p></section>
      <section><div class="section-no">02 / BF.1–BF.11</div><h2>零均值周期压力满足精确的径向恒等式</h2><p>固定 0&lt;R&lt;r₀/2，在局部提升中分解周期 Green 函数，并保留完整远场和平滑修正，可得</p><div class="equation">∫_(B_R(x₀)) (2p+|u_T|²)/r dx
= R⁻¹∫_(B_R(x₀)) (3p+|u|²) dx
= R² T_R[u].                                      (BF.6)</div><p>修正 C_(r₀,x₀)[u] 与 R 无关，且 |C_(r₀,x₀)[u]|≤C(r₀)||u||₂²。证明使用分布自伴性与调和平均值，不把全空间衰减条件套到周期核上；压力零均值规范不可省略。</p></section>
      <section><div class="section-no">03 / BF.12–BF.15</div><h2>平滑周期修正已付，局部环带和时间输入仍未付</h2><p>能量确实支付 R²|C[u]|≤C(r₀)M²R²；但环带只得到 2M²/R，随 R↓0 恶化，不能把整个右端称为可忽略远场。</p><p>若额外假设某个固定 R₀ 上的中心、时间一致单侧压力势界，非负核心才给 R⁻¹∫_(B_R)|u|² 的统一空间控制。这个结论是条件性的空间代数，不提供原证明后续所需的左连续性、局部能量或小量正则性，也没有建立移动缩球合同 G。</p></section>
      <section><div class="section-no">04 / BG.1–BG.7</div><h2>基本能量给时间可积压力势，而不是时间一致控制</h2><p>对真实的规范周期压力负部 p_-，两套逐时估计为</p><div class="equation">sup_x P_R^-(x) ≤ C R g²,
sup_x P_R^-(x) ≤ C R^(1/2) M^(1/2) g^(3/2).          (BG.5)</div><p>因此 ∫_I sup_(R,x) P_R^-/R≤C∫_I||∇u||₂²，并对每个固定 R 得到 R^(-1/2)sup_x P_R^- 的 L_t^(4/3) 界。两者都是充分上界；本章不声称 4/3 是最优时间指数，也不把严格早于最大光滑时间的逐时连续统一延伸到候选终点。</p></section>
      <section><div class="section-no">05 / BG.8–BG.14</div><h2>固定能量的真实负压力势在场族之间可以任意大</h2><p>一个紧支撑径向旋转种子在中心产生严格负的 Newton 压力。周期缩放保持光滑、无散、零均值和固定 L² 能量，奇异压力为 ε⁻³p_V 加 O(M²) 的周期平滑修正，从而固定 R 上</p><div class="equation">P_R^-(x_*) ≥ c M²/ε → ∞.                            (BG.14)</div><p>这只否定仅依赖能量、对所有场统一的逐时常数。每个固定静态场自身仍有有限并左连续的 C 型压力势；它不是一条 NS 轨道上的条件 C 反例。</p></section>
      <section><div class="section-no">06 / BG.15–BG.22</div><h2>抽象能量关系型时间族没有端点控制，但它明确不是 NS 解</h2><p>取 ε(t)=ε₀(T−t)^α、0&lt;α&lt;1/2，并让能量严格按耗散下降，可构造弱 L² 连续、属于 L∞_tL²_x∩L²_tH¹_x 且满足全局标量能量不等式的无散时间族；其瞬时规范压力势在 T 前发散。</p><p>然而泡核心的涡量空间项全为零，而 A′/A 在临近 T 时为正，直接违反 NS 涡量方程。压力不能修复取 curl 后的矛盾。本章不赋予该族弱 NS、局部能量不等式或 suitable 身份，也不把它写成 NS 反例。</p></section>
      <section><div class="section-no">07 / 原始证明阅读</div><h2>条件 C 的作用发生在时间一致势界与端点传递，而不只是一条空间恒等式</h2><p>本轮完整阅读 Seregin–Šverák 正式发表版 §2–§4，并与相关预印本段落核对。径向恒等式本身不需要条件 C；原证明还使用中心、时间一致的势界、强 L² 左连续性、势的左连续性、局部能量与小量正则性。正式版把预印本远场方向校正为 R→∞，末段使用 ε_*(1)；局部迭代尺度按 θ^kρ 理解。</p><p>外引局部正则性论文没有逐篇全文重审，周期域整套正则性定理也没有导入。这是有界的原始证明机制阅读，不是穷尽新颖性检索或外部同行评审。</p></section>
      <section><div class="section-no">08 / 证据、边界与下一问题</div><h2>energy-only 候选在此停止，下一步只复评真正使用 NS 演化的机制</h2><table><thead><tr><th>类别</th><th>本章范围</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>BF 的规范周期径向恒等式与固定外尺度能量修正；BG 的两套压力势能量界和真实 p_- 集中构造。</td></tr><tr><td>ENERGY-CLASS OBSTRUCTION</td><td>抽象时间族严格阻断从基本能量、弱连续、标量能量关系和瞬时 Poisson 压力到端点势控制的推断；该族不是 NS 解。</td></tr><tr><td>FINITE CHECKS ONLY</td><td>四份文本源、37 个公式编号、74/74 文件哈希、25 项有理复算和负向变异；不替代 PDE 证明。</td></tr><tr><td>OPEN</td><td>真实 NS 是否强制或绕过条件 C，Q_J、带符号净压力功上界、移动缩球 G、一般正则性与 Clay。</td></tr></tbody></table><p class="note">科学源提交：1df0d394d3da2c6ae01b843a86b4830d266148a7；冻结提交：e29c13699b36dd81dd924476bffc5e8ce724f550。七份本轮文件、六十七份依赖和一份冻结 manifest 由 SHA-256 绑定。BF/BG 源稿中的 INTERNAL/PENDING 是推导时状态；当前 PASS 与冻结范围由审核、报告和 manifest 定义。内部模型复核不是外部同行评审。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_periodic_radial_pressure_identity_20260906.md">BF 周期径向恒等式</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_potential_energy_screen_20260906.md">BG 压力势能量筛查</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_mechanism_primary_reading_20260906.md">原始证明阅读记录</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_mechanism_screen_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap；第三方原始 PDF 与私有热演化论文不属于发布资产。G OPEN / NOT CLAY。</strong></p></section>
    </article>
    <footer class="footer">CB.14 · Independent HTML research note · ClayB-PressureMechanismScreen-20260906 · 2026-09-06</footer>
  </main>'''


EN_MAIN = '''  <main data-language="en">
    <article>
      <header class="hero">
        <div class="kicker">CB.14 · Independent Clay-B methods note · 2026-09-06</div>
        <h1>CB.14 | One-sided pressure mechanism: periodic identity and energy-class boundary</h1>
        <p class="dek">The radial spatial identity in the one-sided pressure criterion can be recomputed exactly for normalized periodic pressure, and energy pays the smooth fixed-outer-scale correction. It does not pay the local annulus or time-uniform negative-pressure potential. Basic energy supplies only time-integrable control, not endpoint control. This closes an energy-only candidate, not NS dynamics itself.</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>FINITE CHECKS ONLY</span><span>EXACT SPATIAL IDENTITY</span><span>ENERGY-CLASS OBSTRUCTION</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / Result map</div><h2>The spatial identity transfers to the torus, but basic energy does not provide a time-uniform pressure potential</h2><div class="grid"><div class="card"><strong class="proved">BF / exact spatial identity</strong>Normalized periodic pressure obeys an exact radial identity. The fixed-outer-scale correction is independent of the inner scale R and is controlled by total energy.</div><div class="card"><strong class="open">BF / unpaid local input</strong>The local annulus has only a coarse bound that worsens as R→0. Center- and time-uniform one-sided pressure-potential control remains an extra assumption.</div><div class="card"><strong class="open">BG / energy-class screen</strong>Energy gives a scale-uniform L¹_t bound and a fixed-R L_t^(4/3) bound, but no L∞_t control or finite endpoint left trace.</div></div><p>This chapter neither enlarges a regularity class nor closes Q_J or G, and it neither constructs nor excludes an NS singularity.</p></section>
      <section><div class="section-no">02 / BF.1–BF.11</div><h2>Normalized periodic pressure satisfies an exact radial identity</h2><p>Fix 0&lt;R&lt;r₀/2. Splitting the periodic Green function in a local lift and retaining the full far-field and smooth corrections gives</p><div class="equation">∫_(B_R(x₀)) (2p+|u_T|²)/r dx
= R⁻¹∫_(B_R(x₀)) (3p+|u|²) dx
= R² T_R[u].                                      (BF.6)</div><p>The correction C_(r₀,x₀)[u] is independent of R and satisfies |C_(r₀,x₀)[u]|≤C(r₀)||u||₂². The proof uses distributional self-adjointness and harmonic averaging, not whole-space decay imposed on the periodic kernel. The zero-mean pressure normalization is essential.</p></section>
      <section><div class="section-no">03 / BF.12–BF.15</div><h2>The smooth periodic correction is paid, while the local annulus and temporal input remain unpaid</h2><p>Energy does pay R²|C[u]|≤C(r₀)M²R². The annulus, however, has only the bound 2M²/R, which worsens as R↓0; the entire right-hand side cannot be called a negligible far field.</p><p>Only after assuming a center- and time-uniform one-sided pressure-potential bound at one fixed R₀ does the nonnegative core yield uniform spatial control of R⁻¹∫_(B_R)|u|². This is conditional spatial algebra. It supplies none of the left continuity, local energy, or smallness regularity needed later in the original proof, and it does not establish the moving shrinking-ball contract G.</p></section>
      <section><div class="section-no">04 / BG.1–BG.7</div><h2>Basic energy makes the pressure potential time-integrable, not time-uniform</h2><p>For the genuine negative part p_- of normalized periodic pressure, two pointwise estimates are</p><div class="equation">sup_x P_R^-(x) ≤ C R g²,
sup_x P_R^-(x) ≤ C R^(1/2) M^(1/2) g^(3/2).          (BG.5)</div><p>Hence ∫_I sup_(R,x) P_R^-/R≤C∫_I||∇u||₂², while each fixed R gives an L_t^(4/3) bound for R^(-1/2)sup_x P_R^-. These are sufficient bounds. The chapter does not claim that 4/3 is the optimal time exponent, nor does it extend pointwise continuity strictly before the maximal smooth time uniformly to a candidate endpoint.</p></section>
      <section><div class="section-no">05 / BG.8–BG.14</div><h2>Genuine negative-pressure potential can grow arbitrarily large across a fixed-energy family</h2><p>A compactly supported radial rotation seed creates strictly negative Newton pressure at its center. Periodic scaling preserves smoothness, divergence freedom, zero mean, and fixed L² energy. Singular pressure is ε⁻³p_V plus an O(M²) smooth periodic correction, so at fixed R</p><div class="equation">P_R^-(x_*) ≥ c M²/ε → ∞.                            (BG.14)</div><p>This rules out only a pointwise constant depending solely on energy and uniform over all fields. Each fixed static field still has a finite, left-continuous condition-C-type pressure potential. It is not a counterexample to condition C along an NS trajectory.</p></section>
      <section><div class="section-no">06 / BG.15–BG.22</div><h2>An abstract energy-relation time family lacks endpoint control, but it is explicitly not an NS solution</h2><p>Taking ε(t)=ε₀(T−t)^α with 0&lt;α&lt;1/2 and making energy decay exactly by dissipation produces a weakly L²-continuous, divergence-free family in L∞_tL²_x∩L²_tH¹_x that satisfies a global scalar energy inequality. Its instantaneous normalized pressure potential diverges before T.</p><p>In the bubble core, however, every spatial term in the vorticity equation vanishes while A′/A is positive near T, directly violating the NS vorticity equation. Pressure cannot repair the contradiction after taking curl. The chapter assigns the family no weak-NS, local-energy-inequality, or suitable status and does not call it an NS counterexample.</p></section>
      <section><div class="section-no">07 / Primary-proof reading</div><h2>Condition C acts through time-uniform potential control and endpoint transfer, not merely through one spatial identity</h2><p>This round reads §§2–4 of the published Seregin–Šverák paper in full and checks the corresponding preprint portions. The radial identity itself does not use condition C. The proof also uses center- and time-uniform potential control, strong L² left continuity, left continuity of the potential, local energy, and an epsilon-regularity step. The published version corrects the preprint's far-field direction to R→∞ and uses ε_*(1) at the end; the local iteration scale is read as θ^kρ.</p><p>The externally cited local-regularity papers were not individually reread in full, and the complete regularity theorem was not imported to the periodic setting. This is a bounded primary-proof mechanism review, not an exhaustive novelty search or external peer review.</p></section>
      <section><div class="section-no">08 / Evidence, boundary, and next question</div><h2>The energy-only candidate stops here; the next review retains only mechanisms that genuinely use NS evolution</h2><table><thead><tr><th>Class</th><th>Scope here</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>BF's normalized periodic radial identity and fixed-outer-scale energy correction; BG's two energy bounds for pressure potential and genuine p_- concentration construction.</td></tr><tr><td>ENERGY-CLASS OBSTRUCTION</td><td>The abstract time family strictly blocks inference from basic energy, weak continuity, a scalar energy relation, and instantaneous Poisson pressure to endpoint potential control; it is not an NS solution.</td></tr><tr><td>FINITE CHECKS ONLY</td><td>Four text sources, 37 formula labels, 74/74 file hashes, 25 rational recomputations, and negative mutations; none replaces PDE proof.</td></tr><tr><td>OPEN</td><td>Whether genuine NS forces or bypasses condition C, Q_J, the signed net pressure-work upper bound, moving shrinking G, general regularity, and Clay.</td></tr></tbody></table><p class="note">Scientific source commit: 1df0d394d3da2c6ae01b843a86b4830d266148a7; freeze commit: e29c13699b36dd81dd924476bffc5e8ce724f550. Seven current files, sixty-seven dependencies, and one frozen manifest are SHA-256-bound. INTERNAL/PENDING in the BF/BG source drafts records derivation-time states; the audit, report, and manifest define the present PASS and frozen scope. Internal model review is not external peer review.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_periodic_radial_pressure_identity_20260906.md">BF periodic radial identity</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_potential_energy_screen_20260906.md">BG pressure-potential energy screen</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_mechanism_primary_reading_20260906.md">primary-proof reading record</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_mechanism_screen_frozen_ledger_20260906.json">portable ledger</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap. Third-party source PDFs and the private heat-evolution paper are not publication assets. G OPEN / NOT CLAY.</strong></p></section>
    </article>
    <footer class="footer">CB.14 · Independent HTML research note · ClayB-PressureMechanismScreen-20260906 · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-pressure-mechanism-screen" aria-labelledby="clay-b-pressure-mechanism-screen-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.14 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · PRESSURE MECHANISM SCREEN</p><h2 class="route-map-title" id="clay-b-pressure-mechanism-screen-title">CB.14｜单侧压力机制：周期恒等式与能量类边界</h2><p class="route-map-intro">规范周期压力的径向空间恒等式可以精确重算，固定外尺度修正由能量支付；局部环带和时间一致负压力势仍未付。基本能量只给时间可积控制。一个抽象端点反检查明确不是 NS 解，因此本轮停止 energy-only 候选，而不排除真实 NS 动力学。G OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 压力机制筛查笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-pressure-mechanism-screen-20260906.html">阅读最新 CB.14 压力机制筛查笔记 →</a><a href="/literature-review.html#clay-b-pressure-mechanism-screen-boundary">查看原始证明与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 压力机制筛查结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>周期径向恒等式精确成立</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>energy-only 端点推断停止</span><span><i class="route-legend-mark current" aria-hidden="true"></i>真实 NS 机制、Q_J 与 G OPEN · NOT CLAY</span></div></div></section>'''


CB14_ROW = '''          <div class="tree-row clay-b-pressure-mechanism-screen-row">
            <article class="tree-node current">
              <div class="tree-node-head"><span class="route-range">CB.14 · 2026-09-06 · BF–BG PRESSURE MECHANISM SCREEN</span><span class="tree-state current">当前路线边界</span></div>
              <h3>CB.14｜单侧压力机制：周期恒等式与能量类边界</h3>
              <p>BF 在零均值周期压力规范下精确重算径向恒等式：固定外尺度平滑修正由总能量支付，但局部环带仍只有随内尺度恶化的粗界，时间一致单侧压力势仍是额外输入。</p>
              <p>BG 给真实 p_- 势的尺度一致 L¹_t 与固定尺度 L_t^(4/3) 界，并以明确非 NS 的抽象能量时间族阻断端点推断；这不构成 NS 反例，也不宣称 4/3 最优。</p>
              <p class="tree-path">CB.13 近期源 norm 路线停止 → BF 周期径向恒等式 → 固定外尺度修正已付、局部环带未付 → BG 能量类仅给时间可积 → 非 NS 抽象端点反检查 → energy-only 候选停止</p>
              <p><a href="/notes/clay-b-recent-source-screen-20260906.html">CB.13：近期源筛查</a> · <a href="/notes/clay-b-pressure-mechanism-screen-20260906.html">CB.14：压力机制筛查</a></p>
            </article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发问题：有界路线重评</h3><p>只保留真正使用 NS 演化、尚未落入既有范数成本的候选。每条必须提出明确的新不等式或紧性/刚性命题及其缺失输入；否则不另起章节或计算任务。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.15 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.14</h3><p>CB.15 只是下一章占位，不是已完成研究。真正使用 NS 演化的新机制、Q_J、近期源带符号净压力功上界、条件 C 的动态强制或绕过、移动缩球 G/G-P/G-C 与首次奇点排除均未冻结。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-pressure-mechanism-screen-boundary">CB.14 · Clay-B 单侧压力机制的文献和主张边界</h3><p>本轮完整阅读 <a href="https://www.pdmi.ras.ru/~seregin/Recent%20Publications/Pres.pdf">Seregin–Šverák 正式发表版作者副本</a> 的 §2–§4（PDF 第 3–20 页、期刊第 67–84 页），并核对 <a href="https://files-www.mis.mpg.de/mpi-typo3/preprints/2001/preprint2001_92.pdf">MiS 92/2001 预印本</a> 的相关 §2–§4；书目信息由 <a href="https://doi.org/10.1007/s002050200199">DOI 10.1007/s002050200199</a> 与机构页交叉确认。原文径向恒等式本身不需要条件 C；后续还使用中心、时间一致压力势界、强 L² 左连续性、势的左连续性、局部能量和小量正则性。正式版的远场极限按 R→∞、末段按 ε_*(1) 核对，局部迭代尺度按 θ^kρ 理解。外引正则性论文未逐篇全文重审，整套全空间定理没有导入周期能量框架，也未做穷尽新颖性检索。</p><div class="boundary"><strong>CB.14 · ClayB-PressureMechanismScreen-20260906 公开边界</strong><p>PROVED LOCALLY：BF 精确重算规范周期压力的径向空间恒等式，固定外尺度平滑修正由能量支付，但局部环带与时间一致单侧压力势未付。ENERGY-CLASS OBSTRUCTION：BG 给真实 p_- 势的尺度一致 L¹_t 与固定 R 的 L_t^(4/3) 上界；一个弱连续、满足全局标量能量不等式的抽象时间族具有发散端点势，但它直接违反 NS 涡量方程，不是弱 NS、suitable 解或 NS 反例。两套能量界不宣称最优时间指数。FINITE CHECKS ONLY：四份文本源、37 个公式编号、74/74 文件哈希、25 项有理复算与负向变异不替代证明。OPEN：真实 NS 是否强制或绕过条件 C，Q_J、净压力功上界、移动缩球 G 与一般正则性。没有完整新颖性审查、外部同行评审或 Clay 声明，无图件、仿真或累计 recap。NOT CLAY。<a href="/notes/clay-b-pressure-mechanism-screen-20260906.html">阅读完整 CB.14 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-recent-source-screen-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>单侧压力机制：周期恒等式与能量类边界</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 单侧压力机制的周期径向恒等式、真实负压力势能量界与非 NS 端点反检查的双语方法笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.14 · {DISPLAY_ID}</strong></header>', template, count=1)
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
    value = value.replace("CB.1–CB.13", "CB.1–CB.14")
    value = value.replace("recent-source energy / dyadic cost / static comparison", "periodic pressure identity / energy-class endpoint screen", 1)
    old_focus = "Clay-B 已完成近期源的一轮有限方法筛查：R 的积分 H¹ 能量趋零，但原测试所需 Q_J 未证；逐块绝对值/Young 路线留下正频率矩，静态背景只复制旧压力支付指数。该 norm 路线停止，带符号上界、缩球路径和合同 G 继续开放。"
    new_focus = "Clay-B 已完成单侧压力机制的一轮有界筛查：周期径向恒等式精确成立，固定外尺度修正由能量支付；基本能量只给负压力势的时间可积控制，抽象端点反检查明确不是 NS 解。energy-only 候选停止，真实 NS 机制、Q_J 和合同 G 继续开放。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    if 'class="tree-row clay-b-pressure-mechanism-screen-row"' in value:
        if "Clay-B 独立路线停在 CB.14" not in value or "CB.15 · NEXT" not in value:
            raise RuntimeError("existing CB.14 route boundary drift")
        return value
    cb13_start = value.index('<div class="tree-row clay-b-recent-source-screen-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb13_start)
    cb13 = value[cb13_start:boundary_start]
    cb13 = cb13.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb13 = cb13.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb13, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">MECHANISM SCREEN COMPLETED</span><h3>周期压力机制筛查已进入 CB.14</h3><p>BF–BG 已区分精确空间恒等式、固定外尺度能量修正、未付局部环带、时间可积压力势与明确非 NS 的端点反检查；结果见下一个正式路线节点。</p></aside>', cb13, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.13 branch drift")
    value = value[:cb13_start] + cb13 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB14_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-pressure-mechanism-screen-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 14
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.14"
    payload["nextIndependentChapter"] = "CB.15"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note",
            "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.14",
            "sourceCommit": "1df0d394d3da2c6ae01b843a86b4830d266148a7", "baseCommit": "bbb7074c4eb4f6b5955460a49c44db347a9b6ba8",
            "handoffCommit": "e29c13699b36dd81dd924476bffc5e8ce724f550", "logicalPredecessor": "ClayB-RecentSourceScreen-20260906",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False, "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-pressure-mechanism-screen-20260906-gate.test.mjs", "publicationTest": "tests/clay-b-pressure-mechanism-screen-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-pressure-mechanism-screen-20260906-translations.mjs", "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE", "simulationRequired": False, "recapRequired": False,
            "advancesCanonicalR0Series": False, "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "PERIODIC_RADIAL_PRESSURE_IDENTITY_EXACT_FIXED_OUTER_CORRECTION_ENERGY_PAID_LOCAL_ANNULUS_AND_TIME_UNIFORM_NEGATIVE_PRESSURE_POTENTIAL_UNPAID_ENERGY_ONLY_ENDPOINT_INFERENCE_BLOCKED_BY_EXPLICIT_NON_NS_FAMILY_NO_OPTIMAL_TIME_EXPONENT_CLAIM_G_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.14", DISPLAY_ID, "单侧压力机制：周期恒等式与能量类边界", "One-sided pressure mechanism: periodic identity and energy-class boundary", "PROVED", "FINITE", "EXACT SPATIAL IDENTITY", "ENERGY-CLASS OBSTRUCTION", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.14", "Clay-B 独立路线停在 CB.14", "CB.15 · NEXT", 'class="tree-row clay-b-pressure-mechanism-screen-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb14 = home.index('class="tree-row clay-b-pressure-mechanism-screen-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb14)
    if not (r0_start < r0_boundary < divider < clay_start < cb14 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-pressure-mechanism-screen-boundary"' not in literature or "CB.14 · ClayB-PressureMechanismScreen-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.14 · {DISPLAY_ID}" not in index or "14 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.14" or site.get("nextIndependentChapter") != "CB.15":
        raise RuntimeError("version or chapter metadata drift")
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
    subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)

validate()
print(json.dumps({"schemaVersion": "clay-b-pressure-mechanism-screen-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.14", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
