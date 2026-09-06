#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB EnergyAtomCostScreen CB.18 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.62"
SLUG = "clay-b-energy-atom-cost-screen-20260906"
DISPLAY_ID = "ClayB-EnergyAtomCostScreen-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_SECTIONS = [
    ("01 / 结果地图", "有定量代价，但没有形成矛盾", '<div class="grid"><div class="card"><strong class="proved">CONDITIONAL NECESSITY</strong>假设同一固定周期 NS 原解的终端能量测度在 x₀ 有质量 m&gt;0 的原子，最后阈值窗口给出有序半径—时间约束。</div><div class="card"><strong class="proved">SIGNED FLUX</strong>完整局部能量平衡保留规范压力、输运、黏性截止和局部耗散，得到 N_r≥m/8+D_(χ,r)。</div><div class="card"><strong class="open">GLOBAL TAIL COST</strong>D_r≥c m^(5/4)E^(-3/4)r^(1/2) 仍趋于零；嵌套尾积分不可相加，因此没有有限总耗散矛盾。</div></div><p>这既不是能量原子存在或排除定理，也不是局部耗散下界、最佳幂率、一般正则性或 Clay 结果。</p>'),
    ("02 / BO.1–BO.4", "最后阈值时刻保留正确的半径与时间量词", '<p>对径向非增截止 χ_r，记 q_r(t)=∫χ_r|u(t)|²。充分小的每个 r 各自取最后一次 q_r(t_r)=m/2，并令 δ_r=T_*−t_r、D_r=∫_(t_r)^(T_*)||∇u||²₂。</p><div class="equation">r₁&lt;r₂ ⇒ t_(r₁)≥t_(r₂), δ_(r₁)≤δ_(r₂), D_(r₁)≤D_(r₂);\nδ_r→0, D_r→0.                                      (BO.3–BO.4)</div><p>最后阈值之后整个窗口保持 q_r(t)&gt;m/2；没有一个同时适用于所有半径的公共时间窗。</p>'),
    ("03 / BO.5–BO.7", "原子不提供抛物宽度", '<p>固定环面的非齐次 Sobolev 与局部质量下界给整个终端窗口上的全环面梯度下界：</p><div class="equation">G(t)≥c m/r²,\nD_r≥c m δ_r/r²,\nδ_r/r²→0.                                           (BO.5–BO.7)</div><p>这不是局部加权梯度下界。正原子迫使最后阈值窗口严格短于抛物时间 r²，并未产生矛盾；非负可积梯度函数也可以在终点趋于无穷。</p>'),
    ("04 / BO.8–BO.13", "完整带符号局部平衡给出正净通量", '<p>先固定半径、对光滑原解使用局部能量等式，再趋向终点。规范压力的近源、平滑周期修正与远源全部保留；换压力代表不改变净通量。</p><div class="equation">q_r^*/2 − m/4 + D_(χ,r) = V_r + N_r,\nN_r≥m/8+D_(χ,r)&gt;0.                                (BO.8–BO.11)</div><p>输运与压力一起用周期 Calderón–Zygmund、Gagliardo–Nirenberg 和时间 Hölder 控制。这沿用既有 V 稿机制，不宣称新方法。</p>'),
    ("05 / BO.14–BO.16", "四次关系夹住窗口，但尾耗散成本仍然趋零", '<div class="equation">δ_r D_r³ ≥ c m⁴E^(-3)r⁴,\nr⁴=o(δ_r),  δ_r=o(r²),\nD_r≥c m^(5/4)E^(-3/4)r^(1/2).                     (BO.14–BO.16)</div><p>这里 D_r 是全环面终端尾耗散，D_(χ,r) 才是截止局部耗散；二者不能偷换。常数和“充分小”的尺度可依赖原解、m、E 与固定截止，没有给出初值统一可计算半径。</p>'),
    ("06 / BO.17–BO.18", "嵌套窗口不能重复计费，指数配合只证明代数相容", '<p>dyadic 形式的 ∑r_j^(1/2) 本身可和，而真实 D_(r_j) 又是嵌套尾积分。不能把它们当作互不相交的耗散成本，也不能从两个尾积分的下界相减出环带成本。</p><div class="equation">δ≈r^(5/2), D≈r^(1/2) ⇒ δ/r²≈r^(1/2), δD³≈r⁴.  (BO.18)</div><p>这一配合只核对必要不等式可同时满足，不是 NS 解、原子模型、实现性证明或最优率。</p>'),
    ("07 / 原始来源与未审接口", "压力稿已全文读，full-tail 的共同伴随核心仍未完成", '<p>本轮定向复核 Leslie–Shvydkoy 终端能量测度，并完整读取 Huang 压力预印本 arXiv:2608.30715v1 的 17 页；其 FGT、Nash、Hardy–BMO、周期交换子等外部依赖未全部重审，因此不把整篇升级为本项目已证定理。</p><p>Huang full-tail 预印本 arXiv:2608.04138v1 目前只读取 1–7 页。Theorem 2.3 的 packet、共同伴随、full-tail 饱和及延迟二阶障碍的核心证明仍待研究；不得写成已证。两篇早已登记，不称新发现，也没有外部同行评审或穷尽性新颖性结论。</p>'),
    ("08 / 证据、边界与下一步", "下一章只核查同一原解的共同伴随结构", '<p>下一研发动作完整阅读 full-tail 稿 §§3–6 及必要依赖，核查冻结 Hodge 球、gap-two thinning、同一原时间与同一 NS 漂移、共同伴随提取、终端集中、Cauchy 饱和及整个有序时间三角上的一致性。只有这一结构通过，才检查 §7 的延迟二阶障碍。</p><p class="note">科学源提交：7567e791fa3170bc71551c817cecc50b663d4d65；冻结提交：ccad47d0ed3549d1d1bf75d9b18ace5647fd1d96。六份本轮文件、109 份依赖和一份冻结 manifest 由 SHA-256 绑定；三份文本源、18 个 BO 标签、18 项精确算术检查与 3 项有限负对照通过。内部模型复核不是外部同行评审。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_energy_atom_dissipation_20260906.md">BO 原子耗散正文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_energy_atom_primary_reading_20260906.md">原始来源范围</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_energy_atom_report_20260906.md">阶段报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_energy_atom_cost_screen_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap；不分发第三方 PDF。G OPEN / NOT CLAY。</strong></p>'),
]

