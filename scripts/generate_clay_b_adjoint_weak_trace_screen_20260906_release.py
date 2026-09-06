#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Materialize and validate the ClayB AdjointWeakTraceScreen CB.20 HTML-only release."""

from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
VERSION = "2.64"
SLUG = "clay-b-adjoint-weak-trace-screen-20260906"
DISPLAY_ID = "ClayB-AdjointWeakTraceScreen-20260906"
NOTE_PATH = ROOT / f"public/notes/{SLUG}.html"
CHECK_ONLY = "--check-only" in sys.argv[1:]


ZH_SECTIONS = [
    ("01 / 结果地图", "弱初迹问题被校准为一个精确端点通量问题", '<div class="grid"><div class="card"><strong class="proved">PROVED IN STATED SCOPE</strong>在 BP 的额外正终端能量原子条件下，反时共同伴随是前向正黏性、带压力耦合的向量方程，具有弱零初迹和单位范数右极限。</div><div class="card"><strong class="proved">ENDPOINT FLUX</strong>有限 Fourier 通量对 C¹ 时间测试趋于边界泛函 δ₀/2，却在每个正时间几乎处处趋零，因此不一致可积。</div><div class="card"><strong class="open">UNPAID INTERFACE</strong>额外 L²H⁻¹ 时间正则、张量时空 L² 或 Serrin 漂移输入均可关闭跳跃，但基本能量没有支付它们。</div></div><p>这是条件性端点审计；没有构造或排除真实 NS 原子，也没有得到一般正则性。</p>'),
    ("02 / BS.1–BS.4", "零迹位于前向方程的初端", '<p>令 w(ρ)=A(T−ρ)、b(ρ)=−u(T−ρ)。反时后的 w 满足正黏性方程，而 b 满足负黏性方程；b 不是另一个正黏性 NS 解，Leray 投影所代表的非局部压力也没有消失。</p><div class="equation">wρ + P div(w⊗b) = νΔw,   div w = div b = 0.        (BS.2)</div><p>w(ρ) ⇀ 0，但 ||w(ρ)||₂²→1。正时间能量等式不能改写成从 w(0)=0 出发的能量不等式；若唯一性定理把强零迹或该不等式写进解类定义，就尚未证明 w 属于那一解类。</p>'),
    ("03 / BS.5–BS.7", "分布初值合法，基本时间指数仍不足", '<p>能量插值给 w∈L⁴ρL³x、b∈L²ρL⁶x，从而 w⊗b∈L⁴ᐟ³ρL²x，并有 wρ∈L⁴ᐟ³H⁻¹。对光滑无散测试从正时间积分再取初端极限，弱零初迹确实成立，方程中没有额外向量 Dirac 源。</p><div class="equation">1/2 + 1/(4/3) = 5/4 &gt; 1.                         (BS.7)</div><p>这个时间指数不能让 w 直接测试自身。它只说明基本能量估计不足，不证明时间导数不可能具有更强正则性。</p>'),
    ("04 / BS.8–BS.14", "有限模态揭示精确的端点成本", '<p>对 Fourier 正交投影 w_N，有限维方程可以合法测试自身，得到 e_N′+νd_N=Π_N。先固定 δ&gt;0 再令 N→∞，通量积分趋于 1/2；对任意 C¹ 时间测试 η，极限为 η(0)/2。</p><div class="equation">lim_N ∫₀^δ Π_N dρ = 1/2,   lim_N ∫₀ᴸ ηΠ_N dρ = η(0)/2.   (BS.10, BS.12)</div><p>极限泛函有 Radon 表示 δ₀/2，但没有证明 Π_Ndρ 的总变差一致有界、测度弱星收敛，或与 suitable 局部能量缺陷测度相同。Π_N 在正时间几乎处处趋零，因此在任一初端区间都不一致可积；频率极限与初始时间极限不可交换。</p>'),
    ("05 / BS.15–BS.18", "强迹接口明确存在，但所需输入没有付清", '<p>若 Pdiv(w⊗b)∈L²(0,δ;H⁻¹)，则 wρ∈L²H⁻¹。有限 Fourier 能量迹在所有端点上一致收敛，迫使 w 强连续到零初态，与单位范数右极限矛盾。</p><div class="equation">原子条件 ⇒ ||Pdiv(w⊗b)||_{L²H⁻¹}=||wρ||_{L²H⁻¹}=||w⊗b||_{L²}=∞.   (BS.17)</div><p>额外 Serrin 漂移 b∈LᵖLᑫ、q&gt;3、2/p+3/q≤1 可以支付张量 L²；但对 b=−u(T−ρ)，这就是原解的额外正则性条件。基本能量在 q=6 时只有时间 L²，而接口需要 L⁴；q=3 端点没有在本章导入。</p>'),
    ("06 / 四文献接口 I", "后向唯一性标题不能替代方向和解类匹配", '<p>Escauriaza–Seregin–Šverák 的 Theorem 1 允许向量，但其主部、零迹端点、点态闭合不等式、增长与局部导数条件没有被当前对象支付。Lei–Yang–Yuan 处理非局部压力，却针对全空间两个有界 mild NS 解及相应涡量条件；当前周期线性伴随不是那一解类。</p><p>核读范围分别为 ESS PDF 1–3 页和 Lei PDF 1–3、9–10 页；没有把未重做的 Carleman 或加权证明写成已复核，也没有把标题中的“唯一性”当成可直接使用的结论。</p>'),
    ("07 / 四文献接口 II", "四个唯一性接口均缺少必要输入", '<p>Cheskidov–Luo Appendix A 确实给周期压力耦合线性对偶接口，但 Theorems A.1–A.3 需要临界 Ladyzhenskaya–Prodi–Serrin 输入；p=∞ 时是 C_tL³，不是任意 L∞_tL³。Bonicatto–Ciampa–Crippa 的标量定理可从弱分布初值出发，却不能直接跨过向量压力：一般凸测试留下压力项，二次测试虽消压，其无界导数又超出已核读交换子接口。</p><p>这四项核查只证明它们不能在不增加假设时原样导入；不是穷尽性文献缺失、新颖性认证或公认开放问题分类。</p>'),
    ("08 / 来源、证据与下一步", "压力感知凸测试审计尚未开始", '<p>科学源提交 65de3e3b22be98d65fc32a47b56394e22a050f75；冻结提交 456e5c4c28f7e63ec3e84cbf2b8e0fbb516a5819。六份本轮文件、129 份依赖和一份冻结 manifest 由 SHA-256 绑定；三份文本源、18 个 BS 标签、15 项精确算术检查和 3 项有限负对照通过。</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_adjoint_weak_trace_20260906.md">BS 弱初迹正文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_adjoint_trace_primary_reading_20260906.md">四文献核读边界</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_adjoint_trace_report_20260906.md">阶段报告</a></p><p>下一研发动作只检查同一 b,w 上保留压力、交换子和极限顺序的有界凸测试，是否给出比 BS 更强且已支付的信息。该工作尚未开始；不能预设重整化、通量一致可积、张量 L² 或额外临界范数。</p><p><strong>本章不生成新读者 PDF，不创建图件、仿真、DGX 数据或累计 recap；不分发第三方 PDF。原子存在或排除、G、一般正则性仍 OPEN。NOT CLAY。</strong></p>'),
]

