#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB RecentSourceScreen CB.13 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.57"
SLUG = "clay-b-recent-source-screen-20260906"
DISPLAY_ID = "ClayB-RecentSourceScreen-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_MAIN = '''  <main data-language="zh">
    <article>
      <header class="hero">
        <div class="kicker">CB.13 · 独立 Clay-B 方法笔记 · 2026-09-06</div>
        <h1>CB.13｜近期源的能量与频率成本</h1>
        <p class="dek">旧热背景移走后，近期真实非线性源的积分 H¹ 能量确实在窗口上趋零；但原压力测试需要更强的时间集中控制。逐频带热平均留下正频率矩，静态背景又能复制旧压力支付的指数。因此这轮关闭的是一条具体绝对值/Young 方法路线，不是源自压力问题本身。</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>FINITE CHECKS ONLY</span><span>METHOD SCREEN</span><span>CONDITIONAL COMPARISON</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / 结论地图</div><h2>能量小量成立，但压力功所需的平方时间集中仍未关闭</h2><div class="grid"><div class="card"><strong class="proved">BC / 能量基线</strong>实际 R 在 J 上的积分 H¹ 能量趋零，并给出一条能与 BB 必要下界冲突的充分验收量。</div><div class="card"><strong class="open">BD / 频率成本</strong>普通热核与 Young 卷积在所需时间范数中留下 N¹ᐟ² 或 N⁹ᐟ⁸ 的正频率权重。</div><div class="card"><strong class="open">BE / 来源比较</strong>静态有界背景可复制旧压力支付指数，但不等同近期热余量，也不给剩余压力上界。</div></div><p>本章没有证明合法大范数序列存在，也没有构造或排除奇点；所有下界继续是条件必要性陈述。</p></section>
      <section><div class="section-no">02 / 固定对象</div><h2>同一解、同一坏集和同一剩余耗散全部保留</h2><p>始终沿用 AQ/BB 的同一周期 NS 解、固定环带、原 s_J、坏集 B_K、权重 μ_J 与 [s_J,t]。取 K=Λ^(3/4)、τ=Λ^(−8/3)、a=t−δ−τ，并写 h=P_&gt;K u=b+R。R 保留完整速度张量、Leray 投影、散度和真实时间顺序，不是独立无强迫 NS 解。</p><div class="equation">liminf H_t⁻¹∫ μ_J[Kχ(p(R))−5Dχ/8] ds ≥ 1.</div><p>这仍是条件必要下界，不是 p(R) 的上界；旧压力已用掉的 1/8 耗散份额不会再次使用。</p></section>
      <section><div class="section-no">03 / BC.1–BC.18</div><h2>R 的窗口 H¹ 能量趋零，但这不是逐时小量</h2><p>从精确恒等式 R=h−b 与真实热滞后得到</p><div class="equation">∫_J ||∇R||₂² ds ≤ C(A_J+M²δ/τ) = o(1).             (BC.5)</div><p>若源估计使用整个 [a,t]，只能另记 Ã_J=∫_[a,t]g²→0；一般没有 Ã_J≤CA_J 或多项式速率。不能把二者偷换，也不能从 L¹ 时间小量直接推出平方时间小量。</p></section>
      <section><div class="section-no">04 / BC 的充分成功判据</div><h2>真正能产生矛盾的 Q_J 仍是开放输入</h2><p>有限 L³ 双 Riesz 与原 χ|u|u 测试给出一条充分路线：</p><div class="equation">Q_J := H_t⁻¹∫_[s_J,t] μ_J L₃ ||∇R||₂⁴ ds → 0.       (BC.11)</div><p>若 Q_J 成立，可用小于 5/8 的额外耗散得到与条件必要下界冲突的上界。但现有能量没有证明它；直接代入 R=h−b 只能支付纯热部分，并留下 H_t⁻¹∫μ_JL₃g⁴。这是该绝对值方法的充分目标，不是所有带符号方法的必要条件。</p></section>
      <section><div class="section-no">05 / BD.1–BD.22</div><h2>逐块热平均提高时间可积性，却留下未付的正频率矩</h2><p>BD 在每个 N≳K 的非零平滑环带保留完整 F=u⊗u，并在 c_*N⁻² 分开近对角源与旧源。精确核成本为 N^(5/2)e^(−cN²ρ):L^(3/2)→L² 和 N²e^(−cN²ρ):L²→L²。普通 Young 卷积给</p><div class="equation">||∇R_N||_(L²_tL²_x) ≤ C N¹ᐟ² ||F_N||,
