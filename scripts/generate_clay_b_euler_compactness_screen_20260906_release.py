#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB EulerCompactnessScreen CB.17 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.61"
SLUG = "clay-b-euler-compactness-screen-20260906"
DISPLAY_ID = "ClayB-EulerCompactnessScreen-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_SECTIONS = [
    ("01 / 结果地图", "压力输入可以删去，刚性出口仍未成立", '<div class="grid"><div class="card"><strong class="proved">CONDITIONAL COMPACTNESS</strong>同一固定光滑周期 NS 历史若满足每个固定柱体上的局部无权梯度界及统一短窗 L³ 下界，则规范周期压力无需独立假设，并可抽取非零古老有限能量 Euler 极限。</div><div class="card"><strong class="open">LITERATURE OBSTRUCTION</strong>Gavrilov 已知紧支撑定常 Euler 流排除了宽目标类的全零刚性；它并非固定 NS 历史可达性的反例。</div><div class="card"><strong class="open">KNOWN-METHOD ENDPOINT</strong>额外强局部时空 L^(11/3) 可排除终端能量原子；基本能量的 L^(10/3) 不足以支付同一截止估计。</div></div><p>本章没有扩大任何已证明的三维 NS 正则解类。G、原解输入生成、带符号压力功上界和一般正则性继续开放。</p>'),
    ("02 / BK.1–BK.12", "缩放预检只界定可用窗口，不生成临界输入", '<p>能量单独使所选短窗三次质量在 β≥2/3 时消失；若另有明确写出的局部加权梯度控制，则 β&gt;1/2 时也消失。β=1/2 是能量保持边界，不等于梯度预算已经成立。</p><div class="equation">energy only: β ≥ 2/3 ⇒ short-window cubic mass → 0;\nweighted gradient input: β &gt; 1/2 ⇒ short-window cubic mass → 0.  (BK.1–BK.12)</div><p>六份早期 BK 阶段文件按原字节保留，其中旧的 PENDING 和 next-action 文字只是历史记录；本章 BL–BN 报告才是当前进展。</p>'),
    ("03 / BL.1–BL.20", "临界 Euler 缩放下，速度条件足以推出局部压力紧性", '<p>取 w_k=λ_k^(3/2)u(x_k+λ_ky,T_*+λ_k^(5/2)τ)、π_k=λ_k^3p，扩张周期 L_k=λ_k^(-1)，粘性 ν_k=λ_k^(1/2)。整胞 L² 能量来自同一原解；每个固定柱体的无权梯度界与统一短窗 L³ 下界是额外假设。</p><p>完整规范周期压力分解保留奇异 delta 乘法项、平滑周期修正和远源。由此得到局部 L^(5/3) 压力界、全短窗速度强 L³ 和压力强 L^(3/2) 收敛，极限为非零古老有限能量 Euler 解并满足局部能量等式。</p><p><strong>边界：</strong>压力输入只在这条条件性抽取中冗余；局部能量等式不是全局能量守恒。</p>'),
    ("04 / BM.1–BM.8", "宽 Euler 类非零；固定 NS 来源若实现 BL 则必须产生能量原子", '<p>Gavrilov 的已知光滑紧支撑定常 Euler 流属于宽目标类，因此“所有有限能量古老 Euler 解皆为零”不能作为出口。但该文献例并未证明从同一固定初值 NS 历史缩放可达。</p><div class="equation">c_* = ε_*^4 / V^3,\nterminal atom ≥ c_*/2 = ε_*^4/(2V^3).             (BM.4–BM.8)</div><p>这个原子下界来自原解唯一终端能量测度及插值，是 BL 假设若被同一原解实现时的条件必要性；不是能量原子存在定理，也没有使用强 L² 终端迹识别。</p>'),
    ("05 / BN.1–BN.8", "强 L^(11/3) 端点无原子，而能量指数仍留下负截止幂", '<p>若原解在该点固定邻域额外属于强局部时空 L^(11/3)，周期小球截止证明连同导出的 L^(11/6) 压力界排除终端能量原子。时间窗口宽度取 r^(5/2)，时间截止、非线性通量和粘性项的幂分别为 0、0、1/2。</p><div class="equation">strong L^(11/3): powers = 0, 0, 1/2;\nenergy L^(10/3): losses = -3/10, -9/20.          (BN.1–BN.8)</div><p>这是已知无原子机制在当前周期规范下的可审计重算，不是新颖性或一般正则性结论；积分趋零但没有速率，不能直接抵消负幂。</p>'),
    ("06 / 条件链与未付接口", "四个结果不能合并成一个无条件出口", '<table><thead><tr><th>环节</th><th>准确状态</th></tr></thead><tbody><tr><td>BL 速度输入</td><td>EXTRA：固定柱体梯度界与短窗 L³ 正下界尚未由任意候选奇点生成。</td></tr><tr><td>规范压力</td><td>在 BL 条件内可推出，不再作为独立输入。</td></tr><tr><td>BM 原子</td><td>同一原解若实现 BL，则终端原子是条件必要结论；未证明实际存在。</td></tr><tr><td>BN 无原子</td><td>需要额外强 L^(11/3)，基本能量不提供。</td></tr><tr><td>总体出口</td><td>G、BL.3 原解生成、带符号压力功上界、一般正则性均 OPEN。</td></tr></tbody></table>'),
    ("07 / 原始来源与主张边界", "有界原文核查改变策略，但没有完成穷尽性新颖性审查", '<p>本轮有界核对 Tao 的 Euclidean Calderón–Zygmund 讲义、Gavrilov 的紧支撑定常 Euler 存在性、Leslie–Shvydkoy 的终端能量测度以及 Shvydkoy 的能量集中条件。BL 的周期 Green 修正、Sobolev 小证明与短窗紧性在正文中给出；BN 直接在周期域重算。</p><p>两篇无原子文献的全空间假设、强弱端点与当前周期问题严格区分。Tao 工具与 Gavrilov 存在性是引用输入；没有穷尽全部文献、完成 Deep Research、新颖性审查或外部同行评审。</p>'),
    ("08 / 证据、边界与下一步", "下一章只测试正终端原子能否强迫不相容的耗散下界", '<p>下一研发动作从 BM 的终端能量测度出发，固定中心、原始时间、规范压力、全部截止项与有符号通量，检查正原子是否强迫与有限总耗散不相容的下界。不得预设持留宽度，也不得把嵌套窗口当作互不相交。</p><p class="note">科学源提交：14d5a44345c6835aff8dfd19123c979ae185b471；冻结提交：e22c9a5669dbc3cc29fa2e0d313d3656836774c2。十四份本轮文件、九十份依赖和一份冻结 manifest 由 SHA-256 绑定；五份文本源、BK–BN 共 48 个标签、20 项精确算术检查与 3 项有限负对照通过。内部模型复核不是外部同行评审。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_critical_euler_compactness_20260906.md">BL 条件紧性</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_euler_rigidity_energy_atom_20260906.md">BM 刚性与原子</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_periodic_no_atom_endpoint_20260906.md">BN 周期无原子端点</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_euler_compactness_screen_frozen_ledger_20260906.json">便携台账</a></p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap；不分发第三方 PDF。G OPEN / NOT CLAY。</strong></p>'),
]

