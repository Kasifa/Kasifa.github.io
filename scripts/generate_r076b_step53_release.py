#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.76B Step 53 from the verified R0.76A Step 52 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r076a_step52_release as previous
import import_r076b_step53_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "605377ec1443f362d7111ef0f869a87a151dbb39"
VERSION = "2.32"
RELEASE = "r076b"
CODE = "R0.76B"
TITLE = "R0.76B｜固定有限倍频带剪切的逆半径通量支付"
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
            raise RuntimeError(f"R0.76B frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r076b_moderate_carrier_fixed_mode_flux_payment_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or len(certificate.get("assertions", [])) != 15
        or not all(row.get("pass") is True for row in certificate.get("assertions", []))
        or len(certificate.get("negativeMutations", [])) != 123
    ):
        raise RuntimeError("R0.76B certificate verdict drift")
    main = (ROOT / "research/r076b_moderate_carrier_fixed_mode_flux_payment.md").read_text()
    compact_main = " ".join(main.split())
    for token in (
        r"\tag{B.1}", r"\tag{B.4}", r"\tag{B.11}", r"\tag{B.21}",
        r"\tag{B.31}", r"\tag{B.35}", r"\tag{B.37}", r"\tag{B.41}",
        r"n_1,\ldots,n_q\in\mathbb N", r"\phi_j\in\mathbb R",
        "all sufficiently large frozen `L`", r"8q\le\alpha\le a",
        "complete square `G^2`", "no spectral separation",
        "n_1R>1", "Version-M extraction", "**NOT CLAY.**",
    ):
        if token not in compact_main:
            raise RuntimeError(f"R0.76B boundary drift: {token}")
    source_report = (ROOT / "research/r076b_report-source.md").read_text()
    compact = " ".join(source_report.split())
    if "This negative result is not evidence of novelty or priority" not in compact:
        raise RuntimeError("R0.76B bounded source-claim boundary drift")


