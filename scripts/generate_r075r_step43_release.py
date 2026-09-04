#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75R Step 43 from the verified R0.75Q Step 42 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075q_step42_release as previous
import import_r075r_step43_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "5662cd6acd41324dd9f6b58c458a24fd066055cc"
VERSION = "2.22"
RELEASE = "r075r"
CODE = "R0.75R"
TITLE = "R0.75R｜outer-cap 谱集中阻断 plateau-only 多模付款"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-75a.html": "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0",
    PUBLIC / "recap-r0-61-r0-75a.pdf": "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62",
}

sha256 = previous.sha256
write_text = previous.write_text
write_json = previous.write_json
replace_once = previous.replace_once
replace_pattern = previous.replace_pattern
inline_markup = previous.inline_markup


def baseline_text(relative: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{BASELINE_COMMIT}:{relative}"], cwd=ROOT, text=True
    )


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected R0.75A recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.75R frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075r_outer_cap_spectral_concentration_obstruction_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions") != 21
        or certificate.get("passed") != 21
        or len(certificate.get("checks", [])) != 21
    ):
        raise RuntimeError("R0.75R certificate verdict drift")
    main = (ROOT / "research/r075r_outer_cap_spectral_concentration_obstruction.md").read_text()
    for token in (
        r"\tag{R.1}",
        r"D_R(y)=\Xi_R'(y)",
        r"\tag{R.14}",
        r"G_K(y)=A\,d_n(y-y_0)^{2m}\cos(q(y-y_0))",
        r"\tag{R.23}",
        r"(\partial_t+B\partial_2-\partial_2^2)F_K=0",
        r"\tag{R.30}",
        r"\mathcal T_K",
        r"M_{K,{\rm plat}}",
        r"\tag{R.40}",
        r"\frac{304373}{952560000}>0",
        r"\tag{R.41}",
        "plateau-only",
        "not a counterexample to E.24",
        "No novelty or priority claim",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75R boundary drift: {token}")


def render_step43_sections() -> str:
    source = (ROOT / "research/r075r_outer_cap_spectral_concentration_obstruction.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 334
    for block in blocks:
        lines = [line.rstrip() for line in block.splitlines()]
        if lines[0].startswith("# "):
            continue
        if lines[0].startswith("## "):
            if section_open:
                output.append("</section>")
            section_index += 1
            heading = re.sub(r"^\d+\.\s*", "", lines[0][3:])
            output.append(
                f'<section id="s-{section_index:02d}"><div class="section-no">{section_index:02d} / 完整正文</div><h2>{inline_markup(heading)}</h2>'
            )
            section_open = True
            continue
        stripped = block.strip()
        if stripped.startswith(r"\[") and stripped.endswith(r"\]"):
            output.append(f'<div class="equation">{html.escape(stripped)}</div>')
        elif len(lines) >= 2 and lines[0].startswith("|") and re.match(r"^\|[-:| ]+\|$", lines[1]):
            rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
            cell_style = ' style="overflow-wrap:anywhere;word-break:break-word"'
            head = "".join(f"<th{cell_style}>{inline_markup(cell)}</th>" for cell in rows[0])
            body = "".join("<tr>" + "".join(f"<td{cell_style}>{inline_markup(cell)}</td>" for cell in row) + "</tr>" for row in rows[2:])
            output.append(f'<div class="table-wrap"><table style="table-layout:fixed;width:100%"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
        elif all(line.startswith("- ") or line.startswith("  ") for line in lines):
            items: list[str] = []
            current = ""
            for line in lines:
                if line.startswith("- "):
                    if current:
                        items.append(current)
                    current = line[2:]
                else:
                    current += " " + line.strip()
            if current:
                items.append(current)
            output.append("<ul>" + "".join(f"<li>{inline_markup(item)}</li>" for item in items) + "</ul>")
        else:
            output.append(f"<p>{inline_markup(stripped)}</p>")
    if section_open:
        output.append("</section>")
    if section_index != 343:
        raise RuntimeError(f"Step 43 reader section drift: {section_index}")
    # The PDF browser occasionally exposes \qquad as literal text in the
    # generated print layer.  Equivalent explicit thin-space pairs avoid that
    # renderer defect without changing the frozen Markdown source or formula.
    rendered = "\n".join(output).replace(r"\qquad", r"\;\;")
    return rendered.replace("qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.21"', 'data-site-version="2.22"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.21", "/i18n-en.js?v=2.22", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="An exact smooth high-band shear packet concentrates in an outer cap and rules out a uniform multimode payment using only the canonical plateau-shell cubic mass.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75r.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75R · STEP 43 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75R · Step 43 · OUTER-CAP SPECTRAL CONCENTRATION OBSTRUCTION</div><h1>{TITLE}</h1><p>一个显式 real high-band packet 可集中在 radial cutoff 的正 outer cap，并在一个 diffusive time 内保持固定比例能量；canonical plateau shell 只看到 Dirichlet tail。由此 <strong>signed flux / plateau cubic^(2/3)</strong> 以精确正指数发散，排除把 Q 的 plateau-only payment 无条件推广到任意 multimode packet。该反例是 exact global smooth Navier--Stokes shear solution，并不反驳 full-support payment、Version-M 或 E.24。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">NEGATIVE RESULT</span><span class="label">EXACT SMOOTH SHEAR</span><span class="label">REAL HIGH-BAND PACKET</span><span class="label">OUTER-CAP CONCENTRATION</span><span class="label">DIRICHLET KERNEL</span><span class="label">SIGNED FLUX LOWER</span><span class="label">PLATEAU CUBIC UPPER</span><span class="label">AMPLITUDE CANCELS</span><span class="label">EXPONENTIAL DIVERGENCE</span><span class="label">PLATEAU-ONLY NO-GO</span><span class="label">FULL SUPPORT OPEN</span><span class="label">VERSION-M OPEN</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75R STEP 43</strong><p>model：exact smooth constant shear</p><p>spectrum：K &lt;= |j| &lt;= 2K</p><p>location：positive outer cap</p><p>time：T = K^-2</p><p>plateau tail：(nR)^-2m</p><p>smallest rate：304373/952560000</p><p>ruled out：plateau-only multimode payment</p><p>not ruled out：full support / Version-M / E.24</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step43_sections() + '\n<section id="reproduce">', "Step 43 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 43 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075r_outer_cap_spectral_concentration_obstruction.md">Step 43 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075r_outer_cap_spectral_concentration_obstruction_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075r_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075r_outer_cap_spectral_concentration_obstruction_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075r_outer_cap_spectral_concentration_obstruction_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075r_outer_cap_spectral_concentration_obstruction_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075r_outer_cap_spectral_concentration_obstruction_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075r_outer_cap_spectral_concentration_obstruction_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075r_outer_cap_spectral_concentration_obstruction_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075r_outer_cap_spectral_concentration_obstruction_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075r_outer_cap_spectral_concentration_obstruction_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075r_outer_cap_spectral_concentration_obstruction_qa.sh">QA script</a></p><p><a href="/notes/r0-75r.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 21/21、Ruby 23/23、R.1--R.41、41/41 tags 与 43/43 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 76/76 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 43 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-328">← Step 42：spatially spread one-harmonic collar payment</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 43 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">full-support payment and signed multimode alternatives remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.75R Step 43 停止。R 只排除以 canonical plateau shell 的 cubic mass 支付任意 high-band multimode packet 的统一延伸；它不反驳 full cutoff support、Version-M exterior rows、quantitative spreading / thickness、signed multimode cancellation 或 E.24。nonconstant shear、nonlinear mode transfer、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 43 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.21"', 'data-site-version="2.22"', "home version"),
        ("/i18n-en.js?v=2.21", "/i18n-en.js?v=2.22", "home i18n"),
        ("/site-refresh.js?v=2.21.1", "/site-refresh.js?v=2.22.1", "home refresh"),
        ("<strong>v2.21</strong>网页版本", "<strong>v2.22</strong>网页版本", "home stat version"),
        ("<strong>R0.75Q</strong>最新研究节点", "<strong>R0.75R</strong>最新研究节点", "home latest"),
        ("<strong>245</strong>公开研究笔记", "<strong>246</strong>公开研究笔记", "home public count"),
        ("展开 155 篇公开笔记", "展开 156 篇公开笔记", "home route count"),
        ("综述 v2.21 · 2026-09-04", "综述 v2.22 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75Q", "Research topology · R0.1–R0.75R", "home topology"),
        ('href="#r075q">跳到首页 R0.75Q 卡片 →', 'href="#r075r">跳到首页 R0.75R 卡片 →', "home jump"),
        ("R0.70A–R0.75Q：147 节已公开，104 节完整封存", "R0.70A–R0.75R：148 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75Q</span>', '<span class="route-range">R0.69P–R0.75R</span>', "home range"),
        ("<h3>R0.75Q：空间铺展单谐波的 physical-collar payment</h3>", "<h3>R0.75R：outer-cap 谱集中阻断 plateau-only 多模付款</h3>", "home route title"),
        ("R0.72R–R0.75Q：</span>", "R0.72R–R0.75R：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75Q"', 'aria-label="R0.69P–R0.75R"', "home links label"),
        ("全站现有 245 篇公开研究笔记", "全站现有 246 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75R Step 43 构造 exact global smooth high-band shear packet：能量集中在正 outer cap，而 canonical plateau 只看到 Dirichlet tail，从而排除 plateau-only cubic mass 对任意 multimode packet 的统一付款。full support、Version-M 与 signed multimode alternatives 仍开放。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75R · 2026-09-04 · STEP 43 · OUTER-CAP SPECTRAL CONCENTRATION OBSTRUCTION</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">显式 real high-band packet 在正 outer cap 集中，并以 exact smooth constant-shear Navier--Stokes evolution 保持一个 diffusive time；plateau shell 只看到 Dirichlet tail。因此 flux-to-plateau-mass quotient 以精确正指数发散，排除 plateau-only multimode extension，但不反驳 full support、Version-M 或 E.24。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75r.pdf">阅读最新 R0.75R 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">246 篇研究笔记总索引</a><a href="#r075r">查看首页 R0.75R 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75R · 148 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75R Step 43 outer-cap spectral concentration obstruction</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 43 gives an exact smooth outer-cap-concentrated high-band packet and rules out a uniform plateau-only multimode payment; full-support payment, Version-M aggregation, and signed alternatives remain open.</p>', "home current summary")
    page = replace_once(page, 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row → vertical-diffusion packet gain → entrance-concentrated buffered-collar payment → spatially spread one-harmonic collar payment / multimode and general low-entrance packets open</p>', 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row → vertical-diffusion packet gain → entrance-concentrated buffered-collar payment → spatially spread one-harmonic collar payment → plateau-only multimode obstruction / full-support and signed alternatives open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75q.html">R0.75Q</a>', '<a class="milestone" href="/notes/r0-75q.html">R0.75Q</a>\n<a class="milestone" href="/notes/r0-75r.html">R0.75R</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>full-support payment and signed multimode alternatives remain open</h3><p>仍需检验 full cutoff support、Version-M exterior-row aggregation、quantitative spreading / thickness、signed multimode cancellation、nonconstant shear 与 nonlinear mode transfer；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075r" data-release="r075r" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75R Step 43 · 2026-09-04 · OUTER-CAP SPECTRAL CONCENTRATION OBSTRUCTION</p><h3>{TITLE}</h3><p>一个显式 real high-band packet 集中在正 outer cap，并作为 exact global smooth Navier--Stokes shear solution 演化；它在 plateau 上只留下 Dirichlet tail，使 normalized flux-to-plateau-mass quotient 以正指数发散。由此仅排除 plateau-only multimode payment，不排除 full support、Version-M 或 E.24。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75r.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75r.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075q"'
    if anchor not in page:
        raise RuntimeError("home R0.75Q card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.21"', 'data-site-version="2.22"', "literature version"),
        ("/i18n-en.js?v=2.21", "/i18n-en.js?v=2.22", "literature i18n"),
        ("文献综述 v2.21 · 2026-09-04", "文献综述 v2.22 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75Q 只列为研究笔记", "本站 R0.69P–R0.75R 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>multimode interference and general low-entrance packets remain open</strong></header><p>两个及以上 horizontal modes、destructive interference、arbitrary vertical structure、一般 low-entrance packet、nonconstant shear、inter-packet / low-difference summation 与移除 total upper-frequency cap 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75R</b><strong>outer-cap spectral concentration obstructs plateau-only multimode payment</strong></header><p>Step 43 构造 exact global smooth constant-shear solution：real high-band packet 在正 outer cap 集中并保持一个 diffusive time，plateau 只看到 Dirichlet tail；normalized flux-to-plateau-mass quotient 以正指数发散。结论只排除 plateau-only multimode extension，不反驳 full support、Version-M 或 E.24。<a href="/notes/r0-75r.html">研究笔记</a> <a href="#r075r-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>full-support payment and signed multimode alternatives remain open</strong></header><p>full cutoff support、Version-M exterior-row aggregation、quantitative spreading / thickness、signed multimode cancellation、nonconstant shear 与 nonlinear mode transfer 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075r-boundary">R0.75R Step 43 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Egidi--Veselić 2016 给出 torus 上带限函数的 Logvinenko--Sereda 型谱观测；Wang--Wang--Zhang--Zhang 2019 说明 heat observability 依赖 quantitative thickness；Coulhon--Sikora 2008 提供 Gaussian off-diagonal heat bounds 的广泛语境。R0.75R 只在一维周期热核上直接证明所需的短时 separated leakage，并用显式 Dirichlet packet 完成 outer-cap construction；这些相邻文献不替代本地证明。有限检索不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.75R Step 43 公开边界 · LIMITED NO-GO</strong><p>'
        'PROVED：exact radial cross-section identity R.12--R.14；real high-band support R.19--R.23；Dirichlet concentration/tails R.24--R.26；exact smooth Navier--Stokes shear realization R.29--R.30；outer-cap persistence R.31--R.34；positive signed-flux lower bound R.35；plateau cubic upper bound R.38；以及 divergent normalized quotient R.40--R.41。'
        'RULED OUT：只用 canonical plateau shell cubic mass 支付任意 high-band packet 的统一 Q-extension。'
        'NOT RULED OUT / OPEN：full cutoff support、complete Version-M exterior rows、quantitative spreading / thickness、signed multimode cancellation、arbitrary nonconstant shear、nonlinear mode transfer、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity。该 exact solution 全局光滑，不提供 singularity mechanism。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75r.html">阅读完整笔记</a> · '
        '<a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap</a>。</p></div>\n'
    )
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 246 or pdf_count not in (202, 203):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 186:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75r.html",
        "latestPublishedResearchPdf": "/notes/r0-75r.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075q":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 148
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 43
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "OUTER_CAP_SPECTRAL_CONCENTRATION_OBSTRUCTION_TO_PLATEAU_ONLY_MULTIMODE_PAYMENT",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": frozen_import.SOURCE_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_NEGATIVE_RESULT",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "constant_shear_model": "EXACT_GLOBAL_SMOOTH_UNFORCED_NAVIER_STOKES_R29_R30",
            "radial_cross_section_identity": "PROVED_R12_TO_R14",
            "outer_cap_geometry": "PROVED_R15_TO_R18",
            "real_high_band_packet": "PROVED_R19_TO_R23",
            "dirichlet_concentration_and_tails": "PROVED_R24_TO_R26",
            "outer_cap_persistence": "PROVED_R31_TO_R34",
            "signed_flux_lower_bound": "PROVED_R35",
            "plateau_cubic_upper_bound": "PROVED_R38",
            "normalized_divergence": "PROVED_R40_R41",
            "amplitude_dependence": "CANCELS_EXACTLY",
            "plateau_only_multimode_payment": "RULED_OUT_UNIFORMLY",
            "full_cutoff_support_payment": "OPEN_NOT_COUNTEREXAMPLE",
            "version_m_admissibility_and_aggregation": "OPEN_NOT_COUNTEREXAMPLE",
            "spectral_or_physical_spreading_hypothesis": "OPEN",
            "signed_multimode_cancellation": "OPEN",
            "nonlinear_mode_transfer": "OPEN",
            "nonconstant_shear": "OPEN_NOT_PROVED",
            "low_horizontal_difference_sector": "OPEN_NOT_PROVED",
            "E24": "OPEN_NOT_PROVED",
            "complete_clock": "OPEN_NOT_PROVED",
            "fixed_deletion": "OPEN_NOT_PROVED",
            "suitable_weak_transfer": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_12_OF_12",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_21_OF_21",
            "independent_ruby": "PASS_23_OF_23",
            "negative_mutations": "PASS_PYTHON_76_OF_76_RUBY_76_OF_76",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_R1_TO_R41_TAGS_41_OF_41_DISPLAYS_43_OF_43",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75r.html",
            "target_pdf": "/notes/r0-75r.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075r_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 43,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 148,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075s",
        "latestPublishedResearchHtml": "/notes/r0-75r.html",
        "latestPublishedResearchPdf": "/notes/r0-75r.pdf",
        "latestReleaseGate": "tests/r075r-step43-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075r-step43-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075r-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075r-step43-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075r-step43-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075r-step43-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075r-step43-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075r-step43",
            "handoffCommit": frozen_import.HANDOFF_COMMIT,
            "handoffSha256": frozen_import.HANDOFF_SHA256,
            "handoffIndependentAuditSha256": frozen_import.HANDOFF_AUDIT_SHA256,
            "sourceCommit": frozen_import.SOURCE_COMMIT,
            "coreCommit": frozen_import.SOURCE_COMMIT,
            "formalFigureRequired": False,
            "recapRequired": False,
        },
        "latestRecapRelease": "r075a",
        "latestRecapHtml": "/recap-r0-61-r0-75a.html",
        "latestRecapPdf": "/recap-r0-61-r0-75a.pdf",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256(inventory_target),
    }
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-75r.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 43,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 169,
        "formalFigure": None,
        "formalFigureExemption": True,
        "simulation": False,
        "pdeData": False,
        "noveltyClaim": False,
        "clayClaim": False,
        "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