EN_SECTIONS = [
    ("01 / Result map", "There is a quantitative cost, but no contradiction", '<div class="grid"><div class="card"><strong class="proved">CONDITIONAL NECESSITY</strong>Assume the terminal energy measure of the same fixed periodic NS solution has an atom of mass m&gt;0 at x₀. Last-threshold windows then provide ordered radius–time constraints.</div><div class="card"><strong class="proved">SIGNED FLUX</strong>The complete local energy balance retains canonical pressure, transport, the viscous cutoff, and local dissipation, giving N_r≥m/8+D_(χ,r).</div><div class="card"><strong class="open">GLOBAL TAIL COST</strong>D_r≥c m^(5/4)E^(-3/4)r^(1/2) still tends to zero. Nested tail integrals cannot be added, so finite total dissipation is not contradicted.</div></div><p>This is neither an atom-existence nor atom-exclusion theorem, and it is not a local dissipation lower bound, optimal-rate claim, general regularity result, or Clay result.</p>'),
    ("02 / BO.1–BO.4", "Last-threshold times preserve the correct radius and time quantifiers", '<p>For a radial nonincreasing cutoff χ_r, set q_r(t)=∫χ_r|u(t)|². For every sufficiently small r separately, choose the last time q_r(t_r)=m/2 and define δ_r=T_*−t_r and D_r=∫_(t_r)^(T_*)||∇u||²₂.</p><div class="equation">r₁&lt;r₂ ⇒ t_(r₁)≥t_(r₂), δ_(r₁)≤δ_(r₂), D_(r₁)≤D_(r₂);\nδ_r→0, D_r→0.                                      (BO.3–BO.4)</div><p>The local energy stays above m/2 throughout the final interval after t_r. There is no single time window common to all radii.</p>'),
    ("03 / BO.5–BO.7", "An atom does not provide parabolic width", '<p>The inhomogeneous Sobolev inequality on the fixed torus and the local mass lower bound imply a whole-torus gradient lower bound throughout the terminal window:</p><div class="equation">G(t)≥c m/r²,\nD_r≥c m δ_r/r²,\nδ_r/r²→0.                                           (BO.5–BO.7)</div><p>This is not a localized weighted-gradient lower bound. A positive atom forces the last-threshold window to be strictly shorter than parabolic time r², but creates no contradiction. A nonnegative integrable gradient function may diverge at the endpoint.</p>'),
    ("04 / BO.8–BO.13", "The complete signed local balance yields a positive net flux", '<p>Fix the radius first, use local energy equality for the smooth solution, then approach the endpoint. The near source, smooth periodic correction, and far source of canonical pressure all remain. Changing the pressure representative leaves the net flux unchanged.</p><div class="equation">q_r^*/2 − m/4 + D_(χ,r) = V_r + N_r,\nN_r≥m/8+D_(χ,r)&gt;0.                                (BO.8–BO.11)</div><p>Transport and pressure are controlled together using periodic Calderón–Zygmund, Gagliardo–Nirenberg, and time Hölder estimates. This reuses the existing V mechanism and is not claimed as a new method.</p>'),
    ("05 / BO.14–BO.16", "A quartic relation squeezes the window, while the tail-dissipation cost still vanishes", '<div class="equation">δ_r D_r³ ≥ c m⁴E^(-3)r⁴,\nr⁴=o(δ_r),  δ_r=o(r²),\nD_r≥c m^(5/4)E^(-3/4)r^(1/2).                     (BO.14–BO.16)</div><p>Here D_r is whole-torus terminal tail dissipation; D_(χ,r) is localized cutoff dissipation. They cannot be interchanged. Constants and the sufficiently-small scale may depend on the solution, m, E, and the fixed cutoff; no initial-data-uniform computable radius is obtained.</p>'),
    ("06 / BO.17–BO.18", "Nested windows cannot be charged repeatedly; the exponent pair proves only algebraic compatibility", '<p>The dyadic formal series ∑r_j^(1/2) is summable, and the actual D_(r_j) are nested tail integrals. They cannot be treated as disjoint dissipation costs, nor can lower bounds for two tails be subtracted to lower-bound an annular cost.</p><div class="equation">δ≈r^(5/2), D≈r^(1/2) ⇒ δ/r²≈r^(1/2), δD³≈r⁴.  (BO.18)</div><p>This pair only checks that the necessary inequalities can hold simultaneously. It is not an NS solution, atom model, realizability proof, or optimal rate.</p>'),
    ("07 / Primary sources and unaudited interfaces", "The pressure paper was read in full; the common-adjoint core of the full-tail paper remains incomplete", '<p>This round rereads the Leslie–Shvydkoy terminal energy measure and all 17 pages of Huang\'s pressure preprint arXiv:2608.30715v1. Its external FGT, Nash, Hardy–BMO, periodic-commutator, and other dependencies were not all reaudited, so the full paper is not promoted to a project-proved theorem.</p><p>Only pages 1–7 of Huang\'s full-tail preprint arXiv:2608.04138v1 have been read. The core proofs for the packets, common adjoint, full-tail saturation, and delayed second-order obstruction behind Theorem 2.3 remain research work and must not be stated as proved. Both preprints were already registered; neither is presented as newly discovered, externally peer-reviewed, or exhaustively novelty-audited.</p>'),
    ("08 / Evidence, boundary, and next step", "The next chapter audits only the common-adjoint structure for one original solution", '<p>The next research action reads full-tail §§3–6 and required dependencies, checking frozen Hodge balls, gap-two thinning, the same original time and NS drift, common-adjoint extraction, terminal concentration, Cauchy saturation, and uniformity on the entire ordered-time triangle. Section 7\'s delayed second-order obstruction is considered only if this structure passes.</p><p class="note">Scientific source commit: 7567e791fa3170bc71551c817cecc50b663d4d65; freeze commit: ccad47d0ed3549d1d1bf75d9b18ace5647fd1d96. Six current files, 109 dependencies, and one frozen manifest are SHA-256-bound. Three text sources, 18 BO labels, 18 exact arithmetic checks, and three limited negative controls pass. Internal model review is not external peer review.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_energy_atom_dissipation_20260906.md">BO atom-dissipation source</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_energy_atom_primary_reading_20260906.md">primary-source scope</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_energy_atom_report_20260906.md">stage report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_energy_atom_cost_screen_frozen_ledger_20260906.json">portable ledger</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap and redistributes no third-party PDF. G OPEN / NOT CLAY.</strong></p>'),
]