||∇R_N||_(L^(16/3)_tL²_x) ≤ C N⁹ᐟ⁸ ||F_N||.       (BD.15, BD.18)</div><p>能量只给无权逐块上界，不支付相应的 N^(9/4) 平方和；最低相关环带仍留下 Λ^(3/8) 乘无已知速率的小量。因此这条逐块绝对值/时间核路线在此停止。</p></section>
      <section><div class="section-no">06 / BD 的反推边界</div><h2>标量时间集中例只否定一个测度论推断</h2><p>BD.21–BD.22 构造非负标量时间函数，使 ∫q→0 而 H⁻¹∫Lq²=1。它只说明时间 L¹ 小量不能自动给归一化平方小量；该对象不是无散速度、NS 轨道或压力功反例。</p><p>Fourier 相位、压力符号、无散收缩以及剩余 5/8 耗散能否联合抵消仍未判定，所以本章不是所有带符号动力学方法的 no-go 定理。</p></section>
      <section><div class="section-no">07 / BE.1–BE.17</div><h2>静态背景复制旧压力支付，却没有控制剩余压力</h2><p>BE 取 n=S_Nh、N≥2K，由符号支持精确得到 h−n=P_&gt;N u。一般有界背景估计用一次 εDχ 支付含 n 的压力；取 N=Λ^(4/3)，得到静态高输入压力的条件必要下界。令 τ=N⁻² 时，余项指数与 BB 的旧热背景相同。</p><div class="equation">p(h)=p(P_&gt;N u)+p_bg,
