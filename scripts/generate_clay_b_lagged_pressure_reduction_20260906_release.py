#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB LaggedPressureReduction CB.12 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.56"
SLUG = "clay-b-lagged-pressure-reduction-20260906"
DISPLAY_ID = "ClayB-LaggedPressureReduction-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_MAIN = '''  <main data-language="zh">
    <article>
      <header class="hero">
        <div class="kicker">CB.12 · 独立 Clay-B 方法笔记 · 2026-09-06</div>
        <h1>CB.12｜旧热背景可以移走，近期源项仍待估计</h1>
        <p class="dek">在 AQ 原来的同一解、早时点、坏集、权重和积分域上，把 Duhamel 热起点放到窗口之前，就能用一份明确的负耗散与低阶余项支付所有含旧热分量的压力。必要净工作因此缩减到近期真实非线性源的自压力；这仍是条件下界，不是矛盾上界。</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>FINITE CHECKS ONLY</span><span>CONDITIONAL REDUCTION</span><span>SUFFICIENT SCALE ONLY</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / 结论地图</div><h2>时间滞后支付旧压力，但没有支付近期源自压力</h2><div class="grid"><div class="card"><strong class="open">AY / AZ 方法成本</strong>从压力窗口内部起算时，绝对值估计留下热耗散相关项或 A_J²Λ 的速率缺口。</div><div class="card"><strong class="proved">BA / BB 正面缩减</strong>窗口前的真实热滞后将旧压力控制为 εDχ+o(H_t)，并保留原压力测试。</div><div class="card"><strong class="open">剩余对象</strong>近期源积分 R 的自压力减剩余耗散仍只有条件必要下界，没有上界。</div></div><p>本章不构造大范数序列、NS 轨道或奇点，也不把一个充分滞后指数写成必要尺度或最优尺度。</p></section>
      <section><div class="section-no">02 / 固定对象与两个起点</div><h2>AQ 的压力积分起点没有被 Duhamel 起点替换</h2><p>始终保留同一周期 NS 解、固定环带、K=Λ_A^(3/4)、AQ 实际选择的 s_J、μ_J、坏集与 [s_J,t]。热展开另从窗口前的</p><div class="equation">a=t−δ−τ,    δ=c₀r²Λ_A⁻⁴,    a&lt;s_J&lt;t</div><p>起算。a 只服务于热分解，不是新的局部能量低值点；R 保留 Leray 投影、散度以及低低、低高和高高全部真实非线性源。</p></section>
      <section><div class="section-no">03 / AY.1–AY.33</div><h2>从原 s_J 展开：分拆增加相关成本，重组返回 AW</h2><p>AY 写全初始—初始、初始—源和源—源三类压力的相位、输出分母、源导数及 Volterra 时间顺序。逐类作充分绝对值估计会留下热耗散密度与实际耗散密度的相关项及原 g⁴ 成本；先把三类重组为真实高频场，则精确回到 AW 的界。</p><div class="equation">|Kχ(p_h)| ≤ Cχ(M²g²+g⁴).                         (AY.33)</div><p>这次检查没有给 AQ 上界，但也不是所有带符号动力学路线的 no-go。</p></section>
      <section><div class="section-no">04 / AZ.1–AZ.23</div><h2>联合早时点合法，但纯热绝对值界仍缺速率</h2><p>AZ 在同一窗口前半联合选出局部三次能量低值和平均尺度梯度界，并从该新点重新推导权重；它没有把新点冒充 AQ 原 s_J。纯热压力保留原测试后得到</p><div class="equation">H_t⁻¹∫ μ_(J,a)|Kχ(p_bb)| ≤ C(M⁴Λ_A⁻³+A_J²Λ_A).       (AZ.23)</div><p>能量只给 A_J=o(1)，不支付 A_J²Λ_A。这里的小量要求只是该估计的充分成本，不是 NS 必要条件。</p></section>
      <section><div class="section-no">05 / BA.1–BA.17</div><h2>窗口前真实热滞后可以支付含旧分量的压力</h2><p>BA 取 τ=Λ_A⁻¹，使热分量在 J 上具有真实滞后。精确分解 p_h=p(R)+p_old 后，用有限 L³ 双 Riesz、原加权测试与一次 Young 吸收得到</p><div class="equation">Kχ(p_old) ≤ εDχ+E_J,    H_t⁻¹∫μ_JE_J→0.             (BA.12–14)</div><p>εDχ 是真实成本且只能使用一次。因此本章没有证明旧压力功自身是 o(H_t)，而是用一份耗散加 o(H_t) 支付它。</p></section>
      <section><div class="section-no">06 / BB.1–BB.25</div><h2>精确重组给出更短的充分滞后尺度</h2><p>BB 先验证固定倍数 K⁻² 已支付粗 Young 账本的五项余项，即使热背景并不一致小。再用</p><div class="equation">p_old=Π(b,h)−p(b),    τ=Λ_A⁻⁸ᐟ³=K⁻³²ᐟ⁹             (BB.14, BB.22)</div><p>以及纯热压力梯度的 Fourier 绝对和界，缩短一条可证明的充分滞后。指数 −8/3 不是必要性、最优性或成熟时间定理；R 也不是自由小残差或无强迫 NS 解。</p></section>
      <section><div class="section-no">07 / 条件必要性缩减</div><h2>必要净工作只被定位到近期真实源，并未得到上界</h2><p>对任意预先固定 0&lt;ε&lt;3/4，旧压力支付代回 AQ.8 只推出</p><div class="equation">liminf H_t⁻¹∫_[s_J,t] μ_J[Kχ(p(R))−(3/4−ε)Dχ] ds ≥ 1.   (BB.25)</div><p>不等号方向来自旧压力的单侧上界。这是源自压力减剩余耗散的条件必要下界，不是 p(R) 的上界，也不与 AQ 构成矛盾。原合法序列是否存在仍未证明。</p></section>
      <section><div class="section-no">08 / 文献、证据与下一问题</div><h2>下一步只检查近期源积分是否真的带来动力学收益</h2><p>下一检查固定 ε=1/8，并在原 [s_J,t] 上审查 Kχ(p(R))−5Dχ/8；任何耗散吸收都只能从剩余 5/8 扣除。若 dyadic 或 Volterra 展开只返回 AW/AY 的 g⁴ 成本、未付临界范数或另一个时间速率，就停止该项并复评问题选择。</p><table><thead><tr><th>类别</th><th>本章范围</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>AY/AZ 的方法成本边界；BA/BB 对旧压力的耗散支付与条件必要性缩减。</td></tr><tr><td>FINITE CHECKS ONLY</td><td>八份文本源、98 个公式编号、51/51 字节核验及 Fraction 指数账本；不替代 PDE 证明。</td></tr><tr><td>LITERATURE INPUT</td><td>有限读取 Tao arXiv:1908.04958v2 的指定陈述和 (3.7)–(3.15)；不调用其临界有界正则性定理。</td></tr><tr><td>CONDITIONAL / OPEN</td><td>近期源自压力上界、实际 NS 输入、移动缩球 G、奇点排除与一般正则性仍开放。</td></tr></tbody></table><p class="note">科学源提交：891e6b85f53ae19272973c191726f1278e47918b；冻结提交：3501cf9d70cbb5140186bb18d0cf1da8c110480f。十份源、四十一份依赖与一份冻结 manifest 按 SHA-256 绑定。原 AY–BB 的 INTERNAL/PENDING 是推导时状态；当前 PASS 与冻结范围由审查、报告和 manifest 定义。内部实际文件审查不是外部同行评审或完整新颖性审查。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_time_ordered_pressure_preflight_20260906.md">AY 时间有序筛查</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_joint_early_heat_work_preflight_20260906.md">AZ 联合早时点</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_lagged_heat_pressure_reduction_preflight_20260906.md">BA 真实热滞后</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_lag_scale_pressure_budget_preflight_20260906.md">BB 滞后尺度</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_lagged_pressure_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap；私有热边缘论文不在本次发布范围。G OPEN / NOT CLAY。</strong></p></section>
    </article>
    <footer class="footer">CB.12 · Independent HTML research note · ClayB-LaggedPressureReduction-20260906 · 2026-09-06</footer>
  </main>'''


EN_MAIN = '''  <main data-language="en">
    <article>
      <header class="hero">
        <div class="kicker">CB.12 · Independent Clay-B methods note · 2026-09-06</div>
        <h1>CB.12 | The old heat background can be removed; the recent source remains</h1>
        <p class="dek">For AQ's same solution, early time, bad set, weight, and integration interval, placing the Duhamel heat start before the window pays every pressure term containing the old heat component by one explicit share of negative dissipation plus lower-order errors. The necessary work is thereby reduced to the self-pressure of the recent genuine nonlinear source. This remains a conditional lower bound, not a contradictory upper bound.</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>FINITE CHECKS ONLY</span><span>CONDITIONAL REDUCTION</span><span>SUFFICIENT SCALE ONLY</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / Result map</div><h2>Time lag pays the old pressure but not the recent source pressure</h2><div class="grid"><div class="card"><strong class="open">AY / AZ method costs</strong>Starting inside the pressure window leaves either a heat/actual-dissipation correlation or an A_J²Λ rate gap after absolute-value estimates.</div><div class="card"><strong class="proved">BA / BB reduction</strong>A genuine heat lag before the window controls old pressure by εDχ+o(H_t), with the original pressure test retained.</div><div class="card"><strong class="open">Remaining object</strong>The self-pressure of the recent source integral R minus the remaining dissipation has only a conditional necessary lower bound and no upper bound.</div></div><p>This chapter constructs no large-norm sequence, NS trajectory, or singularity, and it does not present a sufficient lag exponent as necessary or optimal.</p></section>
      <section><div class="section-no">02 / Fixed objects and two starting times</div><h2>The AQ pressure-integration start is not replaced by the Duhamel start</h2><p>The same periodic NS solution, fixed annulus, K=Λ_A^(3/4), AQ's actual s_J, μ_J, bad set, and [s_J,t] are retained throughout. The heat expansion starts separately before the window at</p><div class="equation">a=t−δ−τ,    δ=c₀r²Λ_A⁻⁴,    a&lt;s_J&lt;t.</div><p>The time a serves only the heat decomposition; it is not a new local-energy low point. The term R retains the Leray projection, divergence, and all genuine low–low, low–high, and high–high nonlinear sources.</p></section>
      <section><div class="section-no">03 / AY.1–AY.33</div><h2>Starting at the original s_J: splitting adds a correlation cost, recombination returns AW</h2><p>AY records the phases, output denominator, source derivative, and Volterra time order for initial–initial, initial–source, and source–source pressure. Separate sufficient absolute-value estimates retain a correlation between heat dissipation and actual dissipation, together with the old g⁴ cost. Recombining the three pieces into the actual high-frequency field returns exactly the AW bound.</p><div class="equation">|Kχ(p_h)| ≤ Cχ(M²g²+g⁴).                         (AY.33)</div><p>The check gives no AQ upper bound, but it is not a no-go theorem for every signed dynamical route.</p></section>
      <section><div class="section-no">04 / AZ.1–AZ.23</div><h2>A joint early time is legal, but the pure-heat absolute bound still lacks a rate</h2><p>AZ jointly selects a local-cubic-energy low point and an average-scale gradient bound in the first half of the same window, then rederives the weight from that new point. It does not identify this time with AQ's original s_J. With the original test retained, pure-heat pressure obeys</p><div class="equation">H_t⁻¹∫ μ_(J,a)|Kχ(p_bb)| ≤ C(M⁴Λ_A⁻³+A_J²Λ_A).       (AZ.23)</div><p>Energy yields only A_J=o(1), which does not pay A_J²Λ_A. This smallness request is a sufficient cost of the estimate, not an NS necessity.</p></section>
      <section><div class="section-no">05 / BA.1–BA.17</div><h2>A genuine heat lag before the window pays pressure containing the old component</h2><p>BA takes τ=Λ_A⁻¹, so the heat component has a genuine lag throughout J. After the exact decomposition p_h=p(R)+p_old, finite-L³ double Riesz bounds, the original weighted test, and one Young absorption give</p><div class="equation">Kχ(p_old) ≤ εDχ+E_J,    H_t⁻¹∫μ_JE_J→0.             (BA.12–14)</div><p>The εDχ share is a real cost and can be used only once. Thus the chapter does not prove that old pressure work itself is o(H_t); it pays old pressure with one dissipation share plus o(H_t).</p></section>
      <section><div class="section-no">06 / BB.1–BB.25</div><h2>Exact regrouping gives a shorter sufficient lag scale</h2><p>BB first verifies that a fixed multiple of K⁻² pays all five remainders in the coarse Young ledger even when the heat background is not uniformly small. It then uses</p><div class="equation">p_old=Π(b,h)−p(b),    τ=Λ_A⁻⁸ᐟ³=K⁻³²ᐟ⁹             (BB.14, BB.22)</div><p>together with a Fourier absolute-sum bound for the pure-heat pressure gradient to shorten one provable sufficient lag. The exponent −8/3 is neither necessary nor optimal, nor a mature-time theorem. The term R is not a freely small remainder or an unforced NS solution.</p></section>
      <section><div class="section-no">07 / Conditional necessary reduction</div><h2>Necessary work is only localized to the recent genuine source; no upper bound is obtained</h2><p>For every fixed 0&lt;ε&lt;3/4, substituting the old-pressure payment into AQ.8 yields only</p><div class="equation">liminf H_t⁻¹∫_[s_J,t] μ_J[Kχ(p(R))−(3/4−ε)Dχ] ds ≥ 1.   (BB.25)</div><p>The direction comes from a one-sided upper bound on old pressure. This is a conditional necessary lower bound for source pressure minus the remaining dissipation, not an upper bound for p(R), and it does not contradict AQ. Existence of the original legal sequence remains unproved.</p></section>
      <section><div class="section-no">08 / Literature, evidence, and next question</div><h2>The next step asks only whether the recent source integral has a genuine dynamical gain</h2><p>The next check fixes ε=1/8 and studies Kχ(p(R))−5Dχ/8 on the original [s_J,t]. Any new dissipation absorption must be deducted from the remaining 5/8. If a dyadic or Volterra expansion only returns the AW/AY g⁴ cost, an unpaid critical norm, or another time-rate assumption, the check stops and the problem choice is reassessed.</p><table><thead><tr><th>Class</th><th>Scope here</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>The AY/AZ method-cost boundaries and the BA/BB dissipation payment and conditional reduction for old pressure.</td></tr><tr><td>FINITE CHECKS ONLY</td><td>Eight text sources, 98 numbered formulas, 51/51 byte checks, and a Fraction exponent ledger; none replaces PDE proof.</td></tr><tr><td>LITERATURE INPUT</td><td>Limited reading of specified statements and (3.7)–(3.15) in Tao arXiv:1908.04958v2; its critically bounded regularity theorem is not invoked.</td></tr><tr><td>CONDITIONAL / OPEN</td><td>A recent-source pressure upper bound, actual NS inputs, moving shrinking G, singularity exclusion, and general regularity remain open.</td></tr></tbody></table><p class="note">Scientific source commit: 891e6b85f53ae19272973c191726f1278e47918b; freeze commit: 3501cf9d70cbb5140186bb18d0cf1da8c110480f. Ten source files, forty-one dependencies, and one frozen manifest are SHA-256-bound. The INTERNAL/PENDING labels in the original AY–BB drafts are derivation-time states; the audit, report, and manifest define the current PASS and frozen scope. Internal actual-file review is neither external peer review nor a complete novelty audit.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_time_ordered_pressure_preflight_20260906.md">AY time-ordered screen</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_joint_early_heat_work_preflight_20260906.md">AZ joint early time</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_lagged_heat_pressure_reduction_preflight_20260906.md">BA genuine heat lag</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_lag_scale_pressure_budget_preflight_20260906.md">BB lag scale</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_lagged_pressure_frozen_ledger_20260906.json">portable ledger</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap. The private heat-edge paper is outside this release. G OPEN / NOT CLAY.</strong></p></section>
    </article>
    <footer class="footer">CB.12 · Independent HTML research note · ClayB-LaggedPressureReduction-20260906 · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-lagged-pressure-reduction" aria-labelledby="clay-b-lagged-pressure-reduction-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.12 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · LAGGED PRESSURE REDUCTION</p><h2 class="route-map-title" id="clay-b-lagged-pressure-reduction-title">CB.12｜旧热背景可以移走，近期源项仍待估计</h2><p class="route-map-intro">保持 AQ 原 s_J、坏集、权重与积分域，在窗口前另设 Duhamel 热起点，可把旧压力控制为一份 εDχ 加 o(H_t)。必要净工作缩减到近期真实源自压力减剩余耗散；这仍是条件下界，不是上界。τ=Λ_A⁻⁸ᐟ³ 只是充分选择，近期源上界与 G 仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 滞后压力缩减笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-lagged-pressure-reduction-20260906.html">阅读最新 CB.12 滞后压力缩减笔记 →</a><a href="/literature-review.html#clay-b-lagged-pressure-reduction-boundary">查看文献与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 滞后压力缩减结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>旧压力：εDχ+o(H_t) 已付</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>τ=Λ_A⁻⁸ᐟ³：充分尺度</span><span><i class="route-legend-mark current" aria-hidden="true"></i>近期源上界与 G OPEN · NOT CLAY</span></div></div></section>'''


