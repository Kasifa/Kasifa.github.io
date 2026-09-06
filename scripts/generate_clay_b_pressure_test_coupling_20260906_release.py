#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB PressureTestCoupling CB.11 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.55"
SLUG = "clay-b-pressure-test-coupling-20260906"
DISPLAY_ID = "ClayB-PressureTestCoupling-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_MAIN = '''  <main data-language="zh">
    <article>
      <header class="hero">
        <div class="kicker">CB.11 · 独立 Clay-B 方法笔记 · 2026-09-06</div>
        <h1>CB.11｜压力不能与它的测试因子分开估计</h1>
        <p class="dek">固定能量和统一 H¹ 上界仍允许高频压力的 Fourier 绝对和任意大；但保留原非线性测试的输出频率后，完整配对有与速度、压力截止无关的瞬时上界。前者不能否定后者，后者仍留下未付的四次梯度时间成本。</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>FINITE CHECKS ONLY</span><span>STATIC OBSTRUCTION</span><span>CONDITIONAL</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / 结论地图</div><h2>压力侧静态发散与原测试压力功是不同对象</h2><div class="grid"><div class="card"><strong class="proved">已证方法界</strong>AR–AV 支付低输出、记录分频成本、证明尾持留，并说明换测试最终回到原立方能量恒等式。</div><div class="card"><strong class="proved">原测试配对</strong>AW 保留最终输出匹配，即使去掉相位仍有 W_ang≤Cχ(M²g²+g⁴)。</div><div class="card"><strong class="open">静态阻碍与开放项</strong>AX 只让压力 Fourier-ℓ¹ 发散；时间积分中的 g⁴、AQ 上界和 G 仍未支付。</div></div><p>本章不构造合法大范数序列、NS 轨道或奇点，也不把静态压力绝对和写成压力 L∞ 或原压力工作反例。</p></section>
      <section><div class="section-no">02 / AR.1–AR.21</div><h2>低压力输出可以移走，但扩散频率仍留下未付速率</h2><p>对同一坏时间、早时点和积分因子另取固定输出阈值 L。低输出压力功的归一化成本满足</p><div class="equation">e_J(L)=C min{c₀M⁴r²L⁴Λ_A⁻⁷, M²L²A_JΛ_A⁻³}.       (AR.19)</div><p>只要 e_J(L)→0，AQ 的必要净工作可转到高压力输出。取扩散频率 L≈δ⁻¹ᐟ²≈Λ_A² 时，现有估计留下 A_JΛ_A；能量只给 A_J=o(1)。这是充分估计未闭合，不是实际低输出必定很大。</p></section>
      <section><div class="section-no">03 / AS.1–AS.37</div><h2>分离输入有频率比增益，可比输入留下半阶频率矩</h2><p>高高压力按可比输入和严格分离输入精确分组。分离输入产生 Q_i/Q_j 增益，可比输入仍允许任意非零低输出；压力侧绝对账本受半阶矩 𝔠_K 控制。</p><div class="equation">||p_h^&gt;L||∞ ≤ C 𝔯_(K,L) ≤ C 𝔠_K,
