#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB FixedHistoryScreen CB.16 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.60"
SLUG = "clay-b-fixed-history-screen-20260906"
DISPLAY_ID = "ClayB-FixedHistoryScreen-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_MAIN = '''  <main data-language="zh">
    <article>
      <header class="hero">
        <div class="kicker">CB.16 · 独立 Clay-B 方法笔记 · 2026-09-06</div>
        <h1>CB.16｜固定初值完整历史：增长窗口尾项与时间账本边界</h1>
        <p class="dek">同一固定初值的完整峰值历史确实多给出一条真实 NS 尾估计：固定初始热项消失，且增长窗口 S_k=M_k^(1+η) 之外的旧非线性项趋零。但固定窗口控制仍未支付；若局部古老极限是单位常向量，中间增长时间段反而必须保留有符号贡献。record 倍增账本只给间隔下界，不自动给上界。</p>
        <div class="meta"><span>PROVED IN STATED SCOPE</span><span>CONDITIONAL ANCIENT BRANCH</span><span>FINITE CHECKS ONLY</span><span>QUANTIFIER BOUNDARY</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / 结论地图</div><h2>完整历史支付增长窗口外的尾部，却没有关闭固定窗口</h2><div class="grid"><div class="card"><strong class="proved">BI / 已付</strong>热项趋零，且 ||N_old^S||∞≤CE₀(M_k/S+t_k/M_k)；取 S_k=M_k^(1+η) 后旧尾趋零。</div><div class="card"><strong class="open">BI / 条件必要来源</strong>若古老局部极限是单位常向量，则每个固定窗口的近期项趋零，中间增长窗口的有符号贡献必须保留该常量。</div><div class="card"><strong class="open">BJ / 时间账本</strong>局部 mild 寿命只给 D_j≥4c_*；有限总时间只给 Σ4^(-j)D_j&lt;∞，不产生有界 D_j 子列。</div></div><p>本章既不构造奇点，也不把有符号项解释为正测度；一般古老解刚性、G/Q 与正则性仍开放。</p></section>
      <section><div class="section-no">02 / BI.1–BI.11</div><h2>固定初值、周期 Oseen 核与终点紧性接口都被完整保留</h2><p>对同一周期光滑初值，在 record 峰值 M_k 处作精确抛物缩放，完整过去长度为 b_k=M_k²t_k，周期尺度为 M_k。均值、远端初值、整胞能量与耗散缩放保持精确。周期化的 e^(tΔ)P div 核包含 Leray 投影、压力作用和所有周期副本；这里没有把裸投影误当成 L∞ 有界算子。</p><div class="equation">||K_L(t)||₁ ≤ C t^(-1/2),
||K_L(t)||∞ ≤ C(t^(-2)+L^(-4)).                  (BI.8–BI.9)</div><p>统一短时 mild bootstrap 与标准局部平滑、紧性接口给出终点两侧的安全紧柱；后者作为外部 PDE 输入明确标注，并未被有限代数检查替代。</p></section>
      <section><div class="section-no">03 / BI.12–BI.16</div><h2>固定窗口的完整 mild 分解保留了旧历史的真实符号</h2><p>终点速度精确分解为初始热项、固定窗口前的旧非线性项和固定窗口内的近期项：</p><div class="equation">v_k(0)=H_k+N_old^S+N_recent^S,
||H_k||∞ → 0.                                    (BI.12–BI.14)</div><p>若另行假设 v_k 局部趋于单位常向量 c，则核的零积分、空间远尾与短时间可积性给 N_recent^S→0，对每个固定 S 因而有 N_old^S→c。这里先固定 S 再取 k→∞，不能未经证明把 S 换成随 k 增长的窗口。</p></section>
      <section><div class="section-no">04 / BI.17–BI.20</div><h2>能量只在增长窗口之外让旧尾消失</h2><p>同一原解的全局能量给出</p><div class="equation">||N_old^S||∞ ≤ C E₀(M_k/S+t_k/M_k),
