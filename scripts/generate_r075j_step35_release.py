#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Publish frozen R0.75J Step 35 from the verified R0.75I Step 34 baseline."""

from __future__ import annotations

import html
import json
import re
import subprocess
import sys
from pathlib import Path

import generate_r075i_step34_release as previous
import import_r075j_step35_frozen as frozen_import

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
HOME = PUBLIC / "research-review.html"
LITERATURE = PUBLIC / "literature-review.html"
VERSION = "2.14"
RELEASE = "r075j"
CODE = "R0.75J"
TITLE = "R0.75J｜有符号 collar flux 的零均值伴随障碍"
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
            raise RuntimeError(f"R0.75J frozen source drift: {relative}")
    certificate = json.loads(
        (ROOT / "research/r075j_mean_zero_adjoint_flux_obstruction_certificate.json").read_text()
    )
    if (
        certificate.get("verdict") != "PASS"
        or certificate.get("assertions", {}).get("total") != 19
        or certificate.get("assertions", {}).get("passed") != 19
        or len(certificate.get("checks", {})) != 19
    ):
        raise RuntimeError("R0.75J certificate verdict drift")
    main = (ROOT / "research/r075j_mean_zero_adjoint_flux_obstruction.md").read_text()
    for token in (
        r"\mathcal L^*\psi=a",
        r"\psi\text{ changes sign.}",
        r"\mathcal T_{\xi,\eta}(F,b)",
        r"\int\psi_-|\nabla_{23}F|^2",
        r"\frac C2\bigl(E(s)-E(t_2)\bigr)-CD=0",
        r"a\le\mathcal L^*\Phi",
        r"\tag{J.20}",
        "does not by itself improve R0.75F/H",
        "does not rule out every adjoint method",
        "does not construct the paid majorant or close",
        r"\mathbf{NOT\ CLAY}",
    ):
        if token not in main:
            raise RuntimeError(f"R0.75J boundary drift: {token}")


def render_step35_sections() -> str:
    source = (ROOT / "research/r075j_mean_zero_adjoint_flux_obstruction.md").read_text(encoding="utf-8").strip()
    blocks = re.split(r"\n\s*\n", source)
    output: list[str] = []
    section_open = False
    section_index = 278
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
        elif len(lines) >= 2 and lines[0].startswith("|") and re.match(r"^\|[-:| ]+\|$", lines[1]):
            rows = [[cell.strip() for cell in line.strip().strip("|").split("|")] for line in lines]
            head = "".join(f"<th>{inline_markup(cell)}</th>" for cell in rows[0])
            body = "".join("<tr>" + "".join(f"<td>{inline_markup(cell)}</td>" for cell in row) + "</tr>" for row in rows[2:])
            output.append(f'<div class="table-wrap"><table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div>')
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
    if section_index != 285:
        raise RuntimeError(f"Step 35 reader section drift: {section_index}")
    return "\n".join(output)


