#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.76H Step 59 from the verified R0.76G Step 58 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r076g_step58_release as previous
import import_r076h_step59_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "f3b0ec54b99032134adfc6d76ba774e0c5c01a88"
VERSION = "2.38"
RELEASE = "r076h"
CODE = "R0.76H"
TITLE = "R0.76H｜完整平台吸收平移二项式障碍"
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
            raise RuntimeError(f"R0.76H frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r076h_full_plateau_absorption_for_shifted_packet_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertionsPassed") != 126
        or certificate.get("assertionsTotal") != 126
        or not all(
            value is True
            for group in certificate.get("checks", {}).values()
            for value in group.values()
        )
        or len(certificate.get("negativeMutations", [])) != 126
    ):
        raise RuntimeError("R0.76H certificate verdict drift")
    main = (ROOT / "research/r076h_full_plateau_absorption_for_shifted_packet.md").read_text()
    compact_main = " ".join(main.split())
    for token in (
        r"\tag{H.1}", r"\tag{H.10}", r"\tag{H.20}", r"\tag{H.30}", r"\tag{H.39}",
        r"M_L^{\rm plat}", r"\exp\!\left(C_*\frac ma\right)",
        r"=\frac3{40000}", r"=-\frac2{11907}<0",
        "candidate-killing result", "not a full-plateau counterexample", "**NOT CLAY.**",
    ):
        if token not in compact_main:
            raise RuntimeError(f"R0.76H boundary drift: {token}")
    source_report = (ROOT / "research/r076h_report-source.md").read_text()
    compact = " ".join(source_report.split())
    if "imports no external observability, Remez, or control theorem" not in compact:
        raise RuntimeError("R0.76H source boundary drift")