def main_block(lang: str, sections: list[tuple[str, str, str]]) -> str:
    if lang == "zh":
        kicker, title = "CB.18 · 独立 Clay-B 方法笔记 · 2026-09-06", "CB.18｜终端能量原子的耗散成本：最后阈值窗口"
        dek = "假设同一固定周期 NS 原解具有正终端能量原子，最后阈值窗口、完整带符号局部能量平衡和周期压力估计给出 r⁴=o(δ_r)、δ_r=o(r²) 及 D_r≥c m^(5/4)E^(-3/4)r^(1/2)。该成本趋零，且窗口嵌套，因而没有形成有限总耗散矛盾。"
        footer = "独立 HTML 研究笔记"
    else:
        kicker, title = "CB.18 · Independent Clay-B methods note · 2026-09-06", "CB.18 | Dissipation cost of a terminal energy atom: the last-threshold window"
        dek = "Assuming that the same fixed periodic NS solution has a positive terminal energy atom, last-threshold windows, the complete signed local energy balance, and periodic pressure estimates yield r⁴=o(δ_r), δ_r=o(r²), and D_r≥c m^(5/4)E^(-3/4)r^(1/2). The cost vanishes and the windows are nested, so finite total dissipation is not contradicted."
        footer = "Independent HTML research note"
    body = "".join(f'<section><div class="section-no">{n}</div><h2>{h}</h2>{c}</section>' for n, h, c in sections)
    return f'''  <main data-language="{lang}">
    <article><header class="hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="dek">{dek}</p><div class="meta"><span>PROVED IN STATED SCOPE</span><span>CONDITIONAL NECESSITY</span><span>SIGNED FLUX</span><span>GLOBAL TAIL COST</span><span>ALGEBRAIC COMPATIBILITY</span><span>FINITE CHECKS ONLY</span><span>G OPEN · NOT CLAY</span></div></header>{body}</article>
    <footer class="footer">CB.18 · {footer} · {DISPLAY_ID} · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-energy-atom-cost-screen" aria-labelledby="clay-b-energy-atom-cost-screen-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.18 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · ENERGY-ATOM COST SCREEN</p><h2 class="route-map-title" id="clay-b-energy-atom-cost-screen-title">CB.18｜终端能量原子的耗散成本：最后阈值窗口</h2><p class="route-map-intro">在同一固定原解具有正终端能量原子的条件分支中，最后阈值窗口与完整带符号局部平衡给出严格次抛物宽度和 r^(1/2) 全局尾耗散成本。但该成本趋零，窗口又相互嵌套，不能重复计费，因此没有形成有限总耗散矛盾。G OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 终端能量原子成本笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-energy-atom-cost-screen-20260906.html">阅读最新 CB.18 原子成本笔记 →</a><a href="/literature-review.html#clay-b-energy-atom-cost-screen-boundary">查看原始来源与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 原子耗散成本筛查结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>最后阈值与正带符号净通量成立</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>趋零成本不产生耗散矛盾</span><span><i class="route-legend-mark current" aria-hidden="true"></i>原子存在/排除与一般正则性 OPEN · NOT CLAY</span></div></div></section>'''

