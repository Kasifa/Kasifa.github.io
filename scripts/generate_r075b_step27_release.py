#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75B Step 27 from the verified R0.75A Step 26 baseline."""

from __future__ import annotations

import hashlib
import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075a_step26_release as previous
import import_r075b_step27_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.06"
RELEASE = "r075b"
CODE = "R0.75B"
TITLE = "R0.75B｜完整时钟外层填充门：safe subclock 已付，outer dissipation 待解"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-75a.html": "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0",
    PUBLIC / "recap-r0-61-r0-75a.pdf": "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62",
}


def sha256(target: Path) -> str:
    return hashlib.sha256(target.read_bytes()).hexdigest()


def write_text(target: Path, value: str) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(value, encoding="utf-8")


def write_json(target: Path, value: object) -> None:
    write_text(target, json.dumps(value, ensure_ascii=False, indent=2) + "\n")


def replace_once(value: str, old: str, new: str, label: str) -> str:
    if new in value:
        return value
    count = value.count(old)
    if count != 1:
        raise RuntimeError(f"{label}: expected one occurrence, found {count}")
    return value.replace(old, new, 1)


def replace_pattern(value: str, pattern: str, replacement: str, label: str) -> str:
    value, count = re.subn(pattern, lambda _: replacement, value, count=1, flags=re.S)
    if count != 1:
        raise RuntimeError(f"{label}: expected one pattern occurrence, found {count}")
    return value


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected R0.75A recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.75B frozen source drift: {relative}")
    certificate = json.loads((ROOT / "research/r075b_bulk_clock_outer_padding_gate_certificate.json").read_text())
    if certificate.get("verdict") != "PASS" or certificate.get("assertions") != 8 or certificate.get("tags") != 47:
        raise RuntimeError("R0.75B certificate verdict drift")
    main = (ROOT / "research/r075b_bulk_clock_outer_padding_gate.md").read_text()
    for token in (
        r"\textbf{SAFE COMPLETE SUBCLOCK: PAID;}",
        r"\textbf{OUTER-COLLAR ENDPOINT: PAID;}",
        r"\textbf{OUTER-COLLAR ACCUMULATED DISSIPATION: OPEN;}",
        r"\frac{27163}{476280000}>0",
        r"\frac{4279}{79380000}",
        "failure of this estimate**, not a counterexample",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75B boundary drift: {token}")


def inline_markup(value: str) -> str:
    return previous.inline_markup(value)


def render_step27_sections() -> str:
    source = (ROOT / "research/r075b_step27_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 215
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
    if section_index != 225:
        raise RuntimeError(f"Step 27 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.05"', 'data-site-version="2.06"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.05", "/i18n-en.js?v=2.06", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="The safe complete subclock and full endpoint row are paid for the frozen smooth common-shear family; outer-collar accumulated dissipation remains open">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75b.html">',
        "note canonical URL",
    )
    hero = f'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75B · STEP 27 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75B · Step 27 · OUTER PADDING GATE</div><h1>{TITLE}</h1><p>time-cutoff Caccioppoli ledger 将 frozen shell 分成 safe region 与 outer transition collar。<strong>safe complete subclock、inner padding 和完整 endpoint row 已支付；只剩 outer-collar accumulated dissipation。adverse full-window rate 是方法失败，不是 counterexample。完整 K、fixed deletion、suitable-weak extension 与 regularity 仍 OPEN。NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">SAFE SUBCLOCK PAID</span><span class="label">FULL ENDPOINT PAID</span><span class="label">OUTER DISSIPATION OPEN</span><span class="label">TEMPORAL PACKING GATE</span><span class="label">METHOD FAILURE ≠ COUNTEREXAMPLE</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75B STEP 27</strong><p>exact smooth common-shear family</p><p>safe complete subclock：PAID</p><p>inner padding：PAID</p><p>full endpoint row：PAID</p><p>safe rate：-92837/476280000</p><p>outer endpoint gain：4279/238140000</p><p>outer accumulated dissipation：OPEN</p><p>packing threshold：4279/79380000</p><p>full K / fixed deletion：OPEN</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_pattern(page, r'<section id="figure">[\s\S]*?</section>', "", "remove inherited Step 26 figure")
    page = replace_once(page, '<section id="reproduce">', render_step27_sections() + '\n<section id="reproduce">', "Step 27 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 27 主文、primary/literature audits、双实现证书与 QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075b_bulk_clock_outer_padding_gate.md">Step 27 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075b_bulk_clock_outer_padding_gate_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075b_literature_collision_note.md">bounded literature screen</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075b_bulk_clock_outer_padding_gate_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075b_bulk_clock_outer_padding_gate_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075b_bulk_clock_outer_padding_gate_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075b_bulk_clock_outer_padding_gate_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075b_bulk_clock_outer_padding_gate_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075b_bulk_clock_outer_padding_gate_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075b_bulk_clock_outer_padding_gate_qa.sh">QA script</a></p><p><a href="/notes/r0-75b.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 8/8、Ruby 9/9、47 unique tags、3 个 hash seeds 字节一致、20/20 与 21/21 mutations rejected。证书只覆盖 finite exact arithmetic、source binding 与 structural sentinels。bounded literature screen 只确认 Caccioppoli 属于既有方法；finite non-hit 不构成 novelty 或 priority 判断。本节纯解析，无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 27 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-206">← Step 26：moving-cutoff local dichotomy</a> · <a href="#next">outer-collar accumulated-dissipation packing 仍 OPEN →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 27 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / R0.75C 未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">outer-collar accumulated-dissipation packing 保持 OPEN</h2><p style="margin:.15rem 0">本站在 R0.75B Step 27 停止。下一命题必须证明有效 temporal packing threshold，或构造 accounting 完整的 exact smooth counterexample；二者均未完成。不得把 adverse upper-bound coefficient 写成反例，也不得把 strip lower 写成 whole-shell upper。full K、fixed deletion、arbitrary suitable weak extension、regularity 与 singularity 均未证明。R0.75C/D/E 与其他后续工作未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 27 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    # Keep regeneration idempotent: the release card is rebuilt from this
    # frozen generator rather than appended on every run.
    page = re.sub(
        r'\s*<div class="task-one" id="r075b"[\s\S]*?</div>\s*',
        "\n",
        page,
    )
    for old, new, label in (
        ('data-site-version="2.05"', 'data-site-version="2.06"', "home version"),
        ("/i18n-en.js?v=2.05", "/i18n-en.js?v=2.06", "home i18n"),
        ("/site-refresh.js?v=2.05.1", "/site-refresh.js?v=2.06.1", "home refresh"),
        ("<strong>v2.05</strong>网页版本", "<strong>v2.06</strong>网页版本", "home stat version"),
        ("<strong>R0.75A</strong>最新研究节点", "<strong>R0.75B</strong>最新研究节点", "home latest"),
        ("<strong>229</strong>公开研究笔记", "<strong>230</strong>公开研究笔记", "home public count"),
        ("展开 139 篇公开笔记", "展开 140 篇公开笔记", "home route count"),
        ("综述 v2.05 · 2026-09-03", "综述 v2.06 · 2026-09-03", "home footer"),
        ("Research topology · R0.1–R0.75A", "Research topology · R0.1–R0.75B", "home topology"),
        ('href="#r075a">跳到首页 R0.75A 卡片 →', 'href="#r075b">跳到首页 R0.75B 卡片 →', "home jump"),
        ("R0.70A–R0.75A：131 节已公开，104 节完整封存", "R0.70A–R0.75B：132 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75A</span>', '<span class="route-range">R0.69P–R0.75B</span>', "home range"),
        ("<h3>R0.75A：moving-cutoff local dichotomy 与 complete-clock open boundary</h3>", "<h3>R0.75B：safe complete subclock 与 outer-dissipation packing gate</h3>", "home route title"),
        ("R0.72R–R0.75A：</span>", "R0.72R–R0.75B：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75A"', 'aria-label="R0.69P–R0.75B"', "home links label"),
        ("全站现有 229 篇公开研究笔记", "全站现有 230 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(page, r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>', '<div class="summary-item"><strong>我目前关注</strong><span>R0.75B Step 27 已用 time-cutoff Caccioppoli ledger 支付 safe complete subclock、inner padding 和完整 endpoint row。唯一剩余项是 outer-collar accumulated dissipation；其 coarse full-window 正系数只是现有 upper-bound method 失败，不是 counterexample。下一缺口是有效 temporal packing。</span></div>', "home focus")
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75B · 2026-09-03 · STEP 27 · OUTER PADDING GATE</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">safe complete subclock、inner padding 与 full endpoint row 已由 cubic payment 支付；outer-collar accumulated dissipation 归约为有效 temporal packing。adverse full-window coefficient 不是 counterexample。full K、fixed deletion 与 suitable-weak extension 仍 OPEN。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75b.pdf">阅读最新 R0.75B 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">230 篇研究笔记总索引</a><a href="#r075b">查看首页 R0.75B 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75B · 132 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75B Step 27 outer padding gate</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">Step 27 pays the safe complete subclock and the full endpoint row for the frozen smooth common-shear family. Only outer-collar accumulated dissipation remains, reduced to an effective temporal-packing threshold. The adverse coarse rate is method failure, not a counterexample.</p>', "home current summary")
    page = replace_once(page, 'remote-tube coercivity / conditional endpoint persistence → exact moving-cutoff dichotomy / critical and shorter focusing closed / complete clock open</p>', 'moving-cutoff endpoint dichotomy → safe complete subclock paid / full endpoint paid / outer accumulated-dissipation packing open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75a.html">R0.75A</a>', '<a class="milestone" href="/notes/r0-75a.html">R0.75A</a>\n<a class="milestone" href="/notes/r0-75b.html">R0.75B</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · R0.75C NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>outer-collar accumulated-dissipation packing</h3><p>必须证明有效 temporal-packing threshold，或构造 accounting 完整的 exact smooth counterexample。R0.75C/D/E 与后续工作未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075b" data-release="r075b" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75B Step 27 · 2026-09-03 · OUTER PADDING GATE</p><h3>{TITLE}</h3><p>time-cutoff Caccioppoli 支付 safe complete subclock 与 full endpoint row；outer-collar accumulated dissipation 归约为 \(N_{{\\rm eff}}\) temporal packing。正的 coarse rate 是方法失败，不是反例。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75b.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75b.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075a"'
    if anchor not in page:
        raise RuntimeError("home R0.75A card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    # The bounded-screen boundary is generated here, so discard any prior
    # generated copy before inserting the single canonical block below.
    page = re.sub(
        r'\s*<h3 id="r075b-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\s*',
        "\n",
        page,
    )
    for old, new, label in (
        ('data-site-version="2.05"', 'data-site-version="2.06"', "literature version"),
        ("/i18n-en.js?v=2.05", "/i18n-en.js?v=2.06", "literature i18n"),
        ("文献综述 v2.05 · 2026-09-03", "文献综述 v2.06 · 2026-09-03", "literature footer"),
        ("本站 R0.69P–R0.75A 只列为研究笔记", "本站 R0.69P–R0.75B 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    route = '<div class="route-step kept"><header><b>R0.74W</b><strong>remote adjacent-inward relative threshold</strong></header><p>Step 22 证明 all-winding conditional-bridge threshold；fixed deletion 仍 OPEN。<a href="/notes/r0-74w.html">研究笔记</a> <a href="#r074w-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74X</b><strong>two-coordinate T* obstruction and cubic-payment no-go</strong></header><p>Step 23 证明 two-coordinate T* endpoint obstruction；actual normalized counterexample NOT PROVED。<a href="/notes/r0-74x.html">研究笔记</a> <a href="#r074x-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74Y</b><strong>frozen self-payment no-go and formal cancellation window</strong></header><p>Step 24 证明 frozen same-packet self-payment no-go；changed geometry 只有 formal window。<a href="/notes/r0-74y.html">研究笔记</a> <a href="#r074y-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.74Z</b><strong>remote persistence gate and full-clock open boundary</strong></header><p>Step 25 证明 persistent remote tube 的 exact kinetic coercivity 与 strict subcritical threshold；endpoint-to-tube 是 conditional。<a href="/notes/r0-74z.html">研究笔记</a> <a href="#r074z-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.75A</b><strong>moving-cutoff endpoint persistence/payment dichotomy</strong></header><p>Step 26 证明 persistence 与 rapid-rise 两支穷尽并强制 W-remote payment，覆盖 critical 与任意短光滑 focusing。<a href="/notes/r0-75a.html">研究笔记</a> <a href="/recap-r0-61-r0-75a.html">P–A recap</a> <a href="#r075a-boundary">文献与主张边界</a></p></div><div class="route-step kept"><header><b>R0.75B</b><strong>safe complete subclock and outer-padding gate</strong></header><p>Step 27 支付 safe complete subclock、inner padding 与完整 endpoint row；outer accumulated dissipation 归约为 temporal packing，full K 仍 OPEN。<a href="/notes/r0-75b.html">研究笔记</a> <a href="#r075b-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · R0.75C</b><strong>outer-collar accumulated-dissipation packing</strong></header><p>必须证明有效 packing threshold 或构造 accounting 完整的 exact smooth counterexample；后续材料未读取、未公开。</p></div>'
    page = replace_pattern(page, r'<div class="route-step kept"><header><b>R0\.74W</b>[\s\S]*?<div class="route-step pause"><header><b>开放接口[^<]*</b>[\s\S]*?</div>', route, "literature route")
    boundary = '<h3 id="r075b-boundary">R0.75B Step 27 的 bounded literature screen 与主张边界</h3><p>Chang--Kang（arXiv:1806.02516）与 Gallay--Slijepcevic（arXiv:1308.1544）确认 local-energy/Caccioppoli 与 localized dissipation 是既有方法；Wang--Wang--Zhang--Zhang（arXiv:1711.04279）提供 heat-observability 邻近背景。三篇一手来源的 bounded non-hit 不证明 novelty、priority、nonexistence、correctness 或 publishability。</p><div class="boundary"><strong>R0.75B Step 27 公开边界</strong><p>PROVED：冻结 exact smooth inversion-paired common-shear family 上的 safe complete subclock、inner padding 与 full endpoint row payment。FINITE：Python 8/8、Ruby 9/9、20/20 与 21/21 mutation rejection。OPEN：outer-collar accumulated dissipation、effective temporal packing、full K、fixed deletion、arbitrary suitable-weak extension、regularity 与 singularity。adverse full-window coefficient 是 method failure，不是 counterexample。正式图件 NOT APPLICABLE；无 simulation、DNS 或 DGX。<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75b.html">阅读完整笔记</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap</a>。</p></div>\n'
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 230 or pdf_count not in (186, 187):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    post_r060 = len(previous.route_post_r060_slugs(HOME.read_text(encoding="utf-8")))
    if post_r060 != 170:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1", "version": VERSION, "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75b.html", "latestPublishedResearchPdf": "/notes/r0-75b.pdf",
        "publicHtmlNoteCount": html_count, "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169, "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count, "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r075a":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 132
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {"r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22, "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26, "r075b": 27}
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1, "research_version": CODE,
        "scope": "BULK_COMPLETE_CLOCK_OUTER_PADDING_GATE",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": None,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 10,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_THEOREM_AND_FAIL_CLOSED_ROUTE_DIAGNOSIS",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED", "dgx": "NOT_USED",
            "novelty_priority_publishability": "NOT_CLAIMED",
            "safe_complete_subclock": "PAID",
            "full_endpoint_row": "PAID",
            "outer_accumulated_dissipation": "OPEN",
            "full_clock_fixed_deletion": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_10_OF_10",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_8_OF_8",
            "independent_ruby": "PASS_9_OF_9",
            "negative_mutations": "PASS_PYTHON_20_OF_20_RUBY_21_OF_21",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/", "target_html": "/notes/r0-75b.html",
            "target_pdf": "/notes/r0-75b.pdf", "target_primary_figure": None,
            "recap_update_required": False, "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075b_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE, "latestCompletedStep": 27, "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count, "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060, "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 132, "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075c", "latestPublishedResearchHtml": "/notes/r0-75b.html",
        "latestPublishedResearchPdf": "/notes/r0-75b.pdf",
        "latestReleaseGate": "tests/r075b-step27-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075b-step27-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075b-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075b-step27-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075b-step27-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075b-step27-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075b-step27-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075b-step27", "handoffCommit": None,
            "handoffSha256": frozen_import.HANDOFF_SHA256,
            "handoffIndependentAuditSha256": frozen_import.HANDOFF_AUDIT_SHA256,
            "sourceCommit": frozen_import.SOURCE_COMMIT, "coreCommit": frozen_import.SOURCE_COMMIT,
            "formalFigureRequired": False, "recapRequired": False,
        },
        "latestRecapRelease": "r075a", "latestRecapHtml": "/recap-r0-61-r0-75a.html",
        "latestRecapPdf": "/recap-r0-61-r0-75a.pdf", "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {"path": "research/formal-archive-inventory.json", "sha256": sha256(inventory_target)}
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-75b.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated", "latestRelease": CODE, "latestCompletedStep": 27,
        "siteVersion": VERSION, "recapUpdated": False, "recapNodes": 169,
        "formalFigure": None, "formalFigureExemption": True,
        "simulation": False, "pdeData": False, "noveltyClaim": False,
        "clayClaim": False, "dgxUsed": False,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
