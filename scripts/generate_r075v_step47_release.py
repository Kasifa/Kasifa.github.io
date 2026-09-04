#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75V Step 47 from the verified R0.75U Step 46 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075u_step46_release as previous
import import_r075v_step47_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
BASELINE_COMMIT = "fed5c55f349c918e6cae7079b0a128acb4e74627"
VERSION = "2.26"
RELEASE = "r075v"
CODE = "R0.75V"
TITLE = "R0.75V｜单个 dyadic 二谐波剪切的完整 signed-flux 付款"
RECAP_SLUG = "recap-r0-61-r0-75v"
RECAP_HASHES = {
    PUBLIC / "recap-r0-61-r0-75a.html": "208a225b64f7dcffefb9822846180d19245f20617e2e70e91fdac696b4d48dc0",
    PUBLIC / "recap-r0-61-r0-75a.pdf": "13342b731db2a85780d21ab721347d2cc23f6fee03809e9150b895eb7931ef62",
}

sha256 = previous.sha256
write_text = previous.write_text
write_json = previous.write_json
replace_once = previous.replace_once
replace_pattern = previous.replace_pattern
base_inline_markup = previous.inline_markup


def inline_markup(value: str) -> str:
    """Render the frozen source's lightweight inline Markdown for the public reader."""
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
            raise RuntimeError(f"protected R0.75A recap drift: {target.relative_to(ROOT)}")
    for relative, expected in frozen_import.FROZEN.items():
        if sha256(ROOT / relative) != expected:
            raise RuntimeError(f"R0.75V frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075v_complete_two_harmonic_flux_payment_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertionCount") != 17
        or len(certificate.get("assertions", [])) != 17
    ):
        raise RuntimeError("R0.75V certificate verdict drift")
    main = (ROOT / "research/r075v_complete_two_harmonic_flux_payment.md").read_text()
    for token in (
        r"\tag{V.1}", r"\tag{V.3}", r"\tag{V.4}", r"\tag{V.6}",
        r"\tag{V.13}", r"\tag{V.21}", r"\tag{V.27}", r"\tag{V.31}",
        r"\tag{V.40}", r"\tag{V.43}",
        "Bounding those rows separately destroys",
        "complete flux theorem only for the exact high-carrier dyadic pair",
        "If `xy=0`",
        "three or more harmonics",
        "**NOT CLAY.**",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75V boundary drift: {token}")
    source_report = (ROOT / "research/r075v_report-source.md").read_text()
    if "not evidence of novelty" not in source_report or "priority" not in source_report:
        raise RuntimeError("R0.75V bounded source-claim boundary drift")


def render_step47_sections() -> str:
    source = (ROOT / "research/r075v_complete_two_harmonic_flux_payment.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 363
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
    if section_index != 373:
        raise RuntimeError(f"Step 47 reader section drift: {section_index}")
    # The PDF browser occasionally exposes \qquad as literal text in the
    # generated print layer.  Equivalent explicit thin-space pairs avoid that
    # renderer defect without changing the frozen Markdown source or formula.
    rendered = "\n".join(output).replace(r"\qquad", r"\;\;")
    return rendered.replace("qquad", r"\;\;")


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.25"', 'data-site-version="2.26"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.25", "/i18n-en.js?v=2.26", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="Joint self-and-sum payment and complete signed collar-flux theorem for one exact diffusive high-carrier dyadic two-harmonic pair.">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75v.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75V · STEP 47 · 2026-09-04</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75V · Step 47 · COUPLED SELF/SUM PAYMENT</div><h1>{TITLE}</h1><p>V 保留 two self-frequency rows 与 sum-frequency row 的联合二次抵消并支付这一 coupled block；与 U 的 difference-frequency payment 合并后，只对一个 exact diffusive high-carrier dyadic two-harmonic pair 得到完整 signed collar-flux theorem，且保留精确 <strong>-2/11907</strong> 对数率。低载频、三模以上和任意 packet 仍开放。<strong>NOT CLAY.</strong></p><div class="labels"><span class="label">SELF + SUM BLOCK PAID</span><span class="label">JOINT CANCELLATION RETAINED</span><span class="label">EXACTLY TWO HARMONICS</span><span class="label">ONE DYADIC PAIR</span><span class="label">HIGH CARRIER</span><span class="label">COMPLETE CLOCK</span><span class="label">FULL EXACT-PAIR FLUX</span><span class="label">MULTIPLIER TWO-JET</span><span class="label">RIGHT-ENDPOINT TRACE</span><span class="label">R POWERS CANCEL</span><span class="label">EXACT RATE -2/11907</span><span class="label">VERSION-M CONDITIONAL</span><span class="label">MULTIMODE OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75V STEP 47</strong><p>scope：exact pair only</p><p>band：1 &lt;= m &lt; k &lt;= 2m</p><p>carrier：maR &gt;= C_0</p><p>clock：T_R = 4R^2</p><p>U：difference row paid</p><p>V：self + sum block paid</p><p>payment：a^(2/3)R^(-1/3)M^(2/3)</p><p>normalized R-power：0</p><p>rate：-2/11907</p><p>open：low carrier / 3+ modes / packets</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step47_sections() + '\n<section id="reproduce">', "Step 47 sections")
    evidence = '''<section id="reproduce"><div class="section-no">V / 冻结证据</div><h2>Step 47 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075v_complete_two_harmonic_flux_payment.md">Step 47 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075v_complete_two_harmonic_flux_payment_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075v_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075v_complete_two_harmonic_flux_payment_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075v_complete_two_harmonic_flux_payment_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075v_complete_two_harmonic_flux_payment_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075v_complete_two_harmonic_flux_payment_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075v_complete_two_harmonic_flux_payment_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075v_complete_two_harmonic_flux_payment_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075v_complete_two_harmonic_flux_payment_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075v_complete_two_harmonic_flux_payment_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075v_complete_two_harmonic_flux_payment_qa.sh">QA script</a></p><p><a href="/notes/r0-75v.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75v.html">最新累计回顾（截止 R0.75V）</a> · <a href="/recap-r0-61-r0-75v.pdf">同步 recap PDF</a></p><p class="note">Certificate：Python 17/17、Ruby 18/18、V.1--V.43、43/43 tags 与 43/43 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 84/84 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。有限检查不代替 continuum multiplier-jet 或 endpoint-trace 证明；本节无正式图、simulation、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 47 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>T、U 与 V 的精确分工</h2><p><a href="#s-351">T：spatial collar coercivity</a> · <a href="#s-358">U：difference-frequency payment</a> · <a href="#next">后续边界 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 47 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">low carriers, three or more harmonics, and arbitrary packets remain OPEN</h2><p style="margin:.15rem 0">本站在 R0.75V Step 47 停止。V 仅对一个 exact diffusive high-carrier dyadic two-harmonic pair 关闭完整 signed collar flux；low-carrier pairs、三个及以上 harmonics、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍开放。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 47 next")


def update_home() -> None:
    page = baseline_text("public/research-review.html")
    for old, new, label in (
        ('data-site-version="2.25"', 'data-site-version="2.26"', "home version"),
        ("/i18n-en.js?v=2.25", "/i18n-en.js?v=2.26", "home i18n"),
        ("/site-refresh.js?v=2.25.1", "/site-refresh.js?v=2.26.1", "home refresh"),
        ("<strong>v2.25</strong>网页版本", "<strong>v2.26</strong>网页版本", "home stat version"),
        ("<strong>R0.75U</strong>最新研究节点", "<strong>R0.75V</strong>最新研究节点", "home latest"),
        ("<strong>249</strong>公开研究笔记", "<strong>250</strong>公开研究笔记", "home public count"),
        ("展开 159 篇公开笔记", "展开 160 篇公开笔记", "home route count"),
        ("综述 v2.25 · 2026-09-04", "综述 v2.26 · 2026-09-04", "home footer"),
        ("Research topology · R0.1–R0.75U", "Research topology · R0.1–R0.75V", "home topology"),
        ('href="#r075u">跳到首页 R0.75U 卡片 →', 'href="#r075v">跳到首页 R0.75V 卡片 →', "home jump"),
        ("R0.70A–R0.75U：151 节已公开，104 节完整封存", "R0.70A–R0.75V：152 节已公开，104 节完整封存", "home accounting"),
        ('<span class="route-range">R0.69P–R0.75U</span>', '<span class="route-range">R0.69P–R0.75V</span>', "home range"),
        ("<h3>R0.75U：单个二谐波 dyadic pair 的差频项完整时钟付款</h3>", "<h3>R0.75V：单个 dyadic 二谐波 pair 的完整 signed-flux 付款</h3>", "home route title"),
        ("R0.72R–R0.75U：</span>", "R0.72R–R0.75V：</span>", "home detail range"),
        ('aria-label="R0.69P–R0.75U"', 'aria-label="R0.69P–R0.75V"', "home links label"),
        ("全站现有 249 篇公开研究笔记", "全站现有 250 篇公开研究笔记", "home recap count"),
    ):
        page = replace_once(page, old, new, label)
    page = replace_pattern(
        page,
        r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
        '<div class="summary-item"><strong>我目前关注</strong><span>R0.75V Step 47 已保留并支付 two self rows 与 sum row 的联合抵消；与 U 的 difference row 合并后，对一个 exact diffusive high-carrier dyadic two-harmonic pair 得到完整 signed collar-flux theorem。low carriers、三个及以上 modes 与 arbitrary packets 仍开放。</span></div>',
        "home focus",
    )
    latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75V · 2026-09-04 · STEP 47 · COUPLED SELF/SUM PAYMENT</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">T 给出 two-wave spatial collar coercivity，U 支付 difference-frequency row，V 保留并支付 two self rows 与 sum row 的联合抵消；三者合并后，只对一个 exact diffusive high-carrier dyadic two-harmonic pair 得到完整 signed collar-flux theorem，并保留精确 <strong>-2/11907</strong> 对数率。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75v.pdf">阅读最新 R0.75V 研究笔记 →</a><a href="/{RECAP_SLUG}.html">最新累计回顾（R0.61–R0.75V，190 节）</a><a href="/notes/">250 篇研究笔记总索引</a><a href="#r075v">查看首页 R0.75V 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75V · 152 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75V Step 47 exact-pair complete signed-flux payment</span></div></div></section>'''
    page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
    page = replace_pattern(page, r'<p class="tree-current-summary">.*?</p>', '<p class="tree-current-summary">T supplies spatial coercivity, U pays the difference row, and V jointly pays the two self rows and sum row. The resulting full signed-flux theorem is limited to one exact diffusive high-carrier dyadic two-harmonic pair.</p>', "home current summary")
    page = replace_once(page, 'high-carrier two-harmonic spatial coercivity → complete-clock difference-frequency payment / combined self-sum block open</p>', 'high-carrier two-harmonic spatial coercivity → complete-clock difference-frequency payment → coupled self-sum payment → exact-pair complete signed flux / low carriers and multimode open</p>', "home route path")
    page = replace_once(page, '<a class="milestone" href="/notes/r0-75u.html">R0.75U</a>', '<a class="milestone" href="/notes/r0-75u.html">R0.75U</a>\n<a class="milestone" href="/notes/r0-75v.html">R0.75V</a>', "home milestone")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>low carriers, three or more harmonics, and arbitrary packets</h3><p>V 只关闭一个 exact diffusive high-carrier dyadic two-harmonic pair 的完整 signed collar flux。low-carrier pairs、三个及以上 harmonics、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、E.24 与 Version-M extraction 仍开放。后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075v" data-release="r075v" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75V Step 47 · 2026-09-04 · COUPLED SELF/SUM PAYMENT</p><h3>{TITLE}</h3><p>V 的 multiplier two-jet、quadratic cancellation、separate phase integration 与 right-endpoint trace 联合支付 self/sum block；加上 U 的 difference row，得到 exact high-carrier dyadic pair 的完整 signed-flux theorem。低载频、三模以上、任意 packets 与一般 Version-M extraction 仍开放。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75v.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75v.pdf">PDF</a> · <a href="/{RECAP_SLUG}.html">最新 milestone recap（截止 V）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075u"'
    if anchor not in page:
        raise RuntimeError("home R0.75U card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    recap_card = f'''<div class="task-one" id="post-r060-recap" style="margin-top:2rem"><p class="eyebrow">累计里程碑回顾 R0.61–R0.75V · 2026-09-04</p><h3>R0.60 recap 之后的累计回顾收录 190 个节点；全站现有 250 篇公开研究笔记</h3><p>T 固定 two-wave spatial coercivity，U 支付 difference-frequency row，V 联合支付 self 与 sum rows；exact high-carrier dyadic pair 的完整 signed flux 已闭合。</p><p><strong>当前边界：</strong>low carriers、三个及以上 modes、arbitrary packets、Version-M 一般化、regularity 与 Clay 仍 OPEN。</p><p><a href="/{RECAP_SLUG}.html"><strong>阅读 R0.61–R0.75V 完整累计回顾 →</strong></a> · <a href="/{RECAP_SLUG}.pdf">下载同步 PDF</a> · <a href="/recap-r0-61-r0-75a.html">保留上一版本</a></p></div>'''
    page = replace_pattern(page, r'<div class="task-one" id="post-r060-recap"[\s\S]*?</div>', recap_card, "home recap card")
    write_text(HOME, page)


def update_literature() -> None:
    page = baseline_text("public/literature-review.html")
    for old, new, label in (
        ('data-site-version="2.25"', 'data-site-version="2.26"', "literature version"),
        ("/i18n-en.js?v=2.25", "/i18n-en.js?v=2.26", "literature i18n"),
        ("文献综述 v2.25 · 2026-09-04", "文献综述 v2.26 · 2026-09-04", "literature footer"),
        ("本站 R0.69P–R0.75U 只列为研究笔记", "本站 R0.69P–R0.75V 只列为研究笔记", "literature intro"),
    ):
        page = replace_once(page, old, new, label)
    old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>combined self / sum frequency payment remains open</strong></header><p>two self-frequency rows 与 sum-frequency row 的联合付款、complete two-harmonic signed-flux theorem、low carriers、三个及以上 harmonics、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、E.24 与 Version-M extraction 均未闭合。后续材料未授权、未读取、未公开。</p></div>'
    route = f'<div class="route-step kept"><header><b>R0.75V</b><strong>coupled self/sum payment and complete exact-pair signed flux</strong></header><p>Step 47 以 radial quotient two-jet、quadratic cancellation、逐相位 integration by parts 与 right-endpoint complete-clock trace 联合支付 two self rows 和 sum row；与 U 的 difference row 合并后，得到 exact diffusive high-carrier dyadic pair 的完整 signed collar-flux theorem。<a href="/notes/r0-75v.html">研究笔记</a> <a href="/{RECAP_SLUG}.html">milestone recap</a> <a href="#r075v-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>low carriers, three or more modes, and arbitrary packets</strong></header><p>exact pair 之外，low carriers、三个及以上 harmonics、arbitrary packets、inter-packet aggregation、nonconstant or vertical shear、projection、E.24 与 Version-M extraction 均未闭合。后续材料未授权、未读取、未公开。</p></div>'
    page = replace_once(page, old_next, route, "literature route")
    boundary = (
        '<h3 id="r075v-boundary">R0.75V Step 47 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Singh--Sridhar、Bedrossian--Vicol--Wang、Egidi--Veselić 与 Clay 官方说明只提供 exact shear、mixing、observability 和 Millennium problem 的相邻背景；V 的 multiplier two-jet、quadratic cancellation、endpoint trace 与 flux payment 均由本地 elementary argument 证明，不导入这些外部定理。有限检索不构成 completeness、novelty 或 priority 判断。</p>'
        '<div class="boundary"><strong>R0.75V Step 47 公开边界 · EXACT HIGH-CARRIER PAIR ONLY</strong><p>'
        'PROVED：V.13--V.17 radial quotient two-jet；V.21--V.25 quadratic cancellation 与 heat extra term；V.27 exact separate-phase integration；V.31--V.36 right-endpoint trace；V.3 joint self/sum payment；V.4--V.7 complete exact-pair signed-flux estimate、R-power cancellation 与 -2/11907 rate；V.42 exact smooth unforced shear。CONDITIONAL：V.43 仍要求 realized-subclass 与 ledger alignment，且 F 是同一实际速度的 component。'
        'OPEN：low-carrier pairs；三个及以上 harmonics；arbitrary packets；inter-packet aggregation；nonconstant or vertically dependent shear；projection；arbitrary-field E.24；complete Version-M extraction；fixed deletion；suitable-weak transfer；regularity 与 singularity。finite checks 不代替 continuum lemmas；无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>EXACT HIGH-CARRIER DYADIC PAIR ONLY. NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75v.html">阅读完整笔记</a> · '
        f'<a href="/{RECAP_SLUG}.html">阅读截至 V 的 milestone recap</a>。</p></div>\n'
    )
    anchor = '<section id="references">'
    if anchor not in page:
        raise RuntimeError("literature reference anchor missing")
    page = page.replace(anchor, boundary + anchor, 1)
    write_text(LITERATURE, page)


def route_post_r060_slugs(page: str) -> list[str]:
    start = page.index('<section class="route-overview"')
    end = page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    return ordered[ordered.index("r0-61"):]


def render_recap() -> str:
    slugs = route_post_r060_slugs(HOME.read_text(encoding="utf-8"))
    if len(slugs) != 190 or slugs[0] != "r0-61" or slugs[-1] != "r0-75v":
        raise RuntimeError(f"R0.75V recap route coverage drift: {len(slugs)} {slugs[:1]} {slugs[-1:]}")
    links = "\n".join(f'<a href="/notes/{slug}.html">{slug[3:].upper()}</a>' for slug in slugs)
    nodes = [
        ("B--G", "complete-clock and signed-flux gates", "把 A 的 local dichotomy 接到完整时钟和物理 signed flux。", "B 支付 safe subclock；C--F 排除 packing、positivity 与 naive modal routes；G 固定 exact gain threshold。", "把方法失败当反例；逐模绝对值；忽略 signed cancellation。", "这些步骤整理必要账本，不是任意场 E.24。", "构造能够真正支付 flux 的 exact family。"),
        ("H--L", "one-harmonic transport and diffusion", "在 exact common-shear family 中实现物理 flux gain。", "H 的 ballistic residence、K 的 positive-majorant no-go 与 L 的单实谐波 diffusive k^(-2/3) gain，隔离出 cancellation-compatible route。", "fixed positive adjoint majorant；用 amplitude scaling 制造 gain。", "只覆盖单谐波或诊断性 family。", "推广到 dyadic packet。"),
        ("M--Q", "packet, collar, and concentration", "把单模 gain 推到有限 packet 并连接物理 collar mass。", "M 保留 mode-count-free packet gain；N 校准 radial-collar Wiener row；O--Q 给出 vertical diffusion、entrance concentration 与 spatially spread single-harmonic payments。", "逐 packet cardinality loss；只用 plateau mass 支付任意 multimode flux。", "inter-packet aggregation 与 arbitrary field 仍未闭合。", "压力测试两波 cancellation。"),
        ("R--S", "multimode obstruction and one-wave closure", "识别 plateau-only obstruction 并闭合单谐波完整频率。", "R 给出 multimode concentration obstruction；S 对 exact single harmonic 在所有频率完成 complete-clock payment。", "把单模定理直接推广为 packet theorem。", "S 的 Version-M 结论仍依赖 realized-subclass 与 ledger alignment。", "精确处理一个 two-harmonic dyadic pair。"),
        ("T", "two-wave spatial coercivity", "同一 dyadic pair 的 cubic collar mass 是否保留 cancelling beat defect。", "证明 sharp spatial collar coercivity，以 H^2=(A-C)^2+AC min(1,(d aR)^2+delta_pi^2) 记录两波抵消。", "把两波 cubic mass 拆成两个单波下界。", "只是空间 coercivity，不支付时间 signed flux。", "支付 difference-frequency row。"),
        ("U", "difference-frequency payment", "用 T 的 beat defect 支付 exact flux 的低差频行。", "weighted moving-phase lemma 与 radial quotient 给出 difference row 的 complete-clock payment，所有 R 幂抵消，率为 -2/11907。", "fixed-grid fast-phase quadrature 作为证明。", "two self rows 与 sum row 尚未控制，不能称完整 pair theorem。", "保留三行联合二次抵消并付款。"),
        ("V", "coupled self/sum and full exact pair", "在不破坏 quadratic cancellation 的前提下支付剩余 self/self/sum block。", "multiplier two-jet、exact quadratic identity、逐相位 integration by parts、heat extra term 与 right-endpoint trace 联合证明 V.3；加上 U 得到完整 exact-pair signed flux V.4。", "对三行分别取绝对值；过早 factor common phase；用 finite stress test 代替 continuum lemmas。", "只对 exact diffusive high-carrier dyadic two-harmonic pair；Version-M V.43 仍条件化。", "low carriers、三个及以上 modes、arbitrary packets 与一般 Version-M extraction。"),
    ]
    cards = "\n".join(
        f'''<article class="card node"><p class="eyebrow">{code} / {name}</p><dl><dt>Problem</dt><dd>{problem}</dd><dt>Result</dt><dd>{result}</dd><dt>Rejected</dt><dd>{rejected}</dd><dt>Boundary</dt><dd>{boundary}</dd><dt>Next</dt><dd>{next_step}</dd></dl></article>'''
        for code, name, problem, result, rejected, boundary, next_step in nodes
    )
    return rf'''<!doctype html>
<html lang="zh-CN" data-site-version="{VERSION}"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>R0.61–R0.75V 累计里程碑回顾｜从 clock compression 到 exact-pair signed flux</title>
<meta name="description" content="R0.61 至 R0.75V 的 190 节累计回顾，区分 T 的空间 coercivity、U 的 difference-frequency payment、V 的 coupled self/sum payment 与 exact-pair theorem">
<link rel="canonical" href="https://kasifa.github.io/{RECAP_SLUG}.html"><link rel="stylesheet" href="/bilingual.css">
<script>document.documentElement.classList.add('js')</script><script defer src="/i18n-en.js?v={VERSION}"></script><script defer src="/bilingual.js"></script>
<script>window.MathJax={{tex:{{inlineMath:[["\\(","\\)"]],displayMath:[["\\[","\\]"]]}},options:{{skipHtmlTags:['script','noscript','style','textarea','pre','code']}}}};</script><script defer src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>
<style>:root{{color-scheme:light dark;--paper:#f3ecd8;--raised:#fff8e8;--ink:#26231d;--muted:#625d52;--rule:#8b2f2b;--line:#b8ad97}}@media(prefers-color-scheme:dark){{:root{{--paper:#181714;--raised:#24211c;--ink:#eee5d2;--muted:#b9ad9b;--rule:#df8c6a;--line:#665d52}}}}*{{box-sizing:border-box}}html,body{{max-width:100%;overflow-x:hidden}}body{{margin:0;background:var(--paper);color:var(--ink);font:17px/1.7 Georgia,"Songti SC","Noto Serif SC",serif}}nav{{padding:12px 5vw;border-top:5px solid var(--ink);border-bottom:3px double var(--ink);display:flex;justify-content:space-between;gap:1rem}}main{{width:min(1040px,90vw);margin:auto}}header{{padding:55px 0 30px;border-bottom:1px solid var(--line)}}h1{{font-size:clamp(2rem,5vw,3.7rem);line-height:1.08}}h2{{color:var(--rule);margin-top:2.4rem}}section{{border-bottom:1px dotted var(--line);padding-bottom:1.2rem}}.eyebrow{{font:700 12px/1.5 ui-monospace,SFMono-Regular,monospace;letter-spacing:.06em;text-transform:uppercase}}.grid{{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}}.card,.boundary{{background:var(--raised);border:1px solid var(--line);padding:1rem 1.2rem}}.node dl{{display:grid;grid-template-columns:7rem 1fr;gap:.28rem .7rem;margin:0}}.node dt{{font-weight:700;color:var(--rule)}}.node dd{{margin:0}}.node-links{{display:flex;flex-wrap:wrap;gap:.45rem}}.node-links a{{border:1px solid var(--line);padding:.2rem .45rem;text-decoration:none}}a{{color:var(--rule)}}code{{overflow-wrap:anywhere}}@media(max-width:720px){{body{{font-size:15px}}.grid{{grid-template-columns:1fr}}nav{{font-size:13px}}.node dl{{grid-template-columns:1fr}}}}@media print{{:root{{color-scheme:light;--paper:#fff;--raised:#fff;--ink:#111;--muted:#444;--rule:#7d251f;--line:#999}}nav{{display:none}}body{{font-size:8.5pt}}main{{width:auto}}header{{padding-top:0}}.card{{break-inside:avoid}}}}</style></head>
<body><nav><a href="/research-review.html">研究首页</a><span>R0.61–R0.75V · 2026-09-04</span></nav><main><header><p class="eyebrow">CUMULATIVE MILESTONE RECAP · 190 NODES</p><h1>从 clock compression 到 exact high-carrier pair 的完整 signed flux</h1><p>这是 R0.60 之后的累计里程碑回顾。收录节点：190；回顾截止时公开笔记：250。它保留截至 R0.75A 的既有 recap 字节不变，并把 B–V 二十一节点压缩为一条可审计路线，尤其严格区分 T、U、V 三个连续结论。</p><p><a href="/{RECAP_SLUG}.pdf">下载同步累计回顾 PDF</a> · <a href="/notes/r0-75v.html">阅读 R0.75V Step 47</a> · <a href="/recap-r0-61-r0-75a.html">保留上一版 milestone recap</a></p></header>
<article><section id="retained"><p class="eyebrow">01 / RETAINED THROUGH A</p><h2>早期 clock-compression 路线与 A 的 local dichotomy 继续有效</h2><p>R0.61–R0.75A 的 169 节账本保持为独立、逐字节不变的上一版 recap。B–V 从 A.63 的 complete-clock extraction 缺口出发，经过 signed-flux 路线筛选、单模与 packet 支付、collar 校准、多模 obstruction，最终把精确 two-harmonic high-carrier branch 分解为 T、U、V 三步。</p><ul><li>projected-Lamb 全局与局部压缩，以及 \(\int_0^\infty\Theta_s^2ds\le\frac12\|u\|_4^4\)。</li><li>归一化热体积 \(\mathcal V\in L_t^1\) 的无条件 Leray 能量估计。</li><li>固定 Parseval 框架上的精确 \(2K^2\) 底边迹代价，以及若干量词明确的光滑 NSE 解族和有限 Fourier 符号对。</li></ul></section>
<section id="timeline"><p class="eyebrow">02 / B–V FIVE-FIELD LEDGER</p><h2>Problem / Result / Rejected / Boundary / Next</h2><div class="grid">{cards}</div></section>
<section id="tuv"><p class="eyebrow">03 / T–U–V EXACT DISTINCTION</p><h2>空间 coercivity、difference row 与 coupled self/sum block 不互相替代</h2><div class="grid"><article class="card"><h3>T · spatial coercivity</h3><p>T 只证明同一 high-carrier dyadic pair 的 plateau cubic mass 控制 sharp two-wave beat defect；它没有支付时间 signed flux。</p></article><article class="card"><h3>U · difference-frequency payment</h3><p>U 用 complete-clock weighted moving-phase estimate 支付差频行；self/self/sum 三行仍作为一个未付 coupled block。</p></article><article class="card"><h3>V · coupled self/sum payment</h3><p>V 不逐行取绝对值，而是保留 quadratic cancellation 联合支付剩余 block；只有与 U 合并后，才得到 exact pair 的完整 signed-flux theorem。</p></article></div></section>
<section id="changed"><p class="eyebrow">04 / WHAT CHANGED AT V</p><h2>exact high-carrier dyadic pair 的四频 signed flux 已完整付款</h2><p>对 (A,C\ge0)、(1\le m&lt;k\le2m)、(maR\ge C_0) 的 exact diffusive pair，T、U、V 合并得到</p><p>\[|\mathcal T_{{k,m,R}}|\le Ca^{{2/3}}R^{{-1/3}}(M_{{k,m,R}}^{{\rm plat}})^{{2/3}},\qquad \mathfrak X_{{k,m,R}}\le Ca^{{2/3}}\omega^{{1/3}}(p_{{k,m,R}}^{{\rm plat}})^{{2/3}}.\]</p><p>所有 R 幂抵消，精确 (L^2) 对数率仍为 (-2/11907)。这是 finite-dimensional exact-subfamily theorem，不是任意 two-mode projection 或 arbitrary-field estimate。</p></section>
<section id="open-next"><p class="eyebrow">05 / OPEN BOUNDARY</p><h2>pair closure 之后的边界从 low carriers 与 three-plus modes 开始</h2><p>low-carrier pairs、三个及以上 harmonics、arbitrary dyadic packets、inter-packet aggregation、nonconstant or vertically dependent shear、projection from a larger velocity、arbitrary-field E.24、complete Version-M extraction、fixed deletion、suitable-weak transfer、regularity 与 singularity 仍 OPEN。R0.75W 与后续版本未授权、未读取、未发布。<strong>NOT CLAY.</strong></p></section>
<section id="audit"><p class="eyebrow">06 / AUDIT BOX</p><h2>冻结 commit、证书与发布边界</h2><div class="boundary"><p><strong>Core commit：</strong><code>{frozen_import.SOURCE_COMMIT}</code></p><p><strong>Handoff commit：</strong><code>{frozen_import.HANDOFF_COMMIT}</code></p><p><strong>Handoff SHA-256：</strong><code>{frozen_import.HANDOFF_SHA256}</code></p><p><strong>Main / primary / source SHA-256：</strong><code>{frozen_import.FROZEN['research/r075v_complete_two_harmonic_flux_payment.md']}</code> / <code>{frozen_import.FROZEN['research/r075v_complete_two_harmonic_flux_payment_primary_audit.md']}</code> / <code>{frozen_import.FROZEN['research/r075v_report-source.md']}</code></p><p><strong>Certificate：</strong>Python 17/17；Ruby 18/18；V.1–V.43；3 seeds byte-identical；84 targeted mutations rejected by both implementations。</p><p><strong>Scope：</strong>12/12 frozen files；无正式科学图、simulation、DNS 或 DGX；finite checks 不代替 continuum multiplier-jet 或 endpoint-trace proof。NO NOVELTY CLAIM. NOT CLAY.</p></div></section>
<section id="node-index"><p class="eyebrow">NODE INDEX / 190</p><h2>R0.61–R0.75V 全部节点</h2><div class="node-links">{links}</div></section></article></main></body></html>'''


def update_accounting() -> None:
    html_count = len([item for item in (PUBLIC / "notes").glob("r0-*.html") if " 2" not in item.name])
    pdf_count = len([item for item in (PUBLIC / "notes").glob("r0-*.pdf") if " 2" not in item.name])
    if html_count != 250 or pdf_count not in (206, 207):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 190:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75v.html",
        "latestPublishedResearchPdf": "/notes/r0-75v.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 190,
        "latestRecapRelease": "R0.75V",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-04",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(baseline_text("research/formal-archive-inventory.json"))
    if inventory.get("latestPublishedRelease") == "r075u":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 152
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"][RELEASE] = 47
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "COMPLETE_EXACT_HIGH_CARRIER_TWO_HARMONIC_SIGNED_FLUX_PAYMENT",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "core_parent_commit": frozen_import.CORE_PARENT_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_COMPLETE_EXACT_PAIR_SIGNED_FLUX_THEOREM",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "difference_frequency_component": "PROVED_U4_FROZEN_INPUT",
            "dyadic_pair_condition": "ONE_LE_M_LT_K_LE_2M",
            "high_carrier_condition": "MA_R_GE_C0_REQUIRED",
            "radial_quotient_two_jet": "PROVED_V13_V17",
            "quadratic_cancellation": "PROVED_V21_V25",
            "separate_phase_integration_by_parts": "PROVED_V26_V28",
            "right_endpoint_complete_clock_trace": "PROVED_V31_V36",
            "joint_self_sum_block": "PROVED_V3",
            "complete_exact_pair_signed_flux": "PROVED_V4",
            "normalized_exact_pair_estimate": "PROVED_V6_V7_R_POWERS_CANCEL",
            "exact_l2_rate": "MINUS_2_OVER_11907",
            "exact_smooth_unforced_shear_solution": "PROVED_V42",
            "version_m_same_velocity_inclusion": "CONDITIONAL_V43_SAME_AS_R075S_U",
            "finite_stress_tests": "EXCLUDED_AS_PROOF_OF_CONTINUUM_LEMMAS",
            "weighted_temporal_difference_frequency_estimate": "PROVED_U4",
            "combined_self_and_sum_frequency_block": "PROVED_V3",
            "complete_two_harmonic_signed_flux_payment": "PROVED_V4_EXACT_PAIR_ONLY",
            "low_carrier_pair": "OPEN_NOT_PROVED",
            "three_or_more_harmonics": "OPEN_NOT_PROVED",
            "arbitrary_packets_and_inter_packet_aggregation": "OPEN_NOT_PROVED",
            "projection_from_larger_velocity": "OPEN_NOT_PROVED",
            "nonconstant_shear": "OPEN_NOT_PROVED",
            "vertically_dependent_shear": "OPEN_NOT_PROVED",
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
            "negative_mutations": "PASS_PYTHON_84_OF_84_RUBY_84_OF_84",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_V1_TO_V43_TAGS_43_OF_43_DISPLAYS_43_OF_43",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75v.html",
            "target_pdf": "/notes/r0-75v.pdf",
            "target_primary_figure": None,
            "recap_update_required": True,
            "recap_terminal_release": "R0.75V_STEP47",
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075v_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(baseline_text("research/release-manifest.json"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 47,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 190,
        "postR070APublishedReleaseCount": 152,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075w",
        "latestPublishedResearchHtml": "/notes/r0-75v.html",
        "latestPublishedResearchPdf": "/notes/r0-75v.pdf",
        "latestReleaseGate": "tests/r075v-step47-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075v-step47-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075v-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075v-step47-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075v-step47-pdfs.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075v-step47-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075v-step47-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075v-step47",
            "handoffCommit": frozen_import.HANDOFF_COMMIT,
            "handoffSha256": frozen_import.HANDOFF_SHA256,
            "handoffIndependentAuditSha256": frozen_import.HANDOFF_AUDIT_SHA256,
            "sourceCommit": frozen_import.SOURCE_COMMIT,
            "coreCommit": frozen_import.SOURCE_COMMIT,
            "formalFigureRequired": False,
            "recapRequired": True,
        },
        "latestRecapRelease": "r075v",
        "latestRecapHtml": "/recap-r0-61-r0-75v.html",
        "latestRecapPdf": "/recap-r0-61-r0-75v.pdf",
        "recapPolicy": "MILESTONE_ONLY",
    })
    manifest["formalArchiveInventory"] = {
        "path": "research/formal-archive-inventory.json",
        "sha256": sha256(inventory_target),
    }
    write_json(manifest_target, manifest)


def main() -> None:
    verify_frozen_sources()
    write_text(PUBLIC / "notes/r0-75v.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        write_text(PUBLIC / f"{RECAP_SLUG}.html", render_recap())
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 47,
        "siteVersion": VERSION,
        "recapUpdated": True,
        "recapNodes": 190,
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
