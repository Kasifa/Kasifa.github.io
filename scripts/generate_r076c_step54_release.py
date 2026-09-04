#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.76C Step 54 from the verified R0.76B Step 53 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r076b_step53_release as previous
import import_r076c_step54_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "53fda24d9430a9405c9ed2d6978bbb950289c0b8"
VERSION = "2.33"
RELEASE = "r076c"
CODE = "R0.76C"
TITLE = "R0.76C｜固定有限倍频带剪切的全频通量支付"
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
            raise RuntimeError(f"R0.76C frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r076c_full_frequency_fixed_mode_flux_payment_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or len(certificate.get("assertions", [])) != 15
        or not all(
            value is True
            for group in certificate.get("assertions", {}).values()
            for value in group.values()
        )
        or len(certificate.get("negativeMutations", [])) != 140
    ):
        raise RuntimeError("R0.76C certificate verdict drift")
    main = (ROOT / "research/r076c_full_frequency_fixed_mode_flux_payment.md").read_text()
    compact_main = " ".join(main.split())
    for token in (
        r"\tag{C.1}", r"\tag{C.4}", r"\tag{C.12}", r"\tag{C.14}",
        r"\tag{C.15}", r"\tag{C.26}", r"\tag{C.30}", r"\tag{C.35}",
        r"n_1,\ldots,n_q\in\mathbb N", r"\phi_j\in\mathbb R",
        "all sufficiently large frozen `L`", r"\lambda=\frac{\alpha^2}{a^2}",
        "every `Q(.;z)` an exponential polynomial satisfying C.12",
        r"\lambda^{-1/3}H^{2/3}", "complete real square",
        "n_1R<=1", "no carrier upper bound", "Version-M extraction", "**NOT CLAY.**",
    ):
        if token not in compact_main:
            raise RuntimeError(f"R0.76C boundary drift: {token}")
    source_report = (ROOT / "research/r076c_report-source.md").read_text()
    compact = " ".join(source_report.split())
    if "This negative screen is not evidence of novelty or priority" not in compact:
        raise RuntimeError("R0.76C bounded source-claim boundary drift")


