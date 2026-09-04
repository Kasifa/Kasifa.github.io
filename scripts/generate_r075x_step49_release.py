#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75X Step 49 from the verified R0.75W Step 48 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075w_step48_release as previous
import import_r075x_step49_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "4e5dd6edefc59c55e7be9df5c84be494fc29f5a9"
VERSION = "2.28"
RELEASE = "r075x"
CODE = "R0.75X"
TITLE = "R0.75X｜固定有限谐波族的低载频 signed-flux 付款"
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
            raise RuntimeError(f"R0.75X frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075x_fixed_finite_mode_low_carrier_payment_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertionCount") != 18
        or len(certificate.get("assertions", [])) != 18
    ):
        raise RuntimeError("R0.75X certificate verdict drift")
    main = (ROOT / "research/r075x_fixed_finite_mode_low_carrier_payment.md").read_text()
    for token in (
        r"\tag{X.1}", r"\tag{X.5}", r"\tag{X.7}", r"\tag{X.15}",
        r"\tag{X.22}", r"\tag{X.29}", r"\tag{X.33}", r"\tag{X.36}",
        "Fix an integer `q>=1`", "No uniform control of `C_q` as `q` grows is proved",
        "high-carrier sector for three or more modes", "never divides by `v`",
        "**NOT CLAY.**",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75X boundary drift: {token}")
    source_report = (ROOT / "research/r075x_report-source.md").read_text()
    if "no completeness, novelty, or priority claim" not in source_report:
        raise RuntimeError("R0.75X bounded source-claim boundary drift")


def render_step49_sections() -> str:
    source = (ROOT / "research/r075x_fixed_finite_mode_low_carrier_payment.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 383
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
    if section_index != 392:
        raise RuntimeError(f"Step 49 reader section drift: {section_index}")
    return "\n".join(output).replace(r"\qquad", r"\;\;").replace("qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.27"', 'data-site-version="2.28"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.27", "/i18n-en.js?v=2.28", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Low-carrier signed collar-flux payment for every fixed finite real harmonic family in one dyadic band, with explicit nonuniform-in-q and high-carrier boundaries.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75x.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75X · STEP 49 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75X · Step 49 · FIXED FINITE LOW CARRIER</div><h1>{TITLE}</h1><p>X 把 W 的低载频 local-energy mechanism 推广到每个固定有限 real harmonic family：对固定 <strong>q</strong>、一个 dyadic band 与 <strong>n_1aR&lt;C_0</strong>，得到常数为 C_q 的 complete low-carrier signed collar-flux payment。常数不依赖频率、频差、振幅、相位、R 或 B，但没有 q 增长的一致控制；三模以上的 high-carrier sector 仍开放。精确对数率仍为 <strong>-2/11907</strong>。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">FIXED FINITE q</span><span class="label">LOW CARRIER ONLY</span><span class="label">ONE DYADIC BAND</span><span class="label">2q-STATE CONFLUENT ODE</span><span class="label">2q-TERM TRACE</span><span class="label">NO GAP DIVISOR</span><span class="label">NO V DIVISION</span><span class="label">R POWERS CANCEL</span><span class="label">EXACT RATE -2/11907</span><span class="label">NO UNIFORM q GROWTH</span><span class="label">HIGH CARRIER 3+ OPEN</span><span class="label">VERSION-M CONDITIONAL</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75X STEP 49</strong><p>scope：fixed finite q</p><p>band：n_1&lt;...&lt;n_q&lt;=2n_1</p><p>sector：n_1aR &lt; C_0</p><p>clock：T_R = 4R^2</p><p>constant：C_q</p><p>uniform in q：NO</p><p>payment：a^(2/3)R^(-1/3)M^(2/3)</p><p>normalized R-power：0</p><p>rate：-2/11907</p><p>open：high carrier 3+ / packets</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step49_sections() + '\n<section id="reproduce">', "Step 49 sections")
    evidence = '''<section id="reproduce"><div class="section-no">X / 冻结证据</div><h2>Step 49 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075x_fixed_finite_mode_low_carrier_payment.md">Step 49 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075x_fixed_finite_mode_low_carrier_payment_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075x_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075x_fixed_finite_mode_low_carrier_payment_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075x_fixed_finite_mode_low_carrier_payment_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075x_fixed_finite_mode_low_carrier_payment_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075x_fixed_finite_mode_low_carrier_payment_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075x_fixed_finite_mode_low_carrier_payment_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075x_fixed_finite_mode_low_carrier_payment_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075x_fixed_finite_mode_low_carrier_payment_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075x_fixed_finite_mode_low_carrier_payment_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075x_fixed_finite_mode_low_carrier_payment_qa.sh">QA script</a></p><p><a href="/notes/r0-75x.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75w.html">上一大里程碑累计回顾（截止 R0.75W）</a> · <a href="/recap-r0-61-r0-75w.pdf">W recap PDF</a></p><p class="note">Certificate：Python 18/18、Ruby 19/19、X.1--X.36、36/36 tags 与 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 90/90 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 fixed-q continuum ODE compactness 或 Turan–Nazarov lemma；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 49 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>W 与 X 的精确分工</h2><p><a href="#s-374">W：full-frequency exact two-harmonic pair</a> · <a href="#s-384">X：fixed-finite low-carrier family</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 49 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">quantitative q-growth, high-carrier three-plus modes, and arbitrary packets remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.75X Step 49 停止。X 只支付每个固定有限 q 的单 dyadic band 低载频 family；q 随 L 增长的定量常数、三模以上 high-carrier sector、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 49 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.27"', 'data-site-version="2.28"', "home version"),
        ("/i18n-en.js?v=2.27", "/i18n-en.js?v=2.28", "home i18n"),
        ("/site-refresh.js?v=2.27.1", "/site-refresh.js?v=2.28.1", "home refresh"),
        ("<strong>v2.27</strong>网页版本", "<strong>v2.28</strong>网页版本", "home stat version"),
        ("<strong>R0.75W</strong>最新研究节点", "<strong>R0.75X</strong>最新研究节点", "home latest"),
        ("<strong>251</strong>公开研究笔记", "<strong>252</strong>公开研究笔记", "home public count"),
        ("展开 161 篇公开笔记", "展开 162 篇公开笔记", "home route count"),
        ("综述 v2.27 · 2026-09-04", "综述 v2.28 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75W", "Research topology · R0.1–R0.75X", "home topology"),
        ('href="#r075w">跳到首页 R0.75W 卡片 →', 'href="#r075x">跳到首页 R0.75X 卡片 →', "home jump"),
        ("R0.70A–R0.75W：153 节已公开，104 节完整封存", "R0.70A–R0.75X：154 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75W</span>', '<span class="route-range">R0.69P–R0.75X</span>', "home range"),
        ("<h3>R0.75W：单个 dyadic 二谐波 pair 的全载频 signed-flux 付款</h3>", "<h3>R0.75X：固定有限谐波族的低载频 signed-flux 付款</h3>", "home route title"),
        ("R0.72R–R0.75W：</span>", "R0.72R–R0.75X：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75W"', 'aria-label="R0.69P–R0.75X"', "home links label"),
        ("全站现有 251 篇公开研究笔记", "全站现有 252 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75X Step 49 把 W 的低载频 local-energy route 推广到每个固定有限 q 的单 dyadic band real harmonic family。C_q 可依赖固定 q，但不依赖频率、频差、振幅、相位、R 或 B；q-growth、三模以上 high-carrier sector、arbitrary packets 与 Version-M 一般化仍开放。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75X · 2026-09-04 · STEP 49 · FIXED FINITE LOW CARRIER</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">X 用 2q-state confluent observation、at-most-2q-term Turan–Nazarov terminal trace 与 W 的 exact local-energy identity，支付每个固定有限 q 的低载频 signed flux。常数 C_q 没有统一 q-growth 控制，三模以上高载频与任意 packets 仍开放。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75x.pdf">阅读最新 R0.75X 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾仍截止 R0.75W（191 节）</a><a href="/notes/">252 篇研究笔记总索引</a><a href="#r075x">查看首页 R0.75X 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75X · 154 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75X Step 49 fixed-finite low-carrier payment</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">W closes all carriers for one exact two-harmonic pair. X extends only the low-carrier route to every fixed finite real harmonic family in one dyadic band; the constant is not uniform as q grows, and the high-carrier three-plus-mode problem remains open.</p>', "home current summary")
    page = replace_once(page, 'high-carrier spatial coercivity → difference row → coupled self/sum block → high-carrier exact-pair flux → independent low-carrier local-energy payment → full-frequency exact-pair flux / 3+ modes and packets open</p>', 'high-carrier spatial coercivity → difference row → coupled self/sum block → full-frequency exact pair → fixed-finite low-carrier family / q-growth, high-carrier 3+ modes, and packets open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75w.html">R0.75W</a>', '<a class="milestone" href="/notes/r0-75w.html">R0.75W</a>\n<a class="milestone" href="/notes/r0-75x.html">R0.75X</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>quantitative q-growth, high-carrier three-plus modes, and arbitrary packets</h3><p>X 只关闭每个固定有限 q 的低载频单带 family。q=q(L) 的定量控制、三模以上 high-carrier sector、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、E.24 与 Version-M extraction 仍开放。后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075x" data-release="r075x" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75X Step 49 · 2026-09-04 · FIXED FINITE LOW CARRIER</p><h3>{TITLE}</h3><p>X 对每个固定有限 q，在一个 dyadic band 与 n_1aR&lt;C_0 下证明 complete low-carrier signed-flux payment；2q-state confluent observation 与 2q-term trace 都无 gap divisor。没有 q-growth 一致界，三模以上高载频和任意 packets 仍开放。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75x.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75x.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">最新 milestone recap 仍截止 W</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075w"'
    if anchor not in page:
        raise RuntimeError("home R0.75W card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.27"', 'data-site-version="2.28"', "literature version"),
        ("/i18n-en.js?v=2.27", "/i18n-en.js?v=2.28", "literature i18n"),
        ("文献综述 v2.27 · 2026-09-04", "文献综述 v2.28 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75W 只列为研究笔记", "本站 R0.69P–R0.75X 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>three or more modes, arbitrary packets, and Version-M transfer</strong></header><p>exact pair 之外，三个及以上 harmonics、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、E.24 与 Version-M extraction 均未闭合。后续材料未授权、未读取、未公开。</p></div>'
    route = f'<div class="route-step kept"><header><b>R0.75X</b><strong>fixed-finite-mode low-carrier payment</strong></header><p>Step 49 用 2q-state confluent spatial observation、at-most-2q-term frequency-gap-free Turan–Nazarov terminal trace 与 W 的 exact local-energy identity，对每个固定有限 q 支付 n_1aR&lt;C_0 的 single-dyadic-band family。C_q 没有 uniform q-growth 控制，三模以上 high-carrier sector 仍开放。<a href="/notes/r0-75x.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">保留的 W milestone recap</a> <a href="#r075x-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>quantitative q-growth, high-carrier three-plus modes, and arbitrary packets</strong></header><p>q=q(L) 的定量 spatial constant、三模以上 high-carrier sector、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、E.24 与 Version-M extraction 均未闭合。后续材料未授权、未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075x-boundary">R0.75X Step 49 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Nazarov 1993/1994 的原始记录与 Friedland--Yomdin 2013 的 primary restatement 提供 exponential-polynomial measurable-set inequality；其常数不依赖 imaginary frequencies 或 frequency gaps，但保留 term-count dependence。X 的 2q-state confluent spatial observation、scaled kernel 与 local-energy identity 均在本地直接证明。有限检索不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.75X Step 49 公开边界 · FIXED FINITE q · LOW CARRIER ONLY</strong><p>'
        'PROVED：X.10--X.14 low-carrier scaling；X.15--X.20 fixed-q 2q-state confluent observation；X.21--X.25 at-most-2q-term frequency-gap-free terminal trace；X.26--X.33 radial primitive 与 exact local-energy identity；X.34--X.35 physical payment；X.5--X.7 normalized estimate、R-power cancellation 与 -2/11907 rate；X.36 exact smooth unforced shear。CONDITIONAL：Version-M consequence 仍要求 measurement row、weight、realized subclass、actual component 与 ledger alignment。'
        'OPEN：uniform quantitative q-growth；q=q(L)；三模以上 high-carrier sector；arbitrary packets；inter-packet aggregation；nonconstant or vertically dependent shear；projection；arbitrary-field E.24；complete Version-M extraction；fixed deletion；suitable-weak transfer；regularity 与 singularity。finite checks 不代替 continuum lemmas；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>FIXED FINITE q. LOW CARRIER ONLY. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75x.html">阅读完整笔记</a> · '
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
    if html_count != 252 or pdf_count not in (208, 209):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 192:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75x.html",
        "latestPublishedResearchPdf": "/notes/r0-75x.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "latestRecapRelease": "R0.75W",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075w":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 154
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 49
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "FIXED_FINITE_MODE_LOW_CARRIER_SIGNED_FLUX_PAYMENT",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_FIXED_FINITE_MODE_LOW_CARRIER_THEOREM",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "harmonic_scope": "EVERY_FIXED_FINITE_REAL_FAMILY_ONE_DYADIC_BAND",
            "low_carrier_sector": "PROVED_X5_N1_A_R_LT_C0",
            "fixed_q_constant": "FINITE_CQ_INDEPENDENT_OF_R_FREQUENCIES_GAPS_AMPLITUDES_PHASES_B",
            "uniform_q_growth": "OPEN_NOT_PROVED",
            "q_depending_on_L": "OPEN_NOT_PROVED",
            "confluent_spatial_observation": "PROVED_X15_X20_DIMENSION_2Q",
            "frequency_gap_free_terminal_trace": "PROVED_X21_X25_AT_MOST_2Q_TERMS",
            "local_energy_identity": "PROVED_X26_X33_NO_DIVISION_BY_V_AMPLITUDE_FREQUENCY_OR_GAP",
            "normalized_estimate": "PROVED_X6_X7_R_POWERS_CANCEL",
            "exact_l2_rate": "MINUS_2_OVER_11907",
            "exact_smooth_unforced_shear_solution": "PROVED_X36",
            "version_m_same_velocity_inclusion": "CONDITIONAL_MEASUREMENT_WEIGHT_REALIZED_SUBCLASS_ACTUAL_COMPONENT_LEDGER_ALIGNMENT",
            "high_carrier_three_or_more_modes": "OPEN_NOT_PROVED",
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
            "python_certificate": "PASS_18_OF_18",
            "independent_ruby": "PASS_19_OF_19",
            "negative_mutations": "PASS_PYTHON_90_OF_90_RUBY_90_OF_90",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_X1_TO_X36_TAGS_AND_DISPLAYS_36_OF_36",
            "exact_fixtures": "PASS_Q3_COMPANION_TRANSPORT_SCALE",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75x.html",
            "target_pdf": "/notes/r0-75x.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "retained_recap_terminal_release": "R0.75W_STEP48",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075x_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 49,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 191,
        "postR070APublishedReleaseCount": 154,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075y",
        "latestPublishedResearchHtml": "/notes/r0-75x.html",
        "latestPublishedResearchPdf": "/notes/r0-75x.pdf",
        "latestReleaseGate": "tests/r075x-step49-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075x-step49-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075x-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075x-step49-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075x-step49-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075x-step49-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075x-step49-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075x-step49",
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
    write_text(PUBLIC / "notes/r0-75x.html", render_note())
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
        "latestCompletedStep": 49,
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
