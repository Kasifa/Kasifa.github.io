#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.76E Step 56 from the verified R0.76D Step 55 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r076d_step55_release as previous
import import_r076e_step56_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "a9bc6b1209024d52b0529b37e72c09b1b7d0047d"
VERSION = "2.35"
RELEASE = "r076e"
CODE = "R0.76E"
TITLE = "R0.76E｜精确剪切的线性模态熵窗口"
RECAP_SLUG = "recap-r0-61-r0-75w"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-75w.html": "ac5256b1d262232c1934aae69e8583f203b8b57a5af1f6dad844efe6ca7abbfc",
    PUBLIC / "recap-r0-61-r0-75w.pdf": "d98261500e70a333605735f8798ec771d8d2c4d5dcb166a74e939721726cd7ce",
}

sha256 = previous.sha256
write_text = previous.write_text
write_json = previous.write_json
replace_once = previous.replace_once
replace_pattern = previous.replace_pattern
base_inline_markup = previous.inline_markup


def inline_markup(value: str) -> str:
    rendered = base_inline_markup(value)
    return re.sub(r"`([^`\n]+)`", r"<code>\1</code>", rendered)


def baseline_text(relative: str) -> str:
    return subprocess.check_output(
        ["git", "show", f"{BASELINE_COMMIT}:{relative}"], cwd=ROOT, text=True
    )


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected W milestone recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.76E frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r076e_linear_modal_entropy_window_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertionsPassed") != 135
        or certificate.get("assertionsTotal") != 135
        or not all(
            value is True
            for group in certificate.get("checks", {}).values()
            for value in group.values()
        )
        or len(certificate.get("negativeMutations", [])) != 135
    ):
        raise RuntimeError("R0.76E certificate verdict drift")
    main = (ROOT / "research/r076e_linear_modal_entropy_window.md").read_text()
    compact_main = " ".join(main.split())
    for token in (
        r"\tag{E.1}", r"\tag{E.3}", r"\tag{E.10}", r"\tag{E.15}",
        r"\tag{E.18}", r"\tag{E.22}", r"\tag{E.29}", r"\tag{E.34}",
        r"n_j\in\mathbb N", r"\phi_j,B\in\mathbb R",
        r"e^{C_*q}a^{2/3}R^{-1/3}", r"q(L)=o(L^2)",
        r"(\alpha+q)^{-1}\|G_z(s)\|_{L^\infty(J)}",
        r"S_N=C_0N\log(N+1)", r"4^{-1/3}S_N^{4/3}K_T^{2/3}",
        r"e^{CN}T^{-2/3}K_T^{2/3}", r"\lambda^{-1/3}H^{2/3}",
        "complete real square", "If `lambda>1`", "Version-M extraction", "**NOT CLAY.**",
    ):
        if token not in compact_main:
            raise RuntimeError(f"R0.76E boundary drift: {token}")
    source_report = (ROOT / "research/r076e_report-source.md").read_text()
    compact = " ".join(source_report.split())
    if "The bounded search establishes no literature completeness, novelty, priority, or sharpness" not in compact:
        raise RuntimeError("R0.76E bounded source-claim boundary drift")