S_k=M_k^(1+η),  0&lt;η&lt;1,
||N_old^(S_k)||∞ → 0.                            (BI.17–BI.18)</div><p>S_k 在归一化时间中趋于无穷，而对应原时间长度趋零。若同时处在单位常向量条件分支，则 [-S_k,-S] 的中间有符号贡献局部趋于 c。它不是正源测度或已构造的奇点来源；固定 S 后的统一尾小性仍未得到。</p></section>
      <section><div class="section-no">05 / BJ.1–BJ.26</div><h2>record 倍增的局部寿命给下界，额外上界才排常量</h2><p>令 M_j=2^jM₀、t_j 为首次达到时刻，并设 D_j=M_j²(t_j−t_(j−1))。严格局部 mild bootstrap 得到 D_j≥4c_*；有限首次候选末端只给指数加权可和性：</p><div class="equation">Σ_(j≥1) 4^(-j) D_j &lt; ∞,
A_j=Σ_(m≥1)4^(-m)D_(j+m),
D_j=4A_(j−1)−A_j.                               (BJ.12–BJ.15)</div><p>只有另有 D_j 有界子列时，极限在某个过去时刻保留速度上界 1/2，而终点模长为 1，从而排除时空常向量。这个上界不是基本能量或有限总时间的自动结果。</p></section>
      <section><div class="section-no">06 / BJ.27–BJ.32</div><h2>标量反检查只否定时间账本推论，Type I 仍是额外输入</h2><p>显式标量族 D_j=d_*+j² 满足局部寿命型下界和 Σ4^(-j)D_j&lt;∞，却没有有界子列。这只是时间账本的反检查，不是 NS 解、压力模型、适当弱解或能量预算反例。</p><p>速度 Type I 条件确实给 D_j≤4K_I²，并进而排常量极限；但本章没有从任意初值推出 Type I。即使非恒定性成立，三维有界非恒定古老 mild 解的刚性仍然未付。</p></section>
      <section><div class="section-no">07 / 原始来源与量词边界</div><h2>不同缩放的初始胞 L³ 恒等式不能替代单个古老解的全空间时间序列</h2><p>本轮重读 KNSS 作者预印本 PDF 页 6–13、18–20，并视觉核验页 7、10、11、19；Albritton–Barker arXiv v2 全 15 页读取并视觉核验页 2–4。这里只把其 Theorem 1.2 用作未满足条件的对照。</p><p>每个 v_k 在各自逃逸左端时刻拥有周期胞 L³ 恒等式，不等于同一个全空间古老解在一列趋于负无穷的固定时刻具有统一全空间 L³ 界。不得交换缩放序列、域或时间量词。未完成穷尽新颖性检索、Deep Research 或外部同行评审。</p></section>
      <section><div class="section-no">08 / 证据、边界与下一步</div><h2>固定历史预检完成，下一研发动作是阶段策略复评</h2><table><thead><tr><th>类别</th><th>本章范围</th></tr></thead><tbody><tr><td>PROVED IN STATED SCOPE</td><td>完整周期 mild 历史、增长窗口旧尾估计和 record 时间账本结论。</td></tr><tr><td>CONDITIONAL</td><td>单位常向量极限要求中间增长窗口保留有符号贡献；有界 D_j 子列排常量。</td></tr><tr><td>FINITE CHECKS ONLY</td><td>四份文本源、52 个 BI/BJ 标签、89/89 文件绑定、23 项精确代数检查和 3 项有限负对照；不替代 PDE 证明。</td></tr><tr><td>OPEN</td><td>固定窗口控制、实际 NS 的 D_j 上界、Type I、非恒定古老解刚性、G/Q、一般正则性与 Clay。</td></tr></tbody></table><p class="note">科学源提交：67476e7a2e236af9c3ce50ca95f8925f032d5704；冻结提交：20a2abc781ad6784f552d2a80211298e5711c97f。七份本轮文件、八十二份依赖和一份冻结 manifest 由 SHA-256 绑定。内部模型复核不是外部同行评审。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_fixed_history_mild_preflight_20260906.md">BI 完整 mild 历史</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_record_time_history_preflight_20260906.md">BJ record 时间账本</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_fixed_history_primary_reading_20260906.md">原始来源记录</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_fixed_history_screen_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap；不分发第三方 PDF，也不改私有热演化论文。G OPEN / NOT CLAY。</strong></p></section>
    </article>
    <footer class="footer">CB.16 · Independent HTML research note · ClayB-FixedHistoryScreen-20260906 · 2026-09-06</footer>
  </main>'''


EN_MAIN = '''  <main data-language="en">
    <article>
      <header class="hero">
        <div class="kicker">CB.16 · Independent Clay-B methods note · 2026-09-06</div>
        <h1>CB.16 | Complete fixed-data history: growing-window tails and the time-ledger boundary</h1>
        <p class="dek">The complete peak history from one fixed initial datum does yield a genuine NS tail estimate: the fixed initial heat term vanishes, and the old nonlinear contribution outside S_k=M_k^(1+η) tends to zero. Fixed-window control is still unpaid. If the local ancient limit is a unit constant vector, the intermediate growing-time slab must instead retain a signed contribution. The record-doubling ledger supplies only a lower lag bound, not an automatic upper bound.</p>
        <div class="meta"><span>PROVED IN STATED SCOPE</span><span>CONDITIONAL ANCIENT BRANCH</span><span>FINITE CHECKS ONLY</span><span>QUANTIFIER BOUNDARY</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / Result map</div><h2>The complete history pays the tail outside a growing window, but does not close a fixed window</h2><div class="grid"><div class="card"><strong class="proved">BI / paid</strong>The heat term vanishes and ||N_old^S||∞≤CE₀(M_k/S+t_k/M_k); choosing S_k=M_k^(1+η) makes the old tail vanish.</div><div class="card"><strong class="open">BI / conditional necessary source</strong>If the ancient local limit is a unit constant, the recent term in every fixed window vanishes and the signed intermediate growing-window contribution must retain that constant.</div><div class="card"><strong class="open">BJ / time ledger</strong>Local mild lifetime gives only D_j≥4c_*; finite total time gives only Σ4^(-j)D_j&lt;∞ and no bounded D_j subsequence.</div></div><p>The chapter neither constructs a singularity nor turns the signed term into a positive measure. General ancient rigidity, G/Q, and regularity remain open.</p></section>
      <section><div class="section-no">02 / BI.1–BI.11</div><h2>Fixed-data provenance, the periodic Oseen kernel, and the terminal compactness interface are all retained</h2><p>At record peaks M_k of one smooth periodic initial datum, exact parabolic rescaling retains the complete past length b_k=M_k²t_k and period scale M_k, together with exact mean, remote initial data, cell energy, and dissipation scalings. The periodized e^(tΔ)P div kernel includes the Leray projection, pressure action, and every periodic image; the bare projection is not treated as L∞ bounded.</p><div class="equation">||K_L(t)||₁ ≤ C t^(-1/2),
