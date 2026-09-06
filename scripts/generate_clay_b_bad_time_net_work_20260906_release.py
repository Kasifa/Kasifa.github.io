#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB BadTimeNetWork CB.10 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.54"
SLUG = "clay-b-bad-time-net-work-20260906"
DISPLAY_ID = "ClayB-BadTimeNetWork-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in __import__("sys").argv[1:]


ZH_MAIN = '''  <main data-language="zh">
    <article>
      <header class="hero">
        <div class="kicker">CB.10 · 独立 Clay-B 解析笔记 · 2026-09-06</div>
        <h1>CB.10｜坏时间净压力工作：从频率支付到必要下界</h1>
        <p class="dek">同一周期 Navier–Stokes 解、固定中心与固定正则环带上，低频参与压力和局部高频尾较小的好时间已被支付。若存在一列合法的大局部 L³ 成熟窗口，剩余坏时间正净工作必须至少达到终端局部能量量级。这是条件必要下界，不是上界，也不证明大范数序列或奇点存在。</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>FINITE: NONE</span><span>LITERATURE INPUT</span><span>NECESSARY CONDITION</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / 结论地图</div><h2>已付部分、必要集中与未付上界必须分开</h2><div class="grid"><div class="card"><strong class="proved">已付</strong>AM 支付全部含低频速度的压力；AP 给固定正则环带；AO 在局部高频尾小的好时间吸收高高压力。</div><div class="card"><strong class="proved">必要下界</strong>若合法大局部 L³ 成熟窗口序列存在，则 liminf 𝓑_J/Hχ(t)≥1，并保留带权带符号版本。</div><div class="card"><strong class="open">未付</strong>𝓑_J 的真实 NS 上界、缩球一致常数、移动路径和合同 G 仍 OPEN。</div></div><p>本章不制造大范数序列，不断言奇点存在或不存在，也不把固定球结论写成移动缩球结论。</p></section>
      <section><div class="section-no">02 / AK.1–AL.22</div><h2>低频可付，但能量尾没有给出所需时间速率</h2><p>AK 把平滑低频压力作为完整局部配对处理，保留压力内部项与 ∇χ 壳项的 gauge 抵消。若终端固定球范数为 Λ_A、窗口长度 δ=c₀r²Λ_A⁻⁴，则低频成本在 K=o(Λ_A^(7/4)) 时相对 Hχ(t) 消失。</p><div class="equation">∫_J ||P_&gt;K u||₃² dσ ≤ C K⁻¹ A_J,
A_J=∫_J||∇u||₂² dσ.                                      (AK.16)</div><p>能量绝对连续性只给 A_J=o(1)，不给让坏时间比例消失所需的多项式速率。AL 在当前周期规范下复证耗散波数能量接口 𝔡≤1+Ca⁻²ν⁻²||∇u||₂²；L¹_t 控制不能升级成 L^(5/2)_t，也没有支付二次压力输出或截止交换子。</p></section>
      <section><div class="section-no">03 / AM.1–AM.20</div><h2>无散结构支付所有含低频速度的压力</h2><p>写 u=l+h、h=b+w，并精确分解 p(u)=p₀+p_lh+p(h)。b 与 w 的内部交互全部保留在 p(h) 中；分离低高压力 Π(l,w) 因无散获得一个逆频率梯度增益。</p><div class="equation">||p_lh||∞ ≤ C M K²||∇u||₂,
K=Λ_A^(3/4),
(R₀+R_lh)/Hχ(t) → 0.                                  (AM.11, AM.17–AM.19)</div><p>完整测试权重仍是 |u|u。任意固定小份额的 Dχ 吸收梯度部分，其余只用同一解 A_J→0 支付；高高速度自相互作用产生的完整压力 p(h)，包括所有低输出，继续保留。</p></section>
      <section><div class="section-no">04 / AN.1–AN.28</div><h2>全环面小尾原型保留高高压力的所有低输出</h2><p>令 h=P_&gt;K u、p_h=Tij(h_i h_j)、η_K=||h||₃，并仍用完整原速度测试。周期乘子、Calderón–Zygmund 与非齐次 Sobolev 给</p><div class="equation">|W_h| ≤ Cη_K D + Cη_K D^(1/2)||u||₃^(3/2).              (AN.12)</div><p>η_K 小时可吸收一部分耗散，good set 上的当前 H 时间积分也可由能量支付；但坏集合测度小不控制其上的压力功集中。AN 是全域基准，不是局部闭合。</p></section>
      <section><div class="section-no">05 / AP.1–AP.6</div><h2>CKN 文献输入只供应依解的固定正则环带</h2><p>对合同中的同一 suitable continuation，CKN 的部分正则性输入给终端奇异切片 H¹ 测度为零。到指定中心的距离函数为 1-Lipschitz，因此可选一个避开奇异切片的球面；有限正则邻域覆盖再给固定厚度、左时间宽度和速度界。</p><div class="equation">ess sup_{|d*(x)−ρ|&lt;a,
T*−τ&lt;σ&lt;T*} |u(x,σ)| ≤ B.                               (AP.5)</div><p>该环带可依赖解、continuation、T*、中心和半径；它不提供缩球一致常数、内球正则性、压力界或高阶导数界。公开原文访问路径和 OCR 限制在文献边界中保留。</p></section>
      <section><div class="section-no">06 / AO.1–AO.22</div><h2>好时间高高压力可吸收，坏时间净工作原样留下</h2><p>AO 用六个固定半径分开近源和远源，显式估计 [P≤K,θ]u 交换子。扩大球梯度没有偷换成局部耗散，而以固定环带速度界乘全局 ||∇u||₂² 支付。存在与 K 无关的固定 η*，使</p><div class="equation">η_K≤η* ⇒ |Kχ(p_h)|≤¼Dχ+C_S(Hχ+1+||∇u||₂²).            (AO.16)</div><p>合并 AM 后，好时间保留一半耗散；坏时间留下 β_K=Kχ(p_h)−¾Dχ。积分因子处理当前 H，不假定 H 单调，也不把坏集合小测度当作工作积分小。</p></section>
      <section><div class="section-no">07 / AQ.1–AQ.8</div><h2>合法大范数成熟窗口迫使坏时间承担终端量级</h2><p>对同一解、固定环带和固定参数，若 Λ_A=||u(t)||_(L³(B_r))→∞、δ=c₀r²Λ_A⁻⁴、K=Λ_A^(3/4)，且窗口合法并处于成熟时间带，能量插值可在每个窗口中选到实际早时点 s_J，使 Hχ(s_J)/Hχ(t)→0。</p><div class="equation">𝓑_J=∫_(B_K)[Kχ(p_h)−¾Dχ]_+ dσ,
liminf 𝓑_J/Hχ(t) ≥ 1.                                      (AQ.6)</div><p>更精确的 AQ.8 保留积分因子 w_J 和实际带符号 β_K。即使 w_J→1 一致，没有 ∫_(B_K)|β_K| 的控制也不能免费删除权重。这是下界，不是已经得到的上界。</p></section>
      <section><div class="section-no">08 / 量词、文献与下一问题</div><h2>必要条件不会反向制造奇点或大范数序列</h2><p>先固定同一个 suitable continuation、指定中心、AP 环带、半径、截止、能量界和 c₀，再对一列合法窗口取极限。本章不证明该序列存在；若不存在，必要条件不产生存在性结论。若未来从真实 NS 结构推出 𝓑_J=o(Hχ(t))，才可能与 AQ.6 冲突。</p><table><thead><tr><th>类别</th><th>本章范围</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>低频参与压力支付、固定环带好时间局部吸收、坏时间正净工作必要下界与带权符号版本。</td></tr><tr><td>LITERATURE INPUT</td><td>CKN 部分正则性、耗散波数接口及固定环带相关作者稿；访问范围与 OCR 限制明确记录。</td></tr><tr><td>NECESSARY CONDITION</td><td>仅在合法同一解大局部 L³ 序列存在时，𝓑_J/Hχ(t) 的下极限至少为 1。</td></tr><tr><td>OPEN</td><td>𝓑_J 的 NS 上界、缩球一致性、移动路径、G/G-P/G-C、首次奇点排除和一般正则性。</td></tr></tbody></table><p class="note">科学源提交：22c0064338dbad20a6cc37cf054c24850cd2dc2e；冻结提交：ca1bf2ecad5716ef9a4a653806e4a27fbfb2957f。十四份源、三份依赖和两份冻结信封按 SHA-256 绑定；AK–AQ 共 131 个公式标签。内部实际文件审查不是外部同行评审。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_mature_frequency_preflight_20260906.md">AK 低频与能量尾</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_separated_pressure_pair_preflight_20260906.md">AM 低高压力支付</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_fixed_regular_annulus_interface_20260906.md">AP 固定环带</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_local_high_high_pressure_preflight_20260906.md">AO 局部高高压力</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_bad_time_net_work_necessity_20260906.md">AQ 必要下界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_bad_net_work_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap。独立论文私有包不在本次发布范围。G OPEN / NOT CLAY。</strong></p></section>
    </article>
    <footer class="footer">CB.10 · Independent HTML research note · ClayB-BadTimeNetWork-20260906 · 2026-09-06</footer>
  </main>'''


