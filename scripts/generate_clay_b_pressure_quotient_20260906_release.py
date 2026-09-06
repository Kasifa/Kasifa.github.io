#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB PressureQuotient CB.8 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.52"
SLUG = "clay-b-pressure-quotient-20260906"
DISPLAY_ID = "ClayB-PressureQuotient-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in __import__("sys").argv[1:]


ZH_MAIN = '''  <main data-language="zh">
    <article>
      <header class="hero">
        <div class="kicker">CB.8 · 独立 Clay-B 解析笔记 · 2026-09-06</div>
        <h1>CB.8｜压力投影：抵消成立，一个特定瞬时残差预算失败</h1>
        <p class="dek">只依赖速度模长的压力部分对全域 L³ 压力功不可见；相应残差时间积分给出条件延拓接口，但能量没有支付它。固定总能量单泡构造排除一条具体瞬时残差界，同时也显示大残差可以来自完全不做压力功的 F=0 平台。</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>LITERATURE / CONDITIONAL</span><span>FINITE: NONE</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / 结论地图</div><h2>一个精确抵消、一个条件接口、一个准确反检查</h2><div class="grid"><div class="card"><strong class="proved">全域投影</strong>对所有合法的速率函数 Φ，都有 ∫qΦ(q)F=0；压力功只看 p−P_qp。</div><div class="card"><strong>条件延拓</strong>若 ∫R²/H dt 有限，则周期光滑解可延拓；这不是能量自动给出的估计。</div><div class="card"><strong class="open">瞬时障碍</strong>固定 L² 能量仍不能用 H(1+||∇u||²) 普适控制 R²；但该例不说明 W 很大。</div></div><p>CB.8 没有支付近源、外壳、成熟时间、固定轨道时间积分或合同 G。</p></section>
      <section><div class="section-no">02 / AE.1–AE.19</div><h2>F 的真实演化已完整写出，但当前估计没有闭合</h2><p>在 q&gt;0 上，q=|u|、e=u/q、F=−e·∇q。两条独立代数链得到一致的物质热演化：压力 Hessian、方向弯曲、二阶速度导数和零集退化全部保留。幅值方程中的有利负项只恢复标准 L³ 耗散。</p><div class="equation">Lq = −e·∇p − q|∇e|²,
LA = −A² − ∇²p.                                                   (AE.6, AE.10)</div><p>当前逐点分部积分没有闭合，不等于所有加权弱形式不可能；对 1/q 使用一致界还需要额外的 q≥κ 局部非退化条件。</p></section>
      <section><div class="section-no">03 / AF.1–AF.13</div><h2>速率函数正交与最佳加权压力投影</h2><p>令 dμ=q dx，在零集把 F 取零。Lipschitz 原函数、coarea 和 Sobolev 链式法则给出</p><div class="equation">∫ q Φ(q) F dx = 0,
W = −∫ q (p−P_qp) F dx,
R² = inf_Φ ∫ q|p−Φ(q)|² dx.                                  (AF.4, AF.10–AF.11)</div><p>P_q 是 L²(q dx) 中到只依赖 q 的函数空间的正交投影。平台原子、同速不同分支、压力 gauge、零状态和时间 Borel 可测性均单独处理；R² 是未归一化条件方差积分，不是压力总范数。</p></section>
      <section><div class="section-no">04 / AF.14–AF.22</div><h2>R²/H 的时间可积性足以延拓，但只是附加条件</h2><div class="equation">H′ + ½D ≤ ½R²,
∫_s^(T*) R²/H dt &lt; ∞  ⇒  u∈L³_tL⁹_x  ⇒ H¹ restart.             (AF.17–AF.22)</div><p>证明保留周期 Sobolev 的低模项，并接已经核查的 H¹ 重启。当前没有从基本能量推出该时间积分，因此不能把条件准则写成一般正则性结论。</p></section>
      <section><div class="section-no">05 / AH.1–AH.21</div><h2>固定总能量仍排除一条具体瞬时残差预算</h2><p>对任意 E₀&gt;0，构造一只紧支撑无散种子：在球内速度为非零常向量，远处支撑分离的涡却使球内压力不恒定。缩成单泡并嵌入环面后，</p><div class="equation">||u_ε||₂²=E₀,
H(u_ε)≈ε^(−3/2),  ||∇u_ε||₂²≈ε^(−2),  R²(u_ε)≳ε^(−9/2),
(R²/H)/(1+||∇u_ε||₂²) ≳ ε^(−1) → ∞.                           (AH.14, AH.20–AH.21)</div><p>因此不存在只依赖 E₀ 的 C(E₀)，使所有光滑周期无散初值满足 R²≤C(E₀)H(1+||∇u||₂²)。证明保留 Newtonian 分布 Hessian 和周期光滑余项，不使用数值拟合。</p></section>
      <section><div class="section-no">06 / AH.22</div><h2>大残差来自 F=0 平台，不等于大压力功</h2><div class="equation">F=0,
p u·∇q=0  on the constant-speed platform.                         (AH.22)</div><p>反检查揭示 R² 会把常速平台上不做功的远源压力变化也计入。它只否定包含初始时刻的特定瞬时界，不证明同一固定解的时间积分失败，也不触及成熟时间、首次奇点、反向持留或合同 G。</p></section>
      <section><div class="section-no">07 / AG.1–AG.14</div><h2>局部化保留外壳；Bernoulli 只重组输运</h2><div class="equation">K_χ(p)=K_χ(p−Φ(q))+∫[qΦ(q)−A_Φ(q)]u·∇χ.                   (AG.6)</div><p>外壳通量没有固定符号。取 Φ(q)=−q²/2 得总压 Q=p+q²/2，它恰把显式输运并入总压功，没有让输运或临界大系数消失。环面上只有整组正则等值面的通量和为零，单个非分隔连通分量不必为零。</p></section>
      <section><div class="section-no">08 / 文献、证据与下一问题</div><h2>不把 pressure moderator 重写当作新机制</h2><p><a href="https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/12230/Tran_2016_Regularity_AML_AAM.pdf?isAllowed=y&amp;sequence=1">Tran–Yu 的 pressure moderator 引理</a>已经包含光滑速率函数抵消；<a href="https://www.cambridge.org/core/services/aop-cambridge-core/content/view/CE28509C5B6844BC5F27F3EF52075E47/S0022112020010332a.pdf/velocitypressure_correlation_in_navierstokes_flows_and_the_problem_of_global_regularity.pdf">Tran–Yu–Dritschel 2021</a>给出相关的压力—速度条件准则。本站只把周期 Borel/平台/投影细节和准确反检查作为本地核查，不作新颖性、优先权或发表等级声明。</p><table><thead><tr><th>类别</th><th>本章范围</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>AE 完整演化式；AF 正交、投影和残差恒等式；AG 外壳与 Bernoulli 重组；AH 固定能量瞬时反检查。</td></tr><tr><td>LITERATURE / CONDITIONAL</td><td>moderator 核心抵消已有文献；∫R²/H dt 延拓是额外条件，未由能量推出。</td></tr><tr><td>FINITE COMPUTATION</td><td>无；没有仿真、数值证书或科学图。</td></tr><tr><td>OPEN</td><td>真实有符号压力功的能量已付时空控制；近源、外壳、成熟时间、固定解首次奇点、缩球、原路径、G/G-P/G-C。</td></tr></tbody></table><p class="note">科学源提交：094124aa2e6d74be4400e5d3e5a969d83acf9468；冻结提交：02c0cbba61060fe268e0dc13877298faf26a1311。八份科学源、四份依赖和两份冻结信封按 SHA-256 绑定；四份数学源共 77 个公式标签。内部实际文件审查不是外部同行评审。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_longitudinal_strain_preflight_20260906.md">AE 演化</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_projection_20260906.md">AF 投影</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_bernoulli_shell_20260906.md">AG 外壳</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_residual_obstruction_20260906.md">AH 反检查</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_quotient_independent_audit_20260906.md">独立审查</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_quotient_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap。独立论文 v2 私有包不在本次发布范围。G OPEN / NOT CLAY。</strong></p></section>
    </article>
    <footer class="footer">CB.8 · Independent HTML research note · ClayB-PressureQuotient-20260906 · 2026-09-06</footer>
  </main>'''