def render_step53_sections() -> str:
    source = (ROOT / "research/r076b_moderate_carrier_fixed_mode_flux_payment.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 415
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
    if section_index != 424:
        raise RuntimeError(f"Step 53 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.31"', 'data-site-version="2.32"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.31", "/i18n-en.js?v=2.32", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Inverse-radius signed-flux payment for each fixed finite exact real dyadic-band shear, using complete-real-square observation and energy payment.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76b.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76B · STEP 53 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76B · Step 53 · FIXED-Q INVERSE-RADIUS FLUX PAYMENT</div><h1>{TITLE}</h1><p>B 对固定整数 q、正整数频率与实相位的 exact real dyadic-band shear，在 n_1 R &lt;= 1 且所有充分大的 frozen L 上证明 inverse-radius signed collar-flux estimate。X 支付 alpha &lt; 8q，B 支付 8q &lt;= alpha &lt;= a；B 在取绝对值前用完整实场平方重组全部 self/cross terms，从而绕过 A 的 localized-current sign obstruction。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">FIXED INTEGER Q</span><span class="label">INTEGER MODES</span><span class="label">REAL PHASES</span><span class="label">EXACT REAL DYADIC BAND</span><span class="label">N_1 R &lt;= 1</span><span class="label">ALPHA &lt; 8Q · X</span><span class="label">8Q &lt;= ALPHA &lt;= A · B</span><span class="label">COMPLETE REAL SQUARE</span><span class="label">ALL SELF / CROSS TERMS</span><span class="label">NO GAP LOSS</span><span class="label">NO LOCALIZED-CURRENT SIGN</span><span class="label">Q-GROWTH OPEN</span><span class="label">N_1 R &gt; 1 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76B STEP 53</strong><p>q：fixed integer q &gt;= 1</p><p>modes：n_j in N</p><p>phases：phi_j in R</p><p>band：n_1 &lt; ... &lt;= 2 n_1</p><p>gate：n_1 R &lt;= 1</p><p>low branch：alpha &lt; 8q · X</p><p>new branch：8q &lt;= alpha &lt;= a</p><p>field：complete real G^2</p><p>gradient cost：(alpha/a)^2 &lt;= 1</p><p>growing q：OPEN</p><p>ultra-high：n_1 R &gt; 1 OPEN</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step53_sections() + '\n<section id="reproduce">', "Step 53 sections")
    evidence = '''<section id="reproduce"><div class="section-no">B / 冻结证据</div><h2>Step 53 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076b_moderate_carrier_fixed_mode_flux_payment.md">Step 53 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076b_moderate_carrier_fixed_mode_flux_payment_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076b_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076b_moderate_carrier_fixed_mode_flux_payment_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076b_moderate_carrier_fixed_mode_flux_payment_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076b_moderate_carrier_fixed_mode_flux_payment_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076b_moderate_carrier_fixed_mode_flux_payment_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076b_moderate_carrier_fixed_mode_flux_payment_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076b_moderate_carrier_fixed_mode_flux_payment_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076b_moderate_carrier_fixed_mode_flux_payment_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076b_moderate_carrier_fixed_mode_flux_payment_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076b_moderate_carrier_fixed_mode_flux_payment_qa.sh">QA script</a></p><p><a href="/notes/r0-76b.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75w.html">上一大里程碑累计回顾（截止 R0.75W）</a> · <a href="/recap-r0-61-r0-75w.pdf">W recap PDF</a></p><p class="note">Certificate：Python 15/15、Ruby 15/15、B.1--B.41、41/41 tags 与 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 123/123 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 continuum Turan--Nazarov 或 compact companion-ODE argument；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 53 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>A 的局部符号障碍与 B 的完整实场平方支付</h2><p><a href="#s-409">A：complete-clock localized-current sign obstruction</a> · <a href="#s-416">B：fixed-q inverse-radius payment by the complete real square</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 53 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">growing packets, ultra-high carriers, and arbitrary fields remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.76B Step 53 停止。B 只闭合固定 q、exact real dyadic-band shear 在 n_1 R &lt;= 1 的 inverse-radius signed-flux estimate；常数不对 growing q 一致。n_1 R &gt; 1、arbitrary growing packets、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 53 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.31"', 'data-site-version="2.32"', "home version"),
        ("/i18n-en.js?v=2.31", "/i18n-en.js?v=2.32", "home i18n"),
        ("/site-refresh.js?v=2.31.1", "/site-refresh.js?v=2.32.1", "home refresh"),
        ("<strong>v2.31</strong>网页版本", "<strong>v2.32</strong>网页版本", "home stat version"),
        ("<strong>R0.76A</strong>最新研究节点", "<strong>R0.76B</strong>最新研究节点", "home latest"),
        ("<strong>255</strong>公开研究笔记", "<strong>256</strong>公开研究笔记", "home public count"),
        ("展开 165 篇公开笔记", "展开 166 篇公开笔记", "home route count"),
        ("综述 v2.31 · 2026-09-04", "综述 v2.32 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.76A", "Research topology · R0.1–R0.76B", "home topology"),
        ('href="#r076a">跳到首页 R0.76A 卡片 →', 'href="#r076b">跳到首页 R0.76B 卡片 →', "home jump"),
        ("R0.70A–R0.76A：157 节已公开，104 节完整封存", "R0.70A–R0.76B：158 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.76A</span>', '<span class="route-range">R0.69P–R0.76B</span>', "home range"),
        ("<h3>R0.76A：完整时钟局部载频电流负号障碍</h3>", "<h3>R0.76B：固定有限倍频带剪切的逆半径通量支付</h3>", "home route title"),
        ("R0.72R–R0.76A：</span>", "R0.72R–R0.76B：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.76A"', 'aria-label="R0.69P–R0.76B"', "home links label"),
        ("全站现有 255 篇公开研究笔记", "全站现有 256 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.76B Step 53 对固定整数 q 的 exact real dyadic-band shear，在 n_1 R &lt;= 1 和所有充分大的 frozen L 上闭合 inverse-radius signed flux。X 与 B 的 alpha 分支穷尽该范围；完整实场平方在取绝对值前保留全部 self/cross terms，绕过 A 的 localized-current sign obstruction。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76B · 2026-09-04 · STEP 53 · FIXED-Q INVERSE-RADIUS FLUX PAYMENT</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">B 对固定整数 q、正整数频率与实相位的 exact real dyadic-band shear 闭合 n_1 R &lt;= 1：X 支付 alpha &lt; 8q，B 支付 8q &lt;= alpha &lt;= a。完整实场平方在绝对值之前重组所有 self/cross terms，不使用 localized-current sign。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76b.pdf">阅读最新 R0.76B 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾仍截止 R0.75W（191 节）</a><a href="/notes/">256 篇研究笔记总索引</a><a href="#r076b">查看首页 R0.76B 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76B · 158 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76B Step 53 fixed-q inverse-radius flux payment</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">X pays the fixed-q low-carrier branch, A blocks localized-current sign-dropping, and B restores the complete real square to close every fixed finite exact dyadic shear through n_1 R &lt;= 1.</p>', "home current summary")
    page = replace_once(page, 'strongly separated high-carrier family → unresolved-cluster envelope/current normal form → complete-clock localized sign obstruction / perturbative, nonlocal signed, joint-block, and general cluster payment open</p>', 'unresolved-cluster envelope/current normal form → complete-clock localized sign obstruction → complete-real-square fixed-q inverse-radius payment / growing q, n_1 R &gt; 1, arbitrary fields, and Version-M extraction open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-76a.html">R0.76A</a>', '<a class="milestone" href="/notes/r0-76a.html">R0.76A</a>\n<a class="milestone" href="/notes/r0-76b.html">R0.76B</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>growing packets, ultra-high carriers, and arbitrary-field transfer</h3><p>B 只闭合固定 q、exact real dyadic-band shear 在 n_1 R &lt;= 1 的范围。q-uniform growing packets、n_1 R &gt; 1、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、regularity 与 singularity 仍开放。后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r076b" data-release="r076b" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76B Step 53 · 2026-09-04 · FIXED-Q INVERSE-RADIUS FLUX PAYMENT</p><h3>{TITLE}</h3><p>固定整数 q、正整数频率与实相位；X 的 alpha &lt; 8q 与 B 的 8q &lt;= alpha &lt;= a 分支在 n_1 R &lt;= 1 内穷尽。B 通过完整实场平方统一支付 self/cross terms，不使用 A 所否定的 localized-current sign。q-uniform、ultra-high carriers、arbitrary fields 与 unconditional Version-M 仍开放。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-76b.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76b.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap 仍截止 W</a></p></div>\n'''
    anchor = '<div class="task-one" id="r076a"'
    if anchor not in page:
        raise RuntimeError("home R0.76A card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.31"', 'data-site-version="2.32"', "literature version"),
        ("/i18n-en.js?v=2.31", "/i18n-en.js?v=2.32", "literature i18n"),
        ("文献综述 v2.31 · 2026-09-04", "文献综述 v2.32 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.76A 只列为研究笔记", "本站 R0.69P–R0.76B 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76B</b><strong>fixed-q inverse-radius flux payment by the complete real square</strong></header><p>Step 53 对固定整数 q 的 exact real dyadic-band shear 闭合 n_1 R &lt;= 1：X 支付 alpha &lt; 8q，B 支付 8q &lt;= alpha &lt;= a。B 在取绝对值前用完整实场平方重组全部 self/cross terms，绕过 A 的 localized-current sign obstruction；常数不对 growing q 一致。<a href="/notes/r0-76b.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">保留的 W milestone recap</a> <a href="#r076b-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>growing packets, ultra-high carriers, and arbitrary-field transfer</strong></header><p>q-uniform growing packets、n_1 R &gt; 1、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、regularity 与 singularity 均未闭合。后续材料未授权、未读取、未公开。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · 后续未授权</b>[\s\S]*?</div>', route, "literature route")
    boundary = (
        '<h3 id="r076b-boundary">R0.76B Step 53 的 bounded primary-source screen 与主张边界</h3>'
        '<p><a href="https://www.mathnet.ru/eng/aa397">Nazarov 1993/1994</a> 与 <a href="https://arxiv.org/abs/1107.0039">Friedland--Yomdin 2013</a> 支持 finite exponential polynomial 的 measurable-set Turan--Nazarov observation 以及不依赖虚部频率或 gap 的边界。Erdelyi、Brudnyi 与 Jaming--Saba 只作 adjacent derivative-inequality context；B 的 companion-ODE derivative row、complete-real-square energy identity 与 physical scaling 都在本地证明。bounded collision screen 不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.76B Step 53 公开边界 · FIXED-Q INVERSE-RADIUS EXACT-SHEAR PAYMENT</strong><p>'
        'PROVED：固定整数 q、n_j in N、phi_j in R、exact real dyadic band 1 &lt;= n_1 &lt; ... &lt;= 2 n_1；对所有充分大的 frozen L，在 n_1 R &lt;= 1 下有 |T| &lt;= C_q a^(2/3) R^(-1/3) M^(2/3)。X 的 alpha &lt; 8q 与 B 的 8q &lt;= alpha &lt;= a 分支不重不漏。B.15--B.25 用两次 Turan--Nazarov 与 compact companion ODE 给出 gap/speed-independent observation；B.29--B.35 对完整实场平方做能量支付，在绝对值前保留全部 self/cross terms；B.36--B.37 完成尺度换算。'
        'NARROW CONSEQUENCE：在这一 fixed-q exact-shear、n_1 R &lt;= 1 范围内，B 绕过 A 的 localized-current sign obstruction；不需要 spectral separation 或 localized-current positivity。'
        'CONDITIONAL：任何 Version-M consequence 仍要求同一 velocity component 与同一 measurement row；非零常背景尚未放入 frozen mean-zero Version-M subclass。'
        'OPEN：q-uniform growing q、n_1 R &gt; 1 ultra-high carrier、arbitrary growing packets、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。finite checks 不代替 continuum Turan--Nazarov 或 compact ODE argument；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>FIXED Q ONLY. EXACT SHEAR ONLY. NO UNCONDITIONAL VERSION-M. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76b.html">阅读完整笔记</a> · '
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
    if html_count != 256 or pdf_count not in (212, 213):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 196:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76b.html",
        "latestPublishedResearchPdf": "/notes/r0-76b.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "latestRecapRelease": "R0.75W",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r076a":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 158
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 53
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "FIXED_Q_INVERSE_RADIUS_EXACT_REAL_DYADIC_SHEAR_FLUX_PAYMENT",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_FIXED_Q_EXACT_SHEAR_PAYMENT",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "fixed_q": "PROVED_FOR_EACH_FIXED_INTEGER_Q_GE_1_NOT_UNIFORM_IN_GROWING_Q",
            "integer_modes": "REQUIRED_NJ_IN_POSITIVE_INTEGERS",
            "real_phases": "REQUIRED_PHIJ_IN_REAL_NUMBERS",
            "dyadic_band": "REQUIRED_ONE_LE_N1_LT_DOTS_LT_NQ_LE_TWO_N1",
            "large_frozen_L_gate": "REQUIRED_ALL_SUFFICIENTLY_LARGE_FROZEN_L",
            "inverse_radius_carrier": "PROVED_N1_R_LE_ONE",
            "low_branch": "PAID_BY_R075X_ALPHA_LT_8Q",
            "moderate_branch": "PROVED_HERE_8Q_LE_ALPHA_LE_A",
            "branch_exhaustion": "PROVED_WITHIN_N1_R_LE_ONE",
            "spatial_observation": "TURAN_NAZAROV_PLUS_COMPACT_COMPANION_ODE_NO_GAP_LOSS",
            "temporal_trace": "TURAN_NAZAROV_REAL_PARTS_IN_MINUS4_TO_ZERO_SPEED_INDEPENDENT",
            "complete_real_square": "RETAINED_BEFORE_ABSOLUTE_VALUES",
            "self_cross_terms": "ALL_REASSEMBLED_BEFORE_ABSOLUTE_VALUES",
            "localized_current_sign": "NOT_USED_R076A_OBSTRUCTION_BYPASSED",
            "gradient_absorption": "ALPHA_OVER_A_SQUARED_LE_ONE",
            "ultra_high_carrier": "OPEN_N1_R_GT_ONE",
            "arbitrary_growing_packets": "OPEN_NOT_PROVED",
            "nonconstant_or_vertical_shear": "OPEN_NOT_PROVED",
            "projection_from_larger_velocity": "OPEN_NOT_PROVED",
            "E24": "OPEN_NOT_PROVED",
            "complete_version_m_extraction": "OPEN_NOT_PROVED",
            "fixed_deletion": "OPEN_NOT_PROVED",
            "suitable_weak_transfer": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_12_OF_12",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_15_OF_15",
            "independent_ruby": "PASS_15_OF_15",
            "negative_mutations": "PASS_PYTHON_123_OF_123_RUBY_123_OF_123",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_B1_TO_B41_TAGS_AND_DISPLAYS_41_OF_41",
            "exact_fixtures": "PASS_Q3_ENDPOINT_WINDOWS_TEMPORAL_REAL_PART_PDE_ENERGY_AND_SCALE_LEDGER",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76b.html",
            "target_pdf": "/notes/r0-76b.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "retained_recap_terminal_release": "R0.75W_STEP48",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076b_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 53,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "postR070APublishedReleaseCount": 158,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r076c",
        "latestPublishedResearchHtml": "/notes/r0-76b.html",
        "latestPublishedResearchPdf": "/notes/r0-76b.pdf",
        "latestReleaseGate": "tests/r076b-step53-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r076b-step53-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076b-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076b-step53-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076b-step53-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076b-step53-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076b-step53-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076b-step53",
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
    write_text(PUBLIC / "notes/r0-76b.html", render_note())
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
        "latestCompletedStep": 53,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 191,
        "formalFigure": None,
        "formalFigureExemption": True,
        "simulation": False,
        "pdeData": False,
        "noveltyClaim": False,
        "clayClaim": False,
        "fixedQInverseRadiusPayment": True,
        "growingQClaim": False,
        "ultraHighCarrierClaim": False,
        "arbitraryFieldClaim": False,
        "unconditionalVersionMClaim": False,
        "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