||K_L(t)||∞ ≤ C(t^(-2)+L^(-4)).                  (BI.8–BI.9)</div><p>A uniform short-time mild bootstrap and standard local smoothing and compactness give a safe cylinder across the terminal time. The latter remain explicit external PDE inputs, not consequences of finite algebra checks.</p></section>
      <section><div class="section-no">03 / BI.12–BI.16</div><h2>The fixed-window complete mild decomposition retains the true sign of old history</h2><p>The terminal velocity splits exactly into the initial heat term, the old nonlinear contribution before a fixed window, and the recent contribution inside it:</p><div class="equation">v_k(0)=H_k+N_old^S+N_recent^S,
||H_k||∞ → 0.                                    (BI.12–BI.14)</div><p>If one additionally assumes that v_k converges locally to a unit constant c, kernel cancellation, spatial-tail control, and short-time integrability yield N_recent^S→0 and hence N_old^S→c for every fixed S. The order fixes S before k→∞; replacing S by a k-dependent window is not licensed.</p></section>
      <section><div class="section-no">04 / BI.17–BI.20</div><h2>Energy removes the old tail only beyond a growing window</h2><p>The global energy of the same original solution gives</p><div class="equation">||N_old^S||∞ ≤ C E₀(M_k/S+t_k/M_k),
S_k=M_k^(1+η),  0&lt;η&lt;1,
||N_old^(S_k)||∞ → 0.                            (BI.17–BI.18)</div><p>S_k diverges in normalized time while its original-time duration vanishes. Under the unit-constant branch, the signed contribution on [-S_k,-S] must then converge locally to c. It is neither a positive source measure nor a constructed singularity mechanism, and uniform control beyond fixed S remains unavailable.</p></section>
      <section><div class="section-no">05 / BJ.1–BJ.26</div><h2>Local lifetime bounds record doubling from below; an additional upper bound is what excludes constants</h2><p>Let M_j=2^jM₀, let t_j be the first hitting time, and set D_j=M_j²(t_j−t_(j−1)). A strict local mild bootstrap yields D_j≥4c_*, while a finite candidate terminal time yields only exponentially weighted summability:</p><div class="equation">Σ_(j≥1) 4^(-j) D_j &lt; ∞,
