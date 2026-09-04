#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.76A Step 52 from the verified R0.75Z Step 51 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075z_step51_release as previous
import import_r076a_step52_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "8649d96e0943cc162a4b95cc2c4eaab704bfa7a7"
VERSION = "2.31"
RELEASE = "r076a"
CODE = "R0.76A"
TITLE = "R0.76A｜完整时钟局部载频电流负号障碍"
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
            raise RuntimeError(f"R0.76A frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r076a_complete_clock_localized_current_sign_obstruction_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or len(certificate.get("assertions", [])) != 15
        or not all(row.get("pass") is True for row in certificate.get("assertions", []))
        or len(certificate.get("negativeMutations", [])) != 86
    ):
        raise RuntimeError("R0.76A certificate verdict drift")
    main = (ROOT / "research/r076a_complete_clock_localized_current_sign_obstruction.md").read_text()
    compact_main = " ".join(main.split())
    for token in (
        r"\tag{A.1}", r"\tag{A.3}", r"\tag{A.8}", r"\tag{A.9}",
        r"\tag{A.10}", r"\tag{A.17}", r"\tag{A.31}", r"\tag{A.34}",
        r"0<\delta_0<\delta", "actual unresolved high-carrier cluster",
        "full-period current is nonnegative, but the collar multiplier is local",
        "localized carrier-current row by sign", "not a counterexample to the two-mode collar-flux estimate",
        "positive carrier-density term", "quantitative localized current estimate",
        "Version-M extraction", "**NOT CLAY.**",
    ):
        if token not in compact_main:
            raise RuntimeError(f"R0.76A boundary drift: {token}")
    source_report = (ROOT / "research/r076a_report-source.md").read_text()
    compact = " ".join(source_report.split())
    if "bounded negative search is not represented as evidence of novelty" not in compact:
        raise RuntimeError("R0.76A bounded source-claim boundary drift")