def render_step56_sections() -> str:
    source = (ROOT / "research/r076e_linear_modal_entropy_window.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 441
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
        elif lines[0].startswith("### "):
            output.append(f"<h3>{inline_markup(lines[0][4:])}</h3>")
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
        elif re.match(r"^\d+\. ", lines[0]):
            items = []
            current = ""
            for line in lines:
                if re.match(r"^\d+\. ", line):
                    if current:
                        items.append(current)
                    current = re.sub(r"^\d+\. ", "", line)
                else:
                    current += " " + line.strip()
            if current:
                items.append(current)
            output.append("<ol>" + "".join(f"<li>{inline_markup(item)}</li>" for item in items) + "</ol>")
        else:
            output.append(f"<p>{inline_markup(stripped)}</p>")
    if section_open:
        output.append("</section>")
    if section_index != 449:
        raise RuntimeError(f"Step 56 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.34"', 'data-site-version="2.35"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.34", "/i18n-en.js?v=2.35", "note i18n")
    page = replace_once(
        page,
        "</head>",
        '<style>.hero p code{margin-inline:.08em}@media print{.table-wrap{overflow:visible!important}table{table-layout:fixed!important;width:100%!important}th,td{overflow-wrap:anywhere!important;word-break:break-word!important;white-space:normal!important}}</style></head>',
        "note print table containment",
    )
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Linear exp(C q) modal-entropy loss and q(L)=o(L^2) window for exact real constant shears.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76e.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76E · STEP 56 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76E · Step 56 · LINEAR MODAL-ENTROPY WINDOW</div><h1>{TITLE}</h1><p>E 延迟 stable heat-tail 分割，用全程观测质量支付早段，只在 tail 已单调递减后调用 Turan--Nazarov；这把 D 的 <code>exp(C_* q log(q+1))</code> 损失改进为 <code>exp(C_* q)</code>，并把增长窗口扩展到 <code>q(L)=o(L^2)</code>，仍保留 frozen rate <code>-2/11907</code>。last-unit endpoint 与 complete-real energy ledger 保持所有 carrier powers 精确抵消。有限证书不替代 continuum proof。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">EXACT REAL CONSTANT SHEAR</span><span class="label">EXP(C Q) LOSS</span><span class="label">LINEAR MODAL ENTROPY</span><span class="label">Q(L) = o(L^2)</span><span class="label">DELAYED STABLE HEAT CLOCK</span><span class="label">EARLY HOLDER PAYMENT</span><span class="label">MONOTONE TAIL ONLY</span><span class="label">LAST-UNIT ENDPOINT</span><span class="label">LAMBDA^(-1/3) WEIGHTED</span><span class="label">LAMBDA^0 TERMINAL</span><span class="label">COMPLETE REAL SQUARE</span><span class="label">B!=0 VERSION-M CONDITIONAL</span><span class="label">NO ARBITRARY PACKETS</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76E STEP 56</strong><p>q：integer q &gt;= 1</p><p>band：integer n_1 &lt; ... &lt;= 2 n_1</p><p>entropy：exp(C_* q)</p><p>window：q(L) = o(L^2)</p><p>split：S_N = C_0 N log(N+1)</p><p>early：Holder with full K_T</p><p>tail：after monotonicity</p><p>endpoint：exp(CN) T^(-2/3)</p><p>rate：-2/11907</p><p>external：Turan--Nazarov · Erdelyi</p><p>Version-M：conditional when B!=0</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step56_sections() + '\n<section id="reproduce">', "Step 56 sections")
    evidence = '''<section id="reproduce"><div class="section-no">E / 冻结证据</div><h2>Step 56 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076e_linear_modal_entropy_window.md">Step 56 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076e_linear_modal_entropy_window_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076e_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076e_linear_modal_entropy_window_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076e_linear_modal_entropy_window_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076e_linear_modal_entropy_window_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076e_linear_modal_entropy_window_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076e_linear_modal_entropy_window_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076e_linear_modal_entropy_window_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076e_linear_modal_entropy_window_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076e_linear_modal_entropy_window_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076e_linear_modal_entropy_window_qa.sh">QA script</a></p><p><a href="/notes/r0-76e.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75w.html">上一大里程碑累计回顾（截止 R0.75W）</a> · <a href="/recap-r0-61-r0-75w.pdf">W recap PDF</a></p><p class="note">Certificate：Python 135/135、Ruby 135/135、E.1--E.34、38/38 displays（含 4 个有意不编号 displays），3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 135/135 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 Turan--Nazarov、Erdelyi 或 analytic flux theorem 的 continuum proof；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 56 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>D 的定量模态熵损失与 E 的线性模态熵窗口</h2><p><a href="#s-433">D：exp(C q log(q+1)) growing-mode window</a> · <a href="#s-442">E：exp(C q) linear modal-entropy window</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 56 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续尚未发布</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">arbitrary growing packets, arbitrary fields, and Version-M extraction remain OPEN</h2><p style="margin:.15rem 0">本站当前发布至 R0.76E Step 56。E 只对 exact real constant-shear family 给出 <code>exp(C_* q)</code> 损失及 <code>q(L)=o(L^2)</code> 窗口，不是 arbitrary growing packets 的统一定理。当 <code>B!=0</code> 时，常背景尚未证明属于 frozen mean-zero、inversion-paired Version-M subclass；arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续队列尚未发布。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 56 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.34"', 'data-site-version="2.35"', "home version"),
        ("/i18n-en.js?v=2.34", "/i18n-en.js?v=2.35", "home i18n"),
        ("/site-refresh.js?v=2.34.1", "/site-refresh.js?v=2.35.1", "home refresh"),
        ("<strong>v2.34</strong>网页版本", "<strong>v2.35</strong>网页版本", "home stat version"),
        ("<strong>R0.76D</strong>最新研究节点", "<strong>R0.76E</strong>最新研究节点", "home latest"),
        ("<strong>258</strong>公开研究笔记", "<strong>259</strong>公开研究笔记", "home public count"),
        ("展开 168 篇公开笔记", "展开 169 篇公开笔记", "home route count"),
        ("综述 v2.34 · 2026-09-04", "综述 v2.35 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.76D", "Research topology · R0.1–R0.76E", "home topology"),
        ('href="#r076d">跳到首页 R0.76D 卡片 →', 'href="#r076e">跳到首页 R0.76E 卡片 →', "home jump"),
        ("R0.70A–R0.76D：160 节已公开，104 节完整封存", "R0.70A–R0.76E：161 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.76D</span>', '<span class="route-range">R0.69P–R0.76E</span>', "home range"),
        ("<h3>R0.76D：精确剪切的定量增长模态熵窗口</h3>", "<h3>R0.76E：精确剪切的线性模态熵窗口</h3>", "home route title"),
        ("R0.72R–R0.76D：</span>", "R0.72R–R0.76E：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.76D"', 'aria-label="R0.69P–R0.76E"', "home links label"),
        ("全站现有 258 篇公开研究笔记", "全站现有 259 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.76E Step 56 用 delayed stable heat clock 把 exact-shear 损失从 exp(C_* q log(q+1)) 改进为 exp(C_* q)，将窗口扩展到 q(L)=o(L^2)，同时保留 -2/11907 的 frozen rate。任意增长包与 Version-M 提取仍开放。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76E · 2026-09-04 · STEP 56 · LINEAR MODAL-ENTROPY WINDOW</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">E 对 exact real constant-shear family 给出 exp(C_* q) 模态熵损失，并在 q(L)=o(L^2) 时保留 -2/11907 的 frozen rate。delayed split、early Holder payment、last-unit endpoint 与 complete-real energy payment 是本地推导；Turan--Nazarov 与 Erdelyi 是外部输入。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76e.pdf">阅读最新 R0.76E 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾仍截止 R0.75W（191 节）</a><a href="/notes/">259 篇研究笔记总索引</a><a href="#r076e">查看首页 R0.76E 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76E · 161 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76E Step 56 linear modal-entropy window</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">E delays the stable-tail split and improves the exact-shear loss to exp(C_* q); q(L)=o(L^2) preserves the frozen coefficient rate, without giving an arbitrary-packet theorem.</p>', "home current summary")
    page = replace_once(page, 'complete-real-square inverse-radius payment → ultra-high heat-clock payment → quantitative modal-entropy loss / q log(q+1)=o(L^2) exact-shear window; arbitrary packets, arbitrary fields, and Version-M extraction open</p>', 'ultra-high heat-clock payment → exp(C q log(q+1)) growing-mode window → delayed stable-clock exp(C q) loss / q=o(L^2) exact-shear window; arbitrary packets, arbitrary fields, and Version-M extraction open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-76d.html">R0.76D</a>', '<a class="milestone" href="/notes/r0-76d.html">R0.76D</a>\n<a class="milestone" href="/notes/r0-76e.html">R0.76E</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.76F · QUEUED, NOT PUBLISHED</span><span class="tree-state current">OPEN</span></div><h3>arbitrary growing packets, arbitrary-field transfer, and Version-M extraction</h3><p>E 的线性模态熵窗口只覆盖 exact real constant-shear family；arbitrary growing packets、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、regularity 与 singularity 仍开放。当 B!=0 时，常背景尚未证明属于 frozen mean-zero、inversion-paired Version-M subclass。后续队列尚未发布。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r076e" data-release="r076e" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76E Step 56 · 2026-09-04 · LINEAR MODAL-ENTROPY WINDOW</p><h3>{TITLE}</h3><p>对 exact real constant-shear family，E 用 delayed stable heat clock 将损失改进为 exp(C_* q)，把窗口扩展到 q(L)=o(L^2)。early Holder 使用完整 K_T，tail 仅在单调区间调用 centered estimate，last-unit endpoint 消除 factorial；finite certificate 不是 continuum proof。任意增长包、unconditional Version-M、regularity 与 singularity 仍开放。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-76e.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76e.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap 仍截止 W</a></p></div>\n'''
    anchor = '<div class="task-one" id="r076d"'
    if anchor not in page:
        raise RuntimeError("home R0.76D card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.34"', 'data-site-version="2.35"', "literature version"),
        ("/i18n-en.js?v=2.34", "/i18n-en.js?v=2.35", "literature i18n"),
        ("文献综述 v2.34 · 2026-09-04", "文献综述 v2.35 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.76D 只列为研究笔记", "本站 R0.69P–R0.76E 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76E</b><strong>linear modal-entropy window for exact shears</strong></header><p>Step 56 保留 D 的空间 observation，以 <code>S_N=C_0N log(N+1)</code> 延迟 stable-tail 分割；early Holder、monotone tail 与 last-unit endpoint 把损失改进为 <code>exp(C_* q)</code>，从而得到 <code>q(L)=o(L^2)</code> 的 exact-shear 窗口。<a href="/notes/r0-76e.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">保留的 W milestone recap</a> <a href="#r076e-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.76F 尚未发布</b><strong>arbitrary growing packets, arbitrary-field transfer, and Version-M extraction</strong></header><p>线性模态熵窗口不是 arbitrary-packet theorem。nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、regularity 与 singularity 均未闭合；当 B!=0 时，常背景尚未证明属于 frozen mean-zero、inversion-paired Version-M subclass。后续队列尚未发布。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · 后续未授权</b>[\s\S]*?</div>', route, "literature route")
    boundary = (
        '<h3 id="r076e-boundary">R0.76E Step 56 的 bounded primary-source screen 与主张边界</h3>'
        '<p><a href="https://www.mathnet.ru/eng/aa397">Nazarov 1993/1994</a> 与 <a href="https://arxiv.org/abs/1107.0039">Friedland--Yomdin 2013</a> 提供 measurable-set Turan--Nazarov inequality；<a href="https://arxiv.org/abs/1602.02315">Erdelyi 2017, Theorem 2.7.1</a> 提供依赖 maximum spatial frequency 与 term count 的 point derivative inequality。E 的 delayed split、early Holder payment、monotone tail、last-unit endpoint、carrier accounting、complete-real energy payment、physical conversion 与 growing-window corollary都是本地推导；bounded search 不构成 completeness、novelty、priority 或 sharpness 判断。</p>'
        '<div class="boundary"><strong>R0.76E Step 56 公开边界 · LINEAR MODAL-ENTROPY WINDOW</strong><p>'
        'PROVED：对 exact real constant-shear dyadic family，|T| &lt;= exp(C_* q) a^(2/3) R^(-1/3) M^(2/3)。E.15 选取统一 delayed split，E.16 用完整 K_T 支付 early interval，E.17 只在 tail 单调后使用 centered estimate，E.22 给出 exp(CN) T^(-2/3) K_T^(2/3) 的 last-unit endpoint。'
        'NARROW CONSEQUENCE：当 q(L)=o(L^2) 时，normalized coefficient 保留 -2/11907 的 frozen rate；这严格扩展 D 的 q(L) log(q(L)+1)=o(L^2) 窗口，但仍不是 arbitrary growing packets 的统一结论。'
        'SOURCE BOUNDARY：Turan--Nazarov 与 Erdelyi 是外部输入；delayed split、early Holder payment、monotone tail、last-unit endpoint、carrier accounting、complete-real energy payment 与 scale conversion 是本地推导。'
        'CONDITIONAL：任何 Version-M consequence 仍要求同一 velocity component 与同一 measurement row；当 B!=0 时，常背景尚未证明属于 frozen mean-zero、inversion-paired Version-M subclass。'
        'OPEN：matching lower bound、sharp q dependence、linear modal-entropy loss removal、arbitrary growing packets、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。finite checks 不代替 continuum theorem；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>EXACT SHEAR ONLY. EXP(CQ) LOSS RETAINED. Q=o(L^2) WINDOW. LAST-UNIT ENDPOINT. NO UNCONDITIONAL VERSION-M. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76e.html">阅读完整笔记</a> · '
        f'<a href="/{RECAP_SLUG}.html">保留截至 W 的 milestone recap</a>。</p></div>\n'
    )
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 259 or pdf_count not in (215, 216):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 199:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76e.html",
        "latestPublishedResearchPdf": "/notes/r0-76e.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "latestRecapRelease": "R0.75W",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r076d":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 161
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 56
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "LINEAR_MODAL_ENTROPY_WINDOW_FOR_EXACT_REAL_CONSTANT_SHEARS",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_LINEAR_MODAL_ENTROPY_WINDOW",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "fixed_q": "EXPLICIT_EXP_CSTAR_Q_LOSS",
            "integer_modes": "REQUIRED_NJ_IN_POSITIVE_INTEGERS",
            "real_phases": "REQUIRED_PHIJ_IN_REAL_NUMBERS",
            "dyadic_band": "REQUIRED_ONE_LE_N1_LT_DOTS_LT_NQ_LE_TWO_N1",
            "large_frozen_L_gate": "REQUIRED_ALL_SUFFICIENTLY_LARGE_FROZEN_L",
            "all_carriers": "INHERITED_EXACT_REAL_CONSTANT_SHEAR_FAMILY_WITH_QUANTIFIED_Q_LOSS",
            "modal_entropy_loss": "EXP_CSTAR_Q_REQUIRED_NOT_SUPPRESSED",
            "growing_mode_window": "Q_OF_L_IS_O_OF_L_SQUARED",
            "frozen_coefficient_rate": "MINUS_TWO_OVER_11907_RETAINED_IN_WINDOW",
            "spatial_observation": "TURAN_NAZAROV_VALUE_ROW_AND_ERDELYI_ALPHA_PLUS_Q_DERIVATIVE_ROW",
            "maximum_spatial_frequency": "EXPLICIT_ALPHA_DEPENDENCE_RETAINED_NO_GAP_DENOMINATOR",
            "temporal_trace": "EVERY_TIME_FIBRE_MUST_BE_EXPONENTIAL_POLYNOMIAL_WITH_REAL_PARTS_MINUS4_TO_MINUS1",
            "delayed_stable_clock": "S_N_EQUALS_C0_N_LOG_N_PLUS_1_UNIFORM_IN_N",
            "early_interval": "HOLDER_WITH_FULL_K_T_GIVES_S_N_TO_FOUR_THIRDS",
            "late_interval": "CENTERED_ESTIMATE_USED_ONLY_AFTER_MONOTONICITY",
            "endpoint_comparison": "LAST_UNIT_TURAN_NAZAROV_EXP_CN_T_MINUS_TWO_THIRDS_K_T_TWO_THIRDS",
            "external_inputs": "TURAN_NAZAROV_AND_ERDELYI",
            "local_deductions": "DELAYED_SPLIT_EARLY_HOLDER_MONOTONE_TAIL_LAST_UNIT_ENDPOINT_CARRIER_ACCOUNTING_ENERGY_PAYMENT_SCALE_CONVERSION_GROWING_WINDOW",
            "weighted_lambda_power": "MINUS_ONE_THIRD",
            "terminal_lambda_power": "ZERO",
            "complete_real_square": "RETAINED_BEFORE_ABSOLUTE_VALUES",
            "gradient_absorption": "LAMBDA_PLUS_Q_SQUARED_OVER_A_SQUARED_MODAL_FACTOR",
            "arbitrary_growing_packets": "OPEN_NOT_PROVED_LINEAR_MODAL_ENTROPY_WINDOW_IS_NOT_ARBITRARY_PACKET_THEOREM",
            "nonconstant_or_vertical_shear": "OPEN_NOT_PROVED",
            "projection_from_larger_velocity": "OPEN_NOT_PROVED",
            "E24": "OPEN_NOT_PROVED",
            "complete_version_m_extraction": "OPEN_NOT_PROVED_WHEN_B_NE_ZERO_BACKGROUND_NOT_SHOWN_IN_FROZEN_SUBCLASS",
            "fixed_deletion": "OPEN_NOT_PROVED",
            "suitable_weak_transfer": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_12_OF_12",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_135_OF_135",
            "independent_ruby": "PASS_135_OF_135",
            "negative_mutations": "PASS_PYTHON_135_OF_135_RUBY_135_OF_135",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_E1_TO_E34_TAGS_AND_38_OF_38_DISPLAYS_WITH_FOUR_INTENTIONAL_UNNUMBERED",
            "exact_fixtures": "PASS_Q3_N6_M10_S96_TAIL_BELOW_TWO_TO_MINUS93_LAMBDA4_T16_GRADIENT_257_OVER_64",
            "continuum_boundary": "FINITE_CERTIFICATE_IS_NOT_PROOF_OF_IMPORTED_INEQUALITIES_OR_ANALYTIC_FLUX_THEOREM",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76e.html",
            "target_pdf": "/notes/r0-76e.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "retained_recap_terminal_release": "R0.75W_STEP48",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076e_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 56,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "postR070APublishedReleaseCount": 161,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r076f",
        "latestPublishedResearchHtml": "/notes/r0-76e.html",
        "latestPublishedResearchPdf": "/notes/r0-76e.pdf",
        "latestReleaseGate": "tests/r076e-step56-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r076e-step56-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076e-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076e-step56-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076e-step56-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076e-step56-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076e-step56-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076e-step56",
            "handoffCommit": None,
            "coreParentCommit": frozen_import.CORE_PARENT_COMMIT,
            "handoffSha256": frozen_import.HANDOFF_SHA256,
            "handoffIndependentAuditSha256": frozen_import.HANDOFF_AUDIT_SHA256,
            "sourceCommit": frozen_import.SOURCE_COMMIT,
            "coreCommit": frozen_import.SOURCE_COMMIT,
            "formalFigureRequired": False,
            "recapRequired": False,
        },
        "latestRecapRelease": "r075w",
        "latestRecapHtml": "/recap-r0-61-r0-75w.html",
        "latestRecapPdf": "/recap-r0-61-r0-75w.pdf",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256(inventory_target),
    }
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-76e.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
        for target, expected in RECAP_HASHES.items():
            if sha256(target) != expected:
                raise RuntimeError(f"protected W milestone recap drift after generation: {target.relative_to(ROOT)}")
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 56,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 191,
        "formalFigure": None,
        "formalFigureExemption": True,
        "simulation": False,
        "pdeData": False,
        "noveltyClaim": False,
        "clayClaim": False,
        "modalEntropyLoss": "EXP_CSTAR_Q",
        "growingModeWindow": "Q_IS_O_L_SQUARED",
        "arbitraryGrowingPacketClaim": False,
        "delayedStableClock": True,
        "lastUnitEndpoint": True,
        "arbitraryFieldClaim": False,
        "unconditionalVersionMClaim": False,
        "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