liminf H_t⁻¹∫ μ_J[Kχ(p(P_&gt;N u))−(3/4−ε)Dχ] ds ≥ 1.   (BE.16)</div><p>这只是方法来源比较：R 不等于 P_&gt;N u，p(P_&gt;N u) 不等于 P_&gt;N p，二者的带符号压力功也未比较。静态复制不否定热历史定位，更不提供上界。</p></section>
      <section><div class="section-no">08 / 文献、证据与下一问题</div><h2>下一步转向单侧压力判据的原文机制，而不是继续调指数</h2><p>下一项只对照 Seregin–Šverák 单侧压力判据实际如何生成临界控制。其全空间条件 (C) 包含中心一致压力势控制与左连续性，不由当前周期能量推出，也不会被直接移植成周期定理。若原文机制只留下完整 (C) 或重复既有开放量，就按计划停止。</p><table><thead><tr><th>类别</th><th>本章范围</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>BC 的 R 能量基线与充分判据；BD 的逐块核成本；BE 的静态背景条件比较。</td></tr><tr><td>FINITE CHECKS ONLY</td><td>七份文本源、57 个公式编号、65/65 文件哈希、29 项有理算术与负向变异；不替代 PDE 证明。</td></tr><tr><td>LITERATURE INPUT</td><td>有限读取 Tao 的指定热核工具与 Seregin–Šverák 的设置、Definition 2.1、Theorem 2.2 及 §3 开头；不是全证明复审。</td></tr><tr><td>OPEN</td><td>Q_J、源自压力净功上界、真实 NS 输入、移动缩球 G、一般正则性与 Clay。</td></tr></tbody></table><p class="note">科学源提交：5314045dcedcc7e781d9fed0f167cae5c0451d62；冻结提交：9b556d81330a93f274372ed2e3be262e4be37d98。九份源、五十六份依赖与一份冻结 manifest 按 SHA-256 绑定。原 BC–BE 的 INTERNAL/PENDING 是推导时状态；当前 PASS 与冻结范围由审查、报告和 manifest 定义。内部模型复核不是外部同行评审或完整新颖性审查。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_recent_source_energy_benchmark_20260906.md">BC 能量基线</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_dyadic_recent_source_screen_20260906.md">BD dyadic 筛查</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_static_background_comparison_20260906.md">BE 静态比较</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_recent_source_screen_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap；第三方原论文 PDF 与私有热边缘论文均不在发布资产中。G OPEN / NOT CLAY。</strong></p></section>
    </article>
    <footer class="footer">CB.13 · Independent HTML research note · ClayB-RecentSourceScreen-20260906 · 2026-09-06</footer>
  </main>'''


EN_MAIN = '''  <main data-language="en">
    <article>
      <header class="hero">
        <div class="kicker">CB.13 · Independent Clay-B methods note · 2026-09-06</div>
        <h1>CB.13 | Energy and frequency costs of the recent source</h1>
        <p class="dek">After the old heat background is removed, the integral H¹ energy of the recent genuine nonlinear source does become small on the window, but the original pressure test requires stronger control of temporal concentration. Dyadic heat averaging leaves a positive frequency moment, while a static background can reproduce the old-pressure exponents. This closes one specific absolute-value/Young route, not the recent-source pressure problem itself.</p>
        <div class="meta"><span>PROVED LOCALLY</span><span>FINITE CHECKS ONLY</span><span>METHOD SCREEN</span><span>CONDITIONAL COMPARISON</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / Result map</div><h2>The energy smallness holds, but the squared temporal concentration needed by pressure work does not close</h2><div class="grid"><div class="card"><strong class="proved">BC / energy baseline</strong>The actual R has vanishing integral H¹ energy on J and yields a sufficient acceptance quantity that would contradict BB's necessary lower bound.</div><div class="card"><strong class="open">BD / frequency cost</strong>Ordinary heat kernels and Young convolution leave positive N¹ᐟ² or N⁹ᐟ⁸ frequency weights in the required time norms.</div><div class="card"><strong class="open">BE / source comparison</strong>A static bounded background reproduces the old-pressure exponents but is not the recent heat remainder and gives no upper bound for the remaining pressure.</div></div><p>This chapter proves neither existence of a legal large-norm sequence nor existence or exclusion of a singularity. Every lower bound remains a conditional necessity statement.</p></section>
      <section><div class="section-no">02 / Fixed objects</div><h2>The same solution, bad set, and remaining dissipation are all retained</h2><p>AQ/BB's same periodic NS solution, fixed annulus, original s_J, bad set B_K, weight μ_J, and [s_J,t] are retained throughout. Set K=Λ^(3/4), τ=Λ^(−8/3), a=t−δ−τ, and write h=P_&gt;K u=b+R. The term R retains the complete velocity tensor, Leray projection, divergence, and true time order; it is not an independent unforced NS solution.</p><div class="equation">liminf H_t⁻¹∫ μ_J[Kχ(p(R))−5Dχ/8] ds ≥ 1.</div><p>This is still a conditional necessary lower bound, not an upper bound for p(R). The 1/8 dissipation share spent on old pressure is not used again.</p></section>
      <section><div class="section-no">03 / BC.1–BC.18</div><h2>The window H¹ energy of R vanishes, but this is not pointwise smallness</h2><p>The exact identity R=h−b and the genuine heat lag give</p><div class="equation">∫_J ||∇R||₂² ds ≤ C(A_J+M²δ/τ) = o(1).             (BC.5)</div><p>If a source estimate uses the full [a,t], one must separately write Ã_J=∫_[a,t]g²→0. In general there is no Ã_J≤CA_J or polynomial rate. The two quantities cannot be exchanged, and temporal L¹ smallness does not directly imply squared temporal smallness.</p></section>
      <section><div class="section-no">04 / BC sufficient success criterion</div><h2>The Q_J that would create a contradiction remains an open input</h2><p>Finite-L³ double Riesz bounds and the original χ|u|u test give one sufficient route:</p><div class="equation">Q_J := H_t⁻¹∫_[s_J,t] μ_J L₃ ||∇R||₂⁴ ds → 0.       (BC.11)</div><p>If Q_J held, an additional dissipation share smaller than 5/8 would give an upper bound contradicting the conditional necessary lower bound. Present energy does not prove it. Directly substituting R=h−b pays the pure-heat part but leaves H_t⁻¹∫μ_JL₃g⁴. This is a sufficient target of the absolute-value method, not a necessity for every signed method.</p></section>
      <section><div class="section-no">05 / BD.1–BD.22</div><h2>Blockwise heat averaging improves time integrability but leaves an unpaid positive frequency moment</h2><p>For every nonzero smooth block N≳K, BD retains the complete F=u⊗u and splits near-diagonal from old sources at c_*N⁻². The exact kernel costs are N^(5/2)e^(−cN²ρ):L^(3/2)→L² and N²e^(−cN²ρ):L²→L². Ordinary Young convolution yields</p><div class="equation">||∇R_N||_(L²_tL²_x) ≤ C N¹ᐟ² ||F_N||,