EN_SECTIONS = [
    ("01 / Result map", "Pressure input can be removed; the rigidity exit is still unavailable", '<div class="grid"><div class="card"><strong class="proved">CONDITIONAL COMPACTNESS</strong>For one fixed smooth periodic NS history, local unweighted gradient bounds on every fixed cylinder plus a uniform short-window L³ lower bound make an independent canonical-pressure assumption unnecessary and yield a nonzero ancient finite-energy Euler limit.</div><div class="card"><strong class="open">LITERATURE OBSTRUCTION</strong>Gavrilov\'s known compactly supported steady Euler flow rules out all-zero rigidity for the broad target class; it is not a fixed-NS-history attainability counterexample.</div><div class="card"><strong class="open">KNOWN-METHOD ENDPOINT</strong>Additional strong local spacetime L^(11/3) excludes a terminal energy atom; the energy-level L^(10/3) does not pay the same cutoff estimate.</div></div><p>No proved three-dimensional NS regularity class is enlarged here. G, original-solution input generation, the signed pressure-work upper bound, and general regularity remain open.</p>'),
    ("02 / BK.1–BK.12", "The scaling precheck only identifies admissible windows; it does not generate critical input", '<p>Energy alone makes the selected short-window cubic mass vanish for β≥2/3. With the separately stated local weighted-gradient control it also vanishes for β&gt;1/2. The β=1/2 energy-preserving boundary does not establish the required gradient budget.</p><div class="equation">energy only: β ≥ 2/3 ⇒ short-window cubic mass → 0;\nweighted gradient input: β &gt; 1/2 ⇒ short-window cubic mass → 0.  (BK.1–BK.12)</div><p>Six earlier BK stage files remain byte-identical. Their old PENDING and next-action language is historical; the BL–BN report is the current progress record.</p>'),
    ("03 / BL.1–BL.20", "At critical Euler scaling, the velocity hypotheses imply local pressure compactness", '<p>Set w_k=λ_k^(3/2)u(x_k+λ_ky,T_*+λ_k^(5/2)τ), π_k=λ_k^3p, with expanding period L_k=λ_k^(-1) and viscosity ν_k=λ_k^(1/2). Whole-cell L² energy comes from the same original solution. Local unweighted gradient bounds on every fixed cylinder and a uniform short-window L³ lower bound are extra assumptions.</p><p>The complete canonical periodic-pressure decomposition retains the singular delta multiplier, smooth periodic correction, and far source. It yields local L^(5/3) pressure control, strong L³ velocity convergence on the full short window, and strong local L^(3/2) pressure convergence. The limit is nonzero, ancient, finite-energy Euler and obeys local energy equality.</p><p><strong>Boundary:</strong> pressure is redundant only within this conditional extraction; local energy equality is not global energy conservation.</p>'),
    ("04 / BM.1–BM.8", "The broad Euler class is nonzero; realization by one fixed NS source would force an energy atom", '<p>Gavrilov\'s known smooth compactly supported steady Euler flow belongs to the broad target class, so an all-zero theorem for that class is false. The literature example has not been shown attainable by rescaling one fixed-data NS history.</p><div class="equation">c_* = ε_*^4 / V^3,\nterminal atom ≥ c_*/2 = ε_*^4/(2V^3).             (BM.4–BM.8)</div><p>The bound uses the original solution\'s unique terminal energy measure and interpolation. It is a conditional necessity if the same source realizes the BL assumptions, not a proof that an atom exists; no strong L² terminal-trace identification is used.</p>'),
    ("05 / BN.1–BN.8", "Strong L^(11/3) is atom-free, while the energy exponent leaves negative cutoff powers", '<p>If the original solution additionally lies in strong local spacetime L^(11/3) near the point, a periodic small-ball cutoff proof, with derived L^(11/6) pressure, excludes a terminal energy atom. With time width r^(5/2), the time-cutoff, nonlinear-flux, and viscous powers are 0, 0, and 1/2.</p><div class="equation">strong L^(11/3): powers = 0, 0, 1/2;\nenergy L^(10/3): losses = -3/10, -9/20.          (BN.1–BN.8)</div><p>This is an auditable periodic rederivation of a known no-atom mechanism, not a novelty or general-regularity result. Mere integral decay without a rate cannot cancel the negative powers.</p>'),
    ("06 / Conditional chain and unpaid interfaces", "The four results do not compose into an unconditional exit", '<table><thead><tr><th>Link</th><th>Exact status</th></tr></thead><tbody><tr><td>BL velocity inputs</td><td>EXTRA: fixed-cylinder gradient bounds and a short-window positive L³ lower bound are not generated for arbitrary candidate singularities.</td></tr><tr><td>Canonical pressure</td><td>Derived within the BL assumptions; no separate pressure input is needed there.</td></tr><tr><td>BM atom</td><td>A conditional necessity if one original solution realizes BL; actual existence is not proved.</td></tr><tr><td>BN no atom</td><td>Requires additional strong L^(11/3), unavailable from basic energy.</td></tr><tr><td>Overall exit</td><td>G, BL.3 source generation, signed pressure-work control, and general regularity remain OPEN.</td></tr></tbody></table>'),
    ("07 / Primary sources and claim boundary", "Bounded source reading changed the strategy but did not complete an exhaustive novelty audit", '<p>The bounded review covers Tao\'s Euclidean Calderón–Zygmund notes, Gavrilov\'s compactly supported steady Euler existence result, Leslie–Shvydkoy on terminal energy measures, and Shvydkoy on energy-concentration conditions. BL supplies its periodic Green correction, short Sobolev proof, and full-window compactness directly; BN is recomputed on the periodic domain.</p><p>The whole-space hypotheses and strong/weak endpoints in the no-atom literature are kept separate from the present periodic problem. Tao\'s tool and Gavrilov\'s existence theorem are cited inputs. No exhaustive literature search, completed Deep Research, novelty claim, or external peer review is asserted.</p>'),
    ("08 / Evidence, boundary, and next step", "The next chapter only tests whether a positive terminal atom forces an incompatible dissipation lower bound", '<p>The next research action starts from BM\'s terminal energy measure and keeps fixed centers, original time, canonical pressure, every cutoff term, and signed flux. It tests whether a positive atom forces a lower dissipation cost incompatible with finite total dissipation. No persistence width may be assumed, and nested windows may not be counted as disjoint.</p><p class="note">Scientific source commit: 14d5a44345c6835aff8dfd19123c979ae185b471; freeze commit: e22c9a5669dbc3cc29fa2e0d313d3656836774c2. Fourteen current files, ninety dependencies, and one frozen manifest are SHA-256-bound. Five text sources, 48 BK–BN labels, 20 exact arithmetic checks, and three limited negative controls pass. Internal model review is not external peer review.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_critical_euler_compactness_20260906.md">BL conditional compactness</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_euler_rigidity_energy_atom_20260906.md">BM rigidity and atom</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_periodic_no_atom_endpoint_20260906.md">BN periodic no-atom endpoint</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_euler_compactness_screen_frozen_ledger_20260906.json">portable ledger</a></p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap and redistributes no third-party PDF. G OPEN / NOT CLAY.</strong></p>'),
]


