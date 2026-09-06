#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB AncientConstantScreen CB.15 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.59"
SLUG = "clay-b-ancient-constant-screen-20260906"
DISPLAY_ID = "ClayB-AncientConstantScreen-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_MAIN = '''  <main data-language="zh">
    <article>
      <header class="hero">
        <div class="kicker">CB.15 · 独立 Clay-B 方法笔记 · 2026-09-06</div>
        <h1>CB.15｜常向量古老极限：真实 NS 有限段的粗预算反检查</h1>
        <p class="dek">扩张周期域上的真实、无外力、单位黏性光滑 NS 有限段，可以同时具有零均值、过去速度 1+o(1)、终点单位峰值、整胞能量 O(周期尺度) 与归一化耗散趋零，却局部收敛到非零常向量。这排除的是从这些粗预算自动排除常量极限的方法，不是固定初值首次爆破序列，也不是 Navier–Stokes 反例。</p>
        <div class="meta"><span>PROVED METHOD OBSTRUCTION</span><span>GENUINE NS SEGMENTS</span><span>FINITE CHECKS ONLY</span><span>FIXED-HISTORY NOT REPRODUCED</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / 结论地图</div><h2>真实 NS 演化仍不足以让粗能量预算自动排除常量极限</h2><div class="grid"><div class="card"><strong class="proved">BH / 真实 NS 有限段</strong>每一项都是扩张环面上的光滑、无外力、单位黏性 NS 解，满足零均值压力规范与局部能量等式。</div><div class="card"><strong class="open">BH / 方法阻碍</strong>终点归一化、过去统一速度、整胞能量与小归一化耗散仍允许局部极限为单位常向量。</div><div class="card"><strong class="open">边界 / 固定历史未复制</strong>同一固定初值、首次候选奇点、精确 running record、完整历史比例与遥远初值趋零均未复制。</div></div><p>因此本章没有构造奇点、排除奇点、扩大正则解类或减少 G/Q 的假设。</p></section>
      <section><div class="section-no">02 / BH.1–BH.8</div><h2>紧支撑无散种子给出与大环面和小黏性一致的短时控制</h2><p>从一个核心等于非零常向量的紧支撑 curl 种子 V 出发，在周期尺度 n²、黏性 1/n 的环面上求解 U_n。未归一化非齐次 H^m 估计在所有大环面上一致：</p><div class="equation">½ d||U_n||_(H^m)²/dτ + n⁻¹||∇U_n||_(H^m)²
≤ C ||U_n||_(H^m)³.                               (BH.5)</div><p>标准周期局部存在与延拓接口因此给出共同寿命和统一 H^m 界，并在 τ≤n^(-1/2) 上得到 ||U_n(τ)−V||_∞=O(n^(-1/2))。这里明确调用标准局部理论，不宣称重新证明其全部依赖。</p></section>
      <section><div class="section-no">03 / BH.9–BH.12</div><h2>第一次精确缩放把小黏性解变成单位黏性的真实 NS 历史</h2><p>令 v_n(y,s)=U_n(y/n,(s+√n)/n)。时间、输运、压力梯度与黏性项精确匹配，v_n 在周期尺度 L_n=n³、历史区间 [−√n,0] 上满足单位黏性无外力 NS。</p><div class="equation">sup_s ∫|v_n|² ≤ n³||V||₂² = O(L_n),
∫∫|∇v_n|² ≤ C n^(3/2) = o(L_n).                   (BH.11–12)</div><p>小归一化耗散使用 BH.6 的逐时统一梯度界；若只使用小黏性能量等式，只能得到 O(L_n)，不能把两种证据混为一谈。</p></section>
      <section><div class="section-no">04 / BH.13–BH.15</div><h2>终点峰值再归一化后，真实 NS 有限段趋向单位常向量</h2><p>以终点最大值 q_n 和最大点 y_n 作第二次精确抛物缩放，得到 w_n。其周期尺度与历史长度分别为 ℓ_n=q_n n³、b_n=q_n²√n，且</p><div class="equation">|w_n(0,0)|=1,
sup_(-b_n≤s≤0)||w_n(s)||_∞≤1+O(n^(-1/2)),
w_n → c,  |c|=1,  locally uniformly.              (BH.14–15)</div><p>每个 w_n 都是真实光滑 NS 解、严格零均值并保留规范周期压力。非零常向量 c 本身也是合法的古老 mild NS 解，所以得到 c 不产生矛盾。</p></section>
      <section><div class="section-no">05 / BH.16–BH.18</div><h2>反检查没有复制同一固定初值的完整峰值历史</h2><p>若真正从周期尺度 1 的同一固定初值在首次候选奇点前作峰值缩放，则完整历史保留</p><div class="equation">b_k/ℓ_k² → T_* &gt; 0,
