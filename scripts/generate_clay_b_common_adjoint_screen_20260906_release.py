#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB CommonAdjointScreen CB.19 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.63"
SLUG = "clay-b-common-adjoint-screen-20260906"
DISPLAY_ID = "ClayB-CommonAdjointScreen-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_SECTIONS = [
    ("01 / 结果地图", "条件结构成立，算子出口并未变弱", '<div class="grid"><div class="card"><strong class="proved">LITERATURE RECONSTRUCTION</strong>在正终端能量原子这一额外条件下，BP/BQ 重构同一固定周期 NS 原解驱动的共同伴随与最终保留离散链的全尾结构。</div><div class="card"><strong class="proved">SECOND-ORDER OBSTRUCTION</strong>一个固定后继解在互异晚期时间单元上的二阶作用与 enstrophy 生产正部发散，但这不与一阶能量矛盾。</div><div class="card"><strong class="open">BUDGET STRENGTH AUDIT</strong>BR 证明全单位初态延迟算子预算即使只对某一对时刻有限，也已等价于同一原解越过 T 光滑延拓；没有证明该预算有限。</div></div><p>本章没有证明原子存在或排除，也没有扩大一般三维 NS 正则性类别。</p>'),
    ("02 / BP.1–BP.10", "共同伴随保留同一原解、原时间和正原子条件", '<p>固定同一个无外力、终点前光滑的周期 NS 原解，并额外假设终端能量测度在 a 有质量 m&gt;0 的原子。先固定局部 Hodge 球与差投影，再定义正交 packet；链的选择依赖原子，但不更换漂移或原时间。</p><div class="equation">|u(t)|²dx ⇀* μ_*,  μ_*({a})=m&gt;0;\nq_j=D_j u(τ_j)/||D_j u(τ_j)||₂.                 (BP.2, BP.10)</div><p>这里没有终端强 L² 迹，也没有从任意奇点自动生成原子或 packet。</p>'),
    ("03 / BP.11–BP.16", "被动避让与带压力反向局部化是两个不同工具", '<p>周期 Nash 给逐分量被动演化的 L¹→L² 与 L²→L∞ 平滑，用于选球时支付小体积；反向脉冲则保留 Leray 投影、零均值规范压力和完整局部能量式。</p><div class="equation">||S(t,s)||_(1→2), ||S(t,s)||_(2→∞) ≤ C[1+(ν(t−s))^(−3/4)].  (BP.11)</div><p>这个标量平滑界不转写成受压力约束演化 U 的同一 L∞ 估计；压力输运项也没有被删除。</p>'),
    ("04 / BP.17–BP.32", "弱零终端迹、原子定位和 Hilbert 饱和给离散全尾", '<p>反向脉冲先在每个严格终点前区间紧化为同一个伴随 A。它与原解保持常配对，却只有弱零终端迹；反向局部化把其能量定位到原子，Cauchy–Schwarz 饱和给终端范数一。</p><div class="equation">A(t) ⇀ 0,  ⟨u(t),A(t)⟩=√m,  |A(t)|²dx ⇀* δ_a.       (BP.20–BP.25)</div><p>固定 Hilbert 直和中的范数相等再给全尾强收敛，并统一覆盖最终保留链的所有晚期离散节点对；不是任意连续时间对，也不是原目录全部条目。</p>'),
    ("05 / BQ.1–BQ.9", "二阶作用发散不与一阶能量矛盾", '<p>固定一个起点 J 和一个后继解 H(t)=U(t,τ_J)q_J。相邻晚期节点接近两个正交向量，迫使每个互不重叠时间单元走过固定 L² 距离。</p><div class="equation">K_j=∫_(I_j)||ΔH||²₂→∞,\n∫_(τ_(J+1))^T||ΔH||²₂=∞,  ∫_(τ_(J+1))^T(P_H)_+=∞.  (BQ.6–BQ.9)</div><p>这里使用互异时间单元，没有重复计算 BO 的嵌套尾窗口。能量只支付一阶耗散，因此上述二阶发散本身不产生矛盾。</p>'),
    ("06 / BQ.10–BQ.13", "原文的 Serrin 算子上界仍是额外输入", '<p>延迟算子预算 R_u(s,r) 对全部单位无散初态取上确界。正原子给一个具体初态使其发散；原文在额外 Serrin 条件下才给上界。</p><div class="equation">u∈L^p_tL^q_x,  3&lt;q≤∞,  2/p+3/q≤1  ⇒  R_u(s,r)&lt;∞.  (BQ.10–BQ.13)</div><p>在基本能量的 L²_tL⁶_x 水平，q=6 的估计需要时间四次方；一阶能量没有支付该条件。</p>'),
    ("07 / BR.1–BR.12", "全算子预算已经等价于延拓", '<p>共同伴随给每个固定 s 的特定后继 F_s(t)=U(t,s)A(s) 一个严格正配对。若 F_s 有强终端迹，便与 A(t) 的弱零终端迹矛盾；有限二阶作用会产生这样的强迹。</p><div class="equation">T 前光滑延拓 ⇔ ∃ s&lt;r: R_u(s,r)&lt;∞ ⇔ ∀ s&lt;r: R_u(s,r)&lt;∞.  (BR.12)</div><p>反向蕴含把原解初态 u(s) 代入全算子预算，再用周期嵌入、enstrophy 估计和已知 H¹ 局部理论。这个等价只属于固定无外力周期、终点前光滑设定；它识别条件强度，不证明条件成立，也不宣称新颖性。</p>'),
    ("08 / 来源、证据与下一步", "终端唯一性适用性核查尚未开始", '<p>本轮完整使用 Huang arXiv:2608.04138v1 的 §§2–7，但第 20 页未读，Appendix A 未完整核查；Tao arXiv:1108.1165v4 只调用周期 H¹ 局部存在、唯一性、光滑性与延拓接口。两者的全部外部依赖并未重审，内部模型复核不是外部同行评审。</p><p>下一研发动作仅核查带压力、由真实 NS 原解驱动的共同伴随是否有适用的终端唯一性定理，并逐项匹配时间方向、弱终端迹、漂移空间、非局部投影与定义域。该核查尚未开始，不得展示成已有定理。</p><p class="note">科学源提交：32b12bff99e7a88d6be3d1317fd125cf30a72792；冻结提交：2a2b6c9ee51cab238b11b485ae1b6b5564a75395。八份本轮文件、117 份依赖和一份冻结 manifest 由 SHA-256 绑定；五份文本源、57 个 BP/BQ/BR 标签、31 项精确算术检查与 3 项有限负对照通过。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_common_adjoint_full_tail_20260906.md">BP 共同伴随正文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_full_tail_second_order_20260906.md">BQ 二阶成本正文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_operator_budget_strength_20260906.md">BR 预算强度审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_common_adjoint_report_20260906.md">阶段报告</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap；不分发第三方 PDF。G OPEN / NOT CLAY。</strong></p>'),
]