A_j=Σ_(m≥1)4^(-m)D_(j+m),
D_j=4A_(j−1)−A_j.                               (BJ.12–BJ.15)</div><p>Only if a bounded D_j subsequence is supplied separately does the limit retain speed at most 1/2 at a past time while having unit terminal magnitude, thereby excluding a spacetime constant. Basic energy and finite total time do not supply that upper bound.</p></section>
      <section><div class="section-no">06 / BJ.27–BJ.32</div><h2>The scalar countercheck targets only the time-ledger inference; Type I remains extra input</h2><p>The explicit scalar family D_j=d_*+j² satisfies the local-lifetime lower bound and Σ4^(-j)D_j&lt;∞ but has no bounded subsequence. It is only a countercheck of the time ledger, not an NS solution, pressure model, suitable solution, or energy-budget counterexample.</p><p>A velocity Type I condition does give D_j≤4K_I² and hence excludes a constant limit, but it is not derived here from arbitrary initial data. Even after nonconstancy, rigidity of bounded nonconstant three-dimensional ancient mild solutions remains unpaid.</p></section>
      <section><div class="section-no">07 / Primary sources and quantifier boundary</div><h2>Initial cell L³ identities for different rescalings do not become a whole-space time sequence for one ancient solution</h2><p>This round rereads KNSS author-preprint PDF pages 6–13 and 18–20, with visual checks of pages 7, 10, 11, and 19. Albritton–Barker arXiv v2 is read in all 15 pages, with pages 2–4 visually checked. Only its Theorem 1.2 is used as an unmet-input comparison.</p><p>Each v_k has a periodic-cell L³ identity at its own escaping left endpoint. This is not a uniform whole-space L³ bound for one ancient solution at a sequence of fixed times tending to minus infinity. Rescaling index, domain, and time quantifiers may not be exchanged. No exhaustive novelty search, Deep Research, or external peer review is claimed.</p></section>
      <section><div class="section-no">08 / Evidence, boundary, and next step</div><h2>The fixed-history precheck is complete; the next research action is a stage strategy reassessment</h2><table><thead><tr><th>Class</th><th>Scope here</th></tr></thead><tbody><tr><td>PROVED IN STATED SCOPE</td><td>The complete periodic mild history, growing-window old-tail estimate, and record-time ledger conclusions.</td></tr><tr><td>CONDITIONAL</td><td>A unit constant limit requires a signed intermediate growing-window contribution; a bounded D_j subsequence excludes constants.</td></tr><tr><td>FINITE CHECKS ONLY</td><td>Four text sources, 52 BI/BJ labels, 89/89 file bindings, 23 exact algebra checks, and three limited negative controls; none replaces PDE proof.</td></tr><tr><td>OPEN</td><td>Fixed-window control, an actual NS upper bound for D_j, Type I, nonconstant ancient rigidity, G/Q, general regularity, and Clay.</td></tr></tbody></table><p class="note">Scientific source commit: 67476e7a2e236af9c3ce50ca95f8925f032d5704; freeze commit: 20a2abc781ad6784f552d2a80211298e5711c97f. Seven current files, eighty-two dependencies, and one frozen manifest are SHA-256-bound. Internal model review is not external peer review.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_fixed_history_mild_preflight_20260906.md">BI complete mild history</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_record_time_history_preflight_20260906.md">BJ record-time ledger</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_fixed_history_primary_reading_20260906.md">primary-source record</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_fixed_history_screen_frozen_ledger_20260906.json">portable ledger</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap; it redistributes no third-party PDF and does not modify the private heat-evolution paper. G OPEN / NOT CLAY.</strong></p></section>
    </article>
    <footer class="footer">CB.16 · Independent HTML research note · ClayB-FixedHistoryScreen-20260906 · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-fixed-history-screen" aria-labelledby="clay-b-fixed-history-screen-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.16 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · FIXED HISTORY SCREEN</p><h2 class="route-map-title" id="clay-b-fixed-history-screen-title">CB.16｜固定初值完整历史：增长窗口尾项与时间账本边界</h2><p class="route-map-intro">同一固定初值的完整 mild 历史给出增长窗口 S_k=M_k^(1+η) 之外的真实旧尾小性；固定窗口控制仍未支付。在单位常向量条件分支中，中间增长时间段必须保留有符号贡献。record 时间账本只给倍增间隔下界，不自动给上界。G OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 固定初值完整历史笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-fixed-history-screen-20260906.html">阅读最新 CB.16 固定历史笔记 →</a><a href="/literature-review.html#clay-b-fixed-history-screen-boundary">查看原始来源与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 固定历史筛查结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>增长窗口外尾估计成立</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>固定窗口与自动倍增上界未得</span><span><i class="route-legend-mark current" aria-hidden="true"></i>Type I、古老解刚性、G/Q OPEN · NOT CLAY</span></div></div></section>'''