EN_MAIN = '''  <main data-language="en">
    <article>
      <header class="hero">
        <div class="kicker">CB.8 · Independent Clay-B analytic note · 2026-09-06</div>
        <h1>CB.8 | Pressure projection: the cancellation holds, and one specific instantaneous residual budget fails</h1>
        <p class="dek">The part of pressure depending only on speed is invisible to global L³ pressure work. Time integrability of the residual gives a conditional continuation interface, but energy does not pay for it. A single-bubble construction at fixed total energy excludes one specific instantaneous residual bound while also showing that a large residual can come from an F=0 plateau that does no pressure work.</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>LITERATURE / CONDITIONAL</span><span>FINITE: NONE</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / Result map</div><h2>One exact cancellation, one conditional interface, and one precise stress test</h2><div class="grid"><div class="card"><strong class="proved">Global projection</strong>For every admissible speed function Φ, ∫qΦ(q)F=0; pressure work sees only p−P_qp.</div><div class="card"><strong>Conditional continuation</strong>If ∫R²/H dt is finite, the periodic smooth solution continues; this estimate is not automatic from energy.</div><div class="card"><strong class="open">Instantaneous obstruction</strong>At fixed L² energy, H(1+||∇u||²) still cannot universally control R²; the example does not show that W is large.</div></div><p>CB.8 does not pay the near field, outer shell, mature time, a fixed-trajectory time integral, or contract G.</p></section>
      <section><div class="section-no">02 / AE.1–AE.19</div><h2>The genuine evolution of F is complete, but the current estimate does not close</h2><p>On q&gt;0, let q=|u|, e=u/q, and F=−e·∇q. Two independent algebraic chains give the same material heat evolution, retaining the pressure Hessian, direction curvature, second velocity derivatives, and zero-set degeneracy. The favorable negative term in the amplitude equation only recovers the standard L³ dissipation.</p><div class="equation">Lq = −e·∇p − q|∇e|²,
LA = −A² − ∇²p.                                                   (AE.6, AE.10)</div><p>The present pointwise integration by parts does not close; this is not an impossibility theorem for all weighted weak formulations. Uniform use of 1/q also requires the extra local nondegeneracy q≥κ.</p></section>
      <section><div class="section-no">03 / AF.1–AF.13</div><h2>Orthogonality of speed functions and the best weighted pressure projection</h2><p>Let dμ=q dx and set F=0 on the zero set. A Lipschitz primitive, coarea, and the Sobolev chain rule give</p><div class="equation">∫ q Φ(q) F dx = 0,
W = −∫ q (p−P_qp) F dx,
R² = inf_Φ ∫ q|p−Φ(q)|² dx.                                  (AF.4, AF.10–AF.11)</div><p>P_q is the orthogonal projection in L²(q dx) onto functions depending only on q. Plateau atoms, distinct branches at the same speed, pressure gauge, the zero state, and Borel time measurability are handled separately. R² is an unnormalized conditional-variance integral, not the total pressure norm.</p></section>
      <section><div class="section-no">04 / AF.14–AF.22</div><h2>Time integrability of R²/H is sufficient for continuation, but remains an extra condition</h2><div class="equation">H′ + ½D ≤ ½R²,
∫_s^(T*) R²/H dt &lt; ∞  ⇒  u∈L³_tL⁹_x  ⇒ H¹ restart.             (AF.17–AF.22)</div><p>The proof retains the periodic low mode in Sobolev and then uses the already-audited H¹ restart. Basic energy has not been shown to imply this time integral, so the conditional criterion is not a general regularity result.</p></section>
      <section><div class="section-no">05 / AH.1–AH.21</div><h2>Fixed total energy still excludes one specific instantaneous residual budget</h2><p>For every E₀&gt;0, construct a compactly supported divergence-free seed that is a nonzero constant vector on a ball while a separated remote vortex makes pressure nonconstant there. After shrinking a single bubble and embedding it in the torus,</p><div class="equation">||u_ε||₂²=E₀,
H(u_ε)≈ε^(−3/2),  ||∇u_ε||₂²≈ε^(−2),  R²(u_ε)≳ε^(−9/2),
(R²/H)/(1+||∇u_ε||₂²) ≳ ε^(−1) → ∞.                           (AH.14, AH.20–AH.21)</div><p>Hence no C(E₀) depending only on E₀ can make R²≤C(E₀)H(1+||∇u||₂²) hold for every smooth periodic divergence-free datum. The proof retains the distributional Newtonian Hessian and the smooth periodic remainder; it uses no numerical fit.</p></section>
      <section><div class="section-no">06 / AH.22</div><h2>The large residual comes from an F=0 plateau, not large pressure work</h2><div class="equation">F=0,
p u·∇q=0  on the constant-speed platform.                         (AH.22)</div><p>The stress test shows that R² counts remote pressure variation that does no work on a constant-speed plateau. It excludes only the stated instantaneous bound including initial time. It does not prove failure of a time integral along one fixed solution and does not reach mature time, a first singularity, backward persistence, or contract G.</p></section>
      <section><div class="section-no">07 / AG.1–AG.14</div><h2>Localization retains the shell; Bernoulli only recombines transport</h2><div class="equation">K_χ(p)=K_χ(p−Φ(q))+∫[qΦ(q)−A_Φ(q)]u·∇χ.                   (AG.6)</div><p>The shell flux has no fixed sign. Taking Φ(q)=−q²/2 gives total pressure Q=p+q²/2, which exactly moves explicit transport into total-pressure work without making transport or the large critical coefficient disappear. On the torus, only the sum of fluxes across all regular level-set components is zero; a single nonseparating component need not have zero flux.</p></section>
      <section><div class="section-no">08 / Literature, evidence, and next question</div><h2>The pressure-moderator rewrite is not presented as a new mechanism</h2><p><a href="https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/12230/Tran_2016_Regularity_AML_AAM.pdf?isAllowed=y&amp;sequence=1">Tran–Yu's pressure-moderator lemma</a> already contains the smooth speed-function cancellation. <a href="https://www.cambridge.org/core/services/aop-cambridge-core/content/view/CE28509C5B6844BC5F27F3EF52075E47/S0022112020010332a.pdf/velocitypressure_correlation_in_navierstokes_flows_and_the_problem_of_global_regularity.pdf">Tran–Yu–Dritschel 2021</a> gives related conditional pressure–velocity criteria. This site treats the periodic Borel, plateau, and projection details and the precise stress test as local checks, with no novelty, priority, or publication-level claim.</p><table><thead><tr><th>Class</th><th>Scope here</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>AE complete evolution; AF orthogonality, projection, and residual identities; AG shell and Bernoulli recombination; AH fixed-energy instantaneous stress test.</td></tr><tr><td>LITERATURE / CONDITIONAL</td><td>The core moderator cancellation has prior literature; ∫R²/H dt continuation is an extra condition not derived from energy.</td></tr><tr><td>FINITE COMPUTATION</td><td>None; there is no simulation, numerical certificate, or scientific figure.</td></tr><tr><td>OPEN</td><td>Energy-paid spacetime control of genuine signed pressure work; near field, outer shell, mature time, first singularity of a fixed solution, shrinking balls, original paths, and G/G-P/G-C.</td></tr></tbody></table><p class="note">Scientific source commit: 094124aa2e6d74be4400e5d3e5a969d83acf9468; freeze commit: 02c0cbba61060fe268e0dc13877298faf26a1311. Eight scientific sources, four dependencies, and two frozen envelopes are SHA-256-bound; the four mathematical sources contain 77 formula tags. Internal actual-file review is not external peer review.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_longitudinal_strain_preflight_20260906.md">AE evolution</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_projection_20260906.md">AF projection</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_bernoulli_shell_20260906.md">AG shell</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_residual_obstruction_20260906.md">AH stress test</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_quotient_independent_audit_20260906.md">independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_pressure_quotient_frozen_ledger_20260906.json">portable ledger</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap. The private independent-paper v2 package is outside this release. G OPEN / NOT CLAY.</strong></p></section>
    </article>
    <footer class="footer">CB.8 · Independent HTML research note · ClayB-PressureQuotient-20260906 · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-pressure-quotient" aria-labelledby="clay-b-pressure-quotient-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.8 · INDEPENDENT CLAY-B ANALYTIC NOTE · 2026-09-06 · PRESSURE QUOTIENT</p><h2 class="route-map-title" id="clay-b-pressure-quotient-title">CB.8｜压力投影：抵消成立，一个特定瞬时残差预算失败</h2><p class="route-map-intro">速率函数压力对全域压力功精确不可见，最佳 L²(q dx) 残差给出条件延拓接口；但固定能量单泡使一条特定瞬时 R²/H 候选界失败。大残差来自 F=0 常速平台，不能读成压力功大、时间积分失败、成熟时间或首次奇点反例。近源、外壳与合同 G 仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 压力投影笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-pressure-quotient-20260906.html">阅读最新 CB.8 压力投影笔记 →</a><a href="/literature-review.html#clay-b-pressure-quotient-boundary">查看文献与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 压力投影结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>速率投影抵消：已证且有文献前例</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>∫R²/H dt 延拓：条件性</span><span><i class="route-legend-mark current" aria-hidden="true"></i>特定瞬时界失败；真实压力功预算 OPEN · NOT CLAY</span></div></div></section>'''