CB12_ROW = '''          <div class="tree-row clay-b-lagged-pressure-reduction-row">
            <article class="tree-node current">
              <div class="tree-node-head"><span class="route-range">CB.12 · 2026-09-06 · AY–BB LAGGED PRESSURE REDUCTION</span><span class="tree-state current">当前路线边界</span></div>
              <h3>CB.12｜旧热压力的耗散支付与近期源条件下界</h3>
              <p>AY/AZ 保留压力窗口内部起点时，分别留下热—实际耗散相关项或 A_J²Λ_A 的充分速率缺口；这些方法成本不是一般动力学 no-go。</p>
              <p>BA/BB 在窗口前设置独立热起点，保持 AQ 原 s_J、坏集、μ_J 和 [s_J,t]。精确重组后，旧压力由一份 εDχ 和 o(H_t) 支付；τ=Λ_A⁻⁸ᐟ³=K⁻³²ᐟ⁹ 只是充分选择。剩余近期源自压力减耗散只有条件必要下界。</p>
              <p class="tree-path">CB.11 原测试匹配界 → AY 原起点分拆成本 → AZ 联合早时速率缺口 → BA 窗口前真实热滞后 → BB 精确重组与充分尺度 → 近期源自压力上界 OPEN</p>
              <p><a href="/notes/clay-b-pressure-test-coupling-20260906.html">CB.11：压力与测试配对</a> · <a href="/notes/clay-b-lagged-pressure-reduction-20260906.html">CB.12：滞后压力缩减</a></p>
            </article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发问题：近期源积分是否有动力学收益</h3><p>固定 ε=1/8 与 AQ 原对象，检查 Kχ(p(R))−5Dχ/8 的 dyadic/Volterra 时间顺序。不能把 R 当作自由小残差，也不能重新使用已经支付旧压力的耗散份额。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.13 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.12</h3><p>CB.13 只是下一章占位，不是已完成研究。近期源自压力上界、实际 NS 生成 R.216–R.217、缩球一致常数、移动路径、G/G-P/G-C 与首次奇点排除尚未冻结；不把候选源能量或 dyadic/Volterra 检查写成已证结论。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-lagged-pressure-reduction-boundary">CB.12 · Clay-B 滞后压力缩减的文献和主张边界</h3><p>本章有限读取了 <a href="https://arxiv.org/pdf/1908.04958">Tao arXiv:1908.04958v2</a> 的问题设置、Theorem 1.2、Proposition 3.1 完整陈述及 (3.7)–(3.15) 推导，只用于确认线性热项/非线性余量分解与热滞后本身不是新方法。该文的全空间统一临界 L³ 假设不属于当前周期能量框架，因此不调用其正则性结论；没有全文证明复审或穷尽新颖性检索。</p><div class="boundary"><strong>CB.12 · ClayB-LaggedPressureReduction-20260906 公开边界</strong><p>PROVED LOCALLY：AY 写全原 s_J 起点的时间有序压力并定位绝对值分拆成本；AZ 合法重选早时点并重建权重，但留下 A_J²Λ_A；BA/BB 保持 AQ 原 s_J、μ_J、坏集和 [s_J,t]，只另设窗口前热起点，并将旧压力控制为 εDχ+o(H_t)。CONDITIONAL REDUCTION：必要净工作只转到 Kχ(p(R))−(3/4−ε)Dχ，方向仍是下界而非上界。SUFFICIENT SCALE ONLY：τ=Λ_A⁻⁸ᐟ³=K⁻³²ᐟ⁹ 不是必要或最优；R 保留完整非线性源，不是自由小残差或无强迫 NS 解。FINITE CHECKS ONLY：八份文本源、98 个公式编号、51/51 文件哈希与 Fraction 指数核算不替代证明。OPEN：近期源自压力上界、实际 NS 输入、移动缩球 G、奇点排除与一般正则性。没有完整新颖性审查、外部同行评审或 Clay 声明，无图件、仿真或累计 recap。NOT CLAY。<a href="/notes/clay-b-lagged-pressure-reduction-20260906.html">阅读完整 CB.12 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-pressure-test-coupling-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>旧热背景可以移走，近期源项仍待估计</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 时间有序压力、真实热滞后、旧压力耗散支付与近期源条件必要下界的双语方法笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.12 · {DISPLAY_ID}</strong></header>', template, count=1)
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
    value = value.replace("CB.1–CB.11", "CB.1–CB.12")
    value = value.replace("pressure output / tail persistence / original-test coupling", "lagged heat / old-pressure payment / recent source", 1)
    old_focus = "Clay-B 已把压力侧静态绝对成本与原测试压力功分开：固定能量和统一 H¹ 不能控制压力 Fourier-ℓ¹，但保留原测试输出匹配后有与截止无关的瞬时界。真正未付的是窗口内 g⁴ 的充分时间成本；AQ 上界、缩球路径和合同 G 继续开放。"
    new_focus = "Clay-B 已用窗口前真实热滞后支付所有含旧热分量的压力：成本是一份明确的 εDχ 加 o(H_t)，不是旧压力功自身 o(H_t)。必要净工作缩减到近期真实源自压力减剩余耗散；其上界、缩球路径和合同 G 继续开放。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    if 'class="tree-row clay-b-lagged-pressure-reduction-row"' in value:
        if "Clay-B 独立路线停在 CB.12" not in value or "CB.13 · NEXT" not in value:
            raise RuntimeError("existing CB.12 route boundary drift")
        return value
    cb11_start = value.index('<div class="tree-row clay-b-pressure-test-coupling-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb11_start)
    cb11 = value[cb11_start:boundary_start]
    cb11 = cb11.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb11 = cb11.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb11, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">NEXT TEST COMPLETED</span><h3>真实热滞后缩减已进入 CB.12</h3><p>AY–BB 已把窗口内起点的未付成本与窗口前滞后对旧压力的正面支付分开；结果见下一个正式路线节点。</p></aside>', cb11, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.11 branch drift")
    value = value[:cb11_start] + cb11 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB12_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-lagged-pressure-reduction-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 12
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.12"
    payload["nextIndependentChapter"] = "CB.13"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note",
            "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.12",
            "sourceCommit": "891e6b85f53ae19272973c191726f1278e47918b", "baseCommit": "299a3b4e7deab8f561c83559c13741aaa5137343",
            "handoffCommit": "3501cf9d70cbb5140186bb18d0cf1da8c110480f", "logicalPredecessor": "ClayB-PressureTestCoupling-20260906",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False, "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-lagged-pressure-reduction-20260906-gate.test.mjs", "publicationTest": "tests/clay-b-lagged-pressure-reduction-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-lagged-pressure-reduction-20260906-translations.mjs", "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE", "simulationRequired": False, "recapRequired": False,
            "advancesCanonicalR0Series": False, "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "OLD_PRESSURE_PAID_BY_ONE_EPSILON_DISSIPATION_SHARE_PLUS_O_HT_NOT_OLD_WORK_O_HT_SUFFICIENT_LAG_SCALE_NOT_NECESSARY_OR_OPTIMAL_RECENT_SOURCE_PRESSURE_MINUS_REMAINING_DISSIPATION_HAS_ONLY_CONDITIONAL_NECESSARY_LOWER_BOUND_G_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.12", DISPLAY_ID, "旧热背景可以移走，近期源项仍待估计", "The old heat background can be removed", "PROVED", "FINITE", "CONDITIONAL REDUCTION", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.12", "Clay-B 独立路线停在 CB.12", "CB.13 · NEXT", 'class="tree-row clay-b-lagged-pressure-reduction-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb12 = home.index('class="tree-row clay-b-lagged-pressure-reduction-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb12)
    if not (r0_start < r0_boundary < divider < clay_start < cb12 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-lagged-pressure-reduction-boundary"' not in literature or "CB.12 · ClayB-LaggedPressureReduction-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.12 · {DISPLAY_ID}" not in index or "12 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.12" or site.get("nextIndependentChapter") != "CB.13":
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
print(json.dumps({"schemaVersion": "clay-b-lagged-pressure-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.12", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