𝔠_K=Σ_j Q_j³||v_j||₂².                                  (AS.27)</div><p>统一 L² 与 H¹ 不能静态控制 𝔠_K，且对应剪切例的压力恰为零。因此这个频率矩只是某条充分绝对值路线的成本，不能冒充真实压力功或动态必要条件。</p></section>
      <section><div class="section-no">04 / AT.1–AU.37</div><h2>全域与固定环带的小尾持留只给必要机制</h2><p>AT 写出固定平滑高频尾的完整受迫方程；AU 在 AP 的同一固定正则环带上补齐 cutoff、近中远压力和低频强迫。沿合法大局部 L³ 窗口，局部高频尾最终不能在窗口中降到固定小阈值。</p><div class="equation">||θP_&gt;Λ_A^(3/4)u(σ)||₃ &gt; η_loc/4  for every σ∈J.       (AU.37)</div><p>重新选择公共阈值后，这至多令相应好时间集为空；AQ 的必要下界仍留在实际 [s_J,t] 上。尾持留没有给坏时间净工作上界，也不是缩球一致估计。</p></section>
      <section><div class="section-no">05 / AV.1–AV.11</div><h2>把原速度测试换成高尾测试不会产生新上界</h2><p>测试缺陷、端点能量差、耗散差与低频强迫必须一并保留。对显式全坏窗口完成消元后，所谓新方括号精确返回原局部立方能量恒等式。</p><div class="equation">β_K=Hχ(u)′+¼Dχ(u)−𝓡_u.                                  (AV.11)</div><p>任意坏集指标不能仅凭小原函数穿过时间导数。换测试路线因此停止，但这不是所有带符号动力学方法的 no-go。</p></section>
      <section><div class="section-no">06 / AW.1–AW.44</div><h2>保留原测试输出匹配后，静态半阶频率矩可以消去</h2><p>AW 写全压力符号、两个无散收缩、输出分母、零模、相位和真实非多项式测试。方向因子 Γ 在近反平行低输出可达到常数量级；单看角度不能给统一小量。</p><div class="equation">|𝓚χ(p_h^&gt;L)| ≤ W_ang(χ,K,L)
                 ≤ Cχ(M²g²+g⁴),                           (AW.43)
g=||∇u||₂.</div><p>该界即使删除相位也成立，常数在固定 χ 下不依赖 K、L。沿原窗口积分后 M²A_J/Hχ(t) 已付，真正未付的是 Hχ(t)⁻¹∫μ_Jg⁴；它的小量只是这条绝对值路线的充分条件。</p></section>
      <section><div class="section-no">07 / AX.1–AX.20</div><h2>静态双频块只排除压力侧 Fourier-ℓ¹ 能量预算</h2><p>AX 构造光滑实值零均值无散有限 Fourier 场族。对任意预先固定 K、L 和 E₀，可保持能量精确为 E₀、H¹ 一致有界，而受保护高输出区的实际压力系数全部同号。</p><div class="equation">||u_Q||₂²=E₀,  ||∇u_Q||₂²≤E₀+(2π)³/2,