def render_step52_sections() -> str:
    source = (ROOT / "research/r076a_complete_clock_localized_current_sign_obstruction.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 408
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
    if section_index != 415:
        raise RuntimeError(f"Step 52 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;").replace("qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.30"', 'data-site-version="2.31"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.30", "/i18n-en.js?v=2.31", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Complete-clock strict negativity of a localized carrier-current row for an exact unresolved two-mode cluster, with narrow method boundary.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76a.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76A · STEP 52 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76A · Step 52 · COMPLETE-CLOCK LOCALIZED CURRENT SIGN OBSTRUCTION</div><h1>{TITLE}</h1><p>A 在实际冻结 collar primitive 与完整时钟上构造 exact q=2 unresolved high-carrier cluster，证明局部载频电流及 correction row 严格为负。它只排除凭单边 offset spectrum 丢弃该行或宣称其非负的证明步骤；不反驳 W 的两模态通量估计，也不排除 perturbative、nonlocal signed 或 joint density/carrier cancellation。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">0 &lt; DELTA_0 &lt; DELTA</span><span class="label">ACTUAL COLLAR PRIMITIVE</span><span class="label">COMPLETE CLOCK</span><span class="label">Q=2 UNRESOLVED CLUSTER</span><span class="label">LOCAL CURRENT STRICTLY NEGATIVE</span><span class="label">CORRECTION ROW STRICTLY NEGATIVE</span><span class="label">CARRIER DENSITY RETAINED</span><span class="label">SIGN-DROPPING CLOSED</span><span class="label">W TWO-MODE PAYMENT INTACT</span><span class="label">PERTURBATIVE ROUTE OPEN</span><span class="label">NONLOCAL SIGNED ROUTE OPEN</span><span class="label">JOINT CANCELLATION OPEN</span><span class="label">VERSION-M CONDITIONAL</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76A STEP 52</strong><p>profile：0 &lt; delta_0 &lt; delta</p><p>carrier：N=ceil(16/ell)</p><p>cluster：(N,N+1), q=2</p><p>clock：0 &lt;= s &lt;= 4</p><p>primitive：Xi_a &gt;= 0, positive mass</p><p>current：J &lt; 0 locally</p><p>correction：|Z_z|^2+2 alpha J &lt; 0</p><p>positive density row：retained</p><p>obstruction：sign-dropping only</p><p>general cluster payment：OPEN</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step52_sections() + '\n<section id="reproduce">', "Step 52 sections")
    evidence = '''<section id="reproduce"><div class="section-no">A / 冻结证据</div><h2>Step 52 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076a_complete_clock_localized_current_sign_obstruction.md">Step 52 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076a_complete_clock_localized_current_sign_obstruction_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076a_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076a_complete_clock_localized_current_sign_obstruction_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076a_complete_clock_localized_current_sign_obstruction_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076a_complete_clock_localized_current_sign_obstruction_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076a_complete_clock_localized_current_sign_obstruction_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076a_complete_clock_localized_current_sign_obstruction_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076a_complete_clock_localized_current_sign_obstruction_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076a_complete_clock_localized_current_sign_obstruction_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076a_complete_clock_localized_current_sign_obstruction_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076a_complete_clock_localized_current_sign_obstruction_qa.sh">QA script</a></p><p><a href="/notes/r0-76a.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75w.html">上一大里程碑累计回顾（截止 R0.75W）</a> · <a href="/recap-r0-61-r0-75w.pdf">W recap PDF</a></p><p class="note">Certificate：Python 15/15、Ruby 15/15、A.1--A.34、34/34 tags 与 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 86/86 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 continuum identities；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 52 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>Z 的局部载频问题与 A 的严格负号障碍</h2><p><a href="#s-401">Z：cluster normal form and current gate</a> · <a href="#s-409">A：actual primitive, complete clock, and strict localized negativity</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 52 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">general clustered-sector payment remains OPEN</h2><p style="margin:.15rem 0">本站在 R0.76A Step 52 停止。A 只证明实际 primitive 与完整时钟上的 localized current/correction row 严格负号，排除凭单边 offset spectrum 丢弃该行或宣称非负。W 的 exact q=2 通量支付保持有效；perturbative estimate、localized boundary error、nonlocal signed estimate、joint density/carrier cancellation、一般簇支付、跨簇聚合、E.24、complete Version-M extraction、regularity 与 singularity 仍开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 52 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.30"', 'data-site-version="2.31"', "home version"),
        ("/i18n-en.js?v=2.30", "/i18n-en.js?v=2.31", "home i18n"),
        ("/site-refresh.js?v=2.30.1", "/site-refresh.js?v=2.31.1", "home refresh"),
        ("<strong>v2.30</strong>网页版本", "<strong>v2.31</strong>网页版本", "home stat version"),
        ("<strong>R0.75Z</strong>最新研究节点", "<strong>R0.76A</strong>最新研究节点", "home latest"),
        ("<strong>254</strong>公开研究笔记", "<strong>255</strong>公开研究笔记", "home public count"),
        ("展开 164 篇公开笔记", "展开 165 篇公开笔记", "home route count"),
        ("综述 v2.30 · 2026-09-04", "综述 v2.31 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75Z", "Research topology · R0.1–R0.76A", "home topology"),
        ('href="#r075z">跳到首页 R0.75Z 卡片 →', 'href="#r076a">跳到首页 R0.76A 卡片 →', "home jump"),
        ("R0.70A–R0.75Z：156 节已公开，104 节完整封存", "R0.70A–R0.76A：157 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75Z</span>', '<span class="route-range">R0.69P–R0.76A</span>', "home range"),
        ("<h3>R0.75Z：未解簇正规形与载频电流门</h3>", "<h3>R0.76A：完整时钟局部载频电流负号障碍</h3>", "home route title"),
        ("R0.72R–R0.75Z：</span>", "R0.72R–R0.76A：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75Z"', 'aria-label="R0.69P–R0.76A"', "home links label"),
        ("全站现有 254 篇公开研究笔记", "全站现有 255 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.76A Step 52 在实际冻结 primitive 与完整时钟上证明 exact q=2 unresolved cluster 的 localized current/correction row 严格为负；它只排除依赖单边 offset spectrum 的 sign-dropping。W 的两模态通量付款保持有效，一般簇支付与联合抵消仍开放。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76A · 2026-09-04 · STEP 52 · COMPLETE-CLOCK LOCALIZED CURRENT SIGN OBSTRUCTION</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">A 用 actual collar primitive、complete clock 与 exact q=2 unresolved cluster 证明 localized carrier current/correction row 严格负号，只排除 sign-dropping。W 的 two-mode flux estimate 不受影响；perturbative、nonlocal signed、joint density/carrier 与 general cluster payment 仍开放。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76a.pdf">阅读最新 R0.76A 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾仍截止 R0.75W（191 节）</a><a href="/notes/">255 篇研究笔记总索引</a><a href="#r076a">查看首页 R0.76A 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76A · 157 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76A Step 52 localized current sign obstruction</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Z isolates the clustered carrier-current row; A proves that this localized row and its correction can remain strictly negative across the complete clock, closing sign-dropping only while leaving joint payment open.</p>', "home current summary")
    page = replace_once(page, 'fixed-finite low-carrier family → strongly separated high-carrier family with q^2 cost → unresolved-cluster envelope and carrier-current gate / full cluster payment and aggregation open</p>', 'strongly separated high-carrier family → unresolved-cluster envelope/current normal form → complete-clock localized sign obstruction / perturbative, nonlocal signed, joint-block, and general cluster payment open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75z.html">R0.75Z</a>', '<a class="milestone" href="/notes/r0-75z.html">R0.75Z</a>\n<a class="milestone" href="/notes/r0-76a.html">R0.76A</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>joint density/carrier payment and general cluster control</h3><p>A 只排除 localized current/correction row 的 sign-dropping；W 的 exact q=2 通量估计保持有效。perturbative 与 boundary-error estimates、nonlocal signed control、joint density/carrier cancellation、一般簇支付、cross-cluster aggregation、arbitrary packets 与 Version-M extraction 仍开放。后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r076a" data-release="r076a" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76A Step 52 · 2026-09-04 · COMPLETE-CLOCK LOCALIZED CURRENT SIGN OBSTRUCTION</p><h3>{TITLE}</h3><p>A 物化 actual primitive、complete clock 与 exact q=2 unresolved high-carrier cluster 上的 current/correction strict negativity，只关闭 sign-dropping。W 的 two-mode payment 保持有效；perturbative、nonlocal signed、joint density/carrier cancellation 与 general cluster payment 仍开放。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-76a.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76a.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap 仍截止 W</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075z"'
    if anchor not in page:
        raise RuntimeError("home R0.75Z card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.30"', 'data-site-version="2.31"', "literature version"),
        ("/i18n-en.js?v=2.30", "/i18n-en.js?v=2.31", "literature i18n"),
        ("文献综述 v2.30 · 2026-09-04", "文献综述 v2.31 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75Z 只列为研究笔记", "本站 R0.69P–R0.76A 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76A</b><strong>complete-clock localized carrier-current sign obstruction</strong></header><p>Step 52 用 actual frozen primitive、complete clock 与 exact q=2 unresolved high-carrier cluster 证明 localized current/correction row 严格为负；它只排除凭单边 offset spectrum 的 sign-dropping。W 的 two-mode flux estimate 保持有效；perturbative、nonlocal signed、joint density/carrier cancellation 与 general cluster payment 仍开放。<a href="/notes/r0-76a.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">保留的 W milestone recap</a> <a href="#r076a-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>joint density/carrier payment and general cluster control</strong></header><p>perturbative estimate、localized boundary error、nonlocal signed control、joint density/carrier cancellation、full Z-sector payment、cross-cluster aggregation、arbitrary packets 与 Version-M extraction 均未闭合。后续材料未授权、未读取、未公开。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · 后续未授权</b>[\s\S]*?</div>', route, "literature route")
    boundary = (
        '<h3 id="r076a-boundary">R0.76A Step 52 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Nazarov、Kovrijkine、Egidi--Veselic 与 Jaming--Saba 只提供 finite exponential sums 与 spectral observation 的经典语境，不给出 positive-frequency polynomial 的 localized current positivity。A 的 strict sign obstruction 来自 actual primitive 与 exact two-term formula；bounded negative search 不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.76A Step 52 公开边界 · COMPLETE-CLOCK STRICT NEGATIVITY · SIGN-DROPPING ONLY</strong><p>'
        'PROVED：A.1--A.18 actual frozen primitive 的 nonnegativity、support 与 positive mass；A.19--A.22 complete-clock damping/phase bounds；A.23--A.31 exact q=2 unresolved cluster 的 localized current 与 correction row strict negativity；A.32 保留 positive carrier-density row；A.33--A.34 给出 current scaling 与 fixed-amplitude upper scale C R/a。'
        'NARROW CONSEQUENCE：只关闭凭 one-sided offset spectrum 丢弃 localized carrier current/correction row 或宣称其 nonnegative 的证明步骤；不是 R0.75W two-mode collar-flux estimate、一般簇支付、perturbative estimate、nonlocal signed estimate 或 joint density/carrier cancellation 的反例。'
        'CONDITIONAL：Version-M consequence 仍要求同一 measurement row、weight、realized subclass、actual component 与 ledger alignment。'
        'OPEN：general cluster-current estimate、joint density/carrier-block payment、full Z-sector payment、cross-cluster aggregation、arbitrary packets、E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。finite checks 不代替 continuum identities；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>W TWO-MODE PAYMENT INTACT. NO GENERAL CLUSTER PAYMENT. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76a.html">阅读完整笔记</a> · '
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
    if html_count != 255 or pdf_count not in (211, 212):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 195:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76a.html",
        "latestPublishedResearchPdf": "/notes/r0-76a.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "latestRecapRelease": "R0.75W",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075z":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 157
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 52
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "COMPLETE_CLOCK_LOCALIZED_CURRENT_SIGN_OBSTRUCTION",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_LOCALIZED_SIGN_OBSTRUCTION",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "profile_assumption": "PROVED_WITH_0_LT_DELTA0_LT_DELTA",
            "frozen_primitive": "PROVED_NONNEGATIVE_COMPACTLY_SUPPORTED_POSITIVE_MASS",
            "exact_cluster": "PROVED_Q2_UNRESOLVED_HIGH_CARRIER_N_AND_N_PLUS_1",
            "complete_clock_current": "PROVED_UNIFORMLY_STRICTLY_NEGATIVE_ON_PRIMITIVE_SUPPORT",
            "current_correction_row": "PROVED_UNIFORMLY_STRICTLY_NEGATIVE",
            "positive_carrier_density_row": "RETAINED_FULL_GRADIENT_NONNEGATIVE",
            "localized_sign_dropping": "CLOSED_ONLY_ONE_SIDED_OFFSET_SPECTRUM_DOES_NOT_GIVE_LOCAL_POSITIVITY",
            "r075w_two_mode_flux_payment": "INTACT_NOT_COUNTEREXAMPLE",
            "perturbative_boundary_nonlocal_joint_routes": "OPEN_NOT_DISPROVED",
            "full_clustered_sector_payment": "OPEN_NOT_PROVED_OR_DISPROVED",
            "general_cluster_current_estimate": "OPEN_NOT_PROVED_OR_DISPROVED",
            "joint_density_carrier_block_payment": "OPEN_NOT_PROVED",
            "cross_cluster_aggregation": "OPEN_NOT_PROVED",
            "counterexample_to_two_mode_or_general_cluster_flux": "NOT_CLAIMED",
            "version_m_same_velocity_inclusion": "CONDITIONAL_MEASUREMENT_WEIGHT_REALIZED_SUBCLASS_ACTUAL_COMPONENT_LEDGER_ALIGNMENT",
            "arbitrary_packets": "OPEN_NOT_PROVED",
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
            "negative_mutations": "PASS_PYTHON_86_OF_86_RUBY_86_OF_86",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_A1_TO_A34_TAGS_AND_DISPLAYS_34_OF_34",
            "exact_fixtures": "PASS_PRIMITIVE_CLOCK_Q2_CLUSTER_CURRENT_CORRECTION_PDE_AND_FULL_GRADIENT",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76a.html",
            "target_pdf": "/notes/r0-76a.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "retained_recap_terminal_release": "R0.75W_STEP48",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076a_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 52,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "postR070APublishedReleaseCount": 157,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r076b",
        "latestPublishedResearchHtml": "/notes/r0-76a.html",
        "latestPublishedResearchPdf": "/notes/r0-76a.pdf",
        "latestReleaseGate": "tests/r076a-step52-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r076a-step52-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076a-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076a-step52-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076a-step52-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076a-step52-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076a-step52-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076a-step52",
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
    write_text(PUBLIC / "notes/r0-76a.html", render_note())
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
        "latestCompletedStep": 52,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 191,
        "formalFigure": None,
        "formalFigureExemption": True,
        "simulation": False,
        "pdeData": False,
        "noveltyClaim": False,
        "clayClaim": False,
        "counterexampleClaim": False,
        "fullClusterPaymentClaim": False,
        "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