||v_k(-b_k)||_∞ → 0.                              (BH.17)</div><p>本章序列却满足 b_n/ℓ_n²=n^(-11/2)→0，左端速度趋于 1，并且没有让每一项成为精确的 running record。因此它只否定 BH.1 粗预算的自动排常量推断，不能否定利用固定初值来源、完整历史比例、遥远初值或精确时间排序的更窄方案。</p></section>
      <section><div class="section-no">06 / 两条动力学路线复查</div><h2>应变几何与古老解刚性都仍缺少真正的闭合输入</h2><p>中间应变特征值路线仍需临界时空积分界，移动中心局部化还产生未支付的 cutoff 输运项；运动学恒等式本身不是新的时间控制。古老解路线则必须区分“一般有界古老 mild 解是否只能是常量”和“固定初值峰值历史能否排除非零常量”两层问题。</p><p>本章的常向量极限不是一般常量分类命题的反例。两条策略都没有减少 G/Q、带符号压力功或正则性假设，也没有扩大任何已知正则解类。</p></section>
      <section><div class="section-no">07 / 原始来源阅读</div><h2>所读原文支持边界定位，不构成穷尽文献或新颖性审计</h2><p>本轮实际读取 KNSS 作者预印本的引言与第 3–6 节，并视觉检查 PDF 页 18–20；用其区分 mild、古老解、峰值提取及 Proposition 6.1 后的常向量障碍。另读取 Miller v4 的指定页段和第 5 节证明，用于确认中间应变特征值的条件正则性目标。</p><p>2025/2026 出版方材料只作有限时效核验；未读部分、外引局部理论和一般三维分类问题没有被补写成已审计结论。第三方 PDF 不属于公开资产，也不声明完成 Deep Research、新颖性检索或外部同行评审。</p></section>
      <section><div class="section-no">08 / 证据、边界与下一问题</div><h2>下一步只检查固定初值完整历史中的时间排序与 mild 尾项</h2><table><thead><tr><th>类别</th><th>本章范围</th></tr></thead><tbody><tr><td>PROVED METHOD OBSTRUCTION</td><td>真实光滑 NS 有限段在 BH.1 的粗预算下仍可局部趋于非零常向量。</td></tr><tr><td>FIXED-HISTORY NOT REPRODUCED</td><td>不是同一固定初值、首次爆破序列或精确 record；BH.17 的历史比例与遥远初值趋零没有复制。</td></tr><tr><td>FINITE CHECKS ONLY</td><td>三份文本源、18 个 BH 公式标签、81/81 文件绑定与 22 项缩放复算；不替代 PDE 证明。</td></tr><tr><td>OPEN</td><td>固定初值完整历史的定量非恒定性、mild 时间排序、一般古老解刚性、G/Q、奇点排除与 Clay。</td></tr></tbody></table><p class="note">科学源提交：4dfd49be08e9f8bb253432851669c9d632936b5c；冻结提交：b44960f63d35f0fd269cf1fc412921df91523a9a。六份本轮文件、七十五份依赖和一份冻结 manifest 由 SHA-256 绑定。内部模型复核不是外部同行评审。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_ancient_constant_sequence_preflight_20260906.md">BH 常向量极限反检查</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_dynamic_strategy_review_20260906.md">动力学策略复查</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_dynamic_strategy_primary_reading_20260906.md">原始来源阅读记录</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_ancient_constant_screen_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap；不分发第三方 PDF，也不改私有热演化论文。G OPEN / NOT CLAY。</strong></p></section>
    </article>
    <footer class="footer">CB.15 · Independent HTML research note · ClayB-AncientConstantScreen-20260906 · 2026-09-06</footer>
  </main>'''


EN_MAIN = '''  <main data-language="en">
    <article>
      <header class="hero">
        <div class="kicker">CB.15 · Independent Clay-B methods note · 2026-09-06</div>
        <h1>CB.15 | Constant ancient limits: a coarse-budget countercheck with genuine NS segments</h1>
        <p class="dek">Genuine smooth, unforced, unit-viscosity NS segments on expanding periodic domains can simultaneously have zero mean, past velocity 1+o(1), a terminal unit peak, cell energy O(period scale), and normalized dissipation tending to zero, while converging locally to a nonzero constant vector. This blocks automatic constant exclusion from those coarse budgets. It is neither a fixed-data first-blow-up sequence nor a Navier–Stokes counterexample.</p>
        <div class="meta"><span>PROVED METHOD OBSTRUCTION</span><span>GENUINE NS SEGMENTS</span><span>FINITE CHECKS ONLY</span><span>FIXED-HISTORY NOT REPRODUCED</span><span>G OPEN · NOT CLAY</span></div>
      </header>
      <section><div class="section-no">01 / Result map</div><h2>Genuine NS evolution still does not make coarse energy budgets exclude constant limits automatically</h2><div class="grid"><div class="card"><strong class="proved">BH / genuine NS segments</strong>Every member is a smooth, unforced, unit-viscosity NS solution on an expanding torus, with normalized pressure and the local energy equality.</div><div class="card"><strong class="open">BH / method obstruction</strong>Terminal normalization, a uniform past velocity bound, cell energy, and small normalized dissipation still permit a unit constant local limit.</div><div class="card"><strong class="open">Boundary / fixed history absent</strong>A common fixed initial datum, first candidate singularity, exact running record, full-history ratio, and vanishing remote initial amplitude are not reproduced.</div></div><p>The chapter therefore neither constructs nor excludes a singularity, enlarges a regularity class, or reduces assumptions in G or Q.</p></section>
      <section><div class="section-no">02 / BH.1–BH.8</div><h2>A compact divergence-free seed gives short-time control uniform in the large torus and small viscosity</h2><p>Start from a compactly supported curl seed V that equals a nonzero constant vector in its core, then solve for U_n on a torus of period scale n² with viscosity 1/n. The unnormalized inhomogeneous H^m estimate is uniform across all large tori:</p><div class="equation">½ d||U_n||_(H^m)²/dτ + n⁻¹||∇U_n||_(H^m)²