def main_block(lang: str, sections: list[tuple[str, str, str]]) -> str:
    if lang == "zh":
        kicker = "CB.17 · 独立 Clay-B 方法笔记 · 2026-09-06"
        title = "CB.17｜临界 Euler 紧性：压力输入、能量原子与无原子端点"
        dek = "在明确的局部速度假设下，规范周期压力无需独立输入，并可抽取非零古老有限能量 Euler 极限；但宽 Euler 类已有非零定常例。若同一固定 NS 历史实现这些假设，则终端能量原子成为必要条件，而额外强 L^(11/3) 又触发已知无原子机制。两端尚未由基本能量接上。"
        footer = "独立 HTML 研究笔记"
    else:
        kicker = "CB.17 · Independent Clay-B methods note · 2026-09-06"
        title = "CB.17 | Critical Euler compactness: pressure input, energy atoms, and a no-atom endpoint"
        dek = "Under explicit local velocity hypotheses, canonical periodic pressure needs no independent input and one can extract a nonzero ancient finite-energy Euler limit. Yet the broad Euler class already contains nonzero steady examples. If one fixed NS history realizes the hypotheses, a terminal energy atom is necessary, while additional strong L^(11/3) activates a known no-atom mechanism. Basic energy has not connected the two ends."
        footer = "Independent HTML research note"
    body = "".join(f'<section><div class="section-no">{number}</div><h2>{heading}</h2>{content}</section>' for number, heading, content in sections)
    return f'''  <main data-language="{lang}">
    <article><header class="hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="dek">{dek}</p><div class="meta"><span>PROVED IN STATED SCOPE</span><span>CONDITIONAL COMPACTNESS</span><span>LITERATURE OBSTRUCTION</span><span>CONDITIONAL ATOM</span><span>KNOWN-METHOD ENDPOINT</span><span>FINITE CHECKS ONLY</span><span>G OPEN · NOT CLAY</span></div></header>{body}</article>
    <footer class="footer">CB.17 · {footer} · {DISPLAY_ID} · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-euler-compactness-screen" aria-labelledby="clay-b-euler-compactness-screen-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.17 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · EULER COMPACTNESS SCREEN</p><h2 class="route-map-title" id="clay-b-euler-compactness-screen-title">CB.17｜临界 Euler 紧性：压力输入、能量原子与无原子端点</h2><p class="route-map-intro">明确的局部速度预算足以推出规范压力紧性和非零古老有限能量 Euler 极限，但宽 Euler 类已有非零定常反例。同一固定 NS 来源若实现该分支，终端能量原子成为条件必要结论；额外强 L^(11/3) 又给已知无原子端点。基本能量尚未接通两端。G OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 临界 Euler 紧性笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-euler-compactness-screen-20260906.html">阅读最新 CB.17 临界紧性笔记 →</a><a href="/literature-review.html#clay-b-euler-compactness-screen-boundary">查看原始来源与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 临界紧性筛查结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>条件内压力输入可删</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>宽 Euler 全零刚性被文献反例排除</span><span><i class="route-legend-mark current" aria-hidden="true"></i>原解输入生成与一般正则性 OPEN · NOT CLAY</span></div></div></section>'''