EN_SECTIONS = [
    ("01 / Result map", "The weak-trace question becomes a precise endpoint-flux problem", '<div class="grid"><div class="card"><strong class="proved">PROVED IN STATED SCOPE</strong>Under BP’s additional positive-terminal-energy-atom condition, the time-reversed common adjoint solves a forward positive-viscosity pressure-coupled vector equation with weak-zero initial trace and unit-norm right limit.</div><div class="card"><strong class="proved">ENDPOINT FLUX</strong>The finite Fourier fluxes converge against C¹ time tests to the boundary functional δ₀/2, while converging to zero almost everywhere at positive times, so they are not uniformly integrable.</div><div class="card"><strong class="open">UNPAID INTERFACE</strong>Additional L²H⁻¹ time regularity, spacetime L² tensor control, or Serrin drift input would close the jump, but basic energy pays none of them.</div></div><p>This is a conditional endpoint audit. It constructs or excludes no actual NS atom and proves no general regularity result.</p>'),
    ("02 / BS.1–BS.4", "The zero trace is at the initial endpoint of a forward equation", '<p>Set w(ρ)=A(T−ρ) and b(ρ)=−u(T−ρ). The reversed w obeys a positive-viscosity equation, whereas b obeys a negative-viscosity equation. Thus b is not another positive-viscosity NS solution, and the nonlocal pressure represented by the Leray projection has not disappeared.</p><div class="equation">wρ + P div(w⊗b) = νΔw,   div w = div b = 0.        (BS.2)</div><p>We have w(ρ) ⇀ 0 but ||w(ρ)||₂²→1. Positive-time energy equality cannot be rewritten as the energy inequality starting from w(0)=0. If a uniqueness theorem includes a strong-zero trace or that inequality in its solution class, membership of the present w has not been proved.</p>'),
    ("03 / BS.5–BS.7", "The distributional initial value is valid, but the basic time exponents are insufficient", '<p>Energy interpolation gives w∈L⁴ρL³x and b∈L²ρL⁶x, hence w⊗b∈L⁴ᐟ³ρL²x and wρ∈L⁴ᐟ³H⁻¹. Integrating against smooth divergence-free tests from positive time and then taking the endpoint limit proves the weak-zero initial trace; no vector Dirac source is added to the equation.</p><div class="equation">1/2 + 1/(4/3) = 5/4 &gt; 1.                         (BS.7)</div><p>This time exponent does not allow w to test itself directly. It shows only that the basic energy estimate is insufficient, not that a better time derivative is impossible.</p>'),
    ("04 / BS.8–BS.14", "Finite modes reveal the exact endpoint cost", '<p>For the orthogonal Fourier projection w_N, the finite-dimensional equation can be tested by w_N, giving e_N′+νd_N=Π_N. Fixing δ&gt;0 before sending N→∞ makes the flux integral tend to 1/2; against every C¹ time test η, the limit is η(0)/2.</p><div class="equation">lim_N ∫₀^δ Π_N dρ = 1/2,   lim_N ∫₀ᴸ ηΠ_N dρ = η(0)/2.   (BS.10, BS.12)</div><p>The limiting functional has the Radon representation δ₀/2, but no uniform total-variation bound, measure weak-star convergence, or identification with a suitable local-energy defect measure is proved. Since Π_N tends to zero almost everywhere at positive times, it is not uniformly integrable on any initial interval. Frequency and initial-time limits cannot be interchanged.</p>'),
    ("05 / BS.15–BS.18", "A strong-trace interface is explicit, but its inputs are unpaid", '<p>If Pdiv(w⊗b)∈L²(0,δ;H⁻¹), then wρ∈L²H⁻¹. The finite Fourier energy traces then converge uniformly at all endpoints, forcing strong continuity to the zero initial state and contradicting the unit-norm right limit.</p><div class="equation">atom condition ⇒ ||Pdiv(w⊗b)||_{L²H⁻¹}=||wρ||_{L²H⁻¹}=||w⊗b||_{L²}=∞.   (BS.17)</div><p>An additional Serrin drift bound b∈LᵖLᑫ, q&gt;3, 2/p+3/q≤1 pays the tensor L² interface. For b=−u(T−ρ), however, this is additional regularity of the parent. At q=6 basic energy gives only L² in time, whereas the interface needs L⁴. No q=3 endpoint is imported here.</p>'),
    ("06 / Four literature interfaces I", "A backward-uniqueness title does not replace matching direction and solution class", '<p>Escauriaza–Seregin–Šverák Theorem 1 allows vectors, but its principal part, zero-trace endpoint, closed pointwise differential inequality, growth, and local derivative inputs have not been paid for the present object. Lei–Yang–Yuan handles nonlocal pressure, but for two bounded mild NS solutions in full space with the corresponding vorticity conditions; the present periodic linear adjoint is not that solution class.</p><p>The recorded reading ranges are ESS PDF pages 1–3 and Lei PDF pages 1–3 and 9–10. Unreproduced Carleman or weighted proofs are not presented as reverified, and the word “uniqueness” in a title is not treated as a directly applicable theorem.</p>'),
    ("07 / Four literature interfaces II", "All four uniqueness interfaces lack required inputs", '<p>Cheskidov–Luo Appendix A does provide a periodic pressure-coupled linear duality interface, but Theorems A.1–A.3 require critical Ladyzhenskaya–Prodi–Serrin input; when p=∞ the endpoint is C_tL³, not arbitrary L∞_tL³. The scalar theorem of Bonicatto–Ciampa–Crippa can start from a weak distributional initial value, but it does not directly cross vector pressure: a general convex test leaves a pressure term, while the quadratic test removes pressure only with an unbounded derivative outside the checked commutator interface.</p><p>These four checks show only that the interfaces cannot be imported unchanged without additional assumptions. They are not an exhaustive literature-absence theorem, novelty certification, or classification of a recognized open problem.</p>'),
    ("08 / Sources, evidence, and next step", "The pressure-aware convex-test audit has not started", '<p>Scientific source commit: 65de3e3b22be98d65fc32a47b56394e22a050f75; freeze commit: 456e5c4c28f7e63ec3e84cbf2b8e0fbb516a5819. Six current files, 129 dependencies, and one frozen manifest are SHA-256-bound. Three text sources, 18 BS labels, 15 exact arithmetic checks, and three limited negative controls pass.</p><p class="note"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_adjoint_weak_trace_20260906.md">BS weak-trace source</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_adjoint_trace_primary_reading_20260906.md">four-source reading boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/clay_b_adjoint_trace_report_20260906.md">stage report</a></p><p>The next research action asks only whether a bounded convex test for the same b,w, with pressure, commutators, and limit order retained, yields stronger information already paid by the inputs. That work has not started. Renormalization, endpoint-flux uniform integrability, tensor L², and extra critical norms may not be assumed.</p><p><strong>This chapter creates no new reader PDF, figure, simulation, DGX data, or cumulative recap and redistributes no third-party PDF. Atom existence or exclusion, G, and general regularity remain OPEN. NOT CLAY.</strong></p>'),
]


