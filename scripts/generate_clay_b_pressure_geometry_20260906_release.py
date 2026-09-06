#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB PressureGeometry CB.7 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CHECK_ONLY = "--check-only" in sys.argv[1:]
VERSION = "2.51"
DISPLAY_ID = "ClayB-PressureGeometry-20260906"
SLUG = "clay-b-pressure-geometry-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"


ZH_MAIN = r'''  <main data-language="zh">
    <header class="hero">
      <div>
        <div class="kicker">CB.7 · 独立 Clay-B 解析笔记 · 2026-09-06</div>
        <h1>CB.7｜压力功的符号、速度方向与临界条件</h1>
        <p class="deck">完整局部 L³ 恒等式区分了耗散与可能推动增长的压力功。固定能量上界 M 和固定半径 r 时，带速度权重的远源压力功可以支付；方向分解给出零集安全的条件接口，但能量没有提供所需临界控制；一个显式周期构造则证明压力功没有普适耗散符号。</p>
        <p><strong>带权远源小量只在同一固定 M、r 下成立，不支付近源、输运和外壳。F∈L²_tL³_x 是附加条件，不是能量结论。显式正负号例子改变初值并放大能量，只给瞬时与短时行为。周期零线例不判定 Vasseur 全空间原类中的必要性。G 仍 OPEN。NOT CLAY，不主张新颖性或发表等级。</strong></p>
        <div class="badges"><span class="badge">PROVED LOCALLY</span><span class="badge">LITERATURE</span><span class="badge">CONDITIONAL</span><span class="badge">FINITE: NONE</span><span class="badge">NO FIGURE</span><span class="badge">NO SIMULATION</span><span class="badge">OPEN</span><span class="badge">NOT CLAY</span></div>
      </div>
      <aside class="stamp"><strong>结论边界</strong><p class="proved">固定 M/r 远源压力功：已支付</p><p class="proved">方向耗散分解：已证</p><p>F 的临界时空控制：条件性</p><p class="proved">压力功两种符号：已构造</p><p class="proved">短时真实 NS 增长：已证</p><p>有限计算：无</p><p class="open">近源/外壳/F 演化/G：OPEN</p></aside>
    </header>
    <article>
      <section><div class="section-no">01 / 结论地图</div><h2>已经付掉一项，识别一项条件，并排除一个符号捷径</h2><div class="grid"><div class="card"><strong class="proved">固定球远源功</strong>同一解、固定 M 与 r 下，带权远源压力功相对终点 L³ 能量按 L⁻⁷ 衰减。</div><div class="card"><strong>方向条件</strong>零集安全的 F 把方向结构接到延拓准则，但临界 L²_tL³_x 控制并非能量所给。</div><div class="card"><strong class="open">压力符号</strong>压力功可正可负；不能不经支付地把它当作耗散，也不能由此推出持留。</div></div><p>CB.7 没有闭合一般固定球的近源压力、输运、黏性和外壳预算。它把当前可用结构与仍缺失的动力学控制分开。</p></section>
      <section><div class="section-no">02 / AB.1–AB.5</div><h2>完整带符号 L³ 预算与固定球远源支付</h2><p>以零速度正则化后的 χ|u|u 测试原方程，得到</p><div class="equation">H_χ'(t) + D_χ(t) = W_χ(t),
H_χ(s) = H_χ(t) + ∫_s^t D_χ(σ)dσ − ∫_s^t W_χ(σ)dσ.                    (AB.2–AB.3)</div><p>反向积分时，耗散提高早时能量下界；可能造成快速正增长的是带符号工作。对固定 M、r，令 L=L_r(t)、δ=c₀r²L⁻⁴，由逐时远场压力梯度界与能量得到</p><div class="equation">sup_(s∈[t−δ,t]) |∫_s^t∫χ|u|u·∇q_far| / H_χ(t)
  ≤ C c₀ M⁴ r⁻² L⁻⁷.                                                     (AB.5)</div><p>固定 M、r 且 L→∞ 时，这一项相对趋零。它不是把 CB.6 的裸压力冲量替换成速度加权功，也不适用于未经另控的缩球、移动路径、近源或外壳。</p></section>
      <section><div class="section-no">03 / AB.6–AB.8</div><h2>标准全环面压力链留下不可吸收的大 L 系数</h2><p>全环面原型中，周期压力估计、加权 Cauchy–Schwarz 与保留低模项的 Sobolev 链给</p><div class="equation">|W| ≤ C L D + C L^(5/2) D^(1/2)
    ≤ (C L + η)D + C_η L⁵,
H' ≤ (C L + η − 1)D + C_η L⁵.                                           (AB.8)</div><p>当 L 很大时，D 留在错误的一侧；这不是只依赖 L 的闭合微分不等式。高频无散剪切只说明固定 L 不能给 D 的上界，它是瞬时范数检查，不是持留或奇点的动力学反例。</p></section>
      <section><div class="section-no">04 / AC.1–AC.6</div><h2>速度方向给出精确分解，但只改善结构与常数</h2><p>令 q=|u|，只在 q&gt;0 上定义 e=u/q，并把加权量在零集取零。则</p><div class="equation">D = 2D_r + D_θ,
F = q div e = −e·∇q,
W = −∫p q F,
Z_e ≤ min(D_r, 2D_θ) ≤ 2D/5.                                             (AC.2–AC.5)</div><p>F 的可测代表满足 |F|≤|∇u|，没有方向除零问题；这不表示 e 跨零集属于普通 Sobolev 空间。径向或角向部分小时分解有额外信息，但最坏情形仍留下 C L D_r 或 C L√(D_rD_θ)，固定常数的改善不能自动吸收。</p></section>
      <section><div class="section-no">05 / AC.7–AC.12</div><h2>方向结构只产生一条明确的条件延拓接口</h2><p><a href="https://web.ma.utexas.edu/users/vasseur/documents/preprints/NSdirection2.pdf">Vasseur 2007 作者原稿</a>在全空间 Leray–Hopf 类中给出附加方向可积性下的正则性。这里不把其方向重写声明为新发现，也不把全空间量词直接移植到周期域。</p><div class="equation">∫_(t₀)^T ||F(t)||₃² dt &lt; ∞
  ⇒ 周期光滑解可延拓越过有限时间 T.                                  (AC.9)</div><p>本地证明保留压力估计、周期低模项、Gronwall、L³_tL⁹_x 控制与 H¹ 重启；最后使用<a href="https://terrytao.wordpress.com/2018/09/16/254a-notes-1-local-well-posedness-of-the-navier-stokes-equations/">标准周期次临界局部理论</a>。能量只给 F∈L²_tL²_x，没有给 F∈L²_tL³_x。因此这是一条 CONDITIONAL 接口，不是一般正则性结论。</p></section>
      <section><div class="section-no">06 / AC.13–AC.14</div><h2>周期光滑解的零速度线可使未加权方向散度不可积</h2><p>全时光滑周期 Taylor–Green 解</p><div class="equation">u=e^(−2t)(sin x cos y, −cos x sin y, 0),
p=(e^(−4t)/4)(cos 2x + cos 2y)</div><p>在零线附近有 div e=(y²−x²)/r³+O(r)。在固定角锥内 |div e|≥c/r，所以其局部 L^b 对 b≥2 发散，而加权 F 仍有界。下界只在固定角锥内，不是所有方向的双边可比。这个周期例不是 NS 奇点，也不能判定 Vasseur 全空间原类中条件的必要性。</p></section>
      <section><div class="section-no">07 / AD.1–AD.23</div><h2>显式有限模态初值使压力功严格取两种符号</h2><p>取 Ψ=cos x+cos y+cos(x+y)、v=(∂_yΨ,−∂_xΨ,0)，并令 V_ε=(a cos z,sin z,0)+εv，a&gt;1。背景与交叉项不产生压力源，逐模计算与一致余项给</p><div class="equation">W(V_ε)=ε³κ(a)π²+O(ε⁴),    κ(a)&gt;0.                                 (AD.16)</div><p>充分小的正 ε 给 W&gt;0，取相反初值给 W&lt;0。两个初值分别生成自己的局部光滑 NS 解，不是把一条正向轨道整体取负。再以有限幅值 A 放大，W(AU)=A⁴W(U)、D(AU)=A³D(U)，可使 H'(0)&gt;0 并在短正时间保持。初始能量同时增长，寿命不要求对 A 一致；它不触及成熟时间、固定能量或固定解首次奇点。</p></section>
      <section><div class="section-no">08 / 边界、证据与下一问题</div><h2>下一步只检查 F 的真实演化能否产生缺失控制</h2><table><thead><tr><th>类别</th><th>本章范围</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>完整带符号局部 L³ 恒等式；固定 M/r 的带权远源压力功；方向耗散分解；压力功正负号与大幅值短时真实 NS 增长。</td></tr><tr><td>LITERATURE / CONDITIONAL</td><td>Vasseur 全空间方向准则为文献背景；周期 F∈L²_tL³_x 延拓接口是附加条件，未由能量推出。</td></tr><tr><td>FINITE COMPUTATION</td><td>无；没有仿真、数值证书或科学图。</td></tr><tr><td>OPEN</td><td>F 的真实演化控制、近源压力、输运、黏性与外壳；缩球和原移动路径；G/G-P/G-C、R.216–R.217 及既有 U/V/W/Y 缺口。</td></tr></tbody></table><p class="note">科学源提交：40b18a9c29499f4956d72e197f8d285bd3f6b453；冻结提交：e63575d6bbb81332441d74c0916c5663e89ac74c。六份科学源、三份依赖和两份冻结信封按 SHA-256 绑定，三份数学源共 45 个公式标签；内部实际文件审查不是外部同行评审。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_mature_l3_budget_preflight_20260906.md">局部 L³ 预算</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_geometry_20260906.md">压力方向结构</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_sign_20260906.md">压力功符号构造</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_geometry_independent_audit_20260906.md">独立审查</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_geometry_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap。没有新颖性、优先权、发表等级或 Clay 正则性主张。G OPEN / NOT CLAY。</strong></p></section>
    </article>
    <footer class="footer">CB.7 · Independent HTML research note · ClayB-PressureGeometry-20260906 · 2026-09-06</footer>
  </main>'''