EN_SECTIONS = [
    ("01 / Result map", "The conditional structure holds; the operator exit is not weaker", '<div class="grid"><div class="card"><strong class="proved">LITERATURE RECONSTRUCTION</strong>Under the additional assumption of a positive terminal energy atom, BP/BQ reconstruct a common adjoint driven by the same fixed periodic NS parent and full-tail structure on the final retained discrete chain.</div><div class="card"><strong class="proved">SECOND-ORDER OBSTRUCTION</strong>One fixed descendant has divergent second-order action and positive enstrophy-production part on disjoint late time cells, but this does not contradict first-order energy.</div><div class="card"><strong class="open">BUDGET STRENGTH AUDIT</strong>BR proves that finiteness of the full unit-initial-data delayed operator budget for even one time pair is already equivalent to smooth continuation of the same parent across T. Its finiteness is not proved.</div></div><p>This chapter proves neither atom existence nor atom exclusion and enlarges no general three-dimensional NS regularity class.</p>'),
    ("02 / BP.1–BP.10", "The common adjoint retains the same parent solution, original time, and positive-atom condition", '<p>Fix the same unforced periodic NS parent, smooth before the endpoint, and additionally assume that its terminal energy measure has an atom of mass m&gt;0 at a. Local Hodge balls and difference projections are fixed before the orthogonal packets are defined. The retained chain depends on the atom, but neither drift nor original time is changed.</p><div class="equation">|u(t)|²dx ⇀* μ_*,  μ_*({a})=m&gt;0;\nq_j=D_j u(τ_j)/||D_j u(τ_j)||₂.                 (BP.2, BP.10)</div><p>No strong terminal L² trace is assumed, and no atom or packet is automatically generated from an arbitrary singularity.</p>'),
    ("03 / BP.11–BP.16", "Passive avoidance and pressure-retaining reverse localization are distinct tools", '<p>Periodic Nash smoothing gives L¹→L² and L²→L∞ bounds for componentwise passive evolution, paying for small volume when balls are selected. Reverse pulses instead retain the Leray projection, zero-mean canonical pressure, and the complete local energy identity.</p><div class="equation">||S(t,s)||_(1→2), ||S(t,s)||_(2→∞) ≤ C[1+(ν(t−s))^(−3/4)].  (BP.11)</div><p>This scalar smoothing bound is not transferred to the pressure-constrained evolution U as the same L∞ estimate, and pressure transport is not deleted.</p>'),
    ("04 / BP.17–BP.32", "Weak-zero terminal trace, atomic localization, and Hilbert saturation yield a discrete full tail", '<p>Reverse pulses first compactify to one common adjoint A on every interval strictly before the endpoint. It has constant pairing with the parent but only weak-zero terminal trace. Reverse localization concentrates its energy at the atom, and Cauchy–Schwarz saturation gives terminal norm one.</p><div class="equation">A(t) ⇀ 0,  ⟨u(t),A(t)⟩=√m,  |A(t)|²dx ⇀* δ_a.       (BP.20–BP.25)</div><p>Norm equality in a fixed Hilbert direct sum then gives full-tail strong convergence uniformly over all late discrete pairs in the final retained chain. This is neither arbitrary continuous-time propagation nor the entire original catalogue.</p>'),
    ("05 / BQ.1–BQ.9", "Divergent second-order action does not contradict first-order energy", '<p>Fix one start J and one descendant H(t)=U(t,τ_J)q_J. Adjacent late nodes approach two orthogonal vectors, forcing a fixed L² distance across every disjoint time cell.</p><div class="equation">K_j=∫_(I_j)||ΔH||²₂→∞,\n∫_(τ_(J+1))^T||ΔH||²₂=∞,  ∫_(τ_(J+1))^T(P_H)_+=∞.  (BQ.6–BQ.9)</div><p>These are disjoint cells, not repeated charges on BO’s nested tail windows. Energy pays only first-order dissipation, so the second-order divergence itself creates no contradiction.</p>'),
    ("06 / BQ.10–BQ.13", "The paper's Serrin operator upper bound remains an additional input", '<p>The delayed operator budget R_u(s,r) takes a supremum over all unit divergence-free initial data. A positive atom supplies one concrete datum that makes it infinite; the paper obtains an upper bound only under an additional Serrin condition.</p><div class="equation">u∈L^p_tL^q_x,  3&lt;q≤∞,  2/p+3/q≤1  ⇒  R_u(s,r)&lt;∞.  (BQ.10–BQ.13)</div><p>At the energy-level L²_tL⁶_x input, the q=6 estimate needs fourth-power time integrability. First-order energy does not pay it.</p>'),
    ("07 / BR.1–BR.12", "The full operator budget is already equivalent to continuation", '<p>For every fixed s, the common adjoint gives a specific descendant F_s(t)=U(t,s)A(s) with strictly positive pairing. A strong terminal trace for F_s would contradict the weak-zero terminal trace of A(t); finite second-order action would create that strong trace.</p><div class="equation">smooth continuation across T ⇔ ∃ s&lt;r: R_u(s,r)&lt;∞ ⇔ ∀ s&lt;r: R_u(s,r)&lt;∞.  (BR.12)</div><p>The reverse implication inserts the parent datum u(s) into the full operator budget and then uses periodic embedding, the enstrophy estimate, and known H¹ local theory. This equivalence belongs only to the fixed unforced periodic, preterminal-smooth setting. It identifies the condition’s strength, proves no finiteness, and makes no novelty claim.</p>'),
    ("08 / Sources, evidence, and next step", "The terminal-uniqueness applicability audit has not started", '<p>This round uses §§2–7 of Huang arXiv:2608.04138v1 in full, but page 20 was not read and Appendix A was not completely audited. From Tao arXiv:1108.1165v4 it invokes only the periodic H¹ local existence, uniqueness, smoothness, and continuation interfaces. Not every external dependency was reaudited, and internal model review is not external peer review.</p><p>The next research action only asks whether a terminal-uniqueness theorem applies to the pressure-coupled common adjoint driven by the true NS parent, matching time direction, weak terminal trace, drift space, nonlocal projection, and domain. That audit has not started and must not be displayed as an available theorem.</p><p class="note">Scientific source commit: 32b12bff99e7a88d6be3d1317fd125cf30a72792; freeze commit: 2a2b6c9ee51cab238b11b485ae1b6b5564a75395. Eight current files, 117 dependencies, and one frozen manifest are SHA-256-bound. Five text sources, 57 BP/BQ/BR labels, 31 exact arithmetic checks, and three limited negative controls pass.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_common_adjoint_full_tail_20260906.md">BP common-adjoint source</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_full_tail_second_order_20260906.md">BQ second-order source</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_operator_budget_strength_20260906.md">BR budget-strength audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_common_adjoint_report_20260906.md">stage report</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap and redistributes no third-party PDF. G OPEN / NOT CLAY.</strong></p>'),
]