||∇R_N||_(L^(16/3)_tL²_x) ≤ C N⁹ᐟ⁸ ||F_N||.       (BD.15, BD.18)</div><p>Energy supplies only unweighted blockwise bounds and does not pay the corresponding N^(9/4) square sum. Even the lowest relevant block leaves Λ^(3/8) times a small quantity with no known rate. This blockwise absolute-value/time-kernel route therefore stops here.</p></section>
      <section><div class="section-no">06 / Boundary of the BD countercheck</div><h2>The scalar time-concentration example rejects only one measure-theoretic inference</h2><p>BD.21–BD.22 construct nonnegative scalar time functions with ∫q→0 but H⁻¹∫Lq²=1. This shows only that temporal L¹ smallness does not automatically imply normalized squared smallness. The object is not a divergence-free velocity, NS trajectory, or pressure-work counterexample.</p><p>Whether Fourier phase, pressure sign, divergence-free contraction, and the remaining 5/8 dissipation can combine to improve the result remains undecided. The chapter is not a no-go theorem for every signed dynamical method.</p></section>
      <section><div class="section-no">07 / BE.1–BE.17</div><h2>A static background reproduces old-pressure payment but does not control the remaining pressure</h2><p>BE takes n=S_Nh with N≥2K. Symbol support gives exactly h−n=P_&gt;N u. A general bounded-background estimate pays pressure involving n with one εDχ share. Choosing N=Λ^(4/3) gives a conditional necessary lower bound for static high-input pressure. Setting τ=N⁻² reproduces the old-heat-background remainder exponents in BB.</p><div class="equation">p(h)=p(P_&gt;N u)+p_bg,
liminf H_t⁻¹∫ μ_J[Kχ(p(P_&gt;N u))−(3/4−ε)Dχ] ds ≥ 1.   (BE.16)</div><p>This is only a comparison of method sources: R is not P_&gt;N u, p(P_&gt;N u) is not P_&gt;N p, and their signed pressure works are not compared. Static reproduction neither invalidates the heat-history localization nor supplies an upper bound.</p></section>
      <section><div class="section-no">08 / Literature, evidence, and next question</div><h2>The next step examines the primary mechanism of a one-sided pressure criterion instead of tuning more exponents</h2><p>The next item only compares how the Seregin–Šverák one-sided pressure criterion actually generates critical control. Its whole-space condition (C) contains center-uniform pressure-potential control and left continuity; present periodic energy does not imply it, and it will not be imported directly as a periodic theorem. If the primary mechanism retains the full condition (C) or only repeats existing open quantities, the candidate check stops.</p><table><thead><tr><th>Class</th><th>Scope here</th></tr></thead><tbody><tr><td>PROVED LOCALLY</td><td>BC's energy baseline and sufficient criterion for R; BD's blockwise kernel costs; BE's conditional static-background comparison.</td></tr><tr><td>FINITE CHECKS ONLY</td><td>Seven text sources, 57 numbered formulas, 65/65 file hashes, 29 rational checks, and negative mutations; none replaces PDE proof.</td></tr><tr><td>LITERATURE INPUT</td><td>Limited reading of Tao's specified heat-kernel tools and the Seregin–Šverák setting, Definition 2.1, Theorem 2.2, and the opening of §3; not a full-proof review.</td></tr><tr><td>OPEN</td><td>Q_J, the signed recent-source pressure-work upper bound, actual NS inputs, moving shrinking G, general regularity, and Clay.</td></tr></tbody></table><p class="note">Scientific source commit: 5314045dcedcc7e781d9fed0f167cae5c0451d62; freeze commit: 9b556d81330a93f274372ed2e3be262e4be37d98. Nine source files, fifty-six dependencies, and one frozen manifest are SHA-256-bound. The INTERNAL/PENDING labels in the original BC–BE drafts are derivation-time states; the audit, report, and manifest define the present PASS and frozen scope. Internal model review is neither external peer review nor a complete novelty audit.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_recent_source_energy_benchmark_20260906.md">BC energy baseline</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_dyadic_recent_source_screen_20260906.md">BD dyadic screen</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_static_background_comparison_20260906.md">BE static comparison</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_recent_source_screen_frozen_ledger_20260906.json">portable ledger</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap. The third-party source PDF and private heat-edge paper are outside the publication assets. G OPEN / NOT CLAY.</strong></p></section>
    </article>
    <footer class="footer">CB.13 · Independent HTML research note · ClayB-RecentSourceScreen-20260906 · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-recent-source-screen" aria-labelledby="clay-b-recent-source-screen-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.13 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · RECENT SOURCE SCREEN</p><h2 class="route-map-title" id="clay-b-recent-source-screen-title">CB.13｜近期源的能量与频率成本</h2><p class="route-map-intro">近期源 R 的积分 H¹ 能量确实趋零，但原压力测试所需的 Q_J 平方时间集中仍未证。逐频带热核/Young 路线留下正频率矩；静态背景复制旧压力支付指数，却不等同热余量或给出上界。本轮停止这条具体 norm 路线，Q_J、带符号上界与 G 仍 OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 近期源筛查笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-recent-source-screen-20260906.html">阅读最新 CB.13 近期源筛查笔记 →</a><a href="/literature-review.html#clay-b-recent-source-screen-boundary">查看文献与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 近期源筛查结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>∫_J||∇R||₂²=o(1)</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>绝对值/Young 路线停止</span><span><i class="route-legend-mark current" aria-hidden="true"></i>Q_J、带符号上界与 G OPEN · NOT CLAY</span></div></div></section>'''