EN_MAIN = r'''  <main data-language="en">
    <header class="hero">
      <div>
        <div class="kicker">CB.7 · Independent Clay-B analytic note · 2026-09-06</div>
        <h1>CB.7 | Pressure-work signs, velocity direction, and the critical condition</h1>
        <p class="deck">The complete local L³ identity separates dissipation from pressure work that may drive growth. For fixed energy bound M and radius r, the velocity-weighted far-source pressure work can be paid. A direction decomposition gives a zero-safe conditional interface, but energy does not supply the required critical control. An explicit periodic construction then proves that pressure work has no universal dissipative sign.</p>
        <p><strong>The weighted far-field smallness holds only for the same fixed M and r; it pays neither the near field, transport, nor the outer shell. F∈L²_tL³_x is an extra hypothesis, not an energy consequence. The explicit positive/negative examples change the initial data and increase its energy, giving only instantaneous and short-time behavior. The periodic zero-line example does not decide necessity in Vasseur's original whole-space class. G remains OPEN. NOT CLAY. No novelty or publication-level claim.</strong></p>
        <div class="badges"><span class="badge">PROVED LOCALLY</span><span class="badge">LITERATURE</span><span class="badge">CONDITIONAL</span><span class="badge">FINITE: NONE</span><span class="badge">NO FIGURE</span><span class="badge">NO SIMULATION</span><span class="badge">OPEN</span><span class="badge">NOT CLAY</span></div>
      </div>
      <aside class="stamp"><strong>Claim boundary</strong><p class="proved">Fixed-M/r far-pressure work: paid</p><p class="proved">Directional dissipation split: proved</p><p>Critical space-time control of F: conditional</p><p class="proved">Both pressure-work signs: constructed</p><p class="proved">Short-time genuine NS growth: proved</p><p>Finite computation: none</p><p class="open">Near field / shell / F evolution / G: OPEN</p></aside>
    </header>
    <article>
      <section><div class="section-no">01 / Result map</div><h2>One term is paid, one hypothesis is isolated, and one sign shortcut is ruled out</h2><div class="grid"><div class="card"><strong class="proved">Fixed-ball far work</strong>For the same solution at fixed M and r, weighted far-source pressure work decays relative to terminal L³ energy as L⁻⁷.</div><div class="card"><strong>Direction condition</strong>The zero-safe F connects direction structure to a continuation criterion, but critical L²_tL³_x control is not supplied by energy.</div><div class="card"><strong class="open">Pressure sign</strong>Pressure work can have either sign; it cannot be treated as dissipation for free, and this alone does not yield persistence.</div></div><p>CB.7 does not close the near-pressure, transport, viscosity, or outer-shell budget for a general fixed ball. It separates the available structure from the missing dynamical control.</p></section>
      <section><div class="section-no">02 / AB.1–AB.5</div><h2>The complete signed L³ budget and the fixed-ball far-field payment</h2><p>Testing the original equation with the zero-regularized χ|u|u gives</p><div class="equation">H_χ'(t) + D_χ(t) = W_χ(t),
H_χ(s) = H_χ(t) + ∫_s^t D_χ(σ)dσ − ∫_s^t W_χ(σ)dσ.                    (AB.2–AB.3)</div><p>Under backward integration, dissipation raises the early-time energy lower bound; signed work is the term that may drive rapid positive growth. At fixed M and r, set L=L_r(t) and δ=c₀r²L⁻⁴. The pointwise far-pressure gradient bound and energy give</p><div class="equation">sup_(s∈[t−δ,t]) |∫_s^t∫χ|u|u·∇q_far| / H_χ(t)
  ≤ C c₀ M⁴ r⁻² L⁻⁷.                                                     (AB.5)</div><p>This tends to zero for fixed M and r as L→∞. It does not replace CB.6's bare pressure impulse by weighted pressure work, and it does not cover an uncontrolled shrinking ball, moving path, near field, or outer shell.</p></section>
      <section><div class="section-no">03 / AB.6–AB.8</div><h2>The standard whole-torus pressure chain leaves a non-absorbable large-L coefficient</h2><p>In the whole-torus prototype, periodic pressure estimates, weighted Cauchy–Schwarz, and the Sobolev inequality with its low mode retained give</p><div class="equation">|W| ≤ C L D + C L^(5/2) D^(1/2)
    ≤ (C L + η)D + C_η L⁵,
H' ≤ (C L + η − 1)D + C_η L⁵.                                           (AB.8)</div><p>For large L, D remains on the wrong side; this is not a closed differential inequality in L alone. A high-frequency divergence-free shear only shows that fixed L cannot bound D above. It is an instantaneous norm check, not a dynamical counterexample to persistence or singularity.</p></section>
      <section><div class="section-no">04 / AC.1–AC.6</div><h2>Velocity direction gives an exact split, but only improves structure and constants</h2><p>Let q=|u|, define e=u/q only where q&gt;0, and extend the weighted quantities by zero on the zero set. Then</p><div class="equation">D = 2D_r + D_θ,
F = q div e = −e·∇q,
W = −∫p q F,
Z_e ≤ min(D_r, 2D_θ) ≤ 2D/5.                                             (AC.2–AC.5)</div><p>The measurable representative of F satisfies |F|≤|∇u| and has no division-by-zero problem. This does not assert that e is an ordinary Sobolev field across the zero set. The split retains extra information when either the radial or angular part is small, but the worst case still leaves C L D_r or C L√(D_rD_θ). A better fixed constant does not create absorption.</p></section>
      <section><div class="section-no">05 / AC.7–AC.12</div><h2>The direction structure yields one explicit conditional continuation interface</h2><p><a href="https://web.ma.utexas.edu/users/vasseur/documents/preprints/NSdirection2.pdf">Vasseur's 2007 author manuscript</a> gives a regularity criterion under additional directional integrability in the whole-space Leray–Hopf class. The direction rewrite is not claimed as new here, and the whole-space quantifiers are not transferred literally to the torus.</p><div class="equation">∫_(t₀)^T ||F(t)||₃² dt &lt; ∞
  ⇒ the periodic smooth solution continues beyond finite time T.          (AC.9)</div><p>The local proof retains the pressure estimate, periodic low mode, Gronwall, L³_tL⁹_x control, and H¹ restart; the final step uses <a href="https://terrytao.wordpress.com/2018/09/16/254a-notes-1-local-well-posedness-of-the-navier-stokes-equations/">standard periodic subcritical local theory</a>. Energy gives only F∈L²_tL²_x, not F∈L²_tL³_x. This is therefore a CONDITIONAL interface, not a general regularity theorem.</p></section>
      <section><div class="section-no">06 / AC.13–AC.14</div><h2>A zero line in a smooth periodic solution can make unweighted direction divergence non-integrable</h2><p>The global smooth periodic Taylor–Green solution</p><div class="equation">u=e^(−2t)(sin x cos y, −cos x sin y, 0),
p=(e^(−4t)/4)(cos 2x + cos 2y)</div><p>has div e=(y²−x²)/r³+O(r) near a zero line. On a fixed angular cone, |div e|≥c/r, so local L^b diverges for b≥2, while weighted F remains bounded. The lower bound is on a fixed cone, not a two-sided comparison in every direction. This periodic example is not an NS singularity and does not decide whether Vasseur's condition is necessary in its original whole-space class.</p></section>
      <section><div class="section-no">07 / AD.1–AD.23</div><h2>Explicit finite-mode initial data make pressure work strictly positive or negative</h2><p>Take Ψ=cos x+cos y+cos(x+y), v=(∂_yΨ,−∂_xΨ,0), and V_ε=(a cos z,sin z,0)+εv with a&gt;1. The background and cross terms create no pressure source. Mode-by-mode calculation with a uniform remainder gives</p><div class="equation">W(V_ε)=ε³κ(a)π²+O(ε⁴),    κ(a)&gt;0.                                 (AD.16)</div><p>Small positive ε gives W&gt;0, while the opposite initial datum gives W&lt;0. The two data generate their own local smooth NS solutions; this is not a sign reversal of one forward trajectory. Scaling by a finite amplitude A gives W(AU)=A⁴W(U) and D(AU)=A³D(U), so H'(0)&gt;0 for large enough A and remains positive for a short positive interval. Initial energy grows at the same time, and no A-uniform lifespan is claimed. The example does not reach mature time, fixed energy, or the first singularity of one fixed solution.</p></section>
      <section><div class="section-no">08 / Boundary, evidence, and next question</div><h2>The next step asks only whether the true evolution of F creates the missing control</h2><table><thead><tr><th>Class</th><th>Scope in this chapter</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>The complete signed local L³ identity; fixed-M/r weighted far-pressure work; the directional dissipation split; both pressure-work signs and large-amplitude short-time genuine NS growth.</td></tr><tr><td>LITERATURE / CONDITIONAL</td><td>Vasseur's whole-space direction criterion is background; the periodic F∈L²_tL³_x continuation interface is an extra hypothesis not derived from energy.</td></tr><tr><td>FINITE COMPUTATION</td><td>None; no simulation, numerical certificate, or scientific figure.</td></tr><tr><td>OPEN</td><td>True evolution control of F; near pressure, transport, viscosity, and the outer shell; shrinking balls and the original moving path; G/G-P/G-C, R.216–R.217, and the existing U/V/W/Y gaps.</td></tr></tbody></table><p class="note">Scientific source commit: 40b18a9c29499f4956d72e197f8d285bd3f6b453. Freeze commit: e63575d6bbb81332441d74c0916c5663e89ac74c. Six scientific sources, three dependencies, and two frozen-envelope files are SHA-256-bound; the three mathematical sources contain 45 formula tags. Internal actual-file review is not external peer review.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_mature_l3_budget_preflight_20260906.md">Local L³ budget</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_geometry_20260906.md">Pressure-direction structure</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_sign_20260906.md">Pressure-work sign construction</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_geometry_independent_audit_20260906.md">Independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_geometry_frozen_ledger_20260906.json">Portable ledger</a></p><p><strong>This chapter generates no new reader PDF, figure, simulation, DGX data, or cumulative recap. No novelty, priority, publication-level, or Clay regularity claim is made. G OPEN / NOT CLAY.</strong></p></section>
    </article>
    <footer class="footer">CB.7 · Independent HTML research note · ClayB-PressureGeometry-20260906 · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-pressure-geometry" aria-labelledby="clay-b-pressure-geometry-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.7 · INDEPENDENT CLAY-B ANALYTIC NOTE · 2026-09-06 · PRESSURE GEOMETRY</p><h2 class="route-map-title" id="clay-b-pressure-geometry-title">CB.7｜压力功的符号、速度方向与临界条件</h2><p class="route-map-intro">固定 M、r 的带权远源压力功相对终点 L³ 能量按 L⁻⁷ 衰减；方向分解给出零集安全的条件接口，但能量只到 F∈L²_tL²_x，没有给出所需的 L²_tL³_x。显式有限模态初值使压力功取正负两种符号，并可产生放大初值能量后的短时真实 NS L³ 增长。近源、外壳、F 的真实演化与合同 G 仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 压力几何笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-pressure-geometry-20260906.html">阅读最新 CB.7 压力几何笔记 →</a><a href="/literature-review.html#clay-b-pressure-geometry-boundary">查看文献与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 压力几何结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>固定 M/r 远源压力功：已支付</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>F 的 L²_tL³_x 控制：条件性</span><span><i class="route-legend-mark current" aria-hidden="true"></i>压力功无普适符号；F 演化 OPEN · NOT CLAY</span></div></div></section>'''


