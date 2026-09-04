#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75Z Step 51 from the verified R0.75Y Step 50 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075y_step50_release as previous
import import_r075z_step51_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "3259082d0153517a9d6d7d0803b2fba288d0da66"
VERSION = "2.30"
RELEASE = "r075z"
CODE = "R0.75Z"
TITLE = "R0.75Z｜未解簇正规形与载频电流门"
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
            raise RuntimeError(f"R0.75Z frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075z_unresolved_cluster_carrier_current_gate_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or len(certificate.get("assertions", [])) != 15
        or not all(row.get("pass") is True for row in certificate.get("assertions", []))
        or len(certificate.get("negativeMutations", [])) != 72
    ):
        raise RuntimeError("R0.75Z certificate verdict drift")
    main = (ROOT / "research/r075z_unresolved_cluster_carrier_current_gate.md").read_text()
    compact_main = " ".join(main.split())
    for token in (
        r"\tag{Z.1}", r"\tag{Z.3}", r"\tag{Z.6}", r"\tag{Z.7}",
        r"\tag{Z.18}", r"\tag{Z.20}", r"\tag{Z.26}", r"\tag{Z.31}",
        "Cut the ordered frequencies at every adjacent gap at least `8q/ell`",
        "The density block contains only offset differences", "The carrier block contains the self",
        "it has no fixed sign locally",
        "not a counterexample to the desired cluster flux estimate",
        "No full Z-sector flux payment is claimed here", "cross-cluster products",
        "Version-M boundary", "**NOT CLAY.**",
    ):
        if token not in compact_main:
            raise RuntimeError(f"R0.75Z boundary drift: {token}")
    source_report = (ROOT / "research/r075z_report-source.md").read_text()
    compact = " ".join(source_report.split())
    if "No novelty, priority, or completeness claim is made" not in compact:
        raise RuntimeError("R0.75Z bounded source-claim boundary drift")