Σ_(m≠0)|p̂_(P_&gt;K u_Q)^&gt;L(m)| ≥ c_*Q → ∞.               (AX.20)</div><p>这不是数值拟合，但它只是一族静态场：不证明压力 L∞、原测试压力功、同一 NS 轨道、成熟窗口或奇点失效，也不与 AW 的测试匹配上界冲突。</p></section>
      <section><div class="section-no">08 / 当前边界与下一问题</div><h2>下一步只检查真实时间 Duhamel 是否改善 g⁴ 成本</h2><p>先固定同一解、固定环带、AQ 的实际 s_J、窗口和 K，再把高频尾的热初始项及完整 Leray 非线性源项放回原压力和原 χ|u|u 测试。精确 Duhamel 恒等式本身不算新估计；若只返回 g⁴、A_JΛ_A 或原能量恒等式，就记录等价关系并停止。</p><table><thead><tr><th>类别</th><th>本章范围</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>AR–AV 方法检查、AW 精确符号与保留测试匹配的瞬时上界。</td></tr><tr><td>STATIC OBSTRUCTION</td><td>AX 的固定能量、统一 H¹ 压力 Fourier-ℓ¹ 发散。</td></tr><tr><td>FINITE CHECKS ONLY</td><td>有限有理数核算和 37/37 源字节核验；不替代解析证明。</td></tr><tr><td>CONDITIONAL / OPEN</td><td>合法序列量词保留；g⁴ 时间成本、AQ 上界、移动缩球 G 与一般正则性仍开放。</td></tr></tbody></table><p class="note">科学源提交：ebaf7e8a51cf08f890caf727850f1b65d6fbd0fd；冻结提交：2e3706c5fe1f43586b1e9a59a24cb41d04935c9a。十二份源、二十五份依赖和两份冻结信封按 SHA-256 绑定；七份数学源共 202 个公式编号。历史 INTERNAL/PENDING 与旧下一步文字是推导时快照，当前范围由报告和 manifest 定义。内部实际文件审查不是外部同行评审或完整新颖性审查。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_output_reduction_preflight_20260906.md">AR 输出截断</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_dyadic_pressure_ledger_preflight_20260906.md">AS 分频账本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_exact_pressure_symbol_preflight_20260906.md">AW 原压力符号</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_angular_cost_obstruction_20260906.md">AX 静态阻碍</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_test_coupling_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap。AY 以后稿件与独立私有论文不在本次发布范围。G OPEN / NOT CLAY。</strong></p></section>
    </article>
    <footer class="footer">CB.11 · Independent HTML research note · ClayB-PressureTestCoupling-20260906 · 2026-09-06</footer>
  </main>'''


EN_MAIN = '''  <main data-language="en">
    <article>
      <header class="hero">
        <div class="kicker">CB.11 · Independent Clay-B methods note · 2026-09-06</div>
        <h1>CB.11 | Pressure cannot be estimated apart from its test factor</h1>
        <p class="dek">Fixed energy and a uniform H¹ bound still allow the Fourier absolute sum of high-frequency pressure to grow without bound. Yet once the output frequency of the original nonlinear test is retained, the complete pairing has an instantaneous bound independent of the velocity and pressure cutoffs. The former does not refute the latter, while the latter still leaves an unpaid fourth-power gradient cost in time.</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>FINITE CHECKS ONLY</span><span>STATIC OBSTRUCTION</span><span>CONDITIONAL</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / Result map</div><h2>Static pressure-side divergence and original-test pressure work are different objects</h2><div class="grid"><div class="card"><strong class="proved">Paid method checks</strong>AR–AV pay low outputs, record dyadic costs, prove tail persistence, and show that changing the test returns to the original cubic energy identity.</div><div class="card"><strong class="proved">Original-test pairing</strong>AW keeps final-output matching and obtains W_ang≤Cχ(M²g²+g⁴) even after deleting phases.</div><div class="card"><strong class="open">Static obstruction and open cost</strong>AX makes only pressure Fourier-ℓ¹ diverge; the time integral of g⁴, the AQ upper bound, and G remain unpaid.</div></div><p>This chapter constructs no legal large-norm sequence, NS trajectory, or singularity, and it does not turn a static pressure absolute sum into a pressure-L∞ or original-pressure-work counterexample.</p></section>
      <section><div class="section-no">02 / AR.1–AR.21</div><h2>Low pressure outputs can be removed, but the diffusion frequency retains an unpaid rate</h2><p>On the same bad times, early time, and integrating factor, introduce a fixed output threshold L. The normalized low-output pressure-work cost satisfies</p><div class="equation">e_J(L)=C min{c₀M⁴r²L⁴Λ_A⁻⁷, M²L²A_JΛ_A⁻³}.       (AR.19)</div><p>Whenever e_J(L)→0, the AQ necessary net work transfers to high pressure outputs. At the diffusion frequency L≈δ⁻¹ᐟ²≈Λ_A², the present estimate leaves A_JΛ_A, while energy gives only A_J=o(1). This is a failure of a sufficient estimate to close, not a lower bound on the actual low output.</p></section>
      <section><div class="section-no">03 / AS.1–AS.37</div><h2>Separated inputs gain a frequency ratio; comparable inputs retain a half-order moment</h2><p>The high–high pressure is grouped exactly into comparable and strictly separated inputs. Separated inputs gain Q_i/Q_j, while comparable inputs still permit arbitrary nonzero low outputs. The pressure-side absolute ledger is bounded by a half-order moment 𝔠_K.</p><div class="equation">||p_h^&gt;L||∞ ≤ C 𝔯_(K,L) ≤ C 𝔠_K,