CB8_ROW = '''          <div class="tree-row clay-b-pressure-quotient-row">
            <article class="tree-node current">
              <div class="tree-node-head">
                <span class="route-range">CB.8 · 2026-09-06 · AE/AF/AG/AH PRESSURE QUOTIENT</span>
                <span class="tree-state current">当前路线边界</span>
              </div>
              <h3>CB.8｜速率投影抵消、条件残差准则与固定能量反检查</h3>
              <p>AE 完整写出 F 的真实演化，但压力 Hessian、方向弯曲与二阶速度导数仍未支付。AF 用零集安全的 Borel 原函数证明 ∫qΦ(q)F=0，并在 L²(q dx) 中定义最佳压力残差 R；∫R²/H dt 有限可条件性推出 L³_tL⁹_x 与 H¹ 重启，但能量没有给出该积分。</p>
              <p>AH 的固定总能量单泡令特定瞬时 R²≤C(E₀)H(1+||∇u||²) 候选界失败；下界位于 F=0 常速平台，所以不代表压力功大或轨道时间积分失败。AG 显示局部投影保留外壳，Bernoulli 只重组输运。moderator 核心抵消已有文献前例，不作新颖性声明。</p>
              <p class="tree-path">CB.7 压力几何 → AE 真实 F 演化未闭合 → AF 速率投影与条件延拓 → AH 固定能量瞬时残差界失败但 W 不大 → AG 外壳与 Bernoulli 重组 → 真实有符号压力功配对 OPEN</p>
              <p><a href="/notes/clay-b-pressure-geometry-20260906.html">CB.7：压力功与方向几何</a> · <a href="/notes/clay-b-pressure-quotient-20260906.html">CB.8：压力投影与瞬时反检查</a></p>
            </article>
            <aside class="tree-branch right current">
              <span class="tree-state current">OPEN · NOT CLAY</span>
              <h3>下一研发问题：真实压力功的带符号方向配对</h3>
              <p>从 H′+D=−∫pqF 出发，把能量已付部分和真正正增长区分开；新估计必须排除 F=0 平台的虚假成本，并实际支付近源与外壳，不能只添加另一条临界相关性假设。该问题尚未冻结。</p>
            </aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.9 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.8</h3><p>CB.9 只是下一章占位，不是已完成研究。真实有符号压力功的能量已付时空控制、近源、外壳、成熟时间、固定解首次奇点、缩球、原移动路径及 G/G-P/G-C 尚未冻结；不把后续研发写成已证结论。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-pressure-quotient-boundary">CB.8 · Clay-B 压力投影、残差准则与固定能量反检查的文献和主张边界</h3><p><a href="https://research-repository.st-andrews.ac.uk/bitstream/handle/10023/12230/Tran_2016_Regularity_AML_AAM.pdf?isAllowed=y&amp;sequence=1">Tran–Yu, accepted manuscript, Lemma 1 and equations (6)–(8)</a>已经包含全空间光滑衰减设置中的 pressure moderator；取空间常量系数便包含速率函数抵消的光滑版本，所以该核心抵消不是本站的新发现。<a href="https://www.cambridge.org/core/services/aop-cambridge-core/content/view/CE28509C5B6844BC5F27F3EF52075E47/S0022112020010332a.pdf/velocitypressure_correlation_in_navierstokes_flows_and_the_problem_of_global_regularity.pdf">Tran–Yu–Dritschel 2021, §3.1 and §4.1</a>给出相关的压力—速度混合积分条件准则；本站不把其定性模型讨论作为一般正则性输入。</p><div class="boundary"><strong>CB.8 · ClayB-PressureQuotient-20260906 公开边界</strong><p>PROVED LOCALLY：AE 在 q&gt;0 上的 q、e、A、F 完整演化与两个代数形式，当前估计未闭合且不是加权方法 no-go；AF 对有界 Borel 速率函数的 ∫qΦ(q)F=0、L²(q dx) 条件期望投影、平台/零集/时间可测性和最小残差 R；AG 的准确 cutoff 外壳、Bernoulli 输运重组及整组而非单个非分隔等值面分量的零通量；AH 对每个固定 E₀ 构造光滑零均值周期无散初值，使 (R²/H)/(1+||∇u||²) 无界。LITERATURE / CONDITIONAL：核心 speed-only moderator 抵消已有文献；∫R²/H dt 有限可推出周期 L³_tL⁹_x、H¹ 重启和延拓，但该额外条件没有由能量给出。STRICT LIMITS：AH 只否定 R²≤C(E₀)H(1+||∇u||²) 这一具体瞬时候选界；大残差来自 F=0 平台，不能推出 W 很大、固定轨道时间积分失败、成熟时间或首次奇点反例；Bernoulli 只重组输运，局部投影保留外壳。FINITE COMPUTATION：无。OPEN：真实有符号压力功的能量已付时空控制、近源、外壳、成熟时间、固定解首次奇点、缩球、原路径和 G/G-P/G-C。没有图件、仿真、数值证书、新颖性、优先权、发表等级或 Clay 正则性主张；独立论文 v2 私有包不在本次发布。NOT CLAY。<a href="/notes/clay-b-pressure-quotient-20260906.html">阅读完整 CB.8 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-pressure-geometry-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>压力投影：抵消成立，一个特定瞬时残差预算失败</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 压力速率投影、条件残差延拓、局部外壳与固定能量瞬时残差反检查的双语解析笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = template.replace("h1 { max-width:16ch;", "h1 { max-width:16ch; overflow-wrap:anywhere;", 1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.8 · {DISPLAY_ID}</strong></header>', template, count=1)
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
    value = value.replace("CB.1–CB.7", "CB.1–CB.8")
    value = value.replace(
        "weighted far-pressure work / direction geometry / sign obstruction / F evolution",
        "speed projection / conditional residual / fixed-energy obstruction / signed pairing",
        1,
    )
    old_focus = "Clay-B 的固定 M/r 带权远源压力功已经支付；零集安全的方向分解给出 F∈L²_tL³_x 条件延拓接口，但能量只到 L²_tL²_x。显式周期初值证明压力功没有普适耗散符号；近源、外壳、F 的真实演化与合同 G 仍开放。"
    new_focus = "Clay-B 的速率函数压力对全域压力功精确不可见；最佳加权残差的时间积分给出条件延拓接口，但未由能量支付。固定能量单泡排除一条特定瞬时残差候选界，同时揭示 F=0 平台可产生大残差而不做压力功；近源、外壳与合同 G 仍开放。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")

    if 'class="tree-row clay-b-pressure-quotient-row"' in value:
        if "Clay-B 独立路线停在 CB.8" not in value or "CB.9 · NEXT" not in value:
            raise RuntimeError("existing CB.8 route boundary drift")
        return value

    cb7_start = value.index('<div class="tree-row clay-b-pressure-geometry-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb7_start)
    cb7 = value[cb7_start:boundary_start]
    cb7 = cb7.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb7 = cb7.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb7, aside_count = re.subn(
        r'<aside class="tree-branch right current">[\s\S]*?</aside>',
        '<aside class="tree-branch right kept"><span class="tree-state">NEXT TEST COMPLETED</span><h3>速率投影与残差候选已进入 CB.8</h3><p>核心抵消、条件残差准则、局部外壳与固定能量瞬时反检查已经区分；结果见下一个正式路线节点。</p></aside>',
        cb7,
        count=1,
    )
    if aside_count != 1:
        raise RuntimeError("CB.7 branch drift")
    value = value[:cb7_start] + cb7 + value[boundary_start:]
    value, boundary_count = re.subn(
        r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>',
        CB8_ROW + '\n        </div>\n      </div>\n    </section>',
        value,
        count=1,
    )
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-pressure-quotient-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 8
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.8"
    payload["nextIndependentChapter"] = "CB.9"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1",
            "kind": "independent-analytic-note",
            "releaseId": SLUG,
            "displayReleaseId": DISPLAY_ID,
            "chapter": "CB.8",
            "sourceCommit": "094124aa2e6d74be4400e5d3e5a969d83acf9468",
            "baseCommit": "b113bf0623388c0c17cae9e7313bdf3e02b56f08",
            "handoffCommit": "02c0cbba61060fe268e0dc13877298faf26a1311",
            "logicalPredecessor": "ClayB-PressureGeometry-20260906",
            "html": f"public/notes/{SLUG}.html",
            "pdfGenerated": False,
            "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-pressure-quotient-20260906-gate.test.mjs",
            "publicationTest": "tests/clay-b-pressure-quotient-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-pressure-quotient-20260906-translations.mjs",
            "browserQaScript": "scripts/qa-publication-browser.mjs",
            "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False,
            "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE",
            "simulationRequired": False,
            "recapRequired": False,
            "advancesCanonicalR0Series": False,
            "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "PRESSURE_SPEED_FUNCTION_ORTHOGONALITY_AND_WEIGHTED_PROJECTION_PROVED_MODERATOR_PRIOR_ART_CONDITIONAL_RESIDUAL_TIME_INTEGRAL_CONTINUATION_NOT_ENERGY_PAID_LOCAL_SHELL_RETAINED_BERNOULLI_RECOMBINES_TRANSPORT_FIXED_ENERGY_SPECIFIC_INSTANTANEOUS_RESIDUAL_BOUND_FALSE_LARGE_RESIDUAL_FROM_F_ZERO_NOT_LARGE_W_MATURE_TIME_FIRST_SINGULARITY_G_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in [
        "CB.8", DISPLAY_ID, "one specific instantaneous residual budget fails",
        "∫R²/H dt", "fixed total energy", "F=0 plateau", "moderator",
        "FINITE: NONE", "OPEN", "NOT CLAY",
    ]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1:
        raise RuntimeError("bilingual note structure drift")
    if note.count("<section>") != 16 or "<img" in note:
        raise RuntimeError("note section/image policy drift")
    if f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("new reader PDF must remain absent")

    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in [
        "CB.1–CB.8", "Clay-B 独立路线停在 CB.8", "CB.9 · NEXT",
        'class="tree-row clay-b-pressure-quotient-row"', f"/notes/{SLUG}.html",
    ]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb8 = home.index('class="tree-row clay-b-pressure-quotient-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb8)
    if not (r0_start < r0_boundary < divider < clay_start < cb8 < clay_boundary):
        raise RuntimeError("homepage route topology drift")

    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-pressure-quotient-boundary"' not in literature or "CB.8 · ClayB-PressureQuotient-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or "CB.8 · ClayB-PressureQuotient-20260906" not in index or "8 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION:
        raise RuntimeError("version metadata drift")
    if site.get("latestIndependentChapter") != "CB.8" or site.get("nextIndependentChapter") != "CB.9":
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
print(json.dumps({
    "schemaVersion": "clay-b-pressure-quotient-generation-v1",
    "releaseId": DISPLAY_ID,
    "status": "PASS",
    "mode": "check-only" if CHECK_ONLY else "apply",
    "siteVersion": VERSION,
    "chapter": "CB.8",
    "canonicalR0Endpoint": "R0.76L",
    "independentSpotlightCount": 1,
    "readerPdf": "OMIT_NEW",
}, ensure_ascii=False))