≤ C ||U_n||_(H^m)³.                               (BH.5)</div><p>The standard periodic local-existence and continuation interface supplies a common lifetime and uniform H^m bound, yielding ||U_n(τ)−V||_∞=O(n^(-1/2)) for τ≤n^(-1/2). The standard local theory is invoked explicitly, not claimed re-proved in full.</p></section>
      <section><div class="section-no">03 / BH.9–BH.12</div><h2>The first exact scaling turns the small-viscosity solution into a genuine unit-viscosity NS history</h2><p>Set v_n(y,s)=U_n(y/n,(s+√n)/n). The time, transport, pressure-gradient, and viscous factors match exactly, so v_n solves unforced unit-viscosity NS on period scale L_n=n³ over [−√n,0].</p><div class="equation">sup_s ∫|v_n|² ≤ n³||V||₂² = O(L_n),
∫∫|∇v_n|² ≤ C n^(3/2) = o(L_n).                   (BH.11–12)</div><p>The small normalized dissipation uses the pointwise-in-time uniform gradient bound from BH.6. The small-viscosity energy equality alone would give only O(L_n), and the two evidence routes are not conflated.</p></section>
      <section><div class="section-no">04 / BH.13–BH.15</div><h2>After terminal-peak normalization, genuine NS segments approach a unit constant vector</h2><p>A second exact parabolic scaling at the terminal maximum q_n and point y_n gives w_n. Its period scale and past length are ℓ_n=q_n n³ and b_n=q_n²√n, with</p><div class="equation">|w_n(0,0)|=1,
sup_(-b_n≤s≤0)||w_n(s)||_∞≤1+O(n^(-1/2)),
w_n → c,  |c|=1,  locally uniformly.              (BH.14–15)</div><p>Every w_n remains a genuine smooth NS solution, has exactly zero mean, and retains normalized periodic pressure. The nonzero constant c is itself a legitimate ancient mild NS solution, so reaching c creates no contradiction.</p></section>
      <section><div class="section-no">05 / BH.16–BH.18</div><h2>The countercheck does not reproduce the complete history of one fixed initial datum</h2><p>A peak rescaling from the same period-one initial datum near a first candidate singularity retains</p><div class="equation">b_k/ℓ_k² → T_* &gt; 0,