def main_block(lang: str, sections: list[tuple[str, str, str]]) -> str:
    if lang == "zh":
        kicker = "CB.20 · 独立 Clay-B 方法笔记 · 2026-09-06"
        title = "CB.20｜伴随的弱零初迹：边界通量与唯一性接口"
        dek = "在正终端能量原子的条件分支中，反时共同伴随具有弱零初迹却保留单位能量右极限。有限模态把缺口定位为 δ₀/2 的初端通量；四个已核读唯一性接口均需要当前尚未支付的方向、解类、压力或临界范数输入。"
        footer = "独立 HTML 研究笔记"
    else:
        kicker = "CB.20 · Independent Clay-B methods note · 2026-09-06"
        title = "CB.20 | Weak-zero trace of the adjoint: boundary flux and uniqueness interfaces"
        dek = "On the conditional positive-terminal-energy-atom branch, the reversed common adjoint has weak-zero initial trace but retains a unit-energy right limit. Finite modes locate the gap in an initial boundary flux δ₀/2. Each of the four checked uniqueness interfaces requires an unpaid direction, solution-class, pressure, or critical-norm input."
        footer = "Independent HTML research note"
    body = "".join(f'<section><div class="section-no">{n}</div><h2>{h}</h2>{c}</section>' for n, h, c in sections)
    return f'''  <main data-language="{lang}">
    <article><header class="hero"><div class="kicker">{kicker}</div><h1>{title}</h1><p class="dek">{dek}</p><div class="meta"><span>PROVED IN STATED SCOPE</span><span>CONDITIONAL</span><span>ENDPOINT AUDIT</span><span>LITERATURE</span><span>FINITE CHECKS ONLY</span><span>G OPEN · NOT CLAY</span></div></header>{body}</article>
    <footer class="footer">CB.20 · {footer} · {DISPLAY_ID} · 2026-09-06</footer>
  </main>'''