𝔠_K=Σ_j Q_j³||v_j||₂².                                  (AS.27)</div><p>Uniform L² and H¹ bounds do not control 𝔠_K statically, and the corresponding shear example has zero pressure. Thus this moment is only the cost of one sufficient absolute-value route, not genuine pressure work or a dynamical necessary condition.</p></section>
      <section><div class="section-no">04 / AT.1–AU.37</div><h2>Global and fixed-annulus small-tail persistence supplies only a necessary mechanism</h2><p>AT writes the complete forced equation for a fixed smooth high-frequency tail. AU pays the cutoff, near/middle/far pressure, and low-frequency forcing on the same fixed regular annulus from AP. Along a legal large-local-L³ window, the local high-frequency tail eventually cannot fall below a fixed small threshold anywhere in the window.</p><div class="equation">||θP_&gt;Λ_A^(3/4)u(σ)||₃ &gt; η_loc/4  for every σ∈J.       (AU.37)</div><p>After redefining a common threshold, this can at most make the corresponding good-time set empty. The AQ necessary lower bound remains on the actual interval [s_J,t]. Tail persistence gives no upper bound for bad-time net work and no shrinking-scale uniform estimate.</p></section>
      <section><div class="section-no">05 / AV.1–AV.11</div><h2>Replacing the original-velocity test by a high-tail test creates no new upper bound</h2><p>The test defect, endpoint energy difference, dissipation difference, and low-frequency forcing must all remain. After complete elimination on an explicitly all-bad window, the purported new bracket returns exactly to the original local cubic energy identity.</p><div class="equation">β_K=Hχ(u)′+¼Dχ(u)−𝓡_u.                                  (AV.11)</div><p>An arbitrary bad-set indicator cannot be moved through a time derivative from a small primitive alone. The test-change route therefore stops, but this is not a no-go theorem for every signed dynamical method.</p></section>
      <section><div class="section-no">06 / AW.1–AW.44</div><h2>Retaining original-test output matching removes the static half-order frequency moment</h2><p>AW keeps the full pressure symbol, both solenoidal contractions, output denominator, zero mode, phase, and genuine nonpolynomial test. The direction factor Γ can remain order one for nearly antiparallel low outputs, so angle alone gives no uniform smallness.</p><div class="equation">|𝓚χ(p_h^&gt;L)| ≤ W_ang(χ,K,L)
                 ≤ Cχ(M²g²+g⁴),                           (AW.43)
g=||∇u||₂.</div><p>This estimate survives phase deletion and, for fixed χ, its constant is independent of K and L. After integration on the original window, M²A_J/Hχ(t) is paid. The truly unpaid term is Hχ(t)⁻¹∫μ_Jg⁴; its smallness is only sufficient for this absolute-value route.</p></section>
      <section><div class="section-no">07 / AX.1–AX.20</div><h2>The static two-block family rules out only a pressure-side Fourier-ℓ¹ energy budget</h2><p>AX constructs smooth real mean-zero divergence-free finite Fourier fields. For any preassigned K, L, and E₀, the energy stays exactly E₀ and H¹ stays uniformly bounded, while every actual pressure coefficient in a protected high-output region has the same sign.</p><div class="equation">||u_Q||₂²=E₀,  ||∇u_Q||₂²≤E₀+(2π)³/2,