||v_k(-b_k)||_∞ → 0.                              (BH.17)</div><p>Here instead b_n/ℓ_n²=n^(-11/2)→0, the left-end amplitude tends to 1, and the members are not arranged as exact running records. The construction therefore blocks only automatic constant exclusion from the BH.1 coarse budgets. It does not rule out a narrower argument using fixed-data provenance, the complete-history ratio, remote initial data, or exact temporal ordering.</p></section>
      <section><div class="section-no">06 / Review of two dynamical routes</div><h2>Strain geometry and ancient-solution rigidity still lack their actual closing inputs</h2><p>The middle-strain-eigenvalue route still needs a critical spacetime bound, while moving-center localization creates an unpaid cutoff-transport term. Kinematic identities are not new temporal control. The ancient-solution route must separate two questions: whether all bounded ancient mild solutions are constants, and whether a nonzero constant can be excluded for limits coming from one fixed-data peak history.</p><p>The constant limit here is not a counterexample to a general classification by constants. Neither route reduces assumptions in G, Q, or signed pressure work, and neither enlarges a known regularity class.</p></section>
      <section><div class="section-no">07 / Primary-source reading</div><h2>The sources locate the boundary; they do not constitute exhaustive literature or novelty review</h2><p>This round reads the introduction and §§3–6 of the KNSS author preprint and visually checks PDF pages 18–20, using them to distinguish mild solutions, ancient solutions, peak extraction, and the constant-vector obstacle following Proposition 6.1. Specified portions of Miller v4 and the proofs in §5 are also read to identify the conditional middle-strain-eigenvalue regularity target.</p><p>Publisher material from 2025/2026 supplies only a bounded freshness check. Unread sections, external local theory, and the general three-dimensional classification problem are not rewritten as audited conclusions. Third-party PDFs are not public assets, and no Deep Research, exhaustive novelty search, or external peer review is claimed.</p></section>
      <section><div class="section-no">08 / Evidence, boundary, and next question</div><h2>The next check is limited to temporal ordering and mild tails in the complete fixed-data history</h2><table><thead><tr><th>Class</th><th>Scope here</th></tr></thead><tbody><tr><td>PROVED METHOD OBSTRUCTION</td><td>Genuine smooth NS finite segments can approach a nonzero constant under the BH.1 coarse budgets.</td></tr><tr><td>FIXED-HISTORY NOT REPRODUCED</td><td>This is not a common-fixed-data first-blow-up sequence or exact record; the BH.17 history ratio and vanishing remote initial amplitude are absent.</td></tr><tr><td>FINITE CHECKS ONLY</td><td>Three text sources, 18 BH formula labels, 81/81 file bindings, and 22 scaling recomputations; none replaces PDE proof.</td></tr><tr><td>OPEN</td><td>Quantitative nonconstancy in a complete fixed-data history, mild temporal ordering, general ancient rigidity, G/Q, singularity exclusion, and Clay.</td></tr></tbody></table><p class="note">Scientific source commit: 4dfd49be08e9f8bb253432851669c9d632936b5c; freeze commit: b44960f63d35f0fd269cf1fc412921df91523a9a. Six current files, seventy-five dependencies, and one frozen manifest are SHA-256-bound. Internal model review is not external peer review.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_ancient_constant_sequence_preflight_20260906.md">BH constant-limit countercheck</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_dynamic_strategy_review_20260906.md">dynamical strategy review</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_dynamic_strategy_primary_reading_20260906.md">primary-source reading record</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_ancient_constant_screen_frozen_ledger_20260906.json">portable ledger</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap; it redistributes no third-party PDF and does not modify the private heat-evolution paper. G OPEN / NOT CLAY.</strong></p></section>
    </article>
    <footer class="footer">CB.15 · Independent HTML research note · ClayB-AncientConstantScreen-20260906 · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-ancient-constant-screen" aria-labelledby="clay-b-ancient-constant-screen-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.15 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · ANCIENT CONSTANT SCREEN</p><h2 class="route-map-title" id="clay-b-ancient-constant-screen-title">CB.15｜常向量古老极限：真实 NS 有限段的粗预算反检查</h2><p class="route-map-intro">真实、无外力、单位黏性光滑 NS 有限段，在零均值、过去速度 1+o(1)、终点单位峰值、整胞能量 O(周期尺度) 和归一化耗散趋零的粗预算下，仍可局部趋于非零常向量。这只阻断粗预算自动排常量，不复制同一固定初值、首次爆破或精确 record。G OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 常向量极限反检查笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-ancient-constant-screen-20260906.html">阅读最新 CB.15 常向量反检查笔记 →</a><a href="/literature-review.html#clay-b-ancient-constant-screen-boundary">查看原始来源与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 常向量反检查结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>真实 NS 有限段构造成立</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>粗预算自动排常量停止</span><span><i class="route-legend-mark current" aria-hidden="true"></i>固定初值完整历史、G/Q 与正则性 OPEN · NOT CLAY</span></div></div></section>'''