CB18_ROW = '''          <div class="tree-row clay-b-energy-atom-cost-screen-row">
            <article class="tree-node current"><div class="tree-node-head"><span class="route-range">CB.18 · 2026-09-06 · BO ENERGY-ATOM COST SCREEN</span><span class="tree-state current">当前路线边界</span></div><h3>CB.18｜终端能量原子的耗散成本：最后阈值窗口</h3><p>BO 在同一固定周期 NS 原解具有质量 m 的正终端能量原子这一额外条件下，构造有序最后阈值窗口，保留完整规范压力、输运、黏性截止和局部耗散，得到 N_r≥m/8+D_(χ,r)。</p><p>必要约束为 r⁴=o(δ_r)、δ_r=o(r²) 及 D_r≥c m^(5/4)E^(-3/4)r^(1/2)。成本趋零且尾窗口嵌套，不能相加或由下界相减，所以本次没有产生有限总耗散矛盾。</p><p class="tree-path"><a href="/notes/clay-b-energy-atom-cost-screen-20260906.html">阅读 CB.18 HTML</a> · <a href="/literature-review.html#clay-b-energy-atom-cost-screen-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发动作：共同伴随结构核查</h3><p>完整阅读 full-tail 稿 §§3–6，核对冻结 Hodge 球、同一 NS 漂移、共同伴随提取、终端集中及整个有序时间三角上的统一性；§7 二阶障碍仍未进入已证范围。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.19 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.18</h3><p>CB.19 只是下一章占位，不是已完成研究。full-tail 共同伴随核心、延迟二阶算子预算、原子存在或排除、G、任意奇点输入生成、一般正则性与 Clay 均未关闭。</p></article></div>'''