def render_note() -> str:
    page = previous.render_note()
    page = replace_once(page, 'data-site-version="2.13"', 'data-site-version="2.14"', "note version")
    page = replace_once(page, "/i18n-en.js?v=2.13", "/i18n-en.js?v=2.14", "note i18n")
    page = replace_pattern(
        page,
        r'<title>.*?</title><meta name="description" content=".*?">',
        f'<title>{TITLE}</title><meta name="description" content="The exact zero-terminal adjoint of the signed mean-zero collar source must change sign; a paid nonnegative majorant remains open">',
        "note metadata",
    )
    page = replace_pattern(
        page,
        r'<link rel="canonical" href="https://kasifa\.github\.io/notes/r0-[^"]+\.html">',
        '<link rel="canonical" href="https://kasifa.github.io/notes/r0-75j.html">',
        "note canonical URL",
    )
    hero = rf'''<body><nav class="top"><a href="/research-review.html">研究首页</a><span>R0.75J · STEP 35 · 2026-09-03</span></nav><main><header class="hero"><div class="hero-inner"><div><div class="section-no">研究笔记 R0.75J · Step 35 · MEAN-ZERO ADJOINT OBSTRUCTION</div><h1>{TITLE}</h1><p>物理有符号源 <strong>a=eta_R b partial_2 xi</strong> 在每个固定参数切片上零均值，因此其 exact zero-terminal adjoint 若非零就必然变号。精确对偶把负权重转化为不利的正加权耗散；常数平移在完整恒等式中恰好抵消，丢弃有利耗散则支付全局 surcharge <strong>CD</strong>。<strong>PAID POSITIVE MAJORANT OPEN. E.24 OPEN. NOT A BLANKET NO-GO. NOT CLAY.</strong></p><div class="labels"><span class="label">MEAN-ZERO SOURCE</span><span class="label">EXACT ADJOINT SIGN-CHANGING</span><span class="label">DUALITY EXACT</span><span class="label">NEGATIVE WEIGHTED DISSIPATION</span><span class="label">CONSTANT SHIFT CANCELED</span><span class="label">SURCHARGE CD</span><span class="label">POSITIVE MAJORANT VIABLE</span><span class="label">INITIAL ROW UNPAID</span><span class="label">NOT BLANKET NO-GO</span><span class="label">E.24 OPEN</span><span class="label">NO FIGURE / NO DNS</span><span class="label">NO NOVELTY CLAIM</span><span class="label">NOT CLAY</span></div></div><div class="stamp"><strong>状态 · R0.75J STEP 35</strong><p>source mean zero：PROVED</p><p>exact adjoint sign change：PROVED</p><p>duality signs：PROVED</p><p>constant shift：CANCELED</p><p>dropped-row surcharge：CD</p><p>positive majorant：VIABLE</p><p>majorant payment：OPEN</p><p>formal figure：NOT APPLICABLE</p></div></div></header><article>'''
    page = replace_pattern(page, r'<body><nav class="top">[\s\S]*?</header><article>', hero, "note hero")
    page = replace_once(page, '<section id="reproduce">', render_step35_sections() + '\n<section id="reproduce">', "Step 35 sections")
    evidence = '''<section id="reproduce"><div class="section-no">R / 冻结证据</div><h2>Step 35 主文、primary-source boundary、双实现证书与 fail-closed QA</h2><p class="files"><a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075j_mean_zero_adjoint_flux_obstruction.md">Step 35 主文</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075j_mean_zero_adjoint_flux_obstruction_primary_audit.md">primary audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075j_report-source.md">primary-source boundary</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075j_mean_zero_adjoint_flux_obstruction_fixtures.json">fixtures JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075j_mean_zero_adjoint_flux_obstruction_expected.json">expected JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075j_mean_zero_adjoint_flux_obstruction_certificate.json">certificate JSON</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075j_mean_zero_adjoint_flux_obstruction_certificate_report.md">Python report</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075j_mean_zero_adjoint_flux_obstruction_independent_audit.md">Ruby independent audit</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/research/r075j_mean_zero_adjoint_flux_obstruction_qa_report.md">certificate QA</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate.py">Python script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075j_mean_zero_adjoint_flux_obstruction_certificate_independent.rb">Ruby script</a> · <a href="https://github.com/Kasifa/Kasifa.github.io/blob/main/scripts/r075j_mean_zero_adjoint_flux_obstruction_qa.sh">QA script</a></p><p><a href="/notes/r0-75j.pdf">同步 reader PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（截止 R0.75A）</a> · <a href="/recap-r0-61-r0-75a.pdf">上一大里程碑 recap PDF</a></p><p class="note">Certificate：Python 19/19、Ruby 24/24、J.1--J.20 与 20/20 displays，3 个 Python hash seeds 及完整 regeneration 字节稳定；两套实现分别拒绝 84/84 定向 mutations，unknown mutations 均 fail closed。完整冻结 ledger 为 12/12。本节无正式图、simulation、numerical fit、DNS 或 DGX。</p></section>'''
    page = replace_pattern(page, r'<section id="reproduce">[\s\S]*?</section>', evidence, "Step 35 evidence")
    adjacent = '''<section id="adjacent"><div class="section-no">NAV / 相邻研究节点</div><h2>上一冻结步骤与后续边界</h2><p><a href="#s-272">← Step 34：diffusion-safe block participation</a> · <a href="#next">后续工作未授权、未读取 →</a></p></section>'''
    page = replace_pattern(page, r'<section id="adjacent">[\s\S]*?</section>', adjacent, "Step 35 adjacent")
    next_section = '''<section id="next"><div class="section-no">NEXT / 后续未授权、未读取</div><h2 style="margin:.35rem 0 .15rem;font-size:1.15rem">可支付的正 majorant 仍为 OPEN</h2><p style="margin:.15rem 0">本站在 R0.75J Step 35 停止。exact signed-source adjoint 被零均值迫使变号；常数正移不会增加 exact 信息，丢弃耗散则产生 CD surcharge。仍需独立构造并支付 nonnegative majorant 的 initial occupation/source row，且处理 transition、periodic recrossing、E.24、complete clock、fixed deletion、suitable-weak transfer、regularity 与 singularity。后续工作未授权、未读取、未公开。</p></section>'''
    return replace_pattern(page, r'<section id="next">[\s\S]*?</section>', next_section, "Step 35 next")


