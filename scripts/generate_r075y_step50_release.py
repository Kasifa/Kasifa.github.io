#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75Y Step 50 from the verified R0.75X Step 49 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075x_step49_release as previous
import import_r075y_step50_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "2bcce5b77ce1f82077e21859cbf65795ce70124a"
VERSION = "2.29"
RELEASE = "r075y"
CODE = "R0.75Y"
TITLE = "R0.75Y｜强分离多谐波族的完整 signed-flux 付款"
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
            raise RuntimeError(f"R0.75Y frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075y_strongly_separated_multimode_flux_payment_certificate.json").read_text()
    )
    summary = certificate.get("summary", {})
    if (
        summary.get("verdict") != "PASS"
        or summary.get("assertions") != 17
        or summary.get("passed") != 17
        or summary.get("failed") != 0
        or len(certificate.get("assertions", [])) != 17
    ):
        raise RuntimeError("R0.75Y certificate verdict drift")
    main = (ROOT / "research/r075y_strongly_separated_multimode_flux_payment.md").read_text()
    for token in (
        r"\tag{Y.1}", r"\tag{Y.3}", r"\tag{Y.6}", r"\tag{Y.9}",
        r"\tag{Y.18}", r"\tag{Y.21}", r"\tag{Y.28}", r"\tag{Y.39}",
        "all displayed mode-count dependence is the\nexplicit factor `q^2`",
        "unresolved spectral clusters", "sparse class when `q` grows", "not valid merely for a Fourier projection",
        "**NOT CLAY.**",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75Y boundary drift: {token}")
    source_report = (ROOT / "research/r075y_report-source.md").read_text()
    if "not evidence of completeness, novelty, or priority" not in " ".join(source_report.split()):
        raise RuntimeError("R0.75Y bounded source-claim boundary drift")


def render_step50_sections() -> str:
    source = (ROOT / "research/r075y_strongly_separated_multimode_flux_payment.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 392
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
        else:
            output.append(f"<p>{inline_markup(stripped)}</p>")
    if section_open:
        output.append("</section>")
    if section_index != 400:
        raise RuntimeError(f"Step 50 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;").replace("qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.28"', 'data-site-version="2.29"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.28", "/i18n-en.js?v=2.29", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Complete signed collar-flux payment for a strongly separated multimode exact shear, with explicit q-squared cost and unresolved-cluster boundary.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75y.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75Y · STEP 50 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75Y · Step 50 · STRONGLY SEPARATED MULTIMODE</div><h1>{TITLE}</h1><p>Y 关闭三模以上 high-carrier sector 的一个定量分离子类：对同一 dyadic band 的 exact real diffusive shear，若 signed-spectrum gap 满足 <strong>aR delta_n &gt;= 8q</strong>，则全部 self、difference 与 sum rows 共 <strong>q^2</strong> 项都由 plateau cubic mass 支付。代价显式为 q^2，簇拥区域仍开放；精确对数率为 <strong>-2/11907</strong>。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">STRONGLY SEPARATED</span><span class="label">HIGH-CARRIER SUBSECTOR</span><span class="label">SIGNED-SPECTRUM GAP</span><span class="label">GRAM COERCIVITY</span><span class="label">PHASE-FREE CLOCK</span><span class="label">ALL q^2 ROWS</span><span class="label">EXPLICIT q^2 COST</span><span class="label">NO HIDDEN q CONSTANT</span><span class="label">R POWERS CANCEL</span><span class="label">EXACT RATE -2/11907</span><span class="label">CLUSTERS OPEN</span><span class="label">VERSION-M CONDITIONAL</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75Y STEP 50</strong><p>scope：strongly separated</p><p>band：n_1&lt;...&lt;n_q&lt;=2n_1</p><p>gap：aR delta_n &gt;= 8q</p><p>rows：q^2 exact</p><p>cost：explicit q^2</p><p>clock：T_R = 4R^2</p><p>payment：q^2 a^(2/3)R^(-1/3)M^(2/3)</p><p>growing q：log q=o(L^2), sparse class</p><p>rate：-2/11907</p><p>open：unresolved clusters / packets</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step50_sections() + '\n<section id="reproduce">', "Step 50 sections")
    evidence = '''<section id="reproduce"><div class="section-no">Y / 冻结证据</div><h2>Step 50 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075y_strongly_separated_multimode_flux_payment.md">Step 50 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075y_strongly_separated_multimode_flux_payment_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075y_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075y_strongly_separated_multimode_flux_payment_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075y_strongly_separated_multimode_flux_payment_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075y_strongly_separated_multimode_flux_payment_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075y_strongly_separated_multimode_flux_payment_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075y_strongly_separated_multimode_flux_payment_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075y_strongly_separated_multimode_flux_payment_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075y_strongly_separated_multimode_flux_payment_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075y_strongly_separated_multimode_flux_payment_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075y_strongly_separated_multimode_flux_payment_qa.sh">QA script</a></p><p><a href="/notes/r0-75y.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75w.html">上一大里程碑累计回顾（截止 R0.75W）</a> · <a href="/recap-r0-61-r0-75w.pdf">W recap PDF</a></p><p class="note">Certificate：Python 17/17、Ruby 18/18、Y.1--Y.39、39/39 tags 与 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 85/85 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 continuum Gram 或 complete-clock lemmas；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 50 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>X 与 Y 的精确分工</h2><p><a href="#s-384">X：fixed-finite low-carrier family</a> · <a href="#s-393">Y：strongly separated high-carrier family</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 50 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">unresolved clusters and arbitrary packets remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.75Y Step 50 停止。Y 只支付满足 aR delta_n &gt;= 8q 的 strongly separated exact common-shear family；unresolved high-carrier clusters、weakening the separation condition、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 50 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.28"', 'data-site-version="2.29"', "home version"),
        ("/i18n-en.js?v=2.28", "/i18n-en.js?v=2.29", "home i18n"),
        ("/site-refresh.js?v=2.28.1", "/site-refresh.js?v=2.29.1", "home refresh"),
        ("<strong>v2.28</strong>网页版本", "<strong>v2.29</strong>网页版本", "home stat version"),
        ("<strong>R0.75X</strong>最新研究节点", "<strong>R0.75Y</strong>最新研究节点", "home latest"),
        ("<strong>252</strong>公开研究笔记", "<strong>253</strong>公开研究笔记", "home public count"),
        ("展开 162 篇公开笔记", "展开 163 篇公开笔记", "home route count"),
        ("综述 v2.28 · 2026-09-04", "综述 v2.29 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75X", "Research topology · R0.1–R0.75Y", "home topology"),
        ('href="#r075x">跳到首页 R0.75X 卡片 →', 'href="#r075y">跳到首页 R0.75Y 卡片 →', "home jump"),
        ("R0.70A–R0.75X：154 节已公开，104 节完整封存", "R0.70A–R0.75Y：155 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75X</span>', '<span class="route-range">R0.69P–R0.75Y</span>', "home range"),
        ("<h3>R0.75X：固定有限谐波族的低载频 signed-flux 付款</h3>", "<h3>R0.75Y：强分离多谐波族的完整 signed-flux 付款</h3>", "home route title"),
        ("R0.72R–R0.75X：</span>", "R0.72R–R0.75Y：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75X"', 'aria-label="R0.69P–R0.75Y"', "home links label"),
        ("全站现有 252 篇公开研究笔记", "全站现有 253 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75Y Step 50 支付满足 aR delta_n &gt;= 8q 的 strongly separated exact common-shear family：全部 q^2 个 self、difference 与 sum rows 得到显式 q^2 代价。簇拥区域、任意 packets 与一般 Version-M extraction 仍开放。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75Y · 2026-09-04 · STEP 50 · STRONGLY SEPARATED MULTIMODE</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">Y 用 signed-spectrum Gram coercivity、phase-free complete-clock lemma 与 exact q^2 modal expansion，支付 strongly separated high-carrier family。显式代价为 q^2；unresolved clusters 与 arbitrary packets 仍开放。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75y.pdf">阅读最新 R0.75Y 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾仍截止 R0.75W（191 节）</a><a href="/notes/">253 篇研究笔记总索引</a><a href="#r075y">查看首页 R0.75Y 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75Y · 155 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75Y Step 50 strongly separated multimode payment</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">X pays every fixed finite family in the low-carrier sector. Y pays the strongly separated high-carrier sector with an explicit q^2 factor; unresolved clusters and arbitrary packets remain open.</p>', "home current summary")
    page = replace_once(page, 'high-carrier spatial coercivity → difference row → coupled self/sum block → full-frequency exact pair → fixed-finite low-carrier family / q-growth, high-carrier 3+ modes, and packets open</p>', 'exact-pair full-frequency closure → fixed-finite low-carrier family → strongly separated high-carrier family with q^2 cost / unresolved clusters and packets open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75x.html">R0.75X</a>', '<a class="milestone" href="/notes/r0-75x.html">R0.75X</a>\n<a class="milestone" href="/notes/r0-75y.html">R0.75Y</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>unresolved clusters and arbitrary packets</h3><p>Y 只关闭 aR delta_n &gt;= 8q 的强分离子类。簇拥的 high-carrier modes、分离条件弱化、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、E.24 与 Version-M extraction 仍开放。后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075y" data-release="r075y" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75Y Step 50 · 2026-09-04 · STRONGLY SEPARATED MULTIMODE</p><h3>{TITLE}</h3><p>Y 对满足 aR delta_n&gt;=8q 的 strongly separated exact common-shear family 证明 complete signed collar-flux payment；exact Gram coercivity 与 phase-free clock 支付全部 q^2 rows，代价显式为 q^2。unresolved clusters 与 arbitrary packets 仍开放。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75y.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75y.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap 仍截止 W</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075x"'
    if anchor not in page:
        raise RuntimeError("home R0.75X card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.28"', 'data-site-version="2.29"', "literature version"),
        ("/i18n-en.js?v=2.28", "/i18n-en.js?v=2.29", "literature i18n"),
        ("文献综述 v2.28 · 2026-09-04", "文献综述 v2.29 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75X 只列为研究笔记", "本站 R0.69P–R0.75Y 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>quantitative q-growth, high-carrier three-plus modes, and arbitrary packets</strong></header><p>q=q(L) 的定量 spatial constant、三模以上 high-carrier sector、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、E.24 与 Version-M extraction 均未闭合。后续材料未授权、未读取、未公开。</p></div>'
    route = f'<div class="route-step kept"><header><b>R0.75Y</b><strong>strongly separated multimode complete payment</strong></header><p>Step 50 用 signed-spectrum Gram coercivity、phase-free complete-clock lemma、exact q^2 modal row count 与 plateau mass，支付 aR delta_n&gt;=8q 的 strongly separated exact common-shear family。显式 mode-count 代价为 q^2；簇拥区域仍开放。<a href="/notes/r0-75y.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">保留的 W milestone recap</a> <a href="#r075y-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>unresolved clusters and arbitrary packets</strong></header><p>unresolved high-carrier clusters、分离条件弱化、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、E.24 与 Version-M extraction 均未闭合。后续材料未授权、未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075y-boundary">R0.75Y Step 50 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Jaming--Saba 2023 的 survey 与 Kunis--Möller--Peter--von der Ohe 2017 的 separated-frequency reconstruction 记录只提供 classical Ingham-type context。Y 不导入外部 theorem，而以 finite signed-spectrum Gram calculation 直接得到分离条件下的 L2 coercivity。有限检索不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.75Y Step 50 公开边界 · STRONGLY SEPARATED · EXPLICIT q^2 COST</strong><p>'
        'PROVED：Y.1--Y.3 signed-spectrum gap 与 strong separation；Y.15--Y.19 phase-uniform Gram coercivity；Y.20--Y.25 phase-free complete-clock lemma；Y.26--Y.34 exact radial/modal expansion 与 q^2 row payment；Y.35--Y.37 plateau mass 与 physical payment；Y.7--Y.9 normalized estimate、R-power cancellation、显式 q^2 cost 与 -2/11907 rate；Y.38 exact smooth unforced shear。CONDITIONAL：growing-q rate 还要求 log q=o(L^2) 且 strong separation 持续成立；Version-M consequence 仍要求 measurement row、weight、realized subclass、actual component 与 ledger alignment。'
        'OPEN：aR delta_n&lt;8q 的 unresolved clusters；strong separation 的移除或弱化；arbitrary packets；inter-packet aggregation；nonconstant or vertically dependent shear；projection；arbitrary-field E.24；complete Version-M extraction；fixed deletion；suitable-weak transfer；regularity 与 singularity。finite checks 不代替 continuum lemmas；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>STRONGLY SEPARATED ONLY. EXPLICIT q^2 COST. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75y.html">阅读完整笔记</a> · '
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
    if html_count != 253 or pdf_count not in (209, 210):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 193:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75y.html",
        "latestPublishedResearchPdf": "/notes/r0-75y.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "latestRecapRelease": "R0.75W",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075x":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 155
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 50
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "STRONGLY_SEPARATED_MULTIMODE_SIGNED_FLUX_PAYMENT",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_STRONGLY_SEPARATED_MULTIMODE_THEOREM",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "harmonic_scope": "STRONGLY_SEPARATED_FINITE_REAL_FAMILY_ONE_DYADIC_BAND",
            "strong_separation": "PROVED_ASSUMPTION_Y3_A_R_DELTA_N_GE_8Q",
            "explicit_mode_count_cost": "Q_SQUARED_NO_HIDDEN_Q_CONSTANT",
            "signed_spectrum_gram": "PROVED_Y15_Y19",
            "phase_free_complete_clock": "PROVED_Y20_Y25_WITH_ETA_ZERO_ONSET",
            "modal_row_count": "EXACTLY_Q_SQUARED_SELF_DIFFERENCE_SUM_ROWS",
            "radial_quotient_and_payment": "PROVED_Y26_Y37",
            "normalized_estimate": "PROVED_Y7_Y9_R_POWERS_CANCEL",
            "exact_l2_rate": "MINUS_2_OVER_11907_FIXED_Q_OR_LOG_Q_O_L2_WITH_SEPARATION",
            "exact_smooth_unforced_shear_solution": "PROVED_Y38",
            "version_m_same_velocity_inclusion": "CONDITIONAL_MEASUREMENT_WEIGHT_REALIZED_SUBCLASS_ACTUAL_COMPONENT_LEDGER_ALIGNMENT",
            "unresolved_high_carrier_clusters": "OPEN_A_R_DELTA_N_LT_8Q",
            "weakened_separation": "OPEN_NOT_PROVED",
            "arbitrary_packets_and_inter_packet_aggregation": "OPEN_NOT_PROVED",
            "projection_from_larger_velocity": "OPEN_NOT_PROVED",
            "nonconstant_or_vertically_dependent_shear": "OPEN_NOT_PROVED",
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
            "python_certificate": "PASS_17_OF_17",
            "independent_ruby": "PASS_18_OF_18",
            "negative_mutations": "PASS_PYTHON_85_OF_85_RUBY_85_OF_85",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_Y1_TO_Y39_TAGS_AND_DISPLAYS_39_OF_39",
            "exact_fixtures": "PASS_Q3_GRAM_ROW_COUNT_SCALE",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75y.html",
            "target_pdf": "/notes/r0-75y.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "retained_recap_terminal_release": "R0.75W_STEP48",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075y_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 50,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "postR070APublishedReleaseCount": 155,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075z",
        "latestPublishedResearchHtml": "/notes/r0-75y.html",
        "latestPublishedResearchPdf": "/notes/r0-75y.pdf",
        "latestReleaseGate": "tests/r075y-step50-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075y-step50-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075y-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075y-step50-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075y-step50-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075y-step50-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075y-step50-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075y-step50",
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
    write_text(PUBLIC / "notes/r0-75y.html", render_note())
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
        "latestCompletedStep": 50,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 191,
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