LITERATURE_BLOCK = '''<h3 id="clay-b-energy-atom-cost-screen-boundary">CB.18 · Clay-B 终端能量原子耗散成本的文献和主张边界</h3><p>本轮定向复核 <a href="https://arxiv.org/abs/1705.04420v4">Leslie–Shvydkoy 终端能量测度</a>；完整读取 <a href="https://arxiv.org/abs/2608.30715v1">Huang 压力预印本 2608.30715v1</a> 全 17 页，但 FGT、Nash、Hardy–BMO 与周期交换子等外部依赖未全部重审；<a href="https://arxiv.org/abs/2608.04138v1">Huang full-tail 预印本 2608.04138v1</a> 只读取 1–7 页，Theorem 2.3 的共同伴随核心与 §§3–7 完整证明仍待核查。两稿此前已登记，不称新发现；没有穷尽文献、完成 Deep Research、新颖性审查或外部同行评审。</p><div class="boundary"><strong>CB.18 · ClayB-EnergyAtomCostScreen-20260906 公开边界</strong><p>CONDITIONAL NECESSITY：假设同一固定周期 NS 原解终端有质量 m 的正能量原子，最后阈值窗口满足 r⁴=o(δ_r)、δ_r=o(r²)。SIGNED FLUX：完整带符号局部平衡给 N_r≥m/8+D_(χ,r)。GLOBAL TAIL COST：D_r≥c m^(5/4)E^(-3/4)r^(1/2)，但这是趋零的全局尾耗散成本，不是局部耗散下界。ALGEBRAIC COMPATIBILITY：δ≈r^(5/2)、D≈r^(1/2) 只证明必要不等式相容，不是 NS 实现或最优率。嵌套窗口不能相加或由尾积分下界相减；本次没有有限总耗散矛盾。FINITE CHECKS ONLY：三份文本源、18 个 BO 标签、115/115 文件绑定、18 项精确算术检查和 3 项有限负对照不替代 PDE 证明。原子存在/排除、共同伴随核心、二阶算子预算、G、一般正则性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。<a href="/notes/clay-b-energy-atom-cost-screen-20260906.html">阅读完整 CB.18 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-euler-compactness-screen-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>终端能量原子的耗散成本：最后阈值窗口</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 终端能量原子、最后阈值窗口、带符号局部通量和全局尾耗散成本的双语方法笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.18 · {DISPLAY_ID}</strong></header>', template, count=1)
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
    value = value.replace("CB.1–CB.17", "CB.1–CB.18")
    value = value.replace("critical Euler compactness / energy-atom screen", "terminal energy atom / dissipation-cost screen", 1)
    old_focus = "Clay-B 已完成临界 Euler 紧性筛查：额外局部速度预算可删去独立压力输入，并导出条件性终端能量原子；但宽 Euler 类全零刚性已被文献反例排除，强 L^(11/3) 无原子端点仍是额外条件。下一步只测试原子与总耗散的关系。"
    new_focus = "Clay-B 已完成终端能量原子的直接耗散成本测试：最后阈值窗口和完整带符号局部平衡给出严格次抛物宽度及 r^(1/2) 全局尾成本，但成本趋零且窗口嵌套，本次没有形成有限总耗散矛盾。下一步只核查 full-tail 的共同伴随结构。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    if 'class="tree-row clay-b-energy-atom-cost-screen-row"' in value:
        return value
    cb17_start = value.index('<div class="tree-row clay-b-euler-compactness-screen-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb17_start)
    cb17 = value[cb17_start:boundary_start]
    cb17 = cb17.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb17 = cb17.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb17, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">ENERGY-ATOM COST SCREEN COMPLETED</span><h3>原子—耗散测试已进入 CB.18</h3><p>BO 已核对最后阈值、完整带符号通量、全局尾耗散成本及嵌套窗口不可重复计费；结果见下一个正式路线节点。</p></aside>', cb17, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.17 branch drift")
    value = value[:cb17_start] + cb17 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB18_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-energy-atom-cost-screen-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 18
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.18"
    payload["nextIndependentChapter"] = "CB.19"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note",
            "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.18",
            "sourceCommit": "7567e791fa3170bc71551c817cecc50b663d4d65", "baseCommit": "11f6e30c0f181d9b590303e47d41f902b3046009",
            "handoffCommit": "ccad47d0ed3549d1d1bf75d9b18ace5647fd1d96", "logicalPredecessor": "ClayB-EulerCompactnessScreen-20260906",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False, "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-energy-atom-cost-screen-20260906-gate.test.mjs", "publicationTest": "tests/clay-b-energy-atom-cost-screen-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-energy-atom-cost-screen-20260906-translations.mjs", "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE", "simulationRequired": False, "recapRequired": False,
            "advancesCanonicalR0Series": False, "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "CONDITIONAL_POSITIVE_TERMINAL_ENERGY_ATOM_GIVES_ORDERED_LAST_THRESHOLD_WINDOWS_POSITIVE_SIGNED_LOCAL_FLUX_SUBPARABOLIC_WIDTH_AND_VANISHING_GLOBAL_TAIL_DISSIPATION_COST_NESTED_WINDOWS_NOT_DISJOINT_NO_FINITE_DISSIPATION_CONTRADICTION_NO_ATOM_EXISTENCE_OR_EXCLUSION_COMMON_ADJOINT_CORE_UNREAD_GENERAL_REGULARITY_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def handoff_bytes() -> bytes:
    ledger = json.loads((ROOT / "research/clay_b_energy_atom_cost_screen_frozen_ledger_20260906.json").read_text(encoding="utf-8"))
    qa = json.loads((ROOT / "release/qa/clay-b-energy-atom-cost-screen-20260906.json").read_text(encoding="utf-8"))
    artifacts = [{"path": r["path"], "sha256": r["sha256"], "role": "frozen-scientific-source" if r["role"] == "scientific-source" else "frozen-dependency", "commit": r["commit"]} for r in ledger["files"]]
    artifacts += [{"path": r["path"], "sha256": r["sha256"], "role": "frozen-release-manifest", "commit": r["commit"]} for r in ledger["handoffEnvelope"]]
    outputs = [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html", "public/notes/index.html", "public/site-version.json", "research/release-manifest.json", "VERSION"]
    support = ["research/clay_b_energy_atom_cost_screen_frozen_ledger_20260906.json", "release/handoffs/clay-b-energy-atom-cost-screen-20260906.json", "release/qa/clay-b-energy-atom-cost-screen-20260906.json", "scripts/import_clay_b_energy_atom_cost_screen_20260906_frozen.py", "scripts/generate_clay_b_energy_atom_cost_screen_20260906_release.py", "scripts/generate_note_index.py", "scripts/add-clay-b-energy-atom-cost-screen-20260906-translations.mjs", "tests/clay-b-energy-atom-cost-screen-20260906-gate.test.mjs", "tests/clay-b-energy-atom-cost-screen-20260906-release.test.mjs", "tests/release-publication-invariant.test.mjs", "translations/en.json", "public/i18n-en.js"]
    managed = list(dict.fromkeys(outputs + [r["path"] for r in artifacts] + support))
    payload = {
        "schemaVersion": "research-publication-handoff-v1", "releaseId": DISPLAY_ID, "frozenCommit": "ccad47d0ed3549d1d1bf75d9b18ace5647fd1d96", "sourceRepository": "navier-stokes-r074m", "translationRoute": "LOCAL_DIRECT_NO_DGX", "artifacts": artifacts,
        "artifactPolicy": {"readerPdf": "OMIT_NEW", "scientificFigure": "NOT_REQUIRED"},
        "claimBoundary": {"requiredLabels": ["PROVED", "FINITE", "CONDITIONAL NECESSITY", "SIGNED FLUX", "GLOBAL TAIL COST", "ALGEBRAIC COMPATIBILITY", "OPEN", "NOT CLAY"], "publicFiles": [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html"]},
        "recap": {"mode": "PRESERVE", "latestRecapRelease": "r076i", "preservedArtifacts": [{"path": "public/recap-r0-61-r0-76i.html", "sha256": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9"}, {"path": "public/recap-r0-61-r0-76i.pdf", "sha256": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98"}]},
        "stages": {"generate": {"runner": "python-local", "script": "scripts/generate_clay_b_energy_atom_cost_screen_20260906_release.py", "inputs": [r["path"] for r in artifacts] + ["research/clay_b_energy_atom_cost_screen_frozen_ledger_20260906.json"], "outputs": outputs}, "translate": {"runner": "node-local", "script": "scripts/add-clay-b-energy-atom-cost-screen-20260906-translations.mjs", "inputs": ["public/research-review.html", "public/literature-review.html", "public/notes/index.html", "translations/en.json"], "outputs": ["translations/en.json", "public/i18n-en.js"]}},
        "publication": {"expectedCommit": None, "siteBaseUrl": "https://kasifa.github.io", "repository": "Kasifa/Kasifa.github.io", "workflow": "pages.yml", "remote": "origin", "targetBranch": "main", "commitMessage": "Publish ClayB EnergyAtomCostScreen CB.18 HTML note", "managedPaths": managed, "expectedLive": qa["online"]["expectedLive"], "expectedAbsent": qa["online"]["expectedAbsent"], "siteVersionExpectations": qa["online"]["siteVersionExpectations"]},
        "visualQa": {"evidencePath": qa["browser"]["evidencePath"], "configPath": "release/qa/clay-b-energy-atom-cost-screen-20260906.json", "requiredChecks": [f"{t['id']}-{s['id']}" for t in qa["browser"]["targets"] for s in qa["browser"]["scenarios"]]},
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.18", DISPLAY_ID, "终端能量原子的耗散成本：最后阈值窗口", "Dissipation cost of a terminal energy atom: the last-threshold window", "PROVED IN STATED SCOPE", "CONDITIONAL NECESSITY", "SIGNED FLUX", "GLOBAL TAIL COST", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.18", "Clay-B 独立路线停在 CB.18", "CB.19 · NEXT", 'class="tree-row clay-b-energy-atom-cost-screen-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"'); r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start); divider = home.index('class="route-lane-divider"', r0_boundary); clay_start = home.index('class="route-tree clay-b-route-tree"', divider); cb18 = home.index('class="tree-row clay-b-energy-atom-cost-screen-row"', clay_start); clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb18)
    if not (r0_start < r0_boundary < divider < clay_start < cb18 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-energy-atom-cost-screen-boundary"' not in literature or "CB.18 · ClayB-EnergyAtomCostScreen-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.18 · {DISPLAY_ID}" not in index or "18 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8")); manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.18" or site.get("nextIndependentChapter") != "CB.19":
        raise RuntimeError("version or chapter metadata drift")
    if manifest.get("latestCompletedRelease") != "r076l" or site.get("latestRelease") != "R0.76L":
        raise RuntimeError("canonical R0 endpoint drift")
    expected = handoff_bytes(); path = ROOT / "release/handoffs/clay-b-energy-atom-cost-screen-20260906.json"
    if not path.is_file() or path.read_bytes() != expected:
        raise RuntimeError("publication handoff drift")


if not CHECK_ONLY:
    NOTE_PATH.write_text(build_note(), encoding="utf-8")
    home_path = ROOT / "public/research-review.html"; home_path.write_text(update_home(home_path.read_text(encoding="utf-8")), encoding="utf-8")
    literature_path = ROOT / "public/literature-review.html"; literature_path.write_text(update_literature(literature_path.read_text(encoding="utf-8")), encoding="utf-8")
    (ROOT / "VERSION").write_text(VERSION + "\n", encoding="utf-8")
    update_metadata(ROOT / "public/site-version.json"); update_metadata(ROOT / "research/release-manifest.json")
    subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    (ROOT / "release/handoffs/clay-b-energy-atom-cost-screen-20260906.json").write_bytes(handoff_bytes())

validate()
print(json.dumps({"schemaVersion": "clay-b-energy-atom-cost-screen-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.18", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