CB15_ROW = '''          <div class="tree-row clay-b-ancient-constant-screen-row">
            <article class="tree-node current">
              <div class="tree-node-head"><span class="route-range">CB.15 · 2026-09-06 · BH ANCIENT CONSTANT SCREEN</span><span class="tree-state current">当前路线边界</span></div>
              <h3>CB.15｜常向量古老极限：真实 NS 有限段的粗预算反检查</h3>
              <p>BH 构造扩张周期域上的真实、无外力、单位黏性光滑 NS 有限段：零均值、终点单位峰值、过去速度 1+o(1)、整胞能量 O(周期尺度)、归一化耗散趋零，并局部收敛到单位常向量。</p>
              <p>这只排除用 BH.1 粗预算自动排常量的方法。序列没有复制同一固定初值、首次候选奇点、精确 running record、b/ℓ²→T_*&gt;0 或遥远初值速度趋零；常向量也不是一般分类命题的反例。</p>
              <p class="tree-path">CB.14 energy-only 候选停止 → BH 真实 NS 有限段 → 两次精确缩放 → 非零常向量局部极限 → 粗预算排常量受阻 → 固定初值完整历史仍 OPEN</p>
              <p><a href="/notes/clay-b-pressure-mechanism-screen-20260906.html">CB.14：压力机制筛查</a> · <a href="/notes/clay-b-ancient-constant-screen-20260906.html">CB.15：常向量极限反检查</a></p>
            </article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发问题：固定初值完整历史</h3><p>只检查峰值归一化后的时间排序与 mild 表达式：线性项虽趋零，遥远过去的非线性尾是否仍能留下常向量尚未支付。若只能重写未知正则性条件，就停止该尝试。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.16 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.15</h3><p>CB.16 只是下一章占位，不是已完成研究。同一固定初值完整历史的定量非恒定性、mild 时间排序、一般古老解刚性、G/Q、带符号压力功上界、首次奇点排除与 Clay 均未冻结。</p></article></div>'''


