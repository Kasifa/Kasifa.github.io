#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.76D Step 55 from the verified R0.76C Step 54 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r076c_step54_release as previous
import import_r076d_step55_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "ed7b154d97ecdcb162b00ffbdb63ea647e1d99f4"
VERSION = "2.34"
RELEASE = "r076d"
CODE = "R0.76D"
TITLE = "R0.76D｜精确剪切的定量增长模态熵窗口"
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
            raise RuntimeError(f"R0.76D frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r076d_quantitative_growing_mode_entropy_window_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertionsPassed") != 123
        or certificate.get("assertionsTotal") != 123
        or not all(
            value is True
            for group in certificate.get("checks", {}).values()
            for value in group.values()
        )
        or len(certificate.get("negativeMutations", [])) != 123
    ):
        raise RuntimeError("R0.76D certificate verdict drift")
    main = (ROOT / "research/r076d_quantitative_growing_mode_entropy_window.md").read_text()
    compact_main = " ".join(main.split())
    for token in (
        r"\tag{D.1}", r"\tag{D.4}", r"\tag{D.15}", r"\tag{D.18}",
        r"\tag{D.23}", r"\tag{D.25}", r"\tag{D.38}", r"\tag{D.41}",
        r"n_1,\ldots,n_q\in\mathbb N", r"\phi_j\in\mathbb R",
        r"\exp\!\bigl(C_*q\log(q+1)\bigr)",
        r"q(L)\log(q(L)+1)=o(L^2)", r"(\alpha+q)^{-1}\|g'\|_{L^\infty(J)}",
        r"\left(\frac54\right)^m", r"\frac{(m+1)!}{4}",
        r"\lambda^{-1/3}H^{2/3}", "complete real square",
        "When `lambda>1`", "Version-M extraction", "**NOT CLAY.**",
    ):
        if token not in compact_main:
            raise RuntimeError(f"R0.76D boundary drift: {token}")
    source_report = (ROOT / "research/r076d_report-source.md").read_text()
    compact = " ".join(source_report.split())
    if "This negative screen is not evidence of novelty or priority" not in compact:
        raise RuntimeError("R0.76D bounded source-claim boundary drift")


