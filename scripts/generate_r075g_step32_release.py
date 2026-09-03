#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75G Step 32 from the verified R0.75F Step 31 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075f_step31_release as previous
import import_r075g_step32_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.11"
RELEASE = "r075g"
CODE = "R0.75G"
TITLE = "R0.75G｜正号 collar flux 的精确增益阈值：一组三分之一足够，四分之一不够这条路线"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-75a.html": "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0",
    PUBLIC / "recap-r0-61-r0-75a.pdf": "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62",
}

sha256 = previous.sha256
write_text = previous.write_text
write_json = previous.write_json
replace_once = previous.replace_once
replace_pattern = previous.replace_pattern
inline_markup = previous.inline_markup


def verify_frozen_sources() -> None:
    previous.verify_frozen_sources()
    for target, expected in RECAP_HASHES.items():
        if sha256(target) != expected:
            raise RuntimeError(f"protected R0.75A recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.75G frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075g_signed_flux_gain_threshold_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions", {}).get("total") != 16
        or certificate.get("assertions", {}).get("passed") != 16
        or len(certificate.get("checks", {})) != 16
    ):
        raise RuntimeError("R0.75G certificate verdict drift")
    main = (ROOT / "research/r075g_signed_flux_gain_threshold.md").read_text()
    for token in (
        r"\mathfrak X_{\xi,R}(F,b)",
        r"\frac{27163}{107163}",
        r"\frac{27163}{35721}",
        r"-\frac{4279}{238140000}<0",
        r"\frac{1489}{1905120000}>0",
        r"\tag{G.24}",
        "not a proof of (G.1)",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75G boundary drift: {token}")


def render_step32_sections() -> str:
    source = (ROOT / "research/r075g_step32_report-source.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 255
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
    if section_index != 264:
        raise RuntimeError(f"Step 32 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.10"', 'data-site-version="2.11"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.10", "/i18n-en.js?v=2.11", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="The exact conditional gain threshold for the positive signed collar flux is alpha greater than 27163 over 107163; every positive gain remains open">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75g.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75G · STEP 32 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75G · Step 32 · EXACT SIGNED-FLUX GAIN THRESHOLD</div><h1>{TITLE}</h1><p>若独立动力学估计给出 <strong>R^alpha</strong> signed-flux gain，则这条 reduction 的精确充分条件是 <strong>alpha &gt; 27163/107163</strong>。R^(1/3) 有严格负 margin，R^(1/4) 对这条路线不够。<strong>正增益、G.24 与 E.24 仍 OPEN；NO NOVELTY CLAIM. NOT CLAY.</strong></p><div class="labels"><span class="label">EXACT THRESHOLD PROVED</span><span class="label">ALPHA STAR 27163/107163</span><span class="label">STRICT INEQUALITY REQUIRED</span><span class="label">ONE THIRD CONDITIONALLY SUFFICIENT</span><span class="label">ONE QUARTER INSUFFICIENT BY THIS ROUTE</span><span class="label">AMPLITUDE GAIN IMPOSSIBLE</span><span class="label">RESIDENCE BETA STAR 27163/35721</span><span class="label">POSITIVE GAIN OPEN</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75G STEP 32</strong><p>threshold arithmetic：PROVED</p><p>alpha star：27163/107163</p><p>alpha=1/3 margin：NEGATIVE</p><p>alpha=1/4 margin：POSITIVE</p><p>beta star：27163/35721</p><p>G.24：OPEN</p><p>E.24：OPEN</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step32_sections() + '\n<section id="reproduce">', "Step 32 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 32 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075g_signed_flux_gain_threshold.md">Step 32 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075g_signed_flux_gain_threshold_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075g_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075g_signed_flux_gain_threshold_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075g_signed_flux_gain_threshold_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075g_signed_flux_gain_threshold_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075g_signed_flux_gain_threshold_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075g_signed_flux_gain_threshold_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075g_signed_flux_gain_threshold_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075g_signed_flux_gain_threshold_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075g_signed_flux_gain_threshold_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075g_signed_flux_gain_threshold_qa.sh">QA script</a></p><p><a href="/notes/r0-75g.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 16/16、Ruby 18/18、G.1--G.24 与 24/24 displays，3 个 Python hash seeds 字节稳定；两套实现分别拒绝 57/57 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12，显式包含两套验证器直接读取的 fixtures 与 expected JSON。本节纯解析，无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 32 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-248">← Step 31：phase-substitution no-go</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 32 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">G.24 与 E.24 均保持 OPEN</h2><p style="margin:.15rem 0">本站在 R0.75G Step 32 停止。本节只给出 conditional gain estimate 的 exact threshold；没有证明任意实场的 positive gain、interaction atom 或 diffusion residence estimate。complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity 均未闭合。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 32 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    page = re.sub(r'\s*<div class="task-one" id="r075g"[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.10"' in page:
        for old, new, label in (
            ('data-site-version="2.10"', 'data-site-version="2.11"', "home version"),
            ("/i18n-en.js?v=2.10", "/i18n-en.js?v=2.11", "home i18n"),
            ("/site-refresh.js?v=2.10.1", "/site-refresh.js?v=2.11.1", "home refresh"),
            ("<strong>v2.10</strong>网页版本", "<strong>v2.11</strong>网页版本", "home stat version"),
            ("<strong>R0.75F</strong>最新研究节点", "<strong>R0.75G</strong>最新研究节点", "home latest"),
            ("<strong>234</strong>公开研究笔记", "<strong>235</strong>公开研究笔记", "home public count"),
            ("展开 144 篇公开笔记", "展开 145 篇公开笔记", "home route count"),
            ("综述 v2.10 · 2026-09-03", "综述 v2.11 · 2026-09-03", "home footer"),
            ("Research topology · R0.1–R0.75F", "Research topology · R0.1–R0.75G", "home topology"),
            ('href="#r075f">跳到首页 R0.75F 卡片 →', 'href="#r075g">跳到首页 R0.75G 卡片 →', "home jump"),
            ("R0.70A–R0.75F：136 节已公开，104 节完整封存", "R0.70A–R0.75G：137 节已公开，104 节完整封存", "home accounting"),
            ('<span class="route-range">R0.69P–R0.75F</span>', '<span class="route-range">R0.69P–R0.75G</span>', "home range"),
            ("<h3>R0.75F：modal phase-integration identity 与 positivity-only diagonal no-go</h3>", "<h3>R0.75G：signed-flux gain 的 exact threshold 与 residence exponent</h3>", "home route title"),
            ("R0.72R–R0.75F：</span>", "R0.72R–R0.75G：</span>", "home detail range"),
            ('aria-label="R0.69P–R0.75F"', 'aria-label="R0.69P–R0.75G"', "home links label"),
            ("全站现有 234 篇公开研究笔记", "全站现有 235 篇公开研究笔记", "home recap count"),
        ):
            page = replace_once(page, old, new, label)
        page = replace_pattern(
            page,
            r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
            '<div class="summary-item"><strong>我目前关注</strong><span>R0.75G Step 32 把剩余 signed collar flux 的独立增益需求量化为精确阈值 alpha&gt;27163/107163；R^(1/3) 条件足够，R^(1/4) 对这条 reduction 不够。任何 arbitrary-real positive gain、G.24 与 E.24 仍待证明。</span></div>',
            "home focus",
        )
        latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75G · 2026-09-03 · STEP 32 · EXACT SIGNED-FLUX GAIN THRESHOLD</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">在独立估计 X ≤ C R^alpha p_b^(1/3) p_F^(2/3) 下，精确充分阈值是 alpha&gt;27163/107163。R^(1/3) 有严格负 margin；R^(1/4) 只说明这条 route 不闭合。positive gain 与 E.24 仍 OPEN。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75g.pdf">阅读最新 R0.75G 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">235 篇研究笔记总索引</a><a href="#r075g">查看首页 R0.75G 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75G · 137 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75G Step 32 exact signed-flux gain threshold</span></div></div></section>'''
        page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
        page = replace_pattern(
            page,
            r'<p class="tree-current-summary">.*?</p>',
            '<p class="tree-current-summary">Step 32 derives the exact conditional threshold alpha&gt;27163/107163 for a genuinely new signed-flux gain. One third is sufficient with strict margin; one quarter does not close this route. Every positive gain and E.24 remain open.</p>',
            "home current summary",
        )
        page = replace_once(
            page,
            'difference-frequency flux → exact phase reconstruction / positivity-only diagonal no-go / dynamic coercivity open</p>',
            'phase-substitution no-go → exact signed-flux gain threshold / one-third target / positive gain open</p>',
            "home route path",
        )
        page = replace_once(
            page,
            '<a class="milestone" href="/notes/r0-75f.html">R0.75F</a>',
            '<a class="milestone" href="/notes/r0-75f.html">R0.75F</a>\n<a class="milestone" href="/notes/r0-75g.html">R0.75G</a>',
            "home milestone",
        )
    elif 'data-site-version="2.11"' not in page:
        raise RuntimeError("home baseline version drift")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>positive signed-flux gain remains unproved</h3><p>必须由 independent dynamics、residence-time、resolvent 或 payment-sensitive information 证明；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075g" data-release="r075g" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75G Step 32 · 2026-09-03 · EXACT SIGNED-FLUX GAIN THRESHOLD</p><h3>{TITLE}</h3><p>conditional estimate 的精确门槛为 alpha&gt;27163/107163；R^(1/3) 足够，R^(1/4) 对这条 route 不足。amplitude scaling 不能制造 gain；residence exponent 必须满足 beta&gt;27163/35721。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75g.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75g.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075f"'
    if anchor not in page:
        raise RuntimeError("home R0.75F card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    page = re.sub(r'\s*<h3 id="r075g-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.10"' in page:
        for old, new, label in (
            ('data-site-version="2.10"', 'data-site-version="2.11"', "literature version"),
            ("/i18n-en.js?v=2.10", "/i18n-en.js?v=2.11", "literature i18n"),
            ("文献综述 v2.10 · 2026-09-03", "文献综述 v2.11 · 2026-09-03", "literature footer"),
            ("本站 R0.69P–R0.75F 只列为研究笔记", "本站 R0.69P–R0.75G 只列为研究笔记", "literature intro"),
        ):
            page = replace_once(page, old, new, label)
        old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>genuine coercive information for E.24</strong></header><p>必须加入 uncertainty、resolvent/hypocoercive、pathwise residence-time 或 payment-sensitive positive Toeplitz estimate；后续材料未读取、未公开。</p></div>'
        route = '<div class="route-step kept"><header><b>R0.75G</b><strong>exact conditional signed-flux gain threshold</strong></header><p>Step 32 证明 conditional estimate 的精确充分阈值 alpha&gt;27163/107163，并把 interaction residence threshold 写成 beta&gt;27163/35721。R^(1/3) 条件足够；R^(1/4) 对此 route 不充分，但不是 counterexample。<a href="/notes/r0-75g.html">研究笔记</a> <a href="#r075g-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>positive signed-flux gain remains open</strong></header><p>必须加入 independent dynamic、resolvent、pathwise residence-time 或 payment-sensitive information；后续材料未授权、未读取、未公开。</p></div>'
        page = replace_once(page, old_next, route, "literature route")
    elif 'data-site-version="2.11"' not in page:
        raise RuntimeError("literature baseline version drift")
    boundary = (
        '<h3 id="r075g-boundary">R0.75G Step 32 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Siming He 的 neighboring shear result 使用 resolvent/semigroup information；'
        'Gardner--Liss--Mattingly 的 pathwise 方法加入 trajectory separation 与 local shear；'
        'Albritton--Dong 的 physical localization 保留 drift flux 并需要定量 drift/geometric control。'
        '没有一个 inspected source 给出 G.1、R^(1/3) target G.24 或 Version-M spherical-collar theorem。'
        '有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75G Step 32 公开边界</strong><p>'
        'PROVED：若独立 gain estimate G.1 成立，则 exact sufficient threshold 为 alpha&gt;27163/107163；'
        'alpha=1/3 的 rate 是 -4279/238140000，alpha=1/4 的 rate 是 1489/1905120000；'
        'amplitude scaling 不改变 correlation ratio；interaction atom 的 threshold 是 beta&gt;27163/35721；'
        'pure-transport benchmark 把 signed flux 写成 endpoint half-energy difference。'
        'FINITE KINEMATIC ONLY：一次 unwrapped monotone crossing 的 O(R^3) occupation 形式上对应 beta=1、alpha=1/3，'
        '但不证明 diffusing/interfering passive field 的 interaction estimate。'
        'OPEN：任意 positive gain、G.18、G.24、E.24、complete clock、fixed deletion、suitable-weak transfer、'
        'regularity 与 singularity。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75g.html">阅读完整笔记</a> · '
        '<a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap</a>。</p></div>\n'
    )
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 235 or pdf_count not in (191, 192):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 175:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75g.html",
        "latestPublishedResearchPdf": "/notes/r0-75g.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r075f":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 137
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {
        "r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22,
        "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26, "r075b": 27,
        "r075c": 28, "r075d": 29, "r075e": 30, "r075f": 31, "r075g": 32,
    }
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "EXACT_CONDITIONAL_SIGNED_FLUX_GAIN_THRESHOLD_AND_RESIDENCE_EXPONENT",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_CONDITIONAL_THRESHOLD",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "background_atom_upper_bound": "PROVED",
            "conditional_alpha_threshold": "PROVED_STRICT_ALPHA_GT_27163_OVER_107163",
            "alpha_one_third": "CONDITIONALLY_SUFFICIENT_STRICT_NEGATIVE_MARGIN",
            "alpha_one_quarter": "INSUFFICIENT_FOR_THIS_REDUCTION_NOT_COUNTEREXAMPLE",
            "amplitude_scaling_gain": "IMPOSSIBLE_BY_HOMOGENEITY",
            "interaction_beta_threshold": "PROVED_STRICT_BETA_GT_27163_OVER_35721",
            "monotone_crossing_benchmark": "KINEMATIC_ONLY_NOT_DIFFUSIVE_PROOF",
            "pure_transport_benchmark": "PROVED_NOT_DIFFUSIVE_PROOF",
            "positive_gain_G1": "OPEN_UNPROVED",
            "interaction_atom_G18": "OPEN_UNPROVED",
            "minimum_target_G24": "OPEN_UNPROVED",
            "arbitrary_real_E24": "OPEN",
            "complete_clock": "OPEN_NOT_PROVED",
            "fixed_deletion": "OPEN_NOT_PROVED",
            "suitable_weak_transfer": "OPEN_NOT_PROVED",
            "regularity_or_singularity": "OPEN_NOT_PROVED_OR_DISPROVED",
            "clay_problem": "NOT_CLAIMED_NOT_CLAY",
        },
        "verification": {
            "frozen_hash_ledger": "PASS_12_OF_12",
            "primary_analytic_audit": "PASS_ZERO_BLOCKERS",
            "python_certificate": "PASS_16_OF_16",
            "independent_ruby": "PASS_18_OF_18",
            "negative_mutations": "PASS_PYTHON_57_OF_57_RUBY_57_OF_57",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_G1_TO_G24_24_OF_24",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75g.html",
            "target_pdf": "/notes/r0-75g.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075g_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 32,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 137,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075h",
        "latestPublishedResearchHtml": "/notes/r0-75g.html",
        "latestPublishedResearchPdf": "/notes/r0-75g.pdf",
        "latestReleaseGate": "tests/r075g-step32-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075g-step32-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075g-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075g-step32-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075g-step32-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075g-step32-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075g-step32-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075g-step32",
            "handoffCommit": frozen_import.HANDOFF_COMMIT,
            "handoffSha256": frozen_import.HANDOFF_SHA256,
            "handoffIndependentAuditSha256": frozen_import.HANDOFF_AUDIT_SHA256,
            "sourceCommit": frozen_import.SOURCE_COMMIT,
            "coreCommit": frozen_import.SOURCE_COMMIT,
            "formalFigureRequired": False,
            "recapRequired": False,
        },
        "latestRecapRelease": "r075a",
        "latestRecapHtml": "/recap-r0-61-r0-75a.html",
        "latestRecapPdf": "/recap-r0-61-r0-75a.pdf",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256(inventory_target),
    }
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-75g.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 32,
        "siteVersion": VERSION,
        "recapUpdated": False,
        "recapNodes": 169,
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