def update_home() -> None:
    page = HOME.read_text(encoding="utf-8")
    page = re.sub(r'\s*<div class="task-one" id="r075j"[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.13"' in page:
        for old, new, label in (
            ('data-site-version="2.13"', 'data-site-version="2.14"', "home version"),
            ("/i18n-en.js?v=2.13", "/i18n-en.js?v=2.14", "home i18n"),
            ("/site-refresh.js?v=2.13.1", "/site-refresh.js?v=2.14.1", "home refresh"),
            ("<strong>v2.13</strong>网页版本", "<strong>v2.14</strong>网页版本", "home stat version"),
            ("<strong>R0.75I</strong>最新研究节点", "<strong>R0.75J</strong>最新研究节点", "home latest"),
            ("<strong>237</strong>公开研究笔记", "<strong>238</strong>公开研究笔记", "home public count"),
            ("展开 147 篇公开笔记", "展开 148 篇公开笔记", "home route count"),
            ("综述 v2.13 · 2026-09-03", "综述 v2.14 · 2026-09-03", "home footer"),
            ("Research topology · R0.1–R0.75I", "Research topology · R0.1–R0.75J", "home topology"),
            ('href="#r075i">跳到首页 R0.75I 卡片 →', 'href="#r075j">跳到首页 R0.75J 卡片 →', "home jump"),
            ("R0.70A–R0.75I：139 节已公开，104 节完整封存", "R0.70A–R0.75J：140 节已公开，104 节完整封存", "home accounting"),
            ('<span class="route-range">R0.69P–R0.75I</span>', '<span class="route-range">R0.69P–R0.75J</span>', "home range"),
            ("<h3>R0.75I：diffusion-safe block estimate 与 exact participation threshold</h3>", "<h3>R0.75J：mean-zero signed adjoint obstruction 与 paid majorant gate</h3>", "home route title"),
            ("R0.72R–R0.75I：</span>", "R0.72R–R0.75J：</span>", "home detail range"),
            ('aria-label="R0.69P–R0.75I"', 'aria-label="R0.69P–R0.75J"', "home links label"),
            ("全站现有 237 篇公开研究笔记", "全站现有 238 篇公开研究笔记", "home recap count"),
        ):
            page = replace_once(page, old, new, label)
        page = replace_pattern(
            page,
            r'<div class="summary-item"><strong>我目前关注</strong><span>.*?</span></div>',
            '<div class="summary-item"><strong>我目前关注</strong><span>R0.75J Step 35 证明 physical signed collar source 的 exact zero-terminal adjoint 因切片零均值而被迫变号；常数正移在 exact identity 中抵消，若丢弃耗散则付出 CD。后续有效路线是可支付 initial row 的 nonnegative majorant。</span></div>',
            "home focus",
        )
        latest = f'''<section class="route-overview latest-release-spotlight" id="latest-release" aria-labelledby="latest-release-title"><div class="route-overview-inner"><header class="route-map-header"><div><p class="eyebrow">LATEST RELEASE · R0.75J · 2026-09-03 · STEP 35 · MEAN-ZERO ADJOINT OBSTRUCTION</p><h2 class="route-map-title" id="latest-release-title">{TITLE}</h2><p class="route-map-intro">signed derivative source 在每个固定参数切片上零均值，迫使 exact zero-terminal adjoint 非零时变号；对偶式中的负权重带来不利正耗散。常数 positivity shift 在 exact identity 中完全抵消，drop 后则付 CD。可行替代是 nonnegative majorant，但其 initial occupation/source row 尚未支付。NO NOVELTY CLAIM. NOT CLAY.</p></div><nav class="route-map-actions" aria-label="最新发布快捷入口"><a class="route-map-latest" href="/notes/r0-75j.pdf">阅读最新 R0.75J 研究笔记 →</a><a href="/recap-r0-61-r0-75a.html">上一大里程碑累计回顾（R0.61–R0.75A，169 节）</a><a href="/notes/">238 篇研究笔记总索引</a><a href="#r075j">查看首页 R0.75J 卡片</a></nav></header><div class="route-legend" aria-label="最新发布计数"><span><i class="route-legend-mark kept" aria-hidden="true"></i>R0.70A–R0.75J · 140 节已公开</span><span><i class="route-legend-mark kept" aria-hidden="true"></i>104 节完整封存</span><span><i class="route-legend-mark current" aria-hidden="true"></i>当前端点 R0.75J Step 35 mean-zero adjoint obstruction</span></div></div></section>'''
        page = replace_pattern(page, r'<section class="route-overview latest-release-spotlight" id="latest-release"[\s\S]*?</section>', latest, "home spotlight")
        page = replace_pattern(
            page,
            r'<p class="tree-current-summary">.*?</p>',
            '<p class="tree-current-summary">Step 35 proves that the exact zero-terminal adjoint of the physical mean-zero signed source must change sign unless trivial. Constant shifts cancel exactly or cost CD after dropping dissipation; a paid nonnegative majorant remains open.</p>',
            "home current summary",
        )
        page = replace_once(
            page,
            'pure-transport terminal tube → diffusion-safe block estimate / exact participation threshold / multi-block dynamics open</p>',
            'diffusion-safe one-block estimate → mean-zero adjoint obstruction / paid positive majorant open</p>',
            "home route path",
        )
        page = replace_once(
            page,
            '<a class="milestone" href="/notes/r0-75i.html">R0.75I</a>',
            '<a class="milestone" href="/notes/r0-75i.html">R0.75I</a>\n<a class="milestone" href="/notes/r0-75j.html">R0.75J</a>',
            "home milestone",
        )
    elif 'data-site-version="2.14"' not in page:
        raise RuntimeError("home baseline version drift")
    next_card = '''<div class="tree-row"><article class="tree-node next"><div class="tree-node-head"><span class="route-range">NEXT · NOT AUTHORIZED</span><span class="tree-state current">OPEN</span></div><h3>a paid nonnegative majorant remains unproved</h3><p>必须构造满足 a&lt;=L*Phi、Phi&gt;=0、Phi(t2)&gt;=0 的 majorant，并以 frozen Version-M atoms 独立支付其 initial occupation/source row 及 transition/periodic geometry；后续工作未授权、未读取、未公开。</p></article></div>'''
    page = replace_pattern(page, r'<div class="tree-row"><article class="tree-node next">[\s\S]*?</article></div>', next_card, "home next")
    card = f'''          <div class="task-one" id="r075j" data-release="r075j" style="margin-top:2rem"><p class="eyebrow">研究笔记 R0.75J Step 35 · 2026-09-03 · MEAN-ZERO ADJOINT OBSTRUCTION</p><h3>{TITLE}</h3><p>exact signed-source adjoint 因切片零均值而被迫变号；精确对偶重现不利加权耗散，constant shift 要么抵消、要么产生 CD surcharge。positive majorant route 仍可行，但 initial row 未支付。无正式图、simulation、DNS 或 DGX。NO NOVELTY CLAIM. NOT CLAY.</p><p><a href="/notes/r0-75j.html"><strong>阅读完整中文笔记 →</strong></a> · <a href="/notes/r0-75j.pdf">PDF</a> · <a href="/recap-r0-61-r0-75a.html">上一大里程碑 recap（截止 A）</a></p></div>\n'''
    anchor = '<div class="task-one" id="r075i"'
    if anchor not in page:
        raise RuntimeError("home R0.75I card anchor missing")
    page = page.replace(anchor, card + anchor, 1)
    write_text(HOME, page)


def update_literature() -> None:
    page = LITERATURE.read_text(encoding="utf-8")
    page = re.sub(r'\s*<h3 id="r075j-boundary">[\s\S]*?<div class="boundary">[\s\S]*?</div>\s*', "\n", page)
    if 'data-site-version="2.13"' in page:
        for old, new, label in (
            ('data-site-version="2.13"', 'data-site-version="2.14"', "literature version"),
            ("/i18n-en.js?v=2.13", "/i18n-en.js?v=2.14", "literature i18n"),
            ("文献综述 v2.13 · 2026-09-03", "文献综述 v2.14 · 2026-09-03", "literature footer"),
            ("本站 R0.69P–R0.75I 只列为研究笔记", "本站 R0.69P–R0.75J 只列为研究笔记", "literature intro"),
        ):
            page = replace_once(page, old, new, label)
        old_next = '<div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>multi-block participation or signed cancellation remains open</strong></header><p>必须独立控制实际 diffusing field 的 N_eff，或证明足够强的 signed inter-block cancellation；单区块估计本身不能闭合 E.24。后续材料未授权、未读取、未公开。</p></div>'
        route = '<div class="route-step kept"><header><b>R0.75J</b><strong>mean-zero signed adjoint obstruction</strong></header><p>Step 35 证明 physical derivative source 的 exact zero-terminal adjoint 非平凡时必然变号；dual identity 把负权重变成不利正耗散，constant shift 在完整恒等式中抵消，drop 后则支付 CD。<a href="/notes/r0-75j.html">研究笔记</a> <a href="#r075j-boundary">文献与主张边界</a></p></div><div class="route-step pause"><header><b>开放接口 · 后续未授权</b><strong>a paid nonnegative majorant remains open</strong></header><p>必须构造并支付满足 a&lt;=L*Phi 的 nonnegative majorant，尤其是 frozen Version-M atoms 下的 initial occupation/source row 及 transition/periodic geometry；后续材料未授权、未读取、未公开。</p></div>'
        page = replace_once(page, old_next, route, "literature route")
    elif 'data-site-version="2.14"' not in page:
        raise RuntimeError("literature baseline version drift")
    boundary = (
        '<h3 id="r075j-boundary">R0.75J Step 35 的 bounded primary-source screen 与主张边界</h3>'
        '<p>Albritton--Dong 的 passive-scalar work 标识 bounded-total-speed drift 的特殊边界；'
        'Gardner--Liss--Mattingly 的 pathwise shear-diffusion work 说明 stochastic representation 可携带超出形式能量恒等式的信息；'
        'Hu--Li 的 Davies weighted-semigroup 方法支持 off-diagonal heat-kernel 思路；'
        '没有一个 inspected source 给出 J.20 所需的 Version-M positive-majorant initial-row payment 或 E.24。'
        '有限 non-hit 不构成 literature completeness、novelty、priority、nonexistence、correctness 或 publishability 判断。</p>'
        '<div class="boundary"><strong>R0.75J Step 35 公开边界</strong><p>'
        'PROVED：physical source 的切片零均值 J.7、exact zero-terminal adjoint 的零均值与 forced sign change J.8--J.9、duality 与不利耗散 J.12--J.13、constant-shift cancellation 及 CD surcharge J.14--J.18、sufficient positive-majorant architecture J.19--J.20。'
        'NOT A BLANKET NO-GO：nonnegative majorant 仍是可行架构，但其 initial occupation/source row 尚未由 frozen Version-M atoms 支付；以 a_+ 替代 a 会改变 signed source。'
        'OPEN：paid positive majorant、transition bands、periodic recrossing、E.24、complete clock、fixed deletion、suitable-weak transfer、'
        'regularity 与 singularity。无 formal figure、simulation、numerical fit、DNS 或 DGX。'
        '<strong>NO NOVELTY CLAIM. NOT CLAY.</strong> <a href="/notes/r0-75j.html">阅读完整笔记</a> · '
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
    if html_count != 238 or pdf_count not in (194, 195):
        raise RuntimeError(f"public note count drift: {(html_count, pdf_count)}")
    route_page = HOME.read_text(encoding="utf-8")
    start = route_page.index('<section class="route-overview"')
    end = route_page.index('<div class="page-shell">', start)
    ordered: list[str] = []
    for slug in re.findall(r'href="/notes/(r0-[^"]+)\.html"', route_page[start:end]):
        if slug not in ordered:
            ordered.append(slug)
    post_r060 = len(ordered[ordered.index("r0-61"):])
    if post_r060 != 178:
        raise RuntimeError(f"post-R0.60 route count drift: {post_r060}")
    write_text(ROOT / "VERSION", VERSION + "\n")
    write_json(PUBLIC / "site-version.json", {
        "schemaVersion": "research-site-version-v1",
        "version": VERSION,
        "latestRelease": CODE,
        "latestPublishedResearchHtml": "/notes/r0-75j.html",
        "latestPublishedResearchPdf": "/notes/r0-75j.pdf",
        "publicHtmlNoteCount": html_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "latestRecapRelease": "R0.75A",
        "publicPdfNoteCount": pdf_count,
        "publishedDate": "2026-09-03",
    })
    inventory_target = ROOT / "research/formal-archive-inventory.json"
    inventory = json.loads(inventory_target.read_text(encoding="utf-8"))
    if inventory.get("latestPublishedRelease") == "r075i":
        inventory["latestPublishedRelease"] = RELEASE
        inventory["publishedReleases"].append(RELEASE)
        inventory["formalFigureExemptReleases"].append(RELEASE)
    if inventory.get("latestPublishedRelease") != RELEASE:
        raise RuntimeError("formal inventory latest release drift")
    if inventory["publishedReleases"].count(RELEASE) != 1 or inventory["formalFigureExemptReleases"].count(RELEASE) != 1:
        raise RuntimeError("formal inventory duplicate release")
    inventory["publishedReleaseCount"] = 140
    inventory["formalSealedReleaseCount"] = 104
    inventory["formalFigureExemptReleaseCount"] = len(inventory["formalFigureExemptReleases"])
    inventory["sameReleaseCompletedSteps"] = {
        "r074s": 18, "r074t": 19, "r074u": 20, "r074v": 21, "r074w": 22,
        "r074x": 23, "r074y": 24, "r074z": 25, "r075a": 26, "r075b": 27,
        "r075c": 28, "r075d": 29, "r075e": 30, "r075f": 31, "r075g": 32,
        "r075h": 33, "r075i": 34, "r075j": 35,
    }
    write_json(inventory_target, inventory)
    freeze = {
        "schema_version": 1,
        "research_version": CODE,
        "scope": "MEAN_ZERO_ADJOINT_OBSTRUCTION_FOR_SIGNED_COLLAR_FLUX",
        "source_commit": frozen_import.SOURCE_COMMIT,
        "handoff_commit": frozen_import.HANDOFF_COMMIT,
        "handoff_sha256": frozen_import.HANDOFF_SHA256,
        "handoff_independent_audit_sha256": frozen_import.HANDOFF_AUDIT_SHA256,
        "frozen_file_count": 12,
        "claim_status": {
            "publication_kind": "AUDITED_ANALYTIC_MEAN_ZERO_ADJOINT_OBSTRUCTION",
            "formal_figure": "NOT_USED_ANALYTIC_RELEASE_NO_SIMULATION",
            "simulation_or_dns": "NOT_USED",
            "dgx": "NOT_USED",
            "literature_completeness_novelty_priority_publishability": "NOT_CLAIMED",
            "physical_signed_source_mean_zero": "PROVED_J7_EVERY_FIXED_PARAMETER_SLICE",
            "exact_zero_terminal_adjoint": "FORCED_SIGN_CHANGE_UNLESS_SOURCE_ZERO_J8_J9",
            "exact_duality": "PROVED_J12_J13_NEGATIVE_WEIGHTED_DISSIPATION_REAPPEARS",
            "constant_shift": "EXACTLY_CANCELED_J14_J17",
            "dropped_dissipation_surcharge": "EXACTLY_CD_J18_GLOBAL_ENERGY_DROP",
            "positive_majorant_architecture": "SUFFICIENT_J19_J20",
            "positive_part_replacement": "CHANGES_PHYSICAL_SIGNED_SOURCE",
            "positive_majorant_initial_row": "OPEN_NOT_PAID",
            "blanket_no_go_for_adjoint_resolvent_or_feynman_kac": "NOT_CLAIMED",
            "transition_bands_and_periodic_recrossing": "OPEN_NOT_PROVED",
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
            "python_certificate": "PASS_19_OF_19",
            "independent_ruby": "PASS_24_OF_24",
            "negative_mutations": "PASS_PYTHON_84_OF_84_RUBY_84_OF_84",
            "unknown_mutations": "FAIL_CLOSED_BOTH_IMPLEMENTATIONS",
            "python_hash_seeds": "PASS_3_OF_3_BYTE_STABLE",
            "equation_tags_and_displays": "PASS_J1_TO_J20_20_OF_20",
            "formal_figure_or_simulation_package": "NOT_APPLICABLE",
        },
        "publication_handoff": {
            "owner_task_id": "01a06480-0532-7fd0-bdf0-57571465a2d4",
            "target": "https://kasifa.github.io/",
            "target_html": "/notes/r0-75j.html",
            "target_pdf": "/notes/r0-75j.pdf",
            "target_primary_figure": None,
            "recap_update_required": False,
            "status": "READY_FOR_SINGLE_LONG_LIVED_PUBLICATION_TASK",
        },
    }
    write_json(ROOT / "research/r075j_freeze_manifest.json", freeze)
    manifest_target = ROOT / "research/release-manifest.json"
    manifest = json.loads(manifest_target.read_text(encoding="utf-8"))
    manifest.update({
        "latestCompletedRelease": RELEASE,
        "latestCompletedStep": 35,
        "siteVersion": VERSION,
        "publicHtmlNoteCount": html_count,
        "publicPdfNoteCount": pdf_count,
        "postR060PublishedNodeCount": post_r060,
        "postR060RecapNodeCount": 169,
        "postR070APublishedReleaseCount": 140,
        "postR070AFormalSealedReleaseCount": 104,
        "formalFigureExemptReleaseCount": inventory["formalFigureExemptReleaseCount"],
        "nextRelease": "r075k",
        "latestPublishedResearchHtml": "/notes/r0-75j.html",
        "latestPublishedResearchPdf": "/notes/r0-75j.pdf",
        "latestReleaseGate": "tests/r075j-step35-gate.test.mjs",
        "latestReleasePublicationTest": "tests/r075j-step35-release.test.mjs",
        "latestReleaseTranslationScript": "scripts/add-r075j-translations.mjs",
        "latestReleaseStepTranslationScript": "scripts/add-r075j-step35-translations.mjs",
        "latestReleasePdfBinder": "scripts/bind-r075j-step35-pdf.mjs",
        "latestReleaseBrowserQaScript": "scripts/qa-r075j-step35-browser.mjs",
        "latestReleaseOnlineVerifierScript": "scripts/verify-r075j-step35-online.mjs",
        "latestPublicationIdentity": {
            "releaseId": "r075j-step35",
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
    write_text(PUBLIC / "notes/r0-75j.html", render_note())
    if "--note-only" not in sys.argv:
        update_home()
        update_literature()
        update_accounting()
        subprocess.run([sys.executable, "scripts/generate_note_index.py"], cwd=ROOT, check=True)
    verify_frozen_sources()
    print(json.dumps({
        "status": "generated",
        "latestRelease": CODE,
        "latestCompletedStep": 35,
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
