#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate the fail-closed R0.73C certified Rayleigh release.

R0.73C closes the exact cubic neutral spectrum and one
infinite-dimensional frozen inviscid Rayleigh instability.  It deliberately
leaves the singular viscous/nonautonomous transfer open; the resulting
super-polynomial complete-row no-go is only conditional.
"""

from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
from dataclasses import replace
from pathlib import Path

from generate_r072o_release import (
    assert_clean,
    digest,
    once,
    required,
    section,
    verify_flat_hash_ledger,
)
from generate_r072p_release import assert_mathjax_clean


ROOT = Path(os.environ.get("R073C_RELEASE_ROOT", Path(__file__).resolve().parents[1])).resolve()
PUBLIC = ROOT / "public"
FIGURE_ID = "fig-r073c-certified-rayleigh-instability"
FIGURE_RELATIVE = f"figures/r073c/{FIGURE_ID}"
CERTIFICATE_RELATIVE = "research/certificates/r073c"
EXPERIMENT_RELATIVE = "experiments/r073c"

R073B_RELEASE_BASELINE = {
    "latestCompletedRelease": "r073b",
    "siteVersion": "1.42",
    "publicHtmlNoteCount": 178,
    "postR060RecapNodeCount": 118,
    "nextRelease": "r073c",
    "latestReleaseGate": "tests/r073b-bloch-kinetic-gate.test.mjs",
    "latestReleasePublicationTest": "tests/r073b-release.test.mjs",
    "postR070APublishedReleaseCount": 80,
    "postR070AFormalSealedReleaseCount": 56,
    "legacyFormalFigureBacklogCount": 24,
}

SOURCE_STAGE_CONTRACT = {
    "release": "r073c",
    "stage": "source-freeze",
    "publicationStatus": "pending-formal-certificate-figure-and-publication",
    "publicCountersAdvanced": False,
    "report": "research/r073c_report-source.md",
    "problemFreeze": "research/r073c_problem_freeze.md",
    "literatureAudit": "research/r073c_literature_audit.md",
    "gapMatrix": "research/r073c_gap_matrix.md",
    "analyticProof": "research/r073c_monodromy_proof.md",
    "independentAudit": "research/r073c_independent_analytic_audit.md",
    "independentAnalyticAudit": "research/r073c_independent_analytic_audit.md",
    "producer": "research/certificates/r073c/generate_certificate.py",
    "independentProducer": "research/certificates/r073c/independent_recompute.py",
    "comparator": "research/certificates/r073c/validate_certificate.py",
    "certificateDirectory": CERTIFICATE_RELATIVE,
    "experimentDirectory": EXPERIMENT_RELATIVE,
    "figureDirectory": FIGURE_RELATIVE,
    "generator": "scripts/generate_r073c_release.py",
    "translationScript": "scripts/add-r073c-translations.mjs",
    "translationSnapshot": "scripts/i18n-snapshots/r073c-missing.json",
    "releaseGate": "tests/r073c-rayleigh-instability-gate.test.mjs",
    "publicationTest": "tests/r073c-release.test.mjs",
    "certificateSourceTest": "tests/r073c-deterministic-certificate-source.test.mjs",
    "figureSourceTest": "tests/r073c-certified-rayleigh-instability-figure-source.test.mjs",
}

NOTE_HERO = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">研究笔记 R0.73C · CUBIC NEUTRAL LEVEL · CERTIFIED RAYLEIGH INSTABILITY</div>
        <h1>我闭合了三次零点的精确中性谱，<br>并认证一条真正的无穷维冻结不稳定行</h1>
        <p class="lead">双谐波碰撞剖面在 \(\gamma_0=\sqrt7/2\) 有唯一负奇异阈值；在 \(\gamma=1/2\) 上，周期单值矩阵的严格区间异号进一步给出 \(\sigma_*\in(0.17035,0.17050)\) 的正实特征值。它不是 Fourier 截断外推。黏性谱延拓和非自治快时间传递仍为 OPEN。</p></div>
      <div class="stamp"><span class="state">状态 · R0.73C frozen Rayleigh theorem 完成</span><strong>Certified frozen instability</strong><p>版本 v0.73C · 2026-08-30</p><p>C3 exact neutral spectrum: CLOSED</p><p>C4 frozen Rayleigh instability: CLOSED</p><p>C5 fast-time transfer: OPEN</p><p>C6 super-polynomial no-go: CONDITIONAL</p><p>A2 / nonlinear / Clay: OPEN</p></div>
    </div></header>'''

NOTE_ARTICLE = r'''      <article>
        <section id="result"><div class="section-no">00 / Direct decision</div><h2>冻结无穷维 Rayleigh 不稳定已经闭合；黏性传递与 Clay 没有闭合</h2><div class="verdict-grid"><div class="verdict-card true"><strong>CLOSED · EXACT CUBIC LEVEL</strong><p>exactCubicNeutralSpectrum=CLOSED；\(\gamma_0=\sqrt7/2\)，奇异 Sturm--Liouville 算子的唯一负阈值为 \(-7/4\)。</p></div><div class="verdict-card true"><strong>CLOSED · INFINITE-DIMENSIONAL FROZEN MODE</strong><p>infiniteDimensionalFrozenRayleighInstability=CLOSED；\(\gamma=1/2\) 时存在 \(\sigma_*\in(0.17035,0.17050)\) 的正实点谱。</p></div><div class="verdict-card false"><strong>OPEN / CONDITIONAL · TRANSFER</strong><p>frozenInstabilityFastTimeTransfer=OPEN；superPolynomialCompleteRowNoGo=CONDITIONAL。小系数乘无界黏性算子不能当作有界小扰动。</p></div><div class="verdict-card false"><strong>OPEN · STRONGER TARGETS</strong><p>sharpLargeLambdaGrowthLaw=OPEN；completeOSSquireA2DirectSum=OPEN；nonlinearNavierStokes=OPEN；Clay=OPEN。</p></div></div></section>
        <section id="operator"><div class="section-no">01 / Frozen operator</div><h2>先固定一条二维 Fourier 行和相速度号约定</h2><div class="equation result">\[A_\gamma(0)=-i\gamma\bigl(M_{W_0}+M_{W_0''}L_{\gamma^2}^{-1}\bigr),\qquad W_0=-\tfrac12\sin x+\tfrac14\sin2x.\]</div><div class="equation result">\[(W_0-c)(\phi''-\gamma^2\phi)-W_0''\phi=0,\qquad \sigma=-i\gamma c.\]</div><p>取 \(c=i\eta\)、\(\eta>0\) 时，时间特征值为 \(\sigma=\gamma\eta>0\)。本节只研究这个冻结线性行。</p></section>
        <section id="neutral"><div class="section-no">02 / Exact cubic neutral level</div><h2>周期 Sobolev 模态与 Pöschl--Teller 谱把 C3 完整闭合</h2><div class="equation result">\[W_0=-2\sin^3(x/2)\cos(x/2),\qquad \phi_0=|\sin(x/2)|^3\in C^2\cap H^2_{\rm per}.\]</div><div class="equation result">\[\left(-\partial_x^2+\frac{W_0''}{W_0}\right)\phi_0=-\frac74\phi_0,\qquad \sigma(H_0)=\left\{\frac{(n+3)^2-16}{4}\right\}_{n\ge0}.\]</div><p>因此 \(-7/4\) 是唯一负奇异阈值，\(\gamma_0=\sqrt7/2\) 给出精确中性模态。周期延拓不是 \(C^3\)，但端点一阶导数匹配，不产生 delta 质量。</p></section>
        <section id="singular"><div class="section-no">03 / Singular boundary</div><h2>三次零点阻止直接套用正则 Tollmien--Lin 延拓</h2><div class="equation result">\[W_0(x)=-\frac{x^3}{4}+O(x^5),\qquad -\frac{W_0''}{W_0}=-\frac6{x^2}+O(1).\]</div><p>中性相速度嵌在本质谱内，有效势既无界也不局部可积。C4 因而不从中性模态自动推出，而改在无奇点的 \(c=i\eta\) 线上直接认证。</p></section>
        <section id="monodromy"><div class="section-no">04 / Periodic monodromy</div><h2>周期单值矩阵的实迹把谱问题降为一个连续实函数的零点</h2><div class="equation result">\[\phi''=Q_\eta\phi,\qquad Q_\eta=\frac14+\frac{W_0''}{W_0-i\eta},\qquad M(\eta)=Y_\eta(2\pi).\]</div><div class="equation result">\[\det M=1,\qquad M^{-1}=S\overline M S,\qquad F(\eta)=\operatorname{tr}M(\eta)-2\in\mathbb R.\]</div><p>又有 \(\det(M-I)=2-\operatorname{tr}M\)，所以存在非零周期解当且仅当 \(F(\eta)=0\)。</p></section>
        <section id="interval"><div class="section-no">05 / Validated interval theorem</div><h2>两组 Picard--Taylor 区间运行在同一对端点给出严格异号</h2><div class="equation result">\[F(0.3407)&lt;0,\qquad F(0.3410)&gt;0.\]</div><p>主程序把三角函数和两列基本解自治化为十二维实系统；每一步先验证整步 Picard 包含，再用正规化 Taylor 系数和区间 Lagrange 余项封住终点。运行 A 使用 1024 步、10 阶、40 位；运行 B 使用 768 步、12 阶、55 位。两次都给严格异号。</p><div class="equation result">\[\exists\eta_*\in(0.3407,0.3410),\qquad \sigma_*=\eta_*/2\in(0.17035,0.17050).\]</div></section>
        <section id="independent"><div class="section-no">06 / Independent arithmetic</div><h2>标准库 Decimal 内核独立复算同一严格符号</h2><p>独立验证器不导入主程序、mpmath、NumPy 或 SciPy；它用 ROUND_FLOOR / ROUND_CEILING、Machin 公式的 \(\pi\) 包含和另一套 Picard--Taylor 实现，在 256 步、8 阶、80 位下重算两个端点。两份正式 JSON 字节一致，determinant 与 imaginary-trace sentinels 同时通过。</p></section>
        <section id="finite"><div class="section-no">07 / Finite diagnostic</div><h2>Fourier--Galerkin 只做独立定位，不承担 C4 证明</h2><div class="equation result">\[\sigma_N\approx0.170407976920434\qquad(N=32,48,64,96,128).\]</div><p>这个值落在严格区间内。独立有限验证复核特征值、残差、投影和 sampled winding；由于没有无穷维 tail enclosure，它只标为 finite diagnostic。</p></section>
        <section id="transfer"><div class="section-no">08 / C5 correction</div><h2>无界黏性算子使“冻结模态直接传递”这一步失效</h2><div class="equation result">\[\partial_\theta q=\operatorname{sgn}(\Lambda)A_{1/2}(\theta/|\Lambda|)q-|\Lambda|^{-1}L_{1/4}q.\]</div><p>在 physical kinetic space 中，\(-|\Lambda|^{-1}L_{1/4}\) 对每个有限 \(|\Lambda|\) 都是无界算子。下一关必须建立黏性特征值延拓、统一 Riesz 围道、补空间 dichotomy 与 graph-domain-compatible Kato transport；这些条件目前没有被证明。</p></section>
        <section id="conditional"><div class="section-no">09 / Conditional consequence</div><h2>超多项式 complete-row no-go 只在 C5 闭合后成立</h2><div class="equation result">\[\|U_{\varepsilon,+}(M\log(1/\varepsilon),0)q_\varepsilon\|_{\mathcal K_{1/4}}\ge c_M\varepsilon^{-M\sigma_*+o_M(1)}.\]</div><p>这是明确列出谱延拓、投影、dichotomy 与 Kato 条件后的条件推论；现在不能把它写成无条件 large-\(|\Lambda|\) 增长定理，也没有证明根唯一或代数单性。</p></section>
        <section id="evidence"><div class="section-no">10 / Evidence boundary</div><h2>解析桥、区间证书、独立复算和有限诊断各自承担不同任务</h2><p>C3 由精确奇异谱承担；C4 由实迹、周期判据、连续性和严格端点异号共同承担；Decimal 复算验证算术独立性；Fourier screen 只用于定位和排错。任何有限 contour sampling 都不被称为无穷维 Riesz 证书。</p></section>
        <section id="figure"><div class="section-no">11 / Journal figure</div><h2>中性谱、单值迹异号、有限交叉验证与下一缺口分面展示</h2><p><img src="/assets/r073c/fig-r073c-certified-rayleigh-instability.svg" alt="R0.73C certified cubic neutral spectrum and frozen Rayleigh instability"></p><p><a href="/assets/r073c/fig-r073c-certified-rayleigh-instability.pdf">下载 PDF</a> · <a href="/assets/r073c/fig-r073c-certified-rayleigh-instability.png">下载 PNG</a> · <a href="/assets/r073c/fig-r073c-certified-rayleigh-instability.svg">打开 SVG</a></p></section>
        <section id="value"><div class="section-no">12 / Research value</div><h2>这把大参数路线从纯非正规瞬态问题改写成谱不稳定与黏性延拓问题</h2><p>严格增量是一个固定、可复核的无穷维不稳定行和增长率区间。它为下一节提供具体谱目标，也暴露真正缺口是 vanishing-viscosity persistence，而不是继续扩大有限矩阵扫描。它仍只是一条冻结二维线性行，离三维 nonlinear closure 和 Clay 很远。</p></section>
        <section id="next"><div class="section-no">13 / Next gate</div><h2>R0.73D：冻结黏性 Evans/Riesz 延拓问题</h2><p>先证明 \(B_{\varepsilon,+}(0)=A_{1/2}(0)-\varepsilon L_{1/4}\) 存在 \(\lambda_\varepsilon\to\sigma_*\) 的特征值，并在共同围道上统一控制 Riesz 投影；只有随后闭合补空间 resolvent，才进入非自治 Kato transport。</p></section>
        <section id="reproduce"><div class="section-no">14 / Reproduction</div><h2>完整报告、解析证明、双区间内核、有限诊断和正式附图</h2><p><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073c_report-source.md">完整数学报告</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073c_monodromy_proof.md">单值迹证明</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073c_independent_analytic_audit.md">独立解析审计</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073c_literature_audit.md">文献边界审计</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073c">正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073c">区间与有限实验</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/figures/r073c/fig-r073c-certified-rayleigh-instability">正式附图包</a> · <a href="/notes/r0-73c.pdf">同步研究笔记 PDF</a> · <a href="/recap-r0-61-r0-73c.html">累计回顾</a> · <a href="/recap-r0-61-r0-73c.pdf">累计回顾 PDF</a></p></section>
      </article>'''

HOME_NEXT = r'''            <article class="tree-node next">
              <div class="tree-node-head"><span class="route-range">NEXT · R0.73D</span><span class="tree-state current">下一检查点</span></div>
              <h3>vanishing-viscosity Evans/Riesz persistence</h3><p>先把冻结正特征值延拓到 \(A_{1/2}(0)-\varepsilon L_{1/4}\)，统一控制 Riesz 投影和补空间 resolvent，再讨论非自治 Kato transport。</p>
            </article>'''

HOME_C_CARD = r'''          <div class="task-one" id="r073c" data-release="r073c" style="margin-top:2rem">
            <p class="eyebrow">研究笔记 R0.73C · 2026-08-30</p><h3>三次中性谱与无穷维冻结 Rayleigh 不稳定</h3>
            <p>周期 Sobolev 模态和 Pöschl--Teller 谱闭合 \(\gamma_0=\sqrt7/2\) 的唯一负奇异阈值；\(\gamma=1/2\) 上，周期单值矩阵的严格区间异号给出 \(\sigma_*\in(0.17035,0.17050)\) 的正实点谱。</p><p>主 mpmath.iv 证明运行和独立 Decimal 内核得到同一严格符号；Fourier--Galerkin 值 \(0.170407976920434\ldots\) 只作为有限诊断。</p>
            <p><strong>结论边界：</strong>&nbsp;C3 与 C4 为 CLOSED；frozenInstabilityFastTimeTransfer 为 OPEN；superPolynomialCompleteRowNoGo 为 CONDITIONAL；A2、nonlinearNavierStokes 与 Clay 保持 OPEN。</p>
            <p><a href="/notes/r0-73c.html"><strong>阅读 R0.73C 研究笔记 →</strong></a><br><a href="/notes/r0-73c.pdf">下载同步研究笔记 PDF</a> · <a href="/assets/r073c/fig-r073c-certified-rayleigh-instability.pdf">下载期刊附图 PDF</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073c">查看正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r073c_report-source.md">查看完整数学报告</a> · <a href="/recap-r0-61-r0-73c.html">打开累计回顾</a></p>
            <p><strong style="color:var(--gold)">下一步 R0.73D：</strong>&nbsp;vanishing-viscosity Evans/Riesz persistence。</p>
          </div>'''

HOME_LATEST_SPOTLIGHT = r'''    <section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title">
      <div class="route-overview-inner">
        <header class="route-map-header">
          <div><p class="eyebrow">LATEST RELEASE · R0.73C · 2026-08-30</p><h2 class="route-map-title" id="latest-release-title">三次中性谱与无穷维冻结 Rayleigh 不稳定</h2><p class="route-map-intro">C3 exact neutral spectrum 与 C4 infinite-dimensional frozen Rayleigh instability 已闭合。C5 viscous fast-time transfer 仍为 OPEN，C6 super-polynomial complete-row no-go 只为 CONDITIONAL；Clay 问题仍未解决。</p></div>
          <nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-73c.html">阅读最新 R0.73C 研究笔记 →</a><a href="/recap-r0-61-r0-73c.html">119 节累计回顾</a><a href="/notes/">179 篇研究笔记总索引</a><a href="#r073c">查看首页完整 R0.73C 卡片</a></nav>
        </header>
        <div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.73C · 81 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>57 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.73C</span></div>
      </div>
    </section>'''


def _validate_source_stage_manifest(release: dict) -> None:
    for key, value in R073B_RELEASE_BASELINE.items():
        if release.get(key) != value:
            raise RuntimeError(f"release manifest is not at R0.73B: {key}")
    if release.get("nextReleaseSourceStage") != SOURCE_STAGE_CONTRACT:
        raise RuntimeError("R0.73C source-stage manifest contract is missing, stale, or has extra fields")


def preflight_release_state() -> None:
    release = json.loads((ROOT / "research/release-manifest.json").read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    expected_site = {
        "schemaVersion": "research-site-version-v1", "version": "1.42",
        "latestRelease": "R0.73B", "publicHtmlNoteCount": 178,
        "publishedDate": "2026-08-30",
    }
    if json.loads((PUBLIC / "site-version.json").read_text(encoding="utf-8")) != expected_site:
        raise RuntimeError("public site-version is not exactly at R0.73B")
    root_version = (ROOT / "VERSION").read_text(encoding="utf-8")
    if root_version not in {"1.41\n", "1.42\n"}:
        raise RuntimeError("root VERSION is neither the known 1.41 drift nor corrected R0.73B v1.42")
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 178:
        raise RuntimeError("R0.73B preflight expected 178 public HTML notes")
    for relative in (
        "notes/r0-73c.html", "notes/r0-73c.pdf",
        "recap-r0-61-r0-73c.html", "recap-r0-61-r0-73c.pdf",
    ):
        if (PUBLIC / relative).exists():
            raise RuntimeError(f"R0.73B preflight found premature public output: {relative}")
    home = (PUBLIC / "research-review.html").read_text(encoding="utf-8")
    for token in (
        'data-site-version="1.42"', "<strong>178</strong>公开研究笔记",
        "<strong>R0.73B</strong>最新研究节点", 'aria-label="R0.69P–R0.73B"',
    ):
        if token not in home:
            raise RuntimeError(f"R0.73B home baseline missing token: {token}")
    if 'data-release="r073c"' in home:
        raise RuntimeError("R0.73B home already contains an R0.73C card")
    recap = (PUBLIC / "recap-r0-61-r0-73b.html").read_text(encoding="utf-8")
    start = recap.index('<section id="node-index">')
    end = recap.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', recap[start:end])
    if len(links) != 118 or len(set(links)) != 118:
        raise RuntimeError("R0.73B recap baseline must contain 118 unique nodes")
    inventory = json.loads((ROOT / "research/formal-archive-inventory.json").read_text(encoding="utf-8"))
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073b", 80, 56, 24):
        raise RuntimeError("formal archive inventory is not at R0.73B")


def _binding_paths(manifest: dict) -> set[str]:
    rows = manifest.get("sourceBindings", manifest.get("bindings", []))
    return {str(row.get("path", "")) for row in rows if isinstance(row, dict)}


def _verify_experiment_manifest() -> None:
    directory = ROOT / EXPERIMENT_RELATIVE
    manifest = json.loads((directory / "manifest.json").read_text(encoding="utf-8"))
    if str(manifest.get("release", "R0.73C")).upper() != "R0.73C":
        raise RuntimeError("R0.73C experiment release mismatch")
    for row in manifest.get("sourceBindings", manifest.get("sources", [])):
        relative = str(row.get("path", ""))
        path = ROOT / relative if relative.startswith(("research/", "experiments/")) else directory / relative
        if not path.is_file() or digest(path) != row.get("sha256"):
            raise RuntimeError(f"R0.73C experiment source hash mismatch: {row.get('path')}")
    if manifest.get("source"):
        path = directory / str(manifest["source"])
        if not path.is_file() or digest(path) != manifest.get("sourceSha256"):
            raise RuntimeError("R0.73C primary experiment source hash mismatch")
    output_rows = [
        *manifest.get("rawEvidence", []),
        *manifest.get("generatedOutputs", []),
        *manifest.get("outputs", []),
    ]
    for row in output_rows:
        path = directory / str(row.get("path", ""))
        if not path.is_file() or path.stat().st_size != row.get("bytes") or digest(path) != row.get("sha256"):
            raise RuntimeError(f"R0.73C experiment output hash mismatch: {row.get('path')}")
    validation = json.loads((directory / "validation.json").read_text(encoding="utf-8"))
    if validation.get("status") != "passed" or not all(validation.get("checks", {}).values()):
        raise RuntimeError("R0.73C experiment validation failed")


def validate_inputs() -> None:
    required_inputs = (
        "research/r073c_report-source.md", "research/r073c_problem_freeze.md",
        "research/r073c_literature_audit.md", "research/r073c_gap_matrix.md",
        "research/r073c_monodromy_proof.md", "research/r073c_independent_analytic_audit.md",
        f"{CERTIFICATE_RELATIVE}/README.md", f"{CERTIFICATE_RELATIVE}/certificate.json",
        f"{CERTIFICATE_RELATIVE}/crosscheck.json", f"{CERTIFICATE_RELATIVE}/manifest.json",
        f"{EXPERIMENT_RELATIVE}/manifest.json", f"{EXPERIMENT_RELATIVE}/contract.json",
        f"{EXPERIMENT_RELATIVE}/summary.json", f"{EXPERIMENT_RELATIVE}/validation.json",
        f"{EXPERIMENT_RELATIVE}/interval_run_a.json", f"{EXPERIMENT_RELATIVE}/interval_run_b.json",
        f"{EXPERIMENT_RELATIVE}/decimal_interval_validation.json",
        f"{EXPERIMENT_RELATIVE}/fourier_screen.json",
        f"{EXPERIMENT_RELATIVE}/independent_fourier_validation.json",
        f"{FIGURE_RELATIVE}/manifest.json", f"{FIGURE_RELATIVE}/contract.json",
        f"{FIGURE_RELATIVE}/config.json", f"{FIGURE_RELATIVE}/caption.md",
        f"{FIGURE_RELATIVE}/README.md", f"{FIGURE_RELATIVE}/validate.py",
        "scripts/i18n-snapshots/r073c-missing.json",
        "public/notes/r0-73b.html", "public/recap-r0-61-r0-73b.html",
    )
    for relative in required_inputs:
        if not (ROOT / relative).is_file():
            raise RuntimeError(f"missing R0.73C release input: {relative}")
    report = (ROOT / "research/r073c_report-source.md").read_text(encoding="utf-8")
    for token in (
        "exactCubicNeutralSpectrum=CLOSED",
        "infiniteDimensionalFrozenRayleighInstability=CLOSED",
        "frozenInstabilityFastTimeTransfer=OPEN",
        "superPolynomialCompleteRowNoGo=CONDITIONAL",
        "sharpLargeLambdaGrowthLaw=OPEN", "completeOSSquireA2DirectSum=OPEN",
        "nonlinearNavierStokes=OPEN", "Clay=OPEN",
    ):
        if token not in report:
            raise RuntimeError(f"R0.73C report missing final stable token: {token}")
    if "TO_PROVE" in report or "TO_DISPROVE" in report:
        raise RuntimeError("R0.73C report still contains candidate-only claim states")
    audit = (ROOT / "research/r073c_independent_analytic_audit.md").read_text(encoding="utf-8")
    for token in ("Decision:", "pass", "Pöschl", "monodromy", "Decimal", "C5", "OPEN"):
        if token not in audit:
            raise RuntimeError(f"R0.73C independent audit missing token: {token}")

    certificate = ROOT / CERTIFICATE_RELATIVE
    figure = ROOT / FIGURE_RELATIVE
    verify_flat_hash_ledger(certificate, "R0.73C certificate")
    verify_flat_hash_ledger(figure, "R0.73C figure")
    certificate_manifest = json.loads((certificate / "manifest.json").read_text(encoding="utf-8"))
    certificate_payload = json.loads((certificate / "certificate.json").read_text(encoding="utf-8"))
    crosscheck = json.loads((certificate / "crosscheck.json").read_text(encoding="utf-8"))
    if certificate_manifest.get("status") != "formal" or certificate_payload.get("certificateStage") != "formal":
        raise RuntimeError("R0.73C certificate is not formal")
    source_commit = str(certificate_payload.get("sourceCommit", ""))
    if not re.fullmatch(r"[0-9a-f]{40}", source_commit):
        raise RuntimeError("R0.73C certificate source commit is absent")
    if crosscheck.get("status") != "passed":
        raise RuntimeError("R0.73C independent crosscheck is not passed")
    expected_bound_sources = {
        "research/r073c_report-source.md", "research/r073c_problem_freeze.md",
        "research/r073c_literature_audit.md", "research/r073c_gap_matrix.md",
        "research/r073c_monodromy_proof.md", "research/r073c_independent_analytic_audit.md",
        "research/r073c_interval_monodromy.py",
        "experiments/r073c/independent_decimal_monodromy_validator.py",
        "experiments/r073c/independent_fourier_spectral_validator.py",
        "experiments/r073c/manifest.json", "experiments/r073c/validation.json",
        "research/certificates/r073c/generate_certificate.py",
        "research/certificates/r073c/independent_recompute.py",
        "research/certificates/r073c/validate_certificate.py",
        "scripts/generate_r073c_release.py", "scripts/add-r073c-translations.mjs",
        "scripts/i18n-snapshots/r073c-missing.json",
        "tests/r073c-rayleigh-instability-gate.test.mjs", "tests/r073c-release.test.mjs",
        "tests/r073c-deterministic-certificate-source.test.mjs",
        "tests/r073c-certified-rayleigh-instability-figure-source.test.mjs",
        f"{FIGURE_RELATIVE}/contract.json", f"{FIGURE_RELATIVE}/config.json",
        f"{FIGURE_RELATIVE}/caption.md", f"{FIGURE_RELATIVE}/README.md",
    }
    missing_bindings = expected_bound_sources - _binding_paths(certificate_manifest)
    if missing_bindings:
        raise RuntimeError(f"R0.73C formal source binding is incomplete: {sorted(missing_bindings)}")
    subprocess.run(
        [sys.executable, str(certificate / "validate_certificate.py"), "--require-formal"],
        cwd=ROOT, check=True,
    )
    _verify_experiment_manifest()

    figure_manifest = json.loads((figure / "manifest.json").read_text(encoding="utf-8"))
    figure_contract = json.loads((figure / "contract.json").read_text(encoding="utf-8"))
    if (
        figure_manifest.get("release") != "R0.73C"
        or figure_manifest.get("figureId") != FIGURE_ID
        or figure_manifest.get("status") != "formal"
    ):
        raise RuntimeError("R0.73C figure identity or formal status mismatch")
    if (
        figure_manifest.get("qa", {}).get("status") != "passed"
        or figure_manifest.get("qa", {}).get("visualInspectionExplicit") is not True
    ):
        raise RuntimeError("R0.73C figure visual QA is not formal")
    claims = figure_contract.get("claimBoundary", {})
    for key in (
        "rootUniqueness", "algebraicSimplicity", "viscousSpectralPersistence",
        "nonautonomousTransfer", "nonlinearNavierStokesClosure",
        "clayMillenniumProblemSolved",
    ):
        if claims.get(key) is not False:
            raise RuntimeError(f"R0.73C figure escaped OPEN boundary: {key}")
    subprocess.run([sys.executable, str(figure / "validate.py")], cwd=ROOT, check=True)
    if figure_manifest.get("publication", {}).get("directory") != "public/assets/r073c":
        raise RuntimeError("R0.73C figure publication directory mismatch")


def publish_figure_assets() -> None:
    figure = ROOT / FIGURE_RELATIVE
    target = PUBLIC / "assets/r073c"
    target.mkdir(parents=True, exist_ok=True)
    for suffix in ("pdf", "svg", "png"):
        source = figure / f"figure.{suffix}"
        destination = target / f"{FIGURE_ID}.{suffix}"
        shutil.copyfile(source, destination)
        if digest(destination) != digest(source):
            raise RuntimeError(f"R0.73C public {suffix} is not byte-identical")


def build_note() -> None:
    html = (PUBLIC / "notes/r0-73b.html").read_text(encoding="utf-8")
    for label, pattern, value in (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="研究笔记 R0.73C：三次中性谱与经区间认证的无穷维冻结 Rayleigh 不稳定；黏性快时间传递仍开放。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.73C｜Certified frozen Rayleigh instability">'),
        ("og description", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="C3 与 C4 CLOSED；C5 OPEN；C6 CONDITIONAL；nonlinear 与 Clay 保持 OPEN。">'),
        ("og image", r'<meta property="og:image" content=".*?">', '<meta property="og:image" content="https://kasifa.github.io/assets/r073c/fig-r073c-certified-rayleigh-instability.png">'),
        ("title", r'<title>.*?</title>', '<title>R0.73C｜Certified frozen Rayleigh instability</title>'),
    ):
        html = section(html, pattern, value, "C note " + label)
    html = required(html, "/i18n-en.js?v=1.42", "/i18n-en.js?v=1.43", "C note i18n")
    nav = '<nav><a href="#result">结论</a><a href="#operator">算子</a><a href="#neutral">中性谱</a><a href="#singular">奇异边界</a><a href="#monodromy">单值矩阵</a><a href="#interval">区间证明</a><a href="#independent">独立复算</a><a href="#finite">有限诊断</a><a href="#transfer">C5</a><a href="#conditional">条件推论</a><a href="#evidence">证据</a><a href="#figure">附图</a><a href="#value">价值</a><a href="#next">下一步</a><a href="#reproduce">复现</a><a href="/">返回主页</a></nav>'
    html = section(html, r'<nav><a href="#result">.*?</nav>', nav, "C note nav")
    html = section(html, r'    <header class="hero">.*?</header>', NOTE_HERO, "C note hero")
    toc_items = [
        ("result", "00 · direct decision"), ("operator", "01 · frozen operator"),
        ("neutral", "02 · cubic neutral level"), ("singular", "03 · singular boundary"),
        ("monodromy", "04 · periodic monodromy"), ("interval", "05 · interval theorem"),
        ("independent", "06 · independent arithmetic"), ("finite", "07 · finite diagnostic"),
        ("transfer", "08 · C5 correction"), ("conditional", "09 · conditional consequence"),
        ("evidence", "10 · evidence boundary"), ("figure", "11 · journal figure"),
        ("value", "12 · value"), ("next", "13 · R0.73D"),
        ("reproduce", "14 · reproduction"),
    ]
    toc = '      <aside class="toc"><strong>CONTENTS</strong><ol>\n' + "".join(
        f'        <li><a href="#{anchor}">{label}</a></li>' for anchor, label in toc_items
    ) + '\n      </ol></aside>'
    html = section(html, r'      <aside class="toc">.*?</aside>', toc, "C note toc")
    html = section(html, r'      <article>.*?</article>', NOTE_ARTICLE, "C note article")
    html = section(
        html, r'<footer>.*?</footer>',
        '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>研究笔记 R0.73C · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>',
        "C note footer",
    )
    for stale in ("fig-r073b-bloch-kinetic-transient", "R0.73B scoped linear theorem"):
        if stale in html:
            raise RuntimeError(f"R0.73C note contains stale R0.73B copy: {stale}")
    assert_clean(html, "R0.73C note")
    assert_mathjax_clean(html, "R0.73C note")
    (PUBLIC / "notes/r0-73c.html").write_text(html, encoding="utf-8")


def build_recap() -> None:
    html = (PUBLIC / "recap-r0-61-r0-73b.html").read_text(encoding="utf-8")
    for label, pattern, value in (
        ("description", r'<meta name="description" content=".*?">', '<meta name="description" content="R0.60 之后的研究回顾：完整覆盖 R0.61 到 R0.73C 的 119 个节点；最新一节闭合精确三次中性谱与一条无穷维冻结 Rayleigh 不稳定。">'),
        ("og title", r'<meta property="og:title" content=".*?">', '<meta property="og:title" content="R0.61–R0.73C｜R0.60 之后的研究回顾">'),
        ("og description", r'<meta property="og:description" content=".*?">', '<meta property="og:description" content="三十八个阶段、119 个节点：从约化递推到经区间认证的冻结 Rayleigh 不稳定。">'),
        ("title", r'<title>.*?</title>', '<title>R0.61–R0.73C｜R0.60 之后的研究回顾</title>'),
    ):
        html = section(html, pattern, value, "C recap " + label)
    html = required(html, "/i18n-en.js?v=1.42", "/i18n-en.js?v=1.43", "C recap i18n")
    hero = r'''    <header class="hero"><div class="hero-inner">
      <div><div class="eyebrow">累计回顾 · R0.61–R0.73C · 2026-08-30</div><h1>R0.60 之后的研究回顾</h1><p class="lead">这页完整保留 R0.61 到 R0.73C 的 119 个研究节点。路线从约化递推、完整 Fourier--Leray 结构和临界账本，推进到 scalar A2 collision、完整线性 physical-kinetic direct sum；R0.73C 又证明固定碰撞剖面存在真正的无穷维冻结 Rayleigh 不稳定。黏性快时间传递、A2、nonlinear 与 Clay 没有被外推。</p></div>
      <div class="stamp"><span class="state">累计回顾</span><strong>R0.61–R0.73C</strong><p>收录节点：119</p><p>回顾截止时公开笔记：179</p><p>回顾截止节点：R0.73C</p><p>问题状态：仍未解决</p></div>
    </div></header>'''
    html = section(html, r'    <header class="hero">.*?</header>', hero, "C recap hero")
    for old, new in (
        ("02 · 118 节完整索引", "02 · 119 节完整索引"),
        ("01 · 三十七个研究阶段", "01 · 三十八个研究阶段"),
        ("R0.60 之后的路线分成三十七个阶段", "R0.60 之后的路线分成三十八个阶段"),
        ('data-current-route="R0.69P–R0.73B"', 'data-current-route="R0.69P–R0.73C"'),
    ):
        html = required(html, old, new, "C recap counter")
    result = r'''        <section id="result"><div class="section-no">00 / 回顾范围</div><h2>版本数、封存数和数学结论分开报告</h2><div class="metrics"><div class="metric"><strong>119</strong><span>R0.61–R0.73C 研究节点</span></div><div class="metric"><strong>81</strong><span>R0.70A–R0.73C 已公开版本</span></div><div class="metric"><strong>57</strong><span>当前 formal-figure 合同下完整封存</span></div><div class="metric"><strong>24</strong><span>旧版附图档案待回补</span></div></div><p>R0.00–R0.60 的内容保留在上一份阶段回顾中。R0.70A–R0.73C 的 81 个版本已公开，其中 57 个满足当前 formal-figure 完整封存合同。公开和封存不表示 Clay 问题已经解决。</p></section>'''
    html = section(html, r'        <section id="result">.*?</section>', result, "C recap result")
    phase = r'''            <article class="phase"><h3>R0.73C · Exact cubic level and certified frozen Rayleigh instability</h3><p>周期 Sobolev 模态与 Pöschl--Teller 谱闭合 exactCubicNeutralSpectrum；周期单值矩阵的实迹、连续性和两端严格区间异号闭合 infiniteDimensionalFrozenRayleighInstability。</p><p>独立 Decimal 内核复算同一符号；Fourier--Galerkin 值只作为 finite diagnostic，不承担无穷维证明。</p><p>frozenInstabilityFastTimeTransfer 为 OPEN；superPolynomialCompleteRowNoGo 为 CONDITIONAL；sharp large-\(|\Lambda|\) law、complete OS--Squire A2 direct sum、nonlinearNavierStokes 与 Clay 保持 OPEN。</p><div class="links"><a href="/notes/r0-73c.html">R0.73C</a><a href="/assets/r073c/fig-r073c-certified-rayleigh-instability.pdf">R0.73C 附图</a><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073c">R0.73C 证书</a></div></article>
'''
    marker = '          </div>\n        </section>\n\n        <section id="node-index">'
    html = once(html, marker, phase + marker, "C recap phase")
    html = required(html, "R0.61–R0.73B 的 118 节公开笔记", "R0.61–R0.73C 的 119 节公开笔记", "C recap node title")
    node_b = '            <span class="node-ref"><a href="/notes/r0-73b.html">R0.73B</a><span class="node-state kind-closed">闭</span></span>\n'
    node_c = '            <span class="node-ref"><a href="/notes/r0-73c.html">R0.73C</a><span class="node-state kind-closed">闭</span></span>\n'
    html = once(html, node_b, node_b + node_c, "C recap node")
    retained = r'''            <li>R0.73C 闭合 exact cubic neutral spectrum 与一条 infinite-dimensional frozen Rayleigh instability；它同时把 viscous fast-time transfer 保留为 OPEN，把 super-polynomial complete-row no-go 保留为 CONDITIONAL。</li>
'''
    html = once(html, "          </ul>\n          <p>这些结果可以分别整理成", retained + "          </ul>\n          <p>这些结果可以分别整理成", "C recap retained")
    html = section(html, r'        <section id="value">.*?</section>', r'''        <section id="value"><div class="section-no">04 / 目前的判断</div><h2>冻结谱不稳定已成为定理；vanishing-viscosity persistence 是新的硬门</h2><p>不能把 119 个节点或 81 个公开版本解释成 Clay 问题完成比例。R0.73C 的严格增量是精确三次中性谱、无穷维周期 ODE 区间证书和独立算术复核；直接 Clay 价值仍有限，因为只处理一条冻结二维线性行。</p></section>''', "C recap value")
    html = section(html, r'        <section id="next">.*?</section>', r'''        <section id="next"><div class="section-no">05 / 下一步</div><h2>R0.73D 研究 vanishing-viscosity Evans/Riesz persistence</h2><p>先闭合冻结黏性特征值、共同 Riesz 围道与补空间 resolvent，再进入非自治 graph-domain Kato transport。</p></section>''', "C recap next")
    html = section(html, r'        <section id="claims">.*?</section>', r'''        <section id="claims"><div class="section-no">06 / 说明边界</div><h2>公开、完整封存与问题解决继续分开计数</h2><p>R0.70A–R0.73C 的 81 节已公开；57 节完整封存；24 节旧档待回补。</p><p>exactCubicNeutralSpectrum 与 infiniteDimensionalFrozenRayleighInstability 为 CLOSED；frozenInstabilityFastTimeTransfer、sharpLargeLambdaGrowthLaw、completeOSSquireA2DirectSum、nonlinearNavierStokes 与 Clay 为 OPEN；superPolynomialCompleteRowNoGo 为 CONDITIONAL。</p></section>''', "C recap claims")
    html = section(html, r'        <section id="reproduce">.*?</section>', r'''        <section id="reproduce"><div class="section-no">07 / 原始资料</div><h2>逐节笔记、正式证书、区间实验、附图和历史回顾</h2><p><a href="/recap-r0-60.html">阅读 R0.00–R0.60 阶段回顾</a> · <a href="/recap-r0-61-r0-73b.html">保留 R0.73B 历史回顾</a> · <a href="/notes/r0-61.html">从 R0.61 开始逐节阅读</a> · <a href="/notes/r0-73c.html">打开最新节点 R0.73C</a></p><p><a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research">浏览完整 research 档案</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/research/certificates/r073c">查看 R0.73C 正式证书</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/tree/main/experiments/r073c">查看双区间内核与有限诊断</a> · <a href="/assets/r073c/fig-r073c-certified-rayleigh-instability.pdf">下载期刊附图</a> · <a href="/recap-r0-61-r0-73c.pdf">下载同步 PDF</a></p><p>严格端点异号来自无穷维周期 ODE 的 validated Picard--Taylor enclosure；独立 Decimal 内核复算同一符号。Fourier screen 只做定位和排错，不证明 tail、Riesz 投影、黏性延拓或 nonlinear convolution。</p><p>完整节点索引保留 R0.61 起的全部历史编号；状态标签只描述证据类型。</p></section>''', "C recap reproduce")
    html = section(html, r'<footer>.*?</footer>', '<footer><div><strong>三维 Navier–Stokes 全局正则性问题</strong><br>我按原编号记录推导、反例和未解决的问题。</div><div>R0.61–R0.73C 回顾 · 2026-08-30<br><a href="/">返回研究主页</a></div></footer>', "C recap footer")
    start = html.index('<section id="node-index">')
    end = html.index("</section>", start)
    links = re.findall(r'href="/notes/(r0-[^"]+)\.html"', html[start:end])
    if len(links) != 119 or len(set(links)) != 119 or html.count('<article class="phase">') != 38:
        raise RuntimeError("R0.73C recap expected 119 unique nodes and 38 phases")
    assert_clean(html, "R0.73C recap")
    assert_mathjax_clean(html, "R0.73C recap", check_naked=False)
    (PUBLIC / "recap-r0-61-r0-73c.html").write_text(html, encoding="utf-8")


def update_home() -> None:
    path = PUBLIC / "research-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ('data-site-version="1.42"', 'data-site-version="1.43"'),
        ("/i18n-en.js?v=1.42", "/i18n-en.js?v=1.43"),
        ("/site-refresh.js?v=1.42", "/site-refresh.js?v=1.43"),
        ("<strong>v1.42</strong>网页版本", "<strong>v1.43</strong>网页版本"),
        ("<strong>178</strong>公开研究笔记", "<strong>179</strong>公开研究笔记"),
        ("<strong>R0.73B</strong>最新研究节点", "<strong>R0.73C</strong>最新研究节点"),
        ("Research topology · R0.1–R0.73B", "Research topology · R0.1–R0.73C"),
        ('<a class="route-map-latest" href="#r073b">阅读 R0.73B 研究笔记 →</a>', '<a class="route-map-latest" href="#r073c">阅读 R0.73C 研究笔记 →</a>'),
        ("R0.70A–R0.73B：80 节已公开，56 节完整封存", "R0.70A–R0.73C：81 节已公开，57 节完整封存"),
        ('<span class="route-range">R0.69P–R0.73B</span>', '<span class="route-range">R0.69P–R0.73C</span>'),
        ('aria-label="R0.69P–R0.73B"', 'aria-label="R0.69P–R0.73C"'),
        ("展开 88 篇公开笔记", "展开 89 篇公开笔记"),
        ("本站 R0.69P–R0.73B 路线", "本站 R0.69P–R0.73C 路线"),
        ("综述 v1.42 · 2026-08-30", "综述 v1.43 · 2026-08-30"),
        ("上次综述 v1.41 · 2026-08-29", "上次综述 v1.42 · 2026-08-30"),
        ("/recap-r0-61-r0-73b.html", "/recap-r0-61-r0-73c.html"),
        ("/recap-r0-61-r0-73b.pdf", "/recap-r0-61-r0-73c.pdf"),
        ('<strong style="color:var(--gold)">下一步 R0.73C：</strong>&nbsp;sharp large-\(|\Lambda|\) transient law。', '<strong style="color:var(--gold)">当时的下一步 R0.73C：</strong>&nbsp;sharp large-\(|\Lambda|\) transient law。'),
    ):
        html = required(html, old, new, "C home " + old)
    html = section(html, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', r'<div class="summary-item"><strong>我目前关注</strong><span>R0.73C 已闭合 exact cubic neutral spectrum 与一条 infinite-dimensional frozen Rayleigh instability。下一关是 vanishing-viscosity Evans/Riesz persistence。</span></div>', "C home focus")
    spotlight_marker = '    </div>\n\n    <section class="route-overview" id="route-map"'
    html = once(
        html,
        spotlight_marker,
        '    </div>\n\n' + HOME_LATEST_SPOTLIGHT + '\n\n    <section class="route-overview" id="route-map"',
        "C home latest spotlight",
    )
    html = required(
        html,
        '<div class="task-one" id="r069v" style="margin-top:2rem">',
        '<div class="task-one" id="r069v" data-history="true" style="margin-top:2rem">',
        "C home R0.69V historical marker",
    )
    html = required(html, "<p class=\"eyebrow\">研究笔记 R0.69V · 2026-08-21</p>", "<p class=\"eyebrow\">历史研究笔记 R0.69V · 2026-08-21</p>", "C home R0.69V historical label")
    html = required(
        html,
        '<div class="task-one" id="r069w" style="margin-top:2rem">',
        '<div class="task-one" id="r069w" data-history="true" style="margin-top:2rem">',
        "C home R0.69W historical marker",
    )
    html = required(html, "<p class=\"eyebrow\">研究笔记 R0.69W · 2026-08-24</p>", "<p class=\"eyebrow\">历史研究笔记 R0.69W · 2026-08-24</p>", "C home R0.69W historical label")
    html = required(html, "<h3>R0.73B：viscous-rate physical-kinetic direct sum 已闭合</h3>", "<h3>R0.73C：无穷维冻结 Rayleigh 不稳定已闭合</h3>", "C home current title")
    html = required(html, "<span>R0.72R–R0.73B：</span>", "<span>R0.72R–R0.73C：</span>", "C home current path")
    html = required(html, "hidden-mean transient → Bloch physical-kinetic direct sum</p>", "hidden-mean transient → Bloch physical-kinetic direct sum → certified frozen Rayleigh instability</p>", "C home current path tail")
    link_b = '<a class="milestone" href="/notes/r0-73b.html">R0.73B</a>'
    html = once(html, link_b, link_b + '\n                  <a class="milestone" href="/notes/r0-73c.html">R0.73C</a>', "C home route link")
    route_c = r'''              <p>R0.73C 用周期 Sobolev 模态与 Pöschl--Teller 谱闭合 exact cubic neutral spectrum，再由周期单值矩阵实迹和双区间严格异号闭合一条 infinite-dimensional frozen Rayleigh instability。viscous fast-time transfer 为 OPEN；super-polynomial complete-row no-go 为 CONDITIONAL；A2、nonlinear 与 Clay 保持 OPEN。</p>
'''
    html = once(html, '              <details class="tree-notes" open>', route_c + '              <details class="tree-notes" open>', "C home route summary")
    html = section(html, r'            <article class="tree-node next">.*?</article>', HOME_NEXT, "C home next")
    recap = r'''          <div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计回顾 R0.61–R0.73C · 2026-08-30</p><h3>R0.60 recap 之后的累计回顾收录 119 个节点；全站现有 179 篇公开研究笔记</h3><p>累计回顾现分三十八个问题阶段，并给出 R0.61–R0.73C 的完整索引；R0.73C 分开记录 exact theorem、validated infinite-dimensional computation、finite diagnostic、conditional implication 与 open gate。</p><p>R0.70A–R0.73C 共 81 个版本已公开；57 个按当前 formal-figure 合同完整封存，24 个旧版附图档案仍列入回补清单。</p><p><strong>阶段判断：</strong>&nbsp;冻结 Rayleigh 不稳定已闭合；vanishing-viscosity transfer、A2、nonlinear 与 Clay 保持 OPEN。</p><p><a href="/recap-r0-61-r0-73c.html"><strong>阅读 R0.60 之后的完整累计回顾 →</strong></a> · <a href="/recap-r0-61-r0-73c.pdf">下载同步 PDF</a></p></div>'''
    html = section(html, r'          <div class="task-one" id="post-r060-recap".*?</div>', recap, "C home recap")
    html = once(html, '          </div>\n        </section>\n\n      </article>', '          </div>\n\n' + HOME_C_CARD + '\n        </section>\n\n      </article>', "C home card")
    if html.count('data-release="r073c"') != 1:
        raise RuntimeError("home must contain exactly one R0.73C card")
    if html.count('<strong style="color:var(--gold)">下一步 R0.73D：') != 1 or '<strong style="color:var(--gold)">下一步 R0.73C：' in html:
        raise RuntimeError("home must distinguish the unique current R0.73D gate from historical R0.73C")
    route = re.search(r'<nav class="route-note-links" aria-label="R0\.69P–R0\.73C">(.*?)</nav>', html, flags=re.S)
    if route is None or len(re.findall(r'href="/notes/r0-[^"]+\.html"', route.group(1))) != 89:
        raise RuntimeError("home current-route index must contain 89 note links")
    assert_clean(html, "R0.73C home")
    assert_mathjax_clean(html, "R0.73C home", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_literature() -> None:
    path = PUBLIC / "literature-review.html"
    html = path.read_text(encoding="utf-8")
    for old, new in (
        ("/i18n-en.js?v=1.42", "/i18n-en.js?v=1.43"),
        ("本站 R0.69P–R0.73B 只列为研究笔记", "本站 R0.69P–R0.73C 只列为研究笔记"),
        ("/recap-r0-61-r0-73b.html", "/recap-r0-61-r0-73c.html"),
        ("文献综述 v1.42 · 2026-08-30", "文献综述 v1.43 · 2026-08-30"),
        ("累计回顾与 118 节索引", "累计回顾与 119 节索引"),
        ("打开 118 节完整索引", "打开 119 节完整索引"),
    ):
        html = required(html, old, new, "C literature " + old)
    old_open = r'<div class="route-step pause"><header><b>开放接口 · R0.73C</b><strong>sharp large-Lambda transient law</strong></header><p>比较 exact lift-up lower bound、triangular low-gap limit 与 polynomial upper mechanism，再选择 A2 modulation 的正确权重。</p></div>'
    new_steps = r'''<div class="route-step kept"><header><b>R0.73C</b><strong>exact cubic level and certified frozen Rayleigh instability</strong></header><p>exact cubic neutral spectrum 与一条 infinite-dimensional frozen Rayleigh instability 已完成。viscous fast-time transfer 为 OPEN；super-polynomial complete-row no-go 为 CONDITIONAL。<a href="/notes/r0-73c.html">研究笔记</a> <a href="/recap-r0-61-r0-73c.html">当前累计回顾</a> <a href="#r073c-boundary">文献边界</a></p></div>
              <div class="route-step pause"><header><b>开放接口 · R0.73D</b><strong>vanishing-viscosity Evans/Riesz persistence</strong></header><p>先闭合黏性特征值延拓、统一 Riesz 投影和补空间 resolvent，再进入非自治 Kato transport。</p></div>'''
    html = once(html, old_open, new_steps, "C literature route")
    boundary = r'''

          <h3 id="r073c-boundary">R0.73C 的 cubic Rayleigh level、冻结不稳定与黏性传递文献边界</h3>
          <p>Lin 的 ideal plane-flow instability theorem、Bian--Grenier 的 degenerate Rayleigh singularity、Lin--Zeng 的 Hamiltonian index/trichotomy 和 Lin--Xu 的 periodic shear spectral theory 给出相邻工具，但没有一个来源已经验证本站三次零点剖面的完整 C3--C5 链。mpmath 1.3.0 只提供定向舍入算术；Picard enclosure、Taylor 余项、周期判据和 Rayleigh 符号桥仍由本站证明。限定的一手文献检索没有找到同时给出本剖面的周期单值异号与 uniform vanishing-viscosity Riesz/Kato package 的定理；这不是 novelty 或 priority proof。</p>
          <div class="boundary"><strong>R0.73C 的主张边界</strong><p>exactCubicNeutralSpectrum 与 infiniteDimensionalFrozenRayleighInstability 为 CLOSED。frozenInstabilityFastTimeTransfer、sharpLargeLambdaGrowthLaw、completeOSSquireA2DirectSum、nonlinearNavierStokes 与 Clay 为 OPEN；superPolynomialCompleteRowNoGo 为 CONDITIONAL。有限 Fourier contour 不被写成无穷维 Riesz 证书。</p></div>'''
    match = re.search(r'(<h3 id="r073b-boundary">.*?<div class="boundary">.*?</div>)', html, flags=re.S)
    if match is None:
        raise RuntimeError("C literature expected R0.73B boundary")
    html = once(html, match.group(1), match.group(1) + boundary, "C literature boundary")
    terminal = "R0.73B 再由 exact Bloch carrier cancellation 闭合 complete linear velocity/Squire rows 的 viscous-rate physical-kinetic direct sum。因而 low-gap vector direct sum at viscous rates 已为 CLOSED；complete OS--Squire A2 direct sum、sharp \\(|\\Lambda|\\) law、nonlinear Navier--Stokes 与 Clay 保持 OPEN。"
    terminal_c = terminal + "R0.73C 随后用 exact cubic neutral spectrum 与 validated periodic-ODE monodromy sign certificate 证明一条 infinite-dimensional frozen Rayleigh instability；viscous fast-time transfer 仍为 OPEN，super-polynomial complete-row no-go 只为 CONDITIONAL。"
    html = required(html, terminal, terminal_c, "C literature deck terminal")
    assert_clean(html, "R0.73C literature")
    assert_mathjax_clean(html, "R0.73C literature", check_naked=False)
    path.write_text(html, encoding="utf-8")


def update_manifests() -> None:
    if len(list((PUBLIC / "notes").glob("r0-*.html"))) != 179:
        raise RuntimeError("expected 179 public HTML notes after R0.73C")
    release_path = ROOT / "research/release-manifest.json"
    release = json.loads(release_path.read_text(encoding="utf-8"))
    _validate_source_stage_manifest(release)
    release.update({
        "latestCompletedRelease": "r073c", "siteVersion": "1.43",
        "publicHtmlNoteCount": 179, "postR060RecapNodeCount": 119,
        "nextRelease": "r073d",
        "latestReleaseGate": "tests/r073c-rayleigh-instability-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r073c-release.test.mjs",
        "postR070APublishedReleaseCount": 81,
        "postR070AFormalSealedReleaseCount": 57,
        "legacyFormalFigureBacklogCount": 24,
    })
    release.pop("nextReleaseSourceStage", None)
    release_path.write_text(json.dumps(release, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    site_path = PUBLIC / "site-version.json"
    site = json.loads(site_path.read_text(encoding="utf-8"))
    if (site.get("version"), site.get("latestRelease"), site.get("publicHtmlNoteCount")) != ("1.42", "R0.73B", 178):
        raise RuntimeError("site-version is not at R0.73B")
    site.update({
        "version": "1.43", "latestRelease": "R0.73C",
        "publicHtmlNoteCount": 179, "publishedDate": "2026-08-30",
    })
    site_path.write_text(json.dumps(site, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    inventory_path = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
    state = (
        inventory.get("latestPublishedRelease"), inventory.get("publishedReleaseCount"),
        inventory.get("formalSealedReleaseCount"), inventory.get("legacyFormalFigureBacklogCount"),
    )
    if state != ("r073b", 80, 56, 24):
        raise RuntimeError("formal archive inventory is not at R0.73B")
    for key in ("publishedReleases", "formalSealedReleases"):
        if inventory[key][-1] != "r073b" or "r073c" in inventory[key]:
            raise RuntimeError(f"formal archive {key} is not append-only from R0.73B")
        inventory[key].append("r073c")
    inventory.update({
        "latestPublishedRelease": "r073c", "publishedReleaseCount": 81,
        "formalSealedReleaseCount": 57, "legacyFormalFigureBacklogCount": 24,
    })
    if len(inventory["publishedReleases"]) != 81 or len(inventory["formalSealedReleases"]) != 57:
        raise RuntimeError("formal archive count mismatch after R0.73C")
    inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (ROOT / "VERSION").write_text("1.43\n", encoding="utf-8")


def update_note_index() -> None:
    # The synchronized note PDF is rendered immediately after this source
    # transaction and before publication.  Render the deterministic index with
    # that required final-state link already present, without creating a fake
    # PDF placeholder.  The ordinary index checker will verify the same bytes
    # once the real PDF has been rendered.
    import generate_note_index as note_index

    note_index.PUBLIC = PUBLIC
    note_index.NOTES = PUBLIC / "notes"
    note_index.OUTPUT = note_index.NOTES / "index.html"
    notes = [note_index.parse_note(path) for path in note_index.note_files()]
    notes = [replace(note, has_pdf=True) if note.slug == "r0-73c" else note for note in notes]
    note_index.OUTPUT.write_text(note_index.render(notes), encoding="utf-8")
    index = (PUBLIC / "notes/index.html").read_text(encoding="utf-8")
    for token in (
        'data-site-version="1.43"', "179 篇公开研究笔记",
        "<strong>R0.73C</strong><span>最新研究节点</span>",
        'data-note="r0-73c"', "/recap-r0-61-r0-73c.html",
        "研究笔记总索引 · v1.43 · 2026-08-30",
    ):
        if token not in index:
            raise RuntimeError(f"R0.73C note index missing token: {token}")


def main() -> None:
    preflight_release_state()
    validate_inputs()
    publish_figure_assets()
    build_note()
    build_recap()
    update_home()
    update_literature()
    update_manifests()
    update_note_index()
    for relative in (
        "research-review.html", "literature-review.html", "notes/index.html",
        "notes/r0-73c.html", "recap-r0-61-r0-73c.html",
    ):
        content = (PUBLIC / relative).read_text(encoding="utf-8")
        assert_clean(content, relative)
        assert_mathjax_clean(content, relative, check_naked=False)
    print(json.dumps({
        "release": "R0.73C", "siteVersion": "1.43", "notes": 179,
        "recapNodes": 119, "published": 81, "formalSealed": 57,
        "legacyBacklog": 24, "phases": 38, "routeNotes": 89,
        "next": "R0.73D", "rootVersion": "1.43",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