CB7_ROW = '''          <div class="tree-row clay-b-pressure-geometry-row">
            <article class="tree-node current">
              <div class="tree-node-head">
                <span class="route-range">CB.7 · 2026-09-06 · AB/AC/AD PRESSURE GEOMETRY</span>
                <span class="tree-state current">当前路线边界</span>
              </div>
              <h3>CB.7｜从带权远源压力功到方向临界缺口</h3>
              <p>AB 给出完整带符号局部 L³ 预算，并在固定 M、r 下支付带速度权重的远源压力功；标准全环面链条仍留下不可吸收的大 L 系数。AC 以零集安全的 F=q div e 分解方向耗散，并证明 F∈L²_tL³_x 的条件延拓接口，但能量只给 L²_tL²_x。</p>
              <p>AD 的显式有限模态周期初值使压力功严格取正负两种符号；有限幅值放大可产生真实 NS 的瞬时和短时 L³ 增长，同时放大初值能量。周期 Taylor–Green 零线只说明同型未加权方向条件不是周期光滑性的必要条件，不判定 Vasseur 全空间原类中的必要性。</p>
              <p class="tree-path">CB.6 集中与持留缺口 → AB 带符号 L³ 预算 → 固定 M/r 远源压力功 → AC 零集安全方向分解 → 条件 F∈L²_tL³_x 延拓 → AD 压力功正负号 → F 真实演化 OPEN</p>
              <p><a href="/notes/clay-b-concentration-limits-20260906.html">CB.6：集中与持留边界</a> · <a href="/notes/clay-b-pressure-geometry-20260906.html">CB.7：压力功与方向几何</a></p>
            </article>
            <aside class="tree-branch right current">
              <span class="tree-state current">OPEN · NOT CLAY</span>
              <h3>下一研发问题：F 的真实演化是否产生可支付控制</h3>
              <p>在 q&gt;0 上推导 F=−eᵀ(∇u)e 的完整物质热演化，逐项保留压力 Hessian、方向导数、高阶项与速度 cutoff；只有能由同一解能量和已知耗散支付的新结构才算推进。该问题尚未冻结。</p>
            </aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.8 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.7</h3><p>CB.8 只是下一章占位，不是已完成研究。F 的真实演化控制、近源压力、黏性、输运与外壳、缩球及原移动路径、G/G-P/G-C 尚未冻结；不把后续研发写成已证结论。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-pressure-geometry-boundary">CB.7 · Clay-B 压力功、速度方向与临界条件的文献和主张边界</h3><p><a href="https://web.ma.utexas.edu/users/vasseur/documents/preprints/NSdirection2.pdf">Vasseur, author manuscript dated 2007-04-25</a>承担全空间 Leray–Hopf 类中附加方向可积性正则准则及其中间加权结构的文献背景；本站已核对全文六页，但不把全空间量词直接移植到周期域，也不把方向重写声明为新发现。<a href="https://terrytao.wordpress.com/2018/09/16/254a-notes-1-local-well-posedness-of-the-navier-stokes-equations/">Tao, Notes 1, Remark 46</a>只承担周期次临界局部理论与 H¹ 重启范围背景。</p><div class="boundary"><strong>CB.7 · ClayB-PressureGeometry-20260906 公开边界</strong><p>PROVED LOCALLY：零速度正则化后的完整带符号局部 L³ 恒等式；固定同一解、固定 M/r 时带权远源压力功相对界 Cc₀M⁴r⁻²L⁻⁷；零集安全的 D=2D_r+D_θ、F=q div e=−e·∇q、W=−∫pqF 及 Z_e≤2D/5；显式零均值有限模态周期初值的压力功严格正负号；有限幅值放大后的真实黏性一 NS 瞬时及短时 L³ 增长。LITERATURE / CONDITIONAL：Vasseur 全空间方向准则为已知文献；周期 F∈L²_tL³_x 条件可推出 L³_tL⁹_x、H¹ 重启与越过有限 T 的延拓，但该条件没有由能量给出。STRICT LIMITS：远源小量固定 M/r，不支付近源、输运或外壳；短时符号例放大初值能量，不触及成熟时间或固定解首次奇点；周期 Taylor–Green 零线只给固定角锥 1/r 下界，不判定 Vasseur 全空间原类中的必要性。FINITE COMPUTATION：无。OPEN：F 的真实演化控制、近源压力、输运、黏性、外壳、缩球、原移动路径、G/G-P/G-C、R.216–R.217 与此前 U/V/W/Y 缺口。没有图件、仿真、数值证书、新颖性、优先权、发表等级或 Clay 正则性主张。NOT CLAY。<a href="/notes/clay-b-pressure-geometry-20260906.html">阅读完整 CB.7 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-concentration-limits-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>压力功的符号、速度方向与临界条件</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 带符号局部 L³ 预算、固定球远源压力功、速度方向条件接口与压力功正负号的双语解析笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.7 · {DISPLAY_ID}</strong></header>', template, count=1)
    template, count = re.subn(
        r'  <main data-language="zh">[\s\S]*?  </main>\n\n  <main data-language="en">[\s\S]*?  </main>',
        ZH_MAIN + "\n\n" + EN_MAIN,
        template,
        count=1,
    )
    if count != 1:
        raise RuntimeError("note bilingual template drift")
    return template


def update_home(value: str) -> str:
    value = set_version(value, "综述", refresh=True)
    value = re.sub(r'<strong>v\d+\.\d+</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', value, count=1)
    value, count = re.subn(
        r'<section class="route-overview independent-release-spotlight"[\s\S]*?</section>',
        SPOTLIGHT,
        value,
        count=1,
    )
    if count != 1:
        raise RuntimeError("independent spotlight drift")
    value = value.replace("CB.1–CB.6", "CB.1–CB.7")
    value = value.replace(
        "fixed-ball concentration / original path / solution-dependent radii / persistence costs",
        "weighted far-pressure work / direction geometry / sign obstruction / F evolution",
        1,
    )
    old_focus = "Clay-B 的固定球集中可进入固定尺度原路径，也可经对角化得到解依赖慢缩半径，但这不是预设幂律或单一变尺度路径。真正的平滑 NS 族排除了不支付初值或远场成本的全窗口持留；固定解的远源压力冲量可支付，近源压力、黏性、成熟时间与首次奇点接口仍开放。"
    new_focus = "Clay-B 的固定 M/r 带权远源压力功已经支付；零集安全的方向分解给出 F∈L²_tL³_x 条件延拓接口，但能量只到 L²_tL²_x。显式周期初值证明压力功没有普适耗散符号；近源、外壳、F 的真实演化与合同 G 仍开放。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")

    if 'class="tree-row clay-b-pressure-geometry-row"' in value:
        if "Clay-B 独立路线停在 CB.7" not in value or "CB.8 · NEXT" not in value:
            raise RuntimeError("existing CB.7 route boundary drift")
        return value

    cb6_start = value.index('<div class="tree-row clay-b-concentration-limits-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb6_start)
    cb6 = value[cb6_start:boundary_start]
    cb6 = cb6.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb6 = cb6.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb6, aside_count = re.subn(
        r'<aside class="tree-branch right current">[\s\S]*?</aside>',
        '<aside class="tree-branch right kept"><span class="tree-state">NEXT TEST COMPLETED</span><h3>压力功几何与方向接口已进入 CB.7</h3><p>固定 M/r 的带权远源功、零集安全方向分解、条件 F 接口与压力功正负号已经分开；结果见下一个正式路线节点。</p></aside>',
        cb6,
        count=1,
    )
    if aside_count != 1:
        raise RuntimeError("CB.6 branch drift")
    value = value[:cb6_start] + cb6 + value[boundary_start:]
    value, boundary_count = re.subn(
        r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>',
        CB7_ROW + '\n        </div>\n      </div>\n    </section>',
        value,
        count=1,
    )
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-pressure-geometry-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 7
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.7"
    payload["nextIndependentChapter"] = "CB.8"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1",
            "kind": "independent-analytic-note",
            "releaseId": SLUG,
            "displayReleaseId": DISPLAY_ID,
            "chapter": "CB.7",
            "sourceCommit": "40b18a9c29499f4956d72e197f8d285bd3f6b453",
            "baseCommit": "b462101c34b2479580048893485e4ab291a9fcff",
            "handoffCommit": "e63575d6bbb81332441d74c0916c5663e89ac74c",
            "logicalPredecessor": "ClayB-ConcentrationLimits-20260906",
            "html": f"public/notes/{SLUG}.html",
            "pdfGenerated": False,
            "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-pressure-geometry-20260906-gate.test.mjs",
            "publicationTest": "tests/clay-b-pressure-geometry-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-pressure-geometry-20260906-translations.mjs",
            "browserQaScript": "scripts/qa-publication-browser.mjs",
            "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False,
            "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE",
            "simulationRequired": False,
            "recapRequired": False,
            "advancesCanonicalR0Series": False,
            "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "FIXED_M_R_WEIGHTED_FAR_PRESSURE_WORK_PROVED_DIRECTION_SPLIT_PROVED_PERIODIC_F_L2T_L3X_CONTINUATION_CONDITIONAL_ENERGY_ONLY_L2T_L2X_EXPLICIT_BOTH_PRESSURE_WORK_SIGNS_AND_SHORT_TIME_TRUE_NS_GROWTH_PROVED_INITIAL_ENERGY_GROWS_PERIODIC_ZERO_LINE_NOT_WHOLE_SPACE_NECESSITY_NEAR_SHELL_F_EVOLUTION_G_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in [
        "CB.7", DISPLAY_ID, "Pressure-work signs", "C c₀ M⁴ r⁻² L⁻⁷", "F∈L²_tL³_x",
        "both pressure-work signs", "Vasseur's original whole-space class", "FINITE: NONE", "OPEN", "NOT CLAY",
    ]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1:
        raise RuntimeError("bilingual main count drift")
    if note.count("<section>") != 16 or "<img" in note:
        raise RuntimeError("note section or figure boundary drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage spotlight count drift")
    for marker in [
        'id="clay-b-pressure-geometry"', 'class="route-tree r0-route-tree"',
        'class="route-tree clay-b-route-tree"', 'class="tree-row clay-b-pressure-geometry-row"',
        "CB.1–CB.7", "Clay-B 独立路线停在 CB.7", "CB.8 · NEXT", f"/notes/{SLUG}.html",
    ]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if '<article class="tree-node current">' in home[
        home.index('class="tree-row clay-b-concentration-limits-row"'):
        home.index('class="tree-row clay-b-pressure-geometry-row"')
    ]:
        raise RuntimeError("CB.6 must no longer be current")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-pressure-geometry-boundary"' not in literature or "CB.7 · ClayB-PressureGeometry-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary drift")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or "CB.7 · ClayB-PressureGeometry-20260906" not in index or "7 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION:
        raise RuntimeError("site version drift")
    if site.get("latestIndependentChapter") != "CB.7" or site.get("nextIndependentChapter") != "CB.8":
        raise RuntimeError("site chapter metadata drift")
    if manifest.get("latestPublication", {}).get("releaseId") != SLUG:
        raise RuntimeError("latest publication drift")
    if (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("new reader PDF must remain absent")


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
print(json.dumps({
    "schemaVersion": "clay-b-pressure-geometry-generation-v1",
    "releaseId": DISPLAY_ID,
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "siteVersion": VERSION,
    "chapter": "CB.7",
    "canonicalR0Endpoint": "R0.76L",
    "independentSpotlightCount": 1,
    "readerPdf": "OMIT_NEW",
}, ensure_ascii=False))