Σ_(m≠0)|p̂_(P_&gt;K u_Q)^&gt;L(m)| ≥ c_*Q → ∞.               (AX.20)</div><p>This is analytic rather than a numerical fit, but it is only a family of static fields. It proves no pressure-L∞ divergence, original-test pressure-work divergence, same-trajectory NS failure, mature-window failure, or singularity, and it does not conflict with AW's test-matched bound.</p></section>
      <section><div class="section-no">08 / Present boundary and next question</div><h2>The next step only asks whether true-time Duhamel improves the g⁴ cost</h2><p>Fix the same solution, annulus, actual AQ time s_J, window, and K. Then return the heat initial term and the complete Leray nonlinear source of the high-frequency tail to the original pressure and original χ|u|u test. An exact Duhamel identity is not itself a new estimate. If the calculation only returns g⁴, A_JΛ_A, or the original energy identity, the equivalence is recorded and the route stops.</p><table><thead><tr><th>Class</th><th>Scope here</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>AR–AV method checks, AW's exact symbol, and its instantaneous bound with test matching retained.</td></tr><tr><td>STATIC OBSTRUCTION</td><td>AX's pressure Fourier-ℓ¹ divergence at fixed energy and uniformly bounded H¹.</td></tr><tr><td>FINITE CHECKS ONLY</td><td>Finite rational checks and 37/37 source-byte verification; neither replaces the analytic proofs.</td></tr><tr><td>CONDITIONAL / OPEN</td><td>The legal-sequence quantifier is retained; the g⁴ time cost, AQ upper bound, moving shrinking G, and general regularity remain open.</td></tr></tbody></table><p class="note">Scientific source commit: ebaf7e8a51cf08f890caf727850f1b65d6fbd0fd; freeze commit: 2e3706c5fe1f43586b1e9a59a24cb41d04935c9a. Twelve source files, twenty-five dependencies, and two frozen envelopes are SHA-256-bound; the seven mathematical sources contain 202 numbered formulas. Historical INTERNAL/PENDING labels and old next-step text are derivation-time snapshots; the report and manifest define the current scope. Internal actual-file review is neither external peer review nor a complete novelty audit.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_output_reduction_preflight_20260906.md">AR output cutoff</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_dyadic_pressure_ledger_preflight_20260906.md">AS dyadic ledger</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_exact_pressure_symbol_preflight_20260906.md">AW exact pressure symbol</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_angular_cost_obstruction_20260906.md">AX static obstruction</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_test_coupling_frozen_ledger_20260906.json">portable ledger</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap. Drafts AY and later and the private independent paper are outside this release. G OPEN / NOT CLAY.</strong></p></section>
    </article>
    <footer class="footer">CB.11 · Independent HTML research note · ClayB-PressureTestCoupling-20260906 · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-pressure-test-coupling" aria-labelledby="clay-b-pressure-test-coupling-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.11 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · PRESSURE/TEST COUPLING</p><h2 class="route-map-title" id="clay-b-pressure-test-coupling-title">CB.11｜压力不能与它的测试因子分开估计</h2><p class="route-map-intro">固定能量与统一 H¹ 仍允许高频压力 Fourier 绝对和发散，但这不控制原测试压力功。保留最终测试输出匹配后，即使删除相位仍有 W_ang≤Cχ(M²g²+g⁴)；未付的是窗口内 g⁴ 的充分时间成本，而非已知动态障碍。AQ 上界、移动缩球 G 与一般正则性仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 压力与测试配对笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-pressure-test-coupling-20260906.html">阅读最新 CB.11 压力与测试配对笔记 →</a><a href="/literature-review.html#clay-b-pressure-test-coupling-boundary">查看文献与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 压力与测试配对结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>原测试输出匹配：瞬时上界</span><span><i class="route-legend-mark closed" aria-hidden="true"></i>压力侧 Fourier-ℓ¹：静态能量预算失败</span><span><i class="route-legend-mark current" aria-hidden="true"></i>g⁴ 时间成本、AQ 上界与 G OPEN · NOT CLAY</span></div></div></section>'''