CB17_ROW = '''          <div class="tree-row clay-b-euler-compactness-screen-row">
            <article class="tree-node current"><div class="tree-node-head"><span class="route-range">CB.17 · 2026-09-06 · BK–BN EULER COMPACTNESS SCREEN</span><span class="tree-state current">当前路线边界</span></div><h3>CB.17｜临界 Euler 紧性：压力输入、能量原子与无原子端点</h3><p>BK 界定缩放窗口；BL 在额外局部速度假设下推出完整规范压力紧性、全短窗强收敛及非零古老有限能量 Euler 极限，压力不再是独立输入。</p><p>BM 用 Gavrilov 已知定常流排除宽类全零刚性，并证明固定 NS 来源若实现 BL 就必须产生定量终端能量原子；BN 在额外强 L^(11/3) 下重算已知无原子端点。两端没有由基本能量自动接通。</p><p class="tree-path"><a href="/notes/clay-b-euler-compactness-screen-20260906.html">阅读 CB.17 HTML</a> · <a href="/literature-review.html#clay-b-euler-compactness-screen-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发动作：原子—耗散下界测试</h3><p>固定中心、原时钟、规范压力、全部截止项与有符号通量；不预设持留宽度，不把嵌套窗口当作互不相交，检查正终端原子是否强迫与有限总耗散不相容的成本。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.18 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.17</h3><p>CB.18 只是下一章占位，不是已完成研究。正终端能量原子是否强迫不相容的耗散下界尚未冻结；G、原解输入生成、带符号压力功上界、一般正则性与 Clay 均未关闭。</p></article></div>'''