EN_MAIN = '''  <main data-language="en">
    <article>
      <header class="hero">
        <div class="kicker">CB.10 · Independent Clay-B analytic note · 2026-09-06</div>
        <h1>CB.10 | Bad-time net pressure work: from frequency payment to a necessary lower bound</h1>
        <p class="dek">For one periodic Navier–Stokes solution with a fixed center and fixed regular annulus, pressure involving low velocity frequencies and high–high pressure on good times with a small local high-frequency tail are paid. If a legal sequence of mature windows with large local L³ norm exists, the remaining positive bad-time net work must be at least the scale of the terminal local energy. This is a conditional necessary lower bound, not an upper bound, and it proves neither a large-norm sequence nor a singularity.</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>FINITE: NONE</span><span>LITERATURE INPUT</span><span>NECESSARY CONDITION</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / Result map</div><h2>Paid terms, necessary concentration, and the unpaid upper bound are distinct</h2><div class="grid"><div class="card"><strong class="proved">Paid</strong>AM pays all pressure involving low velocity frequencies; AP supplies a fixed regular annulus; AO absorbs high–high pressure on good times with a small local high-frequency tail.</div><div class="card"><strong class="proved">Necessary lower bound</strong>If a legal large-local-L³ mature-window sequence exists, then liminf 𝓑_J/Hχ(t)≥1, together with a weighted signed version.</div><div class="card"><strong class="open">Unpaid</strong>A genuine NS upper bound for 𝓑_J, shrinking-scale uniformity, moving paths, and contract G remain OPEN.</div></div><p>This chapter constructs no large-norm sequence, asserts neither existence nor nonexistence of a singularity, and does not turn a fixed-ball statement into a moving shrinking-ball result.</p></section>
      <section><div class="section-no">02 / AK.1–AL.22</div><h2>Low frequencies are payable, but the energy tail gives no required time rate</h2><p>AK treats smooth low-output pressure as a complete local pairing, preserving gauge cancellation between the interior pressure term and the ∇χ shell term. If Λ_A is the terminal fixed-ball norm and δ=c₀r²Λ_A⁻⁴, the low-frequency cost is o(Hχ(t)) when K=o(Λ_A^(7/4)).</p><div class="equation">∫_J ||P_&gt;K u||₃² dσ ≤ C K⁻¹ A_J,
A_J=∫_J||∇u||₂² dσ.                                      (AK.16)</div><p>Absolute continuity of energy gives only A_J=o(1), not the polynomial rate sufficient to make the bad-time proportion vanish. AL rederives the periodic dissipation-wavenumber energy interface 𝔡≤1+Ca⁻²ν⁻²||∇u||₂². Its L¹_t control does not upgrade to L^(5/2)_t and does not pay quadratic pressure output or cutoff commutators.</p></section>
      <section><div class="section-no">03 / AM.1–AM.20</div><h2>Solenoidality pays every pressure term involving low velocity frequencies</h2><p>Write u=l+h and h=b+w, with the exact decomposition p(u)=p₀+p_lh+p(h). All interactions internal to b and w remain in p(h). Solenoidality gives the separated low–high pressure Π(l,w) an inverse-frequency derivative gain.</p><div class="equation">||p_lh||∞ ≤ C M K²||∇u||₂,
K=Λ_A^(3/4),
(R₀+R_lh)/Hχ(t) → 0.                                  (AM.11, AM.17–AM.19)</div><p>The complete test weight remains |u|u. A fixed small share of Dχ absorbs the gradient term, and the remainder uses only A_J→0 for the same solution. The full pressure p(h) produced by high-frequency self-interaction, including every low output, remains.</p></section>
      <section><div class="section-no">04 / AN.1–AN.28</div><h2>The whole-torus small-tail prototype retains every low output of high–high pressure</h2><p>Let h=P_&gt;K u, p_h=Tij(h_i h_j), and η_K=||h||₃, still testing against the full original velocity. Periodic multipliers, Calderón–Zygmund bounds, and inhomogeneous Sobolev give</p><div class="equation">|W_h| ≤ Cη_K D + Cη_K D^(1/2)||u||₃^(3/2).              (AN.12)</div><p>Small η_K absorbs part of the dissipation, and energy pays the current-H time integral on the good set. But small measure of the bad set does not control concentration of pressure work there. AN is a global benchmark, not local closure.</p></section>
      <section><div class="section-no">05 / AP.1–AP.6</div><h2>The CKN literature input supplies only a solution-dependent fixed regular annulus</h2><p>For the same suitable continuation in the contract, the CKN partial-regularity input makes the terminal singular slice have zero H¹ measure. Distance to the specified center is 1-Lipschitz, so one may choose a sphere avoiding that slice. A finite cover by regular neighborhoods then supplies fixed thickness, a left time width, and a velocity bound.</p><div class="equation">ess sup_{|d*(x)−ρ|&lt;a,
T*−τ&lt;σ&lt;T*} |u(x,σ)| ≤ B.                               (AP.5)</div><p>The annulus may depend on the solution, continuation, T*, center, and radius. It supplies no shrinking-scale uniform constants, interior regularity, pressure bound, or higher-derivative bound. The literature boundary records the actual public access path and OCR limitations.</p></section>
      <section><div class="section-no">06 / AO.1–AO.22</div><h2>Good-time high–high pressure is absorbed; bad-time net work remains intact</h2><p>AO uses six fixed radii to separate near and far sources and explicitly estimates the commutator [P≤K,θ]u. The enlarged-ball gradient is not replaced by local dissipation; it is paid by the fixed annular velocity bound times global ||∇u||₂². A fixed η* independent of K satisfies</p><div class="equation">η_K≤η* ⇒ |Kχ(p_h)|≤¼Dχ+C_S(Hχ+1+||∇u||₂²).            (AO.16)</div><p>After combining AM, one half of dissipation remains on good times, while bad times retain β_K=Kχ(p_h)−¾Dχ. The integrating factor handles current H without assuming monotonicity, and small bad-set measure is not substituted for a small work integral.</p></section>
      <section><div class="section-no">07 / AQ.1–AQ.8</div><h2>A legal mature window with large terminal norm forces terminal-scale bad-time work</h2><p>For the same solution with fixed annulus and parameters, suppose Λ_A=||u(t)||_(L³(B_r))→∞, δ=c₀r²Λ_A⁻⁴, and K=Λ_A^(3/4), with each window legal and mature. Energy interpolation selects an actual early time s_J in each window such that Hχ(s_J)/Hχ(t)→0.</p><div class="equation">𝓑_J=∫_(B_K)[Kχ(p_h)−¾Dχ]_+ dσ,
liminf 𝓑_J/Hχ(t) ≥ 1.                                      (AQ.6)</div><p>The sharper AQ.8 keeps the integrating factor w_J and the genuinely signed β_K. Even though w_J→1 uniformly, the weight cannot be removed without control of ∫_(B_K)|β_K|. This is a lower bound, not the desired upper bound.</p></section>
      <section><div class="section-no">08 / Quantifiers, literature, and next question</div><h2>A necessary condition cannot create a singularity or large-norm sequence in reverse</h2><p>First fix one suitable continuation, the specified center, AP annulus, radius, cutoffs, energy bound, and c₀; only then take a limit along a legal window sequence. This chapter does not prove the sequence exists. If it does not, the necessary condition creates no existence result. Only a future genuine NS estimate 𝓑_J=o(Hχ(t)) could conflict with AQ.6.</p><table><thead><tr><th>Class</th><th>Scope here</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>Payment of low-frequency-involving pressure, fixed-annulus local absorption on good times, the necessary lower bound for positive bad-time net work, and its weighted signed version.</td></tr><tr><td>LITERATURE INPUT</td><td>CKN partial regularity, the dissipation-wavenumber interface, and related fixed-annulus author manuscripts, with access scope and OCR limitations recorded.</td></tr><tr><td>NECESSARY CONDITION</td><td>Only if a legal same-solution large-local-L³ sequence exists, liminf 𝓑_J/Hχ(t) is at least one.</td></tr><tr><td>OPEN</td><td>An NS upper bound for 𝓑_J, shrinking-scale uniformity, moving paths, G/G-P/G-C, first-singularity exclusion, and general regularity.</td></tr></tbody></table><p class="note">Scientific source commit: 22c0064338dbad20a6cc37cf054c24850cd2dc2e; freeze commit: ca1bf2ecad5716ef9a4a653806e4a27fbfb2957f. Fourteen source files, three dependencies, and two frozen envelopes are SHA-256-bound; AK–AQ contain 131 formula tags. Internal actual-file review is not external peer review.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_mature_frequency_preflight_20260906.md">AK low frequencies and energy tail</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_separated_pressure_pair_preflight_20260906.md">AM low–high pressure payment</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_fixed_regular_annulus_interface_20260906.md">AP fixed annulus</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_local_high_high_pressure_preflight_20260906.md">AO local high–high pressure</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_bad_time_net_work_necessity_20260906.md">AQ necessary lower bound</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_bad_net_work_frozen_ledger_20260906.json">portable ledger</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap. The private independent-paper package is outside this release. G OPEN / NOT CLAY.</strong></p></section>
    </article>
    <footer class="footer">CB.10 · Independent HTML research note · ClayB-BadTimeNetWork-20260906 · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-bad-time-net-work" aria-labelledby="clay-b-bad-time-net-work-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.10 · INDEPENDENT CLAY-B ANALYTIC NOTE · 2026-09-06 · BAD-TIME NET WORK</p><h2 class="route-map-title" id="clay-b-bad-time-net-work-title">CB.10｜坏时间净压力工作：从频率支付到必要下界</h2><p class="route-map-intro">同一解的低频参与压力与固定环带好时间高高压力已经支付。若合法的大局部 L³ 成熟窗口序列存在，坏时间正净工作满足 liminf 𝓑_J/Hχ(t)≥1，并保留带权带符号版本。它是条件必要下界，不是上界，不证明序列、奇点或合同 G。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 坏时间净工作笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-bad-time-net-work-20260906.html">阅读最新 CB.10 坏时间净工作笔记 →</a><a href="/literature-review.html#clay-b-bad-time-net-work-boundary">查看文献与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 坏时间净工作结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>低频与好时间压力：已支付</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>坏时间正净工作：必要下界</span><span><i class="route-legend-mark current" aria-hidden="true"></i>所需上界、缩球与 G OPEN · NOT CLAY</span></div></div></section>'''


