#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75S Step 44 from the verified R0.75R Step 43 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075r_step43_release as previous
import import_r075s_step44_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "7bb811294029e12a5421bfca04358654d04422c7"
VERSION = "2.23"
RELEASE = "r075s"
CODE = "R0.75S"
TITLE = "R0.75S｜单实谐波的全频率完整时钟 collar 付款"
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
            raise RuntimeError(f"R0.75S frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075s_full_frequency_single_harmonic_clock_payment_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions") != 21
        or certificate.get("passed") != 21
        or len(certificate.get("checks", [])) != 21
    ):
        raise RuntimeError("R0.75S certificate verdict drift")
    main = (ROOT / "research/r075s_full_frequency_single_harmonic_clock_payment.md").read_text()
    for token in (
        r"\tag{S.1}",
        r"D_R(y):=",
        r"\tag{S.13}",
        r"|S_{k,R}|\le C_NaR^2",
        r"\tag{S.17}",
        r"Q_\varepsilon(\psi)",
        r"\tag{S.22}",
        r"\tag{S.30}",
        r"\tag{S.38}",
        r"\tag{S.39}",
        r"u_k(t,x)=(0,B,F_k(t,x_2))",
        r"\tag{S.41}",
        "not a multimode estimate",
        "No novelty or",
        "priority claim is made",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75S boundary drift: {token}")


def render_step44_sections() -> str:
    source = (ROOT / "research/r075s_full_frequency_single_harmonic_clock_payment.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 343
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
    if section_index != 350:
        raise RuntimeError(f"Step 44 reader section drift: {section_index}")
    # The PDF browser occasionally exposes \qquad as literal text in the
    # generated print layer.  Equivalent explicit thin-space pairs avoid that
    # renderer defect without changing the frozen Markdown source or formula.
    rendered = "\n".join(output).replace(r"\qquad", r"\;\;")
    return rendered.replace("qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.22"', 'data-site-version="2.23"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.22", "/i18n-en.js?v=2.23", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="The complete frozen clock pays the physical radial-collar flux of every single real constant-drift harmonic at every integer frequency.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75s.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75S · STEP 44 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75S · Step 44 · FULL-FREQUENCY SINGLE-HARMONIC CLOCK PAYMENT</div><h1>{TITLE}</h1><p>在完整冻结时钟 <strong>T_R=4R^2</strong> 上，每个整数频率、任意振幅、相位和常 shear 的 single real harmonic 都满足 physical radial-collar 付款。证明用 exact radial reduction、moving-phase node lemma 与 high-frequency Fourier decay 覆盖全部频率；它不是 multimode 或 arbitrary-field 估计。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">POSITIVE THEOREM</span><span class="label">COMPLETE CLOCK</span><span class="label">ALL INTEGER FREQUENCIES</span><span class="label">ONE REAL HARMONIC</span><span class="label">EXACT SMOOTH SHEAR</span><span class="label">RADIAL REDUCTION</span><span class="label">MOVING-PHASE LEMMA</span><span class="label">LOW/HIGH COVERAGE</span><span class="label">AMPLITUDE CANCELS</span><span class="label">VERSION-M CONDITIONAL</span><span class="label">MULTIMODE OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75S STEP 44</strong><p>model：exact smooth constant shear</p><p>frequency：every integer k &gt;= 1</p><p>time：T_R = 4R^2</p><p>shear：arbitrary constant B</p><p>payment：a^(2/3) R^(-1/3) M^(2/3)</p><p>normalized rate：-2/11907</p><p>scope：one real harmonic</p><p>open：multimode / E.24 / Version-M</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step44_sections() + '\n<section id="reproduce">', "Step 44 sections")
    evidence = '''<section id="reproduce"><div class="section-no">S / 冻结证据</div><h2>Step 44 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075s_full_frequency_single_harmonic_clock_payment.md">Step 44 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075s_full_frequency_single_harmonic_clock_payment_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075s_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075s_full_frequency_single_harmonic_clock_payment_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075s_full_frequency_single_harmonic_clock_payment_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075s_full_frequency_single_harmonic_clock_payment_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075s_full_frequency_single_harmonic_clock_payment_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075s_full_frequency_single_harmonic_clock_payment_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075s_full_frequency_single_harmonic_clock_payment_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075s_full_frequency_single_harmonic_clock_payment_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075s_full_frequency_single_harmonic_clock_payment_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075s_full_frequency_single_harmonic_clock_payment_qa.sh">QA script</a></p><p><a href="/notes/r0-75s.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 21/21、Ruby 23/23、S.1--S.41、41/41 tags 与 42/42 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 76/76 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 44 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-335">← Step 43：outer-cap spectral concentration obstruction</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 44 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">multimode interference and packet aggregation remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.75S Step 44 停止。S 只证明 complete-clock physical-collar payment 对一个 real constant-drift harmonic 的全频率估计；它不适用于 Fourier projection、两个及以上 harmonics、nonconstant shear、arbitrary vertical structure 或 arbitrary-field E.24。Version-M admissibility/aggregation、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 44 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.22"', 'data-site-version="2.23"', "home version"),
        ("/i18n-en.js?v=2.22", "/i18n-en.js?v=2.23", "home i18n"),
        ("/site-refresh.js?v=2.22.1", "/site-refresh.js?v=2.23.1", "home refresh"),
        ("<strong>v2.22</strong>网页版本", "<strong>v2.23</strong>网页版本", "home stat version"),
        ("<strong>R0.75R</strong>最新研究节点", "<strong>R0.75S</strong>最新研究节点", "home latest"),
        ("<strong>246</strong>公开研究笔记", "<strong>247</strong>公开研究笔记", "home public count"),
        ("展开 156 篇公开笔记", "展开 157 篇公开笔记", "home route count"),
        ("综述 v2.22 · 2026-09-04", "综述 v2.23 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75R", "Research topology · R0.1–R0.75S", "home topology"),
        ('href="#r075r">跳到首页 R0.75R 卡片 →', 'href="#r075s">跳到首页 R0.75S 卡片 →', "home jump"),
        ("R0.70A–R0.75R：148 节已公开，104 节完整封存", "R0.70A–R0.75S：149 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75R</span>', '<span class="route-range">R0.69P–R0.75S</span>', "home range"),
        ("<h3>R0.75R：outer-cap 谱集中阻断 plateau-only 多模付款</h3>", "<h3>R0.75S：单实谐波的全频率 complete-clock collar payment</h3>", "home route title"),
        ("R0.72R–R0.75R：</span>", "R0.72R–R0.75S：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75R"', 'aria-label="R0.69P–R0.75S"', "home links label"),
        ("全站现有 246 篇公开研究笔记", "全站现有 247 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75S Step 44 在完整冻结时钟上支付每个 single real constant-drift harmonic 的 physical radial-collar flux，并移除 Q 的全部频率阈值。multimode interference、packet aggregation、nonconstant shear 与 arbitrary-field E.24 仍开放。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75S · 2026-09-04 · STEP 44 · FULL-FREQUENCY SINGLE-HARMONIC CLOCK PAYMENT</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">完整冻结时钟 <strong>T_R=4R^2</strong> 支付每个 single real constant-drift harmonic 的 physical radial-collar flux，覆盖全部整数频率且不限制 constant shear B。证明不是 multimode 或 arbitrary-field 估计；Version-M 的最后付款仍要求同一实际速度分量和完整时空对齐。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75s.pdf">阅读最新 R0.75S 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">247 篇研究笔记总索引</a><a href="#r075s">查看首页 R0.75S 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75S · 149 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75S Step 44 full-frequency single-harmonic clock payment</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 44 pays every integer frequency on the complete clock for one real constant-drift harmonic; multimode interference, packet aggregation, and arbitrary-field E.24 remain open.</p>', "home current summary")
    page = replace_once(page, 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row → vertical-diffusion packet gain → entrance-concentrated buffered-collar payment → spatially spread one-harmonic collar payment → plateau-only multimode obstruction / full-support and signed alternatives open</p>', 'single-harmonic diffusive signed-flux gain → dyadic-packet mode-count-free gain → canonical radial-collar averaged Wiener row → vertical-diffusion packet gain → entrance-concentrated buffered-collar payment → spatially spread one-harmonic collar payment → plateau-only multimode obstruction → full-frequency single-harmonic complete-clock payment / multimode interference open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75r.html">R0.75R</a>', '<a class="milestone" href="/notes/r0-75r.html">R0.75R</a>\n<a class="milestone" href="/notes/r0-75s.html">R0.75S</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>multimode interference and packet aggregation remain open</h3><p>仍需控制两个及以上 harmonics 的 cubic interference 与 pairwise difference frequencies，并处理 nonconstant shear、arbitrary vertical structure、Version-M admissibility/aggregation 与 arbitrary-field E.24；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075s" data-release="r075s" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75S Step 44 · 2026-09-04 · FULL-FREQUENCY SINGLE-HARMONIC CLOCK PAYMENT</p><h3>{TITLE}</h3><p>完整冻结时钟支付每个 single real constant-drift harmonic 的 physical radial-collar flux，覆盖全部整数频率、任意振幅、相位与 constant shear。normalized coefficient 的精确 L^2 rate 为 -2/11907；multimode、projection、nonconstant shear 与 arbitrary-field E.24 仍开放。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75s.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75s.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075r"'
    if anchor not in page:
        raise RuntimeError("home R0.75R card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.22"', 'data-site-version="2.23"', "literature version"),
        ("/i18n-en.js?v=2.22", "/i18n-en.js?v=2.23", "literature i18n"),
        ("文献综述 v2.22 · 2026-09-04", "文献综述 v2.23 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75R 只列为研究笔记", "本站 R0.69P–R0.75S 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>full-support payment and signed multimode alternatives remain open</strong></header><p>full cutoff support、Version-M exterior-row aggregation、quantitative spreading / thickness、signed multimode cancellation、nonconstant shear 与 nonlinear mode transfer 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    route = '<div class="route-step kept"><header><b>R0.75S</b><strong>full-frequency complete-clock payment for one real harmonic</strong></header><p>Step 44 在完整冻结时钟 T_R=4R^2 上，对 every integer k、任意 amplitude、phase 与 constant shear B 证明 physical radial-collar flux 的 a^(2/3)R^(-1/3)M_plat^(2/3) 付款。该 theorem 只覆盖一个实际 harmonic；multimode interference 与 arbitrary-field E.24 不在结论内。<a href="/notes/r0-75s.html">研究笔记</a> <a href="#r075s-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>multimode interference and packet aggregation remain open</strong></header><p>两个及以上 harmonics 的 cubic interference、pairwise difference frequencies、nonconstant shear、arbitrary vertical structure、Version-M admissibility/aggregation 与 arbitrary-field E.24 仍未闭合；后续材料未授权、未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075s-boundary">R0.75S Step 44 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Bedrossian--Vicol--Wang 2018 与 He 2022 研究 spatially varying shear 产生的 enhanced dissipation；S 的 constant drift 可由平移移除，只含 ordinary heat decay。Egidi--Veselić 2020 与 Wang--Wang--Zhang--Zhang 2019 分别说明 torus spectral observation 与 heat observability 依赖 quantitative geometry；S 不调用这些定理，而是直接计算一个 cosine 在 canonical radial subcollar 上的 mass。有限检索不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.75S Step 44 公开边界 · ONE-HARMONIC SCOPE</strong><p>'
        'PROVED：full frozen clock S.1；exact scalar flux reduction S.11--S.13；radial sine-coefficient bounds S.15--S.17；spatial-node 与 moving-phase lemmas S.18--S.25；low-frequency payment S.26--S.30；high-frequency payment S.31--S.38；normalized all-frequency estimate S.6--S.7；以及 exact smooth shear solution S.40--S.41。'
        'CONDITIONAL：S.39 还要求整个时钟和 plateau tube 对齐同一 scale-2R exterior row，并且 harmonic 是同一实际速度的 coordinate component。'
        'OPEN：two or more harmonics、interference、packet aggregation、Fourier projections、nonconstant shear、arbitrary vertical structure、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。该 exact solution 全局光滑，不提供 singularity mechanism。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75s.html">阅读完整笔记</a> · '
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
    if html_count != 247 or pdf_count not in (203, 204):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 187:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75s.html",
        "latestPublishedResearchPdf": "/notes/r0-75s.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075r":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 149
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 44
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "FULL_FREQUENCY_COMPLETE_CLOCK_SINGLE_REAL_HARMONIC_COLLAR_PAYMENT",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": "9f99f88cdf8fb2d209401d8a6bc213df53bb2130",
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_POSITIVE_THEOREM",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "constant_shear_model": "EXACT_GLOBAL_SMOOTH_UNFORCED_NAVIER_STOKES_S40_S41",
            "complete_frozen_clock": "PROVED_S1",
            "radial_cross_section_identity": "PROVED_S11",
            "exact_scalar_flux_reduction": "PROVED_S12_S13",
            "radial_sine_coefficient_bounds": "PROVED_S15_S17",
            "spatial_node_and_moving_phase_lemmas": "PROVED_S18_S25",
            "low_frequency_payment": "PROVED_S26_S30",
            "high_frequency_payment": "PROVED_S31_S38",
            "all_integer_frequency_payment": "PROVED_S4_S6",
            "amplitude_dependence": "CANCELS_EXACTLY",
            "normalized_logarithmic_L2_rate": "MINUS_2_OVER_11907",
            "version_m_realized_subclass": "CONDITIONAL_S39",
            "multimode_interference_and_packet_aggregation": "OPEN_NOT_PROVED",
            "fourier_projection_of_larger_velocity": "OPEN_NOT_PROVED",
            "nonconstant_shear": "OPEN_NOT_PROVED",
            "arbitrary_vertical_structure": "OPEN_NOT_PROVED",
            "E24": "OPEN_NOT_PROVED",
            "complete_version_m_clock_extraction": "OPEN_NOT_PROVED",
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
            "equation_tags_and_displays": "PASS_S1_TO_S41_TAGS_41_OF_41_DISPLAYS_42_OF_42",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75s.html",
            "target_pdf": "/notes/r0-75s.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075s_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 44,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 149,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075t",
        "latestPublishedResearchHtml": "/notes/r0-75s.html",
        "latestPublishedResearchPdf": "/notes/r0-75s.pdf",
        "latestReleaseGate": "tests/r075s-step44-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075s-step44-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075s-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075s-step44-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075s-step44-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075s-step44-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075s-step44-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075s-step44",
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
    write_text(PUBLIC / "notes/r0-75s.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 44,
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