def main_block(lang: str, sections: list[tuple[str, str, str]]) -> str:
    if lang == "zh":
        kicker = "CB.19 · 独立 Clay-B 方法笔记 · 2026-09-06"
        title = "CB.19｜共同伴随与算子出口：结构保留，预算等价于延拓"
        dek = "在正终端能量原子的条件分支中，共同伴随和最终离散全尾结构可保留；固定后继解的二阶作用发散，但不与一阶能量矛盾。更关键的是，全单位初态延迟算子预算即使只对某一对时刻有限，也已等价于同一原解越过终点光滑延拓。"
        footer = "独立 HTML 研究笔记"
    else:
        kicker = "CB.19 · Independent Clay-B methods note · 2026-09-06"
        title = "CB.19 | Common adjoint and operator exit: retained structure, budget equivalent to continuation"
        dek = "On the conditional positive-terminal-energy-atom branch, the common adjoint and final discrete full-tail structure survive. A fixed descendant has divergent second-order action, without contradicting first-order energy. More importantly, finiteness of the full unit-initial-data delayed operator budget for even one time pair is already equivalent to smooth continuation of the same parent across the endpoint."
        footer = "Independent HTML research note"
    body = "".join(f'<section><div class="section-no">{n}</div><h2>{h}</h2>{c}</section>' for n, h, c in sections)
    return f'''  <main data-language="{lang}">
    <article><header class="hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="dek">{dek}</p><div class="meta"><span>PROVED IN STATED SCOPE</span><span>LITERATURE RECONSTRUCTION</span><span>CONDITIONAL</span><span>SECOND-ORDER OBSTRUCTION</span><span>BUDGET STRENGTH AUDIT</span><span>FINITE CHECKS ONLY</span><span>G OPEN · NOT CLAY</span></div></header>{body}</article>
    <footer class="footer">CB.19 · {footer} · {DISPLAY_ID} · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-common-adjoint-screen" aria-labelledby="clay-b-common-adjoint-screen-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.19 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · COMMON-ADJOINT SCREEN</p><h2 class="route-map-title" id="clay-b-common-adjoint-screen-title">CB.19｜共同伴随与算子出口：结构保留，预算等价于延拓</h2><p class="route-map-intro">正终端能量原子的条件分支保留同一原解驱动的共同伴随与最终离散全尾；固定后继解二阶作用发散，但基本能量不支付该成本。全单位初态延迟算子预算的有限性已等价于同一原解光滑延拓，而不是更弱的已支付条件。G OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 共同伴随与算子出口笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-common-adjoint-screen-20260906.html">阅读最新 CB.19 共同伴随笔记 →</a><a href="/literature-review.html#clay-b-common-adjoint-screen-boundary">查看原始来源与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 共同伴随筛查结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>同一原解与最终离散全尾结构保留</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>全算子预算不是更弱出口</span><span><i class="route-legend-mark current" aria-hidden="true"></i>终端唯一性适用性与一般正则性 OPEN · NOT CLAY</span></div></div></section>'''