CB10_ROW = '''          <div class="tree-row clay-b-bad-time-net-work-row">
            <article class="tree-node current">
              <div class="tree-node-head"><span class="route-range">CB.10 · 2026-09-06 · AK–AQ BAD-TIME NET WORK</span><span class="tree-state current">当前路线边界</span></div>
              <h3>CB.10｜频率支付、固定环带与坏时间净工作必要下界</h3>
              <p>AK/AL 定位能量尾的时间速率缺口；AM 借无散结构支付所有含低频速度的压力。AP 从 CKN 文献输入选出依解的固定正则环带，AO 在局部高频尾小的好时间吸收高高压力，同时保留截止交换子、环带能量成本与坏时间带符号净工作。</p>
              <p>AQ 对同一解、固定参数的一列合法大局部 L³ 成熟窗口证明 liminf 𝓑_J/Hχ(t)≥1，并保留实际积分因子和符号。方向是必要下界，不是上界；不证明序列或奇点存在，也不把固定环带常数称为缩球一致。</p>
              <p class="tree-path">CB.9 真实压力功早时增长 → AK/AL 频率速率缺口 → AM 低频参与压力已付 → AP/AO 固定环带好时间已付 → AQ 坏时间正净工作必要下界 → 真实 NS 上界 OPEN</p>
              <p><a href="/notes/clay-b-pressure-work-window-20260906.html">CB.9：正压力功与统一早时窗口</a> · <a href="/notes/clay-b-bad-time-net-work-20260906.html">CB.10：坏时间净工作必要下界</a></p>
            </article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发问题：坏时间带符号高高压力工作的 NS 上界</h3><p>保持 AQ.7–AQ.8 的同一窗口、截止、测试速度、坏时间集合与时间权重，逐频带寻找真实无散增益或符号抵消；不能用坏集合小测度替代工作积分，也不能免费删除积分因子。该问题尚未冻结。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.11 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.10</h3><p>CB.11 只是下一章占位，不是已完成研究。坏时间带符号净工作的真实 NS 上界、缩球一致常数、移动路径、G/G-P/G-C、实际 R.216–R.217 输入与首次奇点排除尚未冻结；不把后续研发写成已证结论。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-bad-time-net-work-boundary">CB.10 · Clay-B 坏时间净工作的文献和主张边界</h3><p><a href="https://doi.org/10.1002/cpa.3160350604">Caffarelli–Kohn–Nirenberg 1982 正式书目入口</a>本轮只返回元数据；实际核对使用<a href="https://www.scribd.com/document/683377073/Caffarelli-1982">公开原文转录</a>的 Theorem B、正则点定义及覆盖位置，转录 OCR 存在符号损坏，因此不声称重审全篇证明。<a href="https://arxiv.org/pdf/1811.00507">Albritton–Barker, Lemma 2.6 and footnote 5</a>与<a href="https://arxiv.org/html/2602.09951v1#S4.SS2">Barker–Popkin, Lemma 4.2.1</a>只用于交叉核对固定环带接口。<a href="https://arxiv.org/pdf/1102.1944">Cheskidov–Shvydkoy</a>和<a href="https://link.springer.com/article/10.1007/s00030-026-01232-0">Cheskidov–Peng</a>的耗散/决定波数具有不同域、范数与量词，不能替代本章的局部压力功预算。</p><div class="boundary"><strong>CB.10 · ClayB-BadTimeNetWork-20260906 公开边界</strong><p>PROVED LOCALLY：AK 支付完整低频压力配对并量化能量高频尾；AL 在周期规范下复证带基线 1 和 a⁻²ν⁻² 依赖的耗散波数能量接口；AM 用无散增益支付所有含低频速度的压力，保留 p(h) 的全部高高低输出；AN 给保留原速度测试的全环面小尾原型；AP 从已知 CKN 部分正则性为同一 suitable continuation 选择依解的固定正则环带；AO 显式处理近远源、频率截止交换子、环带 B||∇u||₂² 成本和积分因子，在局部尾小的好时间吸收高高压力。NECESSARY CONDITION：对同一解、固定环带/半径/截止/能量界/c₀ 的每个合法大局部 L³ 成熟窗口序列，AQ 证明 liminf 𝓑_J/Hχ(t)≥1，其中 𝓑_J 是坏时间上 [Kχ(p_h)−¾Dχ]_+ 的积分；带权带符号版本也保留。STRICT LIMITS：这是下界，不是上界；不证明该序列或奇点存在，也不证明它们不可能；没有总变差控制时不可免费删除趋近 1 的时间权重；固定环带常数不称为缩球一致。FINITE COMPUTATION：无。OPEN：𝓑_J 的真实 NS 上界、缩球、移动路径、G/G-P/G-C、R.216–R.217、首次奇点排除与一般正则性。文献核查有界，访问限制与 OCR 风险如上；没有新颖性、优先权、发表等级或 Clay 声明，无图件、仿真、数值证书或累计 recap。NOT CLAY。<a href="/notes/clay-b-bad-time-net-work-20260906.html">阅读完整 CB.10 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-pressure-work-window-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = template.replace(
        ".hero { display:grid; grid-template-columns:minmax(0,1fr) 300px; gap:2rem; padding:58px 0 34px; border-bottom:1px solid var(--line); }",
        ".hero { padding:58px 0 34px; border-bottom:1px solid var(--line); }",
        1,
    )
    template = template.replace(
        ".deck { max-width:70ch; font-size:1.08rem; }",
        ".dek { max-width:72ch; font-size:1.08rem; } .meta { display:flex; flex-wrap:wrap; gap:.5rem; margin:1rem 0 0; font:700 11px/1.4 SFMono-Regular,Consolas,monospace; letter-spacing:.035em; } .meta span { padding:.28rem .55rem; border:1px solid var(--line); background:var(--panel); }",
        1,
    )
    template = template.replace(
        ".hero,.grid { grid-template-columns:1fr; }",
        ".grid { grid-template-columns:1fr; }",
        1,
    )
    template = re.sub(r'<title>.*?</title>', '<title>坏时间净压力工作：从频率支付到必要下界</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 频率支付、固定正则环带、好时间高高压力吸收和坏时间净工作必要下界的双语解析笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    if "h1 { max-width:22ch; overflow-wrap:anywhere;" not in template:
        template = template.replace("h1 { max-width:16ch;", "h1 { max-width:22ch; overflow-wrap:anywhere;", 1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.10 · {DISPLAY_ID}</strong></header>', template, count=1)
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
    value = value.replace("CB.1–CB.9", "CB.1–CB.10")
    value = value.replace("compact pressure work / uniform early window / mature-time boundary", "frequency payment / fixed annulus / bad-time necessary work", 1)
    old_focus = "Clay-B 已把真实正压力功保持到统一早时窗口：固定能量单泡取得固定比例的 L³ 三次方增长，而累计梯度平方趋于零。这只排除一条量词精确的候选预算；窗口仍早于成熟扩散时间，同一固定解、近源、外壳与合同 G 继续开放。"
    new_focus = "Clay-B 已在同一解的固定成熟窗口中支付低频参与压力和固定环带好时间高高压力；若合法的大局部 L³ 序列存在，坏时间正净工作必须达到终端局部能量量级。这是必要下界，不是上界；真正的 NS 上界、缩球路径和合同 G 继续开放。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    if 'class="tree-row clay-b-bad-time-net-work-row"' in value:
        if "Clay-B 独立路线停在 CB.10" not in value or "CB.11 · NEXT" not in value:
            raise RuntimeError("existing CB.10 route boundary drift")
        return value
    cb9_start = value.index('<div class="tree-row clay-b-pressure-work-window-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb9_start)
    cb9 = value[cb9_start:boundary_start]
    cb9 = cb9.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb9 = cb9.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb9, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">NEXT TEST COMPLETED</span><h3>成熟窗口坏时间机制已进入 CB.10</h3><p>AK–AQ 已区分已付低频/好时间压力与坏时间必要净工作；结果见下一个正式路线节点。</p></aside>', cb9, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.9 branch drift")
    value = value[:cb9_start] + cb9 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB10_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-bad-time-net-work-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 10
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.10"
    payload["nextIndependentChapter"] = "CB.11"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note",
            "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.10",
            "sourceCommit": "22c0064338dbad20a6cc37cf054c24850cd2dc2e", "baseCommit": "8843d99338d62cdbc3067eaaead81ad93d7326ba",
            "handoffCommit": "ca1bf2ecad5716ef9a4a653806e4a27fbfb2957f", "logicalPredecessor": "ClayB-PressureWorkWindow-20260906",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False, "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-bad-time-net-work-20260906-gate.test.mjs", "publicationTest": "tests/clay-b-bad-time-net-work-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-bad-time-net-work-20260906-translations.mjs", "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE", "simulationRequired": False, "recapRequired": False,
            "advancesCanonicalR0Series": False, "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "LOW_FREQUENCY_INVOLVING_PRESSURE_AND_FIXED_ANNULUS_GOOD_TIME_HIGH_HIGH_PRESSURE_PAID_BAD_TIME_POSITIVE_NET_WORK_HAS_CONDITIONAL_NECESSARY_LOWER_BOUND_NOT_UPPER_BOUND_NO_SEQUENCE_OR_SINGULARITY_EXISTENCE_TIME_WEIGHT_RETAINED_FIXED_ANNULUS_NOT_SHRINKING_UNIFORM_G_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.10", DISPLAY_ID, "坏时间净压力工作", "necessary lower bound", "liminf 𝓑_J/Hχ(t) ≥ 1", "NECESSARY CONDITION", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.10", "Clay-B 独立路线停在 CB.10", "CB.11 · NEXT", 'class="tree-row clay-b-bad-time-net-work-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb10 = home.index('class="tree-row clay-b-bad-time-net-work-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb10)
    if not (r0_start < r0_boundary < divider < clay_start < cb10 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-bad-time-net-work-boundary"' not in literature or "CB.10 · ClayB-BadTimeNetWork-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.10 · {DISPLAY_ID}" not in index or "10 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.10" or site.get("nextIndependentChapter") != "CB.11":
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
    subprocess.run([__import__("sys").executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)

validate()
print(json.dumps({"schemaVersion": "clay-b-bad-time-net-work-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.10", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