def render_step55_sections() -> str:
    source = (ROOT / "research/r076d_quantitative_growing_mode_entropy_window.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 432
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
    if section_index != 441:
        raise RuntimeError(f"Step 55 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.33"', 'data-site-version="2.34"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.33", "/i18n-en.js?v=2.34", "note i18n")
    page = replace_once(
        page,
        "</head>",
        '<style>.hero p code{margin-inline:.08em}@media print{.table-wrap{overflow:visible!important}table{table-layout:fixed!important;width:100%!important}th,td{overflow-wrap:anywhere!important;word-break:break-word!important;white-space:normal!important}}</style></head>',
        "note print table containment",
    )
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Quantitative exp(C q log(q+1)) modal-entropy loss and growing-mode window for exact real constant shears.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76d.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76D · STEP 55 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76D · Step 55 · QUANTITATIVE GROWING-MODE ENTROPY WINDOW</div><h1>{TITLE}</h1><p>D 把 C 的 fixed-q 常数定量化为 <code>exp(C_* q log(q+1))</code>，从而在 <code>q(L) log(q(L)+1)=o(L^2)</code> 时保留 frozen rate <code>-2/11907</code>。空间导数保留 <code>alpha+q</code>，endpoint 比较保留 <code>(5/4)^m</code>。Turan--Nazarov 与 Erdelyi 是外部输入；其余 placement、factorial tail、lambda 分支、energy payment 与尺度换算是本地推导。有限证书不替代 continuum proof。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">EXACT REAL CONSTANT SHEAR</span><span class="label">EXP(C Q LOG(Q+1))</span><span class="label">GROWING-MODE WINDOW</span><span class="label">Q LOG(Q+1) = o(L^2)</span><span class="label">ALPHA+Q DERIVATIVE</span><span class="label">(5/4)^M ENDPOINT</span><span class="label">COUNTED FACTORIAL TAIL</span><span class="label">LAMBDA^(-1/3) WEIGHTED</span><span class="label">LAMBDA^0 TERMINAL</span><span class="label">COMPLETE REAL SQUARE</span><span class="label">B!=0 VERSION-M CONDITIONAL</span><span class="label">NO ARBITRARY PACKETS</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76D STEP 55</strong><p>q：integer q &gt;= 1</p><p>band：n_1 &lt; ... &lt;= 2 n_1</p><p>entropy：exp(C_* q log(q+1))</p><p>window：q log(q+1) = o(L^2)</p><p>derivative：alpha+q</p><p>endpoint：(5/4)^m</p><p>tail：(m+1)!/4</p><p>rate：-2/11907</p><p>external：Turan--Nazarov · Erdelyi</p><p>Version-M：conditional when B!=0</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step55_sections() + '\n<section id="reproduce">', "Step 55 sections")
    evidence = '''<section id="reproduce"><div class="section-no">D / 冻结证据</div><h2>Step 55 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076d_quantitative_growing_mode_entropy_window.md">Step 55 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076d_quantitative_growing_mode_entropy_window_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076d_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076d_quantitative_growing_mode_entropy_window_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076d_quantitative_growing_mode_entropy_window_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076d_quantitative_growing_mode_entropy_window_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076d_quantitative_growing_mode_entropy_window_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076d_quantitative_growing_mode_entropy_window_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076d_quantitative_growing_mode_entropy_window_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076d_quantitative_growing_mode_entropy_window_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076d_quantitative_growing_mode_entropy_window_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076d_quantitative_growing_mode_entropy_window_qa.sh">QA script</a></p><p><a href="/notes/r0-76d.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75w.html">上一大里程碑累计回顾（截止 R0.75W）</a> · <a href="/recap-r0-61-r0-75w.pdf">W recap PDF</a></p><p class="note">Certificate：Python 123/123、Ruby 123/123、D.1--D.41、41/41 tags 与 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 123/123 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 Turan--Nazarov、Erdelyi 或 analytic flux theorem 的 continuum proof；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 55 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>C 的 fixed-q 全频支付与 D 的定量模态熵窗口</h2><p><a href="#s-425">C：fixed-q full-frequency payment</a> · <a href="#s-433">D：quantitative growing-mode entropy window</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 55 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">arbitrary growing packets, arbitrary fields, and Version-M extraction remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.76D Step 55 停止。D 只对 exact real constant-shear family 给出 <code>exp(C_* q log(q+1))</code> 损失及 <code>q(L) log(q(L)+1)=o(L^2)</code> 窗口，不是 arbitrary growing packets 的统一定理。当 <code>B!=0</code> 时，常背景尚未证明属于 frozen mean-zero、inversion-paired Version-M subclass；arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 55 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.33"', 'data-site-version="2.34"', "home version"),
        ("/i18n-en.js?v=2.33", "/i18n-en.js?v=2.34", "home i18n"),
        ("/site-refresh.js?v=2.33.1", "/site-refresh.js?v=2.34.1", "home refresh"),
        ("<strong>v2.33</strong>网页版本", "<strong>v2.34</strong>网页版本", "home stat version"),
        ("<strong>R0.76C</strong>最新研究节点", "<strong>R0.76D</strong>最新研究节点", "home latest"),
        ("<strong>257</strong>公开研究笔记", "<strong>258</strong>公开研究笔记", "home public count"),
        ("展开 167 篇公开笔记", "展开 168 篇公开笔记", "home route count"),
        ("综述 v2.33 · 2026-09-04", "综述 v2.34 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.76C", "Research topology · R0.1–R0.76D", "home topology"),
        ('href="#r076c">跳到首页 R0.76C 卡片 →', 'href="#r076d">跳到首页 R0.76D 卡片 →', "home jump"),
        ("R0.70A–R0.76C：159 节已公开，104 节完整封存", "R0.70A–R0.76D：160 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.76C</span>', '<span class="route-range">R0.69P–R0.76D</span>', "home range"),
        ("<h3>R0.76C：固定有限倍频带剪切的全频通量支付</h3>", "<h3>R0.76D：精确剪切的定量增长模态熵窗口</h3>", "home route title"),
        ("R0.72R–R0.76C：</span>", "R0.72R–R0.76D：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.76C"', 'aria-label="R0.69P–R0.76D"', "home links label"),
        ("全站现有 257 篇公开研究笔记", "全站现有 258 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.76D Step 55 把 fixed-q 常数定量化为 exp(C_* q log(q+1))，并得到 q(L) log(q(L)+1)=o(L^2) 的 exact-shear growing-mode window；空间导数保留 alpha+q，endpoint 比较保留 (5/4)^m。任意增长包与 Version-M 提取仍开放。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76D · 2026-09-04 · STEP 55 · QUANTITATIVE GROWING-MODE ENTROPY WINDOW</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">D 对 exact real constant-shear family 给出 exp(C_* q log(q+1)) 模态熵损失，并在 q(L) log(q(L)+1)=o(L^2) 时保留 -2/11907 的 frozen rate。Turan--Nazarov 与 Erdelyi 是外部输入，其余证明链为本地推导。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76d.pdf">阅读最新 R0.76D 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾仍截止 R0.75W（191 节）</a><a href="/notes/">258 篇研究笔记总索引</a><a href="#r076d">查看首页 R0.76D 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76D · 160 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76D Step 55 quantitative growing-mode entropy window</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">D quantifies the fixed-q constant by exp(C_* q log(q+1)); q(L) log(q(L)+1)=o(L^2) preserves the frozen coefficient rate only inside the exact constant-shear family.</p>', "home current summary")
    page = replace_once(page, 'complete-clock localized sign obstruction → complete-real-square inverse-radius payment → ultra-high heat-clock payment / all carriers closed for fixed q; growing q, arbitrary fields, and Version-M extraction open</p>', 'complete-real-square inverse-radius payment → ultra-high heat-clock payment → quantitative modal-entropy loss / q log(q+1)=o(L^2) exact-shear window; arbitrary packets, arbitrary fields, and Version-M extraction open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-76c.html">R0.76C</a>', '<a class="milestone" href="/notes/r0-76c.html">R0.76C</a>\n<a class="milestone" href="/notes/r0-76d.html">R0.76D</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>arbitrary growing packets, arbitrary-field transfer, and Version-M extraction</h3><p>D 的增长窗口只覆盖 exact real constant-shear family；arbitrary growing packets、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、regularity 与 singularity 仍开放。当 B!=0 时，常背景尚未证明属于 frozen mean-zero、inversion-paired Version-M subclass。后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r076d" data-release="r076d" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76D Step 55 · 2026-09-04 · QUANTITATIVE GROWING-MODE ENTROPY WINDOW</p><h3>{TITLE}</h3><p>对 exact real constant-shear family，D 显式给出 exp(C_* q log(q+1)) 损失与 q(L) log(q(L)+1)=o(L^2) 增长窗口；保留 alpha+q 空间导数和 (5/4)^m endpoint 因子。Turan--Nazarov、Erdelyi 为外部输入；finite certificate 不是 continuum proof。任意增长包、unconditional Version-M、regularity 与 singularity 仍开放。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-76d.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76d.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap 仍截止 W</a></p></div>\n'''
    anchor = '<div class="task-one" id="r076c"'
    if anchor not in page:
        raise RuntimeError("home R0.76C card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.33"', 'data-site-version="2.34"', "literature version"),
        ("/i18n-en.js?v=2.33", "/i18n-en.js?v=2.34", "literature i18n"),
        ("文献综述 v2.33 · 2026-09-04", "文献综述 v2.34 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.76C 只列为研究笔记", "本站 R0.69P–R0.76D 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76D</b><strong>quantitative growing-mode entropy window for exact shears</strong></header><p>Step 55 用 Erdelyi 的 point derivative inequality 与 Turan--Nazarov observation 把 C 的 fixed-q 常数定量化为 exp(C_* q log(q+1))；本地 counted factorial tail、lambda split、complete-real energy payment 与 scale conversion 给出 q(L) log(q(L)+1)=o(L^2) 的 exact-shear 窗口。<a href="/notes/r0-76d.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">保留的 W milestone recap</a> <a href="#r076d-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>arbitrary growing packets, arbitrary-field transfer, and Version-M extraction</strong></header><p>增长窗口不是 arbitrary-packet theorem。nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、regularity 与 singularity 均未闭合；当 B!=0 时，常背景尚未证明属于 frozen mean-zero、inversion-paired Version-M subclass。后续材料未授权、未读取、未公开。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · 后续未授权</b>[\s\S]*?</div>', route, "literature route")
    boundary = (
        '<h3 id="r076d-boundary">R0.76D Step 55 的 bounded primary-source screen 与主张边界</h3>'
        '<p><a href="https://www.mathnet.ru/eng/aa397">Nazarov 1993/1994</a> 与 <a href="https://arxiv.org/abs/1107.0039">Friedland--Yomdin 2013</a> 提供 measurable-set Turan--Nazarov inequality；<a href="https://arxiv.org/abs/1602.02315">Erdelyi 2017, Theorem 2.7.1</a> 提供依赖 maximum spatial frequency 与 term count 的 point derivative inequality。D 的 interval placement、counted factorial tail、(5/4)^m endpoint comparison、lambda split、complete-real energy payment、physical conversion 与 growing-mode corollary都是本地推导；bounded collision screen 不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.76D Step 55 公开边界 · QUANTITATIVE GROWING-MODE ENTROPY WINDOW</strong><p>'
        'PROVED：对 exact real constant-shear dyadic family，|T| &lt;= exp(C_* q log(q+1)) a^(2/3) R^(-1/3) M^(2/3)。D.15 的空间导数明确保留 alpha+q；D.24 的 heat tail 保留 (m+1)!/4；D.25 的 endpoint 比较明确保留 (5/4)^m。'
        'NARROW CONSEQUENCE：仅当 q(L) log(q(L)+1)=o(L^2) 时，normalized coefficient 保留 -2/11907 的 frozen rate。这不是 arbitrary growing packets 的统一结论。'
        'SOURCE BOUNDARY：Turan--Nazarov 与 Erdelyi 是外部输入；spatial placement、factorial tail、lambda branches、energy payment 与 scale conversion 是本地推导。'
        'CONDITIONAL：任何 Version-M consequence 仍要求同一 velocity component 与同一 measurement row；当 B!=0 时，常背景尚未证明属于 frozen mean-zero、inversion-paired Version-M subclass。'
        'OPEN：matching lower bound、sharp q dependence、modal-entropy loss removal、arbitrary growing packets、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。finite checks 不代替 continuum theorem；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>EXACT SHEAR ONLY. MODAL-ENTROPY LOSS RETAINED. ALPHA+Q RETAINED. (5/4)^M RETAINED. NO UNCONDITIONAL VERSION-M. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76d.html">阅读完整笔记</a> · '
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
    if html_count != 258 or pdf_count not in (214, 215):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 198:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76d.html",
        "latestPublishedResearchPdf": "/notes/r0-76d.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "latestRecapRelease": "R0.75W",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r076c":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 160
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 55
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "QUANTITATIVE_GROWING_MODE_ENTROPY_WINDOW_FOR_EXACT_REAL_CONSTANT_SHEARS",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_QUANTITATIVE_GROWING_MODE_ENTROPY_WINDOW",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "fixed_q": "EXPLICIT_EXP_CSTAR_Q_LOG_Q_PLUS_1_LOSS",
            "integer_modes": "REQUIRED_NJ_IN_POSITIVE_INTEGERS",
            "real_phases": "REQUIRED_PHIJ_IN_REAL_NUMBERS",
            "dyadic_band": "REQUIRED_ONE_LE_N1_LT_DOTS_LT_NQ_LE_TWO_N1",
            "large_frozen_L_gate": "REQUIRED_ALL_SUFFICIENTLY_LARGE_FROZEN_L",
            "all_carriers": "INHERITED_EXACT_REAL_CONSTANT_SHEAR_FAMILY_WITH_QUANTIFIED_Q_LOSS",
            "modal_entropy_loss": "EXP_CSTAR_Q_LOG_Q_PLUS_1_REQUIRED_NOT_SUPPRESSED",
            "growing_mode_window": "Q_OF_L_LOG_Q_OF_L_PLUS_1_IS_O_OF_L_SQUARED",
            "frozen_coefficient_rate": "MINUS_TWO_OVER_11907_RETAINED_IN_WINDOW",
            "spatial_observation": "TURAN_NAZAROV_VALUE_ROW_AND_ERDELYI_ALPHA_PLUS_Q_DERIVATIVE_ROW",
            "maximum_spatial_frequency": "EXPLICIT_ALPHA_DEPENDENCE_RETAINED_NO_GAP_DENOMINATOR",
            "temporal_trace": "EVERY_TIME_FIBRE_MUST_BE_EXPONENTIAL_POLYNOMIAL_WITH_REAL_PARTS_MINUS4_TO_MINUS1",
            "factorial_tail": "M_PLUS_ONE_FACTORIAL_OVER_FOUR",
            "endpoint_comparison": "FIVE_OVER_FOUR_TO_THE_M_FACTOR_RETAINED",
            "external_inputs": "TURAN_NAZAROV_AND_ERDELYI",
            "local_deductions": "PLACEMENT_FACTORIAL_TAIL_ENDPOINT_COMPARISON_LAMBDA_BRANCHES_ENERGY_PAYMENT_SCALE_CONVERSION",
            "weighted_lambda_power": "MINUS_ONE_THIRD",
            "terminal_lambda_power": "ZERO",
            "complete_real_square": "RETAINED_BEFORE_ABSOLUTE_VALUES",
            "gradient_absorption": "LAMBDA_PLUS_Q_SQUARED_OVER_A_SQUARED_MODAL_FACTOR",
            "arbitrary_growing_packets": "OPEN_NOT_PROVED_GROWING_WINDOW_IS_NOT_ARBITRARY_PACKET_THEOREM",
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
            "python_certificate": "PASS_123_OF_123",
            "independent_ruby": "PASS_123_OF_123",
            "negative_mutations": "PASS_PYTHON_123_OF_123_RUBY_123_OF_123",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_D1_TO_D41_TAGS_AND_DISPLAYS_41_OF_41",
            "exact_fixtures": "PASS_Q3_N6_M10_FACTORIAL_9979200_LAMBDA4_T16_GRADIENT_257_OVER_64",
            "continuum_boundary": "FINITE_CERTIFICATE_IS_NOT_PROOF_OF_IMPORTED_INEQUALITIES_OR_ANALYTIC_FLUX_THEOREM",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76d.html",
            "target_pdf": "/notes/r0-76d.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "retained_recap_terminal_release": "R0.75W_STEP48",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076d_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 55,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "postR070APublishedReleaseCount": 160,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r076e",
        "latestPublishedResearchHtml": "/notes/r0-76d.html",
        "latestPublishedResearchPdf": "/notes/r0-76d.pdf",
        "latestReleaseGate": "tests/r076d-step55-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r076d-step55-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076d-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076d-step55-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076d-step55-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076d-step55-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076d-step55-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076d-step55",
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
    write_text(PUBLIC / "notes/r0-76d.html", render_note())
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
        "latestCompletedStep": 55,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 191,
        "formalFigure": None,
        "formalFigureExemption": True,
        "simulation": False,
        "pdeData": False,
        "noveltyClaim": False,
        "clayClaim": False,
        "modalEntropyLoss": "EXP_CSTAR_Q_LOG_Q_PLUS_1",
        "growingModeWindow": "Q_LOG_Q_PLUS_1_IS_O_L_SQUARED",
        "arbitraryGrowingPacketClaim": False,
        "alphaPlusQDerivativeRetained": True,
        "endpointFiveFourthsPowerRetained": True,
        "arbitraryFieldClaim": False,
        "unconditionalVersionMClaim": False,
        "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