CB19_ROW = '''          <div class="tree-row clay-b-common-adjoint-screen-row">
            <article class="tree-node current"><div class="tree-node-head"><span class="route-range">CB.19 · 2026-09-06 · BP/BQ/BR COMMON-ADJOINT SCREEN</span><span class="tree-state current">当前路线边界</span></div><h3>CB.19｜共同伴随与算子出口：结构保留，预算等价于延拓</h3><p>BP/BQ 在正终端能量原子的额外条件下重构同一固定周期 NS 原解驱动的共同伴随和最终保留离散链全尾；一个固定后继解在互异时间单元上的二阶作用与 enstrophy 生产正部发散，但不与一阶能量矛盾。</p><p>BR 另证全单位初态延迟算子预算即使只对某一对时刻有限，也已等价于同一原解越过 T 光滑延拓。这个强度识别不证明预算有限，不排除原子，也不扩大一般正则性。</p><p class="tree-path"><a href="/notes/clay-b-common-adjoint-screen-20260906.html">阅读 CB.19 HTML</a> · <a href="/literature-review.html#clay-b-common-adjoint-screen-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发动作：终端唯一性适用性核查</h3><p>逐项比较带压力共同伴随的时间方向、弱终端迹、真实 NS 漂移空间、非局部投影和定义域。该核查尚未开始，不能展示成已适用或已支付的定理。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.20 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.19</h3><p>CB.20 只是下一章占位，不是已完成研究。终端唯一性适用性核查尚未开始；原子存在或排除、G、任意奇点输入生成、一般正则性与 Clay 均未关闭。</p></article></div>'''