def render_step51_sections() -> str:
    source = (ROOT / "research/r075z_unresolved_cluster_carrier_current_gate.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 400
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
    if section_index != 408:
        raise RuntimeError(f"Step 51 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;").replace("qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.29"', 'data-site-version="2.30"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.29", "/i18n-en.js?v=2.30", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Exact X/Y/Z partition and unresolved-cluster carrier-current obstruction, without claiming full cluster payment.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75z.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75Z · STEP 51 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75Z · Step 51 · CLUSTER CARRIER-CURRENT GATE</div><h1>{TITLE}</h1><p>Z 给出 fixed-q X/Y/Z 穷尽分区、唯一 maximal cluster 分解、exact complex envelope PDE、density/carrier 两块与局部/全局 current 恒等式。它只否定把 <strong>2N|J|</strong> 点态吸收到 <strong>|Z|^2+|Z_y|^2</strong> 后递归套用 X 的朴素策略；不证明完整簇支付、簇可加性、交叉簇支付或反例。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">EXHAUSTIVE X/Y/Z PARTITION</span><span class="label">MAXIMAL CLUSTERS</span><span class="label">EXACT ENVELOPE PDE</span><span class="label">DENSITY / CARRIER BLOCKS</span><span class="label">LOCAL CURRENT</span><span class="label">GLOBAL SIGN ONLY</span><span class="label">POINTWISE ABSORPTION NO-GO</span><span class="label">NAIVE X RECURSION CLOSED</span><span class="label">FULL CLUSTER PAYMENT OPEN</span><span class="label">CROSS-CLUSTER OPEN</span><span class="label">VERSION-M CONDITIONAL</span><span class="label">NO COUNTEREXAMPLE CLAIM</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75Z STEP 51</strong><p>scope：fixed q, one dyadic band</p><p>X：n_1 ell &lt; 8q</p><p>Y：high carrier + all gaps &gt;= 8q</p><p>Z：high carrier + one gap &lt; 8q</p><p>cluster cut：gap &gt;= 8q/ell</p><p>envelope：complex, carrier dependent</p><p>square：density + carrier</p><p>current：global sign, no local sign</p><p>no-go：carrier-uniform pointwise absorption</p><p>full payment：OPEN</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step51_sections() + '\n<section id="reproduce">', "Step 51 sections")
    evidence = '''<section id="reproduce"><div class="section-no">Z / 冻结证据</div><h2>Step 51 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075z_unresolved_cluster_carrier_current_gate.md">Step 51 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075z_unresolved_cluster_carrier_current_gate_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075z_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075z_unresolved_cluster_carrier_current_gate_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075z_unresolved_cluster_carrier_current_gate_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075z_unresolved_cluster_carrier_current_gate_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075z_unresolved_cluster_carrier_current_gate_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075z_unresolved_cluster_carrier_current_gate_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075z_unresolved_cluster_carrier_current_gate_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075z_unresolved_cluster_carrier_current_gate_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075z_unresolved_cluster_carrier_current_gate_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075z_unresolved_cluster_carrier_current_gate_qa.sh">QA script</a></p><p><a href="/notes/r0-75z.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75w.html">上一大里程碑累计回顾（截止 R0.75W）</a> · <a href="/recap-r0-61-r0-75w.pdf">W recap PDF</a></p><p class="note">Certificate：Python 15/15、Ruby 15/15、Z.1--Z.31、31/31 tags 与 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 72/72 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 continuum identities；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 51 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>X、Y 与 Z 的穷尽分工</h2><p><a href="#s-384">X：fixed-q low carrier</a> · <a href="#s-393">Y：strongly separated high carrier</a> · <a href="#s-401">Z：unresolved cluster normal form and naive-recursion gate</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 51 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">full clustered-sector payment remains OPEN</h2><p style="margin:.15rem 0">本站在 R0.75Z Step 51 停止。Z 只关闭 X/Y/Z 参数分区、簇正规形、density/carrier split、current identities 与 carrier-uniform pointwise absorption 后递归套用 X 的朴素策略。完整簇支付、簇可加性、full-field mass 对单簇控制、cross-cluster payment、arbitrary packets、E.24、complete Version-M extraction、regularity 与 singularity 仍开放；没有反例主张。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 51 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.29"', 'data-site-version="2.30"', "home version"),
        ("/i18n-en.js?v=2.29", "/i18n-en.js?v=2.30", "home i18n"),
        ("/site-refresh.js?v=2.29.1", "/site-refresh.js?v=2.30.1", "home refresh"),
        ("<strong>v2.29</strong>网页版本", "<strong>v2.30</strong>网页版本", "home stat version"),
        ("<strong>R0.75Y</strong>最新研究节点", "<strong>R0.75Z</strong>最新研究节点", "home latest"),
        ("<strong>253</strong>公开研究笔记", "<strong>254</strong>公开研究笔记", "home public count"),
        ("展开 163 篇公开笔记", "展开 164 篇公开笔记", "home route count"),
        ("综述 v2.29 · 2026-09-04", "综述 v2.30 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75Y", "Research topology · R0.1–R0.75Z", "home topology"),
        ('href="#r075y">跳到首页 R0.75Y 卡片 →', 'href="#r075z">跳到首页 R0.75Z 卡片 →', "home jump"),
        ("R0.70A–R0.75Y：155 节已公开，104 节完整封存", "R0.70A–R0.75Z：156 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75Y</span>', '<span class="route-range">R0.69P–R0.75Z</span>', "home range"),
        ("<h3>R0.75Y：强分离多谐波族的完整 signed-flux 付款</h3>", "<h3>R0.75Z：未解簇正规形与载频电流门</h3>", "home route title"),
        ("R0.72R–R0.75Y：</span>", "R0.72R–R0.75Z：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75Y"', 'aria-label="R0.69P–R0.75Z"', "home links label"),
        ("全站现有 253 篇公开研究笔记", "全站现有 254 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75Z Step 51 给出 fixed-q X/Y/Z 穷尽分区与 unresolved-cluster envelope/current 正规形；它只否定 carrier-uniform pointwise absorption 后递归套用 X 的朴素策略。完整簇支付、簇可加性与 cross-cluster payment 仍开放。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75Z · 2026-09-04 · STEP 51 · CLUSTER CARRIER-CURRENT GATE</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">Z 给出 X/Y/Z 穷尽分区、簇 envelope PDE、density/carrier blocks 与 current identities，只排除 pointwise absolute-current absorption 后递归套用 X。完整簇支付、簇可加性、cross-cluster payment 与反例主张均未建立。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75z.pdf">阅读最新 R0.75Z 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾仍截止 R0.75W（191 节）</a><a href="/notes/">254 篇研究笔记总索引</a><a href="#r075z">查看首页 R0.75Z 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75Z · 156 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75Z Step 51 cluster carrier-current gate</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">X pays fixed-q low carriers, Y pays strongly separated high carriers, and Z gives the exact normal form for the remaining clustered sector while closing only the naive pointwise-current recursion.</p>', "home current summary")
    page = replace_once(page, 'exact-pair full-frequency closure → fixed-finite low-carrier family → strongly separated high-carrier family with q^2 cost / unresolved clusters and packets open</p>', 'fixed-finite low-carrier family → strongly separated high-carrier family with q^2 cost → unresolved-cluster envelope and carrier-current gate / full cluster payment and aggregation open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75y.html">R0.75Y</a>', '<a class="milestone" href="/notes/r0-75y.html">R0.75Y</a>\n<a class="milestone" href="/notes/r0-75z.html">R0.75Z</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>full cluster payment and cross-cluster aggregation</h3><p>Z 只关闭参数分区、簇正规形与朴素 pointwise-current recursion。完整簇支付、簇可加性、full-field plateau mass 对单簇控制、cross-cluster payment、arbitrary packets 与 Version-M extraction 仍开放；没有反例主张。后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075z" data-release="r075z" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75Z Step 51 · 2026-09-04 · CLUSTER CARRIER-CURRENT GATE</p><h3>{TITLE}</h3><p>Z 物化 fixed-q X/Y/Z 穷尽分区、maximal cluster 正规形、exact envelope PDE、density/carrier split 与 current identities。结论只否定把 2N|J| 点态吸收后递归套用 X；不证明 full cluster payment、additivity、cross-cluster payment 或反例。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75z.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75z.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap 仍截止 W</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075y"'
    if anchor not in page:
        raise RuntimeError("home R0.75Y card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.29"', 'data-site-version="2.30"', "literature version"),
        ("/i18n-en.js?v=2.29", "/i18n-en.js?v=2.30", "literature i18n"),
        ("文献综述 v2.29 · 2026-09-04", "文献综述 v2.30 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75Y 只列为研究笔记", "本站 R0.69P–R0.75Z 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.75Z</b><strong>unresolved-cluster normal form and carrier-current gate</strong></header><p>Step 51 给出 fixed-q X/Y/Z 穷尽分区、唯一 maximal clusters、exact complex envelope PDE、density/carrier split 与 local/global current identities；它只排除 carrier-uniform pointwise absolute-current absorption 后递归套用 X。完整簇支付与 cross-cluster aggregation 仍开放。<a href="/notes/r0-75z.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">保留的 W milestone recap</a> <a href="#r075z-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>full cluster payment and cross-cluster aggregation</strong></header><p>localized signed current、joint density/carrier cancellation、full-field mass control、cluster additivity、cross-cluster payment、arbitrary packets 与 Version-M extraction 均未闭合；没有反例主张。后续材料未授权、未读取、未公开。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · 后续未授权</b>[\s\S]*?</div>', route, "literature route")
    boundary = (
        '<h3 id="r075z-boundary">R0.75Z Step 51 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Nazarov、Kovrijkine、Egidi--Veselic、Friedland--Yomdin 与 Jaming--Saba 只提供 finite-cluster observation 的经典语境。Z 的参数分区、modulation、density/carrier split、current identity 与 pointwise no-go 都由 displayed finite Fourier algebra 直接推出；这些来源不提供所需的 signed time-weighted collar-flux payment，有限检索也不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.75Z Step 51 公开边界 · EXACT PARTITION · NARROW METHOD NO-GO</strong><p>'
        'PROVED：Z.1--Z.3 fixed-q X/Y/Z 穷尽分区；Z.4 与 Z.11--Z.13 unique maximal clusters 和 strict width；Z.5--Z.7 exact envelope/current equations；Z.18--Z.21 one-cluster density/carrier square split；Z.22--Z.27 local identity 与 full-period favorable current；Z.28--Z.31 排除 carrier-uniform pointwise absorption of 2N|J| into |Z|^2+|Z_y|^2。'
        'NARROW CONSEQUENCE：只关闭先对新 current 取绝对值再递归套用 X 的朴素策略；不是 signed、nonlocal、joint-block 或 final cluster-flux estimate 的反例。'
        'CONDITIONAL：Version-M consequence 仍要求同一 measurement row、weight、realized subclass、actual component 与 ledger alignment。'
        'OPEN：full clustered-sector payment、cluster additivity、full-field plateau mass 对每个 cluster 的控制、cross-cluster products/payment、localized signed current、joint density/carrier cancellation、arbitrary packets、E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。finite checks 不代替 continuum identities；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO FULL CLUSTER PAYMENT. NO COUNTEREXAMPLE CLAIM. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75z.html">阅读完整笔记</a> · '
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
    if html_count != 254 or pdf_count not in (210, 211):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 194:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75z.html",
        "latestPublishedResearchPdf": "/notes/r0-75z.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "latestRecapRelease": "R0.75W",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075y":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 156
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 51
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "UNRESOLVED_CLUSTER_CARRIER_CURRENT_GATE",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_ROUTE_REDUCTION_AND_METHOD_OBSTRUCTION",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "fixed_q_xyz_partition": "PROVED_Z1_Z3_EXHAUSTIVE_WITH_Y_EQUALITY",
            "maximal_cluster_decomposition": "PROVED_UNIQUE_WITH_STRICT_INTERNAL_GAPS",
            "carrier_envelope_equation": "PROVED_Z5_Z6_COMPLEX_N_DEPENDENT_DRIFT",
            "density_carrier_square_split": "PROVED_Z18_Z21_ONE_CLUSTER_ONLY",
            "local_and_global_current_identities": "PROVED_Z22_Z27_GLOBAL_SIGN_NOT_LOCAL_SIGN",
            "pointwise_absorption": "DISPROVED_CARRIER_UNIFORM_2N_ABS_J_BY_UNWEIGHTED_Q_PLUS_ZY2",
            "naive_recursive_x_strategy": "CLOSED_ONLY_AFTER_POINTWISE_ABSOLUTE_CURRENT",
            "full_clustered_sector_payment": "OPEN_NOT_PROVED_OR_DISPROVED",
            "cluster_additivity": "OPEN_NOT_PROVED",
            "full_field_mass_controls_each_cluster": "OPEN_NOT_PROVED",
            "cross_cluster_products_and_payment": "OPEN_NOT_PROVED",
            "counterexample_to_final_cluster_flux": "NOT_CLAIMED",
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
            "negative_mutations": "PASS_PYTHON_72_OF_72_RUBY_72_OF_72",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_Z1_TO_Z31_TAGS_AND_DISPLAYS_31_OF_31",
            "exact_fixtures": "PASS_Q2_X_STRICT_Y_EQUALITY_Z_CLUSTER_AND_POINTWISE_CURRENT",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75z.html",
            "target_pdf": "/notes/r0-75z.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "retained_recap_terminal_release": "R0.75W_STEP48",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075z_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 51,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "postR070APublishedReleaseCount": 156,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r076a",
        "latestPublishedResearchHtml": "/notes/r0-75z.html",
        "latestPublishedResearchPdf": "/notes/r0-75z.pdf",
        "latestReleaseGate": "tests/r075z-step51-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075z-step51-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075z-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075z-step51-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075z-step51-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075z-step51-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075z-step51-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075z-step51",
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
    write_text(PUBLIC / "notes/r0-75z.html", render_note())
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
        "latestCompletedStep": 51,
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