LITERATURE_BLOCK = '''<h3 id="clay-b-euler-compactness-screen-boundary">CB.17 · Clay-B 临界 Euler 紧性的文献和主张边界</h3><p>本轮有界核查 <a href="https://www.math.ucla.edu/~tao/247a.1.06f/notes4.pdf">Tao Math 247A Notes 4</a> 与 <a href="https://www.math.ucla.edu/~tao/247a.1.06f/notes3.pdf">Notes 3</a> 的 Euclidean Calderón–Zygmund 工具；<a href="https://arxiv.org/abs/1810.08020v1">Gavrilov 的紧支撑定常 Euler 流</a>；<a href="https://arxiv.org/abs/1705.04420v4">Leslie–Shvydkoy 终端能量测度</a>及 <a href="https://arxiv.org/abs/1205.1544v2">Shvydkoy 能量集中条件</a>。周期 Green 修正、短窗紧性与 L^(11/3) 周期无原子端点在本章正文重算。引用工具与存在性结论没有全部重证；没有穷尽文献、完成 Deep Research、新颖性审查或外部同行评审。</p><div class="boundary"><strong>CB.17 · ClayB-EulerCompactnessScreen-20260906 公开边界</strong><p>CONDITIONAL COMPACTNESS：额外局部梯度界与短窗 L³ 下界推出规范压力局部 L^(5/3)、速度强 L³、压力强 L^(3/2) 及非零古老有限能量 Euler 极限；仅在此条件内压力输入冗余。LITERATURE OBSTRUCTION：Gavrilov 已知定常流排除宽目标类全零刚性，但不是固定 NS 历史可达性反例。CONDITIONAL ATOM：同一原解若实现 BL，终端能量原子至少为 ε_*^4/(2V^3)，这不是原子存在证明。KNOWN-METHOD ENDPOINT：额外强 L^(11/3) 排原子；基本能量 L^(10/3) 留下 -3/10 与 -9/20 的负截止幂。FINITE CHECKS ONLY：五份文本源、BK–BN 共 48 个标签、104/104 文件绑定、20 项精确算术检查与 3 项有限负对照不替代 PDE 证明。G、原解输入生成、带符号压力功上界、一般正则性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。<a href="/notes/clay-b-euler-compactness-screen-20260906.html">阅读完整 CB.17 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-fixed-history-screen-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>临界 Euler 紧性：压力输入、能量原子与无原子端点</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 临界 Euler 紧性、规范压力、终端能量原子与强 L11/3 无原子端点的双语方法笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.17 · {DISPLAY_ID}</strong></header>', template, count=1)
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
    value = value.replace("CB.1–CB.16", "CB.1–CB.17")
    value = value.replace("fixed-data history / growing-window tail screen", "critical Euler compactness / energy-atom screen", 1)
    old_focus = "Clay-B 已完成固定初值完整历史预检：原解能量支付增长窗口之外的旧非线性尾，但没有固定窗口控制；record 倍增账本只给下界而不自动给上界。下一研发动作转为阶段策略复评，G/Q 与一般正则性继续开放。"
    new_focus = "Clay-B 已完成临界 Euler 紧性筛查：额外局部速度预算可删去独立压力输入，并导出条件性终端能量原子；但宽 Euler 类全零刚性已被文献反例排除，强 L^(11/3) 无原子端点仍是额外条件。下一步只测试原子与总耗散的关系。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    if 'class="tree-row clay-b-euler-compactness-screen-row"' in value:
        return value
    cb16_start = value.index('<div class="tree-row clay-b-fixed-history-screen-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb16_start)
    cb16 = value[cb16_start:boundary_start]
    cb16 = cb16.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb16 = cb16.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb16, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">EULER COMPACTNESS SCREEN COMPLETED</span><h3>阶段复评已进入 CB.17</h3><p>BK–BN 已区分条件紧性、文献刚性障碍、原子必要条件与额外强端点；结果见下一个正式路线节点。</p></aside>', cb16, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.16 branch drift")
    value = value[:cb16_start] + cb16 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB17_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-euler-compactness-screen-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 17
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.17"
    payload["nextIndependentChapter"] = "CB.18"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1", "kind": "independent-analytic-note",
            "releaseId": SLUG, "displayReleaseId": DISPLAY_ID, "chapter": "CB.17",
            "sourceCommit": "14d5a44345c6835aff8dfd19123c979ae185b471", "baseCommit": "b85838c7139c7e6e248d3c1dfebd0866a92a166a",
            "handoffCommit": "e22c9a5669dbc3cc29fa2e0d313d3656836774c2", "logicalPredecessor": "ClayB-FixedHistoryScreen-20260906",
            "html": f"public/notes/{SLUG}.html", "pdfGenerated": False, "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-euler-compactness-screen-20260906-gate.test.mjs", "publicationTest": "tests/clay-b-euler-compactness-screen-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-euler-compactness-screen-20260906-translations.mjs", "browserQaScript": "scripts/qa-publication-browser.mjs", "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False, "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE", "simulationRequired": False, "recapRequired": False,
            "advancesCanonicalR0Series": False, "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "CONDITIONAL_LOCAL_VELOCITY_INPUTS_YIELD_CANONICAL_PRESSURE_COMPACTNESS_NONZERO_ANCIENT_FINITE_ENERGY_EULER_AND_LOCAL_ENERGY_EQUALITY_GAVRILOV_BLOCKS_BROAD_ZERO_RIGIDITY_FIXED_NS_ATTAINABILITY_UNPROVED_SAME_SOURCE_REALIZATION_FORCES_TERMINAL_ATOM_STRONG_L11_OVER_3_IS_EXTRA_NO_ATOM_ENDPOINT_G_SOURCE_GENERATION_PRESSURE_WORK_REGULARITY_OPEN_NOT_CLAY_NO_NOVELTY_CLAIM",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def handoff_bytes() -> bytes:
    ledger = json.loads((ROOT / "research/clay_b_euler_compactness_screen_frozen_ledger_20260906.json").read_text(encoding="utf-8"))
    qa = json.loads((ROOT / "release/qa/clay-b-euler-compactness-screen-20260906.json").read_text(encoding="utf-8"))
    artifacts = []
    for row in ledger["files"]:
        artifacts.append({
            "path": row["path"], "sha256": row["sha256"],
            "role": "frozen-scientific-source" if row["role"] == "scientific-source" else "frozen-dependency",
            "commit": row["commit"],
        })
    for row in ledger["handoffEnvelope"]:
        artifacts.append({"path": row["path"], "sha256": row["sha256"], "role": "frozen-release-manifest", "commit": row["commit"]})
    outputs = [
        f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html",
        "public/notes/index.html", "public/site-version.json", "research/release-manifest.json", "VERSION",
    ]
    support = [
        "research/clay_b_euler_compactness_screen_frozen_ledger_20260906.json",
        "release/handoffs/clay-b-euler-compactness-screen-20260906.json",
        "release/qa/clay-b-euler-compactness-screen-20260906.json",
        "scripts/import_clay_b_euler_compactness_screen_20260906_frozen.py",
        "scripts/generate_clay_b_euler_compactness_screen_20260906_release.py",
        "scripts/generate_note_index.py",
        "scripts/add-clay-b-euler-compactness-screen-20260906-translations.mjs",
        "tests/clay-b-euler-compactness-screen-20260906-gate.test.mjs",
        "tests/clay-b-euler-compactness-screen-20260906-release.test.mjs",
        "tests/release-publication-invariant.test.mjs", "translations/en.json", "public/i18n-en.js",
    ]
    managed = list(dict.fromkeys(outputs + [row["path"] for row in artifacts] + support))
    payload = {
        "schemaVersion": "research-publication-handoff-v1",
        "releaseId": DISPLAY_ID,
        "frozenCommit": "e22c9a5669dbc3cc29fa2e0d313d3656836774c2",
        "sourceRepository": "navier-stokes-r074m",
        "translationRoute": "LOCAL_DIRECT_NO_DGX",
        "artifacts": artifacts,
        "artifactPolicy": {"readerPdf": "OMIT_NEW", "scientificFigure": "NOT_REQUIRED"},
        "claimBoundary": {
            "requiredLabels": ["PROVED", "FINITE", "CONDITIONAL COMPACTNESS", "LITERATURE OBSTRUCTION", "CONDITIONAL ATOM", "KNOWN-METHOD ENDPOINT", "OPEN", "NOT CLAY"],
            "publicFiles": [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html"],
        },
        "recap": {
            "mode": "PRESERVE", "latestRecapRelease": "r076i",
            "preservedArtifacts": [
                {"path": "public/recap-r0-61-r0-76i.html", "sha256": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9"},
                {"path": "public/recap-r0-61-r0-76i.pdf", "sha256": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98"},
            ],
        },
        "stages": {
            "generate": {
                "runner": "python-local", "script": "scripts/generate_clay_b_euler_compactness_screen_20260906_release.py",
                "inputs": [row["path"] for row in artifacts] + ["research/clay_b_euler_compactness_screen_frozen_ledger_20260906.json"],
                "outputs": outputs,
            },
            "translate": {
                "runner": "node-local", "script": "scripts/add-clay-b-euler-compactness-screen-20260906-translations.mjs",
                "inputs": ["public/research-review.html", "public/literature-review.html", "public/notes/index.html", "translations/en.json"],
                "outputs": ["translations/en.json", "public/i18n-en.js"],
            },
        },
        "publication": {
            "expectedCommit": None, "siteBaseUrl": "https://kasifa.github.io", "repository": "Kasifa/Kasifa.github.io",
            "workflow": "pages.yml", "remote": "origin", "targetBranch": "main",
            "commitMessage": "Publish ClayB EulerCompactnessScreen CB.17 HTML note",
            "managedPaths": managed,
            "expectedLive": qa["online"]["expectedLive"], "expectedAbsent": qa["online"]["expectedAbsent"],
            "siteVersionExpectations": qa["online"]["siteVersionExpectations"],
        },
        "visualQa": {
            "evidencePath": qa["browser"]["evidencePath"],
            "configPath": "release/qa/clay-b-euler-compactness-screen-20260906.json",
            "requiredChecks": [f"{target['id']}-{scenario['id']}" for target in qa["browser"]["targets"] for scenario in qa["browser"]["scenarios"]],
        },
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.17", DISPLAY_ID, "临界 Euler 紧性：压力输入、能量原子与无原子端点", "Critical Euler compactness: pressure input, energy atoms, and a no-atom endpoint", "CONDITIONAL COMPACTNESS", "LITERATURE OBSTRUCTION", "CONDITIONAL ATOM", "KNOWN-METHOD ENDPOINT", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.17", "Clay-B 独立路线停在 CB.17", "CB.18 · NEXT", 'class="tree-row clay-b-euler-compactness-screen-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb17 = home.index('class="tree-row clay-b-euler-compactness-screen-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb17)
    if not (r0_start < r0_boundary < divider < clay_start < cb17 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-euler-compactness-screen-boundary"' not in literature or "CB.17 · ClayB-EulerCompactnessScreen-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.17 · {DISPLAY_ID}" not in index or "17 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.17" or site.get("nextIndependentChapter") != "CB.18":
        raise RuntimeError("version or chapter metadata drift")
    if manifest.get("latestCompletedRelease") != "r076l" or site.get("latestRelease") != "R0.76L":
        raise RuntimeError("canonical R0 endpoint drift")
    expected_handoff = handoff_bytes()
    handoff_path = ROOT / "release/handoffs/clay-b-euler-compactness-screen-20260906.json"
    if not handoff_path.is_file() or handoff_path.read_bytes() != expected_handoff:
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
    (ROOT / "release/handoffs/clay-b-euler-compactness-screen-20260906.json").write_bytes(handoff_bytes())

validate()
print(json.dumps({"schemaVersion": "clay-b-euler-compactness-screen-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.17", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