LITERATURE_BLOCK = '''<h3 id="clay-b-common-adjoint-screen-boundary">CB.19 · Clay-B 共同伴随与算子出口的文献和主张边界</h3><p>本轮完整使用 <a href="https://arxiv.org/abs/2608.04138v1">Huang full-tail 预印本 2608.04138v1</a> 的 §§2–7，但第 20 页未读，Appendix A 未完整核查；定向读取 <a href="https://arxiv.org/abs/1108.1165v4">Tao 周期局部理论 1108.1165v4</a> 的 H¹ 局部存在、唯一性、光滑性、延拓与均值接口。两稿均已登记，不称新发现；引用的全部外部证明依赖未完全重审，没有穷尽性新颖性检索、完成 Deep Research 或外部同行评审。</p><div class="boundary"><strong>CB.19 · ClayB-CommonAdjointScreen-20260906 公开边界</strong><p>LITERATURE RECONSTRUCTION：在同一固定周期 NS 原解具有正终端能量原子的额外条件下，BP/BQ 重构共同伴随、弱零终端迹、原子定位、Cauchy 饱和及最终保留离散链的全尾；不是任意连续时间对或整个原目录。SECOND-ORDER OBSTRUCTION：一个固定后继解在互异晚期时间单元上的二阶作用及 enstrophy 生产正部发散，但一阶能量不支付二阶成本，因此没有矛盾。BUDGET STRENGTH AUDIT：BR 另证全单位初态延迟算子预算对某一对有限、对每一对有限与同一原解越过 T 光滑延拓等价；没有证明该预算有限，也不推广到弱解、外力或全空间。FINITE CHECKS ONLY：五份文本源、57 个 BP/BQ/BR 标签、125/125 文件绑定、31 项精确算术检查和 3 项有限负对照不替代 PDE 证明。原子存在/排除、终端唯一性适用性、G 与一般正则性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。<a href="/notes/clay-b-common-adjoint-screen-20260906.html">阅读完整 CB.19 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-energy-atom-cost-screen-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>共同伴随与算子出口：结构保留，预算等价于延拓</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 共同伴随、离散全尾、二阶作用和延迟算子预算强度的双语方法笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.19 · {DISPLAY_ID}</strong></header>', template, count=1)
    both = main_block("zh", ZH_SECTIONS) + "\n\n" + main_block("en", EN_SECTIONS)
    template, count = re.subn(r'  <main data-language="zh">[\s\S]*?  </main>\n\n  <main data-language="en">[\s\S]*?  </main>', both, template, count=1)
    if count != 1:
        raise RuntimeError("note bilingual template drift")
    return template


def update_home(value: str) -> str:
    value = set_version(value, "综述", refresh=True)
    value = re.sub(r'<strong>v\d+\.\d+</strong>网页版本', f'<strong>v{VERSION}</strong>网页版本', value, count=1)
    value, count = re.subn(r'<section class="route-overview independent-release-spotlight"[\s\S]*?</section>', SPOTLIGHT, value, count=1)
    if count != 1:
        raise RuntimeError("independent spotlight drift")
    value = value.replace("CB.1–CB.18", "CB.1–CB.19")
    value = value.replace("terminal energy atom / dissipation-cost screen", "common adjoint / operator-budget strength screen", 1)
    old_focus = "Clay-B 已完成终端能量原子的直接耗散成本测试：最后阈值窗口和完整带符号局部平衡给出严格次抛物宽度及 r^(1/2) 全局尾成本，但成本趋零且窗口嵌套，本次没有形成有限总耗散矛盾。下一步只核查 full-tail 的共同伴随结构。"
    new_focus = "Clay-B 已完成共同伴随核心与算子出口强度核查：正原子条件下同一原解驱动的共同伴随和最终离散全尾可保留，固定后继解二阶作用发散；但全单位初态延迟算子预算的有限性已等价于原解光滑延拓，并非更弱的能量出口。下一步只核查终端唯一性的适用条件。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    if 'class="tree-row clay-b-common-adjoint-screen-row"' in value:
        return value
    cb18_start = value.index('<div class="tree-row clay-b-energy-atom-cost-screen-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb18_start)
    cb18 = value[cb18_start:boundary_start]
    cb18 = cb18.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb18 = cb18.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb18, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">COMMON-ADJOINT SCREEN COMPLETED</span><h3>共同伴随核查已进入 CB.19</h3><p>BP/BQ/BR 已核对同一原解共同伴随、最终离散全尾、固定后继解二阶成本及全算子预算强度；结果见下一个正式路线节点。</p></aside>', cb18, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.18 branch drift")
    value = value[:cb18_start] + cb18 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB19_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-common-adjoint-screen-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 19
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.19"
    payload["nextIndependentChapter"] = "CB.20"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1",
            "kind": "independent-analytic-note",
            "releaseId": SLUG,
            "displayReleaseId": DISPLAY_ID,
            "chapter": "CB.19",
            "sourceCommit": "32b12bff99e7a88d6be3d1317fd125cf30a72792",
            "baseCommit": "7ea29a64cc1ba081e703afec4b59b3adeb9758da",
            "handoffCommit": "2a2b6c9ee51cab238b11b485ae1b6b5564a75395",
            "logicalPredecessor": "ClayB-EnergyAtomCostScreen-20260906",
            "html": f"public/notes/{SLUG}.html",
            "pdfGenerated": False,
            "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-common-adjoint-screen-20260906-gate.test.mjs",
            "publicationTest": "tests/clay-b-common-adjoint-screen-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-common-adjoint-screen-20260906-translations.mjs",
            "browserQaScript": "scripts/qa-publication-browser.mjs",
            "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False,
            "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE",
            "simulationRequired": False,
            "recapRequired": False,
            "advancesCanonicalR0Series": False,
            "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "CONDITIONAL_POSITIVE_TERMINAL_ATOM_RECONSTRUCTS_SAME_PARENT_COMMON_ADJOINT_AND_FINAL_RETAINED_DISCRETE_FULL_TAIL_FIXED_DESCENDANT_HAS_INFINITE_SECOND_ORDER_ACTION_WITHOUT_FIRST_ORDER_ENERGY_CONTRADICTION_FULL_UNIT_DATA_DELAYED_OPERATOR_BUDGET_FINITE_FOR_ONE_PAIR_IFF_SMOOTH_CONTINUATION_NOT_PROVED_ATOM_EXISTENCE_OR_EXCLUSION_TERMINAL_UNIQUENESS_NOT_STARTED_GENERAL_REGULARITY_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def handoff_bytes() -> bytes:
    ledger = json.loads((ROOT / "research/clay_b_common_adjoint_screen_frozen_ledger_20260906.json").read_text(encoding="utf-8"))
    qa = json.loads((ROOT / "release/qa/clay-b-common-adjoint-screen-20260906.json").read_text(encoding="utf-8"))
    artifacts = [{
        "path": row["path"],
        "sha256": row["sha256"],
        "role": "frozen-scientific-source" if row["role"] == "scientific-source" else "frozen-dependency",
        "commit": row["commit"],
    } for row in ledger["files"]]
    artifacts += [{
        "path": row["path"], "sha256": row["sha256"], "role": "frozen-release-manifest", "commit": row["commit"],
    } for row in ledger["handoffEnvelope"]]
    outputs = [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html", "public/notes/index.html", "public/site-version.json", "research/release-manifest.json", "VERSION"]
    support = ["research/clay_b_common_adjoint_screen_frozen_ledger_20260906.json", "release/handoffs/clay-b-common-adjoint-screen-20260906.json", "release/qa/clay-b-common-adjoint-screen-20260906.json", "scripts/import_clay_b_common_adjoint_screen_20260906_frozen.py", "scripts/generate_clay_b_common_adjoint_screen_20260906_release.py", "scripts/generate_note_index.py", "scripts/add-clay-b-common-adjoint-screen-20260906-translations.mjs", "tests/clay-b-common-adjoint-screen-20260906-gate.test.mjs", "tests/clay-b-common-adjoint-screen-20260906-release.test.mjs", "tests/release-publication-invariant.test.mjs", "translations/en.json", "public/i18n-en.js"]
    managed = list(dict.fromkeys(outputs + [row["path"] for row in artifacts] + support))
    payload = {
        "schemaVersion": "research-publication-handoff-v1",
        "releaseId": DISPLAY_ID,
        "frozenCommit": "2a2b6c9ee51cab238b11b485ae1b6b5564a75395",
        "sourceRepository": "navier-stokes-r074m",
        "translationRoute": "LOCAL_DIRECT_NO_DGX",
        "artifacts": artifacts,
        "artifactPolicy": {"readerPdf": "OMIT_NEW", "scientificFigure": "NOT_REQUIRED"},
        "claimBoundary": {"requiredLabels": ["PROVED", "FINITE", "LITERATURE RECONSTRUCTION", "CONDITIONAL", "SECOND-ORDER OBSTRUCTION", "BUDGET STRENGTH AUDIT", "OPEN", "NOT CLAY"], "publicFiles": [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html"]},
        "recap": {"mode": "PRESERVE", "latestRecapRelease": "r076i", "preservedArtifacts": [{"path": "public/recap-r0-61-r0-76i.html", "sha256": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9"}, {"path": "public/recap-r0-61-r0-76i.pdf", "sha256": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98"}]},
        "stages": {
            "generate": {"runner": "python-local", "script": "scripts/generate_clay_b_common_adjoint_screen_20260906_release.py", "inputs": [row["path"] for row in artifacts] + ["research/clay_b_common_adjoint_screen_frozen_ledger_20260906.json"], "outputs": outputs},
            "translate": {"runner": "node-local", "script": "scripts/add-clay-b-common-adjoint-screen-20260906-translations.mjs", "inputs": ["public/research-review.html", "public/literature-review.html", "public/notes/index.html", "translations/en.json"], "outputs": ["translations/en.json", "public/i18n-en.js"]},
        },
        "publication": {"expectedCommit": None, "siteBaseUrl": "https://kasifa.github.io", "repository": "Kasifa/Kasifa.github.io", "workflow": "pages.yml", "remote": "origin", "targetBranch": "main", "commitMessage": "Publish ClayB CommonAdjointScreen CB.19 HTML note", "managedPaths": managed, "expectedLive": qa["online"]["expectedLive"], "expectedAbsent": qa["online"]["expectedAbsent"], "siteVersionExpectations": qa["online"]["siteVersionExpectations"]},
        "visualQa": {"evidencePath": qa["browser"]["evidencePath"], "configPath": "release/qa/clay-b-common-adjoint-screen-20260906.json", "requiredChecks": [f"{target['id']}-{scenario['id']}" for target in qa["browser"]["targets"] for scenario in qa["browser"]["scenarios"]]},
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.19", DISPLAY_ID, "共同伴随与算子出口：结构保留，预算等价于延拓", "Common adjoint and operator exit: retained structure, budget equivalent to continuation", "PROVED IN STATED SCOPE", "LITERATURE RECONSTRUCTION", "CONDITIONAL", "BUDGET STRENGTH AUDIT", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.19", "Clay-B 独立路线停在 CB.19", "CB.20 · NEXT", 'class="tree-row clay-b-common-adjoint-screen-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb19 = home.index('class="tree-row clay-b-common-adjoint-screen-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb19)
    if not (r0_start < r0_boundary < divider < clay_start < cb19 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-common-adjoint-screen-boundary"' not in literature or "CB.19 · ClayB-CommonAdjointScreen-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.19 · {DISPLAY_ID}" not in index or "19 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.19" or site.get("nextIndependentChapter") != "CB.20":
        raise RuntimeError("version or chapter metadata drift")
    if manifest.get("latestCompletedRelease") != "r076l" or site.get("latestRelease") != "R0.76L":
        raise RuntimeError("canonical R0 endpoint drift")
    expected = handoff_bytes()
    path = ROOT / "release/handoffs/clay-b-common-adjoint-screen-20260906.json"
    if not path.is_file() or path.read_bytes() != expected:
        raise RuntimeError("publication handoff drift")


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
    (ROOT / "release/handoffs/clay-b-common-adjoint-screen-20260906.json").write_bytes(handoff_bytes())

validate()
print(json.dumps({"schemaVersion": "clay-b-common-adjoint-screen-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.19", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