def render_step59_sections() -> str:
    source = (ROOT / "research/r076h_full_plateau_absorption_for_shifted_packet.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 464
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
    if section_index != 471:
        raise RuntimeError(f"Step 59 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.37"', 'data-site-version="2.38"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.37", "/i18n-en.js?v=2.38", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="The full physical plateau absorbs the explicit R0.76G shifted-binomial candidate at subquadratic logarithmic cost, restoring the exact normalized rate -2/11907.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-76h.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.76H · STEP 59 · 2026-09-05</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.76H · Step 59 · FULL-PLATEAU ABSORPTION FOR THE SHIFTED PACKET</div><h1>{TITLE}</h1><p>H 对 G 的同一个显式 shifted-binomial exact shear 完成物理分母检查：正 cap 相邻仅 <code>O(1/a)</code> 的完整三维 plateau fibres 以 <code>exp(O(m/a))</code> 成本吸收指数对比。raw full-plateau quotient 的精确速率是 <code>3/40000</code>，规范化后精确回到 <code>-2/11907</code>。这严格否定该候选，却不推广到任意 packet、E.24 或 Version-M。<strong>NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">CANDIDATE KILLED</span><span class="label">FULL PLATEAU ABSORPTION</span><span class="label">EXPLICIT PACKET ONLY</span><span class="label">COMPLETE CLOCK</span><span class="label">SIGNED FLUX POSITIVE</span><span class="label">RAW RATE 3/40000</span><span class="label">NORMALIZED RATE -2/11907</span><span class="label">EXACT REAL SMOOTH SHEAR</span><span class="label">NO ARBITRARY-PACKET THEOREM</span><span class="label">NO VERSION-M CLAIM</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.76H STEP 59</strong><p>packet：exactly R0.76G</p><p>m：floor(a²/1024)</p><p>q：2m+1</p><p>B：-βa/R ≠ 0</p><p>clock：0 ≤ s ≤ 4</p><p>plateau strip：width δ₀/a</p><p>absorption cost：exp(O(m/a))</p><p>signed flux：positive for large L</p><p>raw rate：3/40000</p><p>normalized rate：-2/11907</p><p>candidate：KILLED</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step59_sections() + '\n<section id="reproduce">', "Step 59 sections")
    evidence = '''<section id="reproduce"><div class="section-no">H / 冻结证据</div><h2>Step 59 主文、source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076h_full_plateau_absorption_for_shifted_packet.md">Step 59 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076h_full_plateau_absorption_for_shifted_packet_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076h_report-source.md">source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076h_full_plateau_absorption_for_shifted_packet_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076h_full_plateau_absorption_for_shifted_packet_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076h_full_plateau_absorption_for_shifted_packet_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076h_full_plateau_absorption_for_shifted_packet_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076h_full_plateau_absorption_for_shifted_packet_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r076h_full_plateau_absorption_for_shifted_packet_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076h_full_plateau_absorption_for_shifted_packet_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076h_full_plateau_absorption_for_shifted_packet_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r076h_full_plateau_absorption_for_shifted_packet_qa.sh">QA script</a></p><p><a href="/notes/r0-76h.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75w.html">上一大里程碑累计回顾（截止 R0.75W）</a> · <a href="/recap-r0-61-r0-75w.pdf">W recap PDF</a></p><p class="note">Certificate：Python 126/126、Ruby 126/126、H.1--H.39、39/39 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 126/126 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 uniform Gaussian-moment comparison 的 continuum proof；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 59 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>G 的中心纤维障碍与 H 的完整平台吸收</h2><p><a href="#s-456">G：central-fibre signed-flux lower bound</a> · <a href="#s-465">H：full-plateau absorption and exact normalized rate</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 59 adjacent")
    next_section = '''<section id="next"><div class="section-no">STOP / NO LATER RELEASE AUTHORIZED</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">Later material remains unauthorized, unread, and unpublished</h2><p style="margin:.15rem 0">本站当前发布至 R0.76H Step 59。H 只否定 G 的同一个显式 shifted-binomial 候选：完整 physical plateau 吸收其指数对比，规范化精确速率为 -2/11907。任意 packets、不同的 cap-localized families、nonconstant shears、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 59 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.37"', 'data-site-version="2.38"', "home version"),
        ("/i18n-en.js?v=2.37", "/i18n-en.js?v=2.38", "home i18n"),
        ("/site-refresh.js?v=2.37.1", "/site-refresh.js?v=2.38.1", "home refresh"),
        ("<strong>v2.37</strong>网页版本", "<strong>v2.38</strong>网页版本", "home stat version"),
        ("<strong>R0.76G</strong>最新研究节点", "<strong>R0.76H</strong>最新研究节点", "home latest"),
        ("<strong>261</strong>公开研究笔记", "<strong>262</strong>公开研究笔记", "home public count"),
        ("展开 171 篇公开笔记", "展开 172 篇公开笔记", "home route count"),
        ("综述 v2.37 · 2026-09-05", "综述 v2.38 · 2026-09-05", "home footer"),
        ("Research topology · R0.1–R0.76G", "Research topology · R0.1–R0.76H", "home topology"),
        ('href="#r076g">跳到首页 R0.76G 卡片 →', 'href="#r076h">跳到首页 R0.76H 卡片 →', "home jump"),
        ("R0.70A–R0.76G：163 节已公开，104 节完整封存", "R0.70A–R0.76H：164 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.76G</span>', '<span class="route-range">R0.69P–R0.76H</span>', "home range"),
        ("<h3>R0.76G：完整时钟中心纤维通量的指数下界</h3>", "<h3>R0.76H：完整平台吸收显式 shifted-binomial 候选</h3>", "home route title"),
        ("R0.72R–R0.76G：</span>", "R0.72R–R0.76H：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.76G"', 'aria-label="R0.69P–R0.76H"', "home links label"),
        ("全站现有 261 篇公开研究笔记", "全站现有 262 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.76H Step 59 证明完整三维 plateau 以 exp(O(m/a)) 成本吸收 G 的同一个显式 shifted-binomial packet，raw quotient 速率为 3/40000，规范化精确速率为 -2/11907；结论只杀死这一候选，不推广到任意 packet 或 Version-M。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.76H · 2026-09-05 · STEP 59 · FULL-PLATEAU ABSORPTION FOR THE SHIFTED PACKET</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">H proves that fibres only O(1/a) from G's favourable cap absorb the same explicit packet at exp(O(m/a)) cost. The raw full-plateau quotient has rate 3/40000, while the normalized quotient returns exactly to -2/11907. CANDIDATE KILLED. EXPLICIT PACKET ONLY. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-76h.pdf">阅读最新 R0.76H 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾仍截止 R0.75W（191 节）</a><a href="/notes/">262 篇研究笔记总索引</a><a href="#r076h">查看首页 R0.76H 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.76H · 164 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.76H Step 59 full-plateau absorption for the shifted packet</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">H kills G\'s explicit shifted-binomial full-plateau candidate: adjacent physical plateau fibres absorb the cap at subquadratic logarithmic cost, restoring the exact normalized rate -2/11907.</p>', "home current summary")
    page = replace_once(page, 'nonzero-drift complete-clock signed-flux exp(cq) lower bound against a central-fibre proxy; full plateau, arbitrary packets, arbitrary fields, and Version-M extraction open</p>', 'nonzero-drift central-fibre lower bound → full-plateau absorption of the same explicit shifted packet and exact normalized rate -2/11907; arbitrary packets, arbitrary fields, and Version-M extraction open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-76g.html">R0.76G</a>', '<a class="milestone" href="/notes/r0-76g.html">R0.76G</a>\n<a class="milestone" href="/notes/r0-76h.html">R0.76H</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED · STOP · NO LATER RELEASE AUTHORIZED</span><span class="tree-state current">BOUNDARY</span></div><h3>Later material remains unauthorized, unread, and unpublished</h3><p>H 只关闭 G 的同一个显式 shifted-binomial candidate。任意 packets、different cap-localized families、nonconstant shears、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r076h" data-release="r076h" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.76H Step 59 · 2026-09-05 · FULL-PLATEAU ABSORPTION FOR THE SHIFTED PACKET</p><h3>{TITLE}</h3><p>H 对 G 的同一个显式 shifted-binomial exact shear 证明：完整 plateau 中相邻 fibres 以 exp(O(m/a)) 成本吸收 cap 对比，完整 signed flux 对 full-plateau mass 的 raw rate 为 3/40000，规范化后精确为 -2/11907。只否定这一候选；不推广到任意 packet、E.24、Version-M、regularity 或 singularity。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-76h.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-76h.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">上一大里程碑 recap 仍截止 W</a></p></div>\n'''
    anchor = '<div class="task-one" id="r076g"'
    if anchor not in page:
        raise RuntimeError("home R0.76G card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.37"', 'data-site-version="2.38"', "literature version"),
        ("/i18n-en.js?v=2.37", "/i18n-en.js?v=2.38", "literature i18n"),
        ("文献综述 v2.37 · 2026-09-05", "文献综述 v2.38 · 2026-09-05", "literature footer"),
        ("本站 R0.69P–R0.76G 只列为研究笔记", "本站 R0.69P–R0.76H 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = f'''<div class="route-step kept"><header><b>R0.76H</b><strong>full-plateau absorption for the explicit shifted packet</strong></header><p>Step 59 对 G 的同一个 shifted-binomial exact shear 证明 adjacent plateau strip payment：cap 与完整三维 plateau fibres 相距仅 <code>O(1/a)</code>，Gaussian moment comparison 的成本为 <code>exp(O(m/a))</code>。complete signed flux 最终为正；raw quotient 的精确速率为 <code>3/40000</code>，normalized full-plateau quotient 精确为 <code>-2/11907</code>。结论只杀死这一显式候选。<a href="/notes/r0-76h.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">保留的 W milestone recap</a> <a href="#r076h-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><span hidden>开放接口 · 后续版本</span><strong>not authorized, unread, and unpublished</strong></header><p>任意 packets、different cap-localized families、nonconstant shears、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续版本未授权、未读取、未公开。</p></div>'''
    page = replace_pattern(page, r'<div class="route-step pause"><header><b>开放接口 · R0\.76H</b>[\s\S]*?</div>', route, "literature route")
    boundary = (
        '<h3 id="r076h-boundary">R0.76H Step 59 的 bounded source boundary 与 candidate-killing 边界</h3>'
        '<p>H 不导入新的 observability、Remez 或 control theorem。<a href="https://arxiv.org/abs/1711.04279">Wang--Wang--Zhang--Zhang 2017</a>、<a href="https://arxiv.org/abs/1711.06088">Egidi--Veselic 2018</a>、<a href="https://arxiv.org/abs/math/0307158">Miller 2004</a>、<a href="https://arxiv.org/abs/1806.00969">Laurent--Leautaud 2021</a>、<a href="https://www.mathnet.ru/eng/aa397">Nazarov</a> 与 <a href="https://arxiv.org/abs/1809.09726">Tikhonov--Yuditskii</a> 仅保留为 G 已冻结的背景。H 的新推论完全来自 exact shell cross-section、Gaussian moment expansion、Hölder、Jensen 与同一显式 packet。bounded search 不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.76H Step 59 公开边界 · FULL-PLATEAU ABSORPTION FOR THE SHIFTED PACKET</strong><p>'
        'PROVED：对 G 的同一个 shifted-binomial exact smooth unforced shear，完整 physical plateau 的 adjacent strip 以 exp(O(m/a)) 成本支付 favourable cap；complete signed flux 对大 L 严格为正。raw quotient T_L/(M_L^plat)^(2/3) 的精确 L² 对数速率为 3/40000，normalized quotient X_L/(p_L^plat)^(2/3) 的精确速率为 -2/11907。'
        'CANDIDATE BOUNDARY：这确认 G 的 central-fibre theorem，同时严格证明同一 packet 不是 full-plateau counterexample。'
        'SOURCE BOUNDARY：H 不导入外部 theorem；既有 heat-observability 与 exponential-polynomial 文献只是语境；不作 novelty、priority 或 exhaustive-search claim。'
        'OPEN：R0.76E 的 uniform exp(Cq) loss 是否可改进、arbitrary real dyadic packets、different cap-localized families、nonconstant shears、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity。finite checks 不代替 uniform Gaussian-moment comparison；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>CANDIDATE KILLED. EXPLICIT PACKET ONLY. EXACT NORMALIZED RATE -2/11907. NO ARBITRARY-PACKET THEOREM. NO VERSION-M CLAIM. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-76h.html">阅读完整笔记</a> · '
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
    if html_count != 262 or pdf_count not in (218, 219):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 202:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-76h.html",
        "latestPublishedResearchPdf": "/notes/r0-76h.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "latestRecapRelease": "R0.75W",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-05",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r076g":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 164
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 59
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "FULL_PLATEAU_ABSORPTION_FOR_EXPLICIT_SHIFTED_BINOMIAL_PACKET",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_CANDIDATE_KILLING_RESULT",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "packet_scope": "EXACT_R076G_SHIFTED_BINOMIAL_PACKET_ONLY",
            "full_plateau_absorption": "PROVED_AT_EXP_O_M_OVER_A_COST",
            "complete_signed_flux": "STRICTLY_POSITIVE_FOR_ALL_LARGE_L",
            "raw_rate": "EXACT_THREE_OVER_40000",
            "normalized_rate": "EXACT_MINUS_TWO_OVER_11907",
            "central_fibre_theorem": "R076G_RETAINED",
            "full_plateau_counterexample": "R076G_CANDIDATE_REFUTED",
            "external_inputs": "NO_EXTERNAL_THEOREM_IMPORTED_CONTEXT_ONLY",
            "local_deductions": "EXACT_SHELL_GEOMETRY_GAUSSIAN_MOMENTS_HOLDER_JENSEN",
            "uniform_exp_cq_improvement": "OPEN_NOT_PROVED",
            "arbitrary_packets": "OPEN_NOT_PROVED",
            "different_cap_localized_families": "OPEN_NOT_PROVED",
            "nonconstant_or_vertical_shear": "OPEN_NOT_PROVED",
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
            "python_certificate": "PASS_126_OF_126",
            "independent_ruby": "PASS_126_OF_126",
            "negative_mutations": "PASS_PYTHON_126_OF_126_RUBY_126_OF_126",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_H1_TO_H39_TAGS_AND_39_OF_39_DISPLAYS",
            "continuum_boundary": "FINITE_CERTIFICATE_IS_NOT_PROOF_OF_UNIFORM_GAUSSIAN_MOMENT_COMPARISON",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-76h.html",
            "target_pdf": "/notes/r0-76h.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "retained_recap_terminal_release": "R0.75W_STEP48",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r076h_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 59,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "postR070APublishedReleaseCount": 164,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r076i",
        "latestPublishedResearchHtml": "/notes/r0-76h.html",
        "latestPublishedResearchPdf": "/notes/r0-76h.pdf",
        "latestReleaseGate": "tests/r076h-step59-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r076h-step59-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r076h-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r076h-step59-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r076h-step59-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r076h-step59-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r076h-step59-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r076h-step59",
            "handoffCommit": frozen_import.HANDOFF_COMMIT,
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
    write_text(PUBLIC / "notes/r0-76h.html", render_note())
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
        "latestCompletedStep": 59,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 191,
        "formalFigure": None,
        "formalFigureExemption": True,
        "simulation": False,
        "pdeData": False,
        "noveltyClaim": False,
        "clayClaim": False,
        "candidateKilled": "R076G_EXPLICIT_SHIFTED_BINOMIAL_FULL_PLATEAU_CANDIDATE",
        "fullPlateauAbsorption": "EXP_O_M_OVER_A",
        "rawRate": "THREE_OVER_40000",
        "normalizedRate": "MINUS_TWO_OVER_11907",
        "arbitraryPacketClaim": False,
        "unconditionalVersionMClaim": False,
        "laterReleaseAuthorized": False,
        "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