LITERATURE_BLOCK = '''<h3 id="clay-b-ancient-constant-screen-boundary">CB.15 · Clay-B 常向量古老极限的文献和主张边界</h3><p>本轮读取 <a href="https://www-users.cse.umn.edu/~sverak/publications/liouville.pdf">Koch–Nadirashvili–Seregin–Šverák 作者预印本</a> 的引言与第 3–6 节（PDF 页 6–24），并视觉检查 PDF 页 18–20，用于区分 mild 解、古老解、峰值提取及 Proposition 6.1 后的常向量障碍；另核对 <a href="https://arxiv.org/abs/1710.05569">Miller v4</a> 的指定页段与第 5 节证明，用于识别中间应变特征值的条件正则性目标。2025/2026 出版方材料只作有限时效核验。未读部分、外引局部存在与正则性理论、一般三维古老解分类均未扩写为已审计结论；没有穷尽文献、Deep Research、新颖性或外部同行评审声明。</p><div class="boundary"><strong>CB.15 · ClayB-AncientConstantScreen-20260906 公开边界</strong><p>PROVED METHOD OBSTRUCTION：BH 构造的每一项都是真实、无外力、单位黏性光滑周期 NS 有限段；在零均值、过去速度 1+o(1)、终点单位峰值、整胞能量 O(周期尺度) 与归一化耗散趋零下，局部极限仍可为非零常向量。FIXED-HISTORY NOT REPRODUCED：它不是同一固定初值的首次爆破序列，不是每项精确 running record；真正固定初值历史保留 b/ℓ²→T_*&gt;0 与遥远左端速度趋零，本构造对应极限分别为 0 与 1。常向量是合法古老 mild 解，不是一般常量分类的反例。FINITE CHECKS ONLY：三份文本源、18 个 BH 标签、81/81 文件绑定与 22 项缩放复算不替代 PDE 证明。OPEN：固定初值完整历史、mild 时间排序、一般古老解刚性、G/Q、奇点排除与 Clay。无图件、仿真、新 PDF 或累计 recap。NOT CLAY。<a href="/notes/clay-b-ancient-constant-screen-20260906.html">阅读完整 CB.15 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-pressure-mechanism-screen-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>常向量古老极限：真实 NS 有限段的粗预算反检查</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 真实 NS 有限段的常向量古老极限构造、粗预算方法阻碍与固定初值历史边界的双语方法笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.15 · {DISPLAY_ID}</strong></header>', template, count=1)
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
    value = value.replace("CB.1–CB.14", "CB.1–CB.15")
    value = value.replace("periodic pressure identity / energy-class endpoint screen", "genuine NS finite-segment / constant-limit obstruction", 1)
    old_focus = "Clay-B 已完成单侧压力机制的一轮有界筛查：周期径向恒等式精确成立，固定外尺度修正由能量支付；基本能量只给负压力势的时间可积控制，抽象端点反检查明确不是 NS 解。energy-only 候选停止，真实 NS 机制、Q_J 和合同 G 继续开放。"
    new_focus = "Clay-B 已完成常向量古老极限的一轮真实 NS 反检查：光滑有限段在粗能量预算下仍可趋于非零常向量，因此自动排常量的方法停止；同一固定初值、完整历史比例、精确 record、mild 时间排序与合同 G 继续开放。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    if 'class="tree-row clay-b-ancient-constant-screen-row"' in value:
        if "Clay-B 独立路线停在 CB.15" not in value or "CB.16 · NEXT" not in value:
            raise RuntimeError("existing CB.15 route boundary drift")
        return value
    cb14_start = value.index('<div class="tree-row clay-b-pressure-mechanism-screen-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb14_start)
    cb14 = value[cb14_start:boundary_start]
    cb14 = cb14.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb14 = cb14.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb14, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">ANCIENT CONSTANT SCREEN COMPLETED</span><h3>真实 NS 常向量反检查已进入 CB.15</h3><p>BH 已用真实光滑 NS 有限段检验粗预算排常量机制，同时保留固定初值完整历史、精确 record 与一般古老解刚性的边界；结果见下一个正式路线节点。</p></aside>', cb14, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.14 branch drift")
    value = value[:cb14_start] + cb14 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB15_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-ancient-constant-screen-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 15
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.15"
    payload["nextIndependentChapter"] = "CB.16"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note",
            "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.15",
            "sourceCommit": "4dfd49be08e9f8bb253432851669c9d632936b5c", "baseCommit": "9069f24128b0ef8db8192b1ddff998516b82a757",
            "handoffCommit": "b44960f63d35f0fd269cf1fc412921df91523a9a", "logicalPredecessor": "ClayB-PressureMechanismScreen-20260906",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False, "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-ancient-constant-screen-20260906-gate.test.mjs", "publicationTest": "tests/clay-b-ancient-constant-screen-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-ancient-constant-screen-20260906-translations.mjs", "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE", "simulationRequired": False, "recapRequired": False,
            "advancesCanonicalR0Series": False, "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "GENUINE_SMOOTH_NS_FINITE_SEGMENTS_CAN_CONVERGE_TO_NONZERO_CONSTANT_UNDER_COARSE_BUDGETS_FIXED_INITIAL_DATUM_FIRST_BLOWUP_EXACT_RECORD_AND_COMPLETE_HISTORY_NOT_REPRODUCED_CONSTANTS_NOT_GENERAL_CLASSIFICATION_COUNTEREXAMPLE_G_Q_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.15", DISPLAY_ID, "常向量古老极限：真实 NS 有限段的粗预算反检查", "Constant ancient limits: a coarse-budget countercheck with genuine NS segments", "PROVED", "FINITE", "GENUINE NS SEGMENTS", "FIXED-HISTORY NOT REPRODUCED", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.15", "Clay-B 独立路线停在 CB.15", "CB.16 · NEXT", 'class="tree-row clay-b-ancient-constant-screen-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb15 = home.index('class="tree-row clay-b-ancient-constant-screen-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb15)
    if not (r0_start < r0_boundary < divider < clay_start < cb15 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-ancient-constant-screen-boundary"' not in literature or "CB.15 · ClayB-AncientConstantScreen-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.15 · {DISPLAY_ID}" not in index or "15 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.15" or site.get("nextIndependentChapter") != "CB.16":
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
print(json.dumps({"schemaVersion": "clay-b-ancient-constant-screen-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.15", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