def render_step54_sections() -> str:
    source = (ROOT / "research/r076c_full_frequency_fixed_mode_flux_payment.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 424
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
    if section_index != 432:
        raise RuntimeError(f"Step 54 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.32"', 'data-site-version="2.33"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.32", "/i18n-en.js?v=2.33", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Full-frequency signed-flux payment for each fixed finite exact real dyadic-band shear, combining B with an ultra-high heat-clock argument.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76c.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76C · STEP 54 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76C · Step 54 · FIXED-Q FULL-FREQUENCY FLUX PAYMENT</div><h1>{TITLE}</h1><p>C 对固定整数 q、正整数频率与实相位的 exact real dyadic-band shear，支付 ultra-high heat-clock 分支 n_1 R &gt; 1；与 B 的 n_1 R &lt;= 1 合并后覆盖全部 carrier。加权尾项保留 lambda^(-1/3)，终端项保留 lambda^0；完整实场平方在取绝对值前重组全部 self/cross terms。C.14 只量化逐点满足 C.12 的 exponential-polynomial family。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">FIXED INTEGER Q</span><span class="label">INTEGER MODES</span><span class="label">REAL PHASES</span><span class="label">EXACT REAL DYADIC BAND</span><span class="label">ALL CARRIERS</span><span class="label">N_1 R &lt;= 1 · B</span><span class="label">N_1 R &gt; 1 · C</span><span class="label">EXPONENTIAL-POLYNOMIAL CLOCK</span><span class="label">C.14 POINTWISE FAMILY</span><span class="label">LAMBDA^(-1/3) WEIGHTED</span><span class="label">LAMBDA^0 TERMINAL</span><span class="label">COMPLETE REAL SQUARE</span><span class="label">Q-GROWTH OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76C STEP 54</strong><p>q：fixed integer q &gt;= 1</p><p>modes：n_j in N</p><p>phases：phi_j in R</p><p>band：n_1 &lt; ... &lt;= 2 n_1</p><p>B branch：n_1 R &lt;= 1</p><p>C branch：n_1 R &gt; 1</p><p>clock：tau = lambda s</p><p>family：pointwise C.12</p><p>weighted：lambda^(-1/3)</p><p>terminal：lambda^0</p><p>field：complete real G^2</p><p>growing q：OPEN</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step54_sections() + '\n<section id="reproduce">', "Step 54 sections")
    evidence = '''<section id="reproduce"><div class="section-no">C / 冻结证据</div><h2>Step 54 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076c_full_frequency_fixed_mode_flux_payment.md">Step 54 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076c_full_frequency_fixed_mode_flux_payment_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076c_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076c_full_frequency_fixed_mode_flux_payment_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076c_full_frequency_fixed_mode_flux_payment_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076c_full_frequency_fixed_mode_flux_payment_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076c_full_frequency_fixed_mode_flux_payment_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076c_full_frequency_fixed_mode_flux_payment_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076c_full_frequency_fixed_mode_flux_payment_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076c_full_frequency_fixed_mode_flux_payment_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076c_full_frequency_fixed_mode_flux_payment_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076c_full_frequency_fixed_mode_flux_payment_qa.sh">QA script</a></p><p><a href="/notes/r0-76c.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75w.html">上一大里程碑累计回顾（截止 R0.75W）</a> · <a href="/recap-r0-61-r0-75w.pdf">W recap PDF</a></p><p class="note">Certificate：Python 140/140、Ruby 140/140、C.1--C.35、35/35 tags 与 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 140/140 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 continuum Turan--Nazarov theorem；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 54 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>B 的逆半径分支与 C 的超高热时钟支付</h2><p><a href="#s-416">B：n_1 R &lt;= 1 inverse-radius payment</a> · <a href="#s-425">C：n_1 R &gt; 1 ultra-high heat-clock payment</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 54 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">growing packets, arbitrary fields, and Version-M extraction remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.76C Step 54 停止。B 与 C 合并后只对每个固定有限 q 的 exact real dyadic-band shear 覆盖全部 carrier；常数不对 growing q 一致。arbitrary growing packets、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 54 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.32"', 'data-site-version="2.33"', "home version"),
        ("/i18n-en.js?v=2.32", "/i18n-en.js?v=2.33", "home i18n"),
        ("/site-refresh.js?v=2.32.1", "/site-refresh.js?v=2.33.1", "home refresh"),
        ("<strong>v2.32</strong>网页版本", "<strong>v2.33</strong>网页版本", "home stat version"),
        ("<strong>R0.76B</strong>最新研究节点", "<strong>R0.76C</strong>最新研究节点", "home latest"),
        ("<strong>256</strong>公开研究笔记", "<strong>257</strong>公开研究笔记", "home public count"),
        ("展开 166 篇公开笔记", "展开 167 篇公开笔记", "home route count"),
        ("综述 v2.32 · 2026-09-04", "综述 v2.33 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.76B", "Research topology · R0.1–R0.76C", "home topology"),
        ('href="#r076b">跳到首页 R0.76B 卡片 →', 'href="#r076c">跳到首页 R0.76C 卡片 →', "home jump"),
        ("R0.70A–R0.76B：158 节已公开，104 节完整封存", "R0.70A–R0.76C：159 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.76B</span>', '<span class="route-range">R0.69P–R0.76C</span>', "home range"),
        ("<h3>R0.76B：固定有限倍频带剪切的逆半径通量支付</h3>", "<h3>R0.76C：固定有限倍频带剪切的全频通量支付</h3>", "home route title"),
        ("R0.72R–R0.76B：</span>", "R0.72R–R0.76C：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.76B"', 'aria-label="R0.69P–R0.76C"', "home links label"),
        ("全站现有 256 篇公开研究笔记", "全站现有 257 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.76C Step 54 对每个固定整数 q 的 exact real dyadic-band shear 支付 n_1 R &gt; 1 的 ultra-high heat-clock 分支；与 B 的 n_1 R &lt;= 1 合并后覆盖全部 carrier。C.14 只适用于逐点满足 C.12 的 exponential-polynomial family，完整实场平方在取绝对值前保留全部 self/cross terms。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76C · 2026-09-04 · STEP 54 · FIXED-Q FULL-FREQUENCY FLUX PAYMENT</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">C 对固定整数 q、正整数频率与实相位的 exact real dyadic-band shear 支付 n_1 R &gt; 1；与 B 的 n_1 R &lt;= 1 合并后覆盖全部 carrier。加权与终端 lambda 幂分别为 -1/3 与 0，完整实场平方在绝对值之前重组全部 self/cross terms。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76c.pdf">阅读最新 R0.76C 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾仍截止 R0.75W（191 节）</a><a href="/notes/">257 篇研究笔记总索引</a><a href="#r076c">查看首页 R0.76C 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76C · 159 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76C Step 54 fixed-q full-frequency flux payment</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">B pays n_1 R &lt;= 1 and C uses the ultra-high heat clock for n_1 R &gt; 1, so every carrier is covered for each fixed finite exact real dyadic shear.</p>', "home current summary")
    page = replace_once(page, 'unresolved-cluster envelope/current normal form → complete-clock localized sign obstruction → complete-real-square fixed-q inverse-radius payment / growing q, n_1 R &gt; 1, arbitrary fields, and Version-M extraction open</p>', 'complete-clock localized sign obstruction → complete-real-square inverse-radius payment → ultra-high heat-clock payment / all carriers closed for fixed q; growing q, arbitrary fields, and Version-M extraction open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-76b.html">R0.76B</a>', '<a class="milestone" href="/notes/r0-76b.html">R0.76B</a>\n<a class="milestone" href="/notes/r0-76c.html">R0.76C</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>growing packets, arbitrary-field transfer, and Version-M extraction</h3><p>B 与 C 合并后只对每个固定有限 q 的 exact real dyadic-band shear 覆盖全部 carrier。q-uniform growing packets、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、regularity 与 singularity 仍开放。后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r076c" data-release="r076c" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76C Step 54 · 2026-09-04 · FIXED-Q FULL-FREQUENCY FLUX PAYMENT</p><h3>{TITLE}</h3><p>固定整数 q、正整数频率与实相位；C 用 ultra-high heat clock 支付 n_1 R &gt; 1，与 B 的 n_1 R &lt;= 1 合并后覆盖全部 carrier。C.14 明确限定 pointwise exponential-polynomial family；完整实场平方保留所有 self/cross terms。q-uniform growing packets、arbitrary fields 与 unconditional Version-M 仍开放。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-76c.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76c.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap 仍截止 W</a></p></div>\n'''
    anchor = '<div class="task-one" id="r076b"'
    if anchor not in page:
        raise RuntimeError("home R0.76B card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.32"', 'data-site-version="2.33"', "literature version"),
        ("/i18n-en.js?v=2.32", "/i18n-en.js?v=2.33", "literature i18n"),
        ("文献综述 v2.32 · 2026-09-04", "文献综述 v2.33 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.76B 只列为研究笔记", "本站 R0.69P–R0.76C 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76C</b><strong>fixed-q full-frequency flux payment by the ultra-high heat clock</strong></header><p>Step 54 对每个固定整数 q 的 exact real dyadic-band shear 支付 n_1 R &gt; 1：C 用 pointwise exponential-polynomial clock、cutoff onset 与完整实场平方保留 lambda 的正确幂。与 B 的 n_1 R &lt;= 1 合并后覆盖全部 carrier；常数不对 growing q 一致。<a href="/notes/r0-76c.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">保留的 W milestone recap</a> <a href="#r076c-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>growing packets, arbitrary-field transfer, and Version-M extraction</strong></header><p>q-uniform growing packets、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、regularity 与 singularity 均未闭合。后续材料未授权、未读取、未公开。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · 后续未授权</b>[\s\S]*?</div>', route, "literature route")
    boundary = (
        '<h3 id="r076c-boundary">R0.76C Step 54 的 bounded primary-source screen 与主张边界</h3>'
        '<p><a href="https://www.mathnet.ru/eng/aa397">Nazarov 1993/1994</a> 与 <a href="https://arxiv.org/abs/1107.0039">Friedland--Yomdin 2013</a> 支持 finite exponential polynomial 的 measurable-set Turan--Nazarov inequality，以及不依赖虚部频率或 exponent gap 的边界。C 的 polynomial-exponential decay、weighted tail、terminal estimate、cutoff-onset gain、complete-real-square identity 与 physical scaling 都是本地推导；bounded collision screen 不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.76C Step 54 公开边界 · FIXED-Q FULL-FREQUENCY EXACT-SHEAR PAYMENT</strong><p>'
        'PROVED：固定整数 q、n_j in N、phi_j in R、exact real dyadic band 1 &lt;= n_1 &lt; ... &lt;= 2 n_1；对所有充分大的 frozen L，在全部 carrier 下有 |T| &lt;= C_q a^(2/3) R^(-1/3) M^(2/3)。B 覆盖 n_1 R &lt;= 1，C 覆盖 n_1 R &gt; 1。C.12--C.21 只对逐点满足 C.12 的 exponential-polynomial family 建立稳定 heat-clock tail；C.22--C.27 保留 weighted lambda^(-1/3) 与 terminal lambda^0；C.28--C.34 对完整实场平方做能量与尺度支付。'
        'NARROW CONSEQUENCE：在这一 fixed-q exact-shear 范围内，所有 carrier 已覆盖；证明不依赖 exponent gap、imaginary frequency、localized-current positivity 或 standalone carrier integration by parts。'
        'CONDITIONAL：任何 Version-M consequence 仍要求同一 velocity component 与同一 measurement row；非零常背景尚未放入 frozen mean-zero Version-M subclass。'
        'OPEN：q-uniform growing q、arbitrary growing packets、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。finite checks 不代替 continuum Turan--Nazarov theorem；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>FIXED Q ONLY. EXACT SHEAR ONLY. C.14 POINTWISE EXPONENTIAL-POLYNOMIAL FAMILY ONLY. NO UNCONDITIONAL VERSION-M. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76c.html">阅读完整笔记</a> · '
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
    if html_count != 257 or pdf_count not in (213, 214):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 197:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76c.html",
        "latestPublishedResearchPdf": "/notes/r0-76c.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "latestRecapRelease": "R0.75W",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r076b":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 159
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 54
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "FIXED_Q_FULL_FREQUENCY_EXACT_REAL_DYADIC_SHEAR_FLUX_PAYMENT",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_FIXED_Q_FULL_FREQUENCY_EXACT_SHEAR_PAYMENT",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "fixed_q": "PROVED_FOR_EACH_FIXED_INTEGER_Q_GE_1_NOT_UNIFORM_IN_GROWING_Q",
            "integer_modes": "REQUIRED_NJ_IN_POSITIVE_INTEGERS",
            "real_phases": "REQUIRED_PHIJ_IN_REAL_NUMBERS",
            "dyadic_band": "REQUIRED_ONE_LE_N1_LT_DOTS_LT_NQ_LE_TWO_N1",
            "large_frozen_L_gate": "REQUIRED_ALL_SUFFICIENTLY_LARGE_FROZEN_L",
            "all_carriers": "PROVED_FOR_EACH_FIXED_Q_EXACT_REAL_DYADIC_SHEAR",
            "inverse_radius_branch": "PAID_BY_R076B_N1_R_LE_ONE",
            "ultra_high_branch": "PROVED_HERE_N1_R_GT_ONE",
            "branch_exhaustion": "PROVED_ALL_CARRIERS_B_AND_C",
            "spatial_observation": "R076B_GAP_FREE_VALUE_AND_DERIVATIVE_OBSERVATION",
            "temporal_trace": "POINTWISE_EXPONENTIAL_POLYNOMIAL_FAMILY_SATISFYING_C12_ONLY",
            "heat_clock": "TAU_EQUALS_LAMBDA_S_REAL_PARTS_MINUS4_TO_MINUS1",
            "weighted_lambda_power": "MINUS_ONE_THIRD",
            "terminal_lambda_power": "ZERO",
            "complete_real_square": "RETAINED_BEFORE_ABSOLUTE_VALUES",
            "self_cross_terms": "ALL_REASSEMBLED_BEFORE_ABSOLUTE_VALUES",
            "localized_current_sign": "NOT_USED_R076A_OBSTRUCTION_BYPASSED",
            "gradient_absorption": "LAMBDA_PAID_BY_CUTOFF_ONSET_AND_WEIGHTED_HEAT_CLOCK",
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
            "python_certificate": "PASS_140_OF_140",
            "independent_ruby": "PASS_140_OF_140",
            "negative_mutations": "PASS_PYTHON_140_OF_140_RUBY_140_OF_140",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_C1_TO_C35_TAGS_AND_DISPLAYS_35_OF_35",
            "exact_fixtures": "PASS_Q3_N1R2_LAMBDA4_T16_PDE_ENERGY_AND_SCALE_LEDGER",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76c.html",
            "target_pdf": "/notes/r0-76c.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "retained_recap_terminal_release": "R0.75W_STEP48",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076c_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 54,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "postR070APublishedReleaseCount": 159,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r076d",
        "latestPublishedResearchHtml": "/notes/r0-76c.html",
        "latestPublishedResearchPdf": "/notes/r0-76c.pdf",
        "latestReleaseGate": "tests/r076c-step54-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r076c-step54-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076c-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076c-step54-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076c-step54-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076c-step54-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076c-step54-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076c-step54",
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
    write_text(PUBLIC / "notes/r0-76c.html", render_note())
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
        "latestCompletedStep": 54,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 191,
        "formalFigure": None,
        "formalFigureExemption": True,
        "simulation": False,
        "pdeData": False,
        "noveltyClaim": False,
        "clayClaim": False,
        "fixedQFullFrequencyPayment": True,
        "growingQClaim": False,
        "ultraHighCarrierBranch": "PROVED_N1_R_GT_ONE",
        "arbitraryFieldClaim": False,
        "unconditionalVersionMClaim": False,
        "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