SPOTLIGHT = '''<section class="route-overview independent-release-spotlight" id="clay-b-adjoint-weak-trace-screen" aria-labelledby="clay-b-adjoint-weak-trace-screen-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">CB.20 · INDEPENDENT CLAY-B METHODS NOTE · 2026-09-06 · ADJOINT WEAK-TRACE SCREEN</p><h2 class="route-map-title" id="clay-b-adjoint-weak-trace-screen-title">CB.20｜伴随的弱零初迹：边界通量与唯一性接口</h2><p class="route-map-intro">反时共同伴随的零迹位于前向方程初端，但能量右极限为一。有限 Fourier 通量对 C¹ 时间测试趋于 δ₀/2，并非已证明的缺陷测度；额外 L²H⁻¹、张量 L² 或 Serrin 输入仍未支付。四文献核查是有限适用性筛选，不是穷尽性或新颖性结论。G OPEN。NOT CLAY.</p></div><nav class="route-map-actions" aria-label="Clay-B 弱初迹伴随笔记快捷入口"><a class="route-map-latest" href="/notes/clay-b-adjoint-weak-trace-screen-20260906.html">阅读最新 CB.20 弱初迹笔记 →</a><a href="/literature-review.html#clay-b-adjoint-weak-trace-screen-boundary">查看原始来源与主张边界</a><a href="/notes/">研究笔记总索引</a></nav></header><div class="route-legend" aria-label="Clay-B 弱初迹筛查结论"><span><i class="route-legend-mark kept" aria-hidden="true"></i>前向弱零初迹与精确边界通量</span><span><i class="route-legend-mark stopped" aria-hidden="true"></i>四个接口均有未付输入</span><span><i class="route-legend-mark current" aria-hidden="true"></i>压力感知凸测试与一般正则性 OPEN · NOT CLAY</span></div></div></section>'''

CB20_ROW = '''          <div class="tree-row clay-b-adjoint-weak-trace-screen-row">
            <article class="tree-node current"><div class="tree-node-head"><span class="route-range">CB.20 · 2026-09-06 · BS ADJOINT WEAK-TRACE SCREEN</span><span class="tree-state current">当前路线边界</span></div><h3>CB.20｜伴随的弱零初迹：边界通量与唯一性接口</h3><p>BS 把共同伴随反时为前向正黏性、压力耦合向量方程：初迹分布意义下为零，但能量右极限为一。有限 Fourier 通量对 C¹ 时间测试趋于边界泛函 δ₀/2，正时间几乎处处趋零，因而不一致可积。</p><p>额外 L²H⁻¹、张量 L² 或 Serrin 漂移条件会给强初迹并排除该跳跃，但基本能量没有支付。ESS、Lei–Yang–Yuan、Cheskidov–Luo 与 Bonicatto–Ciampa–Crippa 四个接口都不能在不增加假设时原样导入；这不是穷尽性文献结论。</p><p class="tree-path"><a href="/notes/clay-b-adjoint-weak-trace-screen-20260906.html">阅读 CB.20 HTML</a> · <a href="/literature-review.html#clay-b-adjoint-weak-trace-screen-boundary">来源与主张边界</a> · 本章不生成新 PDF</p></article>
            <aside class="tree-branch right current"><span class="tree-state current">OPEN · NOT CLAY</span><h3>下一研发动作：压力感知的有界凸测试</h3><p>只检查同一 b,w 上完整保留压力、交换子和极限顺序的凸测试，是否产生比 BS 初端预算更强且已支付的信息。该审计尚未开始。</p></aside>
          </div>

          <div class="tree-row clay-b-public-boundary-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">CB.21 · NEXT · NOT AUTHORIZED · NOT YET FROZEN · PUBLIC BOUNDARY</span><span class="tree-state current">CLAY-B BOUNDARY</span></div><h3>Clay-B 独立路线停在 CB.20</h3><p>CB.21 只是下一章占位，不是已完成研究。压力感知凸测试、通量一致可积、原子存在或排除、G、任意奇点输入生成、一般正则性与 Clay 均未关闭。</p></article></div>'''