CB13_ROW = '''          <div class="tree-row clay-b-recent-source-screen-row">
            <article class="tree-node current">
              <div class="tree-node-head"><span class="route-range">CB.13 · 2026-09-06 · BC–BE RECENT SOURCE SCREEN</span><span class="tree-state current">当前路线边界</span></div>
              <h3>CB.13｜近期源的能量与频率成本</h3>
              <p>BC 证明实际 R 的窗口积分 H¹ 能量趋零，并把能与 BB 必要下界冲突的充分量定位为 Q_J；现有能量没有证明 Q_J，直接三角界反而留下带 L₃ 的四次耗散成本。</p>
              <p>BD 的完整逐块热核/Young 检查留下 N¹ᐟ² 或 N⁹ᐟ⁸ 正频率权重；BE 的静态有界背景可复制旧压力支付指数，却不等同热余量 R 与静态高通，也不提供源自压力上界。</p>
              <p class="tree-path">CB.12 旧压力已付 → BC 近期源能量基线与 Q_J → BD 逐块正频率矩未付 → BE 静态背景来源比较 → norm 路线停止 → 单侧压力原文机制对照 OPEN</p>
              <p><a href="/notes/clay-b-lagged-pressure-reduction-20260906.html">CB.12：滞后压力缩减</a> · <a href="/notes/clay-b-recent-source-screen-20260906.html">CB.13：近期源筛查</a></p>
            </article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发问题：单侧压力判据实际用了什么机制</h3><p>有限读取 Seregin–Šverák 原证明所需段落，区分条件 (C)、全空间压力规范与当前周期能量。若只重述附加假设或重复开放量，就停止该候选，不包装成新准则。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.14 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.13</h3><p>CB.14 只是下一章占位，不是已完成研究。Q_J、近期源带符号净压力功上界、条件 (C) 的周期兼容机制、实际 NS 生成 R.216–R.217、移动缩球 G/G-P/G-C 与首次奇点排除均未冻结。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-recent-source-screen-boundary">CB.13 · Clay-B 近期源筛查的文献和主张边界</h3><p>本章有限读取 <a href="https://arxiv.org/pdf/1908.04958">Tao arXiv:1908.04958v2</a> 的紧支撑乘子核论证与 (2.3)–(2.5)，只作热核和频率局部化背景；该文预先假定的统一临界范数控制没有导入当前周期能量框架。另读取 <a href="https://www.mis.mpg.de/de/publications/preprint-repository/article/2001/issue-92">Seregin–Šverák MiS Preprint 92/2001</a> 的摘要、引言、§2 设置、Definition 2.1、Theorem 2.2 与 §3 开头，并渲染核对 PDF 第 6–10 页。其全空间条件 (C)、Newton 势压力规范、中心一致上确界与左连续性没有从本站假设推出；§3 后续、§4 和主证明未完整读取，也不声称期刊版逐字相同或完成新颖性检索。</p><div class="boundary"><strong>CB.13 · ClayB-RecentSourceScreen-20260906 公开边界</strong><p>PROVED LOCALLY：BC 证明近期源 R 的窗口积分 H¹ 能量趋零，并定位足以与 BB 条件必要下界冲突的 Q_J；Q_J 仍未证。METHOD SCREEN：BD 保留完整源、Leray 投影、散度和时间顺序，证明普通逐块热核/Young 路线留下 N¹ᐟ² 或 N⁹ᐟ⁸ 正频率权重；其标量集中例不是 NS 反例，也不排除带符号方法。CONDITIONAL COMPARISON：BE 以静态有界背景复制旧压力支付指数，得到另一条件必要下界；R 不等同静态高通，p(P_&gt;N u) 不等同 P_&gt;N p，且没有上界。FINITE CHECKS ONLY：七份文本源、57 个公式编号、65/65 文件哈希、29 项有理算术与负向变异不替代证明。OPEN：Q_J、近期源净压力功上界、真实 NS 输入、移动缩球 G 与一般正则性。没有完整新颖性审查、外部同行评审或 Clay 声明，无图件、仿真或累计 recap。NOT CLAY。<a href="/notes/clay-b-recent-source-screen-20260906.html">阅读完整 CB.13 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-lagged-pressure-reduction-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>近期源的能量与频率成本</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 近期真实非线性源的能量基线、逐频带正频率成本与静态背景比较的双语方法笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.13 · {DISPLAY_ID}</strong></header>', template, count=1)
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
    value = value.replace("CB.1–CB.12", "CB.1–CB.13")
    value = value.replace("lagged heat / old-pressure payment / recent source", "recent-source energy / dyadic cost / static comparison", 1)
    old_focus = "Clay-B 已用窗口前真实热滞后支付所有含旧热分量的压力：成本是一份明确的 εDχ 加 o(H_t)，不是旧压力功自身 o(H_t)。必要净工作缩减到近期真实源自压力减剩余耗散；其上界、缩球路径和合同 G 继续开放。"
    new_focus = "Clay-B 已完成近期源的一轮有限方法筛查：R 的积分 H¹ 能量趋零，但原测试所需 Q_J 未证；逐块绝对值/Young 路线留下正频率矩，静态背景只复制旧压力支付指数。该 norm 路线停止，带符号上界、缩球路径和合同 G 继续开放。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    if 'class="tree-row clay-b-recent-source-screen-row"' in value:
        if "Clay-B 独立路线停在 CB.13" not in value or "CB.14 · NEXT" not in value:
            raise RuntimeError("existing CB.13 route boundary drift")
        return value
    cb12_start = value.index('<div class="tree-row clay-b-lagged-pressure-reduction-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb12_start)
    cb12 = value[cb12_start:boundary_start]
    cb12 = cb12.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb12 = cb12.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb12, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">NEXT TEST COMPLETED</span><h3>近期源方法筛查已进入 CB.13</h3><p>BC–BE 已区分积分能量小量、原测试所需平方时间集中、逐块正频率矩与静态背景来源比较；结果见下一个正式路线节点。</p></aside>', cb12, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.12 branch drift")
    value = value[:cb12_start] + cb12 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB13_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-recent-source-screen-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 13
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.13"
    payload["nextIndependentChapter"] = "CB.14"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note",
            "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.13",
            "sourceCommit": "5314045dcedcc7e781d9fed0f167cae5c0451d62", "baseCommit": "2b7cfe590decf90aea2326e9b76bc04bcf345e0b",
            "handoffCommit": "9b556d81330a93f274372ed2e3be262e4be37d98", "logicalPredecessor": "ClayB-LaggedPressureReduction-20260906",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False, "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-recent-source-screen-20260906-gate.test.mjs", "publicationTest": "tests/clay-b-recent-source-screen-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-recent-source-screen-20260906-translations.mjs", "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE", "simulationRequired": False, "recapRequired": False,
            "advancesCanonicalR0Series": False, "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "RECENT_SOURCE_INTEGRAL_H1_ENERGY_IS_SMALL_BUT_QJ_UNPROVED_BLOCKWISE_NORM_YOUNG_ROUTE_LEAVES_POSITIVE_FREQUENCY_MOMENT_STATIC_BACKGROUND_REPRODUCES_OLD_PAYMENT_WITHOUT_IDENTIFYING_REMAINDERS_OR_GIVING_UPPER_BOUND_G_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.13", DISPLAY_ID, "近期源的能量与频率成本", "Energy and frequency costs of the recent source", "PROVED", "FINITE", "METHOD SCREEN", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.13", "Clay-B 独立路线停在 CB.13", "CB.14 · NEXT", 'class="tree-row clay-b-recent-source-screen-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb13 = home.index('class="tree-row clay-b-recent-source-screen-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb13)
    if not (r0_start < r0_boundary < divider < clay_start < cb13 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-recent-source-screen-boundary"' not in literature or "CB.13 · ClayB-RecentSourceScreen-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.13 · {DISPLAY_ID}" not in index or "13 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.13" or site.get("nextIndependentChapter") != "CB.14":
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
print(json.dumps({"schemaVersion": "clay-b-recent-source-screen-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.13", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