CB11_ROW = '''          <div class="tree-row clay-b-pressure-test-coupling-row">
            <article class="tree-node current">
              <div class="tree-node-head"><span class="route-range">CB.11 · 2026-09-06 · AR–AX PRESSURE/TEST COUPLING</span><span class="tree-state current">当前路线边界</span></div>
              <h3>CB.11｜压力侧静态阻碍与原测试配对上界</h3>
              <p>AR–AV 支付低压力输出、列出分频输入成本、证明全域与固定环带的高频尾持留，并说明换成高尾测试最终返回原局部立方能量恒等式。这些方法检查没有给出 AQ 的相反上界。</p>
              <p>AW 保留原测试的输出频率匹配，得到与 K、L 无关的 W_ang≤Cχ(M²g²+g⁴)；AX 同时证明固定能量和统一 H¹ 不能控制压力侧 Fourier-ℓ¹。两者不矛盾，因为 AX 没有最终测试因子。真正未付的是 g⁴ 的时间充分成本。</p>
              <p class="tree-path">CB.10 坏时间必要下界 → AR 低输出转移 → AS 分频成本 → AT/AU 尾持留 → AV 换测试返回原恒等式 → AW 原测试匹配瞬时界 / AX 静态压力侧阻碍 → 真实时间 Duhamel 检查 OPEN</p>
              <p><a href="/notes/clay-b-bad-time-net-work-20260906.html">CB.10：坏时间净工作必要下界</a> · <a href="/notes/clay-b-pressure-test-coupling-20260906.html">CB.11：压力与测试配对</a></p>
            </article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发问题：真实时间 Duhamel 能否改善 g⁴ 成本</h3><p>保持 AQ 的同一解、固定环带、实际 s_J、窗口、K、坏时间权重与原 χ|u|u 测试，展开高频尾的热初始项和完整 Leray 源项。不能给起点添加小梯度假设，也不能把精确恒等式本身当成新上界。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.12 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.11</h3><p>CB.12 只是下一章占位，不是已完成研究。g⁴ 时间成本、原带符号坏时间工作的真实 NS 上界、缩球一致常数、移动路径、G/G-P/G-C、实际 R.216–R.217 输入与首次奇点排除尚未冻结；不把后续 Duhamel 检查写成已证结论。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-pressure-test-coupling-boundary">CB.11 · Clay-B 压力与测试配对的文献和主张边界</h3><p>本章的 HLS 与 Sobolev 嵌入是标准工具，不作为新正则性定理。实际核对了 <a href="https://terrytao.wordpress.com/2009/03/30/245c-notes-1-interpolation-of-lp-spaces/">Tao 245C Notes 1 当前 Corollary 46</a> 的 HLS 核指数约定；周期版本另由均值分离、热核和周期 Riesz 变换适配。还有限读取 <a href="https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/20720/qjmam_20190430_R1_20190813.pdf?isAllowed=y&amp;sequence=1">Tran–Yu 2019 作者稿</a>的 Lemma 2.1、moderator 定义与相关展开，用于确认压力 moderator 不是新机制；没有调用其 Theorem 3.5，也未重审全部外部证明。历史压力正则性、局部平滑、averaged NS 和压力功记录继续保留各自前提与访问边界。</p><div class="boundary"><strong>CB.11 · ClayB-PressureTestCoupling-20260906 公开边界</strong><p>PROVED LOCALLY：AR 将低输出成本写成 e_J(L)，AS 区分分离与可比输入，AT/AU 给全域和固定环带小尾持留，AV 证明换测试完整支付后返回原能量恒等式；AW 写全原压力符号并在保留测试输出匹配时证明 W_ang≤Cχ(M²g²+g⁴)。STATIC OBSTRUCTION：AX 在任意预先固定 K、L 下构造固定能量、统一 H¹ 的静态无散 Fourier 场，使实际高输出压力 Fourier-ℓ¹ 至少线性增长；这不是压力 L∞、原测试压力功、NS 轨道或成熟窗口反例。CONDITIONAL：所有终端窗口陈述仍以合法同一解大范数序列存在为条件；g⁴ 小量只是 AW 绝对值路线的充分成本。FINITE CHECKS ONLY：有限有理数核算和 37/37 源字节校验不替代证明。OPEN：真实时间有序演化能否改善 g⁴ 成本、AQ 的原带符号上界、移动缩球 G 与一般正则性。没有完整新颖性审查、外部同行评审或 Clay 声明，无图件、仿真或累计 recap。NOT CLAY。<a href="/notes/clay-b-pressure-test-coupling-20260906.html">阅读完整 CB.11 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-bad-time-net-work-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>压力不能与它的测试因子分开估计</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 压力输出、频率账本、尾持留、原测试配对上界与静态压力绝对成本阻碍的双语方法笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.11 · {DISPLAY_ID}</strong></header>', template, count=1)
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
    value = value.replace("CB.1–CB.10", "CB.1–CB.11")
    value = value.replace("frequency payment / fixed annulus / bad-time necessary work", "pressure output / tail persistence / original-test coupling", 1)
    old_focus = "Clay-B 已在同一解的固定成熟窗口中支付低频参与压力和固定环带好时间高高压力；若合法的大局部 L³ 序列存在，坏时间正净工作必须达到终端局部能量量级。这是必要下界，不是上界；真正的 NS 上界、缩球路径和合同 G 继续开放。"
    new_focus = "Clay-B 已把压力侧静态绝对成本与原测试压力功分开：固定能量和统一 H¹ 不能控制压力 Fourier-ℓ¹，但保留原测试输出匹配后有与截止无关的瞬时界。真正未付的是窗口内 g⁴ 的充分时间成本；AQ 上界、缩球路径和合同 G 继续开放。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    if 'class="tree-row clay-b-pressure-test-coupling-row"' in value:
        if "Clay-B 独立路线停在 CB.11" not in value or "CB.12 · NEXT" not in value:
            raise RuntimeError("existing CB.11 route boundary drift")
        return value
    cb10_start = value.index('<div class="tree-row clay-b-bad-time-net-work-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb10_start)
    cb10 = value[cb10_start:boundary_start]
    cb10 = cb10.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb10 = cb10.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb10, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">NEXT TEST COMPLETED</span><h3>压力侧与测试侧的区别已进入 CB.11</h3><p>AR–AX 已分开静态压力 Fourier 绝对成本与保留原测试输出匹配的真实工作估计；结果见下一个正式路线节点。</p></aside>', cb10, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.10 branch drift")
    value = value[:cb10_start] + cb10 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB11_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-pressure-test-coupling-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 11
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.11"
    payload["nextIndependentChapter"] = "CB.12"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note",
            "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.11",
            "sourceCommit": "ebaf7e8a51cf08f890caf727850f1b65d6fbd0fd", "baseCommit": "e887f8fdfee7f1e88d5724d1233832db39fbf1bf",
            "handoffCommit": "2e3706c5fe1f43586b1e9a59a24cb41d04935c9a", "logicalPredecessor": "ClayB-BadTimeNetWork-20260906",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False, "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-pressure-test-coupling-20260906-gate.test.mjs", "publicationTest": "tests/clay-b-pressure-test-coupling-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-pressure-test-coupling-20260906-translations.mjs", "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE", "simulationRequired": False, "recapRequired": False,
            "advancesCanonicalR0Series": False, "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "PRESSURE_SIDE_STATIC_FOURIER_L1_OBSTRUCTION_IS_NOT_ORIGINAL_TEST_WORK_RETAINED_TEST_OUTPUT_MATCHING_GIVES_CCHI_M2G2_PLUS_G4_INSTANTANEOUS_BOUND_G4_TIME_COST_SUFFICIENT_ONLY_AQ_UPPER_BOUND_AND_G_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.11", DISPLAY_ID, "压力不能与它的测试因子分开估计", "Pressure cannot be estimated apart from its test factor", "STATIC OBSTRUCTION", "FINITE", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.11", "Clay-B 独立路线停在 CB.11", "CB.12 · NEXT", 'class="tree-row clay-b-pressure-test-coupling-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb11 = home.index('class="tree-row clay-b-pressure-test-coupling-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb11)
    if not (r0_start < r0_boundary < divider < clay_start < cb11 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-pressure-test-coupling-boundary"' not in literature or "CB.11 · ClayB-PressureTestCoupling-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.11 · {DISPLAY_ID}" not in index or "11 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.11" or site.get("nextIndependentChapter") != "CB.12":
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
print(json.dumps({"schemaVersion": "clay-b-pressure-test-coupling-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.11", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