LITERATURE_BLOCK = '''<h3 id="clay-b-adjoint-weak-trace-screen-boundary">CB.20 · Clay-B 弱初迹伴随的文献和主张边界</h3><p>本轮核读四个原始接口：<a href="https://doi.org/10.1007/s00205-003-0263-8">Escauriaza–Seregin–Šverák 2003</a> PDF 1–3 页；<a href="https://arxiv.org/abs/2311.02429v1">Lei–Yang–Yuan 2311.02429v1</a> PDF 1–3、9–10 页；<a href="https://arxiv.org/abs/2009.06596v2">Cheskidov–Luo 2009.06596v2</a> PDF 1–3、32–34 页及 Appendix A；<a href="https://arxiv.org/abs/2306.15529v1">Bonicatto–Ciampa–Crippa 2306.15529v1</a> PDF 1、5–9 页，并完整读 Lemma 2.6 与 Theorem 2.7 的使用接口。没有把实际核读范围扩大成全篇证明重审。</p><div class="boundary"><strong>CB.20 · ClayB-AdjointWeakTraceScreen-20260906 公开边界</strong><p>CONDITIONAL ENDPOINT AUDIT：在 BP 的额外正终端能量原子条件下，反时共同伴随是前向正黏性、压力耦合向量解，具有弱零初迹和单位能量右极限；反时漂移本身满足负黏性方程。FINITE-MODE FLUX：Π_N 对每个正时间几乎处处趋零，但固定初端窗口积分趋于 1/2，对 C¹ 时间测试趋于 δ₀/2；极限泛函有 Radon 表示，未证明通量测度总变差一致有界、测度弱星收敛或 suitable 缺陷测度识别。UNPAID TRACE INTERFACE：原子条件迫使投影张量散度与 w_t 的 L²H⁻¹ 范数及张量时空 L² 范数在每个初端区间无限；额外 Serrin 条件足够但不是基本能量。LITERATURE：ESS 的方向/迹/闭合条件、Lei 的有界 mild 全空间 NS 解类、CL 的临界压力对偶输入、BCC 的标量凸测试均不能原样导入。CL A.1–A.3 是 Theorems，C_tL³ 不可弱化为任意 L∞_tL³。该四项筛选不证明穷尽性文献缺失或新颖性。FINITE CHECKS ONLY：三份文本源、18 个 BS 标签、135/135 文件绑定、15 项算术检查和 3 项有限负对照不替代 PDE 证明。原子存在/排除、压力感知凸测试、G、一般正则性 OPEN；无图件、仿真、新 PDF 或累计 recap。NOT CLAY。<a href="/notes/clay-b-adjoint-weak-trace-screen-20260906.html">阅读完整 CB.20 笔记</a>。</p></div>
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
    template = (ROOT / "public/notes/clay-b-common-adjoint-screen-20260906.html").read_text(encoding="utf-8")
    template = set_version(template)
    template = re.sub(r'<title>.*?</title>', '<title>伴随的弱零初迹：边界通量与唯一性接口</title>', template, count=1)
    template = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="Clay-B 共同伴随的弱零初迹、有限模态边界通量和四个唯一性接口的双语方法笔记。">', template, count=1)
    template = re.sub(r'<link rel="canonical" href="[^"]+">', f'<link rel="canonical" href="https://kasifa.github.io/notes/{SLUG}.html">', template, count=1)
    template = re.sub(r'<header class="masthead">.*?</header>', f'<header class="masthead"><strong><a href="/research-review.html">研究首页</a> · CB.20 · {DISPLAY_ID}</strong></header>', template, count=1)
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
    value = value.replace("CB.1–CB.19", "CB.1–CB.20")
    value = value.replace("common adjoint / operator-budget strength screen", "adjoint weak-trace / endpoint-flux screen", 1)
    old_focus = "Clay-B 已完成共同伴随核心与算子出口强度核查：正原子条件下同一原解驱动的共同伴随和最终离散全尾可保留，固定后继解二阶作用发散；但全单位初态延迟算子预算的有限性已等价于原解光滑延拓，并非更弱的能量出口。下一步只核查终端唯一性的适用条件。"
    new_focus = "Clay-B 已把共同伴随的唯一性问题校准为弱初迹端点通量：反时后是前向压力耦合方程，有限 Fourier 通量对 C¹ 时间测试趋于 δ₀/2，但总变差、测度弱星收敛和 suitable 缺陷识别均未证明。四个已核读唯一性接口仍需未付输入。下一步只检查压力感知的有界凸测试。"
    if old_focus in value:
        value = value.replace(old_focus, new_focus, 1)
    elif new_focus not in value:
        raise RuntimeError("homepage focus copy drift")
    if 'class="tree-row clay-b-adjoint-weak-trace-screen-row"' in value:
        return value
    cb19_start = value.index('<div class="tree-row clay-b-common-adjoint-screen-row">')
    boundary_start = value.index('<div class="tree-row clay-b-public-boundary-row">', cb19_start)
    cb19 = value[cb19_start:boundary_start]
    cb19 = cb19.replace('<article class="tree-node current">', '<article class="tree-node">', 1)
    cb19 = cb19.replace('<span class="tree-state current">当前路线边界</span>', '<span class="tree-state">独立路线章节</span>', 1)
    cb19, aside_count = re.subn(r'<aside class="tree-branch right current">[\s\S]*?</aside>', '<aside class="tree-branch right kept"><span class="tree-state">ADJOINT WEAK-TRACE SCREEN COMPLETED</span><h3>弱初迹端点核查已进入 CB.20</h3><p>BS 已校准时间方向、弱初迹、有限模态通量和四个原始唯一性接口；结果见下一个正式路线节点。</p></aside>', cb19, count=1)
    if aside_count != 1:
        raise RuntimeError("CB.19 branch drift")
    value = value[:cb19_start] + cb19 + value[boundary_start:]
    value, boundary_count = re.subn(r'          <div class="tree-row clay-b-public-boundary-row">[\s\S]*?</div>\n        </div>\n      </div>\n    </section>', CB20_ROW + '\n        </div>\n      </div>\n    </section>', value, count=1)
    if boundary_count != 1:
        raise RuntimeError("Clay-B boundary drift")
    return value


def update_literature(value: str) -> str:
    value = set_version(value, "文献综述")
    if 'id="clay-b-adjoint-weak-trace-screen-boundary"' not in value:
        marker = '<section id="references">'
        if marker not in value:
            raise RuntimeError("literature references marker missing")
        value = value.replace(marker, LITERATURE_BLOCK + marker, 1)
    return value


def update_metadata(path: Path) -> None:
    payload = json.loads(path.read_text(encoding="utf-8"))
    payload["version" if path.name == "site-version.json" else "siteVersion"] = VERSION
    payload["publicIndependentNoteCount"] = 20
    payload["latestIndependentNote"] = DISPLAY_ID
    payload["latestIndependentResearchHtml"] = f"/notes/{SLUG}.html"
    payload["latestIndependentResearchPdf"] = None
    payload["independentChapterScheme"] = "CB.n"
    payload["latestIndependentChapter"] = "CB.20"
    payload["nextIndependentChapter"] = "CB.21"
    if path.name == "release-manifest.json":
        payload["latestPublication"] = {
            "schemaVersion": "independent-research-publication-v1",
            "kind": "independent-analytic-note",
            "releaseId": SLUG,
            "displayReleaseId": DISPLAY_ID,
            "chapter": "CB.20",
            "sourceCommit": "65de3e3b22be98d65fc32a47b56394e22a050f75",
            "baseCommit": "82b5d1f5a11c13a87151b08d17d6dfe674a89641",
            "handoffCommit": "456e5c4c28f7e63ec3e84cbf2b8e0fbb516a5819",
            "logicalPredecessor": "ClayB-CommonAdjointScreen-20260906",
            "html": f"public/notes/{SLUG}.html",
            "pdfGenerated": False,
            "pdfPolicy": "OMITTED_BY_USER_PUBLISHING_POLICY",
            "gate": "tests/clay-b-adjoint-weak-trace-screen-20260906-gate.test.mjs",
            "publicationTest": "tests/clay-b-adjoint-weak-trace-screen-20260906-release.test.mjs",
            "translationScript": "scripts/add-clay-b-adjoint-weak-trace-screen-20260906-translations.mjs",
            "browserQaScript": "scripts/qa-publication-browser.mjs",
            "onlineVerifierScript": "scripts/verify-publication-online.mjs",
            "formalFigureRequired": False,
            "formalFigureStatus": "NOT_APPLICABLE_ANALYTIC_RELEASE",
            "simulationRequired": False,
            "recapRequired": False,
            "advancesCanonicalR0Series": False,
            "canonicalR0EndpointPreserved": "r076l",
            "claimBoundary": "CONDITIONAL_POSITIVE_TERMINAL_ATOM_COMMON_ADJOINT_REVERSES_TO_FORWARD_PRESSURE_COUPLED_WEAK_ZERO_INITIAL_TRACE_WITH_UNIT_ENERGY_RIGHT_LIMIT_FINITE_MODE_FLUX_CONVERGES_AGAINST_C1_TESTS_TO_DELTA_ZERO_OVER_TWO_WITHOUT_UNIFORM_TOTAL_VARIATION_MEASURE_WEAK_STAR_OR_SUITABLE_DEFECT_IDENTIFICATION_EXTRA_L2H_MINUS1_TENSOR_L2_OR_SERRIN_INPUTS_UNPAID_FOUR_SOURCE_APPLICABILITY_SCREEN_NOT_EXHAUSTIVE_ATOM_EXCLUSION_AND_GENERAL_REGULARITY_OPEN_NOT_CLAY",
        }
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def handoff_bytes() -> bytes:
    ledger = json.loads((ROOT / "research/clay_b_adjoint_weak_trace_screen_frozen_ledger_20260906.json").read_text(encoding="utf-8"))
    qa = json.loads((ROOT / "release/qa/clay-b-adjoint-weak-trace-screen-20260906.json").read_text(encoding="utf-8"))
    artifacts = [{"path": row["path"], "sha256": row["sha256"], "role": "frozen-scientific-source" if row["role"] == "scientific-source" else "frozen-dependency", "commit": row["commit"]} for row in ledger["files"]]
    artifacts += [{"path": row["path"], "sha256": row["sha256"], "role": "frozen-release-manifest", "commit": row["commit"]} for row in ledger["handoffEnvelope"]]
    outputs = [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html", "public/notes/index.html", "public/site-version.json", "research/release-manifest.json", "VERSION"]
    support = ["research/clay_b_adjoint_weak_trace_screen_frozen_ledger_20260906.json", "release/handoffs/clay-b-adjoint-weak-trace-screen-20260906.json", "release/qa/clay-b-adjoint-weak-trace-screen-20260906.json", "scripts/import_clay_b_adjoint_weak_trace_screen_20260906_frozen.py", "scripts/generate_clay_b_adjoint_weak_trace_screen_20260906_release.py", "scripts/generate_note_index.py", "scripts/add-clay-b-adjoint-weak-trace-screen-20260906-translations.mjs", "tests/clay-b-adjoint-weak-trace-screen-20260906-gate.test.mjs", "tests/clay-b-adjoint-weak-trace-screen-20260906-release.test.mjs", "tests/release-publication-invariant.test.mjs", "translations/en.json", "public/i18n-en.js"]
    managed = list(dict.fromkeys(outputs + [row["path"] for row in artifacts] + support))
    payload = {
        "schemaVersion": "research-publication-handoff-v1",
        "releaseId": DISPLAY_ID,
        "frozenCommit": "456e5c4c28f7e63ec3e84cbf2b8e0fbb516a5819",
        "sourceRepository": "navier-stokes-r074m",
        "translationRoute": "LOCAL_DIRECT_NO_DGX",
        "artifacts": artifacts,
        "artifactPolicy": {"readerPdf": "OMIT_NEW", "scientificFigure": "NOT_REQUIRED"},
        "claimBoundary": {"requiredLabels": ["PROVED", "PROVED IN STATED SCOPE", "CONDITIONAL", "ENDPOINT AUDIT", "LITERATURE", "FINITE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"], "publicFiles": [f"public/notes/{SLUG}.html", "public/research-review.html", "public/literature-review.html"]},
        "recap": {"mode": "PRESERVE", "latestRecapRelease": "r076i", "preservedArtifacts": [{"path": "public/recap-r0-61-r0-76i.html", "sha256": "1ea5048bcbecf791a557da94aa4bbf7fbda0a9517c83f40327d119af4f8103c9"}, {"path": "public/recap-r0-61-r0-76i.pdf", "sha256": "5bff642caa0c7ad4bf6cdfc3df252b3c0e68312373e185e3a85f27a5828baa98"}]},
        "stages": {
            "generate": {"runner": "python-local", "script": "scripts/generate_clay_b_adjoint_weak_trace_screen_20260906_release.py", "inputs": [row["path"] for row in artifacts] + ["research/clay_b_adjoint_weak_trace_screen_frozen_ledger_20260906.json"], "outputs": outputs},
            "translate": {"runner": "node-local", "script": "scripts/add-clay-b-adjoint-weak-trace-screen-20260906-translations.mjs", "inputs": ["public/research-review.html", "public/literature-review.html", "public/notes/index.html", "translations/en.json"], "outputs": ["translations/en.json", "public/i18n-en.js"]},
        },
        "publication": {"expectedCommit": None, "siteBaseUrl": "https://kasifa.github.io", "repository": "Kasifa/Kasifa.github.io", "workflow": "pages.yml", "remote": "origin", "targetBranch": "main", "commitMessage": "Publish ClayB AdjointWeakTraceScreen CB.20 HTML note", "managedPaths": managed, "expectedLive": qa["online"]["expectedLive"], "expectedAbsent": qa["online"]["expectedAbsent"], "siteVersionExpectations": qa["online"]["siteVersionExpectations"]},
        "visualQa": {"evidencePath": qa["browser"]["evidencePath"], "configPath": "release/qa/clay-b-adjoint-weak-trace-screen-20260906.json", "requiredChecks": [f"{target['id']}-{scenario['id']}" for target in qa["browser"]["targets"] for scenario in qa["browser"]["scenarios"]]},
    }
    return (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode()


def validate() -> None:
    note = NOTE_PATH.read_text(encoding="utf-8")
    for marker in ["CB.20", DISPLAY_ID, "伴随的弱零初迹：边界通量与唯一性接口", "Weak-zero trace of the adjoint: boundary flux and uniqueness interfaces", "PROVED IN STATED SCOPE", "CONDITIONAL", "ENDPOINT AUDIT", "LITERATURE", "FINITE CHECKS ONLY", "OPEN", "NOT CLAY"]:
        if marker not in note:
            raise RuntimeError(f"note marker missing: {marker}")
    if note.count('<main data-language="zh">') != 1 or note.count('<main data-language="en">') != 1 or note.count("<section>") != 16:
        raise RuntimeError("bilingual note structure drift")
    if "<img" in note or f"/notes/{SLUG}.pdf" in note or (ROOT / f"public/notes/{SLUG}.pdf").exists():
        raise RuntimeError("HTML-only figure-free policy drift")
    home = (ROOT / "public/research-review.html").read_text(encoding="utf-8")
    for marker in ["CB.1–CB.20", "Clay-B 独立路线停在 CB.20", "CB.21 · NEXT", 'class="tree-row clay-b-adjoint-weak-trace-screen-row"', f"/notes/{SLUG}.html"]:
        if marker not in home:
            raise RuntimeError(f"homepage marker missing: {marker}")
    if home.count('class="route-overview independent-release-spotlight"') != 1:
        raise RuntimeError("homepage independent spotlight count drift")
    r0_start = home.index('class="route-tree r0-route-tree"')
    r0_boundary = home.index('class="tree-row r0-public-boundary-row"', r0_start)
    divider = home.index('class="route-lane-divider"', r0_boundary)
    clay_start = home.index('class="route-tree clay-b-route-tree"', divider)
    cb20 = home.index('class="tree-row clay-b-adjoint-weak-trace-screen-row"', clay_start)
    clay_boundary = home.index('class="tree-row clay-b-public-boundary-row"', cb20)
    if not (r0_start < r0_boundary < divider < clay_start < cb20 < clay_boundary):
        raise RuntimeError("homepage route topology drift")
    literature = (ROOT / "public/literature-review.html").read_text(encoding="utf-8")
    if 'id="clay-b-adjoint-weak-trace-screen-boundary"' not in literature or "CB.20 · ClayB-AdjointWeakTraceScreen-20260906 公开边界" not in literature:
        raise RuntimeError("literature boundary missing")
    index = (ROOT / "public/notes/index.html").read_text(encoding="utf-8")
    if f'data-note="{SLUG}"' not in index or f"CB.20 · {DISPLAY_ID}" not in index or "20 NOTES" not in index:
        raise RuntimeError("note index drift")
    site = json.loads((ROOT / "public/site-version.json").read_text(encoding="utf-8"))
    manifest = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    if site.get("version") != VERSION or manifest.get("siteVersion") != VERSION or site.get("latestIndependentChapter") != "CB.20" or site.get("nextIndependentChapter") != "CB.21":
        raise RuntimeError("version or chapter metadata drift")
    if manifest.get("latestCompletedRelease") != "r076l" or site.get("latestRelease") != "R0.76L":
        raise RuntimeError("canonical R0 endpoint drift")
    expected = handoff_bytes()
    path = ROOT / "release/handoffs/clay-b-adjoint-weak-trace-screen-20260906.json"
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
    (ROOT / "release/handoffs/clay-b-adjoint-weak-trace-screen-20260906.json").write_bytes(handoff_bytes())

validate()
print(json.dumps({"schemaVersion": "clay-b-adjoint-weak-trace-screen-generation-v1", "releaseId": DISPLAY_ID, "status": "PASS", "mode": "check-only" if CHECK_ONLY else "apply", "siteVersion": VERSION, "chapter": "CB.20", "canonicalR0Endpoint": "R0.76L", "independentSpotlightCount": 1, "readerPdf": "OMIT_NEW"}, ensure_ascii=False))