CB16_ROW = '''          <div class="tree-row clay-b-fixed-history-screen-row">
            <article class="tree-node current">
              <div class="tree-node-head"><span class="route-range">CB.16 · 2026-09-06 · BI/BJ FIXED HISTORY SCREEN</span><span class="tree-state current">当前路线边界</span></div>
              <h3>CB.16｜固定初值完整历史：增长窗口尾项与时间账本边界</h3>
              <p>BI 保留同一固定初值的完整周期 mild 历史，证明初始热项趋零，并用原解能量支付 ||N_old^S||∞≤CE₀(M_k/S+t_k/M_k)；因此 S_k=M_k^(1+η) 之外的旧尾趋零。</p>
              <p>这不是固定窗口控制。若古老局部极限是单位常向量，中间增长窗口必须保留有符号贡献；BJ 则证明 record 局部寿命只给 D_j 下界，有限总时间不自动给上界。有界子列或 Type I 都是额外输入。</p>
              <p class="tree-path">CB.15 粗预算反检查 → BI 完整 mild 历史 → 增长窗口外旧尾小性 → 固定窗口量词不可交换 → BJ 倍增时间下界 / 上界缺口 → 阶段策略复评</p>
              <p><a href="/notes/clay-b-ancient-constant-screen-20260906.html">CB.15：常向量极限反检查</a> · <a href="/notes/clay-b-fixed-history-screen-20260906.html">CB.16：固定初值完整历史</a></p>
            </article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发动作：阶段策略复评</h3><p>汇总浓集、局部平滑、压力功与古老解障碍，只选择真正减少未证输入且有明确全局出口的问题；不重复固定历史预检，也不把 Type I 或量词交换改名为已付条件。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.17 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.16</h3><p>CB.17 只是下一章占位，不是已完成研究。阶段策略复评尚未冻结；固定窗口控制、实际 NS 的 D_j 上界、Type I、非恒定古老解刚性、G/Q、带符号压力功上界、一般正则性与 Clay 均未关闭。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-fixed-history-screen-boundary">CB.16 · Clay-B 固定初值完整历史的文献和主张边界</h3><p>本轮重读 <a href="https://arxiv.org/abs/0709.3599">Koch–Nadirashvili–Seregin–Šverák 作者预印本</a> PDF 页 6–13、18–20，并视觉检查页 7、10、11、19，用于核对 Stokes 散度源核、mild 表示、局部平滑与峰值紧性接口；另完整读取 <a href="https://arxiv.org/abs/1811.00502v2">Albritton–Barker arXiv:1811.00502v2</a> 15 页并视觉检查页 2–4。后者 Theorem 1.2 只作未满足输入的对照：同一个全空间 mild 古老解须在一列趋于负无穷的时刻具有统一全空间 L³ 界。不同缩放在各自逃逸左端时刻的周期胞恒等式不满足该量词与域条件。标准外部 PDE 接口没有在此全部重证，也没有穷尽文献、Deep Research、新颖性或外部同行评审声明。</p><div class="boundary"><strong>CB.16 · ClayB-FixedHistoryScreen-20260906 公开边界</strong><p>PROVED IN STATED SCOPE：完整周期 mild 历史的初始热项趋零，并有 ||N_old^S||∞≤CE₀(M_k/S+t_k/M_k)；取 S_k=M_k^(1+η)、0&lt;η&lt;1，增长窗口外旧尾趋零。CONDITIONAL：若局部古老极限为单位常向量，固定窗口内近期项趋零，中间增长窗口必须保留该常向量的有符号贡献；若另有有界 D_j 子列则极限非恒定。TIME-LEDGER BOUNDARY：局部寿命给 D_j≥4c_*，有限总时间只给 Σ4^(-j)D_j&lt;∞；标量 d_*+j² 只反检查该推论，不是 NS。Type I 与古老解刚性仍是额外输入。FINITE CHECKS ONLY：四份文本源、52 个 BI/BJ 标签、89/89 文件绑定、23 项精确代数检查和 3 项有限负对照不替代 PDE 证明。OPEN：固定窗口控制、实际 NS 上界、G/Q、一般正则性与 Clay。无图件、仿真、新 PDF 或累计 recap。NOT CLAY。<a href="/notes/clay-b-fixed-history-screen-20260906.html">阅读完整 CB.16 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-ancient-constant-screen-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>固定初值完整历史：增长窗口尾项与时间账本边界</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 固定初值完整 mild 历史、增长窗口尾估计、record 倍增时间账本与量词边界的双语方法笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.16 · {DISPLAY_ID}</strong></header>', template, count=1)
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
    value = value.replace("CB.1–CB.15", "CB.1–CB.16")
    value = value.replace("genuine NS finite-segment / constant-limit obstruction", "fixed-data history / growing-window tail screen", 1)
    old_focus = "Clay-B 已完成常向量古老极限的一轮真实 NS 反检查：光滑有限段在粗能量预算下仍可趋于非零常向量，因此自动排常量的方法停止；同一固定初值、完整历史比例、精确 record、mild 时间排序与合同 G 继续开放。"
    new_focus = "Clay-B 已完成固定初值完整历史预检：原解能量支付增长窗口之外的旧非线性尾，但没有固定窗口控制；record 倍增账本只给下界而不自动给上界。下一研发动作转为阶段策略复评，G/Q 与一般正则性继续开放。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    if 'class="tree-row clay-b-fixed-history-screen-row"' in value:
        if "Clay-B 独立路线停在 CB.16" not in value or "CB.17 · NEXT" not in value:
            raise RuntimeError("existing CB.16 route boundary drift")
        return value
    cb15_start = value.index('<div class="tree-row clay-b-ancient-constant-screen-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb15_start)
    cb15 = value[cb15_start:boundary_start]
    cb15 = cb15.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb15 = cb15.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb15, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">FIXED HISTORY SCREEN COMPLETED</span><h3>完整历史与 record 时间账本已进入 CB.16</h3><p>BI/BJ 已核对增长窗口旧尾、固定窗口量词及倍增间隔上下界边界；结果见下一个正式路线节点。</p></aside>', cb15, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.15 branch drift")
    value = value[:cb15_start] + cb15 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB16_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-fixed-history-screen-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 16
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.16"
    payload["nextIndependentChapter"] = "CB.17"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note",
            "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.16",
            "sourceCommit": "67476e7a2e236af9c3ce50ca95f8925f032d5704", "baseCommit": "56027d0cf173535de10a67865e91fa019fbef332",
            "handoffCommit": "20a2abc781ad6784f552d2a80211298e5711c97f", "logicalPredecessor": "ClayB-AncientConstantScreen-20260906",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False, "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-fixed-history-screen-20260906-gate.test.mjs", "publicationTest": "tests/clay-b-fixed-history-screen-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-fixed-history-screen-20260906-translations.mjs", "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE", "simulationRequired": False, "recapRequired": False,
            "advancesCanonicalR0Series": False, "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "COMPLETE_FIXED_DATA_MILD_HISTORY_GIVES_GROWING_WINDOW_OLD_TAIL_SMALLNESS_NOT_FIXED_WINDOW_CONTROL_CONSTANT_ANCIENT_BRANCH_AND_BOUNDED_DOUBLING_LAG_ARE_CONDITIONAL_TIME_LEDGER_SCALAR_FAMILY_IS_NOT_NS_TYPE_I_AND_ANCIENT_RIGIDITY_UNPAID_G_Q_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.16", DISPLAY_ID, "固定初值完整历史：增长窗口尾项与时间账本边界", "Complete fixed-data history: growing-window tails and the time-ledger boundary", "PROVED IN STATED SCOPE", "CONDITIONAL ANCIENT BRANCH", "FINITE CHECKS ONLY", "QUANTIFIER BOUNDARY", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.16", "Clay-B 独立路线停在 CB.16", "CB.17 · NEXT", 'class="tree-row clay-b-fixed-history-screen-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb16 = home.index('class="tree-row clay-b-fixed-history-screen-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb16)
    if not (r0_start < r0_boundary < divider < clay_start < cb16 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-fixed-history-screen-boundary"' not in literature or "CB.16 · ClayB-FixedHistoryScreen-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.16 · {DISPLAY_ID}" not in index or "16 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.16" or site.get("nextIndependentChapter") != "CB.17":
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
print(json.dumps({"schemaVersion": "clay-b-fixed-history-screen-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.16", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
